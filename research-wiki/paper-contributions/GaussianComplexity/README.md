# Gaussian sampling complexity: dedicated SampleWiki lane

Source: Zhou and Suzuki, [On Complexity of Gaussian Sampling, arXiv:2610.20492v1](https://arxiv.org/abs/2610.20492v1).

This lane was requested on 2026-10-17 in its own chat and active Goal. It does not
reset the existing four-paper ASTIS Goal, alter its phase order, claim its
stabilization queue, or start a detached ASTIS process. The chat heartbeat resumes
one bounded packet per run. Read current Frontier Cells and accepted publication
evidence before scheduling; this intake is not a second proof-status registry.

## What the intake supplies

- The canonical companion model now contains a fifth source case with two
  separate main theorem contracts, formula proof routes, a method comparison,
  and an explicitly incomplete source proof outline.
- The generated reader is
  `example-cases/samplewiki/companions/gaussian-sampling-complexity.html`.
  The same canonical source feeds the interactive workspace and downloads.
- `source-review.json` is independent source-intake review. It does not certify a
  Lean proposition, Statement Seal, semantic round trip, or full paper proof.
- The source index records the fixed HTML content hash. The original HTML is an
  ignored local cache at `.astis/gaussian-complexity/2610.20492v1.html`; the tracked
  reader contains attributed restatements and links, not the full source file.
- `conceptual-mirror.candidate.json` records the reviewed mechanism correspondence.
  The global Functor Hypergraph retains its hypothesis map and failure boundary;
  there is no certified reduction, functor or Lean equivalence.

## Current bounded mathematical packet

The literal single-block precision and the source equation (26) now compile in
`AutoSamplingTheory/ExampleCases/GaussianComplexity/DeterminantFamily.lean` under
Lean 4.33.0 and the pinned Mathlib revision. The proof derives norm preservation
from orthogonality, applies the finite-sum Cauchy–Schwarz inequality internally,
expands the literal quadratic form and discharges the coefficient sign from
κ≥4. No cross-term or spectral estimate is added as a theorem hypothesis.

`Tests/GaussianComplexitySingleBlock.lean` checks the source endpoint n=3, κ=4
and the exact matrices A_I=I and A_{−I}=4I. The theorem uses only the standard
Lean axioms `propext`, `Classical.choice` and `Quot.sound`. The versioned Statement
Seal, independent source-only proof graph and distinct topology review are
stored beside this README. Their acceptance covers this bounded region only.
The definition and theorem also have distinct packet-bound source reviews after
anonymous decoding, both `equivalent-after-elaboration`. The definition's larger
algebraic carrier and the elimination of the ambient dimension d are disclosed;
no regularity claim outside the theorem's standing range is imported.

The equation-(26) result is a local compiled candidate, not repository admission.
The next cycle copied all nine exactly pinned dependency repositories and their
build caches into this isolated checkout, with independent Git objects and build
outputs. The original checkout is read-only. The first aggregate ASTIS gate
completed with one Mathlib cache path failure at the Windows 260-character
boundary. The exact unchanged Mathlib checkout was relocated to a shorter
physical path inside this workspace, retaining its original package entry as a
directory junction. The previously failing target then passed (3021 jobs).
The final-candidate aggregate gate is separate from focused compilation.
No root imports, canonical Registry status,
merge or purification state is promoted by this environment change.

This is an expansion of existing orthogonal-matrix algebra and Cauchy–Schwarz,
not a new generic reusable mathematical primitive or a new conceptual transport.
The one route-local precision definition is consumed by the actual quadratic
bound. Mathlib calls retain their canonical identities; no duplicate generic
isometry wrapper or analogy edge is invented.

## Full block packet

`BlockFamily.lean` now constructs the actual equation-(5) matrix on `Fin d` and
proves `blockPrecision_regular` and `blockPrecision_unique_minimizer`. The first
theorem genuinely calls the existing `singleBlockPrecision_regular`. The second
consumes the resulting full lower bound for the actual quadratic potential.
The finite-coordinate adapter maps `(inner,block)` to `inner+n*block`; the
residual starts at `k*n` and disappears when its dimension is zero. Thus this
packet closes the local matrix content of Lemma 3.4 / B.8 rather than merely
assuming admissibility in a new wrapper.

`lake build Tests.GaussianComplexityBlockFamily` passed under Lean 4.33.0.
Concrete tests use identity and negative-identity blocks to distinguish
consecutive coordinates from interleaving, verify the residual identity, and
cover both `d=7,n=3` and the zero-residual endpoint `d=6,n=3`. Both theorems use
only the standard three Lean axioms. Source-only statement and topology reviews
are pinned separately from compilation; final semantic and publication
acceptance remains governed by the current audit fragments and Frontier Cells.

The initial `block-topology-review.json` discloses a read-scope deviation and is
not the strict input-isolated approval. `block-topology-strict-review.json`
records the fresh restricted review. The extractor corrected its route prose:
minimization branches from the full lower bound, while symmetry and both bounds
feed regularity. The actual source edges were unchanged.

## Pointwise determinant normalization packet

`Normalizer.lean` proves the three actual pointwise identities (16)--(18) in
Appendix B.2.1. With `s=sqrt(kappa)` and `M=(s+1)I-(s-1)O`, they are
`A_O=(1/4)M^T M`, `sqrt(det A_O)=2^(-n)det M`, and
`det(O)sqrt(det A_O)=2^(-n)det((s+1)O-(s-1)I)`. All three retain `n>=3`,
`kappa>=4` and the full real orthogonal group, including determinant -1.

The positive determinant is produced internally. Along `aI-tO` for
`0<=t<=b<a`, orthogonality makes a kernel vector satisfy
`(a^2-t^2)||v||_2^2=0`, so it is zero. Continuity and the intermediate value
theorem then preserve the positive sign from `t=0`. The source obtains the same
nonsingularity from a reverse-triangle norm lower bound. That quantitative norm
bound remains a source-graph node, not a separately formalized Lean estimate.
The differing sufficient proof routes are explicit in the authored lesson.

`lake build Tests.GaussianComplexityNormalizer` passes with 2278 jobs, checking
the source endpoint `kappa=4`, both determinant components in dimension three,
and the even-dimensional sign. All three theorem bodies have only the standard
three axioms. Their fully expanded anonymous types were checked against the
actual compiled targets; compiled constants confirm the factorization is used
by the square-root theorem and that theorem by the signed identity. Independent
preproof statement and source-only topology reviews are stored beside the seal.
Final semantic/reader acceptance is governed by the current audit fragments.

This packet alone closes only the pointwise normalization identities. The
reflection cancellation of principal minors, equation (15), actual Gaussian
density/normalization, Fubini and separation remain open. The same canonical
`singleBlockPrecision` is shared by the quadratic/block and determinant routes;
their proof organizations remain distinct. A shared definition is not a proof
that the subsequent estimates or experimental laws are interchangeable.

## Shared full orthogonal Haar probability

`AutoSamplingTheory/TechnicalLemmas/Probability/OrthogonalHaar.lean` now proves
existence and uniqueness of the actual Borel Haar probability on every finite
real orthogonal group. Closedness and the bound on each matrix entry produce
compactness internally; the inherited topology gives second countability.
The actual Mathlib Haar constructor is normalized on the whole compact group,
and Haar probability uniqueness identifies every competing law.

The existence/uniqueness theorem compiled and received independent proof review
before the production measure definition was written. The pre-definition
snapshot and review are retained as `haar-well-definedness-input.json` and
`haar-well-definedness-review.json`. The separately named characterization
genuinely calls the existence theorem, and fixed-left pushforward invariance
genuinely calls that characterization. The definition body itself is the actual
Haar constructor; no compiled call from its body to the existence theorem is
claimed. The earlier theorem gates its introduction as a characterized object.

`lake build Tests.GaussianComplexityOrthogonalHaar` passes (2596 jobs), including
zero-dimensional normalization and a concrete three-dimensional single-row
reflection with determinant -1. All three theorem axiom checks report only the
standard three axioms. Expanded anonymous target types and the constructor body
were checked against the actual compiled declarations. Final source/reader
acceptance is governed by the current four audit fragments.

This is one canonical shared probability law for the determinant-sign and
eigenbasis experiments. Their main theorem consumers remain planned until their
proofs actually call it. Determinant conditioning and half-mass, principal-minor
sign/expectation cancellation, independence from the algorithm seed, adaptive
posteriors and Krylov representation remain distinct open obligations. The
background includes the singleton group at dimension zero; the paper's
two-component assertions are not extended to that endpoint.

## Full Lemma B.6 cancellation packet

`DeterminantCancellation.lean` now compiles the full equation (15) for every
Borel h with E|h(O_11)| finite, retaining n>=3 and kappa>=4. Its other public
theorem proves both integrability and zero expectation of a weighted principal
minor containing a non-first coordinate. No weighted-integrability,
cancellation or determinant-expansion conclusion is supplied as a premise.
The unchanged concrete full Haar law and literal precision are reused.

The checked proof flips one selected row, preserves O_11, and changes the
principal determinant's sign. Finite row multilinearity expands det(aO-bI);
only the empty set and first singleton survive. The final theorem genuinely
calls the earlier signed pointwise normalizer and, through its private finite
average helper, the new public cancellation theorem. These are actual compiled
uses; the sign main theorem remains a prospective consumer.

`Tests/GaussianComplexityDeterminantCancellation.lean` passes 2689 build jobs.
It checks the nonzero exact averages -1/8 in dimension3 and +1/16 in dimension4
at kappa4, plus the globally unbounded h(t)=t. Both public results use only
`propext`, `Classical.choice` and `Quot.sound`. Expanded anonymous target types
also elaborate against the actual compiled declarations and their definitions.

The source-only inventory retains 38 nodes, 62 edges and six explicit
exclusions. Do not read these counts as 38 separately compiled results. The
source sharp bound |det O_(S,S)|<=1 remains source-only: compactness and
continuity give a sufficient finite bound C_(n,S) for the implemented L1 route.
The earlier normalizer similarly used a kernel argument instead of separately
compiling the source quantitative path norm bound2. The English formula lesson
states these proof-route differences without altering the final identity.
Statement/topology reviews, anonymous decoding and distinct current source
reviews are separate evidence; publication admission is checked mechanically.

Older packet boundary paragraphs describe what those individual packets did
not establish. This packet closes local B.6 cancellation, while Gaussian
laws/densities, spherical Poisson identities, Fubini, radial/Hellinger
separation, conditional sign posteriors/transcripts, the eigenbasis argument
and both main lower bounds remain separate obligations. No full-paper,
integration or purification completion follows.

Local reader acceptance for this packet: the generated site builds with
1006 modules and 5072 declarations, and both affected graph coverage checks
pass. The actual browser lesson has ten rendered formulas, no MathJax errors,
no initially open Lean disclosures and no horizontal overflow. The focused
equation-(15) graph shows five nodes, four edges and three immediate relations:
module ownership plus dashed source/fidelity overlays. It retains the partial
publication badge and does not infer a compiled main theorem or an implication
from conceptual proximity. These observations are separate from the live root
aggregate gate and any later commit-bound admission.

Final aggregate evidence: the earlier live session83319 terminated successfully.
A fresh `python tools/astis.py check` then ran against immutable proof commit
`e4048ad785bee06b43ab6a9836353ac32dc6ca53` and also terminated with exit0:
root library9224 jobs, root Tests9528 jobs, ATLAS36469 named declarations across
26 books, and the forbidden-closure scan all passed. The new module's focused
2689-job tests and expanded-type checks remain its explicit compiler coverage;
this record does not pretend that an unchanged root import newly calls it.
The full site check also passed with 77 reviewed teaching declarations. This
paragraph records observed validation of the proof commit without changing its
mathematical inputs; independent admission, merge and purification remain open.

## Admission and next mathematical packet

For the completed local block regularity packet, start with:

```text
python tools/astis_publication.py packet --cell ASTIS-SW-GAUSSIAN-COMPLEXITY-regularity
```

Complete the current packets' semantic/publication and aggregate gates before
independent commit-bound admission. The earlier aggregate gate reached an actual
terminal failure, its cache path issue was repaired without changing dependency
sources, and a final-candidate gate was started. Keep polling that live process;
an observation timeout is not a failure or permission to restart it.
The next dependency-ready source region is the actual hard prior/Gaussian law
and the Appendix B.2.2 spherical Poisson/density calculation. Fix the next exact
source boundary and Statement Seal before proof search, including any genuine
existence/normalization and Fubini obligations. Do not manufacture a wrapper
around an assumed density, posterior or testing estimate, or repeat the now
compiled B.6 cancellation as another theorem-shaped milestone.
Both main lower-bound proof regions remain individually visible and open.

Pinned Mathlib retrieval for the remaining minor expansion found
`Matrix.coeff_det_one_add_X_smul_eq_sum_minors` and
`Matrix.det_piecewise_one_eq_submatrix_det` in
`Mathlib/LinearAlgebra/Matrix/Charpoly/Coeff.lean`. These are source-present API
candidates. The current proof actually uses row multilinearity and
`Matrix.det_piecewise_one_eq_submatrix_det`; the polynomial coefficient theorem
is still retrieval-only. The cancellation consumes the actual shared Haar law
and its fixed-left invariance rather than accepting them as new binders.

Keep the two main consumers separate:

1. `ASTIS-SW-GAUSSIAN-COMPLEXITY-sign`: conditional Haar posteriors and transcript
   equality, radial separation, Hellinger amplification, mixing/triangle, endpoint
   cases and logarithmic inversion for Theorem 3.1.
2. `ASTIS-SW-GAUSSIAN-COMPLEXITY-eigenbasis`: actual fixed-spectrum experiment,
   joint-law-preserving output/Krylov representation with the extra starting
   Gaussian, uniform cosine estimate, actual target moments, and test separation
   for Theorem 4.1. Section 4.4 records limitations of this analysis; Lemma 4.7 is
   not a prerequisite of the positive lower-bound proof.

Every proof ingredient is a dependency obligation, not an additional binder on
the public source theorem. Keep the exact worst-case deterministic cap distinct
from expected cost, and input-averaged hardness distinct from uniform per-input
accuracy. A known spectrum in Theorem 4.1 is the particular hard spectrum, not a
claim that every prescribed spectrum is hard.

## Graph truth and comparisons

Share a Lean node only after the same exact compiled declaration is genuinely
called under matched hypotheses. Source-present files and prospective search
locations are not compiled dependencies. The source outline and its links remain
planned overlays. Source graph versus Lean graph differences must remain explicit
until actual implementation and source coverage have been audited.

The determinant posterior law and the eigenbasis Krylov representation have a
common residual-symmetry mechanism, but are different statements on different
experiments. Keep their adapters and estimates separate in Lean and connect the
mechanism through the typed hyperedge. Compression must preserve hypothesis,
source, constant and oracle boundaries and lossless drill-down.

Read the source discrepancies in the companion model and independent review,
including the conjecture-confirmation claim, the Conclusion's regime conflict,
and the dimension wording in Lemma A.1. Do not silently change the source theorem.

## Environment and validation

The isolated checkout is based on `c1dfb53b3d403d67a6c5fd9acbf236ddd4603487`.
It is sparse: historical `runs/` trees and raw/gzip snapshots are excluded. A full
checkout of those snapshots exhausted disk during intake; the generated copy was
removed without changing the original repository. Never repeat that expansion.
Only small, exact tracked audit artifacts required by the merged semantic loader
were materialized from Git. Obtain any further historical evidence on demand.

The pinned toolchain remains Lean 4.33.0. The initial intake added no Lean
declarations; subsequent bounded packets add the single-block and full-block
matrix definitions, one single-block theorem and two full-block/minimum theorems.
Their focused compiler evidence is distinct from aggregate admission. Before any theorem admission,
run its focused checks, independent source-blind decoding and source review, then
serialize the repository's normal publication, graph, site, root Tests and ASTIS
gates. Follow the active contributor contract; neither metadata validation nor a
website build proves the paper.

The overall Goal completes only after both main lower bounds, required background,
source fidelity, reader delivery and purification are accepted. A source intake,
one cycle, a local lemma, a draft PR or a successful deployment cannot finish it.
