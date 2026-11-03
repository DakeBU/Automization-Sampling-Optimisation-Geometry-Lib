# SamplingOptimisationGeometryBench

**Natural-language QA**, aligned **Lean-assisted QA** where available, and separate **structured graph QA** for sampling, optimisation and geometry. This is a **public development curriculum**, not a leaderboard or a held-out test set.

[Website](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/benchmarks/samplingoptimisationgeometrybench/) · [Continuing Goal and admission order](GOAL.md) · [Machine-readable curriculum](curriculum.json)

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

Mathematical cores and QA views are counted separately. A supporting theorem is not an equivalent Lean question. Paired views share identity, family, assumptions and public-dev split. The Lean target certifies only its stated conclusion, not every explanatory sentence. Questions/answers are original exposition, not copied textbook passages. Current independent AI editorial eligibility is derived from frozen reports and exact bindings, not this table; revised questions or sources can make earlier acceptance stale. Structural graph editorial decisions are recorded separately; empirical difficulty calibration remains open. Existing theorem review does not certify a new question.

## Review evidence and scope

[Round 1](reviews/round-1/README.md) records the actual distinct decoder, source reviewer and exact-proposal reviewer, their frozen inputs and immutable reports. The reviewer found that our original explanation of the quadratic envelope confused sufficient Gaussian-domination hypotheses with necessary normalization conditions. The corrected explanation includes the counterexample \(V(x)=|x|\). Only that project-authored explanation changed; neither a textbook statement nor a Lean target was repaired.

`tools/sog_bench_review.py` derives item status from exact QA/source/import-closure/toolchain bindings. Editing a question or its mathematical context makes its old review stale. The first three Lean views have **conclusion-only alignment**; the review explicitly lists explanatory claims not formalized by those targets. This is AI editorial checking, not human consensus, canonical theorem publication, model measurement or a calibrated difficulty label. The tool prepares input packets; it never creates independent verdicts. Round 1 is frozen to its original three formal cases; create a new bounded round before adding further formal cases.

[Round 2](reviews/round-2/README.md) independently checks the seven L1 natural-language questions. Its input contains no equivalent Lean target, so its acceptance cannot create a formal QA view. The `prose-packet` route explicitly rejects paired tasks, which still require anonymous decoding. Separate review rounds compose only for disjoint cores; changed content becomes stale and overlapping decisions require an explicit supersession policy.

[Formal round 3](reviews/formal-3/README.md) covers the coupling-normalization pair. New paired batches use `tools/sog_bench_formal_review.py`: select aligned `--ids`, prepare a fresh anonymous `decoder-packet --round ...`, obtain a genuinely independent decoder report, then prepare `reviewer-packet --round ...` for a distinct source reviewer. Each core supplies minimal plain-string `decoder_definitions`; source identities, answers, proofs and previous verdicts must stay out of decoder input. The generated anonymous target retains the actual given definition while removing owning namespace labels. Never alter an earlier report or mint another ID to evade its review. Disjoint `reviews/formal-*` rounds are discovered automatically; input preparation cannot create admission.

[Formal round 5](reviews/formal-5/README.md) applies the same workflow to the sphere and conditional-kernel pairs. The unchanged anonymous input and actual decoder report from initial staging round 4 are reused after a bibliography-only correction; no new decoding or changed mathematical target is claimed.

[Formal round 6](reviews/formal-6/README.md) checks the strict-threshold Wasserstein join. It requires the correct shared-middle joint law, measurable marginal/cost identities and extended L² Minkowski, not a call to the completed exact triangle theorem. The Bernoulli shortcut diagnosis is natural-language explanation, not a separate Lean conclusion. This is a new composition task over existing library mathematics, not a new Registry theorem. Current admission still comes only from the frozen independent reports.

[Formal round 7](reviews/formal-7/README.md) binds the global supporting-vector bound and actual finite-measure heat-bath kernel to separate anonymous reconstructions and source checks. The additional constrained-support and nonconvergence examples are prose, not extra Lean conclusions. [Prose round 3](reviews/prose-3/README.md) separately checks the finite-horizon optimization task, including the exact constant, terminal energy and degenerate cases. Its full unchanged supporting module is available for reading/copying/downloading, with upstream Optlib notices retained, but is not counted as an aligned formal task. The paired and unpaired subgradient exercises share one public family and cannot be split into independent train/test families. As elsewhere, links to evidence do not replace recomputing current acceptance.

