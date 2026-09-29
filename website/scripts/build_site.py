#!/usr/bin/env python3
"""Build the ASTIS literate formalization website."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "website" / "scripts"))

import astis_site  # noqa: E402
import astis_site_source_index  # noqa: E402
import chapter1_reference_shelf  # noqa: E402
import chewi_source_audit_guard  # noqa: E402
import chewi_source_first_contract  # noqa: E402
import chewi_source_first_refinement  # noqa: E402
import chewi_source_first_scope  # noqa: E402
import formalization_progress  # noqa: E402
import declaration_lessons  # noqa: E402
import publication_reader  # noqa: E402
import metadata_lessons  # noqa: E402
import inline_lean  # noqa: E402
import proof_readers  # noqa: E402
import harness  # noqa: E402
import implicit_prerequisites  # noqa: E402
import information_architecture  # noqa: E402
import lean_tutor  # noqa: E402
import library_shelves  # noqa: E402
import reader_contract_final  # noqa: E402
import samplewiki_audit_queue  # noqa: E402
import samplewiki_casebook_assets  # noqa: E402
import samplewiki_casebook_polish  # noqa: E402
import samplewiki_examples  # noqa: E402
import samplewiki_frontier_audit  # noqa: E402
import samplewiki_math_render  # noqa: E402
import samplewiki_primary_audit_additions  # noqa: E402
import samplewiki_reader_contract  # noqa: E402
import samplewiki_companions  # noqa: E402
import source_foundations  # noqa: E402
import source_lineage  # noqa: E402
import textbook_math_contract  # noqa: E402
import theorem_lessons  # noqa: E402
import undergrad_guides  # noqa: E402
import underlying_lean_graph  # noqa: E402
import visual_polish  # noqa: E402


astis_site_source_index.install(astis_site)


ORGANIZER_FOOTER_INPUTS = (
    (
        "<p>Organized by Dake Bu, Ji Cheng, Atsushi Nitanda, Hau-San Wong, "
        "and Qingfu Zhang.</p>"
    ),
    (
        "<p>Organized by Dake Bu, Ji Cheng, Huanjian Zhou, Andi Han, "
        "Zonghao Chen, Sinho Chewi, Matthew S. Zhang, Hau-San Wong, "
        "Qingfu Zhang, and Atsushi Nitanda.</p>"
    ),
)
CANONICAL_ORGANIZER_FOOTER = (
    "<p><strong>Organizer (Authors):</strong> Dake Bu, Ji Cheng, Huanjian Zhou, "
    "Andi Han, Zonghao Chen, Sinho Chewi, Matthew S. Zhang, Hau-San Wong, "
    "Qingfu Zhang, and Atsushi Nitanda.</p>"
)


def repair_final_content_anchors(output: Path) -> None:
    """Keep the global skip-link target valid after all reader overlays."""
    for path in sorted(output.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        if 'href="#content"' not in text or 'id="content"' in text:
            continue
        repaired, count = re.subn(
            r"<main(?![^>]*\bid=)([^>]*)>",
            r'<main id="content"\1>',
            text,
            count=1,
            flags=re.I,
        )
        if count != 1:
            raise RuntimeError(
                f"{path.relative_to(output)}: skip link targets #content but no repairable <main> exists"
            )
        path.write_text(repaired, encoding="utf-8", newline="\n")



def repair_project_author_footer(output: Path) -> None:
    """Keep every generated page aligned with the canonical ASTIS author list."""
    for path in sorted(output.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        original = text
        for source_footer in ORGANIZER_FOOTER_INPUTS:
            text = text.replace(source_footer, CANONICAL_ORGANIZER_FOOTER)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
        if (
            "Samplinglib</strong> is the public formal library and learning interface"
            in text
            and CANONICAL_ORGANIZER_FOOTER not in text
        ):
            raise RuntimeError(
                f"{path.relative_to(output)}: Samplinglib footer is missing the canonical Organizer (Authors) list"
            )


def write_underlying_graph_alias(output: Path) -> None:
    """Keep the public /underlying-lean-graph/ route as a stable alias."""
    rel_path = "underlying-lean-graph/index.html"
    body = """
<section class="page-hero compact">
  <div class="eyebrow">Samplinglib · formal graph</div>
  <h1>Underlying Lean Graph of Libraries</h1>
  <p class="lede">This stable route forwards to the interactive Proof Atlas and underlying Lean graph.</p>
  <p><a class="button primary" href="../lean-foundations.html">Open the graph</a></p>
