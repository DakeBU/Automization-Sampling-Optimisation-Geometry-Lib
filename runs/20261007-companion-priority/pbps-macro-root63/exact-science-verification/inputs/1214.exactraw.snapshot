# Global cutoff removal for scalar resolvent coercivity: source prerequisite preread

2026-10-06. Independent source/API reader: `phase_source_reviewer_20261005`. Repository HEAD: `bd9fa2496e1647040c3455a237ea4855db123e40`; Mathlib: `db584cd6d46c92f209a44c0f1c829460d327499d`, Lean 4.33. This is a bounded route audit, not a new theorem, source-equivalence verdict, compiler check, or verification credit. **The compact weighted coercivity producer is still proposed/exploring; this note does not treat it as proved.** Only established parent interfaces and exact mathematical implications of a future genuine compact inequality are used.

## Primary first, scope and exposure

Freshly read [PBPS arXiv:2609.06905v1 §2.2](https://arxiv.org/html/2609.06905v1#S2.SS2), HTML 168–212, and [Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1), HTML 1197–1234, before the root's `Weighted_cutoff_generator_core_route.md`. The source uses actual Gaussian augmentation, a reflected conditional density, conditional Poincare, and extension from compact smooth tests by density/closedness. It does not explicitly prove the cutoff-resolvent route below. Separately, [SPHMC arXiv:2609.06906v1 §4.1](https://arxiv.org/html/2609.06906v1#S4.SS1), HTML 403–430, uses RGO covariance upper bounds through BL, while CR supplies the other covariance bound. This analytic prerequisite does not complete either source estimate.

Exposure: my earlier source/API prereads and full independent reviews of localized resolvent/compact smooth graph parents are retained; their graph-module bytes were rechecked against current HEAD. Earlier bounded BL retrieval exposed covariance candidate signatures/keywords/matching lines, not proof validation. The present raw core-route note was read after primary reconstruction as a proposal. No ignored prototype, current weighted candidate module, future candidate, anonymous reconstruction, math-review verdict or verifier receipt was read. No compiler was used. Administrative reports of parent admission are not source-fidelity evidence.

## Seven semantic slots

1. **Objects.** Original weak resolvent \(u\in\operatorname{domain}(D.\mathrm{closure})\), its actual vector class \(G=D.\mathrm{closure}(u)\), and input \(f\in L^2(\mu)\). Let \(a=f-\varepsilon u\in L^2(\mu)\). This is the positive weak-generator expression; \(L=\Delta-\nabla W\cdot\nabla\) has the opposite sign. For an actual smooth radial cutoff \(\chi_R\), retain \(v_R=\chi_Ru\), \(G_R=\chi_RG+u\nabla\chi_R\), and the actual localized ordinary PDE right side \(F_R\). Define \(a_R=-F_R+\nabla W\cdot G_R\), through actual representatives and AE links, not an arbitrary supplied generator class.
2. **Domains/measures.** Finite real Hilbert/Borel \(E\), including dimension zero; \(\mu=\mathrm{volume}.\mathrm{tilted}(-W)\) with derived positive finite \(Z=\int e^{-W}\) and density \(e^{-W}/Z\). All global norm limits below are **weighted** L2. Ordinary-volume local L2/weak equations are used for localization and compact approximation, not asserted globally. Original \(D\) is the actual compact-smooth gradient map. This route retains its closure; it does not equate a rough differential expression with a full adjoint/operator domain or generator core.
3. **Quantifiers.** Same common actual \(J,R,S\), then for each fiber \(y\) the same \(D_y\), before \(\varepsilon>0\) and \(f\). One original \(u\) precedes all C2 compact cutoffs. Choose a concrete exhaustion \(R_n=n+1\); one actual cutoff family and scale-uniform derivative constants precede every \(n\). For each cutoff, the compact producer may have its own inner smooth-approximation sequence, but all three inner graph limits must use the same sequence. Scalar inequalities for each radius suffice: no diagonal global smooth core sequence is claimed. No jointly measurable fiber selector is required or produced.
4. **Hypotheses.** Source C2 \(W\), genuine lower/upper Hessian bounds \(0<mI\preceq\nabla^2W\preceq MI\), and the original variational/localized identities. Both bounds matter: an upper quadratic-form bound **alone**, without convexity or a true absolute Hessian norm bound, does not imply linear drift. No C-infinity potential, globally bounded drift, \(\|x\|u\in L^2(\mu)\), global ordinary \(\Delta u\in L^2\), or supplied final core/convergence/coercivity certificate is allowed. Fixed-fiber \(b=\|\nabla W(0)\|\) can depend on \(y\); its contribution vanishes as radius grows.
5. **Conclusion sought.** Conditional on a genuinely produced compact scalar inequality, prove
   \[
   m\|G\|_{L^2(\mu)}^2\le\|f-\varepsilon u\|_{L^2(\mu)}^2
   \le\|f\|_{L^2(\mu)}^2.
   \]
   This is a resolvent gradient bound for the same \(u,D\), not Poincare for arbitrary centered functions. Actual \(v_R\to u\), \(G_R\to G\), \(a_R\to a\) in weighted L2 are proved from original data and tails, not assumed.
6. **Scope.** Narrow global scalar coercivity legitimately avoids rough-Hessian convergence/Fatou and full adjoint/core identification. The older raw route's steps 5–6 belong to a stronger goal; real mixed second-derivative/Hessian convergence is not needed for this scalar passage, once the real compact graph and scalar producer are available. Epsilon-zero, constant kernel, range closure, Poincare, BL, full global weighted core, both main results and composition stay open.
7. **Constants/source scaling.** The reflected source uses \(W_y^S(z)=V((y+z)/2)+\|z-y\|^2/(8\eta)\), so \(m=(\alpha+\eta^{-1})/4\), \(M=(\beta+\eta^{-1})/4\). The RGO uses \(V(x)+\|x-y\|^2/(2\eta)\), with constants four times larger; reflection \(z=2x-y\) has Jacobian \(2^{-d}\), half gradients and quarter Dirichlet energy. Preserve source \(0<\alpha\le\beta\), \(\eta>0\), \(\beta\eta\le1\) in the actual conditional consumer. Final \(m\) is dimension independent; intermediate cutoff Laplacian constants may depend on fixed dimension and disappear in the limit.

## Bounded route, at most seven steps

1. Derive \(\|\nabla W(x)\|\le b+M\|x\|\). `HessianSecantOperator.hessian_secant_operator` genuinely constructs the symmetric segment integral and gradient identity, with norm at most \(\max(|m|,|M|)=M\) under source bounds. At endpoints \(x,0\), the triangle/operator bound gives the claim. `ConvexSmoothGradient.gradient_lipschitz` is an alternative only after producing its actual convexity/quadratic-model premises; it is not a supplied Lipschitz certificate.
2. Reuse `Calculus.Cutoff.radialSmoothCutoff`: \(0\le\chi_R\le1\), plateau on \(\overline B_R\), support in \(\overline B_{2R}\), C-infinity, compact support and pointwise limit one. Its `radialSmoothCutoff_fderiv_bound` has one \(C_1>0\) before all \(R>0,x\). Riesz conversion gives \(\|\nabla\chi_R\|\le C_1/R\). `radialSmoothCutoff_iteratedFDeriv_two_bound` gives \(C_2/R^2\), but explicitly requires `[Nontrivial E]`. The orthonormal trace formula gives \(|\Delta\chi_R|\le dC_2/R^2=:C_\Delta/R^2\). Derivatives vanish where the cutoff is locally constant; handle radius-boundary points by genuine continuity/smoothness, not a false open-neighborhood assertion on the boundary.
3. Combine the already actual localized PDE and gradient formulas. With \(r=\varepsilon u+\nabla W\cdot G-f\), algebra on genuine local AE representatives gives
   \[
   a_R=\chi_R a-2\langle\nabla\chi_R,G\rangle
       +u(\langle\nabla W,\nabla\chi_R\rangle-\Delta\chi_R).
   \]
   Establish local L1/L2 first. In particular \(\nabla W\cdot G\) and \(r\) need **not** be globally weighted L2; their localized cancellation is essential. The resulting expression is globally L2 from the bounds below. Keep the coefficient 2 and sign of \(a\) exact.
4. For \(R\ge1\), derivative terms live on the annulus \(\mathcal A_R=\{R\le\|x\|\le2R\}\). Bound the commutator by
   \[
   \|a_R-\chi_Ra\|_2\le
   \frac{2C_1}{R}\|G\|_2+
   \left[C_1\left(\frac bR+2M\right)+\frac{C_\Delta}{R^2}\right]
   \|1_{\mathcal A_R}u\|_2.
   \]
   The bracket is uniformly finite for \(R\ge1\); the tail tends to zero. This proves the drift contribution without a spatial moment. Gradient error obeys
   \(\|G_R-G\|_2\le\|(\chi_R-1)G\|_2+(C_1/R)\|u\|_2\).
5. Produce all norm limits from actual L2 data. `memLp_two_iff_integrable_sq_norm` supplies integrable squares; `tendsto_integral_of_dominated_convergence` applied to \(1_{\mathcal A_{R_n}}\|u\|^2\) proves the tail limit. The same theorem, with integrable square bounds, proves \((\chi_{R_n}-1)u,G,a\to0\). Prove measurability/AE statements for the chosen representatives, then use `Lp.tendsto_Lp_iff_tendsto_eLpNorm''` or the norm-square integral formula to obtain actual quotient convergence. No Gaussian-tail estimate or extra input moments are needed.
6. Only **after** admission of the proposed compact weighted producer, apply its actual same-D cutoff domain consequence and \(m\|G_R\|_2^2\le\|a_R\|_2^2\). Pass these squared norms to the limit. The original \(u\) was already in the original closure domain, so no new global domain identification is needed. Zero dimension needs an explicit branch because the second-derivative cutoff API assumes nontriviality: all vector derivatives/Laplacians vanish, the cutoff is one on the singleton, and the original variational equation gives \(\varepsilon u=f\).
7. Test the **original** variational equation at \(u\):
   \(\langle f,u\rangle=\varepsilon\|u\|_2^2+\|G\|_2^2\).
   Thus \(\|f-\varepsilon u\|_2^2=\|f\|_2^2-\varepsilon^2\|u\|_2^2-2\varepsilon\|G\|_2^2\le\|f\|_2^2\). This is valid at each positive epsilon; no epsilon-zero limit is inferred.

## Residuals, API findings and failure policy

The actual missing next node is the derived weighted cutoff commutator/representative passage and tail convergence, followed by norm continuity, **contingent on the still-unproved compact weighted producer**. Existing radial cutoff APIs already supply the needed scaling, except for an explicit zero-dimensional branch and the Laplacian trace adapter. `Cutoff.lean` header lines 27–28 still says it supplies no second-derivative bound, whereas lines 339–342 do; this is a concrete stale parent exposition statement, reported without changing it.

To turn resolvent gradient control into Poincare, still prove the original closed-gradient kernel consists exactly of constants (distributional zero gradient and actual density/AE adapter on connected space), constants belong its domain via genuine weighted cutoff approximation, and the centered epsilon-resolvent/range or weak-limit argument. Testing constants for centering requires that produced domain membership. An operator route additionally needs a genuine form/adjoint realization and range/spectral argument; alternatively a weak-compactness/duality route must prove its limits and kernel elimination. Neither can assume Poincare, core equality, or epsilon-zero convergence as a certificate. Failure to prove a quotient/tail/curvature adapter must be recorded exactly, not patched by stronger moments or a new domain.

## Exact read-input footprints

Raw SHA256 preserves CRLF; LF SHA256 replaces CRLF with LF only. These files match their respective checked Git HEAD after LF normalization (not a raw-byte-equality assertion). Source anchors above were freshly opened; no primary source file was manufactured. The existing graph/Bochner parent hashes match their previously read freeze; this is bounded reuse, not a fresh full-proof compilation. No current exploring weighted-candidate file is included.

| Exact input path | Raw SHA256 | LF SHA256 |
|---|---|---|
| `research-wiki/cited-results/Weighted_cutoff_generator_core_route.md` | `afa282b1f59a364cba7255f191bac2d6182e9e98f845903b0ab4cb97a3b20a8a` | `6c71b91b57e2b83993f483bd5ad6145600c40dc7756d41388e562bda84859810` |
| `AutoSamplingTheory/TechnicalLemmas/Analysis/HessianSecantOperator.lean` | `5fd26bfab4df6d62c7a4cfc319a2cfb6e1a7447299930a68ef6cce162e904886` | `5fd26bfab4df6d62c7a4cfc319a2cfb6e1a7447299930a68ef6cce162e904886` |
| `AutoSamplingTheory/TechnicalLemmas/Analysis/ConvexSmoothGradient.lean` | `a6bcdb28498c5b34a18b43a18d2989b46d0fd9d972b22335fd74aaac6948e048` | `7218e97c12a200873455e396128487953b9e07c89862ad9c44925adb77f36cf1` |
| `AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean` | `fe9b99800277b9e9aae9b453a2edcdb2aa6e18a566096440179a4ea9c804d979` | `2e931c85c06a0a5ad815a396e7b9e678dc5fb0fd8bcdf6ba6ab2eabe2cde1706` |
| `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedResolvent.lean` | `34e3d1772e756ff0e59155590877b47bd36fb0c76ed58119810ec16d7c6fa044` | `21108f9c99d5f944e97e3c4721d1f9e5f9e2a68afa6122916ba3a16606e1edd3` |
| `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedBochner.lean` | `d2e566989400b76d4df02f3b47280401e1737c129e4f0ebee7f0b02b0e36c956` | `39b11508ddb3026e3033274a844708fd243621f460c81cc738065754b1364e9c` |
| `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CompactPoissonSmoothGraph.lean` | `fdb744363aa54f0338f203db0da8b0ae591fee76049c95f39af46ae30da93cf5` | `fdb744363aa54f0338f203db0da8b0ae591fee76049c95f39af46ae30da93cf5` |
| `AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalCompactSmoothGraph.lean` | `60d9cdf5e0b7eb0db80fb7664b916adcbe4833cad57aeae809d0a362a8a91287` | `60d9cdf5e0b7eb0db80fb7664b916adcbe4833cad57aeae809d0a362a8a91287` |
| `.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L2Space.lean` | `b27eb9c9823a58a229a17f69860c5bcf3defb433c23ff3bab335f864676df3b5` | `7dd0542490f2841e8a91d2258a903d328383d7305915375d99d589fae40de399` |
| `.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Complete.lean` | `2ac7010038b231d0f95771681fe076fd4c2cf8219c9476ddd474f3a4b72bdf06` | `7b020ac252943ab4b4f8ac917e030d5b21f8de7f2a624675fc0bc5078cf26aa8` |
| `.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean` | `e77596f8709e4af3304d4e810f32a60a242925151b0d868e1c2fad190db71f5a` | `18b709ea5c9ef9136e3e75ded82a6135641e6e19688e0ca3abcb0af45648ab84` |
| `.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Laplacian.lean` | `67c82a0517c6b5c08a30a5e4ff2fd7af170a1c904c5c29959c0cb3744fe35c21` | `3ee312cd1638dc1a6c45f1944df13057eaf24609f7f6bea9057abda1b9a1cf9d` |
| `.lake/packages/mathlib/Mathlib/Analysis/Calculus/BumpFunction/Basic.lean` | `82170bd702caef8e25417266005becfe79e0e2ccad99bd2586b1b4496ab6afa8` | `b1abfd5f8861ac0fde77577d6fbe1207b2bdc8f4410b07764a2a781d2b63726b` |
