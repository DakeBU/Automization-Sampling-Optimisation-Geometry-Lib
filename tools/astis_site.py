#!/usr/bin/env python3
"""Build and validate the ASTIS Blueprint-style textbook website.

The generated status is deliberately not a second theorem registry.  Blue
declarations come from `TechnicalLemmas/Registry.lean`, are resolved against
the Lean source tree, and are covered by the repository's `lake build Tests`
gate.  Pedagogical prose and Chewi source correspondence live under
`website/content`.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import astis_source


ROOT = Path(__file__).resolve().parents[1]
WEBSITE = ROOT / "website"
CONTENT = WEBSITE / "content"
STATIC = WEBSITE / "static"
DIAGRAMS = WEBSITE / "diagrams"
REGISTRY = ROOT / "AutoSamplingTheory" / "TechnicalLemmas" / "Registry.lean"
TESTS = ROOT / "Tests" / "Basic.lean"
DEFAULT_OUTPUT = ROOT / "_site"
GATE_EVIDENCE = ROOT / ".astis" / "site-lean-gate.json"
CHEWI_URL = "https://chewisinho.github.io/main.pdf"


@dataclasses.dataclass
class RegistryEntry:
    key: str
    local_decl: str
    upstream_decl: str
    upstream_file: str
    status: str
    tags: list[str]
    sald_use: str
    note: str
    source_file: str = ""
    source_line: int = 0
    source_text: str = ""
    docstring: str = ""
    explicit_test: bool = False
    dependencies: list[str] = dataclasses.field(default_factory=list)
    consumers: list[str] = dataclasses.field(default_factory=list)

    @property
    def short_name(self) -> str:
        return self.local_decl.rsplit(".", 1)[-1] if self.local_decl else self.key

    @property
    def namespace(self) -> str:
        return self.local_decl.rsplit(".", 1)[0] if "." in self.local_decl else ""

    @property
    def slug(self) -> str:
        return slugify(self.local_decl or self.key)

    @property
    def is_blue(self) -> bool:
        return self.status == "formalizedLocal" and bool(self.source_file)


@dataclasses.dataclass
class SourceDeclaration:
    full_name: str
    short_name: str
    kind: str
    module: str
    source_file: str
    source_line: int
    source_text: str
    docstring: str
    anchor: str
    has_placeholder: bool
    placeholder_tokens: list[str]
    registry_status: str = ""
    registry_card: str = ""
    route_status: str = "Not mapped"
    route_note: str = "No textbook milestone metadata is attached to this declaration."


@dataclasses.dataclass
class SourceModule:
    name: str
    source_file: str
    imports: list[str]
    declarations: list[SourceDeclaration]
    role: str


@dataclasses.dataclass
class GitContext:
    commit: str
    ref: str
    remote_url: str
    web_root: str
    commit_published: bool
    public_source_links: bool
    dirty_files: set[str]


@dataclasses.dataclass
class GateEvidence:
    passed: bool
    current: bool
    commit: str
    source_digest: str
    generated_at: str
    commands: list[str]
    note: str


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return value or "entry"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def source_digest() -> str:
    digest = hashlib.sha256()
    paths = [
        ROOT / "AutoSamplingTheory.lean",
        *sorted((ROOT / "AutoSamplingTheory").rglob("*.lean")),
        ROOT / "Tests.lean",
        *sorted((ROOT / "Tests").rglob("*.lean")),
        ROOT / "lakefile.lean",
        ROOT / "lean-toolchain",
        ROOT / "lake-manifest.json",
    ]
    for path in paths:
        if not path.exists():
            continue
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def git_context() -> GitContext:
    def git(*args: str) -> str:
        result = run_command(["git", *args], check=False)
        return result.stdout.strip() if result.returncode == 0 else ""

    commit = git("rev-parse", "HEAD")
    ref = git("symbolic-ref", "--short", "-q", "HEAD") or commit[:12] or "unknown"
    remote_url = git("remote", "get-url", "origin")
    web_root = ""
    match = re.match(r"(?:https://github\.com/|git@github\.com:)([^/]+/[^/]+?)(?:\.git)?$", remote_url)
    if match:
        web_root = f"https://github.com/{match.group(1)}"
    published_refs = git("branch", "-r", "--contains", commit).splitlines() if commit else []
    dirty_files: set[str] = set()
    status_result = run_command(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        check=False,
    )
    for line in status_result.stdout.splitlines():
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path:
            dirty_files.add(path)
    return GitContext(
        commit=commit,
        ref=ref,
        remote_url=remote_url,
        web_root=web_root,
        commit_published=bool(published_refs),
        public_source_links=os.environ.get("ASTIS_PUBLIC_SOURCE_LINKS", "").lower()
        in {"1", "true", "yes"},
        dirty_files=dirty_files,
    )


def load_gate_evidence(path: Path = GATE_EVIDENCE) -> GateEvidence:
    current_commit = run_command(["git", "rev-parse", "HEAD"], check=False).stdout.strip()
    current_digest = source_digest()
    if not path.exists():
        return GateEvidence(
            passed=False,
            current=False,
            commit=current_commit,
            source_digest=current_digest,
            generated_at="",
            commands=[],
            note="Lean gate has not been recorded for this checkout.",
        )
    try:
        raw = load_json(path)
        assert isinstance(raw, dict)
    except (OSError, ValueError, AssertionError):
        return GateEvidence(
            passed=False,
            current=False,
            commit=current_commit,
            source_digest=current_digest,
            generated_at="",
            commands=[],
            note="Lean gate evidence is unreadable.",
        )
    evidence_commit = str(raw.get("commit", ""))
    evidence_digest = str(raw.get("source_digest", ""))
    current = evidence_commit == current_commit and evidence_digest == current_digest
    passed = bool(raw.get("passed")) and current
    note = (
        "Lean gate passed for this exact Lean source digest."
        if passed
        else "Lean gate evidence does not match this checkout or source digest."
    )
    return GateEvidence(
        passed=passed,
        current=current,
        commit=evidence_commit,
        source_digest=evidence_digest,
        generated_at=str(raw.get("generated_at", "")),
        commands=[str(command) for command in raw.get("commands", [])],
        note=note,
    )


def sanitize_lean(text: str) -> str:
    """Remove comments and strings while preserving line and column positions."""
    chars = list(text)
    result = list(text)
    i = 0
    block_depth = 0
    in_string = False
    while i < len(chars):
        if block_depth:
            if i + 1 < len(chars) and chars[i] == "/" and chars[i + 1] == "-":
                result[i] = result[i + 1] = " "
                block_depth += 1
                i += 2
                continue
            if i + 1 < len(chars) and chars[i] == "-" and chars[i + 1] == "/":
                result[i] = result[i + 1] = " "
                block_depth -= 1
                i += 2
                continue
            if chars[i] != "\n":
                result[i] = " "
            i += 1
            continue
        if in_string:
            if chars[i] == "\\" and i + 1 < len(chars):
                if chars[i] != "\n":
                    result[i] = " "
                if chars[i + 1] != "\n":
                    result[i + 1] = " "
                i += 2
                continue
            if chars[i] == '"':
                result[i] = " "
                in_string = False
            elif chars[i] != "\n":
                result[i] = " "
            i += 1
            continue
        if i + 1 < len(chars) and chars[i] == "-" and chars[i + 1] == "-":
            while i < len(chars) and chars[i] != "\n":
                result[i] = " "
                i += 1
            continue
        if i + 1 < len(chars) and chars[i] == "/" and chars[i + 1] == "-":
            result[i] = result[i + 1] = " "
            block_depth = 1
            i += 2
            continue
        if chars[i] == '"':
            result[i] = " "
            in_string = True
        i += 1
    return "".join(result)


def declaration_anchor(module: str, full_name: str, line: int) -> str:
    stable = hashlib.sha1(f"{module}\0{full_name}\0{line}".encode("utf-8")).hexdigest()[:10]
    return f"decl-{slugify(full_name)[:72]}-{stable}"


def project_lean_paths() -> list[Path]:
    paths = [ROOT / "AutoSamplingTheory.lean", *sorted((ROOT / "AutoSamplingTheory").rglob("*.lean"))]
    paths.extend([ROOT / "Tests.lean", *sorted((ROOT / "Tests").rglob("*.lean"))])
    return [path for path in paths if path.exists()]


def scan_project_sources() -> tuple[list[SourceModule], list[SourceDeclaration]]:
    declaration_re = re.compile(
        r"^\s*(?:@\[[^\]]*\]\s*)*"
        r"(?:(?:noncomputable|private|protected|local|unsafe)\s+)*"
        r"(theorem|lemma|def|abbrev|structure|class|inductive|opaque|axiom|instance)\s+"
        r"([A-Za-z_][A-Za-z0-9_'.]*)"
    )
    modules: list[SourceModule] = []
    declarations: list[SourceDeclaration] = []
    for path in project_lean_paths():
        rel = path.relative_to(ROOT).as_posix()
        module_name = lean_module_from_path(path)
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        clean_lines = sanitize_lean(text).splitlines()
        imports = []
        for line in clean_lines:
            match = re.match(r"^\s*import\s+([A-Za-z0-9_'.]+)", line)
            if match:
                imports.append(match.group(1))

        contexts: list[tuple[str, list[str]]] = []
        starts: list[tuple[int, str, str, list[str]]] = []
        for index, line in enumerate(clean_lines):
            namespace_match = re.match(r"^\s*namespace\s+([A-Za-z0-9_'.]+)\s*$", line)
            if namespace_match:
                contexts.append(("namespace", namespace_match.group(1).split(".")))
                continue
            if re.match(r"^\s*section(?:\s+[A-Za-z0-9_'.]+)?\s*$", line):
                contexts.append(("section", []))
                continue
            if re.match(r"^\s*end(?:\s+[A-Za-z0-9_'.]+)?\s*$", line):
                if contexts:
                    contexts.pop()
                continue
            match = declaration_re.match(line)
            if not match:
                continue
            kind, name = match.groups()
            if kind == "instance" and name in {"where", "by"}:
                continue
            namespace_parts = [
                part
                for context_kind, parts in contexts
                if context_kind == "namespace"
                for part in parts
            ]
            full_name = ".".join([*namespace_parts, *name.split(".")])
            starts.append((index, kind, name, [full_name]))

        module_declarations: list[SourceDeclaration] = []
        for position, (start, kind, name, full_name_box) in enumerate(starts):
            end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
            full_name = full_name_box[0]
            cursor = start - 1
            while cursor >= 0 and not lines[cursor].strip():
                cursor -= 1
            doc_lines: list[str] = []
            if cursor >= 0 and "-/" in lines[cursor]:
                while cursor >= 0:
                    doc_lines.append(lines[cursor])
                    if "/--" in lines[cursor] or "/-!" in lines[cursor]:
                        break
                    cursor -= 1
                doc_lines.reverse()
            docstring = "\n".join(doc_lines)
            docstring = re.sub(r"^\s*/-[*!]?", "", docstring)
            docstring = re.sub(r"-/\s*$", "", docstring).strip()
            source_text = "\n".join(lines[start:end]).rstrip()
            clean_source = sanitize_lean(source_text)
            placeholder_tokens = sorted(
                {
                    token
                    for token in ("sorry", "admit")
                    if re.search(rf"\b{token}\b", clean_source)
                }
            )
            if kind == "axiom":
                placeholder_tokens.append("axiom")
            declaration = SourceDeclaration(
                full_name=full_name,
                short_name=name.rsplit(".", 1)[-1],
                kind=kind,
                module=module_name,
                source_file=rel,
                source_line=start + 1,
                source_text=source_text,
                docstring=docstring,
                anchor=declaration_anchor(module_name, full_name, start + 1),
                has_placeholder=bool(placeholder_tokens),
                placeholder_tokens=placeholder_tokens,
            )
            module_declarations.append(declaration)
            declarations.append(declaration)
        role = "test" if rel == "Tests.lean" or rel.startswith("Tests/") else (
            "root aggregator" if rel == "AutoSamplingTheory.lean" else "production"
        )
        modules.append(
            SourceModule(
                name=module_name,
                source_file=rel,
                imports=imports,
                declarations=module_declarations,
                role=role,
            )
        )
    return modules, declarations


def parse_string(field: str, block: str) -> str:
    match = re.search(rf"\b{re.escape(field)}\s*:=\s*\"((?:[^\"\\]|\\.)*)\"", block)
    if not match:
        return ""
    return json.loads(f'"{match.group(1)}"')


def parse_registry() -> list[RegistryEntry]:
    text = REGISTRY.read_text(encoding="utf-8")
    blocks = re.findall(r"\{\s*key\s*:=.*?\n\s*\}", text, flags=re.S)
    entries: list[RegistryEntry] = []
    for block in blocks:
        status_match = re.search(r"status\s*:=\s*LemmaMemoryStatus\.(\w+)", block)
        tags_match = re.search(r"tags\s*:=\s*\[(.*?)\]", block, flags=re.S)
        tags = re.findall(r'"((?:[^"\\]|\\.)*)"', tags_match.group(1)) if tags_match else []
        entries.append(
            RegistryEntry(
                key=parse_string("key", block),
                local_decl=parse_string("localDecl", block),
                upstream_decl=parse_string("upstreamDecl", block),
                upstream_file=parse_string("upstreamFile", block),
                status=status_match.group(1) if status_match else "referenceOnly",
                tags=[json.loads(f'"{tag}"') for tag in tags],
                sald_use=parse_string("saldUse", block),
                note=parse_string("note", block),
            )
        )
    if not entries:
        raise RuntimeError(f"no registry entries parsed from {REGISTRY}")
    return entries


def lean_module_from_path(path: Path) -> str:
    return ".".join(path.relative_to(ROOT).with_suffix("").parts)


def source_index() -> tuple[dict[str, dict[str, object]], dict[str, str]]:
    """Index top-level Lean declarations by fully qualified and short names."""
    indexed: dict[str, dict[str, object]] = {}
    module_files: dict[str, str] = {}
    declaration_re = re.compile(
        r"^\s*(?:noncomputable\s+)?(?:private\s+)?"
        r"(?:theorem|lemma|def|abbrev|structure|class|inductive)\s+([A-Za-z0-9_'.]+)"
    )
    for path in sorted((ROOT / "AutoSamplingTheory").rglob("*.lean")):
        rel = path.relative_to(ROOT).as_posix()
        module = lean_module_from_path(path)
        module_files[module] = rel
        lines = path.read_text(encoding="utf-8").splitlines()
        namespace_stack: list[str] = []
        starts: list[tuple[int, str, list[str]]] = []
        for i, line in enumerate(lines):
            ns_match = re.match(r"^\s*namespace\s+([A-Za-z0-9_'.]+)\s*$", line)
            if ns_match:
                namespace_stack.append(ns_match.group(1))
                continue
            if re.match(r"^\s*end(?:\s+[A-Za-z0-9_'.]+)?\s*$", line) and namespace_stack:
                namespace_stack.pop()
                continue
            match = declaration_re.match(line)
            if match:
                starts.append((i, match.group(1), list(namespace_stack)))
        for pos, (start, name, namespaces) in enumerate(starts):
            end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
            full = name if "." in name else ".".join([*namespaces, name])
            doc_lines: list[str] = []
            cursor = start - 1
            while cursor >= 0 and not lines[cursor].strip():
                cursor -= 1
            if cursor >= 0 and "-/" in lines[cursor]:
                while cursor >= 0:
                    doc_lines.append(lines[cursor])
                    if "/--" in lines[cursor] or "/-!" in lines[cursor]:
                        break
                    cursor -= 1
                doc_lines.reverse()
            doc = "\n".join(doc_lines)
            doc = re.sub(r"^\s*/-[*!]?", "", doc)
            doc = re.sub(r"-/\s*$", "", doc).strip()
            source_text = "\n".join(lines[start:end]).rstrip()
            record = {
                "full_name": full,
                "short_name": name.rsplit(".", 1)[-1],
                "file": rel,
                "line": start + 1,
                "module": module,
                "source_text": source_text,
                "docstring": doc,
            }
            indexed[full] = record
    return indexed, module_files


def enrich_entries(entries: list[RegistryEntry]) -> tuple[list[RegistryEntry], dict[str, str]]:
    indexed, module_files = source_index()
    modules, _ = scan_project_sources()
    imports_by_module = {module.name: module.imports for module in modules}
    module_by_file = {module.source_file: module.name for module in modules}

    def visible_modules(source_file: str) -> set[str]:
        pending = [module_by_file.get(source_file, '')]
        visible: set[str] = set()
        while pending:
            module = pending.pop()
            if module in visible:
                continue
            visible.add(module)
            pending.extend(imports_by_module.get(module, []))
        return visible
    test_paths = [ROOT / "Tests.lean", *sorted((ROOT / "Tests").rglob("*.lean"))]
    tests_text = "\n".join(path.read_text(encoding="utf-8") for path in test_paths if path.exists())
    by_short: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in indexed.values():
        by_short[str(record["short_name"])].append(record)

    for entry in entries:
        record = indexed.get(entry.local_decl)
        if record is None and entry.local_decl:
            candidates = by_short.get(entry.short_name, [])
            if len(candidates) == 1:
                record = candidates[0]
        if record:
            entry.source_file = str(record["file"])
            entry.source_line = int(record["line"])
            entry.source_text = str(record["source_text"])
            entry.docstring = str(record["docstring"])
        entry.explicit_test = entry.short_name in tests_text

    local_by_short: dict[str, list[RegistryEntry]] = defaultdict(list)
    for entry in entries:
        if entry.local_decl and entry.source_text:
            local_by_short[entry.short_name].append(entry)
    for entry in entries:
        if not entry.source_text:
            continue
        deps: set[str] = set()
        visible = visible_modules(entry.source_file)
        for short, candidates in local_by_short.items():
            # A dot-method name such as const_mul may belong to Mathlib, not
            # an unrelated ASTIS declaration. Imports are a necessary bound;
            # ambiguous visible short names still cannot certify an edge.
            candidates = [candidate for candidate in candidates
                          if module_by_file.get(candidate.source_file) in visible]
            if len(candidates) != 1:
                continue
            full = candidates[0].local_decl
            if full == entry.local_decl:
                continue
            if re.search(rf"(?<![A-Za-z0-9_']){re.escape(short)}(?![A-Za-z0-9_'])", entry.source_text):
                deps.add(full)
        entry.dependencies = sorted(deps)
    by_decl = {entry.local_decl: entry for entry in entries if entry.local_decl}
    for entry in entries:
        for dep in entry.dependencies:
            if dep in by_decl:
                by_decl[dep].consumers.append(entry.local_decl)
    for entry in entries:
        entry.consumers = sorted(set(entry.consumers))
    return entries, module_files


CHAPTER_1_COVERAGE_KINDS = {
    "owned_definition",
    "proved_theorem",
    "derived_identity",
    "solved_exercise",
    "complete_expository_remark",
}
CHAPTER_1_COVERAGE_STATUSES = {"complete", "partial", "planned", "blocked", "external"}
CHAPTER_1_DECLARATION_KINDS = {
    "owned_definition": {"def", "abbrev", "structure", "class", "inductive"},
    "proved_theorem": {"theorem", "lemma"},
    "derived_identity": {"theorem", "lemma"},
    "solved_exercise": {"theorem", "lemma"},
}


def validate_chapter_1_evidence(
    site_data: dict[str, object],
    entries: list[RegistryEntry],
    declarations_by_name: dict[str, SourceDeclaration],
    *,
    require_complete: bool = False,
) -> list[str]:
    """Validate item-level evidence without inferring closure from nearby metadata."""
    errors: list[str] = []
    matrix = list(site_data.get("chapter_1_completion_matrix", []))
    source_rows = list(site_data.get("source_correspondence", []))
    source_by_id = {str(row.get("id", "")): row for row in source_rows}
    registry_by_decl = {entry.local_decl: entry for entry in entries if entry.local_decl}
    registry_by_key = {entry.key: entry for entry in entries}
    route_counts = Counter(str(item.get("source_route_id", "")) for item in matrix)

    if len(matrix) != 125:
        errors.append(f"Chapter 1 evidence requires 125 audited source items, found {len(matrix)}")
    for route_id, count in sorted(route_counts.items()):
        if route_id and count != 1:
            errors.append(f"Chapter 1 source route is reused {count} times: {route_id}")

    for item in matrix:
        item_id = str(item.get("id", ""))
        route_id = str(item.get("source_route_id", ""))
        source_id = str(item.get("source_correspondence_id", ""))
        coverage_kind = str(item.get("coverage_kind", ""))
        coverage_status = str(item.get("coverage_status", ""))
        declarations = [str(name) for name in item.get("required_declarations", [])]
        test_paths = [str(path) for path in item.get("focused_tests", [])]
        registry_keys = [str(key) for key in item.get("registry_keys", [])]
        blockers = [str(value) for value in item.get("residual_blockers", []) if str(value).strip()]

        if not route_id:
            errors.append(f"{item_id}: missing source_route_id")
        if coverage_kind not in CHAPTER_1_COVERAGE_KINDS:
            errors.append(f"{item_id}: invalid coverage_kind {coverage_kind!r}")
        if coverage_status not in CHAPTER_1_COVERAGE_STATUSES:
            errors.append(f"{item_id}: invalid coverage_status {coverage_status!r}")
        source = source_by_id.get(source_id) if source_id else None
        if source_id and source is None:
            errors.append(f"{item_id}: unknown source correspondence row {source_id}")
        if source is not None and coverage_status == "complete":
            for field in ("source_kind", "book_page", "pdf_page", "page", "source_url"):
                if source.get(field) != item.get(field):
                    errors.append(
                        f"{item_id}: {field} differs between matrix and {source_id} "
                        f"({item.get(field)!r} != {source.get(field)!r})"
                    )
            for field in ("status", "local_status", "route_status"):
                if str(source.get(field, "")).lower() != "compiled":
                    errors.append(f"{item_id}: {source_id}.{field} is not compiled")
            source_declarations = [str(name) for name in source.get("lean_declarations", [])]
            for name in declarations:
                if name not in source_declarations:
                    errors.append(
                        f"{item_id}: {source_id} does not cite required declaration {name}"
                    )
            for name in source_declarations:
                source_declaration = declarations_by_name.get(name)
                if source_declaration is None:
                    errors.append(
                        f"{item_id}: source correspondence declaration cannot be resolved: {name}"
                    )
                elif source_declaration.has_placeholder:
                    errors.append(
                        f"{item_id}: source correspondence declaration contains a placeholder: {name}"
                    )

        if coverage_status == "complete" and coverage_kind != "complete_expository_remark":
            if not declarations:
                errors.append(f"{item_id}: complete item has no required declaration")
            if not test_paths:
                errors.append(f"{item_id}: complete item has no focused test")
            if not registry_keys:
                errors.append(f"{item_id}: complete item has no Registry key")
        if coverage_status == "complete" and blockers:
            errors.append(f"{item_id}: complete item retains residual blockers")

        test_contents: dict[str, str] = {}
        for test_path in test_paths:
            path = ROOT / test_path
            if not path.is_file() or path.suffix != ".lean":
                errors.append(f"{item_id}: focused test does not exist: {test_path}")
            else:
                test_contents[test_path] = path.read_text(encoding="utf-8")
        for name in declarations:
            declaration = declarations_by_name.get(name)
            if declaration is None:
                errors.append(f"{item_id}: required declaration cannot be resolved: {name}")
                continue
            if declaration.has_placeholder:
                errors.append(f"{item_id}: required declaration contains a placeholder: {name}")
            allowed_kinds = CHAPTER_1_DECLARATION_KINDS.get(coverage_kind)
            if coverage_status == "complete" and allowed_kinds and declaration.kind not in allowed_kinds:
                errors.append(
                    f"{item_id}: {coverage_kind} cannot be certified by "
                    f"{declaration.kind} declaration {name}"
                )
            if coverage_status == "complete" and coverage_kind == "owned_definition":
                clean_source = sanitize_lean(declaration.source_text)
                if re.search(r":\s*Prop\s*:=\s*(?:by\s+)?(?:True|trivial)\b", clean_source):
                    errors.append(f"{item_id}: owned definition is an empty Prop shell: {name}")
            if coverage_status == "complete" and coverage_kind == "derived_identity":
                clean_source = sanitize_lean(declaration.source_text)
                if not any(token in clean_source for token in ("=", "Tendsto", "∫", "integral", "lintegral")):
                    errors.append(f"{item_id}: derived identity has no equality, limit, or integral: {name}")
            if coverage_status == "complete" and test_contents and not any(
                name in text or declaration.short_name in text for text in test_contents.values()
            ):
                errors.append(f"{item_id}: focused tests do not reference {name}")
            entry = registry_by_decl.get(name)
            if coverage_status == "complete" and (entry is None or not entry.is_blue):
                errors.append(f"{item_id}: required declaration is not compiled in Registry: {name}")
        for key in registry_keys:
            entry = registry_by_key.get(key)
            if entry is None:
                errors.append(f"{item_id}: unknown Registry key: {key}")
            elif entry.local_decl not in declarations:
                errors.append(
                    f"{item_id}: Registry key {key} does not certify a required declaration"
                )
        if require_complete:
            if coverage_status != "complete":
                errors.append(f"{item_id}: coverage status is {coverage_status}, expected complete")
            if blockers:
                errors.append(f"{item_id}: residual blockers remain")
            if source is None:
                errors.append(f"{item_id}: no exact source correspondence row")
    return errors


def validate_chapter_1_closure(
    site_data: dict[str, object],
    entries: list[RegistryEntry],
    declarations_by_name: dict[str, SourceDeclaration],
) -> list[str]:
    """Compatibility wrapper for the strict Chapter 1 completion gate."""
    return validate_chapter_1_evidence(
        site_data, entries, declarations_by_name, require_complete=True
    )


def chapter_1_completion_report(items: list[dict[str, object]]) -> dict[str, object]:
    statuses = Counter(str(item.get("coverage_status", "")) for item in items)
    missing_declarations = sum(
        not item.get("required_declarations")
        and item.get("coverage_kind") != "complete_expository_remark"
        for item in items
    )
    missing_tests = sum(
        not item.get("focused_tests")
        and item.get("coverage_kind") != "complete_expository_remark"
        for item in items
    )
    return {
        "schema_version": 2,
        "total": len(items),
        "complete": statuses["complete"],
        "partial": statuses["partial"],
        "planned": statuses["planned"],
        "blocked": statuses["blocked"],
        "external": statuses["external"],
        "missing_route": sum(not str(item.get("source_route_id", "")).strip() for item in items),
        "missing_declaration": missing_declarations,
        "missing_test": missing_tests,
        "residual_blockers": sum(bool(item.get("residual_blockers")) for item in items),
    }


def test_registry_count() -> int | None:
    text = TESTS.read_text(encoding="utf-8")
    matches = re.findall(r"(?:exact|native_decide|decide).*?(\d+)", text)
    count_lines = [
        line for line in text.splitlines()
        if "technicalLemmaMemory" in line or "formalized" in line.lower() or "256" in line
    ]
    for line in reversed(count_lines):
        match = re.search(r"\b(\d{2,4})\b", line)
        if match:
            return int(match.group(1))
    return int(matches[-1]) if matches else None


def status_class(entry: RegistryEntry) -> str:
    if entry.is_blue:
        return "blue"
    return {
        "portCandidate": "purple",
        "sourceGap": "orange",
        "referenceOnly": "gray",
        "formalizedLocal": "orange",
    }.get(entry.status, "red")


def status_label(entry: RegistryEntry) -> str:
    if entry.is_blue:
        return "compiled Samplinglib leaf"
    return {
        "portCandidate": "external port candidate",
        "sourceGap": "typed source gap",
        "referenceOnly": "external reference",
        "formalizedLocal": "registry/source mismatch",
    }.get(entry.status, "todo")


def badge(label: str, css: str) -> str:
    return f'<span class="status status-{esc(css)}">{esc(label)}</span>'


def list_html(items: Iterable[object], *, empty: str = "None recorded.") -> str:
    values = list(items)
    if not values:
        return f'<p class="muted">{esc(empty)}</p>'
    return "<ul>" + "".join(f"<li>{esc(value)}</li>" for value in values) + "</ul>"


def code_html(code: str, language: str = "lean") -> str:
    return f'<pre class="code-block"><code class="language-{esc(language)}">{esc(code)}</code></pre>'


SIDEBAR_GROUPS = (
    ("Start", (
        ("Overview", "index.html", "Overview"),
        ("What is Samplinglib?", "index.html#samplinglib", "Overview"),
    )),
    ("Learn", (
        ("Log-Concave Sampling", "textbook/index.html", "Textbook"),
        ("Book Map", "learning-path/index.html", "Learning path"),
        ("Chapter 1 Matrix", "textbook/chapter-01-matrix.html", "Chapter 1 Matrix"),
    )),
    ("Formal Library", (
        ("Implementation Map", "implementation-map/index.html", "Implementation"),
        ("Lean Declarations", "declarations/index.html", "Declarations"),
        ("Technical Lemmas", "lean-foundations.html", "Lean Foundations"),
        ("Source Correspondence", "source-correspondence.html", "Source Correspondence"),
    )),
    ("Build & Verify", (
        ("Live Formalization", "live/index.html", "Live Formalization"),
        ("ASTIS Harness", "workflow/index.html", "Workflow"),
        ("Verification Workflow", "maintenance.html", "Maintenance"),
    )),
    ("Community", (
        ("Organizers", "attribution/index.html#organizers", "Attribution"),
        ("Contribute", "contribute/index.html", "Contribute"),
        ("Related Systems", "related-systems/index.html", "Related Systems"),
        ("Roadmap", "roadmap/index.html", "Roadmap"),
        ("Attribution", "attribution/index.html", "Attribution"),
    )),
)

_ACTIVE_GATE: GateEvidence | None = None
_ACTIVE_GIT: GitContext | None = None
_SOURCE_BY_NAME: dict[str, SourceDeclaration] = {}
_TEACHING_BY_NAME: dict[str, dict[str, object]] = {}
_SOURCE_EDITION: dict[str, object] = {}


def route_badge(status: str) -> str:
    css = {
        "Compiled": "blue",
        "Partial": "yellow",
        "Stated/incomplete": "orange",
        "Planned": "gray",
        "Blocked": "red",
        "External/upstream dependency": "purple",
        "Not mapped": "gray",
    }.get(status, "gray")
    return badge(status, css)


def local_declaration_status(declaration: SourceDeclaration, gate: GateEvidence) -> str:
    if declaration.has_placeholder:
        return "Stated/incomplete"
    if declaration.kind in {"structure", "class", "inductive"}:
        return "Compiled" if gate.passed else "Partial"
    return "Compiled" if gate.passed else "Partial"


def source_commit_link_error(url: str, commit: str, web_root: str) -> str | None:
    """Local source uses this checkout; external libraries use their own pins."""
    root = web_root.rstrip("/") or "https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep"
    if url.startswith(root + "/blob/"):
        if commit and f"/blob/{commit}/" not in url:
            return f"source link is not pinned to the generated commit: {url}"
    elif not re.search(r"/blob/[0-9a-f]{40}/", url):
        return f"external source link is not pinned to an immutable commit: {url}"
    return None


def source_href(
    declaration: SourceDeclaration,
    *,
    from_path: str,
) -> tuple[str, str]:
    git = _ACTIVE_GIT or git_context()
    if (
        git.web_root
        and git.commit
        and git.commit_published
        and git.public_source_links
        and declaration.source_file not in git.dirty_files
    ):
        return (
            f"{git.web_root}/blob/{git.commit}/{declaration.source_file}#L{declaration.source_line}",
            f"published source at {git.commit[:12]}",
        )
    prefix = relative_prefix(from_path)
    return (
        f"{prefix}modules/{slugify(declaration.module)}.html#{declaration.anchor}",
        "local preview source",
    )


def relative_prefix(rel_path: str) -> str:
    return "../" * (len(Path(rel_path).parts) - 1)


def textbook_section_path(chapter_number: int, section_id: str) -> str:
    return f"textbook/chapter-{chapter_number:02d}/section-{slugify(section_id)}.html"


def sidebar_html(prefix: str, active: str) -> str:
    groups = []
    for heading, links in SIDEBAR_GROUPS:
        rows = "".join(
            f'<a href="{prefix}{href}"{f" aria-current=\"page\"" if marker == active or (marker == "Textbook" and active.startswith("Textbook:")) else ""}>{esc(label)}</a>'
            for label, href, marker in links
        )
        groups.append(
            f'<section class="sidebar-group"><h2>{esc(heading)}</h2><nav>{rows}</nav></section>'
        )
    chapter_rows = []
    for raw_chapter in _SOURCE_EDITION.get("chapters", []):
        chapter = dict(raw_chapter)
        number = int(chapter["number"])
        if number in {1, 4}:
            part = dict(_SOURCE_EDITION["parts"][0 if number == 1 else 1])
            chapter_rows.append(
                f'<div class="toc-part"><span>Part {part["number"]}</span>{esc(part["title"])}</div>'
            )
        chapter_marker = f"Textbook:{number}"
        section_rows = []
        for raw_section in chapter["sections"]:
            section = dict(raw_section)
            section_id = str(section["id"])
            section_marker = f"Textbook:{section_id}"
            section_rows.append(
                f'<a href="{prefix}{textbook_section_path(number, section_id)}"'
                f'{" aria-current=\"page\"" if active == section_marker else ""}>'
                f'<span>{esc(section_id)}</span>{esc(section["title"])}</a>'
            )
        chapter_rows.append(
            f'<details class="toc-chapter"{" open" if active == chapter_marker or active.startswith(f"Textbook:{number}.") else ""}>'
            f'<summary><span>{number:02d}</span>{esc(chapter["title"])}</summary>'
            f'<a class="chapter-overview-link" href="{prefix}textbook/chapter-{number:02d}.html"'
            f'{" aria-current=\"page\"" if active == chapter_marker else ""}>Chapter overview</a>'
            f'<nav>{"".join(section_rows)}</nav></details>'
        )
    chapters = "".join(chapter_rows)
    groups.insert(
        2,
        f'<details class="chapter-nav"{" open" if active == "Textbook" or active.startswith("Textbook:") else ""}>'
        f'<summary>Canonical book contents</summary><div class="book-toc">{chapters}</div></details>',
    )
    return "".join(groups)


def page(
    title: str,
    rel_path: str,
    body: str,
    *,
    description: str = "Samplinglib: verified sampling theory in Lean",
    active: str = "",
    extra_head: str = "",
    extra_scripts: tuple[str, ...] = (),
) -> str:
    prefix = relative_prefix(rel_path)
    gate = _ACTIVE_GATE or load_gate_evidence()
    git = _ACTIVE_GIT or git_context()
    sidebar = sidebar_html(prefix, active)
    scripts = "".join(f'<script src="{prefix}{esc(path)}"></script>' for path in extra_scripts)
    gate_class = "verified" if gate.passed else "unverified"
    gate_label = "Lean gate passed" if gate.passed else "Lean gate not recorded for this source state"
    gate_detail = (
        f"{gate.generated_at} · {git.commit[:12]}"
        if gate.passed
        else f"{git.ref} · {git.commit[:12] or 'uncommitted'}"
    )
    return f"""<!doctype html>
