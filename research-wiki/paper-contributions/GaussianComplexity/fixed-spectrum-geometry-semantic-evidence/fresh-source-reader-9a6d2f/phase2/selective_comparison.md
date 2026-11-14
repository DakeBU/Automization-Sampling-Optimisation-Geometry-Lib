# Phase 2 selective anonymous comparison

## Bounded finding

The supplied anonymous proposition and its blind reconstruction preserve the **geometric paragraph of Appendix C.4**, `A3.SS4.p2.1`, for the literal hard input of Section 4.1/equation (11). No blocking semantic difference was found within that selected conjunction. This is a selective statement-meaning finding. It is not an equivalence claim to the whole of C.4, Lemma4.6's complete publication interface, Section2's oracle/algorithm model, or the paper's lower bound. The target module, proof, actual declaration binding, lessons, obligation metadata and previous semantic decisions remain unseen.

The comparison baseline was my independently frozen phase1 source reconstruction, manifest SHA-256 `aa9b3ffb40981e0d6d80d9c1ac8458a610c41bb7137e185a89baf6d9c25f81f1`. All28 phase1 payloads were rehashed before comparison and remain unchanged. The new selective packet is 15711 bytes, raw SHA-256 `66454bcce11cf77ab188da7cd77d7c9a943f05fbdf671559b147f730795d1ac9`. Its anonymous statement has UTF-8 SHA-256 `be1d161ba7bcd793361caac3ec131e76166116cd93b1636058b4f36195c7bb1d`. No source understanding was rewritten after anonymous disclosure.

## Seven semantic slots

| Slot | Frozen source and supplied formal meaning | Finding |
| --- | --- | --- |
| Objects | Source θ_j=(j−1/2)π/d, λ_j=(κ+1)/2+(κ−1)cosθ_j/2, Λ=diag(λ_j), A=OΛO^T and f_A=V_A=x^TAx/2. The formal lets construct the same θ, diagonal, rotated A and real quadratic f. | Literal agreement after the exact reindex j=i.val+1. No arbitrary spectrum, witness-selected matrix, opaque characterization or fallback definition replaces the actual grid. |
| Domains | Source hard family has integer d≥2, real κ≥2, O in the full real O(d), and all x∈R^d. Formal d:ℕ with 2≤d, κ:ℝ with 2≤κ, O:Matrix.orthogonalGroup(Fin d) ℝ, EuclideanSpace ℝ(Fin d). | Same hard-family domains. Fin d is 0,…,d−1; d dimensions and full determinant-sign scope are preserved. The broader d≥1,κ≥1 Section2 class is not the local family's parameter range. |
| Quantifiers | Fix d,κ and their literal grid; every O; all pointwise conclusions. Formal ∀d,hd,κ,hκ,O followed by literal lets and a conjunction. Derivative assertion is ∀x; Lipschitz bound ∀x,y; minimizer equivalence ∀x. | Same order and unrestricted spatial scope. θ depends on d,i; A on d,κ,O; f on A. No probability exception, seed, event, trajectory or bounded domain. |
| Assumptions | Only source hard-family parameter thresholds and orthogonality are premises. The source proves geometric properties. | No excess premise in the supplied signature. Smoothness, derivative existence, strong convexity, Lipschitzness and minimization remain conclusions, not hypotheses. Standard real/finite Euclidean typing introduces no extra analytic condition. |
| Conclusion | Source geometric paragraph says C-infinity, Hessian A, 1-strong convexity, κ-smoothness, V_A(0)=0 and unique minimizer0. The formal statement is exactly the six-way conjunction described below. | Agrees for this local geometric content. The source's displayed lower quadratic estimate is not a separately exported conjunct; its role and the broader source residuals are distinguished below. |
| Scopes and senses | Ordinary real Euclidean C-infinity; Hessian as derivative of gradient; source global curvature/smoothness; unique global minimizer. | Standard Mathlib definitions confirm genuine Frechet derivative existence, Euclidean L2 norm, Jensen strong-convexity coefficient1/2 and global minimum predicate. No default-derivative loophole is used as an existence assertion. |
| Constant dependencies | Source normalized bounds1,κ and quadratic factor1/2; no claim of optimality or attained spectral endpoints. | Same thresholds2,2, modulus1, gradient boundκ, zero vector and value0. Hessian is A, not A/2 or2A. No hidden d-,O-,q-,δ-,ε- or probability-dependent constant appears. |

