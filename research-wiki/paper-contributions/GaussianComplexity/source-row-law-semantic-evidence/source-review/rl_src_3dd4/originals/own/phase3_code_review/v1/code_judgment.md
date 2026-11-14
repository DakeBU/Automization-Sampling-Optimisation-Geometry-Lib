# Phase 3 v1: exact whole-module source review

Actor: `rl_src_3dd4`. This v1 judgment binds the seven exact code copies in input-manifest SHA-256 `6ceacfb15a34bbd29d668f4229fe5ede22dd3711b245309a21cb719890d7e01f`. The producer is 2505 bytes, SHA-256 `c370caf377c5d56c97bdb1012d407049e63b04998011df327de79c46fb2b1201`; the private consumer is 7366 bytes, SHA-256 `2ddc49ddc93f24b44e36b8c5dbf1c07b5af49511c16042adbf97bdf791786819`.

**No blocking source-fidelity or parent-applicability defect was found in these exact v1 code copies for the bounded original-product marginal/cutoff fragment.** This is a source/code review, not compilation or kernel certification. It does not grant sourceVERIFIED, permission, or Goal/publication completion. A notified consumer v2 edit has not been received or reviewed here; this v1 must not be attached as a review of v2.

The raw freeze `191a707abba9a252f26ee0b3da16ddd19aeefa30920e7270951e49ed4f8af055` and type freeze `3e0298cf25a3bf8c91dfa7f1f1a2c533ea2a64a26d9590fc656636f99a9903a1` remain unchanged. Both new declaration signatures were extracted from their complete modules and compared to the frozen packet after whitespace normalization; both match exactly.

## Whole-module context

The complete 54-line producer imports only the two supplied canonical Gaussian/product modules. Its scope consists of `noncomputable section`, standard opens, `autoImplicit false`, and the namespace. There are no scoped theorem variables or project hypothesis bundles. The theorem has only natural d,q and the source range hq. The complete 145-line consumer imports that producer, the canonical Gaussian exponential provider, and Markov. Its private theorem has the same hq-only interface and literal source experiment/event definitions. Standard ENNReal notation and namespace opens do not add assumptions. Neither module introduces an axiom, placeholder closure, fallback definition, or theorem-shaped input certificate.

The source standing q/d range, actual product probability law, coordinate orientation, r versus r² dimensions, and q=0 endpoint agree with the raw/type freezes. The producer remains a marginal theorem in the concrete product experiment; its doc comment explicitly leaves joint-row independence and other ambient experiments separate.

## Producer: actual column marginals to the physical row

The producer first uses the exact `map_pi_eq_stdGaussian` theorem to identify each d-dimensional standard Gaussian column with the Euclidean wrapper of d independent N(0,1) scalars. For a fixed actual physical coordinate i, `coordinate_law` (line 33) obtains the measurable scalar evaluation map and uses `Measure.map_map` and `measurePreserving_eval` to show its law is `gaussianReal 0 1`.

`collect_coordinates` (line 43) then applies the exact finite-product `measurePreserving_pi` theorem to this coordinate map in every column factor. It starts from μ, the source product of r independent standard d-Gaussian columns, and ends at the r-fold scalar standard Gaussian product. Its required target-factor sigma-finiteness is supplied by the canonical Gaussian probability measures, not a new source binder. `wrap_row` (line 48) uses the Euclidean r-coordinate wrapper and `map_pi_eq_stdGaussian`; composition yields exactly `row i`, the vector with coordinates ω a i. This proves both output measurability and the row pushforward equality. It does not assume the desired marginal law or derive joint row independence merely from marginals.

## Canonical exponential parent applicability

The complete 100-line `StdGaussianRadialExponential` provider was read. Its theorem requires a finite-dimensional real inner-product space with its Borel measurable structure, and concludes both genuine integrability of exp(||x||²/3) and its exact standard-Gaussian mean 3^(finrank/2). E is the canonical real Euclidean space on Fin(q+1), so all those structural requirements apply directly. The dimension rewrite makes the exponent ((q+1):R)/2, with real half-dimension, including q=0 and odd r; there is no natural-number division error.

