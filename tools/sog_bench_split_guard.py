"""Offline reservation gate for declared Bench family exposure (not certification)."""
from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

if __package__:
    from . import sog_bench_graph_slices as compiled_slices
    from .sog_bench_curriculum import curriculum
else:
    import sog_bench_graph_slices as compiled_slices
    from sog_bench_curriculum import curriculum

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = "benchmarks/samplingoptimisationgeometrybench"
CATALOG = f"{DIRECTORY}/cores.json"
EXERCISES = f"{DIRECTORY}/textbook_exercises.json"
GRAPH_INDEX = f"{DIRECTORY}/{compiled_slices.INDEX}"
GRAPH_SPECS = (f"{DIRECTORY}/graph_tasks.json", *(
    f"{DIRECTORY}/{compiled_slices.spec_name(s)}" for s in compiled_slices.LEGACY_LABELS))
MAX_BYTES = 8 * 1024 * 1024
MAX_REVISIONS = 512
MAX_REVIEW_BYTES = 64 * 1024
MAX_REVIEW_FILES = 128
IDENT = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
HEX = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"[0-9a-f]{40}")
ACTOR = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/@-]{0,127}")
REVIEW_SCOPE = "private-family editorial review; not identity authentication"
REVIEW_CHECKS = {"originality", "public_lineage", "rights", "target_alignment"}


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
                            *tips, "--", CATALOG, EXERCISES, GRAPH_INDEX, *GRAPH_SPECS,
                            f":(glob){DIRECTORY}/compiled_*_graph_tasks.json")
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
                               GRAPH_INDEX, *GRAPH_SPECS).decode("ascii").splitlines()
        index_bytes = None
        if GRAPH_INDEX in graph_paths:
            index_bytes = git_bytes(repo, "show", f"{rev}:{GRAPH_INDEX}")
            try:
                registered = compiled_slices.labels(parse(index_bytes))
            except ValueError as exc:
                raise GuardError("invalid-public-graph-index") from exc
            graph_paths = [p for p in graph_paths if p == GRAPH_SPECS[0]]
            graph_paths.extend(f"{DIRECTORY}/{compiled_slices.spec_name(s)}" for s in registered)
        graphs = {path: git_bytes(repo, "show", f"{rev}:{path}") for path in graph_paths}
        try:
            found.add_catalog(data, parse(exercise_bytes) if exercise_bytes is not None else None)
            for graph in graphs.values():
                found.add_graph_ids(parse(graph), data)
        except (KeyError, TypeError, AttributeError) as exc:
            raise GuardError("invalid-public-catalog-data") from exc
        graph_hashes = {path: digest(graph) for path, graph in graphs.items()}
        if index_bytes is not None:
            graph_hashes[GRAPH_INDEX] = digest(index_bytes)
        receipts.append([rev, digest(blob), digest(exercise_bytes) if exercise_bytes else None, graph_hashes])
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


def family_review_binding(family: dict) -> str:
    """Bind exact family metadata without recursively binding the review digest."""
    prov = {k: v for k, v in family["provenance"].items() if k != "review_sha256"}
    return digest(canonical({**family, "provenance": prov}))


def check_review_evidence(data: dict, raw_reviews: Iterable[bytes], public_hash: str,
                          *, prose_bindings: dict[str, str] | None = None) -> dict:
    """Bind supplied local review bytes to already validated private metadata."""
    hash_id(public_hash)
    issues: Counter = Counter()
    by_digest = {}
    count = 0
    for raw in raw_reviews:
        count += 1
        require(count <= MAX_REVIEW_FILES and 0 < len(raw) <= MAX_REVIEW_BYTES, "private-review-input-limit")
        key = digest(raw)
        if key in by_digest:
            issues["repeated-review-file"] += 1
            continue
        row = parse(raw)
        keys = {"schema_version", "scope", "reviewer", "public_history_sha256",
                "family_binding_sha256", "verdict", "checks"}
        if prose_bindings is not None:
            keys.add("prose_packet_sha256")
        exact_keys(row, keys, "review-file-schema")
        require(type(row["schema_version"]) is int
                and row["schema_version"] == (1 if prose_bindings is None else 2)
                and row["scope"] == REVIEW_SCOPE and row["verdict"] in ("accept", "reject"),
                "review-file-schema")
        require(type(row["reviewer"]) is str and ACTOR.fullmatch(row["reviewer"]) is not None,
                "invalid-review-identity")
        hash_id(row["public_history_sha256"])
        hash_id(row["family_binding_sha256"])
        exact_keys(row["checks"], REVIEW_CHECKS, "review-check-schema")
        require(all(type(note) is str and bool(note.strip()) for note in row["checks"].values()),
                "review-check-schema")
        by_digest[key] = {k: row[k] for k in
                          ("reviewer", "public_history_sha256", "family_binding_sha256", "verdict")}
        if prose_bindings is not None:
            by_digest[key]["prose_packet_sha256"] = hash_id(row["prose_packet_sha256"])
    claimed = set()
    for family in data["families"]:
        prov = family["provenance"]
        key = prov["review_sha256"]
        if key in claimed:
            issues["repeated-review-claim"] += 1
        claimed.add(key)
        row = by_digest.get(key)
        if row is None:
            issues["missing-review-file"] += 1
            continue
        if row["reviewer"] != prov["reviewer"]:
            issues["reviewer-mismatch"] += 1
        if row["public_history_sha256"] != public_hash:
            issues["review-public-history-drift"] += 1
        if row["family_binding_sha256"] != family_review_binding(family):
            issues["review-family-binding-drift"] += 1
        if prose_bindings is not None and row["prose_packet_sha256"] != prose_bindings[family["family"]]:
            issues["review-prose-packet-drift"] += 1
        if row["verdict"] != "accept":
            issues["review-not-accepted"] += 1
    unused = len(by_digest.keys() - claimed)
    if unused:
        issues["unclaimed-review-file"] += unused
    return {"review_files_supplied": count, "all_review_files_bound": not bool(issues),
            "issues": dict(sorted(issues.items()))}


