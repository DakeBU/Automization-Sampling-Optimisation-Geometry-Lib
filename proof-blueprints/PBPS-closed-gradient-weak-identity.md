# Weighted test identity for the same closed gradient

PBPS arXiv:2609.06905v1 Appendix C.1 needs a genuine analytic bridge from the already constructed conditional weak resolvent to a distributional equation. Kolesnikov–Milman arXiv:1310.2526v7 section 2.5 motivates weighted Sobolev completion, but its compact-manifold spectral statements are not asserted here.

Frozen packet: finite-dimensional real inner-product Borel E (including dimension zero), C1 W with exp(-W) integrable, mu = volume.tilted(-W). For ANY given closable partial real linear map D whose original graph is exactly the smooth compact scalar functions and their genuine gradients modulo mu-a.e., every (u,G) in D.closure.graph satisfies, for C1 compact phi and constant v,

    integral phi <G,v> dmu = - integral u (D_v phi - phi D_v W) dmu.

Both products are integrable. This retains the SAME D from the conditional resolvent; it does not construct an unrelated replacement operator. No differentiability of the arbitrary L2 representatives is assumed or inferred.

Proof route: (1) use C1 product rule for exp(-W) phi and compact full-space IBP; (2) normalize to tilted measure; (3) continuous compact vector P=phi v and scalar q=-(D_v phi-phi D_v W) are L2; (4) integral pairings are continuous L2 inner products; (5) the equality set is closed and contains the exact smooth graph; (6) pass to its closure; (7) L2 product estimates establish both integrabilities. Existing WeightedGradient local helper is inaccessible, so adapt only its minimal IBP argument in a private helper; no duplicate public closability construction. Imports reuse WeightedGradient plus its Mathlib APIs.

Owned declaration: AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.WeightedGradientWeak.closed_gradient_weighted_ibp. New isolated module and focused test; no shared imports until stabilization.

Next boundary remains local weight/volume comparison and unweighted distributional identity, then resolvent PDE and actual elliptic regularity. A gradient graph core is not an operator core of D*D. Do not strengthen W to C-infinity merely for convenience. No Poincare/score-variance/macroscopic-coercivity closure. This is an analytic prerequisite, not the original source theorem itself.

Focused implementation passes (3032 jobs), with actual parent construction consumed on every element of the same closure domain. Independent full proof/lesson review passed; blind/source admission is recorded separately in the canonical audit.

Bounded next-API retrieval: pinned Mathlib Measure/Tilted.lean has `integrable_tilted_iff` (line 293), `absolutelyContinuous_tilted` (line 283) and the forward absolute continuity (line 280). These allow genuine measure/representative transfer rather than an assumed density comparison. For compact C1 psi, phi=exp(W)*psi is still C1 compact; the extra derivative terms cancel. A claim of an actual distributional gradient must ALSO establish local volume integrability of u and G, not merely rename the compact-test formula. No next-packet Lean implementation is claimed here.
