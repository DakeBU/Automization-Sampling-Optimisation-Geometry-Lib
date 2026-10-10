# ATLAS v1 external declaration memory

- Website: https://rammalahmad.github.io/atlas/
- Repository: https://github.com/facebookresearch/atlas-lean
- Paper: https://arxiv.org/abs/2605.29955
- Pinned commit: `e8b31c5cb0bec89b487ce33fe525a2c0b0f8b9c6`
- Default external checkout: `../outer_repos/atlas-lean/v1` (override with `ASTIS_ATLAS_ROOT`)
- Upstream toolchain: Lean 4.29.0 / Mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- ASTIS toolchain: Lean 4.33.0 / Mathlib v4.33.0
- License: CC BY-NC 4.0 for academic/research use; commercial use and ML model training, fine-tuning, distillation, evaluation, or development are prohibited; see pinned `v1/LICENSE`.

## Audited inventory

ASTIS deterministically indexes 26 books, 2,653 Lean files, and 36,469 named
source declarations: 17,098 theorems, 6,204 lemmas, and the remaining named
definitions and interfaces. It records 3,502 declarations with a direct
`sorry`, `admit`, or `axiom` marker. ATLAS reports 2,855 of 4,007 selected
textbook targets as passed; that evaluation is metadata, not ASTIS proof ownership.

The compact records live in `research-wiki/retrieval-index/atlas-v1/`. Search:

```bash
python3 tools/atlas_memory.py search markov --route samplewiki-route --clean-only
python3 tools/atlas_memory.py search riemannian --route riemannian-optimization
python3 tools/atlas_memory.py search convex --route optimisation
```

## Route relevance

- SampleWiki and sampling shared floor: 6,573 candidates in probability,
  conditional expectation, martingale, Markov, Brownian, concentration,
  information, semigroup, and PDE material.
- Riemannian Optimization: 1,674 candidates led by GeometryOfManifolds,
  DifferentialGeometry, and DifferentialAnalysis.
- Optimisation: 369 candidates led by CombinatorialOptimization and
  AnAlgorithmistsToolkit.

Every declaration remains searchable. Material outside these controlled book/topic
rules is intentionally unassigned rather than forced into an unrelated route.

## Call policy

Every record is `external-reference`, including records without a direct
placeholder. It becomes callable only after the minimal theorem is ported or
reproved as an ASTIS-owned declaration, tested under Lean 4.33.0, entered in
the Registry, source-mapped, and independently reviewed.
