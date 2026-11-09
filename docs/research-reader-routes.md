# Subject readers and the next lower-bound route

This is the 2026-11-09 user-directed reader/formalization lane, coordinated in
[issue #388](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/issues/388).
It does not claim another collaborator's proof cells or replace the four-paper
phase order. Recheck current main, PRs and cell ownership before every proof packet.

## Where things belong

| Reader question | Canonical destination |
| --- | --- |
| Which sampling setting/method should I study? | `sampling/index.html`, then SampleWiki's regime-first directory |
| How does the textbook argument work? | Existing source-aligned textbook chapter/section |
| What does this paper add? | One canonical SampleWiki paper reader: statement → proof route → verified work |
| What cannot algorithms do? | `lower-bounds/index.html`, independent of Log-Concave Sampling |
| What is the finite-state starting point? | `libraries/discrete-sampling/index.html` → actual random-scan law → reversibility → open quantitative adapters |
| What is proved, reviewed or still missing? | Existing publication/semantic/Frontier evidence projected to `/progress/` and the local reader |
| Which lemma is actually reused? | Exact existing `decl:` node and its canonical owning module/lesson |
| Which method is analogous across domains? | Reviewed Functor family with hypothesis adapters; never a fabricated solid Lean edge |

Do not add a paper/frontier classification level inside SampleWiki. Its sampling
regimes remain first. Lower Bounds is a thematic cross-library door, not an
eighth textbook. MCMC is a method lens, discrete is a state-space lens, and strong
log-concavity/LSI are target assumptions. The new nonlinear query paper concerns
continuous targets; it must not be filed as Discrete Sampling.

The first screen should answer the question, show a few meaningful next actions,
and state the proof boundary. Detailed source inventories, evidence and supporting
calculations go behind descriptive disclosures or focused pages. Never put all
Lean in a detached final appendix: keep each exact statement/proof fold beside
the corresponding authored mathematical proof. Avoid duplicated full proof DOM.

## Zhou–Suzuki, arXiv:2611.05813v1

Source/title/authors/license/PDF fingerprint and the three restatements live once
in `website/content/samplewiki_companion_frontiers.json`. The preliminary source
outline is there too. `functor_hypergraph.json` carries the matching citation,
not an invented transport theorem. The source is CC BY 4.0; the reader is an
attributed ASTIS adaptation. No endorsement is implied.

Primary reader: `example-cases/samplewiki/companions/slc-lsi-query-complexity.html`.
Cross-links: Lower Bounds; SampleWiki; the existing textbook research-extension
projection with Chapters 2, 4 and 9 as reading context. These chapter placements
are not source-text theorem claims or new formal dependencies. Optimisation §4
is relevant for the oracle perspective, not a proved rate-preserving reduction.

Keep three closures separate:

1. Theorem 4: measurable exact oracle model, Gaussian conditioning/decoupling,
   gated tensor hard family, algorithm test failure, target mass moments,
   admissibility conditioning and dimension padding. Its §6.5 proof directly
   gives the capped-query bound.
2. Theorem 8: the actual correlated unknown initializer, two-sided warmness,
   shifted-Gaussian comparison, localization/slab estimates, query truncation,
   and padding. One initializer sample is not an initializer-density oracle.
3. Theorem 9: hidden-cap family and test, local/angular/global functional
   inequalities, common Gaussian warmness, parameter scaling and expected cost.
   No convexity premise is added to the LSI class.

The full paper remains open. An outline is not exhaustive source-region coverage
or a Statement Seal. Before a main theorem is sealed, enumerate its substantive
source proof regions and cited/approximation steps, then obtain independent
topology review. Preserve exact quantifiers, measures, constants and domains.

The first integrated packet is Fact 12, §6.4, Eq. (60): for nonnegative real
g,b with g+b>0, `b/(g+b) ≤ b+(1-sqrt g)^2 ≤ b+(1-g)^2`. PR #392 merged this
one independently reviewed scalar edge; its Cell and publication binding retain
the actual evidence. The next packet is the Gaussian symmetry/cosh ingredient
of Fact 10, in the existing Probability layer, not a copy in a paper module.
See `research-wiki/paper-contributions/SlcLsiQueryComplexity/fact10-integration.md`
for the dependency-ready continuation: literal load → conditional iteration →
actual normalizer moments → Theorem 7's normalization argument. These arrows
are a plan until their corresponding Lean declarations actually call each other.
The subsequent applications must prove their own measurability, positivity,
independence and moment bounds; those do not become extra premises of Theorem 7.

## Discrete Sampling work, without duplicate foundations

The previous source inventory's `scaffold` flags do not erase already reviewed
shared heat-bath results. The subject reader resolves the existing
`proof_readers.json` entries and their build/Cell/semantic evidence. It does not
mark the whole CSV chapter formalized. The exact Boolean specialization and
source repair boundaries remain in each focused proof reader.

The next analytic path is finite reversible Dirichlet pair-sum identity →
appropriate gap/entropy contraction → model-specific estimates, not another
stationarity wrapper. Fix total/per-site clock, positive support, feasible
pinnings and discrete-time periodicity. Read the existing reuse audit before
MLSI work: totalized `Real.log` at zero is not standard jump dissipation.

## Maintenance and acceptance

`subject_readers.py` owns the small subject orientation; it links canonical
proofs without copying them. `samplewiki_companions.py` owns the paper projection;
`samplewiki_placements.py` already puts admitted bindings in textbook extensions.
No new progress ledger is introduced. Publication status and compiler graph truth
continue to use their existing sources and checks.

Run focused tests, then the canonical site build/check once on the stable batch:

```bash
python -m unittest tools.tests.test_subject_readers tools.tests.test_lower_bounds tools.tests.test_samplewiki_navigation tools.tests.test_samplewiki_companions tools.tests.test_discrete_sampling
python website/scripts/build_site.py
python website/scripts/check_site.py
```

Run browser checks with Playwright and an installed Chromium browser; on Windows
an existing Edge installation can be selected with `--channel msedge`:

```bash
python website/scripts/check_subject_readers_browser.py
```

The check serves the built site only for its duration, closes the server, and
saves desktop/mobile screenshots under ignored `.astis/subject-reader-browser/`.
Finish the build before starting checks; do not regenerate `_site` while a
validator is reading it.

Actually inspect desktop/mobile entry → statement → proof → adjacent Lean,
rendered MathJax, the new source outline and an existing exact Lean node. Record
PR/merge/deployment separately. Lean changes additionally require the existing
Statement Seal, focused compile, independent encoder–denoiser/source review,
publication/graph gates and root tests. A reader batch does not finish the Goal.
