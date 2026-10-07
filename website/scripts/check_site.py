#!/usr/bin/env python3
"""Validate ASTIS pages, inventory, status, source links, diagrams, and assets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "website" / "scripts"))

import astis_site  # noqa: E402
import astis_site_source_index  # noqa: E402
import astis_source  # noqa: E402
import chewi_source_first_contract  # noqa: E402
import chewi_source_first_refinement  # noqa: E402
import chewi_source_first_scope  # noqa: E402
import implicit_prerequisites  # noqa: E402
import lean_tutor  # noqa: E402
import reader_contract_final  # noqa: E402
import source_foundations  # noqa: E402
import cross_domain  # noqa: E402
import openai_math_intake  # noqa: E402
import proof_readers  # noqa: E402
import declaration_lessons  # noqa: E402
import publication_reader  # noqa: E402
import metadata_lessons  # noqa: E402
import inline_lean  # noqa: E402
import samplewiki_companions  # noqa: E402
import research_workspace  # noqa: E402


# Validation must resolve Registry entries with the same declaration parser used
# to build the public source inventory. Dotted local names still inherit their
# surrounding namespace.
astis_site_source_index.install(astis_site)


def source_first_proof_coverage_errors(output: Path) -> list[str]:
    """Validate proof supplements against the final theorem-first DOM.

    ``reader_contract_final`` originally emitted ``data-source-proof`` details.
    The later ``chewi_source_first_contract`` deliberately reconstructs every
    source card into the permanent statement/proof/assumptions/ASTIS/Lean order,
    so those intermediate DOM markers no longer survive. The proof equations do
    survive and are the stronger invariant to check here.
    """

    errors: list[str] = []
    sources = reader_contract_final._source_entries()
    proofs = reader_contract_final._proof_supplements()
    for source_id, proof in proofs.items():
        source = sources.get(source_id)
        if source is None:
            continue
        section = str(source.get("section", ""))
        path = reader_contract_final.base.section_path(output, section)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        card = reader_contract_final._source_card_for_id(text, source_id)
        if card is None:
            errors.append(f"{path.relative_to(output)}: missing final source card for proof {source_id}")
            continue

        expected = [
            str(step.get("formula", "")).strip()
            for step in proof.get("steps", [])
            if isinstance(step, dict) and str(step.get("formula", "")).strip()
        ]
        for formula in expected:
            escaped = reader_contract_final.base.esc(formula)
            if escaped not in card:
                errors.append(
                    f"{path.relative_to(output)}: final source card {source_id} is missing proof equation {formula}"
                )

        source_status = str(proof.get("source_status", ""))
        if expected and source_status == "source_proof" and "source-contract-chewi-proof" not in card:
            errors.append(
                f"{path.relative_to(output)}: {source_id} source proof is not in the Chewi proof layer"
            )
        if expected and source_status == "astis_expansion" and "source-contract-astis-latex" not in card:
            errors.append(
                f"{path.relative_to(output)}: {source_id} ASTIS proof expansion is not in the folded ASTIS layer"
            )
    return errors


def source_first_implicit_prerequisite_errors(output: Path) -> list[str]:
    """Validate implicit prerequisites in their final source-first form.

    The early prerequisite renderer includes a large foundation/reference panel
    and ``data-lean-declaration`` attributes. The final source-first pass
    intentionally condenses the public card to mathematical statement,
    assumptions, proof, and folded Lean links. We therefore validate those
    reader-facing invariants on the final card while separately requiring the
    generated data packet to retain ``used_for`` and foundation metadata.
    """

    errors: list[str] = []
    try:
        items = implicit_prerequisites.load_items()
        url_map = implicit_prerequisites.declaration_url_map(output)
    except Exception as exc:
        return [str(exc)]

    data_path = output / "data" / "implicit-prerequisites.json"
    if not data_path.exists():
        errors.append("generated data/implicit-prerequisites.json is missing")
        generated_by_id: dict[str, dict[str, object]] = {}
    else:
        try:
            raw = json.loads(data_path.read_text(encoding="utf-8"))
            generated_by_id = {
                str(item.get("id", "")): dict(item)
                for item in raw
                if isinstance(item, dict) and item.get("id")
            } if isinstance(raw, list) else {}
        except Exception as exc:
            errors.append(f"generated data/implicit-prerequisites.json is unreadable: {exc}")
            generated_by_id = {}

    for item in items:
        item_id = str(item["id"])
        section = str(item["section"])
        path = implicit_prerequisites.section_path(output, section)
        if not path.exists():
            errors.append(f"missing generated section for implicit prerequisite {item_id}: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        pattern = re.compile(
            rf'<article class="[^"]*\bsource-contract-implicit\b[^"]*"[^>]*'
            rf'id="{re.escape(chewi_source_first_contract.esc(item_id))}"[^>]*>.*?</article>',
            flags=re.S,
        )
        match = pattern.search(text)
        if not match:
            errors.append(f"{path}: {item_id} is not rendered as a final implicit-prerequisite card")
            continue
        card = match.group(0)

        required = (
            ('data-provenance="astis-implicit-prerequisite"', "ASTIS provenance"),
            (chewi_source_first_contract.esc(item["latex_statement"]), "LaTeX statement"),
            ("source-contract-implicit-proof", "visible mathematical proof"),
            ("<h3>Mathematical proof</h3>", "mathematical proof label"),
            ("source-contract-lean", "folded Lean disclosure"),
            ("<summary>Source mapping and supporting declarations</summary>", "source-mapping disclosure label"),
        )
        for needle, label in required:
            if needle not in card:
                errors.append(f"{path}: {item_id} missing {label}")

        expected_proof = chewi_source_first_contract.IMPLICIT_PROOF_OVERRIDES.get(
            item_id, str(item["proof"])
        )
        proof_html = chewi_source_first_contract.esc(
            chewi_source_first_refinement.mathify(expected_proof)
        )
        if proof_html not in card:
            errors.append(f"{path}: {item_id} missing final mathematical proof text")

        why_html = chewi_source_first_contract.esc(
            chewi_source_first_refinement.mathify(item["why_needed"])
        )
        if why_html not in card:
            errors.append(f"{path}: {item_id} missing why-needed context")

        for assumption in item["assumptions"]:
            assumption_html = chewi_source_first_contract.esc(
                chewi_source_first_refinement.mathify(assumption)
            )
            if assumption_html not in card:
                errors.append(f"{path}: {item_id} missing explicit assumption: {assumption}")

        for declaration in [str(value) for value in item["lean_declarations"]]:
            url = url_map.get(declaration)
            if str(item["lean_status"]) == "compiled" and not url:
                errors.append(
                    f"{path}: {item_id} compiled declaration has no generated destination: {declaration}"
                )
                continue
            if chewi_source_first_contract.esc(declaration) not in card:
                errors.append(f"{path}: {item_id} missing Lean declaration: {declaration}")
            if url and f'href="../../{chewi_source_first_contract.esc(url)}"' not in card:
                errors.append(f"{path}: {item_id} missing resolved Lean destination for {declaration}")

        generated = generated_by_id.get(item_id)
        if generated is None:
            errors.append(f"generated prerequisite data is missing {item_id}")
        else:
            if generated.get("used_for") != item.get("used_for"):
                errors.append(f"generated prerequisite data lost used_for metadata for {item_id}")
            if generated.get("foundation_sources", []) != item.get("foundation_sources", []):
                errors.append(f"generated prerequisite data lost foundation metadata for {item_id}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="", help="output directory (default: _site)")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--require-chapter-1-closure", action="store_true")
    parser.add_argument("--require-full-exposition", action="store_true")
    args = parser.parse_args()
    source_errors, _ = astis_source.validate_source_contract()
    if source_errors:
        print("Chewi source check failed:", file=sys.stderr)
        for error in source_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    argv = ["check"]
    output = Path(args.output).resolve() if args.output else ROOT / "_site"
    if args.output:
        argv.extend(["--output", args.output])
    if args.rebuild:
        argv.append("--rebuild")
    if args.require_chapter_1_closure:
        argv.append("--require-chapter-1-closure")
    result = astis_site.main(argv)
    if result != 0:
        return result

    # The source-first renderer is the final owner of theorem/proof DOM. Keep
    # the older reader validator for its broad page/formula/style checks, but
    # make its proof coverage inspect the final equations instead of obsolete
    # intermediate data-source-proof markers.
    reader_contract_final._proof_coverage_errors = source_first_proof_coverage_errors
    try:
        reader_contract_final.validate(output)
    except Exception as exc:
        print("Final math-first reader site check failed:", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1

    # Re-run the actual final Chewi contract with the same refinements/scope as
    # build_site.py. This checks the permanent reader order and the block-aware
    # raw-math gate on the final deploy tree.
    try:
        chewi_source_first_refinement.patch(chewi_source_first_contract)
        chewi_source_first_scope.patch(chewi_source_first_contract)
        chewi_source_first_contract.validate(output)
    except Exception as exc:
        print("Final Chewi source-first site check failed:", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1

    # These remain independent evidence checks. The final reader may change
    # presentation, but it may not erase or rewrite audited source/foundation
    # data beneath that presentation.
    foundation_errors = source_foundations.validate_site(output)
    if foundation_errors:
        print("Source foundation site check failed:", file=sys.stderr)
        for error in foundation_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    implicit_errors = source_first_implicit_prerequisite_errors(output)
    if implicit_errors:
        print("Final implicit prerequisite site check failed:", file=sys.stderr)
        for error in implicit_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    try:
        cross_domain.validate_site(output)
    except Exception as exc:
        print(f"Cross-domain source/route/hypergraph check failed: {exc}", file=sys.stderr)
        return 1

    openai_errors = openai_math_intake.validate_site(output)
    if openai_errors:
        print("OpenAI Math intake site check failed:", file=sys.stderr)
        for error in openai_errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    tutor_errors = lean_tutor.validate_site(output)
    if tutor_errors:
        print("Lean learning studio site check failed:", file=sys.stderr)
        for error in tutor_errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    reader_errors = proof_readers.validate_site(output)
    reader_errors.extend(samplewiki_companions.validate_site(output))
    reader_errors.extend(research_workspace.validate_site(output))
    reader_errors.extend(declaration_lessons.validate_site(output, require_complete=args.require_full_exposition))
    reader_errors.extend(publication_reader.validate_site(output))
    reader_errors.extend(inline_lean.validate_textbook(output))
    reader_errors.extend(metadata_lessons.validate_site(output))
    if reader_errors:
        for error in reader_errors:
            print(f"Proof reader check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
