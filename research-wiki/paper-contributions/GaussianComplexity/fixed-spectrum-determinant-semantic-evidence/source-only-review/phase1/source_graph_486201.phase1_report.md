# Frozen phase-1 source extraction — source-graph-486201

This is a raw-source-first extraction of the determinant/known-normalizer context in *On Complexity of Gaussian Sampling*, arXiv:2610.20492v1, Eq. (11) and Appendix C.4. It is a proposed source proof graph, awaiting independent coverage review. No candidate statement, implementation, old graph or prior review was inspected. It confers no Lean, source-V or source-completion credit.

The raw input SHA-256 is `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`. The JSON artifacts bind the instructions, raw source, seven slots, complete selected source coverage and graph with hashes.

The source fixes an integer d≥2 and real κ≥2. For the literal indices i=1,…,d it defines

\[
\theta_i=\frac{(i-\tfrac12)\pi}{d},\qquad
\lambda_i=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_i,\qquad
\Lambda=\operatorname{diag}(\lambda_1,\ldots,\lambda_d).
\]

It draws O from Haar probability on the full real orthogonal group, independently of algorithm randomness, and sets A=OΛOᵀ. Both determinant components are included. For the pointwise statements, O is arbitrary in O(d). The Haar law and seed independence describe the experiment; they are not necessary public premises for determinant invariance.

The determinant component used in the second equality of Ex160 is det(OΛOᵀ)=det Λ. Its standard omitted algebra uses determinant multiplicativity, invariance under transpose and (det O)²=1. Replacing full O(d) by determinant +1 would narrow the source. The source does not state this determinant component as a separately numbered lemma.

The combined claim has two actual prerequisites. Gaussian integration supplies

\[
Z_A=(2\pi)^{d/2}(\det A)^{-1/2},
\]

and determinant invariance supplies its substitution by det Λ. Their use is an AND. A theorem proving only determinant invariance does not itself prove Gaussian integrability or the normalizer formula. Positive definiteness comes from the source grid and orthogonal conjugation; it belongs inside the proof as a dependency, rather than as a convenience public hypothesis.

Since Λ is fixed at fixed d,κ, the resulting Z_A is constant as O varies. When the spectrum is public it is known from the displayed expression. The first is pointwise eigenbasis invariance; the second retains the source's informational condition. Neither is the separate independence between O and algorithm randomness. Z_A conventionally means the Lebesgue mass of exp(−V_A), not an integral against the normalized Gaussian. The selected source does not separately define this base measure, so phase 2 must expose the candidate's actual normalizer definition before comparing meanings.

All of C.4 is covered, including its unnamed material. The first paragraph derives 0<θ_i<π, −1<cos θ_i<1, 1<λ_i<κ and I_d≼A≼κI_d. Only the last spectral bound is the numbered Lemma 4.6 conclusion. The second paragraph states smoothness, Hessian A, 1-strong convexity, κ-smoothness, V_A(0)=0, strict positivity away from 0, and the unique minimizer. The third identifies the target, invokes Gaussian integration, states the determinant equality chain and concludes fixed/public-spectrum normalization. Those statements have separate nodes and consumer-use edges.

The graph has no source-stated alternative sufficient proof route. In particular determinant algebra and Gaussian integration are not OR alternatives for the combined Z result. Omitted standard symmetry/positivity and determinant bridges remain marked SOURCE_GAP; Gaussian integration is an explicitly invoked unnamed result without a proof or citation here. These markers describe omitted source detail, not a claim that the source is false.

The coverage inventory includes every paragraph, display, heading, citation, MathML expression and nonempty text node in the selected source roots, with NODE or EXCLUDED disposition, plus a complete DOM-element inventory for S4.SS1, its admissibility subsection and C.4. Remark 4.2, the Krylov/moment lemmas, Theorem 4.1, oracle complexity, and the distinct hidden determinant-sign construction are explicitly excluded from this bounded component. The [22, §9.2] citation is provenance for a similar construction; C.4 does not invoke that external preprint for this calculation. Its content was not fetched.

Phase 1 stops here. Phase 2 may expose the exact sealed statement and only the definitions necessary to interpret it, then compare all seven frozen slots. This phase has not accepted a candidate, reviewed its proof, updated shared truth, or approved its own source coverage.
