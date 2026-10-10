# Theorem publication: mathematics once, reader views automatically

Applies to **every new or changed production declaration** in every ASTIS route,
including reusable shared foundations. An unchanged historical proof is not
retroactively certified; its missing exposition or semantic audit remains debt.
The current mathematical Goal and frontier are not changed by this protocol.

## Pre-proof constitutional gate: Statement Seal and Source Proof Graph

Every new or materially changed **source-facing** theorem/definition also follows
[`proof-digestion-protocol.md`](proof-digestion-protocol.md) *before* proof search.
The exact source-facing Lean signature is sealed first; project-owned bundled
assumptions are recursively classified as `SOURCE`, `STANDING`, `TYPING`,
`RULED`, or `EXCESS`, and any `EXCESS` binder rejects the source Anchor.
A proof ingredient is represented as a dependency edge and discharged inside the
proof; the existence of a producer theorem never licenses moving its conclusion
into the public theorem hypotheses.

Definitions are audited as `literal`, `characterized`, or
`quotient/representative`. A characterized object may be chosen only after the
real source-level existence/uniqueness theorem has been proved and audited; an
`if`/default/fallback body that invents off-source semantics is not acceptable.

In parallel, build a **Source Proof Graph** from the source independently of the
Lean implementation. Every in-scope theorem, definition, reused display,
citation, and substantive proof paragraph is `NODE` or `EXCLUDED(reason)`;
omitted bridges remain visible `SOURCE_GAP` nodes and alternative sufficient
proofs are explicit OR-routes/hyperedges. This graph answers “how did the author
prove it?”, while the Lean graph answers “what does the checked implementation
depend on?”. They must not be conflated.

After proof sealing and publication, the result enters the purification gate:
remove dead/duplicate/wrapper-only proof debris, canonicalize shared leaves,
compress bookkeeping into reviewed conceptual moves, preserve drill-down audit
evidence, and update the Compressed Shared Spine. `MERGED` therefore does not
imply `PURIFIED` or “done for readers.”

Explicitly private implementation declarations may share the review of a public
theorem in the same file. The diff gate inventories every such declaration,
including anonymous private instances by file/line/column, and prints its public
owner. Coverage requires an accepted independent source review, the exact current
whole-module text, a fresh publication binding and successful publication
validation. Private helpers gain no separate publication edge or proof credit.
Changing a helper invalidates the enclosing module review; making it public
requires its own publication. Unindexed public/Unicode syntax, uncovered private
implementations and private axioms still fail closed. Always run the final
`check --base BASE_COMMIT`; a single-target admission check does not exercise the
changed-module inventory.

## One bounded packet

```bash
python3 tools/astis_publication.py packet --cell CELL_ID
```

Read that cell's source contract, existing parents and exact interfaces. Do not
load all books, all transcripts or all Lean lessons. Search reusable APIs first.
There are no automatic model calls, background agents or new Goals in this tool.
The hosting agent follows the instructions below; mechanical CI verifies them.

## Author once

1. Maintain the existing Frontier Cell: exact canonical declaration, compiled
   checks, independent commit-bound review, consumers and residual boundary.
2. Write one authored unit per declaration in
   `website/content/declaration_lessons/*.json`. State **all** objects, domains,
   quantifiers and assumptions. Give a readable formula proof, not a tactic
   paraphrase; explain each step's Lean correspondence. Keep the exact Lean
   statement and proof in source: the renderer extracts them into separate,
   initially closed disclosures immediately beside the statement and proof.
   List actual ASTIS calls separately from Mathlib calls and external provenance.
3. Add a source item/binding in `website/content/publications/*.json` (schema 1;
   `optimisation.json` is the concrete example). Store the full attributed source
   statement once, with formulas, version and exact anchor. Bind its individual
   proof obligations to declarations and cell IDs. `proof-edge` and
   `prerequisite` are different: a convexity helper alone does not partially
   formalize a downstream gradient-flow theorem. Do not author chapter status.
