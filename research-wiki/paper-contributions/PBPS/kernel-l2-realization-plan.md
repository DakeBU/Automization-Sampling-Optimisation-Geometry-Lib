# PBPS actual kernel/L2 realization — one bounded packet

Status: exact statement/source topology independently accepted before proof;
producer and focused test compiled locally (3259 jobs), standard axioms only.
Post-proof semantic/independent verification, integration and purification remain pending.
Statement seal: `fc2c39d412f077d007b509cebf2952eb7ed3e39a81032f2af07f8e0619099e23`.
Owned target: `ActualKernelL2Realization.actual_kernel_l2_realization`.
Original four-paper Goal, cycles, memory and current continuity stabilization are unchanged.

## Mathematical delta

Keep the SAME actual Z, phase law nu, real-L2 family A, zero-time strong
continuity, momentum flip and Gaussian averaging witnesses from the accepted
continuity parent. Join the existing joint-index probability kernel to Z by
the exact fiber equation Kphase(index)=map(Z(index))P. Its fixed-parameter
state-kernel preserves nu. For every real L2 class f, use its canonical Borel
representative to derive AE fiber integrability and A_T f = integral f dKphase
as equality of L2 representatives AE. Derive positivity and every constant
class being fixed. Do not add any of these as source assumptions.

Consumers: a later Gaussian-momentum-averaged actual position kernel identified
with M A_T B; actual phase semigroup construction after a SEPARATE restart edge.
These are planned uses, not existing Lean consumers.

## Source-only graph and coverage

Primary: arXiv:2609.06905v1 Appendix A.1 Proposition A.1 and Definition D.2.
The source-only seven-node prereview already identified:
S0 literal flow/bounce/rate; S1 exponential clock/nonexplosive realization;
S2 ordered-event expansion; S3 time reversal/Gibbs stationarity;
S4 measurable endpoints -> probability kernels;
S5 stationarity + kernel fibers -> invariance/fiber integrability;
S6 all-L2 realization and Markov-operator constants/positivity.
Dependencies: S0 -> S1 -> S2; S0 AND S2 -> S3; S1 -> S4;
S3 AND S4 -> S5; S5 -> S6.
S0--S3 are existing substrate, S4 existing kernel parent, S5--S6 selected.
Appendix A.1's process Markov/semigroup assertions are explicitly excluded here
and remain red. Definition D.2 density evolution/adjoint fixed constants and
chi-square identities are excluded from this bounded packet; they are not
silently claimed from A preserving constants. Hypocoercivity and cost regions
are excluded as separate consumers. Exact independent source/topology prereview
accepted after the coverage and B4 acyclicity corrections; see the adjacent
kernel-l2-realization-prereview.md. The statement digest never changed.

### Source-region inventory (v1 HTML line locators at inspection)

The seven-node diagram is a compressed spine. This table records the retained
and excluded fine regions of the sealed interface; NODE means a source/proof
obligation, not an additional completion badge.

