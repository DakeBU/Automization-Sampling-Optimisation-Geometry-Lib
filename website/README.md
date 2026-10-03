# Samplinglib website

Samplinglib is the public formal library, learning environment, and
verification surface maintained by Auto-Sampling-Theory-In-Sleep (ASTIS).
This directory contains the maintainable website source. Generated output is
written to the ignored `_site/` directory.

## Source of truth

`tools/astis_site.py` deterministically combines:

- all project Lean modules, imports, declarations, source lines, docstrings,
  and placeholder signals;
- `AutoSamplingTheory/TechnicalLemmas/Registry.lean` and `Tests/Basic.lean`;
- chapter, source-correspondence, milestone, and reviewed teaching metadata in
  `website/content/`;
- the canonical August 9, 2026 edition contract in
  `website/content/source_edition.json` and section guides generated against
  that exact table of contents;
- editable Mermaid sources in `website/diagrams/`;
- source-bound Lean gate evidence in ignored `.astis/site-lean-gate.json`.

Local declaration status and mathematical-route status remain independent.
Task cards, prose, metadata, and a well-typed proposition do not count as a
proof.

## Build

### Companion frontiers and proof-technology deltas

`samplewiki_companion_frontiers.json` extends the pinned SampleWiki snapshot
with two primary-paper cases and a composition view; it does not change the
upstream 34 rows or the active Chewi 8.4.1 case. `samplewiki_proof_deltas.json`
records inherited mechanisms, paper-specific adapters, revealed structures and
their exact source anchors. The generated reader begins at
`example-cases/samplewiki/companions/index.html`.

Add or update a theorem contract in the companion model, not in generated HTML.
Keep the actual law, proxy law, divergence convention, oracle and expected-cost
contracts separate. Every teaching statement/proof has an adjacent closed Lean
disclosure; without a local declaration the disclosure says so instead of
displaying invented Lean. Technology search modules are not proof certificates.

Candidate families and bridges use the existing Graph Memory / Functor
Hypergraph; their source title, URL and anchor are checked against the companion
model. The proof-delta view follows DMS → Fan–Li–Lu → the PBPS discrete adapter,
without claiming an exhaustive novelty ranking. Generated SVGs and the full
graph share metadata identities. All new local theorem targets stay red.

Run the normal build/check commands below and
`python3 -m unittest tools.tests.test_samplewiki_companions` after editing.
Do not move a candidate to blue by changing this metadata: use the existing
independent Lean/source review and Registry gates.

### Shared proof readers

`website/content/proof_readers.json` holds original mathematical exposition for
recent shared prerequisites. Each reader has an exact statement, hypotheses,
displayed equations for every proof step, step-to-Lean explanations, source
scope, and an explicit remaining boundary. It is not a source-theorem closure
record or an addition to the reviewed-teaching count.

`proof_readers.py` resolves declaration links from the existing generated
inventory. Each mathematical statement is immediately followed by its own
closed Lean-statement disclosure; each mathematical proof by its own closed
Lean-proof disclosure, including named private helpers where needed. It reads
compilation, Registry membership, Frontier Cell status
and independent semantic verdict separately. Do not author those statuses in
the exposition. List ASTIS and Mathlib dependencies separately, with a role for
each call. Add a reader to an actual chapter/library consumer using
`entry_pages`. Build and validation commands below include this layer. The
rendered entry is `_site/proofs/index.html`.

### Declaration-by-declaration textbook expansion

The full-library teaching expansion is in progress, not complete. The generated
`_site/lessons/index.html` lists **every production declaration**, including
definitions and provenance records. `_site/data/declaration-exposition.json`
is generated from the source inventory, not a second theorem-status registry.
An older teaching note is not automatically classified as a complete proof.

Author a unit in `website/content/declaration_lessons/*.json`, under `units`.
Required fields are `declaration`, `kind`, `title`, `statement`, `formula`,
`assumptions`, `steps`, `lean_statement`, `lean_proof`, and `boundary`.
Each step needs `title`, natural-language `text`, a display-TeX `formula`, and
a declaration-specific beginner `lean` explanation. The `lean_statement` and
`lean_proof` fields are **explanations**, not duplicated code: exact signatures
and complete proof source are extracted from the current Lean declaration.
Include notation, Samplinglib parents, Mathlib calls, exact sources, tests and their
actual scope. Definitions require their construction and meaning, not invented
proofs of the propositions their metadata describes.

