#!/usr/bin/env python3
"""Deterministic coordination primitives for the ASTIS proof harness.

This module deliberately contains no provider-specific agent code.  It owns
the state that must remain correct when prompts are stale, workers overlap, or
a run is interrupted: typed memory records, append-only events, route
fingerprints, role contracts, and the source-derived proof frontier.
"""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import errno
import hashlib
import json
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Iterator, Sequence

if os.name == "nt":
    import ctypes
    import msvcrt
    from ctypes import wintypes
else:
    import fcntl


ROOT = Path(__file__).resolve().parents[1]
HARNESS_SCHEMA_VERSION = 1

MEMORY_KINDS = frozenset({
    "analytic_contract",
    "integrability_source",
    "domination",
    "measurability",
    "domain",
    "ibp_boundary",
    "failed_path",
    "verified_lemma",
})
VERIFIER_STATUSES = frozenset({"not_reviewed", "accepted", "rejected", "superseded"})
LOCAL_STATUSES = frozenset({"planned", "partial", "compiled", "blocked", "external"})

ROLE_CONTRACTS: dict[str, dict[str, tuple[str, ...] | str]] = {
    "upper": {
        "artifact": "analytic_contract",
        "must_supply": (
            "exact mathematical statement",
            "complete assumptions and ambient measure",
            "source anchor",
            "dependency leaf identifiers",
        ),
        "tools": ("source_reader", "frontier_reader", "memory_reader"),
    },
    "middle": {
        "artifact": "formalization_map",
        "must_supply": (
            "Lean target statement",
            "Mathlib candidate declarations",
            "hypothesis-to-API mapping",
            "rejected candidates with type mismatch",
        ),
        "tools": ("rg", "lake_env_lean", "mathlib_source_reader", "memory_reader"),
    },
    "lower": {
        "artifact": "proof_attempt",
        "must_supply": (
            "one ready leaf",
            "statement-header hash",
            "focused compiler result",
            "remaining exact subgoal on failure",
        ),
        "tools": ("rg", "lake_env_lean", "apply_patch"),
    },
    "reviewer": {
        "artifact": "review",
        "must_supply": (
            "independent assumption audit",
            "source correspondence decision",
            "sorry/axiom scan result",
            "Lean gate evidence",
        ),
        "tools": ("rg", "lake_build", "git_diff", "source_reader"),
    },
}

ROLE_ARTIFACT_FIELDS: dict[str, tuple[str, ...]] = {
    "upper": ("artifact", "statement", "exact_assumptions", "measure", "source", "dependencies"),
    "middle": ("artifact", "lean_statement", "hypothesis_map", "mathlib_candidates", "rejected_candidates"),
    "lower": ("artifact", "leaf_id", "statement_header_hash", "compiler_status", "exact_subgoal"),
    "reviewer": ("artifact", "assumption_audit", "source_verdict", "fake_closure_scan", "lean_gate"),
}


def utc_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@contextlib.contextmanager
def file_lock(path: Path) -> Iterator[None]:
    """Take a cross-process exclusive lock associated with ``path``."""

    canonical = os.path.normcase(str(path.resolve()))
    lock_root = ROOT / ".astis" / "locks"
    lock_root.mkdir(parents=True, exist_ok=True)
    lock_path = lock_root / (hashlib.sha256(canonical.encode("utf-8")).hexdigest() + ".lock")
    with lock_path.open("a+b") as handle:
        if os.name == "nt":
            # Byte-range locks may extend beyond EOF, including on a new empty
            # lock file. Always lock byte zero, independent of append position.
            handle.seek(0)
            while True:
                try:
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError as exc:
                    if exc.errno != errno.EACCES:
                        raise
                    # LK_LOCK gives up after ten attempts; match flock's
                    # blocking behavior without swallowing unrelated failures.
                    time.sleep(0.05)
        else:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == "nt":
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _fsync_directory(path: Path) -> None:
    """Sync a POSIX directory; Windows publication uses write-through rename."""

    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _replace_and_sync(source: str, destination: Path) -> None:
    if os.name == "nt":
        move_file_ex = ctypes.WinDLL("kernel32", use_last_error=True).MoveFileExW
        move_file_ex.argtypes = (wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD)
        move_file_ex.restype = wintypes.BOOL
        # Same-volume replacement, never a copy/delete fallback. The payload
        # was fsynced before closing; request write-through for the rename too.
        flags = 0x1 | 0x8  # MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH
        if not move_file_ex(source, str(destination), flags):
            raise ctypes.WinError(ctypes.get_last_error())
    else:
        os.replace(source, destination)
        _fsync_directory(destination.parent)