<html lang="en" data-theme="blueprint" data-color-scheme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(description)}">
  <meta property="og:title" content="{esc(title)} · Samplinglib">
  <meta property="og:description" content="{esc(description)}">
  <link rel="icon" href="data:,">
  <meta property="og:image" content="{prefix}assets/samplinglib-og.png">
  <meta property="og:site_name" content="Samplinglib">
  <title>{esc(title)} · Samplinglib</title>
  <link rel="stylesheet" href="{prefix}assets/site.css">
  <script>
    window.MathJax = {{
      tex: {{inlineMath: [['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']]}},
      options: {{skipHtmlTags: ['script','noscript','style','textarea','pre','code']}}
    }};
  </script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
  {extra_head}
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <header class="mobile-bar">
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-sidebar">Contents</button>
    <a href="{prefix}index.html"><strong>Samplinglib</strong></a>
    <button id="scheme-toggle-mobile" class="scheme-toggle" title="Toggle color scheme" aria-label="Toggle color scheme">◐</button>
  </header>
  <div class="site-shell">
    <aside id="site-sidebar" class="site-sidebar" aria-label="Samplinglib contents">
      <a class="brand" href="{prefix}index.html">
        <span class="brand-mark">S</span>
        <span><strong>Samplinglib</strong><small>Verified Sampling Theory in Lean</small></span>
      </a>
      <div class="search-shell">
        <label class="sr-only" for="global-search">Search declarations and modules</label>
        <input id="global-search" data-global-search data-search-root="{prefix}" type="search" placeholder="Search the library">
        <ul class="search-results" data-global-results hidden></ul>
      </div>
      <div class="sidebar-contents">{sidebar}</div>
      <div class="sidebar-utility">
        <a href="https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep">GitHub <span aria-hidden="true">↗</span></a>
        <button id="scheme-toggle" class="scheme-toggle" title="Toggle color scheme" aria-label="Toggle color scheme">◐</button>
      </div>
    </aside>
    <button class="sidebar-scrim" type="button" data-sidebar-scrim aria-label="Close contents"></button>
    <div class="site-stage">
      <div class="verification-strip {gate_class}">
        <span><strong>{esc(gate_label)}</strong></span>
        <span>{esc(gate_detail)}</span>
      </div>
      <main id="content">{body}</main>
      <footer>
        <p><strong>Samplinglib</strong> is the public formal library and learning interface of Auto-Sampling-Theory-In-Sleep (ASTIS).</p>
        <p>Organized by Dake Bu, Ji Cheng, Huanjian Zhou, Andi Han, Zonghao Chen, Sinho Chewi, Matthew S. Zhang, Hau-San Wong, Qingfu Zhang, and Atsushi Nitanda.</p>
        <p><a href="{prefix}contribute/index.html">Contribute</a> · <a href="{prefix}attribution/index.html">Attribution</a> · <a href="{prefix}maintenance.html">Build and maintenance</a> · generated from Lean source, route metadata, and gate evidence.</p>
      </footer>
    </div>
  </div>
  <script src="{prefix}assets/site.js"></script>
  {scripts}
</body>
</html>
"""


def write_page(output: Path, rel_path: str, content: str) -> None:
    target = output / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def diagram_block(name: str, caption: str) -> str:
    source = (DIAGRAMS / f"{name}.mmd").read_text(encoding="utf-8")
    return (
        f'<figure class="diagram"><pre class="mermaid">{esc(source)}</pre>'
        f"<figcaption>{esc(caption)}</figcaption></figure>"
    )


def render_home(chapters: list[dict[str, object]], entries: list[RegistryEntry]) -> str:
    blue = [entry for entry in entries if entry.is_blue]
    statuses = Counter(chapter["status"] for chapter in chapters)
    body = f"""
<section class="hero">
  <div class="eyebrow">Textbook · rigorous completion · Lean dependency tree</div>
  <h1>Learn log-concave sampling at the depth you need.</h1>
  <p class="lede">Auto-Sampling-Theory-In-Sleep rebuilds Sinho Chewi's
  <em>Log-Concave Sampling</em> as a student-facing textbook, an audit of the
  arguments that prose often suppresses, and a compiled Lean foundation.</p>
  <div class="hero-actions">
    <a class="button primary" href="textbook/chapter-01.html">Start Chapter 1</a>
    <a class="button" href="implementation-map/index.html">Open implementation map</a>
  </div>
  <div class="metric-row">
    <div><strong>{len(blue)}</strong><span>compiled local leaves</span></div>
    <div><strong>{len(chapters)}</strong><span>book chapters mapped</span></div>
    <div><strong>{statuses.get("active", 0)}</strong><span>active chapter frontier</span></div>
    <div><strong>3</strong><span>linked learning depths</span></div>
  </div>
</section>
<section>
  <div class="section-heading"><span>Choose a depth</span><h2>One route, three lenses</h2></div>
  <div class="depth-grid">
    <article class="depth-card calculation">
      <div class="depth-number">01</div><h3>Calculation Route</h3>
      <p>Follow the concepts, formulas, proof calculations, and complexity route with minimal interruption.</p>
      <a href="calculation-route.html">Read the mathematical spine →</a>
    </article>
    <article class="depth-card rigorous">
      <div class="depth-number">02</div><h3>Rigorous Details</h3>
      <p>Ask why a step is valid: measurability, integrability, approximation, domains, representatives, and limits.</p>
      <a href="rigorous-details.html">Open the hidden contracts →</a>
    </article>
    <article class="depth-card lean">
      <div class="depth-number">03</div><h3>Lean Foundations</h3>
      <p>Trace each compiled leaf to its exact statement, source line, dependencies, consumers, Registry entry, and test gate.</p>
      <a href="lean-foundations.html">Descend to Lean →</a>
    </article>
  </div>
</section>
<section class="split">
  <div>
    <div class="section-heading"><span>Current truth</span><h2>The frontier is not a slogan</h2></div>
    <p>Cycle 28 is the latest completed cycle in this worktree. The generic
    PiLp cutoff-gradient norm limit, source-field integrability handoff, and
    vector integral limit are blue. The next audit targets concrete
    generator-display integrability. Gibbs tails, whole-space weighted
    integration by parts, operator domains, and invariance remain separate red nodes.</p>
    <a class="text-link" href="frontier.html">Inspect the strict boundary →</a>
  </div>
  {diagram_block("current-frontier", "Current Chapter 1–2 frontier. Blue means compiled ASTIS declarations; red means unfinished mathematical edges.")}
</section>
<section>
  <div class="section-heading"><span>Book map</span><h2>Twelve connected chapters</h2></div>
  {diagram_block("chapter-spine", "The chapter spine is a learning dependency map, not a claim that every chapter is already formalized.")}
</section>
<section class="note copyright-note">
  <h2>Self-contained without pretending to be the source</h2>
  <p>The book draft exposes no explicit republication license. ASTIS therefore
  provides original, faithful exposition and exact source correspondence
  rather than reproducing long passages. Chewi did not author, endorse, or
  maintain this site.</p>
  <p><a href="{CHEWI_URL}">Open the original book</a> · <a href="attribution.html">Read the attribution and copyright policy</a></p>
</section>
"""
    return page("Home", "index.html", body, active="Home")


def chapter_status_badge(status: str) -> str:
    mapping = {
        "active": ("active frontier", "orange"),
        "partial": ("partially formalized", "yellow"),
        "planned": ("planned", "red"),
    }
    label, css = mapping.get(status, (status, "gray"))
    return badge(label, css)


def render_textbook_index(chapters: list[dict[str, object]]) -> str:
    cards = []
    for chapter in chapters:
        cards.append(
            f"""<article class="chapter-card">
  <div class="chapter-index">{int(chapter["number"]):02d}</div>
  <div>
    <div class="card-meta">Source pp. {esc(chapter["source_pages"])} · {chapter_status_badge(str(chapter["status"]))}</div>
    <h2><a href="{esc(chapter["id"])}.html">{esc(chapter["title"])}</a></h2>
    <p>{esc(chapter["goal"])}</p>
    <div class="tag-row">{''.join(f'<span>{esc(tag)}</span>' for tag in chapter["concepts"][:5])}</div>
  </div>
</article>"""
        )
    body = f"""
<section class="page-hero compact">
  <div class="eyebrow">Textbook spine</div>
  <h1>A reconstructed learning route through <em>Log-Concave Sampling</em></h1>
  <p class="lede">Read the canonical August 9, 2026 edition section by section,
  with rigorous analytic contracts and Lean evidence available on demand.</p>
</section>
{diagram_block("chapter-spine", "Logical chapter dependencies and recommended route.")}
<section class="chapter-list">{''.join(cards)}</section>
"""
    return page("Textbook", "textbook/index.html", body, active="Textbook")


def chapter_source_entries(chapter_number: int, source_entries: list[dict[str, object]]) -> list[dict[str, object]]:
    return [entry for entry in source_entries if int(entry["chapter"]) == chapter_number]


def render_chapter(
    chapter: dict[str, object],
    source_entries: list[dict[str, object]],
    entries_by_decl: dict[str, RegistryEntry],
) -> str:
    mapped = chapter_source_entries(int(chapter["number"]), source_entries)
    route = "".join(
        f"""<article class="calculation-step">
  <span class="step-kicker">Step {i}</span><h3>{esc(step["title"])}</h3>
  <div class="formula">\\[{esc(step["formula"])}\\]</div><p>{esc(step["explanation"])}</p>
</article>"""
        for i, step in enumerate(chapter["calculation_route"], 1)
    )
    mappings = []
    for source in mapped:
        decls = []
        for decl in source["lean_declarations"]:
            entry = entries_by_decl.get(str(decl))
            if entry:
                decls.append(
                    f'<a class="decl-link" href="../theorems/{entry.slug}.html">{esc(entry.short_name)}</a>'
                )
            else:
                decls.append(f'<span class="status status-orange">unresolved metadata: {esc(decl)}</span>')
        mappings.append(
            f"""<article class="source-card">
  <div class="card-meta">{esc(source["source_kind"])} · p. {esc(source["page"])} · {badge(source["status"], "blue" if source["status"] == "compiled" else "red" if source["status"] == "todo" else "yellow")}</div>
  <h3>{esc(source["source_summary"])}</h3>
  <p>{esc(source["astis_exposition"])}</p>
  <div class="decl-links">{''.join(decls) if decls else '<span class="muted">No ASTIS-owned declaration mapped yet.</span>'}</div>
  <a href="{esc(source["source_url"])}">Precise source anchor ↗</a>
