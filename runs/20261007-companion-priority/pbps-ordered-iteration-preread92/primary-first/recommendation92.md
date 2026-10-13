# Source-first recommendation: actual finite ordered-prefix law

This is a bounded mathematical preread, not an SAU claim, theorem seal, proof, or canonical status change. The fixed primary source was reread for this recommendation; no implementation Lean was read during this preread to determine topology. The reviewer previously reviewed the phase-91 theorem and discloses that context, so this is not a claim of never having seen any related implementation. No previous reviewer verdict determines the statement below.

## Recommended next edge

Prove the **actual first-n-event complete-history law on the strict ordered-time simplex**, for every deterministic n and finite horizon T. Retain the complete sequence of event times and post-event states. This exposes the finite product hidden in the author's iteration sentence before (A.7). It is an attributed ASTIS completion of that sentence, not a printed standalone author theorem.

### Exact mathematical statement

Let d be a finite dimension, V in C^2(R^d), 0<alpha<=beta, and assume

    alpha |v|^2 <= D^2 V(x)[v,v] <= beta |v|^2   for every x,v in R^d.
    0 < eta <= 1/beta.

These are the original standing assumptions (1.1) and Section 2.2. Fix arbitrary y,r in R^d and z0=(x0,p0) in R^d x R^d. Use exactly

    c = y - eta grad V(r),       h(x) = grad V(x)-grad V(r),
    lambda(x,p) = sqrt(eta) max(<p,h(x)>,0),
    Phi_s(x,p) = (c+(x-c)cos(s)+sqrt(eta)p sin(s),
                  -(x-c)sin(s)/sqrt(eta)+p cos(s)),
    B(x,p) = (x,R_h(x) p),       R_0 = I,
    L_z(u) = integral_0^u lambda(Phi_s(z)) ds  for u>=0.

On a probability space carrying independent unit exponential clocks E1,E2,..., use the actual recursion (A.1)-(A.2): T0=0, Z0=z0, waiting time inf{u>=0:L_Zj(u)>=E_(j+1)}, cumulative time T_(j+1)=T_j+wait, and Z_(j+1)=B(Phi_wait(Z_j)) when the wait is finite. An empty hitting set terminates the recursion. For total histories at deterministic depth, one may encode termination by a distinct absorbing stopped tag; it never denotes a live state at a finite event time. The canonical product realization is a literal realization of these inputs, not an additional independence/provider premise.

Let n>=0 and T>=0 be deterministic, with T finite. Define

    Delta_n(T) = {(t1,...,tn) : 0<t1<...<tn<T}.

Delta_0(T) is the singleton empty tuple for every T>=0, carrying mass one. For t in Delta_n(T), put t0=0, z_0^t=z0 and recursively

    delta_j = t_j-t_(j-1),
    z_j^- = Phi_(delta_j)(z_(j-1)^t),
    z_j^t = B(z_j^-),                         j=1,...,n.

Let K_n(t) be the whole live history ((0,z0),(t1,z_1^t),...,(tn,z_n^t)). Let H_n be the whole actual history through event index n. Define E_n(T) as the event that these first n events are live and their times satisfy 0<T1<...<Tn<T; E_0(T) is the whole probability space. This is the event of **at least n strict interior events**, not the event of exactly n events before T: it places no condition on T_(n+1).

Define the nonnegative finite-prefix weight

    q_n(t) = product_(j=1)^n [lambda(z_j^-) exp(-L_(z_(j-1)^t)(delta_j))].
    q_0(empty) = 1.

Then E_n(T) is measurable, K_n and q_n are Borel on their simplex domains, and for every nonnegative extended-valued Borel function F on the complete history space,

    integral_(E_n(T)) F(H_n(w)) P(dw)
      = integral_(Delta_n(T)) F(K_n(t)) q_n(t) dt.

Here dt is n-fold real Lebesgue measure restricted to the strict simplex, with the mass-one empty-product convention at n=0. Equivalently, the pushforward of P restricted to E_n(T) under H_n equals the pushforward of q_n dt under K_n. In particular integral q_n = P(E_n(T))<=1. All restrictions are unnormalized, and no assumption that P(E_n(T))>0 is made. The formula covers n=0, T=0, zero hazard and histories whose next wait is infinite. F may depend on every recorded time and poststate, not just the final position. Measurability, density identification, and finite-prefix support are conclusions to prove, not new source assumptions.

For future integration against the initial phase law, the prescribed-history construction and weight should also be established jointly Borel in (y,r,z0,t) on the corresponding simplex domain, with V,eta fixed. This follows by the same finite Borel recursion; it should be included as a supporting conclusion, not as an added binder. A coordinate-free finite-dimensional inner-product formulation is acceptable if explicitly identified as such; it must retain all standing analytic assumptions.

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
7. Obtain measure equality and subprobability mass from nonnegative tests. Preserve the at-least-n event interpretation and the absent final survival factor.

This source route needs only the actual one-step complete-history finite-event law, prescribed-history identification, Borel parameter integration, finite product-coordinate bookkeeping and induction. A separate full unweighted history-dependent shear theorem is not needed if the absolute one-step law already supplies the translated density.

## Genuine remaining boundaries toward full (A.7)

After this next edge, q_n must still be multiplied by the conditional no-further-event factor

    exp(-L_(z_n^t)(T-t_n)).

This is evaluated at the history-dependent remaining duration. It is neither another jump-rate factor nor normalization of q_n. It converts the first-n-event law to an exactly-n-event-at-horizon law, with the chosen strict/non-strict endpoint convention justified. Existing terminal-survival input may be reused, but its composition at these prescribed histories is still a real obligation.

The sum of the n elapsed segment hazards plus the final segment hazard must be identified with integral_0^T lambda(zeta_s^t) ds. Every factor lambda(z_j^-) must match the rate at the prescribed path's pre-jump state. Actual trajectories on the count event must be identified with the complete prescribed path, with Borel path-observable composition; equality only of terminal states is insufficient.

Almost-sure nonaccumulation and half-open interval coverage supply the exhaustive finite-count partition. These are necessary source ingredients, but this preread does not reopen or reprove the already tracked actual-input nonaccumulation78/coverage79 results. The remaining task is their application to the full path/count representation and strict horizon conventions. No-atom reasoning is required only where strict and non-strict finite-event endpoint conventions are equated; it is not a new hypothesis for the proposed strict prefix law.

Finally, sum over n, justify bounded signed functional integration and absolute convergence, and retain the n=0 no-event path term. The printed cap/simplex-volume argument is a sufficient route. A nonnegative count-partition/Tonelli route followed by bounded signed decomposition is a possible ASTIS alternative, not another mandatory independent assumption. Path reversal (A.8), invariance, the L2 semigroup, averaged kernels, physical-time Markov restart and all main sampling/composition claims remain downstream.

## Classification and stopping boundary

Printed source objects: original assumptions, flow/rate/bounce, (A.1)-(A.2), the simplex, prescribed path and full (A.7).

ASTIS completion: tagged total finite histories; explicit first-n-event prefix density with arbitrary nonnegative complete-history tests; induction and exact finite-product coordinate transport. These elaborate the source's omitted iteration details without changing its target or assumptions.

No implementation was created or reviewed for this next edge. No SAU, source-review acceptance, theorem seal or publication status is claimed. A proving worker must first check current reusable interfaces against this source-derived target, then seal the exact statement and independently review any genuine semantic repair.
