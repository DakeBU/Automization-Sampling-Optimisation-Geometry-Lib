# Independent mathematics review73

Reviewer: /root/header_math72. Checked parent: bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19. The reviewed candidate is the entire 178-line ActualHarmonicFlow.lean module, exact RAW/LF SHA256 506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c, not a committed SCI73 theorem. Root remains the sole canonical proving writer.

Verdict: ACCEPTED_MATHEMATICS_ONLY, conditional on the recorded fresh whole-module Lean terminal EXIT0. No mathematical statement or proof repair is required. All nine literal clauses and the full proof were reviewed. The current six original callers are retained; no caller is asked to provide one of the conclusions or a new analytic regularity fact. This is not source-fidelity admission, strict blind decoding, VERIFIED, publication acceptance or whole-paper completion.

## Exact mathematical reduction

Fix η>0, r=√η, y,xRef∈E, g=gradient V(xRef), c=y−ηg. For initial state z=(q₀,p₀), put w₀=(q₀−c)/r. The literal module defines

w(t)=cos(t) w₀+sin(t) p₀,
p(t)=−sin(t) w₀+cos(t) p₀,
q(t)=c+r w(t).

This is precisely the module's Φ, since η=r² and r>0. E is a finite-dimensional real inner product space; no nontriviality or positive dimension is assumed. y,xRef and η are fixed when forming the time group or differentiating time. Joint continuity/measurability additionally quantifies both y and xRef, the real time t and the entire initial pair z. The theorem does not assert continuity in η or a flow in which xRef changes with time.

## All nine clauses and their proofs

1. Joint continuity (statement36–37, proof101–110). Original hV:C² implies C¹. The imported ASTIS continuous_gradient_of_contDiff_one proves continuity of the actual Mathlib gradient, via the continuous inverse Riesz map applied to continuous fderiv. Thus c(y,xRef) is jointly continuous. Scalar sine/cosine, projections, vector addition and scalar multiplication give joint continuity of Φ on (E×E)×(ℝ×(E×E)). Division is only by the fixed positive r; no moving-parameter singularity is hidden. Proof fun_prop combines these actual continuous expressions rather than accepting a caller continuity certificate.

2. Joint Borel measurability (statement38–39, assembly173). The given MeasurableSpace E/BorelSpace E on finite-dimensional real E and their finite products are compatible with the topology; the proven joint continuous map is measurable. This includes y,xRef,t,z simultaneously, not only each fixed-parameter trajectory. No kernel, conditional law, measure preservation or stochastic process is claimed.

3. Time zero (statement40, proof111–115). cos0=1 and sin0=0 give q(0)=c+(q₀−c)=q₀ and p(0)=p₀. The vector module calculation is direct; it does not assume a flow axiom.

4. Group (statement41–42, proof116–121). In normalized coordinates M(t)=[[cos t,sin t],[-sin t,cos t]]. Trigonometric addition gives M(s)M(t)=M(s+t). The same c is reused in both compositions, so translating back proves the exact stated order Φ(s+t,z)=Φ(s,Φ(t,z)). The Lean proof expands both coordinates, uses sin/cos addition, and clears the nonzero constant r. There is no hidden change of y or xRef, nor an omitted root relation or extra semigroup premise.

5. Both inverses (statement43–45, proof122–127). Substitute (s,t)=(−t,t) and (t,−t) in the proved group law, then time zero. The proof supplies both left and right compositions, even for negative or zero times. It does not infer a global measure-preserving inverse.

6. Both actual ODEs (statement46–51, proof128–145). Differentiating the explicit normalized expressions gives w′=p and p′=−w, hence q′=r p and p′=−(q−c)/r. Since c=y−ηg and η=r²,

−r⁻¹(q−y)−r g=−r⁻¹(q−c)+(η/r−r)g=−r⁻¹(q−c).

This checks both negative signs and both √η factors exactly. In particular the gradient is evaluated at the frozen xRef, not at the moving q(t). The Lean proof uses actual HasDerivAt sine/cosine rules and congr_deriv to identify the computed derivatives, then hr0 and hr2. It neither assumes the desired ODE nor replaces derivatives by pointwise formal differentiation. No global Lipschitz theorem or additional derivative bound is needed for this explicit fixed-center solution.

7. Nonnegative energy (statement52, proof146–148). The literal H=(η⁻¹‖q−c‖²+‖p‖²)/2 is a SUM, with η⁻¹>0. Both squared norms are nonnegative and the denominator is positive. The result is nonnegativity, so zero energy is included.

8. Conserved weighted SUM energy (statement53–54, proof149–165). H=(‖w‖²+‖p‖²)/2. Expanding the two normalized squared norms gives

