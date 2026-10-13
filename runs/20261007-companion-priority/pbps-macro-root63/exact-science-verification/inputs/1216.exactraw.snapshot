# Weighted ordinary resolvent: local H² via the pinned Fourier APIs

Audit date: 2026-10-06. Independent planner: `picard_commit_verifier_20261005`.
Checked repository base: `3dd0f26066b68263deb9db1f37c66f3a5f874b17`.
Pinned Lean: `leanprover/lean4:v4.33.0`; Mathlib: `db584cd6d46c92f209a44c0f1c829460d327499d`.

This is a source/API dependency plan, **not a compiled theorem, source-admission receipt, new SAU, or proof of H²/core/Poincaré/BL**. No compiler was run for this audit. Root's ignored prototypes and subsequent candidate code were not read. The current ordinary-resolvent packet remains subject to its own exact-commit/source admission.

## Exact available input and desired next edge

The current `OrdinaryWeakResolvent.weak_resolvent_laplacian` returns one actual weak solution `u` and the gradient `G = D.closure u` for the original closed-gradient domain `D`, fixed before ε and f. It derives ordinary volume weak-gradient identities, compact-restriction volume L² for u and G, and for

\[
k=\varepsilon u+\langle\nabla W,G\rangle-f
\]

compact-restriction volume L² and the genuine C² compact-test identity

\[
\int u\,\Delta\varphi\,dx=\int k\varphi\,dx.
\]

The proposed next mathematical edge is local second weak derivatives of **these same representatives**, obtained from this identity. It must derive its cutoffs, volume L² classes and distribution identities, rather than accept H², a final PDE certificate, or a supplied approximate solution. Continuity of ∇W on compact sets suffices for the current local RHS; this route does not require W to be C∞.

## Source classification and omissions

