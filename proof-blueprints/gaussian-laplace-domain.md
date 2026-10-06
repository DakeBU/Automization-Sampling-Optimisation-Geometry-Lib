# Actual Gaussian gradient-output Laplace domain

This packet supplies only the genuine first Bochner mean and all signed
centered directional exponential domains needed to interpret SPHMC (4.3).
It strengthens the existing full_range_proximal_gaussian_oracle declaration
and adds one canonical generic Gaussian Lipschitz-domain leaf, consumed there.
Sharp concentration eta*norm(u)^2/2, bias and full Lemma4.2 remain open.

The independently reviewed exact statements and exhaustive169-span source-only
graph were sealed before proof search. The two missing source well-definedness
edges were repaired separately and reviewed; original rejection survives.
No supplied selector, Lipschitz certificate, mean or Laplace premise is added.

1. Retain the actual C2-Hessian gradient bounds, measurable positive-step
   proximal construction and actual G/K law from the preceding proof.
2. For a general Gaussian Banach/Borel law, Lipschitz growth and Gaussian
   norm L1 imply genuine scalar integrability and its own finite mean m.
3. Fernique supplies C>0 and exp(C norm(x)^2) L1.
4. For every signed t let b=abs(t)L, D=abs(t)(abs(f(0))+abs(m)). Young gives
   b norm(x)<=C norm(x)^2+C^-1 b^2. Exp domination yields the domain.
5. Actual gradient-output growth supplies vector Bochner L1 under gamma;
   exact pushforward gives identity Bochner L1 under K_s.
6. Actual scalar direction inner(a,G_s) is norm(a)sqrt(eta_s)-Lipschitz;
   consume the shared domain leaf for all t, with zero directions retained.
7. Bochner map and continuous inner-product integral commute, so the scalar
   mean equals inner(a,int w dK_s). Pull back the exact centered exponential.

The constant in the radial domination depends on Fernique C and f(0).
It is not the printed sharp centered concentration constant. RGO posterior
and HMC laws remain distinct from K_s. TV does not transfer unbounded cost.

Focused leaf2 passes3637. Actual source consumer0 passes3730 before expanded
new tests; final focused1 passes3731 with nonlinear negative/zeroL/0D and the
real unbounded eta(n)=n+2 output signed-domain assertions. Earlier syntax/API
errors and missing Testconstant identifier diagnostics are retained. No literal
proof placeholder was inserted. Independent mathematics/decoder/source/exact
commit/shared aggregate/publication and postmerge purification remain separate.
