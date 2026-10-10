# Hidden Regularity Contracts

This file turns paper prose such as "standard", "smooth", or "by dominated
convergence" into reusable theorem-contract categories.  These are not
annoying bookkeeping details; they are the assumptions that decide whether a
Lean statement is true.

| Contract | Why it matters | Typical ASTIS location |
|---|---|---|
| Measurability | Needed before integrals, kernels, conditional expectations, and laws are well-typed. | `AutoSamplingTheory/TechnicalLemmas/Measure.lean` |
| Integrability | Needed before Bochner integrals, KL/FI terms, and limits under integrals are legal. | `Measure.lean`, `Variational.lean` |
| Domination | Needed for dominated convergence and parametric integral differentiation. | `Measure.lean` |
| Smoothness | Needed for Ito/Taylor generator and Hessian remainder statements. | `Analysis/Calculus/Taylor.lean`, SDE leaf files |
| Bounded Hessian | Needed for one-step Taylor remainders and EM weak-error bounds. | `Analysis/Calculus/Taylor.lean` |
| Compact support or decay | Needed to erase boundary terms in integration by parts. | future `IBP.lean` |
| Probability/finite measure | Needed for law-map, conditional law, and entropy statements. | `Measure.lean` |
| Conditional representative | Needed because conditional laws are only defined up to a.e. equality. | `Measure.lean`, `SDE.lean` |
| Positivity/nonzero density | Needed for log, KL, score, and Fisher-information algebra. | `Variational.lean` |
| Time regularity | Needed for differentiating time-indexed laws and weak-test integrals. | future `WeakFP.lean` |

Reviewer rule: if a lower proof succeeds only by assuming one of these
contracts informally, the result is not complete.  Either add the contract to
the statement, prove it from existing hypotheses, or record a source-cited
proof obligation.
