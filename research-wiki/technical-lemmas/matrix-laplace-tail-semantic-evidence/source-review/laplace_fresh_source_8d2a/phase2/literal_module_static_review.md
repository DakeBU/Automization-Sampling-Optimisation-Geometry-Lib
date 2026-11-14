# Phase 2 literal source, whole-module, and static reader review

Reviewer `/root/laplace_fresh_source_8d2a`; independent of formalizer and source-blind decoder. Phase 1 remains frozen at SHA-256 `1cc889e64d01c49ce933844b358a32c267b59d5f99f7c254dbe1197960888cf4`. This phase was completed before reading either canonical reviewer packet, any decoder reconstruction, or another source/native verdict. This report is the reviewer's own comparison against its frozen raw-source reconstruction. It is not the later canonical packet-bound round trip and makes no compilation, browser-pixel, production publication, global graph, purification, or whole-Goal acceptance claim.

## Inputs and identity

The supplied mathematical commit identity is `1d1103af694b9663a72b0d610004ed85c7c6b527`. No Git command was run to resolve it. Literal current files and frozen preview source copies agree byte-for-byte:

- P: `AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean`, SHA-256 `4924fede99548f6aab4f63605d2beed9dc435d6338a61d89ee301d9e83733749`, all 96 lines.
- T: `Tests/GaussianComplexityLaplaceTail.lean`, SHA-256 `9ecf723f0487ddf50cb1d7c3102ebc04b58c472e56d2b16b186d91bc91cc6aac`, all 193 lines.
- Candidate lesson: SHA-256 `c8d5487ad57b389325ca9c21e694493df6ae83d21c0f4db6074840ae634eb2e3`.
- Candidate publication: SHA-256 `081e58993166fbe4c7aa78549bd4299c325cbd9849488b9b32abb380355518ac`.
- Candidate context file `publication-context.authored-v2.original.json`: SHA-256 `1b36e133f1d86cc35b656d4ef5dcef322beb238978a592292405816603a6f481`; its stored binding is the requested `d38d9501aa243dd110c5bb7958f2a86869fa6ec54b5a373b7d2928df84f3afe8`. Its complete P module text and all shared lesson fields match the actual candidate. The context lesson omits the current lesson's top-level `boundary` key; that boundary was separately read, snapshotted, and reviewed here. I did not independently reproduce the tool's canonical binding-digest algorithm.

All inspected mathematical and reader inputs are in `input_manifest.json`. Independent hash/HTML/span checks are in `static_checks.json`; they do not inherit the preview author's assertions.

## P seven-slot comparison

| Slot | Literal candidate meaning | Comparison with the phase1 source meaning |
|---|---|---|
| Objects | X is an AE strongly measurable Ω→Mat_ι(ℝ), AE Hermitian; μ is a probability measure; ι is finite and nonempty. | Correct disclosed real specialization of the source's finite square complex self-adjoint matrix setting. It is not a formalization of the full complex carrier. |
| Domains | t ranges over ℝ; the infimum ranges over the subtype of positive real s; measure and RHS use nonnegative extended reals. | Threshold/parameter domains match. Extended scalar expectation is a mathematical domain completion, publicly disclosed; the original source does not define ENNReal. |
| Quantifiers | Every X satisfying the stated AE assumptions, every real t, all s>0 through iInf. | No threshold positivity, minimizer existence, independent-family condition, or fixed special s is inserted. |
| Assumptions | MeasurableSpace Ω, probability μ, finite nonempty index with decidable equality, hX and AE Hermiticity. | Carrier/decidability fields are typing. Probability, measurability and AE self-adjointness expand the source's random-matrix/regularity conventions. No centering, norm cap, variance, finite-moment, or tail conclusion premise is smuggled in. |
| Conclusion | μ{t≤sSup(spectrum ℝ X)}≤inf_{s>0} ofReal(exp(-st)) times lintegral of ofReal(trace(exp(sX))). | Correct one-sided algebraic largest-eigenvalue bridge on the AE Hermitian domain, with unnormalized trace. No operator norm or dimension factor replaces it. |
| Scopes/senses | Standard matrix-algebra exponential, ordinary trace, finite nonempty real spectral supremum; nonnegative scalar integral of ofReal(trace). | Correct meanings on the source domain. The standard total spectral expression away from Hermiticity affects only a null exceptional set; the proof uses AE event comparison and does not assert a largest-eigenvalue meaning for general non-Hermitian matrices. The completion is scalar, not an extended matrix-valued Bochner MGF. |
| Constants/dependencies | No additional numerical constant or dimension prefactor; real exp(-st) is finite and strictly positive. | Matches the source bridge. Infinite scalar expectations are legitimate; there is no zero-times-infinity issue. Public P has no ASTIS mathematical parent. |

