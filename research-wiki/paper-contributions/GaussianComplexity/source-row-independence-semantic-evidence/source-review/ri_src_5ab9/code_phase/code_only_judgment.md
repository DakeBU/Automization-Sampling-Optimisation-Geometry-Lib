# Independent current-code-only judgment — ri_src_5ab9, phase 3

Disposition: **no source-meaning or mathematical-applicability blocker detected
in the supplied bounded current code**. This static judgment covers the exact
producer, private consumer, actual older row-law provider, and the relevant
standard declaration bodies/types in the supplied copies. It supplies no
compiler/kernel result, completed round-trip verdict, source-VERIFIED state,
proof seal, publication status, or process-permission grant.

## Exact input boundary

The sole new manifest is
`../phase3-code-only-inputs-v1/input-manifest.json`, SHA-256
`7278908beb43ab9963a69deb4510baf4aee49d752d1c09073ae4d1ae3876e3d5`.
All eight complete copy byte counts and SHA-256 values match it. In particular:

- Full public producer P, 98 lines, SHA-256
  `f63b38ba191d22354f23cf7a518717f47be96728a72b2bb3c7fbd9292c47db86`.
- Full private consumer T, 81 lines, SHA-256
  `7f138451e328360e9dcf049f3de0b267693be622818781705fdf4c6521a33dd0`.
- Full actual old canonical row-law provider, 54 lines, SHA-256
  `c370caf377c5d56c97bdb1012d407049e63b04998011df327de79c46fb2b1201`.

I read those three whole modules. In the five larger supplied Mathlib modules
I read the declarations and surrounding parameter/instance contexts material to
this route; hashing their full bytes is not a claim to have read every unrelated
line. Their exact hashes are repeated in this phase's exposure manifest. The
Mathlib pin identified by the input is
`db584cd6d46c92f209a44c0f1c829460d327499d`.

The current producer signature (P12–20) and private-consumer signature (T11–32)
match the phase-2 sealed strings after whitespace normalization, without any
token changes. Their carriers, parameter scope, actual rows, cutoff, features,
matrix order and target outputs therefore retain the independently reviewed
type meaning. The earlier raw/type freeze files remain unchanged.

## Producer: the material joint-law argument

P40–43 applies `map_pi_eq_stdGaussian` to the physical coordinate space
`D=EuclideanSpace R (Fin d)`. The supplied Multivariate source at lines 137–143
states the entire pushforward equality

`map (WithLp.toLp 2) (pi (fun _ => gaussianReal 0 1)) = stdGaussian D`.

It is not only a collection of one-coordinate marginals. This matters because
`stdGaussian` itself is defined using `stdOrthonormalBasis`: the stated theorem
identifies that law with the full product in the actual physical coordinates,
and its supplied proof uses the full characteristic function. No unsupported
assumption that a chosen basis happens to be the physical basis is made.

P44–53 constructs the measurable unwrapping of each actual column. Rewriting
the complete coordinate-product law and composing unwrapping with `toLp`
returns the identity on the real coordinate array. Thus the claimed
measure-preserving map has the actual input column and the full scalar product
as target. P54–57 applies `measurePreserving_pi` to every actual column, yielding
the full `Q -> I -> R` scalar array law, not merely per-row laws.

P60–77 then carries this *same* array through three explicit transformations:

1. `(curry Q I R).symm` sends the column-curried array to an array indexed by
   `Q x I`. `infinitePi_map_curry_symm`, specialized using
   `infinitePi_eq_pi`, gives the finite product equality needed here.
2. `measurePreserving_piCongrLeft` uses `Equiv.prodComm Q I : Q x I ≃ I x Q`.
   Its supplied type sends a product indexed by the equivalence's domain to
   the product indexed by its codomain. The scalar measure is constant, so the
   reindexed source measure is the required same scalar product. The output
   entry at `(i,a)` is the original entry at `(a,i)`.
3. `curry I Q R`, with `infinitePi_map_curry` and the same finite specialization,
   regroups the scalar array into the row-curried `I -> Q -> R` law.

The explicit `transpose` type is `x |-> (i |-> (a |-> x a i))`, so neither a
column/row index reversal nor a replacement coupling is hidden in the route.
P78–86 wraps each regrouped row using the same complete
`map_pi_eq_stdGaussian` theorem. The resulting `actual_joint` map is exactly
`omega |-> (i |-> row i omega)` on the original `Omega`, and its target is the
product of the standard `E`-Gaussian laws over all physical rows.

P89–96 uses the supplied
`iIndepFun_iff_map_fun_eq_pi_map` in the correct direction. That theorem requires
the row maps to be a.e. measurable and the underlying `mu` to be a probability
measure. The actual older provider supplies the exact row map's
`MeasurePreserving` result, hence its a.e. measurability and exact marginal
pushforward. Its marginal equality rewrites the factors in the already proved
*joint* product equality. Marginals alone do not establish the independence:
`actual_joint`, built by the full-array transformations, is the indispensable
additional content.

## Exact old provider reuse

Both P37 and T56 call the same fully scoped
`FixedSpectrumSourceRowLaw.actual_source_row_marginal_law` with exactly the same
`d,q,hq`. The supplied provider's statement has the same canonical `Omega`,
`mu`, and actual coordinate row, and outputs `forall i, MeasurePreserving
(row i) mu (stdGaussian E)`.

