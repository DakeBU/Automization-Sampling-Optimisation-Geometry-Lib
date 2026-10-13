# Sharp standard Gaussian concentration: reusable leaf

Declaration:
`AutoSamplingTheory.TechnicalLemmas.Probability.GaussianLipschitzExponential.integral_exp_centered_le_stdGaussian_of_lipschitz`.

Home: `AutoSamplingTheory/TechnicalLemmas/Probability/GaussianLipschitzExponential.lean`.
Exact statement and mathematical exposition are centralized in
`website/content/declaration_lessons/gaussian-sharp-concentration.json`.
This note is the reuse/proof-obligation boundary, not a second statement seal.

Actual caller: SPHMC's existing full-range positive-step proximal Gaussian
oracle, consuming the scalar direction of its literal gradient output. Exact
signed exponential coefficient is produced internally. No synthetic consumer.

Searched/reused pinned interfaces: the existing ASTIS general Gaussian domain,
`IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity`,
`StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian`, pinned Mathlib
`IsGaussian.map_rotation_eq_self`, ordinary Haar integration by parts,
`hasDerivAt_integral_of_dominated_loc_of_deriv_le`, `hasDerivAt_mgf`,
MVT monotonicity, normalized bump convolution and dominated convergence.
Lean4.33.0; Mathlib db584cd6d46c92f209a44c0f1c829460d327499d.
The exact imports are recorded in the module; the route is entirely pinned
ASTIS/Mathlib. SLT remains an external reference; no port is credited.

Hidden regularity is internal: Lipschitz continuity/Borel measurability;
first moments and all signed exponential L1; polynomial-exponential product
domination; weighted Haar IBP inputs; genuine Fubini inputs; actual MGF derivative;
unit-mass positive smooth kernel; actual mean convergence and centered DCT.
Neither C1, positive dimension, positive Lipschitz constant nor an LSI estimate
is a public premise. The Gaussian covariance is tied to the given Hilbert metric.

Intended route (implemented and focused compiled):

1. Produce first moments and signed Laplace domains from the unchanged parent.
2. Derive ordinary Gaussian Stein from actual density and true L1 inputs.
3. Rotate independent Gaussians and differentiate the actual integral under domination.
4. Apply conditional Stein to the affine Lipschitz factor and use Fubini.
5. Use the signed multiplier and MVT endpoint comparison to get covariance control.
6. Apply actual MGF differentiation and signed Herbst with exact coefficient one half.
7. Remove internal C1 by same-L normalized convolution and centered dominated convergence.

Failure policy: preserve distinct typed API failures and compiled fragments;
freeze after the first occurrence and two unchanged repeats of one route/progress
fingerprint. Change a mathematical statement only after a real source/API diagnosis.
The existing failures changed only elaboration/notation, not the sealed target.

Tests include the nonsmooth unbounded norm at negative t, zero L, zero dimension,
and the actual quadratic source-output law with eta_n=n+2 and its exact growing
exponential bound. Independent mathematical/source/publication/commit gates
remain separate from these local focused successes.
