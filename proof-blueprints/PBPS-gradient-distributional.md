# Distributional meaning of the same closed weighted gradient

Frozen continuation of PBPS Appendix C.1 analytic prerequisite. E is a finite-dimensional real inner-product Borel space, W is C1 and exp(-W) volume-integrable. Retain any given closable D with exactly the smooth compact gradient graph in L2(mu), mu=volume.tilted(-W), and any (u,G) in D.closure.graph. Prove both representatives locally integrable for volume and, for every C1 compact psi and constant v, both products integrable for volume and integral psi <G,v> dx = -integral u D_v psi dx.

1. Finite mu makes L2 representatives integrable.
2. Mathlib integrable_tilted_iff makes exp(-W) times each representative volume-integrable.
3. Multiply its local integrability by continuous exp(W), cancel exponentials; no new decay or global volume integrability premise.
4. In the existing weighted identity, choose phi=exp(W)*psi, still C1 compact.
5. Genuine product rule gives D_v phi-phi D_v W=exp(W)D_v psi.
6. Convert both integrability conclusions with integrable_tilted_iff; convert the integrals using integral_tilted and cancel the positive normalization.

Imports: WeightedGradientWeak plus LocallyIntegrable. Private generic inverse-weight local-integrability helper serves scalar and vector representatives; only the public distributional theorem receives proof credit. Focused test must consume compact_gradient_closable and apply the result to its same closure domain, not assume the desired integral identity.

This is the distributional-gradient direction only. No converse characterization of the graph domain, H2, resolvent PDE adapter, operator core of D*D, noncompact Bochner, Poincare or whole-paper conclusion. No extra regularity beyond C1 W. Primary PBPS/source background and exact parent source audit were read on the preceding accepted packet; the sources are version-pinned and reused, not reinterpreted as full-space elliptic regularity.

Focused compile PASS3033, including an actual constructor-to-same-closure-domain consumer. Independent full proof and six-step authored lesson review passed; canonical source/commit admission is separate.

Next-route caution: the original core contains C-infinity compact tests, but exp(W)psi is only C1 when W is C1 (C2 under the paper assumptions). Do not silently treat this inverse-weighted test as a member of the original smooth core. The next direct resolvent bridge can use smooth compact psi and derive the weighted divergence-form distributional PDE from its actual domain embedding; a non-divergence-form equation or extra test-domain extension needs its own justification. Keep H2/operator-core work separate.
