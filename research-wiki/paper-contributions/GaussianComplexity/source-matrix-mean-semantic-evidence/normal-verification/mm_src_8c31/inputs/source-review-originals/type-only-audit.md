# Independent type-only audit — mm_src_8c31

Verdict: **TYPE_SOURCE_COMPATIBLE; no genuine type/source blocker found in the supplied exact scope.** This is a type-meaning assessment, not source acceptance of an implementation, Lean truth, a proof seal, VERIFIED status, publication, or integration permission. Both proposed targets remain unproved and their production files have not been inspected. Stop after this freeze and await a separately authorized whole-code-only packet.

## Inputs, chronology, and evidential limit

This actor's raw-source freeze remains unchanged: `raw-freeze-manifest.json` SHA-256 `ba9823613a48e245236022989ad22e2e7a9445b27e10beca19fa2add6040b06f`. Its chronology claim was and remains “before this actor's type/seal exposure,” not before creation of the global seal.

The only new artifact read is `.astis/huanjian-gc-source-matrix-mean-20261112/selective-type-definition-packet.json`, 21043 bytes, SHA-256 `efdba6eea9aa32da4cd9ea8d5022548ac128179f1ba73661fefa342f6ca4d95c`. The authorization also exposed the global seal's digest, not its contents: `b55a1acb837288d580a667903987e5f809610626eb4848c750ff8d3a6c01149b`.

The packet includes exact signatures, literal standard-definition excerpts/instance prints, source locators, and the packet author's binder/output/definition descriptions. I treat those descriptions as visible self-descriptions, not as independent review evidence. I independently expanded the visible signatures. No linked receipt, Mathlib file, seal document, chronology, existing API, target implementation, graph, decoder, other review, old delta, or repair was opened. No Lean/native target computation or proof search was performed. The disclosed `formalizer_API_pristine=false` is recorded; it is not a source-fidelity or failure verdict.

The exact signature string digests were recomputed and matched:

- Producer: `099bcbe9d6cc440754282873a7f1e1001584c3566fc771a70bf9f1a3846b85fe`.
- Private consumer: `00c0b050a632e03d9b169acdb6632ae85a9ec43cc2b5e8aa26b7b6152a711b7e`.
- Definition context: `92117d5029065dcbd8e1a218bb175a7c32d37e9dd34ac2f5255125e2f9c48cfa`, reproduced as the supplied JSON object in insertion order with UTF-8, indent 2, and one final LF.

Every supplied literal definition-excerpt digest and the instance-print string digest also matched. This validates the packet's internal byte identities; it does not validate the unopened receipt or an unbuilt target.

## Independent input expansion

The complete mathematical input to each signature is `{d q : Nat}` together with `hq : 2*q+1 < d`. Natural carriers are TYPING; the inequality is STANDING from the original Lemma 4.4. There are no other proof/data arguments, abstract laws, unknown matrices, project-owned proposition bundles, mean witnesses, norm/moment bounds, Gram certificates, or integrability assumptions. All subsequent `let` values are fixed definitions, not caller-supplied propositions. Thus no EXCESS public premise is present in the displayed type.

The local lets instantiate:

- `D = EuclideanSpace R (Fin d)` and `E = EuclideanSpace R (Fin(q+1))`.
- `Omega = Fin(q+1) -> D`, with `mu = Measure.pi (fun _ => stdGaussian D)`.
- `r = (q+1 : R)`, `L = 2*r + 3*log(1000*d)`.
- A canonical scalar `a = (integral under stdGaussian E of norm(x)^2 on the closed norm-square <= L event) / r`.
- The exact half-step angles, cosine features, physical-coordinate row maps, and actual cutoff matrices.

In particular the function `omega` consists of the original q+1 independent d-dimensional Gaussian columns. `row i omega = toLp 2 (fun b => omega b i)` collects coordinate i of those same columns. The actual row law is not supplied as a hypothesis. The canonical product realization matches the source's joint distribution; the signatures do not separately assert a transport theorem for an arbitrary ambient probability-space realization.

