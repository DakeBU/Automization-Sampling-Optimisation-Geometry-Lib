# Gibbs L2 to ordinary local L2

Base: 238ab415, issue #309. One shared leaf; root is sole writer.

Continuous W and finite exp(-W) integral; normalized Gibbs measure. For any normed-additive target F and a in Gibbs L2, prove squared-norm local volume integrability and MemLp2 on every compact restriction. No scalar structure or completeness on F is needed; only the real squared norm is multiplied by weights.

1. Convert weighted MemLp2 to integrability of the squared norm.
2. Use integrable_tilted_iff to remove normalization and produce exp(-W)*norm(a)^2 integrability.
3. Multiply locally by continuous exp(W), then cancel positive exponentials pointwise.
4. Transfer representative strong measurability by volume << tilted volume.
5. Restrict to compact K and use local integrability plus the MemLp2 characterization.

Consumer test must obtain an actual resolvent witness from WeightedResolvent and apply the shared leaf to u, its gradient and f. No assumed weak equation or local L2 premise.

Publication: attributed elementary prerequisite to PBPS2609.06905v1 Appendix C.1. General weighted Sobolev background1310.2526v7 Section2.5 supplies context, not a transferred elliptic theorem. Continuous W is weaker than source C2. No H2, Sobolev-domain converse, D*D core, Poincare, measurable solution families or complete-paper result. Renderer will receive one formula proof with per-step collapsed Lean and explicit Mathlib parents. Encoder/independent source review and integration remain separate gates.
