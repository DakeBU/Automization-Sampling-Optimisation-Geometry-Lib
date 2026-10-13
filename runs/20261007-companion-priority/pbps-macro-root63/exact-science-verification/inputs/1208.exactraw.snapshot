# Compact weighted coercivity: independent source prerequisite audit

2026-10-06. Author: `phase_source_reviewer_20261005`, distinct from the proving worker. This is a primary-first source/API preread and proposed analytic route, with no theorem admission, source-equivalence verdict, compiler run, independent Lean-verification credit, or lifecycle change. Repository inputs were checked at `0a563a9124e51578aea3dbf7d1d0e68606c80bd0` (current HEAD). The graph packet's exact verification status is administrative information, not evidence for the proposed next edge.

## Primary boundary and reading order

Freshly read [PBPS arXiv:2609.06905v1 §2.2](https://arxiv.org/html/2609.06905v1#S2.SS2), HTML 168–212, and [Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1), HTML 1197–1234, followed by [SPHMC arXiv:2609.06906v1 §4.1](https://arxiv.org/html/2609.06906v1#S4.SS1), HTML 403–430, before inspecting the current raw proposal or next-route APIs. PBPS uses a conditional Poincare estimate and invokes density/closedness of the gradient; the compact weighted graph-to-coercivity construction below supplies an omitted analytic prerequisite, rather than quoting a numbered theorem. SPHMC invokes BL for an RGO covariance upper bound; this prerequisite alone does not produce that bound. CR covariance lower bounds remain a distinct half of the argument.

Prior exposure is explicit: I have read the existing localization and compact smooth graph proofs/reader exposition during their independent source reviews, and my earlier source/API prereads. Earlier bounded BL searches exposed covariance candidate signatures/keywords/matching lines; those searches were not proof-correctness evidence. The current root-authored `Weighted_compact_coercivity_from_graph_route.md` was read only after the primary reconstruction, as a proposal. No ignored weight-transfer prototype, future candidate, anonymous reconstruction, mathematical verdict, or exact-verifier verdict was opened for this preread.

## Seven semantic slots

1. **Objects.** Ordinary-volume weak data are real (v,F:E\to\mathbb R) and vector (G:E\to E). Their actual common approximants are real compact smooth \(\varphi_n\), with function, gradient and Laplacian limits simultaneously. The weighted objects must be actual quotient classes \(v_W,G_W,A_W\), AE-linked to \(v,G,A=\langle\nabla W,G\rangle-F\). Here \(A_W\) denotes this L2 class, not an operator or an assumed output certificate. \(D\) is the original compact-smooth gradient partial linear map, not a newly chosen closed gradient.

2. **Domains and measures.** \(E\) is a finite real Hilbert space with Borel structure and its ordinary Haar volume, including dimension zero. Let \(Z=\int e^{-W}\,dx\) with actual integrability and \(Z>0\), and \(\mu=\mathrm{volume}.\mathrm{tilted}(-W)\), with true density \(e^{-W}/Z\). Ordinary and weighted L2 spaces differ. The required new domain consequence is \(v_W\in\mathrm{domain}(D.\mathrm{closure})\) and \(D.\mathrm{closure}(v_W)=G_W\); no adjoint or generator domain is asserted. Each smooth approximant must have true compact support, not merely decay as a Schwartz function.

3. **Quantifiers.** For the paper consumer retain the original common normalized joint/RGO/reflected kernels \(J,R,S\), then \(\forall y\,\exists D_y\), chosen before \(\varepsilon>0\) and input \(f\). For those inputs there is **one** actual resolvent \(u\) before **all** real C2 compact cutoffs \(\chi\). For each cutoff, produce the actual weighted classes and domain consequence using the **same** one sequence \(\varphi_n\) from the three-component ordinary graph approximation. One common outer compact \(K'\) precedes every \(n\). No replacement \(u\), \(D_y\), sequence for each component, or jointly measurable fiber selection may be smuggled into this order.

4. **Hypotheses.** Generic transfer needs continuous actual density and continuous drift (C1 \(W\) suffices for that part), but the Bochner parent requires C2 \(W\), C-infinity compact tests and a genuine all-vector lower Hessian bound. Retain actual ordinary MemLp/L1 weak gradient and weak Poisson equations, supports, closability and the exact original \(D\)-graph characterization. The source consumer has C2 \(V\), \(0<\alpha\le\beta\), \(\eta>0\), \(\beta\eta\le1\); its normalizer/curvature and original \(D\) come from actual existing producers. Do not add C-infinity \(W\), globally bounded drift, input moments such as \(\|x\|u\in L^2\), or supplied final weighted convergence/domain/adjoint certificates.

5. **Conclusion.** The bounded proposed endpoint is actual weighted MemLp/AE representatives, membership in the same gradient closure and
   \[
   \lambda\|G_W\|_{L^2(\mu)}^2\le\|A_W\|_{L^2(\mu)}^2.
   \]
   For the cutoff, \(v=\chi u\), \(G_\chi=\chi G+u\nabla\chi\),
   \(F_\chi=\chi r+2\langle\nabla\chi,G\rangle+u\Delta\chi\),
   where \(G\) is an actual representative of \(D_y.\mathrm{closure}(u)\) and \(r=\varepsilon u+\langle\nabla W_y,G\rangle-f\). The right side is the norm of \(-F_\chi+\langle\nabla W_y,G_\chi\rangle\), with this exact sign.

6. **Scope.** This is compact localized scalar coercivity plus a produced first-gradient domain membership. It legitimately avoids rough-Hessian convergence for this narrower conclusion. It does not identify the rough Hessian, prove a full Bochner identity on an operator domain, equate generator/adjoint cores, remove cutoffs, solve the epsilon-zero problem, prove Poincare/BL, or close either main theorem or composition. The source's conditional Poincare invocation and density argument leave those larger obligations separate.

7. **Constants and normalization.** The actual reflected conditional potential is
   \[
   W_y^S(z)=V((y+z)/2)+\|z-y\|^2/(8\eta),\qquad
   m_S=(\alpha+\eta^{-1})/4.
   \]
   The unreflected RGO has \(W_y^R(x)=V(x)+\|x-y\|^2/(2\eta)\) and \(m_R=\alpha+\eta^{-1}\). Pushforward by \(z=2x-y\) carries Jacobian \(2^{-d}\); gradients/Dirichlet energies change by factors \(1/2\) and \(1/4\). Do not identify these laws or constants without the true adapter. The Bochner parent accepts any real lower-bound \(\lambda\), including signed values; the source's positive \(m_S\) gives meaningful coercivity. Divide its unnormalized energies by positive \(Z\) exactly once. No Fourier constant appears in this norm-limit passage; the graph parent's already-derived real Laplacian is the one consumed.

## Seven-step route and actual interfaces

1. Consume `CompactPoissonSmoothGraph.compact_weak_poisson_smooth_graph_approximation` (lines 683–719) with genuine compact data and weak equations. Its actual public conclusion gives one real `SchwartzMap` sequence with compact supports and all three L2 limits. It does **not** say \(K'\supseteq K\). Set \(\bar K=K\cup K'\), which is compact. Function, gradient and Laplacian of each smooth term vanish outside \(K'\); original data vanish outside \(K\).
2. On \(\bar K\), derive finite \(C_\rho,M\) bounding \(\rho=e^{-W}/Z\) and \(\|\nabla W\|\). Prove actual measure domination \(\mu|_{\bar K}\le C_\rho\,\mathrm{volume}|_{\bar K}\) from the with-density definition. `Measure.tilted` is normalized (Tilted.lean 42–43); integrability and positive \(Z\) are essential because totalized tilting can otherwise be zero. `withDensity_mono` and `restrict_withDensity` provide the measure identities.
3. Transfer the compact-supported three-component errors via `eLpNorm_restrict_eq_of_support_subset` (Basic.lean 593), `eLpNorm_le_of_measure_le_smul` (689) and `MemLp.of_measure_le_smul` (694). At exponent two the bound is \(\|h\|_{L^2(\mu)}\le\sqrt{C_\rho}\|h\|_{L^2(dx)}\). Prove representative measurability, actual MemLp and volume-AE to \(\mu\)-AE links, then actual `toLp` equalities; do not confuse quotient-class convergence with pointwise convergence. Absolute continuity of \(\mu\) supplies AE transfer. A compact density lower bound is available but not needed for this transfer direction.
4. The actual local drift bound gives
   \(\|\langle\nabla W,\nabla\varphi_n-G\rangle\|_{L^2(\mu)}\le M\|\nabla\varphi_n-G\|_{L^2(\mu)}\).
   Therefore \(-\Delta\varphi_n+\langle\nabla W,\nabla\varphi_n\rangle\to A_W\) in weighted L2, using the same sequence and true support before multiplication. All compact smooth products are L1/L2; rough products follow from these bounds, not formal algebra alone.
5. The original graph characterization places each actual weighted function/gradient pair in \(D.\mathrm{graph}\). Pass both limits in the product space. `LinearPMap.IsClosable.graph_closure_eq_closure_graph` (107–110) equates topological graph closure with \(D.\mathrm{closure}.\mathrm{graph}\). Extract membership and the exact gradient equality. Density is retained from the source producer but is not needed for this isolated closed-graph passage.
6. `WeightedBochner.integrated_bochner_identity` (34 onward) uses C2 \(W\), C-infinity compact \(\varphi_n\), and derives all four compact weighted integrability statements; global weight integrability is not a premise of that parent. Its \(L=\Delta-\nabla W\cdot\nabla=-A\) has opposite sign, irrelevant only after squaring. Its curvature consequence already discards the nonnegative sum of squared directional-gradient terms. Thus for every \(n\), \(\lambda\|\nabla\varphi_n\|_\mu^2\le\|A\varphi_n\|_\mu^2\), after normalization.
7. Continuity of norm and squaring passes this scalar inequality to \(G_W,A_W\). **No second-derivative limit or lower-semicontinuity argument is required.** Conversely it supplies no identity \(A_W=D^*D(v_W)\): that would require an actual adjoint-domain/weak-IBP extension proof, outside the declared endpoint. In dimension zero the directional sums/gradient/Laplacian vanish; the inequality is \(0\le0\), and graph closure reasoning must still retain actual quotient measures without a nonempty-basis assumption.

The smallest missing analytic node is the genuine compact weighted measure/norm/AE transfer of the existing simultaneous sequence, followed by the same-graph closure adapter. Its scalar Bochner limit is then elementary. This is substantive when those actual classes and limits are **produced**; a wrapper assuming final weighted convergence, domain membership, or coercivity is not this edge.

Failure boundary: if domination, coefficient multiplication, AE transfer, original graph compatibility, or exact normalization cannot be derived, record that precise residual. Do not weaken to a different gradient domain or silently supply the desired certificate. Stronger global/rough-Hessian/core conclusions require separate inputs and proofs. No compiler or future prototype was used.

## Exact immutable input footprints

Raw hashes retain on-disk bytes; LF hashes replace CRLF with LF only. All named canonical inputs below match their own repository HEAD after LF normalization; this does not assert raw LF/CRLF equality. Mathlib checkout is `db584cd6d46c92f209a44c0f1c829460d327499d` (Lean 4.33). This note reads source and API contracts, not a new full-proof verification.

| Exact input path | Raw SHA256 | LF SHA256 |
|---|---|---|
| `research-wiki/cited-results/Weighted_compact_coercivity_from_graph_route.md` | `22837a53b4d55e704616709ef083e2d45522fca2fece93762c0208050f84518c` | `22837a53b4d55e704616709ef083e2d45522fca2fece93762c0208050f84518c` |
| `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedBochner.lean` | `d2e566989400b76d4df02f3b47280401e1737c129e4f0ebee7f0b02b0e36c956` | `39b11508ddb3026e3033274a844708fd243621f460c81cc738065754b1364e9c` |
| `AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CompactPoissonSmoothGraph.lean` | `fdb744363aa54f0338f203db0da8b0ae591fee76049c95f39af46ae30da93cf5` | `fdb744363aa54f0338f203db0da8b0ae591fee76049c95f39af46ae30da93cf5` |
| `AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalCompactSmoothGraph.lean` | `60d9cdf5e0b7eb0db80fb7664b916adcbe4833cad57aeae809d0a362a8a91287` | `60d9cdf5e0b7eb0db80fb7664b916adcbe4833cad57aeae809d0a362a8a91287` |
| `.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean` | `53cc37610d1b21725a178c7d8064c59bb28629625d844b02430a30714ecd0c3e` | `355cce542b03dd9130d9511f80ae803cc11a12ba9e6a947e68402b124be2165f` |
| `.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/WithDensity.lean` | `9493b6567e2b4b647792141e1181e646d4f14331c5d5d47cb09c17bf044a1e45` | `b62c4ad72728e11a87bb3cefc6b968a081a70901030e8ac8e60d43b5ec2a8649` |
| `.lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSeminorm/Basic.lean` | `3c03ab83885347264233c79ab606bb99f68f4c6006c971e4eac63fe2dc49451b` | `a9cbdad8fae393b320ba20cf025bbac20722fc85f76b7b44ea8968134f9b0bfb` |
| `.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/LinearPMap.lean` | `8b034650fd42dd1eb87719892c80cc46f8d0d627fd386fe3e5aa5a6a0a451936` | `0f09b4171438d914fb2326706eea68be85b1423d1e9340cdd07afa6fc87e4360` |