The generated lesson starts with a human reading pass: the mathematical claim,
main formula, and a short proof roadmap are visible together. Full assumptions,
scope ledgers, provenance, and exact Lean source remain one click away. This
keeps the mathematical argument readable while preserving every premise and
the complete kernel-checked declaration for audit.

Source entries use either an HTTPS `url` or a repository-relative `path` with
an optional one-based `line`. Mathlib paths resolve using `lake-manifest.json`;
local source contexts are included in the generated site with line anchors.
No absolute machine paths, mutable Mathlib branch links, or invented source
equivalence verdicts are allowed. Preserve the complete mathematical content
of source statements in clearly attributed restatements; distinguish source
assumptions, rigorous supplements, and the actual formal contract. This is not
permission to reproduce copyrighted prose at length.

`inline_lean.py` also gives mapped Chewi source cards adjacent statement/proof
disclosures and makes their existing rigorous mathematical expansion visible.
This presentation pass does **not** invent missing derivations or certify
source fidelity. `declaration_lessons.py` renders authored units and links them
from exact module declarations. The common mathematical unit never changes
Registry, mathematical DAG, Frontier Cell, or semantic-audit state.

Generated structure accessors use `astis_projection_dependencies` entries with
`structure`, `field`, and `role`. The field must exist in the actual linked
structure; reading an assumed integrability field is not a new integrability
proof. Lean names are case-sensitive, so lesson URLs include a stable digest
to prevent an interface type and its similarly named constructor overwriting
one another. Shared module readers use the same authored units in source order.

### Data records are not mathematical proofs

`metadata_reader.py` handles only an independently audited allowlist of 1,062
nullary SALD data definitions, using 62 local data schemas and the Core schemas.
`metadata_lessons.py` publishes their field values, schema defaults, symbolic
data references and adjacent exact Lean construction. The generated ledger
keeps `data-explained` / `data-unresolved` separate from authored mathematics.
The 1,046 currently supported constructions do not add mathematical proofs.
The 16 unsupported records remain explicit: unknown computations are not
guessed, and source containing absolute machine paths is withheld, not silently
redacted and called exact.

The allowlist is `website/content/metadata_reader/audit.json`, bound by its
manifest to the source snapshot and each complete declaration body. Digests
normalize **only CRLF to LF**, so Windows and Linux checkouts agree; all other
source drift requires review, never a blind hash refresh. Strings named
`statement`, `status`, or `dependsOn` remain data. They cannot upgrade the
Registry, source fidelity or the Lean dependency graph. Unsupported proof-bearing
structures and mathematical functions are never admitted by this parser.

```bash
python3 -m unittest tools.tests.test_proof_readers
python3 -m unittest tools.tests.test_metadata_reader
python3 website/scripts/build_site.py
python3 website/scripts/check_site.py
# Strong acceptance check: intentionally fails while any teaching unit is missing.
python3 website/scripts/check_site.py --require-full-exposition
```

The website runtime is Python 3.12 or later (CI uses 3.12; the current Windows
runtime uses 3.14). On Windows use the installed Python 3.14 executable if `python3` is
a Windows Store alias. Retain the repository's pinned Lean toolchain; a website
change does not authorize a toolchain upgrade or mathematical packet change.

Publication is distinct from Git push: pushing a collaboration branch saves
the source remotely. The existing Pages workflow deploys from `main` (or an
explicit manual workflow run), not from that collaboration branch. Do not
present a pushed branch as a changed live website.

From the repository root:

```bash
python3 tools/astis.py chewi-source-check
python3 website/scripts/lean_gate.py
python3 website/scripts/build_site.py
python3 website/scripts/check_site.py
```

The generated site includes the overview, twelve-chapter learning path,
implementation map, exhaustive declaration and module catalogs, reviewed
teaching pages, roadmap, ASTIS workflow, the four-stage contributor guide,
attribution, and Live Formalization workspace. Search, source anchors, status,
diagrams, and source links are all checked before publication.

## Live Formalization

