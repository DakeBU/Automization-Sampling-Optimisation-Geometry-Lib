# Exercise 1.7: publication handoff for two conclusions

The [publication candidate](exercise-conclusions-publication-candidate-v1.json)
has separate source items and progressive reader lessons for two compiled
declarations. It is an isolated overlay, not a released page or Cell:

- **Compact Euclidean PI** is the same-constant implication on compact smooth
  tests with genuine `Admissible` outputs. Its source combines the linearization
  request in [Exercise 1.7](https://chewisinho.github.io/main.pdf#page=55) with
  the compact Euclidean test classes in [§2.1.1](https://chewisinho.github.io/main.pdf#page=60).
  It is not an extension to the full closed form domain or an abstract
  reversible-semigroup theorem.
- **Actual-law KL** covers the finite tilted probability and full-neighborhood
  remainder in [(1.E.1)](https://chewisinho.github.io/main.pdf#page=55).
  [Corollary 2.1.2](https://chewisinho.github.io/main.pdf#page=62) consumes it
  in the source; this packet provides no transport proof for that corollary.

The authored scalar proof uses Taylor's integral remainder. The Lean entropy
parent proves the same coefficient using genuine differentiation, a scalar
quadratic bound and dominated convergence. A similar proof idea is not a
claim that the tactic sequence or every intermediate envelope is identical.
Both candidate records passed the independent seven-slot source review as
`equivalent-after-elaboration`. The KL review records nonblocking differences
in source domain, parameter use and the expository calculus method.

## Reproduction and remaining gates

```bash
python proof-obligations/chewi-exercise-1-7/check_exercise_publication_packets.py
python proof-obligations/chewi-exercise-1-7/check_exercise_publication_packets.py --batch conclusions --replay-trusted-references
```

The first command rehydrates both reviewed overlays and checks their packet
pins, source/module/prose bindings and rendered lesson fragments without
changing the canonical indices. The optional Lean replay verifies 4.33.0 and
compiles the two exact trusted reference bodies under their direct imports.
It checks that the finished answer declaration is absent from those imports
and rejects transitive axioms outside the standard three. It does **not** run
untrusted submissions or establish a sealed agentic evaluation workspace.

Local reader QA used the actual lesson/page renderers, vendored MathJax and
blocked external networking. At widths 1280px and 390px both formulas and
each opened proof step rendered without errors or overflow; the precise Lean
statement/proof disclosures stayed folded by default and exposed code when
clicked. This is not a deployed website read-back.

The [PI draft](compact-pi-bench-draft-v1.md) and
[KL draft](actual-kl-bench-draft-v1.md) use one source family and keep prompts
separate from scoring criteria. These drafts and their local reviews do not
admit tasks, assign empirical difficulty, expose a reference in an evaluation
workspace, or supply model scores. Stabilization still needs the scoped Cells
and canonical publication/graph/Registry updates, CI, actual Bench admission
and renderer/browser checks on the integrated site. The two retained proof
branches share the compensated integral result; an edge from actual-law KL
to compact PI must not be fabricated.
