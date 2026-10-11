# Source-first recommendation v2: actual finite ordered-prefix law

This v2 successor responds to the independently reviewed local candidate corrections; it remains a bounded mathematical preread, not an accepted topology, SAU claim, theorem seal, proof, or canonical status change. All v1 artifacts remain immutable. The fixed primary source was reread for this recommendation; no implementation Lean was read during this preread to determine topology. The reviewer previously reviewed the phase-91 theorem and discloses that context, so this is not a claim of never having seen any related implementation. No previous reviewer verdict determines the statement below.

## Recommended next edge

Prove the **actual first-n-event complete-history law on the strict ordered-time simplex**, for every deterministic n and finite horizon T. Retain the complete sequence of event times and post-event states. This exposes the finite product hidden in the author's iteration sentence before (A.7). It is an attributed ASTIS completion of that sentence, not a printed standalone author theorem.

### Exact mathematical statement

Let d be a finite dimension, V in C^2(R^d), 0<alpha<=beta, and assume

    alpha |v|^2 <= D^2 V(x)[v,v] <= beta |v|^2   for every x,v in R^d.
    0 < eta <= 1/beta.

These are the original six standing analytic conditions from (1.1) and Section 2.2. Write Phase=R^d x R^d with its Borel structure. Fix arbitrary y,r in R^d and z0=(x0,p0) in Phase. Define the actual source objects by

    c = y - eta grad V(r),       h(x) = grad V(x)-grad V(r),
    lambda(x,p) = sqrt(eta) max(<p,h(x)>,0),
    Phi_s(x,p) = (c+(x-c)cos(s)+sqrt(eta)p sin(s),
                  -(x-c)sin(s)/sqrt(eta)+p cos(s)),
    R_v p = p - (2<p,v>/|v|^2) v  if v != 0,    R_0 p = p,
    B(x,p) = (x,R_(h(x)) p),
    L_z(u) = integral_0^u lambda(Phi_s(z)) ds  for u>=0,
    tau_z(e) = inf{u>=0 : L_z(u)>=e} in [0,infinity],  e>=0,

where an empty crossing set has infimum infinity. The closed threshold convention includes equality and tau_z(0)=0. The bounce need only be Borel, not continuous; the zero-normal convention is literal and lambda(x,p)=0 whenever h(x)=0.

Use the canonical actual clock space and law, defined rather than supplied as theorem hypotheses:

    Omega = R^N,    P = infinitePi_(k in N) Exp(1),
    epsilon_k(w) = max(w_k,0) in NNReal.

The product carries its product Borel sigma algebra. Index k starts at zero; epsilon_k represents the source clock E_(k+1). Clipping extends the definition to raw negative inputs. The product law makes every coordinate strictly positive almost surely; this is a consequence of P, not an extra public good-input assumption.

Set Rec=(NNReal x Phase) sum Unit, with Borel product and disjoint-sum structures, writing live(a,z) and stopped for its tags. The actual total finite recursion is literal:

    R_0(w) = live(0,z0),
    R_(k+1)(w) = stopped                              if R_k(w)=stopped,
    R_(k+1)(w) = stopped                              if R_k(w)=live(a,z)
                                                        and tau_z(epsilon_k(w))=infinity,
    R_(k+1)(w) = live(a+v, B(Phi_v(z)))               if R_k(w)=live(a,z)
                                                        and tau_z(epsilon_k(w))=v<infinity.

Thus the absorbing stopped tag totalizes the source's terminated recursion. It never denotes a finite event or a phase point at infinite time. On live records the first component is the actual cumulative time from (A.2). Define Hist_n=Fin(n+1)->Rec with its product Borel structure and H_n(w)_j=R_j(w), for j=0,...,n. Tests below range over all ambient histories, including unrealizable tagged tuples; equality of laws is restricted to the literal strict-prefix event.

Let n>=0 and T>=0 be deterministic, with T finite. Use the Borel simplex subtype

    Delta_n(T) = {t in R^n : 0<t1<...<tn<T}.

Delta_0(T) is the singleton empty tuple for every T>=0, carrying mass one. Its measure m_(n,T) is the restriction of n-fold real Lebesgue measure to the simplex, regarded on that subtype. At n=0 use the mass-one empty product measure. No value of the prescribed history or weight outside this subtype is needed or silently invented.

For t in Delta_n(T), put t0=0, z_0^t=z0 and recursively

    delta_j = t_j-t_(j-1),
    z_j^- = Phi_(delta_j)(z_(j-1)^t),
    z_j^t = B(z_j^-),                         j=1,...,n.

