For every pair of natural numbers d and q satisfying 2q + 1 < d, set n = q + 1 and let r be the real number n. Let E be real Euclidean n-space, with its Euclidean norm and Borel structure, and let μ be the standard centered Gaussian probability measure on E: its coordinates in an orthonormal basis are independent real Gaussian variables of mean zero and variance one.

For x = (x_i) with i in Fin(n), define R(x) = ‖x‖₂², the real n-by-n matrix G(x) by G(x)_{ij} = x_i x_j, and the real n-by-n matrix W(x) = R(x) G(x). Thus W(x)_{ij} = ‖x‖₂² x_i x_j. Scalar multiplication here multiplies every matrix entry. Equip the matrix space with the operator norm induced by the Euclidean norm on real n-space, and with its usual finite-dimensional topology.

The conclusion is the conjunction of the following two assertions for these same E, μ, and W:

1. W is Bochner integrable with respect to μ: it is μ-almost everywhere strongly measurable and ∫_E ‖W(x)‖op dμ(x) < ∞. In this case ‖W(x)‖op = ‖x‖₂⁴, so the norm-integrability assertion is finiteness of the Gaussian fourth norm moment.
2. Its real Bochner integral is exactly

   ∫_E W(x) dμ(x) = (r + 2) I_n = (q + 3) I_n,

   where I_n is the n-by-n identity matrix. Equivalently, for every i,j in Fin(n),

   ∫_E ‖x‖₂² x_i x_j dμ(x) = q + 3 if i = j, and 0 if i ≠ j.

The integral is with respect to the Gaussian probability measure μ, not unweighted Lebesgue measure. Integrability is asserted in the matrix operator norm, rather than merely asserted separately for entries. The integral is the real Bochner integral. Although the supplied definition context gives it a zero default on nonintegrable functions, the explicit integrability conclusion makes that default irrelevant here.

All quantifiers and parameter cases are as follows. The statement is universal in natural d and q and in a witness of 2q + 1 < d; it has no additional hypotheses. This integer inequality is equivalent to d ≥ 2q + 2, so equality d = 2q + 2 is allowed. The symbol d does not determine the dimension of E and does not occur in W, μ, or the resulting constant. The only displayed multiplicative constant is exactly n + 2 = q + 3; it depends on q through n and is independent of d. There is no unspecified constant or further parameter dependence.

The boundary case q = 0 is included: n = 1, admissibility is d ≥ 2, W(x) is the one-by-one matrix with entry x⁴, and its integral under the real standard Gaussian probability law is the one-by-one matrix with entry 3. There is no zero-dimensional case because q + 1 ≥ 1. The values d = 0 and d = 1 admit no q satisfying the hypothesis, and the theorem asserts no case-specific conclusion for a pair that fails the hypothesis. The definition of W includes x = 0, where W(0) = 0, without any nonzero-vector assumption.

There is no unresolved ambiguity for the objects or integrability sense once the supplied approved definition context is used. No hypothesis on d or q beyond their natural-number domains and the displayed strict inequality is added.
