# Independent mathematical reconstruction

This reconstruction uses only the anonymous Lean statement and approved definition context in the supplied input packet. It makes no source-comparison verdict. The input reports compilation; this decoder did not independently run Lean or inspect a proof.

## Ambient objects and hypotheses

Let E be any finite-dimensional real inner-product space, with its induced norm and Borel measurable structure. No positive-dimension or nontriviality hypothesis is imposed. Let V : E → ℝ be twice continuously Fréchet differentiable. Let α, β be nonnegative real numbers, and let η be real. Assume

- α > 0 and α ≤ β;
- for every x, v ∈ E, α ‖v‖² ≤ D²V(x)[v,v] ≤ β ‖v‖²;
- η > 0 and βη ≤ 1.

Here D²V(x)[v,v] is precisely (fderiv ℝ (fderiv ℝ V) x v) v, and ∇V is the real Hilbert-space gradient. The Hessian bounds hold globally for every x and v. All statements below are under these fixed hypotheses. In particular β > 0 and √η > 0. No normalization of exp(-V), stochastic law, probability density, or initial-state distribution is assumed.

## Explicit definitions

For arbitrary y, r ∈ E put c = y − η∇V(r). On the phase space E × E, define for every real s

Φ(y,r,s,(x,v)) = (c + cos(s)(x−c) + √η sin(s)v,
                    −sin(s)/√η (x−c) + cos(s)v).

Scalar multiplication of vectors is understood in this formula. In particular the displayed trigonometric argument is s itself. For g_r(x) = ∇V(x) − ∇V(r), define

S(r,(x,v)) = (x, v − [2⟨v,g_r(x)⟩/‖g_r(x)‖²]g_r(x)).

The inner product is real. Real division by zero is defined as zero. Thus S fixes (x,v) whenever g_r(x)=0; the statement does not require this gradient difference to be nonzero.

For each integer n ≥ 0 and nonnegative real horizon T, let P(n,T) be the subtype of n real coordinates t = (t₁,…,tₙ) satisfying

0 < t₁ < ⋯ < tₙ < T.

Precisely, the Lean coordinates are indexed by Fin n from zero: our tₖ denotes the coordinate with index k−1. The first strict inequality and ordering are expressed by strict monotonicity of the tuple with an initial zero prepended. Put τ₀=0 and τⱼ=tⱼ for 1 ≤ j ≤ n. Let m(n,T) be the pullback, by the subtype inclusion P(n,T) → ℝⁿ, of canonical Lebesgue measure on ℝⁿ. Equivalently, it is Lebesgue measure on the open ordered-time simplex, represented on that subtype. It is not normalized to be a probability measure.

For z₀ ∈ E × E and t ∈ P(n,T), define recursively

zⱼ₊₁ = S(r, Φ(y,r,τⱼ₊₁−τⱼ,zⱼ)),  0 ≤ j < n.

Thus zⱼ is the recorded state after the event at τⱼ for j ≥ 1, and z₀ is the initial recorded state. The finite record type is Rec = ([0,∞) × (E × E)) ⊔ {cemetery}, and Hist(n) consists of n+1 records indexed from zero. The canonical history K records the live pair (τⱼ,zⱼ) at every index j=0,…,n. Formally its timestamp is max(τⱼ,0), which equals τⱼ for these admissible tuples.

The path type Path(T) is the set of functions [0,T] → E × E, equipped with its product measurable structure. For an arbitrary history h, Ψ(y,r,z₀,n,T,h)(s) is defined by the following finite fold in increasing record-index order. Start with accumulator z₀. For each live record (a,w), replace the accumulator by Φ(y,r,s−a,w) if a ≤ s; otherwise leave it unchanged. Cemetery records also leave the accumulator unchanged. The subtraction used formally is truncated nonnegative-real subtraction, then coerced to ℝ; in the branch a ≤ s it is ordinary s−a. For arbitrary histories this selects the last eligible record by index, not necessarily the largest timestamp.

Define Γ(y,r,z₀,n,T,t) = Ψ(y,r,z₀,n,T,K(y,r,z₀,n,T,t)). Since K has increasing timestamps, at each s ∈ [0,T] this path flows from the most recent recorded state zⱼ with τⱼ ≤ s. At an event time it uses the post-event record, with zero elapsed flow. Finally define the terminal-state map

A(y,r,z,t) = Γ(y,r,z,n,T,t)(T),

