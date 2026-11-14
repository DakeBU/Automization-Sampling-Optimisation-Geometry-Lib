# Phase 1: source-only reconstruction (frozen before candidate exposure)

This document reconstructs the pinned raw source. It is neither a Lean audit nor a final fidelity verdict. No candidate proposition, declaration, implementation, decoder output, prior semantic decision, lesson, or publication packet was inspected. The run is candidate-blind, not cue-free: the assignment supplied source identity and anchors, and the required process instructions and runtime labels were visible. See `run_exposure_log.md`.

## Source and scope

Source: *On Complexity of Gaussian Sampling*, supplied arXiv identifier/version 2610.20492v1. Exact local input: `.astis/huanjian-resume-20261103/2610.20492v1.html`, 951991 bytes, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

Primary slice: Appendix C.4 (`A3.SS4`), the proof of Lemma 4.6 (`S4.Thmtheorem6`). Necessary standing inputs: Section 4.1 (`S4.SS1`), especially equation (11) (`S4.E11`), and Section 2 (`S2`). Neighboring Section 4.2 was read to distinguish sibling lemmas from prerequisites. A raw-link trace led to the actual downstream use at `S4.SS3.p2.1`; Section 4.3 was captured/read to identify that consumer's role. Section 4's introduction and Theorem 4.1 were captured for the parameter-scope distinction. Bibliography entry `bib.bib3` was captured only to identify the source's construction citation; its linked external material was not opened.

All raw excerpt byte ranges and raw/readable hashes are in `excerpt_index.json`. Readable files substitute each original math element's exact decoded `alttext` for its MathML rendering; raw excerpts remain the authority. Extracted ids are printed as `[[anchor]]`. No mathematical claim is derived from repository metadata.

## Exact objects and inherited hypotheses

1. Section 2 works in the real Euclidean space R^d with Euclidean norm, identity I_d, and Loewner order on symmetric real matrices: A ≼ B means B−A is positive semidefinite.
2. The model precision class is
   \[
   \mathcal A_{d,\kappa}=\{A\in\mathbb R^{d\times d}: A=A^\top,\ I_d\preceq A\preceq\kappa I_d\}.
   \]
   Section 2 assumes integer d≥1 and κ≥1. These bounds are normalized by rescaling. A is the **precision**, not the covariance. The target is π_A=N(0,A^{-1}). The potential is f_A(x)=x^T A x/2.
3. The hard family in Section 4.1 is more specifically fixed at integer d≥2 and real κ≥2. For i=1,…,d,
   \[
   \theta_i=\frac{(i-\tfrac12)\pi}{d},\qquad
   \lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_i,
   \qquad \Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_d).
   \]
   Thus Λ is a concrete deterministic cosine grid, not an arbitrary matrix whose required properties are merely assumed. These are Chebyshev nodes, not interval endpoints. The source uses indexing 1,…,d; any other indexing convention would need an explicit translation.
4. For O∈O(d)={O∈R^{d×d}:O^T O=I_d}, define A=OΛO^T. The hard experiment draws O with Haar probability independently of the algorithm's private randomness, but Lemma 4.6 and C.4 apply **for every** O in this group. No almost-sure qualification or positive determinant restriction appears. Both components of O(d) are allowed; Section 2 gives each component Haar mass 1/2 and defines the conditioned Haar laws μ_{n,b}. The conditioned laws are not used in C.4.
5. The spectrum is deterministic and may be supplied to the algorithm. The hidden component is the eigenbasis O. “May be supplied” does not make a randomness assumption into a theorem premise. It explains the strength of the lower-bound setup.

The quantifier order for the local result is: fix d≥2 and κ≥2; construct the specific θ_i, λ_i and Λ above; for **every** orthogonal O, set A=OΛO^T and obtain all the C.4 conclusions below. All x-based conclusions then hold for every x∈R^d (with x≠0 where strict positivity is asserted). There is no q, δ, ε, algorithm, seed, Gaussian auxiliary vector, Krylov membership condition, concentration event, or high-probability condition in this local statement.

## Displayed lemma and all additional local conclusions

The displayed Lemma 4.6 states only: for every O∈O(d), A=OΛO^T satisfies I_d ≼ A ≼ κI_d. Symmetry follows from the defined symmetric diagonal Λ and conjugation, so this puts A in the Section 2 class. C.4 additionally states the following substantive facts.

