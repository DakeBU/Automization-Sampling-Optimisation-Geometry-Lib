# Actual proximal-query expected work

Source: Chen, Chewi, Lu and Zhang, arXiv:2609.06906v1, Appendix D.2,
the Jensen step in Lemma D.4 after (D.7), before the final phase-count argument.
Primary source checked 2026-09-29 at https://arxiv.org/html/2609.06906v1#A4.SS2.

## Frozen edge

Keep the hypotheses of `approximate_proximal_execution`, including full
`0 < eta <= c < 1`. For any probability measure nu with integrable
`y ↦ ‖gradient V y‖²`, construct the actual first-success count N and returned
iterate, retaining measurable stopping/output, the proximal equation, pointwise
accuracy and successful execution of `proximalQuery` with fuel N+1. Prove that
the actual gradient-query count N+1 is integrable and

\[
\mathbb E_\nu[N(Y)+1]\le C_c\left(1+\log\left(1+
\frac{\sqrt{\mathbb E_\nu\|\nabla V(Y)\|^2}}{\varepsilon}\right)\right),
\quad C_c=2+\frac{1+\log((1-c)^{-1})}{-\log c}.
\]

There is no supplied accurate-oracle assumption. The witness is obtained from
the existing actual execution theorem, not from an arbitrary count function.

## Reuse and route

1. Reuse `ApproximateProximalExecution.approximate_proximal_execution` unchanged.
2. `memLp_two_iff_integrable_sq` and `MemLp.integrable` give L1 gradient norm.
3. Dominate log(1+r) by r using `Real.log_le_sub_one_of_pos`; prove the log
   and then the measurable nonnegative actual count integrable.
4. Apply Mathlib's `ConcaveOn.le_map_integral` to log on the closed convex
   half-line [1,infinity), not the nonclosed positive half-line.
5. `variance_nonneg` and `variance_eq_sub` give the L1/L2 comparison. Monotonicity
   of log and the nonnegative explicit C_c finish the expectation estimate.

All generic inequalities are reused from fixed Mathlib. Route-local private
glue has no separate mathematical-leaf credit. Only the actual-execution
expected-work theorem is proposed as a new public declaration.

## Excluded claims

The actual Picard center law and (D.7) second-moment bound, approximate-proximal
stability D.1, the 2J per-phase counting, the parameter substitution in (D.8),
full sampling accuracy, and both papers' main theorems remain separate.
This packet does not transfer unbounded expected cost through TV proximity.

## Status

The module and focused test now compile (3488 build jobs, standard three Lean
axioms). The test uses a genuine Dirac input law, automatically proves its
gradient-moment integrability, and exercises eta=3/4 while retaining the real
interpreter equation and the derived pointwise bound. The root has not edited
shared imports or counted another Registry leaf.

Independent read-only mathematical review by `expected_work_math_review` found
no correctness blocker. The new statement retains the proximal equation,
measurable output, accuracy, actual execution, integrability and expected work;
explicit minimizer/earlier-failure conjuncts stay in the parent theorem rather
than being repeated here. The proof uses those parent's actual first-stop
witnesses. A five-step authored formula proof with adjacent folded Lean is in
`website/content/declaration_lessons/sphmc-proximal-expected-work.json`.

The exact commit `488d0bf5dc574e565ef427acecd17ec9dd26d8c4` is now
independently VERIFIED. Fresh direct elaboration of production and focused test,
publication binding, fake-closure scan and the source-reviewed semantic round
trip all pass; the source verdict is `equivalent-after-elaboration`. Do not
repeat mathematical implementation or count D.7/D.8 as completed.

Root stabilization now also passes the complete Tests target (9254 jobs), the
canonical ASTIS/ATLAS gate, publication and graph checks, a 12-chapter site build,
210 reader/protocol tests and actual desktop/mobile/local-graph inspection. Only
remote merge/deployment remain for this edge; the paper boundary is unchanged.
