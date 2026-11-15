# R17 fresh source/module reviewer: raw-first freeze

Phase: source-only obligations frozen before target exposure. This document is
not a fidelity verdict, proof admission, source assimilation, module acceptance,
or completed seven-slot comparison.

## Independence and provenance

Reviewer: `/root/matrix_domain_fresh_source_53d8`.

Read before freezing: repository `AGENTS.md`,
`docs/proof-digestion-protocol.md`,
`.agents/skills/astis-semantic-roundtrip/SKILL.md`,
`docs/theorem-publication-protocol.md`, and the PDF reading skill. Mathematical
evidence came only from the following two pinned raw sources and source-only
extractions/renderings made in this owned directory.

* Joel A. Tropp, *User-Friendly Tail Bounds for Sums of Random Matrices*, source
  revised 15 June 2011, raw PDF
  `.astis/semantic-neutral-20261113/bernstein_raw_intake_74ab/Tro11-User-Friendly-preprint.pdf`.
  SHA-256: `f4c3cff8661011395e793972a1f8d9a199fae4ca0fd098535d7a42166cf8fc86`.
  Read complete PDF pages 7, 8, 9 visually and as text: sections 2.1 through 2.7
  and 3.1. Page 1 was checked for title and revision provenance.
* *On Complexity of Gaussian Sampling*, arXiv 2610.20492v1 raw HTML
  `.astis/huanjian-handoff-20261019/2610.20492v1.html`.
  SHA-256: `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
  Read source section `A3.SS2` (C.2), with the experiment and exact formulas
  `A3.Ex107` through `A3.Ex112`, downstream `A3.Ex121` and
  `A3.SS2.p15.2`. Read source Lemma 4.4 and defining displays `S4.E11`,
  `S4.Ex10`, `S4.Ex12` to recover standing parameters and meanings.

Hashes were recomputed from the raw files and match the supplied hashes. No
current Lean, sealed target, anonymous reconstruction, W17, source graph,
prior audit, authored lesson, author-derived restatement, or implementation
context has been viewed. The source-only freeze must remain intact after those
inputs are supplied; any later comparison belongs in a separate artifact.

## Tropp: source meaning and domain obligations

1. **Finite matrices and self-adjoint carrier.** Section 2.1 takes matrices to be
   finite arrays over the complex numbers, square unless explicitly rectangular.
   The finite-dimensional spectral decomposition of a self-adjoint matrix is
   the domain convention of sections 2.3 through 2.5. Real symmetric matrices
   are a specialization. A real-only result must not be advertised as the
   entire complex source result without identifying that specialization.
   The norm is the induced Euclidean operator (spectral) norm, and semidefinite
   comparison means the Loewner order, not entrywise comparison.

2. **Literal functional calculus.** For real-valued scalar `f`, source (2.1) is
   `f(A) = Q f(Λ) Q*` when `A = Q Λ Q*`, with `f` applied to the eigenvalues.
   The source only needs finitely many eigenvalues; it does not impose global
   scalar continuity for this definition. Formula (2.2) transfers a scalar
   inequality on an interval containing the spectrum to the matrix order.
   Later review must identify the actual matrix functional calculus or prove
   equality to it. A syntactically named function without this semantic
   connection is insufficient.

3. **Exponential.** Section 2.4 defines `exp(A)` by (2.1), equivalently by the
   usual matrix power series. For every finite self-adjoint `A`, `exp(A)` is
   positive definite, because its eigenvalues are `exp(λ)>0`. This is a
   deterministic fact. It requires neither randomness nor a positivity
   assumption on `A`. For real `θ` and self-adjoint `X`, `θX` is self-adjoint,
   so the same conclusion applies to `exp(θX)`; it is not restricted to `θ>0`.

4. **Exponential inequalities must keep their senses.** (2.3) is
   `I + A ⪯ exp(A)`; (2.4) is `cosh(A) ⪯ exp(A²/2)`. Source (2.5) says that
   the **trace exponential** is order monotone. Section 2.5 explicitly warns
   that the matrix exponential itself is neither operator monotone nor
   operator convex. Golden-Thompson (2.6) is a trace inequality for two
   self-adjoint matrices. It is not `exp(A+H)=exp(A)exp(H)` and is not a
   three-matrix rule.

5. **Logarithm domain.** Section 2.5 defines the logarithm as the inverse of
   exponential: `log(exp(A)) = A` for self-adjoint `A`. It thereby defines log
   on the positive-definite cone. Source (2.8) has `0 ≺ A ⪯ H`; (2.9) has
   positive-definite `A,H` and `τ∈[0,1]`. The source does not assign a matrix
   logarithm to a singular PSD matrix, an indefinite matrix, or a fabricated
   off-domain default. A total implementation is acceptable only with a
   domain-restricted public meaning and a proved characterization there.

6. **Dilations are a different carrier adapter.** Section 2.6 has
   `S(B)=[[0,B],[B*,0]]`, its block-square identity, and preservation of the
   spectral norm as (2.10)-(2.12). This source material is in the read scope
   but is not a hypothesis of the self-adjoint exponential theorem. No
   rectangular-to-square transition may silently retain the original matrix
   size in a tail prefactor.

7. **Probability and expectation domain.** Section 2.2 makes sufficient
   regularity for expectations and limit interchange a standing convention,
   and often omits the phrase almost surely. Source (2.13) preserves Loewner
   order under expectation for an almost-sure comparison; (2.14) is
   `(E X)² ⪯ E(X²)`. Expectations are genuine finite matrix expectations on
   the stated probability experiment. A totalized integral's zero value for a
   nonintegrable function is not the source expectation.

8. **MGF and CGF domain caveat.** Section 3.1 starts with a random self-adjoint
   matrix having moments of every order, then writes
   `M_X(θ)=E exp(θX)` and `Ξ_X(θ)=log(E exp(θX))`, `θ∈R`. It expressly allows
   these expectations to fail to exist for some `θ`. Thus all finite
   polynomial moments do not supply exponential integrability for every
   `θ`. Its power-series expansions are called formal. A later theorem may
   quantify over all real `θ` only if the concrete experiment supplies
   exponential integrability, or may restrict to the actual MGF domain.

9. **Expectation-to-log bridge, derived obligation.** This is a mathematical
   obligation inferred from the preceding source domain, not a separately
   numbered source theorem: when `exp(θX)` is integrable under a probability
   law and `X` is self-adjoint almost surely, `E exp(θX)` must be shown
   positive definite before taking its source logarithm. An integral of
   positive-definite matrices has positive quadratic form on each nonzero
   vector under this normalized, nonzero measure. Mere PSD, a zero measure,
   or omitted exponential integrability does not discharge that bridge.
   No uniform samplewise lower spectral bound is asserted by the source.

## Gaussian: exact experiment, endpoints, normalization

* Parameters: integer `q≥0`, integer dimension `d` with `2q+1<d`.
  Set `r=q+1≥1`, `n=2q+1`, hence `d≥2` and `2r≤d`.
* Original law: independent `g_1,...,g_r ∼ N(0,I_d)`. Equivalently, rearrange
  the full standard Gaussian coordinate array into independent row vectors
  `γ_i=((g_1)_i,...,(g_r)_i) ∼ N(0,I_r)`, `1≤i≤d`. Expectations and
  probabilities below are on this original Gaussian experiment.
* Deterministic angles: `θ_i=(i-1/2)π/d`, `1≤i≤d` (midpoint grid).
  Coordinates of `t_i` are indexed `j=0,...,q`, with
  `t_i=(1,√2 cos θ_i,...,√2 cos(q θ_i))ᵀ∈R^r`.
* `B∈R^{d×r²}` has row `d^{-1/2}(γ_i⊗t_i)ᵀ`.
  The tensor order is Gaussian coordinate first and cosine coordinate second.
  `D_n=diag(cos(nθ_1),...,cos(nθ_d))`. The block Krylov space is the span of
  `Λ^j g_a` for `1≤a≤r`, `0≤j≤q`; it is not a separately independent sample.
* Fact C.5 gives `||t_i||²≤2r`, `Σ_i t_i t_iᵀ=dI_r`, and
  `Σ_i cos(nθ_i)t_i t_iᵀ=0`, hence untruncated Gram expectations `I_{r²}`
  and zero. The deterministic cosines are weights, not random signs.
* Set `R_i=||γ_i||²` and `L=2r+3 log(1000d)` (natural logarithm).
  Truncation event `T={∀i,R_i≤L}` is **closed** at `L` and has probability
  at least `0.999`. Its complement and the bias use `R_i>L`, strictly.
  The source does not condition the Gaussian law on `T`.

Exact in-scope displays:

| Raw source anchor | Frozen meaning |
| --- | --- |
| `A3.Ex107` | `Y_i=d^{-1}(γ_iγ_iᵀ⊗t_it_iᵀ) 1_{R_i≤L}`, independent truncated PSD matrices of size `r²×r²`. The indicator multiplies the summand under the original law. |
| `A3.Ex108` | `E[γ_iγ_iᵀ 1_{R_i≤L}]=aI_r`, `a=r^{-1}E[R_i 1_{R_i≤L}]`; `a` is the same deterministic scalar for every `i`. |
| `A3.Ex109` | `0≤a≤1`; `1-a=r^{-1}E[R_i 1_{R_i>L}]≤(L+3)/(1000rd)`. |
| `A3.SS2.p12.4` | `E Y_i=(a/d)(I_r⊗t_it_iᵀ)`. |
| `A3.Ex110` | `Σ_i E Y_i=aI_{r²}` and `Σ_i cos(nθ_i) E Y_i=0`; the second is the truncated weighted expectation, rather than a claim that each summand has zero expectation. |
| `A3.SS2.p13.1` | `Z_i=Y_i-EY_i`; centering occurs after truncation. |
| `A3.Ex111` | `||Y_i||op=(R_i||t_i||²/d)1_{R_i≤L}≤2rL/d`; `||EY_i||op=a||t_i||²/d≤2r/d`. |
| `A3.Ex112` | `||Z_i||op≤R_*=2r(L+1)/d`; the same bound holds for `cos(nθ_i)Z_i`. |
| `A3.Ex119` | The shared variance upper bound needed downstream is `v_*=2r(r+2)/d`; it is an upper bound on `||Σ_i E Z_i²||op`, with the same bound for weighted centered summands. |
| `A3.Ex121` | For every real `t>0`, `P(||Σ_i Z_i||op>t)≤2r² exp(-t²/[2(v_*+R_*t/3)])`. The norm event is **strict** `>t`; the comparison is `≤`. |
| `A3.SS2.p15.2` | The same entire tail bound holds with `Σ_i cos(nθ_i)Z_i` in the event. The prefactor stays `2r²`. |

The variance bridge visible in paragraphs 14.1-14.6 uses Gaussian fourth
moments, PSD order after dropping the truncation indicator, the identity
`E Z_i²=E Y_i²-(E Y_i)²⪯E Y_i²`, and deterministic `cos²≤1`.
It is not an additional Gaussian hypothesis. Independence, centering and
self-adjointness of both sequences are asserted at their Bernstein use site.

Source-domain consequences for later review: `Y_i` can be rank deficient or
zero, so it is PSD rather than generally PD; `Z_i` need not be PSD. Every
real scalar multiple of `Z_i` and of its weighted version is self-adjoint.
Their displayed deterministic operator-norm bound supplies exponential
integrability for every finite real parameter, rather than requiring an
unrelated extra Gaussian input. Any proof of this implication remains a
dependency and must not silently become a new premise of a theorem presented
as the complete concrete Gaussian result.

## Seven slots frozen for the later comparison

1. **Objects:** finite square self-adjoint matrices and their genuine matrix
   exponential; matrix expectation and PD-cone logarithm; in the concrete
   experiment, Gaussian rank-one tensor summands followed by truncation and
   centering, plus their deterministic cosine-weighted versions.
2. **Domains:** complex Hermitian carrier for Tropp, real symmetric
   specialization for Gaussian; normalized original probability law;
   exponential-integrability domain for MGF/CGF; positive-definite log inputs.
3. **Quantifiers:** deterministic exp positivity for every self-adjoint matrix;
   real exponential parameter, not just positive parameters; Gaussian
   parameter regime above; all indices under one experiment; downstream
   Bernstein `∀t>0`. No finite-sample event is replaced by a pointwise assertion
   over possible sample values when taking probabilities.
4. **Assumptions:** self-adjointness and finiteness are carrier assumptions;
   analytic validity of expectations is source standing context. Concrete
   Gaussian regularity, independence, centering, boundedness, and matrix
   positivity must be obtained from the displayed construction when claiming
   that construction, rather than supplied as theorem-shaped assumptions.
5. **Conclusions:** exp is positive definite; any expected exponential fed to
   log is genuinely finite and positive definite; exact truncated expectations,
   centered norm bounds, and strict-event two-sided tails are as above. A PSD
   conclusion is weaker than the exponential/log-domain conclusion.
6. **Scopes and senses:** operator norm and Loewner order; genuine matrix
   functional calculus rather than entrywise exp/log; almost-sure random
   relations; unconditional expectations after truncation; scalar equalities
   and matrix equalities must not be exchanged without their actual adapter.
7. **Constant dependencies:** exp positivity has no concentration constants;
   concrete `L,R_*,v_*` depend exactly on `d,r` as displayed. Bernstein ambient
   matrix dimension is `r²`, yielding `2r²`, not `d`, `r`, or `dr`. The shared
   absolute constant in the later `τ_{d,q}` is independent of Gaussian draws,
   `d,q,κ`; that later constant simplification is outside this bounded domain
   delta's proof credit.

## Later review checks, without an implementation verdict

The fresh packet must enable inspection of all meaning-carrying definitions,
the full changed module including imports/scoped assumptions/private helpers,
and the actual lesson/source correspondence. Specific failure probes are:
entrywise versus matrix exponential; unsound log totalization; expectation
without exponential integrability; zero-mass or unnormalized-law drift;
PSD-versus-PD substitution; pointwise versus almost-sure drift; conditioning
versus indicator truncation; missing `d^{-1}` or `d^{-1/2}`; wrong tensor
dimension; changed `≤L`/`>L` or `>t` endpoints; matrix exponential order
monotonicity falsely inferred from trace monotonicity; concrete conclusions
reintroduced as public hypotheses; and claims of complete Gaussian tail or
Tropp assimilation from a narrower domain lemma.

No judgment on any current theorem, module, lesson, graph, or publication has
been made. Required next input is the newly generated anti-anchored reviewer
packet after actual compilation and independent anonymous decoding, plus the
current full-module and reader context described by the parent task.
