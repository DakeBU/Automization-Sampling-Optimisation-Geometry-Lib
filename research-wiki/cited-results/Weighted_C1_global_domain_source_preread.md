# Weighted global C1 membership in the same original gradient closure

Owner: independent source reviewer `phase_source_reviewer_20261005`. Read2026-10-06. **Raw prerequisite proposal only**: no SAU, candidate acceptance, fresh Lean verification or mathematical completion credit. Compiler not run. Current API footprint HEAD: `801d524eabb5da16169f377d59721e7dc0d75d05`; this records inspected bytes, not repository-wide clean/verification status.

Fresh primary was read before accepted API planning: [PBPSv1 §2.2](https://arxiv.org/html/2609.06905v1#S2.SS2), HTML168–212; [PBPSv1 AppendixC.1](https://arxiv.org/html/2609.06905v1#A3.SS1), HTML1197–1229; [SPHMCv1 §4.1](https://arxiv.org/html/2609.06906v1#S4.SS1), HTML403–430. PBPSC.1 invokes density/closedness at1200 and noncompact directional score tests at1217–1226. The proposed domain producer fills omitted analytic detail; it is not a quoted numbered theorem. SPHMC's RGO covariance inequalities remain separate consumers.

The PBPS reflected potential and parameter score are

\[
W_y(u)=V((y+u)/2)+\|u-y\|^2/(8\eta),\qquad
s_y(u)[a]=-\tfrac12 DV((y+u)/2)[a]-\langle y-u,a\rangle/(4\eta).
\]

Here `s` differentiates the unnormalized log weight in **y**; it is neither the negative u-gradient of W nor a normalized score without centering. Keep source C2 V, actual all-vector alpha/beta Hessian bounds, explicit0<alpha<=beta and0<eta with beta*eta<=1. The reflected Hessian is one quarter of HessV+eta^-1 I; its Dirichlet/Poincare scale is fourfold. RGO uses V(x)+norm(x-y)^2/(2eta), a different law/scale. Those source inequalities are context, not results proved by this note.

## Seven-slot proposed contract

- **Objects:** actual finite normalized Gibbs mu; original real partial-linear compact-smooth gradient D; genuine scalar C1 f and gradient f, with actual weighted L2 classes. Conditional s_y(u)[a] is the actual score above.
- **Domains:** finite real Hilbert/Borel E including0, canonical full-space volume for smooth representatives, weighted L2(mu) for limits and closure. No boundary/disconnected-domain generalization. Positive density permits AE transfer; a zero or infinite normalizer cannot be silently accepted.
- **Quantifiers:** actual mu and ONE original exact closable D precede ALL admissible C1 f. Conditional common J/R/S precede ALL y; each original D_y precedes ALL f, constants and directions. No new D per input, joint measurable fiber selector, or identification of independently chosen conditional versions.
- **Assumptions:** C1 f, MemLp f2mu and MemLp(gradient f)2mu, finite mu and exact closable compact-C-infinity gradient graph. For Gibbs, C1 W and genuine exp(-W) integrability derive positive normalized probability; no C-infinity W, moments, Poincare premise or final domain certificate.
- **Conclusion:** proposed pair of actual function/gradient classes lies in SAME D.closure.graph; constants and directional scores become concrete instances. Original scalar L2 representative equality is AE, not rough classical differentiability.
- **Scope:** only original-gradient domain membership. Constants-domain production is a missing converse input to the already one-way zero-gradient implication, not a declared full kernel-equality theorem here. Epsilon-zero/range/Poincare/BL/weighted generator-core and main/composition remain open.
- **Constants:** one scale-uniform cutoff derivative C/R, score-gradient bound `(eta^-1-alpha)*norm(a)/4`; no norm(x)*f moment. Dimension0 retained without a Nontrivial E premise.

## Actual available APIs versus missing node

`CompactC1GradientDomain.compact_c1_in_closed_gradient` lines118–165 is a genuine producer for C1 **compact** functions against any finite mu with exact closable original graph. It returns actual MemLp witnesses and a pair in the same closure graph, by real normalized mollification. It does not handle noncompact f. Its `l2_convergence` lines100–115 is **private**, hence not a callable shared interface.

`Cutoff.radialSmoothCutoff_*` supplies positive-scale smoothness198, values[0,1]175, pointwise-to-one390, compact support324 and a uniform first-derivative bound235. First-order exhaustion does not consume the second-derivative bound's Nontrivial E premise. `WeightedGradient.compact_gradient_closable`34–41 constructs the actual Gibbs D with exact graph; `ConditionalGradientKernel.conditional_gradient_zero_ae_constant`15–36 constructs actual common reflected laws and original dense/closable D_y, then its one-way zero-output implication. Reuse that actual D, not an arbitrary replacement.

`ConditionalScoreDomain.conditional_curvature_and_score_domain`30–56 produces actual normalized reflected S2_y, C1 directional score, scalar MemLp and pointwise gradient bound for every direction. Its lines350–356 identify the exact reflected density;388–393 derive L2 from the genuine Gaussian envelope, not supplied moments. `Poincare.Admissible`36–39 is only L1/variance/gradient-energy integrability; it gives neither original graph membership nor Poincare. Actual C1 gradient continuity plus the bound and finite probability gives vector MemLp via `MemLp.of_bound`.

The shortest missing analytic node is **global C1 weighted graph membership by actual cutoff exhaustion**, together with its two actual L2 class limits. No supplied smooth-density/graph-domain certificate qualifies as that node.

## Proposed mathematical route, at most seven steps

1. Fix mu and SAME original D. Derive any needed scalar/vector measurability from actual C1 f. Choose R_n=n+1 and actual smooth cutoffs chi_n; set f_n=chi_n*f. Each f_n is genuine C1 compact with gradient `chi_n*gradient f + f*gradient chi_n`.
2. Apply the existing compact C1 producer to each f_n in SAME D. All class constructions must be MemLp-backed with their actual AE representatives; uniform compact support across n is neither available nor needed.
3. Prove the actual scalar limit in weighted L2 by dominated convergence of `|(chi_n-1)*f|^2`, dominated by |f|^2. Prove `(chi_n-1)*gradient f` tends to0 in vector L2 using norm-square domination by norm(gradient f)^2.
4. Prove the product remainder tends to0 by `norm(f*gradient chi_n)_L2 <= C/R_n * norm(f)_L2`; alternatively square integral bound `C^2/R_n^2 * integral |f|^2`. Thus no spatial moment is required. Establish real integrability before using integral algebra or convergence.
5. Convert both actual norm-square limits into L2 quotient convergence (public `Lp.tendsto_Lp_iff_tendsto_eLpNorm''`, or the explicit L2-inner/sqrt calculation). Use SAME closure graph closedness and product convergence. `IsClosable.graph_closure_eq_closure_graph` proves closure is the original graph's topological closure; `mem_graph_iff` recovers actual domain and output. Do not treat the parent's private conversion lemma as public.
6. Instantiate f=constant c: finite probability gives scalar MemLp, genuine gradient=0 gives vector MemLp. Produce constant domain/output0, without assuming volume-global L1 or mean-zero constants; in dimension0 these contracts remain valid.
7. For actual conditional scores, first retain the original R/S/D_y from the actual gradient consumer. Obtain score data from its existing separate S2 producer and prove literal `S2_y=volume.tilted(-W_y)=S_y`. Rewrite MemLp/finite-measure data along this equality only, derive vector-gradient L2, apply the global C1 leaf to SAME D_y for each a. No proof of R2=R or newly selected D is needed or claimed.

## Failure and hidden-regularity boundaries

The two-sided full-space positive Gibbs density and finite normalization are actual obligations, not metadata. Generic finite mu is allowed only with the exact closable original gradient graph; arbitrary singular measures do not automatically have that graph. C1 global functions need both actual L2 premises; probability alone does not make an unbounded function L2. Source score L2 is already a genuine producer, whereas the graph adapter remains the proposed delta. A convergence statement about representatives alone cannot replace L2 quotient convergence; partial-operator domain membership must be extracted from actual graph membership. Do not use arbitrary totalized derivatives for f, score or cutoffs without genuine differentiability.

This route needs no rough Hessian convergence, second-derivative cutoff estimate, global bounded drift, global volume L1, norm(x)*f moments, full adjoint/core identity, epsilon-zero passage or measurable joint fiber choice. Kernel equality may later combine separately proved ingredients; this note neither asserts it nor supplies spectral coercivity. Source claims about smooth tests conceal density/closedness and extension of noncompact score tests; those omitted prerequisites must be proved, not treated as already formal by source attribution.

## Exposure and immutable footprints

Prior exposure consists of my own independent primary/API compact-C1 and kernel prereads and earlier accepted-parent source reviews, plus the previously disclosed covariance keyword/signature exposure. The current assignment's proposed target was seen as a claim. No ignored `WeightedC1DomainPrototype`, future production, anonymous reconstruction, mathematical/verifier verdict or proposal discovery was read. Current accepted public interfaces and necessary implementation lines were inspected; this is not a fresh full-proof reacceptance. Truncated batched output was followed by targeted interface reads.

Fresh primary HTML was opened online; no local primary cache or invented raw source hashes were created. Toolchain is Lean4.33.0, Mathlib pin db584cd6d46c92f209a44c0f1c829460d327499d. Own raw/LF input snapshots and primary-contract evidence are in `runs/20261006-companion-priority/weighted-c1-gradient-domain/source-prereview*`. Exact inspected files follow; raw means original bytes, LF means CRLF converted to LF without JSON reserialization.

| Input | raw SHA256 | LF SHA256 |
|---|---|---|
| AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/CompactC1GradientDomain.lean | `3a08a4dc62796d8a5d021755c841280010d92d2b3259efee311232bf8ab8d096` | `dd6234dfec6d2dfb351d1ad45c3fcc0eb111e1c18038ebc4c6ab48035033a2f7` |
| AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Cutoff.lean | `fe9b99800277b9e9aae9b453a2edcdb2aa6e18a566096440179a4ea9c804d979` | `2e931c85c06a0a5ad815a396e7b9e678dc5fb0fd8bcdf6ba6ab2eabe2cde1706` |
| AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalScoreDomain.lean | `88675897290ba5b11ab1fb96b13fa3170da5c1fff41926b59771bf88c26ec419` | `45d838a1ea0acd078db24d38323be39db4b7485d596adb828179f46f9d9f24e4` |
| AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalScore.lean | `2fc25ec02d242eba8fd5724c4ea1795a6f04f6935b5b5933acb1319d0eeb66b3` | `39eec278de291ed52cf847f40ca064e89c301dac97406127fd3612b772c0776a` |
| AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientKernel.lean | `00576bc3e674590dc60da6f0cd2b6f33f658c055cec3ce52229757819335e5aa` | `964e1698824181ce599dab8cd47c1c0e0380e7bf885ad8a1b33982f58e7864b5` |
| AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradient.lean | `8453ea8758be0ce67c32a434b2b5b4e4523572447001c52de18238c662cfd2a7` | `3452712be04429132cbebcb6b9e6e24835d1f5f3dee9ddcd0af83c7a2d268ed6` |
| AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/WeightedGradient.lean | `c2495b6ab8a4c82cadf0d86b910d663e0e4f65f6b96bc4b449149112756d4690` | `5bd3402124330f69d7875e9bbfc6eb31760b70528850ac841d1ff7c84ab72149` |
| AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/Poincare.lean | `2ed9867990f70b138c247ade00d39b410ed0b7ee361075f32bb55407461a8409` | `e1a01d38ce2c418273d805cc7ade34ba1ec4114b647d6e787a6f5bd6ddb27af3` |
| AutoSamplingTheory/TechnicalLemmas/Analysis/Calculus/Gradient.lean | `b0e6a1c0c60c273621d9d612bf7874ac90fb5d90dee0c202d56b75a149e16db5` | `9482edb1349892d5a8104f25080e5ce2a0b6135862a3ece6ec283a614e42920a` |
| .lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean | `e77596f8709e4af3304d4e810f32a60a242925151b0d868e1c2fad190db71f5a` | `18b709ea5c9ef9136e3e75ded82a6135641e6e19688e0ca3abcb0af45648ab84` |
| .lake/packages/mathlib/Mathlib/MeasureTheory/Function/LpSpace/Complete.lean | `2ac7010038b231d0f95771681fe076fd4c2cf8219c9476ddd474f3a4b72bdf06` | `7b020ac252943ab4b4f8ac917e030d5b21f8de7f2a624675fc0bc5078cf26aa8` |
| .lake/packages/mathlib/Mathlib/Topology/Algebra/Module/LinearPMap.lean | `8b034650fd42dd1eb87719892c80cc46f8d0d627fd386fe3e5aa5a6a0a451936` | `0f09b4171438d914fb2326706eea68be85b1423d1e9340cdd07afa6fc87e4360` |
| .lake/packages/mathlib/Mathlib/LinearAlgebra/LinearPMap.lean | `1633745f8aedaaff56ca35af52e457359f95e9a3f7795d7224720df11ea48cc9` | `1d2975571378546a4b12058c99724b255e5a3b05def0c238e1e800c6f3a60090` |
| lean-toolchain | `b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477` | `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b` |
| lake-manifest.json | `b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2` | `b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37` |
| .agents/skills/astis-source-dependency-audit/SKILL.md | `b6e60a7f0bf53a5eb5f9450df7a56fbd9364e2bae95bb6d468e72939b24ea277` | `5790d02d4cdac24ccea5b33afa253d2fc855d76faef1a99476e7fe90f1cd1df1` |

Compiler: NOT RUN. Production/cells/audits/shared/ledger/Goal: untouched. All writes CLOSED after this preread. No source verdict or theorem admission.
