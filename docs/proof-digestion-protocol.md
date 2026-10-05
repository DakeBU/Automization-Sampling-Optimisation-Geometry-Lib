# Proof Digestion Protocol: Formalize → Audit → Compress → Explain

This protocol governs how Samplinglib turns source mathematics into a verified
Lean library **without leaving machine-generated proof debris as the public
mathematical product**. It complements
`docs/formalization-protocol.md`,
`docs/theorem-publication-protocol.md`, and the semantic round-trip protocol.

The governing principle is:

> **Freeze what is being proved before proof search; reconstruct the source proof
> topology independently of the Lean implementation; formalize exhaustively; then
> purify the resulting proof graph for researchers.**

A green Lean build is necessary, but it is not the end of the lifecycle.

## 1. Three declaration levels

Not every helper receives the same review burden.

### A. Source Anchor

A theorem, proposition, corollary, definition, or other mathematical interface
whose public meaning is tied to a textbook, paper, or explicitly stated
original result.

Required gates:

- source snapshot and exact anchor;
- Statement Seal;
- binder/definition audit;
- source-proof coverage and topology review;
- semantic round trip;
- proof seal;
- reader publication;
- post-proof purification.

### B. Canonical Library Node

A reusable Sampling/Optimisation/Geometry lemma intended to support multiple
source routes.

Required gates:

- exact mathematical statement;
- local/Mathlib/upstream reuse search;
- Lean proof and axiom cleanliness;
- canonicality/reuse audit;
- actual or realistic consumers;
- purification against duplicates/wrappers.

It need not pretend to be a source theorem when it is genuinely library
infrastructure.

### C. Internal Provider

A private or route-local proof helper used only to construct an Anchor or
Canonical Node.

Required gates:

- compilation;
- no fake closure;
- no theorem-shaped assumption smuggling;
- reachability/dead-code review during purification.

Internal providers do not receive independent source credit.

## 2. Statement Seal comes before proof search

For every new or materially changed Source Anchor, first pin:

- source title, edition/version, immutable source locator and source digest where
  available;
- exact objects, domains, quantifier order, constants, endpoint conventions and
  standing assumptions;
- the exact final Lean signature and every meaning-carrying project-owned
  definition used by that signature;
- a versioned statement-seal identifier and statement digest.

The exact final Lean signature may be elaborated in an **untracked temporary
probe**. Samplinglib keeps its production tree zero-`sorry`: a temporary
elaboration probe is deleted after the signature is recorded.

After `STATEMENT_SEALED`, proof workers may change proofs and internal
providers, but **must not change the sealed theorem interface for convenience**.
A genuine source correction or design ruling creates a versioned successor,
invalidates dependent topology/audit evidence, and is reviewed explicitly.

Statement approval is therefore independent of proof success.

## 3. Binder audit: proof ingredients are edges, not hypotheses

Every logical input to a Source Anchor is recursively expanded through
project-owned `Prop` aliases, structures and typeclasses and classified into
exactly one bin:

| Class | Meaning |
| --- | --- |
| `SOURCE` | Explicit premise of this source statement. |
| `STANDING` | Field of a separately audited source-wide standing assumption. |
| `TYPING` | Pure carrier/type information implicit in the source convention. |
| `RULED` | Exact human-approved correction or source ruling. |
| `EXCESS` | Any proof result, estimate, witness, gate, regularity condition or convenience premise not justified above. |

A source-facing theorem with `EXCESS` fails the Statement Seal.

The central invariant is:

```text
proof ingredient = dependency edge
source hypothesis = theorem binder
```

If the proof needs a bound, concentration event, integrability lemma,
localization result, coupling estimate, or moment estimate, prove it as a
dependency and apply it **inside the proof**. The existence of a producer
theorem does not legalize adding the producer's conclusion as a new public
binder.

For Samplinglib this audit must pay particular attention to measurability,
integrability, domination, representatives, finite moments, support,
smoothness, boundary/decay conditions, positivity, normalization and
constant-dependence scope.

## 4. Definitions receive a semantic audit too

Every source-facing definition declares one of:

```text
definition_kind:
  literal
  characterized
  quotient/representative
```

### Literal

