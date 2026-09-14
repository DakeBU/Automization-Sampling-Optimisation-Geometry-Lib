"""Shared data model and naming rules for the Samplinglib proof graph."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = ROOT / "_site"
CASES = ROOT / "research-wiki/source-index/SampleWiki_cases.json"
AUDITS = ROOT / "website/content/samplewiki_frontier_audit.json"
SEMANTIC_REGISTRY = ROOT / "research-wiki/semantic-roundtrip/registry.json"
CSS = ROOT / "website/static/underlying-lean-graph.css"
SEMANTIC_CSS = ROOT / "website/static/semantic-roundtrip-graph.css"
JS = ROOT / "website/static/underlying-lean-graph.js"
PAGE = "lean-foundations.html"
DATA = "data/underlying-lean-graph.json"
LABEL = "Underlying Lean Graph of Libraries"

ROOTS = [
    ("stochastic", "Stochastic calculus & SDEs", [1, 3, 4, 5, 6, 7, 12], "ito stochastic sde brownian stopping martingale diffusion"),
    ("semigroup", "Semigroups, Γ-calculus & functional inequalities", [1, 2, 4, 5, 6, 8, 11, 12], "semigroup generator carre carré poincare poincaré lsi log-sobolev contraction"),
    ("transport", "Optimal transport & Wasserstein geometry", [1, 2, 4, 8, 11, 12], "wasserstein w2 transport coupling geodesic displacement gradient flow"),
    ("information", "KL, Fisher & information geometry", [1, 2, 3, 4, 6, 8, 11, 12], "fisher relative entropy entropy kl score information dissipation"),
    ("proximal", "Proximal kernels & restricted Gaussian oracles", [7, 8, 10, 11], "proximal rgo restricted gaussian conditional kernel gaussian tilt in-and-out"),
    ("renyi", "Rényi divergence & composition", [3, 6, 7, 8, 12], "renyi rényi data processing interpolation warm start composition"),
    ("path", "Path laws, Girsanov & exact diffusion simulation", [3, 4, 5, 6, 7, 12], "girsanov path fors simulation log-density phase-space uld"),
    ("discretization", "Discretization & algorithmic convergence", [4, 5, 6, 7, 8, 10, 11, 12], "lmc ulmc mala midpoint discret averaged algorithm step size"),
    ("oracle", "Oracle models & complexity", [7, 8, 9, 10, 11], "oracle query finite-sum finite sum stochastic gradient lower bound complexity membership"),
    ("mirror", "Mirror, Bregman & weak-smooth geometry", [10, 11], "mirror bregman holder hölder weak smooth nonsmooth"),
    ("convex-body", "Convex bodies & membership queries", [9, 10], "convex body membership annealing constrained kook"),
    ("generative", "Diffusion generative models", [12], "generative score-based reverse diffusion diffusion model probability flow"),
]
ROOT_MAP = {key: (label, chapters, words.split()) for key, label, chapters, words in ROOTS}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def slug(value: object) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", str(value)).strip("-").lower() or "node"


def short(value: object, limit: int = 520) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def case_url(case_id: str) -> str:
    return f"example-cases/samplewiki/cases/{slug(case_id.removeprefix('ASTIS-SW-'))}.html"


def section_url(chapter: int, section: str) -> str:
    return f"textbook/chapter-{chapter:02d}/section-{section.replace('.', '-')}.html"


def roots_for(*values: object) -> list[str]:
    text = " ".join(str(value or "") for value in values).lower()
    scored = [(sum(word in text for word in words), key) for key, (_, _, words) in ROOT_MAP.items()]
    return [key for score, key in sorted(scored, key=lambda item: (-item[0], item[1])) if score][:4]


def chewi_chapters(*values: object) -> list[int]:
    text = " ".join(str(value or "") for value in values)
    found = re.findall(r"(?:Theorem|Corollary|Lemma|§|Chapter)\s*(1[0-2]|[1-9])(?:\.|\b)", text, flags=re.I)
    return sorted({int(value) for value in found})


def status(value: object, *, case: bool = False) -> str:
    text = str(value or "").lower()
    if "literature-open" in text or "lower unknown" in text:
        return "literature-open"
    if case and "audit" in text:
        return "audited"
    if any(word in text for word in ("compiled", "formalizedlocal", "closed")):
        return "compiled"
    if any(word in text for word in ("active", "partial", "progress")):
        return "partial"
    if any(word in text for word in ("audited", "primary theorem")):
        return "audited"
    return "planned"


class GraphBuilder:
    """Deduplicating node/edge builder with graph-search metadata."""

    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: dict[tuple[str, str, str], dict[str, str]] = {}

    def add(self, node_id: str, kind: str, label: object, **extra: Any) -> str:
        node = {"id": node_id, "kind": kind, "label": short(label, 180), **extra}
        tags: list[object] = [
            node_id,
            kind,
            node.get("label", ""),
            node.get("subtitle", ""),
            node.get("summary", ""),
            node.get("fidelity_verdict", ""),
            node.get("blindness", ""),
            node.get("original_theorem", ""),
            node.get("reconstructed_theorem", ""),
            node.get("repaired_theorem", ""),
        ]
        tags.extend(row.get("value", "") for row in node.get("details", []) if isinstance(row, dict))
        for row in node.get("semantic_slots", []):
            if isinstance(row, dict):
                tags.extend(row.get(key, "") for key in ("slot", "original", "reconstructed", "relation", "evidence"))
        for row in node.get("semantic_deltas", []):
            if isinstance(row, dict):
                tags.extend(row.get(key, "") for key in ("slot", "severity", "description", "evidence"))
        for row in node.get("repair_proposals", []):
            if isinstance(row, dict):
                tags.extend(row.get(key, "") for key in ("id", "class", "status", "necessity", "proposed_change", "justification"))
        node["search"] = short(" ".join(map(str, tags)), 12000).lower()
        self.nodes[node_id] = node
        return node_id

    def edge(self, source: str, target: str, relation: str) -> None:
        if source in self.nodes and target in self.nodes and source != target:
            self.edges[(source, target, relation)] = {"source": source, "target": target, "relation": relation}

    def export(self) -> dict[str, Any]:
        return {
            "schema_version": 2,
            "generated_from": "site-data.json + pinned SampleWiki manifests + semantic round-trip registry",
            "nodes": list(self.nodes.values()),
            "edges": list(self.edges.values()),
        }
