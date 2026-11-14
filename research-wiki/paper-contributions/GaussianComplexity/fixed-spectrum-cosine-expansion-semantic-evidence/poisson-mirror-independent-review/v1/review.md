# Independent Poisson/cosine mirror review v1

**Verdict: ACCEPT_CONCEPTUAL_ONLY. No HOLD or payload repair is requested.**

Run: `POISSON-COSINE-MIRROR-INDEPENDENT-REVIEW-20261109-v1`; review timestamp 2026-11-09 06:44:19 UTC. This actor differs from the root proposer/creator. The exact reviewed candidate is `poisson-cosine-mirror-candidate-v1.json`, SHA-256 `bcd24a72d1409f6b0b6747d85116d3317cb51c0d0612d5789d0affd5b317cd1e`.

This accepts a source-backed mathematical interpretation as typed conceptual memory. It is not a Lean implication, formal transport, C7 proof review, source V, Discovery validation action or upgrade of any previous audit. The accepted preproof source graph is not reopened.

## Independent source reading and existing boundary

Before opening the candidate, the complete fixed raw `A1.SS1` was read, including its introductory sentence, entire Lemma A.1 statement, Eq12 and complete proof. Its exact outer HTML is 10691 bytes at [359486, 370177), SHA-256 `28ae091bbde1cb098fcaa07a858dab48f9521cf14d4e32c4909876a85745c4ab`, within the unchanged 951991-byte paper snapshot SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

The literal statement first says n≥2 and later appends “where n≥3.” This is a real source ambiguity, not silently resolved by this review. The proof defines normalized surface measure σ, invokes the Poisson representation formula for harmonic h continuous on the closed ball, evaluates at a=re₁ with h=1 and h=x₁, and divides by 1−r². Its named external source is [5, Theorem 1.21]; that external text was not fetched or independently certified here.

The already understood full C7 statement/proof and C8 finite-grid use at `A3.Ex140`/`A3.SS3.p4.2` were used as the other source side. The raw C8 statement/grid identity was checked as evidence for the candidate's exclusion of finite-grid closed moments, not as a new formal result.

Only the exact signature of `SphericalPoisson.spherical_poisson_moments` was displayed, with no proof body. It has n≥2, 0<r<1; explicitly defines the normalized Euclidean surface measure σ; proves integrability and evaluates the two **raw** reciprocal-power integrals as 1/(1−r²) and r/(1−r²). Its local `K` names the denominator power, not the candidate's normalized kernel. The exact signature is retained separately in this review directory.

The explicitly authorized old frontier was read solely to preserve its boundary: full-source status remains source-underspecified; the n≥3 slice is retained, n=2 remains a disclosed mathematical extension, and the author's arbitrary-harmonic HFT route remains source-only debt distinct from the existing direct alternative. Old verdict/route/API names appearing in that frontier were not used as new proof or library evidence. This review does not recertify compilation, source equivalence or the old reader/audit evidence.

## Candidate-by-candidate mathematical/source comparison

| Candidate part | Independent determination |
|---|---|
| Formula | Correct. Write s=√κ and r=(s−1)/(s+1). Source κ≥2 gives 0<r<1. `A3.Ex136` supplies the spectral normalization: 1−r²=s(1−r)² and λκ(θ)=(1+2r cosθ+r²)/(1−r)². Thus λκ(θ)⁻¹=s⁻¹K₋ᵣ(θ), with Kq=(1−q²)/(1−2q cosθ+q²). No sign or √κ factor is lost. |
| Mechanism | Source-backed interpretation. A1's source proof uses normalized Poisson representation; C7's actual source proof uses geometric series and cosine/exponential algebra. C7 does not call its expression a Poisson kernel. The candidate explicitly labels that kernel reading as an algebraic inference, which is the right attribution. |
| Hypothesis map | Correct with the stated missing adapters. The circle is S¹ in auxiliary real dimension 2. It is not the Gaussian ambient dimension d. The positive-pole A1 theorem does not directly instantiate at q=−r, nor does its stated surface measure directly identify an angular integral without an adapter. The candidate says both certificates are missing. |
| Key estimates | Correct. Multiplication of the raw A1 integrals by 1−r² yields normalized mass 1 and positive-pole coordinate mean r. C7's bound uses r^(j+1), which is summable for each fixed κ. The exact normalization 1−r²=√κ(1−r)² and external 1/√κ factor agree with the source. |
| Conclusion map | Appropriate conceptual scope. Harmonic reproduction and cosine/Fourier decomposition belong to the same normalized Poisson-kernel mechanism after the auxiliary-circle/sign/measure adapters. The existing concrete A1 interface only certifies the two listed integrals; it is not a compiled general-harmonic representation theorem or all-Fourier-mode transport. The candidate does not claim either result is a compiled dependency of the other. Its mentions of current compiled substrates are not independently compiler-certified by this source/math review. |
| Source map | A1.SS1/Eq12 and its proof support raw moments, normalization and the harmonic origin. C7 Ex133–137 supports the rational/cosine identity and fixed-κ convergence. C8 p4.2 supports finite-grid/series exchange only. The review additionally binds raw `A3.Thmtheorem8`/`A3.Ex138` and `A3.Ex139` as evidence for the candidate's finite-grid failure boundary; those source statements do not become current formalization credit. |
| Graph placement/status | `overview`/`functor`, candidate substrate names, `formal_transport_certificate=false` and pending independent validation are consistent with conceptual memory. They cannot generate a solid Lean dependency or a certified functor. This review makes no shared graph/model write. |

