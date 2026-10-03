from __future__ import annotations

import unittest
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
GRAPH_JS = ROOT / "website" / "static" / "underlying-lean-graph.js"
GRAPH_CSS = ROOT / "website" / "static" / "underlying-lean-graph.css"
SEMANTIC_CSS = ROOT / "website" / "static" / "semantic-roundtrip-graph.css"
GRAPH_BUILDER = ROOT / "website" / "scripts" / "underlying_lean_graph.py"
GRAPH_MODEL = ROOT / "website" / "scripts" / "underlying_lean_graph_model.py"
SEMANTIC_GRAPH = ROOT / "website" / "scripts" / "underlying_lean_graph_semantic.py"


class UnderlyingLeanGraphInteractionTests(unittest.TestCase):
    def test_focus_preserves_context_and_marks_direct_relations(self) -> None:
        js = GRAPH_JS.read_text(encoding="utf-8")
        self.assertIn("Focus is a visual overlay, not a graph filter", js)
        self.assertIn('classes.push(related ? "related" : "muted")', js)
        self.assertIn('focusNeighbors.has(n.id)', js)
        self.assertIn('direct relations highlighted', js)
        self.assertIn('Escape', js)

    def test_formal_and_curated_edges_have_distinct_evidence_styles(self) -> None:
        js = GRAPH_JS.read_text(encoding="utf-8")
        css = GRAPH_CSS.read_text(encoding="utf-8")
        builder = GRAPH_BUILDER.read_text(encoding="utf-8")

        formal = re.search(r'const FORMAL_RELATIONS = new Set\(\[(.*?)\]\)', js).group(1)
        self.assertEqual(set(re.findall(r'"([^"]+)"', formal)), {"imports", "declares"})
        self.assertIn("FORMAL_RELATIONS", js)
        self.assertIn('`${relationEvidence(e.relation)}-edge`', js)
        self.assertIn('data-evidence', js)

        self.assertIn(".ulg-edge.formal-edge", css)
        self.assertIn(".ulg-edge.overlay-edge", css)
        self.assertIn("stroke-dasharray:none", css)
        self.assertIn("stroke-dasharray:7 5", css)
        self.assertIn(".ulg-edge.related", css)
        self.assertIn(".ulg-edge.muted", css)
        self.assertIn(".ulg-node.related", css)
        self.assertIn(".ulg-node.muted", css)

        self.assertIn("Solid edges", builder)
        self.assertIn("dashed edges", builder)
        self.assertIn("ulg-line-key formal", builder)
        self.assertIn("ulg-line-key overlay", builder)

    def test_semantic_fidelity_and_denoising_are_graph_native(self) -> None:
        js = GRAPH_JS.read_text(encoding="utf-8")
        semantic_css = SEMANTIC_CSS.read_text(encoding="utf-8")
        builder = GRAPH_BUILDER.read_text(encoding="utf-8")
        model = GRAPH_MODEL.read_text(encoding="utf-8")
        semantic = SEMANTIC_GRAPH.read_text(encoding="utf-8")

        self.assertIn('semantic: new Set(["library", "semantic-stage", "semantic-audit", "repair-proposal"])', js)
        self.assertIn("Blind reconstructed theorem", js)
        self.assertIn("Seven-slot semantic diff", js)
        self.assertIn("Lean theorem denoising proposals", js)
        self.assertIn("Never mutates the source theorem automatically", js)

        for status in ("fidelity-exact", "review-required", "fidelity-mismatch", "fidelity-repaired", "proposal"):
            self.assertIn(status, semantic_css)
        self.assertIn(".ulg-semantic-table", semantic_css)
        self.assertIn(".ulg-repairs", semantic_css)

        self.assertIn("SEMANTIC_REGISTRY", model)
        self.assertIn("semantic round-trip registry", model)
        self.assertIn("add_semantic", builder)
        self.assertIn('data-view="semantic"', builder)
        self.assertIn("Theorem Fidelity Checker", builder)
        self.assertIn("Lean Theorem Denoiser", builder)

        self.assertIn('"blind-reconstruction"', semantic)
        self.assertIn('"fidelity-checker"', semantic)
        self.assertIn('"theorem-denoiser"', semantic)
        self.assertIn('"source-review"', semantic)
        self.assertIn("source hidden from decoder", semantic)
        self.assertIn("proposal remains separate", semantic)

    def test_publication_declarations_exist_before_semantic_edges_are_added(self) -> None:
        builder = GRAPH_BUILDER.read_text(encoding="utf-8")
        self.assertLess(builder.index("publication_reader.project_graph(builder)"),
                        builder.index("semantic = add_semantic(builder, semantic_registry)"))


if __name__ == "__main__":
    unittest.main()
