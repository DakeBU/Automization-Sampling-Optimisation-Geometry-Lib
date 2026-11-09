# Exercise 1.7: compact PI Bench draft, revision 2

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
limits. In particular, establish integrability of \(f\), its squared centered
value, and \(\|\nabla f\|^2\); do not assume that \(f\) already has mean zero.

Suggested level: L4, provisional. The task combines centering, extension of
the test domain and distinct dominated limits; the number of proof lines is
not evidence of difficulty. In a closed-book run give only the prompt and
the mathematical definitions above. In a library-assisted run supply a
separately pinned retrieval context; report the two settings separately.

## Grader only: four binary criteria

Use the [reference proof](compact-pi-candidate-v1.md). Each criterion is 1
only when its mathematical evidence is present, otherwise 0. Report the
four flags separately; all four are necessary for a complete solution.

| Criterion | Required evidence for 1 |
| --- | --- |
| Integrability and centering | Establishes integrability of the original \(f\), its centered square, and \(\|\nabla f\|^2\); centers \(f\) and proves mass one for a positive small affine perturbation. One argument may cover multiple integrability obligations. Derivative support is a valid route, not a mandatory phrase. |
| Legitimate LSI test domain | Justifies the use of the actual square-root test via cutoffs or another valid domain argument without assuming a stronger LSI. In a library-assisted run, an allowed domain extension plus checked hypotheses suffices. |
| Entropy limit | Justifies entropy normalization, cancellation of the linear term, and the \(1/2\) coefficient using domination or an equivalent integrated uniform remainder. Direct expansion of \(p\log p\) is as valid as compensation. |
| Energy limit and PI | Justifies the genuine square-root energy limit with coefficient \(1/4\), passes the inequality using only positive squared parameters, recovers the original variance/gradient, and obtains \(C\) with no stronger premise. |

For the domain criterion, a valid cutoff key is to set \(u=\sqrt p\) and
test the premise on \(\chi_R u\). Choose \(\chi_R=1\) on the radius-\(R\)
ball, zero outside radius \(2R\), between zero and one, with gradient
bounded by \(K/R\). Boundedness of \(u\) and continuity of \(t\log t\)
at zero justify the mass and entropy terms by domination. In the gradient
difference
\[
 \nabla(\chi_R u)-\nabla u=(\chi_R-1)\nabla u+u\nabla\chi_R,
\]
the first term tends to zero in \(L^2(\mu)\) by domination; the second
does so by the derivative bound and boundedness of \(u\) on the probability
space. Thus all parts of LSI pass to the actual test.

A positive-sided limit is valid for this PI task. Neither the standalone
actual-law KL theorem, a proof that centering preserves function support,
nor equality of optimal constants is required. Applying the compact
premise directly to a generally noncompact square root does not receive
domain credit even if later algebra is correct.

## Future tool profiles

In prompt-only prose runs, export only the mathematical prompt and
definitions, with no external retrieval. Library-assisted prose requires
separately pinned eligible retrieval, no answer copies, and separate
reporting. An answer-excluded Lean run must pin Lean, allowed imports and
their transitive context, and declare/enforce search and compiler tools.
Exclude the finished answer through imports, file search and retrieval.
Do not give the agent this rubric, reference links, or reviewer evidence.
An open-web or answer-access run is a different profile. No restricted
ATLAS material may enter a prompt or context. No such run is claimed here.

## Candidate Lean and graph views

The [frozen exact Lean target](compact-pi-statement-v1.lean.txt) adds explicit
`Poincare.Admissible` to the formal conclusion, matching the three required
integrability conclusions. A future
agentic prompt may allow the compiled cutoff-extension, perturbation-energy,
square-root-domain and compensated-entropy producers, but not import the
exercise's finished module into the proof environment. Keep the checked
reference solution separate from the prompt and do not expose it through a
permitted lookup channel in an assessment claiming no such access.
Proposed library-assisted Lean level: L4, provisional, because the task must
connect the genuine noncompact domain, both limits and the compact target.

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
