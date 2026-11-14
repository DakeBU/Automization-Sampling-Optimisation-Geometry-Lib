# Finite real-matrix expectation positivity

Status: candidate, unproved and not callable.

The proposed shared declaration is
`AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef`
in `AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveIntegral.lean`.
Its exact statement is sealed separately. For an arbitrary probability measure,
an integrable function with values almost everywhere in the full positive
semidefinite cone of finite real matrices has a positive semidefinite Bochner
expectation. Empty finite matrix indices are allowed. The declared norm is the
Euclidean operator norm.

This is an explicitly ASTIS-authored background specialization. The Gaussian
paper uses positivity under expectation in C.2 p14, but does not print this
general arbitrary-function theorem. The canonical upstream integral provider is
the fixed Mathlib `Convex.integral_mem` theorem. Existing R4/R5 private local
applications are preserved as history, rather than imported as public providers.

The actual source consumer is the unchanged sealed original-experiment
uncentered squared-moment bound. The centered/weighted centered square
expectations are a second planned consumer family. Each concrete application
must derive integrability and full PSD internally; neither contract is an added
Gaussian theorem binder. Only an actual compiled call will create a Lean edge.

The initial import plan is `Mathlib.Analysis.Convex.Integral`,
`Mathlib.Analysis.CStarAlgebra.Matrix` and
`Mathlib.LinearAlgebra.Matrix.PosDef`, with no ASTIS theorem dependencies.
The actual minimal compiled import closure remains to be checked.

Hidden contracts are the probability measure, actual Bochner integrability
(including AE strong measurability and finite norm integral), AE full Hermitian
and quadratic-form positivity, and internally synthesized finite-matrix
completeness. There is no pointwise-measurability, nonempty-index, externally
supplied closed/convex cone, or source variance certificate input.

The intended route is:

1. Identify the complete PSD predicate with Hermitian matrices whose every
   finite vector quadratic evaluation is nonnegative.
2. Prove that this matrix set is closed in the actual operator-norm topology.
3. Prove convexity using nonnegative scalar multiplication and addition of PSD
   matrices, retaining the Hermitian condition.
4. Apply the exact probability/AE/integrable `Convex.integral_mem` interface and
   identify its set-membership conclusion with the sealed full PSD conclusion.
5. In the actual Gaussian consumer, prove the actual untruncated-majorant minus
   squared-summand residual integrable and PSD, then use this shared declaration
   and identify its integral by justified finite-sum and integral algebra.

No proof attempt is claimed here. Two or three same-shape failures require a
typed diagnosis of statement, representative, API, import or scope, with all
valid fragments retained. An implementation/API failure cannot retire the
mathematical target or justify a new Gaussian hypothesis. A direct
Hermitian/quadratic integral derivation is an alternative route, not another
compulsory proof or a source-author route.

Serialized Registry/source-index/globalgraph/publication integration, actual
reader delivery and purification remain open under the original owner policy.
