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
from conceptual proximity. These observations are separate from the root
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

Complete each current packet's semantic/publication and aggregate gates before
independent commit-bound admission. The earlier cache-path failure was repaired
without changing dependency sources. Both subsequent aggregate sessions83319
and34590 are terminal PASS; neither is a live process to poll or restart.
Each subsequent packet requires its own immutable-commit gate; the completed
radial gate is recorded separately below.
The remaining dependency-ready source region is the actual hard prior/Gaussian
law and the Appendix B.2.2 spherical Poisson/density calculation. Fix the next exact
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

## Finite radialized integral packet

`RadialIntegral.lean` proves `radialized_test_integral` under exactly
`n>=3`, `kappa>=4` and `lambda>=0`, including zero. Its starting object is the
explicit already radialized iterated Haar/spatial integral on the right of
Ex60's first equality. It evaluates that object through the right of Eq21.
Writing `p=(n:R)/2`, `a(O)=kappa+1+4lambda-(kappa-1)O_11`,
`F(O)=det(O)sqrt(det A_O)` and
`N(O)=(sqrt(kappa)+1)O_11-(sqrt(kappa)-1)`, the result is

`E[F(O) integral_x exp(-a(O)||x||^2/4)]/(2pi)^p`
`=((-1)^(n-1)(sqrt(kappa)-1)^(n-1)/2^p) E[N(O)/a(O)^p]`.

The actual full orthogonal Haar law, literal existing precision and Euclidean
volume are fixed. Each spatial integrand, the determinant-weighted outer
integrand and the final quotient are genuinely absolutely integrable; all three
are conclusions. Orthogonality supplies `a(O)>=2+4lambda>=2`. The private spatial
provider calls Mathlib's Gaussian integrability theorem and exact integral
formula. The public proof actually calls the existing general B.6 theorem with
a globally continuous extension `h(u)=1/max(a(u),1)^p`; this equals the exact
source weight on every actual matrix entry. No Borel/L1 premise is added.

Continuity on compact O(n) supplies sufficient finite bounds. The source graph
also inventories sharper domination constants, the numerator bound
`2sqrt(kappa)` and the inherited path/minor estimates; these are not claimed as
new separately compiled results. The independently reconstructed source graph
has 37 nodes, 79 AND-edges and six explicit exclusions. Those counts inventory
source coverage, rather than counting separately compiled declarations.

Focused tests passed (2828 jobs): actual spatial integrability at
`n=3,kappa=4,lambda=0`, the odd-dimensional real exponent `3/2` at lambda1,
and the exact even-dimensional coefficient `-1/4` at `n=4,kappa=4,lambda=0`.
The public theorem uses only `propext`, `Classical.choice` and `Quot.sound`.
Expanded anonymous target checking and actual compiler-reference inspection
also passed. Statement/topology audits, independent anonymous decoding and the
fresh whole-module source/exposition review remain separate evidence artifacts.
Current final aggregate, publication and reader acceptance is recorded below
after the immutable local proof commit is checked.

This packet does not identify the starting integral with the original
`H(lambda)`. Constructing the actual Gaussian law and its density, conjugation
covariance, original-mixture radialization/Fubini, spherical uniformity and
Poisson identities remain open. That original-experiment identification is a
concrete next consumer of the analytic calculation; both main lower bounds and
the fixed-spectrum route remain open. No repeated B.6 wrapper is needed.

## Signed literal-kernel rotation packet

`KernelRotation.lean` proves `signed_kernel_rotation_invariant` under the
unchanged AppendixB2 standing bounds `n>=3,kappa>=4`. The explicit local formula
is `p_O(x)=sqrt(det A_O)/(2pi)^(n/2) exp(-x^T A_O x/2)`, with the existing literal
precision and real exponent. For every fixed vector, `det(O)p_O(x)` is genuinely
Haar L1, and for every fixed Q in full O(n),
`E[det(O)p_O(Qx)]=E[det(O)p_O(x)]`. Reflections are included.

Two reachable private providers supply precision/determinant/quadratic
conjugation covariance and actual full-Haar conjugation preservation. The latter
uses uniqueness of the same normalized probability after right translation,
then genuinely calls the existing canonical fixed-left map theorem. The public
average consumes both providers. Finite-dimensional continuity on compact O(n)
proves fixed-vector L1 internally; no covariance, invariance or integrability
premise is passed in by the caller. No duplicate public matrix or Haar primitive
is introduced.

The source-only graph has20 nodes and15 AND-edges with five explicit exclusions.
Focused tests passed2601 jobs: an actual determinant-minus-one coordinate swap
at n3 with real exponent3/2 and vector(1,2,3), plus genuine zero-vector Haar L1
at n4. The public proof uses only the standard three Lean axioms. Exact expanded
target and compiled-reference checking is separate from semantic source review;
final immutable-commit aggregate and reader evidence is recorded after checking.

