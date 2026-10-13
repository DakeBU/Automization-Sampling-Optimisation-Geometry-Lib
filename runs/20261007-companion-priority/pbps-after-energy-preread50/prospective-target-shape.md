# Proposed minimal public delta (untyped, source/API only)

Proposed `MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks` in prospective `AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicEnergy.lean`. No Lean file/declaration/seal exists.

Bind exactly finite real Hilbert/Borel E, V globally C2, alpha/beta:NNReal with0<alpha<=beta and true everywhere Hessian bounds, eta>0 and beta eta<=1. Let mu=volume.tilted(-V), J=(x,x+sqrt eta z)#(mu prod stdGaussian E), nu=J.snd, Lambda=(y,2x-y)#J, F(x,y)=(x,2x-y), and literal conditional projection P=(lpMeas comap snd).subtypeL o condExpL2.

Produce SAME R/S as the real conditional construction (Markov, J.swap.IsCondKernel R, S_y=(x->2x-y)#R_y, every-y actual density), mu/J/nu probability, Lambda.IsCondKernel S and Lambda.fst=nu. Produce actual L2 isometric selfadjoint involution U with Ug=AE[J] g o F. Put A=P U P and B=(1-P) U P and retain real ReflectionL2 block identities.

For every signed C-infinity compact f, put Tf(y)=integral f dS_y. Produce actual differentiation, MemLp f2nu/Tf2nu/gradientTf2nu and varianceL1nu as in49, plus g:L2(J) with g=AE[J] f o snd, Pg=g and Ag=AE[J] Tf o snd. New literal identities:

    integral Var_(S_y)(f) dnu = ||B g||²
      = ||g||² - ||A g||²
      = integral f² dnu - integral Tf² dnu
    eta * integral ||gradient Tf||² dnu
      <= (1-alpha eta)²/[4(1+alpha eta)] * ||B g||².

These are actual joint operators and an actual classical differentiable representative; this target does not assert membership in repository weightedH1 closure or invent Gamma. Existing49 differentiation/gradient facts remain attached to its literal Tf. Conditional AE uniqueness transports means and L2 classes only. Internal proof ingredients are not additional public binders.
