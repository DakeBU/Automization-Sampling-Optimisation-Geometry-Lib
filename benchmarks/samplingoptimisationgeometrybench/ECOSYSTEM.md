# Bench ecosystem: users, agents, environments and experts

The Bench has four entry routes: **browse tasks**, **train**, **evaluate**, and
**expert review**. These use one catalog, not four independently maintained
datasets. Public-dev is not an unseen test split. No model leaderboard is claimed.

## Task API and portable agent inputs

```bash
python tools/sog_bench.py check
python tools/sog_bench.py export --output .astis/my-bench-export
```

`task-index.json` lists currently editorially admitted views by identity, track,
family, domain, provisional level and exact binding. Each task directory has:

```text
tasks/<core-id>/<track>/
  instruction.md
  prompt.json
  task.json
  response-template.json
```

`task.json` separates the instruction from the environment and verifier contract.
It pins Lean 4.33.0, the Mathlib manifest and evaluator source hashes, names the
actual scoring mode, and explicitly denies an arbitrary-submission executor.
This is a portable data/agent convention, **not a native Harbor runnable task**.
The separate [native graph adapter](HARBOR.md) exports Harbor task directories;
its operator ZIP contains oracle/verifier answers and must not enter model input.
Its version-2 transport bounds the declared answer before host transfer and
requires a checked collection receipt. This does not bound automatic log/storage
channels or make arbitrary Lean execution safe.
Python 3.11+ is the supported local recording/JSON-grading environment, not a
claim that a container image or provider execution was reproduced.

`agent-tasks.zip` contains prompt-side artifacts and license notices only.
`task-files.sha256.json` checks every other ZIP member. It contains no reference
proof, rubric, editorial report, training pair or expert-only source anchor.
Individual task files can also be fetched through the static website API.
Read the prompt and declared tool policy, then preserve the first raw response.

## Training and contamination

`training-pairs.jsonl` is a separate messages-format export of reviewed original
answers: mathematical formula-proof steps for natural language, and the aligned
trusted reference for Lean. It is intended for explicit public-curriculum reuse,
not as hidden-test data. It does not automatically train or call a model.
The original family, split and content binding are retained. Reference answers,
the full pilot ZIP and expert-only material must not enter closed-book prompts.

No restricted ATLAS material/index/derivative, external solution manual or
Terminal-Bench task content is imported. Follow LICENSE_SCOPE.md. A textbook
source mapping does not grant permission to copy its prose into ML data.

`public-exposure.json` is generated alongside every public export, including
unadmitted public drafts and graph views. It records IDs, family labels, exact
source anchors and per-track prompt fingerprints; it contains no answer,
reference proof or private item. Keep the exact file from each release to retain
evidence of retired public items. The export rejects non-public inputs before
writing files.

An operator can preflight private metadata **offline**, without placing the
inventory, prompts or answers in this checkout:

```bash
python tools/sog_bench_exposure.py --inventory /secure/outside-repo/inventory.json \
  --historical-public /retained/earlier/public-exposure.json
```

Omit `--historical-public` only when there are no earlier snapshots to supply;
repeat it for each distinct retained snapshot. The strict JSON inventory uses
`schema_version: 1`, `kind: "sog-bench-private-inventory"`, `split: "private-test"`,
`source_scope: "project-owned-original-only"`, `public_snapshots` (SHA-256 of
the exact current and all supplied historical public files), and `records`.
Each record has exactly `id`, `family`, `anchors` and `views`. Use stable
lowercase hyphenated IDs; typed anchors are `lean:<owned declaration>`,
`exercise:<canonical source ID>` and `original:<private source ID>`. Reserve
the primary target/source, not every shared foundational lemma. Record view
hashes with `tools.sog_bench_exposure.prompt_sha256`: NL uses exactly
`assumptions` and `question`, Lean uses exact fixed template text, and graph
uses the available fields in `GRAPH_FIELDS` (without reference answers).

The preflight rejects exact overlap in IDs, families, primary anchors or
prompts, and returns counts without echoing private labels. Success does not
detect paraphrases, renamed semantic families, alternate theorem names, or
missing historical exposures; it does not verify provenance, rights or
independent novelty. These still require a private independent audit before
admitting a test. There is no private corpus or evaluator in the public export.

### Bind an independent review to the exact held-out files

After offline review, run the same command with all four additional arguments:

```bash
python tools/sog_bench_exposure.py --inventory /secure/outside-repo/inventory.json \
  --historical-public /retained/earlier/public-exposure.json \
  --prompts /secure/outside-repo/prompts.json \
  --references /secure/outside-repo/references.json \
  --review /secure/outside-repo/review.json \
  --expected-review-sha256 SHA256_FROM_TRUSTED_REVIEWER_CHANNEL
```

Keep all four private inputs outside this checkout, including its ignored
folders. Share only the relevant prompt view with a model. The grader's
solution and rubric, review files, private hashes and family assignments stay
with the trusted operator. These checks do not send data or run Lean.

Both packs are strict JSON with `schema_version: 1`, a `kind`, and a `records`
array. Each record has exactly `id` and `views` keyed by the inventory's track
names. The `sog-bench-private-prompts` pack has the same typed payloads used by
`prompt_sha256`. The `sog-bench-private-references` pack instead has nonempty
`solution` and `rubric` strings for each view. IDs and tracks must match the
inventory exactly, including paired views. Keep proof sources as data during
review; this does not qualify private Lean tasks for the public executor.

