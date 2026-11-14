# Independent exact-signature / definition audit

Audited seal: `GC-actual-product-density-Ex70-v1`, file `research-wiki/paper-contributions/GaussianComplexity/product-density-statement-seal.json`, raw SHA256 `eb015980dd1ad6dcc1c7d23ae3e8b95350e108fc806a74345617e451dbb5f10b`. The exact `lean_signature` hashes to `c0d36b866977a6f04fd7a9e63d02541c02370acec456ba69833592bcbf2362fe`, independently recomputed and matched. Declaration: `AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity.actual_product_density`.

Independent source expectations were frozen first in `source-expectations.freeze.md` (SHA256 `ac7da4da3569d2266545e470b55c24c580d45a79dc6870389f7f50a2c9e4c6f1`). The source graph and raw inventory were also written before the seal was opened. They remain unchanged. This audit uses the seal's exact signature and exact definition bodies; it does not use the seal author's draft audit as authority. No current project mathematical proof bodies, prior review verdicts, or blind reconstruction were read. The four exact-definition file hashes were recomputed by reading bytes only and all match the seal. Selected Mathlib public definitions/specifications were read after freezing to check notation and carrier/measure semantics, not to reconstruct author topology.

Verdict: **ACCEPTED FOR THE PREPROOF STATEMENT SEAL**, with no `EXCESS` public binder and no semantic blocker found in the supplied exact bodies. The statement expresses Ex70 through a specified actual density representative and explicitly proves coordinate-volume and normalization bookkeeping. This is a statement/definition verdict only: it does not certify any mathematical proof, discharge the source gaps, approve the source graph's own coverage, or stand in for the later independent semantic round trip.

## Recursive binder classification

| Public input | Expansion | Classification | Source justification |
| --- | --- | --- | --- |
| `{d n : ℕ}` | Two natural finite dimensions, with `d≥n≥3` supplied below | `TYPING` | Section 3.1 dimensions; source design has integer block count. |
| `hn : 3≤n` | Natural-number inequality, no alias | `STANDING` | `S3.SS1.p1.1`; repeated in `A2.SS2.p2.1`. |
| `hnd : n≤d` | Natural-number inequality, no alias | `STANDING` | `S3.SS1.p1.1`. |
| `{κ : ℝ}` | Real condition-number parameter | `TYPING` | Actual Eq4 scalar. |
| `hκ : 4≤κ` | Real inequality, no alias | `STANDING` | `S3.SS1.p1.1`; repeated in `A2.SS2.p2.1`. |
| `{b : ℝ}` | Numerical common determinant sign | `TYPING` | `S2.p2.1`, `S3.SS1.p2.1`. |
| `hb : b=1 ∨ b=-1` | A disjunction of two real equalities, no alias | `SOURCE` | Exact sign set `{-1,+1}`; the same `b` is used for all independent draws. |

There are no public project-owned `Prop` aliases, structures carrying assumptions, or assumption typeclasses to expand. `Matrix.orthogonalGroup` is the standard matrix-group carrier and its orthogonality restriction agrees with the source `O(n)`; this is a type-domain restriction on integration variables, not a free theorem-shaped premise. `Fin`, finite-product, Borel, Euclidean-space and decidable-index instances are canonical typing infrastructure. The explicit local matrix `MeasurableSpace := borel _` is a local definition, not a caller-supplied measurability hypothesis. Every other local item is a `let` definition, not a logical premise.

The floor block count is fixed by the signature as `d/n`, and residual dimension as `d%n`; with natural dimensions and `n≥3`, these equal the source `k=⌊d/n⌋` and `d-kn`. No query budget, `n=2T+1`, positive residual, `NeZero` residual dimension, integrability, normalization, mixture-identification or volume-preservation premise is present. The universal binder scope is exactly every source-admissible `d,n,κ,b` followed by the conjunction of conclusions.

## Exact meaning-carrying definitions

