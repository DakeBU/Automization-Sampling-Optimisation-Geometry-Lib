# Phase 1 raw-source freeze: Gaussian physical rows and original cutoff event

Reviewer: `rl_src_3dd4`. Frozen at 2026-11-12 05:47:43 UTC. This document was written before exposure to any proposed Lean signature, meaning-carrying definition packet, implementation module, decoder reconstruction, prior semantic verdict, source graph, or topology verdict. It is a bounded raw-source interpretation, not mathematical proof approval or permission to change the source contract.

The pinned input is *On Complexity of Gaussian Sampling*, arXiv:2610.20492v1, local HTML `.astis/huanjian-resume-20261103/2610.20492v1.html`, 951991 bytes, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`. Exact HTML fragments, byte offsets, line intervals, and hashes are in `source_locators.json`.

## Standing source scope

The primary experiment comes from Lemma 4.4 (`S4.Thmtheorem4`, lines 1207–1231): q is a nonnegative integer, 2q+1<d, and g_1,...,g_{q+1} are independent N(0,I_d) vectors. Lemma 4.3 (`S4.Thmtheorem3`, lines 1161–1174) explicitly calls q an integer and repeats that range and the original independent Gaussian columns. The construction at `S4.SS1.p1` (1085–1102) has dimension d≥2 and κ≥2. Under the stated q range, d≥2 also follows directly.

Appendix C.2 is the proof of Lemma 4.4. Its p1 sets r=q+1 and n=2q+1. The assigned target here consists only of the physical Gaussian row marginal and the p10 simultaneous cutoff event. The Krylov uniform bound, operator-norm deviations, cosine cancellation, B-Gram expectations, truncation bias, matrix Bernstein, and their later probability budgets are outside this target. The absolute C and the condition τ_{d,q}≤1/2 belong to the larger Lemma 4.4 conclusion; neither is used in the p1 row marginal or p10 cutoff estimate. κ, θ_i, and n do not occur in the law or cutoff being reconstructed.

## Original experiment, coordinates, and laws

The underlying simultaneous experiment is one draw of r independent d-dimensional standard Gaussian columns g_a. A literal realization is the product space (R^d)^r with product law of r copies of N(0,I_d). This merely makes the source experiment explicit; it is not an additional mathematical hypothesis or a change of law.

The d×r random matrix has entries M_{i,a}=(g_a)_i, with 1≤i≤d and 1≤a≤r. Each physical row is the random vector

    γ_i = ((g_1)_i,...,(g_r)_i)^T ∈ R^r.

This is the formula in `A3.SS2.p1` (3317–3329). For each fixed physical coordinate i, γ_i has law N(0,I_r): each selected scalar coordinate has N(0,1) marginal, and the r scalars are independent because they come from independent columns. The marginal statement is a pushforward law under the actual original column experiment. An isolated auxiliary r-dimensional Gaussian with the same distribution does not by itself identify any event of the original d-row experiment; that identification requires the row coordinate map and its marginal law.

The same p1 additionally states that γ_1,...,γ_d are jointly independent N(0,I_r) vectors. This is a stronger source assertion than the collection of one-row marginal laws. Full standard d-Gaussian column laws plus column independence support that assertion through independence of scalar coordinates, but the collection of one-row marginal laws alone does not establish joint row independence. No later finite-union calculation requires joint row independence. Thus a bounded result establishing marginal laws and the simultaneous cutoff does not yet discharge the entire p1 independence assertion.

The neighboring B is a different matrix: B∈R^{d×r²} has row d^{-1/2}(γ_i⊗t_i)^T, with t_i∈R^r. Accordingly γ_i has r coordinates, while the associated B row has r² coordinates. The squared quantity used for cutoff is ||γ_i||², not the B-row norm, not a column norm in R^d, and not a norm of a freely chosen Krylov coefficient vector.

## Exact cutoff and endpoint conventions

Paragraph `A3.SS2.p10` (3532–3556) defines

    L = 2r + 3 log(1000d),
    R_i = ||γ_i||² = Σ_{a=1}^r (g_a)_i²,
    T = {R_i ≤ L for every 1≤i≤d}.

The logarithm is the real natural logarithm, as used by the displayed exponential tail. Both 1000 and the coefficient 3 are exact source constants. The event T is simultaneous over the finite set of d physical row indices in the original column experiment. It has a closed good inequality R_i≤L. Its complement is exactly the any-bad event

    Tᶜ = {there exists 1≤i≤d with L<R_i} = ⋃_{i=1}^d {R_i>L}.

The bad inequality is strict. Replacing it with R_i≥L changes the literal event and is not authorized by this source fragment. Equality R_i=L belongs to T.

## Printed evidence and inferred finite-union arithmetic

What p10 actually prints is:

    E exp(R_i/3) = 3^{r/2},
    P(R_i>2r+3x) ≤ exp((r/2)log 3 - 2r/3 - x) ≤ exp(-x),  x≥0,
    (log 3)/2 < 2/3,
    P(T) ≥ 1-d/(1000d) = 0.999.

The mgf identity is row-marginal Gaussian evidence. The displayed one-row tail is strict in R_i, with x nonnegative. The final printed probability is an all-good lower bound. The paragraph does not separately print an any-bad upper-bound theorem.

The following is the explicit inferred finite-union bridge, not another quotation or independently printed source result. With x=log(1000d)≥0, each original row satisfies P(R_i>L)≤1/(1000d). Finite subadditivity on the same original experiment gives

    P(Tᶜ) ≤ Σ_{i=1}^d P(R_i>L) ≤ d/(1000d) = 0.001,
    P(T) ≥ 1-0.001 = 0.999.

The equality of Tᶜ with the strict any-bad event is the endpoint-sensitive link. This bridge uses one-row marginal laws, their tails, a finite union, and complement arithmetic. It does not use independence among rows. All-good ≥0.999 is printed in p10; any-bad ≤0.001 and the detailed finite-union calculation are reconstructed implications supporting that printed assertion.

## The q=0 endpoint

There is no separate parameter named q_0 in the bounded anchors. The boundary q=0 is allowed by q≥0 and 2q+1<d when d≥2. Then r=1, n=1, g_1 is one standard d-Gaussian column, γ_i=((g_1)_i) is a one-dimensional standard Gaussian row, R_i=(g_1)_i², and L=2+3log(1000d). The same strict-bad/closed-good event and probability arithmetic apply. Any eventual formal representation that requires q>0 or r>1 would discard this source endpoint. The faithful standing range has no d=1 instance; a more general standalone Gaussian fact on d=1 would need to be labeled as a generalization.

## What later phases must still compare

This freeze contains no proposed Lean names, signatures, structure fields, or implementation API choices. Later type/definition review must compare the actual carrier, original product law, coordinate orientation, Gaussian normalization, r versus r² dimensions, exact cutoff, finite physical row set, strict versus closed endpoints, q=0 coverage, and attribution of printed versus inferred probabilities against this freeze. Whole-code and anonymous-reconstruction reviews remain separate, unfrozen phases. Nothing here certifies an implementation, a source graph, a complete Lemma 4.4 proof, the source p1 joint-independence claim as formalized, or a publication/Goal completion state.
