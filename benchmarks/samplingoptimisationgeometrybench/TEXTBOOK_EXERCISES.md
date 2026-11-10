# Textbook exercises: source-to-answer intake

This programme is required by the Bench Goal. It supplements, rather than relabels, original library-grounded QA. **Intake itself is not admission**, a model result or whole-exercise certification. The source snapshot below is historical provenance; current per-question admission and owned-answer build state are generated from the catalog, exact reviews and compiler receipt in textbook-exercise-map.json.

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
| Source snapshot | Primary text and whole relevant PDF page visually checked. The typed Bench entry is sogb-029; current editorial/compiler states are separately derived, not hand-copied into this table. |

The source asks for the Hessian/segment-FTC route to a uniform gradient-map contraction, the balanced step 2/(α+β), and the factor (κ−1)/(κ+1). The section explicitly assumes C² regularity. The condition-number expression needs positive α; distinguish that source-implicit regime from the separate α=0 nonexpansive extension in the library. The minimization is of the **uniform curvature-endpoint envelope**, not the best actual constant for every individual objective. Do not add a minimizer premise or claim an iterate/oracle-complexity theorem.

Existing owned declarations, both confirmed as compiled declaration nodes in the current source-derived graph:

- [AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.gradient_step_endpoint_bound](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/underlying-lean-graph/index.html?focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.gradient_step_endpoint_bound)
- [AutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.optimal_gradient_step](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/underlying-lean-graph/index.html?focus=decl%3AAutoSamplingTheory.TechnicalLemmas.Analysis.GradientDescentOptimalStep.optimal_gradient_step)

Use their existing cells, tests, canonical source/semantic reviews and module ownership; do not create duplicate wrappers for the Bench. The current APIs generalize the finite-dimensional source to complete real Hilbert spaces and expose parameter extensions. An exercise answer must disclose those differences and compare the exercise's requested subparts to the exact existing conclusions.

The PDF and HTML identify an arXiv non-exclusive distribution grant, not a blanket text/solution-manual reuse license. Keep the original PDF/page render in the ignored audit cache, outside ML exports. Publish only bibliographic correspondence and an original faithful mathematical restatement/ASTIS-authored solution unless broader permission is established. Do not distribute a copied exercise passage as project-owned text.

## Optimisation Exercise 3.1: three steps, two pages

