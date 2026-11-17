#!/usr/bin/env python3
"""Incremental contributor contract for changed ASTIS production declarations."""
from __future__ import annotations

import argparse
import os
import json
import re
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


def validate_cell(name: str, cell: dict, lesson: dict | None = None,
                  *, canonical_owner: str | None = None) -> list[str]:
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
            if (canonical_owner or name) not in new_shared:
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
        try:
            cell, owner = associated_private_cell(name, items, data)
        except (ValueError, KeyError, TypeError, OSError) as exc:
            errors.append(f"{name}: {exc}")
        else:
            # Keep the private target in scope and check its actual lesson too.
            # This does not add a public binding, graph node, or theorem credit.
            errors += validate_cell(name, cell, data["lessons"].get(name, {}), canonical_owner=owner)
    return errors


def associated_private_cell(name: str, items: list[dict], data: dict) -> tuple[dict, str]:
    """Cover an explicitly associated private consumer with both fresh reviews.

    A label alone cannot exempt a changed lesson. The unique public owner must
    pass publication validation, and the explicit private registry must pass the
    complete existing semantic contract against the exact current module/lesson.
    """
    associations = [(item, row) for item in items
                    for row in item.get("associated_private_consumers", [])
                    if row.get("declaration") == name]
    if len(associations) != 1:
        raise ValueError("changed declaration/metadata lacks unique contributor-contract publication binding or private association")
    item, row = associations[0]
    owner = row["owner_public_declaration"]
    bindings = [b for i in items for b in i["bindings"] if b["declaration"] == owner]
    if (len(bindings) != 1 or bindings[0] not in item["bindings"]
            or row.get("separate_public_node") is not False
            or any(b["declaration"] == name for i in items for b in i["bindings"])):
        raise ValueError("private association must have one public owner and no public consumer binding")
    binding = bindings[0]
    cell = data["cells"][binding["cell"]]
    locators = [r for r in cell.get("associated_private_consumer_audits", [])
                if r.get("declaration") == name]
    if len(locators) != 1 or locators[0].get("audit_id") != row.get("audit_id"):
        raise ValueError("private association needs one explicit matching audit locator")
    relative = Path(locators[0]["registry"])
    path = ROOT / relative
    if (relative.is_absolute() or ".." in relative.parts or path.is_symlink()
            or not path.resolve().is_relative_to((ROOT / "research-wiki").resolve()) or not path.is_file()):
        raise ValueError("private registry must be an explicit regular research-wiki file")
    registry = publication.roundtrip.load_registry(path)
    violations = publication.roundtrip.validate_registry(registry)
    if violations:
        raise ValueError("private semantic contract failed: " + "; ".join(violations))
    audits = [a for a in registry["audits"] if a["id"] == row["audit_id"]]
    if len(audits) != 1:
        raise ValueError("private registry lacks unique associated audit")
    audit = audits[0]
    decl = data["declarations"][name]
    lesson = data["lessons"].get(name)
    if not lesson or decl.has_placeholder:
        raise ValueError("private consumer needs an authored lesson and a declaration without placeholders")
    for dependency in lesson.get("astis_dependencies", []) + lesson.get("helpers", []):
        if dependency not in data["declarations"]:
            raise ValueError(f"unknown lesson dependency {dependency}; use an exact declaration id, not explanatory prose")
    clean = publication.astis_site.sanitize_lean(decl.source_text)
    header = re.match(r"\s*(?:@\[[^\]]*\]\s*)*((?:(?:noncomputable|private|protected|local|unsafe)\s+)*)(theorem|lemma)\s+", clean)
    if not header or "private" not in header.group(1).split():
        raise ValueError("associated consumer must be an actual private theorem or lemma")
    public_audit = data["audits"].get(binding.get("audit_id"), {})
    if (public_audit.get("state") not in {"accepted", "source-reviewed"}
            or public_audit.get("source_review", {}).get("state") != "accepted"
            or publication.validate([item], data, strict_names={owner})):
        raise ValueError("private association has no fresh accepted public owner review")
    context = audit["publication_context"]
    associated = context["associated_private_consumer"]
    module = associated["whole_module"]
    whole_review = audit["source_review"]["whole_module_review"]
    module_text = (ROOT / decl.source_file).read_text(encoding="utf-8")
    module_sha = publication.file_digest(decl.source_file)
    if (audit.get("state") not in {"accepted", "source-reviewed"}
            or audit["source_review"].get("state") != "accepted"
            or audit["lean"]["declaration"] != name or audit["lean"]["file"] != decl.source_file
            or associated.get("owner_public_declaration") != owner
            or associated.get("separate_public_node") is not False
            or module["file"] != decl.source_file or module["text"] != module_text or module["sha256"] != module_sha
            or whole_review["file"] != decl.source_file or whole_review["sha256"] != module_sha
            or whole_review.get("all_helpers_imports_scoped_context_reviewed") is not True
            or whole_review.get("new_axiom_or_placeholder_found") is not False
            or associated["lesson"] != data["lessons"].get(name)
            or associated["lean_statement"] != audit["lean"]["statement"]
            or context["binding"]["declaration"] != owner
            or audit["publication_binding_sha256"] != publication.binding_digest(item, binding, data)):
        raise ValueError("private association review is stale or does not match current code, lesson, owner and binding")
    return cell, owner


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
