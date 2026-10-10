# Same-prox canonical KL/dimension preread45

The next bounded candidate is the actual standardized-RGO bound KL(r_s‖stdGaussian E).toReal≤eta_s²·finrank(E)/2, with one measurable unique stationary proximal family. This is an internally derived canonical-KL ingredient of SPHMC FIRST4.6. It is not W₂ or FIRST completion. The exact proposed header is in prospective-minimal-target.txt; it is unelaborated and unsealed, not a Lean declaration or theorem approval.

Primary2609.06906v1 was read before current31/43 public extraction. Normalized standing assumptions are C²V andκ⁻¹I≤HessianV≤I, beta1 (physical606–609). S2.E1 defines the positive-step prox (612–620); the RGO density is exp(−V−‖x−y‖²/(2eta)) (627–632); S2.Ex2 defines canonical KL with the +∞ AC convention (652–661). S4.Ex8/S4.SS1.p4.2 fixes p=prox_etaV(y), ρ(u)=V(p+sqrteta·u)−V(p)−sqrteta·〈gradientV(p),u〉, and r as the law of(X−p)/sqrteta (1289–1300). FIRST4.6 (1306) gives the Fisher/moment chain with covariance-I Gaussian reference, and its explanation (1310–1314) invokes GaussianLSI/T₂, gradient Lipschitzness and the strongly-concave Gibbs moment bound. Squaring the last two source inequalities yields Fisher≤eta²·d. The paper does not separately print the canonical-KL numeric leaf; deriving it from its LSI invocation and the source Fisher estimate is an internal assembly, with no added paper assumption.

Actual public parents:

- AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher.standardized_rgo_position_and_fisher (31) supplies measurable p31 and stationarity; literalρ, Q=‖u‖²/2+ρ, mu, R, r; actual probability; positionL²/integrability/second moment≤finrank; actualρ-gradientL²; Fisher≤eta²·moment and Fisher≤eta²·finrank.
- AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOKLFisher.standardized_rgo_unique_prox_and_kl_le_fisher (43) supplies measurable p43, stationarity and uniqueness; literalρ, mu, R, r, gamma=stdGaussian E; actual probability, AC, finite canonical KL, actualρ-gradientL² and KL.toReal≤½Fisher. Root reports PROVED_LOCAL19b569ae0fe37c97da0f98b4d1f4933ebabc7052 with independent exactcommit verification active. This preread neither reads the proof nor awards VERIFIED status.

Both headers have exactly the same input binders. Every eta_s>0 is allowed; no eta≤1, extra reference point or transport hypothesis appears. E is complete finite-dimensional real Hilbert/Borel; S is measurable and eta/y are measurable. These are the existing family/carrier extensions of a fixed Euclidean source parameter. Unit recovers the paper's fixed eta/y; rank0 remains allowed, with finrank cast to real0 and bound0. No dimension division or Nontrivial E premise is needed.

Choose p43 as the output witness. Apply43 uniqueness at each s with z=p31(s) using31 stationarity; obtain p31(s)=p43(s), then p31=p43 by function extensionality. Rewrite all p-dependent31 definitions, especiallyρ and the actual affine pushforward r. Q is also transported if the full31 output tuple is rewritten; mu and R are independent of p. A same-ρ assertion with an unaligned r is insufficient. No public p, coherence or normalization certificate is introduced.

After transport, the exact two quantitative inequalities concern the same genuine integral I_s=∫‖gradientρ_s(u)‖²∂r_s.31 gives I_s≤eta_s²·(finrankℝE:ℝ).43 gives finite canonical KL.toReal≤(1/2)I_s. Multiply31's inequality by the nonnegative scalar1/2 and use(1/2)(eta²·d)=eta²·d/2. Nothing is divided by I_s, eta_s or d; the calculation includes zero energy and rank0. The finrank in31's real inequality is already an implicit Nat→Real coercion; the proposed final RHS makes that same cast explicit. The squared eta is essential: eta√d is the later W₂ scale and is not the canonical-KL numeric bound.

Finite canonical KL is preserved as an actual output before using toReal. Actualρ-gradientL² is preserved as an output and supplies the genuine finite Fisher domain; no derivative of canonical llr is used. Probability and AC come from43. The proposed minimal quantitative header retains these43 semantics and replaces the energy RHS with the numeric RHS; it does not export Q or the entire31 position ledger.31's real positionL²/moment outputs remain available for a future T₂ consumer and can be aligned again using the retained unique witness. They are not additional caller inputs.

Source obligations, at most seven steps:

1. Apply actual31 and, only after independent verification,43 under the shared exact source/carrier/family assumptions.
2. Select43's measurable unique stationary witness.
3. Derive31/43 witness equality internally using43 uniqueness and31 stationarity; use function extensionality.
4. Transport every requiredρ/Q/r output by that equality, with mu/R unchanged, preserving actual gradients and measures.
5. Retrieve43's canonical probability/AC/finiteKL/gradientL² outputs and half-Fisher inequality; retrieve31's final numeric Fisher inequality for the aligned witness.
6. Compose the two real inequalities using scalar½ monotonicity, rewrite the exact finrank cast and RHS arithmetic, including zero/rank0.
7. Assemble the proposed output tuple. Statement/typecheck/source review and independently reconstructed/reviewed topology must precede proof; independent implementation verification follows proof.

No moment, gradient-growth or Gaussian LSI background is reproved. No prospective header has been admitted here.43 independent verification is the execution prerequisite; no nextclaim/proof should start before it. Gaussian T₂ and actual W₂ remain the typed44 gap. FIRST4.6, Gaussian bias/main/error/query-cost composition and reader PURIFIED status remain separate.44 packet originals are immutable; current/prior exposure and raw/LF input bindings are recorded in this packet.
