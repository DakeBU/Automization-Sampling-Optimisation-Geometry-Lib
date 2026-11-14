# Independent shared-background type/meaning audit

## Scope and type-only result

The sole new read input is the packet with raw SHA-256
`d2d9493c6fd09222fbe183fcb296bd0c104328a462a03f28b7c9930caa9b9e95`.
The packet identifies statement seal
`a5179ed392ef8e55ab470a3a98ebd542e35301f51472e9cdd7bc168a88bafa26`;
that seal's original file was not opened. This comparison uses my already
frozen p14 raw interpretation and R9 exact-type meanings. Those earlier files
have not been revised or newly reinterpreted to fit this proposal.

**Result: no blocking type/definition-meaning issue found for the explicitly
authored shared bridge.** This is not an exact-source-theorem fidelity verdict.
The bridge is a general mathematical background statement authored by ASTIS,
not a theorem printed in the primary paper, not an independent discovery of
such a printed theorem, and not a source repair. Its intended applications in
R9 remain proof obligations. No implementation, library/API search, proof,
build, final anti-review, publication acceptance, or Goal credit occurred.

The packet contains author-supplied classifications and binder annotations;
they were visible. The assessment below follows the exact type and expanded
definitions, not those annotations as an independent verdict. The formalizer
is expressly **not API-pristine**: ROOT's task records prior knowledge of old
R4/R5 private cone proofs and R9 floor APIs, and the packet records
`formalizer_API_pristine=false`. This phase makes no claim of pristine theorem
discovery or independent upstream search.

## Exact statement and relation to the raw source

The proposed declaration is
`AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef`,
signature SHA-256
`283e07e3c85b9a5cce5c3c40f574f23f593dfcca5e35be4d3e2800f378208b19`.
Its full mathematical meaning is:

> On an arbitrary measurable sample space with an arbitrary probability law,
> an integrable real square-matrix-valued function on an arbitrary finite index
> set has a Hermitian positive-semidefinite Bochner integral whenever its
> values are Hermitian positive semidefinite almost everywhere.

The pinned paper's p14 contains an uncentered moment comparison obtained by
dropping a nonnegative/PSD truncation term, then centered and deterministic
cosine-square PSD comparisons. My original raw reading already identified
expectation/order and positivity of the relevant integrals as internal ports.
The paper does **not** state this arbitrary-function/arbitrary-probability-law
lemma with the above quantifiers and hypotheses. Citation to p14 motivates a
background expansion of an omitted step; it does not make this generalized
statement a verbatim or equivalent primary-paper theorem.

The proposed type is suitable as a separate reusable background node. It does
not establish the source Gaussian fourth moments, feature sums, truncated
matrix integrability, centering identity, variance bounds, concentration, or
final Krylov statement on its own. The R9 proof must supply the concrete
premises at each use.

## Every generic binder

| Binder | Independent classification and exact role |
|---|---|
| `{n : Type*}` | TYPING: arbitrary matrix index carrier. |
| `[Fintype n]` | TYPING: finite matrix dimension; no nonemptiness or positive cardinality. |
| `[DecidableEq n]` | TYPING: standard finite-matrix/index infrastructure, not a positivity certificate. |
| `{Omega : Type*}` | TYPING: arbitrary sample carrier, independent of the matrix index set. |
| `[MeasurableSpace Omega]` | TYPING: measurable sample structure, not a choice of Gaussian law. |
| `{mu : Measure Omega}` | Authored background data: the arbitrary law under which this function is integrated. |
| `[IsProbabilityMeasure mu]` | AUTHORED_BACKGROUND_HYPOTHESIS: explicitly restricts this version of the bridge to probability laws. It is not claimed as a necessary premise of a printed source theorem, nor is mathematical maximal generality claimed. |
| `(f : Omega -> Matrix n n Real)` | Authored background data: arbitrary actual random matrix, not an arbitrary symbol for an already calculated expectation. |
| `(hf : Integrable f mu)` | AUTHORED_BACKGROUND_HYPOTHESIS: genuine analytic contract for arbitrary f; expands below. |
| `(hpos : AE_mu (fun omega => PosSemidef(f omega)))` | AUTHORED_BACKGROUND_HYPOTHESIS: actual a.e. full matrix positivity; expands below. |

