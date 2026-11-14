# Independent candidate challenge before reading the author's phase-2 overlay

This successor preserves independent phase 1, freeze SHA-256 `0e6680aa5f2c9452f479f783d88da712fc5eba41a2703be41959f1c41ac1b930`, unchanged. It was written after disclosure of the original source graph and the four exact candidate/meaning files, but **before opening the author's candidate overlay**. The overlay's location/hash has been supplied; its contents have not yet been read.

This is pre-proof source/interface review. There is no proved new producer or consumer. The meaning fixture defines two propositions and prints/checks them; proposition formation is not a proof. No implementation, proof/API experiment, build, lifecycle operation, remote action, or shared metadata edit was performed by this reviewer.

## Exact reviewed endpoints

Producer `actual_first_order_query`: SHA-256 **452c547235344031f5f8c3035dc3f590a876741993c7ae9a1be2a7e129a948c1**.

Private actual consumer `actual_reference_precision_first_order_consumer`: SHA-256 **f0059bed1e49535a1dde0aba66a62bf371958bc8915d40a2b6c65c5df8366e4d**.

Candidate seal: **464ea7820b3545baa17669528532199017cf42a5255d6b2bfa88076c1b6992f0**. Meaning-only fixture: **1fa7e4ca83c3e15b636b85e52fbb5dc0b92e87bfb910109556f96e0b1c54818f**. Original source-graph phase-1 manifest: **756e51e694cd0d720e7b7fdec87d754292f4b8a109d080e41e9c3249d949a30f**; all 19 bound file hashes checked. Their correctness as mathematics is not inferred from those hashes.

## Independent seven-slot comparison

| Slot | Producer | Actual forward consumer |
|---|---|---|
| Objects | The explicit cosine-grid precision \(A=O\Lambda O^\top\), exact centered quadratic \(f\), and exact precision response \(Ax\). | A single same-\(O\) family \(A(\eta)\); actual \(A(2)x\) is the reference response; reconstructed \((\kappa-1)A(2)x-(\kappa-2)x\). |
| Domains | `Fin d` coordinates inside real \(\ell^2\) Euclidean space; matrix carrier is real \(d\times d\); `O` is in the full real orthogonal group. `WithLp` changes the type/norm presentation, not the coordinates. | The identical carrier and one `O`; `A` is a literal real-parameter family, not a second independently rotated family. Only its values at \(\kappa\) and 2 are used. |
| Quantifiers | For every natural \(d\), real \(\kappa\), and full-group \(O\), under the retained local inequalities, every \(x\), including zero. | Same order and all-\(x\) scope. No algorithm or seed quantifier, and no existential algorithm indexed by a publicly revealed \(O\). |
| Assumptions | Exactly `hd : 2 ≤ d`, `hκ : 2 ≤ κ`, and the typed full-group carrier. No gradient, symmetry, admissibility, reply-correctness, normalizer, integrability, or differentiability premise. **EXCESS = []**. | Same inputs. The affine reply identity and real gradient existence are not supplied premises. The consumer is forward only; no division or inverse/nonzero premise. **EXCESS = []**. |
| Conclusion | Genuine `HasGradientAt f (query x) x` AND actual `(f x, gradient f x)` equals the exact value/vector reconstruction. This is stronger semantically than a named numerical oracle definition, as required to interpret Eq. (1). | Genuine gradient at the reconstructed response AND the actual value/total-gradient pair at \(\kappa\) recovered from that response. The stated conclusion is a directional reconstruction, not full oracle-complexity equality. |
| Scopes/senses | §2 Eq. (1) states the value/gradient formula literally on the precision class; §4 supplies the literal fixed-spectrum family. C.4 provides the surrounding calculus setting but does not literally write the gradient formula. `HasGradientAt` is the Fréchet/Riesz meaning expansion of the source gradient assertion. | Remark 4.2 gives the same-rotation affine precision identity and either-reply determination; the candidate selects its **forward** algebraic consequence and combines it with Eq. (1)'s actual calculus/value semantics. No rounded, covariance, or hidden-eigenbasis reply is used. |
| Constant dependencies | The factor \(1/2\), zero additive constant, half-node grid, exact \(\pi\), and both appearances of \(\kappa\) agree. No \(\delta,\varepsilon,d_0,q,\tau\), random event, or absolute-error parameter appears. | The coefficients are exactly \(\kappa-1\) and \(\kappa-2\). At \(\kappa=2\), reconstruction is the original response. There is no reverse division and hence no necessary nonzero bridge in this directional closure. |