[Exercise 3.1, printed/PDF pp. 22–23](https://arxiv.org/pdf/2605.07006v1#page=22)
uses the same pinned edition; the last part is at the
[top of p. 23](https://arxiv.org/pdf/2605.07006v1#page=23).
The reference answer (sogb-030) follows the affine tilt, then the sum of the
two endpoint gaps, then Cauchy–Schwarz. It does not assume a Lipschitz
gradient in the quadratic upper-model premise. The reciprocal expression
needs positive modulus; the division-free and Lipschitz conclusions extend
to zero, and no Hessian is required. The exercise map names all three
existing `ConvexSmoothGradient` answers and preserves the Euclidean versus
Hilbert-space distinction. This is an NL exercise with owned Lean answers,
not another fixed Lean reconstruction task. Both source pages were rendered
and checked against the original wording; no source prose is reproduced.

## Next real source route: Log-Concave Sampling Exercise 1.7

The pinned August 20, 2026 edition has 333 pages and SHA-256
`8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`.
[Exercise 1.7 / (1.E.1)](https://chewisinho.github.io/main.pdf#page=55)
is on printed p.43 / PDF p.55. Corollary 2.1.2 explicitly reuses the same
expansion on printed p.50 / PDF p.62. The entire relevant exercise page and
the PI/LSI conventions were inspected, not just a search snippet.

This is **not another admitted QA**. The first actual prerequisite is tracked by
`ASTIS-SHARED-bounded-density-kl-linearization`: the compensated-entropy integral
limit for a finite measure and a uniformly a.e.-bounded measurable real test.
Its exact Lean signature, actual compiler checks, semantic audit and later
integration state are separate evidence. Do not infer a full exercise answer
from that prerequisite.

The immutable source-only proposal/review and corrected successor are retained
under `proof-obligations/chewi-exercise-1-7/`. Their topology review is not a
Lean proof or a source-equivalence verdict. In particular:

- Centering a compact test generally destroys compact support of the function;
  its gradient stays compactly supported. The second consumer uses this broader
  bounded smooth compact-gradient class.
- The probability KL adapter must prove positivity, mass one, the actual
  Radon--Nikodym representative, finite KL and zero-mean cancellation.
- A positive perturbation is not automatically an admissible compact LSI test:
  its square root is noncompact. The LSI-domain extension and gradient-energy
  integrability/Fisher limit are explicit separate obligations.
- The compact Euclidean PI target and the broader chapter-1 form-domain or
  abstract reversible-semigroup conclusion must not be conflated. Same
  admissible constant means `C_PI <= C_LSI` for optimal constants, not equality.

The primary PDF contains no permission established here to redistribute its
prose as ML data. Keep the cached PDF/page renders out of exports and author
original mathematical statements and answers with exact correspondence.

For exercises with separate canonical source components, use
`publication_components` instead of `publication_file`. Each entry names a
`{publication_file, item_id}` with a proof-edge binding to the same pinned
book, chapter, and exercise. Do not conjoin distinct assumptions. The reader
lists the component corresponding to the current question's answer anchor
first; its source, hypotheses and graph links stay separate. An accepted
question credits only its component, not the other components or the
exercise's remaining mathematical obligations. All views share one source
family. Agent prompts receive only the bibliography.

## Transport intake: Chapter 1, Exercise 6

The next transport exercise candidate is Chapter 1, §1.8, no. 6 of
*Statistical Optimal Transport* by Chewi, Niles-Weed and Rigollet
([printed p. 44 / PDF p. 50](https://chewisinho.github.io/st_flour.pdf#page=50),
edition fingerprint in `Libraries/StatisticalOptimalTransport/source-map.json`).
The equal-weight and reweighted Gaussian mixtures have finite second
moments and means separated by `m/2`. The source hint uses the 1-Lipschitz
test `f(x) = -x`, then the probability-coupling Cauchy–Schwarz bound.
For the upper bound, couple the common left quarter and right half on
the diagonal; translate the remaining left quarter by `2m` using the
same Gaussian noise. The candidate squared cost is `m²`. Mathlib has
Gaussian means, L² and translation APIs, and the owned Wasserstein upper
bridge accepts an actual coupling. The unbounded-test lower bound and
actual mixture coupling/marginals still need proof; the bounded-feature
transport lemma is not a substitute. No QA or Lean coverage is claimed yet.

## Admission checklist

1. Pin the actual work, author(s), edition/hash, number/subparts and both page conventions; inspect the relevant page, not only a search snippet.
2. Write the full mathematical statement and all intended source hypotheses in original prose. Classify an added condition as source implicit, mathematically necessary, a genuine restriction or a technical formalization limit; never hide it.
3. Supply a complete stepwise formula proof. Compare all requested subparts with the exact compiled declarations and existing graph nodes. Reuse existing proofs; new substantive gaps follow normal theorem publication and independent semantic review.
4. Add a content-bound Bench rubric/review and family assignment. Distinguish an existing compiled exercise answer from a separately aligned Lean reconstruction challenge. Source/answer/graph/compiler/editorial statuses are separate.
5. Validate source links, code copy/download, tests, graph ownership and readable mathematics. Only admitted QA enters the reviewed prompt/reference export. Exercise variants/subparts/derived questions stay together for contamination control.
6. Continue the same process for *Log-Concave Sampling*, the cited *Statistical Optimal Transport* route and suitable exercises elsewhere in the seven domains. This first reuse lead is not coverage of those books.

The reference answer should be complete, independently checked and easy to study; equivalent valid proofs receive credit. No unmeasured claim that an answer is uniquely “best” is made.