Static GitHub Pages supports LaTeX rendering, reviewed mappings, library
navigation, dependency inspection, and ASTIS packet export. It cannot execute
Lean or call a formalizer.

Local verified mode adds a deterministic ASTIS formalization adapter and the
pinned Lean compiler:

```bash
python3 website/scripts/build_site.py
python3 website/scripts/ide_server.py
# http://127.0.0.1:8088/live/
```

The server is deliberately loopback-only. It limits request size and runtime,
serializes compiler work, uses a temporary directory, does not alter repository
source, and does not log submitted source bodies. It is a development service,
not a public execution sandbox.

The workspace never merges these states:

- candidate translation;
- Lean elaboration or compilation;
- semantic review;
- proof status;
- reviewer acceptance.

Unsupported formulas remain unresolved and can be exported with
`analytic_contract`, `formalization_map`, `proof_attempt`, and `review`
boundaries for ASTIS decomposition. No provider credentials are sent to the
browser.

## Authenticated private preview

Set both credentials in the remote shell before starting local verified mode:

```bash
export ASTIS_PREVIEW_USER='reviewer'
export ASTIS_PREVIEW_PASSWORD='generate-a-secret-outside-git'
python3 website/scripts/ide_server.py --port 8087
```

The same process then protects both static pages and `/api/*` with Basic Auth.
Forward it from a local computer:

```bash
ssh -N -o ExitOnForwardFailure=yes \
  -L 127.0.0.1:18087:127.0.0.1:8087 USER@SERVER
curl -I http://127.0.0.1:18087/  # 401 Unauthorized
cloudflared tunnel --url http://127.0.0.1:18087
```

Keep the preview server, SSH forward, and `cloudflared` process running. A
`trycloudflare.com` URL is temporary and is not a production deployment.
Credentials must never be committed.

For a static-only authenticated preview, `website/scripts/serve_preview.py`
remains available with the same environment variables.

## Source links and gate rules

The build checks the current commit, ref, remotes, and dirty files. Source
links use site-local declaration anchors by default. Set
`ASTIS_PUBLIC_SOURCE_LINKS=1` only after confirming the remote is public; clean
files then link to the exact published commit SHA, never assumed `main`.

`lean_gate.py` writes evidence only after the canonical ASTIS check succeeds.
The site refuses to show “Lean gate passed” when the evidence does not match
the current commit and Lean-source digest.

`check_site.py` rejects stale gate claims, Registry/test drift, unknown
metadata declarations, incomplete inventories, missing anchors, broken links,
unpinned source links, missing formulas/diagrams/assets, leaked paths, and
missing public/system identity markers.

## CI and Pages

Sites reuses the existing project in `.openai/hosting.json`, without changing
its audience. After a checked build, `python3 website/scripts/build_sites_bundle.py`
stages static output in ignored `build/` for the Sites packaging helper; it
also preserves the legacy `.open-next/` adapter. The `--archive` option is the
legacy worker format, not the current Sites upload format. Use the Sites
plugin's `package-site.sh PROJECT_DIR ARCHIVE_PATH` for a current upload.
The build refuses to replace a pre-existing `build/` not marked as generated.
Only a successful source push and exact source-bound build may be published.

`.github/workflows/blueprint-site.yml` runs Python and JavaScript contract
checks, harness tests, source-derived site generation, site validation, browser
checks and Pages artifact creation. This website-first job can build without
installing Lean or Mathlib; external source links remain lockfile-pinned.
The separate canonical Lean gate is required for a current compiled claim:
a source-only website build does not manufacture gate evidence. Pages receives
only `_site/`; the loopback compiler server is never deployed.

Website prose is original Samplinglib/ASTIS exposition. Chewi's public draft
is summarized with source correspondence rather than copied at length.


## Cross-domain extension

`library_shelves.py` renders five peer libraries in the same reader; `cross_domain.py` adds the eight-chapter/two-appendix OT source map, coordinated shared prerequisite order, and higher-order sampling research contract. `formalization_progress.py` owns all five public routes. `underlying_lean_graph.py` exports schema-3 graph data with first-class conceptual `hyperedges` as well as incidence edges; the new Functor Hypergraph view never upgrades source correspondence to a Lean certificate. See `docs/cross-domain-program.md` for schema semantics and source/fallback rules.
