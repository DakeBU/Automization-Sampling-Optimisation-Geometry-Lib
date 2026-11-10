# Joint radial level law

In the [fixed-location calculation before Eq. (51)](https://arxiv.org/html/2611.05813v1#S6.SS1),
the level sums are formed from disjoint families of independent degree
fields. `RadialLevels.radialLevels_hasLaw` makes their exact joint product
law explicit on the actual unconditioned coefficient vector. The
construction uses one full deterministic location, its exact tails, the
literal shell quotients and the zero extension. A variance-zero factor is
a Dirac measure. No pairwise-only or independent-copy substitute is used.

The implementation regroups `jointCoefficientBlocks_hasLaw`, proves
measurability of the coordinatewise level evaluations, then identifies each
pushforward with `radialLevel_hasLaw`. The real-valued slot sum in the joint
signature agrees exactly with the cast of the natural slot sum in the
marginal by `Nat.cast_sum` and `Nat.cast_pow`. This is an internal bridge,
not a new public premise. There is no additional generic wrapper or new
Functor transport. The source's linear-feature → degree-law → grouped
level-law route and the Lean product-pushforward route are separate views.

The signature was sealed at `96a3ae437`.
Candidate `678f1751c` passed focused Tests
(3194 jobs), including exact marginals and mutual independence, with only the
three standard axioms. Canonical Cell, ledger and semantic audit record
review and integration separately; no Registry or online credit follows
from this handoff.

## Next real consumer

The actual weighted Gaussian sum and Eq. (51) exponential moment are
independently verified on `a672b8d23`; the cutoff envelope and its
spatial Gaussian integral are independently verified on `b72dca28e`
and `adebd3e20`. None is included in this release. The conditional §6.2
step depends on all earlier coefficient blocks and the gate measurability,
not just independence of the scalar H_i. The joint coefficient/location
measurability and exchange in Eq. (70) are also separate.

## Integration boundary

[PR #402](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/pull/402)
merged at `98425863` after all seven exact-head remote checks passed.
The actual tree is identical to the local accepted tree. Independent
postmerge purification accepted the exact proof, three reader moves,
adjacent Lean folds and module download without changes (Exposition Seal
`SLC-LSI-RadialLevels-Exposition-merge98425863-v1`). No conditioning,
multi-location or weighted moment credit follows from that merge.

GitHub Pages run [42695392378](https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/actions/runs/42695392378)
passed both build and deploy. The [proof page](https://dakebu.github.io/Automization-Sampling-Optimisation-Geometry-Lib/proofs/source-slc-lsi-radial-levels.html)
and live site data were checked at `98425863` (Registry 616).

On `feb6a20e`, the exact verified joint law, test and authored binding
are unchanged. The full Lean gate (Tests: 9648 jobs), whole site check,
publication, semantic, contributor, Frontier, exact graph and four-subject
browser tests passed. One Registry entry (616 candidate) and one theorem
reader are added. There is no joint-in-location, conditional, moment or
paper completion claim, and remote acceptance is tracked separately.