4. Fill `assumption_deltas`: source wording, actual formal assumption,
   classification and mathematical explanation. Categories are `same`,
   `source-implicit`, `mathematically-necessary`, `API-limitation`,
   `generalization`, `unresolved`. A technical limitation is not a textbook
   correction. Explicitly address relevant measurability, representatives,
   regularity, integrability, domination, boundaries, domains and constants;
   omit inapplicable checklist boilerplate; explain only non-obvious omissions.

Mathematical exposition is authored and independently checked, not inferred from
declaration names. Existing authored units are reused in the chapter reader.
No copied status table, HTML editing or new wrapper theorem is required.

## Graph contribution: part of the same publication

Codex and Claude Code use this contract (`CLAUDE.md` imports `AGENTS.md`). A
formalization is not publication-ready if its contribution disappears from the
Underlying Lean Graph or its affected source/route views. Reuse stable ids;
never draw a second copy of a shared declaration to make a chapter look complete.

| Changed fact | Canonical input and affected view |
|---|---|
| Declaration, owning module, imports, reuse | Lean source + Registry → Underlying Lean Graph / Lean Branches, module and dependency views |
| Source proof component, prerequisite, remaining boundary | Publication binding + source obligations → chapter/Overview graph and generated progress |
| Frontier parent, consumer, retired or blocked route | Existing Frontier Cell and route/source metadata → relevant frontier and theorem-local DAG |
| Semantic mismatch or proposed repair | Existing round-trip audit → Semantic fidelity & repair view |
| New recurring mathematical mechanism | Existing conceptual-mirror audit; only a real discovery updates Graph Memory / Functor Hypergraph |

Only change the rows affected by the contribution. A routine lemma does not
require a new conceptual bridge, a full-book redraw, or a graph-specific agent.
An intended consumer is a planned/curated edge, not an existing Lean use.
Source-name scans are incomplete reference signals, not elaborated Lean proof
dependencies. Keep them dashed and labelled; solid `imports`/`declares` edges
record module structure. Do not infer theorem implication from an import,
source correspondence, a proof-route leaf, or conceptual similarity. Blue still
requires owned, compiled evidence; library/source colours do not confer it.

At stabilization, build the site once and inspect the contribution:

```bash
python3 website/scripts/build_site.py
python3 tools/astis_publication.py graph-check --cell CELL_ID
python3 website/scripts/check_site.py
```

`graph-check` reads the generated graph, verifies mapped nodes, owning modules,
reference/consumer edges and chapter links, then prints a bounded one-hop slice
and focus links. The site check runs the same graph contract for all publication
bindings, including unchanged mappings affected by a generator regression.
It does not certify that source scanning found every Lean dependency.
If `_site` is absent/stale, regenerate it; never paste the entire graph into an
agent prompt. If a curated SVG/Mermaid theorem/frontier diagram is affected,
update its maintained source too; do not hand-edit generated SVG/PNG/HTML.

Open the changed branch and any changed static diagram: check labels, directions,
solid/dashed distinction, status, reader links and legibility. Inspect mobile
layout when layout code or branch size changes. Automation does not claim to
perform this visual review. Add a short graph delta to the **existing** PR or
`integration_notes`: node/focus links, changed connections or topology, remaining
red boundary, and commands + views actually inspected. Do not repeat the proof
or add a new screenshot/report ledger. Layout-only changes do not invalidate
mathematical audits; changed source/assumptions/proof explanations do.

## Cost discipline

Each requirement protects one boundary: Lean checks truth, round trips check
source fidelity, authored lessons explain the mathematics, graph checks prevent
omitted/misclassified contributions, and visual inspection checks readability.
Reuse those results rather than adding another reviewer for each surface.
Use focused tests while editing; run aggregate acceptance once on the final
candidate (again only after a relevant change). Reuse unchanged audit hashes and
existing `none-found` conceptual-mirror evidence. Do not read unrelated books,
dump full graphs, create duplicate metadata, or repeat full builds after every
sentence edit. This is a bounded workflow, not a claim of globally optimal tokens.