The first publication transition rejected a provenance-schema mismatch: the
decoder recorded the JSON transport path instead of the packet's canonical
artifact labels. The mathematical reconstruction was unchanged. Superseded
decoder/reviewer evidence is explicitly named in `rotation-semantic-evidence/`;
the corrected decoder result requires a fresh anti-anchored packet-bound review
before publication acceptance. This is an evidence correction, not a theorem
repair or a new mathematical proof route.

This is the fixed-Q step in AppendixB2.2 p4.1 underlying Ex58. The formula has
not yet been identified with an actual `N(0,A_O^-1)` probability density. The
orthogonal-transitivity bridge to `||x||e1`, full Ex58, joint spatial domination,
original-mixture Fubini and H(lambda) identification remain open. The next
consumer joins this fixed-Q invariance to that axis and genuine law/density
identification, then to the already compiled radial integral. Neither main
lower bound, fixed-spectrum experiment nor overall Goal is completed.

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


## Radial packet validation record

The immutable local proof commit `9d13dd93c88ac4536a0a6c1be4e9e2a88c3d0fb7` passed the actual
`python tools/astis.py check` gate with terminal exit0: root library9224 jobs,
root Tests9528 jobs, ATLAS36469 named declarations in26 books and the
forbidden-closure scan. The new radial module is additionally covered by its
focused2828-job test and expanded-type/reference check; no unchanged root
import is presented as new direct consumer coverage.

Contributor, diff-aware publication, semantic-roundtrip and Frontier checks
passed. Both private providers are covered by the fresh accepted independent
whole-module source/exposition review. The frozen-input generated site passed
build and full validation:1008 modules,5075 declarations and77 reviewed teaching
declarations. The affected graph coverage check passed with no omitted required
connections. In the actual browser, the lesson has seven rendered formulas,
no MathJax errors, no initially open Lean disclosures and no horizontal overflow.
Its six mathematical proof steps are visible. The focused graph has five nodes,
four edges and three immediate relations; module ownership is solid, while
source correspondence and semantic review remain dashed. The source-present
partial badge is retained. Compiler-reference evidence, rather than these
structural/curated lines, establishes the actual canonical B.6 call.

This validation note changes no frozen mathematical/publication/Frontier inputs.
The packet remains PROVED_LOCAL; independent commit-bound admission, public
upload, repository integration and purification remain separate. Original
H(lambda) identification, both main lower bounds and the overall Goal remain open.


## Kernel rotation validation record

Exact immutable local proof commit `bbe54fbb3cb46920576915ff0a5ee834ea533982` passed
`python tools/astis.py check` with actual terminal exit0: root library9224 jobs,
root Tests9528 jobs, ATLAS36469 named declarations in26 books and the
forbidden-closure scan. The new module also has its focused2601-job tests
and successful expanded-type/actual compiler-reference check; unchanged root
imports are not represented as direct coverage of the new declaration.

Contributor, diff-aware publication, semantic and Frontier gates passed.
Both private providers have fresh accepted whole-module source/exposition
coverage after independent anonymous decoding. Frozen-input site build and
full check passed:1010 modules,5079 declarations,77 reviewed teaching
declarations. The affected graph coverage check passed with no omitted required
connections. The actual browser lesson has seven rendered formulas, zero
MathJax errors, zero initially open disclosures and no horizontal overflow;
all six mathematical proof steps are visible. The focused branch has five nodes,
four edges and three immediate relations, with solid module ownership and
dashed source/fidelity overlays. Its source-present partial badge is retained.

This README-only validation note changes no frozen mathematical or graph input.
The result remains PROVED_LOCAL. Independent commit-bound admission, public
upload, integration, merge and purification remain separate. Gaussian-law
identification, norm-axis transitivity, original Fubini/H(lambda), both main
lower bounds and the overall Goal remain open.


## Literal norm-axis reduction and exact first-entry exponent

The next bounded source step now has an actual compiled consumer of
`KernelRotation.signed_kernel_rotation_invariant`: the public
`KernelAxis.signed_kernel_radial` closes the literal-function Ex58 norm-axis
average and the immediately following exact O11 exponent evaluation. For every
Euclidean x, the signed average of the unchanged real Gaussian formula equals
the signed average with exponent
`-(kappa+1-(kappa-1)*O_11)*||x||_2^2/4`. Both fixed-x Haar L1 assertions are
proved outputs under the same full O(n) canonical Haar law, n>=3 and kappa>=4.
The normalizer uses the real dimension-half power, including odd n.

