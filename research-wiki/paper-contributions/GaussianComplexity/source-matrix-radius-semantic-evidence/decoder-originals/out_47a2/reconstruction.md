# Source-blind mathematical reconstruction

The sole mathematical input was the anonymous packet identified below. Only its proposition and approved definition context were used. The seven reconstruction slots are recorded explicitly. No source identity, original theorem, proof, review, repair proposal, or repository instructions were inspected.

## Reconstructed theorem

For every pair of natural numbers d and q satisfying 2q + 1 < d, make the following definitions. Put m = q + 1, I = {0, ..., d - 1}, J = {0, ..., q}, and K = J × J. Let D be real d-dimensional Euclidean space, E real m-dimensional Euclidean space, Ω = J → D, and μ = ⨂_{b∈J} N(0, Id_D), the finite product of the standard Gaussian probability laws on D. Put r = m as a real number and L = 2r + 3 log(1000d), where log is the natural logarithm and natural numbers in real formulas are cast to real numbers.

For i ∈ I and k ∈ J, define
  θ_i = (i + 1 - 1/2)π/d,
  t_i(k) = 1 if k = 0, and t_i(k) = √2 cos(kθ_i) otherwise.
For ω ∈ Ω, let x_i(ω) ∈ E have coordinates x_i(ω)_b = ω(b)_i for b ∈ J. Define a real K-by-K matrix Y_i(ω) by
  Y_i(ω) = d⁻¹ (x_i(ω)x_i(ω)^T) ⊗ (t_i t_i^T)  if ||x_i(ω)||₂² ≤ L,
  Y_i(ω) = 0  otherwise.
The first tensor factor is indexed by J and the second by J; thus, in the first branch, its entry at row (b,k) and column (c,ℓ) is d⁻¹ ω(b)_i ω(c)_i t_i(k)t_i(ℓ). The branch includes equality at L.

Let M_i = ∫_Ω Y_i(ω) dμ(ω), using the Bochner integral with the stipulated convention that this integral equals the zero matrix if Y_i is not integrable. Define Z_i(ω) = Y_i(ω) - M_i, w_i = cos((2q + 1)θ_i), and R_* = 2r(L + 1)/d.

Then both assertions hold:
  (1) For every i ∈ I and every ω ∈ Ω, ||Z_i(ω)||op ≤ R_*.
  (2) For every i ∈ I and every ω ∈ Ω, ||w_i Z_i(ω)||op ≤ R_*.
Here each matrix norm is the operator norm for its action on real Euclidean space indexed by K. No additional integrability premise or separate integrability conclusion is asserted in this proposition.

## Objects

d and q are natural-number parameters; hq is the proof/assumption of 2*q+1<d. D, E, Ω, μ, r, L, θ, t, row, Y, mean, Z, w, and Rstar are the successive local let-bound objects in the statement. For explanatory notation, m=q+1, I=Fin d, J=Fin(q+1), K=J×J, x_i=row i, M_i=mean i, and R_*=Rstar. μ is the finite product over b∈J of the centered identity-covariance Gaussian probability law on D. θ_i is the half-grid angle (i+1/2)π/d. The vector t_i has constant coordinate 1 at k=0 and coordinate √2 cos(kθ_i) at every other k. x_i(ω) collects coordinate i from each vector ω(b). Y_i is the indicated truncated and scaled Kronecker product of two outer-product matrices; mean i is its totalized Bochner integral; Z_i is its difference from that integral. w_i is a deterministic cosine scalar and Rstar is the displayed common bound.

## Domains

I=Fin d={0,...,d-1}, J=Fin(q+1)={0,...,q}, and K=J×J. D=EuclideanSpace ℝ I≈ℝ^d; E=EuclideanSpace ℝ J≈ℝ^(q+1), each with its Euclidean norm and Borel structure. Ω=J→D has the product measurable structure and μ=Measure.pi(fun b:J => stdGaussian D). r,L,Rstar∈ℝ; θ:I→ℝ; t:I→(J→ℝ); row:I→Ω→E; Y,Z:I→Ω→Matrix K K ℝ; mean:I→Matrix K K ℝ; w:I→ℝ. Matrix norms are the real Euclidean operator norms on ℝ^K. WithLp.toLp 2 wraps exactly the specified coordinates, and WithLp.ofLp recovers them without changing them. Scalar multiplication and subtraction are ordinary real matrix operations.

## Quantifiers

The outer universal quantifiers range over every d,q∈ℕ, implicit in the Lean binder, and over a proof hq:2*q+1<d. Each let binding is local to that universal instance; these are definitions, not additional existential or universal premises. The final connective is a conjunction of (∀i:I,∀ω:Ω, ||Z_i(ω)||op≤Rstar) and (∀i:I,∀ω:Ω, ||w_i Z_i(ω)||op≤Rstar). Both quantifiers are unrestricted pointwise quantifiers; there is no exceptional μ-null set. The integration variable in mean i is bound inside that integral and independent of the sample point later supplied to Z_i. Coordinate indices b,k,c,ℓ range over J whenever used.