The zero-based angle is `((i.val : ℝ) + 1 / 2) * π / d`. Under the source reindexing \(j=i+1\), it is exactly \((j-1/2)\pi/d\); `hd` discharges the positive denominator when needed. The potential uses the coordinate dot product with the actual precision matvec divided by 2. It has no chosen/default branch, regularity gate, arbitrary offset, normalized log-density offset, or opaque project-owned predicate. The query is the actual full \(A x\), not \(A^{-1}x\).

## Definition semantics and required internal bridges

The permitted `Gradient.Basic` definitions show that `HasGradientAt` is a `HasFDerivAtFilter` assertion for the Riesz-dual functional at the point. The total `gradient` is inverse Riesz applied to total `fderiv`; its documented zero fallback does not by itself certify differentiability. Here the first conjunct requires real existence at every point. A future proof must connect that existence to the total-gradient value in the second conjunct. Neither a conveniently named response nor a default zero derivative can close it.

`Matrix.mulVec` is row-wise dot product; `dotProduct` is the finite sum of coordinate products. `EuclideanSpace ℝ (Fin d)` is `PiLp 2`, itself `WithLp 2` of real coordinates; `WithLp.toLp`/`ofLp` are the constructor/field. The \(\ell^2\) inner product sums coordinate inner products. A future proof must discharge the exact coordinate-dot/real-inner and transport adapters internally; these are typing/definition semantics, not analytic assumptions.

The orthogonal alias points to the unitary submonoid with both star-inverse identities; real matrices use transpose. There is no determinant-one condition. The local theorem therefore has the full-group scope frozen in phase 1.

The source-level closure is acyclic if separated as follows:

1. **Family meaning:** local domain + Eq. (11) + full-group interpretation yield the actual precision construction. Symmetry is internal algebra. C.4/Lemma 4.6 yield the bounds, which together with symmetry discharge §2's precision-class applicability when that source interface is specialized.
2. **Narrow actual-gradient producer:** Eq. (1) is the literal source formula anchor. The genuine gradient predicate needs a quadratic differentiation/Fréchet-Riesz expansion with symmetry internally discharged; real coordinate adapters connect it to the candidate `query`. This need not close the stronger bundled C-infinity/Hessian claim.
3. **Pair assembly:** the literal potential and exact real dot/inner identification, together with the actual-gradient result, produce the exact value/gradient pair. The pair is not defined in a way that assumes its own correctness.
4. **Forward affine bridge:** Eq. (11) at \(\kappa\) and 2, same \(O\), and Remark 4.2 yield the forward precision reply identity. Transport between coordinate and Euclidean carriers is internal.
5. **Actual consumer:** AND the producer at \(\kappa\) with the forward bridge to identify the reconstructed response with the actual precision response, then obtain both the real gradient and actual pair. There is no consumer-to-producer edge. The old compiled affine declaration is an intended internal provider identified by the parent/candidate, not a proof or use inspected by this reviewer. Actual compiled use must be checked after implementation; an import/name does not suffice.

The two full bidirectional FO expansions in the original source graph remain optional OR routes for their own broader bidirectional target. They are not necessary parents of this one-directional consumer. Both new existence and pair conjuncts are outputs of one actual-calculus contract, not two theorem assumptions. No Gaussian-integration, determinant, normalizer, public-spectrum, Krylov, target-moment, concentration, expected-cost, or main-theorem parameter node is necessary to these local endpoint closures.

## Frozen phase-1 challenge outcomes against the exact candidate

