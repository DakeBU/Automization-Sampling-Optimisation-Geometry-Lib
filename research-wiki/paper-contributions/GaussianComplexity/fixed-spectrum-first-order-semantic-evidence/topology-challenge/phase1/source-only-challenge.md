# Fixed-spectrum first-order packet: independent source-only topology and binder challenge

Phase: **1 — frozen before disclosure of any proposed Source Proof Graph, candidate statement, Statement Seal, Lean interface, API, or proof**.

Role: independent pre-proof topology/binder challenger. This is a source reading and adversarial dependency specification, not a mathematical implementation, approval of a producer, or approval of a consumer. No source-VERIFIED, admission, or lifecycle claim is made.

## Pinned input and scope

The only mathematical input read was the local original HTML of *On Complexity of Gaussian Sampling*, arXiv:2610.20492v1, at `.astis/huanjian-resume-20261103/2610.20492v1.html`. Its actual bytes were checked: **951991 bytes**, SHA-256 **6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915**.

Read in full: §2; all of §4, including §4.1/Eq. (11), Remark 4.2, Lemmas 4.3–4.6, the parameter use sites in §4.3, and the failure boundaries in §4.4; all of Appendix C.4 (`A3.SS4`). Also read the introductory oracle paragraph `S1.p2`, the informal theorem `S1.Thmtheorem2`, Remark 1.3, and the original bibliography entries [9] and [22]. The Appendix C.1–C.3 proofs and external [22] were not opened. They are not silently certified by the §4 statement-level reading.

Procedural instructions read: `AGENTS.md`, `.agents/skills/astis-source-dependency-audit/SKILL.md`, `docs/proof-digestion-protocol.md`, `docs/evidence-routed-memory-protocol.md`, `docs/theorem-publication-protocol.md`, `docs/contributor-codex-contract.md`, and `research-wiki/paper-contributions/README.md`. No candidate, existing Source Proof Graph, implementation Lean, API inventory, proof, earlier private audit, source correspondence, or registry was opened. A file-name inventory incidentally listed other historical audit directories; none of their contents were read. Parent messages before freezing conveyed the task boundary and acknowledged the already independently found Eq. (1) anchor; no candidate signature or graph was supplied.

The attached raw HTML excerpts are byte-exact source slices, identified by original element IDs and offsets in `raw-excerpts.json`. Readable text is mechanically extracted from the HTML's math `alttext` and prose; it does not replace the raw HTML.

## Independently fixed source meaning

### 1. Global oracle model and the literal first-order formula

In §2 the ambient class is

\[
\mathcal A_{d,\kappa}=\{A\in\mathbb R^{d\times d}:A=A^\top,\ I_d\preceq A\preceq\kappa I_d\},\quad d\ge1,\ \kappa\ge1.
\]

For an input in this class, the centered potential is **literally** \(f_A(x)=\tfrac12x^\top A x\), and the target is \(N(0,A^{-1})\). Eq. (1), `S2.E1`, explicitly writes

\[
\operatorname{FO}_A(x):=(f_A(x),\nabla f_A(x))=(\tfrac12x^\top A x,Ax).
\]

This is not merely an inference from C.4: the gradient component \(\nabla f_A(x)=Ax\) occurs literally in Eq. (1). Immediately following it, `S2.SS0.SSS0.Px1.p2.1` explicitly argues exact value-and-gradient, gradient-only, and matrix–vector query equivalence: projection obtains \(Ax\) from a first-order reply; the same exact vector gives the scalar \(\tfrac12\langle x,Ax\rangle\).

The local source equality must still be interpreted by actual calculus in a formal system. A definition named “gradient” whose body is \(Ax\), or a pair defined directly as \((\tfrac12x^\top Ax,Ax)\), does not by its name establish that the second component is the gradient of the first. A genuine `HasGradientAt`/Fréchet-gradient existence conclusion is a legitimate semantics expansion of Eq. (1), to be proved. It is not an additional permissible public hypothesis. The same applies to project-owned `Prop` bundles containing that conclusion.

### 2. Fixed-spectrum local domain and full orthogonal group

