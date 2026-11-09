# Sampling-Optimisation-Geometry-Bench

**Natural-language QA**, aligned **Lean-assisted QA** where available, and separate **structured graph QA** for sampling, optimisation and geometry. This is a **public development curriculum**, not a leaderboard or a held-out test set.

[Website](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/benchmarks/samplingoptimisationgeometrybench/) · [Continuing Goal and admission order](GOAL.md) · [Machine-readable curriculum](curriculum.json)

Choose [SamplingBench](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/benchmarks/samplingoptimisationgeometrybench/sampling/),
[OptimisationBench](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/benchmarks/samplingoptimisationgeometrybench/optimisation/) or
[GeometryBench](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/benchmarks/samplingoptimisationgeometrybench/geometry/).
These overlapping subject collections retain one catalog, original task/family
identities and public-dev split. Each provides admitted prompt-only JSONL and a
source-bound manifest; collection counts must not be summed as independent data.
The existing directory and machine identifiers remain compatible.

The reader/evaluator requirements are in [the reader contract](../../docs/bench-reader-contract.md).
Agentic Lean remains a required environment milestone, not something completed
by the native Graph JSON adapter or by compiling trusted reference solutions.

| Core | Topic | Natural-language task | Lean task |
|---|---|---|---|
| sogb-001 | Sampling / MCMC | Derive reversibility from atomic detailed balance; audit infinite and zero masses | Reconstruct the existing countable-kernel proof |
| sogb-002 | Optimisation | Derive the PL iteration bound, including the negative-factor case | Prove the actual-iterate bound from the supplied upper model and PL inequality |
| sogb-003 | Geometry | Derive the midpoint quadratic envelope and its exact constant | Reconstruct the normed-space midpoint proof |
| sogb-004 | Statistical Optimal Transport | Prove symmetry using near-optimal swapped couplings | Not yet aligned; supporting theorem only |
| sogb-005 | Riemannian Optimisation | Project a derivative onto the unit-sphere tangent space; diagnose nonunit normals | Not yet aligned |
| sogb-006 | Discrete Sampling / MCMC | Handle null atoms without applying a formula off support | Not yet aligned |
| sogb-007 | SampleWiki / MCMC | Compose adaptive hybrid error bounds; refute unbounded-cost transfer | Not yet aligned |
| sogb-008 | Log-Concave Sampling | Distinguish a log-concave shape from a normalized probability density (L1) | Not yet aligned |
| sogb-009 | SampleWiki | Separate approximation, invariance and actual-input expected cost (L1) | Not yet aligned |
| sogb-010 | Optimisation | Read the PL convention without assuming an algorithmic rate (L1) | Not yet aligned |
| sogb-011 | Riemannian Optimisation | Identify the tangent space, metric and gradient (L1) | Not yet aligned |
| sogb-012 | Statistical Optimal Transport | Read coupling marginal constraints without assuming independence (L1) | Not yet aligned |
| sogb-013 | Discrete Sampling | Distinguish one random-site step from a sweep and an oracle cost (L1) | Not yet aligned |
| sogb-014 | MCMC | Separate invariance, detailed balance and convergence (L1) | Not yet aligned |
| sogb-015 | Statistical Optimal Transport | Recover joint mass one from a prescribed probability marginal (L2) | Reconstruct the actual local coupling-normalization proof (L2) |
| sogb-016 | Riemannian Optimisation | Characterize a quadratic's sphere differential with the actual induced pairing (L3) | Derive the genuine gradient and normalized tangent projection (L3) |
| sogb-017 | SampleWiki / MCMC | Average an integrable conditional event-error bound (L3) | Check measurability, finite-mass conversion and integral inequalities (L3) |
| sogb-018 | Statistical Optimal Transport / Log-Concave Sampling | Join near-optimal coupling selection, conditional gluing and L² Minkowski; refute an independent-coordinate shortcut (L4) | Reconstruct the actual strict-threshold multi-module join (L4) |
| sogb-019 | Optimisation | Bound globally supporting vectors using Lipschitz growth; refute a constrained variant (L3) | Reconstruct the actual support-test norm estimate (L2) |
| sogb-020 | Optimisation | Telescope the actual subgradient update, select a finite best iterate and optimize its step; audit zero cases (L3) | Not aligned; exact supporting module available below the prose proof |
| sogb-021 | MCMC / Discrete Sampling | Prove conditional-resampling invariance and distinguish it from convergence (L3) | Reconstruct the actual finite-measure kernel/disintegration calculation (L2) |
| sogb-022 | Riemannian Optimisation / Statistical Optimal Transport | Take the exact selected-curve chord-to-first-order limit; separate geometric adapters (L3) | Reconstruct positive division, right-filter limits and order passage (L3) |
| sogb-023 | Optimisation | Derive objective monotonicity and the actual gradient-flow value rate in both curvature branches (L4) | Join genuine chain rules, strong-convexity and scalar Gronwall on the supplied trajectory (L4) |
| sogb-024 | MCMC / SampleWiki | Construct a non-countably-generated kernel example auditing a.e. quantifiers without refuting averaged-law equality (L3) | Not aligned; exact supporting averaging module is readable below the proof |
| sogb-025 | Log-Concave Sampling / SampleWiki | Derive the actual directional Gibbs covariance upper bound through smooth linear observables, L² domains and Poincaré (L3) | Reconstruct the existing producer with both curvature and moment premises (L3) |
| sogb-026 | SampleWiki / Sampling / Optimisation | Audit the SPHMC smoothing mechanism under weak convexity, including unnormalized regularity, signed constants and a concave-quadratic failure example (L4) | Not aligned; separate hash-bound supporting sources, not an extension certificate |
| sogb-027 | Discrete Sampling / Log-Concave Sampling | Derive finite-cube log-Sobolev by conditional entropy, RMS contraction and dimension induction; diagnose the conditional-mean shortcut (L3) | Not aligned; full substantive induction is available as supporting source, not a final-call wrapper task |
| sogb-028 | Log-Concave Sampling / Discrete Sampling | Produce homogeneous entropy and full-flip limits, track 16BK/√m and 1/2×4=2, including zero mass (L4) | Compose the actual finite-law/entropy/flip producers and pass inequalities through real limits (L3) |
| sogb-029 | Optimisation · actual Chewi Exercise 3.2 | Complete the Hessian/FTC and balanced-step minimax argument; distinguish the uniform bound from an individual optimum (L3) | No fixed challenge; two named owned core answers are separately compiled and axiom-checked |
| sogb-030 | Optimisation · actual Chewi Exercise 3.1 | Derive cocoercivity and gradient Lipschitzness from the quadratic upper model (L3) | Three separately checked owned answer parts; no fixed challenge |
| sogb-032 | Riemannian Optimisation / Statistical Optimal Transport | Bound changes to a sphere-projected feature gradient when its law and point change (L4) | Compose the angular, Bochner-mean and tangent-gradient producers without importing the answer (L4) |
| sogb-033 | Riemannian Optimisation / Statistical Optimal Transport | Contrast finite angular cost with infinite intrinsic path cost on the two-point sphere (L2) | Angular cost and transport definitions are support only |
| sogb-034 | SampleWiki / MCMC | Compute exact binary hybrid gaps and refute an incorrectly weighted adjacent bound (L2) | Generic kernel averaging and telescope are support only |
| sogb-035 | SampleWiki / MCMC | Transfer stopped work by a pathwise likelihood budget and refute the ideal-average substitute (L5) | TV comparison and single-phase work bounds are support only |

