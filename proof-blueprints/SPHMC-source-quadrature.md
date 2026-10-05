# Actual source quadrature to counted phase

For natural J>=2 and real h>0, enumerate i=0,...,J-1 with Fin J and set t_i=h/2[1-cos(i*pi/(J-1))], ell_j=Lagrange.basis(univ,t,j), Lambda=sup_{s in[0,h]} sum_j |ell_j(s)|, omega_ij=integral_0^{t_i}(t_i-s)ell_j(s) ds and b_j=integral_0^h ell_j(s) ds. Each node is in[0,h], the node map is injective, and t_{J-1}=h. The cardinal identity ell_i(t_j)=1_{i=j} and the constant partition sum_j ell_j(s)=1 hold for every real s. The actual compact supremum satisfies Lambda>=1. For each i, sum_j|omega_ij|<=t_i^2*Lambda/2<=h^2*Lambda/2, and sum_j b_j=h.

Exact source coefficient construction and the row/momentum-total components of B1. No input row/Lebesgue envelope. Lambda is the actual compact supremum. Nonnegative Clenshaw-Curtis momentum weights, logarithmic Lambda<=2/pi*log J+1, polynomial remainder B2, run-wide accuracy/work and main results remain independent obligations; not complete B1.

## Construct distinct source nodes

Fin J index i corresponds to the paper index j=i+1. Cosine lies between minus one and one, giving 0<=t_i<=h. All cosine arguments lie in[0,pi]; cosine is injective there. Since h>0 and J-1>0, equality of nodes implies equality of arguments and indices. At the final index the argument is pi and t_{J-1}=h.

$$0\le t_i\le h,\quad t_{J-1}=h,\quad t_i=t_j\Longrightarrow i=j.$$

## Reuse actual Lagrange cardinal and constant identities

Use Mathlib Lagrange.basis at these distinct nodes. The basis equals one at its own node and zero at every other node. Mathlib sum_basis gives polynomial sum equal to one; evaluating at any real s gives the constant partition. No interpolation basis or coefficient array is supplied as a hypothesis.

$$\ell_i(t_j)=\mathbf1_{i=j},\qquad\sum_j\ell_j(s)=1.$$

## Make the actual supremum and regularity explicit

Each basis polynomial is continuous. The finite sum of its absolute evaluations is continuous, hence bounded above on the compact interval[0,h]. le_csSup gives the pointwise Lebesgue bound. At an actual node the absolute cardinal sum is one, yielding Lambda>=1. All subsequent coefficient integrands and absolute integrands are continuous, so their interval integrability is derived.

$$\sum_j|\ell_j(s)|\le\Lambda_J\quad(s\in[0,h]),\qquad1\le\Lambda_J<\infty.$$

## Integrate the sharp row bound

For every i, the norm of each defining coefficient integral is at most the integral of its norm. Move the finite sum under the integral using proved interval integrability. On[0,t_i], t_i-s is nonnegative, so the absolute sum factors as (t_i-s) sum_j|ell_j(s)| and is bounded by (t_i-s)Lambda. Integrate the latter exactly to t_i^2 Lambda/2. Node range and nonnegative Lambda give the final h^2 Lambda/2 bound.

$$\sum_j|\omega_{ij}|\le\int_0^{t_i}(t_i-s)\sum_j|\ell_j(s)|\,ds\le\frac{t_i^2}2\Lambda_J\le\frac{h^2}2\Lambda_J.$$

## Integrate the constant partition

Sum the actual b_j integrals using polynomial interval integrability. The partition identity turns the integrand into one, whose integral on[0,h] is h. This proves the total momentum weight exactly but does not prove every weight nonnegative.

$$\sum_j b_j=\int_0^h\sum_j\ell_j(s)\,ds=\int_0^h1\,ds=h.$$

