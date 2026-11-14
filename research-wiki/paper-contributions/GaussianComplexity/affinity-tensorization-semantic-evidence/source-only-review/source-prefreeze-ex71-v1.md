# Ex71: independent source expectations, frozen before exact seal

Status: `SOURCE_EXPECTATIONS_PREFROZEN`; exact-signature/binder/definition audit is pending. This is source evidence, not a Lean proof, a compiler receipt, or self-approval of graph coverage.

Source: *On Complexity of Gaussian Sampling*, arXiv:2610.20492v1, local raw HTML `.astis/huanjian-resume-20261103/2610.20492v1.html`, 951991 bytes, SHA-256 `6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915`. The HTML's own stable ID `A2.Ex71` is an unnumbered display in Appendix B.2.3, not an exercise number. Its raw lines are 2806–2823. The preceding product-density display is `A2.Ex70`; the following TV display is `A2.Ex72`.

Independence boundary: the mathematical expectations and topology below were reconstructed from that raw HTML before seeing a proposed Lean signature, implementation Lean, previous source reviews, or extractor conclusions. Only repository operating instructions and semantic-review protocols were additionally read. No shared frontier, ledger, source registry, or site truth is changed by this packet.

## Seven frozen semantic slots

| Slot | Frozen source expectation | Exact source anchors |
| --- | --- | --- |
| Objects | The two actual averaged Gaussian target laws `barπ_{+1}` and `barπ_{-1}`, constructed through the determinant-conditioned Haar priors `D_b`; the actual single-block Gaussian mixture laws `P_{+1}` and `P_{-1}`; their nonnegative Lebesgue densities `bar p_b` and `p_b`; the single-block affinity `a`. A theorem about freely supplied functions alone does not realize this source claim. | `S2.p2.1`, `S2.SS0.SSS0.Px1.p1.2`, `S3.E4`, `S3.E5`, `S3.SS1.p2.1`, `S3.SS1.p3.1`, `S3.E6`, `A2.SS2.p2.1`, `A2.Ex68`, `A2.SS2.SSS3.p3.1` |
| Domains | Euclidean `R^n` for a block, `R^d` for the actual averaged target, `R^(d-kn)` for a residual block only when `kn<d`; canonical Lebesgue measures `dx`, `dx_j`, `dz`. `d,n` are integers, `3≤n≤d`, `k=floor(d/n)`, and `κ≥4`. | `S3.SS1.p1.1`, `S3.E6`, `S3.SS1.p3.2`, `A2.Ex68`, `A2.SS2.SSS3.p3.1`, `A2.Ex71` |
| Quantifiers | For every permitted construction parameter choice, compare the pair of signs `+1` and `-1`. Within each prior all `k` orthogonal blocks share the same fixed sign `b` and are sampled independently from `μ_{n,b}`. The affinity integrates the *averaged law*, rather than averaging the affinity of individual Gaussian inputs. Density representatives may vary within their Lebesgue-a.e. equivalence class. | `S3.SS1.p2.1`, `S3.SS1.p3.1`, `S3.E6`, `A2.SS2.SSS3.p1.1`, `A2.Ex71` |
| Assumptions | The construction/standing assumptions above, together with the standard meaning of “density of” a probability law. Normalization, nonnegativity, measurability, absolute continuity and product-law identification must be derived for the actual objects or justified as the relevant standard library bridges. The factorization identity, Tonelli applicability, `∫φ=1`, an affinity bound, and Eq. (25) are proof ingredients, not new public hypotheses. | `S2.p2.1`, `S3.SS1.p1.1`, `A2.SS2.p2.1`, `A2.SS2.SSS3.p3.1–p3.3` |
| Conclusion | `∫_(R^d) sqrt(bar p_{+1}(x) bar p_{-1}(x)) dx = a^k`, with `a=∫_(R^n) sqrt(p_{+1}(x)p_{-1}(x)) dx`. Equivalently, the Hellinger affinity of the two actual averaged measures is the kth power of the affinity of the two actual single-block measures. This is an equality, not an upper bound. | `A2.Ex68`, `A2.Ex71`, `A2.SS2.SSS3.p3.3` |
| Scopes / senses | Nonnegative square root, ordinary finite real affinity integral, kth natural power. Product-density identities can be chosen pointwise for suitable source representatives; equality between arbitrary density representatives, including canonical RN representatives, is only asserted Lebesgue-a.e. The final numerical integral is representative independent. `kn<d` and `kn=d` are separate exhaustive cases, with the residual Gaussian absent in the equality case. | `A2.SS2.SSS3.p2.2`, `A2.Ex70`, `A2.SS2.SSS3.p3.2`, `A2.Ex71`, `A2.SS2.SSS3.p3.3`, `S3.SS1.p3.2` |
| Constant dependencies | Ex71 introduces no numerical estimate or universal constant. `a` depends on the actual single-block construction `(n,κ)` and the two determinant signs, while `k` depends on `(d,n)`; dependence on the ambient dimension enters through `k` and the normalized common residual factor, whose affinity contribution is exactly one. The constants `1/8`, `10` and the exponential bound belong to Eq. (25)/Ex72 and are not inputs to the identity. | `A2.Ex68`, `S3.SS1.p1.1`, `A2.Ex71`, `A2.E25`, `A2.Ex72` |