The complete Lean body must agree with the source formula/predicate on the whole
public carrier. No invented off-source fallback semantics.

### Characterized

If the source defines an object as the unique object satisfying
(Phi(x)), first prove and audit the real well-definedness theorem

[
exists! x,; Phi(x).
]

Only then define the object from that theorem and land a separately named,
sorry-free characterization/uniqueness theorem. The definition and
characterization form one semantic unit.

A fallback such as “if existence is known, choose; otherwise return zero” fails.

### Quotient / representative

If the mathematical object is defined only up to an equivalence or requires a
representative, record the equivalence relation, public quotient semantics,
choice mechanism, and every theorem whose statement must be representative
independent. Never confuse “some representative exists” with a canonical
object.

High-risk Samplinglib examples include optimal-transport maps and plans,
Wasserstein geodesics, scores, conditional-expectation representatives, Markov
kernels, invariant laws, Poisson-equation solutions, proximal maps and RGO
objects.

## 5. Build the Source Proof Graph independently of Lean

Before Lean implementation topology is allowed to influence exposition, build a
source-only proof graph.

The source-topology extractor/reviewer may use the pinned source and the sealed
Anchor interface, but it must not use implementation Lean to decide what the
author's proof structure was.

Every in-scope item receives exactly one disposition:

- theorem/proposition/lemma/corollary/claim;
- source definition;
- reused display/equation;
- external citation;
- substantive proof paragraph or unnamed estimate;

as either:

```text
NODE <stable-id>
```

or

```text
EXCLUDED <explicit reason>
```

Silence is not coverage.

Each source edge records the **consumer use site**, not merely where the
prerequisite was proved. Conditional premises must be shown as discharged.
Omitted mathematical bridges remain visible `SOURCE_GAP` nodes.

This prevents a section from being reported “100% formalized” merely because
all numbered lemmas were covered while unnamed bookkeeping paragraphs were
lost.

## 6. Alternative proofs are OR-routes, not one false AND

If a target (T) has two sufficient routes,

[
A land B Rightarrow T,
qquad
C land D Rightarrow T,
]

the graph must not flatten them into (A,B,C,D	o T). Use explicit route
nodes/hyperedges so the semantics are

[
(Aland B)lor(Cland D)Rightarrow T.
]

A Chewi proof, a Villani/OT proof, a coupling proof, a semigroup proof, or a
Mathlib-compatible proof may all coexist as alternative routes. Statement
fidelity remains tied to the target Anchor; proof-route provenance is recorded
separately.

When choosing among routes before formalization, record at least:

- formalization cost;
- existing Samplinglib/Mathlib reuse;
- new reusable leaves created;
- hidden analytical prerequisites;
- reader/pedagogical quality.

## 7. Four graph views with four different questions

Samplinglib keeps these views semantically distinct.

### 1. Source Proof Graph — “How did the author prove it?”

Source-derived theorem/step/citation topology, including omitted bookkeeping and
alternative routes.

### 2. Lean Dependency Graph — “What does the checked implementation actually depend on?”

Compiler-backed modules/declarations and reviewed proof dependencies. Imports
alone never masquerade as theorem implication.

### 3. Compressed Shared Spine — “After removing implementation bookkeeping, what mathematical primitives recur?”

The purified reusable backbone: canonical lemmas/families plus explicit
adapters. Fine-grained Lean leaves stay available by drill-down, but the default
researcher view shows conceptual moves rather than machine residue.

### 4. Functor Hypergraph — “Which proof mechanisms persist after changing the space, metric, energy, oracle or discrepancy?”

Reviewed conceptual transports with hypothesis/conclusion maps and failure
boundaries. Conceptual similarity remains distinct from formal implication.

The existing Overview Graph remains the route/source navigation surface around
these four mathematical views.

## 8. Decompose a paper contribution before discussing novelty

For each formalized paper/result, maintain the reviewed decomposition

[
G_{mathrm{paper}}
=
G_{mathrm{existing}}
cup
G_{mathrm{bookkeeping}}
cup
G_{mathrm{new reusable}}
cup
G_{mathrm{new topology}}.
]

- **existing substrate reuse**: proof edges already supplied by Samplinglib,
  Mathlib, or an admitted compatible library;
