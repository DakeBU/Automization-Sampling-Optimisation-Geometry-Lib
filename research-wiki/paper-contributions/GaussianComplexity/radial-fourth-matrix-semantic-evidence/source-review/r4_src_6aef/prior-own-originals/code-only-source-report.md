# Independent whole-module code-only source review

## Judgment

Accepted as a static whole-module mathematical/source review of the exact
producer and private consumer below. No blocking source mismatch, excess
premise, integrability/default-integral shortcut, incorrect square, PSD-order
error, lost q=0 boundary, or unused producer conclusion was found.

This phase does not assert successful Lean elaboration, compilation, axiom
checking, normal independent verification, publication correctness, or a
semantic-roundtrip verdict. No compiler result, proof history, decoder,
exposition, source map, graph, other review, or prior packet report was
opened. The interpretation is compared with this reviewer's own already
frozen source and type readings. No pristine-API claim about the proving
worker is made or required by this static judgment.

## Exact inputs and complete-module inventory

The input manifest is
`code-only-inputs/input-manifest.json`, SHA-256
`8c52fb6dbf45cb74dbfdae923ff1a54fc0062781958d7ae4caa84a5bcae9c006`.
All five supplied copies were hash-checked before reading. The two reviewed
modules were read in full, including their imports, options, scopes,
namespaces, comments, statements, and complete proofs:

| Role | Exact whole-module SHA-256 | Complete lines |
| --- | --- | --- |
| Producer, FixedSpectrumRadialFourthMoment.lean | `346fc4b30dd5252f422c803eb7f77160cf7657dabe74c67fc8f23de1d5e674f6` | 1–190 |
| Private consumer, GaussianComplexityFixedSpectrumRadialFourthMoment.lean | `9bb4d6223404f1d96a262d0d8c85a1c2edab31dae3cb6fc949a6d5abbbec2f24` | 1–160 |

The producer has exactly one public theorem and no additional public or
private declaration. All proof helpers are local have/let expressions.
The test module has exactly one private theorem and no extra declaration.
Both use `autoImplicit false`; neither adds a scoped variable, custom
instance, assumed law, opaque result, axiom, placeholder, or fake closure.
Their exact signatures match the separately reviewed signatures after
whitespace normalization. There is no interface change hidden in the
proofs. The global matrix norm scope is the previously reviewed L2 operator
norm in both modules.

The canonical ASTIS scalar provider was read completely, lines 1–93,
SHA-256 `c3576c191c2fa7bafcdc2a30c5731d0ea60c88e96be9e58e52ae09e33013b65c`.
The supplied pinned Mathlib Gaussian Multivariate and Fernique modules were
also read completely. Their hashes are respectively
`1fec35cf781da1009c37db80a96b05d70f2296ca7768e19bfc0b6314c9b43d49` and
`86660bae117cac863b46dd7205f3161908b42a8cc5ba65ebd52a7a98e3d723a6`.
No alternate ASTIS module, earlier packet report, or source mapping was used.

The Mathlib checkout reports exactly
`db584cd6d46c92f209a44c0f1c829460d327499d`. Bounded additional canonical
API intervals used to check specific operations are preserved with exact
paths, line intervals, Unicode/UTF-8 byte locators, and hashes in
`code-only-review/additional-api-manifest.json`. Their containing files are
checked byte-for-byte against that git revision, not merely against the
working-tree revision label.

## Producer: integrability is proved before matrix expectation

The relevant complete proof is lines 35–188. Its construction has the
following dependency order:

| Lines | Mathematical content |
| --- | --- |
| 37–44 | Literal Euclidean Gaussian law, squared radius, rank-one matrix, and scalar entries |
| 45–46 | Integrability of the fourth power of the Euclidean radius |
| 47–61 | Continuity and domination of every weighted entry by the fourth radius power |
| 62–70 | Finite-coordinate integrability and continuous linear transport into the L2 operator-norm matrix space |
| 71–78 | Entrywise evaluation of the established integrable matrix expectation |
| 80–103 | Off-diagonal entries vanish by a coordinate reflection preserving law and radius |
| 105–161 | Product-coordinate law, scalar power integrability, second/fourth moments and mixed square moments |
| 162–180 | Finite sum expansion of each diagonal entry, giving r+2 |
| 181–188 | Integrability conclusion and entrywise assembly of the exact matrix mean |

