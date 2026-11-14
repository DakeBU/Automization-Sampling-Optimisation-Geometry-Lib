# Blind mathematical reconstruction

For every pair of natural numbers d and q (implicit parameters in Lean), and for every hypothesis hq : 2q + 1 < d, make the following local choices and definitions.

Put I = Fin(q + 1) = {0, ..., q} and J = Fin(d) = {0, ..., d - 1}; an index's numerical value is its zero-based natural-number value. Let M be the real matrix space with both rows and columns indexed by I × I. Fix, as the local measurable-space instance on M, the Borel sigma algebra of its ordinary finite-coordinate topology. The matrix norm convention is the L2 operator norm for the action on real Euclidean spaces; this induces the same topology.

Let D = EuclideanSpace ℝ (Fin d), the real d-dimensional Euclidean space, and let E = EuclideanSpace ℝ (Fin(q + 1)), the real (q + 1)-dimensional Euclidean space. Use their Euclidean norms and Borel sigma algebras. Let Ω = I → D, with its finite product measurable structure, and define the measure

    μ = Measure.pi (b ↦ stdGaussian D),  b ∈ I.

Thus each factor in this displayed product measure is the centered Gaussian probability measure on D with identity covariance. Define the real scalars

    r = (q + 1 : ℕ), coerced to ℝ,
    L = 2r + 3 log(1000 · (d : ℝ)),

where log is the natural logarithm. For every i ∈ J define

    θ(i) = ((i.val : ℝ) + 1 - 1/2) · π / (d : ℝ).

For every i ∈ J and k ∈ I define the real-valued function t by

    t(i)(k) = 1                                      if k.val = 0,
              sqrt(2) · cos((k.val : ℝ) · θ(i))       otherwise,

where sqrt is the nonnegative square root. For every i ∈ J and ω ∈ Ω define the Euclidean vector

    row(i, ω) = WithLp.toLp 2 (b ↦ ω(b)(i)) ∈ E.

In particular, its coordinate b is ω(b)(i); WithLp.ofLp(row(i, ω)) is that same coordinate function on I, and its norm is the Euclidean norm on E. Define Y : J → Ω → M by

    Y(i, ω) = (d : ℝ)⁻¹ ·
              [vecMulVec(WithLp.ofLp(row(i, ω)), WithLp.ofLp(row(i, ω)))
               ⊗ vecMulVec(t(i), t(i))]              if ‖row(i, ω)‖² ≤ L,
              0                                     otherwise.

Here 0 is the zero matrix, multiplication by (d : ℝ)⁻¹ is scalar multiplication, vecMulVec(u, v) is the matrix with entry u(a)v(c) at row a and column c, and ⊗ is the Kronecker product. Precisely, for b, c, b′, c′ ∈ I, the entry of Y(i, ω) at row (b, c) and column (b′, c′), when the cutoff holds, is

    (d : ℝ)⁻¹ · ω(b)(i) · ω(b′)(i) · t(i)(c) · t(i)(c′).

When the cutoff fails, all its entries are zero. The cutoff includes equality.

For every i ∈ J define the deterministic matrix

    mean(i) = ∫_Ω Y(i, ω) dμ(ω),

and then define Z : J → Ω → M by

    Z(i, ω) = Y(i, ω) - mean(i).

These integrals are Bochner integrals, with the Lean convention that the integral is zero when the integrand is not integrable. The definition of mean uses this totalized integral.

With exactly these local definitions, the following five claims hold together:

1. For every i ∈ J, the function ω ↦ Z(i, ω) is measurable from Ω with its displayed product measurable structure into M with the locally fixed Borel sigma algebra.
2. The entire indexed family (ω ↦ Z(i, ω)) indexed by i ∈ J is jointly independent under μ, in the sense of iIndepFun Z μ.
3. For every i ∈ J, the function ω ↦ Z(i, ω) is Bochner integrable with respect to μ: it is almost everywhere strongly measurable and the integral of its matrix norm is finite.
4. For every i ∈ J, its Bochner integral is the zero matrix:

       ∫_Ω Z(i, ω) dμ(ω) = 0.

5. For every i ∈ J and every ω ∈ Ω, the real matrix Z(i, ω) is Hermitian. Equivalently, it equals its transpose; in entries, Z(i, ω)[(b, c), (b′, c′)] = Z(i, ω)[(b′, c′), (b, c)] for every b, c, b′, c′ ∈ I.

All the definitions and the five conclusions lie inside the scope of the initial quantifiers on d, q, and hq. The parameter range allows q = 0. The hypothesis forces d ≥ 2q + 2, hence d ≥ 2, so J and I are nonempty and the displayed real denominator d is nonzero. The final symmetry claim is pointwise for every sample ω, while the asserted integrability has its usual almost-everywhere strong-measurability component.

## Artifact record

- Decoder: neutral_decode_328a
- Input artifact: /Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261113/anon_328a/input.json
- Input artifact byte SHA-256: 3097f8763d47af768f0e308efaedc5ed9856772baaf001443845dbc19fcd2f8f
- Packet SHA-256 field: d98e85cb41fbb7a57d8ecba30563a1998492da80167a052762c9c04a84396fda
- Reconstructed theorem text SHA-256 (UTF-8): a18526c5af93340cdd4fe026fc94871c3097fc923622cff08929bcba95da7686
- Source text visible: false

## Ambiguity

No unresolved ambiguity remains after applying the approved definition context. Matrix pair-index ordering, the Borel measurable-space instance, the L2 operator norm convention, joint independence, the totalized Bochner integral, and real Hermitian symmetry are interpreted explicitly above.
