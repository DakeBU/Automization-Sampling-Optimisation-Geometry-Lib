# Gaussian Talagrand preread44: typed analytic/API obstruction

This is an independent source-only preread. No44 theorem has been admitted, implemented or compiled. Root is the sole mathematical writer.43 is still awaiting independent source review; its eventual inequality is a downstream parent, not evidence that T₂ exists.

The exact SPHMC source is2609.06906v1, S2.Ex2/S2.p5.2 (pinned HTML physical652–661), S4.Ex8/S4.SS1.p4.2 (1289–1300), S4.E6/S4.SS1.p4.3 (1301–1314). It defines W₂² as the infimum of E‖X−Y‖² over all joint couplings. FIRST4.6 uses W₂(r_y,N(0,I))≤sqrt(E_r‖gradientρ_y‖²), followed by separate Lipschitz/moment bounds. The reference law is covarianceI, after the actual affine standardization (X−p)/sqrtη. This is not the original unstandardized RGO, whose reference noise has covarianceηI.

The needed transport direction is KL(r_y‖gamma), never KL(gamma‖r_y). W₂ is symmetric; KL is not. Gaussian T₂ is W₂(r,gamma)²≤2 KL(r‖gamma), equivalently W₂≤sqrt(2 KL). Thus eventual43's KL≤Fisher/2 gives W₂²≤Fisher with coefficient1. No dimension/eta factor enters this standardized step. A scalar varianceσ² reference would carry T₂ constantσ²; it is outside the proposed covarianceI leaf.

The paper names Talagrand and Gaussian LSI together but gives no citation at that invocation. Its general bibliography includes CHE26, Log-concave sampling (physical7517–7526). The repository-pinned August9 Chewi edition was fetched from author commit b3ad6e874119983ae5f689a3295df4cdb44b11a7 and verified against canonical SHA2569b454ccf44fe700081e13a766ae9cabb83c3530f5fdc532d59ac335f53652597. This edition is an exact background source; the current live author PDF was not substituted.

Chewi §2.1.1, book48–49/PDF60–61, defines T₂(C) on P₂ as KL(µ‖π)≥W₂²/(2C), and cites Exercise1.16 for LSI(C)⇒T₂(C). Example2.4.4, book69/PDF81, states the standard Gaussian LSI constant1. Exercise1.16, book46/PDF58, assumes a true Wasserstein gradient flow, a PL bound, convergence to the minimizer and a metric-speed bound; none is supplied by a scalar algebra wrapper. The static alternative is §1.4.2, book33–34/PDF45–46: exact entropy/Jacobian identity(1.4.3), convexity of −logdet, and Theorem1.4.5 imply canonical KL is1-convex for the Gaussian quadratic potential. §1.3.1, book20/PDF32, fixes P₂, all couplings and genuine optimal-plan existence. The book expressly calls the transport-calculus proofs intuitive sketches; omitted regularity must be supplied internally.

The minimal source-domain target is a proposed genuine shared leaf, not Lean code:

> For any finite complete real Hilbert/Borel E, any probabilityµ with Integrable(‖x‖²,µ), let gamma=stdGaussian E. Then actual WassersteinSpace.wassersteinDistance(µ,gamma)²≤(2:ENNReal)·InformationTheory.klDiv(µ,gamma).

The moment premise is the textbook P₂ domain, a real analytic domain rather than a bound certificate. The extended-valued target needs no public finite-KL or AC assumption: if KL=∞ the RHS is∞; in the finite branch the pinned canonical API gives AC and llr integrability. For FIRST the actual standardized RGO moment is a previously existing paper dependency, not a new assumption to be charged to the paper. Root reports actual31 provides the required Fisher/moment bound;31's proof was not read or duplicated. Removing the P₂ premise would be a separately reviewed extension: finite Gaussian KL should imply the moment via an exponential-moment/entropy argument, but that argument has not been established here.

Keep ENNReal in the primary target. A real-valued corollary may use KL.toReal only after KL≠∞, and W₂.toReal only after W₂<∞. Both finite moments plus actual Gaussian moments yield the latter internally. It is invalid to totalize an infinite W₂ or KL through toReal and claim a real inequality. Canonical klDiv is the actual Mathlib divergence; its finite-measure correction vanishes for probabilities. Its llr is an AE object and must not be differentiated.