- **bookkeeping expansion**: source-faithful compositions of known estimates,
  event/error budgets, recursive accounting, index manipulations, parameter
  checks or other mechanically necessary glue;
- **new reusable primitives**: genuinely new canonical lemmas/families with
  plausible future consumers;
- **new topology**: a new way of composing existing/new primitives into a
  theorem route.

Counts and graph shape are **not automatic novelty scores**. They are auditable
evidence for the researcher asking whether a paper adds mostly bookkeeping, a
new primitive, or a new proof architecture.

## 9. Proof Seal

A Source Anchor reaches `PROOF_SEALED` only when:

- its final signature matches the Statement Seal;
- focused and repository Lean checks compile the actual target;
- unauthorized axioms/placeholders/fake closures are absent;
- binder audit still contains no `EXCESS`;
- every required conditional premise is supplied by actual dependencies;
- the semantic encoder–denoiser review is accepted or the mismatch is published
  explicitly;
- the Source Proof Graph identifies what source obligations have and have not
  been discharged.

## 10. PURIFICATION is the final human-facing state

`PROVED` and `MERGED` do not mean `DONE`.

After proof integration, run a purification pass. The result is not called
finished for readers until it is `PURIFIED`.

The pass checks:

| Check | Required question |
| --- | --- |
| dead declarations | Did failed agent attempts leave unreachable lemmas? |
| duplicate semantics | Are two declarations mathematically the same interface? |
| wrapper-only lemmas | Does a declaration merely repackage assumptions or another theorem? |
| import minimization | Are proof-only dependencies unnecessarily polluting foundations? |
| canonicalization | Should a route-local result move to the shared technical layer? |
| proof-route compression | Which bookkeeping leaves can be folded behind one reviewed conceptual move? |
| graph compression | Which nodes instantiate one reusable family and which adapters are essential? |
| elaboration | Did automation leave pathologically expensive proof scripts? |
| reader compression | What should a researcher see by default, and what should remain drill-down detail? |

Purification must **never delete evidence needed to audit the proof**. It changes
the public presentation and canonical library organization while preserving a
lossless path back to source nodes and Lean leaves.

The rule is simple:

> **Do not leave machine garbage for humans.**

## 11. Lifecycle

The human-facing lifecycle is:

```text
SOURCE_PINNED
  -> STATEMENT_SEALED
  -> SOURCE_TOPOLOGY_REVIEWED
  -> PROVED_LOCAL
  -> PROOF_SEALED
  -> PUBLISHED
  -> MERGED
  -> PURIFIED
```

The existing Frontier Cell state machine remains the repository-integration
state machine until its schema is migrated. In particular, `merged` means
“repository truth has landed”; it does **not** imply `PURIFIED`.

No chapter/paper may advertise “finished” merely from a merge flag when
purification remains pending.

## 12. Sampling-specific compression targets

Purification should preferentially expose reusable mechanisms such as:

- metric/entropy/energy dissipation;
- functional inequalities and coercivity;
- coupling and contraction;
- transport/geodesic interpolation;
- proximal/regularized energies;
- martingale, stopping and localization;
- discretization and one-step error control;
- recursive error/cost accumulation;
- Lyapunov and Grönwall closures.

These names are navigation families, not licenses to identify distinct
hypotheses. The compressed view must retain the adapters showing exactly where
Euclidean, Riemannian, Wasserstein, Markov-chain, discrete-state and other
settings differ.

## 13. Required contribution report

A substantive source-facing contribution must report, in addition to existing
ASTIS fields:

```text
statement_seal:
  source_revision
  statement_version
  signature_digest
  binder_audit
  definition_kind

source_proof_coverage:
  inventory
  reviewed_nodes
  excluded_with_reason
  source_gaps
  alternative_routes

proof_digestion:
  existing_substrate
  bookkeeping
  new_reusable
  new_topology

purification:
  status: pending | purified
  dead_code_audit
  duplicate_semantics_audit
  canonicalization
  compressed_spine_delta
  reader_default_view
```

A future checker may make these fields mechanically mandatory. Until then they
are a **normative protocol requirement** for new Source Anchors and major paper
routes and should be included in their Frontier/publication records without
weakening any existing gate.
