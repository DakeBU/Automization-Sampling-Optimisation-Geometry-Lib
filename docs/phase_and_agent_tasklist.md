# ASTIS Phase And Agent Task List

ASTIS follows the public Quantum automation reference:
https://github.com/DakeBU/Quantum-Computing-Block-Encoding/tree/wip/ghl2025-faithful-20260518-0201

ASTIS also records MathCode as a workflow reference for proof diagnostics and
theorem reuse discipline:
https://github.com/math-ai-org/mathcode

ASTIS also attributes and studies LeanMarathon as a Lean-specific long-horizon
autoformalization reference:
https://github.com/YuanheZ/LeanMarathon
and its paper:
https://arxiv.org/abs/2606.05400

The domain is different.  ASTIS formalizes SDE/Sampling theory, so the shared
objects are laws, densities, transport velocities, scores, guide tilts,
Fokker--Planck identities, KL/FI/LSI/PI interfaces, Euler--Maruyama
discretization, and particle approximations.

## Phase 1: Faithful Transcript

Phase 1 is the priority for `ASTIS-SALD-001`.

- Reproduce the original VA-SALD paper
  [arXiv:2605.07950](https://arxiv.org/abs/2605.07950) faithfully.
- Keep theorem statements, constants, hypotheses, and source proof order fixed.
- Map every source theorem, definition, equation, and proof step to a Lean
  declaration, cited-result row, or `ProofObligation`.
- Prefer narrow obligation refinement over broad proof search when an analytic
  backend is missing.
- Keep the source index, conversion window, proof obligations, technical lemma
  memory, SLT port audit, and proof DAG synchronized.
- Keep paper contribution memory separate from technical lemma memory:
  `research-wiki/paper-memory/<task>/` stores task-specific source-line
  leaves and proof DAG state, while `research-wiki/technical-lemma-memory/`
  and `AutoSamplingTheory/TechnicalLemmas/` store reusable prior facts.

## Current Single-Backend Backfill Sprint

The SALD theorem-skeleton route is now stable enough that the next long runs
should not spend most cycles on rebaseline/source-index work, isolated scalar
sublemmas, or broad theorem-route restatement.  Upper and middle must focus on
one shared analytic backend until it either compiles locally or is reduced to a
minimal source-cited interface.

The active backend is the Euler--Maruyama interpolation conditional-law / weak
Fokker--Planck interface:

- primary Lean route: `sald.general_moving_target_discrete.em_interpolation_fp`;
- source window: `appendix.tex:1358-1387`;
- theorem consumers: `thm:forward-KL-discrete` and
  `thm:general-moving-target-SALD-discrete`;
- allowed reference material:
  ASTIS `AutoSamplingTheory/TechnicalLemmas` first; external
  `lean-stat-learning-theory` files only as port/provenance sources, never as
  callable dependencies.

Lower work should follow this order:

1. conditional-law/measurability and named conditional drift interfaces;
2. endpoint-law-to-conditional-law compatibility;
3. weak conditional Fokker--Planck source-sign statement;
4. KL-derivative handoff from the weak FP identity;
5. only if blocked, a narrow source-cited Mathlib/measure-theory interface.

Before attempting local background analysis, every slow analytic backend must
exist as a precise source-cited Lean interface with explicit hypotheses and a
non-formalized status:

1. Gronwall with endpoint-safe differentiability/FTC assumptions.
2. Donsker--Varadhan with common-space, absolute-continuity, finite-KL, and
   finite-log-mgf assumptions.
3. LSI-to-KL/FI with density, zero-set, admissible-test, entropy, and Fisher
   chain-rule assumptions.
4. Continuous forward-KL Fokker--Planck/KL derivative identity.
5. Euler--Maruyama interpolation Fokker--Planck endpoint/conditional-law
   backend.

Once those interfaces are explicit, the cycle work should wire them into the
faithful theorem skeletons in this order:

1. `thm:forward-KL`.
2. `thm:forward-KL-discrete`.
3. `prop:guided_path_residual`.
4. `thm:general-moving-target-SALD`.
5. `thm:unified-forward-KL`.
6. `thm:general-moving-target-SALD-discrete`.

The theorem skeletons may remain `contractOnly` or depend on
`sourceCited`/`obligation` interfaces; reviewer must reject any upgrade to
`formalized` that is not backed by compiled local proofs.  Systematic
measure-theory and SDE backfill, including material guided by
`/workspace/repos/outer_papers/sampling_theory_sde/Statistical Learning Theory in Lean 4 Empirical Processes from Scratch`
and `YuanheZ/lean-stat-learning-theory`, comes
after this theorem skeleton is stable.

## Post-Cycle-84 Closure Sprint

Cycles 70--84 completed the faithful EM-backend transcript through endpoint
conditional readiness, weak-FP source signs, and KL/log-ratio handoff.  The
remaining risk is no longer missing source-to-Lean naming.  It is that many
compiled declarations are still supplied-hypothesis wrappers.  The next run
must therefore discharge or sharply narrow the hypotheses instead of adding
more wrappers of the same shape.

Use this priority order:

1. Prove or narrowly isolate the conditional-kernel theorem behind
   `appendix.tex:1368-1377`: Mathlib `condDistrib`/`condExpKernel`, named
   `hat rho_s` marginal, component conditional-integral fields, and
   measurability/integrability of `bar b_{k,s}`.
2. Prove or narrowly isolate the generator-to-law weak Fokker--Planck theorem
   behind `appendix.tex:1379-1387`: weak-test `Measure.map` integral
   derivative, generator action, drift source sign, diffusion source sign, and
   coefficient `sigma_eta^2/2`.
3. Prove or narrowly isolate the KL/log-ratio boundary behind
   `appendix.tex:1358-1366`: KL differentiability, log-ratio admissibility,
   integration by parts, FI identification, and weak-FP action substitution.
4. Run a theorem pressure test for `thm:forward-KL-discrete` after one supplied
   EM hypothesis has been removed or narrowed.
5. If and only if the EM backend is blocked by a named Mathlib/theory gap, move
   one cycle to the smallest LSI/DV/Gronwall backend needed by theorem closure.

- Local references to consult before inventing declarations:

- `research-wiki/paper-memory/ASTIS-SALD-001/unfinished_source_map.md` for
  SALD-specific source-line leaves and the next smallest unfinished boundary.
- `AutoSamplingTheory/TechnicalLemmas/Gaussian.lean`,
  `AutoSamplingTheory/TechnicalLemmas/Taylor.lean`, and
  `AutoSamplingTheory/TechnicalLemmas/Registry.lean` for compiled local
  technical lemmas.
- `research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl` for
  searchable local lemma names and tags.
- `research-wiki/technical-lemma-memory/SALD_remaining_map.md` for the current
  SALD remaining-leaf mapping.
- `research-wiki/technical-lemma-memory/SLT_port_queue.jsonl` for upstream
  theorem shapes that still need ASTIS-owned ports before use.
- External `lean-stat-learning-theory` files only after the local memory search
  fails, and only to create a local port or a precise proof obligation.
- Mathlib `Probability.Kernel.CondDistrib`, `Probability.Kernel.Condexp`, and
  `Analysis/Calculus/ParametricIntegral` for the actual measure/SDE theorem
  boundaries.

Every lower packet after cycle 84 must be tagged in the handoff as
`discharges-supplied-hypothesis`, `narrows-source-cited-boundary`, or
`rejected-wrapper-churn`.  Reviewer should reject wrapper churn: a new wrapper
is acceptable only if it removes an older supplied hypothesis, exposes a
strictly smaller missing theorem, or compiles a real local proof.

## Efficiency And Self-Reflection Guard

The system should not use six-hour runs to rediscover already recorded
blockers.  For SALD cycles after cycle 84, each generated run directory has a
`05_context_pack.md`; upper, middle, lower, and reviewer should use it as the
main context instead of replaying full task history.

At the start of each cycle:

1. Upper reads only the compact context pack, blueprint, TODO, and paper
   memory summary, then names the active blocker.
2. Middle checks task-local paper memory first, then existing ASTIS
   declarations, technical lemma memory, proof obligations, and cited-result
   ledgers before inventing a new interface.
3. Lower states the packet classification and exact source-line leaf or
   technical-lemma registry entry before editing Lean.
4. Reviewer rejects the cycle if it lacks a classification, repeats a wrapper,
   cites a non-compiled technical lemma as proved, or claims completion without
   concrete source-line coverage.

Use the efficiency report after every long run:

```bash
python3 tools/astis.py efficiency-report
```

Use the LeanMarathon-inspired proof blueprint before choosing the next proof
packet:

```bash
python3 tools/astis.py blueprint-refresh ASTIS-SALD-001
```

High token use is only acceptable when it buys one of the two useful progress
signals: a supplied hypothesis is discharged, or a source-cited theorem
boundary is strictly narrowed.  The local technical lemma memory is the
callable source; the SLT project and article are proof-engineering references
for future local ports, not unchecked imported facts.

## LeanMarathon-Inspired Control Loop

ASTIS keeps the EoH candidate-population layer for `exploratoryProof`, the
Learning-beyond-gradients trial-memory layer, and the auto-research-in-sleep
long-window upper/middle/lower/reviewer runner, but adopts the following
LeanMarathon controls:

- Blueprint system of record: the generated proof blueprint summarizes the
  current Lean/source/proof-obligation/trial state; the status JSON keeps the
  compact machine-readable control summary.
- Target review discipline: a cycle must prove no less and no more than the
  source theorem or the named proof obligation.
- Dynamic leaf discharge: upper should choose a local proof packet whose
  dependencies are already represented, rather than reopening broad proof DAGs.
- Illness-area refiner: if the blocker propagates through a connected sub-DAG,
  middle names that local affected region and lower avoids unrelated edits.
- Deterministic gate: `python3 tools/astis.py check` is the only progress
  authority; agent confidence is not enough.

For SALD after cycle 173, the generated proof blueprint should be treated as
the current system-of-record snapshot.  The expected next packet is the
source-Hessian leaf behind
`SALD.selectedWeakTestHessianOpNormOfSourceHessianField`: either prove or
strictly narrow the two fields
`hSourceHasHessian : forall z, HasFDerivAt (fderiv Real sourceTest)
(sourceHessian z) z` and `hSourceHessianBound : forall z, norm
(sourceHessian z) <= C1`.  If those fields are not actually supplied by the
source paper's selected weak-test regularity, the system must record that as a
source-contract gap and move only to the next connected Brownian/Ito leaf
inside the same backend: selected-line Taylor domination, Gaussian dominated
convergence integrability, quadratic-variation normalization, or
per-coordinate Hessian generator identity.

Mode boundary: `faithfulPaper` may keep failed proof attempts and negative
caches for a fixed theorem, but must not use EoH-style mutation to change the
paper construction.  EoH-style populations belong to PRIVATE-like
`exploratoryProof` tasks after the target predicate is explicit.

## Phase 2: Reorganization And Reuse

Phase 2 begins only after the faithful transcript is complete.

- Reorganize shared SDE/Sampling APIs for future papers.
- Add teaching-friendly structure for users who want to reproduce their own
  sampling or SDE proofs.
- Support `exploratoryProof` mode for active projects such as PRIVATE.
- Refactor repeated proof blocks into reusable Lean interfaces only after the
  Phase 1 source correspondence is stable.

## Upper Agent

- Choose the mode and phase for the cycle.
- Start every cycle with a global phase judgment: previous-cycle recovery,
  Phase 1 skeleton stability, and whether a cited-theory backfill is now
  justified.
- Choose one source theorem or proof block.
- In the current sprint, keep the lower packet on the active EM
  conditional-law/Fokker--Planck backend unless reviewer found a blocking defect
  in a theorem route.
- After cycle 84, prefer proof-producing or boundary-narrowing work over new
  supplied-hypothesis wrappers.  State which supplied hypothesis is being
  discharged or narrowed.
- After the LeanMarathon-inspired update, choose either the current dynamic
  leaf or a named illness-area refiner packet from `blueprint-refresh`.
- If the previous cycle failed after an upper or middle handoff, recover that
  cycle first instead of advancing to a fresh source target.
- State non-goals, especially what must not be reorganized during Phase 1.
- Give middle a source-to-Lean translation objective.
- Give lower one narrow target.
- Give reviewer a checklist for source correspondence, fake proof closures,
  cited results, and phase discipline.

## Middle Agent

- Maintain the two-way conversion layer.
- Before lower work, translate source LaTeX/Markdown proof steps into Lean
  declarations, cited-result rows, or obligations.
- In the current sprint, avoid fresh theorem-route audits unless needed for
  source correctness.  Convert only the active EM conditional-law/Fokker--
  Planck source slice into lower-ready Lean declarations.
- After cycle 84, classify each proposed lower packet as
  `discharges-supplied-hypothesis`, `narrows-source-cited-boundary`, or
  `rejected-wrapper-churn`.
- State whether the packet is dynamic-leaf worker work or illness-area refiner
  work, and keep the lower-ready declarations inside that local region.
- Consult ASTIS technical lemma memory before inventing a new abstraction.
  External SLT files may be inspected only as port references, and never
  imported as dependencies.
- Follow the MathCode-inspired reuse rule: search existing ASTIS declarations,
  `AutoSamplingTheory/TechnicalLemmas`, conversion windows, proof obligations,
  cited-result ledgers, and port queues before creating duplicate interfaces.
- After lower and reviewer work, translate the Lean state back into Markdown
  and LaTeX notes.
- Maintain `conversion-windows/`, `proof-obligations/`,
  `research-wiki/cited-results/`, and `research-wiki/source-index/`.
- Export the project LaTeX and external technical-report snippets only at the
  end of a multi-hour batch, after the final reviewer gate.
- Treat the report-writing pass as a middle-agent responsibility inherited
  from the ARIS-style paper-writing workflow: explain what Lean proved, what
  remains a named obligation, why the remaining boundary is mathematically
  meaningful, and which coordination rules should guide the next upper/middle
  cycle.

## Lower Agent

- Work on one Lean declaration, proof block, source-index update, or obligation
  refinement.
- Do not change theorem targets, constants, or assumptions in faithful mode.
- Do not close analytic content with fake proof patterns.
- If an analytic fact is not formalized, record or refine a `ProofObligation`
  and keep the build green.
- After cycle 84, do not add a new supplied-hypothesis wrapper unless it
  removes an older supplied hypothesis, exposes a smaller theorem boundary, or
  proves a local theorem using Mathlib/local SLT-style ingredients.
- For worker-style packets, first attempt a local refinement inside the
  assigned target before asking for upstream changes.  For refiner-style
  packets, touch only the connected illness area named by middle.

## Reviewer Agent

- Run or verify `python3 tools/astis.py check`.
- Run or inspect `python3 tools/astis.py proof-diagnostics` when a cycle makes
  broad Lean edits or claims proof progress.
- Reject source drift, hidden assumptions, overstated cited-result status, and
  fake proof closures.
- Treat hidden `axiom`, `constant`, `postulate`, `sorry`, `admit`,
  `Prop := True`, and `:= trivial` closures as blocking defects.
- Check that Phase 1 work remains a faithful transcript rather than a broad API
  redesign.
- Confirm that the conversion window and proof-obligation ledger describe the
  actual Lean state.
- After cycle 84, reject wrapper churn and require handoffs to name the exact
  supplied hypothesis discharged or the exact missing theorem boundary.
- After the LeanMarathon-inspired update, also reject cycles that do not name
  the dynamic leaf or illness area, or that rely on agent self-assessment
  instead of the deterministic ASTIS gate.
