# Phase 1 initial cognition — raw paper only

This document records the mathematical reading before exposure to any new
sealed interface, packet, implementation, prior private proof capsule, root
preseal audit, or reuse/exposure rationale. It is not a source-VERIFIED verdict.
The exact source is arXiv:2610.20492v1, *On Complexity of Gaussian Sampling*,
the local 951991-byte HTML with SHA256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

## Objects and quantifiers recovered from the paper

The hard family is introduced in §4.1 under **local** assumptions: integer
`d >= 2`, real `kappa >= 2`, and indices `i = 1,...,d`. Equation (11) defines
`theta_i=(i-1/2)pi/d`, `lambda_i=(kappa+1)/2 + (kappa-1)cos(theta_i)/2`, and
`Lambda=diag(lambda_1,...,lambda_d)`. The index convention is implicit in the
display's list of d entries and must survive a zero-based implementation.
For a **real** orthogonal matrix `O` with `O^T O = I_d`, set
`A=O Lambda O^T`. Lemma 4.6 is pointwise for **every** `O in O(d)`, including
both determinant components. Haar randomness and its independence from the
algorithm's private seed describe the hard-instance distribution; they are
not assumptions needed to prove the pointwise geometry.

The quadratic is `f_A(x)=x^T A x/2` in §2 and §4.1. Appendix C.4 calls the
same literal function `V_A`. Its argument is a real Euclidean d-vector.
The source precision class requires both symmetry and
`I_d <= A <= kappa I_d` in the Loewner order. Lemma 4.6 only displays the
inequalities, so symmetry must be recovered from the conjugation formula
when its introductory claim of class membership is used.

## Author's geometric/calculus route

1. The grid gives `0 < theta_i < pi`.
2. Therefore `-1 < cos(theta_i) < 1`, hence `1 < lambda_i < kappa`.
3. Orthogonal conjugation transfers the diagonal bounds to
   `I_d <= A <= kappa I_d` (Lemma 4.6).
4. The quadratic is `C^infinity` with Hessian `A`. Appendix C.4 states these
   facts directly and supplies no derivative calculation or external citation.
5. The Hessian bounds imply 1-strong convexity and kappa-smoothness.
6. Independently of the Hessian route, the lower quadratic-form bound gives
   `V_A(0)=0` and `V_A(x)>=||x||^2/2>0` for `x != 0`.
   This proves that zero is the unique **global** minimizer.

The source omits the square-orthogonal right-inverse/norm argument, expansion
of the conjugated quadratic form, matrix symmetry calculation, polynomial
regularity/derivative calculations, and the precise Hessian-to-convexity and
smoothness criteria. These are visible `SOURCE_GAP` completion obligations,
not new public premises and not a diagnosis that the source claim is false.
No citation supplies these steps in C.4.

Euclidean meanings needed to avoid convention drift are:
`grad f_A(x)=Ax`, `D f_A(x)[h]=<Ax,h>`, `D^2 f_A(x)[h,k]=<Ah,k>`;
`f_A(y)>=f_A(x)+<Ax,y-x>+||y-x||^2/2`; and
`||Ax-Ay||<=kappa||x-y||`. The source does not define the latter two terms
formally. The proposed meanings are the usual Euclidean conventions that
the Hessian sentence in C.4 requires; a later interface audit must compare
the exact norms, factors, derivative carriers, and quantifier scopes.

## Fixed-input actual-oracle bridge

Section 2 equation (1) literally specifies
`FO_A : R^d -> R x R^d`, `FO_A(x)=(x^T A x/2, Ax)`.
For the hard family, the admissibility/symmetry facts justify identifying
this pair with the value and Euclidean gradient of the actual quadratic.
The source says adaptive queries, stopping decisions, and the output are
Borel functions of seed and past responses, and later refers to the output
law for each fixed input. It does **not** state a separate theorem that
`x -> FO_A(x)` is continuous or Borel.

For fixed `A`, the literal oracle map is polynomial, hence continuous and
Borel for the standard Euclidean Borel structures. This is an omitted
source-model bridge, recorded separately from the author's stated calculus
claims. It does not require joint measurability in `O`, a measurable choice
of eigenbasis, Haar integration, an arbitrary externally supplied response,
or a new hypothesis asserting that the oracle is measurable. Continuity of
the quadratic and of the linear gradient suffices as one route; direct
coordinate polynomial continuity is another sufficient route. They are OR
options, not cumulative analytic assumptions. Neither option is credited to
an explicit source proof, and no Lean route has been inspected.

The full induction showing that an arbitrary bounded adaptive transcript
and stopped output are measurable is a further model-construction task.
It is not proved by merely identifying a Borel oracle and is outside this
bounded geometry/oracle-map audit.

## Scope boundaries recovered before interface exposure

Theorem 4.1 separately quantifies `delta in (0,1)`, sufficiently large
`d >= d_0(delta)`, `2 <= kappa <= d^(1-delta)`, and
`0 < epsilon <= 1/10`, with a query lower bound. Those restrictions do not
replace §4.1's local geometry conditions. The §2 general class is introduced
for `d >= 1, kappa >= 1`; that broader ambient class does not silently
broaden this hard-family source contract either.

The Gaussian target and public fixed spectrum are definition/context. The
normalizer display in C.4 uses Gaussian integration and determinant
invariance; it is an independent analytic branch, excluded from geometry
closure. No normalizer theorem is a prerequisite for the derivative,
convexity, minimizer, or fixed-input polynomial-oracle facts.

Remark 4.2's affine comparison to kappa=2, its query simulation, oscillatory
test, Lemmas 4.4/4.5, and its lower-bound explanation are excluded. Citation
[22, §9.2] is construction provenance, not an invoked background theorem in
the C.4 geometric proof. Its bibliography entry is preserved from this same
paper; the cited preprint was not retrieved.

TV inequalities, uniform accuracy, finite deterministic query caps, expected
query costs, and the main lower-bound result remain outside this result.
The caps and seed independence are retained only as the exact §2 model
boundary. A statement about the actual oracle's measurability alone does
not prove query equivalence, adaptive output measurability, an accuracy
guarantee, or any lower bound.

## Independence and review limits

The allowed reads were repository instructions, the source-dependency-audit
skill, and the pinned raw HTML/extracts. A broad initial filename search
returned unrelated artifact names (no file contents); no mathematical
conclusion or graph edge uses those names. The system Python's optional bs4
import failed, so the extractor uses only the standard-library HTML parser.
No source, dependency, or model retrieval, network/browser/build, lifecycle
API, ledger mutation, Lean construction, or additional agent was used.

Phase 1 records my reconstruction and its exhaustive inventory. It does not
approve its own coverage or certify the source graph: the separate topology
challenger and later exact-interface review remain necessary.
