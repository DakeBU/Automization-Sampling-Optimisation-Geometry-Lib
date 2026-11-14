# Phase 3 frozen whole-module code-only source review

Reviewer: `/root/radial_cov_fresh_source_42df`. Date: 2026-11-11 (Asia/Tokyo).
Immutable candidate: `86c9bb627c61955f2a47f492c59a044230536739`.

**Verdict:** No blocking source mismatch or mathematical proof defect was found in the supplied complete producer and private-consumer modules. Their statements are byte-for-byte the exact Phase 2 signatures, and the proofs as written implement the source's radial-symmetry/trace argument and deterministic tensor expectation at the canonical single-row marginal boundary. The finite-integrability conclusions are genuinely proved. The private consumer materially uses both parts of the producer. No source repair or extra premise is indicated.

This is an immutable-code review against my own previously frozen raw-source and type readings. No compiler execution, execution receipt, candidate exposition, source map, decoder, graph, or other review was inspected. Consequently this is not yet final source verification, compilation certification, axiom-trace certification, or a ledger transition. The original-family row-law transport remains outside these declarations, as it was in Phase 2.

## Exact reviewed inputs

The sole new handoff index is `inputs.json`, 1625 bytes, SHA-256 `70bed00483f0f315542a4d02f5f925f749d9c7e3936be609ec2c116c796112f8`. Every supplied blob was rehashed before reading:

- Producer `AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumTruncatedRowMoment.lean`: 8719 bytes, SHA-256 `1a97dd98ecc4e3965db20a91c1d22ca8520406ea22cbbfbd631579522d071310`.
- Private consumer `Tests/GaussianComplexityFixedSpectrumTruncatedRowMoment.lean`: 4343 bytes, SHA-256 `0125f27884195dc6210ade46987373d0b4674ba067067a03d91dcd0d2828276e`.
- Existing supporting module `AutoSamplingTheory/TechnicalLemmas/Probability/StdGaussianMoment.lean`: 2764 bytes, SHA-256 `f87a1c18284dbe58658c3c312f1015fa2eec0b203d5a1187618e5f43ea2a6e00`.
- Pinned `stdGaussian_map` excerpt from Mathlib `Gaussian/Multivariate.lean`, source lines 128–135: 462 bytes, SHA-256 `23b56f9ef0361267b8b9cdfc0e399d7dd5bddf763de14dd5246f4bda58b6e456`. The index pins Mathlib commit `db584cd6d46c92f209a44c0f1c829460d327499d` and whole upstream file SHA-256 `1fec35cf781da1009c37db80a96b05d70f2296ca7768e19bfc0b6314c9b43d49`.

These exact bytes are snapshotted beside this report. I did not inspect the worktree versions, candidate prose or maps, or additional library files.

The extracted producer signature still hashes to `e231ce32f517936350efface8c277491562d1537dcc02441db6907410929ae05`; the extracted private-consumer signature still hashes to `0395f749c993cc8ebad7f71d3feb36a10c84543fb54fb35dabfe81a6ded54323`. Both string comparisons with the Phase 2 packet succeeded. My Phase 1 source report/manifest and Phase 2 review/manifest also rehashed unchanged.

## Producer: actual integrability and matrix meaning

Producer lines 21–33 retain the sealed natural d,q boundary, exact source cutoff, unnormalized coefficient a, closed event R<=L, real outer product, and identity matrix. There are no added covariance, symmetry, moment, boundedness, or expectation hypotheses. The body is local proof, not a theorem-shaped assumption bundle.

Lines 47–58 establish measurable retained event and integrable squared radius under the fixed canonical standard Gaussian. The only project-owned support call is the `.1` integrability projection of `StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian`. The source-facing target does not ask a caller for this fact. The retained scalar integral defining a is explicitly integrable at line 57; hence a is not being interpreted through Bochner's totalized nonintegrable zero branch.