§4.1 starts with **\(d\ge2,\kappa\ge2\)**. With \(1\le i\le d\), Eq. (11) fixes

\[
\theta_i=\frac{(i-1/2)\pi}{d},\qquad
\lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_i,\qquad
\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_d),\qquad A=O\Lambda O^\top.
\]

Here the spectrum is deterministic and can be public; the eigenbasis is unknown. `S4.SS1.p1.2` draws \(O\) Haar from the **full** orthogonal group independently of the algorithm's seed. In contrast, Lemma 4.6 is explicitly **for every \(O\in O(d)\)**. §2 defines the full group by \(O^\top O=I\) and mentions both determinant components. A pointwise local algebra/calculus theorem cannot be weakened silently to Haar-almost-every \(O\), restricted to \(SO(d)\), or burdened with random-seed/independence hypotheses merely because the lower-bound experiment later randomizes \(O\).

The finite Euclidean carrier, matrix dimensions, transpose, inner product, and conversion between source indexing \(1,\ldots,d\) and a zero-based finite carrier are meaning-carrying typing data. In zero-based notation, the angle is \((i+1/2)\pi/d\), not \((i-1/2)\pi/d\). A candidate must expose the actual reindexing; names and dimensions do not settle it.

### 3. What C.4 literally says, and what it leaves as expansion

All of C.4 was read, including its final normalizer paragraph. Its substantive units are:

1. `A3.SS4.p1.1`: \(0<\theta_i<\pi\), then \(-1<\cos\theta_i<1\), hence \(1<\lambda_i<\kappa\); orthogonal conjugation yields \(I\preceq A\preceq\kappa I\).
2. `A3.SS4.p2.1`: \(V_A(x)=\tfrac12x^\top A x\) is \(C^\infty\), with **literal Hessian formula** \(\nabla^2 V_A(x)=A\); therefore it is 1-strongly convex and \(\kappa\)-smooth. Also \(V_A(0)=0\) and \(V_A(x)\ge\tfrac12\|x\|^2>0\) for \(x\ne0\), so zero is the unique minimizer.
3. `A3.SS4.p3.1`, `A3.Ex160`, `A3.SS4.p3.2`: the target is \(N(0,A^{-1})\); Gaussian integration gives \(Z_A=(2\pi)^{d/2}(\det A)^{-1/2}=(2\pi)^{d/2}(\det\Lambda)^{-1/2}\); it is independent of \(O\) and known when the spectrum is public.

C.4 does **not** literally display \(\nabla V_A=Ax\); Eq. (1) does. Replacing the global literal Eq. (1) anchor by “inferred from C.4” loses source information. Conversely, treating the exact formal gradient predicate, Fréchet derivative representation, continuity witnesses, or Lean coercions as literal source syntax overstates what the paper writes. The faithful classification is: Eq. (1) is the direct source formula; the formal operator/existence interpretation is an obligation; the quadratic calculus proof is an elementary expansion.

No first-order identity needs a Gaussian integral, determinant identity, public normalizer, target moment, Krylov representation, or concentration theorem. Those branches must remain visible where used, but cannot be mandatory parents of the first-order producer simply because they share C.4.

### 4. Same-rotation affine comparison

Remark 4.2 states, with **the same rotation \(O\)**,

\[
A_\kappa=(\kappa-1)A_2-(\kappa-2)I_d.
\]

It explicitly says one matrix–vector reply for either matrix determines the corresponding reply for the other. Forward and reverse reply maps are elementary expansions of that literal statement; the reverse uses \(\kappa-1\ne0\), discharged by the local \(\kappa\ge2\). “Same spectrum shape” does not replace “same \(O\)”. The statement compares coupled matrices at the same dimension and grid. It does not allow two independent rotations or tell an algorithm the hidden rotation.

This affine comparison can be an optional route for oracle transfer. It is not necessary to prove the same-matrix first-order formula. The paragraph about the later cosine test refers to Lemmas 4.4 and 4.5 and explains the \(\sqrt\kappa\) factor; it is downstream lower-bound motivation, not a prerequisite for exact reply conversion.

