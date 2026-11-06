# License and reuse

## Apache-2.0 for Samplinglib's original material

Effective November 3, 2026, the project makes its original Lean code, tests,
automation, metadata, documentation and website source/exposition available
under the unmodified [Apache License, Version 2.0](LICENSE), unless a file or
identified third-party component states otherwise. This includes the original
material in `AutoSamplingTheory/TechnicalLemmas/Analysis/`,
`AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/` and
`AutoSamplingTheory/TechnicalLemmas/Geometry/`, and their corresponding umbrella
modules. Each contributor retains their copyright; no copyright assignment or
third-party ownership is asserted by this notice.

Reuse, modification and redistribution, including commercial use, are welcome
under the license. Distribute the license, retain applicable copyright and
attribution notices, mark modified files, and carry applicable NOTICE material
as required by Apache-2.0 section 4. The software is provided without warranty.
Citation through [CITATION.bib](CITATION.bib) is appreciated, not an additional
license condition. This project is not affiliated with or endorsed by the
Apache Software Foundation.

## Historical revision requested in issue #351

The grant above also covers project-original versions of the Analysis,
FunctionalInequalities and Geometry modules at revision
[`933dd38de9423d2967bc36b501b3a2006343000d`](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/tree/933dd38de9423d2967bc36b501b3a2006343000d/AutoSamplingTheory/TechnicalLemmas),
subject to the same third-party exclusions below. This is an express grant
made now, not a claim that that historical tree already contained a
repository-wide license. For reproducible redistribution of those versions,
retain the original revision, file headers and provenance, and include copies
of the current LICENSE, NOTICE and this scope statement.

## Third-party boundaries

- Existing file-level and upstream notices remain authoritative. In particular,
  adapted Apache-2.0 modules retain Yuanhe Zhang's copyright and attribution;
  adding the root license does not replace them with project authorship.
- Lean, Mathlib and other dependencies retain their own licenses. A dependency
  or a bibliography entry does not become project-owned code by being linked.
- Source textbooks and papers, PDFs, third-party figures, quotations and other
  external expression remain under their owners' terms. Our license does not
  grant permission to reproduce Chewi's textbook or another author's paper.
  Original Samplinglib explanation and Lean implementation are distinguished
  from these sources in the source-correspondence records.
- `outer_repos/`, `outer_papers/`, `.lake/packages/` and any vendored material
  remain subject to their respective upstream licenses, not this default.
- The ATLAS-v1-derived reference index under
  `research-wiki/retrieval-index/atlas-v1/` and `atlas-v1-*` files retains the
  pinned upstream terms recorded in `Libraries/upstreams/atlas-v1.json`:
  academic/research use only, no commercial use and no ML-model training,
  fine-tuning, distillation, evaluation or development. Copies/projections of
  that restricted index, including generated website data or bundles, retain
  the same boundary. These restrictions are not imposed on unrelated original
  Samplinglib code by the Apache-2.0 grant.
- A component with absent or unclear upstream permission is not made reusable
  merely by this root LICENSE. Check its recorded provenance; request an exact
  file audit when needed. No rights beyond those the relevant licensors can
  grant are represented here.

See [NOTICE](NOTICE), [the detailed source notices](NOTICE.md), and each file's
own provenance. Report any missing attribution or conflicting notice through
[issue #351](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/issues/351)
or a new repository issue.

## Website reuse and entry points

- Website: https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/
- Local build: [`_site/index.html`](_site/index.html), generated with
  `python website/scripts/build_site.py`; build prerequisites are documented in
  [`website/README.md`](website/README.md).
- Sho Sonoda's [Lean-Ridgelet](https://github.com/shosonoda/lean-ridgelet)
  and its [Blueprint implementation map](https://shosonoda.github.io/lean-ridgelet/blueprint/html-multi/overview/#Lean-Ridgelet-Blueprint--L2-theory___-arXiv___2106___04770v2-implementation-map)
  inspired the organization of mathematical explanations, status, dependencies
  and Lean links. As recorded in NOTICE.md, this is design inspiration:
  no Lean-Ridgelet source code, template, stylesheet or mathematical exposition
  is included on that basis. Lean-Ridgelet is Apache-2.0 licensed; its license
  does not grant rights over separately cited textbooks or papers.
- ASTIS's Python generator, project CSS, diagrams and original explanations
  are project material under the grant above. Vendored MathJax under
  `website/static/vendor/mathjax@3.2.2/` is actual software reuse; retain its
  accompanying Apache-2.0 LICENSE and upstream notices in distributions.
- Sho Sonoda does not participate in, endorse or maintain this project.

Temporary `trycloudflare.com` preview URLs expire and are not canonical website
addresses. Preview passwords are not published in this repository.

## Contributions

Unless explicitly identified otherwise, original contributions intentionally
submitted for inclusion are provided under Apache-2.0, consistent with section
5 of the license. Contributors must have authority to license their work,
preserve upstream notices, and clearly identify third-party material and its
license. Do not submit code copied from an unlicensed source. This policy does
not invent consent, provenance or copyright transfers for other people's work.
