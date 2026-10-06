# Compact Sobolev to smooth weighted graph: bounded dependency audit

Read-only mathematical/API plan, 2026-10-06, picard_commit_verifier_20261005. No compiler, new SAU, theorem admission or core certificate. Inspected HEAD: 30ad6ddb991c190d912d5bd8a48b39bd486d4d7b; Lean4.33.0; Mathlib db584cd6d46c92f209a44c0f1c829460d327499d. Root integration may continue independently. Ignored prototypes/candidates, anonymous reconstructions and current source-review verdicts were not read. Only this note was written.

## Decision

The direct spectral route is mathematically viable and avoids a full family of real mixed second derivatives. The requested function/gradient/Laplacian graph convergence does not need that tensor family. Pinned Mathlib already supplies Schwartz density, L2 Fourier isometries, inverse Bessel identities and uniqueness of Lp distribution representatives. The missing adapter is a **chosen norm-controlled L2 Fourier multiplier with compatibility on Schwartz and tempered distributions**. The existing bounded-multiplier Sobolev theorem provides membership/existence, not convergence of a chosen sequence.

The shortest inspected library route is spectral approximation of the actual Bessel-L2 witness, followed by real projection and one fixed outer plateau. This is an API assessment, not a measured compilation comparison. A direct weak-equation/mollifier route is also viable without mixed derivatives, but requires less-packaged L2 approximate-identity and weak-derivative commutation adapters.

## Retained actual input and source boundary

Keep the same original D, constructed before epsilon/f, and the same actual u before **all** compact C2 cutoffs chi. The accepted localization produces

\[
v=\chi u,\quad g=G_\chi=\chi G+u\nabla\chi,\quad
F=F_\chi=\chi(\epsilon u+\langle\nabla W,G\rangle-f)
 +2\langle\nabla\chi,G\rangle+u\Delta\chi,
\]

where G=D.closure(u). All three are global ordinary-volume L2 and supported in K=tsupport(chi). The same producer proves the actual first weak identity against every compact C1 test and Delta(v)=F against every compact C2 test, including every L1 product. CompactWeakPoissonSobolev then derives actual complex L2 classes vc/Fc, their volume-AE ofReal identities, all-complex-Schwartz PDE, actual TD Laplacian and MemSobolev2. These are actual inputs, not supplied final H2/core/approximation certificates. The target gradient is **Gchi**, not unlocalized G.