The independent reviewer produces a `sog-bench-private-review` JSON object
with `schema_version: 1`, `inventory_sha256`, `prompts_sha256`,
`references_sha256` (all on exact bytes), distinct `author` and `reviewer`
labels, and a `families` array. Each family needs an `{id, decision, checks}`
entry with decision `accept` and all four check IDs: `source-and-rights`,
`family-independence`, `solution-and-rubric`, `tool-and-graph-scope`. The
reviewer should inspect the entire family against past public variants and
reject unsupported graph claims, false difficulty labels, and inappropriate
tool access. Obtain the receipt hash separately from that trusted reviewer;
computing it from an untrusted receipt is not authentication.

`matches-pinned-private-review` means the byte bindings, exact exposure screen,
view coverage and receipt checklist matched. It is **not** proof of the
reviewer's identity, human independence, formal correctness, corpus admission
or a model score. Run it again before execution against the then-current
public snapshots; changes require a newly bound receipt. No private-corpus
export, provider integration or public CI collection is added by this check.

## What can actually be run today?

| Track | Available path | Not certified |
| --- | --- | --- |
| Natural language | Freeze answers with `sog_bench_prose.py prepare`; actual human rubric assessment; archive with `score` | Automatic semantic correctness, authenticated model/human execution |
| Graph JSON | `sog_bench.py grade-graph` scores the exact frozen structural question | Mathematical necessity, full proof closure, unseen generalization |
| Native graph trials | `sog_bench_harbor.py export`; Harbor oracle/nop fixtures in separate Docker verification; inspect the dedicated CI result | A model measurement, all paid-agent compatibility, arbitrary Lean execution, exhaustive security verification |
| Trusted Lean references | `sog_bench.py check-lean` compiles the aligned references using the pinned project | Arbitrary submitted-code safety, source equivalence or model performance |
| Fixed-target Agentic Lean tools | Experimental [Linux compiler workspace](lean-runtime/WORKSPACE.md): bounded checks, one immutable final, official target/axiom comparison and fresh kernel replay; controlled native acceptance is independently reviewed | General hosted execution, exhaustive security, authenticated model performance or unseen generalization |

The experimental CLI's controlled native software acceptance is recorded in
[the runtime evidence](../../runs/20261105-bench-lean-runtime/README.md), separately
from actual provider use. The optional [model bridge](lean-runtime/MODEL.md)
remains staged: code review and synthetic API-shaped fixtures do not establish
a real provider handshake or model measurement. An authorized provider/model
and spending policy are required before paid calls. No API key is bundled in
the static website or portable agent inputs.

Use [EVALUATION.md](EVALUATION.md) for the existing commands, response schemas,
first-attempt denominator, provenance fields and human-grading procedure.
Trusted-reference/oracle software tests are not measured agent scores.

## Expert graph inspection

Every question has an immediately visible library-result card and a deep link
to its actual declaration, or explicitly labelled owning-module fallback.
The expert directory lists each core once, with exact sources, additional owned
support/numbered-exercise answer parts, and coverage boundaries.
`expert-graph-positions.json` exposes those source-derived identities separately
from model inputs. It exports owned result anchors, never the full mixed graph.

A position is not an implication edge. Only the separately replayed compiler
slices carry selected proof-body occurrences; import scans and conceptual
parallels retain different semantics. Source/statement/assumption/proof context
must remain one click away. Supporting Lean is not an aligned QA by default.

## Presentation acceptance

Typography is a lossless projection of reviewed text, not a rewrite of gold.
Explicit TeX and code stay untouched; compact mathematical notation is rendered
as TeX with its exact original token retained. Ambiguous/unbalanced expressions
stay literal instead of being guessed. Real-browser checks cover every core,
rendered assumptions and proofs, graph anchors and desktop/mobile layouts.
Do not accept “one formula rendered” as whole-page readability evidence.

For an expert's declaration deep link, frame the selected node at a readable
screen scale rather than shrinking the whole atlas into tiny text. Keep pan,
zoom and the explicit Fit action for the rest of the unchanged graph. Frame
the selected card in both axes: a readable zoom floor
must not leave a low-row declaration below the clipped canvas.
Small local slices use a bounded-height canvas; exact namespace-qualified identifiers
use compact code typography, not oversized display headings. Muted context
cards remain opaque so behind-the-card edges do not cross their labels. These
are presentation rules, never new dependency or verification evidence.

Mobile acceptance must wait for the contents-drawer transition and reframe the
actual mobile layout. Check the selected node's screen text size and hit-test
its visible centre, not just document overflow. Retain a real screenshot:
an unoccluded document width alone does not establish readable content.

## Standards used and remaining work

[Terminal-Bench](https://www.tbench.ai/) and
[Harbor's task organization](https://docs.harborframework.com/tasks/overview)
motivate separating instructions, environments, solutions and verification.
We reuse that organizational lesson, not their benchmark data or a claim of
ecosystem compatibility. Harbor's [verifier contract](https://docs.harborframework.com/tasks/verifier)
is used by the optional native graph adapter. Its runtime acceptance is separate
from task export, editorial admission and trusted Lean compilation.

The experimental fixed-target Linux CLI has bounded controlled acceptance;
that is not the full evaluation environment or Goal. Required work still
includes validated actual-model harness runs, provider/native bridge acceptance,
authenticated run provenance where available, genuinely new private families,
empirical difficulty calibration and broader domain/textbook exercise coverage.
General hosted execution is not currently provided. No UI badge, scripted
oracle trajectory or repeated reference compilation closes those boundaries.