| Item | Independent audit of supplied body |
| --- | --- |
| Matrix Borel `letI` | Fixes the finite-dimensional source Borel measurable space for the matrix prior/kernel. Does not change the Gaussian target or add a premise. |
| `singleBlockPrecision` | Supplied body is exactly `((κ+1)/2)I-((κ-1)/4)(O+Oᵀ)`, the literal Eq4 precision. The group subtype is source orthogonality. |
| `blockCoordinates`, signature `e` | Same formula in the sealed definition context and signature. `Equiv.prodComm` followed by Mathlib `finProdFinEquiv` sends `(i,j)` to `i+n*j`; `finSumFinEquiv` appends residual coordinate `t` after `(d/n)*n`. The final `finCongr` only changes a proved dimension equality. Thus blocks are contiguous and in the same order as Eq5; no alternate packing is hidden. |
| `blockPrecision` | `Matrix.blockDiagonal` has entries `M_j(i,i')` when block labels match and zero otherwise; `Matrix.fromBlocks` appends the residual identity, and reindexing uses the exact coordinate equivalence above. This is the literal Eq5 matrix. Its source support must be positive definite by an internal dependency; no such premise is asked of the caller. |
| `split` | Each selected block is converted with `WithLp.toLp 2` into a genuine Euclidean block; residual is Euclidean too. The outer block family remains an ordinary Pi, with its ordinary product/Pi volume. The statement asserts only measure preservation of `split`; it asserts no isometry into a max-norm Pi. Hence the source's volume-identification obligation remains a theorem conclusion rather than an invalid norm claim. |
| `orthogonalHaar n` | Supplied project body is `Measure.haarMeasure (⊤ : PositiveCompacts ...)`. Mathlib defines this Haar measure normalized on the specified positive compact, with `haarMeasure_self=1`. At the top compact of the orthogonal group it is full normalized Haar, matching Section 2. This pre-existing characterized object is used; no new unproved choice/fallback definition is introduced. |
| `ν` | Exactly `2 • Haar.restrict {det O=b}`. Because the two components have Haar mass `1/2` in the source range, this is the source conditioned probability `μ_{n,b}`. Half-mass, measurability, and probability are internal obligations/dependencies; their correctness is not assumed by a new binder. |
| `D` | Product of identical actual `ν` over `Fin(d/n)`, pushed through actual `blockPrecision`. This is the actual independent prior from Section 3.1, not a law defined by the desired product-density conclusion. |
| `γ` | `multivariateGaussian 0 A⁻¹`, whose supplied Mathlib body pushes the standard Euclidean Gaussian through the square root of covariance. For the actual positive symmetric precision support this is precisely `N(0,A⁻¹)`. Mathlib gives a total expression on ambient matrices; this audit attributes no off-source covariance meaning to non-positive/nonsymmetric matrices. The support/positive-definiteness and kernel-measurability facts needed under actual `D` remain internal dependencies. |
| `p` | Exact real normalized precision density `sqrt(det A_O)/(2π)^{n/2} * exp(-xᵀA_Ox/2)`, with the real exponent `n/2` and genuine Euclidean coordinates. No arbitrary density function is bound. Actual positivity of `A_O` in the source parameter range is an internal obligation. |
| `pb` | Literally `x ↦ ∫ O, p O x ∂ν`, a specified representative of the actual source mixture density. For every fixed `x`, the integrability that makes this Bochner integral an actual Gaussian average must be proved/reused internally. One must not rely on the total integral's nonintegrable fallback; no fallback branch was added to the definition. The signature uses actual `ν` and `p`, so it has not replaced the source `P_b` by an arbitrary pair of densities. |
| `φ` | Literal standard Euclidean residual Gaussian density `(2π)^(-r/2) exp(-‖z‖²/2)` for `r=d%n`, including the genuine zero-dimensional unit case. The formula is never fed a Pi max norm, since `z` is Euclidean. |
| `q` | Literal finite product of the specified actual `pb` and common `φ`. This defines a candidate density; the statement separately proves it is a density of the actual averaged target. It does not define the averaged target to make Ex70 tautological. |
| `volume` | On the ordinary Pi of Euclidean blocks, volume is finite product measure; on its product with residual Euclidean space, volume is the binary product. These are the expected product Lebesgue references. Mathlib's `PiLp.volume_preserving_toLp` confirms the separate Euclidean/Pi volume identification semantics; the supplied theorem still has to establish its own specific `split` volume law. |
| `ENNReal.ofReal` and `withDensity` | Standard nonnegative density conversion. Global `q≥0` is proved in the conjunction, so the actual density is not being altered by silently truncating negative values. |

