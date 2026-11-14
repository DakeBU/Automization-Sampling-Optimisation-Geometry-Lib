# Evidence-Routed Research Memory and Scheduling Protocol

This protocol complements `docs/proof-digestion-protocol.md`. It adapts the
useful cross-round learning ideas of arXiv:2609.40324 to Samplinglib without
turning the repository into a generic multi-agent proof factory.

The operating rule is:

> **Verified mathematics may become proof memory; verified failure may become
> negative knowledge; repeated process mistakes may become process instructions.
> None of these are interchangeable.**

Samplinglib keeps the final acceptance authority in Lean plus the existing
source/semantic review gates.

## 1. Failure is typed before it changes scheduling

Every non-successful route is classified as exactly one of:

- `REFUTED`: the mathematical route/claim is ruled out by a checked
  counterexample or rigorous reviewed argument;
- `SOURCE_INVALID`: the pinned source statement/convention is false,
  ill-posed, or needs a separately reviewed repair;
- `API_BLOCKED`: the mathematics is not refuted; the current Lean/Mathlib/API
  surface is the obstruction;
- `ENV_BLOCKED`: filesystem, dependency, CI, toolchain, package, or runtime
  environment prevents the attempt;
- `IMPLEMENTATION_FAILED`: this implementation/proof attempt failed without
  evidence that the mathematics is false;
- `NONE`: no failure is being recorded.

Only `REFUTED` or a reviewed `SOURCE_INVALID` record may retire a route on
mathematical grounds. API, environment, and implementation failures must never
be displayed as negative mathematical evidence.

## 2. Salvage before garbage collection

Before a blocked/rejected proof branch is discarded or purified away, run a
**salvage audit**.

For every theorem-shaped fragment that appears to have survived the failed
route:

1. isolate it from theorem-local context;
2. minimize assumptions and imports;
3. check that no failed parent is smuggled in as a hypothesis;
4. compile it independently;
5. run the shared-floor/canonicality audit;
6. classify it as `canonical-library-node | route-local | counterexample |
   process-only | discard`.

A fragment becomes reusable proof memory only after the ordinary Lean and
source/semantic gates appropriate to its declaration level. Text from a failed
proof is never promoted merely because another model described it as correct.

This gate runs **before** dead-code deletion in PURIFICATION. Thus machine
debris is not kept, but verified mathematical content is not thrown away with
a failed parent proof.

## 3. Two durable ledgers: positive and negative

Positive proof memory remains the canonical compiled Lean library plus the
existing Frontier/Discovery records.

Negative/process memory lives in
`research-wiki/process-memory.json` and is validated by
`tools/astis_process_memory.py`.

A negative-memory record includes its exact scope, evidence, invalidation keys,
and route effect. It is not a global ban. For example, an API-blocked route may
reopen after a Mathlib/toolchain change; a source-invalid record may reopen
after a new source edition or accepted repair.

A process-standing instruction must be **process-only**: it may say “separate
the normalization base measure from the Fisher integration law before proof
search”, but it may not invent a mathematical lemma or tell workers that a
particular unverified proof direction is true.

## 4. Evidence-bound failure router

The control plane has no mathematical authority. It may route evidence:

| Failure class | Default next process |
| --- | --- |
| `REFUTED` | retire same sealed route; salvage verified fragments; search a mathematically distinct route |
| `SOURCE_INVALID` | source audit / repair lane; no proof search on the stale seal |
| `API_BLOCKED` | retrieval/API adapter or upstream-dependency lane |
| `ENV_BLOCKED` | deterministic environment/infrastructure repair |
| `IMPLEMENTATION_FAILED` | inspect error signature; retry only with a changed route fingerprint |
| `NONE` | ordinary proof/frontier scheduling |

The router may recommend a **process**, never a theorem conclusion.

## 5. Parallelism is admitted by distinct uncertainty

Samplinglib's default is serial/bounded scheduling. Parallel workers are
admitted only when their packets have different `direction_fingerprint`
values and own genuinely different uncertainty, for example:

- coupling versus semigroup proof routes;
- proof construction versus counterexample search;
- source audit versus implementation;
- two disjoint theorem leaves with non-overlapping ownership.

Each parallel packet receives:

- the same Statement Seal and verified shared-memory digest;
- only route-specific failed-history relevant to its direction;
- disjoint file ownership where possible;
- an explicit expected-information-gain statement.

Duplicating the same large context across workers to attack the same
unclassified leaf is not an admissible parallel experiment.

## 6. Cross-route common-blind-spot audit

When two or more serious routes to the same Source Anchor survive to
verification, a distinct reviewer performs a side-by-side audit. Its purpose is
not to re-prove every line; it asks whether the routes share the same hidden
premise, representative choice, integrability assumption, invariant-law gap,
constant-scope error, or source misreading.

A parallel/multi-route Source Anchor cannot be called proof-sealed until the
required common-blind-spot audit is accepted or every alternative but one has
been retired with evidence.

## 7. Verified-route comparator

After the common-blind-spot audit, if more than one route remains verified, a comparator selects the **default reader route**, not the only true route. It may compare source fidelity, assumption strength, reuse of canonical primitives, proof compression, and pedagogical readability. The selected route and reason are recorded, while all other verified alternatives remain explicit OR-routes in the Source Proof Graph.

The comparator may choose only among routes that already passed their own verification; it cannot promote an unverified candidate because it looks shorter or more elegant.

## 8. Reader backpressure and Exposition Seal

Samplinglib explicitly tracks the debt created when proof production outruns
human digestion:

- `merged_not_purified`: merged Source Anchors whose proof forest has not been
  compressed;
- `purification_age`: time from merge to PURIFIED;
- `fine_to_conceptual_ratio`: fine Lean/source nodes divided by reviewed
  conceptual moves, when the graph exposes both counts.

These metrics are scheduling signals, not mathematical quality scores. If the
debt grows, the scheduler must reserve capacity for synthesis/purification
rather than spending all capacity on new Source Anchors.

A PURIFIED source-facing result additionally receives an **Exposition Seal**.
The compressed reader statement must expand losslessly to source and Lean nodes,
preserve hidden hypotheses and the remaining boundary, and be independently
reviewable without knowledge of the agent run.

The Exposition Seal is evidence-bearing rather than a status word alone: it records the source nodes and Lean nodes to which the compressed explanation expands, plus independent confirmation that assumptions and the remaining boundary were preserved.

## 9. Run-record integration

New Frontier Cells should use schema version 3 and record a
`learning_contract` containing:

- process-memory IDs consulted;
- failure class;
- salvage status;
- serial/parallel admission and direction fingerprints;
- common-blind-spot audit status;
- reader-backpressure / exposition status.

Historical schema-1/2 cells remain valid. This is a forward protocol, not
retroactive evidence fabrication.

## 10. Samplinglib-specific standing lessons

The initial process-memory registry is deliberately small and evidence-backed.
It records only lessons already visible in the repository's reviewed runs,
including:

- do not conflate the normalization base measure of a tilted law with the
  probability measure used by a Fisher-information integral;
- positive-time/domain repairs for normalized gradient-flow and gradient-descent
  rate formulae remain source-repair knowledge, not theorem assumptions silently
  inserted by future formalizers.

The registry should grow only when repeated or high-impact evidence justifies a
durable instruction.

## Design provenance

This protocol is informed by the cross-round attempt/lemma/advisor architecture
of arXiv:2609.40324. Samplinglib deliberately differs in three ways: verified
fragments are promoted only through Lean/source gates, control-plane memory has
no mathematical authority, and the terminal goal is a PURIFIED researcher-facing
proof spine rather than proof-discovery throughput alone.