Define K_n(t) in Hist_n by K_n(t)_0=live(0,z0) and K_n(t)_j=live(t_j,z_j^t) for j=1,...,n. Here t_j is regarded as NNReal using its positivity on the subtype. Define E_n(T) literally as the event that the first n actual records R_1,...,R_n are live and their stored cumulative times satisfy 0<T1<...<Tn<T; E_0(T)=Omega. This is the **strict first-n prefix event**. It places no condition on R_(n+1) or T_(n+1). A count interpretation as at least n interior events is valid only almost surely on the positive-clock event; it is not asserted pointwise on raw zero-clock inputs and is not needed for the prefix theorem. In particular this is not an exactly-n-at-horizon event.

Define the finite nonnegative real weight and its extended-nonnegative embedding:

    qReal_n(t) = product_(j=1)^n [lambda(z_j^-) exp(-L_(z_(j-1)^t)(delta_j))],
    q_n(t) = ENNReal.ofReal(qReal_n(t)),
    qReal_0(empty) = 1,       q_0(empty) = 1.

Then E_n(T) and H_n are Borel measurable. For every fixed V,eta,n,T satisfying the preceding conditions, the maps (y,r,z0,t)->K_n(t) and (y,r,z0,t)->q_n(t) are jointly Borel on R^d x R^d x Phase x Delta_n(T). This does not assert regularity in V or eta or a new joint parameter-integral identity.

For every fixed y,r,z0 and every Borel F:Hist_n->[0,infinity], with possibly infinite values,

    integral_(E_n(T)) F(H_n(w)) P(dw)
      = integral_(Delta_n(T)) F(K_n(t)) q_n(t) m_(n,T)(dt).

Equivalently, the pushforward of P restricted to E_n(T) under H_n equals the pushforward of the measure q_n*m_(n,T) under K_n. In particular integral q_n = P(E_n(T))<=1. Multiplication and integration use ENNReal conventions, including 0*infinity=0. Restrictions are unnormalized; P(E_n(T)) may be zero. The identity covers n=0, T=0, zero hazard, stopped histories, and an infinite next wait. F can inspect all recorded times and poststates, not only the terminal position. Measurability, the density law, positive-clock support and finite-prefix bookkeeping are conclusions/dependencies, not new source hypotheses.

A coordinate-free finite-dimensional real inner-product version remains possible as an explicitly identified extension. It must preserve all six original analytic conditions and the same literal input and tagged-history construction. No exact Lean header is sealed by this recommendation.

## Primary anchors and why this edge is necessary

The source snapshot is `runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html`, SHA256 `d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760`. It is arXiv:2609.06905v1. Its banner and the previously verified official fixed-version/license pages identify the arXiv non-exclusive distribution license. No full source is republished here.

- `S1.p1.1`, equation `(1.1)`: original potential regularity and two-sided curvature bounds.
- `S2.SS2.p1.1`: positive scale and eta<=1/beta.
- `S3.SS2.p4.2`, equation `(3.4)`: center and residual gradient.
- `A1.SS1.p1.1` through `p1.3`: actual rate, flow, bounce, and zero-normal convention.
- `A1.SS1.p2.1`, `(A.1)-(A.2)`, and `p2.2`: independent clocks, actual recursive cumulative times/poststates, stopping and between-event flow. These are mandatory literal objects for the prefix law.
- `A1.SS1.SSS0.Px1.p4.1`: strict ordered absolute-time simplex.
- `A1.SS1.SSS0.Px1.p4.2`, `(A.7)`: prescribed path and iteration sentence; the printed conclusion tests every bounded measurable functional of the entire path on [0,T]. Its weight includes the final survival interval, which q_n deliberately does not yet include.
- `A1.SS1.SSS0.Px1.p4.3`: absolute convergence via simplex volume and the rate cap.
- `A1.SS2.p3.1`: joint Borel objects, threshold times and recursive states; terminal-state construction is a later part of that paragraph.

Finite ordered-prefix density is necessary because a one-step coordinate law alone does not supply the n-dimensional simplex integral, identify all prescribed states, or multiply all n pre-bounce rates. Keeping the whole history makes the result usable with the final survival factor and with a measurable functional of the prescribed entire path. A terminal-position-only marginal would discard information needed for those consumers.

## Source-derived route, at most seven steps