Two reachable private providers supply the actual reflection/matrix-coordinate
witness and exact axis quadratic form. Existing Mathlib `reflection_sub`,
`toMatrix_mem_unitaryGroup` and `toMatrix_mulVec_repr` are consumed directly;
zero and equal vectors require no division or added premise. The canonical
fixed-Q theorem, precision and Haar law are reused without local copies.
This exact reuse creates Lean dependencies; it introduces no conceptual-mirror
transport into the separate fixed-spectrum hidden-eigenbasis route.

Production2601 and focused Tests2602jobs passed, with only the standard three
axioms. The concrete n3 vector (1,2,2) has Euclidean squared norm9, distinct from
its coordinate sup-norm square4; the exact reduced exponent and both L1 outputs
are checked. The n4 zero-vector case is also checked. Fully expanded anonymous
type and compiler-reference checks passed. The preproof source statement and
independent strict source topology inventory contain21 nodes,14 AND-edges and7
explicit exclusions; these are source ingredients, not21 public Lean theorems.
Fresh anonymous decoding and independent whole-module/private-provider/source/
six-step exposition review are required for publication admission.

Actual Gaussian probability-law/density identification, normalization and
covariance, joint spatial domination/Fubini, original H(lambda), sharp Ex59
domination, sphere/Poisson, TV/amplification/transcript and both main lower
bounds remain open. The formalized object is an explicit real formula and Haar
average. No Gaussian law, expected-cost adapter or main result is inferred.
The existing model/cost contracts and both lower-bound routes are preserved.
The packet stays local PROVED_LOCAL: exact-commit aggregate, reader/graph
acceptance and independent admission remain separate from integration,
public upload, merge and purification.


## Kernel norm-axis validation record

Exact immutable local proof commit `7c1f88e4a05b3d2757c417c7096d557400fa1e36` passed
`python tools/astis.py check` with actual terminal exit0: root library9224jobs,
root Tests9528jobs, ATLAS36469named declarations in26books and forbidden-closure
scan. The new module is covered separately by focused2602-job tests and a
successful expanded-type/actual compiler-reference check; unchanged root
imports are not represented as direct coverage of this new declaration.

Contributor, diff-aware publication, semantic and Frontier gates passed.
The two private providers and six-step lesson have fresh accepted independent
whole-module source/exposition review after anonymous decoding. Frozen-input
site build and full check passed:1012modules,5083declarations and
77reviewed teaching declarations. Graph coverage passed with no omitted
required connections. Actual browser inspection found seven rendered formulas,
zero MathJax errors, zero initially open Lean disclosures and no horizontal
overflow, with all six mathematical proof steps. The focused branch has five
nodes, four edges and three immediate relations. Module ownership remains
solid, source/fidelity overlays dashed and the source-present partial badge
retained. Compiler-reference evidence separately establishes the actual calls
to the identical fixed-Q theorem and canonical Mathlib geometry.

This README-only validation note changes no frozen mathematical/graph input.
The result remains local PROVED_LOCAL. Independent commit-bound admission,
public upload, integration, merge and purification remain separate. Gaussian
law/density identification, original-mixture spatial Fubini/H(lambda), both
main lower bounds and the overall Goal remain open.


## Literal mixture transform: genuine joint L1 and Fubini

The source H definition, Ex58 and Ex60-to-Eq21 calculation now have one actual
integration consumer: `MixtureFubini.literal_mixture_transform`. Under unchanged
n>=3, kappa>=4 and ell>=0, both original and radial determinant-weighted literal
integrands are genuinely absolutely L1 on the identical full-O(n) Haar probability
times canonical Euclidean volume. Two legitimate Fubini swaps join the original
nested transform to the exact Eq21 scalar expectation.

The proof actually calls canonical `singleBlockPrecision_regular`,
`KernelAxis.signed_kernel_radial` and `RadialIntegral.radialized_test_integral`,
with the same literal precision and actual Haar/spec. Two reachable private
providers use existing GaussianFourier integrability and a compact continuous
prefactor bound. The latter is sufficient for joint L1, but is distinguished
from the sharp source Ex59 prefactor (kappa/(2pi))^(n/2), which is not separately
claimed compiled. Prior B6 sharp-minor/path estimates retain their already
disclosed parent source-only status.

The exact preproof statement was independently source-reviewed and sealed.
The first locator-access gap was corrected before sealing and its original
rejection record is preserved; it was not a mathematical/source correction.
The independent strict source topology inventory covers50 nodes,34 AND/OR
edges and5 exclusions. These are reviewed source ingredients and alternatives,
not50 public Lean declarations. The exact public signature stayed unchanged.
Production2829jobs and expanded anonymous type/reference checks passed; focused
endpoint tests and fresh independent anonymous/whole-module source/exposition
reviews are recorded separately in the accepted packet.