The radius-four integrability at lines 45–46 comes from the actual IsGaussian
instance for stdGaussian, together with Fernique's finite-moments theorem.
The finite-dimensional Euclidean space has the completeness, Borel,
second-countability, and normed-space properties required by that API;
none is an arbitrary proposition binder. For every entry,

    |R(x) x_i x_j| <= ||x||^2 ||x|| ||x|| = ||x||^4.

The code proves continuity of the entry, the coordinate norm inequalities,
and nonnegativity of R before using integrable domination. It then uses
Integrable.of_eval twice to integrate the finite matrix of scalar entries.
The explicit continuous linear equivalence from function rows to the
operator-norm matrix space makes the norm/topology transport visible. It
does not silently treat a function norm as the matrix operator norm.

The integral-entry evaluation is therefore applied in an already
integrable context. Although some underlying transport theorems are also
valid for totalized integrals, the present proof does not obtain its matrix
identity from a nonintegrable default.

## Producer: exact fourth moment and law route

For i!=j, lines 83–95 define the coordinate-i sign flip as a genuine linear
isometry equivalence. It leaves R unchanged and negates the selected entry.
`stdGaussian_map` is exactly invariance under such an isometry. The
integral-map step uses measurability and the already established entry
integrability; the resulting I=-I yields I=0. No full-vector negation is
substituted for the required single-coordinate sign flip.

For the diagonal, lines 106–112 introduce the actual product law of
independent scalar N(0,1) coordinates. `map_pi_eq_stdGaussian` identifies
its pushforward through toLp 2 with the canonical Euclidean stdGaussian.
This is the law of the source gamma_i, not an arbitrary covariance law or
a radial conditional distribution.

Lines 113–121 establish integrability of every scalar power and each
coordinate power from the open exponential-integrability domain of the
real Gaussian. Thus the scalar and coordinate second/fourth moments below
are not nonintegrable totalized expressions.

Lines 122–131 obtain the scalar second moment one from the exact mean and
variance of N(0,1), and transport it through a product-coordinate
evaluation. Lines 132–138 similarly obtain the fourth moment three from
the canonical ASTIS scalar provider. That provider proves

    E[X^4] = 3 v^2 for X~N(0,v)

by differentiating the actual Gaussian MGF four times. Its required MGF
interior condition is discharged by the full exponential-integrability
domain of the Gaussian; the referenced MGF theorem has that condition
explicitly. Its intermediate derivative formulas yield 3v^2 at zero.
The caller independently has scalar fourth-power integrability before
using the value at v=1, even though the provider statement does not package
integrability as a conjunct.

The squared coordinate family at lines 139–141 is independent under the
product law. For distinct coordinates, lines 149–150 prove integrability
of the product of squares using independence and the two coordinate
second-power integrabilities. The corresponding product integral is one.
The coincident-coordinate case is handled separately as the fourth power,
with value three. The proof never asserts independence of a coordinate
from itself.

Finally, the Euclidean norm-square identity expands R as sum_k x_k^2.
Every mixed term is integrable before finite sum/integral exchange. The
sum contains one contribution three and q contributions one, so it equals
r+2 with r=q+1. This is precisely the source's diagonal calculation
3+(r-1), without introducing a natural-number subtraction endpoint.
The diagonal/off-diagonal results are assembled into (r+2)I. Both the
constant and unconditional expectation sense agree with Ex113.

## Consumer: actual source square and producer use

All consumer definitions at lines 38–60 are the exact literals audited in
the type phase: the source midpoint grid, distinguished constant feature
coordinate, closed radius cutoff, d^(-1) normalization, Gaussian-first
tensor order, and ordinary matrix multiplication. No feature-length bound
or previously proved PSD estimate is inserted as a premise.

The code defines S=sum_k t_i(k)^2, c=S/d^2, and the linear tensor map
A -> A tensor feature. Flipping kroneckerBilinear at the fixed feature
gives this order. Scaling that finite-dimensional continuous linear map
by c gives

    W(x) = (S/d^2) (R(x) G(x) tensor feature).

At lines 61–63, the consumer calls the exact producer with the same d,q,hq,
and its integrability conjunct is used to prove W integrable. At lines
144–146, the exact mean conjunct is passed through the same linear map.
Thus both producer conclusions materially affect the proof. The consumer
does not merely call the producer and then prove its goal independently,
nor assume the needed moment as an input.