## Encoder–denoiser: required semantic round trip

Follow [.agents/skills/astis-semantic-roundtrip/SKILL.md](../.agents/skills/astis-semantic-roundtrip/SKILL.md).
Compilation certifies the Lean proposition, **not** fidelity to the source.

1. Pin the original/faithfully paraphrased source and fully elaborated Lean
   statement in the canonical semantic registry. Link `audit_id` from the
   publication binding. A draft audit is allowed at `PROVED_LOCAL`, not at
   `VERIFIED` or `STABILIZING`.
2. Export `review-context --item ITEM_ID --declaration FULL_NAME` with
   `tools/astis_publication.py` and copy its `publication_binding_sha256` and
   `publication_context` into that audit. They bind the
   entire Lean module (including imports and scoped parameters), toolchain,
   dependency manifest, source statement, obligation map, assumption ledger and
   authored lesson. Both enter the independent source/repair review packets, so
   refreshing a hash cannot replay an older review. The candidate context omits
   earlier verdicts and assumption-delta classifications. A stale binding fails.
3. Export the anonymous `decoder-packet` using the existing round-trip tool.
   Give **only this packet** to a distinct source-blind decoder. The publication
   packet contains source identity and must never be used as decoder input.
4. Export a fresh anti-anchored `reviewer-packet` for a reviewer distinct from
   formalizer and decoder. Compare all seven canonical semantic slots and
   record packet/run-bound evidence. No self-certified equivalence.
5. If a source gap is discovered, retain four separate objects: the pinned
   source, actual Lean theorem, semantic mismatch and proposed repaired theorem.
   Expose the gap and its reason publicly. A repair requires its own blinded-to-
   prior-verdict, independent exact-proposal `repair-reviewer-packet`, minimality
   evidence and rigorous reference/counterexample. API convenience cannot justify
   adding a mathematical assumption to the source.

Reuse unchanged audit evidence. Reaudit only the affected bounded packet when
code, source, assumptions or explanation changes. File-level invalidation is
conservative; it intentionally catches changes outside the visible theorem body.
The system does not claim this is an optimal token budget or replace human review.

## Admission and generated views

New Harness advances use schema 4. At `PROVED_LOCAL`, include
`publication_declarations` equal to `lean_declarations`; real metadata validation
runs. `VERIFIED` and `STABILIZING` carry that same target set and require completed
independent source review. Rejected source fidelity can be published as explicit
local mathematics and a visible mismatch, never as source assimilation.
Schema 1–3 ledgers remain replayable; the Git diff gate also covers legacy lanes.

```bash
python3 tools/astis_publication.py check --base BASE_COMMIT
python3 tools/astis_semantic_roundtrip.py check
python3 website/scripts/build_site.py
python3 website/scripts/check_site.py
lake build Tests
python3 tools/astis.py check
git diff --check
```

The diff gate is intentionally conservative: all declarations in a changed
production module need publication coverage (including scoped-variable/import
changes). Root imports, Tests and the generated Registry catalog are not new
theorem proofs. CI checks the PR/push base before the expensive Lean build.
The site projects the same mapping into source chapter readers, chapter labels,
route progress and overview graph. No mapping means no inferred chapter credit.
The declaration-level Lean gate remains authoritative for **blue**; chapter
partial progress is orange and never implies exhaustive source coverage.

Migration boundary: precisely the two unchanged StrongConvexFirstOrder proofs
present at commit `5c6adf3b812f3ba9315c92ba78a4ff59ccc2a53e` may retain visible
historical round-trip debt. This is a fixed file-hash allowlist, not a contributor
opt-out. They supply partial proof components, not a source-complete certificate.
