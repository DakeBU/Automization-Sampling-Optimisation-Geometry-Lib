# Final independent source-facing review — S

**Decision:** accept source fidelity as `equivalent-after-elaboration` for the
explicitly ASTIS-authored shared background statement and this exact packet /
publication binding. The canonical overlay is `source-reviewed` with child
`source_review.state=accepted`. This is not compiler acceptance or a whole
Gaussian-source/Goal decision.

The reviewed anti packet has raw hash
`d7ac7dcc8d645411d6bec1e8b473ec316658d85c33235bac289e13ac8af6fa2e`,
canonical hash `5fa6bc71b0635cb54edb6a7ffac19435fe3ad5e875b65553dc2bd1614ad0e3a3`,
and publication binding
`b00fd0010a6e17a98b5aecb42259c6e6fee4949e873fc654f5d3c0a1b239489b`.

The exact original decoder input, unabridged reconstruction, original run and
original freeze manifest were copied and checked. The reconstructed text is
byte-for-byte the complete original `reconstruction.md`, SHA
`d603074344160f46d6282e33a6e1666b22bbe0c415692c2ea171ec03fef9673e`.
Its original run hash is
`e9cdc1fd37c4d46d3eef39c1acda5be183d139376c5e7f0aa581af6d08be3dea`.
The supplied run records one anonymous mathematical input and no source,
implementation or earlier-review exposure. I inspected that anonymous input:
its approved definitions give standard finite-matrix/PSD/AE/Bochner meanings
and contain no source/declaration/audit identity or repair. The reviewer
`/root/mv_fresh_source_6e28` is distinct from both formalizer and decoder.

## Seven semantic slots

- **Objects:** both the authored source contract and reconstruction quantify
  arbitrary actual f and its actual integral; neither supplies an arbitrary
  expected matrix. The explanatory A in the reconstruction is an abbreviation.
- **Domains:** both allow every finite real square-matrix index type, including
  empty n, and any measurable sample type carrying the stated probability law.
  Decidable equality is finite-index typing elaboration. No nonempty n appears.
- **Quantifiers:** both are universal over the carriers, law and f. A.e. applies
  to the whole full-PSD predicate, with its all-vector condition within the
  good set. The conclusion concerns one deterministic integral matrix.
- **Assumptions:** probability, actual integrability and a.e. full PSD are the
  same authored generic contracts. They are not new inputs to the actual
  Gaussian target. Strong measurability and finite extended-norm integral
  expand Integrable; no pointwise-for-every-sample strengthening is introduced.
- **Conclusion:** both require Hermitian symmetry and nonnegative quadratic
  form of the actual integral. For real finite matrices this is exactly the
  reconstruction's transpose symmetry and all-vector test, including zero.
- **Scopes/senses:** the same mu governs input hypotheses and integration.
  The actual code explicitly selects the Euclidean operator norm; the
  complete Bochner integral is genuine under hf. Full PSD is not entrywise
  positivity, and no representative certificate or cone-geometry assumption
  is supplied by the caller.
- **Constant dependencies:** no free/existential estimate constant is asserted.
  The only fixed normalization endpoints are probability mass one and
  quadratic-form lower bound zero. There is no dimension positivity threshold.

The accompanying `semantic-slots.json` records original/reconstruction text,
relation and independent evidence for every slot. No blocking delta or theorem
repair is needed.

## Source, code and reader explanation

This is **not** a generic theorem printed in arXiv2610.20492v1. It is the
explicit authored specialization of the pinned `Convex.integral_mem` contract
to the complete real matrix space and its full PSD cone. The actual upstream
46–83 contract was read from the already frozen source. Its closed/convex
premises are discharged in the complete shared body, not passed as new
generic hypotheses. The closed cone includes the Hermitian equalizer and every
continuous quadratic inequality; its convexity follows from genuine scalar
and additive PSD closure. Empty n is preserved by those contracts.

The draft source map faithfully separates external background, authored cone
geometry and the primary paper's concrete need. All nine mapped source/code
spans match their exact byte and character slices. It does not relabel this
authored general theorem as a printed primary-paper result.

The current lesson assumptions, formula and three proof steps agree with this
meaning and the already independently read whole code. All three folded Lean
blocks concatenate **byte-exactly to the entire shared module**, including
imports, norm scope, statement, complete proof and namespace end. The packet's
current module is byte-identical to the whole-code freeze. The full publication
binding was recomputed from the complete current lesson/publication payload,
not merely the reduced anti-anchored context; it equals the advertised hash.

The fixed mathematical candidate is commit
`9964c33c4599f85d27dc8687e8bd6fdb5c44ff49`. Only `git show` for already read
source/author files was used, confirming exact byte equality with the frozen
code and current reader files. No commit history or historical evidence was
read. The independent whole-code report remains part of the evidence chain.

The actual uncentered P body materially calls this shared lemma. Its source
assumptions do not gain hf/hpos binders. Planned centered/weighted applications
are not current completed consumers. The S lesson explicitly preserves these
boundaries, and this review grants none of the absent T/concentration/main
results, integration, public-reader delivery, or purification.

## Exposure and evidence limits

The anti packet and anonymous input include a `compiled:true` metadata field;
that incidental supplied field was visible. No compiler/native receipt or
result was read or generated, and the field is not used as independent proof
of compilation. The original decoder run likewise discloses that metadata.
ROOT's custody-run success statements were visible messages, not mathematical
evidence for this decision. No SG/TC or other reviewer verdict was read.

The accepted claim here is source/Lean/reconstruction/current-explanation
fidelity at the exact hashes, with independent prior whole-code review. Lean
kernel truth and final project admission remain separate.
