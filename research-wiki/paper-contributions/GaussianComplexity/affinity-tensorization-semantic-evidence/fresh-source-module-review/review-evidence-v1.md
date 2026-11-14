# Independent Ex71 source, whole-module and static-reader review

The candidate is source-faithful after the explicit measure and representative elaborations. I found no blocking source, theorem, definition, proof, parent or static-reader discrepancy in the bounded target. This is an independent review result, with no repository lifecycle transition or canonical-audit edit.

Reviewer: `/root/ex71_fresh_source_module_review`, distinct from formalizer `huanjian_gc_20261107_ex71` and blind decoder `/root/decode_683204`.

## Independence and exact inputs

The raw HTML hash is `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`. My raw-source expectations were frozen as `0180f0190eaadce263df6799e9354e5bd5cbb1a60691aa38ff173e294ae7e43c` before seeing the seal, decoder, implementation or publication context.

I then opened only `source` and `blind_reconstruction` from the fresh packet and froze the seven-slot comparison as `ad347b270fa85d6a727361f81675b78567d8e6f13a82af1758d06f88b574f4e7`. Only after this second freeze did I inspect the candidate, actual parents and reader. No old fidelity review, other source/topology actor verdict, or root capsule conclusion was used. Candidate mathematical statements and claims were checked against the independently frozen raw expectations rather than accepted as evidence.

The packet raw hash is `1667083a35060d3432439711b3c68fa6d66352b3a82504c4594fb968977e2f38`. Its canonical hash was independently recomputed by removing `packet_sha256` and serializing sorted keys with UTF-8, `ensure_ascii=False`, and compact separators: `ca61048cb47a11d9f6cb941d8b4f3c56f56ef4d2c4ca52bdc11979d6687ed34a`.

The publication binding supplied in that packet is `9104d934f897b788965a51b8681eb96cf568a43d3a7b7dc5ed743ffe0469533d`. The packet module equals the actual module text; its module, toolchain, manifest, source text, reconstruction text and lesson fields were checked against the actual inputs. The actual lesson has one additional `boundary` field; the static page preserves the explicit remaining boundary. I did not read or change the canonical semantic audit. The review therefore does not claim that the original candidate commit's then-draft audit had already been independently accepted.

## Whole-module and definition review

Mathematical candidate commit: `4014feb9c6dff0b4e0dcb9fb49ae1b961cf3cf0b`.

The entire production module has three imports, one public theorem, no private helpers, no source-facing definitions of its own, no section variables, and `autoImplicit false`. The module hash is `e8dc0243da541be81bbf9b878c037bc4ec61caaf9d43c9a3b9c11b33ffef294c`; the entire focused Test module hash is `a8d50d319eca9e5854dcfb36b88596fc7c151570fd73433b64fb2a22551b4c40`.

I read and hashed sixteen complete candidate/Test/parent modules, including ProductDensity, MixtureDensities, AveragedBlockLaw, GaussianBlockLaw, GaussianMixtureLaws, GaussianLawDensity, DeterminantComponents, DeterminantFamily, BlockFamily, OrthogonalHaar, DensityAffinity, GaussianPrecisionDensity, IsotropicGaussianDensity and the project RadonNikodym leaves. Every listed file matches its bytes at the mathematical candidate commit; exact paths/hashes are in `module-input-manifest-v1.json`. Relevant Mathlib Gaussian, RN and product-integral definitions/statements were also inspected locally.

The public theorem's only logical premises are the source bounds `3 ≤ n`, `n ≤ d`, and `4 ≤ κ`, with natural d,n and real κ. No product-density identity, normalization, integrability, absolute-continuity, positivity estimate or positive-remainder condition is supplied as a public binder. The fixed Borel structure and Euclidean carriers are typing data. There is no hidden project `Prop` bundle in the theorem signature.

`orthogonalHaar` is the actual full-group Haar constructor normalized by the whole compact group, with existence and uniqueness proved. The sign priors are literally twice its restrictions, and component probabilities are proved for positive n, available from n≥3. `singleBlockPrecision` is exactly the source Eq4 formula. `blockPrecision` is the actual contiguous block-diagonal Eq5 construction, with residual identity and no fallback definition. Block regularity proves positive definiteness on the entire construction image. The actual Gaussian constructor is Mathlib's covariance-square-root pushforward. The Gaussian precision-density parent identifies that constructor with the literal normalized density under positive definiteness, so off-domain inverse/Gaussian totalizations do not affect the source law on the prior support.

MixtureDensities proves inner Haar integrability at every x using continuity on the compact orthogonal group, before identifying its Bochner average with the nonnegative integral. It proves actual bind identities, measurability, L1 and unit mass for both block densities. AveragedBlockLaw constructs the actual same-sign independent prior, proves measurable averaging and positive-definite support, and derives the genuine Eq6 product law from the conditional Gaussian product theorem. ProductDensity then derives the actual product and ambient density equalities. Thus the main theorem is not an identity for arbitrary stipulated normalized functions.

## RN, L1, volume and residual checks

At production lines 110–117, both RN derivatives are identified a.e. with `ofReal` of the actual Ex70 ambient density. The required measurable densities and sigma-finite canonical Euclidean volume are present. Since those values are finite and nonnegative, lines 119–122 use `toReal_ofReal` a.e. to identify F with the actual square-root product. No pointwise equality of arbitrary RN representatives, or everywhere-finiteness assertion, is inferred. Null-set changes cannot change the affinity integral. Both absolute-continuity conclusions are derived from actual withDensity law equalities.