## Binder and dependency classification fixed before any candidate

| Prospective input/fact | Classification and source boundary |
|---|---|
| Local \(d\ge2,\kappa\ge2\) | SOURCE for the §4.1 fixed-spectrum domain. Global §2 uses \(d\ge1,\kappa\ge1\); do not silently identify these domains. |
| \(O\in O(d)\) | SOURCE in the local hard-family/Lemma 4.6 setting; all determinant components. |
| \(x\in\mathbb R^d\) arbitrary | TYPING and source quantification in Eq. (1). No norm, support, genericity, or almost-sure restriction. |
| \(\theta,\lambda,\Lambda,A,f,V\) bodies | Literal source definitions; source reindexing and all coercions need audit. |
| Symmetry of \(A\), \(\nabla V=Ax\), derivative existence, smoothness | Proof ingredients/conclusions when \(A=O\Lambda O^\top\) and \(V\) are already defined. A local target may not assume them as a convenience. |
| Spectral bounds, positivity, invertibility, determinant positivity | Derived in the appropriate branch. They are not extra free binders of the specialized hard-family first-order theorem. |
| \(V(0)=0\), known unique minimizer | Derived from the fixed centered literal potential; not a premise one must supply to prove its gradient. |
| Public spectrum/known \(Z_A\) | Explicit hard-family information model or downstream conclusion; not needed for same-matrix reply reconstruction. |
| Haar law/seed independence | STANDING for the randomized lower-bound experiment; not a hypothesis of deterministic local reply algebra/calculus. |
| Fixed-budget Borel algorithm model | STANDING for query-complexity transport; unnecessary to state a local vector/pair equality. |
| \(q\ge0,2q+1<d\), \(\tau\le1/2\), Gaussian starting vectors | Specific hypotheses of the Krylov/test route; not first-order producer inputs. |
| \(\delta\in(0,1)\), \(d\ge d_0(\delta)\), \(\kappa\le d^{1-\delta}\), \(0<\varepsilon\le1/10\) | SOURCE for Theorem 4.1, not for Eq. (11), Lemma 4.6, C.4, or the pointwise first-order formula. |
| A bundled “admissibility/regularity/oracle correctness” premise containing a desired conclusion | EXCESS unless each field independently matches the exact source interface; existence of an upstream producer does not legalize adding its conclusion to the public target. |

This table does not preapprove an unseen candidate signature. A generalization can be mathematically true but needs to be identified as such rather than falsely presented as the literal local source domain.

## Minimal closure shapes and AND/OR challenges

The following is an adversarial closure specification, not a replacement full coverage table or an approval of any graph.

**P1: actual first-order calculus producer.** Literal quadratic potential + the symmetry supplied by its matrix construction + a real quadratic-calculus argument support the gradient formula/existence. The global Eq. (1) provides the direct source-facing formula anchor. Orthogonality is part of the local domain, but mere symmetry already suffices for this calculus step. Spectral positivity is unnecessary for this step. If a route chooses to instantiate the global class theorem instead, it must actually discharge membership (including symmetry) inside the proof.

**C1: same-matrix first-order response consumer.** The actual calculus producer and the literal potential/first-order pair definition support the exact response pair. A direct route from an independently proved general centered-quadratic first-order theorem is also sufficient. These are alternative ways to discharge the same obligation; they are not a false AND demanding two different derivations. An implementation which only expands a pair already defined as \((\tfrac12x^\top Ax,Ax)\) has not consumed the calculus producer unless it also connects that pair to the actual value/gradient semantics.

**C2: exact oracle simulation/complexity consumer.** FO-to-matvec is projection; matvec-to-FO uses the public query point and its exact response to compute the dot product and pair. A claim about equal query complexity additionally needs the algorithm simulations to preserve Borel adaptivity, seed independence, output law, and the deterministic cap. Those simulation obligations do not become assumptions about an individual input matrix. A local pair identity alone is not the whole algorithmic theorem.