Rank0 is retained: any probability on the one-point finite Hilbert space equals its standard Gaussian, so W₂=KL=0. Prove this internally, without Nontrivial E, dimension positivity or division bydimension. Canonical volume/Gaussian density has empty-product normalizer1. Positive-dimensional covarianceI is nonsingular; no singular positive-dimensional covariance variant is silently included.

Existing genuine substrate was found, but no T₂ producer:

- Transport.IsCoupling/transportCost and WassersteinSpace.quadraticCost/wassersteinDistance use the real marginal constraints and extended infimum. `wassersteinDistance_sq`, `wassersteinDistance_sq_le_lintegral_of_isCoupling`, `wassersteinDistance_comm` and finite-second-moment finiteness are actual local declarations.
- OptimalContinuousCost.exists_optimal_coupling produces a true minimizer from probability laws and a continuous nonnegative cost; it assumes neither an optimizer nor finite moments. QuadraticOptimalBrenierMap.exists_base_map_gradient_eq_of_quadraticOptimal identifies a genuine Rockafellar gradient map after an optimizer, AC and moments are supplied internally. It does not supply differentiability of that map or a density/Jacobian identity.
- IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity atη=1 identifies the actual covarianceI law with canonical-volume density, including rank0. Pinned Gaussian IsGaussian.memLp_id and isGaussian_stdGaussian support its finite moments.
- DisplacementPotentialEnergy proves the potential-energy half with explicit integrability. DisplacementJacobianEntropy has finite-matrix logdet leaves. DisplacementChangeOfVariables requires a measurable full set, an actual derivative, global monotonicity and PSD Jacobian. DisplacementEntropyPushforward requires the log-density/Jacobian AE identity and integrability. These are consumers, not actual Brenier regularity/density producers.
- GeodesicConvexity and GeodesicFisherTransport are abstract/scalar joins with caller-supplied geodesic convexity, first variation or score pairing. FisherTransport consumes KL²≤FI·W₂². None proves Gaussian T₂. The Probability/SDE cards expose contracts, not the missing gradient flow. Pinned Mathlib searches found Gaussian/KL/moment/measure tools, no Wasserstein/Talagrand producer. Scoped calculus/convex searches found no Alexandrov producer; this is a search result, not a universal absence theorem.

Typed blocker: **missing actual measure-level displacement entropy/regularity producer**, or, on the independent dynamic route, **missing genuine Gaussian flow/speed/dissipation/convergence producer**. An optimal coupling alone does not estimate its cost by KL. Passing optimal-map, differentiability, entropy-change or desired T₂ certificates into the public Gaussian leaf would replace the mathematical task with a consumer interface.

The static route is the narrower candidate given existing local transport substrate, in seven steps:

1. Split rank0 and KL∞; derive actual Gaussian density/moments and endpoint AC/domains in the finite branch.
2. Produce an optimal quadratic coupling and its actual Rockafellar gradient transport map internally.
3. Supply an actual AE differentiability/PSD-Jacobian theorem for that produced map on the convex effective interior, with measurable full sets. This is the first strictly smaller missing edge; existing positivity leaves assume stronger supplied smoothness.
4. Supply the actual displacement log-density change-of-variables relation and logdet/domain controls, including endpoint/approximation passage for finite-KL P₂ laws. This remains a separate missing edge; do not assume global C¹ Brenier regularity.
5. Join entropy displacement convexity with the exact Gaussian quadratic-energy chord identity, preserving canonical KL and finite domains: KL(µ_t‖gamma)≤t KL(µ‖gamma)−t(1−t)W₂²/2 for interpolation gamma→µ.
6. Use canonical KL≥0 and t→0+ to deduce W₂²≤2 KL, with the internally produced cost; no first-variation or flow is required on this route.
7. After independent44 admission and43 verification, apply to the same actual r and gamma, combine2×½=1, then take the nonnegative square root. Reuse31 for the separateη√d bound.

Steps3 and4 are explicit source/API obligations, not proved claims or a ready proof script. No source repair or extra paper premise is justified by this preread. T₂, FIRST composition, both main theorems and cost/full-reader/PURIFIED remain unproved here. Search/audit data, exposure and exact pins are recorded in the JSON packet. All actual leases close as the final filesystem operation.
