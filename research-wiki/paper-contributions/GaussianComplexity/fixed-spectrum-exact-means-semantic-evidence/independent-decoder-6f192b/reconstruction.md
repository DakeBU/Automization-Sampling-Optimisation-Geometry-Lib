# Packet-only mathematical reconstruction

For every natural number d with d ≥ 2, every real number κ with κ ≥ 2, and every natural number n with 1 ≤ n < d, define, for each coordinate index i ∈ {0, …, d − 1},

θᵢ = (i + 1/2)π/d,
λᵢ = (κ + 1)/2 + ((κ − 1)/2) cos θᵢ.

Let Λ = diag(λ₀, …, λ_{d−1}). On the real Euclidean space Rᵈ, let μ be the centered multivariate Gaussian measure with covariance matrix Λ⁻¹. More explicitly, μ is the image of the standard Gaussian measure under the linear map whose matrix is the positive semidefinite square root of Λ⁻¹. Define the real-valued function

Q(x) = ∑_{i=0}^{d−1} cos(nθᵢ) xᵢ²

and the real number

r = (√κ − 1)/(√κ + 1).

Then x ↦ ‖x‖² and Q are both Bochner integrable with respect to μ, and their real Bochner integrals satisfy the two exact identities

∫_{Rᵈ} ‖x‖² dμ(x) = (d/√κ) (1 − r^{2d})/(1 + r^{2d}),

(−1)ⁿ ∫_{Rᵈ} Q(x) dμ(x) = (d/√κ) (rⁿ − r^{2d−n})/(1 + r^{2d}).

Here ‖·‖ is the standard Euclidean norm, all coordinate sums include every index from 0 through d − 1, and all displayed angles and scalar expressions are real. Powers have natural-number exponents. The expression 2d − n uses natural subtraction, which is ordinary nonnegative subtraction under 1 ≤ n < d. Matrix and real inverses and the real square root retain the totalized meanings in the supplied context. In this parameter range every λᵢ is positive, so Λ⁻¹ is the usual inverse and the Gaussian parameter is its ordinary positive definite covariance. The Gaussian construction agrees with the supplied totalized definition, whose matrix square root is zero outside the positive semidefinite domain; the assumptions here stay within that domain.

The assertions hold separately for every admissible triple (d, κ, n). Both integrability conclusions and both equalities concern this same μ, and Q depends on n as defined above. There is no limiting, asymptotic, approximate, almost-everywhere, or optimization assertion and no unspecified constant. All numerical factors are displayed explicitly; μ depends on d and κ, the formula for Q depends only on d and n, while its integration measure also depends on κ, and r depends only on κ.

# Exposure and limits

This reconstruction uses only the supplied neutral input packet, including its Lean statement and approved definition context. It does not assert agreement with an unseen original source or verification of the packet's compiled flag. No original theorem prose, source identity, source anchor, source-facing declaration identity, audit, lesson, ledger, frontier, proof, or other actor's artifacts were inspected.

Nonmathematical ambient cues were visible: the task path contains ASTIS-GC, .astis, semantic-neutral-20261110, and the neutral directory token 6f192b; the packet contains an ASTIS-BLIND identifier and a statement hash. The session also supplied a home-directory path, date, timezone, tool and workflow descriptions, and a parent instruction referring to a source-blind semantic-roundtrip protocol. These may suggest a mathematical formalization workflow. The packet itself exposes Lean notation, standard Gaussian terminology, and the approved ProbabilityTheory context; these are the authorized mathematical inputs. I did not inspect repository instructions or derive source identities from any cue.