**C3: affine cross-\(\kappa\) comparison.** Eq. (11) at \(\kappa\) and at 2 **with the same \(O\)** gives Remark 4.2's affine relation. Exact arithmetic gives the two reply conversions; nonzero \(\kappa-1\) is discharged locally. First-order transfer can compose this with C2. C3 is optional for C1/C2 on a fixed matrix.

**Separate branches in C.4.** The trigonometric grid and orthogonality yield admissibility. Quadratic Hessian plus the spectral bounds yield strong convexity and smoothness; the coercive lower bound and value at zero yield unique minimizer. Positive-definite Gaussian integration and determinant invariance yield the normalizer; fixed \(\Lambda\) yields its independence of \(O\). Do not flatten these separate conclusions into one AND which is then inherited by every consumer of “C.4”.

**Optional inferred routes.** A route deriving the gradient from a constant Hessian and a base-point gradient must expose its own integration/base-point obligations; a direct differentiation route need not also depend on them. Remark 4.2 transfer and direct same-matrix recovery are different purposes and neither is a hidden necessary parent of the other. Alternative sufficient routes remain OR-routes. A source graph should distinguish literal author statements from elementary expansions and from any omitted bridge, and should record exact consumer use sites rather than only producer locations.

## Adversarial checks reserved for phase 2

| ID | Challenge and fail witness/risk |
|---|---|
| TC01 | **Eq. (1) anchor retained.** Reject coverage which describes the whole first-order formula as only inferred from C.4 or omits `S2.E1`; distinguish formula from formal calculus existence elaboration. |
| TC02 | **True gradient semantics.** Expand every project-owned potential, oracle, and gradient definition. A value-only definition named `gradient`, or a conclusion already inside an input record, cannot certify differentiation. |
| TC03 | **Symmetry discharge.** For a general nonsymmetric matrix \(B\), the quadratic gradient is \(\tfrac12(B+B^\top)x\), not \(Bx\). This prevents dropping the actual symmetry connection while reusing Eq. (1). For \(A=O\Lambda O^\top\), prove the connection internally. |
| TC04 | **Same \(O\).** At \(d=2,\kappa=3\), use \(O_\kappa=I\) and the coordinate-swap rotation for \(A_2\). The two grid eigenvalues are distinct; the affine RHS has the diagonal order reversed and is not \(A_\kappa\). A graph that forgets the coupling binder admits this counterexample. |
| TC05 | **Full group and total vector domain.** Test determinant \(-1\) rotations and \(x=0\). There is no det\(+1\), nonzero-vector, generic-position, or Haar-a.s. restriction on the local identities. |
| TC06 | **Centered value normalization.** For \(W(x)=\tfrac12x^\top Ax+c\), \(\nabla W=Ax\) still holds but an \(Ax\) reply cannot reveal an unknown \(c\). The literal zero-offset potential matters for exact value reconstruction. A normalized negative log density adds \(\log Z_A\); equality of gradients is insufficient for equality of FO scalar components. Public known shifts permit a separately explained simulator, not silent literal equality. |
| TC07 | **Local versus main parameters.** No \(\delta,\varepsilon,d_0,q,\tau\) premise is needed for the local producer/response consumer. Conversely, a local algebra/calculus result does not establish Theorem 4.1 or its parameter range. |
| TC08 | **Fixed cap versus expectation.** A claim preserving only expected cost does not match §2's fixed query budget. Conversely, do not apply the fixed-cap lower bound directly to an unbounded stopping time with a small expectation. A truncation argument would be a new explicit route with its own error accounting. |
| TC09 | **Exact versus finite precision.** Both recoveries and the affine inverse use exact arithmetic. The paper provides no finite-precision reply/rounding model here. Rounding can alter values; no bit complexity, stability, or rounded-oracle equivalence follows. |
| TC10 | **Public information versus mathematical binder.** Writing \(O\) as a theorem parameter must not reveal it to the algorithm. If \(O\) and \(\Lambda\) are public, a sampler can form \(O\Lambda^{-1/2}g\) with zero matrix queries; this illustrates why “unknown eigenbasis” is an information boundary. The algorithm quantifier must not become \(\forall O\ \exists\mathrm{Alg}_O\). |
| TC11 | **No gratuitous AND parents.** Remove the normalizer, determinant, public-spectrum, target-moment, Krylov, and concentration branches from the proposed first-order closure in turn. They should not be necessary to the actual pointwise calculus/response argument. If claimed essential, demand the exact use site. |
| TC12 | **Index and parameter endpoints.** Test \(i=1,d\) against \(0<\theta_i<\pi\) after any reindexing. At \(\kappa=1\), strict \(1<\lambda_i<\kappa\) and the affine inverse fail; the local source domain \(\kappa\ge2\) avoids both. Do not justify an off-domain fallback body by having a restricted theorem. |
| TC13 | **Literal definition on the public carrier.** A piecewise zero/default potential, oracle, matrix, or selected object outside the source domain is not approved merely because the intended theorem later assumes admissibility. Check total body semantics or an explicitly restricted carrier. |
| TC14 | **Actual producer-to-consumer use.** The candidate consumer must connect the exact producer's calculus conclusion to the actual response semantics. An import, declaration-name scan, source citation, or an unused producer does not make a mathematical dependency. |
| TC15 | **No overextension through §4.4.** The test's limitations apply to this proof method. They neither refute stronger lower bounds for the family nor establish accuracy-dependent or all-condition-number bounds. Local first-order facts do not remove the uniform-Krylov obstruction. |

