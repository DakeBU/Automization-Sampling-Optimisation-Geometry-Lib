# Actual proximal-estimator input stability

Source: Chen, Chewi, Lu, Zhang, arXiv:2609.06906v1, Lemma 4.2,
equations (4.4) and (4.5), using the actual estimator (3.2).

At main 08b7eb3913ea7423f2cec34cfa1f68ac28ffd30c the existing
ProximalGaussianEstimator constructs the actual measurable oracle and kernel.
GibbsPositionMoment is also present. Neither supplies the global input bounds.
Independent rgo_independent_verifier compared the PBPS frontier and recommends
this dependency-ready SPHMC edge before the PBPS operator-domain/core bridge.

## Frozen bounded target

File: AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/ProximalEstimatorLipschitz.lean.
Namespace: AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalEstimatorLipschitz.
Public declaration: proximal_estimator_lipschitz.
Import the existing ProximalGaussianEstimator module only.
Finite-dimensional complete real inner-product E with Borel measurable space;
V is genuinely C2, kappa is NNReal with kappa>=1, Hessian between kappa^-1 and1.
Fix 0<eta<=1/2. Construct measurable p with the genuine proximal equation,
unique-minimum identification, Lipschitz constant1, and both estimator input
inequalities with constants1 and sqrt(eta). No assumed nonexpansiveness.

The eta<=1/2 restriction is inherited from the existing measurable construction,
not mathematically required for the two inequalities and not a source repair.
The private optimality-to-nonexpansiveness proof works for every eta>=0.
This is partial source coverage, not the entire Lemma 4.2 for all eta.

## Reuse audit and proof route

Searched ASTIS and pinned Mathlib Analysis/Convex for proximal/nonexpansive
interfaces; none supplies this actual map. outer_repos is absent locally.
Reuse QuadraticRegularization at r=0 for genuine gradient Lip1/strong convexity;
reuse StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn.
No external code is copied. Existing proximal-energy conceptual family suffices.

1. Obtain actual p and unique global minimizer from proximal_gaussian_estimator.
2. Use the genuine C2 gradient and existing strong-convex first-order theorem
   to obtain nonnegative gradient monotonicity pairing.
3. Subtract the two proximal equations. Pair with the proximal displacement.
4. Monotonicity and Cauchy imply ||dp||^2<=||dy|| ||dp||; handle dp=0 before cancellation.
5. Apply gradient Lip1 and translation invariance for the position estimate.
6. Apply gradient Lip1 and norm_smul for the Gaussian input estimate.
7. Focused test checks the public theorem and axioms before source/reader admission.

Consumer: the two random Picard estimator evaluations in Algorithm 3.1;
Lemma 4.2 input stability, later local error analysis. These are intended source
consumers, not claims that unimplemented Picard Lean declarations exist.
No score bias, Gaussian concentration/MGF, smoothing derivatives, actual Picard
accuracy, initialization, or total query-cost conclusion is included.

Failure policy: after repeated identical errors, audit the statement/API rather
than replay tactics. No semantic hypothesis changes without explicit review.
