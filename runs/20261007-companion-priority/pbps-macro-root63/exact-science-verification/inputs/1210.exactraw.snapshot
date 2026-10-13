# Compact weak PDE to complex Schwartz and Sobolev: independent source preread

Date: 2026-10-06. Source/API actor: `phase_source_reviewer_20261005`.
Repository read baseline: `d0dfa1207402a5ac75423424994a743e51aa3d91`.
Pinned Lean: `leanprover/lean4:v4.33.0`; Mathlib: `db584cd6d46c92f209a44c0f1c829460d327499d`.
This is a dependency/source-contract note, not a theorem receipt, source verdict, SAU, independent verification or completion claim. No compiler was run.

## Original source boundary, reconstructed first

[PBPS, arXiv:2609.06905v1, Appendix C.1](https://arxiv.org/html/2609.06905v1#A3.SS1), HTML1197–1234 and1276–1310, begins with smooth compact observables and uses gradient density/closedness for extension. Its conditional Gibbs density, integration by parts and conditional Poincare are concrete analytic objects. The text does not state this Fourier/Schwartz/Sobolev producer as a numbered theorem. It is an explicitly authored analytic prerequisite for a possible rigorous domain route; it does not itself prove the source conditional Poincare or macroscopic extension.

[SPHMC, arXiv:2609.06906v1, Section4.1](https://arxiv.org/html/2609.06906v1#S4.SS1), HTML403–430, uses the actual unreflected RGO covariance identities and BL covariance upper bound; CR covariance lower is separate. Compact unweighted regularity does not prove BL, the required global weighted operator domain, or the complete smoothing theorem.

PBPS uses
\[
W_y^{\rm ref}(z)=V((y+z)/2)+\|z-y\|^2/(8\eta),
\]
while SPHMC RGO uses \(W_y^{\rm rgo}(x)=V(x)+\|x-y\|^2/(2\eta)\).
Under \(z=2x-y\), inverse Jacobian is \(2^{-d}\), reflected partition is \(2^d\) times the unreflected partition, reflected Hessian is quarter-scaled, and the RGO Dirichlet energy of a reflected observable's pullback is four times the reflected energy. Operator/resolvent/epsilon identification needs an actual measure/domain/scaling adapter. No such identity follows merely from similar potentials.

## Actual available input and exact proposed output

Use `LocalizedWeakResolvent.localized_weak_resolvent`, not a supplied localized PDE certificate. Its generic hypotheses are finite real Hilbert/Borel/full-space volume, W C1 with integrable exp(-W), and one actual closable partial gradient D with exact smooth compact gradient graph. The genuine source consumer `ConditionalLocalizedResolvent.conditional_localized_resolvent` produces D from actual C2 V, all-point/all-vector alpha/beta curvature, positive alpha<=beta, eta>0 and beta eta<=1, retaining true common kernels/disintegration/reflected density and positive partition.

For each epsilon>0 and forcing f in the original weighted L2 law, one u in the original closure domain serves all C2 compact cutoffs chi. With G=closureD(u), r=epsilon*u+inner(gradW,G)-f, the parent gives actual functions
\[
v=\chi u,\quad G_\chi=\chi G+u\nabla\chi,\quad
F_\chi=\chi r+2\langle\nabla\chi,G\rangle+u\Delta\chi,
\]
global volume L2 and support inclusions in K=tsupport chi, plus all C1 weak-gradient and C2 compact weak-PDE identities with both products L1. Standard quotient representatives are distinct from weighted L2 classes.

The next proposed output is, for the actual complex volume L2 classes Vc and Fc of ofReal(v) and ofReal(Fchi),
\[
\forall\psi\in\mathcal S(E,\mathbb C),\quad
\int \psi\,F_\chi\,dx=\int(\Delta\psi)\,v\,dx,
\qquad \Delta T_v=T_{F_\chi},\qquad
\mathrm{MemSobolev}\ 2\ 2\ T_v.
\]
All coefficients v/Fchi in these integrals are embedded in C. The TD pairing is complex **bilinear** integral psi times the embedded function, with no conjugation. Derivatives of complex test functions are real Frechet derivatives on E; Re/Im are real-linear CLMs, not complex-linear projections.

## Source-to-API route: seven steps maximum

1. **Consume the same solution.** Keep the parent D before epsilon/f, the same u before all C2 compact chi, all original properties and formula-defined cutoff functions. Obtain global *volume* L2/support from the actual parent. C2 chi need not be Schwartz or smooth. Do not assume a new solution, global weighted-to-volume implication or final Schwartz equation.
2. **Construct one outer plateau.** Enclose compact K strictly inside an inner ball and choose an ordinary unnormalized `ContDiffBump` theta in C-infinity compact, equal to1 on an open neighborhood of K. `Basic.lean:137,166,169` supplies the plateau, compact support and eventual equality; `FiniteDimension.lean:463` supplies the instance without Nontrivial. A normalized mollifier is not this plateau. The theta depends on chi/K, not on the arbitrary test or a replacement u.
3. **Extend real compact tests to every complex Schwartz test.** Apply the real C2 compact PDE to theta*Re(psi) and theta*Im(psi). Real-linear `Complex.reCLM`/`imCLM` and `ContDiffAt.laplacian_CLM_comp_left` commute projections and actual Laplacian. On K, local theta=1 makes the Laplacian agree with the original test; outside K both v and Fchi vanish. Prove every complex product L1 before combining real/imaginary integrals: Schwartz psi and Delta psi are global volume L2, so Holder2,2,1 applies. This fixed compact-support argument needs no expanding-cutoff tail limit or density-in-graph-norm assumption.
4. **Build the genuine complex L2 classes.** `MemLp.ofReal`, actual `MemLp.toLp` and `MemLp.coeFn_toLp` give Vc/Fc and their volume-a.e. representative identities. Keep these identities through every integral and quotient operation. Neither a weighted class nor an arbitrary pointwise nonsmooth function is silently embedded as an L2 TD.
5. **Prove the actual TD Laplacian.** Use `Lp.toTemperedDistribution`/`_apply`, volume's temperate-growth instance, Schwartz Laplacian evaluation and extensionality against every complex Schwartz test. `TemperedDistribution.laplacian_apply_apply` has positive sign for the second derivative. Derive Delta(Tv)=TFchi; supplying this equation as a new paper premise would omit the substantive test-extension edge.
6. **Use the correct Bessel normalization.** Pinned `besselPotential E C s` is multiplier `(1+norm(x)^2)^(s/2)`, not the convention I-Delta. `laplacian_eq_fourierMultiplierCLM` gives Delta T=-(2pi)^2 FM(norm^2)T. Specialize order2 and use constant/sum multipliers to derive
   \[
   B_2T=T-(2\pi)^{-2}\Delta T.
   \]
   The actual complex volume L2 class Vc-(2pi)^-2 Fc witnesses `MemSobolev 2 2 Tv` by its definition. This specialized algebraic identity still needs a compiled proof; API presence is not a new theorem certificate.
7. **Bind the actual consumer and stop at this boundary.** Apply the adapter to every parent cutoff for the same original u/G and D. Conditional order remains exists common R/S, forall y exists D_y, forall epsilon>0/f exists u, forall chi, forall Schwartz psi. No joint measurable y-dependent solution/class/cutoff selector is concluded. This packet may stop at the real parent properties, complex tested identity, actual TD Laplacian and MemSobolev conclusion.

## Pinned declarations independently inspected

Paths below are relative to `.lake/packages/mathlib/Mathlib/`.

| Contract | Exact inspected API |
|---|---|
| Actual complex embedding/quotient representatives | `MeasureTheory/Function/LpSpace/Basic.lean:758` MemLp.ofReal; :105–112 MemLp.toLp/coeFn_toLp |
| Legal Schwartz products | `Analysis/Distribution/SchwartzSpace/Basic.lean:1316` SchwartzMap.memLp; `MeasureTheory/Function/L1Space/Integrable.lean:1085` MemLp.integrable_mul with HolderTriple p q 1 |
| Real-linear projections/test Laplacian | `Analysis/Complex/Basic.lean:150,173,321` reCLM/imCLM/ofRealCLM; `Analysis/InnerProductSpace/Laplacian.lean:382` ContDiffAt.laplacian_CLM_comp_left |
| Actual TD pairing/Laplacian | `Analysis/Distribution/TemperedDistribution.lean:160–175,440` Lp.toTemperedDistribution, its integral evaluation and laplacian_apply_apply; `SchwartzSpace/Deriv.lean:208` actual test Laplacian |
| Fourier/Bessel/Sobolev | `Analysis/Distribution/FourierMultiplier.lean:156,180,208` constant/sum/Laplacian multipliers; `Sobolev.lean:71,149` besselPotential/MemSobolev |

## Missing boundaries and zero dimension

MemSobolev here is a Bessel-potential statement about the actual complex TD. It is not yet a published real mixed-second-derivative representative theorem for the original u. `MemSobolev.lineDerivOp` twice and `memSobolev_zero_iff` identify candidate L2 derivative classes, but realness, representatives, compact-test agreement, restriction where chi=1 and finite-basis Hessian reconstruction need explicit proofs. Do not assert them from the scalar Laplacian alone.

No localized membership in the original weighted D/closure domain, global operator core, graph/H2 smoothing density, global weighted Bochner or boundary/tail estimates, epsilon0, Poincare/BL, source main result or composition follows. Ordinary Lp Schwartz density does not fill those domain contracts.

Retain dimension zero: empty derivative basis gives Delta=0, frequency norm=0 gives B2=I, bump instances need no Nontrivial premise. The proposed adapter concerns actual canonical volume in a finite real Hilbert space, not arbitrary atomic/weighted measures. Generic C1 W/C2 chi and zero dimension are disclosed generalizations of the source Euclidean C2 setting.

## Evidence and exposure

Primary sections were reread before the current parent/API reads. This actor already read the full current localized producer and authored its source review; those current parent facts are available dependencies, not a verdict on any upcoming candidate. Earlier covariance-keyword/signature exposure from a bounded BL search and inherited task/status labels remain honestly disclosed. No root ignored prototype, upcoming candidate statement, decoder, math-review or source verdict was opened for this preread. The earlier independent `Weighted_local_H2_Fourier_dependency_audit.md` was used as an API plan only, then the named original Mathlib contracts were checked directly.

Current parent footprints, SHA256 raw / CRLF-to-LF:

- Shared localized module: `2e35799ed7d7beef354caa22e32d1a6e75d3bed9c50217eda599c8e6fd8b3114` / `5fb157f3bfd725cddd571178f52cd244b4949386a2db6dd6e41efbde835e7c8d`.
- Conditional localized module: `4351d551aca307ae01097405b3f5667906e72f792aa697a019c95ddd054b9431` / `1ffa8ec3ea09aa9f52c8b80b95df6e113e60f028a5ccf1c696c0eb727d7b4d35`.
- Earlier Fourier dependency plan: raw=LF `6320cd721a07a9eccf56495ac9c5c0acd0bebb61d439670b005e63b256466c6c`.

Only this preread file was written. No production, metadata, lifecycle, registry or current admission file was edited; no compiler session was started. Proposed route and unresolved adapters remain research evidence only.