This theorem concerns explicit real functions. Actual Gaussian-law/density
identification, law normalization/covariance and target-mixture/TV interpretation
remain open, as do sphere/Poisson, parameter choice, sign separation,
amplification/transcript, hidden-eigenbasis and both main lower bounds. A
conceptual analogy cannot substitute for those adapters. Both oracle/cost routes
and the other ASTIS integration queues remain unchanged. Local compilation,
independent admission, integration/publication, merge and purification remain
separate; no self-VERIFIED or whole-Goal completion is claimed.


## Literal mixture Fubini validation record

Exact immutable local proof commit `7555f2684b997f8e6375c299493beea90c1200ba` passed
`python tools/astis.py check` with actual terminal exit0: root library9224jobs,
root Tests9528jobs, ATLAS36469named declarations in26books and forbidden-closure
scan. The new module is covered separately by focused2831-job endpoint tests
and successful expanded-type/actual compiler-reference checks; unchanged root
imports are not represented as direct coverage of this new declaration.

Contributor, diff-aware publication, semantic and Frontier gates passed. The
two reachable private providers and six-step lesson have fresh accepted
independent whole-module/source/exposition review after anonymous decoding.
Frozen-input site build and full check passed:1014modules,5086declarations
and77reviewed teaching declarations. Graph coverage passed with no omitted
required connections. Actual browser inspection found seven rendered formulas,
zero MathJax errors, zero initially open Lean disclosures and no horizontal
overflow, with all six mathematical proof steps. The focused branch has five
nodes, four edges and three immediate relations. Module ownership remains
solid, source/fidelity overlays dashed and the source-present partial badge
retained. Compiler-reference evidence separately establishes the actual calls
to identical regularity, norm-axis, radial/B6, Haar/spec and Fubini nodes.

This README-only note changes no frozen mathematical/graph input. The result
remains local PROVED_LOCAL. Independent commit-bound admission, public upload,
integration, merge and purification remain separate. Actual Gaussian-law and
density identification, resulting target-mixture/TV meaning, sphere/Poisson,
both main lower bounds and the overall Goal remain open.


## Actual Gaussian law and exact precision density

The historical literal-only packets above now have their missing Gaussian-law
interface: the actual existing canonical `multivariateGaussian 0 A^-1` equals
Euclidean volume with density sqrt(det A)/(2pi)^(n/2) exp(-x^T A x/2).
`TechnicalLemmas.Measure.GaussianPrecisionDensity` supplies one canonical shared
SPD background theorem for every natural dimension, including zero. This is
standard Gaussian background expanded for the source, not an all-matrices
theorem attributed to Zhou--Suzuki. It consumes the identical existing
isotropic Gaussian density theorem at variance1 and the identical measurable
equivalence density-transport node. Its one private provider builds an actual
invertible Euclidean linear map and verifies its inverse and determinant.

`GaussianLawDensity.gaussian_law_eq_density` is the actual source consumer.
Under unchanged n>=3, kappa>=4 and every full-O(n) input, its exact existing
precision lower bound produces strict SPD internally before the shared call.
No SPD, invertibility, density, Jacobian or normalization premise is added to
the paper-facing theorem. The actual CFC covariance-square-root constructor,
inverse determinant Jacobian, true Euclidean squared norm and real n/2 powers
are checked explicitly. No replacement Gaussian law is defined.

The sealed statement and independent source topology inventory cover24nodes,
18AND/ORedges and6exclusions, rather than24public declarations. The topology
review's B0 precision note is respected: WithLp.ofLp provides coordinates and
the Euclidean norm-square formula, without asserting isometry into the default
Pi sup norm. The proof obtains its Jacobian directly from the canonical
Euclidean linear equivalence. Two exact public signatures remain unchanged.
Production3120jobs, Tests3122jobs and both expanded anonymous types passed.
Tests exercise the n0 volume identity, anisotropic n3 precision diag(4,1,1)
with exact factor2 and real3/2, and probability normalization of the source
density at n3,kappa4 for every full-O input. Both theorems use only the usual
three axioms. Actual compiler references distinguish shared isotropic/transport
reuse from the source regularity/shared-node call.

The fixed-spectrum route is a planned second consumer of this same generic
node and still requires its own SPD adapter. No lower bound is transported
between the determinant-sign and hidden-eigenbasis routes. Target-mixture
construction and H-to-TV interpretation, sphere/Poisson, parameter choice,
amplification/transcript and both main lower bounds remain open. The previous
literal Fubini theorem is unchanged and can use this new law/density interface
only through a subsequent explicit measure/integral adapter. Local proof,
independent admission, public integration and purification remain separate.


## Actual Gaussian law-density validation record

