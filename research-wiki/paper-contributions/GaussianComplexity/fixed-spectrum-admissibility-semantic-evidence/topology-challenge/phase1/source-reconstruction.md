# Independent raw-source reconstruction — phase 1

Role: distinct BINDER / MEANING / TOPOLOGY CHALLENGER, `/root/fs_admiss_topology_challenge`.
This is source-first reconstruction evidence, not a proof, source-V approval,
Statement Seal approval, source-graph approval, or theorem-completion claim.

The only mathematical input is the pinned raw HTML for *On Complexity of Gaussian
Sampling*, arXiv:2610.20492v1, by Huanjian Zhou and Taiji Suzuki:
`.astis/huanjian-resume-20261103/2610.20492v1.html`, SHA-256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
The construction is Eq. (11), HTML `S4.E11`; the named result is Lemma 4.6,
`S4.Thmtheorem6`; the complete source proof is `A3.SS4` (Appendix C.4).
I have not inspected a candidate statement/seal, target Lean/API/proof, root
audit, graph author's output, previous source verdict, publication artifact,
site, browser, remote service, old frontier, or ATLAS content/index/derivative.

## Seven semantic slots

### 1. Objects

The integer dimension is `d`. The real parameter is `κ`. For source indices
`i = 1, …, d`,

`θᵢ = ((i − 1/2) π) / d`,

`λᵢ = (κ + 1)/2 + ((κ − 1)/2) cos θᵢ`,

`Λ = diag(λ₁, …, λ_d)`.

The rotation `O` is a real orthogonal matrix, and the precision matrix is
`A = O Λ Oᵀ`. The potential, called `f_A` in Sections 2 and 4.1 and `V_A` in
Appendix C.4, is the literal quadratic `x ↦ xᵀ A x / 2`. These names denote
the same function. The associated target is the actual centered Gaussian law
`π_A = N(0, A⁻¹)`, with precision `A` and covariance `A⁻¹`.
The normalizer `Z_A` belongs to the density proportional to `exp(−V_A)` on
Euclidean space; the appendix computes it by Gaussian integration.

Evidence: `S4.SS1.p1.1`, `S4.E11`, `S4.SS1.p1.2`, the targets/oracle paragraph
of `S2`, `A3.SS4.p2.1`, `A3.SS4.p3.1`, `A3.Ex160`.

### 2. Domains

`d` is an integer with `d ≥ 2`; `κ` is real with `κ ≥ 2` in the local hard
family. Matrices are real `d × d`, vectors belong to `ℝ^d`, and `O` belongs to
`O(d) = {O ∈ ℝ^(d×d) : Oᵀ O = I_d}`. The source uses its standard real
Euclidean norm. For symmetric matrices, `B ≼ C` means `C − B` is positive
semidefinite. The ambient precision class is

`𝒜_(d,κ) = {A ∈ ℝ^(d×d) : A = Aᵀ, I_d ≼ A ≼ κ I_d}`.

The broader class definition in Section 2 permits `d ≥ 1, κ ≥ 1`; that does
not erase the explicitly narrower local construction domain. A zero-based
finite-index implementation must use source index `i = j+1`, hence angle
`((j + 1/2)π)/d`. Substituting `j−1/2` is not the displayed construction.

Evidence: opening of `S2`, its targets/oracle paragraph, `S4.SS1.p1.1`, `S4.E11`.

### 3. Quantifiers

Unpacking the standing construction, the lemma says: for each integer `d ≥ 2`
and each real `κ ≥ 2`, define the displayed grid and diagonal matrix; then for
every `O ∈ O(d)`, the constructed `A` satisfies the stated matrix inequalities.
The grid bounds hold for every source index. Potential consequences hold for
every `x ∈ ℝ^d`; positive potential and strict uniqueness concern `x ≠ 0`.

The universal rotation quantifier includes rotations and reflections. No
probability qualifier appears in the lemma. Section 4.1 draws `O` from Haar
measure independently of algorithm randomness for the later hard distribution,
but Lemma 4.6 holds pointwise for every `O`. It is neither almost-sure
admissibility nor existence of one admissible rotation.

There is no `δ`, query budget `q` or `T`, frequency `n`, accuracy `ε`, dimension
threshold, concentration event, or additional random vector in this lemma.
Those belong to other Section 4 results, not its input quantifiers.

Evidence: `S4.SS1.p1.1–p1.2`, `S4.Thmtheorem6.p1.1`, `A3.SS4`.

### 4. Assumptions

The source conditions are exactly the local domain conditions `d ≥ 2`,
`κ ≥ 2`, and orthogonality of `O`, together with the literal definitions.
Finite real carriers, the Euclidean inner product, and transpose/matrix
operations are typing/convention information. The definitions of the grid,
potential and target fix meaning; they do not supply arbitrary witnesses.