## Adapter and failure-boundary checks

1. **Raw versus normalized A1 moments.** The raw integrands are D^(−n/2) and U D^(−n/2), where D=1+r²−2rU. Their expectations are not 1 and r; those are the moments only after multiplying by 1−r². The candidate makes this distinction correctly. For n=2 the normalized kernel has denominator power 1; for other dimensions its power is n/2.

2. **Circle measure and negative pole.** A mathematical circle realization uses u(θ)=(cosθ,sinθ) and normalized angular measure dθ/(2π), after a surface-measure/parametrization identity. Replacing positive r by q=−r requires a rotation or θ→θ+π, not the existing theorem's prohibited direct negative-r instantiation. Under that adapter the coordinate mean changes sign to −r, and j-th cosine modes change by (−1)^j. The candidate's positive-pole A1 mean r is not asserted as the C7 negative-pole mean. Neither adapter is supplied as a certified artifact by this candidate.

3. **Auxiliary dimension.** The use of dimension 2 is mathematical circle interpretation plus the disclosed existing n=2 extension. It does not settle the raw A1 wording, reduce a Gaussian in dimension d to a circle, or identify a d-dimensional spherical harmonic kernel with the plain cosine expression. The generic n/2 denominator and appropriate spherical-harmonic content remain essential outside the circle.

4. **Fixed κ, not uniform κ.** At θ=π, the signed positive-mode terms become r^j. The unscaled tail after modes 1,…,N is r^(N+1)/(1−r). As κ→∞ and r→1, no common N controls that tail. Even the full spectral reciprocal's scaled remainder at θ=π is 2r^(N+1)/(1+r), tending to 1 for fixed N. The candidate correctly refuses uniformity over unbounded κ and excludes r≥1 from this majorant argument.

5. **Continuous measure is not the finite midpoint grid.** Continuous normalized angular averaging cancels nonconstant integer cosine modes once the angular/surface adapter is established. The d midpoint nodes instead retain modes k=2ad with alternating signs (`A3.Ex139`). The paper's raw C8 formula is M=(d/√κ)(1−r^(2d))/(1+r^(2d)), not d/√κ. This source contrast substantiates the candidate's warning; it is not a newly proved C8 declaration. The current finite-sum/series interchange alone neither evaluates aliases nor identifies Gaussian means.

6. **No downstream transfer.** There is no inference here to closed C8 moments, variance/bias, Gaussian expectation laws, TV, oracle precision, deterministic caps, expected costs or either main bound. The missing circle/sign/measure adapters cannot be bypassed by a family label. The candidate preserves all of these limits explicitly.

## Freeze and final scope

`input-manifest.json` records the exact candidate, raw-source fragments, old theorem file/signature, authorized frontier and policy hashes. The old theorem body was neither displayed nor reviewed; the first signature extractor stopped early at a literal let-assignment, and a corrected proof-marker extraction displayed only the full signature. No compilation, proof search, browser/network access, broad repository scan, Discovery validation API, canonical/shared write or agent delegation occurred. Writes are confined to this review directory.

The exact candidate may proceed to a separately authorized normal independent validation as **conceptual-only** evidence. This review does not execute that action. Any later change to the candidate's formulas, adapter claims, source/domain status or failure boundary requires a newly bound review of the changed content.
