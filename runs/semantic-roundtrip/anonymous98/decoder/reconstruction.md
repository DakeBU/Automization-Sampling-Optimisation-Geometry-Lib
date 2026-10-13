# Anonymous theorem reconstruction

Let E be any finite-dimensional real inner-product space, equipped with its normed additive group structure and a measurable-space structure whose measurable sets are the Borel sets. Let V : E → ℝ be twice continuously Fréchet differentiable. Let α, β be nonnegative real numbers and η a real number. Assume

- α > 0 and α ≤ β;
- for every x, v ∈ E, α ‖v‖² ≤ D²V(x)[v,v] ≤ β ‖v‖²;
- η > 0 and βη ≤ 1.

Here D²V(x)[v,v] means exactly (fderiv ℝ (fderiv ℝ V) x v) v, and ∇V denotes the real Hilbert gradient. The occurrences of α and β in real expressions use their coercions to ℝ.

For y, r ∈ E define c(y,r) = y − η ∇V(r). For any real u and phase-space point (q,p) ∈ E × E define

Φ(y,r,u,(q,p)) = (c(y,r) + cos(u)(q − c(y,r)) + √η sin(u) p, −sin(u)/√η (q − c(y,r)) + cos(u) p).

Scalar multiplication here is real scalar multiplication on E. Put d_r(q) = ∇V(q) − ∇V(r), and define

S_r(q,p) = (q, p − [2 ⟨p,d_r(q)⟩ / ‖d_r(q)‖²] d_r(q)).

Division uses Lean real division: a division by zero is zero. In particular S_r(q,p) = (q,p) when d_r(q) = 0; there is no nonzero-gradient-difference assumption.

Choose arbitrarily y, r ∈ E, an initial phase-space point z ∈ E × E, an integer n ≥ 0, a nonnegative real horizon T, and n real times τ₁,…,τₙ satisfying

0 < τ₁ < ⋯ < τₙ < T.

When n = 0 this condition is empty. Set τ₀ = 0 and Z₀ = z. Recursively, for j = 1,…,n, set

Zⱼ = S_r(Φ(y,r,τⱼ − τⱼ₋₁,Zⱼ₋₁)).

Thus Zⱼ is the state after applying S_r at time τⱼ. This indexing is a mathematical reindexing of the input's zero-based Fin n coordinates.

For 0 ≤ s ≤ T, let k(s) be the largest index j ∈ {0,…,n} such that τⱼ ≤ s, and define

Γ(s) = Φ(y,r,s − τₖ₍ₛ₎,Zₖ₍ₛ₎).

The index exists because τ₀ = 0. This is exactly the stated increasing-index fold: every live record whose time is at most s overwrites the accumulated value with its own flow value, so the last eligible record supplies the result. At each listed time τⱼ the path takes the post-reflection state Zⱼ. There is no reflection scheduled at T. Extend the path to every real s by

γ(s) = Γ(min(max(s,0),T)),

and set A = Γ(T). Define velocity reversal, the nonnegative rate, and the energy by

R(q,p) = (q,−p),
λ_r(q,p) = √η max(0, ⟨p,∇V(q) − ∇V(r)⟩),
U_y(q,p) = V(q) + ‖q − y‖²/(2η) + ‖p‖²/2.

Let

I₊ = ∫₀ᵀ λ_r(γ(s)) ds,
I₋ = ∫₀ᵀ λ_r(R(γ(s))) ds,

where ds is Lebesgue measure on ℝ and both expressions are Lean's interval integrals, with their usual signed orientation. Since T is nonnegative, the endpoints have nonnegative orientation.

The theorem asserts, for every choice above, all four statements simultaneously:

1. s ↦ λ_r(γ(s)) is interval-integrable with respect to Lebesgue measure between 0 and T.
2. s ↦ λ_r(R(γ(s))) is interval-integrable with respect to Lebesgue measure between 0 and T.
3. U_y(A) − U_y(z) = I₊ − I₋.
4. exp(−U_y(z)) exp(−I₊) = exp(−U_y(A)) exp(−I₋).

## Exact auxiliary objects and scope

The time-prefix set Δ(n,T) consists of t : Fin n → ℝ such that the function obtained by prepending 0 is strictly increasing and every coordinate is strictly less than T. Prefix(n,T) is the subtype of such t. Its membership proof is part of its type; the theorem quantifies over every element of that subtype, not almost every element.

The anonymous declaration also defines Rec = (ℝ≥0 × (E × E)) ⊕ Unit and Hist(n) = Fin(n+1) → Rec. A left summand is a time/state record, and the Unit right summand is the cemetery branch. The canonical history K has the n+1 live records (τⱼ,Zⱼ), with times converted by Real.toNNReal; all these times are already nonnegative. K never uses a cemetery record.

Path(T) is the full function type {s : ℝ≥0 | s ≤ T} → E × E. For a general Hist(n), Ψ evaluates a path by starting its fold at z, traversing all n+1 records in increasing index order, ignoring cemetery records and records with time greater than s, and overwriting the accumulator with Φ(y,r,s−a,state) at each eligible live record (a,state). The subtraction in this definition is nonnegative-real truncated subtraction, then coerced to ℝ; eligibility a ≤ s makes it ordinary elapsed time. No sortedness is required for the definition of Ψ on arbitrary histories. The theorem only applies Ψ to the canonical K above, producing Γ. It asserts no general-history result.

The local measure m(n,T) is Measure.comap of the subtype-value map Prefix(n,T) → (Fin n → ℝ), applied to volume on the real coordinate-function space. This is the exact unnormalized subtype measure specified by the input. It is unused in the conclusion and supplies no measure-theoretic hypothesis or probabilistic quantifier.

All displayed constructions are local definitions inside the theorem. They depend on the fixed E, V, and η where those parameters occur. α and β constrain V and η through the hypotheses, but no local flow, reflection, path, rate, or energy formula contains α or β explicitly. The center and flow depend on y and r; reflection and rate depend on r; energy depends on y; the canonical trajectory depends on y,r,z,n,T,t. No constants are existentially quantified, and there is no unspecified constant or uniformity convention.

The conclusions are deterministic statements for every finite prescribed prefix. They do not assert a distribution of prefixes, a random event count, path sampling, invariance of a probability measure, normalization of an exponential density, reversibility of a path law, or a relation to a separately constructed reversed trajectory. R in I₋ reverses the velocity at the same γ(s), without changing the time argument.

If n = 0 then Γ(s) = Φ(y,r,s,z) on [0,T]. If T = 0 then Prefix(n,T) is empty for n > 0, so those quantifications are vacuous; for n = 0 the trajectory endpoint is z and both integrals vanish. The space E is not required to have positive dimension. The path is not asserted continuous at reflection times; the theorem asserts interval integrability of the two scalar rate functions.

## Input limitations

Only the anonymous Lean statement and its approved definition context were inspected. The supplied metadata reports compilation, but this decoding performs no independent compilation or proof inspection. No original source text, source identity, or source-equivalence verdict is used or asserted. There is no unresolved ambiguity in the decoded quantifier or construction scopes; the input's exact Measure.comap convention is retained without replacing it by a probability law.
