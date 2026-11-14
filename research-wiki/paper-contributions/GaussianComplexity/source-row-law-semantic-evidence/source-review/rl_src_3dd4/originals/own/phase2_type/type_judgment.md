# Phase 2: exact types and canonical definitions only

Actor: `rl_src_3dd4`. This phase follows, and does not modify, raw freeze SHA-256 `191a707abba9a252f26ee0b3da16ddd19aeefa30920e7270951e49ed4f8af055`.

Input: `selective-type-definition-packet.json`, SHA-256 `71806be7febb91c6ea9a847ce022065cec7eebf6b224503663fcbb7921bc5353`, 9976 bytes. The supplied exact producer signature has SHA-256 `82e3c608d456b2d190e50a7426aa5cb0c3f5a9c622906c7cb02cfe86cf3caf38`; the consumer signature has SHA-256 `93587ca60509760c39e7cfc60b71ec7fbc9059fd3cb98b1ec0c6b4da5e7d7c31`. These were recomputed and match. Embedded canonical-print and literal product-definition excerpt hashes also match. Referenced receipt paths, Mathlib implementation paths, and planned target modules were not opened.

The type-only judgment is **consistent with the frozen raw-source meaning for the explicitly concrete product experiment and bounded marginal/cutoff fragment**. No blocking type or literal-definition mismatch was found. This is not proof acceptance, independent source verification of compiled code, or permission to publish/close the source result.

## Objects and original probability experiment

`D := EuclideanSpace ℝ (Fin d)` is the d-coordinate standard real Euclidean space. `E := EuclideanSpace ℝ (Fin (q+1))` has exactly r=q+1 real Euclidean coordinates. `Ω := Fin (q+1) → D` is a tuple of r column vectors, and `μ := Measure.pi (fun _ => stdGaussian D)` is the finite product of their actual standard d-Gaussian laws. The literal finite-product excerpts supplied in the packet resolve the otherwise opaque print of `Measure.pi`. The source independent-column experiment is therefore built into μ, rather than assumed through a project-owned proposition bundle.

The standard Gaussian definition is the canonical centered identity-covariance Euclidean law assembled from independent `gaussianReal 0 1` coefficients in an orthonormal basis. Its use on D and E preserves the source Gaussian normalization. No `stdGaussian Ω`, alternate row-only sampling law, normalized restriction, conditional law, or independently resampled law replaces μ.

A canonical product realization is a valid concrete distributional realization of the source independent-column experiment. The declared theorem has no variable arbitrary probability space, no arbitrary random column maps, and no transport of an arbitrary extension/coupling. Therefore its direct formal scope is this concrete Ω and μ. Source correspondence may state that concrete experiment; it must not promote this signature alone to an arbitrary-external-space transport theorem.

## Literal physical rows and norm

For a physical index `i : Fin d`, `row i ω := WithLp.toLp 2 (fun a : Fin (q+1) => ω a i)` takes coordinate i from each of the r columns of the same outcome ω. The a-th row coordinate is the source `(g_a)_i`; the packet's one-based source interpretation is a.val+1 and i.val+1. There is no coordinate swap.

`WithLp.toLp 2` is the Euclidean wrapper of that literal r-coordinate function. The supplied Euclidean norm-square identity identifies `‖row i ω‖^2` with the sum over a of `(ω a i)^2`. It is not a d-dimensional column norm, an r²-dimensional tensor/B-row norm, or a coefficient-vector norm. All meaningful target-local definitions are literal lets; none chooses a representative or supplies fallback semantics.

## Producer quantifiers and both output fields

The only explicit logical premise is `hq : 2*q+1<d`, on natural d and q. After the literal lets, the conclusion is `∀ i : Fin d, MeasurePreserving (row i) μ (stdGaussian E)`.

The supplied structure expansion makes both fields conclusions:

1. `Measurable (row i)`;
2. `Measure.map (row i) μ = stdGaussian E`.

Thus neither measurability nor the row-law equality is smuggled in as a hypothesis. The producer establishes a marginal pushforward law for every actual physical row of the same original experiment. It does not state mutual independence of all row maps, joint row-law equality, almost-sure equality between a row and a separately sampled Gaussian, or a transport theorem on an arbitrary extension. The source p1 joint-independence sentence is stronger and remains outside this producer's conclusion.

## Consumer event, probability threshold, and endpoints

The consumer repeats exactly the same D, E, Ω, μ and row definitions. The real r is the explicit cast of q+1, and

    L = 2r + 3 Real.log(1000*d),
    good = {ω | ∀ i : Fin d, ‖row i ω‖² ≤ L}.

Every conjunct uses the same ω. This is the original simultaneous all-good event, with exactly d physical row indices and the source closed inequality. Its complement is the strict any-bad event `∃ i, L < ‖row i ω‖²`; replacing the bad event by a nonstrict inequality would change the literal endpoint. The type contains neither a supplied tail estimate nor a supplied union bound or good-event premise.

`ENNReal.ofReal (999/1000 : ℝ) ≤ μ good` has the correct lower-bound direction. The numerator and denominator are real numerals, so the rational is exact and positive; `ofReal` embeds 0.999 without a probability renormalization. Canonical Gaussian factors and their finite product are probability measures as described by the supplied standard instances. The source all-good lower bound is printed; any-bad ≤1/1000 and the finite-union bridge are inferred proof steps and must keep that attribution.

The literal event is measurable in the standard product/Euclidean setting: row measurability, the norm-square predicate, and a finite conjunction supply this source-event interpretation. Actual use or derivation of these facts remains to be checked in whole code; the type-only phase has not inspected a proof that μ is used as a probability or a proof of event measurability. No extra measurability hypothesis is needed on the public statement.

## Assumptions, constants, and q=0

Natural d and q are source typing. `hq` is the explicit source range and prevents empty-physical-row vacuity: it implies d≥2. The signature includes q=0, where E has one coordinate, Ω has one standard d-Gaussian column, the row is one-dimensional, and L=2+3log(1000d). It does not impose q>0, r>1, or a nonempty positive-frequency list.

The exact constants are 2, 3, 1000 and 999/1000. κ, n, θ_i, the larger source lemma's absolute C, and τ_{d,q}≤1/2 do not enter the row marginal or cutoff; their absence is faithful to this bounded fragment. The source's q/d standing range is retained even though Gaussian marginal/tail facts can have a larger general domain. No additional public mathematical premise appears in either supplied signature.

## Explicit remaining boundaries

- The packet contains no new target implementation or compiled proof certificate. Compilation, axiom cleanliness, actual producer use, internal strict-tail derivation, finite union, complement arithmetic, and whole-module assumptions are unreviewed.
- Canonical definitions/prints were supplied inside this selective packet. Their provenance hashes were checked internally; referenced provider code and receipt files were not opened or independently certified.
- Neither signature directly supplies arbitrary-external-space transport or the source p1 joint-row independence assertion.
- The all-good consumer's label and planned test location do not establish its actual visibility or production/publication role. That belongs to the later whole-code/publication review.
- A complete Lemma 4.4 conclusion, source graph/topology acceptance, semantic round trip, and Goal/source completion remain outside this judgment.

Stop after this type-only freeze. The whole-code and anonymous-reconstruction packets remain separate future inputs.
