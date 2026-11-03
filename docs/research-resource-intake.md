# Research resource directory

The `/resources/` reader is Samplinglib's subject-and-purpose directory, inspired
by [Optlib](https://github.com/optsuite/optlib) and the
[Optimization × AI Forum collection](https://optimization-x-ai.github.io/resources/).
It connects the existing seven libraries; it is not an eighth library or a new
formalization Goal. SampleWiki keeps sampling regimes first and research cases
below them. The four-paper mathematical priority is unchanged.

## What is absorbed

- Optlib's mathematical hierarchy: differential calculus → convex analysis /
  function structure → optimality → algorithms. Every Lean module at the existing
  pinned commit is listed, including umbrella files. Its mathematical/tool links,
  textbook topics, publications and references are indexed too.
- The Forum's complete six-category title/link/date bibliography: AI research,
  verification, education, modeling, algorithms, lower bounds/counterexamples.
- A reader-first adaptation: three subject entrances; seven existing textbook /
  research homes; short reading routes; separate category pages; searchable
  titles; initially folded module inventories and source/reuse details.
- Existing Optlib-citing declaration lessons are discovered from their canonical
  `sources` fields. They link to complete formula proofs, adjacent folded Lean
  and graph locations, without copying reviewed exposition or inventing status.

This is **complete inventory intake of the selected source surfaces**, not an
audit, proof reconstruction, code port or formalization of every linked paper.
Recruitment, team lists and obsolete meeting notices are not copied. Books and
papers still require primary-source reading before a theorem can be scheduled.

## Sources of truth

| Fact | Owner |
|---|---|
| Pinned external titles, URLs, supplied dates, module paths/blob hashes | `research-wiki/resource-intake.json` |
| Original subject guides, library navigation and upstream-topic reading contexts | `website/content/resource_guides.json` |
| Lean version and dependencies | Root `lean-toolchain` / `lake-manifest.json` |
| Optlib compatibility pin | Existing `Libraries/FirstOrderOptimization/upstreams.yml` |
| Authored local mathematics and actual proof status | Existing lessons, publication bindings, compiler/review evidence |
| Generated pages | `website/scripts/resource_library.py`; never edit `_site/` |

The guide's seven navigation paths are checked against the existing canonical
seven-library placement map. They contain **no theorem completion state**.

## Refresh once, review the diff

Normal builds/checks are offline and deterministic. Refresh is explicit:

```bash
python tools/research_resources.py check
python tools/research_resources.py source-check
python tools/research_resources.py refresh
python -m unittest tools.tests.test_research_resources
python website/scripts/build_site.py
python website/scripts/check_site.py
```

`source-check` compares the fetched inventory and fingerprints without updating
files. `refresh` writes a proposed metadata diff; it never changes Lean, source
bindings, Frontier Cells, Registry or graph truth. Review changed categories,
links, dates, license findings and source identity before publication. If GitHub
rate-limits the public API, save the authenticated connector's pinned recursive
Git-tree response locally and use `--optlib-tree PATH` on either command. The
tree must identify the recorded commit/tree and be complete. No credentials enter
tracked files. Source structure changes fail closed rather than silently dropping
a category. Intentional source updates also update snapshot-count regression tests.

For Windows, run the same commands with `python` from the repository root;
Linux/CI may use `python3`. No absolute checkout paths or network calls are needed
by the normal website build.

## From a reference to a theorem

Use the existing contributor/theorem-publication protocol, not a new parallel
workflow. Search local declarations, fixed Mathlib, shared cells, existing OpenAI
Math intake/coverage and compatible upstreams first. Read the exact primary source,
audit definitions/hypotheses, choose reuse/adapter/missing/out-of-scope and one
real consumer. Only then claim a substantive theorem packet. Optlib's Lean 4.13.0
is not our Lean 4.33.0: no bulk dependency, automatic compatibility claim or
toolchain downgrade is authorized. The upstream README has several stale paths;
the module inventory uses the pinned Git tree instead. Migrated Mathlib references
are resolved using our fixed Mathlib revision.

New source-facing mathematics still needs the statement seal, explicit hidden
conditions, readable formula proof, adjacent folded Lean, independent
encoder–denoiser/source review and the existing compiler/publication gates.
Reuse its existing textbook chapter or a clearly labeled extended chapter;
research discovery placement is not a textbook theorem or chapter-completion edge.

## Graph and license boundaries

Resource → subject/chapter links are navigation/reading-context overlays, never
solid Lean dependencies. No new Functor Hypergraph bridge is inferred from a
title or directory category. Exact local graph links reuse existing declaration
identities. Bibliographic intake alone does not change Registry counts or any red
frontier.

A native admission is the Optlib subgradient-method packet in
`AutoSamplingTheory/TechnicalLemmas/Analysis/SubgradientMethod.lean`: supporting-vector
norm control, the actual-update weighted energy telescope, and a finite best-iterate
bound. It reuses the existing `SupportsAt` predicate and is imported by the main
analysis library, Registry and root Tests. The nonconstant nonsmooth absolute-value
run is exercised in `Tests/Shared/SubgradientMethod.lean`. The extracted weighted
intermediate explicitly permits zero steps and the empty horizon; the normalized
best-iterate theorem requires positive steps and a nonempty horizon. No oracle
selection, asymptotic iterate convergence or sampling guarantee is inferred.
Publication bindings, independent semantic review and the current code hash drive
the native-result panel on the Optlib page; source citations alone cannot enter it.

Optlib is Apache-2.0; copyright stays with its authors and any later code port
must retain applicable notices. No explicit reuse license was established for
the Forum site. Only factual bibliographic titles, links and listed dates are
indexed; no site code, design assets, abstracts, proofs or prose are copied.
Forum dates/AI-assistance categories are source-supplied, not independent audits.
No endorsement or participation of either project is implied. Every resource
stays `external-reference`, regardless of upstream claims.

Check browser rendering after changes: readable subject hierarchy, working
search/folds, MathJax title fragments, desktop/mobile wrapping and existing source
reader links. Use the finite `check_resource_library_browser.py` test; it closes
its own server/browser. Record the scope in the existing PR, not another ledger.
