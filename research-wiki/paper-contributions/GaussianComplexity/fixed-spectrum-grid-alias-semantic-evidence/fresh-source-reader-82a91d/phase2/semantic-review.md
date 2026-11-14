# Phase 2: independent statement-only semantic comparison

Reviewer: `source_reader_82a91d`, distinct from the root formalizer and the supplied blind decoder `/root/decoder_6c92f7`.

Decision: the anonymous producer and the independent blind reconstruction are mathematically equivalent to the raw source's all-integer finite-grid cosine identity, after the explicit finite-index relabeling. No blocking semantic delta was found. The anonymous private consumer is a faithful deterministic intermediate obtained by substituting that identity into the source's cosine-series formula; its explicit summability conclusion is justified by the source's absolute-convergence argument. This decision is restricted to the supplied statements and reconstruction. It does not certify proofs, actual compiled dependencies, a whole module, a reader lesson, or the whole of Lemma 4.5.

## Inputs and review order

My phase 1 source-only freeze remained fixed before these inputs were received: SHA-256 `caa5267d47d2e486901b3aef29db516317ad22573eb939a75b74e610637417bc`. It includes exact raw source slices and a complete reconstruction of Section 4.1, Lemma 4.5, and Appendix C.3.

At phase 2 I read only `phase2-inputs/selective-input.json` (raw SHA-256 `e836b608629197b217fa7be8c11fbc4c593e046ea5c77d99b073eee0a71185a3`) and its manifest (raw SHA-256 `30935de1cbda39b6ba163129590d041d30cd579fd08bace4b26285ff8d735f77`). I verified their hashes and the three embedded text hashes. Exact copies and exposure records are saved with this review. The full canonical packet with SHA-256 `e8cacf92f2d511b273fc78eb30e7da6126f673ff6fcc553b569881a206b0cbfc` remains a hash reference only; I did not locate or open it.

The input's `source.original_text` is an attributed restatement with implementation-representation commentary. I did not treat that commentary as raw source evidence: its mathematical claims were compared to the earlier frozen raw source reading. No implementation, proof, API, lesson, publication context, graph, prior semantic decision/repair, or runtime evidence was read. The packet declares decoder source blindness; this phase records that provenance without independently re-auditing the decoder's execution. Prior ambient filename exposure remains disclosed in phase 1; there is no zero-cue claim.

## Producer: seven semantic slots

| Slot | Frozen raw source | Anonymous producer and blind reconstruction | Finding |
| --- | --- | --- | --- |
| Objects | Midpoint angles `theta_i = (i-1/2)pi/d`; finite sum of real cosines at an integer mode `k`; signed aliases. | Literal local `theta : Fin d -> R` with `theta(i)=(i.val+1/2)pi/d`; sum of `Real.cos((k:R)*theta(i))`; conditional signed coefficient. Reconstruction gives the same explicit grid and sum. | Same objects after `i_source=i.val+1`. The grid is locally defined and cannot be supplied as an arbitrary function. |
| Domains | Standing integer dimension `d>=2` from Section 4.1; `k` is any integer. The alias witness `a` is any integer. Angles and sum values are real. | `d : N`, `hd : 2<=d`, `k : Z`; `Fin d` ranges over each index once. The quotient is in `Z`; the base and amplitude are real. Reconstruction explicitly retains these meanings. | Equivalent domains. A finite dimension is naturally encoded by `N`; the all-integer frequency, including zero/negative modes, is preserved. |
| Quantifiers | For each admissible dimension and every integer `k`, the formula selects the multiple-of-`2d` case or its complement. | `forall {d:N} (hd:2<=d) (k:Z)`, followed by a local grid definition and equality. Reconstruction uses that order. | Same scope and universal strength. Implicit `d` is still universally quantified. The alias case does not require a caller-supplied alias witness. |
| Assumptions | Dimension bound and the literal grid. No extra trigonometric, denominator, divisibility, or frequency-range premise. | Only `hd` is a logical premise; `theta` is a literal `let`. No sign/size/parity restriction on `k` and no producer-result premise. Reconstruction says the same. | No excess premise visible in the supplied statement. The omitted `kappa` is irrelevant to the identity: its grid is independent of `kappa`, and the C.8 proof states the identity for every integer `k`. |
| Conclusion | `sum_i cos(k theta_i)=d(-1)^a` when `k=2ad`, `a in Z`, and zero when `k` is not a multiple of `2d`. | `(d:R)*(if (2*(d:Z)) divides k then (-1:R)^(k/(2*(d:Z))) else 0)`. Reconstruction expands precisely those two cases and the corresponding even/odd alias amplitudes. | Equivalent. Since `d>=2`, `2d` is nonzero. On the divisible branch, integer division yields the unique alias witness `a=k/(2d)`. Off that branch the real product is exactly zero. |
| Scopes/senses | Exact finite-grid equality, not approximate orthogonality; exceptional nonzero aliases alternate at multiples of `2d`. | Exact real equality using integer divisibility and integer powers. Reconstruction correctly treats negative alias exponents as inverse powers of the nonzero base `-1`, retaining parity. | Same sense. At `k=0`, the sum is `d`; at `k=2d`, it is `-d`; at `k=4d`, it is `d`. Negative opposite modes have the same value. Nonmultiples vanish. |
| Constants/dependencies | Literal `1/2`, `pi`, dimension `d`, alias period `2d`, amplitude `d`, base `-1`, and alias parity. No errors, limits, unspecified constants, or dependence on the spectral parameter. | Same literals, casts and dependencies. Reconstruction introduces `4` only in its equivalent description of even aliases. | No constant or dependency drift. In the angle `1/2` is real division; in the alias branch `k/(2d)` is integer division. |

