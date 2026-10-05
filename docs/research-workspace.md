# Samplinglib research proof workspace

The `/live/` workspace is a theorem- and proof-step-oriented interface between
human mathematical reading, AI assistance, and Lean verification. It is not a
general chat box and it is not a new theorem-status registry.

## Truth and interaction model

The interface keeps four states visibly separate:

1. **Pinned source context** — source URL/version/anchor, full ASTIS statement,
   assumptions, formula proof step, downstream boundary, and bookkeeping data.
2. **AI explanation or candidate** — useful for navigation, reconstruction,
   retrieval and proposed Lean, but always unverified.
3. **Lean certificate** — exact-snippet elaboration/compilation under the pinned
   project toolchain, with diagnostics; it does not certify source equivalence.
4. **Independent source review and admission** — the existing encoder–denoiser,
   focused-test, publication and Registry gates. Only this pipeline can admit a
   blue ASTIS-owned declaration.

The public static site provides layer 1 and portable handoff artifacts. Local
verified mode adds layers 2 and 3. Layer 4 remains the repository contribution
protocol; the workspace cannot assign it.

## Canonical data

The current research workspaces are generated from:

```text
website/content/samplewiki_companion_frontiers.json
```

`website/scripts/research_workspace.py` projects the same theorem statements,
proof steps, source anchors, compiled-support lists and Section 6 bookkeeping
into:

```text
_site/data/research-workspaces.json
_site/downloads/<source>-research-context.json
_site/downloads/<source>-research-context.md
_site/downloads/<source>-research-pack.zip
_site/downloads/samplinglib-research-mcp.zip
```

Do not edit generated downloads or HTML. Update the source companion metadata,
build the site, and let `check_site.py` reject drift or invented support.

Each research pack contains a standalone visual reader, the bounded JSON and
Markdown packet, a manifest, pinned toolchain metadata, and the exact source
modules of attached declarations whose generated declaration record says
`formalizedLocal`. The enclosing paper theorem can still remain red.

## Static researcher workflow

1. Open a source theorem or one of its individual proof steps in `/live/`.
2. Read the formula, explanation, assumptions, strict boundary, and attached
   reusable Lean support.
3. Inspect the recursive-call/error ledger when present. Call count and law
   error are deliberately separate views.
4. Choose an assistant action. Static mode copies a bounded prompt containing
   only the selected context and its evidence labels.
5. Download the context or full research pack for ChatGPT, Codex, or an offline
   review.

The Gaussian-cloud Section 6 workspace is the reference interaction: a reader
can move from the request queue to the deterministic cap, then to an adjacent
conditional-kernel replacement and finally to the one-time cap charge without
losing which pieces have compiled support.

## Local API assistant

The loopback-only `website/scripts/ide_server.py` exposes:

```text
GET  /api/health
POST /api/assist
POST /api/formalize
POST /api/compile
```

`/api/assist` accepts only a workspace id, theorem id, step id, one of the
maintained actions, and a bounded optional question. The server reloads the
canonical generated context instead of trusting source text supplied by the
browser. It calls the OpenAI Responses API only when both `OPENAI_API_KEY` and
`ASTIS_OPENAI_MODEL` are present in the server environment. API credentials are
never embedded in GitHub Pages, JavaScript, exports, or logs.

The response carries the explicit status `ai_explanation_unverified` and no
Lean/source-fidelity certificate. Provider request ids may be returned for
diagnosis, but ASTIS never treats them as proof evidence.

OpenAI's API authentication documentation requires keys to remain server-side:
https://developers.openai.com/api/reference/overview

## ChatGPT plan and MCP App

The downloadable package under `integrations/samplinglib-research-mcp/` is a
read-only MCP App. It exposes tools to list/open workspaces, inspect one proof
step, and export a bounded verification packet. Its MCP Apps widget renders the
proof route and ledger inside compatible ChatGPT/Codex hosts.

The app does not call an AI provider itself, store credentials, run Lean, or
write repository files. A ChatGPT user can connect it in developer mode through
an HTTPS `/mcp` URL when that capability is available on their account. This
lets the host model interact with the structured ASTIS context using the user's
ChatGPT experience without ASTIS receiving an API key.

OpenAI currently documents full MCP developer-mode support for ChatGPT Plus and
Pro. That route is distinct from the website's optional Responses API mode:
ChatGPT subscriptions and API Platform billing are separate. ASTIS therefore
never asks a browser user to paste an API key, and it does not imply that a GPT
subscription pays for `/api/assist`.

Official MCP Apps setup:
https://developers.openai.com/plugins/build/app-quickstart

Official ChatGPT/API billing boundary:
https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform

OpenAI also documents eligible ChatGPT-plan-backed inference for participating
open-source apps. ASTIS does not currently implement or claim approval for the
separate OAuth flow; availability must be checked against current OpenAI terms:
https://developers.openai.com/siwc/quickstart

## Security and deployment boundary

- GitHub Pages publishes static reading, packets and the downloadable MCP App.
- The loopback service is a developer tool, not a hardened public execution
  service.
- A future hosted assistant must add real authentication, per-user quotas,
  request limits, audit-safe logging, isolation and abuse controls.
- A public service must never expose `/api/compile` from the current loopback
  implementation as arbitrary remote code execution.
- ChatGPT/MCP tools are read-only by default. Repository mutation and PR creation
  belong to the existing contributor workflow.
- User-authored claims, AI output, successful elaboration, focused tests,
  source-fidelity review, and merged blue declarations remain distinct states.

## Checks

```bash
python -m unittest tools.tests.test_samplewiki_companions tools.tests.test_astis_ide_server
python3 website/scripts/build_site.py
python3 website/scripts/check_site.py
node --check website/static/research-workspace.js
node --check integrations/samplinglib-research-mcp/server.mjs
git diff --check
```

The full ASTIS/Lean gates remain required before publishing a source revision
that changes mathematical declarations.
