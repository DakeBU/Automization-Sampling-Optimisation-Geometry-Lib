# Independent raw-source expectations: actual Ex70

Freeze version: `gc-actual-ex70-source-expectations-v1`.

Source: *On Complexity of Gaussian Sampling*, arXiv `2610.20492v1`, local snapshot `.astis/huanjian-resume-20261103/2610.20492v1.html`, SHA256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`.

This freeze was prepared from raw HTML before any exact Lean signature, implementation Lean, blind reconstruction, or previous review conclusion was read. Process instructions in `AGENTS.md`, `docs/proof-digestion-protocol.md`, `docs/evidence-routed-memory-protocol.md`, and `.agents/skills/astis-semantic-roundtrip/SKILL.md` were read. They are process evidence, not mathematical source inputs. No shared ledger or frontier was changed. No mathematical Lean was written. This document is the extractor's independent expectation, not self-approval of source topology, a Lean-proof claim, or a semantic-roundtrip verdict.

## Bounded source slice and exhaustive disposition

The bounded slice is the union of the entire Section 2 (`S2`), entire Section 3.1 (`S3.SS1`), and entire Appendix B.2 (`A2.SS2`). The broad B.2 inclusion makes the intervening determinant-cancellation and single-block-separation proof regions visible; they are explicitly excluded item by item from this minimal actual-Ex70 packet. Proposition B.7's statement is retained as an opaque upstream boundary only for the quantitative Ex72 consumer context. Its proof is not claimed covered or discharged by this packet.

`raw-source-inventory.freeze.json` classifies every paragraph, display group, formula occurrence (including inline definitions), heading, and citation/link occurrence as `NODE` or `EXCLUDED(reason)`, with raw HTML line numbers and source text. Display-group child formulas preserve all equality-chain rows. `raw-source-inventory.freeze.md` provides the paragraph/display/citation projection. Titles are excluded as navigation while their mathematical bodies remain classified. Every source definition receives the additional semantic registry below. A structural classification count is not mathematical approval.

## Source objects, domains, quantifiers, and conditions

1. `S2.p1.1`: the norm is the Euclidean norm. Real vector spaces have their standard Euclidean/Lebesgue interpretation. The source does not define a max norm carrier for this argument.
2. `S2.p2.1`: `O(n)={O∈ℝ^{n×n}:OᵀO=I_n}` carries Haar probability; each determinant component has mass `1/2`; for each sign `b∈{-1,+1}`, `μ_{n,b}` is the Haar probability conditioned on `det O=b`.
3. `S2.Ex1`, `S2.SS0.SSS0.Px1.p1.2`: `π_A=N(0,A^{-1})`, where `A` is a real symmetric precision matrix with `I_d ≼ A ≼ κI_d`. Oracle definitions and algorithm choices are not premises of a density identity.
4. `S3.SS1.p1.1`: fix real `κ≥4`, integers `3≤n≤d`, and `k:=⌊d/n⌋`. Therefore `k≥1`, `kn≤d`, and `r:=d-kn≥0`. A broader reusable theorem for arbitrary natural `k` and `kn≤d` can specialize to this source design; that generalization must not silently replace the actual source-facing anchor. The subsequent `n=2T+1`, `T≥1`, `2T+1≤d` are a main-theorem application and are not required for Ex70.
5. For every `O∈O(n)`, `S3.E4` literally defines `A_O=((κ+1)/2)I_n-((κ-1)/4)(O+Oᵀ)`. The actual Gaussian block law is `N(0,A_O^{-1})`.
6. For a tuple `O⃗=(O₁,…,O_k)∈O(n)^k`, `S3.E5` defines `A_{O⃗}=diag(A_{O₁},…,A_{O_k},I_r)`. For each fixed sign `b`, `S3.SS1.p2.1` draws all `O_j` independently from the same `μ_{n,b}` and defines `D_b` as the law of that actual block matrix. Equal determinant signs do not mean the matrices are equal; the sign is fixed before the independent draws.
7. `S3.SS1.p3.1` defines the actual one-block mixture `P_b=E_{O∼μ_{n,b}}[N(0,A_O^{-1})]`. `S3.E6` defines the averaged target `barπ_b=E_{A∼D_b}[π_A]` and asserts its equality to `P_b^{⊗k}⊗N(0,I_r)` in block coordinates. This is a claim about the actual mixture laws, not an arbitrary pair of normalized functions.
8. `A2.SS2.p2.1`: throughout B.2, `n≥3`, `κ≥4`, and `O` is Haar on the full `O(n)`; `U:=O₁₁`. `p_O` is the density of the actual `N(0,A_O^{-1})`; `p_b` is the density of the actual `P_b`, for each sign `b`. These are not free density parameters unrelated to the Gaussian construction.
9. `A2.SS2.SSS3.p3.1`: `barp_b` is the density of the actual `barπ_b`. For the branch `kn<d`, `φ_r` is the standard Gaussian density on `ℝ^r`. Ex70 is asserted for all block coordinates `x_j∈ℝ^n` and residual `z∈ℝ^r`, for either fixed sign `b`:

   `barp_b(x₁,…,x_k,z)=(∏_{j=1}^k p_b(x_j)) φ_r(z)`.

10. `S3.SS1.p3.2` says that when `kn=d`, the identity block and final Gaussian factor are omitted. `A2.SS2.SSS3.p3.3` repeats the omission convention for the affinity identity. A zero-dimensional residual implementation is acceptable only with a proved unit-factor/one-point-volume identification, not by leaving the equality branch unsupported. The source does not cover `kn>d`.

There is no source premise asserting the product-density conclusion itself, coordinate-volume identification, block density integrability/normalization, Tonelli's conclusion, affinity multiplicativity, a mixture-density witness, or the desired actual-law identification. Such mathematical ingredients belong to dependency edges. Pure finite-dimensional type information is `TYPING`; the source parameter design and actual-family definitions are `STANDING`; an extra analytical or theorem-shaped public premise is `EXCESS` unless independently sourced or explicitly ruled.

## Definition semantics registry

| Definition/source anchor | Expected semantics and audit boundary |
| --- | --- |
| `S2.p1.1` Euclidean norm, identity, Loewner order | Literal conventions. A coordinate permutation between Euclidean spaces may be an isometry; the same map into an ordinary Pi carrier with its max norm is not thereby a Euclidean isometry. |
| `S2.p2.1` `O(n)`, full Haar, `μ_{n,b}` | Literal/characterized standard group probability and conditional component law. Must preserve full group versus fixed-sign law. |
| `S2.Ex1` precision class | Literal real symmetric spectral bounds. |
| `S2.SS0.SSS0.Px1.p1.2` `π_A` | Actual centered Gaussian with covariance `A^{-1}`; quadratic potential/oracle definitions are outside target. |
| `S2.Ex2` `TV` | Literal probability TV normalization `1/2∫|p-q|`; consumer context. |
| `S3.SS1.p1.1` `k` | Literal integer floor `⌊d/n⌋`, source family has positive `k`; no query-budget condition is imported. |
| `S3.E4` `A_O` | Literal precision formula over the actual orthogonal group. |
| `S3.E5` `A_{O⃗}` | Literal ordered block diagonal matrix and identity residual, omitted at `r=0`. |
| `S3.SS1.p2.1` `D_b` | Law of actual block matrix under independent sign-conditioned Haar draws. |
| `S3.SS1.p3.1` `P_b` | Actual Gaussian mixture measure, not a placeholder arbitrary law. |
| `S3.E6` `barπ_b` | Actual average under `D_b`; the product-law equality is asserted, not the definition of a substitute target. |
| `A2.SS2.p2.1` `U` | Literal `O₁₁`; excluded from minimal Ex70 ancestors since used only in single-block separation. |
| `A2.SS2.p2.1` `p_O` | A Lebesgue density of the actual Gaussian. The normalized precision formula is standard background, not explicitly a definition formula in this paragraph. |
| `A2.SS2.p2.1` `p_b` | A Lebesgue density of the actual `P_b`. The source does not supply a canonical representative in this paragraph. |
| `A2.SS2.SSS3.p2.1`, `A2.Ex68` `a` | Literal single-block affinity `∫_{ℝ^n}√(p_{+1}p_{-1})`; consumer context, not an Ex70 ancestor. |
| `A2.SS2.SSS3.p3.1` `barp_b`, `φ_r` | Densities of the actual averaged target and standard residual Gaussian; representative compatibility and reference volume must be audited. |

Definitions in the excluded B.2.1/B.2.2 derivations (`O_{S,S}`, the empty determinant, `D_i`, `h_λ`, `H`, `r`, `λ`) and Section 2 algorithm/query-complexity definitions remain visible as excluded formula/paragraph occurrences in the inventory. They do not become actual-Ex70 binders or prerequisites.

## Author's route versus omitted bridges

The author's explicit Ex70 route is exactly: the actual averaged target has product-law form by Eq6; hence the displayed product density. The source writes no intermediate proof. Its prerequisite construction is the actual block design and independent priors in Section 3.1. The source does not cite Cauchy–Schwarz, B.7, Eq25, affinity, Tonelli, or TV to prove Ex70.

The following `SOURCE_GAP` records mean omitted mathematical bridges, not a claim that the paper is false and not additional source assumptions:

- `SOURCE_GAP:eq6-independent-mixture-disintegration`: Eq6 is asserted after the block design. A complete derivation would identify the inverse/covariance of the block diagonal precision, Gaussian block independence including the identity residual, and averaging under independent priors. The source gives those ingredients but does not write that derivation. An already established faithful Eq6 can serve as an upstream dependency of this minimal packet; no new Ex70 binder is licensed.
- `SOURCE_GAP:coordinate-volume-identification`: pass between `ℝ^d` and `(ℝ^n)^k×ℝ^r` using the ordered block coordinates, with the standard Lebesgue volume pushed to the product of block and residual volumes. Dimension accounting is `kn+r=d`. This is a coordinate/measure identity omitted by the author. A proof using a measurable equivalence must prove the volume law. A linear equivalence or ordinary Pi's max norm alone supplies neither a Euclidean isometry nor the needed volume identification. A genuine Euclidean/L2 coordinate isometry or determinant-one coordinate permutation can discharge the appropriate statement.
- `SOURCE_GAP:product-density-and-representative`: product measures of the actual density-bearing laws have the nonnegative measurable product as density; transport that density along the coordinate map. Since arbitrary densities are only a.e. unique, pointwise Ex70 requires a compatible chosen representative. A theorem asserting that the explicit product is a density of the actual law, or an a.e. equality to an arbitrary density representative, captures the invariant source meaning. An unconditional pointwise equality for every arbitrary `barp_b` representative does not follow. This is a representation convention/omission to audit, not permission to choose a different target law.
- `SOURCE_GAP:zero-residual-bridge`: prove the no-residual branch directly or identify the residual `ℝ^0` Gaussian and its volume as one point with unit density/integral, then reconcile the paper's omitted-factor statement.
- `SOURCE_GAP:consumer-integral-identifications`: the source says Tonelli and Gaussian normalization for Ex71. Expanding this needs measurable/nonnegative actual densities, the product square-root identity, finite-product Tonelli, and the same coordinate-volume identification. These are dependency obligations inherited/proved for the actual densities, not public assumptions. They are downstream of Ex70.

These named bridges are source reconstruction evidence only. No claim is made that any present or future Lean implementation follows them, and no implementation-specific theorem names or routes determine this source graph.

## Actual consumer use sites and direction

| Producer | Consumer use site | Source use and discharged condition |
| --- | --- | --- |
| Actual Section 3.1 block design and independent priors | `S3.SS1.p3.1`, `S3.E6` | Product-law assertion for a fixed sign; independent draws are specified at `S3.SS1.p2.1`. |
| `S3.E6` | `A2.SS2.SSS3.p3.1` immediately before `A2.Ex70` | Explicit “By Eq. (6)”; positive-residual branch `kn<d` is stated there. |
| Density definitions + product-density/coordinate bridges | `A2.Ex70` | Actual-law density, with reference measure and representative compatibility as above. |
| `A2.Ex70` for both signs | `A2.SS2.SSS3.p3.2`, first equality in `A2.Ex71` | Replace both actual target densities by product densities, use common residual Gaussian and nonnegativity. |
| Tonelli + residual `∫φ_r=1` | `A2.SS2.SSS3.p3.2`, factorization and final row of `A2.Ex71` | Author explicitly names both; normalization is of the standard residual Gaussian. |
| `A2.Ex68` definition of `a` | Final row of `A2.Ex71` | Each identical block integral is `a`, giving `a^k`. |
| `S3.SS1.p3.2` omission convention | `A2.SS2.SSS3.p3.3` after `A2.Ex71` | `kn=d` branch has the same affinity identity with no residual factor; separate branch, not a missing case or an extra AND-premise. |
| `S2.Ex2` TV convention and probability normalization | First row of `A2.Ex72` | `TV(barπ_+,barπ_-)=1-∫min(barp_+,barp_-)`. The overlap identity is stated without a separate proof. |
| Scalar `min(u,v)≤√(uv)` for `u,v≥0` | `A2.SS2.SSS3.p3.3`, second row of `A2.Ex72` | Nonnegativity is supplied by actual densities. |
| `A2.Ex71` | Third row of `A2.Ex72` | Replaces actual averaged-law affinity by `a^k`. |
| `A2.E25` | Last row of `A2.Ex72`, explicitly referenced in `A2.SS2.SSS3.p3.4` | Raises the affinity upper bound to nonnegative integer `k` and applies the exponential power identity. |

For the consumer-only side route, `A2.Ex69` uses Cauchy–Schwarz and `∫p_+=∫p_-=1` in `A2.SS2.SSS3.p2.2`; `A2.E25` uses that relation and B.7 at `p2.3`, plus the stated scalar log bound at `p2.4`. Neither B.7 nor Ex68/69/Eq25/71/72 is an ancestor of Ex70. The positive-residual and zero-residual branches are case alternatives, not simultaneously required premises. No alternative author proof of Ex70 is presented.

## Frozen acceptance questions for the later exact seal

The exact-signature audit remains pending. Once the final signature and meaning-carrying definitions arrive, compare them to this freeze without changing it: actual Gaussian target and actual priors, sign quantification, `n/κ/d/k` scope, actual `P_b` and averaged target, exact reference volume, genuine coordinate identification, residual branch completeness, and density representative sense. Recursively expand every project `Prop`/structure/typeclass input. In particular reject a public actual-Ex70 statement that asks for its own product density, a free density/mixture identification, a normalization estimate, an affinity result, or a coordinate-volume theorem as an extra assumption merely because a producer exists.

A successful minimal packet may establish the explicit product as density of the actual averaged target in block coordinates, plus the actual coordinate-volume identification and source specialization to `k=⌊d/n⌋`. This freeze does not prejudge the exact Lean representation. Generic finite-product density infrastructure is reusable substrate, and the actual-family specialization is the source anchor. Compilation, independent topology review, statement-seal binder/definition audit, and semantic-roundtrip review remain separate future gates.