def atomic_write_text(path: Path, text: str) -> None:
    """Publish a complete text file under a canonical-path lock.

    Sync the staged payload before same-directory replacement. POSIX then
    fsyncs the parent directory; Windows requests a write-through native rename
    instead, not a directory fsync. Crash durability remains bounded by the
    filesystem/device's flush guarantees; newly created ancestors are not
    individually synced. Windows readers denying delete sharing can prevent
    replacement, in which case the native error is propagated.
    """

    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with file_lock(path):
        fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            _replace_and_sync(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


def _recover_jsonl_unlocked(path: Path) -> tuple[list[dict[str, Any]], bool]:
    if not path.exists():
        return [], False
    raw = path.read_bytes()
    complete_end = raw.rfind(b"\n") + 1
    complete = raw[:complete_end]
    trailing = raw[complete_end:]
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(complete.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid complete JSONL record {path}:{line_number}: {exc}") from exc
        if not isinstance(value, dict):
            raise ValueError(f"JSONL record must be an object: {path}:{line_number}")
        records.append(value)
    recovered = bool(trailing)
    if recovered:
        with path.open("r+b") as handle:
            handle.truncate(complete_end)
            handle.flush()
            os.fsync(handle.fileno())
    return records, recovered


def recover_jsonl(path: Path) -> tuple[list[dict[str, Any]], bool]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with file_lock(path.resolve()):
        return _recover_jsonl_unlocked(path.resolve())


def _append_jsonl_unlocked(path: Path, record: dict[str, Any]) -> None:
    payload = (canonical_json(record) + "\n").encode("utf-8")
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o644)
    try:
        written = 0
        while written < len(payload):
            written += os.write(fd, payload[written:])
        os.fsync(fd)
    finally:
        os.close(fd)


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    """Recover an interrupted tail, then append one durable JSON record."""

    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with file_lock(path):
        _recover_jsonl_unlocked(path)
        _append_jsonl_unlocked(path, record)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return recover_jsonl(path)[0]


@dataclasses.dataclass(frozen=True)
class MemoryRecord:
    record_id: str
    kind: str
    task_id: str
    target: str
    exact_assumptions: tuple[str, ...]
    measure: str
    codomain: str
    declaration_hash: str
    source: str
    verifier_status: str = "not_reviewed"
    local_status: str = "planned"
    supersedes: tuple[str, ...] = ()
    details: dict[str, Any] = dataclasses.field(default_factory=dict)
    created_at: str = dataclasses.field(default_factory=utc_stamp)

    def validate(self) -> None:
        if self.kind not in MEMORY_KINDS:
            raise ValueError(f"unsupported memory kind: {self.kind}")
        if self.verifier_status not in VERIFIER_STATUSES:
            raise ValueError(f"unsupported verifier status: {self.verifier_status}")
        if self.local_status not in LOCAL_STATUSES:
            raise ValueError(f"unsupported local status: {self.local_status}")
        required = {
            "record_id": self.record_id,
            "task_id": self.task_id,
            "target": self.target,
            "measure": self.measure,
            "codomain": self.codomain,
            "declaration_hash": self.declaration_hash,
            "source": self.source,
        }
        missing = [name for name, value in required.items() if not value.strip()]
        if missing:
            raise ValueError("empty required memory fields: " + ", ".join(missing))

    def as_dict(self) -> dict[str, Any]:
        self.validate()
        value = dataclasses.asdict(self)
        value["schema_version"] = HARNESS_SCHEMA_VERSION
        return value


def append_memory(path: Path, record: MemoryRecord) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    value = record.as_dict()
    with file_lock(path):
        existing, _ = _recover_jsonl_unlocked(path)
        ids = {item.get("record_id") for item in existing}
        if record.record_id in ids:
            raise ValueError(f"duplicate memory record id: {record.record_id}")
        missing_superseded = set(record.supersedes) - ids
        if missing_superseded:
            raise ValueError(f"unknown superseded records: {sorted(missing_superseded)}")
        _append_jsonl_unlocked(path, value)


@dataclasses.dataclass(frozen=True)
class ProofBranch:
    """Immutable analytic route record in the append-only proof tree."""

    branch_id: str
    task_id: str
    parent_branch_id: str
    target_statement: str
    exact_assumptions: tuple[str, ...]
    measure: str
    spaces: tuple[str, ...]
    regularity: tuple[str, ...]
    integrability: tuple[str, ...]
    domination: tuple[str, ...]
    domains: tuple[str, ...]
    source_citations: tuple[str, ...]
    lean_declarations: tuple[str, ...] = ()
    compiler_errors: tuple[str, ...] = ()
    unresolved_siblings: tuple[str, ...] = ()
    created_at: str = dataclasses.field(default_factory=utc_stamp)

    def as_dict(self) -> dict[str, Any]:
        required = {
            "branch_id": self.branch_id,
            "task_id": self.task_id,
            "target_statement": self.target_statement,
            "measure": self.measure,
        }
        missing = [name for name, value in required.items() if not value.strip()]
        if missing or not self.exact_assumptions or not self.source_citations:
            raise ValueError(
                "invalid proof branch: "
                + ", ".join(missing + (["exact_assumptions"] if not self.exact_assumptions else [])
                    + (["source_citations"] if not self.source_citations else []))
            )
        value = dataclasses.asdict(self)
        value.update({
            "schema_version": HARNESS_SCHEMA_VERSION,
            "event": "branch_created",
            "contract_digest": digest({
                "target_statement": " ".join(self.target_statement.split()),
                "exact_assumptions": sorted(" ".join(item.split()) for item in self.exact_assumptions),
                "measure": self.measure,
                "spaces": self.spaces,
                "regularity": self.regularity,
                "integrability": self.integrability,
                "domination": self.domination,
                "domains": self.domains,
            }),
        })
        return value


def append_branch(path: Path, branch: ProofBranch) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    value = branch.as_dict()
    with file_lock(path):
        records, _ = _recover_jsonl_unlocked(path)
        branches = {str(item.get("branch_id")): item for item in records}
        if branch.branch_id in branches:
            raise ValueError(f"duplicate proof branch id: {branch.branch_id}")
        if branch.parent_branch_id and branch.parent_branch_id not in branches:
            raise ValueError(f"unknown parent proof branch: {branch.parent_branch_id}")
        _append_jsonl_unlocked(path, value)


def restore_branch(path: Path, branch_id: str) -> dict[str, Any]:
    matches = [item for item in load_jsonl(path) if item.get("branch_id") == branch_id]
    if len(matches) != 1:
        raise ValueError(f"expected one immutable proof branch {branch_id}, found {len(matches)}")
    return matches[0]


def bounded_memory_capsule(
    records: Sequence[dict[str, Any]], *, task_id: str, max_records: int = 24
) -> dict[str, Any]:
    """Select bounded task memory without summarizing exact analytic fields."""

    if max_records <= 0:
        raise ValueError("max_records must be positive")
    task_records = [item for item in records if item.get("task_id") == task_id]
    superseded = {
        str(record_id)
        for item in task_records
        for record_id in item.get("supersedes", [])
    }
    active = [item for item in task_records if item.get("record_id") not in superseded]
    selected_by_id: dict[str, dict[str, Any]] = {}
    for item in active + task_records[-max_records:]:
        key = str(item.get("record_id") or digest(item))
        selected_by_id[key] = item
    selected = list(selected_by_id.values())[-max_records:]
    return {
        "task_id": task_id,
        "records": selected,
        "record_count": len(selected),
        "omitted_count": len(task_records) - len(selected),
        "serialized_characters": len(canonical_json(selected)),
        "capsule_digest": digest(selected),
    }


def statement_header_hash(statement: str) -> str:
    """Hash a declaration header while excluding its proof body."""

    header = statement.split(":=", 1)[0]
    header = re.split(r"\bby\b", header, maxsplit=1)[0]
    header = " ".join(header.split())
    return hashlib.sha256(header.encode("utf-8")).hexdigest()


def route_fingerprint(
    *,
    target_statement: str,
    missing_property: str,
    assumptions: Sequence[str],
    mathlib_candidates: Sequence[str],
    compiler_error_class: str,
) -> str:
    return digest({
        "target_statement": " ".join(target_statement.split()),
        "missing_property": " ".join(missing_property.split()),
        "assumptions": sorted(" ".join(item.split()) for item in assumptions),
        "mathlib_candidates": sorted(set(mathlib_candidates)),
        "compiler_error_class": compiler_error_class.strip(),
    })


def record_route_attempt(
    path: Path,
    *,
    task_id: str,
    leaf_id: str,
    fingerprint: str,
    candidate: str,
    exact_subgoal: str,
    compiled_declarations: Sequence[str] = (),
    freeze_after_repeats: int = 2,
) -> dict[str, Any]:
    """Append an attempt and deterministically freeze a no-progress route.

    ``freeze_after_repeats=2`` means the first attempt plus two unchanged
    repeats.  A changed candidate, subgoal, or compiled declaration resets the
    no-progress counter even when the route fingerprint is unchanged.
    """

    records = load_jsonl(path)
    progress = digest({
        "candidate": candidate,
        "exact_subgoal": " ".join(exact_subgoal.split()),
        "compiled_declarations": sorted(set(compiled_declarations)),
    })
    matching = [
        item for item in records
        if item.get("event") == "route_attempt"
        and item.get("task_id") == task_id
        and item.get("leaf_id") == leaf_id
        and item.get("fingerprint") == fingerprint
    ]
    identical_tail = 0
    for item in reversed(matching):
        if item.get("progress_signature") != progress:
            break
        identical_tail += 1
    frozen = identical_tail >= freeze_after_repeats
    record = {
        "schema_version": HARNESS_SCHEMA_VERSION,
        "event": "route_attempt",
        "timestamp": utc_stamp(),
        "task_id": task_id,
        "leaf_id": leaf_id,
        "fingerprint": fingerprint,
        "candidate": candidate,
        "exact_subgoal": exact_subgoal,
        "compiled_declarations": sorted(set(compiled_declarations)),
        "progress_signature": progress,
        "unchanged_repeat_count": identical_tail,
        "decision": "freeze_for_review" if frozen else "continue",
    }
    append_jsonl(path, record)
    return record


def classify_retry(error_class: str) -> str:
    transient = {
        "provider_timeout",
        "provider_rate_limit",
        "network_reset",
        "temporary_unavailable",
    }
    return "retry" if error_class in transient else "freeze_for_review"


def run_with_retry(
    provider: Callable[[], Any],
    classify_error: Callable[[Exception], str],
    *,
    max_transient_retries: int = 2,
) -> tuple[Any, int]:
    """Run a provider and retry only errors classified as transient."""

    attempts = 0
    while True:
        attempts += 1
        try:
            return provider(), attempts
        except Exception as exc:
            error_class = classify_error(exc)
            if classify_retry(error_class) != "retry" or attempts > max_transient_retries:
                raise


def recover_run_events(path: Path) -> list[str]:
    """Close started executions that have no durable terminal event."""

    records = load_jsonl(path)
    started: dict[str, dict[str, Any]] = {}
    terminal: set[str] = set()
    for record in records:
        execution_id = str(record.get("execution_id", ""))
        if not execution_id:
            continue
        if record.get("event") == "role_started":
            started[execution_id] = record
        elif record.get("event") in {"role_completed", "role_failed", "role_interrupted"}:
            terminal.add(execution_id)
    interrupted = sorted(set(started) - terminal)
    for execution_id in interrupted:
        original = started[execution_id]
        append_jsonl(path, {
            "schema_version": HARNESS_SCHEMA_VERSION,
            "event": "role_interrupted",
            "timestamp": utc_stamp(),
            "execution_id": execution_id,
            "task_id": original.get("task_id", ""),
            "role": original.get("role", ""),
            "reason": "started execution had no durable terminal event",
        })
    return interrupted


def ordered_control_events(events: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    """Order steering before followups while retaining FIFO within each kind."""

    priority = {"steering": 0, "followup": 1}
    ordered = sorted(
        enumerate(events),
        key=lambda pair: (priority.get(pair[1].get("kind"), 2), pair[0]),
    )
    return [item for _, item in ordered]


@dataclasses.dataclass(frozen=True)
class FrontierNode:
    node_id: str
    chapter: str
    label: str
    declarations: tuple[str, ...]
    dependencies: tuple[str, ...]
    priority: int
    route_status: str = "partial"
    source_id: str = ""


FRONTIER_NODES: tuple[FrontierNode, ...] = (
    FrontierNode(
        "generator_display_integrability", "1", "Concrete generator-display integrability",
        ("integrable_expNeg_langevinGenerator_rhs_of_contDiff_of_hasCompactSupport",), (), 1,
    ),
    FrontierNode(
        "gibbs_tail", "1", "Gibbs tail outside expanding balls",
        ("tendsto_setIntegral_expNeg_norm_ge_comp_toLp_of_lintegral_expNeg_ne_top",), (), 2,
    ),
    FrontierNode(
        "whole_space_weighted_ibp", "1", "Whole-space Gibbs-weighted integration by parts",
        ("integral_expNeg_langevinGenerator_rhs_eq_zero_of_contDiff_of_hasCompactSupport",),
        ("generator_display_integrability",), 3,
    ),
    FrontierNode(
        "generator_core_contract", "1", "Compactly supported C2 generator core",
        ("CoreContract",), ("whole_space_weighted_ibp",), 4,
    ),
    FrontierNode(
        "normalized_core_annihilation", "1", "Normalized Gibbs core annihilation",
        ("integral_operator_normalizedGibbs_eq_zero_on_compactlySupportedC2",),
        ("generator_core_contract",), 5,
    ),
    FrontierNode(
        "abstract_semigroup_invariance_bridge", "1", "Abstract generator-to-invariance bridge",
        ("isInvariantOn_of_integral_generator_eq_zero",), (), 6,
    ),
    FrontierNode(
        "conditional_langevin_core_invariance", "1", "Conditional Langevin core invariance",
        ("isInvariantOn_normalizedGibbs_on_compactlySupportedC2",),
        ("normalized_core_annihilation", "abstract_semigroup_invariance_bridge"), 7,
    ),
    FrontierNode(
        "concrete_langevin_semigroup", "1", "Concrete Langevin Markov semigroup contract",
        ("langevinIntegratedSemigroupGeneratorContract",),
        ("conditional_langevin_core_invariance",), 20, "external",
    ),
    FrontierNode(
        "semigroup_stable_domain_extension", "1", "Semigroup-stable domain/core extension",
        ("integral_langevinGenerator_eq_zero_on_semigroupDomain",),
        ("concrete_langevin_semigroup",), 21,
    ),
    FrontierNode(
        "invariant_gibbs_law", "1", "Invariant normalized Gibbs law",
        ("normalizedGibbs_isInvariant_langevinSemigroup",),
        ("semigroup_stable_domain_extension",), 22,
    ),
    FrontierNode(
        "unit_cutoff_second_derivative_bound", "1", "Unit cutoff second derivative bound",
        ("smoothUnitCutoff_secondDeriv_bounded",), (), 30,
    ),
    FrontierNode(
        "second_order_cutoff_scaling", "1", "Scaled Hessian/Laplacian cutoff estimates",
        (
            "radialSmoothCutoff_iteratedFDeriv_two_bound",
            "radialSmoothCutoff_laplacian_bound",
        ),
        ("unit_cutoff_second_derivative_bound",), 40,
    ),
    FrontierNode(
        "chapter2_poincare_interface", "2", "Typed Poincare inequality interface",
        ("Satisfies", "mono_constant"), (), 50,
    ),
    FrontierNode(
        "chapter2_bakry_emery", "2", "Bakry--Emery Poincare criterion",
        ("poincare_of_strongConvexity",),
        ("chapter2_poincare_interface", "concrete_langevin_semigroup"), 60, "external",
    ),
    FrontierNode(
        "chapter2_localization", "2", "Localization and one-dimensional reduction",
        ("poincare_of_localization",),
        ("chapter2_poincare_interface",), 61, "external",
    ),
    FrontierNode(
        "chapter2_sharp_logconcave_isoperimetry", "2",
        "Dimension-sharp log-concave isoperimetry",
        ("logConcave_isoperimetric_bound",),
        ("chapter2_localization",), 62,
    ),
)


def source_frontier_nodes(root: Path = ROOT) -> tuple[FrontierNode, ...]:
    """Load optional proof leaves from the shared textbook correspondence.

    A source block enters the deterministic frontier only when it has an
    explicit ``proof_leaves`` list. This keeps the book spine, website, and
    harness synchronized without turning every not-yet-audited section into a
    fabricated theorem task.
    """

    path = root / "website" / "content" / "source_correspondence.json"
    if not path.exists():
        return ()
    rows = json.loads(path.read_text(encoding="utf-8"))
    nodes: list[FrontierNode] = []
    for row in rows:
        for leaf in row.get("proof_leaves", []):
            declarations = tuple(leaf.get("declarations", ()))
            if not declarations:
                raise ValueError(f"frontier leaf has no declarations: {row.get('id', '<unknown>')}")
            nodes.append(FrontierNode(
                node_id=str(leaf["node_id"]),
                chapter=str(row["chapter"]),
                label=str(leaf["label"]),
                declarations=declarations,
                dependencies=tuple(leaf.get("dependencies", ())),
                priority=int(leaf["priority"]),
                route_status=str(leaf.get("route_status", row.get("status", "partial"))),
                source_id=str(row["id"]),
            ))
    return tuple(nodes)


DECLARATION_RE = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|local|unsafe)\s+)*"
    r"(?:theorem|lemma|def|instance|structure|class|inductive)\s+([A-Za-z0-9_.'-]+)",
    re.MULTILINE,
)