## Assumptions

The only explicit hypothesis beyond typing is 2*q+1<d. The parameters are natural numbers, so q≥0 and the hypothesis entails d≥2q+2≥2; consequently m=q+1≥1 and the real denominator d is positive. These numerical facts are consequences, not extra hypotheses. The Gaussian law, product structure, Euclidean norms, and totalized Bochner integral are the approved meanings of the displayed definitions. There is no separate integrability, measurability, independence, bounded-sample, or positive-probability premise to add. The Gaussian product measure itself is part of the definitions; no separate hypothesis about random vectors is quantified.

## Conclusion

For all permitted d,q, the conjunction of two bounds holds: every i∈Fin d and every ω∈Ω satisfies ||Y_i(ω)−mean i||op≤2r(L+1)/d; every i and every ω also satisfies ||cos((2q+1)θ_i)·(Y_i(ω)−mean i)||op≤2r(L+1)/d. The same deterministic Rstar is used in both inequalities. The proposition is a uniform pointwise assertion, not an almost-everywhere or high-probability formulation. It displays no bound on a sum of the matrices, no tail probability, no concentration rate, no optimality of Rstar, and no separate integrability conclusion. Those statements are not part of the asserted conclusion; no claim about whether they are derivable is made here.

## Scopes

All local definitions, including the mean and common bound, remain in scope for both conjuncts under the fixed outer d,q,hq. A given Y_i(ω) uses exactly the branch ||row i ω||²≤L, including equality; otherwise it is the zero K-by-K matrix. Its entries in the active branch are d⁻¹ω(b)_iω(c)_i t_i(k)t_i(ℓ) at ((b,k),(c,ℓ)). The matrix mean i integrates the entire Ω-variable with respect to μ, separately for each i. It is fixed as ω varies in either conclusion. The approved integral is the usual Bochner integral when the integrand is integrable and is zero when it is not; in the latter case Z_i(ω)=Y_i(ω). The statement neither assumes nonintegrability nor supplies an integrability assertion. The square on the row norm is the square of the Euclidean vector norm; both conclusion norms are Euclidean operator norms on the paired index space. There is no conclusion restricted to the truncation event; both branches and every ω are covered. No source identity, source theorem, proof, or source-fidelity/compilation verdict is reconstructed.

## Constant dependencies

m=q+1∈ℕ and r=(q+1:ℕ) cast to ℝ depend only on q. L=2r+3 log(1000·d) depends only on d,q. θ_i=((i+1−1/2)π)/d depends only on i,d; t_i(k) depends only on d,i,k and its domain size q+1. The constants 1, 1/2, √2, π, 2, 3, and 1000 are fixed exactly as displayed. Y_i has scalar normalization d⁻¹. w_i=cos((2q+1)θ_i) uses the natural-number value 2q+1 cast to ℝ and depends only on d,q,i. Rstar=2r(L+1)/d=2(q+1)(2(q+1)+3 log(1000d)+1)/d depends only on d,q, not on i or ω; the additive 1 and all numerical factors are preserved. mean i depends on d,q,i and the fully specified product measure, not on the sample point ω in either bound. All inverse and logarithm operations are real operations; d>0 and 1000d>0 follow from hq.

## Literal assertion boundary

The displayed conclusion consists of exactly the two universally quantified inequalities joined by conjunction. All truncation cases, including equality in the active branch, are included. The definitions specify a Gaussian product measure and a totalized matrix integral; they do not introduce an integrability premise or append an integrability conclusion. No probability bound, sum estimate, source-fidelity conclusion, or compiler verification is supplied by this reconstruction. This is a reconstruction of the proposition as written, with no hidden premises and no additional theorem claims.

## Provenance and hashes

- Decoder: OpenAI Codex; independent source-blind mathematical decoder; task /root/neutral_decode_47a2
- Packet ID: ASTIS-BLIND-bae3298a138e618d
- source_text_visible: false
- Exact input_artifacts: ["lean-statement", "approved-definition-context"]
- Raw packet SHA256: 2704ea9593b0da9656864a0ec7f157dc0ac944fa502f0af915ae07c8affb4050
- Canonical packet SHA256: b160dc614d6bdd68cade26775ddc25d40e04ccfb8c71b0dd65a75bbd77da1a9a
- Canonicalization: UTF-8 JSON, sorted keys, compact separators, ensure_ascii=false, with the top-level packet_sha256 field omitted; no trailing newline.
- Embedded statement SHA256 (checked against the anonymous string): bae3298a138e618d5b12dac499cb3239cf202a8db26bea881e1345af1867ade7
- Reconstructed theorem text SHA256: 441d64520f2b54666881e49c9a00c8ac6d9d5af69faefa303a12e1ecc76331ff
- Text hash covers the exact UTF-8 bytes of reconstructed_theorem.txt, including its final newline.
- The packet reports compiled=true; no compiler or source was consulted and no compiler/source fidelity verdict is issued.
- Run provenance is in decoder_run.json; its hash is in result.json. The manifest and terminal freeze close the output set without embedding their own hashes.