## Binder and definition audit

The supplied public signature has only the following mathematical inputs.

- `{d : ℕ}` is carrier/dimension typing; `(hd : 2 ≤ d)` is the exact standing Section4.1 hard-family bound. It also makes real division by d nonzero on the entire quantified domain.
- `{κ : ℝ}` is parameter typing; `(hκ : 2 ≤ κ)` is the exact standing Section4.1 bound. This is not silently reduced to the source's broader Section2 κ≥1 class or restricted by Theorem4.1's κ≤d^{1−δ}.
- `(O : Matrix.orthogonalGroup (Fin d) ℝ)` is the source's universally quantified orthogonal matrix. Membership packages transpose-inverse identities, with no det O=+1, Haar draw, distribution, or seed-independence premise.
- `θ`, `A`, and `f` are **let definitions**, not quantified assumptions or supplied witnesses. The diagonal expression is fixed by d,κ. The `WithLp.ofLp` use is a coordinate equivalence, not a change of norm or scale.
- All remaining named mathematical predicates occur on the conclusion side. There is no input Hessian estimate, smoothness certificate, strong-convexity witness, Gaussian normalizer, Borel map, derivative assumption or minimizer premise.

For i∈Fin d, put j=i.val+1. Then j∈{1,…,d} and `(i.val+1/2)π/d=(j−1/2)π/d`. This bijection preserves the order of the grid and the corresponding diagonal/eigenvector-coordinate labels; it does not replace the spectrum by an unspecified list. All half/division expressions in θ, λ and f are real division. The matrix conjugation order OΛO^T matches the source, and the real dot product with coordinates is x^TAx. This uses A as the quadratic precision; it does not invert A or use covariance in f.

## Conclusion and standard-definition audit

1. `ContDiff ℝ ∞ f` means continuous derivatives of every finite order globally. The Mathlib definition uses an ℕ∞ branch at ∞, distinct from its ω analyticity branch. This is the source C^∞ conclusion. It is not mere differentiability or continuity and does not claim analyticity.
2. `∀x, HasFDerivAt (gradient f) (Matrix.toEuclideanCLM A) x` asserts a genuine real Frechet derivative of the gradient at every point. Mathlib's HasFDerivAt is a little-o derivative-existence proposition. Matrix.toEuclideanCLM acts on coordinates by h↦Ah, so this is the standard real Euclidean Hessian equality ∇²f(x)=A, with a constant linear map independent of x.
3. Mathlib's gradient is `(toDual ℝ E).symm (fderiv ℝ f x)`, and its documentation records the zero default when no derivative exists. That totalization does not weaken this conjunction: global C^∞ supplies differentiability of f, while HasFDerivAt expressly supplies existence of the gradient derivative. An equality involving a total derivative alone would need separate scrutiny; this supplied statement contains the genuine existence assertion.
4. `StrongConvexOn univ 1 f` unfolds to convexity of the domain and the inequality
   \[
   f(ax+by)\le af(x)+bf(y)-\frac{ab}{2}\|x-y\|^2
   \]
   for all x,y and nonnegative real a,b with a+b=1. The all-space convexity side condition is automatic, not an extra source premise. The modulus normalization agrees with source1-strong convexity.
5. `∀x y, ||gradient f x−gradient f y||≤κ||x−y||` is the standard global Euclidean κ-smoothness meaning supported by the source's Hessian bound. It does not assert a sharp Lipschitz constant or restrict the estimate to a neighborhood.
6. `f 0=0` and `∀x, IsMinOn f univ x↔x=0` give minimum value0, existence at0 and uniqueness. Mathlib's IsMinOn on univ means f(x)≤f(y) for every y. Specializing the biconditional at x=0 supplies actual attainment; it is not a uniqueness implication lacking existence. This is global minimization on all R^d.

The source geometric paragraph also displays V_A(x)≥||x||²/2>0 for x≠0 as its intermediate reason for the unique minimum. The selected signature does not export that estimate separately. There is no incompatible weakening of the represented quadratic geometry: for the literal quadratic, f(x/2)=f(x)/4; the stated strong-convexity inequality at x,0 with a=b=1/2 and f(0)=0 yields f(x)/4≤f(x)/2−||x||²/8, hence f(x)≥||x||²/2. This is a short semantic check of the source paragraph's meaning, not a checked Lean declaration or an additional source-credit claim.

