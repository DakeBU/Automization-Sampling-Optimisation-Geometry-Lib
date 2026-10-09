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
