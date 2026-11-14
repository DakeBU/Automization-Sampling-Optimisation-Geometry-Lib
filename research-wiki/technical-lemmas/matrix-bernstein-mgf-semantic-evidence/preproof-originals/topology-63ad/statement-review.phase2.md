# Independent pre-proof statement / binder / definition challenge

Review identity: **pre-proof only**. This is not post-proof verification. No Lean implementation, lessons, old reviews, old source graphs, API search, proof construction, or theorem proof was read or executed. Phase 1 source-first notebook and inventory were frozen before this phase.

Reviewed exact ROOT draft `.astis/huanjian-gc-weighted-mgf-20261114/statement-seal.draft.v1.json`, SHA256 `ffd262b268a842b142e3bd115deb0a4b6095a60d6a48010fa5cb702a3064a793`. Exact P signature SHA256 `be468f1df7abfd7159c2188857dc22ea3bbcdc3d40bcf8932d8826e425cd94de`; exact T signature SHA256 `dbdb0f08d11e6ad281af71d13b1abb1953013bd422867306e8e44e3bc1ea7c9e`. Both files' hashes were independently recomputed. The cited proof-free formation receipt reports exit 0 and unchanged HEAD `107eb7d0b519bc77c96e0a9d5ff7df24854bb80b`. That is formation evidence only, not proof evidence.

## Decision

**ADMITTED for exact P/T statement content, binder and definition semantics at pre-proof stage.** No EXCESS premise was found. No mathematical signature change is requested. Complete pre-proof gate remains **HOLD pending the separate source-graph edge/coverage challenge**, not because these signatures are rejected. This review gives no theorem-completion, compiled-proof, source-proof closure, or post-proof approval.

## Every P binder

| Binder | Class | Challenge and disposition |
| --- | --- | --- |
| `Ω : Type v` | TYPING | Arbitrary probability sample carrier; no finite, countability, Gaussian, or atom assumption is inserted. |
| `[MeasurableSpace Ω]` | TYPING | Required to interpret random matrix measurability and expectations. |
| `μ : Measure Ω` | TYPING | Explicit measure carrier for the source probability law. The draft's summary omitted it from the enumerated typing string; record it explicitly in the final audit. |
| `[IsProbabilityMeasure μ]` | STANDING | Source random-variable/probability convention. Needed for actual mean zero and unit coefficient in expectation. It is not an extra concentration or moment estimate. Record it explicitly in final audit. |
| `ι : Type u` | TYPING | Matrix index carrier. |
| `[Fintype ι]` | TYPING | Finite square matrices are Tropp's ambient matrix convention. |
| `[DecidableEq ι]` | TYPING | Matrix algebra indexing support; no mathematical inequality. |
| `[Nonempty ι]` | TYPING | Positive finite dimension convention. No forbidden dimension lower bound such as dimension>=2. |
| `X : Ω → Matrix ι ι ℝ` | TYPING | Real specialization explicitly disclosed. Tropp permits complex matrices; this is deliberately a real restricted interface and must keep that attribution. |
| `hX : AEStronglyMeasurable X μ` | STANDING | Concrete regularity expansion of Tropp 2.2. It is logically redundant with `hintX`, but its content is source-standing regularity, not a smuggled mathematical estimate. Redundancy is not an EXCESS classification here. |
| `hintX : Integrable X μ` | STANDING | Required to interpret source EX and actual expectation linearity. This does not assume centering. |
| `hintSq : Integrable (fun ω => X ω * X ω) μ` | STANDING | Required to interpret source E(X²). One-sided cap permits arbitrarily negative eigenvalues and does not itself ensure finite second moment. The premise expands the source regularity convention; it supplies no upper variance cap or MGF conclusion. |
| `hherm : ∀ᵐ ω, (X ω).IsHermitian` | SOURCE | Tropp's random self-adjoint matrix. Almost-sure qualifier agrees with 2.2. |
| `hcap : ∀ᵐ ω, (1-X ω).PosSemidef` | SOURCE | Exactly lambda_max(X)<=1 for a self-adjoint matrix. It does **not** imply or require X>=-I. The one-sided source boundary survives. |
| `hzero : (∫ X dμ)=0` | SOURCE | Exact source EX=0 under the same μ. No proxy matrix or conditional representative. |
| `s : ℝ` | TYPING | MGF parameter. |
| `hs : 0<s` | SOURCE | Every positive s remains available. There is no s<1, sR<1, or small-parameter cap. |

No independence, index-family sum, variance budget, exponential-integrability certificate, pointwise deterministic proof conclusion, trace inequality, tail threshold, dimension prefactor, or concentration event was added. Exponential integrability for each s>0 must be discharged internally from the actual regularity, self-adjointness and upper spectral cap; it is not a missing source binder.

