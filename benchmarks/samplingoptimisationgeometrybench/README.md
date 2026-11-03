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

Mathematical cores and QA views are counted separately. A supporting theorem is not an equivalent Lean question. Paired views share identity, family, assumptions and public-dev split. The Lean target certifies only its stated conclusion, not every explanatory sentence. Questions/answers are original exposition, not copied textbook passages. Content-bound independent AI editorial review accepts cores 001–007, including a separately reviewed correction to 003. New cores 008–014, graph QA editorial review and empirical difficulty calibration remain pending. Existing theorem review does not certify a new question.

## Review evidence and scope

[Round 1](reviews/round-1/README.md) records the actual distinct decoder, source reviewer and exact-proposal reviewer, their frozen inputs and immutable reports. The reviewer found that our original explanation of the quadratic envelope confused sufficient Gaussian-domination hypotheses with necessary normalization conditions. The corrected explanation includes the counterexample \(V(x)=|x|\). Only that project-authored explanation changed; neither a textbook statement nor a Lean target was repaired.

`tools/sog_bench_review.py` derives item status from exact QA/source/import-closure/toolchain bindings. Editing a question or its mathematical context makes its old review stale. The first three Lean views have **conclusion-only alignment**; the review explicitly lists explanatory claims not formalized by those targets. This is AI editorial checking, not human consensus, canonical theorem publication, model measurement or a calibrated difficulty label. The tool prepares input packets; it never creates independent verdicts. Round 1 is frozen to its original three formal cases; create a new bounded round before adding further formal cases.

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
python -m unittest tools.tests.test_sog_bench tools.tests.test_sog_bench_review
python website/scripts/build_site.py
python website/scripts/check_site.py
```

Open `_site/benchmarks/samplingoptimisationgeometrybench/index.html` through a local static server. The website has separate natural-language and Lean entry points and one short page per exercise. Reference solutions, rubric and exact Lean are initially folded. Downloads include:

- `questions.jsonl`: available mathematical prompt-only views; no solutions, reference Lean or rubric;
- `reference.jsonl`: mathematical cores, explanations, rubrics and exact Lean only where aligned;
- `reviewed-questions.jsonl` / `reviewed-reference.jsonl`: only the currently accepted editorial subset, with questions still separated from answers;
- `editorial-review.json`: per-item review scope, evidence hashes, stale/pending states and unformalized explanation;
- `graph-questions.jsonl` / `graph-reference.jsonl`: separate structural prompts and answers;
- `curriculum.json` / `coverage.json`: seven domains, five levels, separate draft track counts and gaps;
- `lean/*-task.lean.txt`: imports/context and a fixed target with a comment slot; fill the slot with a proof, then save as `.lean`;
- `lean/*-reference.lean`: runnable references extracted from the existing library proof;
- `manifest.json`: version, core/family/split identities, LF-normalized source hashes, exact toolchain/Mathlib manifest hashes and export file hashes;
- the project license, scope and attribution notices.

Use the repository's pinned **Lean 4.33.0** and `lake-manifest.json`. The target module is deliberately not imported: imported ancestor modules remain allowed. This is **open-library reconstruction**, not a claim that all equivalent statements are unavailable elsewhere. `check-lean` builds only required imported modules, compiles the three trusted references, and records command results and source-bound fingerprints under `.astis/sog-bench/`. It does not execute model submissions, certify source equivalence, run the full ASTIS gate, or advance the Registry. Website compiler labels are conservative: absent or stale receipts mean no current reference check is recorded. CI runs the same focused compiler check separately from website-only checks.

## Assess a model

1. Give the model a prompt-only record, its track and the allowed-library policy. Do not include the reference export in its prompt.
2. For natural-language QA, a human or independently validated grader awards each of four criteria 0 or 1; report criterion scores and the full response. Do not use keyword matching as a correctness metric.
3. For Lean, keep imports, context, assumptions and conclusion fixed. Audit for additional hypotheses, changed definitions, placeholders, new axioms and unsafe verification bypasses. Compiler acceptance alone is **not** an assessment of arbitrary generated code. Execute untrusted submissions only in a separately provisioned, network-disabled sandbox with resource limits; this starter does not provide one.
4. Report both tracks separately, with model/version, prompt, decoding settings, allowed retrieval/tools, attempts, time and grader. A paired answer is not two independent samples. No model scores have been measured here.
5. All pilot answers and source proofs are public and potentially contaminated. They are useful for learning, training where rights allow, regression checks and rubric development—not evidence of unseen generalization. Reserve entire mathematical families before designing a genuinely private evaluation set; never move a public-dev item into a secret test split.

## Add a core

Edit `cores.json`: stable id/family, `library_domains`, per-available-track `track_levels`, reasoning-based `difficulty_reason`, `skills`, explicit assumptions, question, formula solution, four-point rubric and source boundary. Set `lean_enabled: false` when a support theorem is not a complete equivalent task. If aligned, record the existing declaration, source file, context and actual dependencies. Views are generated from one record. Content/source changes invalidate the binding; never replay old reviews. Obtain independent source-blind comparison before reviewed admission. New production mathematics follows the normal publication and encoder–denoiser protocol; a Bench item is no shortcut.

## Graph questions and scoring

`graph_tasks.json` selects an induced import slice from explicitly listed original local Lean files. Edges point **consumer → imported module**. Omitted imports are outside this slice, not absent from the library. The slice is source-hashed; no mixed upstream/ATLAS graph data is used. Current tasks ask direct imports (L1), common parents (L2) and node-ablation reachability (L3). These are structural skills—not theorem difficulty or a minimal mathematical-premise certificate. All variants remain in the PL family's public-dev split.

Graph answers have exactly `nodes` (distinct module IDs) and `entails_mathematical_necessity` (Boolean). One point requires both the exact node set and the false necessity certification; that constant boundary answer alone earns no credit. The grader never executes code or grades a mathematical proof:

```bash
python tools/sog_bench.py grade-graph --submissions responses.jsonl --run-metadata run.json --output .astis/my-graph-run
```

Each response supplies `id`, the prompt's `binding_sha256`, `attempt: 1` and `answer`. Run metadata requires `run_id`, `model`, `model_version`, `created_at`, `prompt_profile: "given-snapshot"`, `attempt_policy: "first-attempt"`, `tools` and `seed`. Unknown/duplicate IDs, stale bindings and alternate attempt policies are rejected. Missing answers remain in the denominator with zero credit. Retain raw prompts/responses, timing/tokens and grader versions for experiments. Reference self-tests are software tests, not measured model performance. Prose grading and safe untrusted-Lean evaluation remain separate work.

Only original/permission-cleared material may enter ML training or evaluation exports. Do not use restricted ATLAS-derived indexes, source text, projections or derivatives in this benchmark. The root Apache-2.0 grant does not relicense external books, papers, code or data; retain their applicable notices. This pilot exports the three aligned local modules' extracted target proofs and original QA only, not external datasets or transitive source trees. Historical review packets retain rejected wording for audit and are **not reference-answer gold**; use the derived reviewed-reference export instead. Dependencies remain installed under their own licenses.