TC03/TC04/TC06/TC10 are mathematical counterexample **designs for mutated statements**, not refutations of an unseen candidate. No candidate has been provided.

## Accuracy, query, and failure-boundary firewall

`S2.SS0.SSS0.Px2.p1.1` requires queries/stopping/output to be Borel functions of independent private randomness and previous responses. A fixed query budget bounds **every admissible input and every seed realization**. `S2.SS0.SSS0.Px4.p1.2` emphasizes that these are deterministic per-run caps, **not expected query bounds**. The output TV guarantee averages over the seed but is uniform in the input. These quantifiers are separate from the Haar experiment used in §4.

The only expected-query comparison found is Remark 1.3's literature comparison to [9], concerning a warm-start strongly log-concave upper bound. It is not a definition of the present \(Q_G\). A raw text search found no “finite precision”, “finite-precision”, “roundoff”, “round-off”, or “bit complexity” expression; that absence is a diagnostic, not a theorem about every possible numerical interpretation. Here “precision matrix” means inverse covariance, not arithmetic precision.

Theorem 4.1 has fixed \(\delta\in(0,1)\), \(d\ge d_0(\delta)\), \(2\le\kappa\le d^{1-\delta}\), and \(0<\varepsilon\le1/10\). It gives \(Q_G\ge(\delta/256)\sqrt\kappa\log d\). The theorem does not grow as \(\varepsilon\to0\). In §4.3, the uniform accuracy premise and admissibility permit evaluation at every hard-family input; Lemmas 4.3/4.4 control algorithmic output and Lemma 4.5 controls target samples. The proof then averages per-input TV inequalities over the independent Haar input. Those uses are downstream of the local oracle/calculus facts.

§4.4 explicitly limits this uniform-Krylov test: once \((q+1)^2\ge d\), the enlarged Krylov space is all of \(\mathbb R^d\) a.s.; a cosine-coordinate direction gives a normalized quadratic statistic at least \(1/\sqrt2\), obstructing the required small uniform threshold. The accuracy discussion combines \(c/\sqrt d\le a<|\mu_n|/M\le e^{-2(2q+1)/\sqrt\kappa}\), forcing \(q=O(\sqrt\kappa\log d)\) independently of \(\varepsilon\). Remark 4.8 says these are limitations of the proof; stronger bounds for the same fixed-spectrum family remain open. Their role in this packet is to prevent overclaiming the reach of the exact first-order edge.

## Phase-1 disposition

Source-only cognition, raw excerpts, and challenge IDs are frozen. No proposed node, edge, declaration, source seal, or proof has yet been inspected or accepted. Phase 2 must inspect the exact producer **and the actual consumer**, preserve this frozen record, and issue any correction or additional finding as a successor overlay rather than editing phase 1.