The blind reconstruction's extra explanatory statements are valid consequences of the supplied identity: all odd integer frequencies are nondivisible by the even nonzero number `2d`; even frequencies may still lie outside the alias set. The reconstruction does not incorrectly identify all even modes as nonzero. Its negative-frequency discussion and parity reformulation do not enlarge the original domain or add a hypothesis.

## Private consumer: precise mathematical meaning

This is a universally quantified deterministic series statement. For `d : N` with `d>=2`, `kappa : R` with `kappa>=2`, and `n : N` with `1<=n<d`, it defines the literal midpoint grid, the source eigenvalues

`lambda_i=(kappa+1)/2 + ((kappa-1)/2)cos(theta_i)`,

the source parameter

`r=(sqrt(kappa)-1)/(sqrt(kappa)+1)`,

and the dimension-normalized alias coefficient

`a(k)=(-1)^(k/(2d))` for integer `2d|k`, and `0` otherwise.

Writing the positive series index as `ell=j+1` for `j : N`, the conclusion has two conjuncts:

1. The real family `(-r)^ell (a(ell-n)+a(ell+n))`, `ell=1,2,...`, is summable.
2. Its sum gives the deterministic weighted grid expression:

   `sum_i cos(n theta_i)/lambda_i`

   `= (d/sqrt(kappa)) sum_(ell>=1) (-r)^ell [a(ell-n)+a(ell+n)]`.

Here `ell` and `n` are cast into integers before subtraction. In particular, the `ell-n` argument can be negative; no truncated natural subtraction is used. The frequency alias coefficient is not restricted to positive inputs. The `Summable` conjunct is understood in the standard real-family sense, and the `tsum` is its real sum. For a real sequence this summability is absolute/unconditional summability, which is what the source's geometric domination supports. No extra definition context is needed to interpret this statement.

## Private consumer: seven semantic slots