| Source region | Disposition and node | Scope / actual inherited reference |
| --- | --- | --- |
| A.1,710--722: rate, harmonic flow, bounce, clocks, (A.1)--(A.2), stopping and between-jump prescription | NODE S0,S1 | Literal source dynamics retained by both actual-process parent interfaces. |
| A.1,724--744 up to global nonexplosion/uniqueness | NODE S1 | Existing actual nonaccumulation, physical cover and measurable phase parents; raw witness identification is B1 below. |
| A.1,744: final memorylessness/time-homogeneous Markov assertion | EXCLUDED | Distinct restart/process Markov/Chapman--Kolmogorov edge, not supplied by probability fibers. |
| A.1,745--750 and (3.1): momentum flip and phase density | NODE Nnu,S0 | Existing ActualPhaseNormalization and inherited flip law; exact probability normalization is reused internally. |
| Prop A.1(i)--(iii),753--768 | NODE S3,S5,S6,Nflip,Nsc,Npos for the exact retained components | Invariance, L2 flip/contraction, zero-time continuity and Gaussian self-adjoint contraction retained. The semigroup assertion in (ii) and position-kernel Markov conclusion in (iii) remain excluded future edges. |
| Idea of proof,771--789: formal generator/adjoint/exponentiation | EXCLUDED | Nonselected heuristic OR-route. No generator domain or integration-by-parts shortcut enters this proof. |
| A.1,792--805: arc density, (A.4)--(A.6), reversal and Borel volume preservation | NODE S0,S3 | Inherited source reversal/Gibbs parents, not reproved as new leaves. |
| A.1,806--811: ordered times, complete path expansion (A.7), summability | NODE S2 | Inherited actual clock/path-density and bounded expansion parents. |
| A.1,813--821: (A.8), Borel change of variables, matched survival/rates, Tonelli and signed duality | NODE S3 | Inherited prescribed reversal, weighted sectors and bounded Gibbs duality; full L2 extension is Nflip. |
| A.1,822: invariance and density extension to (A.3) | NODE S3,Nflip | Existing ActualBoundedGibbsDuality and ActualL2FlipDuality; preserved by the continuity parent. |
| A.1,823--826: Jensen contraction, small-time core limit, DCT and density | NODE Nsc | Inherited ActualL2Expectation, ActualOuterBoundedL2Continuity and accepted ActualL2StrongContinuity; exact inherited cell ASTIS-SW-PBPS-actual-l2-strong-continuity and its l2-strong-continuity-prereview.md eight-node coverage. No new semigroup claim. |
| A.1,828--831: Gaussian averaging/flip absorption, self-adjointness and contraction | NODE Npos | Inherited ActualPositionL2Averaging; JB=B, MJ=M, Kpos=M A B. Literal position probability-kernel realization and its Markov packaging are a later consumer, excluded here. |
| D.1,1575--1584: real L2, norm, AE equivalence and adjoint convention | NODE Q0 | Canonical Mathlib Lp quotient/representatives and inherited L2/flip/averaging contract. Other D.1 orthogonal projections and Loewner/spectral material are EXCLUDED as unused in this packet. |
| D.2,1591--1594: invariant kernel observable integral (D.4), contraction and fixed constants of K | NODE S4--S6 | Existing probability-kernel parent and L2 contraction; new same-Z realization, AE positivity and all constants. Positivity is an explicit ASTIS analytical completion of the Markov-operator interpretation, not a new paper assumption. |
| D.2,1594--1600: adjoint density evolution/fixed constants, (D.5), centered norm-to-chi-square transfer | EXCLUDED | Independent downstream results; not claimed from constants of the observable operator alone. |

ASTIS analytical completion nodes, rather than additional source hypotheses:

- B1: exact equality of the two existential Z witnesses from the same raw
  record/arc/fallback prescription (S1 -> S4 and same-A identification).
- Q0: canonical strongly measurable Lp representatives and AE quotient equality,
  expanding the source's D.1 convention.
- B2: exact endpoint product pushforward -> invariant state-kernel measure
  (S3 AND S4 -> S5), with index nesting and measurable sets explicit.
- B3: canonical-representative integral-map and AE fiber integrability
  (S5 AND Q0 -> S6), retaining the SAME operator A.
- B4: positivity follows from S5 invariance AND Q0 AND B3's realization
  equality, by AE null-set transport and nonnegative integration. Constants
  follow from Nnu probability AND S4 probability fibers AND B3's realization
  equality. S6 is the aggregate output of B3/B4, never an input to B4.

These bridge nodes complete omitted bookkeeping; none is a theorem binder or
an invented source citation. Parameterwise AE is retained, not one event
uniform in all times, parameters and L2 observables.

## Reuse and proof plan (now implemented and focused-compiled)

Search completed: actual phase kernel, accepted actual L2/flip/position/continuity
interfaces; existing KernelInvariance; pinned Mathlib Kernel.Invariance,
Kernel.Composition.MeasureComp/MapComap and Lp representative APIs. No generic
kernel-to-Lp operator constructor was found in the inspected pinned kernel tree;
do not duplicate the existing L2 family.

1. Obtain the accepted continuity witnesses and existing phase kernel witnesses.
2. Identify their actual Z pointwise from identical record/arc/fallback clauses.
3. Reuse normalization internally and derive fixed-parameter kernel invariance
   from the existing measure-preserving endpoint and exact map fibers.
4. Transfer the existing clock-side integrability/AE class identification to
   kernel fibers using canonical Lp strongly measurable representatives.
5. Derive positivity by product AE/Fubini and nonnegative integral, and constants
   from probability clocks. Preserve the actual A, not a newly chosen operator.
6. Retain all prior flip, strong-continuity and Gaussian-averaging conclusions.

Do not silently identify two existential Z witnesses; do not demand a common
full-measure event over all parameters/times; bounded Borel tests alone are
not the promised all-L2 realization. Probability fibers are NOT process
Markovness. Do not replace a real representative obligation with totalized
integral syntax.

## Review / delivery

One writer (root_20261016); independent precise source/topology prereview before
proof, then focused compile, independent exact-commit compiler/math review,
anonymous encoder and fresh anti-anchored source reviewer, all via existing
protocol. Mathematical exposition and adjacent folded exact Lean will be
authored once in the existing lesson/publication system after actual compilation.
No shared Registry/root edits outside the already-owned sole stabilization lane.
Conceptual mirror audit: none-found (exact kernel realization of an existing
operator; no new cross-domain mechanism). No graph-only agent.