1. Define K_n and q_n by the actual harmonic/reflection recursion on strict absolute times; prove joint Borel dependence by finite recursion. Define actual E_n using live tags and all ordered times.
2. At n=0, the actual history and K_0 are the same deterministic one-record history; the singleton integral equals that constant test value.
3. At n+1, condition at deterministic event index n on the **complete actual history** and use the fresh exponential clock's finite-event density, expressed in absolute time u with T_n<u<T. Restrict the old history to E_n(T). No random physical-time restart is involved.
4. Use the induction identity with the nonnegative history test obtained by integrating the appended-history test over u. Its Borel measurability follows from joint Borel constructions and nonnegative parameter integration; it is not a new premise.
5. Identify the appended actual history with K_(n+1)(t,u), preserving every earlier record. Multiply q_n(t) by lambda(Phi_(u-t_n)(z_n^t)) exp(-L_(z_n^t)(u-t_n)); this is exactly q_(n+1)(t,u).
6. Tonelli and the section identity Delta_(n+1)(T)={(t,u):t in Delta_n(T), t_n<u<T}, with t_0=0 in the n=0 step, turn the nested integral into the (n+1)-simplex integral. Prove the required finite-product/Fin.snoc coordinate transport rather than assuming a supplied Jacobian or density certificate.
7. Obtain measure equality and subprobability mass from nonnegative tests. Preserve the literal strict first-n prefix event and the absent final survival factor. Any at-least-n interior-count interpretation is only almost sure on the positive-clock event, not pointwise on totalized inputs.

This source route needs only the actual one-step complete-history finite-event law, prescribed-history identification, Borel parameter integration, finite product-coordinate bookkeeping and induction. The measurability node explicitly depends on the defined actual clock/record recurrence, not only on smoothness and flow formulas. A separate full unweighted history-dependent shear theorem is not needed if the absolute one-step law already supplies the translated density.

## Genuine remaining boundaries toward full (A.7)

After this next edge, q_n must still be multiplied by the conditional no-further-event factor

    exp(-L_(z_n^t)(T-t_n)).

This is evaluated at the history-dependent remaining duration. It is neither another jump-rate factor nor normalization of q_n. After the relevant count/good-clock and endpoint identifications, it supplies the exactly-n-event-at-horizon term from the strict-prefix law. Those identifications must be proved or reused; they are not pointwise consequences on every totalized raw clock sequence. Existing terminal-survival input may be reused, but its composition at these prescribed histories is still a real obligation.

The sum of the n elapsed segment hazards plus the final segment hazard must be identified with integral_0^T lambda(zeta_s^t) ds. Every factor lambda(z_j^-) must match the rate at the prescribed path's pre-jump state. Actual trajectories on the count event must be identified with the complete prescribed path, with Borel path-observable composition; equality only of terminal states is insufficient.

Almost-sure nonaccumulation and half-open interval coverage supply the exhaustive finite-count partition. These are necessary source ingredients, but this preread does not reopen or reprove the already tracked actual-input nonaccumulation78/coverage79 results. The remaining task is their application to the full path/count representation and strict horizon conventions. No-atom reasoning is required only where strict and non-strict finite-event endpoint conventions are equated; it is not a new hypothesis for the proposed strict prefix law.

Finally, sum over n, justify bounded signed functional integration and absolute convergence, and retain the n=0 no-event path term. The printed cap/simplex-volume argument is a sufficient route. A nonnegative count-partition/Tonelli route followed by bounded signed decomposition is a possible ASTIS alternative, not another mandatory independent assumption. Path reversal (A.8), invariance, the L2 semigroup, averaged kernels, physical-time Markov restart and all main sampling/composition claims remain downstream.

## Classification and stopping boundary

Printed source objects: original assumptions, flow/rate/bounce, (A.1)-(A.2), the simplex, prescribed path and full (A.7).

ASTIS completion: tagged total finite histories; explicit first-n-event prefix density with arbitrary nonnegative complete-history tests; induction and exact finite-product coordinate transport. These elaborate the source's omitted iteration details without changing its target or assumptions.

No implementation was created or reviewed for this next edge. No SAU, source-review acceptance, theorem seal or publication status is claimed. A proving worker must first check current reusable interfaces against this source-derived target, then seal the exact statement and independently review any genuine semantic repair.

## Exact v2 source-coverage corrections

The source residual bound |grad V(x)-grad V(r)|<=beta|x-r| is assigned to the existing source energy/rate-cap ingredient. The full conditional-force recombination in Section 3.2 is explicitly excluded from the prefix dependency graph as generator/background explanation. Bounce involution in A.1 is explicitly excluded as downstream reflection/reversal algebra, while rate zero at a zero residual normal is recorded as a literal-rate consequence in O92. Reflection still requires only Borel measurability. These are distinct source dispositions, not new theorem assumptions or proof claims.

The independent target reviewer gave a null-input counterexample to the old unqualified count gloss: for V(x)=x^2/2, alpha=beta=eta=1, y=r=0, z0=(1,1), T=pi/2 and clocks e1=0,e2=1/4, the first jump time is 0 and the second is 5pi/12 in (0,T). Thus E_1(T) is false despite an interior event. The canonical exponential law assigns these zero-clock inputs probability zero. The density identity was not refuted; v2 restricts the count gloss to its correct almost-sure scope.

Distinct reviewer recheck is required for this successor. No acceptance follows from its creator applying these corrections.
