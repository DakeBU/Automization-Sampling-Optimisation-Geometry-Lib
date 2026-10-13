# Compact weak PDE → Schwartz tests → genuine L² tempered distribution

Independent dependency audit, 2026-10-06, `picard_commit_verifier_20261005`.
Checked base HEAD: `612dc53d7203483f099344c73a0ca6d2bab6042f`.
Lean: `leanprover/lean4:v4.33.0`; Mathlib: `db584cd6d46c92f209a44c0f1c829460d327499d`.

This is a read-only source/API plan, not a compiled theorem or VERIFIED admission. No compiler was run. The current `LocalizedWeakResolvent` packet is PROVED_LOCAL and undergoing separate source review; its source verdict and anonymous reconstruction were not read. Ignored prototypes and the new weighted-core planning note were not read. Only this audit file was written.

## Exact input and next boundary

The independently mathematics-reviewed `LocalizedWeakResolvent.localized_weak_resolvent` calls the accepted `OrdinaryWeakResolvent.weak_resolvent_laplacian`. For the original closed-gradient domain D, fixed before ε and f, it returns the same actual u and G = D.closure u before **all** compact C² cutoffs χ. With ordinary Lebesgue volume,

\[
r=\varepsilon u+\langle\nabla W,G\rangle-f,\quad
v=\chi u,\quad G_\chi=\chi G+u\nabla\chi,\quad
F_\chi=\chi r+2\langle\nabla\chi,G\rangle+u\Delta\chi.
\]

It derives global volume L² of v, Gχ and Fχ, their topological supports contained in K = tsupport χ, the actual weak first-derivative identity, and, for every real compact C² φ, integrability of both sides and

\[
\int v\Delta\varphi\,dx=\int F_\chi\varphi\,dx.
\]

These are pointwise functions taken from the same u/G representatives. Subsequent `toLp` constructions must explicitly carry their volume-AE equalities; support conclusions must not silently be asserted for newly selected quotient representatives. The generic producer assumes the actual specified closable D/graph; it does not construct such a D for every arbitrary atomic measure. The source consumer `ConditionalLocalizedResolvent.conditional_localized_resolvent` constructs D for the genuine reflected positive Gibbs fibre first, then takes ε, f, u and χ in that order.

The desired next result is `MemSobolev 2 2` of the genuine complex volume-L² embedding of **this v**, derived from its compact-test PDE. A supplied Schwartz PDE or H² certificate would omit the next proof obligation. W only needs the existing C¹ regularity; χ is C², not implicitly C∞.

## Source role

