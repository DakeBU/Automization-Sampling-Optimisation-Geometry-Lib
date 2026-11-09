# Exercise 1.7: compact PI Bench draft

Scope: Chewi's [Exercise 1.7](https://chewisinho.github.io/main.pdf#page=55)
in the [compact Euclidean setting](https://chewisinho.github.io/main.pdf#page=60).
Original restatement and grading plan. This draft is not in any export and
has no catalog ID, admission, empirical difficulty or model result.

Proposed family: `chewi-lcs-2026-08-20-exercise-1-7`. Any public views of the
compact implication, the same exercise's standalone KL expansion, and
near-duplicates of its linearization must stay in this family. Do not use a
publicly exposed family as a private evaluation family.

The [actual-law KL expansion](actual-kl-candidate-v1.md) is a distinct
mathematical result within the same family. If offered as a separate task,
require the actual tilted probability, finite extended-real KL, and the
quadratic coefficient with a valid little-o remainder. An answer about a
compensated integral alone does not certify that task; conversely the
compact PI target below does not require calling the actual-law theorem.

## Natural-language prompt

Let \(\mu\) be a Borel probability measure on a finite-dimensional real
Hilbert space. For every compactly supported smooth real \(v\), assume
\[
  \operatorname{Ent}_\mu(v^2)\le 2C\int\|\nabla v\|^2\,d\mu,
  \qquad
  \operatorname{Ent}_\mu(q)=\int q\log q\,d\mu
        -\Big(\int q\,d\mu\Big)\log\Big(\int q\,d\mu\Big),
\]
where \(0\log0=0\) and \(C\) is fixed. Prove by linearization that every
compactly supported smooth \(f\) satisfies
\[
  \operatorname{Var}_\mu(f)\le C\int\|\nabla f\|^2\,d\mu.
\]
Use the square root of a mass-one affine perturbation built from \(f\).
Justify its admissibility as an LSI test and justify the integrals and
limits; do not assume that the original \(f\) already has mean zero.

Suggested level: L4, provisional. The task combines centering, extension of
the test domain and distinct dominated limits; the number of proof lines is
not evidence of difficulty. In a closed-book run give only the prompt and
the mathematical definitions above. In a library-assisted run supply a
separately pinned retrieval context; report the two settings separately.

## Grader-only draft

Use the [reference proof](compact-pi-candidate-v1.md), not exact wording.
The proposed ten points are independently reviewable:

| Points | Required evidence |
| --- | --- |
| 2 | Centers an arbitrary \(f\), proves mass-one perturbation, and retains derivative support without claiming that centering preserves function support. |
| 2 | Makes the perturbation positive for small parameters and justifies applying compact-test LSI to the actual test, by cutoffs or another valid domain argument with control of all terms. |
| 2 | Cancels the entropy normalization and compensation; justifies the quadratic entropy limit with coefficient \(1/2\) and an integrable bound. |
| 2 | Derives the true square-root energy and its \(1/4\) coefficient, with domination or another valid integral-limit argument. |
| 2 | Divides only by a positive squared parameter, passes the inequality to the limit, recovers the original variance/gradient, and preserves \(C\). |

A one-sided positive-parameter limit is valid. A proof that applies the
compact LSI directly to a generally noncompact square root cannot receive
the domain points; an unsupported factor, assumption of the target PI, or
replacement of the given measure by a Gaussian is not a complete answer.
The task is not asking for equality of optimal constants or a semigroup PI.

## Candidate Lean and graph views

The [frozen exact Lean target](compact-pi-statement-v1.lean.txt) adds explicit
`Poincare.Admissible` to the conclusion, not to the assumptions. A future
agentic prompt may allow the compiled cutoff-extension, perturbation-energy,
square-root-domain and compensated-entropy producers, but not import the
exercise's finished module into the proof environment. Keep the checked
reference solution separate from the prompt and do not expose it through a
permitted lookup channel in an assessment claiming no such access.

The local proof-body probe confirmed direct occurrences of those four owned
producers. A graph view may ask which path reuses the Gaussian cutoff proof
within an explicitly induced compiled slice; that path does not establish
mathematical necessity. Wait for canonical publication and a fresh exported
graph, answer equivalence, exact replay and separate editorial review before
admitting any of these views. Do not describe the draft as a runnable task.

A source-faithful comparison is available for a later two-target slice:
the compact PI proof and the actual-law KL proof both directly call
`BoundedDensityPerturbation.tendsto_integral_klFun_one_add_mul_div_sq`.
Only the KL branch uses the actual-law identity; only the PI branch uses the
square-root energy and cutoff-LSI extension. Ask for the shared producer in
the supplied slice, not whether either theorem mathematically entails the
other. Keep the explicit source use by Corollary 2.1.2 as a source edge until
there is a corresponding compiled theorem body.