## Definition expectations

The objects form this semantic chain; none may be silently replaced by a function-level tensor product:

1. `O(n)={O : OᵀO=I_n}` has Haar probability measure. `μ_{n,b}` is that Haar law conditioned on `det O=b`. The source says each component has probability `1/2` (`S2.p2.1`, lines 645–652).
2. `A_O=((κ+1)/2)I_n-((κ-1)/4)(O+Oᵀ)` (`S3.E4`, 800–807). `π_A=N(0,A⁻¹)` is the actual centered target law (`S2.SS0.SSS0.Px1.p1.2`, 670–673).
3. For a tuple of `k` independent `μ_{n,b}` blocks, `A_boldO=diag(A_O1,…,A_Ok,I_(d-kn))` (`S3.E5`, 809–816). `D_b` is the law of this random matrix, not an independently supplied proxy (`S3.SS1.p2.1`, 819–822).
4. `P_b=E_(O~μ_{n,b})[N(0,A_O⁻¹)]` (`S3.SS1.p3.1`, 825–828). The averaging is an average of probability measures.
5. `barπ_b=E_(A~D_b)[π_A]=P_b^⊗k ⊗ N(0,I_(d-kn))` (`S3.E6`, 829–836); at `kn=d` both the identity block and final Gaussian factor are omitted (`S3.SS1.p3.2`, 837–838).
6. `p_O` and `p_b` are densities of those actual Gaussian/single-block laws (`A2.SS2.p2.1`, 2341–2348). `bar p_b` is a density of the actual `barπ_b` (`A2.SS2.SSS3.p3.1`, 2794–2797). No formula for a canonical RN representative is stated in the source.
7. `a` is literally the affinity integral in `A2.Ex68` (2754–2760). It is not defined to be the desired kth root of the ambient affinity, nor to be an arbitrary bounded scalar.

Literal constructions above require fidelity to their full meaning. Densities have `quotient/representative` semantics: equivalence is equality Lebesgue-a.e.; the observable affinity must be independent of representative choice. A canonical RN-based definition is acceptable only with the identifications described below, not as an extra source definition falsely attributed to the author.

## Author's proof topology

The proof paragraph explicitly invokes Eq. (6), gives the product density (Ex70), and then invokes Tonelli and normalization of the residual Gaussian. It evaluates the product of `k` identical block-affinity integrals as `a^k` (Ex71). It then states that the same identity holds with the Gaussian factor omitted when `kn=d`.

The source's two cases are:

- **Residual dimension positive (`kn<d`).** Eq. (6) → Ex70 → nonnegative square-root product algebra → Tonelli under the block/residual Lebesgue decomposition → `k` copies of Ex68 and `∫φ_(d-kn)=1` → Ex71.
- **Residual dimension zero (`kn=d`).** Eq. (6) with its explicit omission convention → product density without a residual factor → the same nonnegative square-root algebra and finite-product Tonelli argument → `k` copies of Ex68 → the same Ex71 identity.

These form a conditional **OR**: `(kn<d ∧ positive-residual route) ∨ (kn=d ∧ zero-residual route)`. Their union is exhaustive because the source fixes `k=floor(d/n)` and hence `kn≤d`. They are not one false AND requiring both `kn<d` and `kn=d`. The residual Gaussian normalization is required only on the first route. The source parameter range implies `k≥1`; no new public `k>0` premise is needed. A general library result may additionally handle `k=0`, but that extension is not part of the source's parameter range.

