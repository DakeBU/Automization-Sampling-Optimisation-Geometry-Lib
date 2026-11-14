# Anonymous statement reconstruction

For every pair of natural numbers d and q satisfying 2q + 1 < d, let D = ℝ^d and E = ℝ^(q+1), with their Euclidean structures. Write γ_D and γ_E for the centered Gaussian probability measures with identity covariance on these spaces. Let Ω = D^(q+1), whose elements are tuples ω = (ω_a) indexed by a ∈ {0, …, q}, and equip Ω with the product measurable space and the probability measure μ = ⊗_{a=0}^q γ_D.

For each i ∈ {0, …, d−1}, define R_i : Ω → E by

    (R_i(ω))_a = (ω_a)_i,  for every a ∈ {0, …, q}.

Then, for every i ∈ {0, …, d−1}, the map R_i is measurable and its pushforward of μ is γ_E:

    (R_i)_* μ = γ_E.

Equivalently, for every measurable subset A of E,

    μ({ω ∈ Ω : R_i(ω) ∈ A}) = γ_E(A).

Thus, if q+1 independent vectors each have the standard Gaussian distribution in ℝ^d, the vector consisting of their i-th coordinates has the standard Gaussian distribution in ℝ^(q+1), for every fixed coordinate index i.

## Objects and domains

- d and q are natural numbers. Their quantification allows q = 0. The strict dimension hypothesis is equivalent, for these natural numbers, to d ≥ 2q + 2; in particular d ≥ 2.
- Fin d is the coordinate-index set {0, …, d−1}; Fin (q+1) is the factor-index set {0, …, q}.
- D is the real d-dimensional Euclidean space, with coordinates indexed by Fin d.
- E is the real (q+1)-dimensional Euclidean space, with coordinates indexed by Fin (q+1).
- Ω is the function space Fin (q+1) → D, interpreted as a finite product with its product measurable space. For ω ∈ Ω, ω_a is a vector in D and (ω_a)_i is a real number.
- μ is the product of q+1 copies of γ_D. Its coordinate factors ω_a are independent standard Gaussian D-valued vectors.
- R_i is the map called row i in the anonymous statement. It collects the i-th real coordinate from each factor. WithLp.toLp 2 merely represents that coordinate function as an element of E and changes none of its coordinates.
- γ_D and γ_E are probability measures with zero mean and identity covariance; their dimensions are d and q+1 respectively.

## Quantifiers and assumptions

The outer quantifiers are universal over d ∈ ℕ and q ∈ ℕ. For each such pair, hq is a proof of the assumption 2q + 1 < d. The local definitions D, E, Ω, μ, and row are made within that scope. The concluding quantifier is universal over i ∈ Fin d. The symbol ω is the bound argument in the definition of each map, and a is the bound factor index defining its output coordinates.

There is no existential choice of dimensions, coordinate index, measure, or map. The displayed equality for every measurable A is an expansion of the pushforward conclusion, not an extra hypothesis. No further condition on q, no selected vector or subset, and no nondegeneracy hypothesis beyond the displayed dimension assumption is present.

## Conclusion and its scope

For every allowed d, q, and every coordinate index i, both measurability of R_i and the exact equality (R_i)_* μ = γ_E hold. This is equality of measures on the entire codomain E, not an approximation or a bound on selected events. The standard Gaussian law of R_i includes centered coordinates of variance one and identity covariance in dimension q+1.

The universal quantifier over i concerns the separate map and distribution for each index. The statement does not include an additional formula for the joint pushforward of all the rows together. MeasurePreserving here asserts measurability and pushforward equality; it asserts no injectivity, bijectivity, inverse map, or pointwise preservation of vector norms. There is no almost-everywhere qualifier on the map's measurability or on the equality of measures.

## Constant and parameter dependencies

There are no unspecified constants, existential constants, error parameters, limiting variables, or asymptotic qualifications. The values zero, one, and two have fixed roles: zero mean, identity covariance, the dimension constraint 2q + 1 < d, the factor count q+1, and the Euclidean exponent 2 in WithLp.toLp 2. D and γ_D depend on d; E and γ_E depend on q; Ω and μ depend on d and q; R_i additionally depends on i. The proof term hq supplies the dimension hypothesis and is not an additional numeric or probabilistic parameter.

## Reconstruction basis

This reconstruction uses only the supplied anonymous Lean statement and its five approved definition explanations. The packet's compilation flag was supplied as data; no compilation, proof, source lookup, implementation inspection, or comparison with an original source was performed. No source identity or source-fidelity verdict is inferred.