PROSE_INPUT_FIELDS = ("id", "assumptions", "question", "retrieval_profile", "allowed_tools")


def prose_prompt(task: dict) -> dict:
    fields = {k: task[k] for k in PROSE_INPUT_FIELDS}
    return {**fields, "track": "natural-language", "split": "private-test",
            "prompt_sha256": digest(canonical(fields))}


def private_prose_packet(reservation: dict, packet: dict) -> tuple[dict[str, str], bytes]:
    """Bind canonical private tasks to an already validated prose-only reservation."""
    exact_keys(packet, {"schema_version", "split", "tasks"}, "private-prose-schema")
    require(type(packet["schema_version"]) is int and packet["schema_version"] == 1
            and packet["split"] == "private-test", "private-prose-schema")
    expected = {}
    groups = {}
    for family in reservation["families"]:
        name = family["family"]
        groups[name] = []
        for task in family["tasks"]:
            exact_keys(task, {"id", "nl_prompt_sha256"}, "private-packet-requires-prose-only")
            expected[task["id"]] = (name, task["nl_prompt_sha256"])
    plan = curriculum()
    prompts = []
    for task in sequence(packet["tasks"], "private-prose-tasks", nonempty=True):
        exact_keys(task, {*PROSE_INPUT_FIELDS, "family", "domain", "level", "skills", "source_notes",
                          "proof_steps", "rubric"}, "private-prose-task-schema")
        identifier(task["id"])
        identifier(task["family"])
        require(task["id"] in expected, "private-prose-task-set-mismatch")
        family, prompt = expected.pop(task["id"])
        require(task["family"] == family, "private-prose-family-mismatch")
        for key, options in (("domain", plan["domains"]), ("level", plan["levels"])):
            require(type(task[key]) is str and task[key] in options, "private-prose-curriculum")
        skills = sequence(task["skills"], "private-prose-curriculum", nonempty=True)
        require(all(type(s) is str and s in plan["skills"] for s in skills)
                and len(set(skills)) == len(skills), "private-prose-curriculum")
        for field in ("assumptions", "proof_steps", "rubric", "allowed_tools"):
            rows = sequence(task[field], "private-prose-text-list", nonempty=field == "proof_steps")
            require(all(type(s) is str and bool(s.strip()) for s in rows), "private-prose-text-list")
        require(len(task["rubric"]) == len(set(task["rubric"])) == 4, "private-prose-four-rubric-points")
        require(type(task["source_notes"]) is str and bool(task["source_notes"].strip()), "private-prose-source-notes")
        require(task["retrieval_profile"] in ("closed-book", "open-library"), "private-prose-retrieval-profile")
        require(prompt_digest(task["assumptions"], task["question"]) == prompt, "private-prose-prompt-drift")
        groups[family].append(task)
        prompts.append(prose_prompt(task))
    require(not expected, "private-prose-task-set-mismatch")
    bindings = {family: digest(canonical({"schema_version": 1, "split": "private-test",
                                         "tasks": sorted(tasks, key=lambda t: t["id"])}))
                for family, tasks in groups.items()}
    return bindings, b"".join(canonical(prompt) + b"\n" for prompt in sorted(prompts, key=lambda p: p["id"]))


def require_private_path(path: Path, repo: Path) -> None:
    if path.is_relative_to(repo):
        rel = path.relative_to(repo)
        require(bool(rel.parts) and rel.parts[0] == ".astis", "reservation-must-stay-out-of-tracked-paths")
        # check-ignore with no --no-index rejects tracked paths.
        git_bytes(repo, "check-ignore", "-q", "--", rel.as_posix(),
                  failure="reservation-must-stay-ignored")


