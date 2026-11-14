# Independent phase-3 review at immutable candidate 25922bb4

**Decision: ACCEPT, within the bounded source/whole-module/static-reader/focused-runtime scope below.** The canonical semantic verdict proposed is `equivalent-after-elaboration`. No blocking semantic or implementation defect was found. This is not a source-V/API transition, an `independently_verified` setting, full repository acceptance, graph/UI acceptance, or completion of Fact C.8/Lemma 4.5.

Reviewer identity is `/root/source_reader_d63b90`, distinct from the formalizer and `/root/decoder_47c18e`. The independent raw-source cognition was frozen before any candidate exposure, and phase 2 was frozen before whole-module/proof access. Both earlier freezes remain preserved.

## Exact reviewed boundary and binding

The checked mathematical candidate is commit `25922bb4c3b5a14ec882ebd4d876ed4a309b8843`. Four authorized candidate files were copied with `git show` into this phase's private snapshot and matched their working copies byte for byte:

- Producer `FixedSpectrumGaussianMoments.lean`: SHA-256 `6fb5f83f8c392814246dd39c1f95201215407fd8e14243f3b0e1e6e7895a847d`.
- Focused Test: `8fd259050d495b7c3a9f88319f41d6096ef8c598654c9eaa6509b49d32862fd4`.
- Authored lesson: `3c41463c96ad8ca2dc80bf7e53aa0d3da30ae20cfb4a615a0dfdd03b667ec547`.
- Publication item: `5753a24662e02d75993dff5fd40fd784308d84e66f48c86e965b00e93afaf0bf`.

The v2 canonical reviewer packet raw hash is `5eac0d7b79a1418baf8b8811277d33e7f9497b58c74ca1a35c1381eab44650a2`, and its canonical hash (excluding the packet hash field) is `e1adea42232f6dd227d77cf8cf1696fd211b85993d3939f2dbe02032586e2f22`. All four anti-anchoring flags are false. I independently reconstructed the publication binding from the exact source/lesson/publication/toolchain/manifest snapshots: it is exactly `a9b67ab0b35b750530b517e14f081f53ccb1d70e1bc39d769d15a8737d2bad17`. The packet's sanitized publication context equals the context reconstructed from these snapshots.