Ex68 defines `a`. The normalization/Cauchy–Schwarz paragraph supplies its ordinary finite probability-affinity meaning. Ex69's TV–affinity inequality, Proposition B.7 and Eq. (25) do not participate in the factorization identity. They feed the subsequent TV estimate. The source use-site direction is:

`Ex71 → Ex72`, `Eq25 → Ex72`, and `B7 + Ex69 → Eq25`.

There is no `Ex72 → Ex71`, `Eq25 → Ex71`, or `B7 → Ex71` edge. Source order alone is not proof necessity. The B.2.3 introduction describes the overall separation route; it does not make every earlier separation step an ancestor of tensorization.

## Source omissions and standard bridges

The inventory/graph marks these separately from the author's written proof. They supply no additional public convenience premise.

| Bridge | What the source gives | Required interpretation / expansion |
| --- | --- | --- |
| Actual Gaussian/mixture realization | Orthogonal family Eq. (4), actual Gaussian laws, definitions of priors and mixtures | Positive-definiteness, Gaussian absolute continuity, and measurable probability-mixture construction are background well-definedness obligations. The tensorization paragraph does not invoke the later regularity lemma or provide a new proof of them. They must be internally available for the actual objects. |
| Mixture density and RN identification | “`p_b` is the density of `P_b`”; “`bar p_b` is the density of `barπ_b`” | For canonical Lebesgue `λ_n,λ_d`, show `p_b = (dP_b/dλ_n)` and `bar p_b = (dbarπ_b/dλ_d)` a.e., interpreted in the chosen real/extended-real density convention. This follows from density/RN uniqueness and absolute continuity; it is `source-implied / library bridge`, not a distinct author proof. |
| Coordinate measure identification | Euclidean block coordinates `(x_1,…,x_k,z)` are used in Ex70/71 | Identify canonical ambient Lebesgue with product block Lebesgue under the standard coordinate concatenation (and its zero-residual specialization). A bare measurable equivalence is insufficient; measure preservation/normalization matters. |
| Product-density meaning | Eq. (6) and Ex70, with the zero-residual omission sentence | Obtain the product density of the actual law. For arbitrary RN versions the equality is a.e.; a chosen product representative can satisfy the displayed formula pointwise. The zero-residual density formula is implicit in “same identity,” rather than separately printed as a display. |
| Square-root/product algebra | Nonnegative densities and the displayed factorization | `sqrt((∏p_+)(∏p_-)φ²)=(∏sqrt(p_+p_-))φ` a.e.; the last factor uses `φ≥0`. On the zero branch omit `φ` entirely. |
| Tonelli and finiteness | Tonelli is named; all factors are probability densities | Measurability and nonnegativity justify product nonnegative integration; density normalization/Cauchy–Schwarz give finite affinity so real-integral and nonnegative-integral conventions agree. `IsProbabilityMeasure`, AC, measurability and integrability are discharged internally, rather than added as unexplained public binders. |
| Density representative independence | Source says “the density,” without selecting a representative | An a.e. density change leaves the square-root product integral unchanged. The source does not assert pointwise equality of all density versions. |

These are visible omitted bookkeeping/standard analysis, not a finding that the source needs an extra mathematical hypothesis. No source correction or repaired theorem is proposed here.

## Pending exact-seal audit criteria

The later binder/definition audit must expand every meaning-carrying project definition used by the exact signature. It must establish that the left side is the affinity of the actual averaged target and the base is the affinity of the actual `P_b` laws. It must check the full prior/precision/Gaussian/mixture definitions rather than accepting their names. A function-product provider can be an internal dependency but cannot alone be the source-facing result.

Classify the construction assumptions as `SOURCE`/`STANDING`, Euclidean carriers and sign indices as `TYPING`, and any producer result, identity-law premise, normalization/integrability premise or free affinity scalar admitted only to ease the implementation as `EXCESS` unless it is derived inside the actual source theorem. There is currently no `RULED` correction.

An implementation using RN derivatives must state and internally justify the actual measures' domination by canonical Lebesgue, use the correct real/extended-real convention, and identify the source densities a.e. Product splitting must preserve the ambient Euclidean volume normalization in both cases. The source anchor may use an equivalent reindexing of Euclidean coordinates, with the relevant measure-preserving bridge; it may not change the target law.

No Lean file, final signature or existing review has been read at this freeze. The binder verdict and definition verdict therefore remain `PENDING_EXACT_SEAL`, not “accepted.”