def lean_declaration_inventory(root: Path = ROOT) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {}
    for path in sorted((root / "AutoSamplingTheory").rglob("*.lean")):
        text = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(root))
        for match in DECLARATION_RE.finditer(text):
            inventory.setdefault(match.group(1), []).append(relative)
    return inventory


def reconcile_frontier(root: Path = ROOT) -> dict[str, Any]:
    inventory = lean_declaration_inventory(root)
    nodes = FRONTIER_NODES + source_frontier_nodes(root)
    node_ids = [node.node_id for node in nodes]
    duplicates = sorted({node_id for node_id in node_ids if node_ids.count(node_id) > 1})
    if duplicates:
        raise ValueError(f"duplicate frontier node ids: {duplicates}")
    compiled: set[str] = set()
    rows: list[dict[str, Any]] = []
    for node in nodes:
        present = [name for name in node.declarations if name in inventory]
        dependencies_compiled = all(item in compiled for item in node.dependencies)
        if len(present) == len(node.declarations):
            local_status = "compiled"
            compiled.add(node.node_id)
        elif node.route_status == "external":
            local_status = "external_dependency"
        elif node.route_status == "blocked":
            local_status = "blocked"
        elif dependencies_compiled:
            local_status = "ready"
        else:
            local_status = "blocked"
        rows.append({
            **dataclasses.asdict(node),
            "present_declarations": present,
            "missing_declarations": [name for name in node.declarations if name not in inventory],
            "dependencies_compiled": dependencies_compiled,
            "local_status": local_status,
        })
    ready = sorted((row for row in rows if row["local_status"] == "ready"), key=lambda row: row["priority"])
    return {
        "schema_version": HARNESS_SCHEMA_VERSION,
        "generated_at": utc_stamp(),
        "active_program": "ASTIS-CHEWI-001",
        "task_relationship": {
            "ASTIS-CHEWI-001": "primary log-concave-sampling textbook foundation",
            "ASTIS-SALD-001": "downstream faithful-paper consumer of shared sampling/SDE leaves",
            "ASTIS-RMFLD-001": "planned downstream exploratory consumer",
        },
        "source_of_truth": (
            "current Lean declaration inventory plus static foundation nodes and "
            "source_correspondence proof leaves"
        ),
        "lean_declaration_count": sum(len(paths) for paths in inventory.values()),
        "nodes": rows,
        "selected_ready_leaf": ready[0] if ready else None,
    }


