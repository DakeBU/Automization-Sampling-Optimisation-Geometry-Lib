# Independent source-first notebook, phase 1

Role: independent pre-proof topology/binder/definition challenger. This notebook was written before reading ROOT's statement seal, P/T signatures, any existing Lean, lessons, old reviews, or source graphs. No proof search, API search, network access, proving, or subagent delegation was performed. Writes are confined to this agent's raw-material directory.

Read policy: repository AGENTS.md, docs/proof-digestion-protocol.md, docs/evidence-routed-memory-protocol.md. The binder bins are SOURCE, STANDING, TYPING, RULED, EXCESS; proof ingredients are dependency edges. Pre-proof approval does not mean Lean proof acceptance, publication, or purification.

Pinned original sources:

- Gaussian HTML `.astis/huanjian-handoff-20261019/2610.20492v1.html`, SHA256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
- Tropp PDF `.astis/semantic-neutral-20261113/bernstein_raw_intake_74ab/Tro11-User-Friendly-preprint.pdf`, SHA256 `f4c3cff8661011395e793972a1f8d9a199fae4ca0fd098535d7a42166cf8fc86`. This is independently selected external infrastructure, not a citation supplied by the Gaussian paper.

Reading range: complete Gaussian Appendix C.2 (Ex85–132, including C.5, C.6, and the final Lemma 4.4 consumer); original Lemma 4.4 assumptions; Tropp 2.2–2.3, Lemma 6.7 printed pp25–26. The directly referenced I+A<=exp(A) display 2.3 and expectation-order display 2.13 were also read in the surrounding raw PDF text. Tropp's subsequent Theorem 6.1 proof was read only to delimit downstream material.

## Independent mathematical inventory and intended boundaries

Tropp 6.7 is a generic **single-matrix**, dimension-free MGF statement: X is a random self-adjoint square matrix, EX=0 and lambda_max(X)<=1 almost surely; for every theta>0, E exp(theta X) <= exp((exp(theta)-theta-1) E(X^2)). The output retains the actual second moment, not an arbitrary variance proxy. It has no sum, independence, tail threshold, probability event, dimension prefactor, or variance cap. Replacing lambda_max<=1 by a two-sided norm hypothesis silently strengthens the source. A real symmetric specialization is a declared narrower carrier choice, not an exact complex-matrix generalization.

Tropp 2.2 supplies a global regularity convention and omitted almost-sure qualifiers. A concrete formal statement needs enough explicit measurability/integrability to make these exact expectations meaningful, but the convention must not become permission to add any convenient theorem conclusion as a premise. In particular all positive theta are in scope. One-sided spectral boundedness does not bound the negative tail and is not by itself a finite-second-moment assumption. Any concrete standing assumption must identify the necessary expectations, not assume the desired MGF inequality.

Tropp 2.3 defines matrix functions spectrally using a unitary eigenbasis. Matrix exp is not entrywise scalar exp. Its transfer rule applies scalar inequalities on an interval containing the actual eigenvalues. In 6.7 the interval is (-infinity,1], so negative eigenvalues of arbitrary magnitude must remain covered. The smooth scalar f has the literal removable value theta^2/2 at x=0; deleting this branch or assigning zero changes the source. The last step uses I+A<=exp(A), not operator monotonicity of matrix exp (the surrounding text explicitly warns that exp is not operator monotone).

Gaussian C.2 starts with r=q+1 and n=2q+1; each gamma_i is an independent N(0,I_r) vector. The actual law is unconditional Gaussian, not the Gaussian law conditioned on the truncation event. The source constructs the indicator-truncated matrix Y_i at Ex107, takes its actual expectation at Ex108–110, and centers by the actual expectation before applying concentration.

Immediate local formulas and obligations:

