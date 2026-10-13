# Anonymous theorem reconstruction

Let E be a finite-dimensional real inner-product space with its normed additive group structure and Borel measurable structure. Let V : E → ℝ be twice continuously Fréchet differentiable. Let α,β ∈ ℝ≥0 and η ∈ ℝ. Assume α > 0, α ≤ β, η > 0, βη ≤ 1 and, for every x,v ∈ E,
α‖v‖² ≤ D(DV)(x)[v][v] ≤ β‖v‖².
All derivatives and gradients are over ℝ.

Fix the following local definitions. For y,r ∈ E, put c(y,r) = y − η∇V(r). For every real u and (x,v) ∈ E × E, put
Φ(y,r,u,(x,v)) =
(c(y,r) + cos(u)(x − c(y,r)) + √η sin(u)v,
 −sin(u)/√η (x − c(y,r)) + cos(u)v).
Multiplication of vectors by real coefficients denotes scalar multiplication.

Set d_r(x) = ∇V(x) − ∇V(r) and
S(r,(x,v)) = (x, v − [2⟨v,d_r(x)⟩/‖d_r(x)‖²] d_r(x)).
Real division by zero is zero, so S is the identity when d_r(x) = 0. Nonzero gradient difference is not assumed.

Define Rec = (ℝ≥0 × (E × E)) ⊕ Unit. A left-summand record is a live nonnegative timestamp/state pair; the right summand is a cemetery marker. Define Hist(n) to be the functions from {0,…,n} to Rec.

For n ∈ ℕ and T ∈ ℝ≥0, Δ(n,T) consists of real n-tuples t such that prepending zero gives a strictly increasing sequence and every coordinate is strictly below T. Prefix(n,T) is the subtype of these tuples. For n > 0 this means 0 < t₀ < ⋯ < tₙ₋₁ < T. Prefix(0,T) contains the unique empty tuple, even for T = 0; Prefix(n,0) is empty for n > 0. Define the local measure m(n,T) exactly as Measure.comap of the subtype-value map Prefix(n,T) → (Fin n → ℝ), applied to volume on (Fin n → ℝ). It is unnormalized, does not occur in the conclusion, and supplies no hypothesis.

Fix y,r,z₀,n,T and t ∈ Prefix(n,T). Set g₀ = 0 and gⱼ = tⱼ₋₁ for 1 ≤ j ≤ n. Define zAt(y,r,z₀,n,T,t) on indices j = 0,…,n by the recursion
p₀ = z₀,
pᵢ₊₁ = S(r,Φ(y,r,tᵢ − gᵢ,pᵢ)), for i = 0,…,n−1.
Here pⱼ is its jth value. Define K(y,r,z₀,n,T,t) ∈ Hist(n) to have live record (Real.toNNReal(gⱼ),pⱼ) at index j. Real.toNNReal is the nonnegative part, so on these valid tuples it is simply gⱼ viewed as a nonnegative real.

Define Path(T) to be the functions {s ∈ ℝ≥0 : s ≤ T} → E × E. For arbitrary h ∈ Hist(n), define Ψ(y,r,z₀,n,T,h)(s) by an increasing-index fold through j = 0,…,n, starting with accumulator z₀. A cemetery marker leaves the accumulator unchanged. A live record (a,w) with a > s also leaves it unchanged. A live record with a ≤ s replaces it by Φ(y,r,s − a,w). This subtraction is first in ℝ≥0, hence truncated at zero, and then coerced to ℝ; in the applicable branch it is ordinary nonnegative elapsed time. Thus the last eligible live record in index order determines the result, or the result remains z₀ if none is eligible. General histories need not have ordered timestamps.

Define Γ(y,r,z₀,n,T,t) = Ψ(y,r,z₀,n,T,K(y,r,z₀,n,T,t)). Define R(x,v) = (x,−v) and
rate(r,(x,v)) = √η max(0,⟨v,∇V(x) − ∇V(r)⟩).

The theorem asserts: for every n ∈ ℕ and every T ∈ ℝ≥0, there is a function ρ : Prefix(n,T) → Prefix(n,T) such that, for every valid t and i = 0,…,n−1,
(ρ(t))ᵢ = T − tₙ₋₁₋ᵢ.
For the same ρ, the following hold for every y,r ∈ E, every initial state z ∈ E × E, and every t ∈ Prefix(n,T).

Set the forward grid g = (0,t₀,…,tₙ₋₁,T), indexed 0,…,n+1. For j = 0,…,n, define
pⱼ = zAt(y,r,z,n,T,t)(j),
aⱼ = Φ(y,r,gⱼ₊₁ − gⱼ,pⱼ).
Set A = Γ(y,r,z,n,T,t)(T), evaluating at the final point of the nonnegative closed interval. Set the reversed grid bar g = (0,(ρ(t))₀,…,(ρ(t))ₙ₋₁,T) and, for j = 0,…,n, define
bar pⱼ = zAt(y,r,R(A),n,T,ρ(t))(j),
bar aⱼ = Φ(y,r,bar gⱼ₊₁ − bar gⱼ,bar pⱼ).
In particular, both recursions use the same y,r,V,η, and the reversed recursion starts from R(A).

Then for every j = 0,…,n,
bar pⱼ = R(aₙ₋ⱼ) and bar aⱼ = R(pₙ₋ⱼ),
and moreover
∏ᵢ₌₀ⁿ⁻¹ rate(r,bar aᵢ) = ∏ᵢ₌₀ⁿ⁻¹ rate(r,aᵢ).

The tuple reversal is n−1−i on n coordinates, whereas the state reversal is n−j on n+1 states. The rate products include only arrival indices 0,…,n−1, excluding the final arrival index n. Zero rate factors are allowed and retained; there is no division by a rate. The recursion reflects at interior event times, with no reflection at the terminal endpoint.

When n = 0, both rate products are empty and equal 1. The state identities still concern j = 0: A = Φ(y,r,T,z), bar p₀ = R(A), and bar a₀ = R(z). They also apply when n = T = 0, with zero elapsed time. When T = 0 and n > 0, claims quantified over Prefix(n,T) are vacuous.

All ambient parameters and hypotheses are fixed before n,T are quantified. The function ρ is chosen before y,r,z,t and works uniformly for all of them. Its prescribed coordinate formula uses only n,T,t and uniquely determines it on valid tuples. The constants α and β appear in the assumptions but not in the definitions or final identities. The flow and rate use η as displayed; the reflection uses V and r. No additional numerical constants are quantified. There are no distributional, randomness, integral, measure-preservation, or full-path equality assertions in this conclusion.

This reconstruction uses the anonymous Lean statement and its approved definition context only. The input packet reports compiled = true; I performed no compilation and make no independent compilation or source-fidelity claim.