Lines 53–75 identify each retained matrix entry with the literal indicator times x_i*x_j, establish its measurability, and dominate its absolute value by the retained squared radius. The argument uses |x_i|<=||x|| and |x_j|<=||x|| in the Euclidean domain. Inside the event the bound is ||x||^2; outside both sides are zero. It neither changes the event nor substitutes a probability-normalized function.

Lines 76–84 assemble the finitely many integrable entries into an integrable function of coordinate arrays and transfer it through `Matrix.ofLinearEquiv` as a continuous linear equivalence to the declared matrix codomain. This is meaningful for the actual real Euclidean operator norm from `Matrix.Norms.L2Operator`: finite coordinate integrability implies finite matrix norm integral, and the continuous equivalence performs the transfer. It is not a proof about a different silently substituted matrix norm.

Lines 85–92 transport the matrix integral back to its actual entries using the same continuous equivalence and finite evaluation integrals. The later entrywise calculation therefore proves the matrix-valued Bochner equality itself.

## Producer: radial invariance, cancellation, trace and coefficient

Lines 93–101 prove invariance of each integrated retained entry under a real linear isometry equivalence of E. The code invokes the actual `stdGaussian_map` theorem, gives the entry's almost-everywhere strong measurability under the mapped law from its proved integrability, and applies the map-integral identity. No invariance equation is a supplied premise.

The supplied upstream excerpt states map invariance for a linear isometry equivalence and proves it using equality of Gaussian characteristic functions and invariance of the relevant dual operator norm. This is the correct canonical standard-Gaussian symmetry result. Its role here is symmetry of one standard row law. It does not establish the original paper's joint-family row-law bridge.

Lines 104–125 build a coordinate sign flip at the first off-diagonal index. Its norm preservation leaves the closed radial event unchanged, while the selected product x_i*x_j changes sign because i!=j. Equality of the integrals before and after the flip yields a real number equal to its negative, hence zero. The index-distinctness condition is internal to the off-diagonal case; no assumption r>=2 is added.

Lines 128–145 build the coordinate transposition of i and j. The swap preserves the norm and retained event, and sends the squared coordinate at i to that at j. The same law invariance therefore equates all retained diagonal expectations. The construction also works when i=j.

Lines 148–159 show that the finite sum of diagonal entries is exactly the retained squared Euclidean norm, then legitimately exchange the finite sum and integral using the already-proved diagonal integrabilities. The trace is not replaced by an unretained or normalized radial quantity.

Lines 160–172 prove r>0 from q+1, identify the sum of equal diagonal expectations as r times any one of them, and divide by the positive r. The resulting diagonal value is the literal a=(integral retained R)/r. There is no dimension-dependent rescaling error. Lines 173–180 combine this diagonal identity and off-diagonal cancellation to obtain the exact matrix equality.

This is a faithful expansion of the source's “By radial symmetry” step: coordinate symmetries implement the invariant-matrix argument, and trace identifies its coefficient. The proof does not need the source's later scalar range bound, Ex109 tail bias, or a cosine frame identity.

## Existing squared-radius support

The complete supplied `StdGaussianMoment` module is mathematically consistent with this use. It obtains finite squared-norm integrability from the standard Gaussian L2 identity at lines 29–30. Its separate expectation formula uses zero mean and covariance identity along a standard orthonormal basis at lines 32–38, bounds the directional squares at lines 39–47, and applies finite-dimensional Parseval plus finite integral summation at lines 49–57.

The producer actually invokes only the integrability projection. The support theorem's additional expectation-equals-dimension conclusion is available in that existing node but is not used to smuggle E[R]=r or the target isotropy equation into the producer premises. In the scoped source argument, E[R]=r explains the adjacent a<=1 remark; it is unnecessary for identifying a by trace. No new higher moment or independence statement is asserted by the support module.

## Private consumer: material use and ordered tensor transport

The consumer's entire proposition at lines 20–38 remains the exact Phase 2 type. The midpoint formula `(j.val+1/2)*pi/d` corresponds to source row j.val+1. Its feature index is the zero-based frequency k.val. Frequency zero is exactly 1; positive frequencies have exactly sqrt(2)*cos(k.val*theta). There is no extra vector normalization. The first Kronecker index remains the Gaussian coordinate and the second the feature frequency.

