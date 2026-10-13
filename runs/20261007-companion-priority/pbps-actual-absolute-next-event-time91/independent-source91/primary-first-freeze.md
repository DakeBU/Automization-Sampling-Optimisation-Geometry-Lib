# Primary-first source expectation (stage 1, immutable)

Reviewer: independent source reviewer `/root/primary_source91`.
Scope: fixed arXiv:2609.06905v1, Appendix A.1 equations (A.1), (A.2), (A.7), Appendix A.2, and their standing assumptions and object definitions.
This record was written before seeing production Lean, a candidate statement, a decoder reconstruction, earlier fidelity decisions, or repair proposals. It is an expectation, not a verdict on an implementation.

## Source identity and rights

The primary input is `runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html`, SHA-256 `d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760` (1,482,128 bytes). Its local banner identifies v1, 7 September 2026, and the arXiv perpetual non-exclusive license. The official fixed-version abstract page, https://arxiv.org/abs/2609.06905v1, independently identifies the title, authors, and v1 submission. Its license link resolves to https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html. That license grants distribution rights to arXiv and is not a general permission to republish the full paper. This artifact contains independently authored mathematical description; it does not copy the source snapshot or prose. No second raw snapshot was made.

## Standing assumptions versus needed ingredients

The source studies finite-dimensional Euclidean phase space, V in C^2(R^d), and constants 0 < alpha <= beta with alpha I <= Hess V <= beta I everywhere, equation (1.1). Section 2.2 takes 0 < eta <= 1/beta. In particular grad V is globally beta-Lipschitz and continuous. These are the source-wide conditions, even when a bounded coordinate-measurability result uses only continuity and eta positivity. Any deliberate weakening must be labelled as such, not asserted to be the literal standing context.

For this construction y and the reference point r are fixed arbitrary vectors; the initial phase point z0 = (x0,p0) is arbitrary. Neither stationarity nor a Gaussian distribution of the initial momentum is needed for the fixed-reference recursion itself. Algorithm 1 later samples the reference from pi_eta^(X|Y=y) and independently samples p0 from N(0,I), holds the reference fixed throughout this run, and returns the position at time pi. The sequence of Exp(1) clocks is independent, with the fresh clock independent of the entire past. Full mixing-time warmness and complexity assumptions are not assumptions for this local coordinate.

## Objects and recursion required by the primary source

At r, write c = y - eta grad V(r), h_r(x) = grad V(x) - grad V(r), lambda_r(x,p) = sqrt(eta) max(<p,h_r(x)>,0). The deterministic flow is

Phi_u(x,p) = (c + (x-c) cos u + sqrt(eta) p sin u,
              -(x-c) sin u / sqrt(eta) + p cos u).

The bounce is B_r(x,p) = (x,R_(h_r(x)) p), where R_h reflects orthogonally to h for h != 0 and R_0 = I. At a zero residual normal the rate is zero; discontinuity of the bounce map is allowed. A continuity assumption on the bounce map would therefore be inappropriate.

At T0=0 and post-event state Z0=z0, let H_(Zn)(u) = integral from 0 to u of lambda_r(Phi_s(Zn)) ds. Formula (A.1) sets the next waiting time to inf{u >= 0 : H_(Zn)(u) >= E_(n+1)}. If this set is empty the next waiting time and absolute event time are infinity and the source stops its recursion. For a finite wait, (A.2) sets T_(n+1)=T_n+S_(n+1) and Z_(n+1)=B_r(Phi_(S_(n+1))(Zn)). Between events the state follows Phi. The time argument in H is elapsed time since T_n; the event-time coordinate T_(n+1) is absolute time since this run began. It is not S_(n+1).

The source provides the reflection update and the elapsed-to-absolute addition explicitly. A theorem about an abstract hazard inverse, an arbitrary supplied poststate map, or a supplied previous-time map has not yet identified this actual recursion unless those maps are discharged by its definitions or proved adapters.

## Complete histories and totalization

Fixing a deterministic depth n means recording the input parameters and the first n independent clocks (and hence every state/time recursively determined by them), with the next clock fresh. It is not sampling a new point from stationarity at depth n, forgetting the reference, or conditioning only on the last wait. The next-coordinate map must retain the same initial point, reference, all n clock inputs, and accumulated event time.

The source directly describes a stopped sequence: once an empty crossing set occurs, no next post-event state is defined. To make an everywhere-defined map at every deterministic depth, ASTIS may need an explicit cemetery/option encoding. Extending every later absolute event-time coordinate by infinity is a faithful representation of no further events, but is an implicit completion of the stopped source recursion, not another literal clause of (A.2). A dummy poststate used only after termination must be declared an off-event encoding and never interpreted as an actual bounce at infinity. Applying a finite flow to an infinite elapsed time without a guarded branch is not justified by the source.

