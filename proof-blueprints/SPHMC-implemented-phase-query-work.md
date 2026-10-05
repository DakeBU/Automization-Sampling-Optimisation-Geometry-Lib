# Same actual phase, both query-layer moments and costs

Source: arXiv:2609.06906v1 Algorithm 3.1, Algorithm D.2, and D.4 before/after (D.7).
Target: `ImplementedPhaseWork.implemented_phase_query_moments_and_work`.
Reusable implementation identity: `ProximalExecutionIdentity.successful_query_unique`.
The unchanged `RealizedProximalWork` conclusion now imports that identity once.

Let the incoming phase-state law nu be a probability with

    E_nu[||X-xstar||^2+||P||^2] <= M,

and true integrability, with grad V(xstar)=0. Retain the normalized C2 Hessian
bounds and 0<eta<=c<1, eps>0. With h>=0, independent zeta0,zeta1 and Gaussian
arrays G0,G1, retain the entire implementation law

    gamma=(Gaussian x Gaussian) x (Gaussian^I x Gaussian^I),
    mu=nu x gamma.

The supplied finite nodes satisfy |t_i|<=1 and sum_j|omega_ij|<=S. Source
Chebyshev quadrature and source step selection are not constructed by this packet.
The exact full phase P0/Y0/Z0/Y1/Z1/Phi formulas are authored once in
`website/content/declaration_lessons/sphmc-implemented-phase-query-work.json`.

1. Probability-product projections and inverse product association send the full
   state/noise law to ((state,zeta0),G0) with the exact PicardInputLaw measure.
   Do not use `MeasurePreserving.integral_comp`: the projection is not an embedding.
   Use pushforward equality and `integral_map` for noninjective transport.
2. Pull back the true refreshed L2 state bound and Gaussian-array moments:

       MR=M+(1-exp(-h))*d,    E_mu||G0_j||^2=d.

   MR, rather than M, includes the refresh innovation contribution.
3. Get the complete implementation's p,q,N, measurable full Phi and Markov K.
   Get both Picard-center moment estimates under mu. Compare successful returned
   pairs at every y: same deterministic execution yields q=q' and N=N'. The
   exact proximal witnesses need not be equated.
4. The same centers then satisfy true L1 gradient squares and

       A0=2MR,  B=6MR+3eps^2+3eta*d,  A1=4MR+2S^2*B.

5. Apply actual-input expected work with the same successful q,N under mu, and
   monotonicity of sqrt/log with eps>0 and C>=0:

       E_mu[N(Yk_i)+1] <= C[1+log(1+sqrt(Ak)/eps)],
       C=2+(1+log((1-c)^(-1)))/(-log c).

   Count integrability is derived; no count or queried-gradient moment premise.
6. Return the same complete Gaussian Markov kernel and both per-node moment/cost
   contracts, retaining final zeta1 and G1 even though their marginal is not needed
   for the center estimate. The actual per-node proximal count includes the final
   successful gradient test. It excludes the additional Z0/Z1 gradient evaluations.

Focused build: `lake build Tests.SmoothedPicardHMCImplementedPhaseWork`, PASS3667.
The actual E=R, I=Fin2, h=1 consumer takes incoming delta_(0,0), derives both
center count integrabilities without assuming a center moment, and retains gamma.
Independent mathematical receipt: `runs/20261005-companion-priority/phase-query.math-review.json`.
Independent blind and source reviews are separately bound; local compilation is
not source-fidelity or complete-paper evidence.

Conceptual mirror audit: none found. The measure-preserving marginal and unique
successful execution reuse ordinary product/pushforward mechanisms, not a new
cross-domain equivalence or formal graph edge.

Remaining: source quadrature/node-count bounds, actual finite-array direct and
proximal gradient execution accounting, incoming-state induction / numerical
run-wide D.7, parameter substitution and D.8; Wp/proxy-warmness, initialization,
PBPS/SPHMC composition and both main results. No unbounded cost is transferred
between nearby laws via TV.
