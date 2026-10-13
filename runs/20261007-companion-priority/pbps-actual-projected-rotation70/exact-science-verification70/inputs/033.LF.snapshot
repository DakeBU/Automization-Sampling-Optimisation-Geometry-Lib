#!/usr/bin/env python3
"""Incremental contributor contract for changed ASTIS production declarations."""
from __future__ import annotations

import argparse
import os
import json
import subprocess
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


METADATA_ROOTS = (
    "website/content/publications", "website/content/declaration_lessons",
    "research-wiki/frontier-cells",
)


def resolve_base(base: str | None, *, ci=False) -> str:
    if ci:
        base = base or os.environ.get("PUBLICATION_BASE")
        if not base:
            raise ValueError("CI requires a comparison commit (PUBLICATION_BASE/--base)")
        if set(base) == {"0"}:
            # A first topic-branch push has no previous tip. HEAD^ would hide
            # earlier commits in a multi-commit contribution.
            if os.environ.get("GITHUB_REF") == "refs/heads/main":
                raise ValueError("Initial main push requires an explicit review base")
            base = publication.git("merge-base", "HEAD", "origin/main").strip()
    if not base:
        raise ValueError("Comparison scope required: use --base COMMIT or --ci with PUBLICATION_BASE")
    return publication.git("rev-parse", "--verify", base + "^{commit}").strip()


def _metadata_records(path: str, raw) -> dict:
    if path.startswith("website/content/publications/"):
        # Source-level edits affect every binding, but an edit to one binding
        # must not drag unrelated declarations in the same file into migration.
        records = {}
        for item in raw["items"]:
            source = {k: v for k, v in item.items() if k != "bindings"}
            for binding in item["bindings"]:
                key = (item["id"], binding["declaration"])
                if key in records:
                    raise ValueError(f"{path}: duplicate binding {key}")
                records[key] = (binding["declaration"], {"source": source, "binding": binding})
        return records
    if path.startswith("website/content/declaration_lessons/"):
        units = raw["units"] if isinstance(raw, dict) else raw
        return {u["declaration"]: (u["declaration"], u) for u in units}
    return {raw["cell_id"]: (raw["cell_id"], raw)}


def affected_metadata(base: str) -> tuple[set[str], set[str]]:
    paths = set(publication.git("diff", "--no-renames", "--name-only", "-z", base,
                                "--", *METADATA_ROOTS).split("\0"))
    paths.update(publication.git("ls-files", "--others", "--exclude-standard", "-z",
                                 "--", *METADATA_ROOTS).split("\0"))
    before = set(publication.git("ls-tree", "-r", "--name-only", "-z", base,
                                "--", *METADATA_ROOTS).split("\0"))
    names, cells = set(), set()
    for path in sorted(paths):
        if not path.endswith(".json"):
            continue
        # Only the Frontier Cell loader excludes these names. Publication and
        # lesson loaders include every JSON file, even _prefixed/schema files.
        if path.startswith("research-wiki/frontier-cells/") and (
            Path(path).name.startswith("_") or Path(path).name == "schema.json"
        ):
            continue
        old = _metadata_records(path, json.loads(publication.git("show", f"{base}:{path}"))) if path in before else {}
        current = ROOT / path
        new = _metadata_records(path, json.loads(current.read_text())) if current.exists() else {}
        target = cells if path.startswith("research-wiki/frontier-cells/") else names
        for key in old.keys() | new.keys():
            if old.get(key) != new.get(key):
                target.add((new.get(key) or old[key])[0])
    return names, cells


def scope(base: str, items: list[dict]) -> tuple[set[str], set[str]]:
    names, cells = affected_metadata(base)
    names |= publication.changed_declarations(base)
    names |= {b["declaration"] for i in items for b in i["bindings"] if b.get("cell") in cells}
    return names, cells


def validate_cell(name: str, cell: dict, lesson: dict | None = None) -> list[str]:
    errors = []
    label = f"{name} ({cell.get('cell_id', 'missing cell')})"
    reader = cell.get("reader_contract")
    if not isinstance(reader, dict):
        errors.append(f"{label}: Frontier Cell reader_contract required")
    else:
        if reader.get("reference_standard") != REFERENCE_READER:
            errors.append(f"{label}: reader reference must be {REFERENCE_READER}")
        for flag in READER_FLAGS:
            if reader.get(flag) is not True:
                errors.append(f"{label}: reader_contract.{flag}=true required")
    for key in (("astis_dependencies", "mathlib_dependencies", "sources") if lesson is not None else ()):
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
            missing = sorted(set((lesson or {}).get("astis_dependencies", [])) - set(reused))
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
    return errors


def validate_targets(targets: set[str], items: list[dict], data: dict,
                     changed_cells: set[str] | None = None) -> list[str]:
    errors, seen, checked_cells = [], set(), set()
    for item in items:
        for binding in item.get("bindings", []):
            name = binding.get("declaration", "")
            if name not in targets:
                continue
            seen.add(name)
            cell_id = binding.get("cell", "")
            checked_cells.add(cell_id)
            errors += validate_cell(name, data["cells"].get(cell_id, {}), data["lessons"].get(name, {}))
    for cell_id in sorted((changed_cells or set()) - checked_cells):
        cell = data["cells"].get(cell_id)
        # Removing an unbound planned cell does not invent a theorem obligation.
        # Removing a bound cell is rejected by the publication gate.
        if cell is not None:
            name = cell.get("shared_floor_audit", {}).get("canonical_declaration") or cell_id
            errors += validate_cell(name, cell)
    for name in sorted(targets - seen):
        errors.append(f"{name}: changed declaration/metadata lacks contributor-contract publication binding")
    return errors


def validate(base: str | None) -> list[str]:
    base = resolve_base(base)
    items, data = publication.load(), publication.inputs()
    targets, cells = scope(base, items)
    return validate_targets(targets, items, data, cells)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check",))
    parser.add_argument("--base")
    parser.add_argument("--ci", action="store_true")
    args = parser.parse_args(argv)
    try:
        base = resolve_base(args.base, ci=args.ci)
        items, data = publication.load(), publication.inputs()
        targets, cells = scope(base, items)
        errors = validate_targets(targets, items, data, cells)
        print(f"Contributor scope: base={base}; HEAD={publication.git('rev-parse', 'HEAD').strip()}; "
              f"affected declarations={len(targets)}; changed cells={len(cells)}")
        print("Scope includes base-to-working-tree edits and untracked production/metadata files.")
        for name in sorted(targets):
            print(f"- declaration: {name}")
        for cell in sorted(cells):
            print(f"- cell: {cell}")
        if errors:
            print("ASTIS contributor contract failed:", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        if not targets and not cells:
            print("ASTIS contributor contract N/A: no affected declarations or cells; "
                  "this is not a full inventory or semantic audit")
        else:
            print("ASTIS contributor contract PASS (affected metadata only; "
                  "publication/semantic/Lean gates remain required)")
        return 0
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        print(f"ASTIS contributor contract failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