Exact immutable local proof commit `b1d42a4ad7691d33d514dbdb51bbe3a180871939` passed
`python tools/astis.py check` with actual terminal exit0: root library9224jobs,
root Tests9528jobs, ATLAS36469named declarations in26books and forbidden-closure
scan. The new modules are covered separately by the focused3122-job tests and
both expanded-type/actual compiler-reference checks; unchanged root imports
are not represented as direct coverage of the new declarations.

Diff-aware contributor/publication, semantic and Frontier gates passed. Two
anonymous decoders and two fresh anti-anchored source reviewers independently
checked the exact generic/source statements, actual whole modules/private
provider and all seven/three mathematical proof steps. The true Euclidean
norm, matrix inverse/square-root, determinant Jacobian, real n/2 and generic
zero-dimensional boundary were preserved. The all-SPD theorem is explicitly
standard background, not an all-matrices result attributed to the paper.

Frozen-input site build and full check passed: 1017modules, 5089declarations
and 77reviewed teaching declarations. Both new cells passed graph coverage.
Actual browser inspection of the generic/source lessons found eight/four
rendered formulas, no MathJax errors, no initially open Lean disclosures and
no horizontal overflow. The focused source graph keeps ownership/import
structure solid and source/fidelity overlays dashed, with the partial
source-present badge retained. Actual compiler-reference evidence separately
establishes source-to-shared and shared-to-isotropic/transport calls.

This README-only note changes no frozen mathematical or graph inputs. Both
declarations remain local PROVED_LOCAL. Independent commit-bound admission,
public upload/integration, merge and purification remain separate. Target
mixtures/H-to-TV, sphere/Poisson, both main lower bounds and the overall Goal
remain open. The fixed-spectrum consumer is planned and requires its own SPD
adapter; no determinant-sign lower bound is transferred to that route.


## Actual signed Gaussian expectation through Eq21

`GaussianExpectation.actual_gaussian_transform` now makes the density-based H
calculation an actual canonical Gaussian test-expectation calculation. Under
unchanged n>=3,kappa>=4,ell>=0, every full-O input has genuine test Gaussian L1,
genuine weighted Euclidean-volume L1, and equality between the two actual
integrals. The signed Gaussian expectation is itself absolutely Haar L1 and its
Haar average equals the exact Eq21 coefficient and O11 scalar expectation.

The proof derives continuity and 0<t<=1 from ell>=0, uses actual canonical
Gaussian probability for test L1, and calls the identical
`GaussianLawDensity.gaussian_law_eq_density`. Nonnegative finite measurable p_O
allows the existing Mathlib withDensity integrability and Bochner-integral APIs
to supply weighted-volume L1 and exact expectation transport. The identical
`MixtureFubini.literal_mixture_transform` supplies joint L1; its integrated
sections give outer Haar L1. The same pointwise transport and exact literal
Eq21 parent then evaluate the actual signed Gaussian expectation. No new
Gaussian/Haar constructor, generic withDensity wrapper or copied Fubini proof
is introduced. No measurability or L1 conclusion is a public premise.

The exact statement was independently source-reviewed and sealed before proof.
A separate source-only topology review covers22nodes,18ANDedges,14exclusions;
these are source/background ingredients, not22public Lean theorems. Production
3129jobs and focused Tests3131jobs passed. The tests exercise n3,kappa4,ell0
real p_O-volume integral1 and actual endpoint signed Haar L1, plus n4,kappa4,
ell1 actual Gaussian test expectation with exact -1/4 coefficient and denominator
9-3U. Only the usual three axioms occur. Expanded anonymous type and actual
compiled references to the same density, Fubini, Haar and transport APIs pass.

The source H definition is literally written using p_O. This packet rigorously
identifies that H with the actual Gaussian signed test expectation; it does not
construct determinant-conditioned target-mixture measures, prove component
half-mass, or implement Ex57/Eq20 H-to-TV. Sphere/Poisson, parameter choice,
amplification/transcript/eigenbasis and both main lower bounds remain open.
Sharp Ex59/B6 estimates retain the unchanged disclosed parent boundaries. Both
oracle/cost routes and the other ASTIS queues remain unchanged. Local proof,
independent commit-bound admission, public integration and purification remain
separate, and the overall Goal remains unfinished.


## Actual Gaussian expectation validation record

Exact immutable local proof commit `c240ec0d44a084b30b51b17f8e9669d73bbf601d` passed
`python tools/astis.py check` with actual terminal exit0: root library9224jobs,
root Tests9528jobs, ATLAS36469named declarations in26books and forbidden-closure
scan. The new declaration has separate focused3131-job tests and successful
expanded-type/actual compiler-reference checks; unchanged root imports do not
claim direct coverage of the new module.