At lines 123–125, the shared normalized-density theorem supplies genuine L1 of the split affinity using actual Ex70 density hypotheses. At line 171 that L1 property is pulled back by the actual measure-preserving split, then transferred across the a.e. RN identity. The theorem therefore concludes genuine ambient integrability rather than exploiting the default value of a nonintegrable real integral. The actual single-block densities also satisfy the normalized-density hypotheses, so the scalar a has the intended finite block-affinity meaning.

ProductDensity's split proof composes measurable coordinate equivalences, Euclidean/coordinate volume identifications, sum splitting and a unit-cube-normalized additive-Haar argument for currying. It does not identify the Euclidean norm with a Pi maximum norm. The source R^d ambient volume and the product reference measure are actually connected; this is not only dimension counting.

The common residual formula is nonnegative in every residual dimension. Lines 142–153 derive its unit mass from the actual Ex70 total mass one and the positive block-product mass one. This is a valid dependency route, distinct from the source's direct invocation of Gaussian normalization. It does not add a normalization premise or use a scalar affinity bound. The root factorization at lines 154–163 uses nonnegative block densities and the common nonnegative residual factor.

Both source parameter cases are covered uniformly. Under 3≤n≤d, k=d/n and r=d%n are the source floor quotient and nonnegative residual. ProductDensity proves the literal residual formula equals one at r=0 and obtains its law from the standard Gaussian density theorem valid in dimension zero. The main proof derives residual mass one for all r, including zero. There is no r>0 branch guard and no artificial kn>d source case. The final finite-product integral has exactly k copies of the same block affinity, with residual factor one and no constant loss.

## Real compiler and consumer evidence

Independent fresh commands, all exit zero:

- `lake env lean AutoSamplingTheory/ExampleCases/GaussianComplexity/AffinityTensorization.lean`
- `lake env lean Tests/GaussianComplexityAffinityTensorization.lean`
- `lake env lean AutoSamplingTheory/ExampleCases/GaussianComplexity/ProductDensity.lean`
- `lake env lean AutoSamplingTheory/ExampleCases/GaussianComplexity/MixtureDensities.lean`
- `lake env lean .astis/ex71-independent-source-module-review/AnonymousEquivalent.lean`

These are direct source elaborations; imported dependency oleans were reused. They are not described as Lake cache-replay builds or full-root checks. Each command has its own log, elapsed time, input hash and receipt. The final scratch command compiles the packet's fully expanded signature as a proposition discharged by the actual public theorem, checking definitional equivalence to the supplied anonymous statement. Its only warnings concern unused binder names in that verification example.

Recursive axiom output for the target, ProductDensity, MixtureDensities and DensityAffinity is exactly `[propext, Classical.choice, Quot.sound]`. The comment-stripped source scan of all sixteen reviewed modules found no fake-closure or unsafe/native escape token. This supplements rather than replaces the recursive axiom check.

The actual Test consumer bounds the ambient integral of the RN-affinity of the actual Gaussian binds for every source d,n,κ. It substitutes the new exact equality and then applies the pre-existing single-block Eq25 bound. Its result is therefore an actual-law exponential-decay statement, not only an inequality for a scalar power. The compiled direct target-parent list contains ProductDensity, MixtureDensities, DensityAffinity, OrthogonalHaar and the literal precision definitions. Eq25 is not a parent of tensorization itself.

## Candidate static reader

I inspected the actual task-local generated lesson at `.astis/huanjian-ex71-20261107/reader-preview/lessons/module-autosamplingtheory-examplecases-gaussiancomplexity-affinitytensorization.html`, hash `60b014347938fe6f63feb3d470baa7ffefcfcfffc595197083bc1594e051fed3`.

The main formula appears first; the full hypotheses and objects are folded but present. All five mathematical proof steps are present, with correct formulas and corresponding Lean explanations. The exact statement is adjacent in an initially closed disclosure. The initially closed proof disclosure reproduces the exact theorem source through its namespace-end line. An initial mechanical comparison omitted that end line and was corrected before the final record; no actual proof-body discrepancy was found.

The complete module source page is linked at a valid anchor and contains the entire exact module including imports and namespace. The downloadable `.lean` bytes equal the production hash e8dc0243… . All reviewed local parent/module/download links and their fragments exist. The external source link reaches the pinned arXiv version and Ex71 anchor. The generated search index has the target declaration and module entries with existing destinations and anchors. The actual lesson fields equal the packet lesson fields, with the additional explicit remaining-boundary field preserved.

No static content or disclosure defect was found. MathJax assets are local in this preview, but I did not run a browser or inspect rendered geometry. The page appropriately says the current source-state Lean gate is not recorded; its old root catalog does not establish new root integration. This review is not final browser, canonical root/site, remote publication, merge, purification, Exposition Seal or whole-Goal acceptance.

## Verdict and remaining boundary

All seven semantic slots preserve the raw source expectation. The source density integral is represented by actual-law RN derivatives after an explicit a.e. finite-density identification, and Lean additionally concludes AC and genuine L1. The verdict is `equivalent-after-elaboration`; no blocking delta or repair is proposed.

Accepted review scope is the exact Ex71 source target, whole current module and stated source-critical parents, actual focused compilation/consumer, and candidate static reader explanation. Ex72 TV amplification, query/oracle lower bounds, global integration, public delivery and postmerge lifecycle remain separate. No shared ledger, frontier, Registry, root import, source audit or lifecycle field was changed by this reviewer.