| ID | Independent candidate finding |
|---|---|
| TC01 | **Signature passes; annotation/graph correction required.** §2 Eq. (1) must be an explicit producer formula parent. The seal's broad “gradient formula inferred” wording must be scoped only to C.4; it must not erase the global literal formula. |
| TC02 | **Pass at statement level; proof open.** `HasGradientAt` is an output, with the actual standard gradient in the pair. No hidden project predicate substitutes an assumed gradient. |
| TC03 | **Pass at binder level; internal discharge required.** The actual conjugation is explicit. Symmetry and its use in real differentiation must be proved internally, not appended as a public premise. |
| TC04 | **Pass.** One `O` is captured by the family `A η`, so the independently frozen different-rotation counterexample is excluded. |
| TC05 | **Pass.** Full `orthogonalGroup`, all points including zero, and no event qualifier. |
| TC06 | **Pass.** The entire potential body is exactly zero-offset quadratic. The consumer recovers the actual value at \(\kappa\), with no unknown additive constant or \(\log Z\). |
| TC07 | **Pass.** Local `hd`, `hκ` retained; no main-theorem or query-statistic premise enters. |
| TC08 | **Scope excluded correctly.** Neither endpoint claims an algorithm cap or expectation theorem. Fixed-cap simulation obligations remain open outside this packet. |
| TC09 | **Pass in exact scope.** Real precision matvec and exact scalar operations; no finite-precision or bit-cost claim. |
| TC10 | **Pass in local scope.** The signature is a pointwise mathematical identity. It makes no algorithmic public-information claim or lower-bound assertion. |
| TC11 | **Pass for statements; sourcegraph narrowing required.** Normalizer/statistical branches are unnecessary. The bundled C-infinity/Hessian differentiation node must not be reported closed by the narrower producer. |
| TC12 | **Pass.** Correct half-shift reindexing and retained local endpoints. The current forward consumer needs no \(\kappa-1\ne0\) inverse bridge, even though the complete Remark 4.2 equivalence does. |
| TC13 | **Pass.** Definitions are literal total formulas. `A η` exists algebraically for all real \(\eta\), with no false positivity claim outside the theorem's domain and no fallback semantics. |
| TC14 | **Open implementation check.** The exact consumer is consequential: it recovers real \(\kappa\)-value/gradient from the reference response. Later proof review must establish actual use of the new producer plus the affine provider, rather than an unused import or counting wrapper. |
| TC15 | **Boundary retained.** Neither endpoint closes §4.4's uniform-Krylov obstruction or strengthens either main lower bound. |

## Original source graph: independent challenges to resolve in the overlay

The graph inventories Eq. (1), Eq. (11), C.4 and Remark 4.2 correctly at the raw formula level. Its `INF:gradient` truth boundary even acknowledges Eq. (1). However, edge `E026` gives `INF:gradient` only the stronger `INF:quadratic-differentiation` parent, which bundles C-infinity, gradient, and Hessian. The present endpoint is narrower. It requires a narrow existence/gradient elaboration node with Eq. (1)'s literal source-parent role explicit; it cannot award the entire bundled regularity node as closed.

`E046` correctly combines complete admissibility with Eq. (1) for the hard-family pair. The exact producer/consumer closure must retain the source-class applicability (bounds plus separately derived symmetry) internally whenever using this specialization route. This does not make membership a new public theorem hypothesis, nor does it require proving unnecessary spectral facts on a direct symmetric-quadratic implementation route.

`E047` assembles both affine directions and both scalar formulas for the broader `INF:fo-affine-transport`. This is valid scope for its bidirectional target but overbroad for the actual forward consumer. A separate directional consumer closure must not inherit `INF:affine-inverse-matvec`, `INF:affine-inverse-value`, or nonzero division. Likewise, a parent node which mentions Haar and the definition of \(A\) must be projected to only the deterministic construction/group information used here; Haar/seed independence must not become necessary conjuncts of local calculus.

This initial review finds **no blocking mathematical delta in either exact endpoint signature** and **no EXCESS binder**. It withholds final graph/interface admission until the frozen author overlay is separately checked against these independent requirements. All actual proof bridges remain open and must be discharged inside the later proof.

## Exposure candor

Phase 1 was frozen before any Lean/candidate/sourcegraph content was read. Phase 2 intentionally read only the four authorized candidate/meaning files and definition semantics, plus the author's original frozen source graph. A definition-location `rg` used an overbroad OR pattern and incidentally printed `WithLp`/`PiL2` lemma names and some local `rfl`/`simp` lines; the group-location search printed membership-lemma names; the authorized Matrix.Mul 696–705 window includes `mulVec_apply` and its `rfl`. The reviewer reports this exposure and does **not** claim complete Lean-proof blindness in phase 2. No gradient/calculus proof lemma or producer implementation was opened, no proof/API experiment was run, and the independent raw reading and 15 challenges predate every such exposure. Narrow carrier-definition reads followed the incident; the overbroad command was not repeated.