| Slot | Source comparison | Finding |
| --- | --- | --- |
| Objects | Source C.7 expands `1/lambda_i`; `A3.Ex140` identifies the deterministic weighted sum underlying `mu_n`; `A3.Ex144` gives its product-to-sum expansion. The consumer uses the literal same grid, eigenvalues, `r`, and two shifted integer cosine modes, replacing each inner grid sum by `d*a(k)`. | Faithful deterministic representation. `a(k)` is the normalized grid sum, so the single `d` outside the series is required. |
| Domains | `d>=2`, real `kappa>=2`, positive integer `1<=n<d`, finite real grid, and positive integer series modes. | The consumer's natural `n` with `1<=n` represents exactly the source's positive integer modes. `j:N` with exponent/index `j+1` represents exactly source `ell>=1`; there is no extra zero series term. |
| Quantifiers | The source construction fixes `d,kappa`; the intermediate calculation holds for every admissible `n`. | The supplied statement quantifies in that order and defines its grid, spectral data, and coefficient locally. No caller-supplied `a`, eigenvalue sequence, or expansion witness can change their meaning. |
| Assumptions | The source's standing construction supplies `d>=2`, `kappa>=2`, and the lemma supplies `1<=n<d`. The series convergence and the grid identity are proved ingredients. | Those are the complete mathematical hypotheses visible in the consumer statement. Summability is a conclusion, not an added premise. No Gaussian moment or law assumption is required for this deterministic intermediate. |
| Conclusion | `A3.Ex144` states `(1/sqrt(kappa)) sum_(ell>=1) (-r)^ell [sum_i cos((ell-n)theta_i)+sum_i cos((ell+n)theta_i)]` for the weighted grid expression, after the base mode vanishes. The anonymous producer supplies each inner sum as `d*a`. | The equality is algebraically the source intermediate after that substitution. The factor 2 from C.7 cancels the product-to-sum factor `1/2`; the consumer correctly has neither an extra 2 nor an extra `1/2`. |
| Scopes/senses | This is an exact intermediate before splitting the three alias classes and evaluating their geometric sums. It is not itself the final exact moment formula. | The consumer claims only summability and the weighted grid-series equality. It does not assert a Gaussian expectation, a variance, the exact `1+rho^(2d)` closed form, positivity, a normalized mean ratio, an exponential bound, or any query/concentration result. |
| Constants/dependencies | The source's `1/sqrt(kappa)` normalization and dimension factor from the finite-grid identity remain. The parameter is the literal `rho_kappa`; mode shifts are `ell-n` and `ell+n`. | The prefactor is exactly `d/sqrt(kappa)`. All powers use the same `r` and positive exponent. Both signed shifts and the full integer alias period are preserved. No unspecified constants or error terms occur. |

The explicit `Summable` conjunct is a presentation expansion of a source proof ingredient, not an unsupported new mathematical condition: the frozen C.7 proof gives geometric absolute domination with `0<r<1`, while each literal alias coefficient has absolute value at most one. Thus the two-coefficient family is dominated by `2*r^ell`. This is the source convergence reasoning applied after the finite-grid identity, without any implementation or API assumptions.

The source's vanishing base term is valid at the consumer's inputs because `1<=n<d` excludes divisibility of `n` by `2d`. The statement itself need not take that vanishing as an input premise. Later proof review must check that it is actually discharged and that the producer is genuinely used in constructing the consumer; phase 2 cannot infer compiled use from a compatible statement.

## Deltas, issues, and decision boundary

| ID | Difference | Classification | Blocking? |
| --- | --- | --- | --- |
| P2-D1 | Source indices `1,...,d` become `Fin d` values `0,...,d-1`, with `i-1/2` becoming `i.val+1/2`. | Equivalent finite-index representation. | No. |
| P2-D2 | Source's alias witness `a in Z`, `k=2ad`, becomes integer divisibility plus quotient `k/(2d)`. | Equivalent conditional representation, since `2d>0`. | No. |
| P2-D3 | Source integer parity at negative aliases is encoded by real integer powers, including negative exponents. | Equivalent parity semantics on the nonzero real base `-1`. | No. |
| P2-D4 | The private consumer states the deterministic weighted sum directly, without a Gaussian variable or the name `mu_n`. | Faithful narrowing to `A3.Ex140`/`A3.Ex144`'s deterministic intermediate. It must not be presented as the whole moment lemma. | No at the supplied scope. |
| P2-D5 | The private consumer replaces the two inner finite cosine sums by normalized alias coefficients and moves their common dimension factor outside. | Equivalent substitution of the producer into the source intermediate. | No. |
| P2-D6 | The private consumer makes summability an explicit conclusion. | Source-supported expansion of C.7's absolute convergence; no new input premise. | No. |
| P2-D7 | A natural positive mode and a zero-based natural series index encode the source positive integer mode and `ell>=1` sum. | Equivalent indexing under the visible `n>=1` bound and the `j+1` shift. | No. |

No blocking mismatch or source-repair issue was found among the supplied statements. The appropriate producer verdict is **mathematically equivalent to the cited source identity**. The private consumer is **a faithful source-derived deterministic intermediate**, with the limited conclusion specified above. These decisions do not establish that an implementation proves those statements, that a current full-module context preserves their binders, that the expected actual dependency is present, or that a reader-facing exposition preserves this boundary. Those require the later immutable-candidate review.
