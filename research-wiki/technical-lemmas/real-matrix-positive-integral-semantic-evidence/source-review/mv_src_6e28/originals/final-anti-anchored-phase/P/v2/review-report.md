# Final independent source-facing review — P v2

**Decision:** accept source fidelity as `equivalent-after-elaboration` for the
actual **uncentered** squared-moment result, with the v2 reader explanation.
The canonical overlay is `source-reviewed` with child
`source_review.state=accepted`. This grants no centered/weighted variance,
concentration, whole R9, full Lemma 4.4, integration, or Goal credit.

The accepted anti packet is v2, raw SHA
`7a5c5006648fde850a9f8631d6d7c51be0df95d8d6c663298d67acffc15773ff`,
canonical SHA `acd49908a2a487fe6bbe0f26e3609bc0c3cb84b185cf0c681ee95d10385f91bd`,
publication binding
`b9cbe04292fb3b39c5f05f867fa2a28b9a4922423ca52ccc0d28e523d5f3b777`.
The prior v1 packet and author files were **not accepted**: their statement
that “variance estimates” were produced inside this proof overclaimed the
implemented scope. My finding and its exact inputs were frozen before the v2
packet was read, under `P/V1-FINDING-FROZEN.json` SHA
`10b2c5b090613e438ae2f830c0b90598b4563812ccd90bc6855df93c1e9ec4c5`.
That record is retained unchanged.

V2 changes exactly the single assumption sentence in each of the two author
files to name the **uncentered squared-moment PSD estimate**. In the anti
packet this changes the corresponding two exposition strings and the binding
and packet hashes. Source text, Lean, decoder and approved context are
unchanged. This is a reader-scope correction, not a source theorem repair.

The complete original decoder reconstruction is byte-identical to the text
embedded in both anti packets, SHA
`4ac774369cb4172253000f5c71b7658584c9888657075b6349bbbf2a18518d26`.
The original decoder run's raw hash is
`55db3b687c9579ec2ed7b784898f1d932a77b2d956a69befb10d4f7d41f90f2e`.
The anonymous input, full original run and original freeze were inspected.
Its run records one anonymous input and no source/implementation/earlier-review
exposure; the inspected input and approved context contain no source identity
or declaration/audit name. Reviewer identity differs from formalizer and
decoder. No guessed source identity is used as reconstruction evidence.

## Seven semantic slots

- **Objects:** both the original C.2 experiment and reconstruction use the same
  r independent standard d-dimensional columns, actual physical rows, exact
  cosine features and actual truncated Y. The reconstruction's x_i and the
  source's gamma_i are the same row under a name change. Paired coordinates
  remain Gaussian first and feature second. No arbitrary mean/law/moment
  witness replaces these objects.
- **Domains:** d,q are natural with `2q+1<d`; source nonnegative integer query
  budgets and dimension are represented discretely. This implies d>=2, keeps
  q=0, and gives exactly r=q+1 coordinates. Fin zero-based rows correspond to
  original physical index i.val+1. The source's kappa condition concerns the
  separate spectral/Krylov setup; this local feature/moment endpoint is
  kappa-independent and asserts no spectral equivalence theorem.
- **Quantifiers:** for every allowed d,q, each physical row's actual ordinary
  square is integrable, and the deterministic sum of its expectations has the
  PSD bound. Neither the cutoff nor the bound constant is an existential
  witness, and there is no event-probability or samplewise conclusion.
- **Assumptions:** the sole explicit proposition is the source range. Gaussian
  product law, row maps, L and features are literal definitions. The cutoff
  inequality is a branch condition, not an assumption on samples. Transport,
  moments, frame, integrability and PSD are internal proof ingredients, never
  new source-facing binders. The main lemma's tau<=1/2 condition belongs to
  its later uniform conclusion, not this local moment endpoint.
