#!/usr/bin/env python3
"""Validate and summarize collaborative ASTIS Frontier Cell records.

A Frontier Cell is the GitHub-visible unit of mathematical progress used by the
SampleWiki, Riemannian Optimization, Optimisation, and shared-foundation lanes.
The validator is intentionally stdlib-only so it can run in every ASTIS CI job.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CELL_ROOT = ROOT / "research-wiki" / "frontier-cells"
PROCESS_MEMORY = ROOT / "research-wiki" / "process-memory.json"

ROUTES = {"samplewiki-route", "riemannian-optimization", "optimisation", "statistical-optimal-transport", "higher-order-sampling", "discrete-sampling", "mcmc", "shared"}
MODES = {"faithfulPaper", "exploratoryProof"}
STATUSES = {
    "claimed",
    "proved_locally",
    "independently_verified",
    "stabilized",
    "merged",
    "blocked",
    "quarantined",
}
CLASSIFICATIONS = {"reuse", "adapt", "missing", "out_of_scope"}
DECISIONS = {
    "reuse_existing",
    "adapt_existing",
    "new_route_local",
    "new_canonical_shared",
    "out_of_scope",
}
FAILURE_CLASSES = {
    "REFUTED",
    "SOURCE_INVALID",
    "API_BLOCKED",
    "ENV_BLOCKED",
    "IMPLEMENTATION_FAILED",
    "NONE",
}
SALVAGE_STATUSES = {"pending", "completed", "not-applicable"}
PARALLEL_DECISIONS = {"serial", "parallel"}
CROSS_ROUTE_STATUSES = {"pending", "accepted", "not-applicable"}
PURIFICATION_STATUSES = {"pending", "purified", "not-applicable"}
EXPOSITION_STATUSES = {"pending", "accepted", "not-applicable"}


def cell_paths(root: Path = DEFAULT_CELL_ROOT) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.rglob("*.json")
        if not path.name.startswith("_") and path.name != "schema.json"
    )


def load_cells(root: Path = DEFAULT_CELL_ROOT) -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = []
    for path in cell_paths(root):
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            cells.append({"__path__": str(path), "__load_error__": str(exc)})
            continue
        if not isinstance(raw, dict):
            cells.append({"__path__": str(path), "__load_error__": "top level must be an object"})
            continue
        raw["__path__"] = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        cells.append(raw)
    return cells


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_cells(cells: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: dict[str, str] = {}
    process_memory_ids: set[str] = set()
    try:
        memory = json.loads(PROCESS_MEMORY.read_text(encoding="utf-8"))
        process_memory_ids = {
            str(entry.get("id", "")).strip()
            for entry in memory.get("entries", [])
            if isinstance(entry, dict) and str(entry.get("id", "")).strip()
        }
    except Exception as exc:
        errors.append(f"process memory unavailable: {exc}")
    common = (
        "schema_version",
        "cell_id",
        "route",
        "title",
        "mode",
        "source_anchor",
        "target_statement",
        "status",
        "parents",
        "consumers",
        "shared_floor_audit",
        "evidence",
        "blocked",
    )

    for cell in cells:
        path = str(cell.get("__path__", "<unknown>"))
        if "__load_error__" in cell:
            errors.append(f"{path}: unreadable cell: {cell['__load_error__']}")
            continue
        missing = [key for key in common if key not in cell]
        if missing:
            errors.append(f"{path}: missing required fields {missing}")
            continue

        cell_id = str(cell.get("cell_id", "")).strip()
        if not cell_id:
            errors.append(f"{path}: empty cell_id")
        elif cell_id in seen:
            errors.append(f"{path}: duplicate cell_id {cell_id!r}; first seen in {seen[cell_id]}")
        else:
            seen[cell_id] = path

        route = str(cell.get("route", ""))
        status = str(cell.get("status", ""))
        mode = str(cell.get("mode", ""))
        if route not in ROUTES:
            errors.append(f"{path}: invalid route {route!r}")
        if status not in STATUSES:
            errors.append(f"{path}: invalid status {status!r}")
        if mode not in MODES:
            errors.append(f"{path}: invalid mode {mode!r}")
        if not _nonempty(cell.get("title")):
            errors.append(f"{path}: title must be non-empty")
        if not _nonempty(cell.get("source_anchor")):
            errors.append(f"{path}: source_anchor must pin an exact source location")
        if not _nonempty(cell.get("target_statement")):
            errors.append(f"{path}: target_statement must be non-empty")
        if not isinstance(cell.get("parents"), list) or not isinstance(cell.get("consumers"), list):
            errors.append(f"{path}: parents and consumers must be lists")

        audit = cell.get("shared_floor_audit")
        if not isinstance(audit, dict):
            errors.append(f"{path}: shared_floor_audit must be an object")
            audit = {}
        searched = audit.get("searched")
        classification = str(audit.get("classification", ""))
        decision = str(audit.get("decision", ""))
        canonical = str(audit.get("canonical_declaration", "")).strip()
        canonical_shared_cell = str(audit.get("canonical_shared_cell", "")).strip()
        if not isinstance(searched, list) or not searched:
            errors.append(f"{path}: shared_floor_audit.searched must record at least one reuse search")
        if classification not in CLASSIFICATIONS:
            errors.append(f"{path}: invalid shared-floor classification {classification!r}")
        if decision not in DECISIONS:
            errors.append(f"{path}: invalid shared-floor decision {decision!r}")
        if decision in {"reuse_existing", "adapt_existing"} and not canonical:
            errors.append(f"{path}: {decision} requires canonical_declaration")
        if decision == "new_canonical_shared":
            if route == "shared":
                if len(_list(cell.get("consumers"))) < 2:
                    errors.append(f"{path}: a shared Frontier Cell must name at least two consuming routes")
            elif not canonical_shared_cell:
                errors.append(
                    f"{path}: route-local detection of a missing shared foundation must name canonical_shared_cell"
                )
            if route != "shared" and status not in {"claimed", "blocked", "quarantined"}:
                errors.append(
                    f"{path}: route-local cell may not implement a new shared foundation; open/use the shared cell first"
                )

        schema_version = cell.get("schema_version")
        if (route in {"statistical-optimal-transport", "higher-order-sampling", "discrete-sampling", "mcmc"} or "mcmc" in _list(cell.get("consumers"))) and schema_version not in {2, 3}:
            errors.append(f"{path}: new cross-domain routes require schema_version 2 or 3")
        if schema_version not in {1, 2, 3}:
            errors.append(f"{path}: unsupported schema_version")
        if schema_version in {2, 3}:
            searches = " ".join(map(str, searched or [])).lower()
            for library in ("samplinglib", "mathlib"):
                if library not in searches:
                    errors.append(f"{path}: schema-2 cells must search {library}")
            detail = cell.get("source_detail_audit")
            if not isinstance(detail, dict):
                errors.append(f"{path}: schema-2 cells require source_detail_audit")
                detail = {}
            for key in ("primary_edition", "primary_anchor", "fidelity_boundary"):
                if not _nonempty(detail.get(key)):
                    errors.append(f"{path}: source_detail_audit.{key} must be explicit")
            detail_status = detail.get("detail_status")
            if detail_status not in {"sufficient", "omitted", "cites_external"}:
                errors.append(f"{path}: invalid source detail status")
            if detail_status in {"omitted", "cites_external"}:
                if not _nonempty(detail.get("gap")):
                    errors.append(f"{path}: omitted source detail requires an exact gap")
                consulted = detail.get("consulted")
                if not isinstance(consulted, list) or not consulted:
                    errors.append(f"{path}: omitted source detail requires a consulted background theorem")
                else:
                    for reference in consulted:
                        if not isinstance(reference, dict) or any(not _nonempty(reference.get(k)) for k in ("source", "anchor", "hypothesis_adapter")):
                            errors.append(f"{path}: background reference needs source, anchor, hypothesis_adapter")
            if route == "higher-order-sampling":
                comparison = cell.get("comparison_contract", {})
                if not isinstance(comparison, dict):
                    comparison = {}
                for key in ("potential_class", "smoothness_p", "oracle_q", "dynamics_k", "accuracy_r", "metric", "start", "cost"):
                    if not _nonempty(comparison.get(key)):
                        errors.append(f"{path}: higher-order sampling needs comparison_contract.{key}")


        if schema_version == 3:
            learning = cell.get("learning_contract")
            if not isinstance(learning, dict):
                errors.append(f"{path}: schema-3 cells require learning_contract")
                learning = {}

            if learning.get("control_plane_math_authority") is not False:
                errors.append(f"{path}: learning_contract.control_plane_math_authority must be false")
            if learning.get("process_memory_checked") is not True:
                errors.append(f"{path}: learning_contract.process_memory_checked must be true")

            memory_ids = learning.get("process_memory_ids")
            if not isinstance(memory_ids, list) or any(not _nonempty(item) for item in memory_ids):
                errors.append(f"{path}: learning_contract.process_memory_ids must be a string list")
                memory_ids = []
            unknown_memory = sorted(set(memory_ids) - process_memory_ids)
            if unknown_memory:
                errors.append(f"{path}: unknown process-memory ids {unknown_memory}")

            failure_class = learning.get("failure_class")
            if failure_class not in FAILURE_CLASSES:
                errors.append(f"{path}: invalid learning_contract.failure_class")

            salvage = learning.get("salvage")
            if not isinstance(salvage, dict):
                errors.append(f"{path}: learning_contract.salvage must be an object")
                salvage = {}
            if salvage.get("status") not in SALVAGE_STATUSES:
                errors.append(f"{path}: invalid salvage status")
            if not isinstance(salvage.get("required"), bool):
                errors.append(f"{path}: salvage.required must be boolean")
            if failure_class != "NONE" and salvage.get("required") is not True:
                errors.append(f"{path}: every non-success failure requires an explicit salvage audit")
            if salvage.get("status") == "not-applicable" and not _nonempty(salvage.get("reason")):
                errors.append(f"{path}: not-applicable salvage requires a reason")
            for field in ("promoted_fragments", "discarded_fragments"):
                if not isinstance(salvage.get(field), list):
                    errors.append(f"{path}: salvage.{field} must be a list")

            parallel = learning.get("parallelism")
            if not isinstance(parallel, dict):
                errors.append(f"{path}: learning_contract.parallelism must be an object")
                parallel = {}
            decision_parallel = parallel.get("decision")
            if decision_parallel not in PARALLEL_DECISIONS:
                errors.append(f"{path}: invalid parallelism decision")
            directions = parallel.get("direction_fingerprints")
            if not isinstance(directions, list) or any(not _nonempty(item) for item in directions):
                errors.append(f"{path}: direction_fingerprints must be a string list")
                directions = []
            if len(directions) != len(set(directions)):
                errors.append(f"{path}: direction_fingerprints must be unique")
            if decision_parallel == "parallel":
                if len(directions) < 2:
                    errors.append(f"{path}: parallel work requires at least two distinct direction fingerprints")
                if not _nonempty(parallel.get("expected_information_gain")):
                    errors.append(f"{path}: parallel work requires expected_information_gain")
                if not _nonempty(parallel.get("shared_verified_context_digest")):
                    errors.append(f"{path}: parallel work requires shared_verified_context_digest")

            cross = learning.get("cross_route_blind_spot_audit")
            if not isinstance(cross, dict):
                errors.append(f"{path}: cross_route_blind_spot_audit must be an object")
                cross = {}
            for field in ("evidence", "canonical_route", "selection_reason"):
                if field not in cross or not isinstance(cross.get(field), str):
                    errors.append(f"{path}: cross_route_blind_spot_audit.{field} must be a string")
            if not isinstance(cross.get("required"), bool):
                errors.append(f"{path}: cross_route_blind_spot_audit.required must be boolean")
            if cross.get("status") not in CROSS_ROUTE_STATUSES:
                errors.append(f"{path}: invalid cross-route audit status")
            if decision_parallel == "parallel" and cross.get("required") is not True:
                errors.append(f"{path}: parallel routes require a common-blind-spot audit")
            if status == "merged" and decision_parallel == "parallel" and cross.get("status") != "accepted":
                errors.append(f"{path}: merged parallel route requires accepted common-blind-spot audit")
            if cross.get("status") == "accepted":
                for field in ("evidence", "canonical_route", "selection_reason"):
                    if not _nonempty(cross.get(field)):
                        errors.append(f"{path}: accepted cross-route audit requires {field}")

            reader = learning.get("reader_backpressure")
            if not isinstance(reader, dict):
                errors.append(f"{path}: reader_backpressure must be an object")
                reader = {}
            if reader.get("purification_status") not in PURIFICATION_STATUSES:
                errors.append(f"{path}: invalid purification_status")
            if reader.get("exposition_seal_status") not in EXPOSITION_STATUSES:
                errors.append(f"{path}: invalid exposition_seal_status")
            for field in ("source_expansion_nodes", "lean_expansion_nodes"):
                if not isinstance(reader.get(field), list) or any(not _nonempty(item) for item in reader.get(field, [])):
                    errors.append(f"{path}: reader_backpressure.{field} must be a string list")
            for field in ("assumptions_preserved", "boundary_preserved"):
                if not isinstance(reader.get(field), bool):
                    errors.append(f"{path}: reader_backpressure.{field} must be boolean")
            if "exposition_evidence" not in reader or not isinstance(reader.get("exposition_evidence"), str):
                errors.append(f"{path}: reader_backpressure.exposition_evidence must be a string")
            if reader.get("exposition_seal_status") == "accepted":
                if not _nonempty(reader.get("exposition_evidence")):
                    errors.append(f"{path}: accepted Exposition Seal requires evidence")
                if not reader.get("source_expansion_nodes") or not reader.get("lean_expansion_nodes"):
                    errors.append(f"{path}: accepted Exposition Seal requires source and Lean expansion nodes")
                if reader.get("assumptions_preserved") is not True or reader.get("boundary_preserved") is not True:
                    errors.append(f"{path}: accepted Exposition Seal must preserve assumptions and boundary")
            if reader.get("purification_status") == "purified" and reader.get("exposition_seal_status") != "accepted":
                errors.append(f"{path}: PURIFIED requires an accepted Exposition Seal")
            if mode == "faithfulPaper" and status == "merged" and reader.get("purification_status") == "not-applicable":
                errors.append(f"{path}: merged source-facing work may be pending or purified, not purification-not-applicable")

            if status in {"blocked", "quarantined"} and failure_class == "NONE":
                errors.append(f"{path}: blocked/quarantined schema-3 cell requires a typed failure class")

        if route == "mcmc" or "mcmc" in _list(cell.get("consumers")):
            contract = cell.get("mcmc_contract")
            if not isinstance(contract, dict):
                errors.append(f"{path}: MCMC consumers require mcmc_contract")
                contract = {}
            for key in ("state_space", "target", "support", "operator", "time_model", "clock", "invariance", "ergodicity", "initialization", "metric", "cost", "objective", "source_proof_status"):
                if not _nonempty(contract.get(key)):
                    errors.append(f"{path}: mcmc_contract.{key} must be explicit")
            if contract.get("time_model") not in {"static", "discrete-time", "continuous-time"}:
                errors.append(f"{path}: MCMC time model must be explicit")
            if contract.get("invariance_class") not in {"exact-target", "approximate-target", "not-applicable"}:
                errors.append(f"{path}: MCMC invariance_class must separate exact and approximate targets")
            if contract.get("invariance_class") == "approximate-target" and not _nonempty(contract.get("bias_contract")):
                errors.append(f"{path}: approximate MCMC needs a bias_contract; mixing is not target accuracy")
            if contract.get("time_model") == "discrete-time" and not _nonempty(contract.get("periodicity")):
                errors.append(f"{path}: discrete-time MCMC must address periodicity")

        if route == "discrete-sampling" or "discrete-sampling" in _list(cell.get("consumers")):
            contract = cell.get("discrete_state_contract")
            if not isinstance(contract, dict):
                errors.append(f"{path}: discrete consumers require discrete_state_contract")
                contract = {}
            for key in ("state_space", "support", "target", "operator", "time_model", "clock", "reversibility", "pinning", "regime", "metric", "cost", "source_proof_status"):
                if not _nonempty(contract.get(key)):
                    errors.append(f"{path}: discrete_state_contract.{key} must be explicit")
            if contract.get("time_model") not in {"discrete-time", "continuous-time", "static"}:
                errors.append(f"{path}: discrete time_model must be discrete-time, continuous-time or static")
            if contract.get("time_model") == "discrete-time" and not _nonempty(contract.get("aperiodicity_or_absolute_gap")):
                errors.append(f"{path}: discrete-time claims require aperiodicity_or_absolute_gap (or explicit not-applicable reason)")
            # Static/shared algebra may say why a field is not applicable, but
            # cannot silently omit the finite-state consumer's contract.

        evidence = cell.get("evidence")
        if not isinstance(evidence, dict):
            errors.append(f"{path}: evidence must be an object")
            evidence = {}
        checks = evidence.get("focused_checks")
        if status in {"proved_locally", "independently_verified", "stabilized", "merged"}:
            if not isinstance(checks, list) or not checks:
                errors.append(f"{path}: status {status} requires focused_checks evidence")
        if status in {"independently_verified", "stabilized", "merged"}:
            if not _nonempty(evidence.get("independent_verification")):
                errors.append(f"{path}: status {status} requires independent_verification")
        if status in {"stabilized", "merged"}:
            if not _nonempty(evidence.get("root_build")):
                errors.append(f"{path}: status {status} requires root_build evidence")
            if not _nonempty(evidence.get("graph_regeneration")):
                errors.append(f"{path}: status {status} requires graph_regeneration evidence")
        if status == "merged" and not _nonempty(evidence.get("pr")):
            errors.append(f"{path}: merged cell requires a PR/merge reference")

        blocked = cell.get("blocked")
        if not isinstance(blocked, dict):
            errors.append(f"{path}: blocked must be an object")
            blocked = {}
        if status == "blocked":
            if not _nonempty(blocked.get("reason")):
                errors.append(f"{path}: blocked cell requires an exact blocker reason")
            if not isinstance(blocked.get("children"), list) or not blocked.get("children"):
                errors.append(f"{path}: blocked cell must name at least one smaller child Frontier Cell")
        if status == "quarantined" and not _nonempty(blocked.get("reason")):
            errors.append(f"{path}: quarantined cell requires a reason")

    return errors


def summarize(cells: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    by_route: dict[str, Counter[str]] = defaultdict(Counter)
    for cell in cells:
        if "__load_error__" in cell:
            continue
        route = str(cell.get("route", ""))
        status = str(cell.get("status", ""))
        if route in ROUTES and status in STATUSES:
            by_route[route][status] += 1
    return {route: dict(counter) for route, counter in sorted(by_route.items())}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "summary"))
    parser.add_argument("--root", default=str(DEFAULT_CELL_ROOT))
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    cells = load_cells(root)
    errors = validate_cells(cells)
    if errors:
        print("ASTIS Frontier Cell protocol check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if args.command == "summary":
        print(json.dumps(summarize(cells), indent=2, sort_keys=True))
    else:
        print(f"ASTIS Frontier Cell protocol check passed: {len(cells)} registered cells")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