The raw body hashes matched the seal for `DeterminantFamily.lean` (`10ea9afa…b78dd4`), `BlockFamily.lean` (`79661674…7d2df`), `OrthogonalHaar.lean` (`30f47e12…9a1de`), and Mathlib `Multivariate.lean` (`1fec35cf…d49`). Only the exact bodies supplied in the seal were used from the project files. Hash comparison did not expose/read their proof content.

## Conclusion correspondence and representative sense

The conjunction proves:

1. The exact source coordinate map preserves standard ambient and product volumes. This discharges the coordinate/reference-measure omission and adds no hypothesis.
2. The explicit product candidate is everywhere nonnegative, measurable, volume-integrable, and has mass one. These are the standard actual density properties, stated as bookkeeping conclusions rather than demanded as source premises.
3. `(D.bind γ).map split = volume.withDensity q`, identifying the density of the actual averaged target in the source's block coordinates.
4. `D.bind γ = volume.withDensity (q ∘ split)`, identifying the same actual target in ambient coordinates. This is the real consumer-facing link needed for integrals over ambient measurable sets.
5. If `d%n=0`, then `φ=1` everywhere on the zero-dimensional Euclidean residual. Together with the actual density conclusions, this realizes the source's omitted-factor branch. The standard zero-dimensional volume/probability identification still belongs to the proof dependencies.

The signature does not assert pointwise equality to every possible representative called `barp_b`. It chooses the raw actual `p_O` average for `pb` and then the literal product `q`, and proves the invariant law-density identity. This is the correct representative-aware reading of Ex70; there is no representative-strengthening defect. The standard normalized Gaussian density formula is background required to connect actual `p_O` to the source's density definition, not an additional source theorem assumption.

The ordinary Pi target has the correct product measure, and nothing in the signature claims it has Euclidean product norm. All `‖z‖` uses are on the Euclidean residual. The already explicit `MeasurePreserving split volume volume` is the required mathematical statement; a future proof must actually discharge it. A future implementation route may differ from the author's one-line “By Eq6” step and must retain its own route provenance.

Ex71 and Ex72 remain downstream only. This seal does not claim affinity tensorization, quantitative TV amplification, main-theorem lower bounds, oracle properties, or source-graph purification. No additional source repair is proposed. The only pending preproof gate external to this audit is the distinct raw-source topology challenge; all mathematical producer facts and the actual proof remain to be checked by the owning worker and subsequent independent verification.

## Mathlib semantic checks consulted after source freeze

The following public definition/specification regions were consulted solely to expand exact notation: `Logic/Equiv/Fin/Basic.lean` (`finSumFinEquiv`, `finProdFinEquiv`); `Data/Matrix/Block.lean` (`blockDiagonal`); `LinearAlgebra/UnitaryGroup.lean` (`orthogonalGroup` and its transpose identity); `MeasureTheory/Measure/Haar/Basic.lean` (`haarMeasure` normalization); `Probability/Distributions/Gaussian/Multivariate.lean` (`stdGaussian`, plus the `multivariateGaussian` body supplied in the seal); `MeasureTheory/Measure/Prod.lean` (product volume instance); `MeasureTheory/Constructions/Pi.lean`/`MeasureTheory/Measure/Haar/InnerProductSpace.lean` (Pi/Euclidean volume semantics). No alternative proof route was derived from these readings or retroactively attributed to the author.
