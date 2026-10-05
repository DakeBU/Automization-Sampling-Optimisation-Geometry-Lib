# Actual finite two-layer phase work

Under mu=nu product ((Gaussian product Gaussian) product (Gaussian Fin-m array product Gaussian Fin-m array)), set d=finrank(E), a=exp(-h/2), sigma=sqrt(1-exp(-h)), MR=M+(1-exp(-h))*d, B=6MR+3eps^2+3eta*d, C=2+(1+log((1-c)^(-1)))/(-log c), L0=C[1+log(1+sqrt(2MR)/eps)], L1=C[1+log(1+sqrt(4MR+2S^2B)/eps)]. There exist measurable p,q,N with exact proximal equation, ||q(y)-p(y)||<=eps and successful proximalQuery from y with fuel N(y)+1 returning (q(y),N(y)+1) for every y. P0=aP+sigma zeta0, Y0_i=X+t_i P0, Z0_j=grad V(q(Y0_j)+sqrt(eta)G0_j), Y1_i=Y0_i-sum_j omega_ij Z0_j, Z1_j=grad V(q(Y1_j)+sqrt(eta)G1_j), Phi=(X+hP0-sum_j positionWeight_j Z1_j, a(P0-sum_j momentumWeight_j Z1_j)+sigma zeta1). The same Phi is measurable and defines the Gaussian pushforward Markov kernel. The count T=2*m+sum_i[(N(Y0_i)+1)+(N(Y1_i)+1)] is measurable. For every driving input w, phaseQuery with fuel(y)=N(y)+1 returns exactly some(Phi(w),T(w)); the real cast of T is integrable under mu and E_mu T<=m*(2+L0+L1).

Single full Gaussian phase with supplied incoming integrable state L2 budget, finite bounded nodes and row l1 bounds; actual successful exact-real interpreter output and total gradient count. Sufficient finite fuel certifies execution and is not a runtime precomputation or a count/cost hypothesis. No cost claim for failed insufficient-fuel executions. Gaussian sampling and arithmetic are not gradient queries. Source quadrature/J adapter, run-wide D7 induction, D8 parameter/iteration substitution, Wp, proxy-warmness, initialization, PBPS and composition/main results remain open. No TV-to-unbounded-cost transfer.

## Execute a finite successful query array

Induct on the finite array size. The empty array returns count zero. For a nonempty array, execute index zero, then the tail, returning the actual vector of outputs and the sum of their returned counts. Fin.cons reconstruction and Fin.sum_univ_succ identify the complete returned vector and count. This helper has no probabilistic or termination premise beyond the individual successful calls.

$$\operatorname{collect}(r_i)=(x_i,\sum_i c_i)\quad\text{if }r_i=\operatorname{some}(x_i,c_i).$$

## Run the actual two-layer program

For each first center, run the residual-stopped proximal interpreter and evaluate the Gaussian-shifted gradient of its returned point, adding one direct query. Construct the second centers using these actual first returned gradients; run the second array in the same manner. Form the full updated state including both half-refreshes from the second returned gradients. In both layers each proximal count N(Y)+1 already includes its terminal successful residual test. Thus the returned count is the sum of both arrays plus exactly 2*m direct gradient evaluations. Failed insufficient-fuel calls return none.

$$T=2m+\sum_{i=0}^{m-1}\bigl[N(Y_i^0)+1+N(Y_i^1)+1\bigr],\quad \mathbb E_\mu T\le m(2+L_0+L_1).$$

## Use one actual full-law witness

The existing full-phase moments/work theorem supplies the same measurable p,q,N, full phase map and kernel, with both count integrabilities and the bounds L0,L1 under mu. No center moment, count-integrability or expected-query bound is introduced as a new premise. The execution identity applies its global successful proximal runs directly, with certified fuel N(y)+1.

$$\operatorname{phaseQuery}(w)=\operatorname{some}(\Phi(w),T(w)).$$

## Prove measurable and integrable total actual cost

The C2 gradient is measurable, as are the stopped q/N and finite center maps. Therefore the natural count T is measurable. Cast the finite natural sum to the reals. Its constant part is integrable under the full probability law; each first- and second-layer count has L1 integrability supplied by the actual-law parent, so finite addition proves L1 integrability of the actual program count.

$$T\in L^1(\mu),\qquad \mu(\Omega)=1.$$

## Integrate and sum the actual query bounds

Use integral_add and integral_finsetSum only after establishing their integrability hypotheses. For each index the two count expectations add to at most L0+L1. Summing over Fin m gives m*(L0+L1); probability normalization makes the constant contribution exactly 2*m. Ring arithmetic yields m*(2+L0+L1). All inputs and costs use the same full Gaussian law.

$$T=2m+\sum_{i=0}^{m-1}\bigl[N(Y_i^0)+1+N(Y_i^1)+1\bigr],\quad \mathbb E_\mu T\le m(2+L_0+L_1).$$

Status: independent mathematics, final blind decoding and whole-module source review passed; independently VERIFIED at a5579e03460cb638f12a8e44838787c779b8bd93. Focused PASS3668; standard3 Lean foundations. Shared root integration and canonical aggregate/site/graph gates are separate.