No hidden project-owned proposition bundle occurs. The input is not the desired
integral-PSD conclusion disguised as a certificate: `hpos` concerns values of
the arbitrary function almost everywhere; the output concerns its actual
integral. The generic theorem is conditional by design. These premises are
appropriate at this reusable arbitrary-function boundary and must not become
new assumptions of a source-facing R9 theorem whose concrete function and law
are already fixed.

## Empty index set and sample-carrier endpoints

`n` may be empty. There is no `[Nonempty n]`, positive dimension hypothesis,
chosen diagonal coordinate, or dimension-normalization denominator in the
signature. A real matrix on an empty index set is the zero-dimensional matrix
carrier; the Hermitian equality remains meaningful and its quadratic sums are
empty. The l2 operator interpretation is the linear-map space on the
zero-dimensional Euclidean space. Nothing in the mathematical statement
requires adding a nonempty-index binder.

This is a type/meaning endpoint assessment, not a Lean endpoint proof. The
eventual generic module must elaborate for arbitrary finite n, including the
empty case, with the stated instances and no added nonemptiness. The supplied
instance receipt is copied from the R9 paired-index context, not a new
generic-empty-index compiler receipt, so this phase does not falsely certify
that compilation check.

`Omega` is also syntactically arbitrary. The existence of a probability law is
already an explicit contract. An empty sample carrier has no probability law
satisfying mass-one normalization, so it supplies no contradictory instance;
there is no need to add an independent nonempty-sample binder. This does not
restrict the separate empty matrix-index endpoint.

## Full definition meanings

**Matrix and PSD.** `Matrix n n Real` is a finite two-index function. The
supplied standard definition of `Matrix.PosSemidef A` is the conjunction of

    A.conjTranspose = A,
    for every x : Finsupp n Real,
      sum_i,j star(x_i) * A(i,j) * x_j >= 0.

For real coefficients the star is the identity, and the Hermitian clause
requires symmetry. For finite n the finitely supported-vector quantifier
captures all finite-dimensional vectors. Thus the premise and output require
full Hermitian PSD. They are not merely nonnegative diagonal entries,
entrywise nonnegative entries, or a quadratic condition lacking symmetry.
There is no conversion to complex coefficients or claim of complex generality.

**AE.** `forall^mu omega, PosSemidef(f omega)` means the complete PSD property
holds outside a mu-null exceptional set. It is not pointwise positivity at
every omega, nor positivity of an unspecified representative or of a proposed
expected matrix. The full Hermitian and all-vector quadratic property are
inside the a.e. predicate. In an R9 application, pointwise PSD can supply this
weaker a.e. requirement internally without imposing a new source assumption.

**Integrable.** The literal definition expands `Integrable f mu` to an a.e.
strongly measurable representative together with a finite extended-norm
integral. This includes the required measurability/integrability content,
rather than a bare finite coordinate formula. `hf` is meaningful for the
arbitrary function in the generic statement. R9 instead fixes its concrete
functions and must establish the same property from those definitions.

**Norm and Bochner integral.** The supplied definition excerpts give the
L2Operator matrix norm by identification with continuous linear maps between
Euclidean spaces. The supplied actual normed-ring/normed-space prints use the
L2-operator instances; the complete matrix structure is standard finite
dimensional. This fixes the integrability/Bochner meaning rather than leaving
the matrix's underlying function type to imply an entrywise sup norm. The
generic conclusion contains no explicit norm inequality, so this bridge
itself is not a variance norm theorem.

