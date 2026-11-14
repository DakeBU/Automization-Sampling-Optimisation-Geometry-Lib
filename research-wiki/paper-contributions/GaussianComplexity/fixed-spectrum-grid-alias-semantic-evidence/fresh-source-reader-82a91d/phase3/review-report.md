# Phase 3: immutable whole-module, static reader, and fresh runtime review

Reviewer: `source_reader_82a91d`. Candidate: `cbf3c22b901a484c463f417a3e206bb200622294`.

The producer source semantics and the supplied complete production/Test proofs pass this review at the stated narrow boundary. Both exact actual theorem types match the sealed anonymous signatures, both recompiled successfully into an owned overlay, and their recursive axiom closures contain only `propext`, `Classical.choice`, and `Quot.sound`. The private consumer genuinely depends on both canonical public producers. Static reader acceptance is withheld for issue **P3-R1**: its consumer explanation does not define its newly introduced spectral data and does not explicitly state the integer domain of the new mode `n`. There is no proposed source repair and no mathematical theorem mismatch. No V/status API call, integration, rendered-site/UI, browser, remote, or Goal acceptance was performed.

## Exact reviewed inputs and anti-anchoring

The phase 1 and phase 2 freezes preceded candidate disclosure and remain unchanged. Phase 3 read exactly the delivered manifest and its seven delivered files: the fresh canonical anti-anchored reviewer packet, whole current production module, whole current private Test, current authored lesson, current publication, `lean-toolchain`, and `lake-manifest.json`. All delivered file bytes were verified against their manifest hashes and actual current source paths. The phase 3 manifest raw SHA-256 is `843145acf5eeb85913e581e977e5cc303e36d3973e70163acadb990d10cc869a`.

The canonical packet's raw file hash is `5272486412cbdd9412478324e8fe39c954b9f5061b91da37e80c3ce026995eb9`; its canonical payload hash, independently recomputed after excluding the `packet_sha256` field using sorted compact UTF-8 JSON, is `e8cacf92f2d511b273fc78eb30e7da6126f673ff6fcc553b569881a206b0cbfc`. It declares publication binding `61592fe8185d0b422b28796db4901756b74affca24e557096ab6a818c4f78a43`. Its module, source, attributed statement, formulas, assumptions, obligations, and all included lesson fields match the delivered current inputs exactly. The current lesson additionally contains `boundary`; that complete boundary was independently read from the separately bound current lesson rather than inferred from the packet.

Current producer: 3,617 bytes, SHA-256 `c98c899bd8b596388ae433e9241a7827e01d29c3ffcc945719238fa2e96f7d60`.

Current private Test: 6,912 bytes, SHA-256 `9f3b9e64dced3467dbd163fde7918c376571d766bcebf7f7e25717b87de5d128`.

Current authored lesson SHA-256: `f35d1ed10277f2a58dfdd47d4cfe55df43ac98573537723ab7fc1ddc2b549d10`.

Current publication SHA-256: `596bfcc1eef259d609c58a8a4bfa86439e19bd4a76465898dbbe54e612db20d6`.

No prior source judgment, repair, semantic graph, or root proof/gate verdict was opened. The packet's `compiled` flag and dependency claims were treated as claims to verify. Kernel runtime inspection of actual imported constants and generated local proof constants was performed separately. The earlier phase 1 filename-only exposure and its unavailable truncated-output hash remain disclosed; no zero-cue claim is made.

## Whole-module and binder/definition audit

The production module imports six Mathlib modules, opens only `BigOperators`, enters the stated namespace, and authors exactly one public theorem, `actual_midpoint_grid_cosine_alias`. It has no scoped `variable` declarations, project-owned typeclasses, public helper definitions, local axioms, or other authored declarations. Its only logical premise is `2<=d`; `d:N` is carrier information, this bound is the source standing dimension input, and `k:Z` is the unrestricted source frequency. The local `theta` is the literal grid, not an assumed or chosen object. Integer divisibility/quotient and the integer power of real `-1` have their standard meanings. The false conditional branch is the literal source zero coefficient, not an off-source existence fallback.

The current Test imports the alias module and the canonical cosine-expansion module and authors exactly one private theorem. It has no scoped variables or extra source-facing definitions. Its only premises are the source dimension/parameter/mode bounds: `d>=2`, real `kappa>=2`, and natural `n` with `1<=n<d`. This natural mode represents precisely the source's positive integer mode. Its `theta`, eigenvalue, `r`, alias coefficient, and proof functions `w,f,g,G,F` are literal local definitions. All shifts are formed after casting positive series modes and `n` to integers; natural subtraction is never used for the negative shifted modes. Eigenvalue positivity, nonzero dimension/square root, vanishing base mode, summability, and finite/infinite exchange are derived in the proof. They do not appear as added theorem binders.