In a binder audit, the dimension and parameter bounds may be classified as
contextual SOURCE or audited STANDING, and `OᵀO = I` as SOURCE (or as the
corresponding orthogonal-group carrier). Real finite-dimensional carriers are
TYPING. There is no source ruling known to this reviewer. The following are
derived obligations, never legal extra public premises: angle/cosine bounds,
positive eigenvalues, symmetry or positive definiteness of `A`, the Loewner
bounds, invertibility, determinant positivity, finite positive Gaussian
normalization, smoothness/Hessian identities, strong convexity/smoothness,
existence/uniqueness of a minimizer, identification of the Gaussian law, or
rotation invariance of `Z_A`.

There is no source assumption of determinant `+1`, a known inverse/covariance
certificate, simple spectrum, Haar genericity, an algorithm, Borel regularity
of an input algorithm, an already normalized probability law, or separately
supplied Gaussian integral estimates.

### 5. Conclusion

The exact named Lemma 4.6 conclusion is

`I_d ≼ O Λ Oᵀ ≼ κ I_d`.

The surrounding paragraph describes this as membership in the prescribed
class. That membership additionally needs symmetry, supplied by the real
orthogonal conjugation of the real diagonal matrix; it is not an input
assumption. The lemma is about the precision matrix, not a covariance sandwich
with the same orientation.

Appendix C.4 substantively derives more facts: `V_A` is `C^∞` and has Hessian
`A`, is 1-strongly convex and κ-smooth; `V_A(0)=0` and
`V_A(x) ≥ ‖x‖²/2 > 0` for `x ≠ 0`, so zero is its unique minimizer; its target
is `N(0,A⁻¹)`; and

`Z_A = (2π)^(d/2) (det A)^(−1/2)`

`    = (2π)^(d/2) (det Λ)^(−1/2)`.

Because `Λ` is fixed, this normalizer does not depend on `O` and is known when
the spectrum is public. These appendix consequences must stay represented in
an exhaustive source-proof inventory even if the exact named lemma interface
only asserts the sandwich. Proving the sandwich alone is not automatically a
formalization of every appendix consequence.

### 6. Scopes and senses

The spectrum is deterministic conditional on `d,κ`, independent of the choice
of eigenbasis. Admissibility is deterministic. The normalizer may depend on
`d,κ` through the eigenvalues, but not on `O`. Its being known is conditional
on the public-spectrum convention, not a universal computational oracle claim.

`κ` is an upper spectral ratio bound for the class. The finite cosine grid has
strictly interior eigenvalues, so the source does not assert that its least
eigenvalue is exactly 1, its greatest exactly κ, or its actual condition number
exactly κ. No probability of success or numerical approximation error is
involved.

`A⁻¹` is the genuine inverse of the positive-definite precision; no singular
matrix fallback is part of source semantics. `N(0,A⁻¹)` is a Gaussian
probability distribution on all of `ℝ^d`, not merely a tagged covariance object
or an unspecified probability measure. A normalized Gibbs construction would
need an internally discharged equality to this actual law. The normalized
density relative to Euclidean Lebesgue measure is
`Z_A⁻¹ exp(−xᵀAx/2)`, as the standard meaning of the source's potential,
target, and Gaussian integration computation; that density formula is a
semantic expansion, not an additional displayed theorem in C.4.

### 7. Constants and dependencies

All constants in Eq. (11) and C.4 are literal: `1/2`, `π`, `1`, `κ`, and
`(2π)^(d/2)`. There are no hidden big-O constants and no parameter dependence
on an algorithm, accuracy, query budget, or δ. The lower curvature constant is
1 and the upper smoothness constant is κ. The inverse covariance therefore
has reciprocal spectral bounds, if those are used as internal bridges.
The determinant is positive, so inverse-square-root notation means the
positive real reciprocal square root. Dimension half-power is real/analytic
notation; it does not mean integer truncation of `d/2` when `d` is odd.

## Definitions and semantic obligations

| Object | Source meaning / required treatment |
| --- | --- |
| `θ`, `λ`, `Λ`, `A`, `f_A = V_A` | Literal formulas on their public carriers. No altered grid, endpoint clipping, or fallback. |
| `O(d)` | Real orthogonal group, defined in S2 by `OᵀO=I`; both determinant components allowed. |
| `≼`, `𝒜_(d,κ)` | S2 positive-semidefinite matrix order and symmetric precision class; membership cannot mean only a scalar eigenvalue tag. |
| `A⁻¹`, `Λ⁻¹` | Genuine inverse on internally established positive-definite matrices. Totalized library inverse semantics require their validity to be proved inside the construction. |
| `π_A` | Actual centered Gaussian probability law with covariance `A⁻¹`. If characterized through density, well-definedness and the Gaussian characterization require real proofs, not a conditional choice with a default law. |
| `Z_A` | The actual finite positive Euclidean integral of `exp(−V_A)`; the determinant expression must be proved equal to it. Merely defining a scalar by the determinant expression does not prove Gaussian integration. |

