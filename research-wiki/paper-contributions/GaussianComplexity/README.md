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
outputs. The original checkout is read-only. The aggregate ASTIS gate now passes
the download stage and is compiling the project; its final result remains
separate from focused compilation. No root imports, canonical Registry status,
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

## Next mathematical packet

Use `ASTIS-SW-GAUSSIAN-COMPLEXITY-regularity`: Lemma 3.4 and Appendix B.3,
the literal source block precision, its spectral interval, and the unique
minimizer of its quadratic potential. Start with:

```text
python tools/astis_publication.py packet --cell ASTIS-SW-GAUSSIAN-COMPLEXITY-regularity
```

Complete the current block packet's semantic/publication and aggregate gates
before admission. Then select the next dependency-ready source region in the
sign route: the actual hard prior and its Gaussian target/normalizing constant,
or the named determinant/Haar ingredients whose exact source contracts are
already visible. Audit the corresponding definitions and freeze their own
Statement Seals before proof search. Do not manufacture a wrapper around an
assumed spectral, posterior or testing estimate. The main lower-bound proof
regions remain individually visible and open.

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
