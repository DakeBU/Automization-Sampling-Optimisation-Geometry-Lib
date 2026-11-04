# Textbook exercises: source-to-answer intake

This programme is required by the Bench Goal. It supplements, rather than relabels, the original library-grounded QA. An intake record is **not an admitted question**, a model result or a certificate that every part of an exercise has been formalized.

## First verified source route: Chewi Optimization Exercise 3.2

| Field | Verified source |
|---|---|
| Work | Sinho Chewi, *Lectures on Optimization* |
| Edition | arXiv:2605.07006v1; PDF title date May 11, 2026 |
| Primary exercise | Chapter 3, Exercise 3.2; printed p.23 / one-based PDF p.23 |
| PDF | [Pinned v1, p.23](https://arxiv.org/pdf/2605.07006v1#page=23), 149 pages |
| PDF SHA-256 | 9e28afeacb0121b79691fadc6af9c145ccd787bffd2cf9c3f2310806112e644b |
| HTML | [v1 Chapter 3](https://arxiv.org/html/2605.07006v1#S3) |
| Existing source/solution record | chewi-opt-v1-exercise-3-2 in website/content/publications/optimisation.json |
| Existing readable answer | [Optimization chapter 3](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/libraries/optimisation/chapter-03.html#chewi-opt-v1-exercise-3-2) |
| Intake status | Primary text and whole relevant PDF page visually checked; not yet Bench-admitted |

The source asks for the Hessian/segment-FTC route to a uniform gradient-map contraction, the balanced step 2/(α+β), and the factor (κ−1)/(κ+1). The section explicitly assumes C² regularity. The condition-number expression needs positive α; distinguish that source-implicit regime from the separate α=0 nonexpansive extension in the library. The minimization is of the **uniform curvature-endpoint envelope**, not the best actual constant for every individual objective. Do not add a minimizer premise or claim an iterate/oracle-complexity theorem.

Existing owned declarations, both confirmed as compiled declaration nodes in the current source-derived graph:

- [AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.gradient_step_endpoint_bound](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/underlying-lean-graph/index.html?focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.gradient_step_endpoint_bound)
- [AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.optimal_gradient_step](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/underlying-lean-graph/index.html?focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.optimal_gradient_step)

Use their existing cells, tests, canonical source/semantic reviews and module ownership; do not create duplicate wrappers for the Bench. The current APIs generalize the finite-dimensional source to complete real Hilbert spaces and expose parameter extensions. An exercise answer must disclose those differences and compare the exercise's requested subparts to the exact existing conclusions.

The PDF and HTML identify an arXiv non-exclusive distribution grant, not a blanket text/solution-manual reuse license. Keep the original PDF/page render in the ignored audit cache, outside ML exports. Publish only bibliographic correspondence and an original faithful mathematical restatement/ASTIS-authored solution unless broader permission is established. Do not distribute a copied exercise passage as project-owned text.

## Admission checklist

1. Pin the actual work, author(s), edition/hash, number/subparts and both page conventions; inspect the relevant page, not only a search snippet.
2. Write the full mathematical statement and all intended source hypotheses in original prose. Classify an added condition as source implicit, mathematically necessary, a genuine restriction or a technical formalization limit; never hide it.
3. Supply a complete stepwise formula proof. Compare all requested subparts with the exact compiled declarations and existing graph nodes. Reuse existing proofs; new substantive gaps follow normal theorem publication and independent semantic review.
4. Add a content-bound Bench rubric/review and family assignment. Distinguish an existing compiled exercise answer from a separately aligned Lean reconstruction challenge. Source/answer/graph/compiler/editorial statuses are separate.
5. Validate source links, code copy/download, tests, graph ownership and readable mathematics. Only admitted QA enters the reviewed prompt/reference export. Exercise variants/subparts/derived questions stay together for contamination control.
6. Continue the same process for *Log-Concave Sampling*, the cited *Statistical Optimal Transport* route and suitable exercises elsewhere in the seven domains. This first reuse lead is not coverage of those books.

The reference answer should be complete, independently checked and easy to study; equivalent valid proofs receive credit. No unmeasured claim that an answer is uniquely “best” is made.
