# Statement seal: half-Rayleigh sphere Hessian and Boumal Exercise 5.18

Primary source: Nicolas Boumal, pre-publication PDF, §5.5, printed p. 96 /
PDF p. 112. The reviewed 367-page snapshot has SHA-256
`95e9c219298bcf718493885ba6f00cbcc95474e34fa8e4b0bf363e6e07f1b71b`.
Personal-use PDF: this record and the reader do not redistribute source text,
pages, or figures.

Before proof search the exact intermediate and terminal interfaces were type-checked
under Lean 4.33.0. The independent prospective reviewer `boumal_518_source_preflight`
accepted the actual gradient pairing, projected derivative with tangent subtype
output and finite-dimensional terminal statement. The adopted refinements were
smoothness at `ContDiff ℝ ∞` instead of analytic order, and explicit genuine
manifold differentiability of the half quadratic. No new assumption was added.
The production port preserved the mathematical statements and made the
single-module actual ambient derivative proof private.

The source operator is symmetric and the objective is exactly one half of the
quadratic form. The gradient must be the induced gradient of the restriction.
The Hessian acts on the tangent subtype and is built from the Fréchet derivative
of the checked extension, not assumed equal to a numerical form. PSD quantifies
over all tangent directions. Finite-dimensional real E matches the Euclidean
source; the unit point rules out dimension zero. Ambient dimension one, zero
tangent vectors, repeated eigenvalues, singular A and indefinite A are permitted.
The conclusion is global comparison on the sphere, nonzero eigenvector
attainment and comparison with every actual real eigenvalue.

This is a prospective scope record, not the independent semantic
round-trip, final proof audit, or Bench editorial decision.