the velocity reversal R(x,v)=(x,−v), and the phase-volume measure ℓ = vol_E ⊗ vol_E. Dependence of A on the fixed n,T is suppressed in this notation.

## Reconstructed theorem

For every n ≥ 0 and T ≥ 0 there exists a single map ρ : P(n,T) → P(n,T), chosen before and independently of the quantified y,r,z, with all the following properties.

1. For each admissible t and each k=1,…,n,

   (ρ(t))ₖ = T − tₙ₊₁₋ₖ.

   This map is measurable, is an involution (ρ(ρ(t))=t), and preserves the measure m(n,T). Preservation means its pushforward of m(n,T) equals m(n,T); the Lean MeasurePreserving predicate also includes measurability.

2. For every y,r ∈ E, every z ∈ E × E, and every t ∈ P(n,T), the terminal state equals the flow after the last recorded event:

   A(y,r,z,t) = Φ(y,r,T−τₙ,zₙ).

   Here the recursion defining zₙ starts at the quantified initial state z, and τₙ is the last entry of (0,t₁,…,tₙ).

3. The map (y,r,z,t) ↦ A(y,r,z,t) is jointly measurable from ((E × E) × (E × E)) × P(n,T) to E × E, with its displayed product/subtype measurable structures. The first E × E packages y,r; the second packages the initial position and velocity. The claim is for each fixed n,T, not a joint measurability claim across n,T or V,α,β,η.

4. For every fixed y,r ∈ E and every fixed t ∈ P(n,T), the map z ↦ A(y,r,z,t) preserves ℓ on E × E, including measurability of this map.

5. For every y,r,z,t as above, terminal evolution with reversed velocity and reflected event times satisfies the exact identity

   A(y,r,R(A(y,r,z,t)),ρ(t)) = R(z).

   The parameters y and r are held fixed in both evolutions.

6. Define the map on phase state and event times

   Θ(y,r,(z,t)) = (R(A(y,r,z,t)),ρ(t)).

   The map (y,r,z,t) ↦ Θ(y,r,(z,t)) is jointly measurable on the same packaged input domain as in item 3, with codomain (E × E) × P(n,T). For every fixed y,r, Θ(y,r,·) is an involution and preserves the product measure ℓ ⊗ m(n,T). Thus applying Θ twice returns exactly (z,t); its measure-preservation assertion is equality of pushforward and original product measure, together with measurability.

All these conclusions hold simultaneously for the same ρ at fixed n,T. There are no existential unspecified constants in the conclusion and no omitted small-time, dimension, initial-state, or reference-point restriction. The constants α,β appear as assumptions; the constructed flow and event reflection use V,η and y,r. The formula for ρ uses only n,T and t. No rates or quantitative probability bounds are asserted.

## Empty, zero, and scope cases

When n=0, P(0,T) contains the unique empty tuple for every T ≥ 0, including T=0. Its measure is the zero-dimensional canonical Lebesgue measure, with mass one on that point. There are no event reflections; zₙ=z and τₙ=0, so A(y,r,z,t)=Φ(y,r,T,z). The map ρ is the identity on the singleton.

When T=0 and n>0, P(n,0) is empty. Its measure is zero, the map ρ is the unique empty-domain map, and all conclusions quantified over admissible event tuples are vacuous; the corresponding phase/time product domain is empty. When n=0 and T=0, A is the identity on phase states and Θ acts by velocity reversal on the phase state and identity on the empty tuple.

Zero-dimensional E is allowed. Phase space is then a singleton and all vector formulas have their usual zero-dimensional meaning. Zero gradient differences are explicitly allowed, with the event map equal to the identity there. The square-root denominators in Φ never divide by zero because η>0.

The path Γ is used through its definition and terminal evaluation. The proposition does not separately assert joint measurability of the entire path-valued Γ, path continuity, a distribution of random event times, invariance of a target probability measure, convergence, or a finite-time error estimate. Measures preserved in the explicit conclusions are Lebesgue phase volume, simplex Lebesgue measure, and their product. No statement about arbitrary histories h beyond the definition of Ψ is part of the conclusion.

## Decoder limitations

This is a semantic decoding of the supplied statement and approved definition context. Compilation is an input assertion, not newly verified evidence from this decoder. No source text, source identity, source anchor, implementation proof, publication lesson, registry entry, or previous audit was consulted. No claim of source fidelity or proof correctness is made here.