Diff-aware contributor/publication, semantic and Frontier gates passed. The
anonymous decoder and fresh anti-anchored source reviewer accepted the exact
current whole module and all five mathematical proof steps. The preproof seal
and separate exhaustive source topology22nodes18ANDedges14exclusions passed;
these source ingredients are not22public Lean declarations.

Frozen-input site build and full check passed:1019modules,5090declarations
and77reviewed teaching declarations. Graph coverage passed with no omitted
required connections. Actual browser inspection found6rendered formulas, no
MathJax errors, no initially open Lean disclosures and no horizontal overflow,
with all five proof steps. The focused branch has5nodes,4edges and3immediate
relations, with solid ownership, dashed source/fidelity overlays and retained
partial/source-present status. Actual compiler references separately establish
the exact GaussianLawDensity/MixtureFubini/Haar and measure-transport calls.

This README-only note changes no frozen mathematical or graph inputs. The
packet remains local PROVED_LOCAL. Independent commit-bound admission, public
upload/integration, merge and purification remain separate. Conditioned target
mixtures, H-to-TV, sphere/Poisson, both main lower bounds and the overall Goal
remain open. The hidden-eigenbasis route remains distinct.


## Determinant-component prior normalization

The preceding intake and accepted proof pages were published through PR326,
merged at `d349d2a16590b55f704ffe6963c021f96cb185c6`. The deployed GitHub Pages
build has that exact content tree. Historical local-only notes above describe
their original validation times; merge does not imply purification or a full
paper theorem.

The new `DeterminantComponents.component_probabilities` proves that actual full
orthogonal Haar gives mass1/2 to each determinant sign and that the literal
measures2 times each restriction are genuine probability priors. Its sole
non-typing premise is n>0. This elementary background extends the source's n>=3
application explicitly; n0 is excluded, and a focused test proves its negative
event has mass0. There is no kappa/ell, supplied reflection, partition,
measurability or half-mass premise.

The actual same canonical Haar/spec/left-invariance declarations are consumed.
Determinant continuity and orthogonality provide the Borel binary partition;
a locally constructed coordinate reflection exchanges its events, so their
masses agree. Probability additivity and finite ENNReal arithmetic give1/2.
Restriction/scaling then give actual total mass1 for both priors. These are
mathematical probability-law conclusions, not a new characterized constructor.

The pinned paragraph asserts half-mass but omits its elementary symmetry proof.
The source-first graph retains that omission explicitly; the current background
proof supplies it without inventing an explicit author proof. Independent
statement review, source-only reconstruction and separate strict13inventory/
5node/5consumer-edge coverage review passed. Anonymous decoding and fresh
current whole-module/source/five-step exposition review passed, recording three
informational distinctions (domain extension, normalization expansion, supplied
background proof), with no repairs. These are not5public Lean declarations.

Production2596jobs and focused2597jobs passed, with the usual three axioms only.
The expanded anonymous proposition and actual compiler-reference check passed.
Root imports and the focused root test are wired, without Registry or
self-VERIFIED promotion. Exact-commit aggregate/site/graph/browser and public
integration remain separate validation steps recorded below when terminal.

This packet does not construct the actual Gaussian target mixtures, identify
their test expectations with the conditional nested integrals, prove the H-to-TV
adapter, or prove spherical/Poisson, transcript, parameter or either main query
lower-bound result. The hidden-eigenbasis route, deterministic query cap, exact
matvec oracle, TV convention and parameter contracts are unchanged.

Validation at immutable proof commit
`3b1fe108dfde806011500a5961704dff37c3967f` passed the canonical aggregate:
9240 library jobs, 9559 root test jobs, ATLAS36469 declarations in26 books and
the forbidden-closure scan. The source-bound site receipt matches digest
`1dc2f56f3a0674c6da109a1f2107723a3b1da3d7a15cb495d71cb334200a94f2`.
Frozen site build and full check passed:1027 modules,5101 declarations and77
reviewed teaching declarations. Required graph coverage has zero omissions.
Actual local browser inspection confirmed six rendered formulas, five proof
steps, no formula errors, no initially open Lean and no horizontal overflow.
The focused graph retains solid structure, dashed source/fidelity relations
and PARTIAL/source-present status. Independent commit-bound integration review
accepted this exact proof commit and preserved the other queues and ledgers.
This README-only validation note changes no mathematical or generated-site
inputs. Public merge, deployment and post-merge purification are separate;
the packet remains PROVED_LOCAL rather than self-promoted VERIFIED.


## Actual conditioned Gaussian mixture laws

