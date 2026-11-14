# Independent exact Gaussian-consumer meaning review

Reviewer: `/root/fs_admiss_topology_challenge`, distinct from the producer and
consumer implementer. Verdict: **SOURCE-COMPATIBLE INTERFACE — IMPLEMENTATION
ADMISSION ONLY** for the unchanged mathematical producer and the exact sealed
actual Test consumer. No remaining statement/carrier/meaning blocker was found.
This review does not certify a producer proof, consumer proof, compiler run,
source-V result, or full C.4 completion.

The consumer seal SHA-256 is
`620f79693f278af2409e4b7bbc7709d158a15465dd7571df2cb79dfb921f80a1`;
its exact signature SHA-256 is
`ef756379bce4efb8c2b4a323b2bb5aaa626bb2a4195ee5da09321f20f6c0c870`.
The unchanged producer signature remains
`186231307d4c41acba15a1098c56518120394295cf048f504fed6f8ea50018d5`.
The previous independent pre-proof gate was frozen as
`46ba36787dc791a4f0476b0b8c84fd6ee8e44ba8819815adedf0c0dbd2675b2a`.

## Seven semantic slots

| Slot | Exact consumer meaning and source comparison |
| --- | --- |
| Objects | The same literal half-grid θ, cosine diagonal and real A=OΛOᵀ as the producer. The actual measure `multivariateGaussian 0 A⁻¹` is equated to an explicit quadratic density. A is precision; A⁻¹ is covariance. |
| Domains | Integer d≥2, real κ≥2, full real O(d), vectors in `EuclideanSpace ℝ (Fin d)`. Finite real coordinate entries are extracted by `WithLp.ofLp`; no coordinate is dropped or rescaled. |
| Quantifiers | For every d, κ in the source local ranges and every orthogonal O, define this actual A and assert the measure equality. No random/generic O, almost-sure qualification, or existential covariance replaces the source object. |
| Assumptions | Exactly the source endpoint premises and orthogonal-group carrier. No hPD, hCovariance, hDensity, hNormalizer, inverse identity, measurability, or Gaussian correctness binder. Zero EXCESS public premises. |
| Conclusion | Equality of actual measures on Euclidean space: N(0,A⁻¹) equals Euclidean Lebesgue measure weighted by `ofReal (sqrt(det A)/(2π)^(d/2) * exp(−xᵀAx/2))`. This realizes the actual target/potential and determinant-normalization context, rather than just proving an `IsGaussian` predicate. |
| Scopes/senses | The equality is for the literal positive precision. It is not a different block family, arbitrary probability-law witness, formal Gaussian tag, covariance A, surface measure, or probability reference measure. The existing total Gaussian definition's non-PSD fallback must be excluded by internally supplied positivity. |
| Constants/dependencies | Half-offset and π are unchanged. The exponent is real division `(d : ℝ)/2`, correct also when d is odd. The normalizing coefficient is reciprocal to C.4's `(2π)^(d/2)(det A)^(−1/2)` under positive determinant. There is no κ≥4, n≥3, δ, accuracy, or algorithm/query condition. |

This is a faithful concrete semantic expansion of `S4.SS1.p1.2` and
`A3.SS4.p3.1`/`A3.Ex160`, under the already reviewed Eq. (11) construction.
The source does not separately display this normalized density in C.4; the
consumer supplies the standard actual-law interpretation of its potential,
Gaussian target, and Gaussian integration formula. No source correction is
being introduced.

## Reference measure and coordinates

The sealed code explicitly uses
`(volume : Measure (EuclideanSpace ℝ (Fin d)))`. The canonical reused leaf has
the same explicit reference measure. The standard `EuclideanSpace` alias is
`PiLp 2 (fun _ : Fin d => ℝ)`. `WithLp` has an underlying `ofLp` field, so
`WithLp.ofLp x` returns the real coordinates of the same Euclidean vector.
The matrix definitions give `mulVec A x` by row dot products and `dotProduct`
by the ordinary finite sum. Thus the exponent is exactly the real quadratic
`−xᵀAx/2` on the whole source space.

