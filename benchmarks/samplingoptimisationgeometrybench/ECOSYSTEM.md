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
For Lean tasks the descriptor fingerprints the fixed-target evaluator and
its policy, not the prose grader. The operator provisions the separate
[isolated Linux workspace](lean-runtime/WORKSPACE.md); the prompt ZIP supplies
neither verifier nor hosted execution. Its tool/retrieval declarations are
not evidence that a run occurred or that retrieval was enforced.

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
from model inputs. The site checks each location against its actual graph;
an indexed module does not mean its declaration is indexed. Standalone
`sog_bench.py export` leaves `node_id` and `graph_url` null unless supplied
the generated graph via `--graph-index PATH`. The `anchor_kind` distinguishes
declaration, owning module, not indexed, and not checked. The exact declaration
and source file remain present even when no graph position is available.
The export never supplies the full mixed graph.

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