The new GaussianMixtureLaws.actual_mixture_laws constructs the literal source
single-block mixtures as actual measure binds. At exactly n>=3 and kappa>=4,
it proves actual Gaussian-family measurability, both mixture probabilities and
their evaluations on every Borel event. Joint density continuity and the
identical actual law-density provider discharge family measurability; the
identical determinant-component probability theorem supplies both priors.
No producer conclusion is a caller assumption and no replacement Gaussian,
Haar or characterized kernel is introduced.

Production and concrete constant-test/Borel-ball tests passed3132jobs with
only the standard three axioms. The fully expanded anonymous statement and
actual compiler-reference checks passed. Independent exact statement, separate
source-only topology, anonymous decoding and fresh whole-module/source/formula
exposition review accepted. Source coverage17nodes/20uses/11exclusions/4gaps
is not a count of public Lean declarations. G01/G02/G03 are supplied internally
or by the identical law-density parent; actual mixture density/expectation
interchanges in G04 remain open.

The concise progressive reader keeps conditions, notation and five typeset
proof steps expandable, with exact Lean directly accessible. Root imports and
focused root Tests are wired without Registry or self-VERIFIED promotion.
Aggregate/site/graph/browser and independent commit-bound integration follow
on an immutable proof commit. Merge, purification and whole-paper completion
remain separate. Actual bounded radial-test expectation transport and the 2H
gap, H-to-TV, block products, sphere/Poisson, parameter choice, transcripts and
both main lower bounds remain open. The fixed-spectrum hidden-eigenbasis
route, cost/oracle contracts and other ASTIS integration queues are unchanged.


## Actual mixture expectation transport and signed gap

MixtureExpectation.actual_mixture_expectation_gap proves actual radial-test
L1 under both determinant-conditioned mixture laws, actual component-expectation
L1 under both priors, both real Bochner transports and their exact factor2
signed Gaussian Haar gap. The only mathematical premises are source n>=3,
kappa>=4 and ell>=0, including zero. Measurability, probability laws, finite
nonnegative expectations, real transport and sign partition are internal.
Identical actual_mixture_laws, component_probabilities and canonical Haar nodes
are consumed. Density identification is source alignment and an existing
separate interface, not a mandatory analytic premise of actual bind transport.

The frozen v2 statement, distinct source-only topology, anonymous decoding
and fresh current whole-module/source/five-step exposition were independently
accepted. Source13NODE+14EXCLUDED,14uses and5gaps are not13public Lean theorems.
Production/focused3133jobs and expanded anonymous target/compiler references
passed with only the standard three axioms. Tests include actual zero-tilt L1,
nonzero n4/kappa9/ell1 negative-mixture real transport, and actual signed
zero-tilt expectation0 obtained through the new gap and actual mixture masses.

The progressive page keeps the short typeset gap first, conditions and notation
folded, five formula steps expandable and exact Lean directly accessible.
Root imports and focused root Tests are wired without Registry or self-VERIFIED
promotion; exactcommit aggregate/site/graph/browser and independent integration
are separate acceptance steps. Actual TV inequality, Eq21 composition, products,
spherical/Poisson, parameter/transcript/eigenbasis and both main query bounds
remain open. Postmerge purification and whole-paper completion stay separate,
and other ASTIS queues and oracle/cost contracts remain unchanged.


## Actual radial-test TV bound (Eq20)

ActualTotalVariation.actual_radial_test_tv proves the exact source Eq20 for
the actual determinant-conditioned Gaussian mixtures and source density-defined
H. It reuses the identical compiled Markov TV contraction through an internally
constructed Bernoulli test kernel; actual law/density correspondence, all real
L1/transport, probability and event-supremum conditions are internal.
The exact preproof seal, distinct source topology challenge, anonymous decode,
fresh whole-module/source/five-step reader review and native focused checks
are recorded. Root/site/immutable integration/merge and postmerge purification
remain separate. Numerical B7, product/amplification and both mains remain open.


## Scalar exponential separation floor (B.7 Eq19)

NumericSeparation.explicit_ratio_ge_exponential proves the exact scalar
comparison from the explicit ratio to (1/2)exp(-5n/sqrt(kappa)), at n>=3
and kappa>=4. It consumes identical canonical Mathlib log/exp/order nodes.
Two log tangent bounds provide a sufficient alternative to the original
integral estimate; the source integral identity and sharper8/3 step retain
their separate provenance. Source topology, blind decode and current full
module/formula review are independent; exact boundary and non-boundary tests
compile. Actual TV first ratio, sphere/Poisson, both main bounds, immutable
integration/publication and postmerge purification remain separate.


## Positive selected tilt and denominator matching (Eq22-23)