The pinned source remains arXiv:2610.20492v1 HTML SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`. The public source boundary is C.3 p4.1/Ex140: the two actual Gaussian expectation-to-reciprocal-grid-sum identities. The private consumer is the actual Gaussian cosine alias-series precursor from p4.2/p6.1/Ex144, with the Ex139 alias coefficient. Closed C.8 resummations, fourth moments, variances, bias, orthogonal transport, algorithm/output laws and full lower bounds remain outside the result.

## Statement, definitions and all hypotheses

The elaborated public type has precisely d:Nat with d>=2, kappa:Real with kappa>=2, and n:Nat with 1<=n<d. Its five local definitions are the exact midpoint angles, cosine precision eigenvalues, diagonal precision matrix, literal multivariate Gaussian with covariance Lambda inverse, and coordinate cosine quadratic form. No scoped variable, typeclass premise, moment witness, arbitrary measure, integrability premise, covariance certificate or interchange premise appears as an extra public assumption. Imports and open/scoped declarations do not introduce hidden hypotheses.

The source's one-based angles become `(i+1/2)pi/d` on Fin d. The covariance argument is Lambda inverse, preserving the precision/covariance distinction. The norm is Euclidean. The coordinate Q is exactly the real diagonal quadratic form. A separate independent Lean theorem verifies, for arbitrary real weights and Euclidean x, that `dotProduct x (Matrix.mulVec (Matrix.diagonal w) x) = sum_i w_i*x_i^2`.

Both integrability facts are conclusions, not assumptions. They explicitly discharge what the raw source treats implicitly in its finite Gaussian expectations. This is an explicit elaboration, not a source repair or a weakened premise. The phase-2 source, anonymous statement and blind reconstruction string hashes are unchanged in v2. All seven semantic slots are preserved, with explicit integrability elaboration recorded in the exact canonical application proposal.

## Actual analytic proof

The producer proves lambda_i>=1 internally using the cosine lower bound and kappa>=2, then obtains strict positivity and diagonal positive definiteness. It proves the actual matrix inverse equals the diagonal reciprocal matrix by an explicit left-inverse multiplication. Matrix.PosDef.inv supplies the positive-definite inverse covariance. Thus neither totalized matrix inversion nor the Gaussian square-root constructor's off-positive-semidefinite Dirac branch changes the intended object on this theorem's entire domain.

I read the pinned Mathlib multivariate Gaussian constructor and its Gaussian-instance, mean and covariance/variance proofs. The constructor is the pushforward of the standard Gaussian by the covariance square root and mean shift. Its variance-evaluation API requires positive semidefiniteness, which this producer supplies from the proved inverse positive definiteness.

Each coordinate belongs to L2 by `IsGaussian.memLp_dual` applied to the actual Gaussian coordinate projection. `MemLp.integrable_sq` then proves coordinate-square integrability. The vector Gaussian mean is zero; commuting the projection with the vector integral proves the coordinate mean is zero. `variance_eval_multivariateGaussian`, the actual covariance entry, and `variance_eq_integral` identify the coordinate second moment with lambda_i inverse. Although the variance rewrite itself takes only almost-everywhere measurability, the independently produced L2/integrability facts prevent a nonintegrable totalized-integral interpretation.

`EuclideanSpace.real_norm_sq_eq` expands the squared norm. Finite sums and real constant multiples of the coordinate-square integrands are integrable. The two uses of finite Bochner integral linearity, followed by the coordinate second moments, prove the actual norm and Q expectation identities. No independence or fourth-moment hypothesis is needed for these means.

The producer does not wrap an assumed desired identity. It builds the Gaussian moment bridge from canonical Mathlib facts and internally proved precision-domain facts. Its unused hd/hn/hnd binders retain the exact source range; the underlying analytic argument happens to work on a larger range. The only producer warnings are those three unused source-range binders.

## Private consumer, actual compiled uses and majorant

The private Test theorem begins with the actual producer result. Its Q-integrability and Q expectation equality are used in the final conjunction and composition, while the literal Gaussian remains the left-hand measure throughout.

The weighted inverse-spectrum series is handled as a scalar finite-grid/tsum exchange after the actual Gaussian mean has been obtained. C7 supplies the reciprocal-spectrum identity and absolute convergence. Bounded cosine weights give weighted absolute convergence. Product-to-sum, the exact all-integer midpoint alias identity, and the discharged low-mode guard give the two signed aliases. Natural j+1 is cast to Int before subtracting n; no natural-subtraction truncation is used. The factor two in the Fourier expansion cancels the product-to-sum half, yielding exactly d/sqrt(kappa).

The alias coefficient is normalized: `a(k)=(-1)^(k/(2d))` on 2d divisibility and zero otherwise. Its norm is at most one, including negative integer exponents. The proof establishes r>=0, computes the power norm, and proves the explicit absolute majorant `norm(F_j)<=2*r^(j+1)`. C7 at angle zero supplies summability of r^(j+1). `Summable.of_nonneg_of_le` then gives norm-summability and Summable F. These are outputs and are materially used, rather than displayed and discarded.

The actual compiled direct ASTIS parent set, derived from the fresh Test proof expression, is exactly:

1. `FixedSpectrumGaussianMoments.actual_diagonal_gaussian_quadratic_means`;
2. `FixedSpectrumCosineExpansion.actual_inverse_spectrum_cosine_expansion`;
3. `FixedSpectrumGridAlias.actual_midpoint_grid_cosine_alias`.

The producer has no ASTIS theorem parent. In the compiled consumer expression, the named proof binders hactual, ha_bound, hFmajor, hFnorm and hF are all used in their bodies. The detailed inspection records direct constant references, local proof closure, complete elaborated types and recursive axioms. This establishes actual local proof use, rather than merely source-name similarity or imports.

## Fresh isolated runtime and kernel evidence

Pinned Lean is 4.33.0, compiler commit `d8b18978322de05a8f3dba51ef03cf5461676c17`. LEAN_PATH was read through the actual Lake environment, then a private output overlay was prepended. All new producer/Test/probe oleans and ileans were written only under this phase's runtime overlay. No global Lake build or whole Tests command was run.

The focused fresh runs all exited 0:

| Run | Elapsed seconds | Log SHA-256 |
| --- | ---: | --- |
| Producer compilation | 4.415 | `e37e86fedc0fcd64d1b3929f464e7377c9ab79421d180452f2648b4c5945e52b` |
| Focused Test compilation after overlay completion | 6.110 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Independent persisted kernel/type/dependency inspection | 61.026 | `95ab0881277180e791363cb5a8add848ddbe20339947d19df775f8456278c44a` |
| Independent source-coordinate correspondence and API types | 4.973 | `029b6d733bebb5be255b740e25b66762b8de7b339881b3cc0073990dc5beb6b4` |

Every command has exact argv, cwd, LEAN_PATH, real UTC start/end times, exit code and output log digest in its runtime JSON. An earlier focused-Test attempt stopped before elaboration because Lean resolved the AutoSamplingTheory package at the overlay and expected reused C7/GridAlias cache files there. Copying only those hash-recorded cache files into the overlay corrected that isolated environment. The failed log is retained. Scratch inspection/data-output and notation/API mistakes are also retained separately; their failures were in reviewer tooling, not the immutable candidate. The final successful evidence is identified explicitly above.

C7/GridAlias and Mathlib were reused from existing caches, not freshly compiled in this review. Their source/cache hashes are recorded. The pinned Mathlib revision `db584cd6d46c92f209a44c0f1c829460d327499d` matches the dependency manifest. No claim is made to have freshly rechecked every imported library proof.

The independent inspection enumerated all 11 declarations belonging to the fresh producer and focused Test modules. All are theorems, and all values passed `Meta.checkWithKernel` plus inferred-type comparison. Recursive axioms are subsets of exactly `propext`, `Classical.choice`, and `Quot.sound`; no sorryAx or new mathematical axiom is present in the accepted target/module closure. The source closure scan found no sorry/admit/axiom or trivial/True closure.

Two generated `_proof` auxiliaries are in the private consumer's proof closure. Seven generated `_simp` specializations, for elementary nonzero/false simplifications, are not in the final theorem proof closure. They were nevertheless independently kernel/type/axiom checked. They are compiler elaboration products, not handwritten abandoned routes or public mathematical nodes, and receive no separate theorem credit. The source contains only the intended public producer and private consumer; no handwritten dead helper or wrapper-only theorem was found.

## Static reader review and limitations

All objects, parameter ranges, Gaussian law, coordinate convention and Q interpretation are stated in the authored assumptions. The five formula steps correspond to the checked domain proof, Gaussian moments, finite integrals, scalar Fourier exchange, and signed-alias/majorant calculation. The explanation correctly distinguishes Gaussian finite-integral linearity from scalar finite-tsum exchange. Its claim that the majorant is actually used agrees with the compiled proof.

The static progressive-renderer hooks were read without invoking a site scan/build: the statement disclosure is beside the mathematical claim, and the proof disclosure follows the mathematical steps. The disclosure takes exact declaration source, rather than the lesson's explanatory `lean_statement`/`lean_proof` prose, and emits closed details. Applying the exact split helper to this declaration preserves all five let definitions and separates only the outer proof assignment. The resulting exact statement/full-proof excerpts are frozen in this phase. This checks the static code path and content; no desktop/mobile/live DOM, graph branch, deployment or browser claim is made.

The result reuses canonical Gaussian/linear algebra/norm/integration APIs and the two existing ASTIS scalar nodes. The private consumer is a substantive Gaussian-to-Fourier composition. It remains private and does not imply any broader public downstream theorem has been admitted. Compiler-only simp artifacts stay out of the human-facing mathematical contribution.

No repair proposal is necessary or accepted. The separate canonical application proposal contains exactly the reviewed semantic slots, informational deltas, fidelity verdict and source_review payload, bound to this commit, v2 packet, publication binding and actual independent review-run artifact. Root may apply that exact proposal and run its separately authorized gates. This reviewer has not called a canonical API, changed an audit/ledger, set independently_verified, or performed source V.