The actual imported C7 type was independently printed from the Lean environment. It fixes real `kappa>=2` and literal `r`, provides the inverse-spectrum identity for every real angle, provides summability of the norms of the positive cosine modes, and provides uniform convergence of their partial sums. This matches the frozen source C7 normalization and convergence requirements used by this consumer. I did not open a previous C7 review or its source implementation; the existing C7 compiled cache was reused and its actual type/recursive proof axiom dependencies were checked at runtime.

Both target source files were lexically scanned for fake closure tokens. They contain no `sorry`, `admit`, authored `axiom`, `unsafe`, `native_decide`, `Prop := True`, or `:= trivial` closure. More substantively, the recursive actual proof/type traversal found no `sorryAx` or axiom beyond the ordinary three listed above.

## Production proof: actual mathematical route

The source all-integer identity remains mathematically equivalent after the `Fin d` relabeling. The complete implementation discharges both cases:

- On `2d|k`, the exact integer quotient `q=k/(2d)` yields `k=2dq`. Each zero-based grid angle is `q*pi + (q*i)*(2*pi)`. Integer periodicity and `cos(q*pi)=(-1)^q` give identical summands, including zero and negative aliases; the finite constant sum gives `d*(-1)^q`.
- Off divisibility, the proof establishes `sin(k*pi/(2d))!=0` internally: a zero would give an integer multiple of `pi`, which casts back to a forbidden divisibility witness. The finite grid is transported to a range sum. `Real.sin_mul_sum_cos` gives the multiplied midpoint identity, and the double-angle identity plus integer `sin(k*pi)=0` annihilates its right side. The internally established nonzero sine then forces the sum to vanish.

This uses the same finite trigonometric sum mathematics as the raw source. It is exact for every integer mode. No denominator premise, frequency cap, sign/parity restriction, probability law, spectral parameter, or asymptotic approximation has been inserted. The source dimension anchor `S4.SS1.p1.m3` was checked against the frozen exact math snippets and is literally `d>=2`.

## Private consumer: actual use and normalization

The consumer's final literal type is definitionally equal to the phase 2 sealed anonymous type. Its proof actually obtains `heq` and absolute convergence `habs` from canonical C7 at every actual grid point. It weights by `w_i=cos(n*theta_i)`, uses `|w_i|<=1` to preserve norm summability, sums over the finite grid to obtain summability of `G`, and justifies the actual `Summable.tsum_finsetSum` exchange.

The actual alias theorem is materialized as `hcos` for every integer frequency. It is used at `n` to remove the base grid term and at both integer shifted frequencies in `hprod`. The mode bounds prove `2d` does not divide `n`; this is not assumed separately. Product-to-sum proves the pointwise `2G_j=dF_j` relation. Nonzero dimension transports summability from `G` to `F` by `F=(2/d)G`; summing the relation yields `2*tsum(G)=d*tsum(F)`.

The literal eigenvalue is normalized internally to C7's reciprocal: `2*lambda_i=kappa+1+(kappa-1)cos(theta_i)`. Its positive lower bound follows from `kappa>=2` and `cos>=-1`. This supplies the reciprocal rewrite without an extra public denominator assumption. Combining the weighted reciprocal expansion, the convergent exchange, base-mode vanishing, and `2G=dF` gives exactly the prefactor `d/sqrt(kappa)` and both shifted alias modes. The factor 2 from C7 cancels the product-to-sum factor, as required by raw `A3.Ex144`.

This proves a deterministic weighted reciprocal-grid alias series and its summability. It does not identify a Gaussian expectation, partition the three alias classes, sum their tails into the C8 closed forms, bound variances/biases, or prove either main lower bound. That boundary agrees with the current source metadata and authored boundary.

## Fresh runtime and actual dependency evidence

All commands, start/end times, exact argument vectors, candidate HEAD before/after, exit codes, environment override, and complete stdout/stderr bytes and SHA-256 hashes are retained under `runtime/`. The pinned Lean is 4.33.0, executable `/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean`, compiler commit `d8b18978322de05a8f3dba51ef03cf5461676c17`. Mathlib HEAD `db584cd6d46c92f209a44c0f1c829460d327499d` matches the pinned manifest. The tracked tree was clean before review.

`06-fresh-producer` compiled the actual current production source to an owned overlay `.olean`, exit 0. `07c-fresh-private-consumer` compiled the actual current Test to an owned overlay `.olean`, exit 0. The Test's import-resolution check independently prints the overlay producer path, establishing fresh producer-to-Test provenance. The imported C7 cache was reused with its byte hash recorded; C7 and Mathlib were not claimed to be rebuilt from source in this review.

Two mechanical failed attempts are preserved, without unchanged repeats:

1. `07-fresh-private-consumer`, exit 1: Lean selected the overlay namespace but its C7 cache was not present there. This was `ENV_BLOCKED`, not a mathematical failure. The changed environment exposes the existing hashed C7 `.olean`/`.ilean` in the same overlay while retaining the fresh alias object.
2. `07b-fresh-private-consumer`, exit 1: my first retry selected the probe runner's owned-relative path instead of the actual Test path. This was a reviewer harness invocation error, not a source/compiler theorem failure. The changed `consumer` stage invokes the actual absolute Test source and emits its owned object; `07c` passed.