The provider constructs integrability through finite nonnegative exponential mass, rather than relying on a totalized Bochner integral value alone. Its standard/variance-three density conversion and factor 3^(dimension/2) are consistent with the source mgf. Its imported established isotropic-density dependency was not newly audited transitively. The exact provider statement and proof were inspected for this application's requirements; no compiler or old audit receipt was opened.

## Both integrability and mean are transported noninjectively

The consumer materially calls the producer at line 46 and the canonical moment provider at line 49. `row_moment` (line 55) first obtains actual-row integrability with `(row_law i).integrable_comp_of_integrable`. The additional exact Mathlib `Function/L1Space/Integrable.lean` dependency was inspected and verified byte-identical to the declared Mathlib pin. Its theorem requires a measure-preserving map and target integrability, with no injectivity or measurable-embedding condition.

For the exact mean, the consumer separately builds `AEStronglyMeasurable` under `Measure.map (row i) μ` by rewriting the producer's map equality and using canonical integrability. It calls the general `integral_map` theorem with row aemeasurability and that target aestrong measurability. The supplied exact Bochner theorem has no embedding premise. Rewriting the map equality and canonical mean, then taking symmetry, yields the original-space row mean. This is valid for the generally noninjective row map. The code does not invoke the distinct embedding-only `MeasurePreserving.integral_comp` shortcut. Both producer output fields are used; integrability and the exact mean are produced internally rather than public assumptions.

## Markov, constants, simultaneous event, and closed complement

The numerical proof establishes log(3)<4/3 by splitting log(3)=2log(3/2)+log(4/3) and using log(x)≤x-1, strictly for 3/2. With r≥0 this yields log(3)*(r/2)≤2r/3. Therefore 3^(r/2)/exp(L/3)≤1/(1000d), with the exact L=2r+3log(1000d). Proving this direct cutoff ratio does not require taking a separately supplied x≥0 tail theorem as a premise.

`row_tail` (line 88) is applied on the original μ and same row map. It includes the strict event L<||row i ω||² in the nonstrict exponential-threshold event, applies the exact ENNReal Markov inequality with measurable weight and a finite positive threshold, and converts the lintegral using the separately proved actual-row integrability and nonnegativity. The resulting one-row bound is on μ(bad i), not on an unrelated auxiliary row measure.

`good_complement` (line 112) identifies the complement of the simultaneous closed condition with the union of the strict bad events. The v1 simp list explicitly contains `not_le`; this is the exact v1 code being reviewed. `bad_union_bound` uses finite subadditivity over Fin d, the transported row tails, and d/(1000d)=1/1000. No row-independence premise appears. The d positivity/nonzero facts follow from hq, so no empty-row vacuity or division-by-zero escape occurs.

`good_measurable` (line 129) explicitly derives each closed norm-square predicate from producer measurability and forms their finite intersection. `good_measure` then uses a measurable complement and the finite probability measure μ to obtain μ(good)=1-μ(goodᶜ). Canonical standard-Gaussian probability and finite-product probability instances were checked in the supplied exact background. The final ENNReal subtraction step gives exactly ofReal(999/1000)≤μ(good), preserving equality at L on the good side.

The implementation agrees with the raw-source attribution: Appendix C.2 p10 prints the all-good lower bound 0.999. The explicit strict-any-bad ≤0.001 calculation and its finite-union bridge are reconstructed proof bookkeeping supporting it. The source p1 additionally asserts joint row independence; this producer/consumer pair does not formalize that stronger assertion. Neither theorem is an arbitrary-external-space transport result or the full uniform-Krylov conclusion of Lemma 4.4.

## Review limits and next version

All seven input sizes/hashes were verified. Complete new target modules and the canonical exponential provider were read; only directly relevant sections of larger background files were displayed. The one additional direct integrability dependency, its exact displayed ranges, file hash, and match to the Mathlib pin are recorded separately. No compiler/kernel receipt, diagnostics, SG/TC judgment, graph, root proof history, decoder reconstruction, authored publication, ledger, or prior semantic verdict was opened.

This v1 has no identified blocking mathematical/source mismatch. Compilation, kernel/axiom evidence, later semantic-reconstruction comparison, source-publication attachment, and any v2 code remain unreviewed in this phase. Preserve this v1 evidence and require a separate exact whole-module binding for v2.