- Ex85, Ex102: deterministic t_i=(1,sqrt(2)cos theta_i,...,sqrt(2)cos(q theta_i)), theta_i=(i-1/2)pi/d, and ||t_i||²<=2r.
- Paragraph p10.1: L=2r+3log(1000d), R_i=||gamma_i||². Ex104–106 control the truncation probability and tail bias; they are not needed just to formulate or establish the MGF of the already-truncated single summand.
- Ex107: Y_i=d^-1 (gamma_i gamma_i^T tensor t_i t_i^T) 1_{R_i<=L}. Equality at R_i=L is included in the indicator.
- Ex108–109: EY_i=(a/d)(I_r tensor t_i t_i^T), a=(1/r)E[R_i 1_{R_i<=L}], 0<=a<=1. This is actual expectation under the unchanged Gaussian law. The common scalar a is independent of i.
- Ex110: summed unweighted and weighted expectations. These use C.5 identities; they are needed for later identification of the weighted total, not for centering each single summand, which is definitionally Y_i-EY_i.
- p13.1 and Ex111–112: Z_i=Y_i-EY_i, ||Y_i||<=2rL/d, ||EY_i||<=2r/d, hence ||Z_i||<=R_* with R_*=2r(L+1)/d.
- p13.3: the **same two-sided norm bound** holds for cos(n theta_i) Z_i because |cos|<=1. This is indispensable if the weight can be negative. A one-sided cap for Z_i alone cannot be multiplied by a negative cosine.
- The normalized actual consumer is X_i=R_*^-1 cos(n theta_i) Z_i. Positivity and nonzeroness of R_* must be derived on the source domain before division. Its actual second moment is E[(R_*^-1 cos(n theta_i)Z_i)^2]; retaining this is distinct from replacing it with a closed variance bound.
- Ex113–114: fourth Gaussian moments and squared Kronecker/outer-product formula. Ex115–117: dropping a positive semidefinite indicator and using C.5 controls the sum of EY_i².
- Ex118–119: centering variance identity and v_*=2r(r+2)/d.
- Ex120: cosine-square factor in the actual second moment, then a semidefinite upper bound. This is not permission to remove the square of the cosine from an equality.
- p15.1, Ex121, p15.2: independent centered self-adjoint sequences feed the two-sided matrix Bernstein sum tail. This is strictly downstream of one-summand MGF; independence and v_* are not prerequisites for a single-matrix MGF.

All q>=0 are part of Lemma 4.4. In particular q=0 gives r=1 and n=1, and the nonconstant cosine-coordinate range is empty; it must not be excluded by an accidental q>0 assumption. The source arithmetic premise 2q+1<d gives d>=2 and 2r<=d. It also makes the displayed L and R_* positive. No tau<=1/2 premise is needed for the normalized one-summand MGF; that premise is used only by the final Krylov-space ratio step.

## Actual downstream consumer map (not target completion claims)

The chain after Ex121 is substantive and must not disappear from full-section coverage:

1. Ex122–123 select z and Delta and verify the exponent inequality.
2. p16.3 and Ex124 apply individual failure bounds then a union bound over the weighted and unweighted sums.
3. p17.1 and Ex125 use the truncation event and actual mean identities to relate the original Gram matrices to centered sums. This equality is asserted **on the truncation event**, not unconditionally.
4. p17.2 and Ex126 intersect the truncation event with both concentration events and account for 0.995.
5. p18.1, Ex127–128 and p18.2 compare Delta+(1-a) with tau using hq, r=q+1, absolute constants, and a sufficiently large C.
6. p19.1–19.4 and Ex129–132 use C.6 plus range(B)=K_q and tau<=1/2, on one common event, to obtain simultaneous control for all u and probability >=0.99.

These are true later consumers. They must be explicitly excluded as downstream from a P/T-only audit; a P/T seal cannot claim C.6, Ex121, or Lemma4.4 is proved. Conversely a whole-C.2 graph cannot mark them covered merely by counting numbered displays.

## Independent topology challenges frozen for phase 3

- Check every actual consumer edge and conjunction/alternative route; an imported module cannot justify a source edge.
- The Gaussian author's proof cites unnamed two-sided bounded matrix Bernstein, not Tropp 6.7. A Tropp MGF insertion is an explicitly chosen external route supporting that step; provenance must say so.
- Single-summand generic MGF and Gaussian application require self-adjointness, actual mean zero, one-sided normalized cap and adequate real integrability; the Gaussian cap route requires a signed/two-sided control because cosine changes sign.
- Actual expectation centering plus Bochner linearity requires discharged integrability, not just syntactic subtraction from an arbitrary proxy mean.
- MGF finite/integrable for each theta>0 and second-moment integrability are separate obligations from any total variance estimate. A graph edge from Ex119 to P would conflate them.
- For the chosen normalized source consumer, q=0, the endpoint indicator <=, all theta>0 and the actual unconditioned Gaussian law must survive all adapters.
- Spectral transfer, congruence, expectation-order, and I+A<=exp(A) have distinct roles. The last step must not be a false use of exponential order preservation.

Disposition at phase 1: SOURCE INVENTORY FROZEN; no P/T statement or source graph has yet been reviewed. All dependency candidates above are source-derived, not implementation-derived.
