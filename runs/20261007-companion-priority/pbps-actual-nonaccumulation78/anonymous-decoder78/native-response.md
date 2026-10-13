# Anonymous theorem reconstruction

Let E be any finite-dimensional real inner-product space, possibly of dimension zero, with its Borel measurable structure. Let V : E → ℝ be twice continuously differentiable. Fix nonnegative real parameters α and β and a real parameter η satisfying α > 0, α ≤ β, η > 0, and βη ≤ 1. For every x,v ∈ E assume
α‖v‖² ≤ D²V(x)[v,v] ≤ β‖v‖².

For any fixed y,xRef ∈ E and any fixed initial pair z₀=(x₀,v₀) ∈ E×E, put c=y−η∇V(xRef). Define, for every real duration s and state z=(x,v),
Φ(s,z)=(c+cos(s)(x−c)+√η sin(s)v, −sin(s)(x−c)/√η+cos(s)v).
Writing g(x)=∇V(x)−∇V(xRef), define the bounce
S(x,v)=(x,v−[2⟨v,g(x)⟩/‖g(x)‖²]g(x)),
and the nonnegative rate rate(x,v)=√η max(0,⟨v,g(x)⟩).
For each state z and nonnegative duration u define the cumulative hazard
Λ(z,u)=∫₀ᵘ rate(Φ(s,z)) ds.
For a nonnegative threshold e define τ(z,e) as the infimum, in [0,∞], of nonnegative u for which Λ(z,u)≥e, with infinity for an empty hit set.

Take sample=(sample₀,sample₁,…) under the canonical countable product of rate-one exponential measures on ℝ. Define eₖ=max(sampleₖ,0), viewed in ℝ≥0. Starting with record₀=(0,z₀), update recordₖ with threshold eₖ. A stopped record remains stopped. For a finite record (a,z), if τ(z,eₖ)=∞ the next record is stopped; otherwise the next record is (a+τ(z,eₖ), S(Φ(τ(z,eₖ),z))). Define Tₙ to be the accumulated time in a finite record and infinity in a stopped record; in particular T₀=0.

For each fixed y,xRef,z₀, almost every sample satisfies both of the following simultaneously: for every finite nonnegative horizon t, Tₙ>t for all sufficiently large natural indices n; and for every such t the set {n∈ℕ : Tₙ≤t} is finite. This is escape beyond every finite horizon in the extended nonnegative time line, allowing an absorbing infinity record. It does not assert eventual stopping or that a finite event time ever becomes infinity.

## Objects

Potential V; parameters α,β,η; fixed center c depending on y and xRef; literal oscillator flow Φ; gradient-difference bounce S; rate; interval-integral cumulative hazard Λ; extended hitting time τ; absorbing finite-or-stopped update next; record recursion; extended eventTime T; product law P and clipped thresholds ε.

## Domains

E is a finite-dimensional real inner-product space with a normed additive commutative group and Borel measurable structure; dimension zero is allowed. V:E→ℝ, α,β∈ℝ≥0, η∈ℝ. States lie in E×E. Φ accepts all real durations, whereas hazard tests and horizons lie in ℝ≥0. Thresholds and finite accumulated times lie in ℝ≥0; τ and T lie in WithTop ℝ≥0. Samples are real sequences, indices are naturals, and records lie in (ℝ≥0×(E×E))⊕Unit.

## Quantifiers

Universally choose E and its displayed structures, V, α, β, η subject to the six supplied hypotheses. The Hessian bounds quantify every x,v∈E. After defining the process, universally fix y,xRef∈E and z₀∈E×E; then the conjunction holds almost everywhere in sample under P. Within that same almost-everywhere conjunction, each clause universally quantifies every finite nonnegative t. In the first clause the natural-index threshold for eventuality may depend on t and the sample.

## Assumptions

Exactly six analytic premises: hα:α>0; hαβ:α≤β; hV:V∈C²; hH:the global Hessian quadratic-form sandwich for every x,v; hη:η>0; hβη:βη≤1. Nonnegativity of α,β is encoded by their types. There are no extra restrictions on y,xRef,z₀, no positive-dimension premise, and no pointwise positivity premise on every sampled coordinate.

## Conclusion

For each fixed deterministic y,xRef,z₀, almost surely T eventually exceeds each finite nonnegative horizon, and the set of natural indices at or before each such horizon is finite. Index 0 is included. Infinity is greater than every tested horizon, so stopped records satisfy the eventual inequality and do not contribute indices after stopping to the finite-horizon set. No eventual-stopping, finite stopping index, quantitative growth, expectation, cost, invariant measure or convergence-of-state claim is stated.

## Scopes

The null set may depend on the fixed deterministic triple y,xRef,z₀, and on the preceding potential and parameters; there is no single asserted full-measure set uniform over all such triples. For a fixed triple the same full-measure assertion includes all horizons and both clauses. The horizon is always finite; infinity is only an event-time value. The recursion updates k to k+1 using sample coordinate k. A finite state is retained only in Sum.inl; stopped records carry no state. The integral is the literal real interval integral, and τ is the infimum hitting-time definition, not an independently assumed positive or attained waiting time.

## Constant Dependencies

No unnamed numerical constant, finite-index cutoff bound, event-count bound or uniform rate estimate appears. α,β,η are universally fixed input parameters with the displayed inequalities; √η and 2 are literal coefficients. c depends on y,η,V,xRef; Φ on c,η; S on V,xRef; rate on η,V,xRef; Λ and τ on the fixed y,xRef and starting state; record and T additionally on z₀ and the threshold sequence. P is the fixed rate-one product law, independent of E,V,α,β,η,y,xRef,z₀. An eventual natural-index cutoff is existential through atTop and may depend on horizon, sample, and fixed input data; no uniformity or quantitative dependence is supplied.

## Literal and boundary details

The displayed flow has literal unit-angle trigonometric time: the position displacement uses cos(s) and √η sin(s), and the velocity uses −sin(s)/√η and cos(s). The rate is √η times the positive part of the velocity/gradient-difference inner product. The bounce leaves position fixed. At a zero gradient difference, the literal real division by zero yields zero, so the bounce is the identity and the rate is zero. No separate nonzero-gradient premise is present.

The product law gives rate-one exponential coordinates; clipping nevertheless defines thresholds at every real sequence, including exceptional nonpositive coordinates. Such coordinates become zero rather than invalid inputs. The proposition is an almost-everywhere assertion and gives no conclusion for every exceptional sequence. An e=0 threshold has zero in its hazard hit set because Λ(z,0)=0; initialization index 0 and any coincident event indices are counted by the displayed natural-index set.

The absorbing branch is essential to the literal conclusion: if a hazard never reaches its threshold, τ is infinity and the next record becomes stopped. The guarded finite branch uses untopD 0 only when τ is finite; its default value does not turn an infinite waiting time into a zero-time bounce. An infinite record has eventTime infinity and no pair (x,v) attached. Escape beyond finite horizons also allows an infinite sequence of finite event times increasing without bound. The conclusion does not force finite-index stopping. In dimension zero the formulas still have a meaning, and the statement makes no exception for that space.

This reconstruction describes the anonymous proposition and the approved context only. It supplies no proof credit and no source-fidelity verdict.