def deterministic_capsule(root: Path = ROOT) -> dict[str, Any]:
    frontier = reconcile_frontier(root)
    memory_path = root / ".astis" / "memory.jsonl"
    memory = bounded_memory_capsule(
        load_jsonl(memory_path) if memory_path.exists() else [],
        task_id=frontier["active_program"],
    )
    return {
        "schema_version": HARNESS_SCHEMA_VERSION,
        "generated_at": frontier["generated_at"],
        "active_program": frontier["active_program"],
        "task_relationship": frontier["task_relationship"],
        "selected_ready_leaf": frontier["selected_ready_leaf"],
        "frontier_status": {
            row["node_id"]: row["local_status"] for row in frontier["nodes"]
        },
        "bounded_typed_memory": memory,
        "role_contracts": ROLE_CONTRACTS,
        "control_policy": {
            "search_order": ["local ASTIS declarations", "Mathlib", "audited external references"],
            "no_progress": "freeze after two unchanged repeats following the first attempt",
            "retry": "transient provider/network failures only",
            "publish": "cross-process lock plus atomic canonical-path publication",
            "queue": "steering before followup; FIFO within each class",
        },
    }


def validate_role_preflight(role: str, available_tools: Sequence[str]) -> list[str]:
    if role not in ROLE_CONTRACTS:
        return [f"unknown role: {role}"]
    required = set(ROLE_CONTRACTS[role]["tools"])
    return [f"missing tool: {name}" for name in sorted(required - set(available_tools))]