These four reviewed additions retain their existing public IDs. StatOT
Exercise 6 (`sogb-031`) remains on its separate proof-and-publication route.
See [formal round 12](reviews/formal-12/README.md),
[prose round 9](reviews/prose-9/README.md) and
[prose round 10](reviews/prose-10/README.md) for the exact independent reports.

Mathematical cores and QA views are counted separately. A supporting theorem is not an equivalent Lean question. Paired views share identity, family, assumptions and public-dev split. The Lean target certifies only its stated conclusion, not every explanatory sentence. Questions/answers are original exposition, not copied textbook passages. Current independent AI editorial eligibility is derived from frozen reports and exact bindings, not this table; revised questions or sources can make earlier acceptance stale. Structural graph editorial decisions are recorded separately; empirical difficulty calibration remains open. Existing theorem review does not certify a new question.

## Review evidence and scope

[Round 1](reviews/round-1/README.md) records the actual distinct decoder, source reviewer and exact-proposal reviewer, their frozen inputs and immutable reports. The reviewer found that our original explanation of the quadratic envelope confused sufficient Gaussian-domination hypotheses with necessary normalization conditions. The corrected explanation includes the counterexample \(V(x)=|x|\). Only that project-authored explanation changed; neither a textbook statement nor a Lean target was repaired.

