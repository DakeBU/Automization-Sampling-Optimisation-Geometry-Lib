# OpenAI Math coverage across the seven Samplinglib libraries

Status: audited external-source map, pinned to `openai/math` commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a` (2026-10-06).

The canonical data is
`research-wiki/openai-math-textbook-coverage.json`. The website, counts and
chapter-extension shelves are generated from that file. This document records
the placement rule and audit conclusion; it is not a second status ledger.

## Audit conclusion

Commit `01851dc0a799731158b9981088b16521e9a4c9e6` established the right trust
boundary: a pinned upstream snapshot, explicit upstream verification classes,
statement and definition audits, encoder--denoiser review, no namespace-wide
transplant, and separation of source, conceptual and compiled Lean edges. Its
14 intake clusters cover the most obvious log-concave, transport/Riemannian and
discrete-mixing routes.

The remaining gap was *coverage topology*. The intake did not say where every
relevant cluster belongs in the seven reader libraries, and it omitted several
directly relevant families visible in the upstream catalogue or formalization
manifest. The coverage map now preserves all 14 initial clusters and adds 18
audited domain routes, including convex/log-concave geometry, transport-map
stability, exact combinatorial sampling and counting, reconstruction and Ising
thresholds, Gaussian information lower bounds, and metric geometry of Markov
chains.

The audited upstream catalogue has 372 result families and 722 manuscripts.
The upstream `lean/formalization.yaml` lists 185 main-result endpoints, but its
project status is “Partial progress” and its overall review status is
“unchecked”. The map therefore records endpoint-level evidence; it never turns
an upstream result, a linked Comparator statement, or a manuscript into a blue
Samplinglib theorem.

## Placement rule

Each upstream route is placed by mathematical consumer, not by directory name
or keyword:

1. If an existing textbook chapter genuinely teaches the required objects or
   proof mechanism, the item is shown as a **chapter extension** beside that
   chapter.
2. If the mathematics belongs to a library's domain but not to its primary
   source, it is placed in a named **extended chapter** (`E1`, `E2`, ...).
3. If another library merely supplies useful vocabulary, it receives a
   **cross-reference**, not a dependency edge.
4. Source-specific research results also receive a SampleWiki placement when a
   reader-facing frontier case is useful.
5. Lexical collisions are rejected explicitly. Ergodic weak mixing, quantum
   entropy or a random walk in random environment is not silently classified as
   MCMC, KL/LSI or sampling.

Extended chapters are ASTIS editorial organization. They are not chapters of
Chewi, Boumal, Chen--Štefankovič--Vigoda, Fearnhead--Nemeth--Oates--Sherlock, or
Chewi--Niles-Weed--Rigollet, and the website labels them accordingly.

## Verification vocabulary

- `comparator-backed`: an exact declaration and Comparator configuration are
  present in the audited upstream manifest.
- `comparator-backed-partial-family`: one or more named endpoints are checked,
  but they do not cover every claim in the result family.
- `comparator-doc-linked`: the result-specific upstream documentation links a
  Comparator statement, but the audited main-result manifest does not expose a
  solution declaration that ASTIS can seal.
- `lean-present-not-comparator-audited`: Lean files exist, but this audit did
  not establish a Comparator-backed source endpoint.
- `manuscript-only`: no admitted upstream Lean endpoint was located.

Every one of these remains an external reference. A solid ASTIS Lean edge still
requires an ASTIS-owned declaration, local compilation, tests, a definition and
hypothesis diff, source-blind reconstruction, anti-anchored review, and normal
publication admission.

## Website contract

`website/scripts/openai_math_intake.py` renders:

- one central coverage and truth-status page;
- one generated extension shelf for each of the seven libraries;
- a compact link card on each library's landing page; and
- explicit exclusions that demonstrate why keyword matching is insufficient.

The validator checks the pinned commit, the seven exact library identities,
unique route ids, complete placement targets, extended-chapter identifiers,
upstream evidence fields, local truth status and rendered pages. It also checks
that the pages never use the ASTIS blue/compiled badge for upstream material.

## Next mathematical intake order

The current user-authorized local OAI lane continues the work already present:
the intake protocol, original 14 clusters, 32 domain placements and generated
seven-library shelves are **not** to be rebuilt. Its bounded first phase is
`oai-logconcave`, recorded in the existing intake's `execution` object. This is
an execution capsule, not another proof-status ledger. The initial researcher
guide exposes the source result and its proof mechanisms; source reading is not
local formalization or independent source certification.

At the 2026-10-09 start, a bounded search of Registry, production publication
bindings, Frontier Cells and the semantic registry found no OAI-specific local
admission record. This does not assert that mathematically reusable ASTIS lemmas
are absent, or that unmerged collaborator work does not exist. Inspect exact
declarations and evidence before deciding reuse/adapt/missing. Keep distinct:
protocol absorbed; chapter mapped; source explained; upstream Lean available;
ASTIS compiled; independently reviewed; integrated; researcher-purified.

Each source reader must answer: which existing mathematics is reused; what the
source claims to improve; what new ingredient or arrangement carries the proof;
and which part is actually checked locally. A first implementation in this
library is not research novelty. Historical baselines need compatible model,
metric, initialization and cost contracts plus exact sources. Until independently
audited, display them as source-authored comparisons, not settled priority claims.

### First local prerequisite checkpoint (2026-10-09)

Reuse `ASTIS-SHARED-gaussian-complementary-noise`, rather than re-proving it.
Its exact declaration is
`AutoSamplingTheory.TechnicalLemmas.Probability.GaussianComplementaryNoise.map_stdGaussian_product_of_adjoint_norm_sq`.
The focused test and independent mathematical/source review passed; the canonical
cell remains `proved_locally`, not a main-integrated source-main certificate.
The publication binding is a **shared prerequisite**, attached to the existing
Chapter 1 probability substrate; OAI compiler absorption is its planned consumer,
not the claimed theorem source. The audited natural-language proof and folded
Lean explain projection, independence and exact covariance restoration.

The source-specific square root, tensor seed construction and balance,
pathwise query invariance, parent-conditioned independence, recursive error,
termination and every-run query cap remain open. Exact Gaussian law does not
prove any of these. Follow the cell, publication binding and semantic audit for
evidence; this paragraph is only a continuation pointer, not another status ledger.

The OAI lane preserves the companion-paper owners and their unfinished work.
This map does not supersede their paper-priority lane. When another OpenAI Math
route becomes dependency-ready, prefer a small reusable interface with an
existing paper or textbook consumer. High-value audits are:

1. exact statement/definition comparison for the log-concave oracle model;
2. Brenier stability against the Statistical OT Chapter 3 map API;
3. conditional-resampling, comparison and TV-conversion leaves shared by
   Discrete Sampling and MCMC;
4. Weak MTW/RCD adapters only after smooth and nonsmooth curvature predicates
   are kept separate; and
5. metric Markov type/cotype as an extended conceptual route, not as an MCMC
   convergence theorem.

No item should be ported merely to increase a declaration count.