</section>
"""
    text = astis_site.page(
        "Underlying Lean Graph of Libraries",
        rel_path,
        body,
        active="Lean Foundations",
        description="Stable route to the Samplinglib Underlying Lean Graph of Libraries.",
    )
    text = text.replace(
        "</head>",
        '  <link rel="canonical" href="../lean-foundations.html">\n'
        '  <meta http-equiv="refresh" content="2; url=../lean-foundations.html">\n'
        '  <script src="../assets/graph-alias.js"></script>\n'
        "</head>",
        1,
    )
    astis_site.write_page(output, rel_path, text)


def inherit_final_reader_contract(output: Path) -> None:
    """Attach the final reader stylesheet to pages added after its render pass."""
    style_name = reader_contract_final.STYLE_NAME
    for path in sorted(output.rglob("*.html")):
        rel = path.relative_to(output)
        prefix = "../" * len(rel.parent.parts)
        href = f"{prefix}assets/{style_name}"
        text = path.read_text(encoding="utf-8")
        if href in text:
            continue
        if "</head>" not in text:
            raise RuntimeError(f"{rel}: missing </head> while inheriting final reader contract")
        text = text.replace(
            "</head>",
            f'  <link rel="stylesheet" href="{href}">\n</head>',
            1,
        )
        path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="", help="output directory (default: _site)")
    args = parser.parse_args()
    argv = ["build"]
    output = Path(args.output).resolve() if args.output else ROOT / "_site"
    if args.output:
        argv.extend(["--output", args.output])
    result = astis_site.main(argv)
    if result != 0:
        return result

    undergrad_guides.enrich_site(output)
    theorem_lessons.enrich_site(output)
    source_foundations.enrich_site(output)
    implicit_prerequisites.enrich_site(output)
    lean_tutor.enrich_site(output)
    samplewiki_examples.enrich_site(output)
    information_architecture.enrich_site(output)
    samplewiki_math_render.enrich_site(output)
    samplewiki_frontier_audit.enrich_site(output)
    samplewiki_audit_queue.enrich_site(output)
    chapter1_reference_shelf.enrich_site(output)
    visual_polish.enrich_site(output)

    textbook_math_contract.patch_reader_contract(reader_contract_final)
    reader_contract_final.enrich_site(output)
    textbook_math_contract.enrich_site(output, reader_contract_final)

    chewi_source_audit_guard.enrich_site(output)
    chewi_source_first_refinement.patch(chewi_source_first_contract)
    chewi_source_first_scope.patch(chewi_source_first_contract)
    chewi_source_first_contract.enrich_site(output)

    samplewiki_casebook_polish.patch(samplewiki_reader_contract)
    samplewiki_primary_audit_additions.patch(samplewiki_reader_contract)
    samplewiki_reader_contract.enrich_site(output)
    samplewiki_casebook_assets.enrich_site(output)

    underlying_lean_graph.enrich_site(output)

    harness.enrich_site(output)
    harness.validate_site(output)

    write_underlying_graph_alias(output)
    library_shelves.enrich_site(output)

    # Mathematical provenance comes before the final Current Progress overlay.
    # source_lineage still owns the primary/supplement/background source layers
    # and library theme normalization; the collaboration dashboard then becomes
    # the final owner of every /progress/ route so no late overlay can recreate
    # a separate blue Riemannian/Optimisation mini-site.
    source_lineage.enrich_site(output)

    # Current Progress is one project-level collaboration board. It preserves the
    # detailed SampleWiki dependency view as a drill-down, redirects historical
    # per-route URLs to anchors, renders Frontier Cell records, and enforces the
    # common Harness/shared-foundation protocol.
    formalization_progress.enrich_site(output)

    proof_readers.enrich_site(output)
    declaration_lessons.enrich_site(output)
    # Publication bindings can target companion-paper readers too. Materialize
    # those source pages before attaching their checked theorem/proof lessons;
    # running the companion generator later would overwrite the attachments.
    samplewiki_companions.enrich_site(output)
    publication_reader.enrich_site(output)
    metadata_lessons.enrich_site(output)
    inline_lean.enrich_textbook(output)

    inherit_final_reader_contract(output)
    repair_project_author_footer(output)
    repair_final_content_anchors(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