- For every i=1,…,d, 0<θ_i<π, −1<cos θ_i<1, and **1<λ_i<κ**. Consequently A is symmetric positive definite and invertible. The displayed admissibility bound uses weak Loewner inequalities; the proof supplies strictly interior eigenvalues. Neither 1 nor κ is asserted to be attained, and κ is an allowed upper spectral/condition parameter, not an assertion that the actual condition number equals κ.
- C.4 writes V_A(x)=x^T A x/2, the same quadratic denoted f_A in Section 2/4.1. It is C^∞, with Hessian ∇²V_A(x)=A for all x. Hence it is 1-strongly convex and κ-smooth in the Euclidean convention. In particular the standard strong-convexity inequality has coefficient 1/2 in its squared norm term; κ-smoothness is the Lipschitz gradient bound with constant κ. These are valid bounds, with no claim of optimal constants.
- V_A(0)=0 and V_A(x)≥||x||²/2>0 when x≠0. Thus 0 is its unique minimizer. There is no unknown translation/minimizer in this hard family.
- The associated target is N(0,A^{-1}). Its normalizing constant is
  \[
  Z_A=(2\pi)^{d/2}(\det A)^{-1/2}
      =(2\pi)^{d/2}(\det\Lambda)^{-1/2}.
  \]
  This is the Gaussian normalization for exp(−V_A) on R^d with the ordinary Lebesgue convention. The Gaussian-integration passage is the source's bridge to this convention; the source does not separately spell out a definition of Z_A in Section 2. Here det A=det Λ=∏_{i=1}^d λ_i>0, so the reciprocal square-root is the positive real one and Z_A is finite and positive. It is a normalization of the unnormalized density, not its reciprocal prefactor.
- Since Λ is fixed, Z_A is independent of O and known whenever the spectrum is public. It may still depend on d and κ through the grid. The source gives no numeric evaluation complexity, bit complexity, approximate integration algorithm, or additional oracle-query cost for computing this formula.

The pointwise geometry, the target covariance, and the normalizer must be kept as separate conclusions even though they share prerequisites. A claim of spectral admissibility alone does not textually include all of C.4's proof paragraphs.

## Author proof route, without implementation reconstruction

C.4 has one route, with three paragraphs and one displayed normalization formula.

1. Use the actual midpoint grid and i∈{1,…,d} to get 0<θ_i<π. Apply the strict cosine range on that open interval, then the positive affine coefficient (κ−1)/2 to get 1<λ_i<κ. Orthogonal conjugation transfers the diagonal spectral bounds to I_d≼A≼κI_d. This is the proof of the displayed Lemma 4.6.
2. Differentiate the quadratic with symmetric matrix A. Its derivatives are polynomial, Hessian is A, and the matrix bounds imply the convexity and smoothness assertions. Evaluate at zero and use the lower quadratic bound for x≠0 to establish uniqueness of the minimizer.
3. Apply Gaussian integration for a positive-definite precision matrix A. Use determinant invariance under orthogonal conjugation to replace det A by det Λ. Since Λ is fixed, independence from O and knowledge from a public spectrum follow.

This route does **not** invoke Lemmas 4.3, 4.4, or 4.5, their Krylov representation, cosine concentration, target moments, or their Appendix C.1–C.3 proofs. Sharing Section 4.2 or Appendix C is not a mathematical dependency. The `[22, Section 9.2]` construction citation in Section 4.1 is provenance for the family; the elementary C.4 argument as written does not import an unquoted result from that citation. The Section 4.2 paragraph heading “Admissibility and oracle equivalence” does not create an oracle-equivalence theorem inside C.4: the displayed lemma is spectral, and its proof contains the geometric/normalization assertions above. The actual exact oracle equivalence is stated and explained in Section 2.

The real downstream use is `S4.SS3.p2.1`: the proof of Theorem 4.1 supposes a uniform TV guarantee for every admissible A, then says that Lemma 4.6 makes the hard family admissible. This discharges membership in the quantifier range of that uniform guarantee for every rotated hard input. It is not an input assumption of Lemma 4.6. The downstream proof separately invokes Lemmas 4.3/4.4 for algorithmic outputs and Lemma 4.5 for target moments. Theorem 4.1's restrictions δ∈(0,1), d≥d_0(δ), 2≤κ≤d^{1−δ}, ε≤1/10, and its query cap are downstream restrictions, not inherited by C.4. C.4's normalizer and minimum assertions are not explicitly cited as ingredients in the Section 4.3 contradiction.

## Omitted standard background and semantic obligations

These bridges are implicit standard background, not new source premises. They are recorded as omitted-background nodes in `source_topology.json`; this records the source's level of detail and does not assert a source defect.

- Elementary index arithmetic yields 0<(i−1/2)/d<1; π>0 and the strict cosine range yield the angle/cosine bounds.
- A diagonal matrix with real entries in [1,κ] has the corresponding quadratic-form bounds. For square real O, O^T O=I implies OO^T=I, norm preservation and invertibility. Then x^T A x=(O^T x)^TΛ(O^T x); symmetry and positive definiteness follow. Strict positivity gives invertibility.
- Differentiation of a symmetric quadratic yields gradient Ax and Hessian A. Continuous/polynomial higher derivatives give C^∞; Hessian bounds give the usual Euclidean strong-convexity and gradient-Lipschitz conclusions. Strict positivity away from zero proves the argmin statement.
- The positive-definite Gaussian integral over Lebesgue measure is (2π)^{d/2}/sqrt(det A), with covariance A^{-1} after normalization. A change of coordinates by O has absolute Jacobian determinant 1. Determinant multiplication and (det O)^2=1 give det A=det Λ. These facts explain rather than add integrability, nonzero determinant, or positivity premises.
- Finite-dimensional polynomial operations are continuous and hence Borel. This supports the elementary fixed-input reply observation below, but is not a new theorem expressly stated in C.4.