[PBPS v1, Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1), HTML lines 1197–1237, invokes compact smooth tests, density and gradient closedness in its macroscopic-coercivity argument. The local regularity/core adapters remain analytic prerequisites; the source does not supply this particular compact-to-Schwartz producer. [SPHMC v1, §4.1](https://arxiv.org/html/2609.06906v1#S4.SS1), lines 403–430, uses posterior covariance and Brascamp–Lieb to obtain smoothing bounds. A local Sobolev producer alone proves neither Brascamp–Lieb nor the necessary global weighted operator/core extension. Both anchors were reread for this audit.

The PBPS reflected potential is Wref(y,z) = V((y+z)/2) + ‖z−y‖²/(8η). The SPHMC RGO potential is Wrgo(y,x) = V(x) + ‖x−y‖²/(2η). Under z = 2x−y, normalization contributes 2^d and the pulled-back Dirichlet energy contributes a factor 4. The present ordinary-volume argument is fibrewise for its actual W and does not identify these laws, operators, ε scales, or measurable fibre selectors.

## Pinned interfaces inspected

All Mathlib paths below are relative to `.lake/packages/mathlib/Mathlib/`. These are source-inspected APIs, not fresh elaboration evidence.

| Role | Actual interface and contract |
| --- | --- |
| Strictly enclosing K | `Topology/MetricSpace/Bounded.lean:105`, `Bornology.IsBounded.subset_ball_lt`: choose rIn > 0 with K ⊆ ball 0 rIn, then rOut > rIn. Compactness implies boundedness. |
| Outer unnormalized cutoff | `Analysis/Calculus/BumpFunction/Basic.lean`: `ContDiffBump.contDiff`, `hasCompactSupport`, `eventuallyEq_one_of_mem_ball` (169); finite-dimensional bump instances via `BumpFunction/FiniteDimension.lean`. It is the bump itself, not its mass-normalized mollifier. |
| Local Laplacian equality | `Analysis/InnerProductSpace/Laplacian.lean:261`, `laplacian_congr_nhds`; at 382, `ContDiffAt.laplacian_CLM_comp_left` for **real-linear** continuous maps. |
| Real/imaginary tests | `Analysis/Complex/Basic.lean:150,173`, `Complex.reCLM`, `Complex.imCLM`, both ℂ →L[ℝ] ℝ. Compose with the smooth Schwartz function using their real CLM calculus. Optional `SchwartzMap.postcompCLM`/`postcompCLM_apply`, `Analysis/Distribution/SchwartzSpace/Basic.lean:1033,1053`, at scalar ℝ. `compCLM` is domain composition and is not this adapter. |
| Schwartz L² and actual Laplacian | `Analysis/Distribution/SchwartzSpace/Basic.lean:1316,1328`, `SchwartzMap.memLp`, `coeFn_toLp`; `SchwartzSpace/Deriv.lean:208`, `SchwartzMap.laplacian_apply`. Δψ remains a genuine Schwartz function. |
| Complex L² and L¹ products | `MeasureTheory/Function/LpSpace/Basic.lean:758`, `MemLp.ofReal`; actual `MemLp.toLp` and `coeFn_toLp`. `Function/L1Space/Integrable.lean:1085`, `MemLp.integrable_mul`, with `HolderTriple 2 2 1`. This proves the **bilinear** products integrable, without misusing a conjugated inner product. |
| Integrals commute with Re/Im | `MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean:164,168`, `integral_re`, `integral_im`, requiring integrability; `ContinuousLinearMap.integral_comp_comm` is the underlying interface. |
| Genuine Lp embedding | `Analysis/Distribution/TemperedDistribution.lean:160,169,195`, `MeasureTheory.Lp.toTemperedDistribution`, `_apply`, `toTemperedDistributionCLM`. Specify exponent `(2 : ℝ≥0∞)` and measure `volume` explicitly; the coercion cannot infer them from the output. Completeness is satisfied by codomain ℂ. |
| Measure growth | `Analysis/Distribution/TemperateGrowth.lean:442`, `IsAddHaarMeasure.instHasTemperateGrowth`, applies to finite-dimensional Lebesgue volume. Weighted Gibbs L² is not substituted for volume L². |
| Distribution Laplacian | `TemperedDistribution.lean:440`, `TemperedDistribution.laplacian_apply_apply`: (ΔT)(ψ) = T(Δψ). Each first derivative has a minus sign; the two derivatives in Δ give a plus sign. |
| Exact Fourier symbol | `Analysis/Distribution/FourierMultiplier.lean:208`, `TemperedDistribution.laplacian_eq_fourierMultiplierCLM`: ΔT = −(2π)² · FM(‖ξ‖²)T. Constant/sum/scalar multiplier APIs are at 156/180/173; TD `smulLeftCLM_add` is at `TemperedDistribution.lean:277`. Polynomial symbols have temperate growth. |
| Actual Sobolev witness | `Analysis/Distribution/Sobolev.lean:71,149`, `besselPotential`, `MemSobolev`. At 153/316, `memSobolev_zero_iff`, `MemSobolev.lineDerivOp` support later derivative extraction. `MemSobolev.laplacian` is forward regularity, not a converse. |

The existing `HasCompactSupport.toSchwartzMap` requires C∞ and only embeds an admissible compact smooth function. It does not extend a PDE to all Schwartz tests; the outer-cutoff argument below supplies that extension. Similarly, Schwartz density in Lp does not supply H² or weighted graph/core density.

## Proposed proof, at most seven steps

1. **Retain the actual compact output.** Take the above v/Gχ/Fχ from the single actual u. Use their already derived global `MemLp ... 2 volume` and supports ⊆ compact K. Do not make a local-L²-to-global or weighted-to-volume jump. This next interface need not require that v belongs to the original weighted closed-gradient domain.
2. **Construct one outer bump.** Enclose K strictly inside an inner ball and take an unnormalized `ContDiffBump` θ with larger outer radius. For every x ∈ K, θ = 1 in a neighborhood of x by `eventuallyEq_one_of_mem_ball`. This uses finite-dimensional real Hilbert structure and compactness, and works also in dimension zero. No nontrivial-space or unit-vector premise is needed.
3. **Actually extend the tests.** Given arbitrary ψ : 𝓢(E,ℂ), use φre = θ·Re ψ and φim = θ·Im ψ as real compact C² tests. On a neighborhood of each x ∈ K they equal Re ψ and Im ψ. Laplacian locality plus `ContDiffAt.laplacian_CLM_comp_left` derives Δφre = Re(Δψ), Δφim = Im(Δψ) there. Outside K, v and Fχ are zero. Thus each original real PDE yields the corresponding Re/Im equality for ψ. No Schwartz-test equation is assumed and no expanding-cutoff limit is necessary.
4. **Justify the complex integral equality.** Prove L¹ of (ofReal v)·Δψ and (ofReal Fχ)·ψ using `MemLp.ofReal`, Schwartz L² and `MemLp.integrable_mul`. Only then apply `integral_re`/`integral_im` and `Complex.ext` to combine Step 3:
   \[
   \int (v(x):\mathbb C)\Delta\psi(x)\,dx
     =\int(F_\chi(x):\mathbb C)\psi(x)\,dx.
   \]
   Handle multiplication order by commutativity. There is **no complex conjugation** in this equation.
5. **Build and identify the actual distributions.** Let vC and FC be the actual complex volume-L² classes of the pointwise functions. Set T = LpTD(vC), S = LpTD(FC). Use their volume-AE `toLp` representatives, `toTemperedDistribution_apply` and `laplacian_apply_apply` to prove ΔT = S by extensionality on all complex Schwartz tests. The pairing is ∫ψ(x)·vC(x) dx. A Schwartz-only integration-by-parts theorem cannot be applied directly to the rough vC.
6. **Produce `MemSobolev 2 2` with the correct symbol.** Prove the specialized algebraic identity
   \[
   B_2T=T-(2\pi)^{-2}\Delta T.
   \]
   Expand the order-2 Bessel symbol to 1+‖ξ‖², use constant/addition multiplier linearity and the exact Fourier Laplacian identity. Record real a = (2π)⁻², a's cast to ℂ and cancellation using 2π ≠ 0. The actual class vC − (a:ℂ)·FC then witnesses `MemSobolev 2 2 T` by complex linearity of LpTD. No inverse-symbol regularity or assumed H² is required. The bounded search found these ingredients, not a ready named specialized reverse-Poisson leaf.
7. **Keep representative extraction separate.** A later application of `MemSobolev.lineDerivOp` twice followed by `memSobolev_zero_iff` provides complex L² candidates for every mixed directional second derivative. Taking real parts, proving their actual compact-real-test identities, assembling a finite-basis Hessian and restricting to a neighborhood where χ=1 are distinct remaining adapters. No actual real mixed-second representative producer, original weighted H²/core, global tail estimate, or smooth Bochner extension is claimed here.

## Edge cases and acceptance boundary

E carries a finite-dimensional real inner-product structure, measurable/Borel structure and its ordinary Lebesgue volume. Complex codomain ℂ has coherent real and complex scalar structures and is complete. Re/Im calculus uses ℝ-linear maps; TD/Sobolev linearity uses ℂ-linear maps. Explicit scalar/exponent/measure types avoid mixing these interfaces.

For dimension zero, the orthonormal basis is empty, both ordinary and distribution Laplacians are zero, and B₂ = I. ΔT = S then forces S = 0 as a distribution. The bump construction still uses positive radii around the singleton space; the argument must not divide by dimension or choose a unit vector. Actual volume remains a genuine measure in this case, not an artificial atom inserted to obtain a graph.

The smallest missing producer is the compact C² real-test to all-complex-Schwartz extension in Steps 2–5, followed by the algebraic B₂ identity and actual L² witness in Step 6. These are suggested dependency-ready interfaces with this real consumer, not new SAUs or formal DAG nodes. If implementation fails, distinguish cutoff locality, real/complex Laplacian compatibility, actual AE Lp representatives, bilinear L¹, or Fourier-symbol/cast elaboration. Do not repair the target by assuming Schwartz validity or final H².

Current PROVED_LOCAL localization still awaits its independent source/exact admission. The proposed next edge supplies no measurable fibrewise solution selector, local-to-global weighted H², same-operator core, Poincaré/BL, PBPS hypocoercivity, SPHMC history/query-cost guarantee, or either complete main result/composition. No completion credit or lifecycle transition follows from this audit.