- [PBPS, arXiv:2609.06905v1, Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1): the smooth compact argument, closure/domain extension and conditional Poincaré estimate concern the actual reflected conditional Gibbs law. A Fourier local-H² construction is an analytic prerequisite for extending suitable rough-solution arguments, not a theorem asserted there or an already supplied Poincaré proof.
- [SPHMC, arXiv:2609.06906v1, §4.1](https://arxiv.org/html/2609.06906v1#S4.SS1): the covariance upper estimate uses Brascamp–Lieb for the actual RGO posterior. Local H² of a resolvent alone supplies neither that functional inequality nor its global operator/core justification.
- [Chewi, *Log-Concave Sampling*](https://chewisinho.github.io/main.pdf), auxiliary locally cached edition `.astis/chewi-20261006-covariance.pdf`, SHA256 `8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`, printed pp. 113–114, Theorem 3.5.8 and Corollary 3.5.9: the lower covariance estimate follows from the linear-observable Cramér–Rao consequence of weighted IBP; the upper estimate invokes BL. These statements do not fill a local-H² or core/density proof. This auxiliary edition does not replace the repository's older pinned Chewi source.

Thus the edge is a shared analytic adapter with actual sampling consumers. It is not a new source theorem or a repetition of the already reviewed linear covariance lower bound.

## Pinned API inventory

Paths below are relative to `.lake/packages/mathlib/Mathlib/`. Names were read in the pinned files; availability is source inspection, not a new elaboration claim.

| Required interface | Available pinned API | Actual remaining adapter |
| --- | --- | --- |
| Smooth compact χ and an outer θ equal to 1 near a compact set | `Analysis/Calculus/BumpFunction/Basic.lean`: `ContDiffBump.contDiff`, `hasCompactSupport`, `one_of_mem_closedBall`, `eventuallyEq_one_of_mem_ball` (lines 137–170); `FiniteDimension.lean` supplies finite-dimensional bump instances | Enclose the compact set strictly inside the inner ball, not merely on its boundary. Use an unnormalized bump: a mass-normalized mollifier is not 1 inside. Preserve the zero-dimensional case. |
| Compact products and derivatives | `tsupport_fderiv_subset`, `tsupport_fderiv_apply_subset`; finite-basis Laplacian in `Analysis/InnerProductSpace/Laplacian.lean` | Derive support/boundedness of ∇χ and Δχ and the Laplacian product rule by the actual finite-basis second derivative formulas. The bounded search did not find a direct `laplacian_mul` in that file. |
| Actual ordinary weak-gradient/PDE and compact L² | ASTIS `WeightedLocalL2`, `WeightedResolventC1`, `OrdinaryWeakResolvent`; actual reflected-law consumer `ConditionalOrdinaryResolvent` | Convert restricted-measure L² plus compact support to global volume `MemLp`, with measurable representatives and AE restriction identities explicit. Weighted L² is not already volume L². |
| Real to complex L² | `MeasureTheory/Function/LpSpace/Basic.lean`: `MemLp.ofReal`; `LpSeminorm/Monotonicity.lean`: `MemLp.re` | Build the actual complex `toLp` classes and prove their representative/AE identities. Real-part derivative/test commutation still needs the appropriate CLM calculus. |
| L² to genuine tempered distributions | `Analysis/Distribution/TemperedDistribution.lean`: `Lp.toTemperedDistribution`, `_apply` (lines 160–169), `toTemperedDistributionCLM` (195), `ker_toTemperedDistributionCLM_eq_bot` (215) | Apply to **global volume** L² after cutoff; volume has the required temperate growth. The pairing is ∫φ(x) • v(x), complex bilinear, not the conjugated Hilbert inner product. |
| Compact tests and Schwartz tests | `SchwartzSpace/Basic.lean`: `HasCompactSupport.toSchwartzMap` (555), `SchwartzMap.memLp`/`toLp` (1316ff.); `TemperedDistribution.laplacian_apply_apply` (440) | Extend the actual compact-test PDE to every complex Schwartz test. Compact-test embedding alone is not such an extension. |
| Exact Fourier constants | `FourierMultiplier.lean`: TD `fourierMultiplierCLM_const` (156), `sum` (180), `laplacian_eq_fourierMultiplierCLM` (208); `TemperedDistribution.smulLeftCLM_add/sub` (277/283) | Prove the specialized Bessel order-2 identity below. The search found the ingredients, not a ready named converse elliptic-regularity theorem. |
| H² and mixed weak derivatives | `Sobolev.lean`: `besselPotential` (71), `MemSobolev` (149), `memSobolev_zero_iff` (153), `MemSobolev.lineDerivOp` (316) | Construct the order-2 witness from actual v and Δv, then apply directional differentiation twice and extract actual order-0 L² representatives. |
| Density | `SchwartzSpace/Basic.lean`: `SchwartzMap.denseRange_toLpCLM` (1383); `Distribution/AEEqOfIntegralContDiff.lean`: compact-test AE uniqueness | The density is in Lᵖ only. It does **not** establish compact smooth density in H² or the same weighted gradient/operator graph norm. No such core is claimed by this audit. |

`Distribution.lean` uses real compact tests; the tempered-distribution Fourier APIs use complex Schwartz tests. That change of test space/scalars must be proved in the adapter. The already available `MemSobolev.laplacian` is the forward map Hˢ → Hˢ⁻² and cannot be used as a converse.

## Proposed route, at most seven steps

1. **Localize actual representatives.** For χ ∈ C∞c set v = χu and Gχ = χG + u∇χ. Derive global volume L² of these functions from the actual compact-restriction L² output and boundedness/support of χ and ∇χ. Set
   \[
   F_\chi=\chi k+2\langle\nabla\chi,G\rangle+u\Delta\chi.
   \]
   Derive its actual global volume L² separately; no local-to-global implication without cutoff is permitted.
2. **Derive the cutoff PDE.** Use the actual C¹ weak-gradient identities and C² compact PDE with product tests to prove ∇v = Gχ weakly and ∫vΔφ = ∫Fχφ. Validate the coefficient 2 and every L¹ product before splitting integrals. All these functions have support contained in K = tsupport χ (at least after the required representative/AE statements).
3. **Extend tests with one outer cutoff.** Choose θ ∈ C∞c identically 1 on a neighborhood of K. For an arbitrary complex Schwartz ψ, the real and imaginary parts of θψ are admissible compact smooth tests. Since θ is locally constant 1 near K, Δ(θψ) = Δψ there. This gives the PDE for ψ without an expanding-cutoff limit or unproved tail estimate. Prove the requisite real/imaginary derivative identities and integrability. This outer-cutoff argument is the smallest identified test-extension adapter.
4. **Build actual complex distributions.** Form complex volume L² classes of v and Fχ and embed them with `Lp.toTemperedDistributionCLM`. Using `_apply`, AE representative identities and `laplacian_apply_apply`, deduce ΔT = LpTD(Fχ), where T = LpTD(v). No weighted class is silently treated as tempered.
5. **Construct H² with the exact Bessel convention.** Pinned Mathlib has
   \[
   \Delta T=-(2\pi)^2\operatorname{FM}(\|\xi\|^2)T,
   \qquad B_2T=T-(2\pi)^{-2}\Delta T.
   \]
   The second identity follows from the definition of `besselPotential` at s = 2, simplification of the real power, and addition/constant multiplier APIs; it still needs a compiled leaf. Thus the actual complex volume L² class v − (2π)⁻²Fχ witnesses `MemSobolev 2 2 T`. Replacing this by I − Δ would use the wrong normalization.
6. **Extract the actual local weak Hessian.** Apply `MemSobolev.lineDerivOp` twice (2 → 1 → 0), use `memSobolev_zero_iff`, and take real parts to produce each finite-basis mixed second weak derivative. Prove representative/test compatibility. On an open set where χ = 1, identify v with the original u and Gχ with the original G. Finite basis reconstruction/all-direction identities and their restriction are explicit obligations; the scalar Laplacian alone is not a supplied Hessian.
7. **Keep the next domain edge separate.** Any later application of smooth compact Bochner to u requires actual smoothing/core convergence in the needed derivative and weighted graph norms, plus boundary/tail estimates. `denseRange_toLpCLM` alone does not supply those. Global weighted H², same-operator core density, BL/Poincaré and resolvent energy estimates remain distinct future edges.

For dimension zero, preserve the existing empty-basis conventions: there are no mixed second directions and Δ = 0; B₂ = I. Do not add a nontrivial-space or unit-vector premise merely to reuse a cutoff or Fourier helper. The Fourier route above uses complex scalar codomain ℂ, a complete inner-product space, finite-dimensional real Euclidean domain and actual Lebesgue volume; it is not stated for an arbitrary finite/atomic measure.

## Smallest next producer and failure boundary

The algebraic shared leaf `B₂T = T − (2π)⁻²ΔT`, followed by an actual global-L² Poisson-to-`MemSobolev 2 2` interface, is a short dependency-ready target with this local-H² consumer. It must accept an actual tested distribution equation, not an H² certificate. The separate cutoff/test-extension producer then connects the existing u/G/PDE to that leaf. These are suggested interfaces only; no declaration or SAU is claimed here.

If the test-extension or restriction proof stalls, report exactly whether the gap is compact cutoff support, AE/global-L² class construction, real/complex derivative compatibility, or missing norm-density. Do not replace it with an assumption that the weak PDE holds for Schwartz tests, or accept final second derivatives/core existence as input to the claimed producer. Fourier proves local unweighted regularity after these adapters; it does not remove global weighted tails.

## Reflected law versus RGO

PBPS has the reflected conditional potential
\[
W^{\rm ref}_{y,\eta}(z)=V((y+z)/2)+\|z-y\|^2/(8\eta),
\]
whereas the RGO potential is
\[
W^{\rm rgo}_{y,\eta}(x)=V(x)+\|x-y\|^2/(2\eta).
\]
Under z = 2x − y, the partition masses satisfy Zref = 2ᵈ Zrgo. For a reflected observable a and its RGO pullback b(x) = a(2x − y), ∇b = 2(∇a) ∘ (2x − y), so its RGO Dirichlet energy is four times the reflected energy. In the other direction, the reflected potential Hessian is one quarter of the RGO potential Hessian at x = (y + z)/2. Any transfer of domains, Laplacian/resolvent or ε must derive those operator factors and the measure pushforward. The local-H² plan is fibrewise and supplies no measurable selector in y. Reflected PBPS, RGO smoothing/BL, stochastic history/work, and both main results/composition retain independent acceptance boundaries.

Only this planning file was written. No production proof, new formal parent, lifecycle transition, independent source verdict, compiler credit, or completion badge results from this audit.