The standard finite-dimensional inner-product `MeasureSpace` instance defines
volume as the additive Haar measure of the standard orthonormal basis.
The corresponding volume documentation identifies its normalization as
Lebesgue measure, giving volume one to a parallelepiped spanned by an
orthonormal basis. Therefore the explicit reference is ordinary Euclidean
Lebesgue volume. A pretty-printer's `ℙ` for a default measure does not change
that explicit constant into a probability or Gaussian reference measure.
The review uses the sealed explicit source term and standard measure
definition, not the pretty-printed glyph as evidence of measure identity.

The real determinant is positive once the new producer supplies A.PosDef.
The factor `sqrt(det A)` is therefore the positive determinant square root;
`2π` is positive, real power is well defined, and the exponential density is
positive. `ENNReal.ofReal` is the standard embedding of this nonnegative real
density, not an intended clipping/default replacement for failed positivity.
All required positivity and normalization belong to internal dependencies.

## Canonical leaf and inverse semantics

I inspected the exact existing shared leaf interface in
`AutoSamplingTheory/TechnicalLemmas/Measure/GaussianPrecisionDensity.lean`
(file SHA-256
`1a1b9a929076ab77bf0e0f207f0d3d4fa25ac30dd56b2275e1fc319970f0f5e5`).
Its statement, lines 48–53, accepts only an arbitrary real finite precision
matrix A and `hA : A.PosDef`, and returns precisely the consumer's measure
equality with dimension n. There is no source-family-specific hypothesis,
extra covariance/density equation, arbitrary reference-measure parameter, or
hidden section assumption. The file's imports, namespace and open declarations
were checked for the interface context. The consumer specializes n to d and A
to the literal source precision.

The standard `multivariateGaussian μ S` definition maps the standard Gaussian
through `μ + CFC.sqrt S` as a Euclidean linear map. Its documented meaning is
mean μ and covariance S when S is PSD; if S is not PSD, the square-root
construction collapses to a Dirac fallback. This is why an `IsGaussian` result
alone would be insufficient. Here S is exactly A⁻¹. A narrowly inspected
existing-leaf proof line explicitly derives `A⁻¹.PosDef` from `hA.inv` before
using its square root. The leaf therefore uses genuine inverse-positive
covariance, excluding that fallback for the proposed application. This is an
inspection of an existing canonical dependency, not construction of a new
producer or consumer proof.

The old source-specific `GaussianLawDensity.gaussian_law_eq_density` was not
opened or reused. Its different literal block family and stronger local
endpoint conditions cannot serve as the cosine-family consumer. The generic
shared leaf above has exactly the needed arbitrary-precision meaning and
requires no new generic wrapper, transport theorem, or duplicate library node.

## Genuine producer use and remaining boundary

The proposed integration dependency is substantive: the new
`actual_precision_admissible` must supply A.PosDef for this same literal A;
that output supplies the canonical leaf's internal positivity input; the
shared leaf then gives the exact actual Test equality. A.PosDef must not be
added as a Test binder or obtained from an unrelated family/covariance/density
assumption. A Test that merely asserts `IsGaussian`, uses an unrelated A, or
bypasses the new producer would not satisfy the intended producer-consumer
integration check. This review accepts the exact statement and dependency
plan; only later inspection/compilation of the actual Test can certify that
the producer was genuinely consumed.

The sealed statement is type-only at this stage. I did not run a build, open
the typecheck receipt/log, inspect a new producer/Test proof, or claim compiled
consumer evidence. The reported type-only pass is not a mathematical proof.
The immutable pre-proof commit was reported by root; this role did not perform
a remote or repository-state audit of it.

This permits mathematical implementation of the already sealed producer and
the exact actual Test through the existing canonical leaf. Source-V and
post-proof fidelity gates remain separate. In particular it does not close
det A=det Λ, the known/public fixed-spectrum normalizer, the rest of C.4
calculus/minimizer assertions, target moments, Krylov/concentration arguments,
algorithmic/oracle/cost/TV transports, either main lower bound, publication,
purification, or the whole Goal. No prior frozen phase was changed.