P's two private helpers implement standard spectral functional calculus/trace facts; they do not change the public statement. The implementation applies Markov directly to the trace observable after the pointwise exponential comparison, while Tropp first applies Markov to exp(λmax) and then dominates its expectation by the trace expectation. This is a legitimate elementary rearrangement of the same source argument, disclosed in the lesson, not a new public assumption or a claim that the source uses ENNReal.

P is acceptable within the explicitly disclosed real specialization and scalar-domain completion. It must not be labelled literal equality with the original complex Proposition3.1, nor source proof of a complete Bernstein theorem. The current prose makes both boundaries visible. The publication's first assumption delta uses `same`; its explanatory reason says `Explicit real specialization`. Thus `same` can be read only within the advertised real scope, not as equality of the original complex and real carriers.

## T seven-slot comparison

| Slot | Literal candidate meaning | Comparison with original Gaussian C.2 |
|---|---|---|
| Objects | d,q natural with 2q+1<d; r=q+1 independent d-dimensional standard Gaussians in the original product law; literal own-row Y, unconditional mean, Z, two weights and two global signs. | These are exactly the two actual C.2 centered sequences and their four signed sums reconstructed before exposure. The theorem is an authored private intermediate application, not a numbered theorem printed in C.2. |
| Domains | Ω=(ℝ^d)^r, μ=product stdGaussian; matrices indexed by Fin(r)×Fin(r), hence r²×r². Fin d encodes physical row i by i.val+1. | Correct index order (Gaussian coordinate first, feature coordinate second), normalization 1/d, midpoint angles and source dimensions. q=0 remains included. |
| Quantifiers | For every s>0, every real a, and every useCos/minus Boolean choice, the fixed-parameter one-sided tail estimate holds. | All four choices are covered without equality of the laws of S and -S. It asserts no operator-norm union conclusion. |
| Assumptions | Only the source dimension condition hq is a mathematical input; law, threshold L, features, row, cutoff, mean, weights, signs and sums are literal lets. | No row-law, matrix-integrability, mean, boundedness, structure, trace-positivity or tail-bound certificate is promoted to a new binder. No κ is needed by these cosine/Gaussian objects. |
| Conclusion | For each literal S=εΣ_iw_iZ_i, μ{λmax(S)≥a}≤ofReal(exp(-sa)·E_μ tr exp(sS)), with an ordinary finite Bochner scalar expectation. | Correct fixed-parameter precursor to the eventual two-sided C.2 tail argument. Both signs are present, but strict-norm conversion, union bound, independent-sum MGF and Bernstein remain separate. |
| Scopes/senses | The indicator uses ||row_i||²≤L, including equality; mean is the integral under unchanged μ; cosine weighting is deterministic and global sign is deterministic. | No conditional law on the all-rows event, cross-row cutoff, wrong transpose/Kronecker order, fallback mean, entrywise exponential, or trace-normalization drift. The real integral is not merely a default for a nonintegrable expression: integrability is proved internally. |
| Constants/dependencies | L=2r+3log(1000d), ρ=2r(L+1)/d, ||S||≤dρ; actual exp and trace integrability follow before applying P. | These are the original radius consequences used to discharge finite-expectation side conditions. This is not a Bernstein variance estimate or optimized MGF cap. |

The direct structure parent is invoked for measurability and Hermiticity; independence, integrability and zero mean in its package are explicitly discarded by this probability reduction. The direct radius parent supplies the actual Y and actual-mean norm bounds. The necessary mean-parent definition and conclusion prove Y integrable and identify its unconditional expectation. Therefore the use of mean=∫Y is meaningful and is not a circular assumption that a convenient mean exists.

## Whole-module inventory and semantic audit

Every declaration in the two complete files was inspected, including imports, scopes, universes, namespace, local instance setup and complete bodies.

- P private `trace_exp_eq_sum`: ordinary spectral trace identity for real Hermitian matrices and every real s. Used by the next helper.
- P private `exp_max_eigenvalue_le_trace_exp`: the exponential of one actual maximal eigenvalue is a nonnegative summand in the trace sum, even when s is negative. Used by P.
- P public `max_eigenvalue_tail_le_iInf_trace_exp`: the only public theorem in P. All meaningful assumptions are visible in its signature.
- T private `hermitian_exp_norm_le`: derives the exponential norm cap from a Hermitian norm cap for positive s; used for finite integrability.
- T private `hermitian_trace_exp_nonneg`: derives nonnegativity using standard functional calculus and PSD trace; used for the real/nonnegative integral conversion.
- T private `actual_source_four_sums_laplace_tail`: complete literal four-family application. Its private status is retained in prose and graph.

