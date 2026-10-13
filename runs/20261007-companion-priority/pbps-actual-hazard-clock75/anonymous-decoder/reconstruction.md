# Blind theorem reconstruction

Let E be a finite-dimensional real inner-product space, with its compatible norm and Borel measurable structure. Dimension zero is permitted. Let V : E -> R, let alpha,beta be nonnegative real numbers, and let eta be real. Assume alpha > 0, alpha <= beta, V is twice continuously Frechet differentiable, eta > 0, beta*eta <= 1, and, for every x,v in E,
  alpha*||v||^2 <= (fderiv_R (fderiv_R V) x v) v <= beta*||v||^2.
Here grad V is the Hilbert gradient represented by the Frechet derivative.

Use the following eight literal definitions; write z=(q,p) in E x E.
(1) c(y,xRef) = y - eta*grad V(xRef), an element of E.
(2) For real t,
  Phi(y,xRef,t,(q,p)) =
    (c(y,xRef) + cos(t)*(q-c(y,xRef)) + (sqrt(eta)*sin(t))*p,
     (-sin(t)/sqrt(eta))*(q-c(y,xRef)) + cos(t)*p).
  Products of real scalars with vectors mean scalar multiplication.
(3) rate(xRef,(q,p)) = sqrt(eta)*max(0, <p,grad V(q)-grad V(xRef)>_R).
(4) H(y,xRef,(q,p)) = (eta^(-1)*||q-c(y,xRef)||^2 + ||p||^2)/2.
(5) C(y,xRef,z) = sqrt(eta)*beta*sqrt(2*H(y,xRef,z))
                    *(sqrt(2*eta*H(y,xRef,z)) + ||c(y,xRef)-xRef||).
(6) For nonnegative t,
  Lambda(y,xRef,z,t) = integral_{s in 0..t} rate(xRef,Phi(y,xRef,s,z)) ds,
  the oriented real interval integral with respect to real Lebesgue measure.
(7) For nonnegative e, tau(y,xRef,z,e) is hittingAfter of the process
  (t,a) |-> Lambda(a.1.1,a.1.2,a.2.1,t) - real(a.2.2)
  into [0,infinity), with start 0 and parameter a=((y,xRef),z,e).
  Equivalently, tau(y,xRef,z,e) is the infimum of the nonnegative real times t
  with Lambda(y,xRef,z,t) >= e, as an element of [0,infinity]; it is infinity
  if there is no such time. The time index is continuous, not discrete.
(8) W(y,xRef,z) = (e |-> tau(y,xRef,z,toNNReal(e)))_# expMeasure(1).
  This is the actual pushforward of the rate-one exponential probability
  measure on R, along the displayed measurable extended-time map. It is a
  measure on [0,infinity], not on E or E x E. toNNReal(e)=max(e,0).

Then the following ten conclusion groups hold together.
1. Lambda is jointly continuous in (y,xRef,z,t) in (E x E) x (E x E) x [0,infinity), with the product topology.
2. Lambda is jointly measurable in those variables, with the corresponding Borel/product measurable structures.
3. For every y,xRef in E, z in E x E, and nonnegative t, s |-> rate(xRef,Phi(y,xRef,s,z)) is IntervalIntegrable with respect to real Lebesgue measure between 0 and real(t).
4. For every y,xRef,z, Lambda(y,xRef,z,0)=0; Lambda(y,xRef,z,t)>=0 for every nonnegative t; and t |-> Lambda(y,xRef,z,t) is monotone nondecreasing on the nonnegative reals.
5. For every y,xRef,z and nonnegative e,t,
  tau(y,xRef,z,e) <= extended(t) if and only if e <= Lambda(y,xRef,z,t).
6. For every y,xRef,z and nonnegative e, all four statements hold:
  (a) tau(y,xRef,z,e)=infinity if and only if Lambda(y,xRef,z,t)<e for every nonnegative t;
  (b) if tau(y,xRef,z,e) is not infinity, then
      Lambda(y,xRef,z,untopA(tau(y,xRef,z,e)))=e;
  (c) if e>0, then extended(0)<tau(y,xRef,z,e);
  (d) tau(y,xRef,z,0)=extended(0).
  The equality in (b) is explicitly guarded against infinity; untopA has a default value at infinity.
7. The map (y,xRef,z,e) |-> tau(y,xRef,z,e) is jointly measurable from (E x E) x (E x E) x [0,infinity) to [0,infinity].
8. For every y,xRef,z, W(y,xRef,z) is a probability measure; for every nonnegative t,
  W(y,xRef,z).real((extended(t),infinity]) = exp(-Lambda(y,xRef,z,t)).
  The event is the strict upper interval of the extended-time space and includes infinity. Measure.real is the real value of the measure of this event.
9. For every y,xRef,z, C(y,xRef,z)>=0, and for every nonnegative t,
  Lambda(y,xRef,z,t) <= C(y,xRef,z)*real(t).
10. For every y,xRef,z and nonnegative e, both implications hold:
  (a) if C(y,xRef,z)>0, then
      extended(toNNReal(real(e)/C(y,xRef,z))) <= tau(y,xRef,z,e);
  (b) if C(y,xRef,z)=0 and e>0, then tau(y,xRef,z,e)=infinity.

All variables y,xRef and z in the conclusions are arbitrary; the theorem imposes no initial-energy, positive-dimension, or finite-hitting-time premise. All square roots are nonnegative real square roots and real division is total. The displayed C depends on beta, eta, V through grad V(xRef), and y,xRef,z through c and the initial H; it is independent of e and t and has no explicit alpha or dimension factor. alpha enters through the hypotheses. No expectation, almost-sure finiteness, jump construction, rejection/thinning algorithm, or target-space sampling law is asserted beyond the ten groups above.

## Ambiguity notes

- No original source, source identity, proof body, theorem name, or audit verdict is visible. No fidelity verdict or compilation result is inferred.
- The compatible Borel structures and meanings of hittingAfter, expMeasure, Measure.real and untopA are taken only from the authorized definition context.
- The packet does not assert almost-sure finiteness, a finite expected time, a jump simulation algorithm, or a target-state distribution; W may assign mass to infinity.
- Finite-value equality applies only under tau!=infinity. No claim is made about the default value of untopA at infinity.
- The interval notation [0,infinity) denotes finite NNReal time, while [0,infinity] denotes WithTop NNReal. The tail event includes its top element.

Decoder run SHA256: f9016ecd0457a05ae9cfc9767386af4a10441468080cef5f0827467df6698233