def validate_role_artifact(role: str, artifact: dict[str, Any]) -> list[str]:
    if role not in ROLE_CONTRACTS:
        return [f"unknown role: {role}"]
    errors = [
        f"missing artifact field: {field}"
        for field in ROLE_ARTIFACT_FIELDS[role]
        if field not in artifact or artifact[field] in (None, "", [], {})
    ]
    expected = ROLE_CONTRACTS[role]["artifact"]
    if artifact.get("artifact") != expected:
        errors.append(f"artifact kind must be {expected}")
    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ASTIS deterministic harness state")
    sub = parser.add_subparsers(dest="command", required=True)
    reconcile = sub.add_parser("reconcile")
    reconcile.add_argument("--root", type=Path, default=ROOT)
    capsule = sub.add_parser("capsule")
    capsule.add_argument("--root", type=Path, default=ROOT)
    recover = sub.add_parser("recover-jsonl")
    recover.add_argument("path", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "reconcile":
        print(json.dumps(reconcile_frontier(args.root), indent=2, ensure_ascii=False))
        return 0
    if args.command == "capsule":
        print(json.dumps(deterministic_capsule(args.root), indent=2, ensure_ascii=False))
        return 0
    records, recovered = recover_jsonl(args.path)
    print(json.dumps({"records": len(records), "recovered": recovered}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
