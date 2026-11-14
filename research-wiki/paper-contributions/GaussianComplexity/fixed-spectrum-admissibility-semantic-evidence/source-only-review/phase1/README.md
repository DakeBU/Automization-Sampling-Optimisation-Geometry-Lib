# Phase-one source-only freeze

This packet reconstructs the source topology for Eq. (11), the actual cosine-grid rotated hard precision, and Lemma 4.6 (admissibility) from the pinned full raw `2610.20492v1.html`. It was constructed before any candidate Statement Seal, implementation Lean, Test, root preseal audit, authored publication, target API or earlier review was opened. The exact full original source is included; its SHA-256 is `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

The source family assumes integer `d ≥ 2` and real `κ ≥ 2`. It defines, for one-based indices `i=1,…,d`,

\[
\theta_i=\frac{(i-\tfrac12)\pi}{d},\qquad
\lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_i,
\qquad\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_d),
\qquad A=O\Lambda O^\top.
\]

The numbered lemma concludes `I_d ≼ A ≼ κ I_d` for **every** real orthogonal `O`. The Haar draw and independence from the algorithm seed describe the randomized input family; they are not needed for this deterministic conclusion. The source does not take an arbitrary spectrum together with an eigenvalue-envelope premise. It derives the envelope from its literal grid.

The source route is:

1. The grid gives `0 < θ_i < π`.
2. Hence `−1 < cos θ_i < 1`, then `1 < λ_i < κ`.
3. Orthogonal conjugation transfers this diagonal bound to the stated Loewner bounds. Symmetry of the defined `A` is internal, and is needed for the precision-class definition in Section 2.
4. At the exact consumer `S4.SS3.p2.1`, the proof of Theorem 4.1 uses admissibility to restrict a sampler's guarantee over every admissible matrix to this hard family.

Appendix C.4 also asserts that the quadratic is smooth with Hessian `A`, is strongly convex and smooth with constants `1,κ`, has unique minimizer `0`, and has a Gaussian normalizer independent of `O`. These are separate consequence branches. They are not additional assumptions or ingredients for the literal numbered Loewner conclusion. Section 2's oracle equivalence is separate background; its presence in a subsection heading does not make it an admissibility premise.

Eight explicit `SOURCE_GAP` nodes retain the unexpanded grid arithmetic, strict cosine fact, affine envelope calculation, matrix congruence/symmetry/norm calculation, quadratic calculus, Hessian/minimizer adapters, Gaussian normalization, and determinant invariance. These are unproved internal bridges in this source-only packet. They do not assert source invalidity and do not license extra theorem binders. The source uses `Z_A` with the usual Gaussian normalizer convention, without a standalone integral definition in the selected text; that meaning remains visible as an obligation if this appended branch is claimed.

`coverage.json` inventories the selected full S1, S2, S4 and C.4 source regions, theorem wrappers, citation occurrences, and incidental raw-source search exposures as `NODE` or `EXCLUDED(reason)`. Sibling Krylov, moment, test-event, determinant-sign and limitations branches are explicitly excluded because they do not supply a premise for this bounded admissibility closure. No external linked theorem document was accessed. Bibliography identities are included only to make citation exposure auditable.

`source-contract.json` contains the independent seven-slot source reconstruction and source binder/definition classification. `source-graph.json` contains nodes, directed AND-edges with exact consumer use sites, and branch boundaries. There is one source proof route here; no alternative route or false conjunction with sibling proof branches is asserted. `raw-inputs.json` and `exposure-manifest.json` bind the inputs and record actual exposure, including incidental source-search paragraphs and a mistaken bibliography element inspected before identifying the displayed reference number.

This freeze is source extraction evidence, pending a distinct coverage/topology review and later candidate matching. It is not Lean evidence, accepted source fidelity, theorem completion, or a self-approved coverage result. Phase one stops here. Phase two may begin only after root receives the freeze hashes and provides the exact candidate and its necessary definition meanings.