No representative/quotient choice is present in the source construction.
All analytic regularity needed to interpret the integral or Gaussian law must
be derived from the finite-dimensional quadratic and its positive spectrum.
This phase has not inspected any project definition body and therefore gives
no verdict about a candidate's literal/characterized implementation.

## Critical internal estimates and failure boundaries

1. For `1 ≤ i ≤ d`, positivity of `d` and the half-integer index yield
   `0 < θᵢ < π`. The endpoint inequalities are strict.
2. On that open interval, `−1 < cos θᵢ < 1`.
3. Since `(κ−1)/2 > 0`, the affine expression gives
   `1 < λᵢ < κ`. Positivity of this scale must be discharged from κ≥2.
4. Real diagonal symmetry and the diagonal quadratic bounds, transported by
   orthogonality, give symmetry of `A` and `‖x‖² ≤ xᵀAx ≤ κ‖x‖²` for all x.
   Orthogonality must be used in the correct direction to obtain the norm
   identity for `Oᵀx`; a one-sided identity may require a finite-dimensional
   invertibility bridge. This is the source sandwich.
5. The lower bound gives positive definiteness, invertibility, and positive
   determinant. These make covariance and inverse square root meaningful.
6. Differentiating the actual symmetric quadratic gives smoothness and Hessian
   `A`, hence the curvature bounds. The lower quadratic bound gives the unique
   zero minimizer. Smoothness and minimization are not independent premises.
7. Gaussian integration of the actual potential gives the determinant
   normalizer and identifies the Gaussian covariance. Orthogonal conjugation
   preserves determinant: factors `det O` and `det Oᵀ` cancel for either sign.
   Consequently `det A = det Λ = ∏ λᵢ > 0`; the final expression depends only
   on the fixed spectrum. These are mathematical edges even though C.4
   compresses them into short sentences.

Failure boundaries: d=0 makes the angle denominator unusable; replacing the
half-grid by an endpoint or wrong zero-based formula changes the construction;
κ=1 removes the strict affine coefficient (although the non-strict
admissibility statement has a natural separate extension); κ<1 can reverse
bounds. None licenses changing the present local statement. Arbitrary
nonorthogonal conjugation does not preserve the sandwich with constants 1,κ.
Assuming determinant +1 loses source cases. Replacing `A⁻¹` by `A` changes the
target. Declaring determinant/normalizer positivity as hypotheses hides
obligations. `det A = det Λ` alone does not establish that a scalar expression
is the Gaussian integral. Adding lower-bound theorem restrictions
`κ≤d^(1−δ)` or sufficiently large d would narrow this lemma without source
justification.

## Source-only topology baseline for later challenge

This is my independent expected dependency shape, frozen before receiving
any proposed Source Proof Graph. It does not approve another extractor's graph.

The single source route is: local domain and Eq. (11) → angle bounds → cosine
bounds → eigenvalue bounds → diagonal quadratic bounds → orthogonal transport
→ spectral sandwich. Real diagonal symmetry plus conjugation supplies the
symmetry needed for class membership. An orthogonal norm/inverse bridge is an
implicit finite-dimensional background dependency, not a new public premise.

From that common result, the appendix branches into (a) differentiating the
quadratic and applying the sandwich to its Hessian, (b) the lower quadratic
bound and the unique minimizer, and (c) positive definiteness/inverse,
Gaussian-law identification and Gaussian integration. Determinant invariance
plus the Gaussian integral formula then yields rotation-independent
normalization. These are consequence branches, not additional assumptions
needed to make the named sandwich hold.

Required in-scope dispositions for later review are the domain paragraph and
display `S4.E11`; the construction/target paragraph `S4.SS1.p1.2`; the fixed
spectrum/public normalizer paragraph `S4.SS1.p2.1`; the class definition and
order/orthogonal conventions in S2; `S4.Thmtheorem6`; all four proof paragraphs
`A3.SS4.p1.1`, `.p2.1`, `.p3.1`, `.p3.2`; and the display `A3.Ex160`.
The named lemma is used in the opening proof of Theorem 4.1 (`S4.SS3`) to
discharge admissibility of the hard family. That is a consumer edge pointing
out of Lemma 4.6, not a reverse dependency from the lower-bound theorem.

The first-order oracle formula and equivalence in S2 give surrounding oracle
meaning. The C.4 proof does not itself contain a separate oracle-equivalence
argument despite the heading of `S4.SS2.SSS0.Px4`; a graph must not silently
award one. The [22, Section 9.2] reference is stated construction provenance;
C.4's direct argument does not require treating all of [22] as a mathematical
prerequisite. The other Section 4 concentration/Krylov/moment/lower-bound
lemmas are out of scope as proofs of admissibility. Their use of the same
family is not an AND-edge into this result. There is no alternative proof route
in the C.4 source; equivalent scalar/matrix elaborations do not create an
additional independent source route.

The words “Gaussian integration” omit a standard analytic argument and the
target identification omits its standard positive-definite Gaussian bridge.
Those remain explicit unproved source-background obligations for any later
formalization. This reconstruction neither claims they fail nor marks them
discharged.
