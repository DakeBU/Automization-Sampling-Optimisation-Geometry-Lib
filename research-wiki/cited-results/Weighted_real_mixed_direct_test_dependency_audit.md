# Real mixed weak derivative via direct compact tests

Bounded independent mathematical/API audit, 2026-10-06, `picard_commit_verifier_20261005`.
Read base: `bfa789218dcfe274e65d99f6ac70b219ca411e21`.
Pinned Lean `leanprover/lean4:v4.33.0`; Mathlib `db584cd6d46c92f209a44c0f1c829460d327499d`.

**Verdict: mathematically viable shorter route, requiring a small real/complex mixed-test adapter.** This note is planning only: no compiler, Lean declaration, new SAU, source verdict, lifecycle transition or verification credit. The already mathematics-reviewed focused-PASS complex Sobolev candidate remains subject to its separate independent source/exact admission. Anonymous reconstructions/source verdicts, ignored root prototypes and the raw alternative route note were not read. Only this file was written.

## Exact input and notation boundary

Use the actual complex volume-L² class vC with vC = volume-a.e. ofReal(v), and `MemSobolev 2 2 (Lp.toTemperedDistribution vC)` constructed by `CompactWeakPoissonSobolev.compact_weak_poisson_sobolev`. For its actual source consumer, the accepted localized resolvent supplies the **same** original D, u, and G = D.closure u before every compact C² χ. Its actual localized functions are

\[
v=\chi u,\qquad G_\chi=\chi G+u\nabla\chi.
\]

The available compact-test identity is, for all real compact C¹ ψ and a ∈ E,

\[
\int\psi\langle G_\chi,a\rangle\,dx
  =-\int v D_a\psi\,dx,
\]

with both integrabilities already proved. When the proposed route writes G, it must mean **Gχ**, the weak gradient of v. Using the original G for χu would omit u∇χ and generally be false. Generic notation below writes g for this actual weak gradient. Its source instantiation is g = Gχ, not a supplied derivative certificate.

All L² classes and integrals in this adapter concern **ordinary volume**. The original u is a weighted L² representative, but the preceding actual compact localization derives global volume L² of v/g. No arbitrary weighted class is silently made tempered. The source law remains the reflected Gibbs fibre; no RGO law/operator/ε identification is made.

The proposed bounded conclusion is: for every a,b ∈ E there exists an actual real volume-L² class h_ab such that for every real smooth compact φ,

\[
\int\varphi h_{ab}\,dx
 =\int vD_a(D_b\varphi)\,dx
 =-\int\langle g,a\rangle D_b\varphi\,dx.
\]

Both test products must be integrable. This is the weak derivative in direction b of the scalar weak-gradient component ⟨g,a⟩. It is not yet a classical Hessian, a simultaneously selected bilinear field or an original weighted operator-core theorem.

## Why the derivative order and sign are correct

Let T = LpTD(vC). Pinned `TemperedDistribution.lineDerivOp_apply_apply` defines

\[
(\partial_a T)(\psi)=T(-\partial_a\psi).
\]

Consequently

\[
(\partial_b(\partial_aT))(\psi)
 =T(\partial_a(\partial_b\psi)).
\]

The two minus signs cancel; the nesting on the test reverses the distribution nesting. Apply the actual first weak-gradient identity **directly** at ψ = D_bφ and direction a to obtain the final minus sign in the displayed conclusion. No mixed-derivative commutation or first-order TD equality is needed. If one instead constructs ∂a(∂bT), the matching direct test is D_aφ with direction b; silently mixing these two conventions would give the wrong component interface.

## Original pinned APIs inspected

Paths are relative to `.lake/packages/mathlib/Mathlib/`. This is source inspection, not elaboration evidence.

| Need | API and exact contract |
| --- | --- |
| Obtain actual complex mixed L² class | `Analysis/Distribution/Sobolev.lean:316`, `TemperedDistribution.MemSobolev.lineDerivOp`: arbitrary direction, s → s−1. Apply first a at s=2, then b at s=1. At 153, `memSobolev_zero_iff` gives an actual `Hab : Lp ℂ 2 volume` representing ∂b(∂aT). No final Hab certificate is assumed. |
| Distribution test sign/order | `Analysis/Distribution/TemperedDistribution.lean:367`, `lineDerivOp_apply_apply`; its argument is `−∂m ψ`, not a conjugate or an extra Fourier normalization. Schwartz linearity and TD linearity cancel the two negatives. |
| Genuine embedded smooth real test | `Analysis/Complex/Basic.lean:321`, `Complex.ofRealCLM : ℝ →L[ℝ] ℂ`; `Analysis/Distribution/SchwartzSpace/Basic.lean:555`, `HasCompactSupport.toSchwartzMap`, with actual C∞ and compactness. Compactness survives composition by the zero-preserving ofReal CLM. |
| Directional test evaluation | `Analysis/Distribution/SchwartzSpace/Deriv.lean:104`, `SchwartzMap.lineDerivOp_apply_eq_fderiv`, identifies the actual real Fréchet directional derivative. Use twice; do not use a Schwartz integration-by-parts theorem on the rough v. |
| D_bφ is legal compact C¹ | `Analysis/Calculus/ContDiff/Comp.lean:750`, `ContDiff.fderiv_right`, and at 804, `ContDiff.contDiff_fderiv_apply`, composed with x ↦ (x,b). `Analysis/Calculus/FDeriv/Const.lean:392`, `HasCompactSupport.fderiv_apply`, gives compact support with arbitrary b, including b=0. Taking C∞ φ is enough; the scalar derivative needs only C¹ for the parent identity. |
| Embed/test differentiation commutes with ofReal | `Analysis/Calculus/FDeriv/Linear.lean:57`, `ContinuousLinearMap.hasFDerivAt`, followed by the actual `HasFDerivAt.comp` chain rule and `.fderiv`. Apply ofReal once to φ and once to D_bφ. Explicit real-linear derivative composition gives D_a(D_b(ofReal φ)) = ofReal(D_a(D_bφ)); a small dedicated adapter remains to elaborate. |
| Bilinear L¹ pairing | `Analysis/Distribution/SchwartzSpace/Basic.lean:1316`, `SchwartzMap.memLp`; `MeasureTheory/Function/L1Space/Integrable.lean:1085`, `MemLp.integrable_mul` with HolderTriple 2 2 1. Use Lp.memLp of Hab/vC and actual smooth embedded φ and its mixed Schwartz derivative. Pairing is ∫ψ·Hab with no conjugation. |
| Actual Lp representatives and real projection | `MeasureTheory/Function/LpSpace/Basic.lean`, `MemLp.toLp`/`coeFn_toLp`; `LpSeminorm/Monotonicity.lean:242`, `MemLp.re`. Define h_ab as `((Lp.memLp Hab).re).toLp (fun x => (Hab x).re)` and retain its volume-AE equality. |
| Real integral transfer | `MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean:164`, `integral_re`, only after complex product integrability. At 169 in `TemperedDistribution.lean`, `Lp.toTemperedDistribution_apply` gives the actual bilinear integral. Use both vC's and h_ab's AE links explicitly. |

