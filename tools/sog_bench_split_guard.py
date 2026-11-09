"""Offline reservation gate for declared Bench family exposure (not certification)."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
CATALOG = "benchmarks/samplingoptimisationgeometrybench/cores.json"
EXERCISES = "benchmarks/samplingoptimisationgeometrybench/textbook_exercises.json"
GRAPH_SPECS = tuple(f"benchmarks/samplingoptimisationgeometrybench/{name}.json" for name in (
    "graph_tasks", "compiled_graph_tasks", "compiled_flow_graph_tasks"))
MAX_BYTES = 8 * 1024 * 1024
MAX_REVISIONS = 512
IDENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
HEX = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"[0-9a-f]{40}")
ACTOR = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/@-]{0,127}")


class GuardError(ValueError):
    """A safe diagnostic which contains no supplied private values."""


def require(ok: bool, code: str) -> None:
    if not ok:
        raise GuardError(code)


def canonical(data) -> bytes:
    try:
        return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    except UnicodeError as exc:
        raise GuardError("invalid-unicode") from exc


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def object_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate-json-key")
        result[key] = value
    return result


def parse(raw: bytes) -> dict:
    require(0 < len(raw) <= MAX_BYTES, "metadata-size")
    try:
        result = json.loads(raw, object_pairs_hook=object_pairs)
    except (json.JSONDecodeError, UnicodeDecodeError, RecursionError) as exc:
        raise GuardError("malformed-json") from exc
    require(type(result) is dict, "metadata-object")
    return result


def identifier(x) -> str:
    require(type(x) is str and IDENT.fullmatch(x) is not None, "invalid-identity")
    return x.casefold()


def hash_id(x) -> str:
    require(type(x) is str and HEX.fullmatch(x) is not None, "invalid-sha256")
    return x


def declaration(x) -> str:
    require(type(x) is str and 0 < len(x) <= 256 and "." in x
            and not any(c.isspace() or not c.isprintable() for c in x), "invalid-answer-declaration")
    return x


def prompt_digest(assumptions: list[str], question: str) -> str:
    """Fingerprint NL text only; ignore whitespace, NFC and assumption order."""
    require(type(assumptions) is list and all(type(a) is str for a in assumptions)
            and type(question) is str and bool(question.strip()), "invalid-prompt")
    def norm(s):
        return " ".join(unicodedata.normalize("NFC", s).split())
    return digest(canonical({"assumptions": sorted(norm(a) for a in assumptions),
                             "question": norm(question)}))


def numbered_key(pdf, chapter, number) -> tuple[str, str, str]:
    chapter = identifier(chapter)
    return hash_id(pdf), (chapter.lstrip("0") or "0") if chapter.isdecimal() else chapter, identifier(number)


@dataclass
class Exposure:
    families: set[str] = field(default_factory=set)
    task_ids: set[str] = field(default_factory=set)
    prompt_digests: set[str] = field(default_factory=set)
    exercise_ids: set[str] = field(default_factory=set)
    numbered_sources: set[tuple[str, str, str]] = field(default_factory=set)
    answer_declarations: set[str] = field(default_factory=set)

    def add_catalog(self, catalog: dict, exercise_map: dict | None) -> None:
        require(type(catalog.get("schema_version")) is int and catalog["schema_version"] in (1, 2)
                and catalog.get("name") == "SamplingOptimisationGeometryBench"
                and catalog.get("split") == "public-dev", "not-a-known-public-catalog")
        rows = catalog.get("cores")
        require(type(rows) is list and bool(rows) and all(type(r) is dict for r in rows),
                "invalid-public-cores")
        exercises = {}
        if exercise_map is not None:
            require(type(exercise_map.get("schema_version")) is int
                    and exercise_map["schema_version"] == 1
                    and type(exercise_map.get("exercises")) is list
                    and type(exercise_map.get("books")) is dict, "invalid-public-exercise-map")
            for exercise in exercise_map["exercises"]:
                eid = exercise["id"]
                require(eid not in exercises, "duplicate-public-exercise-id")
                exercises[eid] = exercise
        for row in rows:
            self.families.add(identifier(row["family"]))
            self.task_ids.add(identifier(row["id"]))
            self.prompt_digests.add(prompt_digest(row["assumptions"], row["question"]))
            formal = row.get("lean_enabled", True)
            require(type(formal) is bool, "invalid-public-formal-availability")
            if formal:
                self.answer_declarations.add(declaration(row["declaration"]))
            if "textbook_exercise_id" in row:
                eid = row["textbook_exercise_id"]
                self.exercise_ids.add(identifier(eid))
                require(eid in exercises, "public-exercise-source-not-found")
                ex = exercises[eid]
                book = exercise_map["books"][ex["book_id"]]
                self.numbered_sources.add(numbered_key(book["pdf_sha256"], ex["chapter"], ex["number"]))

    def add_graph_ids(self, graph: dict, catalog: dict) -> None:
        # Structural QA is another view of its core's family, not a new
        # split or a mathematical necessity claim.
        rows = graph.get("tasks")
        require(type(rows) is list and all(type(r) is dict for r in rows), "invalid-public-graph-tasks")
        families_by_core = {r["id"]: r["family"] for r in catalog["cores"]}
        for row in rows:
            self.task_ids.add(identifier(row["id"]))
            family = row.get("family")
            core_id = row.get("core_id", graph.get("core_id"))
            if core_id is not None:
                require(type(core_id) is str and core_id in families_by_core,
                        "public-graph-core-not-found")
                core_family = families_by_core[core_id]
                require(family is None or identifier(family) == identifier(core_family),
                        "public-graph-family-mismatch")
                family = core_family
            self.families.add(identifier(family))

    def counts(self) -> dict:
        return {k: len(v) for k, v in vars(self).items()}


def git_bytes(repo: Path, *args: str, failure: str = "public-git-object-unavailable") -> bytes:
    # Missing objects must fail instead of contacting a promisor remote.
    env = {**os.environ, "GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1", "GIT_TERMINAL_PROMPT": "0",
           "GIT_ALLOW_PROTOCOL": ""}
    try:
        result = subprocess.run(["git", "-c", "protocol.allow=never", *args], cwd=repo,
                                env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=25, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise GuardError("local-git-unavailable") from exc
    require(result.returncode == 0, failure)
    return result.stdout


def inventory(repo: Path, public_tips: list[str], *, observation_only: bool = False) -> tuple[Exposure, dict]:
    require(bool(public_tips) and all(type(t) is str and COMMIT.fullmatch(t) for t in public_tips),
            "declare-exact-public-commit-ids")
    shallow = git_bytes(repo, "rev-parse", "--is-shallow-repository").strip()
    require(shallow in (b"true", b"false"), "invalid-git-history-state")
    require(shallow == b"false" or observation_only, "shallow-public-history")
    tips = sorted(set(public_tips))
    # Compare merges with each parent: otherwise diff-filter can omit the
    # merge snapshot itself, including catalog entries introduced by resolution.
    # Keep map-only changes and each tip, and deduplicate per-parent output.
    raw_history = git_bytes(repo, "log", "--full-history", "--diff-merges=separate", "--no-patch",
                            "--no-renames", "--no-show-signature", "--no-notes", "--no-color",
                            "--no-decorate", "--diff-filter=AM", "--format=%H",
                            *tips, "--", CATALOG, EXERCISES, *GRAPH_SPECS)
    try:
        history = raw_history.decode("ascii").split()
    except UnicodeDecodeError as exc:
        raise GuardError("invalid-public-history-output") from exc
    revisions = sorted(set(history) | set(tips))
    require(0 < len(revisions) <= MAX_REVISIONS and all(COMMIT.fullmatch(x) for x in revisions),
            "public-history-limit")
    found = Exposure()
    receipts = []
    for rev in revisions:
        blob = git_bytes(repo, "show", f"{rev}:{CATALOG}")
        data = parse(blob)
        rows = data.get("cores")
        require(type(rows) is list and all(type(r) is dict for r in rows), "invalid-public-cores")
        exercise_bytes = (git_bytes(repo, "show", f"{rev}:{EXERCISES}")
                          if any("textbook_exercise_id" in r for r in rows) else None)
        graph_paths = git_bytes(repo, "ls-tree", "-r", "--name-only", rev, "--",
                               *GRAPH_SPECS).decode("ascii").splitlines()
        graphs = {path: git_bytes(repo, "show", f"{rev}:{path}") for path in graph_paths}
        try:
            found.add_catalog(data, parse(exercise_bytes) if exercise_bytes is not None else None)
            for graph in graphs.values():
                found.add_graph_ids(parse(graph), data)
        except (KeyError, TypeError, AttributeError) as exc:
            raise GuardError("invalid-public-catalog-data") from exc
        receipts.append([rev, digest(blob), digest(exercise_bytes) if exercise_bytes else None,
                         {path: digest(graph) for path, graph in graphs.items()}])
    require(bool(found.families), "no-public-families")
    return found, {"declared_public_tips": len(tips), "public_snapshots": len(receipts),
                   "history_status": ("shallow-observation-only" if shallow == b"true"
                                      else "not-shallow-declared-tips-only"),
                   "public_history_sha256": digest(canonical(receipts)),
                   "known_public_exposure": found.counts()}


def exact_keys(data, keys: set[str], code: str) -> None:
    require(type(data) is dict and set(data) == keys, code)


def sequence(data, code: str, *, nonempty: bool = False) -> list:
    require(type(data) is list and (bool(data) or not nonempty), code)
    return data


def check_reservation(data: dict, public: Exposure) -> dict:
    exact_keys(data, {"schema_version", "split", "families"}, "reservation-schema")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1
            and data["split"] == "private-test", "reservation-schema")
    rows = sequence(data["families"], "reservation-needs-families", nonempty=True)
    issues: Counter = Counter()
    reserved = Exposure()
    def register(field, value):
        candidate, exposed = getattr(reserved, field), getattr(public, field)
        if value in exposed:
            issues["known-public-" + field] += 1
        if value in candidate:
            issues["repeated-private-" + field] += 1
        candidate.add(value)
    for row in rows:
        exact_keys(row, {"family", "aliases", "derived_from_families", "source_exercise_ids",
                         "numbered_sources", "tasks", "provenance"}, "private-family-schema")
        family = identifier(row["family"])
        own = [family, *(identifier(x) for x in sequence(row["aliases"], "private-aliases"))]
        for name in own:
            register("families", name)
        for parent in sequence(row["derived_from_families"], "private-lineage"):
            parent = identifier(parent)
            if parent in public.families:
                issues["public-lineage"] += 1
            elif parent not in own:
                issues["unresolved-or-cross-family-lineage"] += 1
        for x in sequence(row["source_exercise_ids"], "private-source-ids"):
            register("exercise_ids", identifier(x))
        for x in sequence(row["numbered_sources"], "private-numbered-sources"):
            exact_keys(x, {"pdf_sha256", "chapter", "number"}, "numbered-source-schema")
            register("numbered_sources", numbered_key(x["pdf_sha256"], x["chapter"], x["number"]))
        prov = row["provenance"]
        exact_keys(prov, {"author", "reviewer", "review_sha256", "rights", "uses_restricted_material",
                          "original_independent_family_attested"}, "private-provenance-schema")
        for who in ("author", "reviewer"):
            require(type(prov[who]) is str and ACTOR.fullmatch(prov[who]) is not None,
                    "invalid-review-identity")
        hash_id(prov["review_sha256"])
        if prov["author"].casefold() == prov["reviewer"].casefold():
            issues["no-distinct-reviewer"] += 1
        if prov["rights"] != "project-original" or prov["uses_restricted_material"] is not False:
            issues["rights-or-restricted-material"] += 1
        if prov["original_independent_family_attested"] is not True:
            issues["missing-independence-attestation"] += 1
        for task in sequence(row["tasks"], "private-family-needs-tasks", nonempty=True):
            require(type(task) is dict and "id" in task and 2 <= len(task) <= 3
                    and set(task) <= {"id", "nl_prompt_sha256", "lean_answer_declaration"},
                    "private-task-schema")
            register("task_ids", identifier(task["id"]))
            if "nl_prompt_sha256" in task:
                register("prompt_digests", hash_id(task["nl_prompt_sha256"]))
            if "lean_answer_declaration" in task:
                register("answer_declarations", declaration(task["lean_answer_declaration"]))
    return {"reservation_families": len(rows), "reservation_tasks": len(reserved.task_ids),
            "issues": dict(sorted(issues.items())), "no_known_conflict": not bool(issues)}


def private_input(path: Path, repo: Path) -> dict:
    try:
        path, repo = path.resolve(strict=True), repo.resolve()
        if path.is_relative_to(repo):
            rel = path.relative_to(repo)
            require(bool(rel.parts) and rel.parts[0] == ".astis",
                    "reservation-must-stay-out-of-tracked-paths")
            # check-ignore with no --no-index rejects tracked inputs.
            git_bytes(repo, "check-ignore", "-q", "--", rel.as_posix(),
                      failure="reservation-must-stay-ignored")
        require(path.is_file() and path.stat().st_size <= MAX_BYTES, "reservation-input-size")
        return parse(path.read_bytes())
    except OSError as exc:
        raise GuardError("reservation-input-unavailable") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-tip", action="append", required=True, help="Exact known-public commit; repeat for exposed PR/retired tips")
    parser.add_argument("--reservation", type=Path, help="Private metadata outside repo or under ignored .astis; omit for inventory only")
    args = parser.parse_args()
    try:
        found, report = inventory(ROOT, args.public_tip, observation_only=args.reservation is None)
        report["scope"] = "Declared public exposure only; no secrecy, originality or contamination certificate"
        if args.reservation is not None:
            result = check_reservation(private_input(args.reservation, ROOT), found)
            report["private_check"] = result
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return 1 if args.reservation is not None and not result["no_known_conflict"] else 0
    except GuardError as exc:
        print(json.dumps({"error": str(exc), "scope": "No reservation decision"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