Exp(1) clocks are strictly positive and finite almost surely. Raw clock products can include zero or other off-support inputs depending on their chosen carrier. Formula (A.1) uses >= and u >= 0: at threshold zero the infimum is zero, even for a vanishing hazard. Replacing >= by > requires an explicit equivalence argument on the relevant threshold domain; continuity and monotonicity alone do not remove all flat-level distinctions. The source's probabilistic statements may ignore null clock sets, whereas an everywhere-defined Borel coordinate or literal characterization needs its conventions specified. No claim that every clock sequence has strictly increasing finite times follows from the almost-sure statement.

## Measurability expectation, derived independently

Appendix A.2 says the flow, rate, and bounce are jointly Borel in their parameters; the integrated hazard is jointly Borel and continuous nondecreasing in elapsed time. Rational tests then establish measurability of crossing times. An implementation of this argument must handle the exact >= threshold convention, equality/plateau cases, and infinity, rather than silently use a strict test valid only away from a null threshold set. Recursion yields Borel event-time and poststate coordinates in (y,x0,p0,r,clock sequence), subject to the explicit stopped encoding. At each deterministic depth, addition of the finite previous absolute time to the next elapsed wait, and the terminated branch, complete the actual next-coordinate result.

Measurability of a caller-provided time/state map can be a reusable abstract lemma hypothesis, but the source-facing actual-coordinate theorem should supply that measurability from the source recursion. Likewise, positivity or regularity of the actual hazard should be derived from the source assumptions or clearly identified as a general interface assumption. Such proof results are dependencies, not added source-wide hypotheses.

For law-level use, on any alive history with current time a and poststate z, the fresh exponential clock gives survival P(S>u | history) = exp(-H_z(u)) for u >= 0. This is a statement of law, with equality-point conventions handled under the atomless threshold distribution. The finite next-absolute-time law is the elapsed-time law translated by a. When expressed as a density on s>a, it is lambda_r(Phi_(s-a)(z)) exp(-H_z(s-a)); a possible no-further-event mass sits at infinity and equals exp(-H_z(infinity)). This density/atom description is my mathematical consequence, not a numbered claim stated in Appendix A.2. A next-coordinate law must not discard the no-event atom or previous history; complete-history integration requires the real joint history law and a fresh independent Exp(1) factor.

## Full (A.7) boundary and independent source proof graph

Equation (A.7) fixes an arbitrary finite horizon t >= 0 and an initial point. It evaluates every bounded measurable functional Psi of the entire trajectory up to t. Its n-event term integrates over the ordered absolute event times 0<t1<...<tn<t. The prescribed path flows between those times and reflects at each one. Its weight is survival along the complete path through the horizon, multiplied by the rate at each pre-jump state. One must sum over all n>=0, including the no-event term with empty product. This is neither merely a marginal event-time CDF nor just a product of independent waiting-time distributions.

The source route is:

1. (1.1), (2.4), (3.4), (3.8), (3.9) supply the actual flow, residual rate and bounce.
2. (A.1)-(A.2), fresh independent exponential thresholds, and exact endpoint conventions supply successive waiting times, absolute times and poststates.
3. Shifted harmonic energy preservation by flow and reflection bounds the rate along all produced or prescribed paths from a fixed initial point. A positive bound gives S_j >= E_j / bound whenever finite; the zero-bound case has no events. The strong law then establishes non-explosion almost surely. No deterministic finite depth proves this by itself.
4. The one-step conditional clock law must be iterated over actual histories, with joint measurability, the finite-event density, and survival through the last interval to t. Conversion from elapsed durations to ordered absolute times supplies the simplex formula. The sentence asserting iteration in A.1 suppresses these measure-theoretic details; they remain substantive dependencies to discharge.
5. Sum the disjoint event-count cases, show exhaustion using non-explosion, and justify bounded signed functional integration and absolute convergence. The stated source bound uses the simplex volume t^n/n! and the fixed-energy rate bound.
6. The later path-reversal argument additionally uses (A.4)-(A.6), the measurable measure-preserving endpoint map, time reversal on the simplex, and termwise integration. These are beyond a next-time coordinate.
7. Appendix A.2 additionally builds a terminal-state Borel version from finite-jump approximations, using non-explosion and an explicit zero value on the exceptional limit-failure set. Integrating over reference, Gaussian momentum and clocks gives the measurable half-turn kernel. The exceptional terminal-state convention is stated there; it does not silently specify all posttermination jump states in (A.2).

Thus a correct actual next-absolute-event-time measurability or one-step law result is a bounded dependency of the construction. It does not alone establish (A.7), a complete path law, path reversal, invariance, terminal kernel measurability, stationarity, or Algorithm 1's full correctness.

## Review gate reserved for stage 2

Upon receiving the canonical anti-anchored packet and independent decoder, compare objects, domains, quantifiers, assumptions, conclusion, scopes/senses, and constant dependencies against this frozen expectation. The review must identify the actual stopped recursion and the role of any carrier totalization, and must distinguish exact source material from an implicit completion or generalization. No candidate acceptance or repair verdict is made by this freeze.