No extra declaration, private axiom, theorem-shaped alias, placeholder closure, hidden section hypothesis, existence/default semantic choice, or proof ingredient disguised as a public premise was found in P/T. The matrix norms are the L2 operator norm scope. Matrix squares/exponentials retain algebra multiplication. The actual direct parent modules Radius and Structure were read completely; the necessary Mean module was also read completely for its literal definitions and proved integrability/mean interface. These parent meanings agree with T's local lets. This is not a fresh source-certification of every transitive historical theorem.

Nonblocking purification note: T lines128–133 derive local positivity facts `hd2`, `hd2R`, `hdpos`, `hrpos`, `hlog`, `hLpos`; the remainder does not refer to this positivity block. It appears removable implementation residue. Both private analytic helper declarations are genuinely used, so there is no unused declaration-level mathematical node here. No production cleanup was performed.

## Authored prose and source locators

All current lesson/publication prose, assumptions, formulas, dependency notes, source scopes, source-attribution records, and code-locator fields were read. The six source spans partition every byte of P and T, including module context and all helper bodies. Independently checked each LF-line interval, decoded-character interval, raw UTF8-byte interval, span SHA and full file SHA. All agree. All named Gaussian source anchors exist in the phase1 pinned original HTML, and the Tropp author-page locators agree with the original page images.

The reader clearly distinguishes public P (steps1–3) from associated private T (steps4–6), and explains the real/extended-scalar completion, actual finite expectation, unchanged product law and unproved remainder. It does not attribute ENNReal to Tropp, does not claim Gaussian C.2 explicitly cites Tropp, and does not call the four-family intermediate the full source Bernstein bound.

One minor locator precision issue was found: step5's source-attribution record points at `A3.Ex112` with region label `Truncated radius and actual-mean norm bound`; its exact source formula is the resulting centered bound ||Z_i||≤R_*. The two individual input bounds ||Y_i|| and ||EY_i|| occur at adjacent `A3.Ex111`. The current locator is valid centered-radius context, but the narrow label would be more precise with Ex111, or with wording that says centered-radius consequence. This does not change a mathematical statement and is not a missing source assumption. The global `Radius inputs` source link has the same adjacent-context imprecision. No candidate modification was made.

## Independent static reader checks

The two reader manifests are hash consistent. I independently verified all 118 input-snapshot file hashes, all 207 fixture-file hashes, renderer/overlay hashes, and metadata hashes. The manifests say `metadata_version: authored-v1` while the supplied context filename says `authored-v2`; the actual lesson/pub hashes and all bytes agree, so this is a naming/provenance label issue, not evidence of stale mathematical input.

For both proof and lesson reader pages in both variants, all six exact Lean blocks occur unchanged. In the candidate, all six step disclosures are initially closed, have the correct P/P/P/T/T/T path, and contain a source link with the correct starting line anchor plus a complete matching module download. All four complete source pages decode byte-for-byte to their frozen modules, and every line anchor exists. Each module download equals the corresponding frozen/current source bytes. The source index locates P,T and the two real Gaussian adapters; T is explicitly marked associated private application, without a public declaration node.

The bounded graph is identical between variants, has only partial statuses, uses structural imports/declares and separately labelled source-reference edges, and introduces no public T declaration node. It accurately presents a bounded preview rather than a completed global proof DAG. The renderer supplies empty audit inputs and forces pending publication acceptance; the visible generic `pending historical audit / no source-fidelity verdict` line is a default pending message, not a prior verdict consumed by this reviewer.

The original/candidate distinction is limited to presentation: candidate per-step code actions/source links, complete-source filename/actions/code wrapper, local containment/scroll CSS, and removal of the copied candidate CSS's first Google-font import line. The mathematical lesson/publication payloads and full code text are not changed by the overlay. The stylesheet is scoped to this item and preview variant; no global production renderer or CSS is modified. The renderer does reuse old presentation architecture/file-selection provenance, but its bounded input list contains no old audit/reviewer/decoder payload, and its rendered statuses do not inherit acceptance. I did not open the old provenance sources.

This static review does not establish glyph appearance, mobile/desktop dimensions, horizontal-scroll usability, anchor landing in a running browser, clipboard behavior, browser download contents, graph interaction, or production-site navigation. Full chrome links intentionally extend outside the bounded fixture. No renderer was rerun and no browser was opened in phase2.

## Phase2 disposition

No blocking mathematical/source-type mismatch was found within the advertised real/extended-scalar P and authored private four-family T scopes. The source-complex restriction and extended-expectation completion are disclosed scope deltas, not silent source equality. The minor Ex112/Ex111 locator label, metadata version name, and local positivity residue are recorded above without modifying the candidate. The bounded reader passes static exactness/locator/content review only. Canonical packet-bound source/decoder comparison is deferred to phase3; actual runtime reader acceptance remains deferred.
