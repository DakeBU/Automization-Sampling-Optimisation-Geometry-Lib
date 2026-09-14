#!/usr/bin/env python3
"""Incremental contributor contract for changed ASTIS production declarations."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import astis_publication as publication  # noqa: E402

REFERENCE_READER = "textbook/chapter-01/section-1-3.html"
READER_FLAGS = (
    "source_ordered",
    "source_statement_adjacent",
    "natural_language_formula_proof",
    "hidden_assumptions_visible",
    "lean_collapsed",
    "external_dependencies_visible",
)


def _strings(value):
    if not isinstance(value, list):
        return None
    if any(not isinstance(x, str) or not x.strip() for x in value):
        return None
    return [x.strip() for x in value]


def validate(base: str | None) -> list[str]:
    targets = publication.changed_declarations(base) if base else set()
    if not targets:
        return []
    data = publication.inputs()
    errors = []
    seen = set()
    for item in publication.load():
        for binding in item.get("bindings", []):
            name = binding.get("declaration", "")
            if name not in targets:
                continue
            seen.add(name)
            cell_id = binding.get("cell", "")
            cell = data["cells"].get(cell_id, {})
            lesson = data["lessons"].get(name, {})
            label = f"{name} ({cell_id or 'missing cell'})"

            # Reader/layout obligations live in the Frontier Cell rather than in
            # the semantic publication binding.  This lets us improve the public
            # reader without invalidating an already accepted source-equivalence
            # audit whose theorem/source/exposition payload is unchanged.
            reader = cell.get("reader_contract")
            if not isinstance(reader, dict):
                errors.append(f"{label}: Frontier Cell reader_contract required")
            else:
                if reader.get("reference_standard") != REFERENCE_READER:
                    errors.append(f"{label}: reader reference must be {REFERENCE_READER}")
                for flag in READER_FLAGS:
                    if reader.get(flag) is not True:
                        errors.append(f"{label}: reader_contract.{flag}=true required")
            for key in ("astis_dependencies", "mathlib_dependencies", "sources"):
                if not isinstance(lesson.get(key), list):
                    errors.append(f"{label}: authored lesson must explicitly list {key}")

            reuse = cell.get("reuse_plan")
            if not isinstance(reuse, dict):
                errors.append(f"{label}: Frontier Cell reuse_plan required")
            else:
                searched = _strings(reuse.get("searched_existing"))
                reused = _strings(reuse.get("reused_declarations"))
                new_shared = _strings(reuse.get("new_shared_declarations"))
                known = _strings(reuse.get("known_consumers"))
                planned = _strings(reuse.get("planned_consumers"))
                if not searched:
                    errors.append(f"{label}: reuse_plan.searched_existing must be nonempty")
                for field, value in (("reused_declarations", reused), ("new_shared_declarations", new_shared), ("known_consumers", known), ("planned_consumers", planned)):
                    if value is None:
                        errors.append(f"{label}: reuse_plan.{field} must be a string list")
                if reuse.get("no_duplicate_wrapper") is not True:
                    errors.append(f"{label}: no_duplicate_wrapper must be true")
                if not isinstance(reuse.get("decision_reason"), str) or not reuse["decision_reason"].strip():
                    errors.append(f"{label}: reuse_plan.decision_reason required")
                if reused is not None:
                    missing = sorted(set(lesson.get("astis_dependencies", [])) - set(reused))
                    if missing:
                        errors.append(f"{label}: proof parents missing from reuse_plan: {missing}")
                if cell.get("shared_floor_audit", {}).get("decision") == "new_canonical_shared" and new_shared is not None:
                    if name not in new_shared:
                        errors.append(f"{label}: canonical shared target missing from new_shared_declarations")
                    if len(set((known or []) + (planned or []))) < 2:
                        errors.append(f"{label}: new shared declaration needs at least two consumers")

            graph = cell.get("graph_contribution")
            if not isinstance(graph, dict):
                errors.append(f"{label}: Frontier Cell graph_contribution required")
            else:
                if graph.get("lean_view") not in {"new-node", "reuse-only", "integration-node"}:
                    errors.append(f"{label}: invalid lean_view")
                if graph.get("overview_view") not in {"updated", "no-change-with-reason"}:
                    errors.append(f"{label}: invalid overview_view")
                functor = graph.get("functor_view")
                if functor not in {"none-found", "candidate-published", "stabilized"}:
                    errors.append(f"{label}: invalid functor_view")
                if graph.get("edge_semantics") != "formal-solid; overlays-dashed":
                    errors.append(f"{label}: preserve formal-solid / overlays-dashed edge semantics")
                if graph.get("color_semantics") != "evidence-status; library-scope":
                    errors.append(f"{label}: preserve evidence-status / library-scope colours")
                if not _strings(graph.get("focus_targets")):
                    errors.append(f"{label}: graph focus_targets required")
                if not isinstance(graph.get("visual_review"), str) or not graph["visual_review"].strip():
                    errors.append(f"{label}: graph visual_review required")
                mirror = cell.get("conceptual_mirror_audit", {})
                if functor == "none-found" and mirror.get("status") != "none-found":
                    errors.append(f"{label}: functor none-found must match conceptual_mirror_audit")
                if functor in {"candidate-published", "stabilized"} and (
                    mirror.get("status") != "candidates-published" or not mirror.get("discovery_ids")
                ):
                    errors.append(f"{label}: Functor contribution needs conceptual-mirror discovery ids")
    for name in sorted(targets - seen):
        errors.append(f"{name}: changed production declaration lacks contributor-contract publication binding")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check",))
    parser.add_argument("--base")
    parser.add_argument("--ci", action="store_true")
    args = parser.parse_args(argv)
    base = args.base
    if args.ci:
        base = os.environ.get("PUBLICATION_BASE") or base or "HEAD^"
        if set(base) == {"0"}:
            base = "HEAD^"
    errors = validate(base)
    if errors:
        print("ASTIS contributor contract failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("ASTIS contributor contract PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