SelectedTilt.selected_tilt derives the literal source radius0<r<1,
positive ell, both source presentations of ell and the two denominator
normalizations, under natural n>=3 and real kappa>=4 including equality.
The standalone coefficient equality supplies omitted scalar bookkeeping.
The identities hold for every real u; no arbitrary-u denominator positivity
or replacement for the actual O_11 distribution is asserted.

The focused test uses the proved positive ell in the identical existing
GaussianExpectation.actual_gaussian_transform to obtain actual Gaussian
integrability. It does not make that generic producer depend on this new
module. Actual sphere law, Poisson evaluation/Eq24, actual TV first ratio,
amplification, exact oracle/query/cost adapters, fixed-spectrum eigenbasis
and both main bounds remain open. Source/semantic, immutable integration,
publication and postmerge purification remain separate lifecycle gates.


## Actual selected Gaussian normalization before Eq24

PoissonNormalization.selected_gaussian_normalization joins the identical
SelectedTilt and GaussianExpectation nodes. It derives absolute Haar L1 of
the actual normalized coordinate kernel and the exact selected real-power
prefactor, including odd dimensions and kappa4. Actual U=O_11 bounds are
consumed for positivity; no all-real-u positivity is claimed. Canonical
Mathlib rpow, matrix-coordinate, continuity and compact integration nodes
are reused directly without generic helper clones.

The focused consumer normalizes the actual determinant-conditioned Gaussian
bind-mixture expectation gap. Independent source topology, blind decoding
and fresh whole-module/source/five-step exposition review are separate.
Actual sphere pushforward and Poisson values, evaluated Eq24, positive TV
first ratio, amplification, oracle/query/cost and hidden-eigenbasis results
and both mains remain open. Frozen integration/publication and postmerge
purification are separate; no self-VERIFIED/Registry promotion.


## Actual full-Haar first-column transport

ColumnTransport.selected_column_transport proves probability, genuine Euclidean
l2 sphere support, full orthogonal invariance and absolute L1 for the literal
first-column pushforward. It transports the existing selected actual signed
Gaussian expectation to this same law. The concrete consumer transports the
actual determinant-conditioned Gaussian bind-mixture expectation gap, preserving
the factor two. Exact canonical Haar, unitary norm and measure-map primitives
are reused without new generic wrappers.

Canonical normalized surface identification/uniqueness, both Poisson values
and evaluated Eq24 remain open. Invariance is not labelled a compiled surface
measure equality. Positive TV/amplification, exact matvec and worst-query/cost
adapters, hidden-eigenbasis and main results also remain open. Source topology,
blind decoding and current source/exposition review are distinct from final
immutable integration, public deployment and postmerge purification.


## Canonical Euclidean surface-law identification

SphereHaar.column_map_eq_normalized_surface is the one shared actual
full-orthogonal Haar column/surface identity for every existing coordinate.
Its surface measure is literally Euclidean volume.toSphere with finite nonzero
normalization, not a law defined by invariance. Volume-preserving cone maps,
pointwise reflection, actual Haar right invariance and Tonelli on Borel events
prove equality. The determinant-sign Gaussian route consumes that exact node
in SurfaceLaw.selected_surface_transport, retaining actual probability/L1 and
the selected Gaussian expectation. A genuine bind-mixture consumer preserves
the factor two. A second test identifies two distinct actual column marginals.

The hidden-eigenbasis sphere marginal is a planned consumer of this same node;
conditional residual/subspace laws and independence need their own adapters.
Both Poisson values and evaluated Eq24 remain open, as do positive actual TV,
amplification, exact matvec/worst-query/cost adapters and both main lower bounds.
Source topology, blind decoding and fresh whole-module/source/formula review
are accepted separately from frozen native/site/integration and public merge.
No self VERIFIED or Registry promotion; purification and whole-Goal completion
remain separate.


## Local Laplacian product and two actual consumers

One canonical LaplacianProduct.laplacian_mul proves the real product identity
with C2 regularity only at the evaluation point. The orthonormal trace/Parseval
proof includes dimensions zero and one; these local/coordinate/low-dimensional
generalizations of HFT Eq1.19 are explicit. The literal Poisson quotient test
discharges pole exclusion and local C2 internally. The existing compact smooth
graph proof calls the identical compiled node; its public statement and proof
body remain byte-identical while74 duplicate private lines are removed.

See laplacian-product-source-lean-map.json for the precise source/Lean map.
Source-only extraction, distinct topology challenge, anonymous decoding and
fresh whole-module/source/reader reviews are separate from frozen native,
site, integration and deployment checks. No self VERIFIED or Registry change.
Poisson harmonicity, closed-ball mean-value, both AppendixA1 values, Eq24,
actual positive TV, amplification, oracle/query/cost adapters, conditional
hidden-eigenbasis laws and both main lower bounds remain open.
Merged publication does not imply purification or whole-Goal completion.