[Graph round 1](reviews/graph-1/README.md) independently checks source-scanned arrows, structural answers, exact scoring, family boundaries and provisional reasoning levels. The initial L3 ablation label and an L2 proposal were rejected as inflated for two directly supplied edges. The separately reviewed final L1 correction changes only the label and its binding; the question, graph and answer are unchanged. Earlier reports are immutable audit evidence, not gold. `graph-editorial-review.json` derives the current decisions and becomes stale if the question, source, scorer or curriculum changes. Import edges still certify no mathematical necessity.

[Graph round 4](reviews/graph-4/README.md) rechecks all five current graph tasks under an explicit two-kind evidence policy and supersedes the old graph rounds for current admission without rewriting them. It adds a replayed, source-bound slice of selected constants in compiled proof bodies. The reviewer required lowering g002 to L1, consistent with the similarly explicit shared-parent lookup; [round 5](reviews/graph-5/README.md) independently reviews only that exact label/binding repair. Provisional labels are not measured difficulty.

## Difficulty and subject coverage

The seven domain indexes follow the seven library routes; shared questions can appear in several indexes without multiplying the global count. `python tools/sog_bench.py coverage` computes the domain × L1–L5 × track matrix. An empty cell is a visible gap, not a request for filler or a completion percentage.

| Level | Reasoning target |
|---|---|
| L1 | Concepts, conventions, explicit structural relations |
| L2 | Local derivation with exact assumptions/constants |
| L3 | Multi-step proof, cases, counterexample or faulty-inference diagnosis |
| L4 | Cross-module composition with actual inputs, domains, integrability and errors |
| L5 | Source-grounded research audit or proof transfer with failure boundaries |

Labels are author-assigned and **not empirically calibrated**. Natural-language and Lean views have their own labels; code length, tokens, import depth and graph distance are not difficulty. L5 is currently a gap, not invented solutions to open problems. Import structure, elaborated declaration dependencies, reviewed source-proof routes and conceptual mechanisms are distinct evidence types.

## Try it

From the repository root, with Python 3.11+:

```bash
python tools/sog_bench.py check
python tools/sog_bench.py coverage
python tools/sog_bench.py export --output .astis/sog-bench-export
python tools/sog_bench.py check-lean
python tools/sog_bench_compiled_graph.py check
python -m unittest tools.tests.test_sog_bench tools.tests.test_sog_bench_review tools.tests.test_sog_bench_formal_review tools.tests.test_sog_bench_graph_review tools.tests.test_sog_bench_compiled_graph tools.tests.test_sog_bench_prose
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
3. For Lean, keep imports, context, assumptions and conclusion fixed. Audit for additional hypotheses, changed definitions, placeholders, new axioms and unsafe verification bypasses. Compiler acceptance alone is **not** an assessment of arbitrary generated code. Execute untrusted submissions only in a separately provisioned, network-disabled sandbox with resource limits; this starter does not provide one.
4. Report both tracks separately, with model/version, prompt, decoding settings, allowed retrieval/tools, attempts, time and grader. A paired answer is not two independent samples. No model scores have been measured here.
5. All pilot answers and source proofs are public and potentially contaminated. They are useful for learning, training where rights allow, regression checks and rubric development—not evidence of unseen generalization. Reserve entire mathematical families before designing a genuinely private evaluation set; never move a public-dev item into a secret test split.

## Add a core

Edit `cores.json`: stable id/family, `library_domains`, per-available-track `track_levels`, reasoning-based `difficulty_reason`, `skills`, explicit assumptions, question, formula solution, four-point rubric and source boundary. Set `lean_enabled: false` when a support theorem is not a complete equivalent task. If aligned, record the existing declaration, source file, context and actual dependencies. Views are generated from one record. Content/source changes invalidate the binding; never replay old reviews. Obtain independent source-blind comparison before reviewed admission. New production mathematics follows the normal publication and encoder–denoiser protocol; a Bench item is no shortcut.

An unpaired prose core may opt into `support_source_view: true`. Its exact supporting module, including imports, namespace, copyrights and modification notice, is then folded immediately beneath its natural-language proof and included as `lean/<id>-support.lean` in the reference bundle. This creates no Lean question or trusted-reference certificate; it must explain which proof steps the module actually supports. Source code remains excluded from prompt-only records. Disjoint additional NL-only reviews live under `reviews/prose-*`, use the existing `prose-packet` format and invalidate on content/source changes. Overlapping review decisions fail closed, not last-writer-wins.

For a requested bounded repair, preserve the original report and freeze the exact before/after proposal with `tools/sog_bench_review.py prose-repair-packet` (proof/difficulty fields only) or `paired-repair-packet` (rubric only), using `--review-round`, `--ids` and `--output <round>/packets/repair-input.json`. A fresh independent actor writes `<round>/repair-review.json`; the author/input generator never supplies a verdict. These overlays bind both original evidence hashes, exact repaired content/context, unchanged formal coverage and explicit minimality. They do not authorize source, question or assumption changes; larger changes need a new explicit review/supersession route, not a replacement ID hiding a failed audit.

## Graph questions and scoring

`graph_tasks.json` selects an induced import slice from explicitly listed original local Lean files. Edges point **consumer → imported module**, not a theorem proof call. After independent reclassification, its direct/common/ablation tasks are L1. `compiled_graph_tasks.json` selects a separate eligible public-theorem slice linked to sogb-018. Its shared-parent task is L1 and its two-step normalization-branch task L2, despite the source mathematical QA being L4. All labels remain provisional. Structural views keep the source core/family/public-dev identity but are not equivalent mathematical questions or independent held-out samples.

The second slice is extracted by `tools/sog_bench_compiled_graph.py` from the **actual compiled proof bodies**, using Lean's `body.getUsedConstants`, not a text search or import scanner. It checks theorem identity, source/import closure, fixed compiler/Mathlib/build pins and transitive axioms against the explicit standard foundation set `propext, Classical.choice, Quot.sound`. A fresh trusted replay must match the recorded artifact in Lean CI. Website-only builds validate its source-bound record; they do not execute Lean in the browser or claim fresh compilation. Neither record hashes nor editorial review replace replay. The graph is induced: unselected constants, private auxiliaries and Mathlib parents are omitted. Even a missing path is **not** a full-closure independence certificate; a positive path is **not** mathematical necessity.

To update this eligible slice after a reviewed source change, run `python tools/sog_bench_compiled_graph.py refresh`, then `check` and obtain a fresh content-bound editorial review where required. Refresh creates neither a review verdict nor Registry credit. It compiles only trusted allowlisted source imports and a generated environment inspector—never model submissions. No mixed upstream or restricted ATLAS graph is read or exported. Source-proof/hypergraph questions and deeper mathematical graph audits still need separate evidence and review.

Graph answers have exactly `nodes` (distinct snapshot node IDs: module IDs in import slices, declaration IDs in compiled-proof slices) and `entails_mathematical_necessity` (Boolean). One point requires both the exact node set and the false necessity certification; that constant boundary answer alone earns no credit. The grader never executes code or grades a mathematical proof:

```bash
python tools/sog_bench.py grade-graph --submissions responses.jsonl --run-metadata run.json --output .astis/my-graph-run
```

Each response supplies `id`, the prompt's `binding_sha256`, `attempt: 1` and `answer`. Run metadata requires `run_id`, `model`, `model_version`, `created_at`, `prompt_profile: "given-snapshot"`, `attempt_policy: "first-attempt"`, `tools` and `seed`. Unknown/duplicate IDs, stale bindings, Boolean attempts and alternate attempt policies are rejected. Missing answers remain in the denominator with zero credit. The score archive retains the full frozen structural items, not just a digest requiring a changing live catalog. Retain raw prompts/responses, timing/tokens and grader versions for experiments. Reference self-tests are software tests, not measured model performance. Human-attested prose recording is a separate tool; safe untrusted-Lean evaluation remains open.

Only original/permission-cleared material may enter ML training or evaluation exports. Do not use restricted ATLAS-derived indexes, source text, projections or derivatives in this benchmark. The root Apache-2.0 grant does not relicense external books, papers, code or data; retain their applicable notices. This pilot exports original QA, aligned local target proofs and explicitly selected notice-preserving supporting modules, not external datasets or transitive source trees. Historical review packets retain rejected wording for audit and are **not reference-answer gold**; use the derived reviewed-reference export instead. Dependencies remain installed under their own licenses.