## Every T binder and meaning-bearing let

| Input / let | Class / definition kind | Audit |
| --- | --- | --- |
| `d q : ℕ` | TYPING | q>=0 is built into the natural carrier; q=0 is included. |
| `hq : 2*q+1<d` | SOURCE | Original Lemma 4.4 arithmetic domain. There is no tau condition or positive-q strengthening. |
| `D=EuclideanSpace ℝ (Fin d)` | literal carrier | Standard d-dimensional real Euclidean column space. |
| `E=EuclideanSpace ℝ (Fin(q+1))` | literal carrier | r-dimensional row space with r=q+1. |
| `Ω=Fin(q+1)→D` | literal carrier | q+1 whole Gaussian columns, not d independent matrices supplied as premises. |
| `μ=Measure.pi (fun _=>stdGaussian D)` | literal law | Actual product of q+1 independent N(0,I_d) column laws. No restriction, renormalization, conditioning, good event, or replacement distribution. |
| `r=((q+1:ℕ):ℝ)` | literal | Exact source r=q+1 with correct real cast. |
| `L=2*r+3*log(1000*d)` | literal | Exact source cutoff. hq guarantees d>=2 and positivity is an internal obligation. |
| `θ i=(i.val+1-1/2)*pi/d` | literal | Fin's zero-based i becomes the paper's one-based i. No half-grid shift. |
| `t i k=if k.val=0 then 1 else sqrt2*cos(k.val*θi)` | literal | Exactly (1,sqrt2 cos θi,...,sqrt2 cos(q θi)). At q=0 only constant coordinate exists; the nonconstant branch is unreachable for indices. |
| `row i ω=toLp(fun b=>ω b i)` | literal | Exactly gamma_i=((g_1)_i,...,(g_r)_i); WithLp changes the normed representation, not its values/law. |
| `Y i ω` | literal | Inclusive `||row||²<=L` branch; `(1/d) gammaouter tensor touter`, else zero. This is the source indicator, not an arbitrary fallback. Kronecker factor order matches gamma tensor t. |
| `mean i=∫ω,Y i ω dμ` | literal | Actual unconditional matrix expectation of Y_i under the original law. No postulated radial coefficient and no proxy mean. |
| `Z i ω=Y i ω-mean i` | literal | Exact source actual centering. Actual integrability/mean-zero identity must be proved inside T. |
| `ρ=2*r*(L+1)/d` | literal | Exact R_* from Ex112. The statement is only on hq; division at zero is not public off-domain semantics. Positivity must be proved, not assumed. |
| `w i=cos((2*q+1)*θi)` | literal | Exact original cosine weight. Signed values are retained. |
| `X i ω=ρ^-1 • (w i • Z i ω)` | literal authored adapter | Normalized actual source weighted summand. This normalization is an authored application of Tropp; it is not claimed as a literal numbered Gaussian theorem. |
| `∀s:ℝ,0<s→∀i:Fin d` | SOURCE parameter range / TYPING index | Every positive s and every row, with all previous definitions fixed. No event-local or existential s interpretation. |

All analytic prerequisites (Gaussian probability law, actual measurability, actual moments, Hermitian property, centering, positive ρ and cap) are internal obligations, not T binders. The only target hypothesis is hq. Original source independence is realized by the literal product law, not assumed as an additional theorem-shaped certificate.

## Conclusion and semantic challenges

P and T both retain `∫ X*X dμ` inside the right-hand exponential. This is actual matrix multiplication followed by actual Bochner integration, not `(∫X)^2`, entrywise squaring, a scalar norm moment, v_*, or an arbitrary variance proxy. The left side uses actual matrix-algebra `NormedSpace.exp`. Matching this algebra exponential with the source spectral exponential is an internal semantic bridge, not a new public hypothesis. Positive semidefiniteness of RHS-LHS is the source Loewner inequality in the correct direction.

The signed-weight issue is resolved in the statement design: P needs only a one-sided cap, while T must internally establish a two-sided norm bound for Z_i before multiplication by w_i, or an equally strong signed spectral argument. A route that merely takes `I-Z_i/ρ>=0` and multiplies by w_i without tracking its sign must be rejected. No absolute-value or positive-part alteration of w_i is permitted.

The second-moment variance chain Ex113–120 is legitimate future consumption. T keeps actual ∫X² and does not ask the prover to establish v_* as an input. Ex121 sum tails, Ex122–128 probability/constant bookkeeping, and the final Ex129–132 ratio argument remain outside P/T scope. Neither the draft nor this admission closes those obligations.

Metadata precision requested without signature mutation: expand the final binder inventory to include μ, its probability instance, both index carriers and s explicitly; retain the real-specialization and authored-external-route attribution. No new mathematical assumptions are requested.
