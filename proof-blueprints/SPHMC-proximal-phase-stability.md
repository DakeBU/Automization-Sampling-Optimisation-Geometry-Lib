# Actual proximal implementation phase stability

Construct measurable exact p, actual stopped q and natural N for full0<eta<1, with p+eta gradientV(p)=id, ||q-p||<=eps and proximalQuery(g,eta,eps,y,N(y)+1,y)=some(q(y),N(y)+1). The exact p is nonexpansive. Construct Markov Kp and Kq as the full two-layer source Gaussian pushforwards. For every deterministic phase state s and finite real rho>=1, the Euclidean Wasserstein cost W_rho(Kq(s),Kp(s))<=3h Lambda eps. Moreover every measurable delta-accurate r has its true pushforward Markov Kr with W_rho(Kr(s),Kp(s))<=3h Lambda delta for all s and rho>=1, includingdelta0. Here W_rho is the 1/rho power of the infimum coupling integral of [sqrt(||DX||²+||DP||²)]^rho. It is not the default max-norm product metric.

Appendix D1/D2 one-phase proximal implementation stability only, explicit universal constant3. Both compared phases use the exact same two stochastic-gradient Gaussian arrays and two half-refresh Gaussian vectors; the exact phase uses exact proximal p, not a deterministic smoothed force. N(y)+1 is a noncomputable successful execution certificate, not free runtime fuel determination or expected-work evidence. Repeated-phase D3, weighted contraction, numerical D7/D8, invariant law, bias/concentration, Wp/proxy-warmness/init/PBPS/composition and both main results remain separate. No TV-to-unbounded-cost transfer.

## Construct and identify the actual proximal maps

Use the compiled full-range stopped execution kernel with contraction c=eta. It constructs one exact optimality solution p and its actual finite residual-stopped q,N. Derive gradient monotonicity and 1-Lipschitz gradient from the genuine C2 Hessian through the shared quadratic/first-order APIs, then apply the shared monotone-optimality implication. Strong convexity identifies this unique optimality solution with the source proximal minimizer; no p-nonexpansiveness premise or hidden eta<=1/2 restriction.

$$p(y)+\eta\nabla V(p(y))=y,\quad\|q(y)-p(y)\|\le\varepsilon,\quad\operatorname{Lip}(p),\operatorname{Lip}(\nabla V)\le1.$$

## Use the actual coefficients and preserve the same noise

Use the independent coefficient construction for Lambda>=1 and every omega row sum<=S=h²Lambda/2. Position weights are the final row. The new absolute momentum-integral prerequisite yields sum|b|<=hLambda. Set a=exp(-h/2), sigma=sqrt(1-exp(-h)); P0=aP+sigma*zeta0; both phases use the same P0 and independent G0,G1 arrays, and the same terminal zeta1.

$$S=	frac12h^2\Lambda_J,\quad B=h\Lambda_J,\quad\sum_j|\omega_{ij}|\le S,\quad\sum_j|b_j|\le B.$$

## Propagate the two actual Picard layers

At Y0_i=X+t_iP0, common G0 cancels; gradient Lipschitz and ||r-p||<=delta give first gradient difference<=delta. Therefore ||Y1_r-Y1_p||<=S delta. In the second layer add and subtract p(Y1_r), use r accuracy and exact p nonexpansiveness, then cancel common G1 and use gradient Lipschitz. This works for delta=0 and does not assume r Lipschitz.

$$\|Z^0_{r,j}-Z^0_{p,j}\|\le\delta,\quad\|Y^1_{r,i}-Y^1_{p,i}\|\le S\delta,\quad\|Z^1_{r,j}-Z^1_{p,j}\|\le(1+S)\delta.$$

## Bound true Euclidean phase displacement

The full actual position difference is<=S(1+S)delta and momentum difference<=aB(1+S)delta. From Lambda>=1 and h²Lambda<=1 obtain h<=1, S<=1/2 and S<=B/2; also a<=1. The sum of these norms is<=9Bdelta/4<=3Bdelta. The Euclidean square-root norm is at most that sum by nonnegative cross product. Source prose uses momentum-weight positivity to give a sharper intermediate bound; this proof uses the independently derived absolute sum and keeps the same universal D2 scaling with explicit3, without adding an assumption.

$$\sqrt{\|\Delta X\|^2+\|\Delta P\|^2}\le(S+aB)(1+S)\delta\le\tfrac94B\delta\le3h\Lambda_J\delta.$$

## Construct actual kernels and a coupling for every finite rho

The product Gaussian law gamma contains both refreshes and both Fin J Gaussian arrays. Each full phase map is measurable by finite sums and composition. Map the product id/kernel-constant to construct each Markov kernel, retaining the existing actual Kq. For fixed s, gamma.map(z↦(Phi_r(s,z),Phi_p(s,z))) has exactly Kr(s) and Kp(s) marginals. The pointwise Euclidean displacement bounds its rho-cost integral by A^rho with A=3hLambda delta; probability normalization supplies the constant integral, so no incoming-state moment assumption is needed. Taking the monotone1/rho root gives the bound, for delta=0 as well.

$$\pi_s=(\Phi_r(s,\cdot),\Phi_p(s,\cdot))_\#\gamma,\quad\int d_{\rm Eucl}^{\rho}\,d\pi_s\le A^\rho\Longrightarrow W_\rho\le A.$$

Shared extraction and actual momentum absolute-integral prerequisite are included once; they carry no duplicate wrapper credit.

Status: focused PASS3717; independent mathematics, anonymous decoder and source review pending.
