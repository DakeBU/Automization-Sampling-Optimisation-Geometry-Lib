# Agentic theorem proving references, 2025--2026

Source directory:
`../outer_papers/automation_systems/agentic_theorem_proving_2026/`.

## References

| Key | Source | ASTIS use |
| --- | --- | --- |
| `hierarchical-provers-2602.10512` | [arXiv:2602.10512](https://arxiv.org/abs/2602.10512), also cited under the "Don't Eliminate Cut" framing | Promote repeated analytic subarguments to reusable proof-DAG cuts: Gronwall, KL/FI identities, weak Fokker--Planck, conditional-law, measurability, integrability, and EM local-error lemmas. |
| `statistical-provability-2602.10538` | [arXiv:2602.10538](https://arxiv.org/abs/2602.10538) | Evaluate 6h runs by finite-budget proof success, verifier-call cost, average truncated proof length, high-mass proof-state coverage, and stale-wrapper churn. |
| `cpl-2509.14274` | [arXiv:2509.14274](https://arxiv.org/abs/2509.14274), [repo](https://github.com/auto-res/ConjecturingProvingLoop) | In exploratory mode, separate candidate theorem generation from proving and reuse verified local theorems as in-context examples. |
| `leanconjecturer-2506.22005` | [arXiv:2506.22005](https://arxiv.org/abs/2506.22005), [repo](https://github.com/auto-res/LeanConjecturer) | Generate domain-seeded candidate lemmas only after filtering by assumptions, syntax, non-triviality, and downstream proof utility. |
| `lean-rademacher-2503.19605` | [arXiv:2503.19605](https://arxiv.org/abs/2503.19605), [repo](https://github.com/auto-res/lean-rademacher) | Direct reference for concentration, Rademacher/symmetrization, separability/countable-density bridges, covering numbers, and large-analysis formalization staging. |

## Reviewer rules

- Do not ask lower agents to rederive a standard analytic cut in several
  theorems; make it a named technical lemma or a cited-result obligation.
- A source-cited analytic theorem may guide proof planning but does not close a
  Lean target until ported locally or imported as an audited dependency.
- Exploratory theorem generation is allowed for active exploratory research,
  not for mutating faithful SALD theorem statements.
