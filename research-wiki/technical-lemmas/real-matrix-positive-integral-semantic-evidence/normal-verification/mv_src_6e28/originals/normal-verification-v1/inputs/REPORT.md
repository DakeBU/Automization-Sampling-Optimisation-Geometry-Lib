# Independent native/kernel and bounded reader report

Verifier: `psd_native_7b31`. Mathematical candidate: `9964c33c4599f85d27dc8687e8bd6fdb5c44ff49`. This verifier is neither the prover, decoder nor source reviewer. All created files are inside this verifier's assigned directory. No tracked shared file, ledger, frontier, audit, registry, root test, site source or global graph was changed.

**Result:** native/kernel checks pass for S and actual uncentered P. The production-renderer bounded reader fixture passes the stated desktop/mobile content and visual checks. This is no canonical source-fidelity verdict, full-site acceptance, state transition or normalV authorization. Full R9 centered/weighted T receives no implementation or theorem credit here.

## Independent environment and build

The candidate directory contains exact `git show COMMIT:path` bytes, with each extraction recorded. Its ASTIS output directory was absent and then created empty. No existing project ASTIS `.olean` was copied or searched through `LEAN_PATH`. Pinned external dependencies' existing compiled outputs were reused.

The actual executable is Lean 4.33.0, arm64-apple-darwin24.6.0, commit `d8b18978322de05a8f3dba51ef03cf5461676c17`, Release. `file` independently reports Mach-O arm64. Lean SHA-256 is `1b370cfcbf44e80d1b004ab1b1ab9a4c73951f9f7c242140bcff9bc577576554`; toolchain file SHA-256 is `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b`; manifest SHA-256 is `b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37`. Lake's binary path/hash is also recorded in `toolchain.json`. No `lake update` was executed.

All 9 dependency HEADs match the fixed manifest, and `git status --porcelain=v1 --untracked-files=all` is empty for each, both at preflight and final recheck: mathlib, plausible, LeanSearchClient, importGraph, proofwidgets, aesop, Qq, batteries and Cli. Exact revisions and raw receipts are retained in `dependencies.json` and `receipts/`.

The recursively computed closure contains these 9 modules, all independently compiled successfully in topological order:

1. `AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral`
2. `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw`
3. `AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.GaussianFourthMoment`
4. `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment`
5. `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias`
6. `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram`
7. `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound`
8. `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance`
9. `Tests.RealMatrixPositiveIntegral`

For each module, actual `lean --deps` ASTIS direct imports were checked against the computed closure. `closure.json`, `lean-env.json`, `compile-results.json`, and individual compiler receipts preserve source/output hashes, true argv, cwd, effective environment, candidate/shared HEAD, exit codes and separate raw stdout/stderr. Imports select the build scope; theorem dependencies below were extracted from actual kernel expressions.

## Seals, proof values and axioms

Both final signatures exactly match the statement-seal strings byte for byte, including the local lets in P:

| Target | Statement-seal file SHA-256 | Producer signature SHA-256 |
| --- | --- | --- |
| S `integral_posSemidef` | `a5179ed392ef8e55ab470a3a98ebd542e35301f51472e9cdd7bc168a88bafa26` | `283e07e3c85b9a5cce5c3c40f574f23f593dfcca5e35be4d3e2800f378208b19` |
| P `actual_source_truncated_matrix_second_moments` | `5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14` | `d5ac54443c79ea7b35b09ddcd6b5e3c40bef081bbe4f196cae5ab3ead35aa2ea` |

`candidate/NativeAudit.lean` constructs complete literal propositions independently from the sealed signatures and applies the real roots. The actual root proof values are then substituted into those applications and kernel checked inside a typed let. The four successful cases are universal S (two generic universe parameters), S at `Fin 0` (arbitrary measurable probability carrier, one universe parameter), universal P and P at q=0. No positivity, moment or row-law certificate was added to their premises.

The audit enumerates **46 actual imported declarations** from the 9 ASTIS/test modules, including generated/internal declarations. Every complete type and every complete body is present, closed (no expression/level metavariables, free variables or loose bound variables) and kernel checked; typed lets force proof bodies to have the recorded types. Universes and all outer binder types are inventoried. All axiom sets are subsets of `propext`, `Classical.choice`, `Quot.sound`. A separate raw traversal of actual type/body constants finds exactly these same three axioms at each root, reaching 33,249 constants for S and 57,251 for P.

The new S/P inventory is exactly **2 handwritten theorems + 2 generated theorems**, and all four are root reachable:

- S and `integral_posSemidef._simp_1_1`;
- P and `actual_source_truncated_matrix_second_moments._abel_1_1`.

P's actual direct ASTIS type/body references are the radial-fourth-moment theorem, actual physical row-law theorem, shared S theorem, weighted-frame theorem and its generated `_abel_1_1`. S directly references its generated `_simp_1_1`. The union of actual S/P root reachability contains 39 ASTIS declarations. Seven declarations from older imported substrate are outside that union; their exact names remain in `native-summary.json`. They were still checked, and none is a new S/P helper. These are actual proof-expression references, not import-based implications.