</article>"""
        )
    module_links = []
    for module in chapter["lean_modules"]:
        module_links.append(
            f'<a href="../modules/{slugify(str(module))}.html"><code>{esc(module)}</code></a>'
        )
    chapter_number = int(chapter["number"])
    if chapter_number == 1:
        graph = diagram_block("chapter-01-dag", "Chapter 1 local dependency DAG.")
    elif chapter_number == 2:
        graph = diagram_block("chapter-02-dag", "Chapter 2 functional-inequality dependency DAG.")
    else:
        graph = diagram_block("shared-root-dag", "Shared ASTIS roots used across chapters.")
    body = f"""
<section class="page-hero compact chapter-hero">
  <div class="eyebrow">Chapter {int(chapter["number"]):02d} · source pp. {esc(chapter["source_pages"])}</div>
  <h1>{esc(chapter["title"])}</h1>
  <p class="lede">{esc(chapter["goal"])}</p>
  <div class="tag-row">{chapter_status_badge(str(chapter["status"]))}{''.join(f'<span>{esc(c)}</span>' for c in chapter["concepts"])}</div>
</section>
<nav class="in-page-nav" aria-label="Chapter sections">
  <a href="#guide">Guide</a><a href="#calculation">Calculation Route</a>
  <a href="#details">Rigorous Details</a><a href="#lean">Lean Foundations</a>
  <a href="#source-map">Source map</a><a href="#dependencies">Dependencies</a>
</nav>
<section id="guide" class="two-column">
  <div><h2>Chapter guide</h2><h3>Prerequisites</h3>{list_html(chapter["prerequisites"])}
  <h3>Recommended order</h3>{list_html(chapter["recommended_order"])}</div>
  <div><h2>Source sections</h2>{list_html(chapter["source_sections"])}
  <h3>Core concepts</h3>{list_html(chapter["concepts"])}</div>
</section>
<section class="two-column chapter-essentials">
  <div><div class="section-heading"><span>Vocabulary</span><h2>Core definitions</h2></div>{list_html(chapter["core_definitions"])}</div>
  <div><div class="section-heading"><span>Destination</span><h2>Major results</h2></div>{list_html(chapter["major_results"])}</div>
</section>
<section id="calculation">
  <div class="section-heading"><span>Depth 01</span><h2>Calculation Route</h2></div>
  <p class="section-intro">This is the shortest faithful route through the chapter's main proof calculations.</p>
  <div class="calculation-route">{route}</div>
</section>
<section id="details">
  <div class="section-heading"><span>Depth 02</span><h2>Why these steps are valid</h2></div>
  <div class="detail-grid">{''.join(f'<article><span>{i:02d}</span><p>{esc(detail)}</p></article>' for i, detail in enumerate(chapter["rigorous_details"], 1))}</div>
  <aside class="pitfall"><strong>Strict boundary.</strong> A concise textbook calculation is not promoted to a blue Lean result until its regularity, measurability, integrability, boundary, representative, and domain contracts have compiled.</aside>
</section>
<section id="lean">
  <div class="section-heading"><span>Depth 03</span><h2>Lean Foundations</h2></div>
  <p>The links below are the nearest existing ASTIS modules. A listed module is not a claim that every result in this chapter is complete.</p>
  <div class="module-links">{''.join(module_links)}</div>
</section>
<section id="source-map">
  <div class="section-heading"><span>Correspondence</span><h2>Book → exposition → detail packet → Lean</h2></div>
  <div class="source-grid">{''.join(mappings) if mappings else '<p class="note">This chapter is present in the textbook spine; fine-grained source entries are still being added and are not represented as compiled results.</p>'}</div>
</section>
<section id="dependencies">
  <div class="section-heading"><span>Architecture</span><h2>Dependencies and consumers</h2></div>
  {graph}
  <div class="two-column">
    <div><h3>Current red blockers</h3>{list_html(chapter["blockers"])}</div>
    <div><h3>Downstream consumers</h3>{list_html(chapter["consumers"])}</div>
  </div>
</section>
"""
    return page(
        f"Chapter {chapter['number']}: {chapter['title']}",
        f"textbook/{chapter['id']}.html",
        body,
        active="Textbook",
        description=str(chapter["goal"]),
    )


def render_textbook_chapter(
    chapter: dict[str, object],
    edition_chapter: dict[str, object],
    source_entries: list[dict[str, object]],
    entries_by_decl: dict[str, RegistryEntry],
) -> str:
    number = int(chapter["number"])
    sections = [dict(section) for section in edition_chapter["sections"]]
    first = sections[0]
    chapter_pdf_page = int(edition_chapter["book_page"]) + int(_SOURCE_EDITION["body_pdf_page_offset"])
    chapter_source_url = f'{_SOURCE_EDITION["canonical_url"]}#page={chapter_pdf_page}'
    section_rows = "".join(
        f"""<li><a href="chapter-{number:02d}/section-{slugify(str(section['id']))}.html">
  <span>{esc(section['id'])}</span><strong>{esc(section['title'])}</strong><small>Book p. {section['book_page']}</small>
</a></li>"""
        for section in sections
    )
    mapped = chapter_source_entries(number, source_entries)
    canonical_chapters = [dict(item) for item in _SOURCE_EDITION["chapters"]]
    previous_chapter = canonical_chapters[number - 2] if number > 1 else None
    next_chapter = canonical_chapters[number] if number < len(canonical_chapters) else None

    def chapter_nav(item: dict[str, object] | None, direction: str) -> str:
        if item is None:
            return '<span></span>'
        target_number = int(item["number"])
        return (
            f'<a class="reader-{direction}" href="chapter-{target_number:02d}.html">'
            f'<span>{direction.title()} chapter</span><strong>{target_number}. {esc(item["title"])}</strong></a>'
        )
    formalization_rows = []
    for source in mapped:
        links = []
        for declaration in source["lean_declarations"]:
            entry = entries_by_decl.get(str(declaration))
            if entry:
                links.append(f'<a class="decl-link" href="../theorems/{entry.slug}.html">{esc(entry.short_name)}</a>')
        formalization_rows.append(
            f'<article><strong>{esc(source["source_kind"])}</strong><p>{esc(source["source_summary"])}</p>'
            f'<div class="decl-links">{"".join(links) if links else "No local declaration is mapped yet."}</div></article>'
        )
    body = f"""
<article class="textbook-reader chapter-opening">
  <header class="reader-header">
    <div class="reader-kicker">Chapter {number} · Book pp. {esc(chapter['source_pages'])} · August 9, 2026 edition</div>
    <h1>{esc(chapter['title'])}</h1>
    <p class="reader-lede">{esc(chapter['goal'])}</p>
    <a class="button primary" href="chapter-{number:02d}/section-{slugify(str(first['id']))}.html">Begin with {esc(first['id'])}</a>
    <a class="source-anchor" href="{esc(chapter_source_url)}">Open this chapter in the canonical August 9 source ↗</a>
  </header>
  <section id="calculation" class="reader-prose">
    <h2>Chapter route</h2>
    <p>This chapter develops {esc(', '.join(str(item) for item in chapter['concepts'][:4]))}. Its main destination is to connect the definitions below to the results that later chapters consume.</p>
    <div class="reader-columns"><div><h3>Core definitions</h3>{list_html(chapter['core_definitions'])}</div>
    <div><h3>Main results</h3>{list_html(chapter['major_results'])}</div></div>
    <h2>Contents</h2>
    <ol class="section-contents">{section_rows}</ol>
  </section>
  <details id="details" class="reader-disclosure rigor-disclosure"><summary>Why is this chapter route valid?</summary>
    <div class="disclosure-body"><h3>Analytic contracts</h3>{list_html(chapter['rigorous_details'])}<h3>Open boundaries</h3>{list_html(chapter['blockers'])}</div>
  </details>
  <details id="lean" class="reader-disclosure lean-disclosure"><summary>View Lean formalization</summary>
    <div class="disclosure-body"><p>These mappings are evidence links, not a claim that the entire chapter is formalized.</p>{''.join(formalization_rows) if formalization_rows else '<p>No declaration-level source block is mapped for this chapter yet.</p>'}</div>
  </details>
  <nav class="reader-pagination" aria-label="Adjacent chapters">{chapter_nav(previous_chapter, 'previous')}{chapter_nav(next_chapter, 'next')}</nav>
</article>
"""
    return page(
        f"Chapter {number}: {chapter['title']}",
        f"textbook/chapter-{number:02d}.html",
        body,
        active=f"Textbook:{number}",
        description=str(chapter["goal"]),
    )


def render_textbook_section(
    chapter: dict[str, object],
    section: dict[str, object],
    guide: str,
    source_entries: list[dict[str, object]],
    entries_by_decl: dict[str, RegistryEntry],
    previous: dict[str, object] | None,
    following: dict[str, object] | None,
) -> str:
    number = int(chapter["number"])
    section_id = str(section["id"])
    rel_path = textbook_section_path(number, section_id)
    prefix = relative_prefix(rel_path)
    pdf_page = int(section["book_page"]) + int(_SOURCE_EDITION["body_pdf_page_offset"])
    source_url = f'{_SOURCE_EDITION["canonical_url"]}#page={pdf_page}'
    mapped = [row for row in source_entries if str(row["section"]) == section_id]
    kind = str(section.get("kind", "section"))
    if not guide:
        if kind == "notes":
            guide = "The bibliographical notes identify the papers and books behind this chapter's arguments and indicate where stronger or more technical versions can be found."
        elif kind == "exercises":
            guide = "The exercises test the chapter's definitions, proof calculations, edge cases, and extensions without changing the chapter's formalization status."
        else:
            guide = f"This section advances the chapter goal: {chapter['goal']}"

    rendered_blocks = []
    for source in mapped:
        formula = (
            f'<div class="formula source-formula">\\[{esc(source["latex_statement"])}\\]</div>'
            if source.get("latex_statement") else ""
        )
        rigor = (
            f'<article><p>{esc(source["rigorous_packet"])}</p>'
            f'<h4>Source assumptions</h4>{list_html(source["source_assumptions"])}'
            f'<h4>Formal assumptions</h4>{list_html(source["formal_assumptions"])}</article>'
        )
        declaration_details = []
        for declaration in source["lean_declarations"]:
            entry = entries_by_decl.get(str(declaration))
            if entry:
                source_declaration = _SOURCE_BY_NAME.get(entry.local_decl)
                source_module = next(
                    (module for module in _ALL_MODULES if source_declaration and module.name == source_declaration.module),
                    None,
                )
                dependencies = [
                    f'<a href="{prefix}theorems/{entries_by_decl[name].slug}.html"><code>{esc(entries_by_decl[name].short_name)}</code></a>'
                    for name in entry.dependencies if name in entries_by_decl
                ]
                declaration_details.append(
                    f'<article class="inline-lean"><h4><a href="{prefix}theorems/{entry.slug}.html"><code>{esc(entry.local_decl)}</code></a></h4>'
                    f'<div class="card-meta">{esc(status_label(entry))} · {esc(entry.source_file)}:{entry.source_line}</div>'
                    f'{code_html(entry.source_text)}<h5>Imports</h5>'
                    f'{list_html(source_module.imports if source_module else [], empty="No project import metadata resolved.")}'
                    f'<h5>Local dependencies</h5><div class="decl-links">{"".join(dependencies) if dependencies else "No Registry dependency inferred."}</div></article>'
                )
            else:
                declaration_details.append(f'<span class="status status-orange">unresolved metadata: {esc(declaration)}</span>')
        lean = (
            f'<article><div class="card-meta">{esc(source["status"])} · {esc(source["wording_status"])}</div>'
            f'<p>{esc(source["astis_exposition"])}</p>'
            f'{"".join(declaration_details) if declaration_details else "<p>No ASTIS-owned declaration is mapped yet.</p>"}'
            f'<h4>Downstream consumers</h4>{list_html(source["downstream_consumers"])}</article>'
        )
        rendered_blocks.append(
            f'<article class="textbook-block"><section class="source-passage"><div class="passage-label">{esc(source["source_kind"])}</div>'
            f'<h2>{esc(source["source_summary"])}</h2><p>{esc(source["mathematical_exposition"])}</p>{formula}</section>'
            f'<details class="reader-disclosure rigor-disclosure"><summary>Why is this valid?</summary><div class="disclosure-body">{rigor}</div></details>'
            f'<details class="reader-disclosure lean-disclosure"><summary>View Lean formalization</summary><div class="disclosure-body">{lean}</div></details></article>'
        )
    if not rendered_blocks:
        rendered_blocks.append(
            '<article class="textbook-block"><section class="source-passage"><h2>Place in the proof route</h2>'
            f'<p>The chapter uses this material in the route toward {esc(str(chapter["major_results"][0]))} '
            'The declaration-level source map is intentionally left inside the formalization layer until exact theorem anchors have been audited.</p></section>'
            f'<details class="reader-disclosure rigor-disclosure"><summary>Why is this valid?</summary><div class="disclosure-body"><h3>Chapter-level validity conditions</h3>{list_html(chapter["rigorous_details"])}</div></details>'
            '<details class="reader-disclosure lean-disclosure"><summary>View Lean formalization</summary><div class="disclosure-body"><p>No declaration-level mapping has been accepted for this section. This is a route status, not a failed Lean declaration.</p></div></details></article>'
        )

    def nav_link(item: dict[str, object] | None, direction: str) -> str:
        if item is None:
            return '<span></span>'
        label = f"{item['id']} {item['title']}"
        return f'<a class="reader-{direction}" href="{prefix}{item["path"]}"><span>{direction.title()}</span><strong>{esc(label)}</strong></a>'

    body = f"""
<article class="textbook-reader section-reading">
  <nav class="reader-breadcrumb" aria-label="Breadcrumb"><a href="{prefix}textbook/index.html">Log-Concave Sampling</a><span>/</span><a href="../chapter-{number:02d}.html">Chapter {number}</a></nav>
  <header class="reader-header">
    <div class="reader-kicker">{esc(section_id)} · Book p. {section['book_page']} · PDF p. {pdf_page}</div>
    <h1>{esc(section['title'])}</h1>
    <p class="reader-lede">{esc(guide)}</p>
    <a class="source-anchor" href="{esc(source_url)}">Open this section in the canonical August 9 source ↗</a>
  </header>
  <div class="reader-prose">{''.join(rendered_blocks)}</div>
  <nav class="reader-pagination" aria-label="Adjacent sections">{nav_link(previous, 'previous')}{nav_link(following, 'next')}</nav>
</article>
"""
    return page(
        f"{section_id} {section['title']}",
        rel_path,
        body,
        active=f"Textbook:{section_id}",
        description=guide,
    )


def render_calculation_route(chapters: list[dict[str, object]]) -> str:
    rows = []
    for chapter in chapters:
        first = chapter["calculation_route"][0]
        rows.append(
            f"""<article class="route-row">
  <div class="chapter-index">{int(chapter["number"]):02d}</div>
  <div><h2><a href="textbook/{esc(chapter["id"])}.html#calculation">{esc(chapter["title"])}</a></h2>
  <p>{esc(chapter["goal"])}</p><div class="formula compact-formula">\\[{esc(first["formula"])}\\]</div></div>
</article>"""
        )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Depth 01</div>
<h1>Calculation Route</h1>
<p class="lede">The mathematical spine: what to calculate, in which order, and why the result matters downstream. Open Depth 02 only when you need to audit a suppressed condition.</p></section>
{diagram_block("learning-path", "Recommended progressive-disclosure reading path.")}
<section class="route-list">{''.join(rows)}</section>
"""
    return page("Calculation Route", "calculation-route.html", body)


def render_rigorous_details(chapters: list[dict[str, object]]) -> str:
    categories = {
        "Measure and representatives": [
            "Measurability and strong measurability are stated for the actual codomain.",
            "Almost-everywhere representatives are fixed before applying pointwise calculus.",
            "Normalization, absolute continuity, and zero-density conventions are explicit."
        ],
        "Integrals and limits": [
            "Every Bochner integral has a proved Integrable hypothesis.",
            "Dominating functions are independent of the limiting parameter and integrable.",
            "Tonelli, Fubini, and interchange of limits identify their exact hypotheses."
        ],
        "Calculus and support": [
            "Genuine differentiability is separated from totalized fderiv values.",
            "Support, topological support, and compact support are not interchanged.",
            "Cutoff-gradient and main-term limits are proved as independent edges."
        ],
        "Operators and stochastic laws": [
            "A formal differential expression is not a closed generator.",
            "Core symmetry is not automatically symmetry on the generator domain.",
            "Stationary densities, stationary solutions, and invariant semigroup laws remain distinct."
        ]
    }
    cards = "".join(
        f"<article><h2>{esc(title)}</h2>{list_html(items)}</article>"
        for title, items in categories.items()
    )
    chapter_details = "".join(
        f"""<details><summary>Chapter {int(ch["number"])} · {esc(ch["title"])}</summary>
{list_html(ch["rigorous_details"])}
<a href="textbook/{esc(ch["id"])}.html#details">Open chapter detail layer →</a></details>"""
        for ch in chapters
    )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Depth 02</div>
<h1>Rigorous Details</h1><p class="lede">This layer answers the question a phrase such as “by approximation” leaves open: exactly which hypotheses make the step legal?</p></section>
<section class="detail-category-grid">{cards}</section>
<section><div class="section-heading"><span>Audit by chapter</span><h2>Hidden mathematical contracts</h2></div>
<div class="details-stack">{chapter_details}</div></section>
<section class="note"><h2>No promotion by prose</h2><p>A complete explanation can document a red node, but it does not make the node blue. Blue status is reserved for an ASTIS-owned declaration resolved in the source Registry and covered by the local Lean build gate.</p></section>
"""
    return page("Rigorous Details", "rigorous-details.html", body)


def render_lean_foundations(entries: list[RegistryEntry]) -> str:
    featured_names = [
        "radialSmoothCutoff_contDiff",
        "radialSmoothCutoff_fderiv_bound",
        "radialSmoothCutoff_hasCompactSupport",
        "radialSmoothCutoff_tendsto_one",
        "hasFDerivAt_radialSmoothCutoff_comp_toLp",
        "tendsto_integral_norm_fderiv_radialSmoothCutoff_comp_toLp_apply",
        "tendsto_integral_radialSmoothCutoff_comp_toLp_smul",
        "finiteEuclidean_langevinGenerator_basisDisplay",
    ]
    featured = [entry for name in featured_names for entry in entries if entry.short_name == name]
    cards = "".join(
        f"""<article class="theorem-mini">
  {badge(status_label(entry), status_class(entry))}
  <h3><a href="theorems/{entry.slug}.html"><code>{esc(entry.short_name)}</code></a></h3>
  <p>{esc(entry.note or entry.docstring or entry.sald_use)}</p>
  <span class="file-ref">{esc(entry.source_file)}:{entry.source_line}</span>
</article>"""
        for entry in featured
    )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Depth 03</div>
<h1>Lean Foundations</h1><p class="lede">Read the formalization as mathematics with explicit interfaces—not as an undifferentiated code dump.</p></section>
<section class="two-column">
  <div><h2>How to read a card</h2>
  <ol><li>Read the plain-language role and strict non-claims.</li>
  <li>Compare the exact Lean statement with the source correspondence.</li>
  <li>Inspect typeclasses and Mathlib-facing vocabulary.</li>
  <li>Follow ASTIS dependencies down and consumers up.</li>
  <li>Confirm Registry and test/build status.</li></ol></div>
  <div class="note"><h2>What “blue” means</h2><p>The declaration is ASTIS-owned, has status <code>formalizedLocal</code> in the compiled Lean Registry, resolves to a real source declaration, and is covered by <code>lake build Tests</code>. External code and prose-only nodes never become blue.</p></div>
</section>
<section><div class="section-heading"><span>Chapter 1 packet</span><h2>Cutoff-to-generator foundations</h2></div>
<div class="theorem-grid">{cards}</div></section>
{diagram_block("cutoff-packet", "The local theorem packet from a scalar profile to the generic vector cutoff-gradient limit.")}
<section class="note"><h2>Totalized APIs</h2><p>Mathlib defines <code>fderiv</code> everywhere, returning a default value when differentiability is unavailable. Therefore, an identity involving totalized <code>fderiv</code> is not evidence of genuine differentiability. ASTIS cards explicitly record when a theorem supplies <code>HasFDerivAt</code> or <code>DifferentiableAt</code>.</p></section>
"""
    return page("Lean Foundations", "lean-foundations.html", body)


def source_status_badge(status: str) -> str:
    if status == "compiled":
        return badge("compiled mapping", "blue")
    if status == "partial":
        return badge("partial mapping", "yellow")
    return badge("red source edge", "red")


