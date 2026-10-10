# Internal mathematical completions for the one actual clock

These arguments specify obligations for a future source-facing header/proof.
They are not Lean results, additional source hypotheses, or claims that a75
candidate has passed review. The primary literal is (A.1); the elementary
closure, measurability and probability details below are ASTIS completions.

Fix the original six analytic inputs and arbitrary same-carrier parameters
`a=(y,xRef,z)`, `z=(x,p)`. Use the source center, actual harmonic flow, residual
rate and weighted SUM energy. Let `q(a,s)=lambda_xRef(Phi_s(z))`, and
`Lambda(a,t)=integral_0^t q(a,s) ds` for nonnegative real time. The rate is
jointly continuous and nonnegative; composing with the actual flow supplies
these properties for q internally. Continuity on each compact finite interval
gives interval integrability. The continuous parametric primitive supplies
joint continuity of Lambda, and nonnegative integrands give Lambda(0)=0,
nonnegativity and monotonicity on nonnegative time. No integrability over the
whole half-line is needed or asserted.

For `e>=0`, define `A(a,e)={u>=0:e<=Lambda(a,u)}`. The empty case is assigned
infinity explicitly. If A is nonempty, its nonnegative-time closedness and lower
bound0 give an attained infimum `tau`. This is a continuous-time closed-set
argument, not a discrete-time/WellFoundedLT hitting theorem. Consequently,
`tau<=t iff e<=Lambda(a,t)` for every finite nonnegative t: attainment plus
monotonicity proves the forward direction, membership of t proves the reverse.
Also `tau=top iff A is empty`.

For finite tau, attainment gives `Lambda(tau)>=e`. Equality follows from
minimality and continuity: if tau>0 and the inequality is strict, an earlier
nonnegative time still exceeds the threshold. At tau=0, Lambda0=0 and e>=0
give equality. Thus e=0 yields tau=0, and e>0 yields tau>0, with infinity an
allowed positive value. Continuity at time0 is used internally, never supplied
as a caller. A finite clock does not require strict monotonicity of Lambda.

For each finite t, the joint sublevel of tau in `(a,e)` is exactly
`{(a,e): e<=Lambda(a,t)}`, a closed/Borel set. The top sublevel is the whole
space. With the canonical order Borel structure of WithTop NNReal, these
identities supply joint Borel measurability. Finite-dimensional source typing
must internally discharge the required topological/measurable adapters.
No joint continuity of tau, or of the zero-normal bounce map S, is asserted.

Evaluate the source cap at the SAME actual starting energy `E=H(z)`:

`C(a)=sqrt(eta)*beta*sqrt(2H(z))*(sqrt(2eta H(z))+norm(c-xRef))`.

Actual deterministic flow energy conservation supplies the exact energy-layer
equality needed to apply the cap at every Phi_s(z). Finite-interval comparison
then yields `Lambda(a,t)<=C(a)*t`. If C>0 and tau is finite, the equality at
tau implies `e/C<=tau`; infinity satisfies the same extended-time inequality.
If C=0, nonnegative q and its bound force q=0 and Lambda=0 at all times, so
positive e gives tau=infinity. e=0 still gives tau=0. These are conditional
branches, never assumptions that C is positive, the hazard is unbounded, or the
waiting time is almost surely finite.

Zero starting energy implies p=0 and x=c, so the actual orbit is fixed and its
rate is0 even if h(c) is nonzero. Rank0 has the same legal zero-rate branch.
In contrast, a zero residual or rate at the initial point alone says nothing
about subsequent values on a nonconstant orbit. A positive upper cap alone
also does not imply any threshold crossing.

The pinned exponential API is `ProbabilityTheory.expMeasure (1 : Real)`;
`expMeasure1` in the prior selected contract is descriptive shorthand. A
future local alias would require exact definition review. The rate1 CDF is
0 at nonpositive arguments and `1-exp(-r)` at r>=0. Its support is nonnegative,
its mass at0 is0, and it is a probability measure; these are internal law
facts, not iid, moment, independent-RV or measure premises.

Define the one-clock law by pushing this actual real law through
`r |-> tau(a,Real.toNNReal r)`. Since Lambda(t)>=0, the event equivalence
`tau(a,toNNReal r)>t iff r>Lambda(a,t)` holds even for negative r. The exact
CDF/complement identity therefore gives `P(tau>t)=exp(-Lambda(a,t))`.
If expressed as a measure value, use `ENNReal.ofReal(exp(-Lambda(a,t)))`;
if expressed with toReal, state that convention. This survival law includes
possible mass at infinity. No iid realization, first moment or SLLN is needed
for this single marginal. Source zero-cap “no jumps” holds almost surely for
the positive Exp threshold, while the deterministic all-threshold extension
must still keep the zero-threshold exception.

The actual consumer is (A.1) at the produced postjump state and next clock.
Producing that random state, its measurable A.2 recursion, the global initial
energy bound through every bounce, iid support/moment/SLLN, nonexplosion and
memorylessness/Markov property are distinct future edges. The original source
stationarity/reversal/semigroup and terminal/kernel/main/error/cost/composition
boundaries remain open. A universal fixed-state clock theorem does not supply
those algorithmic producers.
