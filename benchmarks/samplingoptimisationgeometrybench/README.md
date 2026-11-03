# SamplingOptimisationGeometryBench

Two views of the same mathematical core: **natural-language QA** and **Lean-assisted QA** for sampling, optimisation and geometry. This is a small **public development pilot**, not a leaderboard or a held-out test set.

| Core | Topic | Natural-language task | Lean task |
|---|---|---|---|
| sogb-001 | Sampling / MCMC | Derive reversibility from atomic detailed balance; audit infinite and zero masses | Reconstruct the existing countable-kernel proof |
| sogb-002 | Optimisation | Derive the PL iteration bound, including the negative-factor case | Prove the actual-iterate bound from the supplied upper model and PL inequality |
| sogb-003 | Geometry | Derive the midpoint quadratic envelope and its exact constant | Reconstruct the normed-space midpoint proof |

Three cores, six QA views—not six independent problems. Each pair shares its identity, family, assumptions and public-dev split. The Lean target certifies only its stated conclusion, not every explanatory sentence. Questions/answers are original project exposition, not copied textbook passages. Independent semantic review of these new QA pairs is **pending**, even where the underlying library theorem was previously reviewed.

## Try it

From the repository root, with Python 3.11+:

```bash
python tools/sog_bench.py check
python tools/sog_bench.py export --output .astis/sog-bench-export
python tools/sog_bench.py check-lean
python -m unittest tools.tests.test_sog_bench
python website/scripts/build_site.py
python website/scripts/check_site.py
```

Open `_site/benchmarks/samplingoptimisationgeometrybench/index.html` through a local static server. The website has separate natural-language and Lean entry points and one short page per exercise. Reference solutions, rubric and exact Lean are initially folded. Downloads include:

- `questions.jsonl`: six prompt-only views; no solutions, reference Lean or rubric;
- `reference.jsonl`: three shared cores with reference explanations, rubric and source-extracted Lean;
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

Edit only `cores.json`: choose a stable id/family, explicit domain/conventions, a precise question, stepwise formula solution, four-point rubric, existing declaration and source file, required Lean context, actual dependencies and strict boundary. Both tracks are generated from this one record. Changing a question, context, answer or source proof changes its binding hash; do not silently reuse old evidence. Add tests and obtain independent source-blind comparison before advertising a reviewed semantic pair. New production mathematics still follows the normal publication and encoder–denoiser protocols; a Bench item is no shortcut around them.

Only original/permission-cleared material may enter ML training or evaluation exports. Do not use restricted ATLAS-derived indexes, source text, projections or derivatives in this benchmark. The root Apache-2.0 grant does not relicense external books, papers, code or data; retain their applicable notices. This pilot exports the three listed original/adapted local modules' extracted target proofs and original QA only, not external datasets or transitive source trees. Dependencies remain installed under their own licenses.