`08-kernel-dependency-literal-audit`, exit 0, imports the freshly built private Test. It compares both actual kernel types to independent literal proposition definitions copied from the phase 2 sealed statements using definitional equality. Both comparisons succeed. The independently written recursion traverses actual constant types and theorem/definition/opaque bodies. Producer closure: 16,235 constants; consumer closure: 17,555 constants. Each has exactly the actual axiom set `[propext, Classical.choice, Quot.sound]`. A separate standard `#print axioms` confirms the producer set, and `09-actual-C7-parent-type` confirms the C7 set. Warnings concern unused binder names inside the probe's literal proposition definitions, not target compilation.

The producer's public ASTIS frontier after expanding compiler-generated auxiliaries is empty. The consumer's is exactly:

- `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias.actual_midpoint_grid_cosine_alias`;
- `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion.actual_inverse_spectrum_cosine_expansion`.

The compiler generated one producer auxiliary and three private consumer auxiliaries. Their actual complete types, bodies, and direct constants were printed and inspected. They are checked Omega arithmetic contradictions for nonzero dimension, positive casted `n`, and incompatibility of `n<d` with `2d<=n`. They are not additional canonical public theorems. Their captured unused dimensions/modes do not add inputs to the source-facing interfaces. No parent was silently ignored because it was generated.

## Static authored reader/publication review

The primary source statement, formula, four assumption paragraphs, and `S_d(k)` notation are correct and complete for the alias theorem. They preserve the actual finite grid, dimension, unrestricted integer frequency, exact quotient, parity at negative aliases, and lack of excess public assumptions. The public theorem's `astis_dependencies: []` is correct, and its listed Mathlib leaves agree with actual code. The extra consumer dependency statements inside the proof steps are also true, including the claim about exactly two canonical public ASTIS parents after auxiliary expansion.

All five authored proof steps were checked:

1. The multiplied finite midpoint formula is correct for every integer `k`, including the alias case where the multiplier vanishes. Its right side is exactly one half of `sin(k*pi)`. The described Lean route matches the actual range transport and double-angle proof.
2. The nonalias denominator argument is mathematically correct, remains inside the proof, and agrees with the actual sine-zero/divisibility conversion.
3. The signed alias branch's zero-based angle identity, integer cosine parity, and summation are correct for positive, zero, and negative alias quotients.
4. The weighted C7 expansion, absolute-summability preservation, reciprocal normalization, and finite/infinite exchange are mathematically correct and actually implemented. However its introduced `lambda_i` and `r` are not defined in the authored lesson, and the new mode `n` is not explicitly declared integer.
5. The vanishing base mode, both shifted integer frequencies, normalization, produced summability, and final prefactor are correct. It inherits the missing definitions/domain from step 4 rather than supplying them.

**P3-R1 — authored consumer notation/domain incomplete.** Step 4 says “with the literal source lambda_i and r,” but neither their spectral formula nor the formula for `r` appears anywhere in the delivered lesson's statement, assumptions, notation, or proof steps. Its new `n` appears only through `1<=n<d`; the integer domain needed for applying the all-integer alias theorem is implicit. A reader should be able to expand this local intermediate without opening an agent packet or guessing a source convention. The source already supplies the precise definitions and domain, so this is an exposition correction, not a theorem repair or an additional assumption. A sufficient correction is to state real `kappa>=2`, integer/natural positive `n` with `1<=n<d`, display `lambda_i=(kappa+1)/2+((kappa-1)/2)cos(theta_i)`, and display `r=(sqrt(kappa)-1)/(sqrt(kappa)+1)` adjacent to the consumer explanation. This issue withholds complete static reader acceptance of the present lesson; it does not invalidate the correct alias theorem or compiled consumer.

The publication's two producer obligations and binding scope match the actual public theorem. Its assumption descriptions and current boundary are mathematically correct. The source attribution/version/hash/anchors and deterministic-intermediate restriction agree with the frozen raw source slice; the unrelated full-paper boundaries are not inferred as completed. Exact rendered folded-Lean layout, adjacency in generated HTML, UI/mobile behavior, graph delivery, remote integration, aggregate gates, and purification/Exposition Seal were not inspected or accepted by this static review.

## Semantic verdict and remaining acceptance

All seven producer semantic slots retain the phase 2 decision, now supported by whole-module and actual-type evidence: objects, domains, quantifiers, assumptions, conclusions, scopes/senses, and constant dependencies are equivalent after finite-index/divisibility elaboration. The private consumer likewise preserves all seven slots at its narrower deterministic intermediate scope. There are no source-repair proposals or blocking theorem deltas.

At this exact immutable candidate: **source-statement fidelity accepted; whole-module proof/binder and fresh runtime checks accepted; static reader completeness not yet accepted because of P3-R1.** Any changed lesson/publication context requires a fresh exact binding and bounded independent re-review; this review must not be replayed as acceptance of changed authored text. No source VERIFIED transition or whole-Goal credit is supplied by this report.