Using exactly the source t,ell,Lambda,omega,b arrays above, set positionWeight_j=omega_{J-1,j} (the final node is h), momentumWeight_j=b_j and S=h^2 Lambda/2. Under mu=nu product ((Gaussian product Gaussian) product (Gaussian Fin-J array product Gaussian Fin-J array)), set d=finrank(E), a=exp(-h/2), sigma=sqrt(1-exp(-h)), MR=M+(1-exp(-h))*d, B=6MR+3eps^2+3eta*d, C=2+(1+log((1-c)^(-1)))/(-log c), L0=C[1+log(1+sqrt(2MR)/eps)], L1=C[1+log(1+sqrt(4MR+2S^2B)/eps)]. There exist measurable p,q,N with exact proximal equation, ||q(y)-p(y)||<=eps and successful proximalQuery from y with fuel N(y)+1 returning (q(y),N(y)+1) for every y. P0=aP+sigma zeta0, Y0_i=X+t_i P0, Z0_j=grad V(q(Y0_j)+sqrt(eta)G0_j), Y1_i=Y0_i-sum_j omega_ij Z0_j, Z1_j=grad V(q(Y1_j)+sqrt(eta)G1_j), Phi=(X+hP0-sum_j positionWeight_j Z1_j, a(P0-sum_j momentumWeight_j Z1_j)+sigma zeta1). The same Phi is measurable and defines the Gaussian pushforward Markov kernel. The count T=2*J+sum_i[(N(Y0_i)+1)+(N(Y1_i)+1)] is measurable. For every driving input w, phaseQuery with fuel(y)=N(y)+1 returns exactly some(Phi(w),T(w)); the real cast of T is integrable under mu and E_mu T<=J*(2+L0+L1). The node range and row budget needed by the compiled producer are derived from the coefficient certificate; the Fin J cardinal count is exactly J.

Actual Algorithm3.1 source quadrature arrays in one gradient-only full Gaussian phase, with a supplied incoming state L2 budget and explicit0<h<=1. All successful counts and the bound use the same actual driving law. Finite fuel is a noncomputable execution certificate, not runtime N-precomputation or a cost premise; no failed-path cost claim. Logarithmic Lebesgue bound/nonnegative weights/B2/globalD7/numericalD8/Wq/proxy-warmness/initialization/PBPS/composition and both main results remain open. No TV-to-unbounded-cost transfer.

## Instantiate the source node and coefficient certificate

Apply the independently reviewable coefficient leaf to the actual zero-based Chebyshev-Lobatto nodes. Set both stochastic-gradient-array indices to Fin J, the position weights to the final coefficient row and the momentum weights to the actual ell_j integrals. The final node equals h, so that row has exactly the source endpoint integration limit.

$$t_i=\frac h2\{1-\cos(i\pi/(J-1))\},\quad\Lambda_J=\sup_{s\in[0,h]}\sum_j|\ell_j(s)|,\quad\sum_j|\omega_{ij}|\le\frac{t_i^2}2\Lambda_J\le\frac{h^2}2\Lambda_J,\quad\sum_j b_j=h.$$

## Derive the moment-producer inputs

From 0<=t_i<=h<=1 obtain |t_i|<=1. Lambda>=1 gives S=h^2 Lambda/2>=0, and each actual integrated row has l1 norm<=S. These were formerly supplied interface assumptions; here they follow from the true source arrays, with the factor1/2 retained. The h<=1 restriction is explicit and belongs to the existing moment interface, not a hidden theorem assumption.

$$|t_i|\le1,\quad S\ge0,\quad\sum_j|\omega_{ij}|\le S.$$

## Execute and bound the same actual Gaussian phase

Apply the existing actual counted-phase theorem with these derived inputs. It supplies measurable exact/approximate stopped proximal witnesses and the same full pushforward Markov kernel. The actual interpreter executes the first array, uses its returned gradients in the second centers, executes the second array and returns the exact complete update and count. The count includes every terminal residual test and precisely2J direct gradients. Its full-law integrability and expected-work bound are derived from incoming-state moments; there is no count or center-moment assumption.

$$S=\frac{h^2}2\Lambda_J,\quad T=2J+\sum_{i=0}^{J-1}[N(Y_i^0)+1+N(Y_i^1)+1],\quad\mathbb E_\mu T\le J(2+L_0+L_1).$$

## Keep all accuracy and source complexity boundaries explicit

The input law is nu times all four independent Gaussian innovation factors; arithmetic is exact real arithmetic. The query certificate is not a runtime computation of N. The numerical L0/L1 coefficients use the actual Lambda and S; replacing Lambda by its classical logarithmic estimate and proving uniform state history/parameter complexity still require separate proofs. No target-law cost transfer or full theorem claim is made.

$$\mu=\nu\otimes[(\gamma_E\otimes\gamma_E)\otimes(\gamma_E^{\operatorname{Fin}J}\otimes\gamma_E^{\operatorname{Fin}J})].$$

Status: focused PASS3671; independent math, decoder/source and exact-commit admission pending.
