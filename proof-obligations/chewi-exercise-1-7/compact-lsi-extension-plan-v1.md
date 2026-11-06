# Compact-test LSI extension: canonical reuse preflight

Status: **proposal, not a Statement Seal, proof, verified Cell or admitted QA**.
Author: `agent-task:/root`, 2026-11-06. This does not change the current Goal,
paper priority, Exercise 1.7 source topology or any existing theorem statement.
Implement only after the separate model-bridge integration lane is settled.

## Exact mathematical boundary

Let `E` be a finite-dimensional real inner-product space, `mu` a Borel measure,
and `C` a real constant. Assume the function-form inequality

\[
 \operatorname{Ent}_{\mu}(v^2)
 \leq 2C\int \|\nabla v\|^2\,d\mu
 \qquad(v\in C_c^\infty(E)).
\]

For every genuine `C^infinity` real function `u` with `u` and `gradient u` in
`L^2(mu)` and `u^2 log(u^2)` integrable, derive this same inequality for `u`.
Here `Ent_mu(q) = integral(q log q) - (integral q) log(integral q)` and
`0 log 0 = 0`. No probability, nonzero mass, positivity of `u`, log-concavity,
canonical RN representative or existence of a semigroup is assumed. A sign
assumption on `C` is not needed merely to pass inequalities through these real
limits; the eventual source PI consumer fixes its own positive source constant.

These analytic-domain inputs belong to a **canonical extension lemma**, not to
the final source Exercise 1.7 Anchor: its consumer must derive them internally.
Preserve the compact-`C^infinity` test class; a compact-`C2` hypothesis would be a
stronger assumption than the selected source starting point.

## Existing mathematics to reuse, not reprove

- `GaussianLogSobolev.lean` already contains the private measure-generic
  `cutoff_integral_limits`, with its entropy dilation, genuine gradient product,
  uniform energy envelope and local-plateau arguments. It is **not** a
  Gaussian-only analytic result. Preserve discovery
  `ASTIS-DISC-20261105-GenericCutoffLimitsAlreadyPrivate`.
- `Cutoff.radialSmoothCutoff_*` supplies smoothness, range, compact support in
  finite dimension, exhaustion and the scale-uniform first derivative bound.
- `CompactGradientSqrtPerturbation.eventually_contDiff_and_integrable_sqrt_perturbation`
  already supplies the actual source square-root test's smoothness and finite
  integrals. The energy and probability/KL producers already exist separately.
- The `LogSobolev`/`Probability` module cards' certificate bookkeeping does not
  discharge the compact-test domain extension. Mathlib's continuous compact
  support/Lp APIs alone do not prove simultaneous entropy and gradient limits.

**Preferred canonicalization:** move the existing generic cutoff proof and its
implementation-private helpers to one shared functional-inequality module;
expose its generic limit interface once. Make the unchanged public Gaussian
theorem use that interface. Then use the same limits with compact smooth
cutoffs of `u` to prove the extension above. Do not introduce a copied second
cutoff proof, access mangled private names, or count relocation as new
mathematics. The real second consumer is the existing Gaussian LSI producer,
not an invented future application.

## Proof and interface preparation

1. Inspect the existing helper's fully elaborated type before fixing imports,
   typeclasses and exact public names. Keep this plan explicitly unsealed until
   those signatures and definition semantics have been checked.
2. Use `u_n = radialSmoothCutoff (n+1) * u`; each is compact `C^infinity`.
3. Reuse the three actual limits for mass, `q log q` and squared gradient.
   The energy envelope is `2 norm(gradient u)^2 + 2 K^2 u^2` with the existing
   cutoff constant `K`, not a newly assumed convergence premise.
4. Pass the normalization term through the continuous function `q log q`,
   including zero mass. Pass `2*C` times energy through its real limit.
5. Apply the source compact-test inequality to each `u_n`, then closedness of
   real order. No canonical Fisher/score differentiability is used.

## Necessary migration audit before editing old source

Moving helpers changes the entire old Gaussian module's source fingerprint,
even if its public statement and mathematics are unchanged. Inventory affected
publication contexts, semantic audits, compiler graph snapshots and Bench QA
source/import-closure bindings **before** implementation. Reuse only unchanged
evidence; source-bound reviews must be renewed where their actual inputs change.
Do not hand-refresh hashes and replay old verdicts, manufacture another core ID,
hide stale questions, or migrate their public-dev families/splits.

## Source correspondence and remaining boundary

The accepted source-only plan and v2 review in this directory pin Chewi,
*Log-Concave Sampling*, August 20, 2026, PDF SHA256
`8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`.
The compact-test conventions are Section 2.1.1, printed48/PDF60; the density
extension omission is printed49/PDF61. This is an ASTIS-authored proposed
expansion, not quoted textbook prose or source completion.

After this lemma, the actual square-root application, entropy/energy limits,
uncentering, compact Euclidean PI, and wider form-domain/abstract Exercise 1.7
remain separately evidenced obligations. Canonical RN score/Fisher domains do
not follow from a.e. density equality. No QA, Registry, graph or chapter credit
is awarded by this preflight. Independent canonicality/mathematical review and
the normal exact-signature/semantic/publication gates are still required.