The literal Bochner integral definition is total and returns zero if its
integrability/completeness branch fails. Here `hf` explicitly supplies
integrability, and the intended finite-dimensional matrix carrier is complete.
Acceptance of the future proof must therefore refer to the genuine Bochner
integral, not exploit a failed branch. No arbitrary `expectedMatrix` replaces
the integral. Original receipts/library files have not been opened: the
supplied string meanings and instance prints, not fresh runtime synthesis,
are the evidence available in this phase.

The ordinary matrix multiplication excerpt also matches the prior R9 square
meaning. This generic statement has no matrix product in its signature; it
does not independently prove that a given R9 ordinary square or residual is
PSD.

## Isolation from unchanged concrete R9 binders

The new packet reproduces the concrete R9 uncentered target. Its exact
signature recomputes to
`d5ac54443c79ea7b35b09ddcd6b5e3c40bef081bbe4f196cae5ab3ead35aa2ea`,
the same signature hash frozen in my previous R9 type phase. Hence its copied
signature is unchanged. It still has only natural d,q and the explicit source
range `2*q+1<d`, and defines the actual original Gaussian product law, physical
rows, closed-cutoff Y, exact features, and explicit variance coefficient.
The output remains Y-square integrability and the actual uncentered PSD bound.

The newly generic `{mu}`, `[IsProbabilityMeasure mu]`, `f`, `hf`, and `hpos`
are binders of the **background theorem only**. They are not appended to that
R9 signature. In a concrete use:

- the original product Gaussian `mu` supplies the probability law through its
  fixed definition;
- f is instantiated with the actual PSD residual/square involved in the
  calculation, not an arbitrary additional input of the R9 theorem;
- integrability and a.e./pointwise PSD for that actual f are proved internally
  before applying the generic bridge;
- any subsequent finite-sum or algebraic identification needed to obtain the
  R9 displayed difference remains internal evidence.

The earlier centered/weighted exact target is not reprinted in this new
packet. Its existing frozen type remains the comparison baseline; I have not
newly read or byte-checked a current centered code/seal file. It had actual
integral means, actual Z and deterministic weights, three squared-integrability
families across both targets, and two genuine l2-operator-norm variance bounds.
ROOT's instruction says those types remain unchanged. The present generic
bridge can be intended for centered-square integrals as well, but does not
discharge their integrability, symmetry, the centered identity, or PSD-to-norm
conversion. Those duties remain internal to the actual target proofs.

Moving either `hf` or `hpos` into the concrete Gaussian target would break this
isolation and the previous binder audit. The present exact copied signature
does not do that. No extra source-facing binder, source repair, or source-error
diagnosis is warranted by this background proposal.

## Seven-slot meaning summary and remaining boundary

| Slot | Assessment for authored background |
|---|---|
| Objects | Arbitrary actual real matrix-valued f and its actual Bochner integral; no Gaussian-specific placeholder. |
| Domains | Arbitrary finite matrix indices, empty allowed; arbitrary measurable sample type and probability law. |
| Quantifiers | Generic over n, Omega, mu, f with the declared contracts; full PSD holds a.e. before integration and for the resulting matrix. |
| Assumptions | Natural generic integrability and a.e. full PSD, plus probability-law domain; none added to R9. |
| Conclusion | Full Hermitian and quadratic PSD of the actual integral, not entrywise positivity or a variance norm bound. |
| Scopes/senses | L2Operator/finite-dimensional Bochner semantics, real matrices, measure-specific AE sense. |
| Constants | No dimension-dependent constant or positivity threshold in the generic statement. |

The theorem's future mathematical proof, generic arbitrary/empty-index
elaboration, compiled dependency reuse, actual residual/square applications,
R9 bounds, all concentration work, and final source/publication review remain
outside this phase. The referenced p14 is preserved as the source motivation
for an authored omitted-step expansion, not promoted to a falsely attributed
printed general lemma.