All 9 source modules also passed a sanitized fake-closure scan for `axiom`, `sorry`, `admit`, `Prop := True`, and `:= trivial`. The exact audit implementation and raw results remain available for review.

The complete types/bodies dump is retained **losslessly compressed**, with a verified decompression hash, rather than committed or emitted into chat. Final uncompressed size is 2,197,025,857 bytes and SHA-256 is `50fa6a53b0ccbbfbb21095bcedb8640c0e7ae9d74a69ec224790fb74f2c31b37`. `native-summary.json` records the gzip hash and the preserved failed-attempt dump separately.

## Bounded production reader

Only `huanjian-real-matrix-positive-integral` and `huanjian-gaussian-source-matrix-variance` were rendered as lesson and publication pages (4 pages). The fixture executes fixed-commit production `render_unit`, `source_card`, `page`, `canonical_shell`, `render_source_module` and source-export functions. All CSS is unchanged fixed-commit production CSS, including the actual `site.css` import closure. No fixture-specific CSS was introduced. A minimal theme seed supplies the production shell's required theme inputs; this fixture does not reproduce the full serialized site's late overlays or global navigation inventory.

To preserve source-review separation, fixture publication input includes only the two selected lessons/bindings, exact candidate declarations, and empty audit/cell maps. Bindings therefore remain visibly unverified. No older source verdict was opened or injected. The banner deliberately says no repository-wide Lean gate is recorded.

Actual browser: system Google Chrome **157.0.8103.51**, executable SHA-256 `c9a0f292a25c3771f1895ec3397d2cbbee3ce07ce967acd35f34a38978b4aacd`, driven by Playwright using its explicit executable path. A temporary localhost server and browser were managed inside one foreground process and shut down; no detached process remains.

All 4 pages were actually tested at widths **1440 and 390**. On all 8 cases:

- exact Lean statement and complete proof code match fixed candidate source and begin closed;
- assumptions and every authored proof step are present; disclosures actually open;
- adjacent module-source anchors exist and module downloads are byte-identical to the candidate;
- MathJax produces 28 containers for S and 46 for P, with no MathJax errors;
- there are no page errors, missing HTTP resources, asset failures or document-level horizontal overflow in initial/expanded states;
- long formulas/code retain production horizontal scroll containers rather than expanding the page.

`browser-report.json` preserves diagnostics and all screenshot names; `browser-runtime.json` records executable provenance. Actual screenshots were visually inspected for both S/P, desktop/mobile, and both lesson/publication contexts. Final styled screenshots show readable headings, adjacent folded Lean, assumptions/proof disclosures and source attribution. This is bounded visual acceptance, not original-owner full-site, public deployment, globalgraph or serialized publication acceptance. External citation destinations were rendered and their local adjacency checked; their remote availability was not independently fetched.

## Failures and evidence limitations

Every failure was retained and typed as tooling/environment/fixture work, never as mathematical refutation:

1. A guessed `lakefile.toml` read failed; the actual project uses `lakefile.lean`.
2. Kernel script attempt 1 used a nonexistent `Repr ConstantInfo` instance. Attempt 2 reached literal probes but omitted `allowOpaque := true` while reading theorem bodies. Both original scripts, raw failures and the attempt-2 dump remain. Attempt 3 passed.
3. Renderer attempt 1 lacked the required canonical-theme seed. The original failure remains.
4. Browser attempt 1 hit sandbox localhost-bind denial; an explicitly approved escalated command was used thereafter. Playwright's downloaded headless shell was absent; installed system Chrome was located, versioned and hashed.
5. A raw assumption-text comparison after MathJax transformation caused a false failure. Raw generated assumption-ledger content is now checked before mathematical rendering semantics affect text.
6. The base-shell fixture showed mobile expanded P document overflow. The actual production canonical shell removed it. Visual screenshot inspection then caught two missing CSS `@import` assets; the original fixed assets were added to the fixture and all final checks passed. Pre-canonical and missing-asset snapshots/reports are preserved under `attempts/`.

**Raw-archive qualification:** initial bootstrap discovery calls preceded the persistent recorder. Their tool-visible observations are disclosed in `bootstrap-and-exposure-disclosure.json`; one overbroad filenames-only listing was tool-truncated and its missing original full stdout/hash is not invented. All substantive extraction, dependency, build, kernel, renderer and browser evidence has complete on-disk command receipts. Thus bootstrap archival completeness is qualified, not falsely claimed complete.

The selected statement seals themselves embed historical author compiler/environment metadata. It was unavoidably visible when reading those fixed inputs and is disclosed, but none was used as this run's evidence. No ROOT compiler logs, prior native report contents, decoder/source-review verdicts or unrelated T draft were used.

The native and bounded reader phase is now stopped. Held metadata gates require ROOT's later precise HEAD/scope instruction. No normalV, publication, source-fidelity, centered/weighted T or owner-integration conclusion is issued.