The source range includes q=0: then r=1, the feature index has only value zero, t_i=1, and the weight frequency is n=1. The sole range premise becomes 1<d. Every occurrence of d^(-1), division by d, or division by r is therefore nondegenerate by facts derivable from the existing parameters. No q>0, extra d bound, tau cap, or concentration event has been inserted.

## Literal index and cutoff semantics

For physical `i : Fin d`, the expression `(i.val + 1 - 1/2)*pi/d` corresponds exactly to source physical index i.val+1 in {1,...,d}. The feature coordinate `k : Fin(q+1)` uses its unshifted value in {0,...,q}; value zero is 1, and other values are sqrt(2)*cos(k*theta_i). These are the two distinct source index conventions and they have not been confused.

`WithLp.ofLp (row i omega)` is the real coordinate function b -> omega b i. The first `vecMulVec` in `Matrix.kronecker` is its outer product, and the second is the deterministic t_i outer product. The supplied literal `kroneckerMap` body evaluates the first matrix on pair components `.1` and the second on `.2`. Hence both row and column indices are **Gaussian-first, feature-second**, as in the source. The matrix carrier has pairs of Fin(q+1), i.e. r^2 coordinates. Real transpose/outer-product semantics require no complex-conjugation convention.

The branch test is exactly `norm(row i omega)^2 <= L`; the retained branch is d^(-1) times that Kronecker outer product, and the other branch is zero. This is the source indicator on the closed radial cutoff, not a new characterized or fallback object. The definition's zero outside the event is intentional source semantics. It is distinct from the Bochner integral's nonintegrable/default-zero mechanism discussed below.

## The scalar a and the actual common row law

The type defines a under `stdGaussian E`, not under a selected actual i and not by assuming a moment identity. The definition's mathematical agreement with source Ex108 therefore depends on the internal fact that the pushforward of the original product law by **each actual row i** is that same `stdGaussian E`. Independent identical standard scalar coordinates, or an equivalent finite Gaussian-law argument, must establish this internally.

This is the correct statement boundary: one canonical law-defined a appears in all i means, and no independent certificate of its equality with actual-row moments is a premise. A code proof must still identify that canonical radial integral with `E[R_i*1_(R_i<=L)]` in the original experiment and justify the actual radial first moment. The type alone does not prove that bridge. Its absence at an unproved type phase is an **internal applicability obligation**, not a type/source blocker or grounds for adding a premise.

The scalar integrand itself is bounded on the finite-radius retained event and zero elsewhere; measurability and scalar integrability follow mathematically from the actual standard Gaussian setup. Thus its Bochner integral is the genuine radial expectation. The type does not expose scalar integrability as an additional conclusion, but it also does not assume it; the nondefault interpretation is an internal definitional/applicability obligation. No range/bias conclusion for a, independence theorem, or separate public row-moment theorem is claimed by these signatures. Those omissions match the limited new packet rather than pretending to cover all of p12/Ex109.

## Complete Bochner expectation and expanded outputs

The supplied actual instance prints select `Matrix.instL2OpNormedAddCommGroup` and `Matrix.instL2OpNormedSpace` for these finite real matrix carriers. The literal norm excerpt identifies this norm with the operator norm on finite Euclidean spaces. A `Matrix.instCompleteSpace` is also printed for the actual paired-index matrix type. Thus the displayed expectation is a matrix-valued **complete Bochner integral using the L2Operator norm**, not a scalar entrywise integral notation or an unspecified norm certificate. Finite-dimensional norm equivalence explains why this analytic formulation adds no source hypothesis; the code must work in its actual selected structure.

Expanded `Integrable f mu` is `AEStronglyMeasurable f mu` together with finite integral of `enorm(f)`. Expanded a.e. strong measurability is existence of a strongly measurable representative equal a.e. These are substantive properties, but here every occurrence is a target conclusion. No implication has them on its left-hand side.

The producer's output tree is exactly:

1. For every actual i, `Y i` is integrable under the fixed original mu, including the a.e. measurability and finite-norm requirements.
2. For every actual i, its matrix Bochner integral equals `(a/d) * (I_r tensor (t_i t_i^T))`.

The conjunction precedes the universal mean equality. It does not mean “assuming all Y_i are integrable, their means equal ...”. No caller supplies formal mean matrices.

