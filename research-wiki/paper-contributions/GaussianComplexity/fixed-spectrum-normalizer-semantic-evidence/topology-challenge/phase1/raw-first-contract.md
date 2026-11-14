# Independent raw-first normalizer contract — phase 1

Reviewer: `/root/norm_topology_570830`. Freeze time: 2026-11-08 05:54:58 UTC.
This is an independently derived source contract, not acceptance of a candidate,
graph, implementation, source fidelity, or proof. Those gates remain pending.

The only mathematical source is Zhou and Suzuki, *On Complexity of Gaussian
Sampling*, arXiv 2610.20492v1, the exact local HTML with SHA-256
`6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.
The raw excerpt files are byte-for-byte substrings; their offsets and digests
are in the manifest. No source normalization was used for the freeze.

## Seven semantic slots

1. **Objects.** The literal cosine grid is
   \(\theta_i=(i-\tfrac12)\pi/d\),
   \(\lambda_i=(\kappa+1)/2+(\kappa-1)\cos\theta_i/2\),
   \(\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_d)\), and
   \(A=O\Lambda O^\top\). The potential is
   \(f_A(x)=V_A(x)=x^\top Ax/2\), and the actual target is
   \(\pi_A=N(0,A^{-1})\). The selected object is its unnormalized Gaussian
   mass \(Z_A\), not the reciprocal density prefactor. Source anchors:
   `S4.E11`, `S4.SS1.p1.2`, `S2.SS0.SSS0.Px1.p1.2`, `A3.SS4.p3.1`.

2. **Domains.** Locally the hard family assumes integer \(d\ge2\) and real
   \(\kappa\ge2\), with indices \(i=1,\ldots,d\), real matrices, and
   \(x\in\mathbb R^d\). The orthogonal group is the full group
   \(O(d)=\{O:O^\top O=I_d\}\), including determinants \(+1\) and \(-1\).
   Section 2 gives these components Haar masses \(1/2\). No special-orthogonal
   restriction is permitted. The intended integral runs over all of
   \(\mathbb R^d\) with ordinary Euclidean Lebesgue volume. That base measure
   and the integral formula are implicit Gaussian conventions rather than an
   explicitly displayed definition in this source slice.

3. **Quantifiers.** For every such \(d,\kappa\), construct that grid and
   diagonal matrix; for every \(O\in O(d)\), use the literal conjugate \(A\).
   The value does not depend on \(O\). The family is sampled with Haar \(O\)
   in `S4.SS1.p1.2`, but the selected deterministic equality is pointwise for
   every \(O\), not merely almost surely. A Haar integral, averaging over
   private randomness, or conditioning on one determinant sign changes the
   object. The integration variable \(x\) is bound inside the integral.

4. **Assumptions.** The source-local numerical restrictions and orthogonality
   are the substantive premises. Source-implicit typing is finite-dimensional
   real Euclidean space and a finite real \(\kappa\). Spectral positivity,
   determinant positivity, symmetry/positive definiteness of the literal
   conjugate, measurability, integrability and positive finite mass must be
   established dependencies when needed; they are not extra public premises.
   No generic positivity, integrability witness, Gaussian integration formula,
   determinant identity, or previously proved theorem may be smuggled through
   a bundled public assumption. `A3.SS4.p1.1` explicitly derives
   \(0<\theta_i<\pi\), \(-1<\cos\theta_i<1\), and
   \(1<\lambda_i<\kappa\), then admissibility. The named Lemma 4.6 itself
   states only \(I_d\preceq A\preceq\kappa I_d\).

5. **Conclusion.** `A3.Ex160` explicitly states
   \[
   Z_A=(2\pi)^{d/2}(\det A)^{-1/2}
      =(2\pi)^{d/2}(\det\Lambda)^{-1/2}.
   \]
   The following paragraph explicitly states independence from \(O\) and
   knowledge whenever the spectrum is public. The source-implicit integral
   interpretation is
   \[
   Z_A=\int_{\mathbb R^d}\exp(-x^\top Ax/2)\,dx.
   \]
   Positivity and finiteness of this actual integral are implicit analytic
   obligations of that interpretation, not separately written source claims.
   The product form replacing \(\det\Lambda\) by
   \(\prod_{i=1}^d\lambda_i\) is an inferred finite determinant identity,
   not a displayed formula in C.4. An algebraic number called a normalizer,
   without a theorem connecting it to the actual integral, would leave this
   selected component open.

6. **Scopes and senses.** The exponent \(d/2\) means real division after
   interpreting \(d\) as a real number, including odd dimensions. The factor
   \(a^{-1/2}\) for positive determinant \(a\) is the reciprocal of the
   positive square root. This is not integer division or a complex branch.
   The integrand is the ordinary scalar real exponential, with the factor
   \(1/2\) in the energy. The unweighted mass is neither a standard-Gaussian
   expectation nor a Haar/sign-weighted average. The potential's zero at its
   minimizer fixes its additive normalization. The abbreviation \(V_A\) in
   C.4 and \(f_A\) in Section 2/4.1 denote the same literal quadratic.

7. **Constant dependencies.** There is no unspecified constant in the selected
   exact formula. The value depends only on \(d,\kappa\) through the fixed
   grid, not \(O\), its sign, any algorithm, seed, query budget, accuracy, or
   theorem-level \(\delta\). Theorem 4.1 separately fixes
   \(\delta\in(0,1)\), chooses \(d_0(\delta)\), and restricts
   \(d\ge d_0(\delta)\), \(2\le\kappa\le d^{1-\delta}\),
   \(0<\varepsilon\le1/10\). Those lower-bound ranges are not premises of
   C.4's local Gaussian normalizer formula.

## Independent binder and definition challenges to retain

The eventual signature must recursively expand every project-owned predicate,
structure and typeclass. Classify source-local \(d\ge2\), \(\kappa\ge2\)
and \(O\in O(d)\) as SOURCE or explicitly audited STANDING context; classify
carrier and coordinate encodings as TYPING. A conjunction containing any
undischarged derived fact is EXCESS. A producer theorem does not change this.

The grid, conjugate, quadratic energy, exponential integrand and normalizing
integral have literal semantics. No `if known then choose else zero` or other
off-source fallback is permitted. No quotient/representative choice is needed
for these finite matrices or this scalar mass. An abstract target law or a
characterized normalizer would need its real existence/uniqueness and a
separate characterization theorem; merely assigning the source's closed-form
value does not show it normalizes the actual exponential density. A formal
integral's library totalization is not permission to omit integrability.

## Raw source coverage universe

The complete leaf inventory and dispositions are recorded in
`coverage-universe.json`. The selected root is the conjunction of the actual
unweighted integral/value bridge and rotation-independent source value at
`A3.Ex160`/`A3.SS4.p3.2`. Every paragraph of C.4 is accounted for, including
the Hessian/convexity/minimizer paragraph even where excluded from this
component. No numbered-statement-only completeness claim is allowed.

The source says only “Gaussian integration gives” the display: its analytic
integration argument is omitted. The graph must retain that missing background
bridge explicitly, rather than inventing a detailed author proof. The
determinant conjugation and diagonal-product steps are implicit algebraic
bridges. Repeated display/source statements are provenance, not necessarily
separate required AND premises.

The direct source consumers are `A3.SS4.p1.1` for grid bounds and spectral
admissibility, `A3.SS4.p3.1`/`A3.Ex160` for Gaussian integration and determinant
replacement, and `A3.SS4.p3.2` for independence/public-spectrum knowledge.
The graph must attach inputs to those use sites, discharge their conditional
premises, and trace the selected root through them. A formula-only determinant
route cannot close the actual-integral root. An alternative analytic derivation
may be an explicit OR route; it must not be flattened into a false AND with
other sufficient routes or mislabeled as the author's displayed proof.

## Explicit boundary

No algorithm construction, adaptive-query reduction, block Krylov containment,
concentration, target cosine statistic, TV separation, oracle-cost equality,
query-budget bound, Theorem 4.1 closure, or stronger accuracy/condition-number
extension is included. Lemmas 4.3–4.5, Lemma 4.7, Remark 4.8 and Section 4.4's
estimates are boundary context only. The cited [22, §9.2] is construction
provenance, not a necessary Gaussian-integration premise; no external theorem
from that reference was read or used. The whole paper and the full Lemma 4.6
exposition are not claimed completed by this component.

Exposure before this freeze: the designated raw paper, requested instruction
files, and the semantic-roundtrip skill solely for the canonical seven-slot
names. No candidate/seal/signature/audit/definition proposal, sourcegraph
extractor output or rationale, target or ancestor implementation Lean, old
verdict, graph, publication, site, frontier, or ledger was opened. A raw-paper
search for normalizer wording also displayed short unrelated source passages
from Appendix B and C.2/C.3; these are recorded in the exposure ledger and are
not used as premises. No proof, API retrieval, build or control-plane change
was performed.