Necessary local Mathlib definition windows and full-file/window hashes are in `mathlib_definition_inputs.json`. They cover orthogonalGroup, EuclideanSpace/coordinate action, gradient, HasFDerivAt, StrongConvexOn/UniformConvexOn, ContDiff and IsMinOn. Some rendered raw windows incidentally contain nearby standard lemmas/proofs; those exposures are retained, and no candidate proof route was inspected or inferred from them. The approved context agrees with these inspected standard definitions. This run makes no claim about hidden target imports/scoped notation; their exact binding is a later whole-module check.

## Comparison with the independent blind reconstruction

The reconstruction correctly identifies every let, all three input restrictions, the full orthogonal group and zero-based grid. It reconstructs all six conjuncts with the right normalizations, unrestricted quantifiers and genuine derivative-existence semantics. Its distinction between C^∞ and analyticity, its warning about totalized gradient values, its interpretation of the minimizer biconditional and its absence of probability/algorithm claims agree with the supplied proposition and my source baseline. No decoder-added source claim or omitted formal conjunct was found.

The supplied decoder actor is `/root/decode_80a1c2`, distinct from this reader `/root/source_reader_9a6d2f`. Its embedded run says the mathematical input was only the anonymous statement and approved definitions; it records no source lookup or prior verdict access and discloses ambient theorem-adjacent runtime labels. This supports the intended source-blind input separation without a zero-cue claim. I did not open the original decoder files or inspect withheld formalizer/orchestration metadata. Original decoder raw digests are supplied provenance; canonical nested-object digests and the actual reconstruction-text digest were separately computed here. No original serialized-file byte identity is asserted without reading those files.

## Residual source claims and exclusions

These remain outside this selected proposition and outside any complete-source acceptance from this phase.

- C.4 paragraph1 and displayed Lemma4.6: the explicit strict angle/cosine/eigenvalue estimates and the exported Loewner admissibility/class-membership interface. The anonymous proposition has the actual input definitions, but no separate Loewner or strict-eigenvalue conclusion is supplied for review. This selective comparison does not award formal coverage to those interfaces or their proof route.
- C.4 paragraph3 and display `A3.Ex160`: the associated Gaussian target with covariance A^{-1}, Lebesgue Gaussian normalization, determinant invariance, positivity/finiteness of the normalizer, independence from O and knowledge from public spectrum. There is no Gaussian law, determinant, integral, normalization or public-information object in the selected proposition.
- Section2: the exact first-order pair, equality of value-gradient/gradient/matrix-vector query complexities, fixed-input reply conversion and Borel meaning, adaptive Borel policy/stopping/output composition, seed/input independence, output laws, uniform TV accuracy and per-input/per-seed deterministic query caps. None is a conclusion of the selected conjunction. Smoothness of this f is not itself a statement of adaptive oracle equivalence or a probability/cost theorem.
- Section4.3's use-site and the rest of the lower bound: Lemmas4.3–4.5, Krylov representation, concentration, target moments, asymptotic parameter bookkeeping and the averaged TV contradiction remain excluded. No theorem probability, query complexity, or whole-paper result is established by this comparison.
- Implementation obligations: no compiled target binding, complete module inventory, private helper consumers, fake-closure/axiom cleanliness, actual dependency edges, authored lesson/exposition, publication coverage or static/live reader behavior has been inspected. The packet's `compiled=true` is reported metadata, not a fresh check by this reader.

The coverage difference between the selected conjunction and the complete raw slice must remain visible. If this proposition were presented as all of C.4 or as the whole paper theorem, that broader equivalence would not be supported by the supplied proposition. Since publication and intended whole-target claims are deliberately withheld, this phase makes no judgment about whether the eventual artifact makes such an overclaim.

## Phase boundary

No blocking mismatch was found in the selected proposition's geometric meaning or the supplied reconstruction. No repair proposal is made. Full-module/source-fidelity acceptance remains pending the separately authorized later phases and their exact input binding. No sourceV or lifecycle API, Lean command, build, browser/runtime or target inspection occurred. Phase2 artifacts are frozen separately; phase1 remains untouched.
