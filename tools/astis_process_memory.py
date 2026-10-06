#!/usr/bin/env python3
"""Validate ASTIS evidence-routed process and negative memory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MEMORY = ROOT / "research-wiki" / "process-memory.json"

FAILURE_CLASSES = {
    "REFUTED",
    "SOURCE_INVALID",
    "API_BLOCKED",
    "ENV_BLOCKED",
    "IMPLEMENTATION_FAILED",
    "NONE",
}
ENTRY_KINDS = {"standing_instruction", "negative_knowledge"}
ROUTE_EFFECTS = {"retire-same-target", "reopen-on-invalidation", "diagnostic-only"}
STATUSES = {"active", "retired"}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(value: Any, *, nonempty: bool = False) -> bool:
    return (
        isinstance(value, list)
        and (not nonempty or bool(value))
        and all(_nonempty(item) for item in value)
    )


def validate(path: Path = DEFAULT_MEMORY) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path}: cannot load process memory: {exc}"]

    if data.get("schema_version") != 1:
        errors.append("process memory schema_version must be 1")

    policy = data.get("policy")
    if not isinstance(policy, dict):
        errors.append("policy must be an object")
        policy = {}
    if policy.get("control_plane_math_authority") is not False:
        errors.append("control_plane_math_authority must be false")
    if policy.get("salvage_before_discard") is not True:
        errors.append("salvage_before_discard must be true")
    if policy.get("default_parallelism") != "serial":
        errors.append("default_parallelism must remain serial")
    if policy.get("parallel_requires_distinct_direction_fingerprints") is not True:
        errors.append("parallelism must require distinct direction fingerprints")
    if policy.get("cross_route_audit_if_parallel") is not True:
        errors.append("parallel routes must require cross-route audit")
    if set(policy.get("failure_classes", [])) != FAILURE_CLASSES:
        errors.append("failure_classes must match the canonical typed failure classes")
    if not _string_list(policy.get("reader_backpressure_tracks"), nonempty=True):
        errors.append("reader_backpressure_tracks must be a non-empty string list")

    entries = data.get("entries")
    if not isinstance(entries, list):
        return errors + ["entries must be a list"]

    seen: set[str] = set()
    for index, entry in enumerate(entries):
        label = f"entries[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label}: entry must be an object")
            continue
        ident = entry.get("id")
        if not _nonempty(ident):
            errors.append(f"{label}: id must be non-empty")
        elif ident in seen:
            errors.append(f"{label}: duplicate id {ident}")
        else:
            seen.add(ident)

        if entry.get("kind") not in ENTRY_KINDS:
            errors.append(f"{label}: invalid kind")
        if entry.get("status") not in STATUSES:
            errors.append(f"{label}: invalid status")
        if not _string_list(entry.get("scope"), nonempty=True):
            errors.append(f"{label}: scope must be a non-empty string list")

        evidence = entry.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"{label}: evidence must be a non-empty list")
            evidence = []
        for j, item in enumerate(evidence):
            elabel = f"{label}.evidence[{j}]"
            if not isinstance(item, dict):
                errors.append(f"{elabel}: evidence must be an object")
                continue
            if any(not _nonempty(item.get(key)) for key in ("file", "needle", "evidence_kind")):
                errors.append(f"{elabel}: file, needle, evidence_kind are required")
                continue
            evidence_path = ROOT / item["file"]
            if not evidence_path.is_file():
                errors.append(f"{elabel}: missing evidence file {item['file']}")
                continue
            if item["needle"] not in evidence_path.read_text(encoding="utf-8", errors="replace"):
                errors.append(f"{elabel}: evidence needle not found in {item['file']}")

        if entry.get("kind") == "standing_instruction":
            if entry.get("process_only") is not True:
                errors.append(f"{label}: standing instructions must be process_only=true")
            if not _nonempty(entry.get("instruction")):
                errors.append(f"{label}: standing instruction text required")
            if not _nonempty(entry.get("expires_when")):
                errors.append(f"{label}: expires_when required")
            if "classification" in entry:
                errors.append(f"{label}: standing instruction must not masquerade as negative mathematics")

        if entry.get("kind") == "negative_knowledge":
            classification = entry.get("classification")
            if classification not in FAILURE_CLASSES - {"NONE"}:
                errors.append(f"{label}: invalid negative classification")
            if not _nonempty(entry.get("statement")):
                errors.append(f"{label}: negative statement required")
            if entry.get("route_effect") not in ROUTE_EFFECTS:
                errors.append(f"{label}: invalid route_effect")
            if not _string_list(entry.get("invalidation_keys"), nonempty=True):
                errors.append(f"{label}: invalidation_keys required")
            if classification in {"API_BLOCKED", "ENV_BLOCKED", "IMPLEMENTATION_FAILED"} and entry.get("route_effect") == "retire-same-target":
                errors.append(f"{label}: non-mathematical failure may not retire the mathematical target")
            if classification == "REFUTED" and entry.get("route_effect") != "retire-same-target":
                errors.append(f"{label}: REFUTED must retire the same sealed target")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check",), nargs="?", default="check")
    parser.add_argument("--path", default=str(DEFAULT_MEMORY))
    args = parser.parse_args(argv)
    errors = validate(Path(args.path))
    if errors:
        print("ASTIS process-memory check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("ASTIS process-memory check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
