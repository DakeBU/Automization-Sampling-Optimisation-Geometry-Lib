Let E be any finite-dimensional real inner product space with its compatible norm, equipped with a measurable structure equal to its Borel structure. The zero-dimensional space is allowed; products have the product topology and measurable structure. Let V : E → ℝ be twice continuously Fréchet differentiable, let α, β be nonnegative real numbers, and let η be real. Assume

0 < α,  α ≤ β,  0 < η,  βη ≤ 1,

and, for every x, v ∈ E,

α‖v‖² ≤ D(DV)(x)[v][v] ≤ β‖v‖².

Here ∇V is the Hilbert gradient representing the Fréchet derivative, and D(DV)(x)[v][v] is the displayed Hessian quadratic form. Inner products, norms, scalar multiplication, reciprocals, maxima, and square roots are real. Square roots denote the nonnegative real square root. Real division is total, with division by zero equal to zero.

For arbitrary y, a, x, n, p ∈ E and z = (x,p) ∈ E × E, define exactly

c(y,a) = y − η ∇V(a),
h(a,x) = ∇V(x) − ∇V(a),
R(n,p) = p − (2⟨p,n⟩ / ‖n‖²)n,
S(a,(x,p)) = (x, R(h(a,x),p)),
rate(a,(x,p)) = √η max{0, ⟨p,h(a,x)⟩},
H(y,a,(x,p)) = (η⁻¹‖x − c(y,a)‖² + ‖p‖²) / 2.

The following statements all hold jointly.

1. The map (a,z) ↦ S(a,z) from E × (E × E) to E × E is measurable. The map (a,z) ↦ rate(a,z) from E × (E × E) to ℝ is continuous and measurable.

2. For every p ∈ E, R(0,p) = p. For every n,p ∈ E,

R(n,R(n,p)) = p,
‖R(n,p)‖ = ‖p‖,
⟨R(n,p),n⟩ = −⟨p,n⟩.

These identities include n = 0 under the total-division convention.

3. For every a ∈ E and every z = (x,p) ∈ E × E,

(S(a,z))₁ = x,
S(a,S(a,z)) = z.

4. For every y,a ∈ E and every z ∈ E × E,

H(y,a,S(a,z)) = H(y,a,z).

5. For every a ∈ E and every z = (x,p) ∈ E × E,

0 ≤ rate(a,z),
rate(a,S(a,z)) = √η max{0, −⟨p,h(a,x)⟩},
rate(a,z) − rate(a,S(a,z)) = √η ⟨p,h(a,x)⟩.

6. For every a,x,p ∈ E, if h(a,x) = 0, then both

S(a,(x,p)) = (x,p)
and rate(a,(x,p)) = 0.

7. For every y,a ∈ E and every z₀ ∈ E × E, set H₀ = H(y,a,z₀). Then 0 ≤ H₀. For every z = (x,p) ∈ E × E satisfying H(y,a,z) = H₀, all three bounds hold:

‖p‖ ≤ √(2H₀),
‖x − c(y,a)‖ ≤ √(2ηH₀),
rate(a,z) ≤ √η · β · √(2H₀) · (√(2ηH₀) + ‖c(y,a) − a‖).

All assertions are universal over the ambient space and parameters satisfying the stated assumptions. In item 7, y, a, and z₀ are fixed before z is quantified, and the rate bound uses those same y and a. There are no additional existential constants or stochastic objects.