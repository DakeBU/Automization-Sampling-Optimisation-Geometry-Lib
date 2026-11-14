# Full natural-language theorem

Let n be any finite index type, possibly empty, with decidable equality. Let Ω be any type equipped with a chosen sigma algebra, and let μ be any probability measure on Ω, so that μ(Ω) = 1. Consider the space Matrix n n ℝ of real square matrices indexed by n, with the complete Euclidean operator norm.

For every function f : Ω → Matrix n n ℝ, assume that f is integrable with respect to μ: it is almost-everywhere strongly measurable and the integral of its extended norm is finite. Also assume that, for μ-almost every ω, f(ω) is positive semidefinite. This latter assumption means that outside an exceptional μ-null set, (f(ω))ᵀ = f(ω) and, for every vector x : n → ℝ,

    ∑ᵢ∈n ∑ⱼ∈n xᵢ (f(ω))ᵢⱼ xⱼ ≥ 0.

Then the Bochner integral matrix

    A = ∫ ω, f ω ∂μ

is positive semidefinite. Explicitly, Aᵀ = A and, for every vector x : n → ℝ,

    ∑ᵢ∈n ∑ⱼ∈n xᵢ Aᵢⱼ xⱼ ≥ 0.

For these finite real matrices, the displayed symmetry and quadratic-form conditions are the full meaning of positive semidefiniteness: Hermitian means equality with the transpose, and testing every finitely supported vector is the same as testing every vector indexed by n. The nonnegativity condition includes equality to zero.

# Seven-slot analysis

## Objects

The inputs are an index type n, a type Ω equipped with a chosen sigma algebra, a measure μ on Ω, and a function f : Ω → Matrix n n ℝ. The type n carries finite-type and decidable-equality structures, and μ carries the assertion that it is a probability measure. The named arguments hf and hpos are proofs of assumptions, not additional mathematical outputs. The matrix whose positive semidefiniteness is asserted is the Bochner integral ∫ ω, f ω ∂μ; it is an expression formed from the inputs, not an independently quantified matrix. There are no let-bound objects in the anonymous statement. The letter A used in the prose is only an explanatory abbreviation for that integral.

## Domains

The type n is any finite index type and is allowed to be empty; decidable equality means that equality of its indices can be decided. The type Ω is arbitrary apart from its chosen measurable-space structure. The measure μ is a measure on that measurable space with μ(Ω) = 1. Matrices lie in Matrix n n ℝ, the space of real square matrices indexed by n, with the complete Euclidean operator norm specified in the approved definitions. Test vectors are all functions x : n → ℝ; because n is finite, these are exactly the vectors covered by the finitely supported quadratic-form test. The scalar domain is ℝ.

## Quantifiers

Universally quantify over both types n and Ω, every finite-type structure and decidable-equality structure on n, every measurable-space structure on Ω, every measure μ on Ω satisfying the probability-measure condition, and every function f : Ω → Matrix n n ℝ. For each such choice, assume hf : Integrable f μ and hpos : for μ-almost every ω, Matrix.PosSemidef (f ω). Inside hpos, the almost-everywhere quantifier applies to the entire positive-semidefinite predicate: outside one exceptional μ-null set the symmetry condition and the quadratic-form inequality for every vector x both hold. In the conclusion the integral matrix satisfies the quadratic-form inequality for every vector x : n → ℝ.

## Assumptions

The assumptions are: n is finite, n has decidable equality, Ω has its chosen sigma algebra, μ is a probability measure (the whole space has measure one), f is integrable with respect to μ, and f(ω) is positive semidefinite for μ-almost every ω. Integrable means that f is almost-everywhere strongly measurable and the integral of its extended norm is finite. Positive semidefinite means Hermitian together with nonnegativity of the quadratic form for every finitely supported vector; here, for finite real matrices, this is precisely (f(ω))ᵀ = f(ω) and ∑ᵢ∈n ∑ⱼ∈n xᵢ (f(ω))ᵢⱼ xⱼ ≥ 0 for every x : n → ℝ. Both parts of this predicate hold outside an exceptional μ-null set. No pointwise-for-every-ω assumption is imposed.

## Conclusion

The Bochner integral matrix ∫ ω, f ω ∂μ is positive semidefinite. In full, if A denotes this integral, then Aᵀ = A and, for every x : n → ℝ, ∑ᵢ∈n ∑ⱼ∈n xᵢ Aᵢⱼ xⱼ ≥ 0. The endpoint zero is included. This is the entire asserted conclusion.

## Scopes

The probability measure μ and the function f remain fixed within their universally quantified instance; both integrability and the almost-everywhere condition refer to that same μ. The null exceptional set belongs to the input positive-semidefinite assumption and covers the whole predicate, including every test vector. The conclusion is an unconditional property of the single integral matrix within an instance satisfying the hypotheses; it has no remaining ω parameter and is not an almost-everywhere conclusion. All sums use the same finite index type n on both matrix axes and on the test vector. The integral is the Bochner integral in the stated complete normed matrix space. Its approved definition is totalized to zero outside complete or integrable cases, but the explicit integrability hypothesis is required here and the matrix space is complete. There are no let bindings, existential output choices, or additional conclusions.

## Constant dependencies

No existential constant, bound parameter, threshold, rate, or choice of a constant is asserted, so there is no such constant-dependency claim. The numerical values appearing in the meanings of the predicates are the fixed normalization 1 in μ(Ω) = 1 and the fixed lower endpoint 0 in the nonnegative quadratic-form inequalities; the norm-integrability condition requires a finite integral rather than an asserted quantitative upper bound. The integral matrix is determined by f and μ and has the matrix index type n; the hypotheses depend on these same inputs and on the specified measurable and normed structures.
