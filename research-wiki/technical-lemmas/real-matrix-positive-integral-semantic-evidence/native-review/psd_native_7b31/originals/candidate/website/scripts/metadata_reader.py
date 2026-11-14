"""Fail-closed, syntax-only exposition of an audited metadata snapshot.

No filesystem, process, network, Lean, eval, or expression interpreter is used.
The caller provides the trusted audit/manifest and existing SourceDeclarations.
Only literal contents are decoded. Concatenations and references remain syntax
nodes; they are never computed or expanded. No output is proof/DAG evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import html
import json
from pathlib import PurePosixPath
import re
from typing import Any, Mapping, Sequence
from urllib.parse import quote


BOUNDARY = (
    "This Lean definition constructs provenance or workflow data. It does not "
    "prove the mathematical statements stored as text. Status labels, named "
    "dependencies and citations are data, not compilation, proof or source certificates."
)


class Rejected(ValueError):
    """A bounded, non-source-bearing error safe to show as an unresolved reason."""


def digest(raw: bytes) -> str:
    """UTF-8 LF-canonical snapshot: only CRLF/LF checkout variation is ignored.

    No whitespace stripping, source rewriting or decoded String normalization
    is performed. Every other byte change still requires an independent audit.
    """
    return hashlib.sha256(raw.decode('utf-8').replace('\r\n', '\n').encode('utf-8')).hexdigest()


def _relative(path: str) -> str:
    if not isinstance(path, str) or "\\" in path or ":" in path:
        raise Rejected("source path is not a repository-relative path")
    p = PurePosixPath(path)
    if p.is_absolute() or ".." in p.parts or str(p) != path:
        raise Rejected("source path is not a repository-relative path")
    return path


def _get(obj: Any, key: str) -> Any:
    return obj[key] if isinstance(obj, Mapping) else getattr(obj, key)


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    start: int
    end: int
    line: int


IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*")


def tokenize(source: str) -> list[Token]:
    """Small data grammar lexer: strings and arbitrarily nested comments matter."""
    out: list[Token] = []
    i, line = 0, 1
    while i < len(source):
        start, at_line = i, line
        if source[i].isspace():
            line += source[i] == "\n"
            i += 1
        elif source.startswith("--", i):
            i = source.find("\n", i)
            if i < 0:
                break
        elif source.startswith("/-", i):
            i, depth = i + 2, 1
            while depth and i < len(source):
                if source.startswith("/-", i):
                    depth, i = depth + 1, i + 2
                elif source.startswith("-/", i):
                    depth, i = depth - 1, i + 2
                else:
                    line += source[i] == "\n"
                    i += 1
            if depth:
                raise Rejected("unterminated block comment")
        elif source[i] == '"':
            i += 1
            while i < len(source) and source[i] != '"':
                if source[i] == "\\":
                    i += 2
                else:
                    i += 1
            if i >= len(source):
                raise Rejected("unterminated String literal")
            i += 1
            raw = source[start:i]
            line += raw.count("\n")
            out.append(Token("string", raw, start, i, at_line))
        else:
            match = IDENT.match(source, i)
            if match:
                i = match.end()
                kind = "identifier"
            else:
                kind = "symbol"
                i += 2 if source[i:i + 2] in {":=", "++", "=>"} else 1
            out.append(Token(kind, source[start:i], start, i, at_line))
    return out


def literal(token: Token) -> str:
    """Decode only the explicitly supported Lean String escape alphabet."""
    text, out, i = token.text[1:-1], [], 0
    escapes = {'"': '"', "\\": "\\", "n": "\n", "r": "\r", "t": "\t"}
    while i < len(text):
        if text[i] != "\\":
            out.append(text[i])
            i += 1
        else:
            if i + 1 == len(text) or text[i + 1] not in escapes:
                raise Rejected("unsupported String escape")
            out.append(escapes[text[i + 1]])
            i += 2
    return "".join(out)


# A syntactic ++ suffix is not a standalone absolute location. Actual paths
# embedded in a longer note, including Windows, UNC and file URLs, are rejected.
MACHINE_PATH = re.compile(
    r"(?:[A-Za-z]:[\\/]|\\\\[A-Za-z0-9]|file://|(?<!\w)~[\\/]|"
    r"(?<![\w:])/(?:home|Users|mnt|tmp|var|root|opt|srv|etc|private)/|"
    r"(?:^|[\s\"'(<])/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)"
)
ABSOLUTE_FRAGMENT = re.compile(r"(?:^|[\s\"'(])/[A-Za-z][A-Za-z0-9_.-]*(?:/[A-Za-z0-9_.-]+)*(?=$|[\s\"'>),;])")


def source_is_safe(source: str, tokens: list[Token]) -> bool:
    if MACHINE_PATH.search(source):
        return False
    nonliteral_source = list(source)
    for i, token in enumerate(tokens):
        if token.kind != "string":
            continue
        nonliteral_source[token.start:token.end] = " " * (token.end - token.start)
        value = literal(token)
        if MACHINE_PATH.search(value):
            return False
        suffix = value.startswith("/") and i and tokens[i - 1].text == "++"
        if ABSOLUTE_FRAGMENT.search(value) and not suffix:
            return False
    return not ABSOLUTE_FRAGMENT.search("".join(nonliteral_source))


class DataParser:
    """Recognize a typed construction tree; never execute its expressions."""
    def __init__(self, tokens: list[Token], owner: "MetadataReader"):
        self.tokens, self.owner, self.pos, self.depth = tokens, owner, 0, 0

    def peek(self, text: str | None = None) -> bool:
        return self.pos < len(self.tokens) and (text is None or self.tokens[self.pos].text == text)

    def take(self, text: str | None = None) -> Token:
        if not self.peek(text):
            raise Rejected("unsupported or incomplete data expression")
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def expression(self, expected: str) -> dict:
        self.depth += 1
        if self.depth > 80:
            raise Rejected("construction nesting limit exceeded")
        try:
            node = self.atom(expected)
            while self.peek("++"):
                if expected != "String" and not expected.startswith("List "):
                    raise Rejected("concatenation is supported only for String and List data")
                self.take("++")
                node = {"kind": "concat", "type": expected,
                        "parts": [node, self.atom(expected)], "evaluated": False}
            return node
        finally:
            self.depth -= 1

    def atom(self, expected: str) -> dict:
        if self.peek("("):
            self.take("(")
            node = self.expression(expected)
            self.take(")")
            return node
        if self.peek("{"):
            self.take("{")
            return self.record(expected, closing="}")
        if self.peek("["):
            if not expected.startswith("List "):
                raise Rejected("List literal does not match the audited field type")
            self.take("[")
            items = []
            while not self.peek("]"):
                items.append(self.expression(expected[5:]))
                if not self.peek(","):
                    break
                self.take(",")
            self.take("]")
            return {"kind": "list", "type": expected, "items": items}
        token = self.take()
        if token.kind == "string":
            if expected != "String":
                raise Rejected("String literal does not match the audited field type")
            return {"kind": "string", "type": "String", "text": literal(token)}
        word = token.text
        if word in {"localTexAnchor", "AutoSamplingTheory.localTexAnchor"}:
            if expected != "AutoSamplingTheory.SourceAnchor":
                raise Rejected("localTexAnchor result does not match the audited field type")
            args = [self.atom("String") for _ in range(4)]
            values = dict(zip(["key", "pathOrUrl", "label", "note"], args))
            values["kind"] = {"kind": "enum", "type": "AutoSamplingTheory.SourceKind", "label": "localTex"}
            return self.record_values(expected, values, helper="localTexAnchor")
        if expected in self.owner.enums:
            if word == ".":
                word += self.take().text
            permitted = {f".{v}": v for v in self.owner.enums[expected]}
            for v in self.owner.enums[expected]:
                permitted[f"{expected}.{v}"] = v
                permitted[f"{expected.rsplit('.', 1)[-1]}.{v}"] = v
            if word not in permitted:
                raise Rejected("unknown audited enum constructor")
            return {"kind": "enum", "type": expected, "label": permitted[word]}
        reference = self.owner.references.get(word)
        if reference and reference[1] == expected:
            return {"kind": "reference", "type": expected, "declaration": reference[0],
                    "expanded": False, "dependency_evidence": False}
        raise Rejected("unsupported expression or unaudited data reference")

    def record(self, expected: str, closing: str | None = None) -> dict:
        schema = self.owner.schemas.get(expected)
        if schema is None:
            raise Rejected("record literal does not match an audited data schema")
        fields = {f["name"]: f for f in schema}
        values = {}
        while self.peek() and not (closing and self.peek(closing)):
            name = self.take().text
            if name not in fields or name in values:
                raise Rejected("unknown or duplicate record field")
            self.take(":=")
            values[name] = self.expression(fields[name]["type"])
            if self.peek(","):
                self.take(",")
            elif self.peek() and not (closing and self.peek(closing)):
                previous = self.tokens[self.pos - 1]
                if self.tokens[self.pos].line <= previous.line:
                    raise Rejected("record fields need a comma or a new line")
        if closing:
            self.take(closing)
        return self.record_values(expected, values)

    def record_values(self, expected: str, values: dict, helper: str | None = None) -> dict:
        fields = []
        for field in self.owner.schemas[expected]:
            name = field["name"]
            origin = "explicit" if name in values else "schema-default"
            if helper and name in values:
                origin = "helper-fixed" if name == "kind" else "helper-argument"
            if name in values:
                value = values[name]
            else:
                if field["default"] is None:
                    raise Rejected("required record field is missing")
                default_parser = DataParser(tokenize(field["default"]), self.owner)
                value = default_parser.expression(field["type"])
                default_parser.finish()
            fields.append({"name": name, "type": field["type"], "origin": origin,
                           "meaning": self.owner.field_meaning(expected, name, field["type"]),
                           "value": value})
        return {"kind": "record", "type": expected, "fields": fields, "helper": helper}

    def finish(self) -> None:
        if self.peek():
            raise Rejected("unsupported trailing expression or declaration context")


class MetadataReader:
    """Use manifest + exact audit bytes + exact module bytes + caller's inventory.

    declarations may be ASTIS SourceDeclaration objects or equivalent dicts.
    Required fields: full_name, kind, source_file, source_line, source_text.
    The inventory must contain every admitted name exactly once. Extra unrelated
    declarations are ignored; they cannot become admitted through a name pattern.
    """
    def __init__(self, manifest: Mapping, audit_bytes: bytes,
                 source_bytes: Mapping[str, bytes], declarations: Sequence[Any]):
        if manifest.get('digest_mode') != 'utf8-lf-v1':
            raise Rejected('unknown snapshot digest mode')
        if manifest.get("schema_version") != 1 or digest(audit_bytes) != manifest["audit_sha256"]:
            raise Rejected("audit manifest drift; independent re-audit required")
        self.audit = json.loads(audit_bytes)
        self.manifest = manifest
        self.sources = {}
        self.line_offsets = {}
        for path, required_hash in manifest["source_sha256"].items():
            path = _relative(path)
            if path not in source_bytes or digest(source_bytes[path]) != required_hash:
                raise Rejected("source snapshot drift; independent re-audit required")
            self.sources[path] = source_bytes[path].decode("utf-8").replace("\r\n", "\n")
            offsets, offset = [], 0
            for line in self.sources[path].splitlines(keepends=True):
                offsets.append(offset)
                offset += len(line)
            self.line_offsets[path] = offsets
        self.entries = {d["qualified_name"]: d for d in self.audit["matched_definitions"]}
        if len(self.entries) != manifest["expected_definitions"] or len(self.entries) != len(self.audit["matched_definitions"]):
            raise Rejected("audited declaration inventory count or identity drift")
        if len(self.audit["local_record_schemas"]) != manifest["expected_local_schemas"]:
            raise Rejected("audited schema count drift")
        self.schemas, self.enums = {}, {}
        self._read_schemas()
        self.references = {}
        for name, entry in self.entries.items():
            if name != f"{manifest['namespace']}.{entry['name']}":
                raise Rejected("audited namespace mismatch")
            expected = self.data_type(entry["result_type"])
            for alias in (name, entry["name"], "SALD." + entry["name"]):
                if alias in self.references:
                    raise Rejected("ambiguous audited reference")
                self.references[alias] = (name, expected)
        self.declarations = {}
        for declaration in declarations:
            name = _get(declaration, "full_name")
            if name not in self.entries:
                continue
            if name in self.declarations:
                raise Rejected("duplicate caller declaration identity")
            if _get(declaration, "kind") != "def":
                raise Rejected("audited metadata is no longer a def")
            path = _relative(_get(declaration, "source_file"))
            if path != self.audit["snapshot"]["source_path"]:
                raise Rejected("declaration moved outside its audited source module")
            code = _get(declaration, "source_text").replace("\r\n", "\n").rstrip()
            if digest(code.encode('utf-8')) != self.entries[name].get('declaration_sha256'):
                raise Rejected('exact declaration body drift or truncation')
            line = _get(declaration, "source_line")
            if not isinstance(line, int) or line < 1 or line > len(self.line_offsets[path]):
                raise Rejected("invalid caller source line")
            current = self.sources[path]
            start = self.line_offsets[path][line - 1]
            end = start + len(code)
            if not code or not current.startswith(code, start) or (len(current) > end and current[end] not in "\n\r"):
                raise Rejected("caller declaration text is stale or truncated")
            self.declarations[name] = code
        if self.declarations.keys() != self.entries.keys():
            raise Rejected("caller inventory omits audited declarations")

    def data_type(self, text: str) -> str:
        text = " ".join(text.split())
        if text == "String":
            return text
        if text.startswith("List "):
            return "List " + self.data_type(text[5:])
        candidates = [text, "AutoSamplingTheory." + text, "AutoSamplingTheory.SALD." + text]
        matches = [c for c in candidates if c in self.schemas or c in self.enums]
        if len(matches) != 1:
            raise Rejected("unsupported or ambiguous type; Prop and proof fields are excluded")
        return matches[0]

    def _read_schemas(self) -> None:
        for definition in self.audit["core_exact_definitions"]:
            name = "AutoSamplingTheory." + definition["name"]
            exact = definition["exact_schema"]
            if exact.startswith("inductive "):
                self.enums[name] = re.findall(r"^\s*\| ([A-Za-z_][A-Za-z0-9_]*)\s*$", exact, re.M)
                if not self.enums[name]:
                    raise Rejected("unsupported enum schema")
            elif exact.startswith("structure "):
                self.schemas[name] = []
                for line in exact.splitlines()[1:]:
                    if line.startswith("deriving "):
                        continue
                    match = re.fullmatch(r"  (\w+) : (.+?)(?: := (.*))?", line)
                    if not match:
                        raise Rejected("unsupported core record schema")
                    field, type_text, default = match.groups()
                    self.schemas[name].append({"name": field, "type": type_text, "default": default})
            else:
                raise Rejected("unsupported core schema declaration")
        for schema in self.audit["local_record_schemas"]:
            name = schema["qualified_name"]
            if name in self.schemas:
                raise Rejected("duplicate audited schema")
            self.schemas[name] = [dict(f, default=f["default"] or None) for f in schema["fields"]]
        for fields in self.schemas.values():
            if len({f["name"] for f in fields}) != len(fields):
                raise Rejected("duplicate audited schema field")
            for field in fields:
                field["type"] = self.data_type(field["type"])

    def field_meaning(self, type_name: str, name: str, field_type: str) -> str:
        core = self.audit["core_field_semantics"]
        specific = core.get(type_name.rsplit(".", 1)[-1], {}).get(name)
        if specific:
            return specific
        short = field_type.removeprefix("AutoSamplingTheory.")
        return core["local_schema_fields"].get(short, "Nested descriptive data, not a proof witness.")

    def explain(self, name: str) -> dict:
        if name not in self.entries:
            raise Rejected("declaration is not in the exact audited allowlist")
        entry, code = self.entries[name], self.declarations[name]
        lesson = {"declaration": name, "id": "lean-data-" + quote(name, safe="._-"),
                  "kind": "data-construction", "result_type": self.data_type(entry["result_type"]),
                  "boundary": BOUNDARY, "resolution": "unresolved", "lean_source": None,
                  "mathematical_proof_evidence": False, "proof_status_evidence": False,
                  "compiled_dependency_evidence": False, "source_certification": False}
        try:
            tokens = tokenize(code)
            if not source_is_safe(code, tokens):
                raise Rejected("absolute local path in exact source; disclosure withheld, not redacted")
            lesson["lean_source"] = code
            header = tokenize(entry["normalized_full_signature"])
            if [t.text for t in tokens[:len(header)]] != [t.text for t in header]:
                raise Rejected("nullary declaration signature or where/assignment shape drift")
            # Audit signatures must themselves say def NAME : TYPE where/:=.
            if len(header) < 5 or [t.text for t in header[:3]] != ["def", entry["name"], ":"]:
                raise Rejected("audited signature is not an explicit nullary def")
            expected = self.data_type(" ".join(t.text for t in header[3:-1]))
            if expected != lesson["result_type"] or header[-1].text not in {"where", ":="}:
                raise Rejected("audited result type or construction shape mismatch")
            parser = DataParser(tokens[len(header):], self)
            value = parser.record(expected) if header[-1].text == "where" else parser.expression(expected)
            parser.finish()
            lesson.update(resolution="resolved", construction=value,
                          summary=self.summary(value), reason=None)
        except Rejected as error:
            lesson.update(reason=str(error), summary="Construction explanation requires review; no value was guessed.")
        return lesson

    @staticmethod
    def summary(value: dict) -> str:
        kind = value["kind"]
        return {
            "record": "Construct a data record from explicit fields and the audited defaults shown below.",
            "list": "Construct an ordered list of the following data items. It is not a logical conjunction or proof DAG.",
            "string": "Store the following literal text; it is not a proposition in Prop.",
            "reference": "Reuse a named audited data value; no theorem or proof dependency is asserted.",
            "concat": "Concatenate the shown data expressions in source order. They remain symbolic and are not evaluated.",
            "enum": "Store a taxonomy or workflow label, not a proof certificate.",
        }[kind]

    def explain_all(self) -> dict:
        lessons = [self.explain(name) for name in self.entries]
        resolved = sum(x["resolution"] == "resolved" for x in lessons)
        return {"reader_version": self.manifest["reader_version"], "audited": len(lessons),
                "explained": resolved, "unresolved": len(lessons) - resolved,
                "mathematical_proofs_added": 0, "lessons": lessons}


def _node_html(node: dict) -> str:
    esc = html.escape
    kind = node["kind"]
    if kind == "string":
        return '<span class="stored-text">' + esc(node["text"]) + '</span>'
    if kind == "enum":
        label = esc(node["type"] + "." + node["label"])
        return '<code>' + label + '</code><span> — stored label only; no proof certification</span>'
    if kind == "reference":
        return '<code>' + esc(node["declaration"]) + '</code><span> — audited data reference, not expanded and not a compiled dependency edge</span>'
    if kind in {"list", "concat"}:
        children = node["items"] if kind == "list" else node["parts"]
        lead = "Ordered data items" if kind == "list" else "Concatenate these expressions without evaluating them"
        return '<p>' + lead + '</p><ol>' + ''.join('<li>' + _node_html(n) + '</li>' for n in children) + '</ol>'
    if kind == "record":
        prefix = '<p>Use the audited localTexAnchor field mapping.</p>' if node.get("helper") else ''
        return prefix + '<dl>' + ''.join(
            '<dt><code>' + esc(f["name"]) + '</code> : <code>' + esc(f["type"]) + '</code> (' + esc(f["origin"]) + ')</dt>'
            '<dd><p>' + esc(f["meaning"]) + '</p>' + _node_html(f["value"]) + '</dd>'
            for f in node["fields"]) + '</dl>'
    raise Rejected("unknown rendered construction node")


def render_html(lesson: Mapping) -> str:
    """Trusted reader-produced lesson -> escaped adjacent explanation + Lean fold.

    IDs preserve exact case. No links are invented and no status styling is
    assigned. Source strings are escaped as content, never parsed as HTML.
    """
    esc = html.escape
    body = ('<section class="metadata-lesson" id="' + esc(lesson["id"], quote=True) + '">'
            '<h3>' + esc(lesson["declaration"]) + '</h3><p>Data definition / provenance and workflow record</p>'
            '<p>' + esc(lesson["summary"]) + '</p><p>' + esc(lesson["boundary"]) + '</p>')
    if lesson["resolution"] == "resolved":
        body += _node_html(lesson["construction"])
    else:
        body += '<p class="unresolved">Unresolved: ' + esc(lesson["reason"]) + '</p>'
    if lesson["lean_source"] is not None:
        body += ('<details class="inline-lean"><summary>Exact Lean data construction</summary>'
                 '<pre><code class="language-lean">' + esc(lesson["lean_source"]) + '</code></pre></details>')
    return body + '</section>'