‖cos t·w₀+sin t·p₀‖²
  =cos²t‖w₀‖²+2 cos t sin t⟨w₀,p₀⟩+sin²t‖p₀‖²,
‖−sin t·w₀+cos t·p₀‖²
  =sin²t‖w₀‖²−2 sin t cos t⟨w₀,p₀⟩+cos²t‖p₀‖².

Cross terms cancel and sin²t+cos²t=1. The proof performs this exact inner-product norm expansion, rewrites η=r² and clears only nonzero r before using the trigonometric identity. It does not replace H by a difference of squares, an unweighted product norm or an assumed invariant. The positivity/normalization survives arbitrary dimension and all real times.

9. π endpoint (statement55–56, proof166–172). cosπ=−1 and sinπ=0 yield q(π)=c−(q₀−c)=2c−q₀ and p(π)=−p₀. Both components and the actual center are present. The proof reduces these exact trigonometric values and vector identities. This is a deterministic coordinate endpoint, not an admitted conditional half-turn operator or probability kernel.

The proof-local c/Φ/H and the change target reproduce the literal private Prop. The final tuple173 contains precisely all nine proven clauses. The 178-line exhaustive, nonoverlapping audit partition also covers imports, caller/type prefixes, local definitions, square-root facts, gradient/center continuity, namespace closures and the unique exact #print axioms command; there are no unreviewed mathematical lines.

## Binders, boundaries and edge cases

The private and public callers are exactly hα,hαβ,hV,hH,hη,hβη. Their content is α>0, α≤β, V∈C², the original Hessian lower/upper bound, η>0 and βη≤1. The proof uses hV for gradient continuity and hη for r>0 and η=r². The other original standing conditions remain explicit, even though the deterministic harmonic algebra does not need their quantitative force. It would be inappropriate to turn the derived continuity, time group, ODE, energy or endpoint into new caller assumptions.

Finite dimensionality supplies completeness for the gradient API and the usual finite-product Borel compatibility; no new CompleteSpace, second-countability, differentiability, measurability or nonzero-energy premise is passed to the caller. No third/higher derivative, boundary decay, integrability or domination assumption is needed for these deterministic pointwise formulas. The reviewed imported gradient API was pinned and read at its exact type/proof; the pinned Mathlib revision remains db584cd6d46c92f209a44c0f1c829460d327499d, with Lean4.33.0.

Rank zero is valid: all vectors are zero, so every coordinate, derivative, energy and endpoint identity reduces correctly; the alpha/Hessian conditions cause no contradiction since all v are zero. At αη=1, η remains strictly positive, and no formula divides by 1−αη or 1−βη. All nine clauses remain valid, including βη=1. Zero energy is valid: η>0 implies H=0 iff q₀=c and p₀=0; then Φ(t,z)=z and both ODE right sides are zero for every t. The proof never divides by H, a norm or a velocity. η=0 is outside the original caller, correctly.

The exact sealed header is restored by removing only the four proof tactic imports from the compiled module's prefix. The expanded frozen header's entire let-bound literal body matches the private Prop. The deterministic module imports no corrector72 result. No stronger statement about invariant measures, bounce/rates, stochastic construction, nonexplosion, Markov/reversal, actual conditional H/kernel, rρ/B27/B28, main/error/cap/query-cost or actual-input composition follows from this review. Reader/source admission, Exposition Seal, PURIFIED, live/main, full-paper and Goal completion remain separate and open. Because this reviewer has seen the named statement, implementation and header adoptions, it cannot act as strict blind decoder73.

## Evidence and independence

Finite original inputs are preserved as exact RAW snapshots with both RAW and bytewise CRLF→LF-only pins. No recursive history or large encoded source packet was copied. Fresh source elaboration runs the real pinned lean.exe on the exact whole canonical candidate, writes an olean only under independent-math73/output, and uses the original fixed Lake search roots. Its actual foreground PID, terminal EXIT and exact axiom output are recorded separately. The native fake-closure scanner strips Lean comments/strings and checks the entire module; mathematical review separately checks the literal definition and full proof.

There are no canonical, global-ledger, Git, Goal, source/publication/site writes and no VERIFIED transition. Bounded applicable independent-review/round-trip truth-boundary protocols were read; this task does not perform or impersonate their later blind/source review stages. Root's earlier compile/header receipts are input provenance, never substituted for this independent fresh check. All actual failures, if any, remain in the owned raw receipts and failure records. Wholelogical run hash removes ONLY the top-level run_sha256 and canonicalizes the entire remaining JSON with UTF8, sorted keys, ensure_ascii=False and comma/colon separators. Final lease is CLOSED_LAST; external verification afterwards is read-only.