Lines 69–80 prove both rank-one matrix square identities. The identity
G(x)^2=R(x)G(x) uses the actual Euclidean norm-square formula; the feature
square is S*feature. Lines 81–98 prove the pointwise function equality

    Y(x)^2 = 1_{R(x)<=L} W(x).

On the good set, the proof multiplies the scaled Kronecker matrices,
uses the Kronecker multiplication identity and both rank-one squares,
then checks the exact coefficient S/d^2 entrywise. Off the good set, Y=0
and its matrix square is zero. This is the algebra of source Ex114,
including indicator idempotence, the actual matrix square, and d^(-2).
The inclusive cutoff is retained through the set membership case split.

The good set is proved measurable from the continuous squared norm at
lines 64–66. Only after establishing the exact indicator equality does
the proof obtain integrability of the squared matrix at lines 99–101
from W integrable. This is a full matrix-valued integrability proof in
the same declared matrix topology.

## Consumer: PSD removal, integration, and exact mean

For every x, lines 104–116 express W as the nonnegative scalar c*R(x)
times the outer product of the actual tensor vector

    v_(a,j)=x_a t_i(j).

The scalar is nonnegative because S is a sum of squares, d^2 is
nonnegative, and R is a squared norm. The source standing hq excludes
d=0; there is no hidden positive-denominator premise. The cited
vecMulVec PSD theorem uses real conjugation, which is trivial here.
This proves PSD of W pointwise using the actual matrix entries.

The residual W-Y^2 is zero on the closed good set and equals W outside,
so lines 117–121 prove the PSD residual for all x. This is exactly the
source's removal of an indicator from a PSD expression. It is not an
invalid entrywise integration inequality.

Lines 124–138 independently establish that finite real PSD matrices form
a closed convex set in the declared matrix topology. The Hermitian part
is a closed equality set for the continuous star operation. Every
quadratic form is continuous in the matrix, so its nonnegative set is
closed; taking the intersection over all vectors gives the exact PSD
condition. Convexity follows from PSD stability under nonnegative scalar
combinations. The code does not replace the cone with only diagonal or
coordinate-vector tests.

Lines 139–141 apply Convex.integral_mem to the residual. Its probability
measure requirement is met by stdGaussian, its pointwise/a.e. cone
membership is established, and residual integrability follows from the
two already established integrabilities. Thus the cone integration step
has the necessary analytical hypotheses internally discharged.

Lines 142–155 compute E[W] by continuous linear tensor transport of the
producer exact mean. The scalar calculation gives

    E[W] = ((r+2) S/d^2) (I_r tensor feature) = upper.

Finally the proof applies integral_sub with both integrability proofs and
substitutes this exact mean into the integrated PSD residual. Its result
is PosSemidef(upper-E[Y^2]), in the correct source Loewner direction.
There is no use of the Bochner nonintegrable zero case, probability
renormalization, unproved matrix expectation, or assumed variance bound.

## Boundary and exact source credit

At q=0, the Gaussian and feature carriers each have one coordinate, the
feature equals one, and the diagonal finite sum gives three. The
off-diagonal theorem is only used under i!=j; no nonempty complement or
second coordinate is assumed. Mixed squares handle equality separately.
The consumer therefore reduces to E[d^(-2)x^4 1_{x^2<=L}]<=3/d^2.
There is no q>0 or r>=2 branch requirement in either complete module.

The producer corresponds to Ex113 with its source-implicit integrability
made explicit. The consumer realizes Ex114 internally and derives the
termwise PSD bound supporting the first displayed p14 aggregate
inequality. It does not prove the aggregate sum, the deterministic cosine
norm bound, cosine Gram identities, centered-square variance identities,
the final 2r(r+2)/d constant, matrix Bernstein, or Lemma 4.4. None of those
larger claims follows as source credit from these modules alone.

No kappa-dependent factor or free constant appears in the actual moment
or termwise bound. The unused hq inside the producer is a retained source
standing range, not a hidden mathematical restriction. The consumer uses
hq to instantiate that exact producer. No mathematical/source defect was
detected in these exact complete modules within the stated local scope.

## Preservation and later phases

All original source-only artifacts and all sealed type-only artifacts are
rehashed unchanged by the code-review sealing script. The new report,
structured judgment, extra API evidence, and manifest occupy only this
reviewer's neutral directory. No production source, queue, frontier,
canonical ledger, process permission, commit, push, or integration was
modified. No compiler command was run in this phase.

The later anti-anchored semantic packet and publication/exposition/map
review require separate exact inputs and a separate recorded judgment.