def expand_chapter_1_matrix(
    raw: dict[str, object],
    source_entries: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Enrich schema-v2 item evidence for the generated reader."""
    source_by_id = {str(row["id"]): row for row in source_entries}
    items: list[dict[str, object]] = []
    status_labels = {
        "complete": "Compiled",
        "partial": "Partial",
        "planned": "Planned",
        "blocked": "Blocked",
        "external": "External",
    }
    for raw_item in raw.get("items", []):
        item = dict(raw_item)
        source_id = str(item.get("source_correspondence_id", ""))
        source = source_by_id.get(source_id, {})
        declarations = list(item.get("required_declarations", []))
        blockers = list(item.get("residual_blockers", []))
        status = str(item.get("coverage_status", "planned"))
        book_page = int(item["book_page"])
        pdf_page = int(item["pdf_page"])
        category = str(item["category"])
        number = str(item["number"])
        items.append({
            **item,
            "id": f"chapter1-{category}-{slugify(number)}",
            "page": f"book {book_page} / PDF {pdf_page}",
            "source_url": f"{raw['canonical_url']}#page={pdf_page}",
            "source_summary": str(item["title"]),
            "local_declarations": declarations,
            "missing_dependency_ready_leaves": blockers,
            "local_status": "Compiled" if declarations else "Planned",
            "route_status": status_labels.get(status, "Planned"),
            "exact_residual_blocker": (
                "; ".join(str(value) for value in blockers)
                if blockers else "None for this source item."
            ),
            "source_mapping_id": source_id,
            "downstream_consumers": list(item.get(
                "downstream_consumers", source.get("downstream_consumers", [])
            )),
        })
    return items


def render_chapter_1_matrix(items: list[dict[str, object]]) -> str:
    counts = Counter(str(item["category"]) for item in items)
    local_counts = Counter(str(item["local_status"]) for item in items)
    rows = []
    for item in items:
        declarations = item["local_declarations"]
        declaration_html = (
            f"<strong>{len(declarations)}</strong> Registry declarations"
            if declarations else '<span class="muted">No exact local mapping yet</span>'
        )
        rows.append(f"""<tr id="{esc(item['id'])}" data-search="{esc(' '.join([str(item['number']), str(item['source_kind']), str(item['source_summary'])]).lower())}" data-status="{esc(item['category'])}">
  <td><a href="{esc(item['source_url'])}"><strong>{esc(item['source_kind'])}</strong></a><small>{esc(item['page'])}</small></td>
  <td>{esc(item['source_summary'])}</td>
  <td>{route_badge(str(item['local_status']))}<br>{declaration_html}</td>
  <td>{route_badge(str(item['route_status']))}</td>
  <td><details><summary>Exact blocker</summary><p>{esc(item['exact_residual_blocker'])}</p><h4>Formal assumptions</h4>{list_html(item['formal_assumptions'])}</details></td>
</tr>""")
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Chapter 1 · source-complete audit</div>
<h1>Chapter 1 Completion Matrix</h1><p class="lede">Every numbered statement, numbered displayed identity, and exercise in the August 9, 2026 source edition. Local compilation and full mathematical-route completion are tracked separately.</p></section>
<section class="metric-row standalone">
  <div><strong>{counts['statement']}</strong><span>numbered statements</span></div>
  <div><strong>{counts['displayed_identity']}</strong><span>displayed identities</span></div>
  <div><strong>{counts['exercise']}</strong><span>exercises</span></div>
  <div><strong>{local_counts['Compiled']}</strong><span>items with compiled local evidence</span></div>
</section>
<section class="callout"><strong>Status rule.</strong> A blue local declaration does not turn a theorem route blue. Concrete process construction, topology, domains, regularity, or source-level consumers remain visible in the blocker column.</section>
<section class="toolbar table-toolbar">
  <label>Search <input id="implementation-search" type="search" placeholder="Ito formula, 1.2.21, Wasserstein…"></label>
  <label>Category <select id="implementation-status"><option value="">All</option><option value="statement">Statements</option><option value="displayed_identity">Displayed identities</option><option value="exercise">Exercises</option></select></label>
</section>
<div class="table-wrap"><table id="implementation-table"><thead><tr><th>Source</th><th>Faithful summary</th><th>Local status</th><th>Route status</th><th>Rigor boundary</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
"""
    return page("Chapter 1 Completion Matrix", "textbook/chapter-01-matrix.html", body, active="Chapter 1 Matrix")


def render_source_correspondence(
    source_entries: list[dict[str, object]],
    entries_by_decl: dict[str, RegistryEntry],
) -> str:
    rows = []
    for source in source_entries:
        decl_links = []
        for decl in source["lean_declarations"]:
            entry = entries_by_decl.get(str(decl))
            if entry:
                decl_links.append(
                    f'<a href="theorems/{entry.slug}.html"><code>{esc(entry.short_name)}</code></a>'
                )
            else:
                decl_links.append(f'<span class="status status-orange">{esc(decl)} unresolved</span>')
        rows.append(
            f"""<article id="{esc(source["id"])}" class="correspondence-card" data-status="{esc(source["status"])}" data-chapter="{int(source["chapter"])}">
  <header><div><span class="eyebrow">Chapter {int(source["chapter"])} · §{esc(source["section"])} · p. {esc(source["page"])}</span>
  <h2>{esc(source["source_kind"])}</h2></div>{source_status_badge(str(source["status"]))}</header>
  <div class="correspondence-flow">
    <div><h3>Source</h3><p>{esc(source["source_summary"])}</p><span class="wording">{esc(source["wording_status"])}</span></div>
    <div><h3>ASTIS exposition</h3><p>{esc(source["astis_exposition"])}</p></div>
    <div><h3>Rigorous packet</h3><p>{esc(source["rigorous_packet"])}</p></div>
    <div><h3>Lean</h3><div class="decl-links">{''.join(decl_links) if decl_links else '<span class="muted">No owned declaration yet.</span>'}</div></div>
  </div>
  <details><summary>Assumptions and consumers</summary>
    <div class="two-column"><div><h3>Source assumptions</h3>{list_html(source["source_assumptions"])}</div>
    <div><h3>Formal assumptions</h3>{list_html(source["formal_assumptions"])}</div></div>
    <h3>Downstream consumers</h3>{list_html(source["downstream_consumers"])}
  </details>
  <a class="source-anchor" href="{esc(source["source_url"])}">Open exact book anchor ↗</a>
</article>"""
        )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Traceable reconstruction</div>
<h1>Source Correspondence</h1><p class="lede">Every entry distinguishes Chewi's source, ASTIS paraphrase, ASTIS supplemental proof obligations, and compiled Lean declarations.</p></section>
{diagram_block("source-to-lean", "One-way provenance and two-way navigation between the book and the formalization.")}
<section class="toolbar" aria-label="Source correspondence filters">
  <label>Search <input id="card-search" type="search" placeholder="generator, Girsanov, p. 24…"></label>
  <label>Status <select id="status-filter"><option value="">All</option><option value="partial">Partial</option><option value="todo">Todo</option></select></label>
</section>
<section id="filterable-cards" class="correspondence-list">{''.join(rows)}</section>
"""
    return page("Source Correspondence", "source-correspondence.html", body, active="Source map")


def render_implementation_map(entries: list[RegistryEntry]) -> str:
    rows = []
    for entry in entries:
        dependencies = len(entry.dependencies)
        consumers = len(entry.consumers)
        rows.append(
            f"""<tr data-status="{status_class(entry)}" data-search="{esc(' '.join([entry.local_decl, entry.key, entry.upstream_decl, entry.upstream_file, ' '.join(entry.tags)]).lower())}">
  <td>{badge(status_label(entry), status_class(entry))}</td>
  <td><a href="../theorems/{entry.slug}.html"><code>{esc(entry.local_decl or entry.key)}</code></a><small>{esc(entry.key)}</small></td>
  <td>{esc(entry.source_file)}{f':{entry.source_line}' if entry.source_line else ''}</td>
  <td>{dependencies}</td><td>{consumers}</td>
  <td>{''.join(f'<span class="mini-tag">{esc(tag)}</span>' for tag in entry.tags[:5])}</td>
</tr>"""
        )
    counts = Counter(status_class(entry) for entry in entries)
    body = f"""
<section class="page-hero compact"><div class="eyebrow">All Registry entries</div>
<h1>Implementation Map</h1><p class="lede">A generated map from mathematical topic and Registry record to declaration, file, dependencies, consumers, source, and gate status.</p></section>
<section class="metric-row standalone">
  <div><strong>{counts["blue"]}</strong><span>compiled ASTIS leaves</span></div>
  <div><strong>{counts["purple"]}</strong><span>port candidates</span></div>
  <div><strong>{counts["orange"]}</strong><span>typed gaps or mismatches</span></div>
  <div><strong>{counts["gray"]}</strong><span>external references</span></div>
</section>
<section class="toolbar table-toolbar">
  <label>Search <input id="implementation-search" type="search" placeholder="declaration, tag, Mathlib source…"></label>
  <label>Status <select id="implementation-status"><option value="">All</option><option value="blue">Blue</option><option value="purple">Purple</option><option value="orange">Orange</option><option value="gray">Gray</option></select></label>
</section>
<div class="table-wrap"><table id="implementation-table">
<thead><tr><th>Status</th><th>Declaration / Registry key</th><th>Lean file</th><th>Deps</th><th>Consumers</th><th>Tags</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
"""
    return page("Implementation Map", "implementation-map/index.html", body, active="Implementation")


def inferred_natural_statement(entry: RegistryEntry) -> str:
    if entry.docstring:
        return re.sub(r"\s+", " ", entry.docstring).strip()
    if entry.note:
        return entry.note
    return entry.sald_use or "No separate natural-language statement is recorded."


def lean_vocabulary(entry: RegistryEntry) -> list[str]:
    vocabulary = {
        "Integrable": "Bochner integrability: strong measurability plus finite integral norm",
        "IntegrableOn": "integrability restricted to a measurable-set interface",
        "Tendsto": "filter-level convergence with an explicit source and target filter",
        "HasFDerivAt": "a genuine Fréchet derivative at the stated point",
        "DifferentiableAt": "genuine differentiability, stronger than inspecting totalized fderiv",
        "fderiv": "Mathlib's totalized Fréchet-derivative value",
        "ContinuousLinearMap": "a bounded linear map carrying the derivative",
        "EuclideanSpace": "Mathlib's PiLp-wrapped finite Euclidean space",
        "WithLp": "the wrapper controlling the Lp norm instance",
        "Measure": "an explicit measure parameter or instance",
        "volume": "Lebesgue/Haar volume in the ambient finite-dimensional space",
        "ae": "an almost-everywhere proposition relative to a measure",
        "ENNReal": "extended nonnegative real values used by lintegrals",
        "HasCompactSupport": "compactness of the topological support",
        "Function.support": "the pointwise nonzero set, before topological closure",
        "ContinuousOn": "continuity restricted to a set",
        "ContDiff": "iterated Fréchet differentiability to the stated order",
    }
    return [
        f"{token}: {meaning}"
        for token, meaning in vocabulary.items()
        if token in entry.source_text
    ]


def proof_walkthrough(entry: RegistryEntry) -> list[str]:
    source = entry.source_text
    steps = [
        "Read the quantified variables and typeclass brackets as part of the mathematical statement; inferred arguments are not missing assumptions."
    ]
    tactic_meanings = [
        ("intro", "introduces quantified hypotheses into the local proof context"),
        ("have", "creates a named intermediate mathematical fact"),
        ("calc", "records an equality or inequality chain matching a paper calculation"),
        ("rw", "rewrites by an established identity"),
        ("simp", "normalizes through registered definitional and theorem rewrites"),
        ("apply", "reduces the goal to the hypotheses of a reusable theorem"),
        ("refine", "instantiates a reusable theorem while leaving explicit subgoals"),
        ("exact", "closes the current goal with an already typed term"),
        ("simpa", "closes the goal after a controlled simplification of a typed result"),
        ("filter_upwards", "moves an almost-everywhere or eventual statement into a pointwise local context"),
        ("tendsto", "uses a filter-convergence combinator rather than an informal limit"),
    ]
    found = []
    for token, meaning in tactic_meanings:
        if re.search(rf"(?<![A-Za-z0-9_']){re.escape(token)}(?![A-Za-z0-9_'])", source):
            found.append(f"`{token}` {meaning}.")
    steps.extend(found[:7])
    if len(steps) == 1:
        steps.append("The declaration is definition-like or term-style; its typed right-hand side is the proof object.")
    return steps


def hidden_contracts(entry: RegistryEntry) -> list[str]:
    text = " ".join([entry.note, entry.sald_use, " ".join(entry.tags), entry.source_text]).lower()
    contracts = []
    candidates = [
        ("measur", "Measurability is represented explicitly or must be supplied by a dependency."),
        ("integrab", "Integrability is an input or proved output; a displayed integral alone does not supply it."),
        ("fderiv", "Totalized `fderiv` values must not be read as a differentiability theorem."),
        ("differentiab", "Genuine differentiability is localized to the hypotheses shown in the Lean statement."),
        ("support", "Pointwise support, topological support, and compact support retain distinct meanings."),
        ("ae", "Almost-everywhere hypotheses depend on the stated measure and representative."),
        ("density", "Density statements retain normalization and absolute-continuity prerequisites."),
        ("gibbs", "A Gibbs expression is not automatically a probability law or an invariant law."),
        ("generator", "A formal generator display does not establish a closed operator domain."),
        ("cutoff", "A cutoff lemma does not by itself prove a whole-space integration-by-parts identity."),
        ("girsanov", "A finite cylinder identity is not automatically a path-space change-of-measure theorem."),
    ]
    for needle, statement in candidates:
        if needle in text and statement not in contracts:
            contracts.append(statement)
    return contracts[:7] or ["No additional hidden-contract keyword was inferred; the exact Lean hypotheses remain controlling."]


def theorem_card(
    entry: RegistryEntry,
    entries_by_decl: dict[str, RegistryEntry],
    source_links: list[dict[str, object]],
    teaching: dict[str, object] | None = None,
) -> str:
    deps = [
        f'<a href="{entries_by_decl[dep].slug}.html"><code>{esc(entries_by_decl[dep].short_name)}</code></a>'
        for dep in entry.dependencies if dep in entries_by_decl
    ]
    consumers = [
        f'<a href="{entries_by_decl[item].slug}.html"><code>{esc(entries_by_decl[item].short_name)}</code></a>'
        for item in entry.consumers if item in entries_by_decl
    ]
    source_declaration = _SOURCE_BY_NAME.get(entry.local_decl)
    source_url = ""
    source_label = ""
    if source_declaration:
        source_url, source_label = source_href(
            source_declaration,
            from_path=f"theorems/{entry.slug}.html",
        )
    mathlib_items = [entry.upstream_decl, entry.upstream_file]
    strict_note = (
        "This card records a compiled local declaration. Its mathematical scope is exactly the Lean statement below; "
        "the Registry note and source correspondence may describe motivation but do not strengthen it."
        if entry.is_blue else
        "This Registry record is not blue. It is an external candidate, reference, typed gap, or unresolved source mapping."
    )
    statement = entry.source_text or "-- No ASTIS-owned declaration source resolved."
    source_correspondence = [
        f'<a href="../source-correspondence.html#{esc(item["id"])}">'
        f'Chapter {int(item["chapter"])} §{esc(item["section"])} · {esc(item["source_kind"])}</a>'
        for item in source_links
    ]
    natural_statement = (
        str(teaching["plain_english"]) if teaching else inferred_natural_statement(entry)
    )
    if teaching:
        teaching_html = f"""
    <h2>Mathematical statement</h2>
    <div class="math-statement"><p>{esc(teaching["mathematical_statement"])}</p></div>
    <h2>Intuition</h2><p>{esc(teaching["intuition"])}</p>
    <h2>Conditions</h2>{list_html(teaching["assumptions"])}
    <h3>Why these conditions cannot be dropped</h3>{list_html(teaching["why_assumptions"])}
    <h2>Proof route</h2>{list_html(teaching["proof_route"])}
    <h2>Lean interface notes</h2>{list_html(teaching["lean_notes"])}
"""
    else:
        teaching_html = f"""
    <h2>Proof architecture</h2>
    <p>{esc(entry.sald_use or "The declaration is a reusable technical leaf recorded by the ASTIS registry.")}</p>
    <h3>Lean proof walkthrough</h3>{list_html(proof_walkthrough(entry))}
    <h3>Why the statement has this shape</h3>
    <p>The declaration is kept at the reusable level recorded by its Registry tags and direct consumers. Explicit measures, spaces, wrappers, and regularity hypotheses expose interfaces that paper notation often infers. A theorem card explains those interfaces but never widens the compiled statement.</p>
    <h3>Hidden assumptions and non-claims</h3>{list_html(hidden_contracts(entry))}
"""
    body = f"""
<section class="page-hero compact theorem-hero">
  <div class="eyebrow">{'Reviewed teaching declaration' if teaching else 'Registry leaf card'} · {esc(entry.key)}</div>
  <h1><code>{esc(entry.short_name)}</code></h1>
  <div>{badge(status_label(entry), status_class(entry))} {route_badge(str(teaching.get("route_status", "Not mapped")) if teaching else "Not mapped")} {'<span class="status status-green">explicit smoke test</span>' if entry.explicit_test else '<span class="status status-gray">module/build coverage</span>'}</div>
  <p class="lede">{esc(natural_statement)}</p>
</section>
<section class="theorem-layout">
  <article>
    <h2>Plain-English statement</h2>
    <p>{esc(natural_statement)}</p>
    <div class="note"><strong>Scope guard.</strong> {esc(strict_note)}</div>
    {teaching_html if teaching else ''}
    <h2>Lean statement</h2>
    {code_html(statement)}
    {f'<p class="source-links"><a href="{esc(source_url)}">Open {esc(entry.source_file)}:{entry.source_line}</a><span>{esc(source_label)}</span></p>' if source_url else ''}
    {teaching_html if not teaching else ''}
  </article>
  <aside class="theorem-sidebar">
    <section><h2>Status</h2>
      <dl><dt>Registry</dt><dd><code>{esc(entry.status)}</code></dd>
      <dt>Source resolved</dt><dd>{'yes' if entry.source_file else 'no'}</dd>
      <dt>Compiled gate</dt><dd>{'lake build Tests' if entry.is_blue else 'not blue'}</dd>
      <dt>Explicit test</dt><dd>{'yes' if entry.explicit_test else 'module/build coverage'}</dd></dl>
    </section>
    <section><h2>Location</h2><dl><dt>Namespace</dt><dd><code>{esc(entry.namespace)}</code></dd>
      <dt>File</dt><dd><code>{esc(entry.source_file or "unresolved")}</code></dd>
      <dt>Line</dt><dd>{entry.source_line or "—"}</dd></dl></section>
    <section><h2>ASTIS dependencies</h2><div class="decl-links">{''.join(deps) if deps else '<span class="muted">No dependency found by the conservative source scanner.</span>'}</div></section>
    <section><h2>Consumers</h2><div class="decl-links">{''.join(consumers) if consumers else '<span class="muted">No Registry consumer found by the conservative source scanner.</span>'}</div></section>
    <section><h2>Mathlib / external correspondence</h2>{list_html([item for item in mathlib_items if item])}</section>
    <section><h2>Lean vocabulary and typeclasses</h2>{list_html(lean_vocabulary(entry), empty="No highlighted vocabulary token was inferred; inspect the exact statement.")}</section>
    <section><h2>Source correspondence</h2><div class="decl-links">{''.join(source_correspondence) if source_correspondence else '<span class="muted">No fine-grained Chewi anchor mapped yet.</span>'}</div></section>
    <section><h2>Tags</h2><div class="tag-row">{''.join(f'<span>{esc(tag)}</span>' for tag in entry.tags)}</div></section>
  </aside>
</section>
<section class="pitfall"><strong>Common pitfall.</strong> A wrapper or display identity is not a new analytic theorem merely because it has its own Lean name. Check the statement, hypotheses, and downstream consumers before interpreting its mathematical contribution.</section>
"""
    return page(entry.short_name, f"theorems/{entry.slug}.html", body)


def module_card(module: str, rel_file: str, module_entries: list[RegistryEntry]) -> str:
    rows = "".join(
        f"""<li>{badge(status_label(entry), status_class(entry))}
<a href="../theorems/{entry.slug}.html"><code>{esc(entry.short_name)}</code></a>
<span>{esc(entry.note)}</span></li>"""
        for entry in module_entries
    )
    gh_url = f"{GITHUB_ROOT}/{rel_file}"
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Module card</div>
<h1><code>{esc(module)}</code></h1><p class="lede">{len(module_entries)} Registry declarations resolve to this Lean module.</p></section>
<section class="two-column"><div><h2>Source</h2><p><code>{esc(rel_file)}</code></p><p><a href="{esc(gh_url)}">Open module on GitHub ↗</a></p></div>
<div><h2>Status contract</h2><p>Individual declaration status is generated from the Registry and source resolution. Module presence alone does not make every planned chapter result blue.</p></div></section>
<section><h2>Declarations</h2><ul class="module-entry-list">{rows or '<li>No Registry declaration resolves to this module yet.</li>'}</ul></section>
"""
    return page(module, f"modules/{slugify(module)}.html", body)


def render_dependency_explorer(entries: list[RegistryEntry]) -> str:
    reusable = sorted(
        [entry for entry in entries if entry.is_blue],
        key=lambda item: (len(item.consumers), len(item.dependencies)),
        reverse=True,
    )[:18]
    rows = "".join(
        f"<tr><td><a href=\"theorems/{entry.slug}.html\"><code>{esc(entry.short_name)}</code></a></td><td>{len(entry.dependencies)}</td><td>{len(entry.consumers)}</td><td>{esc(', '.join(entry.tags[:4]))}</td></tr>"
        for entry in reusable
    )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Book and theorem DAGs</div>
<h1>Dependency Explorer</h1><p class="lede">Large graphs are split by function: chapter spine, shared roots, Chapter 1, current frontier, and local theorem packets.</p></section>
<section><h2>Book spine</h2>{diagram_block("chapter-spine", "Chapter-level learning dependencies.")}</section>
<section><h2>Shared-root DAG</h2>{diagram_block("shared-root-dag", "Reusable roots are displayed once and tagged by mathematical role.")}</section>
<section><h2>Chapter 1</h2>{diagram_block("chapter-01-dag", "Cutoff, integrability, weighted IBP, domains, and invariance remain separate nodes.")}</section>
<section><h2>Chapter 2</h2>{diagram_block("chapter-02-dag", "The compiled Poincare interface is separated from external criteria and downstream theorem packages.")}</section>
<section><h2>Current frontier</h2>{diagram_block("current-frontier", "The current source-derived statement-audit boundary.")}</section>
<section><h2>Cutoff theorem packet</h2>{diagram_block("cutoff-packet", "A local theorem-level DAG.")}</section>
<section><div class="section-heading"><span>Generated dependency signal</span><h2>Most reused Registry leaves</h2></div>
<p class="muted">Consumers are conservatively inferred from direct declaration-name references in ASTIS source. Namespace-qualified tactic indirection may make the count an under-approximation.</p>
<div class="table-wrap"><table><thead><tr><th>Declaration</th><th>Direct dependencies</th><th>Direct consumers</th><th>Tags</th></tr></thead><tbody>{rows}</tbody></table></div></section>
"""
    return page("Dependency Explorer", "dependency-explorer.html", body, active="Dependencies")


def render_progress(
    chapters: list[dict[str, object]],
    entries: list[RegistryEntry],
    source_entries: list[dict[str, object]],
) -> str:
    counts = Counter(status_class(entry) for entry in entries)
    source_counts = Counter(str(item["status"]) for item in source_entries)
    chapter_rows = "".join(
        f"""<tr><td>{int(ch["number"]):02d}</td><td><a href="textbook/{esc(ch["id"])}.html">{esc(ch["title"])}</a></td>
<td>{chapter_status_badge(str(ch["status"]))}</td><td>{len(ch["calculation_route"])}</td><td>{len(chapter_source_entries(int(ch["number"]), source_entries))}</td><td>{len(ch["blockers"])}</td></tr>"""
        for ch in chapters
    )
    total = len(entries)
    blue_pct = (100 * counts["blue"] / total) if total else 0
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Generated status</div>
<h1>Progress</h1><p class="lede">Registry, source resolution, chapter metadata, and source correspondence are counted independently so documentation cannot masquerade as proof.</p></section>
<section class="metric-row standalone">
  <div><strong>{counts["blue"]}</strong><span>compiled local leaves</span></div>
  <div><strong>{total - counts["blue"]}</strong><span>non-blue Registry records</span></div>
  <div><strong>{len(source_entries)}</strong><span>source anchors</span></div>
  <div><strong>{len(chapters)}</strong><span>chapters</span></div>
</section>
<section class="progress-panel">
  <div><span>Registry entries resolved as compiled ASTIS declarations</span><strong>{blue_pct:.1f}%</strong></div>
  <div class="progress-track"><span style="width:{blue_pct:.2f}%"></span></div>
  <p>This percentage describes the technical-memory Registry, not completion of Chewi's entire book.</p>
</section>
{diagram_block("progress-pipeline", "Status is generated from shared repository truth; HTML is never the status authority.")}
<section><h2>Chapter coverage</h2><div class="table-wrap"><table>
<thead><tr><th>Ch.</th><th>Chapter</th><th>Formalization status</th><th>Calculation steps</th><th>Source entries</th><th>Red blockers</th></tr></thead>
<tbody>{chapter_rows}</tbody></table></div></section>
<section class="two-column"><div><h2>Registry status</h2>
{list_html([f"Blue compiled: {counts['blue']}", f"Purple port candidates: {counts['purple']}", f"Orange typed gaps/mismatches: {counts['orange']}", f"Gray references: {counts['gray']}"])}
</div><div><h2>Source mapping status</h2>
{list_html([f"Partial: {source_counts['partial']}", f"Todo: {source_counts['todo']}", f"Compiled mappings: {source_counts['compiled']}"])}
</div></section>
"""
    return page("Progress", "progress.html", body, active="Progress")


def render_frontier(entries_by_short: dict[str, RegistryEntry]) -> str:
    cycles = [
        ("25", "253", "Radial cutoff smoothness, support, compact support, exhaustion, all-scale derivative bound, PiLp bridge, and basis-trace identity.", "historical baseline"),
        ("26", "254", "Generic L1 norm limit for the PiLp-wrapped cutoff gradient.", "compiled"),
        ("27", "255", "Source-field integrability handoff needed by the cutoff-gradient term.", "compiled"),
        ("28", "256", "Generic vector cutoff-gradient integral tends to zero.", "compiled"),
    ]
    rows = "".join(
        f"<tr><td>{cycle}</td><td>{count}</td><td>{esc(result)}</td><td>{badge(label, 'blue' if label == 'compiled' else 'gray')}</td></tr>"
        for cycle, count, result, label in cycles
    )
    blue_names = [
        "tendsto_integral_norm_fderiv_radialSmoothCutoff_comp_toLp_apply",
        "tendsto_integral_radialSmoothCutoff_comp_toLp_smul",
        "integrable_expNeg_fderivCoordinateField_of_lintegral_expNeg_ne_top_of_fderiv_norm_le",
    ]
    links = []
    for name in blue_names:
        entry = entries_by_short.get(name)
        if entry:
            links.append(f'<a href="theorems/{entry.slug}.html"><code>{esc(name)}</code></a>')
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Strict mathematical boundary</div>
<h1>Roadmap and Current Frontier</h1><p class="lede">The site preserves both the user-supplied Cycle 26 historical snapshot and the later compiled worktree truth. It does not roll the repository back.</p></section>
{diagram_block("current-frontier", "Blue nodes compile locally; red nodes remain mathematically distinct.")}
<section><h2>Cycle ledger</h2><div class="table-wrap"><table><thead><tr><th>Cycle</th><th>Registry count</th><th>Closed edge</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section class="two-column">
  <div><h2>Blue cutoff-limit leaves</h2><div class="decl-links">{''.join(links)}</div>
  <p>The website task does not alter these declarations or their proofs.</p></div>
  <div><h2>Current first red route</h2><p><strong>Concrete generator-display integrability</strong>, with weighted-score integrability isolated as a genuine missing input during the Cycle 29 statement audit.</p></div>
</section>
<section><div class="section-heading"><span>Do not merge</span><h2>Independent red nodes</h2></div>
<div class="red-node-grid">
  <article><h3>Generator-display integrability</h3><p>Connect the generic field-level packet to the actual weighted Langevin source.</p></article>
  <article><h3>Gibbs tail</h3><p>Supply the tail/normalization estimate actually consumed downstream.</p></article>
  <article><h3>Whole-space weighted IBP</h3><p>Combine finite-box cancellation and both justified limit passages.</p></article>
  <article><h3>Generator / semigroup domains</h3><p>Upgrade formal differential identities to closed-operator statements.</p></article>
  <article><h3>Invariant Gibbs law</h3><p>Connect the domain-level generator statement to the Markov semigroup.</p></article>
</div></section>
<aside class="pitfall"><strong>Deferred branch.</strong> Hessian/Laplacian \\(O(R^{{-2}})\\) is not a prerequisite for the current first-order route. It is implemented only when a concrete second-order consumer appears.</aside>
"""
    return page("Current Frontier", "frontier.html", body, active="Frontier")


def render_learn_lean(entries_by_short: dict[str, RegistryEntry]) -> str:
    examples = {
        "fderiv": "radialSmoothCutoff_fderiv_bound",
        "PiLp": "hasFDerivAt_radialSmoothCutoff_comp_toLp",
        "Integrable": "integrable_expNeg_fderivCoordinateField_of_lintegral_expNeg_ne_top_of_fderiv_norm_le",
        "Tendsto": "tendsto_integral_radialSmoothCutoff_comp_toLp_smul",
    }
    links = {
        label: (
            f'<a href="theorems/{entry.slug}.html"><code>{esc(entry.short_name)}</code></a>'
            if (entry := entries_by_short.get(name)) else "<span>entry unavailable</span>"
        )
        for label, name in examples.items()
    }
    lessons = [
        ("Implicit arguments", "Lean infers dimensions, scalar fields, measures, and instances when curly braces mark parameters as implicit. Hover mentally over every inferred object: it is still part of the theorem contract."),
        ("Namespaces", "A short theorem name is resolved inside nested namespaces. The theorem card always displays the fully qualified declaration to eliminate ambiguity."),
        ("Typeclasses", "Finite-dimensional Euclidean structure, normed spaces, measurability, and measure instances are supplied through typeclasses. These are mathematical structure, not compiler decoration."),
        ("Filters and Tendsto", "A limit theorem states a filter-level relation. In cutoff arguments, the radius tends to infinity through `atTop`; the conclusion may live in a normed vector space."),
        ("Integrable", "Mathlib's Bochner `Integrable` combines strong measurability with finite integral norm. It is stronger than the informal statement that an integral symbol looks finite."),
        ("fderiv", "The Fréchet derivative API is totalized. Use `HasFDerivAt` or `DifferentiableAt` for genuine differentiability; never infer it from a convenient value of `fderiv`."),
        ("PiLp", "`EuclideanSpace ℝ ι` is a `WithLp` wrapper around functions. Bridges between wrapped and unwrapped representations are explicit because norms and continuous linear maps see the wrapper."),
        ("Almost everywhere", "Measure-theoretic equalities are usually `=ᵐ[μ]`. Choosing a pointwise representative requires a separate argument."),
        ("Support", "`Function.support f` is the nonzero set, while topological support is its closure. Compact support is a property of the topological support."),
        ("Dominated convergence", "Pointwise convergence is only one input. The family must be measurable, and one integrable function must dominate every member almost everywhere."),
        ("Generator domains", "A formula for `Lf` on smooth functions is not yet a statement about the infinitesimal generator of a strongly continuous semigroup.")
    ]
    cards = "".join(f"<article><h2>{esc(title)}</h2><p>{esc(text)}</p></article>" for title, text in lessons)
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Sampling-first Lean guide</div>
<h1>Learn Lean Through Sampling</h1><p class="lede">Every concept below is motivated by the real ASTIS cutoff, Gibbs, generator, divergence, or convergence route.</p></section>
<section class="lesson-grid">{cards}</section>
<section><h2>Open real examples</h2><div class="example-links">
<div><strong>Fréchet derivative</strong>{links["fderiv"]}</div>
<div><strong>PiLp bridge</strong>{links["PiLp"]}</div>
<div><strong>Bochner integrability</strong>{links["Integrable"]}</div>
<div><strong>Filter limit</strong>{links["Tendsto"]}</div>
</div></section>
{diagram_block("learning-path", "Start with the proof calculation; descend into Lean only as far as the question requires.")}
"""
    return page("Learn Lean Through Sampling", "learn-lean.html", body, active="Learn Lean")


def render_attribution() -> str:
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Sources and rights</div>
<h1>Attribution and Licensing</h1><p class="lede">ASTIS distinguishes source authorship, ASTIS exposition, and ASTIS-owned Lean formalization on every correspondence page.</p></section>
<section class="attribution-grid">
  <article><h2>Sinho Chewi</h2>
  <p>ASTIS is reconstructing Sinho Chewi's <a href="{CHEWI_URL}"><em>Log-Concave Sampling</em></a>. The book is the organizing mathematical source.</p>
  <p>The public draft and author page expose no explicit license permitting wholesale republication. The site therefore uses original faithful paraphrase, precise chapter/section/page correspondence, supplemental derivations, and only necessary short quotations.</p>
  <p>Chewi does not participate in, endorse, or maintain ASTIS.</p></article>
  <article><h2>Design provenance</h2>
  <p>Automation and formalization-site influences are documented in one place so that teaching, contribution, and theorem pages can focus on ASTIS itself.</p>
  <p><a href="related-systems/index.html">Open Related Systems</a> for the complete comparison and design boundaries.</p></article>
  <article><h2>Lean and Mathlib</h2>
  <p>Formal proofs use <a href="https://lean-lang.org/">Lean</a> and <a href="https://mathlib.org/">Mathlib</a>. The theorem cards identify Mathlib-facing source declarations when the ASTIS Registry records them.</p>
  <p>Mathlib declarations remain external until an ASTIS-owned declaration compiles locally; external availability alone never earns blue status.</p></article>
  <article><h2>Other papers and repositories</h2>
  <p>External papers, textbooks, and repositories are provenance and porting sources. Their licenses remain controlling for copied material. ASTIS Registry notes and source correspondence record actual use.</p>
  <p><a href="https://github.com/facebookresearch/atlas-lean/tree/e8b31c5cb0bec89b487ce33fe525a2c0b0f8b9c6/v1">ATLAS v1</a> is pinned external declaration memory. Its CC BY-NC 4.0 academic/research-only terms remain controlling; commercial use and ML model training, fine-tuning, distillation, evaluation, or development are prohibited; indexed declarations stay external until a local ASTIS port passes the current Lean gate.</p>
  <p>No external candidate is represented as an ASTIS proof until it is owned by this repository and builds under the current toolchain.</p></article>
</section>
<section class="note"><h2>Wording labels</h2>{list_html(["licensed original: text may be reproduced under a verified license", "short quotation: a minimal attributed excerpt", "faithful paraphrase: original ASTIS wording that tracks the source", "ASTIS supplement: proof detail or derivation added by ASTIS", "Lean formalization: the exact compiled declaration"])}
</section>
"""
    return page("Attribution and Licensing", "attribution.html", body)


def render_maintenance(count: int) -> str:
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Contributor guide</div>
<h1>Build and Maintain the Site</h1><p class="lede">The site is a generated view of Lean source and reviewed route metadata, not a second proof database.</p></section>
<section class="two-column">
  <div><h2>Build and certify</h2>{code_html("python3 website/scripts/lean_gate.py\npython3 website/scripts/build_site.py\npython3 website/scripts/check_site.py", "shell")}
  <p>The ignored gate record is valid only for the exact commit and Lean-source digest that passed the canonical ASTIS check.</p></div>
  <div><h2>Private preview</h2>{code_html("export ASTIS_PREVIEW_USER='reviewer'\nexport ASTIS_PREVIEW_PASSWORD='generated-outside-git'\npython3 website/scripts/ide_server.py --port 8087", "shell")}
  <p>Credentials come only from environment variables. Forward the loopback port over SSH before opening a local Cloudflare Quick Tunnel; it is not a production deployment.</p></div>
</section>
<section id="contribute"><h2>Contributing</h2><p>This page documents site operations. The full contribution route covers mathematical scope, module ownership, source correspondence, Lean acceptance, review, and credit.</p><p><a class="button primary" href="contribute/index.html">Open the contributor guide</a></p></section>
<section><h2>Consistency checks</h2>{list_html([
  f"Registry formalizedLocal count equals the Tests baseline ({count} at this build).",
  "Every named Lean declaration and module appears in the inventory and search index.",
  "Teaching and milestone metadata may reference only existing declarations.",
  "Internal links and fragments, source links, formulas, Mermaid sources, and assets resolve.",
  "A gate banner can say passed only when evidence matches the current source digest.",
  "Public, clean, published sources use a commit SHA only when ASTIS_PUBLIC_SOURCE_LINKS=1; all other sources use checked local preview anchors."
])}</section>
<section><h2>Deployment</h2><p><code>.github/workflows/blueprint-site.yml</code> runs Lean and Tests before producing the Pages artifact. GitHub Pages must be enabled for Actions; a workflow file alone does not make a 404 deployment live.</p></section>
"""
    return page("Build and Maintenance", "maintenance.html", body)


def render_contribute(count: int) -> str:
    body = f"""
<section class="page-hero compact contribution-hero"><div class="eyebrow">Samplinglib contributor guide</div>
<h1>Move a Mathematical Result into Verified Memory</h1>
<p class="lede">Contribute a focused correction, reusable Lean leaf, textbook reconstruction, proof-route packet, diagram, or teaching improvement without blurring source mathematics, local proof evidence, and route completion.</p>
<div class="hero-actions"><a class="button primary" href="https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep/issues/new">Discuss a large change ↗</a><a class="button" href="https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep">Repository source ↗</a></div></section>
<nav class="contribution-jump" aria-label="Contributor steps"><a href="#discuss"><strong>01</strong><span>Discuss</span></a><a href="#develop"><strong>02</strong><span>Develop</span></a><a href="#verify"><strong>03</strong><span>Verify</span></a><a href="#submit"><strong>04</strong><span>Submit</span></a></nav>
<section><div class="section-heading"><span>Acceptance route</span><h2>One result, explicit ownership, independent review</h2></div>{diagram_block("contribution-route", "Accepted certificates enter Samplinglib; rejected or incomplete work returns with an exact owning layer and blocker.")}</section>
<section id="discuss" class="contribution-step"><div class="step-index">01</div><div class="step-body"><span class="eyebrow">Discuss</span><h2>Fix the scope before a large development</h2><p>Focused corrections, documentation repairs, and narrow API improvements can remain small. Open an issue before adding a theorem route, module or namespace, changing mathematical assumptions, porting a large external development, or changing the ASTIS gate.</p>
<div class="decision-band"><div><h3>Focused change</h3><p>Keep the pull request narrow and name the declaration or page being corrected.</p></div><div><h3>New route or boundary</h3><p>State the result, exact source, owner module, dependencies, and whether it is a reusable leaf or a book/paper consumer.</p></div></div></div></section>
<section id="develop" class="contribution-step"><div class="step-index">02</div><div class="step-body"><span class="eyebrow">Develop</span><h2>Search first, then work in the owning layer</h2><p>Search the <a href="../declarations/index.html">declaration catalog</a>, <a href="../implementation-map/index.html">implementation map</a>, local source, and Mathlib before creating an API. A nearby statement is reusable only when its hypotheses and semantics genuinely match.</p>
<div class="table-wrap"><table><thead><tr><th>Contribution</th><th>Canonical owner</th><th>Admission rule</th></tr></thead><tbody>
<tr><td>Reusable mathematical leaf</td><td><code>TechnicalLemmas/</code> subject module</td><td>Complete local proof; Registry only when selected for shared memory</td></tr>
<tr><td>Textbook or paper result</td><td>Consumer theorem plus exact source correspondence</td><td>Source statement, assumptions, constants, and proof boundary preserved</td></tr>
<tr><td>Open proof work</td><td>Typed ASTIS packet or paper-contribution memory</td><td>Remains Partial, Planned, Blocked, or External; never promoted by prose</td></tr>
<tr><td>Teaching or roadmap content</td><td><code>website/content/</code></td><td>May reference only real declarations; route and local status stay separate</td></tr>
<tr><td>Diagram</td><td><code>website/diagrams/*.mmd</code></td><td>Editable source, real modules/declarations, checked generated rendering</td></tr>
</tbody></table></div>
<p class="status-boundary"><strong>Two independent reports are mandatory:</strong> Local declaration status records what this checkout proves; Mathematical route/paper-reproduction status records how far the source theorem route has actually been reconstructed.</p>
<div class="contribution-rules"><p><strong>Reuse before extension.</strong> Prefer an existing Samplinglib or Mathlib declaration when it is an exact fit.</p><p><strong>Complete proof boundary.</strong> Do not use <code>sorry</code>, <code>admit</code>, hidden axioms, constants, postulates, or fake trivial closure.</p><p><strong>Preserve provenance.</strong> Keep original copyright and author notices for adapted code and record the exact source and substantive changes.</p></div></div></section>
<section id="verify" class="contribution-step"><div class="step-index">03</div><div class="step-body"><span class="eyebrow">Verify</span><h2>Run the library, harness, and website gates</h2><p>Use the Lean and Mathlib revisions pinned by this checkout. From the repository root:</p>{code_html("lake exe cache get\nLEAN_NUM_THREADS=$(nproc) lake build\npython3 tools/astis.py check\npython3 tools/astis.py harness-test\npython3 website/scripts/lean_gate.py\npython3 website/scripts/build_site.py\npython3 website/scripts/check_site.py", "shell")}
<ul class="verification-checklist"><li>The whole Lean build succeeds.</li><li>No forbidden proof placeholder or fake closure was introduced.</li><li>Imports preserve subject ownership and avoid cycles.</li><li>Sources, assumptions, constants, and endpoints are exact.</li><li>Local proof status and route status are reported independently.</li><li>New reusable leaves have focused evidence and warranted Registry metadata.</li><li>Website metadata names only declarations in this checkout.</li><li>Generated <code>_site/</code> output remains uncommitted.</li></ul>
<p class="note">This build currently records {count} compiled Registry leaves. That count is a consistency baseline, not a claim that the Log-Concave Sampling route is complete.</p></div></section>
<section id="submit" class="contribution-step"><div class="step-index">04</div><div class="step-body"><span class="eyebrow">Submit</span><h2>Make the mathematical and formal evidence reviewable</h2><p>Use the repository pull request template. Record the result and source anchor, owning module, API decisions, exact commands run, adapted-code provenance, both status layers, and every remaining obligation.</p>
<div class="review-route"><div><h3>Reviewer checks</h3><ul><li>source fidelity and hidden hypotheses;</li><li>statement or constant drift;</li><li>module ownership and duplicate APIs;</li><li>proof completeness and current gate evidence;</li><li>honest remaining mathematical frontier.</li></ul></div><div><h3>Credit</h3><p>Accepted contributions are credited in Git history and relevant source-file author headers. Co-written commits should include one <code>Co-authored-by</code> trailer per additional author.</p>{code_html("Co-authored-by: Full Name <email@example.com>", "text")}</div></div>
<div class="hero-actions"><a class="button primary" href="https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep/compare">Open a pull request ↗</a><a class="button" href="../roadmap/index.html">Inspect open milestones</a></div></div></section>
<section class="note"><h2>Acceptance principle</h2><p>Discussion and implementation can remain flexible, but admission to Samplinglib requires explicit mathematical ownership, source provenance, current Lean evidence, and an independent reviewer decision.</p></section>
"""
    return page(
        "Contribute",
        "contribute/index.html",
        body,
        active="Contribute",
        description="Contribute source-backed Lean formalizations and teaching material to ASTIS and Samplinglib",
    )


def render_related_systems() -> str:
    rows = (
        (
            "Learning Beyond Gradients",
            "https://github.com/Trinkle23897/learning-beyond-gradients",
            "Role-separated iteration, durable trial memory, summaries, and rejected-route records.",
            "ASTIS maps these ideas to upper planning, middle formalization, lower Lean work, and independent proof review; source correspondence and the compiler gate remain authoritative.",
        ),
        (
            "EoH",
            "https://github.com/FeiLiu36/EoH",
            "Population initialization, variation, selection, and archive pressure for competing routes.",
            "Population search is allowed only for fixed Lean-checkable targets in exploratoryProof; faithfulPaper cannot mutate the source theorem, assumptions, or constants.",
        ),
        (
            "ARIS",
            "https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep",
            "Long-running research loops, plain-file handoffs, and separate reviewer passes.",
            "ASTIS specializes the loop for Lean proof states, exact source anchors, analytic obligations, and reusable sampling-theory memory.",
        ),
        (
            "LeanMarathon",
            "https://github.com/YuanheZ/LeanMarathon",
            "Blueprint-driven target selection, dynamic proof-DAG leaves, bounded workers, and deterministic gates.",
            "ASTIS keeps a local source-backed harness and a separate Samplinglib memory layer instead of requiring a GitHub/PR/Slurm execution substrate.",
        ),
        (
            "MathCode",
            "https://github.com/math-ai-org/mathcode",
            "Lean diagnostics, theorem reuse, and explicit subgoal planning.",
            "Diagnostics and retrieval remain advisory; only ASTIS-owned source correspondence, local compilation, tests, and reviewer evidence can accept a result.",
        ),
        (
            "Sho Sonoda / Lean-Ridgelet",
            "https://github.com/shosonoda/lean-ridgelet",
            "Blueprint-style organization and an implementation map connecting mathematics to Lean declarations.",
            "Samplinglib uses an independently implemented generator, a full textbook route, dual status, hidden-condition packets, and sampling/SDE-specific theorem DAGs.",
        ),
        (
            "StatsMLlib",
            "https://github.com/Lean-MoDS/StatsMLlib",
            "Subject-owned Lean modules, reuse-first development, complete proofs, source attribution, and staged contribution review.",
            "Samplinglib adds textbook-route correspondence, dual local/route status, typed ASTIS packets, and reviewer-controlled admission to formal memory.",
        ),
    )
    table_rows = "".join(
        f'<tr><td><a href="{esc(url)}"><strong>{esc(name)}</strong> ↗</a></td><td>{esc(influence)}</td><td>{esc(boundary)}</td></tr>'
        for name, url, influence, boundary in rows
    )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Design context</div>
<h1>Related Systems</h1><p class="lede">ASTIS combines long-horizon research control, Lean formalization, and a sampling-theory memory library. This is the sole website page that compares those design choices with adjacent systems.</p></section>
<section><div class="section-heading"><span>Comparison boundary</span><h2>What is reused, and what remains ASTIS-specific</h2></div>
<div class="table-wrap"><table class="systems-table"><thead><tr><th>System</th><th>What informs ASTIS</th><th>ASTIS boundary</th></tr></thead><tbody>{table_rows}</tbody></table></div></section>
<section class="note"><h2>Interpretation</h2><p>These links record design provenance. They do not imply code identity, theorem equivalence, endorsement, or local Lean proof ownership. Mathematical sources and software dependencies are documented separately under Attribution.</p></section>
"""
    return page(
        "Related Systems",
        "related-systems/index.html",
        body,
        active="Related Systems",
        description="Related automation and formalization systems informing ASTIS design",
    )


def teaching_card_path(declaration: SourceDeclaration) -> str:
    stable = hashlib.sha1(declaration.full_name.encode("utf-8")).hexdigest()[:10]
    return f"declarations/{slugify(declaration.full_name)[:110]}-{stable}.html"


def declaration_path(declaration: SourceDeclaration) -> str:
    if declaration.registry_card:
        return declaration.registry_card
    if declaration.full_name in _TEACHING_BY_NAME:
        return teaching_card_path(declaration)
    return f"modules/{slugify(declaration.module)}.html#{declaration.anchor}"


def compact_source(source: str, *, max_lines: int = 44, max_chars: int = 9000) -> tuple[str, bool]:
    lines = source.splitlines()
    clipped = len(lines) > max_lines or len(source) > max_chars
    excerpt = "\n".join(lines[:max_lines])
    if len(excerpt) > max_chars:
        excerpt = excerpt[:max_chars]
    if clipped:
        excerpt = excerpt.rstrip() + "\n-- Source excerpt truncated; follow the exact source link."
    return excerpt, clipped


def annotate_declarations(
    declarations: list[SourceDeclaration],
    entries: list[RegistryEntry],
    teaching: list[dict[str, object]],
) -> None:
    registry_by_name = {entry.local_decl: entry for entry in entries if entry.local_decl}
    teaching_by_name = {str(item["declaration"]): item for item in teaching}
    for declaration in declarations:
        entry = registry_by_name.get(declaration.full_name)
        if entry:
            declaration.registry_status = entry.status
            declaration.registry_card = f"theorems/{entry.slug}.html"
        metadata = teaching_by_name.get(declaration.full_name)
        if metadata:
            declaration.route_status = str(metadata.get("route_status", "Not mapped"))
            declaration.route_note = str(metadata.get("plain_english", declaration.route_note))


def render_overview(
    chapters: list[dict[str, object]],
    modules: list[SourceModule],
    declarations: list[SourceDeclaration],
    entries: list[RegistryEntry],
    milestones: list[dict[str, object]],
    teaching: list[dict[str, object]],
) -> str:
    gate = _ACTIVE_GATE or load_gate_evidence()
    production_modules = [module for module in modules if module.role != "test"]
    local_compiled = sum(
        local_declaration_status(declaration, gate) == "Compiled"
        for declaration in declarations
        if declaration.module != "Tests" and not declaration.module.startswith("Tests.")
    )
    blocked = sum(str(item["route_status"]) == "Blocked" for item in milestones)
    body = f"""
<section class="hero overview-hero">
  <span class="eyebrow">Verified sampling theory in Lean</span>
  <h1>Samplinglib</h1>
  <p class="lede">From textbook foundations to AI-assisted formalization: learn the mathematics, inspect its hidden analytic conditions, and follow every verified result to its exact Lean declaration.</p>
  <div class="hero-actions">
    <a class="button primary" href="textbook/index.html">Read Log-Concave Sampling</a>
    <a class="button" href="live/index.html">Open Live Formalization</a>
    <a class="button" href="declarations/index.html">Browse Lean Library</a>
    <a class="button quiet" href="https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep">GitHub ↗</a>
  </div>
  <div class="metric-row">
    <div><strong>{len(production_modules)}</strong><span>Lean modules</span></div>
    <div><strong>{len(declarations)}</strong><span>declarations indexed</span></div>
    <div><strong>{len(teaching)}</strong><span>reviewed explanations</span></div>
    <div><strong>{blocked}</strong><span>named blocked routes</span></div>
  </div>
</section>
<section id="samplinglib" class="overview-band">
  <div class="section-heading"><span>Formalized library</span><h2>A reusable foundation, not a one-off book port</h2></div>
  <div class="prose-columns">
    <p>Samplinglib currently follows Sinho Chewi's <em>Log-Concave Sampling</em> as its first complete pedagogical spine. The implementation is organized into reusable measure, probability, functional-inequality, stochastic-process, Langevin, and sampling modules rather than chapter-specific monoliths.</p>
    <p>Every public status is source-synchronized. Lean declarations, Registry records, tests, source correspondence, route milestones, and the current gate digest remain distinct, so a compiled helper cannot silently mark an unfinished theorem complete.</p>
  </div>
  <p><a class="text-link" href="implementation-map/index.html">Inspect the implementation map →</a></p>
</section>
<section id="architecture" class="architecture-section">
  <div class="section-heading"><span>System and library architecture</span><h2>Formal memory connects research problems to reusable proof leaves</h2></div>
  <figure class="architecture-figure">
    <img src="assets/samplinglib-architecture.svg" alt="Samplinglib architecture from mathematical sources through ASTIS and formal memory to learning and verification surfaces">
    <figcaption>ASTIS turns source mathematics into reviewed Lean certificates; Samplinglib makes the accepted memory reusable for learning and future formalization.</figcaption>
  </figure>
</section>
<section id="three-levels">
  <div class="section-heading"><span>Learn at three levels</span><h2>Move between exposition and formal foundations</h2></div>
  <div class="depth-grid">
    <article class="depth-card calculation"><div class="depth-number">01</div><h3>Calculation Route</h3><p>Follow the formulas and proof strategy with minimal interruption.</p><a href="calculation-route.html">Read the route →</a></article>
    <article class="depth-card rigorous"><div class="depth-number">02</div><h3>Rigorous Details</h3><p>Audit measurability, integrability, limits, representatives, boundaries, and domains.</p><a href="rigorous-details.html">Open the details →</a></article>
    <article class="depth-card lean"><div class="depth-number">03</div><h3>Lean Foundations</h3><p>Inspect exact statements, dependencies, source lines, Registry evidence, and tests.</p><a href="lean-foundations.html">Browse Lean →</a></article>
  </div>
</section>
<section id="book-map">
  <div class="section-heading"><span>Book map</span><h2>Twelve connected chapters</h2></div>
  {diagram_block("chapter-spine", "The chapter map is a learning and dependency route, not a claim that every theorem is complete.")}
  <p><a class="text-link" href="learning-path/index.html">Open the guided book map →</a></p>
</section>
<section id="live-formalization" class="split live-intro">
  <div>
    <div class="section-heading"><span>Live Formalization</span><h2>Bring a mathematical statement into the verification loop</h2></div>
    <p>Render new LaTeX, retrieve related Samplinglib and Mathlib interfaces, inspect an explicit candidate Lean statement, compile it with the local pinned toolchain, and export unresolved work as an ASTIS-compatible packet.</p>
    <p class="muted">Candidate translation, Lean compilation, semantic review, proof, and reviewer acceptance are separate states.</p>
    <a class="button primary" href="live/index.html">Open the workspace</a>
  </div>
  <pre class="pipeline-code"><code>LaTeX
  ↓ semantic/source contract
Lean candidate + retrieval
  ↓ local compilation
diagnostics / proof obligation
  ↓ reviewer
Samplinglib Registry</code></pre>
</section>
<section id="powered-by-astis" class="overview-band compact-band">
  <div class="section-heading"><span>Powered by ASTIS</span><h2>A hierarchical proof system maintains the library</h2></div>
  <p>Upper agents audit mathematics and proof structure; middle agents translate the route into typed Lean leaves; lower agents prove one leaf; reviewers enforce source correspondence and the Lean certificate boundary.</p>
  {diagram_block("harness-workflow", "ASTIS maintains Samplinglib through typed artifacts, feedback, and independent gates.")}
  <p><a class="text-link" href="workflow/index.html">Read the ASTIS harness architecture →</a></p>
</section>
<section id="organizers" class="organizer-strip">
  <div><span class="eyebrow">Organizers</span><h2>Dake Bu · Ji Cheng · Huanjian Zhou · Andi Han · Zonghao Chen · Sinho Chewi · Matthew S. Zhang · Hau-San Wong · Qingfu Zhang · Atsushi Nitanda</h2></div>
  <div class="organizer-links"><a class="text-link" href="contribute/index.html">Become a contributor →</a><a class="text-link" href="attribution/index.html#citation">Citation and attribution →</a></div>
</section>
<section class="note"><h2>Build interpretation</h2><p>{esc(gate.note)} The current generated view classifies {local_compiled} production declarations as compiled only when gate evidence matches this Lean source digest. Registry count ({len(entries)}) and textbook completion are separate quantities.</p></section>
"""
    return page("Overview", "index.html", body, active="Overview")


def render_full_implementation_map(
    modules: list[SourceModule],
    declarations: list[SourceDeclaration],
    milestones: list[dict[str, object]],
) -> str:
    gate = _ACTIVE_GATE or load_gate_evidence()
    milestone_rows = "".join(
        f"""<tr>
  <td><strong>{esc(item["title"])}</strong><small>Chapter {item["chapter"] or "shared"}</small></td>
  <td>{route_badge(str(item["local_status"]))}</td>
  <td>{route_badge(str(item["route_status"]))}</td>
  <td>{esc(item["summary"])}</td>
  <td>{len(item["evidence_declarations"])}</td>
  <td>{len(item["blockers"])}</td>
</tr>"""
        for item in milestones
    )
    module_rows = []
    for module in modules:
        statuses = Counter(local_declaration_status(declaration, gate) for declaration in module.declarations)
        module_rows.append(
            f"""<tr data-search="{esc((module.name + " " + module.source_file + " " + " ".join(module.imports)).lower())}">
  <td><a href="../modules/{slugify(module.name)}.html"><code>{esc(module.name)}</code></a><small>{esc(module.source_file)}</small></td>
  <td>{esc(module.role)}</td><td>{len(module.imports)}</td><td>{len(module.declarations)}</td>
  <td>{statuses["Compiled"]}</td><td>{statuses["Stated/incomplete"]}</td>
</tr>"""
        )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Two status layers</div>
<h1>Sampling/SDE Implementation Map</h1>
<p class="lede">The declaration inventory answers “what Lean accepts locally?” The milestone ledger answers “how much of the mathematical textbook route is reproduced?” A compiled helper never promotes an incomplete chapter theorem.</p></section>
<section><h2>Status vocabulary</h2>
  <div class="status-key">
    {route_badge("Compiled")}{route_badge("Partial")}{route_badge("Stated/incomplete")}
    {route_badge("Planned")}{route_badge("Blocked")}{route_badge("External/upstream dependency")}
  </div>
</section>
<section><h2>Mathematical route and local evidence</h2>
<div class="table-wrap"><table><thead><tr><th>Milestone</th><th>Local evidence</th><th>Route status</th><th>Boundary</th><th>Evidence declarations</th><th>Blockers</th></tr></thead><tbody>{milestone_rows}</tbody></table></div></section>
<section><h2>Major theorem dependencies</h2>{diagram_block("major-theorem-dag", "A theorem DAG using declarations and open boundaries that exist in the current ASTIS route.")}</section>
<section><h2>Complete module inventory</h2>
<div class="toolbar"><label>Filter modules <input id="module-search" data-table-search="module-inventory" type="search" placeholder="Gibbs, ConditionalKernel, SALD"></label></div>
<div class="table-wrap"><table id="module-inventory"><thead><tr><th>Module</th><th>Role</th><th>Imports</th><th>Declarations</th><th>Compiled</th><th>Incomplete</th></tr></thead><tbody>{''.join(module_rows)}</tbody></table></div></section>
"""
    return page(
        "Sampling/SDE Implementation Map",
        "implementation-map/index.html",
        body,
        active="Implementation",
    )


def render_learning_path(
    chapters: list[dict[str, object]],
    teaching: list[dict[str, object]],
    declarations_by_name: dict[str, SourceDeclaration],
) -> str:
    teaching_by_chapter: dict[int, list[dict[str, object]]] = defaultdict(list)
    for item in teaching:
        teaching_by_chapter[int(item["chapter"])].append(item)
    chapter_cards = []
    for chapter in chapters:
        number = int(chapter["number"])
        interfaces = []
        for item in teaching_by_chapter.get(number, []):
            declaration = declarations_by_name[str(item["declaration"])]
            interfaces.append(
                f'<a href="../{declaration_path(declaration)}"><code>{esc(declaration.short_name)}</code></a>'
            )
        chapter_cards.append(
            f"""<article class="chapter-card">
  <div class="chapter-index">{number:02d}</div>
  <div><h2><a href="../textbook/{esc(chapter["id"])}.html">{esc(chapter["title"])}</a></h2>
  <div>{route_badge("Partial" if chapter["status"] in {"active", "partial"} else "Planned")}</div>
  <p>{esc(chapter["core_definitions"][0])}</p>
  <p class="card-meta">Prerequisites: {esc("; ".join(chapter["prerequisites"]))}</p>
  <div class="decl-links">{''.join(interfaces) if interfaces else '<span class="muted">No reviewed declaration selected yet.</span>'}</div></div>
</article>"""
        )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Guided Learning Path</div>
<h1>How to read the formalization</h1><p class="lede">Start from measures and measurable maps, then move through Gibbs laws, kernels, stochastic processes, continuous Langevin dynamics, and finally discrete sampler error. The chapter order follows the textbook, while shared Lean roots are introduced where they are first needed.</p></section>
<section><h2>Recommended path</h2>{diagram_block("learning-path", "A dependency-first reading order; it is not a claim that the later routes are formalized.")}</section>
<section class="two-column">
  <div><h2>Mathematical reading</h2>{list_html([
    "Measure and pushforward law before probability kernels.",
    "Kernels and almost-everywhere conditional representatives before stochastic-process consumers.",
    "Normalized target laws before invariance or convergence claims.",
    "Continuous-time dynamics before discretization and sampler complexity."
  ])}</div>
  <div><h2>Lean reading</h2>{list_html([
    "Read structures and definitions as interfaces, not theorem certificates.",
    "Track every explicit measure in ae, integrability, and conditional statements.",
    "Treat fderiv as totalized unless accompanied by derivative evidence.",
    "Follow imports and declaration consumers from the module pages."
  ])}</div>
</section>
<section><h2>Textbook chapter guide</h2><div class="chapter-list">{''.join(chapter_cards)}</div></section>
"""
    return page("Guided Learning Path", "learning-path/index.html", body, active="Learning path")


def render_declaration_catalog(
    declarations: list[SourceDeclaration],
) -> str:
    gate = _ACTIVE_GATE or load_gate_evidence()
    rows = []
    for declaration in declarations:
        local_status = local_declaration_status(declaration, gate)
        search = " ".join(
            [
                declaration.full_name,
                declaration.kind,
                declaration.module,
                declaration.source_file,
                declaration.docstring,
            ]
        ).lower()
        rows.append(
            f"""<tr data-search="{esc(search)}" data-kind="{esc(declaration.kind)}" data-local-status="{esc(local_status)}">
  <td><a href="../{esc(declaration_path(declaration))}"><code>{esc(declaration.full_name)}</code></a>
    <small>{esc(declaration.docstring[:220])}</small></td>
  <td>{esc(declaration.kind)}</td><td>{route_badge(local_status)}</td><td>{route_badge(declaration.route_status)}</td>
  <td><a href="../modules/{slugify(declaration.module)}.html"><code>{esc(declaration.module)}</code></a></td>
  <td><code>{esc(declaration.source_file)}:{declaration.source_line}</code></td>
</tr>"""
        )
    kinds = sorted({declaration.kind for declaration in declarations})
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Exhaustive source inventory</div>
<h1>Declaration Catalog</h1><p class="lede">Every named declaration scanned from ASTIS production roots and tests appears here. Registry leaves and 12 reviewed interfaces have richer cards; internal helpers stay concise and link to their exact module anchor.</p></section>
<section class="toolbar catalog-toolbar">
  <label>Search <input id="declaration-search" type="search" placeholder="conditional kernel, Gibbs, Tendsto"></label>
  <label>Kind <select id="declaration-kind"><option value="">All</option>{''.join(f'<option value="{esc(kind)}">{esc(kind)}</option>' for kind in kinds)}</select></label>
  <label>Local status <select id="declaration-local-status"><option value="">All</option><option>Compiled</option><option>Partial</option><option>Stated/incomplete</option></select></label>
  <span id="declaration-count" class="result-count">{len(declarations)} declarations</span>
</section>
<div class="table-wrap catalog-table"><table id="declaration-table"><thead><tr><th>Declaration</th><th>Kind</th><th>Local status</th><th>Route status</th><th>Module</th><th>Source</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
"""
    return page("Declaration Catalog", "declarations/index.html", body, active="Declarations")


def render_module_index(modules: list[SourceModule]) -> str:
    reverse_imports: Counter[str] = Counter(
        imported for module in modules for imported in module.imports
    )
    rows = "".join(
        f"""<tr data-search="{esc((module.name + " " + module.source_file + " " + " ".join(module.imports)).lower())}">
  <td><a href="{slugify(module.name)}.html"><code>{esc(module.name)}</code></a><small>{esc(module.source_file)}</small></td>
  <td>{esc(module.role)}</td><td>{len(module.imports)}</td><td>{reverse_imports[module.name]}</td><td>{len(module.declarations)}</td>
</tr>"""
        for module in modules
    )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Imports and ownership</div>
<h1>Module Pages</h1><p class="lede">The module inventory includes both root aggregators and every production/test Lean file. Each page lists imports, reverse consumers, declarations, exact source lines, and concise source excerpts.</p></section>
<section>{diagram_block("module-family-map", "Mathematical ownership follows the actual AutoSamplingTheory namespace and import surface.")}</section>
<section><div class="toolbar"><label>Filter modules <input id="module-index-search" data-table-search="module-index-table" type="search" placeholder="Probability, SDE, Measure"></label></div>
<div class="table-wrap"><table id="module-index-table"><thead><tr><th>Module</th><th>Role</th><th>Imports</th><th>Imported by</th><th>Declarations</th></tr></thead><tbody>{rows}</tbody></table></div></section>
"""
    return page("Module Pages", "modules/index.html", body, active="Modules")


def render_source_module(
    module: SourceModule,
    imported_by: list[str],
) -> str:
    gate = _ACTIVE_GATE or load_gate_evidence()
    imports = [
        f'<a href="{slugify(name)}.html"><code>{esc(name)}</code></a>'
        if any(candidate.name == name for candidate in _ALL_MODULES)
        else f'<code>{esc(name)}</code> <span class="muted">external</span>'
        for name in module.imports
    ]
    consumers = [
        f'<a href="{slugify(name)}.html"><code>{esc(name)}</code></a>'
        for name in imported_by
    ]
    declaration_blocks = []
    for declaration in module.declarations:
        excerpt, clipped = compact_source(declaration.source_text)
        local_status = local_declaration_status(declaration, gate)
        source_url, source_label = source_href(
            declaration,
            from_path=f"modules/{slugify(module.name)}.html",
        )
        detail_link = ""
        target = declaration_path(declaration)
        own_anchor = f"modules/{slugify(module.name)}.html#{declaration.anchor}"
        if target != own_anchor:
            detail_link = f'<a href="../{esc(target)}">Open detailed card</a>'
        declaration_blocks.append(
            f"""<details class="declaration" id="{esc(declaration.anchor)}">
  <summary><span class="kind">{esc(declaration.kind)}</span> <code>{esc(declaration.full_name)}</code> {route_badge(local_status)} {route_badge(declaration.route_status)}</summary>
  <div class="declaration-content">
    {f'<p class="docstring">{esc(declaration.docstring)}</p>' if declaration.docstring else '<p class="muted">No declaration docstring.</p>'}
    {code_html(excerpt)}
    <p class="source-links"><a href="{esc(source_url)}">{esc(module.source_file)}:{declaration.source_line}</a><span>{esc(source_label)}</span>{detail_link}</p>
    {f'<p class="muted">Excerpt truncated; the exact source link is authoritative.</p>' if clipped else ''}
  </div>
</details>"""
        )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">{esc(module.role)} module</div>
<h1><code>{esc(module.name)}</code></h1><p class="lede">{len(module.declarations)} named declarations scanned from <code>{esc(module.source_file)}</code>.</p></section>
<section class="module-meta">
  <div><dt>Imports</dt><dd class="decl-links">{''.join(imports) if imports else 'None'}</dd></div>
  <div><dt>Imported by</dt><dd class="decl-links">{''.join(consumers) if consumers else 'No local reverse import.'}</dd></div>
  <div><dt>Placeholder scan</dt><dd>{sum(item.has_placeholder for item in module.declarations)} declaration(s) flagged</dd></div>
  <div><dt>Gate status</dt><dd>{route_badge("Compiled" if gate.passed else "Partial")}</dd></div>
</section>
<section><h2>Declarations</h2><div class="declaration-list">{''.join(declaration_blocks) if declaration_blocks else '<p class="muted">This aggregator contains no named declarations.</p>'}</div></section>
"""
    return page(module.name, f"modules/{slugify(module.name)}.html", body, active="Modules")


def render_teaching_declaration(
    declaration: SourceDeclaration,
    teaching: dict[str, object],
) -> str:
    gate = _ACTIVE_GATE or load_gate_evidence()
    source_url, source_label = source_href(
        declaration,
        from_path=teaching_card_path(declaration),
    )
    body = f"""
<section class="page-hero compact theorem-hero">
  <div class="eyebrow">Reviewed teaching declaration</div>
  <h1><code>{esc(declaration.short_name)}</code></h1>
  <div>{route_badge(local_declaration_status(declaration, gate))}{route_badge(str(teaching["route_status"]))}</div>
  <p class="lede">{esc(teaching["plain_english"])}</p>
</section>
<section class="theorem-layout">
  <article>
    <h2>Plain-English statement</h2><p>{esc(teaching["plain_english"])}</p>
    <h2>Mathematical statement</h2><div class="math-statement"><p>{esc(teaching["mathematical_statement"])}</p></div>
    <h2>Intuition</h2><p>{esc(teaching["intuition"])}</p>
    <h2>Conditions</h2>{list_html(teaching["assumptions"])}
    <h3>Why these conditions cannot be dropped</h3>{list_html(teaching["why_assumptions"])}
    <h2>Proof route</h2>{list_html(teaching["proof_route"])}
    <h2>Lean statement</h2>{code_html(declaration.source_text)}
    <h2>Lean interface notes</h2>{list_html(teaching["lean_notes"])}
  </article>
  <aside class="theorem-sidebar">
    <section><h2>Location</h2><dl><dt>Module</dt><dd><a href="../modules/{slugify(declaration.module)}.html#{declaration.anchor}"><code>{esc(declaration.module)}</code></a></dd><dt>File</dt><dd><code>{esc(declaration.source_file)}</code></dd><dt>Line</dt><dd>{declaration.source_line}</dd></dl></section>
    <section><h2>Status boundary</h2><p>The local status reports whether this declaration is accepted by the current Lean gate. The route status reports whether the surrounding textbook theorem package is complete.</p></section>
    <section><h2>Exact source</h2><p class="source-links"><a href="{esc(source_url)}">{esc(declaration.source_file)}:{declaration.source_line}</a><span>{esc(source_label)}</span></p></section>
  </aside>
</section>
"""
    return page(
        declaration.short_name,
        teaching_card_path(declaration),
        body,
        active="Declarations",
    )


def render_roadmap(milestones: list[dict[str, object]]) -> str:
    entries = []
    for item in milestones:
        evidence = [
            f'<a href="../{declaration_path(_SOURCE_BY_NAME[name])}"><code>{esc(name.rsplit(".", 1)[-1])}</code></a>'
            for name in item["evidence_declarations"]
            if name in _SOURCE_BY_NAME
        ]
        entries.append(
            f"""<article class="status-entry status-{slugify(str(item["route_status"]))}">
  <header><div><span class="eyebrow">Chapter {item["chapter"] or "shared"}</span><h3>{esc(item["title"])}</h3></div><div>{route_badge(str(item["local_status"]))}{route_badge(str(item["route_status"]))}</div></header>
  <p>{esc(item["summary"])}</p>
  <div class="decl-links">{''.join(evidence) if evidence else '<span class="muted">No local theorem evidence is claimed.</span>'}</div>
  <h4>Open boundary</h4>{list_html(item["blockers"])}
</article>"""
        )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Progress without invented percentages</div>
<h1>Progress and Roadmap</h1><p class="lede">Milestones are categorical and evidence-backed. “Compiled” applies to local declarations. “Partial” or “blocked” records the mathematical route, including unformalized hypotheses and theorem assembly.</p></section>
<section>{diagram_block("milestone-status", "The status graph distinguishes compiled leaves, partial theorem packages, blockers, plans, and external dependencies.")}</section>
<section><h2>Milestone ledger</h2><div class="status-ledger">{''.join(entries)}</div></section>
"""
    return page("Progress and Roadmap", "roadmap/index.html", body, active="Roadmap")


def render_workflow(gate: GateEvidence) -> str:
    commands = "\n".join(gate.commands) if gate.commands else (
        "python3 website/scripts/lean_gate.py\n"
        "python3 website/scripts/build_site.py\n"
        "python3 website/scripts/check_site.py"
    )
    body = f"""
<section class="page-hero compact"><div class="eyebrow">ASTIS Automation Workflow</div>
<h1>Source-backed leaves, independent review, Lean certificates.</h1><p class="lede">The hierarchical loop coordinates mathematical source audit and Lean implementation. It does not convert an agent report, task card, or theorem-shaped data record into a proof.</p></section>
<section><div class="section-heading"><span>System architecture</span><h2>Four proving layers feed reusable formal memory</h2></div>
  <figure class="architecture-figure"><img src="../assets/samplinglib-architecture.svg" alt="ASTIS hierarchy and Samplinglib formal memory"><figcaption>Typed artifacts cross every layer; accepted certificates enter Samplinglib, while unresolved leaves return to planning.</figcaption></figure>
</section>
<section><h2>Agent execution detail</h2>{diagram_block("automation-workflow", "The concrete upper, middle, lower, and reviewer responsibilities from the current harness.")}</section>
<section class="card-grid four">
  <article class="info-card"><h3>Upper</h3><p>Audits the source theorem and shared-root DAG, selects one active leaf, and retires stale routes.</p></article>
  <article class="info-card"><h3>Middle</h3><p>Searches existing ASTIS/Mathlib interfaces, fixes the exact theorem boundary, and writes a lower-ready packet.</p></article>
  <article class="info-card"><h3>Lower</h3><p>Implements one declaration or returns one strictly smaller source-cited proof obligation with typed failure feedback.</p></article>
  <article class="info-card"><h3>Reviewer</h3><p>Runs deterministic gates, checks hidden hypotheses and source correspondence, and rejects wrapper churn or fake closure.</p></article>
</section>
<section class="two-column">
  <div><h2>Reproducible gate</h2>{code_html(commands, "shell")}<p>{esc(gate.note)}</p></div>
  <div><h2>Failure is retained</h2>{list_html([
    "Missing assumptions become explicit proof obligations.",
    "API mismatches are recorded with the attempted declaration and error class.",
    "External theorems remain upstream dependencies until ported and compiled locally.",
    "Repeated same-shape failures trigger statement review rather than silent theorem drift."
  ])}</div>
</section>
<section><h2>Paper-to-proof-leaf conversion</h2>{diagram_block("source-to-lean", "The textbook statement is decomposed through assumptions and shared roots before lower proof work begins.")}</section>
"""
    return page("ASTIS Automation Workflow", "workflow/index.html", body, active="Workflow")


def build_live_mappings(
    teaching: list[dict[str, object]],
    declarations_by_name: dict[str, SourceDeclaration],
) -> list[dict[str, object]]:
    """Build reviewed, source-resolved examples for the static workspace.

    These records are examples of the mathematical-to-Lean interface, not
    claims that merely checking a declaration proves a newly submitted formula.
    """
    mappings: list[dict[str, object]] = []
    for item in teaching:
        declaration = declarations_by_name[str(item["declaration"])]
        statement = declaration.source_text.strip()
        assumptions = [str(value) for value in item.get("assumptions", [])]
        proof_route = [str(value) for value in item.get("proof_route", [])]
        lean_notes = [str(value) for value in item.get("lean_notes", [])]
        mappings.append(
            {
                "name": declaration.full_name,
                "latex": str(item.get("mathematical_statement", "")),
                "plain_language_interpretation": str(item.get("plain_english", "")),
                "source_anchor": (
                    f"modules/{slugify(declaration.module)}.html#{declaration.anchor}"
                ),
                "imports": [declaration.module],
                "lean_statement": statement,
                "lean_source": f"import {declaration.module}\n\n#check {declaration.full_name}\n",
                "assumptions": assumptions,
                "local_candidates": [declaration.full_name],
                "mathlib_candidates": [],
                "rejected_candidates": [],
                "semantic_notes": lean_notes + [
                    "This mapping was checked against the declaration metadata and source location.",
                    "The generated #check snippet checks the existing interface; it does not prove a new instance of it.",
                ],
                "remaining_proof_obligations": proof_route,
                "statement_hash": hashlib.sha256(statement.encode("utf-8")).hexdigest(),
                "status": "candidate",
                "translation_status": "reviewed_mapping",
                "semantic_review_status": "reviewed_mapping",
                "proof_status": "existing_declaration",
                "reviewer_status": "metadata_reviewed",
            }
        )
    return mappings


def render_live_formalization(mapping_count: int) -> str:
    body = f"""
<section class="page-hero compact live-hero"><div class="eyebrow">Mathematics to a typed proof obligation</div>
<h1>Live Formalization</h1>
<p class="lede">Render a sampling-theory statement, inspect a reviewed or deterministic Lean candidate, run the pinned compiler locally, and export unresolved work into the ASTIS hierarchy.</p></section>
<section data-live-app data-live-data="../data/live-mappings.json" class="live-workspace">
  <div data-live-mode class="live-mode-banner">
    <div><strong data-live-mode-title>Checking execution mode</strong><span data-live-mode-detail>The workspace is testing for the loopback-only Lean service.</span></div>
    <a href="#capabilities">Capability boundary</a>
  </div>
  <div class="live-status-rail" aria-label="Formalization status">
    <div><span>Translation</span><strong data-status-translation class="status status-gray">Unresolved</strong></div>
    <div><span>Lean</span><strong data-status-lean class="status status-gray">Not compiled</strong></div>
    <div><span>Proof</span><strong data-status-proof class="status status-orange">Unproved</strong></div>
    <div><span>Review</span><strong data-status-review class="status status-gray">Not reviewed</strong></div>
  </div>
  <div class="live-toolbar">
    <label>Reviewed mapping<select data-live-mapping aria-label="Reviewed mapping"></select></label>
    <button type="button" data-live-load>Load</button>
    <button type="button" class="primary-action" data-live-formalize disabled>Generate candidate</button>
    <button type="button" data-live-compile disabled>Compile with Lean</button>
    <span class="toolbar-spacer"></span>
    <button type="button" data-live-export-json>Export JSON</button>
    <button type="button" data-live-export-markdown>Export Markdown</button>
  </div>
  <div class="live-grid">
    <section class="live-pane math-pane">
      <header><div><span class="pane-kicker">Source mathematics</span><h2>Statement and context</h2></div></header>
      <label>LaTeX statement<textarea data-live-latex rows="8" spellcheck="false"></textarea></label>
      <div class="latex-preview" data-live-preview aria-live="polite"></div>
      <label>Plain-language interpretation<textarea data-live-context rows="5"></textarea></label>
      <div class="field-pair">
        <label>Source anchor<input data-live-source-anchor type="text"></label>
        <label>Preferred module<input data-live-preferred-module type="text"></label>
      </div>
    </section>
    <section class="live-pane lean-pane">
      <header><div><span class="pane-kicker">Formal candidate</span><h2>Lean source</h2></div></header>
      <textarea data-live-lean class="lean-editor" rows="24" spellcheck="false" aria-label="Candidate Lean source"></textarea>
      <p class="muted">A successful compile checks this exact snippet. It does not establish source equivalence or prove an unfilled theorem.</p>
    </section>
  </div>
  <div class="live-output-grid">
    <section class="live-pane diagnostics-pane"><header><h2>Lean diagnostics <small data-live-duration></small></h2></header><pre data-live-diagnostics>Load a reviewed mapping or enter a new statement.</pre></section>
    <section class="live-pane retrieval-pane"><header><h2>Retrieval and obligations</h2></header>
      <div class="retrieval-columns">
        <div><h3>Samplinglib</h3><ul data-live-local></ul></div>
        <div><h3>Mathlib</h3><ul data-live-mathlib></ul></div>
        <div><h3>Assumptions</h3><ul data-live-assumptions></ul></div>
        <div><h3>Open obligations</h3><ul data-live-obligations></ul></div>
      </div>
      <div><h3>Semantic notes</h3><ul data-live-semantic-notes></ul></div>
    </section>
  </div>
</section>
<section id="capabilities">
  <div class="section-heading"><span>Execution boundary</span><h2>Static reading and local verification are different products</h2></div>
  <div class="table-wrap"><table class="capability-table"><thead><tr><th>Capability</th><th>Static Pages</th><th>Local verified mode</th></tr></thead><tbody>
    <tr><td>Render LaTeX and load {mapping_count} reviewed mappings</td><td>Available</td><td>Available</td></tr>
    <tr><td>Browse declaration dependencies and exact source anchors</td><td>Available</td><td>Available</td></tr>
    <tr><td>Export ASTIS typed-artifact packets</td><td>Available</td><td>Available</td></tr>
    <tr><td>Generate a deterministic candidate for supported templates</td><td>Unavailable</td><td>Available through <code>/api/formalize</code></td></tr>
    <tr><td>Execute the pinned Lean compiler</td><td>Unavailable</td><td>Available through <code>/api/compile</code></td></tr>
    <tr><td>General semantic translation or autonomous proof acceptance</td><td>Not claimed</td><td>Not claimed</td></tr>
  </tbody></table></div>
</section>
<section class="note security-note"><h2>Local execution policy</h2><p>The compiler service binds only to loopback, serializes compilation, limits request size and time, writes snippets only to a system temporary directory, and never modifies repository source. It is a developer tool, not a hardened public code-execution sandbox. Keep it behind the documented private preview path.</p></section>
<section><h2>Packet handoff</h2>{diagram_block("source-to-lean", "Exports preserve the analytic_contract, formalization_map, proof_attempt, and review boundaries consumed by ASTIS.")}</section>
"""
    return page(
        "Live Formalization",
        "live/index.html",
        body,
        active="Live Formalization",
        description="Samplinglib Live Formalization workspace for sampling-theory Lean candidates",
        extra_scripts=("assets/ide.js",),
    )


def render_attribution_index(git: GitContext) -> str:
    citation = """@misc{bu2026astis,
  title        = {Auto-Sampling-Theory-In-Sleep: A Hierarchical Automated
                  Theorem Proving System for Sampling Theory},
  author       = {Dake Bu and Ji Cheng and Huanjian Zhou and Andi Han and
                  Zonghao Chen and Sinho Chewi and Matthew S. Zhang and
                  Hau-San Wong and Qingfu Zhang and Atsushi Nitanda},
  year         = {2026},
  howpublished = {GitHub repository and Samplinglib formalization website},
  url          = {https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep}
}"""
    body = f"""
<section class="page-hero compact"><div class="eyebrow">Provenance and ownership</div>
<h1>Attribution</h1><p class="lede">ASTIS separates the textbook route, Mathlib facts, external proof references, ASTIS-owned Lean declarations, and generated exposition.</p></section>
<section id="organizers" class="organizers-panel">
  <div class="section-heading"><span>Organizers</span><h2>The research and formalization team</h2></div>
  <p class="organizer-names">Dake Bu · Ji Cheng · Huanjian Zhou · Andi Han · Zonghao Chen · Sinho Chewi · Matthew S. Zhang · Hau-San Wong · Qingfu Zhang · Atsushi Nitanda</p>
</section>
<section class="attribution-grid">
  <article><h2>Primary mathematical source</h2><p>Sinho Chewi's <a href="{CHEWI_URL}"><em>Log-Concave Sampling</em></a> determines the chapter route. ASTIS uses original summaries, exact source correspondence, and supplemental regularity details; it does not imply author endorsement.</p></article>
  <article><h2>Lean and Mathlib</h2><p>Lean checks the local declarations. Mathlib supplies the measure, probability, analysis, convexity, kernel, and calculus APIs. A Mathlib theorem is labeled external until ASTIS owns the local declaration that consumes it.</p></article>
  <article><h2>External papers and repositories</h2><p>Cited textbooks, papers, <a href="https://github.com/YuanheZ/lean-stat-learning-theory">lean-stat-learning-theory</a>, and <a href="https://github.com/junwei-lu/Lean-Asymptotic-Statistical-Theory">Lean-Asymptotic-Statistical-Theory</a> are audited references or port sources. Their licenses and theorem hypotheses remain controlling.</p><p><a href="https://github.com/facebookresearch/atlas-lean/tree/e8b31c5cb0bec89b487ce33fe525a2c0b0f8b9c6/v1">ATLAS v1</a> contributes a pinned 26-book external declaration index. It is limited to academic/research use under CC BY-NC 4.0; commercial use and ML model training, fine-tuning, distillation, evaluation, or development are prohibited; all 36,469 records remain external-reference until a local ASTIS theorem passes the current gate.</p></article>
  <article><h2>Design provenance</h2><p>Comparisons with adjacent automation and formalization systems are centralized on the <a href="../related-systems/index.html">Related Systems</a> page. This attribution page records ownership, mathematical sources, and software dependencies.</p></article>
</section>
<section id="citation"><div class="section-heading"><span>Citation</span><h2>Cite ASTIS and Samplinglib</h2></div>{code_html(citation, "bibtex")}</section>
<section><h2>Source state</h2><dl><dt>Git ref</dt><dd><code>{esc(git.ref)}</code></dd><dt>Commit</dt><dd><code>{esc(git.commit)}</code></dd><dt>Remote</dt><dd><code>{esc(git.remote_url)}</code></dd><dt>Published commit</dt><dd>{"yes" if git.commit_published else "not found on a configured remote ref"}</dd><dt>Public source links</dt><dd>{"enabled" if git.public_source_links else "disabled; using site-local anchors"}</dd></dl></section>
<section class="note"><h2>Source-link rule</h2><p>By default every declaration links to the generated module anchor, so private or unpublished repositories cannot create public 404s. Set <code>ASTIS_PUBLIC_SOURCE_LINKS=1</code> only after verifying that the remote is public; clean files at a remote-published commit then link to that exact SHA. Modified or untracked files always remain labeled “local preview source”. The generator never assumes that checkout content already exists on <code>main</code>.</p></section>
"""
    return page("Attribution", "attribution/index.html", body)


_ALL_MODULES: list[SourceModule] = []


def copy_assets(output: Path) -> None:
    assets = output / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    for path in STATIC.iterdir():
        if path.is_file():
            shutil.copy2(path, assets / path.name)
    for name in (
        "log_concave_sampling_foundation.svg",
        "log_concave_sampling_foundation.png",
        "log_concave_sampling_status.svg",
        "log_concave_sampling_status.png",
        "astis_lean_arsenal_module_graph.svg",
        "astis_lean_arsenal_module_graph.png",
        "sampling_sde_leaf_network.svg",
        "sampling_sde_leaf_network.png",
    ):
        source = ROOT / "docs" / "assets" / name
        if source.exists():
            shutil.copy2(source, assets / name)
    for path in DIAGRAMS.glob("*.mmd"):
        shutil.copy2(path, assets / path.name)


def build_site(output: Path = DEFAULT_OUTPUT) -> dict[str, object]:
    global _ACTIVE_GATE, _ACTIVE_GIT, _SOURCE_BY_NAME, _TEACHING_BY_NAME, _ALL_MODULES, _SOURCE_EDITION
    source_errors, _ = astis_source.validate_source_contract()
    if source_errors:
        raise RuntimeError("canonical Chewi source check failed: " + "; ".join(source_errors))
    chapters = load_json(CONTENT / "chapters.json")
    source_entries = load_json(CONTENT / "source_correspondence.json")
    source_edition = load_json(CONTENT / "source_edition.json")
    section_guides = load_json(CONTENT / "section_guides.json")
    milestones = load_json(CONTENT / "milestones.json")
    teaching = load_json(CONTENT / "teaching_declarations.json")
    chapter_1_matrix_raw = load_json(CONTENT / "chapter_1_completion_matrix.json")
    assert isinstance(chapters, list)
    assert isinstance(source_entries, list)
    assert isinstance(source_edition, dict)
    assert isinstance(section_guides, dict)
    assert isinstance(milestones, list)
    assert isinstance(teaching, list)
    assert isinstance(chapter_1_matrix_raw, dict)
    chapter_1_matrix = expand_chapter_1_matrix(chapter_1_matrix_raw, source_entries)
    completion_report = chapter_1_completion_report(chapter_1_matrix)
    entries, module_files = enrich_entries(parse_registry())
    entries_by_decl = {entry.local_decl: entry for entry in entries if entry.local_decl}
    entries_by_short = {entry.short_name: entry for entry in entries if entry.local_decl}
    modules, declarations = scan_project_sources()
    declarations_by_name = {declaration.full_name: declaration for declaration in declarations}
    missing_teaching = sorted(
        str(item["declaration"])
        for item in teaching
        if str(item["declaration"]) not in declarations_by_name
    )
    missing_milestone_evidence = sorted(
        str(name)
        for milestone in milestones
        for name in milestone["evidence_declarations"]
        if str(name) not in declarations_by_name
    )
    if missing_teaching:
        raise RuntimeError(f"teaching metadata references unknown declarations: {missing_teaching}")
    if missing_milestone_evidence:
        raise RuntimeError(
            f"milestone metadata references unknown declarations: {missing_milestone_evidence}"
        )
    annotate_declarations(declarations, entries, teaching)
    _ACTIVE_GATE = load_gate_evidence()
    _ACTIVE_GIT = git_context()
    _SOURCE_BY_NAME = declarations_by_name
    _TEACHING_BY_NAME = {str(item["declaration"]): item for item in teaching}
    _ALL_MODULES = modules
    _SOURCE_EDITION = source_edition

    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    copy_assets(output)
    live_mappings = build_live_mappings(teaching, declarations_by_name)
    data_dir = output / "data"
    data_dir.mkdir()
    (data_dir / "live-mappings.json").write_text(
        json.dumps({"reviewed_mappings": live_mappings}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (data_dir / "chapter-1-completion-report.json").write_text(
        json.dumps(completion_report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    write_page(
        output,
        "index.html",
        render_overview(chapters, modules, declarations, entries, milestones, teaching),
    )
    write_page(output, "textbook/index.html", render_textbook_index(chapters))
    write_page(
        output,
        "textbook/chapter-01-matrix.html",
        render_chapter_1_matrix(chapter_1_matrix),
    )
    edition_by_number = {
        int(item["number"]): dict(item) for item in source_edition["chapters"]
    }
    for chapter in chapters:
        write_page(
            output,
            f"textbook/{chapter['id']}.html",
            render_textbook_chapter(
                chapter,
                edition_by_number[int(chapter["number"])],
                source_entries,
                entries_by_decl,
            ),
        )
    flat_sections: list[dict[str, object]] = []
    chapter_by_number = {int(chapter["number"]): chapter for chapter in chapters}
    for edition_chapter in source_edition["chapters"]:
        number = int(edition_chapter["number"])
        for raw_section in edition_chapter["sections"]:
            section = dict(raw_section)
            flat_sections.append({
                **section,
                "chapter": number,
                "path": textbook_section_path(number, str(section["id"])),
            })
    for index, section in enumerate(flat_sections):
        number = int(section["chapter"])
        write_page(
            output,
            str(section["path"]),
            render_textbook_section(
                chapter_by_number[number],
                section,
                str(section_guides.get(str(section["id"]), "")),
                source_entries,
                entries_by_decl,
                flat_sections[index - 1] if index else None,
                flat_sections[index + 1] if index + 1 < len(flat_sections) else None,
            ),
        )
    write_page(output, "calculation-route.html", render_calculation_route(chapters))
    write_page(output, "rigorous-details.html", render_rigorous_details(chapters))
    write_page(output, "lean-foundations.html", render_lean_foundations(entries))
    write_page(
        output,
        "source-correspondence.html",
        render_source_correspondence(source_entries, entries_by_decl),
    )
    write_page(
        output,
        "implementation-map/index.html",
        render_full_implementation_map(modules, declarations, milestones),
    )
    write_page(
        output,
        "learning-path/index.html",
        render_learning_path(chapters, teaching, declarations_by_name),
    )
    write_page(
        output,
        "declarations/index.html",
        render_declaration_catalog(declarations),
    )
    write_page(output, "modules/index.html", render_module_index(modules))
    write_page(output, "roadmap/index.html", render_roadmap(milestones))
    write_page(output, "live/index.html", render_live_formalization(len(live_mappings)))
    write_page(output, "workflow/index.html", render_workflow(_ACTIVE_GATE))
    write_page(output, "attribution/index.html", render_attribution_index(_ACTIVE_GIT))
    write_page(output, "contribute/index.html", render_contribute(sum(entry.is_blue for entry in entries)))
    write_page(output, "related-systems/index.html", render_related_systems())
    write_page(output, "dependency-explorer.html", render_dependency_explorer(entries))
    write_page(output, "progress.html", render_progress(chapters, entries, source_entries))
    write_page(output, "frontier.html", render_frontier(entries_by_short))
    write_page(output, "learn-lean.html", render_learn_lean(entries_by_short))
    write_page(output, "attribution.html", render_attribution())
    write_page(output, "maintenance.html", render_maintenance(sum(entry.is_blue for entry in entries)))

    source_by_decl: dict[str, list[dict[str, object]]] = defaultdict(list)
    for source in source_entries:
        for declaration in source["lean_declarations"]:
            source_by_decl[str(declaration)].append(source)
    for entry in entries:
        write_page(
            output,
            f"theorems/{entry.slug}.html",
            theorem_card(
                entry,
                entries_by_decl,
                source_by_decl.get(entry.local_decl, []),
                _TEACHING_BY_NAME.get(entry.local_decl),
            ),
        )

    reverse_imports: dict[str, list[str]] = defaultdict(list)
    for module in modules:
        for imported in module.imports:
            reverse_imports[imported].append(module.name)
    for module in modules:
        write_page(
            output,
            f"modules/{slugify(module.name)}.html",
            render_source_module(module, sorted(reverse_imports[module.name])),
        )
    for item in teaching:
        declaration = declarations_by_name[str(item["declaration"])]
        if not declaration.registry_card:
            write_page(
                output,
                teaching_card_path(declaration),
                render_teaching_declaration(declaration, item),
            )

    git_data = dataclasses.asdict(_ACTIVE_GIT)
    git_data["dirty_files"] = sorted(_ACTIVE_GIT.dirty_files)
    gate_data = dataclasses.asdict(_ACTIVE_GATE)
    site_data = {
        "project": "Auto-Sampling-Theory-In-Sleep",
        "short_name": "ASTIS",
        "public_library": "Samplinglib",
        "tagline": "Verified sampling theory in Lean, from textbook foundations to AI-assisted formalization.",
        "organizers": [
            "Dake Bu",
            "Ji Cheng",
            "Huanjian Zhou",
            "Andi Han",
            "Zonghao Chen",
            "Sinho Chewi",
            "Matthew S. Zhang",
            "Hau-San Wong",
            "Qingfu Zhang",
            "Atsushi Nitanda",
        ],
        "source_book": {
            "author": source_edition["author"],
            "title": source_edition["title"],
            "url": source_edition["canonical_url"],
            "edition": source_edition["edition"],
            "pdf_sha256": source_edition["pdf_sha256"],
            "body_pdf_page_offset": source_edition["body_pdf_page_offset"],
            "wording_policy": "faithful paraphrase unless a verified license permits more",
        },
        "registry": {
            "total_entries": len(entries),
            "compiled_local_leaves": sum(entry.is_blue for entry in entries),
            "tests_baseline": test_registry_count(),
        },
        "git": git_data,
        "gate": gate_data,
        "inventory": {
            "modules": len(modules),
            "production_modules": sum(module.role != "test" for module in modules),
            "declarations": len(declarations),
            "production_declarations": sum(
                declaration.module != "Tests" and not declaration.module.startswith("Tests.")
                for declaration in declarations
            ),
            "teaching_declarations": len(teaching),
            "live_reviewed_mappings": len(live_mappings),
            "placeholder_declarations": sum(
                declaration.has_placeholder for declaration in declarations
            ),
        },
        "chapters": chapters,
        "milestones": milestones,
        "teaching_declarations": teaching,
        "source_correspondence": source_entries,
        "chapter_1_completion_matrix": chapter_1_matrix,
        "chapter_1_completion_report": completion_report,
        "source_edition": source_edition,
        "textbook_sections": flat_sections,
        "modules": [
            {
                "name": module.name,
                "source_file": module.source_file,
                "role": module.role,
                "imports": module.imports,
                "declaration_count": len(module.declarations),
                "page": f"modules/{slugify(module.name)}.html",
            }
            for module in modules
        ],
        "declarations": [
            {
                "full_name": declaration.full_name,
                "short_name": declaration.short_name,
                "kind": declaration.kind,
                "module": declaration.module,
                "source_file": declaration.source_file,
                "source_line": declaration.source_line,
                "anchor": declaration.anchor,
                "local_status": local_declaration_status(declaration, _ACTIVE_GATE),
                "route_status": declaration.route_status,
                "has_placeholder": declaration.has_placeholder,
                "placeholder_tokens": declaration.placeholder_tokens,
                "registry_status": declaration.registry_status,
                "page": declaration_path(declaration),
            }
            for declaration in declarations
        ],
        "registry_declarations": [
            {
                "key": entry.key,
                "local_decl": entry.local_decl,
                "status": entry.status,
                "display_status": status_class(entry),
                "source_file": entry.source_file,
                "source_line": entry.source_line,
                "dependencies": entry.dependencies,
                "consumers": entry.consumers,
                "tags": entry.tags,
                "explicit_test": entry.explicit_test,
                "card": f"theorems/{entry.slug}.html",
            }
            for entry in entries
        ],
    }
    (data_dir / "site-data.json").write_text(
        json.dumps(site_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    search_index = [
        {
            "name": declaration.full_name,
            "kind": declaration.kind,
            "module": declaration.module,
            "chapter": next(
                (
                    int(item["chapter"])
                    for item in teaching
                    if item["declaration"] == declaration.full_name
                ),
                "",
            ),
            "local_status": local_declaration_status(declaration, _ACTIVE_GATE),
            "route_status": declaration.route_status,
            "url": declaration_path(declaration),
        }
        for declaration in declarations
    ]
    search_index.extend(
        {
            "name": module.name,
            "kind": "module",
            "module": module.name,
            "chapter": "",
            "local_status": "Compiled" if _ACTIVE_GATE.passed else "Partial",
            "route_status": "Not mapped",
            "url": f"modules/{slugify(module.name)}.html",
        }
        for module in modules
    )
    search_index.extend(
        {
            "name": f"{section['id']} {section['title']}",
            "kind": "textbook section",
            "module": "Log-Concave Sampling",
            "chapter": section["chapter"],
            "local_status": "N/A",
            "route_status": chapter_by_number[int(section["chapter"])]["status"],
            "url": section["path"],
        }
        for section in flat_sections
    )
    search_index.extend(
        {
            "name": f"{item['source_kind']}: {item['source_summary']}",
            "kind": item["category"],
            "module": "Log-Concave Sampling Chapter 1",
            "chapter": 1,
            "local_status": item["local_status"],
            "route_status": item["route_status"],
            "url": f"textbook/chapter-01-matrix.html#{item['id']}",
        }
        for item in chapter_1_matrix
    )
    (output / "search-index.json").write_text(
        json.dumps(search_index, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (data_dir / "build-metadata.json").write_text(
        json.dumps(
            {
                "git": git_data,
                "gate": gate_data,
                "source_digest": source_digest(),
                "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    (output / ".nojekyll").write_text("", encoding="utf-8")
    return site_data


def iter_local_links(html_path: Path, output: Path) -> Iterable[tuple[str, Path, str]]:
    text = html_path.read_text(encoding="utf-8")
    for attr, value in re.findall(r"\b(href|src)=[\"']([^\"']+)[\"']", text):
        if value.startswith(("mailto:", "javascript:", "data:")):
            continue
        parsed = urlparse(value)
        if parsed.scheme or parsed.netloc:
            continue
        clean = value.split("#", 1)[0].split("?", 1)[0]
        target = (html_path.parent / clean).resolve() if clean else html_path.resolve()
        yield value, target, parsed.fragment


def validate_site(
    output: Path = DEFAULT_OUTPUT,
    *,
    require_chapter_1_closure: bool = False,
) -> list[str]:
    errors: list[str] = []
    required = [
        "index.html",
        "textbook/index.html",
        "textbook/chapter-01.html",
        "textbook/chapter-01-matrix.html",
        "implementation-map/index.html",
        "learning-path/index.html",
        "declarations/index.html",
        "modules/index.html",
        "roadmap/index.html",
        "live/index.html",
        "workflow/index.html",
        "attribution/index.html",
        "contribute/index.html",
        "related-systems/index.html",
        "maintenance.html",
        "data/site-data.json",
        "data/build-metadata.json",
        "data/live-mappings.json",
        "data/chapter-1-completion-report.json",
        "search-index.json",
        "assets/site.css",
        "assets/site.js",
        "assets/ide.js",
        "assets/samplinglib-og.png",
        "assets/samplinglib-architecture.svg",
    ]
    for rel in required:
        if not (output / rel).exists():
            errors.append(f"missing required output: {rel}")

    if errors:
        return errors
    site_data = json.loads((output / "data" / "site-data.json").read_text(encoding="utf-8"))
    build_metadata = json.loads(
        (output / "data" / "build-metadata.json").read_text(encoding="utf-8")
    )
    compiled = int(site_data["registry"]["compiled_local_leaves"])
    baseline = site_data["registry"]["tests_baseline"]
    if baseline is not None and compiled != int(baseline):
        errors.append(f"compiled Registry count {compiled} != Tests baseline {baseline}")
    if len(site_data["chapters"]) != 12:
        errors.append(f"expected 12 chapters, found {len(site_data['chapters'])}")
    for chapter in site_data["chapters"]:
        for field in (
            "prerequisites",
            "concepts",
            "core_definitions",
            "major_results",
            "calculation_route",
            "rigorous_details",
            "blockers",
            "consumers",
        ):
            if not chapter.get(field):
                errors.append(f"{chapter.get('id', 'chapter')} has empty required field: {field}")

    chapter_1_matrix = site_data.get("chapter_1_completion_matrix", [])
    completion_report = site_data.get("chapter_1_completion_report", {})
    matrix_counts = Counter(str(item.get("category", "")) for item in chapter_1_matrix)
    expected_matrix_counts = {
        "statement": 67,
        "displayed_identity": 37,
        "exercise": 21,
    }
    if matrix_counts != expected_matrix_counts:
        errors.append(
            f"Chapter 1 matrix counts {dict(matrix_counts)} != {expected_matrix_counts}"
        )
    generated_report = json.loads(
        (output / "data" / "chapter-1-completion-report.json").read_text(encoding="utf-8")
    )
    expected_report = chapter_1_completion_report(chapter_1_matrix)
    if completion_report != expected_report or generated_report != expected_report:
        errors.append("Chapter 1 completion report does not match item-level evidence")
    matrix_ids: set[str] = set()
    matrix_numbers: set[tuple[str, str]] = set()
    matrix_fields = {
        "id", "category", "number", "section", "source_kind", "book_page",
        "pdf_page", "page", "source_url", "source_summary", "source_assumptions",
        "formal_assumptions", "local_declarations", "missing_dependency_ready_leaves",
        "downstream_consumers", "local_status", "route_status",
        "exact_residual_blocker", "source_mapping_id",
        "title", "coverage_kind", "source_route_id", "source_correspondence_id",
        "required_declarations", "focused_tests", "registry_keys", "coverage_status",
        "residual_blockers",
    }
    for item in chapter_1_matrix:
        item_id = str(item.get("id", ""))
        key = (str(item.get("category", "")), str(item.get("number", "")))
        missing = matrix_fields - set(item)
        if missing:
            errors.append(f"Chapter 1 matrix item {item_id} missing fields: {sorted(missing)}")
        if item_id in matrix_ids or key in matrix_numbers:
            errors.append(f"duplicate Chapter 1 matrix item: {key}")
        matrix_ids.add(item_id)
        matrix_numbers.add(key)
        if int(item.get("pdf_page", -1)) != int(item.get("book_page", -20)) + 12:
            errors.append(f"Chapter 1 matrix page offset mismatch: {item_id}")
        if not str(item.get("source_summary", "")).strip():
            errors.append(f"Chapter 1 matrix item lacks a source summary: {item_id}")
        if not item.get("source_assumptions") or not item.get("formal_assumptions"):
            errors.append(f"Chapter 1 matrix item lacks assumption audit: {item_id}")
        if not str(item.get("exact_residual_blocker", "")).strip():
            errors.append(f"Chapter 1 matrix item lacks a residual blocker: {item_id}")
        if item.get("local_status") == "Compiled" and not item.get("local_declarations"):
            errors.append(f"Chapter 1 matrix item has unsupported Compiled status: {item_id}")

    entries, _ = enrich_entries(parse_registry())
    modules, declarations = scan_project_sources()
    declarations_by_name = {declaration.full_name: declaration for declaration in declarations}
    module_names = {module.name for module in modules}
    if int(site_data["inventory"]["modules"]) != len(modules):
        errors.append("generated module count does not match source scan")
    if int(site_data["inventory"]["declarations"]) != len(declarations):
        errors.append("generated declaration count does not match source scan")
    if len(site_data["declarations"]) != len(declarations):
        errors.append("site-data declaration inventory is not exhaustive")
    if len(site_data["modules"]) != len(modules):
        errors.append("site-data module inventory is not exhaustive")
    if int(site_data["inventory"]["placeholder_declarations"]) != sum(
        declaration.has_placeholder for declaration in declarations
    ):
        errors.append("placeholder declaration count does not match source scan")
    errors.extend(validate_chapter_1_evidence(
        site_data,
        entries,
        declarations_by_name,
        require_complete=require_chapter_1_closure,
    ))

    for entry in entries:
        if entry.status == "formalizedLocal" and not entry.source_file:
            errors.append(f"formalizedLocal declaration does not resolve: {entry.local_decl}")
        if entry.is_blue and not (output / "theorems" / f"{entry.slug}.html").exists():
            errors.append(f"blue declaration has no theorem card: {entry.local_decl}")

    source_ids: set[str] = set()
    for source in site_data["source_correspondence"]:
        if source["id"] in source_ids:
            errors.append(f"duplicate source correspondence id: {source['id']}")
        source_ids.add(source["id"])
        if source["wording_status"] not in {
            "licensed original", "short quotation", "faithful paraphrase"
        }:
            errors.append(f"invalid wording status for {source['id']}: {source['wording_status']}")
        if not re.fullmatch(r"book \d+(?:–\d+)? / PDF \d+(?:–\d+)?", source["page"]):
            errors.append(f"inconsistent book/PDF page format for {source['id']}: {source['page']}")
        if source["status"] == "todo" and not source["lean_declarations"]:
            pass
        for decl in source["lean_declarations"]:
            if decl not in {entry.local_decl for entry in entries}:
                errors.append(f"source mapping references unknown Registry declaration: {decl}")

    requested_modules = {
        str(module)
        for chapter in site_data["chapters"]
        for module in chapter["lean_modules"]
    }
    for module in requested_modules:
        if module not in module_names:
            errors.append(f"chapter references missing Lean module: {module}")

    valid_statuses = {
        "Compiled",
        "Partial",
        "Stated/incomplete",
        "Planned",
        "Blocked",
        "External/upstream dependency",
        "Not mapped",
    }
    teaching_names: set[str] = set()
    teaching_fields = {
        "declaration",
        "chapter",
        "route_status",
        "plain_english",
        "mathematical_statement",
        "intuition",
        "assumptions",
        "why_assumptions",
        "proof_route",
        "lean_notes",
    }
    for item in site_data["teaching_declarations"]:
        name = str(item.get("declaration", ""))
        if name in teaching_names:
            errors.append(f"duplicate teaching declaration: {name}")
        teaching_names.add(name)
        missing_fields = teaching_fields - set(item)
        if missing_fields:
            errors.append(f"teaching declaration {name} missing fields: {sorted(missing_fields)}")
        if name not in declarations_by_name:
            errors.append(f"teaching metadata references unknown declaration: {name}")
        if item.get("route_status") not in valid_statuses:
            errors.append(f"invalid teaching route status for {name}: {item.get('route_status')}")
    if len(teaching_names) != int(site_data["inventory"]["teaching_declarations"]):
        errors.append("teaching declaration count does not match inventory")

    milestone_ids: set[str] = set()
    for milestone in site_data["milestones"]:
        milestone_id = str(milestone.get("id", ""))
        if milestone_id in milestone_ids:
            errors.append(f"duplicate milestone id: {milestone_id}")
        milestone_ids.add(milestone_id)
        for field in ("local_status", "route_status"):
            if milestone.get(field) not in valid_statuses:
                errors.append(
                    f"invalid milestone {field} for {milestone_id}: {milestone.get(field)}"
                )
        for name in milestone.get("evidence_declarations", []):
            if name not in declarations_by_name:
                errors.append(
                    f"milestone {milestone_id} references unknown declaration: {name}"
                )

    search_index = json.loads((output / "search-index.json").read_text(encoding="utf-8"))
    expected_search_count = (
        len(declarations)
        + len(modules)
        + len(site_data.get("textbook_sections", []))
        + len(site_data.get("chapter_1_completion_matrix", []))
    )
    if len(search_index) != expected_search_count:
        errors.append(
            "search index does not contain every declaration, module, textbook section, "
            "and Chapter 1 matrix item"
        )
    for section in site_data.get("textbook_sections", []):
        if not (output / str(section["path"])).exists():
            errors.append(f"missing generated textbook section page: {section['id']}")
    catalog_text = (output / "declarations" / "index.html").read_text(
        encoding="utf-8", errors="ignore"
    )
    if catalog_text.count("<tr data-search=") != len(declarations):
        errors.append("declaration catalog row count does not match source inventory")

    gate = site_data["gate"]
    gate_current = (
        bool(gate.get("passed"))
        and gate.get("commit") == site_data["git"].get("commit")
        and gate.get("source_digest") == source_digest()
        and build_metadata.get("source_digest") == source_digest()
    )
    if bool(gate.get("passed")) != gate_current:
        errors.append("site claims a Lean gate pass without current matching evidence")

    anchor_cache: dict[Path, set[str]] = {}
    for html_path in output.rglob("*.html"):
        for value, target, fragment in iter_local_links(html_path, output):
            try:
                target.relative_to(output.resolve())
            except ValueError:
                errors.append(f"link escapes output root: {html_path.relative_to(output)} -> {value}")
                continue
            if not target.exists():
                errors.append(f"broken local link: {html_path.relative_to(output)} -> {value}")
                continue
            if fragment and target.suffix.lower() == ".html":
                if target not in anchor_cache:
                    target_text = target.read_text(encoding="utf-8", errors="ignore")
                    anchor_cache[target] = set(
                        re.findall(r"\bid=[\"']([^\"']+)[\"']", target_text)
                    )
                if fragment not in anchor_cache[target]:
                    errors.append(
                        f"broken local anchor: {html_path.relative_to(output)} -> {value}"
                    )
    for module in modules:
        module_page = output / "modules" / f"{slugify(module.name)}.html"
        if not module_page.exists():
            errors.append(f"missing generated module page: {module.name}")
            continue
        module_text = module_page.read_text(encoding="utf-8", errors="ignore")
        for declaration in module.declarations:
            if f'id="{declaration.anchor}"' not in module_text:
                errors.append(
                    f"missing declaration anchor in {module.name}: {declaration.full_name}"
                )

    required_diagrams = {
        "measure-kernel-conditional",
        "probability-sampling-sde",
        "major-theorem-dag",
        "learning-path",
        "automation-workflow",
        "milestone-status",
        "module-family-map",
        "source-to-lean",
        "chapter-02-dag",
        "samplinglib-architecture",
        "contribution-route",
    }
    for name in required_diagrams:
        source = DIAGRAMS / f"{name}.mmd"
        copied = output / "assets" / f"{name}.mmd"
        if not source.exists() or not copied.exists():
            errors.append(f"missing editable Mermaid source or copied asset: {name}")
            continue
        text = source.read_text(encoding="utf-8")
        if not re.search(r"^\s*(?:flowchart|graph)\s+", text):
            errors.append(f"Mermaid diagram has no graph header: {name}")

    generated_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in output.rglob("*")
        if path.is_file() and path.suffix.lower() in {".html", ".json", ".css", ".js", ".mmd"}
    )
    if re.search(
        r"\b[A-Za-z]:\\(?:Users|Program Files|Windows|Temp|home)\\",
        generated_text,
        flags=re.IGNORECASE,
    ):
        errors.append("absolute Windows path leaked into generated website")
    if "Samplinglib" not in generated_text:
        errors.append("Samplinglib public-library identity missing")
    if "Auto-Sampling-Theory-In-Sleep" not in generated_text:
        errors.append("ASTIS system identity missing")
    for organizer in site_data.get("organizers", []):
        if str(organizer) not in generated_text:
            errors.append(f"organizer missing from generated website: {organizer}")
    if "data-live-app" not in generated_text or "/api/compile" not in generated_text:
        errors.append("Live Formalization workspace or compiler boundary missing")
    contributor_text = (output / "contribute" / "index.html").read_text(
        encoding="utf-8", errors="ignore"
    )
    for marker in (
        "Discuss",
        "Develop",
        "Verify",
        "Submit",
        "Local declaration status",
        "Mathematical route/paper-reproduction status",
        "Acceptance principle",
    ):
        if marker not in contributor_text:
            errors.append(f"contributor workflow marker missing: {marker}")
    if "MathJax" not in generated_text:
        errors.append("MathJax configuration missing")
    if "language-lean" not in generated_text:
        errors.append("Lean code blocks missing")
    if generated_text.count('class="mermaid"') < 10:
        errors.append("fewer than ten rendered Mermaid diagram placements")
    if "Sho Sonoda" not in generated_text or "Sinho Chewi" not in generated_text:
        errors.append("required attribution missing")
    if re.search(r"github\.com/DakeBU/Auto-Sampling-Theory-In-Sleep/blob/main/", generated_text):
        errors.append("source links incorrectly assume files exist on main")
    commit = str(site_data["git"].get("commit", ""))
    for source_link in re.findall(
        r'href="(https://github\.com/[^"]+/blob/[^"]+)"',
        generated_text,
    ):
        pin_error = source_commit_link_error(source_link, commit, str(site_data["git"].get("web_root", "")))
        if pin_error:
            errors.append(pin_error)
            break
    if not gate.get("passed") and "Lean gate passed" in generated_text:
        errors.append("unverified build displays a Lean gate passed label")
    return errors


def command_build(args: argparse.Namespace) -> int:
    output = Path(args.output).resolve() if args.output else DEFAULT_OUTPUT
    data = build_site(output)
    print(
        f"built {output}: {len(data['chapters'])} chapters, "
        f"{data['registry']['compiled_local_leaves']} compiled local leaves, "
        f"{data['inventory']['modules']} modules, "
        f"{data['inventory']['declarations']} declarations"
    )
    return 0


def command_check(args: argparse.Namespace) -> int:
    output = Path(args.output).resolve() if args.output else DEFAULT_OUTPUT
    if not output.exists() or args.rebuild:
        build_site(output)
    errors = validate_site(
        output,
        require_chapter_1_closure=args.require_chapter_1_closure,
    )
    if errors:
        print("ASTIS site check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    data = json.loads((output / "data" / "site-data.json").read_text(encoding="utf-8"))
    print(
        f"ASTIS site check passed: {len(data['chapters'])} chapters, "
        f"{data['inventory']['modules']} modules, "
        f"{data['inventory']['declarations']} declarations, "
        f"{data['inventory']['teaching_declarations']} reviewed teaching declarations"
    )
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="generate the static website")
    build.add_argument("--output", help="output directory (default: repository _site)")
    build.set_defaults(func=command_build)
    check = sub.add_parser("check", help="validate generated status, declarations, and links")
    check.add_argument("--output", help="output directory (default: repository _site)")
    check.add_argument("--rebuild", action="store_true", help="rebuild before checking")
    check.add_argument(
        "--require-chapter-1-closure",
        action="store_true",
        help="require all 125 Chapter 1 source items to have exact compiled and explicitly tested evidence",
    )
    check.set_defaults(func=command_check)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