The Sobolev norm has the pinned Bessel normalization B₂ = I−(2π)⁻²Δ. Once that actual Sobolev membership is available, the distribution directional derivative is the physical derivative defined by the above test action. No extra (2π) factor belongs in the real weak-gradient identity; such factors arise only if this derivative is re-expressed as a Fourier multiplier.

## Bounded proof route, six steps

1. **Retain the actual input.** Use the same localized v/g from the same original D/u/χ, its all-compact-C¹ weak-gradient identity, and its actually produced vC/Sobolev membership. No first-order TD identity or all-Schwartz weak-gradient extension is added as a premise.
2. **Construct Hab.** Apply `MemSobolev.lineDerivOp` in direction a and then b, simplify 2−1=1 and 1−1=0, and destruct `memSobolev_zero_iff`. Keep the exact equality ∂b(∂a T)=LpTD(Hab). This constructs Hab from Sobolev regularity; it does not select real mixed derivatives in advance.
3. **Prepare genuine compact tests.** For real φ ∈ C∞c, construct φC = ofReal φ as an actual complex Schwartz map. Derive D_bφ ∈ C¹c using the pinned derivative regularity/support APIs. Prove the two-level ofReal differentiation identity with real CLM calculus. This is the smallest remaining API adapter, not a missing mathematical hypothesis.
4. **Evaluate the actual mixed TD.** Prove L¹ of φC·Hab and (∂a∂bφC)·vC by Holder. Evaluate the Hab identity at φC, cancel the two signs, and transfer vC =ae ofReal(v). After `integral_re`, obtain ∫φ Re(Hab)=∫v D_a(D_bφ), with the actual real-side integrabilities also available from the parent at D_bφ.
5. **Use the original weak-gradient output directly.** Apply it at ψ=D_bφ and direction a to obtain ∫v D_a(D_bφ)=−∫(g·a)D_bφ. This avoids the whole first-order TD equality route. Build h_ab through the genuine MemLp.re class and transfer its AE representative equality through the left integral. Either prove its L¹ product by Holder with real φ L² or by real projection of the already integrable complex product; do not split undefined integrals.
6. **Bind the actual source and stop at real weak coefficients.** Substitute g=Gχ for every existing χ after the same original u, preserving the source's common R/S, fixed D and quantifier order. The endpoint is ∀a,b ∃h_ab with all real smooth compact test identities. Any uniform/bilinear Hessian reconstruction, direction-independent selection, restriction χ=1 or quantitative estimate is a separate bounded conclusion requiring its own proof.

## Source boundary and remaining obligations

[PBPS v1, Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1) uses smooth compact observables and density/gradient closedness. The note supplies a route toward an omitted analytic domain prerequisite; it is not a printed mixed-derivative theorem or a proof of conditional Poincaré/macroscopic coercivity. [SPHMC v1, §4.1](https://arxiv.org/html/2609.06906v1#S4.SS1) uses a separate Brascamp–Lieb covariance upper bound. This real coefficient interface alone does not supply that inequality. Primary anchors/normalization remain those of the preceding independent source/API preread; no new source verdict is inferred here.

E is a finite real Hilbert space with Borel structure and canonical volume. In dimension zero a=b=0, directional operators and their test derivatives vanish. Sobolev-to-Lp still produces a representative and the displayed weak-test conclusion remains valid without choosing a unit vector or dividing by dimension. Proving h_ab =ae 0, uniqueness, or support by distribution injectivity/compact-test AE uniqueness is optional later work, not needed to obtain a real weak derivative. The route does not assume Hab is real or its imaginary part is zero.

It also does not establish that v lies in the original weighted closure domain, that h_ab has global weighted L², a same-operator smooth core, Bochner/density extension, measurable fibrewise/directional selectors, ε→0, BL/Poincaré, either complete sampling theorem or actual-input expected-cost composition. Reflected versus unreflected law/operator/Dirichlet scales remain distinct. No formal DAG edge results from this note.