There are no citations in C.4 itself. No external theorem source was consulted. The run does not claim any Mathlib/Lean availability, formal proof of these bridges, or exhaustive reconstruction of the rest of the paper.

## Exact first-order model and its measurable boundary

Section 2 defines, for fixed A∈𝒜_{d,κ} and x∈R^d,
\[
\operatorname{FO}_A(x)=\bigl(f_A(x),\nabla f_A(x)\bigr)
=\left(\tfrac12 x^T A x, Ax\right).
\]
The response is a scalar and a vector. A value-and-gradient response contains Ax. Given the query x and matrix-vector response y=Ax, the scalar value is reconstructed as ⟨x,y⟩/2. Hence the source states that **exact** value-and-gradient, gradient-only, and matrix-vector query complexities coincide on this centered quadratic class. The word exact matters: no statement about noisy, approximate, finite-precision, or value-only access follows here.

For each fixed admissible A, the map x↦Ax and the map x↦(x^T A x/2,Ax) are polynomial/continuous, hence Borel in the standard Euclidean Borel structures. The decoding map (x,y)↦(⟨x,y⟩/2,y) and projection of a reply onto its vector coordinate are also continuous/Borel. This is a source-derived elementary observation from the displayed formula, not an explicitly displayed C.4 conclusion. A fixed-input Borel reply statement, on its own, neither asserts a randomized algorithm nor proves any of the lower-bound probability statements.

Section 2 separately specifies the algorithm model:

- Internal randomness is independent of the input.
- Queries and stopping decisions are Borel functions of that randomness and previous oracle responses.
- The output may be any R^d-valued Borel function of the same information; it is not required to lie in the span of queries or replies.
- A fixed budget T is a cap for every admissible input and **every** realization of the randomness, rather than merely almost surely or in expectation.
- For a fixed input A, ρ_A^Alg is the output law including all the internal randomness. The TV requirement is uniform over A and applies after averaging over that randomness.
- Q_G(d,κ,ε) is the infimum of nonnegative integer caps T for which there exists an algorithm meeting sup_{A∈𝒜_{d,κ}} TV(ρ_A^Alg,π_A)≤ε, for 0<ε<1.

To lift reply formulas to an adaptive algorithm simulation one must compose the Borel policy/stopping/output maps through successive histories and preserve the same seed/input independence and per-run stopping cap. The displayed Section 2 equivalence explains the reply conversions and asserts the complexity equality; C.4 itself does not present this adaptive composition proof. A statement limited to fixed A and x should not silently acquire quantifiers over seeds, histories, algorithms, or random O. Conversely, fixed-input reply measurability should not be treated as an extra analytical premise of the hard-family admissibility result: it follows from the quadratic formula.

Separate again are joint measurability in a random input O, construction of an output probability law or kernel, independence/coupling extensions, Krylov representation almost surely, the ≥0.99 event, target Gaussian moment/variance bounds, averaged TV contradiction, or any query lower bound. These occur elsewhere or require additional composition/probability reasoning. No such conclusion is supplied merely by C.4, the deterministic normalizer formula, or fixed-input continuity. No expected-cost bound may replace the deterministic cap specified in Section 2.

## Seven-slot source baseline for a later authorized comparison

| Slot | Source baseline |
| --- | --- |
| Objects | Real Euclidean precision A=OΛO^T with literal cosine-grid Λ; quadratic potential f_A=V_A; centered Gaussian with covariance A^{-1}; its Gaussian normalizer. Exact first-order reply is a scalar/vector pair. |
| Domains | d integer ≥2 and κ real ≥2 for this hard family; i=1,…,d; O in full real O(d); x in all R^d. Broader Section 2 model allows d≥1,κ≥1. |
| Quantifiers | Fixed d,κ determine Λ; every O gives admissibility and all C.4 local conclusions; every x, and strict positivity for x≠0. No probabilistic exception. |
| Assumptions | Literal grid and orthogonality, with inherited d,κ bounds. Positivity, integrability, Hessian bounds, minimizer and determinant identities are proved consequences/background, not extra hypotheses. |
| Conclusions | Displayed Loewner bounds; strict eigenvalue bounds; C^∞ quadratic/Hessian; 1-strong convexity; κ-smoothness; unique minimizer zero; target covariance; normalizer formula, independence from O and knowledge from public spectrum. |
| Scopes/senses | Precision versus covariance; Euclidean norm and Loewner order; positive normalizing integral for exp(−V_A); deterministic pointwise family facts; exact access equivalence in Section 2; separate Borel algorithm and output-law model. |
| Constants | 1 and κ are normalized bounds, not attained extrema; Z_A depends on d,κ through fixed Λ but not O. No q,ε,δ or probability constants in C.4. Theorem 4.1's constants/restrictions belong to its downstream lower bound. |

No candidate meaning is inferred and no source-fidelity verdict is issued in this phase. Phase 2 requires explicit authorization and fresh disclosure of its exact inputs.
