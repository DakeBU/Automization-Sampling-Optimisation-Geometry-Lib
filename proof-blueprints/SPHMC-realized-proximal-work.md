# Same implemented query under its realized input

Source: arXiv:2609.06906v1 Algorithm D.2 and Lemma D.4, Jensen step after D.7.
Target: `RealizedProximalWork.realized_proximal_expected_work`.
Parents: actual stopped interpreter and the existing proximal expected-work theorem.
Consumer: the very same q/N returned by `ImplementedPhaseKernel`, evaluated at a
measurable realized Picard center. D.7 moment control and D.8 total work stay open.

For the normalized C2 Hessian bounds and 0 < eta <= c < 1, eps > 0, let q,N satisfy
the actual interpreter's successful-return equation at fuel N(y)+1. For a
probability law mu on an arbitrary measurable input space and a measurable center
Y with integrable ||grad V(Y)||^2, prove

    E_mu[N(Y)+1] <= C_c [1+log(1+sqrt(E_mu||grad V(Y)||^2)/eps)],
    C_c = 2 + (1+log((1-c)^(-1)))/(-log c).

The result includes integrability of this actual count. It assumes no count
measurability, count integrability or expected-cost conclusion: these are derived
by deterministic success uniqueness and the parent's measurable stopped witness.

1. Induct on fuel to show two successful runs from the same input and state have
   identical returned points and counts, including the final gradient test.
2. Push mu forward by Y and transfer gradient square-integrability by Mathlib.
3. Apply the already compiled expected-work theorem to that actual law.
4. Compare its successful run to the supplied successful implementation at every y.
5. Equality of successful counts identifies N pointwise with the measurable witness.
6. Pull back both integrability and the exact expected-work bound along Y.

No TV comparison is used. The moment assumption is an explicit smaller boundary,
not an assertion of the paper's run-wide D.7. No source parameter substitution,
Chebyshev node count, repeated histories, total work or main theorem is proved.
The focused test consumes the positive-dimensional two-node phase's actual q/N,
retains both Gaussian arrays, and checks work under its actual first-center law.
The gradient moment remains the explicitly named D.7 dependency.

Conceptual mirror audit: none found; deterministic execution identification and
ordinary pushforward integration reuse existing mechanisms.
