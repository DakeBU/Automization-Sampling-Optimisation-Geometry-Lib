# Technical Lemmas

Canonical memory for reusable Sampling/SDE background facts: KL/FI/LSI, weak
Fokker--Planck, Ito/Taylor, Gaussian moments, measurability, integrability,
conditional laws, law-map rewrites, and integration-by-parts tools.

This folder is the skill memory for lower agents.  A lemma is callable only
when it is ASTIS-owned Lean code and the local gate covers it.  External Lean
projects such as lean-stat-learning-theory, lean-rademacher, MathCode, and
LeanMarathon are references or port sources; they are not silently treated as
local proofs.

## Memory Split

| Layer | What goes here | What does not go here |
|---|---|---|
| Technical lemma memory | General SDE/Sampling facts that can be reused across papers. | SALD-specific theorem statements or paper-only constants. |
| Paper contribution memory | A paper's own theorem leaves, source lines, and exact proof route. | Generic measure-theory, probability, or analysis facts. |
| Port queue | External declarations that look useful but are not yet ASTIS-owned. | Claims marked callable before they compile locally. |

## Required Leaf Packet

Every new reusable lemma should be accompanied by the template in
`mathlib_ready_leaf_template.md`.  The packet must name local APIs, intended
proof route, hidden regularity contracts, and failure policy.

## DAG Entry Points

- `research-wiki/lemma-dags/SDE_Sampling_skill_tree.md` gives the reusable
  skill tree.
- `research-wiki/lemma-dags/SALD_weak_fp_leaf_dag.md` gives the current SALD
  weak-Fokker--Planck leaf DAG and next lower-agent priorities.
- `hidden_regularities.md` lists reusable regularity contracts that should be
  pulled out of paper prose and made explicit.
