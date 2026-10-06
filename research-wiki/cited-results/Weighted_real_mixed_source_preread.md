# Real mixed weak derivatives: independent source/API preread

Owner: phase_source_reviewer_20261005. Date: 2026-10-06.
Status: source/dependency preread only. No candidate theorem acceptance, compilation,
SAU lifecycle change or mathematical completion credit.

## Primary contract reconstructed first

[PBPS arXiv:2609.06905v1 Section 2.2](https://arxiv.org/html/2609.06905v1#S2.SS2),
HTML168–211, equations2.6–2.14, constructs a normalized Gibbs/Gaussian joint
law. Its ordinary RGO potential is
\(W^{R}_y(x)=V(x)+\|x-y\|^2/(2\eta)\).
[Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1),
HTML1197–1234, uses smooth compact tests, density and closedness of the gradient.
Its reflected conditional potential is
\(W^{S}_y(z)=V((y+z)/2)+\|z-y\|^2/(8\eta)\).
The reflection \(z=2x-y\) has inverse Jacobian \(2^{-d}\),
\(\nabla^2W^{S}_y=(\nabla^2V((y+z)/2)+\eta^{-1}I)/4\).
For corresponding functions, the unreflected Dirichlet energy is four times the
reflected energy. These laws and operators require an actual pushforward adapter.

[SPHMC arXiv:2609.06906v1 Section4.1](https://arxiv.org/html/2609.06906v1#S4.SS1),
HTML403–430, equation4.1/Lemma4.1, uses the unreflected RGO covariance. Its BL
upper-covariance and CR lower-covariance arguments remain separate. This next
mixed-derivative edge is an authored analytic prerequisite, not a quoted numbered
result or a completed BL/Poincare assertion.

## Seven-slot proposed contract

- **Objects:** the actual same resolvent solution \(u\), gradient representative
  \(G=D_y^{\rm cl}u\), localized \(v=\chi u\) and
  \(G_\chi=\chi G+u\nabla\chi\). The actual complex volume-L2 class \(v_c\)
  is volume-a.e. equal to \(v\); its distribution \(T_v\) has genuine
  `MemSobolev 2 2`. The proposed new object is a real volume-L2 weak derivative,
  produced from these inputs rather than supplied as a conclusion certificate.
- **Domains:** finite-dimensional real Hilbert/Borel space with canonical volume,
  including dimension zero. Weighted \(L^2(S_y)\) and ordinary-volume \(L^2\)
  remain distinct. The original graph consists of genuine smooth compact
  functions and their gradients. Cutoffs are real C2 compact functions; the new
  tests are real smooth compact functions.
- **Quantifiers:** common \(R,S\), then every fiber \(y\) and one original
  \(D_y\), then every \(\epsilon>0\) and forcing \(f\), then ONE \(u\),
  then ALL C2 compact \(\chi\), then ALL directions \(a,b\), then a real
  \(h_{ab}\), then ALL smooth compact \(\varphi\). No joint measurable
  selection in fibers, cutoffs or directions follows from these existential facts.
- **Assumptions:** the genuine conditional consumer retains C2 \(V\),
  positive \(\alpha\le\beta\), all-point/all-vector curvature bounds,
  \(\eta>0\), \(\beta\eta\le1\), actual normalized conditional law,
  integrable positive partitions and the original closable compact-smooth gradient.
  The shared analytic edge should consume actual localized global volume-L2,
  AE casting, Sobolev2 and the original all-C1 weak-gradient identity. It should
  not assume mixed derivatives, classical regularity or new weighted-domain facts.
- **Conclusion:** for fixed \(a,b\), construct a real pointwise representative
  \(h_{ab}\) with `MemLp h_ab 2 volume`, both displayed products integrable,
  and
  \[
  \int\varphi h_{ab}\,dx=-\int\langle G_\chi,a\rangle D_b\varphi\,dx
  \quad(\varphi\in C_c^\infty).
  \]
  If the output is instead an actual real Lp class, its AE relation to this
  representative must be explicit. Neither output alone is a classical Hessian.
- **Scope:** directionwise real weak derivatives of the actual localized gradient.
  No asserted support, bilinear Hessian field, simultaneous matrix-valued choice,
  real mixed-derivative symmetry, localized weighted-D membership/core, global
  Bochner inequality, epsilon-zero limit, BL, main theorem or composition result.
- **Constants:** differentiation uses the pinned Fourier convention; the accepted
  Sobolev producer used \(B_2=I-(2\pi)^{-2}\Delta\). No new numeric estimate is
  required for the directionwise existence statement. Reflection factors are
  preserved by the existing actual conditional parent, not transferred by analogy.

## At most seven source-to-API steps

1. Retain the actual parent output before choosing directions. It gives
   `MemLp Gchi 2 volume`, all C1 compact directional weak-gradient tests and the
   same \(v_c\) AE ofReal(v) with `MemSobolev 2 2`. No all-Schwartz first-gradient
   identity is assumed. Generic inputs must say exactly which of these facts are
   consumed; the genuine conditional application must derive all of them.
2. Fix the order \(h_{ab}=\partial_b\langle G_\chi,a\rangle\). Apply pinned
   `TemperedDistribution.MemSobolev.lineDerivOp` first in direction \(a\), then
   \(b\): order2 becomes order1 then order0. `memSobolev_zero_iff` yields an
   actual complex L2 class \(q_{ab}\) representing
   \(\partial_b(\partial_a T_v)\). This is a derived witness, not an assumed
   mixed-derivative certificate.
3. For real \(\varphi\in C_c^\infty\), construct its actual complex Schwartz
   embedding using `Complex.ofRealCLM` and `HasCompactSupport.toSchwartzMap`.
   Derivatives are real Frechet derivatives. The double TD action is
   \(T_v(D_aD_b\varphi)\): the two minus signs cancel. Use the real CLM chain
   rule to identify the embedded derivatives, without silently interchanging
   \(a,b\) or requiring symmetry.
4. All integral manipulations require L1 evidence first. Schwartz functions and
   their directional derivatives are volume-L2; actual q_ab/v/Gchi are L2.
   Holder2,2,1 gives the legal products. The AE relation of v_c transfers its
   integral to the actual original v. The scalar projection
   \(\langle G_\chi,a\rangle\) is L2 by a real continuous linear map.
5. Use the original weak-gradient identity with the actual test
   \(D_b\varphi\) and direction \(a\). This test is smooth and compact;
   `HasCompactSupport.fderiv_apply` supplies compactness and the smooth
   derivative/CLM evaluation supplies C1. Thus
   \(\int vD_aD_b\varphi=-\int\langle G_\chi,a\rangle D_b\varphi\).
6. Take \(h_{ab}=\operatorname{Re}(q_{ab})\) using its standard representative.
   `MemLp.continuousLinearMap_comp` with `Complex.reCLM` (or `MemLp.re`)
   supplies real L2. `integral_re` applies only after proving complex L1. The
   right side is already real, so its real part gives the required real weak
   identity. This route needs no theorem that the entire chosen complex
   representative has imaginary part zero and no representative smoothness.
7. Reattach this result after each cutoff to the same original D/u output;
   retain all previous conjuncts. In dimension zero the only directions are
   zero and the directional derivatives vanish; a zero real witness is valid.
   No positive-dimensional/nonzero-direction premise is permitted. Stop at the
   directionwise weak derivative; subsequent weighted core/global estimates
   require separate genuine producers.

## Exact public interfaces and pinned evidence

Mathlib checkout: `db584cd6d46c92f209a44c0f1c829460d327499d`.
Fresh reads after primary reconstruction:

- `Mathlib/Analysis/Distribution/Sobolev.lean:149–155,316–319`:
  genuine Bessel-Sobolev definition, zero-order Lp witness and one-order loss.
- `Mathlib/Analysis/Distribution/TemperedDistribution.lean:160–175,215–227,361–368`:
  actual bilinear integral embedding, smooth compact Schwartz construction and
  negative test derivative. Pairings use ordinary multiplication, no conjugation.
- `Mathlib/Analysis/Distribution/SchwartzSpace/Deriv.lean:102–129,171`:
  real directional derivative/fderiv and derivative-support inclusion.
- `Mathlib/Analysis/Distribution/SchwartzSpace/Basic.lean:555–563,1316`:
  actual compact-smooth embedding and Schwartz MemLp.
- `Mathlib/Analysis/Calculus/FDeriv/Const.lean:382–394`:
  fderiv support inclusion and compact directional derivative.
- `Mathlib/MeasureTheory/Function/LpSpace/Basic.lean:677–681,762–769`;
  `Mathlib/Analysis/Complex/Basic.lean:150,321`;
  `Mathlib/MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean:164–166`:
  genuine real-linear projections, preserved L2 and legal real-part integration.

Current canonical parent code, not prior verdicts, supplies the facts above:

| Current module | Raw SHA256 | LF SHA256 |
|---|---|---|
| CompactWeakPoissonSobolev.lean | 9572c7f988d24f93b70e70323c2b51afe5c0ae515294022f3d46fcf1745dafc7 | 019f3577b1eb5ff4d7db00a484bbbf206362a1466d84c6bafbdb5e4e315c5676 |
| ConditionalLocalizedSobolev.lean | 28df027149ea11fc514f834e25130e08d6288a2ba940df6846906a962ae46e5e | 265545a7b3f04c58fb07ff34f6e5f9c14e3328b3e259146d1a061ca000ba9342 |
| LocalizedWeakResolvent.lean | 2e35799ed7d7beef354caa22e32d1a6e75d3bed9c50217eda599c8e6fd8b3114 | 5fb157f3bfd725cddd571178f52cd244b4949386a2db6dd6e41efbde835e7c8d |

The conditional parent's public statement and actual application were reread;
other matching frozen parent proofs were independently read in the earlier
review. These are dependency facts, not acceptance of the next candidate.

## Omitted detail, exposure and failure boundary

The papers do not spell out this Fourier-to-real directionwise producer.
Source C2 potentials and finite Euclidean spaces remain explicit; finite-Hilbert
and dimension-zero extension is a disclosed analytic generalization. Actual
normalization, density positivity, weighted/volume AE transfer and locally
legal resolvent tests are inherited from true parent constructions, not replaced
by supplied certificates. Compact test derivatives remain compact; there is no
noncompact inverse-weight test hidden here.

Primary URLs were freshly read before this bounded API reconstruction. Earlier
exposure includes my full parent/source reviews and independent Schwartz/API
preread; an earlier bounded BL search also exposed covariance keywords,
signatures and matching lines. That exposure is not correctness evidence for
this next edge. I did not read `.astis/RealMixedDirectPrototype.lean`, other root
future prototypes/logs, candidate statements, anonymous reconstruction or math
verdicts for this future target. No compiler was run and no prior review edited.

Failure policy: stop if the candidate changes derivative order without proof,
differentiates an Lp representative classically, treats complex L2 as real
without actual projection/L1, selects u after directions/cutoffs, assumes h_ab,
identifies reflected and RGO scales, or promotes directionwise witnesses to a
Hessian/support/weighted core/global estimate. Any such mismatch needs an exact
separate repair or smaller interface; this note provides no acceptance verdict.
