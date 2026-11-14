# Source-blind mathematical reconstruction

For every pair of nonnegative integers d and q satisfying 2q + 1 < d, let D be real d-dimensional Euclidean space and let E be real (q + 1)-dimensional Euclidean space, each with its Borel measurable structure. Let gamma_D be the centered Gaussian probability measure on D with identity covariance. On Omega = D^{Fin(q + 1)}, equip the tuple omega = (omega(a))_{a in Fin(q + 1)} with the product probability measure mu = product_{a in Fin(q + 1)} gamma_D. For each i in Fin d define R_i : Omega -> E by (R_i(omega))_a = (omega(a))_i for every a in Fin(q + 1). Then the entire family (R_i)_{i in Fin d} is mutually independent with respect to mu.

Explicitly, for every subset S of Fin d and every choice of Borel sets A_i contained in E for i in S,

  mu({omega in Omega : R_i(omega) belongs to A_i for every i in S})
    = product_{i in S} mu({omega in Omega : R_i(omega) belongs to A_i}).

Every S is finite. For S empty, the event is Omega and the product is 1.

## Objects

D = EuclideanSpace R (Fin d) is the space of each sampled vector. E = EuclideanSpace R (Fin(q + 1)) is the target space of each row vector. Omega = Fin(q + 1) -> D is the tuple space of q + 1 sampled vectors. gamma_D = stdGaussian D is the centered identity-covariance Gaussian probability measure on D. mu is the finite product of q + 1 copies of gamma_D. For every coordinate i in Fin d, R_i(omega) collects that coordinate from all q + 1 sampled vectors, in their index order. WithLp.toLp 2 only wraps this coordinate function as an element of E; its coordinates do not change.

## Domains

d and q range over the nonnegative integers. The hypothesis implies d >= 2q + 2, so d >= 2; q = 0 is allowed. The sample index a belongs to Fin(q + 1) = {0,...,q}; the row index i belongs to Fin d = {0,...,d-1}. A point omega assigns a vector omega(a) in D to each sample index a. Each R_i maps Omega into E. D and E carry the Euclidean/Borel structures, and Omega carries the product measurable structure. The probability measure is mu on Omega. Target events A_i in the expanded conclusion are Borel subsets of E.

## Quantifiers

The theorem is universal in d and q and in a proof hq of 2 * q + 1 < d. These are not existentially chosen dimensions. After these quantifiers, D, E, Omega, mu, and R are fixed by local definitions, not universally quantified arbitrary spaces, measures, or maps. Mutual independence quantifies over every finite selected set S of row indices and every choice of measurable target event A_i for each selected i. Because Fin d is finite, this includes all subsets of the full row index set and, in particular, the full family. There are no existential witnesses or additional free parameters.

## Assumptions

The explicit dimension hypothesis is 2 * q + 1 < d. The natural-number domains and the given definitions supply all remaining context: real Euclidean spaces with Borel structures, the centered identity-covariance Gaussian measure on D, and its q + 1-fold product measure. The maps R_i are exactly the coordinate-collection maps in the statement. The Gaussian and product-measure specifications are part of the construction of mu, not assumptions about an arbitrary measure that could be varied independently. No separate measurability hypothesis is present.

## Conclusion

The single displayed conclusion is iIndepFun R mu: full mutual finite-family independence of the E-valued row maps (R_i)_{i in Fin d}. It gives the selected-event intersection/product identity displayed above for arbitrary Borel target sets, and therefore includes the full d-member family, not merely pairs. The product factors in that identity are the individual probabilities under mu; they are not replaced in the statement by stdGaussian E probabilities. There is no separately stated marginal-law conclusion such as (R_i)_*mu = stdGaussian E, nor any assertion that the row laws are identical. The construction specifies standard Gaussian factor laws on D for the sampled vectors omega(a); that input specification must not be conflated with an explicit output law for R_i in E. There is also no separate output Measurable R_i, AEMeasurable R_i, or joint measurability assertion. Under the supplied definition, iIndepFun alone does not assert measurability of arbitrary maps. No such extra conclusion is added here.

## Scopes

All local definitions occur inside the universal d, q, hq scope. D depends on d. E depends on q. Omega uses q + 1 copies of D and therefore depends on d and q. mu is defined on this Omega using stdGaussian D in every factor. R is the entire indexed family Fin d -> Omega -> E, with a the target/sample coordinate and i the sampled-vector coordinate. The family-independence assertion is made under this particular mu. The hypothesis hq restricts the permitted dimensions but is not an argument of any coordinate formula or measure definition. The event-product quantifiers concern target sets for selected row indices only; they do not introduce another probability measure or a different family of maps. The theorem makes no assertion for dimensions outside its stated bound, and the reconstruction makes no claim about necessity or sharpness of that bound.

## Constant dependencies

The only dimension parameters are d and q, restricted by 2 * q + 1 < d. The numerals 2 and 1 in that bound and the offset 1 in q + 1 are fixed literal constants. The 2 in WithLp.toLp 2 is the fixed Euclidean exponent, not another parameter. gamma_D is determined by D, hence by d. E is determined by q. Omega, mu, and the indexed row construction are determined by d and q and the fixed real Euclidean/Gaussian structures. There are no additional universal, existential, unspecified, dimension-dependent, tolerance, tail, error, or asymptotic constants, and no quantitative estimate or constant-dependence conclusion.

## Evidence boundary

This reconstruction uses only the anonymous Lean statement and the five approved definitions in input.json. It does not identify a source, declaration, original theorem, intended proof, or source-facing fidelity verdict. The packet reports that the anonymous statement compiled; this run did not independently compile or inspect a proof.