`tools/sog_bench_review.py` derives item status from exact QA/source/import-closure/toolchain bindings. Editing a question or its mathematical context makes its old review stale. The first three Lean views have **conclusion-only alignment**; the review explicitly lists explanatory claims not formalized by those targets. This is AI editorial checking, not human consensus, canonical theorem publication, model measurement or a calibrated difficulty label. The tool prepares input packets; it never creates independent verdicts. Round 1 is frozen to its original three formal cases; create a new bounded round before adding further formal cases.

Research audits can declare `additional_source_declarations` in their canonical core. Materialization resolves each actual, non-placeholder local declaration and records its file, line and LF source hash; editorial context binds the union of those sources' local import closures as well as the primary anchor. Source links are generated in the question's folded source panel. None of those support declarations becomes an aligned Lean task or leaks into prompt-only exports. Old cores without this field retain their exact bindings. For sogb-026, the original extension is distinguished from [SPHMC v1 §4.1, equation (4.1), Lemma 4.1](https://arxiv.org/html/2609.06906v1#S4.SS1); the paper's distribution grant is not treated as a blanket ML-text reuse license, and its prose is not copied into the corpus.

[Formal round 9](reviews/formal-9/README.md) accepts the directional covariance pair with conclusion-only coverage. [Prose round 5](reviews/prose-5/README.md) independently checks the weak-convexity audit and preserves the rejected L5 proposal plus a separately accepted exact L4 repair. The latter has no equivalent Lean task; its additional source links make the reusable producers and missing adapters inspectable rather than borrowing their proof credit.

The Bernoulli/Gaussian pair is one conservative public family. Its NL finite-cube exercise exposes the real RMS induction; the original module retains its upstream authors/license notices. Its Gaussian exercise separates the greater scope of the NL derivation from the fixed Lean composition target: regularity, integrability and limits are proved in the actual linked parents, not invented as new public premises. A source-derived proof graph may show those parents, but neither a graph arrow nor the final constructor call is a new mathematical leaf.

[Prose round 6](reviews/prose-6/README.md) accepts the finite-cube question without manufacturing an aligned task. [Formal round 10](reviews/formal-10/README.md) compares the Gaussian target to an independent anonymous reconstruction, checks the full formula argument and retains conclusion-only formal coverage. These are editorial difficulty judgments, not model measurements.

[Prose round 7](reviews/prose-7/README.md) audits the actual textbook exercise, every canonical source part and seven semantic slots. Its original scoring-overreach finding is preserved; a fresh reviewer accepts the exact rubric-only repair. Valid minimax proofs on the stated h≥0 domain receive credit; a stronger all-real proof is optional. The disjoint NL scoring repair scope cannot change mathematical prose, source, assumptions, question, family, difficulty or coverage, and does not broaden older proof/difficulty repair scopes.

## Numbered textbook exercises and reference solutions

Actual numbered exercises from the cited Chewi textbooks are explicit source-bound entries, alongside original library-grounded QA. Their current editorial admission, exact source parts and owned-answer build records are generated in the numbered-exercise directory and downloadable map, not asserted by this prose. Each needs verified edition/number/pages/subparts, an original complete mathematical answer, independent review and actual Lean/graph/test links. Partial coverage stays partial; alternative valid proofs receive credit. No uniquely “best” answer claim is made.

The first entry, sogb-029, is Chewi Optimization Exercise 3.2. Its complete authored formula answer reuses the existing [source/solution window](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/libraries/optimisation/chapter-03.html#chewi-opt-v1-exercise-3-2), two actual owned core-answer declarations and their graph nodes. It has no separate fixed Lean reconstruction task. The Hilbert/parameter extensions and unformalized contextual material remain explicit; neither code existence nor source intake is whole-exercise certification.

[Exercise provenance and contribution rules](TEXTBOOK_EXERCISES.md) describe the source audit. Canonical book pins are in textbook_exercises.json; source parts/answers are reused from the existing publication record. Generated textbook-exercise-map.json separates editorial state, owned core-answer compilation and available QA tracks. Other Chewi textbooks and all seven domains remain required scope.

[Round 2](reviews/round-2/README.md) independently checks the seven L1 natural-language questions. Its input contains no equivalent Lean target, so its acceptance cannot create a formal QA view. The `prose-packet` route explicitly rejects paired tasks, which still require anonymous decoding. Separate review rounds compose only for disjoint cores; changed content becomes stale and overlapping decisions require an explicit supersession policy.

[Formal round 3](reviews/formal-3/README.md) covers the coupling-normalization pair. New paired batches use `tools/sog_bench_formal_review.py`: select aligned `--ids`, prepare a fresh anonymous `decoder-packet --round ...`, obtain a genuinely independent decoder report, then prepare `reviewer-packet --round ...` for a distinct source reviewer. Each core supplies minimal plain-string `decoder_definitions`; source identities, answers, proofs and previous verdicts must stay out of decoder input. The generated anonymous target retains the actual given definition while removing owning namespace labels. Never alter an earlier report or mint another ID to evade its review. Disjoint `reviews/formal-*` rounds are discovered automatically; input preparation cannot create admission.

[Formal round 5](reviews/formal-5/README.md) applies the same workflow to the sphere and conditional-kernel pairs. The unchanged anonymous input and actual decoder report from initial staging round 4 are reused after a bibliography-only correction; no new decoding or changed mathematical target is claimed.

[Formal round 6](reviews/formal-6/README.md) checks the strict-threshold Wasserstein join. It requires the correct shared-middle joint law, measurable marginal/cost identities and extended L² Minkowski, not a call to the completed exact triangle theorem. The Bernoulli shortcut diagnosis is natural-language explanation, not a separate Lean conclusion. This is a new composition task over existing library mathematics, not a new Registry theorem. Current admission still comes only from the frozen independent reports.

[Formal round 7](reviews/formal-7/README.md) binds the global supporting-vector bound and actual finite-measure heat-bath kernel to separate anonymous reconstructions and source checks. The additional constrained-support and nonconvergence examples are prose, not extra Lean conclusions. [Prose round 3](reviews/prose-3/README.md) separately checks the finite-horizon optimization task, including the exact constant, terminal energy and degenerate cases. Its full unchanged supporting module is available for reading/copying/downloading, with upstream Optlib notices retained, but is not counted as an aligned formal task. The paired and unpaired subgradient exercises share one public family and cannot be split into independent train/test families. As elsewhere, links to evidence do not replace recomputing current acceptance.

[Formal round 8](reviews/formal-8/README.md) independently decodes and checks the selected-curve limiting proof and actual gradient-flow objective estimate. The scalar pairing is not automatically a geometric gradient; the supplied flow/minimizer are not an existence theorem. The time-zero audit is prose, not another Lean conclusion. [Prose round 4](reviews/prose-4/README.md) checks a countable/co-countable measure/kernel construction. It distinguishes event-dependent exceptional sets from a common null set and explicitly computes equal averaged laws. It does not claim to refute the source averaging result or countability-qualified kernel uniqueness. These new questions reuse existing mathematics and create no Registry leaves or empirical difficulty evidence.

[Graph round 1](reviews/graph-1/README.md) independently checks source-scanned arrows, structural answers, exact scoring, family boundaries and provisional reasoning levels. The initial L3 ablation label and an L2 proposal were rejected as inflated for two directly supplied edges. The separately reviewed final L1 correction changes only the label and its binding; the question, graph and answer are unchanged. Earlier reports are immutable audit evidence, not gold. `graph-editorial-review.json` derives the current decisions and becomes stale if the question, source, scorer or curriculum changes. Import edges still certify no mathematical necessity.

[Graph round 4](reviews/graph-4/README.md) rechecked the five then-current graph tasks under an explicit two-kind evidence policy. It adds a replayed, source-bound slice of selected constants in compiled proof bodies. The reviewer required lowering g002 to L1, consistent with the similarly explicit shared-parent lookup; [round 5](reviews/graph-5/README.md) independently reviews only that exact label/binding repair. These are historical decisions, not current admission or measured difficulty.

[Graph round 6](reviews/graph-6/README.md) adds the convex-flow slice and statement-occurrence query, but independently identifies incomplete import-closure pinning on its non-anchor midpoint branch. Its failed admission evidence, old extractor and snapshots are preserved. [Round 7](reviews/graph-7/README.md) freshly audits the corrected current scope; its actual report, not the fact that a replay ran, determines current acceptance. Old rounds remain historical, not silently rebound to new fingerprints.

## Difficulty and subject coverage

The seven domain indexes follow the seven library routes; shared questions can appear in several indexes without multiplying the global count. `python tools/sog_bench.py coverage` computes the domain × L1–L5 × track matrix. An empty cell is a visible gap, not a request for filler or a completion percentage.

| Level | Reasoning target |
|---|---|
| L1 | Concepts, conventions, explicit structural relations |
| L2 | Local derivation with exact assumptions/constants |
| L3 | Multi-step proof, cases, counterexample or faulty-inference diagnosis |
| L4 | Cross-module composition with actual inputs, domains, integrability and errors |
| L5 | Source-grounded research audit or proof transfer with failure boundaries |

Labels are provisional and **not empirically calibrated**. Natural-language and Lean views have their own labels; code length, tokens, import depth and graph distance are not difficulty. Independent review lowered the weak-convexity transfer audit to L4. The stopped-work audit adds one natural-language L5 core shared by SampleWiki and MCMC; it does not fill any L5 Lean cell or prove a cost transfer for either actual sampler. Import structure, elaborated declaration dependencies, reviewed source-proof routes and conceptual mechanisms are distinct evidence types.

## Try it

The website now separates **Browse tasks / Train / Evaluate / Expert review**.
Use `agent-tasks.zip` and `task-index.json` for prompt-only per-task instructions,
environment/verifier contracts and response templates; use the separate
`training-pairs.jsonl` only when intentionally supplying answers. The expert
directory and `expert-graph-positions.json` locate the real owned results and
show missing formal coverage. See [the ecosystem contract](ECOSYSTEM.md).
The portable JSON package is not a native harness. The optional
[native Harbor graph adapter](HARBOR.md) has a dedicated Linux runtime CI gate,
separate verifier and operator download. It does not execute submitted Lean or
certify paid-agent performance; inspect its actual CI evidence and limitations.

The experimental [fixed-target Lean runtime](lean-runtime/README.md) has actual
reference/negative-check evidence and a bounded [compiler tool](lean-runtime/WORKSPACE.md).
Its controlled reference, negative, I/O/resource/input and compiler-workspace
cases passed native08, with a separately recorded
[independent scope review](../../runs/20261105-bench-lean-runtime/native08-independent-review.json).
This accepts an experimental Linux operator CLI under its stated trust and
isolation assumptions, not general hosted execution, security certification or
measured model performance. Fresh integration and authenticated model evaluation
remain separate gates.

From the repository root, with Python 3.11+:

```bash
python tools/sog_bench.py check
python tools/sog_bench.py coverage
python tools/sog_bench.py export --output .astis/sog-bench-export
python tools/sog_bench.py check-lean
python tools/sog_bench_compiled_graph.py check
python -m unittest tools.tests.test_sog_bench tools.tests.test_sog_bench_review tools.tests.test_sog_bench_formal_review tools.tests.test_sog_bench_graph_review tools.tests.test_sog_bench_compiled_graph tools.tests.test_sog_bench_prose
python -m unittest tools.tests.test_sog_bench_experience
python website/scripts/build_site.py
python website/scripts/check_site.py
```

Open `_site/benchmarks/samplingoptimisationgeometrybench/index.html` through a local static server. The website has separate natural-language and Lean entry points and one short page per exercise. Reference solutions, rubric and exact Lean are initially folded. Downloads include:

- `questions.jsonl`: available mathematical prompt-only views; no solutions, reference Lean or rubric;
- `reference.jsonl`: mathematical cores, explanations, rubrics and exact Lean only where aligned;
- `reviewed-questions.jsonl` / `reviewed-reference.jsonl`: only the currently accepted editorial subset, with questions still separated from answers;
- `editorial-review.json`: per-item review scope, evidence hashes, stale/pending states and unformalized explanation;
- `graph-questions.jsonl` / `graph-reference.jsonl`: separate structural prompts and answers;
- `reviewed-graph-questions.jsonl` / `reviewed-graph-reference.jsonl`: only currently admitted graph questions/references, excluding new drafts and stale items;
- `graph-editorial-review.json`: separately bound structural editorial decisions, not theorem/proof certification;
- `compiled-transport-graph.json`: recorded selected proof-body occurrences, source/toolchain/generator fingerprints and approved foundational axioms; fresh compiler replay is a separate CI gate;
- `EVALUATION.md` / `examples/prose-run.json`: offline first-answer recording and human-rubric scoring instructions/template;
- `curriculum.json` / `coverage.json`: seven domains, five levels, separate draft track counts and gaps;
- `lean/*-task.lean.txt`: imports/context and a fixed target with a comment slot; fill the slot with a proof, then save as `.lean`;
- `lean/*-reference.lean`: runnable references extracted from the existing library proof;
- `manifest.json`: version, core/family/split identities, LF-normalized source hashes, exact toolchain/Mathlib manifest hashes and export file hashes;
- the project license, scope and attribution notices.

Use the repository's pinned **Lean 4.33.0** and `lake-manifest.json`. The target module is deliberately not imported: imported ancestor modules remain allowed. This is **open-library reconstruction**, not a claim that all equivalent statements are unavailable elsewhere. `check-lean` builds only required imported modules, compiles all aligned trusted references, and records command results and source-bound fingerprints under `.astis/sog-bench/`. It does not execute model submissions, certify source equivalence, run the full ASTIS gate, or advance the Registry. Website compiler labels are conservative: absent or stale receipts mean no current reference check is recorded. CI runs the same focused compiler check separately from website-only checks.

Compiler receipts bind each selected source and actual local import closure, the given task/reference code and pinned toolchain/Mathlib/build configuration. Relevant changes invalidate the receipt; unrelated live proof files do not. This narrower cache scope is not a substitute for the full integration gate. Browser QA derives its selected Lean pages and download checks from the generated manifest/prompts, so adding a paired core does not require another hand-maintained page list.

## Assess a model

Start with [Run and assess answers](EVALUATION.md). `tools/sog_bench_prose.py prepare` freezes selected prompt/reference/response records and produces a blank human worksheet; `score` records a genuinely supplied human adjudication with exact criterion text, reasons and hashes. Unknown/duplicate/stale responses and unfinished worksheets are rejected; missing/empty answers stay in the denominator. This records declared conditions and human-attested judgments, not authenticated execution/identity or automatically verified mathematics. Historical archives retain their own rubric rather than being reinterpreted under later catalog edits.

1. Give the model a prompt-only record, its track and the allowed-library policy. Do not include the reference export in its prompt.
2. For natural-language QA, a human or independently validated grader awards each of four criteria 0 or 1; report criterion scores and the full response. Do not use keyword matching as a correctness metric.
3. For Lean, keep imports, context, assumptions and conclusion fixed. Audit for additional hypotheses, changed definitions, placeholders, new axioms and unsafe verification bypasses. Compiler acceptance alone is **not** an assessment of arbitrary generated code. The experimental [Linux compiler workspace](lean-runtime/WORKSPACE.md) supports the admitted fixed targets through the declared network-disabled, resource-bounded runtime; provision that environment first and never execute model Lean on the host. It is not a general hosted executor or a claim to support every Lean-language submission.
4. Report both tracks separately, with model/version, prompt, decoding settings, allowed retrieval/tools, attempts, time and grader. A paired answer is not two independent samples. No model scores have been measured here.
5. All pilot answers and source proofs are public and potentially contaminated. They are useful for learning, training where rights allow, regression checks and rubric development—not evidence of unseen generalization. Reserve entire mathematical families before designing a genuinely private evaluation set; never move a public-dev item into a secret test split.

## Add a core

Edit `cores.json`: stable id/family, `library_domains`, per-available-track `track_levels`, reasoning-based `difficulty_reason`, `skills`, explicit assumptions, question, formula solution, four-point rubric and source boundary. Set `lean_enabled: false` when a support theorem is not a complete equivalent task. If aligned, record the existing declaration, source file, context and actual dependencies. Views are generated from one record. Content/source changes invalidate the binding; never replay old reviews. Obtain independent source-blind comparison before reviewed admission. New production mathematics follows the normal publication and encoder–denoiser protocol; a Bench item is no shortcut.

An unpaired prose core may opt into `support_source_view: true`. Its exact supporting module, including imports, namespace, copyrights and modification notice, is then folded immediately beneath its natural-language proof and included as `lean/<id>-support.lean` in the reference bundle. This creates no Lean question or trusted-reference certificate; it must explain which proof steps the module actually supports. Source code remains excluded from prompt-only records. Disjoint additional NL-only reviews live under `reviews/prose-*`, use the existing `prose-packet` format and invalidate on content/source changes. Overlapping review decisions fail closed, not last-writer-wins.

For a requested bounded repair, preserve the original report and freeze the exact before/after proposal with `tools/sog_bench_review.py prose-repair-packet` (proof/difficulty fields only) or `paired-repair-packet` (rubric only), using `--review-round`, `--ids` and `--output <round>/packets/repair-input.json`. A fresh independent actor writes `<round>/repair-review.json`; the author/input generator never supplies a verdict. These overlays bind both original evidence hashes, exact repaired content/context, unchanged formal coverage and explicit minimality. They do not authorize source, question or assumption changes; larger changes need a new explicit review/supersession route, not a replacement ID hiding a failed audit.

`paired-prose-repair-packet` is a distinct explicit scope allowing only the mathematical-proof `steps` field in a paired core. It cannot change the rubric, difficulty, source, task or assumptions. Formal round 8 uses it to remove a sign-dependent adjective while retaining the exact formula and formal statement. Earlier scoring-only repair inputs keep their narrower scope; changing a proposal's scope or fields cannot reuse its old exact-input review.

## Graph questions and scoring

`graph_tasks.json` selects an induced import slice from explicitly listed original local Lean files. Edges point **consumer → imported module**, not a theorem proof call. After independent reclassification, its direct/common/ablation tasks are L1. `compiled_graph_tasks.json` selects a separate eligible public-theorem slice linked to sogb-018. Its shared-parent task is L1 and its two-step normalization-branch task L2, despite the source mathematical QA being L4. All labels remain provisional. Structural views keep the source core/family/public-dev identity but are not equivalent mathematical questions or independent held-out samples.

The second slice is extracted by `tools/sog_bench_compiled_graph.py` from the **actual compiled proof bodies**, using Lean's `body.getUsedConstants`, not a text search or import scanner. It checks theorem identity, source/import closure, fixed compiler/Mathlib/build pins and transitive axioms against the explicit standard foundation set `propext, Classical.choice, Quot.sound`. A fresh trusted replay must match the recorded artifact in Lean CI. Website-only builds validate its source-bound record; they do not execute Lean in the browser or claim fresh compilation. Neither record hashes nor editorial review replace replay. The graph is induced: unselected constants, private auxiliaries and Mathlib parents are omitted. Even a missing path is **not** a full-closure independence certificate; a positive path is **not** mathematical necessity.

`compiled_flow_graph_tasks.json` selects another bounded compiler slice linked to sogb-023: curve slope limit → strong-convexity adapter → actual flow/gradient-pairing proofs, contrasted with the existing midpoint branch. g006 queries paths; g007 combines a path query with exact whitelisted constants emitted by `info.type.getUsedConstants`. These are direct occurrences in the **unexpanded elaborated statement**, not binder-role classification, an inferred hypothesis list or a full type closure. The flow statement contains `Differentiable`, while its proof obtains a genuine gradient; absence of direct `HasGradientAt` is not absence of a gradient. Profiles are a separate table, never extra proof edges or new Mathlib-owned blue nodes. Both new labels are provisional L2, not inherited from the L4 source exercise.

Both snapshots pin the union of **all selected modules' local import closures**, including selected branches outside the anchor's ancestry. This source-code closure is distinct from the displayed induced theorem graph, which still omits constants. `check --slice all` (the default) freshly replays both; `--slice transport` and `--slice convex-flow` focus a trusted diagnostic. New selector/profile/source changes require regenerated records and appropriate fresh editorial evidence. Mathematical cores, structural views and source families are counted separately; these graphs create no theorem or Registry credit.

To update this eligible slice after a reviewed source change, run `python tools/sog_bench_compiled_graph.py refresh`, then `check` and obtain a fresh content-bound editorial review where required. Refresh creates neither a review verdict nor Registry credit. It compiles only trusted allowlisted source imports and a generated environment inspector—never model submissions. No mixed upstream or restricted ATLAS graph is read or exported. Source-proof/hypergraph questions and deeper mathematical graph audits still need separate evidence and review.

Graph answers have exactly `nodes` (distinct snapshot node IDs: module IDs in import slices, declaration IDs in compiled-proof slices) and `entails_mathematical_necessity` (Boolean). One point requires both the exact node set and the false necessity certification; that constant boundary answer alone earns no credit. The grader never executes code or grades a mathematical proof:

```bash
python tools/sog_bench.py grade-graph --submissions responses.jsonl --run-metadata run.json --output .astis/my-graph-run
```

Each response supplies `id`, the prompt's `binding_sha256`, `attempt: 1` and `answer`. Run metadata requires `run_id`, `model`, `model_version`, `created_at`, `prompt_profile: "given-snapshot"`, `attempt_policy: "first-attempt"`, `tools` and `seed`. Unknown/duplicate IDs, stale bindings, Boolean attempts and alternate attempt policies are rejected. Missing answers remain in the denominator with zero credit. The score archive retains the full frozen structural items, not just a digest requiring a changing live catalog. Retain raw prompts/responses, timing/tokens and grader versions for experiments. Reference self-tests are software tests, not measured model performance. Human-attested prose recording and the experimental fixed-target Lean CLI have separate contracts; authenticated model evaluation and general hosted Lean execution remain open.

Only original/permission-cleared material may enter ML training or evaluation exports. Do not use restricted ATLAS-derived indexes, source text, projections or derivatives in this benchmark. The root Apache-2.0 grant does not relicense external books, papers, code or data; retain their applicable notices. This pilot exports original QA, aligned local target proofs and explicitly selected notice-preserving supporting modules, not external datasets or transitive source trees. Historical review packets retain rejected wording for audit and are **not reference-answer gold**; use the derived reviewed-reference export instead. Dependencies remain installed under their own licenses.