The private consumer's output tree is exactly:

1. The actual unweighted finite random sum S(omega)=sum_i Y_i(omega) is integrable.
2. The actual weighted finite random sum W(omega)=sum_i cos((2*q+1)*theta_i) Y_i(omega) is integrable.
3. The complete Bochner integral of S under the same mu is a times the full paired-index identity.
4. The complete Bochner integral of W under the same mu is zero.

The supplied Bochner definition returns zero when completeness or integrability fails. For the matrix expectations at issue, the actual complete-space print and these explicit integrability conclusions rule out obtaining the theorem only from that default. An eventual proof must establish the full conjunction, not merely simplify an integral branch. This type-only audit accepts neither an unopened instance receipt nor an unimplemented proof as proof evidence.

## Relation to the frozen source endpoint

The producer's first-moment equality is the exact actual-Y_i expectation in C.2 p12.4. Its scalar is tied, through the internal common-law bridge, to Ex108. The consumer uses the same actual Y_i and same scalar and gives **integrals of actual finite sums**. Source Ex110 displays **sums of individual expectations**, and p12.5 then states the actual weighted sum has zero expectation.

These are mathematically equivalent forms in this finite integrable setting, but they are not identical syntax. The consumer must internally derive finite integrability and exchange expectation with the finite sum; for the weighted sum it must also pull out the fixed cosine weights. Applying Fact C.5's two deterministic feature sums and the producer mean gives the unweighted aI and weighted zero. The type contains neither deterministic sum identity as a public binder. Applicability of any existing canonical API for them remains unverified until a permitted implementation review; its name or planned `consumer_edge` is no evidence.

## Seven source-meaning slots

| Slot | Independent type-only finding |
| --- | --- |
| Objects | Fixed original Gaussian columns, actual coordinate rows, literal deterministic t_i, actual closed-cutoff matrices, and a fixed canonical radial coefficient; no substitute mean matrices. |
| Domains | Natural q,d with 2q+1<d, q=0 included, physical Fin d and feature Fin(q+1), r^2 paired matrix indices in source tensor order. |
| Quantifiers | For all such parameters, producer concludes integrability and means for every actual i; consumer concludes both actual-sum identities in the same experiment. a is fixed by a let, not an existential/free witness. |
| Assumptions | Only source parameter range beyond carrier information. Integrability, row-law identification, radial scalar mean, deterministic feature sums, and finite exchange are internal obligations, not premises. |
| Conclusion | Exact individual actual Y_i Bochner means plus explicit integrability; exact actual finite-sum Bochner means aI and zero plus explicit sum integrability. Not a bias/concentration theorem. |
| Scopes/senses | Unconditional expectation under the original product probability law, closed cutoff, real L2Operator complete Bochner sense, Gaussian-first pairs; no event-conditional or high-probability reinterpretation. |
| Constant dependencies | r=q+1, n=2q+1, L=2r+3 log(1000d), and a from the common r-dimensional standard Gaussian radial law at L; no dependence on i, a source-extraneous C, or a supplied mean certificate. |

## Remaining obligations and blocker classification

No genuine type/source blocker is identified. No source repair is proposed. The following remain **unproved internal obligations**, not missing source assumptions:

- The actual row pushforward law under the fixed product experiment is the canonical stdGaussian E for every i, with the scalar radial integral transported accordingly.
- Measurability and integrability of the actual closed-cutoff matrices in the selected L2Operator norm, and of the canonical radial scalar integrand.
- The actual radial matrix mean is aI, with common coefficient derived from that law rather than postulated.
- The deterministic source cosine sums apply with all indices including q=0, and with the actual normalization/order.
- The two actual finite sums are integrable and the exact integrals exchange with their finite sums and fixed weights.
- The eventual module really elaborates these exact types and supplied norm/completeness semantics, and its proof supplies all the above without theorem-shaped premise smuggling or Bochner-default shortcuts.

The first five are mathematically ordinary internal proof obligations in the frozen source experiment. The last is a future implementation/provenance check. None authorizes modifying the sealed public signature for convenience. No implementation/compiler/API failure has been observed or classified at this phase.