- **Conclusion:** the source Ex115–117 uncentered Loewner bound is preserved,
  with full Hermitian/quadratic PSD of the difference. Ordinary Y_i*Y_i is
  integrated, not a Hadamard square, square of the mean, or square of the sum.
  Actual Y-square integrability is explicitly proved as an output; this is a
  source-implicit expectation obligation elaborated without a new premise.
- **Scopes/senses:** all rows are evaluated under the one original
  unconditional column-product mu. Each row keeps its own **closed** event
  norm(row)^2<=L, with zero outside. Expectations are actual complete
  Euclidean-operator-norm Bochner integrals. The conclusion is a deterministic
  bound after integrating, not pointwise PSD of C I minus the random square
  sum. No centered Z or weighted-centered norm result is asserted.
- **Constant dependencies:** r=q+1, L=2r+3 log(1000d), and the exact coefficient
  2r(r+2)/d are preserved. The constant degree has normalization one and the
  other degrees sqrt(2). The half-grid shift is exact under zero-based
  renaming. The coefficient is independent of samples and kappa and is not the
  main Lemma 4.4's unspecified absolute constant called C.

The companion `semantic-slots.json` supplies original/reconstruction text,
relation and evidence for every slot. No blocking semantic delta remains for
the accepted v2 input. There is no theorem repair proposal.

## Raw source, source map, proof and current reader consistency

My raw source interpretation was frozen before seeing any new target type.
The final comparison re-read its exact pinned grid, Lemma 4.4 range, C.2 p1,
Fact C.5, p10, p12 and complete p14 extracts. The reviewed local endpoint is
Ex113–117. The later Ex118–120 centered comparisons remain real source content
but are outside the implemented claim; p15 remains excluded.

The draft source map's 22 source/code spans verify against the frozen original
HTML and independently read whole code, including byte and character offsets.
Its source claims agree with the actual mapped use sites: original experiment,
row law plus radial moment, literal rank/tensor square and closed indicator,
PSD majorant residual, genuine integral assembly, and exact frame coefficient.
It does not substitute the generic S theorem for the whole Gaussian proof.

The already independently reviewed full body proves the actual fourth-moment
and majorant integrability contracts, transports through the noninjective
physical-row map using the correct map-integral theorem, proves each actual
Y_i^2 equals its closed indicator times W_i, and integrates a genuinely
integrable **PSD residual**. It then evaluates the fixed tensor/scalar means,
uses the exact source half-grid/frame bound and adds PSD differences. The
source's omitted analytic steps are proved internally. No final pointwise
C I-minus-random-square certificate is an input. These facts are recorded in
the earlier independent whole-code freeze; no compiler result supplies them
to this source review.

The current v2 lesson's four formula steps and their complete conditions agree
with this proof route. All four adjacent folded Lean blocks concatenate
**byte-exactly to the full module**, including imports, operator-norm scope,
literal statement, every proof line and namespace end. The packet's current
module is identical to the pre-decoder whole-code freeze. The lesson and
publication assumptions agree with the v2 packet, and the full publication
payload recomputes to its advertised binding. The corrected sentence now
agrees with the explicit unfinished-centered boundary throughout the lesson
and source scope.

The immutable candidate is commit
`9964c33c4599f85d27dc8687e8bd6fdb5c44ff49`. A bounded `git show` check only of
already read code/author files verifies exact equality to the frozen inputs;
no commit history or historical evidence was read. The generic S node is a
separately attributed authored background, materially consumed internally
without adding assumptions to P.

## Exposure and remaining authority boundary

Packet/author `compiled:true` and compiled-source labels were incidentally
visible and disclosed, as were ROOT messages about custody/correction runner
exit0. No compiler/native output was read or generated, and none of those
labels or messages is used as independent compilation evidence. No SG/TC,
other reviewer verdict or canonical audit was read.

This accepts only the exact source/Lean/reconstruction/v2-explanation fidelity
of the actual uncentered result. Kernel truth, centered T, concentration,
whole R9/Goal, publication gates, integration, public delivery and
purification remain separate. V1's unaccepted finding remains preserved.