def write_private_output(path: Path, repo: Path, raw: bytes) -> None:
    """Require a fresh destination in a private, already existing directory."""
    require(bool(path.name) and path.name not in (".", "..") and ":" not in path.name,
            "invalid-private-output-name")
    try:
        target = path.parent.resolve(strict=True) / path.name
        require_private_path(target, repo.resolve())
        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
        with os.fdopen(os.open(target, flags, 0o600), "wb") as stream:
            stream.write(raw)
    except (OSError, RuntimeError) as exc:
        raise GuardError("private-output-unavailable-or-exists") from exc


def private_bytes(path: Path, repo: Path, max_bytes: int = MAX_BYTES) -> bytes:
    try:
        path, repo = path.resolve(strict=True), repo.resolve()
        require_private_path(path, repo)
        require(path.is_file() and 0 < path.stat().st_size <= max_bytes, "reservation-input-size")
        with path.open("rb") as stream:
            raw = stream.read(max_bytes + 1)
        require(0 < len(raw) <= max_bytes, "reservation-input-size")
        return raw
    except (OSError, RuntimeError) as exc:
        raise GuardError("reservation-input-unavailable") from exc


def private_input(path: Path, repo: Path) -> dict:
    return parse(private_bytes(path, repo))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-tip", action="append", required=True, help="Exact known-public commit; repeat for exposed PR/retired tips")
    parser.add_argument("--reservation", type=Path, help="Private metadata outside repo or under ignored .astis; omit for inventory only")
    parser.add_argument("--review-file", action="append", type=Path, default=[],
                        help="Exact private reviewer report; repeat once per reserved family")
    parser.add_argument("--prose-packet", type=Path, help="Private actual tasks, proofs and rubrics to bind")
    outputs = parser.add_mutually_exclusive_group()
    outputs.add_argument("--prose-review-request", type=Path, help="Write an unsigned private review request")
    outputs.add_argument("--prose-prompts", type=Path, help="Write a private prompt-only JSONL after full evidence checks")
    args = parser.parse_args()
    if (args.review_file or args.prose_packet) and args.reservation is None:
        parser.error("--review-file and --prose-packet require --reservation")
    if (args.prose_review_request or args.prose_prompts) and args.prose_packet is None:
        parser.error("Private prose outputs require --prose-packet")
    if args.prose_prompts and not args.review_file:
        parser.error("Private prose prompt output requires --review-file")
    try:
        found, report = inventory(ROOT, args.public_tip, observation_only=args.reservation is None)
        report["scope"] = "Declared public exposure only; no secrecy, originality or contamination certificate"
        decision = 0
        if args.reservation is not None:
            private = private_input(args.reservation, ROOT)
            result = check_reservation(private, found)
            report["private_check"] = result
            decision = 0 if result["no_known_conflict"] else 1
            prose_bindings = None
            if args.prose_packet and not decision:
                prose_bindings, prompts = private_prose_packet(private, private_input(args.prose_packet, ROOT))
                report["private_prose_check"] = {"task_packet_bound_to_reservation": True,
                                                 "schema_version": 1, "prompt_file_written": False}
            if args.review_file and args.prose_packet and decision:
                report["private_review_check"] = {"status": "skipped after public collision or policy failure"}
            elif args.review_file:
                require(len(args.review_file) <= MAX_REVIEW_FILES, "private-review-input-limit")
                raws = (private_bytes(path, ROOT, MAX_REVIEW_BYTES) for path in args.review_file)
                evidence = check_review_evidence(private, raws, report["public_history_sha256"],
                                                 prose_bindings=prose_bindings)
                report["private_review_check"] = evidence
                if not evidence["all_review_files_bound"]:
                    decision = 1
            else:
                status = "prose packet checked" if prose_bindings is not None else "metadata-only"
                report["private_review_check"] = {"status": f"{status}; no reviewer bytes checked"}
            if not decision and args.prose_review_request:
                request = {"status": "unsigned; not review evidence", "families": [
                    {"family": row["family"], "review": {"schema_version": 2, "scope": REVIEW_SCOPE,
                     "reviewer": row["provenance"]["reviewer"], "public_history_sha256": report["public_history_sha256"],
                     "family_binding_sha256": family_review_binding(row), "prose_packet_sha256": prose_bindings[row["family"]],
                     "verdict": "", "checks": {name: "" for name in REVIEW_CHECKS}}}
                    for row in private["families"]]}
                write_private_output(args.prose_review_request, ROOT, canonical(request) + b"\n")
            if not decision and args.prose_prompts:
                write_private_output(args.prose_prompts, ROOT, prompts)
                report["private_prose_check"]["prompt_file_written"] = True
        print(json.dumps(report, ensure_ascii=False, sort_keys=True))
        return decision
    except GuardError as exc:
        print(json.dumps({"error": str(exc), "scope": "No reservation decision"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