Lines 57–62 form the literal feature outer-product matrix, the linear map A |-> A kronecker feature, and its scalar multiple by d^(-1). The flipped bilinear Kronecker map fixes its second argument, so the Gaussian matrix stays in the first factor. Finite-dimensional continuity gives a genuine continuous linear map between the actual operator-norm matrix spaces.

Lines 63–64 call the producer with these exact d,q,hq and recover both the integrability and equality for the exact retained matrix. Lines 65–71 prove pointwise that the source Y is the scaled tensor map applied to kept, including the zero branch of the retained indicator. This proof preserves the closed retained event.

The producer is materially used in all required ways:

- At line 76, `moment.1` supplies retained-matrix integrability to the continuous linear map, proving Y integrable.
- At line 80, `moment.1` justifies commuting that continuous linear map with the integral.
- At line 81, `moment.2` replaces the integrated retained matrix by a*I inside the same map.

Lines 82–85 then use linearity and scalar algebra to obtain exactly (a/d)*(I kronecker feature). There is no recomputation that bypasses the producer, no assumed expectation equation, no matrix sum, and no use of a frame identity disguised as this single-row application.

This is a private theorem in the Tests module. It supplies a concrete source-form application, not a new public reusable theorem or independently published source-family transport node.

## Endpoint, source parameters and scope

At q=0, the carrier is one-dimensional, r=1, the sole frequency is zero, and t_i=(1). The off-diagonal branch has no realizable distinct indices; the transposition/trace arguments and positivity proof still work. No part selects two distinct coordinates unconditionally. The consumer becomes the expected retained scalar square divided by d. The source hq gives d>=2. The proof never cancels a potentially zero source denominator: its only trace division is by the internally proved positive r, and tensor transport merely carries the literal d reciprocal. The source parameter restriction ensures that reciprocal has its ordinary intended value.

The proof does not separately need L>0 or the log argument's positivity, because Gaussian squared-radius integrability works for every finite cutoff and the indicator argument preserves the fixed source formula. Their absence as separate proof lemmas is therefore not an omitted source condition or fallback-semantic defect. hq stays in the public statement because it is the source standing boundary, although the local radial identity is mathematically more general.

The canonical-marginal limit is unchanged. Neither module constructs the original random starting vectors g_1,...,g_r, defines their rows on the original experiment, proves those row pushforwards equal stdGaussian E, or transports source-family integrals along that row map. `stdGaussian_map` is an internal symmetry map, not that missing source-family map. The Phase 2 bridge remains explicit: derive row law and measurability from the source Gaussian family; map one-based row/Gaussian labels to Fin successors while leaving feature frequencies zero-based; transport the exact scalar/matrix integrability and expectations. Common marginal law is sufficient, and no new source premise should be inserted.

## Coverage, omissions and review limits

Covered source mathematics is Ex108 and the actual individual p12.m5, with the exact Ex107 definition and earlier source conventions. The code expands the finite-integrability, symmetry, trace and deterministic tensor bridges that the source compresses.

No completion credit is given for adjacent 0<=a<=1, Ex109's bias bound, the all-rows truncation event, later frame sums, centered matrices, variances, concentration, the complete Krylov-space lemma, or final complexity bounds. No cross-row independence proof is present or needed for these marginal identities. The existing support module's generic second-moment theorem is reviewed as supplied supporting code, not as fresh independent source-proof credit.

There is no visible `sorry`, `admit`, axiom declaration, assumed target equality, or fake mathematical closure in the reviewed literal modules. That textual conclusion does not replace compiler/axiom receipts, which were deliberately absent from this phase.

The narrow code-only verdict is frozen before exposure to any anti-anchored comparison packet or execution evidence. Await that packet for the next stage; do not convert this review alone into final source verification or a ledger state.