[PBPS v1 Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1), HTML1200-1237, uses compact smooth tests and gradient density/closedness in macroscopic coercivity. It does not itself supply the proposed weighted-generator graph core. [SPHMC v1 §4.1](https://arxiv.org/html/2609.06906v1#S4.SS1), HTML410-430, uses posterior covariance and Brascamp-Lieb for the lower smoothed Hessian bound. The proposed graph adapter is an analytic prerequisite, not Lemma4.1 or either main result.

For the actual reflected law,
\[
 W_y(z)=V((y+z)/2)+\|z-y\|^2/(8\eta),
\]
with Hessian bounds (alpha+eta^-1)/4 and (beta+eta^-1)/4. The RGO potential V(x)+norm(x-y)^2/(2eta) has different variables/scales. Do not identify their laws, generators or constants.

## Exact inspected pinned APIs

All Mathlib locations below are relative to .lake/packages/mathlib/Mathlib/.

| API | Location | Available contract / missing adapter |
| --- | --- | --- |
| SchwartzMap.denseRange_toLpCLM | Analysis/Distribution/SchwartzSpace/Basic.lean:1383 | Lp density for finite p; finite-dimensional Borel, temperate measure, finite on compacts. Not graph density. Choose a sequence in the metrizable L2 target. |
| Lp.fourierTransformₗᵢ; norm_fourier_eq | Analysis/Fourier/LpSpace.lean:50,89 | Complex L2 forward/inverse isometries and norm continuity; specify volume explicitly. |
| SchwartzMap.toLp_fourier_eq; toLp_fourierInv_eq | same:99,108 | Schwartz/L2 Fourier compatibility. |
| Lp.fourier_toTemperedDistribution_eq; inverse version | same:120,132 | L2/TD Fourier compatibility. |
| BoundedContinuousFunction.memLp_top | MeasureTheory/Function/LpSpace/ContinuousFunctions.lean:46 | Turn bounded continuous symbols into actual Linfinity classes. |
| Lp.norm_smul_le; coeFn_lpSMul; add_smul; smul_comm | MeasureTheory/Function/Holder.lean:180-269 | Holder infinity,2,2 multiplication, norm bound, actual AE products and linearity. Package a fixed-symbol L2 CLM; no such named Fourier-L2 CLM was found in these inspected files. |
| SchwartzMap.fourierMultiplierCLM | Analysis/Distribution/FourierMultiplier.lean:48 | Inverse Bessel symbol maps Schwartz to Schwartz; explicitly prove HasTemperateGrowth for identities. |
| fourierMultiplierCLM_toTemperedDistributionCLM_eq | same:190 | Schwartz/TD multiplier compatibility. |
| Lp.toTemperedDistribution_smul_eq | Analysis/Distribution/TemperedDistribution.lean:308 | Lp/TD multiplication compatibility with actual Holder/growth hypotheses. |
| Lp.ker_toTemperedDistributionCLM_eq_bot | same:216 | Injectivity: equal TDs identify actual Lp representatives. |
| besselPotential_besselPotential_apply; besselPotential_neg_apply_eq_iff | Analysis/Distribution/Sobolev.lean:81,99 | Genuine inverse, with B2=I-(2pi)^-2 Delta. |
| MemSobolev.fourierMultiplierCLM_of_bounded | same:281 | Membership/existence only, not the quantitative chosen-map continuity required here. |
| SchwartzMap.lineDeriv_eq_fourierMultiplierCLM; laplacian_eq_fourierMultiplierCLM | Analysis/Distribution/FourierMultiplier.lean:100,107 | Exact 2pi i derivative and -(2pi)^2 Laplacian factors. |
| ae_eq_of_integral_contDiff_smul_eq | Analysis/Distribution/AEEqOfIntegralContDiff.lean:195 | Compact smooth test uniqueness for locally integrable actual representatives. |
| ContinuousLinearMap.compLpL | MeasureTheory/Function/LpSpace/Basic.lean | L2 real projection, viewed as real-linear; alternatively derive the Re norm bound and construct the actual class. |

## Route in seven steps

1. **Use the actual witness.** From MemSobolev choose w:Lp(C,2,volume) with B2(T_vc)=T_w. It can be identified as vc-a Fc, a=(2pi)^-2, using the actual TD PDE and the proved B2 identity. Keep all AE embeddings. Approximating vc in plain L2 would not control its derivatives.
2. **Build bounded multipliers.** Let
   \[
   m_0(\xi)=(1+\|\xi\|^2)^{-1},\quad
   m_b(\xi)=\frac{2\pi i\langle\xi,b\rangle}{1+\|\xi\|^2},\quad
   m_\Delta(\xi)=\frac{-(2\pi)^2\|\xi\|^2}{1+\|\xi\|^2}.
   \]
   They have temperate growth and bounds 1, 2pi norm(b), (2pi)^2 respectively; nonsharp bounds suffice. Define M_m=FourierInv o multiplication(m) o Fourier on L2. Prove norm bounds, Schwartz and TD compatibility using Holder infinity,2,2 and Plancherel. Explicit complex casts, representative equality and continuity are required.
3. **Approximate w and invert Bessel.** Choose actual q_n:Schwartz(E,C) with q_n.toLp -> w. Define s_n=Schwartz.fourierMultiplierCLM(C,m0)(q_n). Then s_n.toLp -> vc, directional derivative(s_n,b).toLp -> M_mb(w), and Delta(s_n).toLp -> Fc. The last limit uses the known actual TD equation, inverse Bessel and Lp-TD injectivity. No extra Fourier normalization factor is inserted in Delta(v)=F.
4. **Identify the actual first gradient; project real.** For each vector of a finite orthonormal basis, pass the ordinary smooth IBP identity for s_n to the L2 limit against real compact smooth tests using continuous Holder pairings. Establish complex L1 before taking integral Re. Compare with the parent's actual compact-C1 weak gradient and use compact-test uniqueness to obtain Re(M_mb(w))=inner(g,b) AE. Assemble finite-basis vector convergence. Real parts of s_n, gradients and Laplacians converge to v,g,F. No assumed complex-class realness, classical Hessian, mixed-derivative commutation or first all-Schwartz gradient identity is needed; an all-Schwartz gradient extension is an alternative.
5. **Fix common outer support.** Construct one unnormalized smooth compact plateau theta=1 on a neighborhood of K. Set phi_n=theta Re(s_n), supported in the common compact K'=tsupport(theta). Ordinary product rules yield
   \[
   \nabla\phi_n=\theta\nabla\Re s_n+\Re s_n\nabla\theta,
   \quad\Delta\phi_n=\theta\Delta\Re s_n+
   2\langle\nabla\theta,\nabla\Re s_n\rangle+\Re s_n\Delta\theta.
   \]
   Every fixed coefficient is bounded. On K the plateau derivatives vanish; off K the actual v,g,F vanish. Hence the cross-term limits are zero and all three ordinary L2 limits hold. Common support is K', not necessarily K.
6. **Transfer this compact graph to the original weighted law.** On K', exp(-W)/Z has a finite upper bound with actual Z>0, and gradient(W) is bounded. Weighted squared errors are at most a fixed constant times ordinary squared errors. Thus phi_n, gradient(phi_n), and A_W(phi_n)=-Delta(phi_n)+inner(gradient(W),gradient(phi_n)) converge in actual weighted L2 to v,g,-F+inner(gradient(W),g). The exact original hgraph puts every smooth pair in D.graph; closedness derives localized v in D.closure with derivative g. That membership is a conclusion, not a premise. Prove volume/weighted AE equivalence and explicit quotient maps. C1 W suffices here; actual source W is C2, never implicitly C-infinity.
7. **Stop at the core boundary.** This establishes approximation of the localized actual solution. Calling it an operator core for A=D*D additionally needs the actual adjoint/form-domain identification with the weighted differential expression and membership of the localized graph. Reaching original unlocalized u requires chi_R plus weighted tail bounds on u Delta(chi_R), grad(chi_R)G and u inner(grad(W),grad(chi_R)). Local L2 or arbitrary C2 W alone does not imply those global estimates. Source upper Hessian bounds offer linear gradient growth, but the cutoff/domain adapter and constants remain separate. Only afterwards can global weighted Bochner/core or BL/Poincare extensions follow.

## Comparison and next bounded consumer

| Route | Missing machinery now | Assessment |
| --- | --- | --- |
| Bessel/spectral | Chosen bounded L2 multiplier CLM+compatibility; first-gradient identification; plateau product convergence; compact weight transfer | Avoids mixed second derivatives and tensor reconstruction. Uses actual existing Sob2/PDE. |
| Direct weak equations+mollifier | L2 approximate identity for v,g,F; derivative/Delta commutation proved from actual weak tests; common support | Also avoids mixed derivatives. Translation continuity exists, but inspected bump convolution limits are pointwise/AE, not the needed L2 convergence result. |
| Real mixed derivatives first | Twice Sobolev differentiation, real representatives and compact mixed-test identification, then smoothing/density | Useful if the next consumer needs Hessian L2/Bochner; surplus for this graph target. |

Pinned Analysis/Convolution.lean explicitly lists Lp convolution bounds as TODO. ContDiffBump.convolution_tendsto_right and its AE variant do not prove L2 convergence. Lp.instContinuousSMulDomMulAct (LpSpace/DomAct/Continuous.lean:53) supplies translation continuity. HasCompactSupport.contDiff_convolution_right/left (Calculus/ContDiff/Convolution.lean:423,430) supplies smoothness. Actual weak first/Delta commutation and norm convergence still need adapters. This is a bounded search of the named files, not proof that no other API exists anywhere.

Recommended one next substantive consumer packet: **compact_weak_poisson_smooth_graph_approximation**, deriving a real compact smooth sequence with common outer support and actual three volume-L2 limits, consumed by the current reflected conditional same-D/same-u producer. Early-check the bounded multiplier adapter inside the packet. A reusable interface earns progress only with this genuine applied consumer, not a wrapper restating membership. If that adapter exposes an actual API blocker, shrink to the applied inverse-Bessel L2 graph approximation interface with exact vc/Fc and derived first-gradient identification; leave common support/weighted/core open. No packet is claimed by this audit.

Dimension zero is retained: frequency norm and derivatives vanish, B2=I, multiplier bounds hold, the finite basis is empty and a plateau is locally1 at the unique point. This concerns canonical zero-dimensional volume, not an arbitrary atomic-law assertion.

## Remaining truth boundary

No new formal credit. Existing VERIFIED Sob2/localization remain unchanged. Real mixed representatives, weighted H2/core/global Bochner/BL/Poincare, the remaining lower smoothed Hessian half, higher smoothing, history/query work, PBPS invariance/nonexplosion/discrete hypocoercivity, both main results and composition remain separate obligations. TV does not transfer unbounded cost. No compile, source verdict, lifecycle transition, shared imports/site/graph/publication mutation was performed.

## Inspected raw/LF footprints

These hashes name inspected inputs only; they add no compile/admission evidence.

| Input | raw SHA256 | LF SHA256 |
| --- | --- | --- |
| AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CompactWeakPoissonSobolev.lean | 9572c7f988d24f93b70e70323c2b51afe5c0ae515294022f3d46fcf1745dafc7 | 019f3577b1eb5ff4d7db00a484bbbf206362a1466d84c6bafbdb5e4e315c5676 |
| AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/LocalizedWeakResolvent.lean | 2e35799ed7d7beef354caa22e32d1a6e75d3bed9c50217eda599c8e6fd8b3114 | 5fb157f3bfd725cddd571178f52cd244b4949386a2db6dd6e41efbde835e7c8d |
| AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalLocalizedSobolev.lean | 28df027149ea11fc514f834e25130e08d6288a2ba940df6846906a962ae46e5e | 265545a7b3f04c58fb07ff34f6e5f9c14e3328b3e259146d1a061ca000ba9342 |
| AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedGradient.lean | c2495b6ab8a4c82cadf0d86b910d663e0e4f65f6b96bc4b449149112756d4690 | 5bd3402124330f69d7875e9bbfc6eb31760b70528850ac841d1ff7c84ab72149 |
| AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CompactC1GradientDomain.lean | 3a08a4dc62796d8a5d021755c841280010d92d2b3259efee311232bf8ab8d096 | dd6234dfec6d2dfb351d1ad45c3fcc0eb111e1c18038ebc4c6ab48035033a2f7 |
| .lake/packages/mathlib/Mathlib/Analysis/Distribution/Sobolev.lean | 184b88dc0a706e5284ad55f34fc3c8be72942a3ee120dd4340035dd201eab8d1 | 626efa98f46bc13e7ef8770bc29e778357c713d15373846f1e49252a7ac1df3e |
| .lake/packages/mathlib/Mathlib/Analysis/Distribution/SchwartzSpace/Basic.lean | 51b1eb816d0c3096efc21a7f6cdd6851b0761409ae5b0751e73df6e26ebdaf4a | 419ecc0c5e5041be90969b55722b67e368c253d62c75e65209a749a031602cd0 |
| .lake/packages/mathlib/Mathlib/Analysis/Distribution/FourierMultiplier.lean | 4a348ce7af8c57fb98a72cccc7397cd333962c55ca20dd1512e4979fcbe45e0a | 22f9fad5a18b2e677fbb861a21f12c78275bffe0fa67c97495b8aa996011f067 |
| .lake/packages/mathlib/Mathlib/Analysis/Fourier/LpSpace.lean | 64fde2a7b42941a479b3fbc4804bae6d2c46cff668d6fbb4d513358d0ad42aee | 901386dd897fc7e1c2d4b3b0cca3adb96829bf9d011e57be5e8f7e85a81598f3 |
| .lake/packages/mathlib/Mathlib/Analysis/Distribution/TemperedDistribution.lean | ec9b7e902081e0de7621532824f434c29bc4a9b18aae02fdd8a7a2d0b783ef87 | 989c6b5a41beaf88018701f17fa14f8b8f37da4ce07218cb9e9bdfd2a147035f |
| .lake/packages/mathlib/Mathlib/Analysis/Distribution/AEEqOfIntegralContDiff.lean | 1c711daa534fa1ed916fd00364e67f921545ec25564911985b2e377385adcde9 | 626e88cc762fe508d78e07923fdb29ab8b5c47e932b30e43e3cc352c0fee9eb2 |
| .lake/packages/mathlib/Mathlib/MeasureTheory/Function/Holder.lean | 62d47146a6431c710ee51bfd11ee390a7a4656019f5a01011abe0607de691d92 | 60ed95457da79c6fe6a595834222474a89d94ad806405e237a0e9c7182c2a030 |
| .lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Basic.lean | f1047ee229a4dc2669e1e8515ef1b65c8c04e142a642059addffae2abc18700f | c333a6caa56906c6203cad3e3214be2114a65728fcfdf95ae639992abefb373f |
| .lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/ContinuousFunctions.lean | abc8af668bd43292b89e74ddef104d3448f1960429a86665b0347dacbe4b88c1 | 9288796d597f70973f01424714259c5dca95b9f8f45db02808cfbe2f97856342 |
| .lake/packages/mathlib/Mathlib/Analysis/Convolution.lean | bcc17adbf4358f6b213501dc51766b28ae35824a87721b80545dfdd023e432b6 | 2e02a96b2ee6de4b52b6414aa938fd46f89690939d5c86964071b73a88dbd184 |
| .lake/packages/mathlib/Mathlib/Analysis/Calculus/BumpFunction/Convolution.lean | 42770c7caab00fa5dcb8412eaed82ab70ca515d14306c2b90be7f79707487c59 | 7e89c7cb27e6d8fbeba7ef17cff8f9f62e4467337e5bf9e9d132b92825cf088a |
| .lake/packages/mathlib/Mathlib/Analysis/Calculus/ContDiff/Convolution.lean | e88453ce9a1e1735a0335b4c092ec662e72e798835b945e3dbb7ca7b3bc265a7 | 51c4b08497f08a898573cabb6ad5a95f4a1e170ab74fec15d2bf4fdd8eba370b |
| .lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/DomAct/Continuous.lean | 45cc55df39af5d1c853fee69d95fc78d10a852249e88559a7e786fb905bbb47b | fca23da1a37bc1cded49f03f98931722e491ceb7be95462516aaae081a8770ba |