The whole provider was checked statically: it obtains the physical coordinate
law from the full `map_pi_eq_stdGaussian` equality, uses the normalized product
evaluation law for that coordinate, collects it across actual independent
columns with `measurePreserving_pi`, and wraps the resulting row. Its
measurability output is part of its actual `MeasurePreserving` conclusion,
not a separately assumed certificate. This phase does not independently
recertify that existing declaration's compiler or historical source status.

## Private consumer: actual local matrices and both outputs

T48–54 defines a separate deterministic function `F i` of one Euclidean row and
sets `Y i omega = F i (row i omega)`. The retained entry at paired indices
`u=(a,j)` and `v=(b,k)` is exactly

`(d:R)^(-1) * ((x a * x b) * (t i j * t i k))`.

The Gaussian coordinate is first and the feature coordinate second in both
pairs, preserving the source's Gaussian-first Kronecker order. The branch is
exactly `norm x ^ 2 <= L`, includes equality, and outside it returns the zero
matrix. This uses only row `i`; neither the sample law nor all rows are cut off
by a common event. `L`, the midpoint grid, and feature zero/frequencies remain
exactly those in the sealed type/source freeze. No iid-matrix conclusion is
introduced; `F i` is allowed to vary with `i` through `t i`.

T61–65 proves coordinate-map measurability and the measurable closed threshold
set. T66–75 proves `F i` measurable into the explicit finite real-entry product
space: it applies `Measurable.ite` on that set, proves the retained branch by
two applications of entrywise `measurable_pi_lambda`, and exhibits each entry
as a product of two measurable row coordinates and fixed real constants.
The removed branch is measurable constant zero. The trigonometric features are
constants with respect to this row input; no extra random-feature
measurability premise is needed.

T76–79 supplies the two distinct target conclusions. For each actual `Y i`,
`F_measurable i` is composed with the actual older provider's *measurable* row
map. For independence it materially calls the new producer, then applies
`row_independent.comp F F_measurable`.

The supplied ordinary `iIndepFun.comp` type at Basic670–673 and its kernel body
at IndepFun197–206 require only a separately measurable function `F i` for each
index. The body applies the original full-family event factorization to the
preimages under these functions. It requires no injectivity, no identical
distribution, and no single common `F`. Thus the actual conclusion applies to
these varying local matrix functions, rather than to an artificial common
matrix surrogate. T's theorem remains private and contributes no additional
public source theorem credit by this review.

## Applicability and whole-module checks

The relevant standard declaration requirements are satisfied in the intended
concrete instances:

| Standard ingredient | Actual applicability |
| --- | --- |
| `map_pi_eq_stdGaussian` | Both physical and row coordinate index types are finite; both spaces are real finite-dimensional Euclidean spaces with their standard Borel structures. |
| `isProbabilityMeasure_stdGaussian` | The supplied Multivariate72–73 instance applies to those Euclidean Borel spaces. |
| `Measure.pi.instIsProbabilityMeasure` | Supplied Pi310–312 supplies probability for `mu` and finite nested scalar products from probability factors. Scalar `gaussianReal 0 1` is the standard probability Gaussian; no caller probability hypothesis is introduced. |
| `measurePreserving_pi` | Supplied Pi908–919 requires sigma-finite target factors. The target scalar product measures and target Euclidean Gaussian measures are finite probability measures, hence sigma-finite. |
| `measurePreserving_piCongrLeft` | Supplied Pi712–734 requires finite source/codomain index types and sigma-finite factors, all supplied by the finite paired indices and scalar probability law. |
| `infinitePi_map_curry(_symm)` | Supplied ProductMeasure523–563 requires probability scalar factors. Finite `Q,I,Q x I,I x Q` allow every `infinitePi_eq_pi` replacement. No infinite-array, countability or ambient-space theorem is being asserted as the target. |
| `measurePreserving_eval` | Supplied Pi401–407 uses probability factors, matching the old provider's normalized scalar product. |
| Joint-product characterization | Supplied Basic860–883 requires finite row index, canonical `mu` probability, and a.e. measurable actual rows; the old provider discharges the last internally. |
| `iIndepFun.comp` | Supplied Basic670–673/Kernel197–206 permits index-dependent measurable row functions; T supplies those functions and their measurability. |

The auxiliary standard `infinitePi` definition contains an off-probability
default, but here only its probability-factor theorems and finite-product
identity are used with standard probability Gaussian factors. That external
implementation branch does not introduce off-source target definitions.

The full P/T/provider modules contain no scoped assumptions beyond their
displayed natural parameters and source range, no local measurable-space
instance overrides, no hidden `letI` certificate, and no source-changing
definition aliases. `noncomputable section`, `classical` and
`autoImplicit false` do not add mathematical premises. Their visible proof
bodies contain no `axiom`, `sorry`, `admit`, or fake closure. There is no
`q>0`, `tau`, `kappa`, Gram, norm, moment, tail, or concentration assumption;
`q=0` remains included.

No claim goes beyond the canonical column experiment, the actual finite row
maps, and the actual row-local finite real matrices. Main paper bounds,
measurable-map transfer to arbitrary ambient experiments, source completeness,
global canonicality/duplicate search, and the compiler's acceptance of tactics
or definitional conversions remain outside this review.

## Freeze barrier

No standard declaration outside the eight supplied copies was needed for this
bounded static source/applicability judgment. No compiler/kernel receipt,
decoder artifact, exposition/lesson, old audit, other-agent graph or verdict was
opened. The next phase remains a separately supplied fresh anti-anchored packet
after independent anonymous decoding; it is not replaced by this code audit.
