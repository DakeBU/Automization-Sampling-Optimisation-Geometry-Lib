---
name: astis-proof-dag
description: Plan and review ASTIS proof work as reusable Lean proof DAGs instead of repeated flat proof traces.
metadata:
  argument-hint: "[task id or Lean theorem]"
---

# ASTIS Proof DAG

Use this when a proof target has repeated analytic or formalization subblocks.

Methodological rule: do not eliminate useful cuts.  Sonoda--Akiyama--Uezato
show in arXiv:2602.10512 that hierarchical theorem provers can be far more
sample-efficient than flat provers when repeated subproofs are represented as
reusable DAG nodes.  For ASTIS this means a repeated KL derivative,
weak-Fokker--Planck, measurability, integrability, Hessian-bound, or
discretization lemma should become a named block, not an inlined proof script.

Efficiency rule: use the statistical-provability framing of arXiv:2602.10538
when judging a run.  A six-hour cycle is useful if it raises the finite-budget
chance of closing a verified Lean proof, shortens the average future proof
route, or improves coverage of high-mass proof states.  Wrapper churn that does
not retire a blocker should be recorded as waste.

## Typical Blocks

- measure definitions and density normalization;
- KL/FI/LSI/PI interfaces;
- Donsker--Varadhan and entropy duality;
- Gronwall or differential inequality integration;
- Fokker--Planck and continuity-equation identities;
- Euler--Maruyama one-step and accumulated discretization error;
- predicted-clean or guide-surrogate error decomposition;
- SMC/Feynman--Kac particle approximation.

## Canonical graph records

Reuse the current Frontier Cell, Registry, source obligations and publication
bindings. Do not copy their status/dependency tables into a second ledger.
For a new proof plan, keep only the missing interfaces and strict boundaries in
the existing proof-obligation file. At publication, follow the graph section of
`docs/theorem-publication-protocol.md` and inspect the affected local view.

## Protocol

- One SAU owner chooses a dependency-ready block and implements its interface.
- The existing independent verifier checks hidden assumptions and truth edges;
  graph-only changes do not require a new mathematical reviewer.
- The stabilization owner regenerates affected views from canonical records.
- Classify failed routes as a missing reusable interface, source gap, retired
  route or typed blocker. Do not restore the legacy role ladder just for graphs.

In `faithfulPaper` mode, the DAG decomposes the paper proof only. It must not
add hypotheses, change constants, or replace the theorem target.

In `exploratoryProof` mode, ASTIS may use a Conjecturing-Proving-Loop style
split: generate candidate analytic lemmas or proof-route statements, filter
them by Lean syntax and domain assumptions, then prove only the survivors.
Verified survivors should be fed back into later context packs as examples.
