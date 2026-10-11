# Candidate: terminally survived finite-count complete-path law

**Recommendation:** one next substantive unit can join 92 and 88 with the existing 79/80 realization to prove the terminally survived, count-indexed finite-history/path law. There is no new analytic or stochastic source assumption missing. There are genuine unproved adapters: localization of 88 to arbitrary history tests, a fixed-horizon no-event-atom lemma, measurable count selection, and finite-history interpolation into the whole-path carrier. These belong inside this coherent integration unit. Compilation effort has not been estimated or attempted.

This is dependency planning only. No claim, cell, ledger, proof, acceptance seal or status transition is created.

## Source expectation and exact scope

The primary-first expectation was written before inspecting 88/79/80. Source A1.E1/A1.E2 gives the stopped actual exponential-clock recursion; A1.SS1.p2 gives half-open arcs. A1.Ex19 and A1.SS1.SSS0.Px1.p4.1–p4.2 use strict ordered times and prescribed complete paths. A1.E7 is a whole-path functional identity, whose weight contains survival up to the terminal horizon, not only survival through the last completed wait. A1.SS1.SSS0.Px1.p4.3 provides the printed rate-cap/simplex absolute-convergence route. A1.SS2 supplies the measurable-realization context.

Keep all six original analytic assumptions: V globally C²; α>0; α≤β; α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for every x,v; η>0; η≤1/β. The Lean encoding βη≤1 is equivalent since β>0. No law, survival, nonexplosion, path-measurability or positive-conditioning-mass premise may be added. Finite-dimensional real Hilbert carriers including rank zero and nonnegative extended tests remain disclosed ASTIS extensions. The canonical product and total representations are ASTIS completions.

Use exactly the existing literal c, Φ, reflection S (identity at zero residual), rate, Λ and closed hitting-time τ. P is the countable product of Exp(1); ε(w,k)=toNNReal(w(k)). Rec=(NNReal×Phase)⊕Unit has an absorbing stopped tag. R₀=live(0,z₀), and the finite-wait update adds τ and stores SΦτ of the preceding phase. An infinite wait stops the recurrence. Let T_j be the live stored time or ∞ when stopped; initialization j=0 is not an event. H_n contains every R₀,…,R_n.

For t=(t₁,…,t_n) in Δ_n(T)={0<t₁<…<t_n<T}, put t₀=0, z_j=SΦ_(t_j−t_(j−1))z_(j−1). K_n(t) is the complete tuple live(t_j,z_j). The measure m_n,T is the existing comap of product real Lebesgue to the simplex subtype. Let

q_n(t)=∏_(j=1)^n [rate(Φ_(t_j−t_(j−1))z_(j−1)) exp(−Λ(z_(j−1),t_j−t_(j−1)))],

ρ_n,T(t)=ofReal(q_n(t) exp(−Λ(z_n,T−t_n))).

Equivalently use the existing ENNReal q multiplied by ofReal of the final exponential. Positivity and finiteness of these real factors justify the equality. At n=0, q₀=1, t₀=0, z₀ is the initial phase and the empty simplex is a singleton with mass1, including T=0.

## Exact bounded theorem candidate

Under the six assumptions, choose the jointly measurable actual phase Z supplied by theorem80. This is an internal choice of the existing existence conclusion, never a new public provider premise. For each finite T≥0 use the explicit carrier Path_T=([0,T]→Phase) with the coordinate-generated product measurable space. Let Z_T(w)(s)=Z(s,w).

Let B_n(T) be precisely theorem92's actual strict-prefix event. Define d_T(h)=T−lastTime(h) using NNReal truncated subtraction, with a total stopped-time observer outside live histories. Define

C_n(T)={w∈B_n(T): R_n(w)=live(a,z) and (T−a)<τ(z,ε(w,n))}.

The comparison takes place in WithTop NNReal; τ=∞ satisfies it. On B_n the last time is ≤T, including n=0,T=0, so the subtraction is the intended terminal duration. The clipped/stopped observer is never interpreted as a physical state at infinity.

For each simplex tuple define Γ_n,T(t)(s)=Φ_(s−t_j)z_j where j is the largest index in {0,…,n} with t_j≤s. This index exists since t₀=0. Internal event values are post-bounce (right-continuous convention); at s=T use j=n. This definition covers n=0 and T=0.

Prove the following package, for every fixed y,r,z₀ and finite T:

1. C_n(T) is measurable; Γ_n,T is measurable into Path_T; Z_T is measurable; ρ_n,T is measurable. A finite coordinate selection proves measurability of Γ, and theorem80 plus the product sigma-algebra proves measurability of Z_T. Joint finite-parameter dependence can be retained with the same fixed-T carrier.
2. On every raw sample w∈C_n(T), theorem92 identifies H_n(w)=K_n(t) for the observed tuple, and theorem80's pointwise covered-arc formula gives **Z_T(w)=Γ_n,T(t) at every s∈[0,T] simultaneously**. No AE intersection over uncountably many s is taken. Strict first-n times and strict terminal survival provide a covering finite interval for each s directly.
3. Construct a measurable integer N_T(w): the unique n with T_n≤T<T_(n+1), when a covering interval exists, and 0 otherwise. The disjoint measurable interval events give a measurable selector; theorem79 supplies existence/uniqueness a.e. For each fixed T, a.e. simultaneously for all n, N_T=n iff C_n(T). On the same fixed-T good event, N_T is the finite cardinality of {j≥1:T_j<T}, and also of {j≥1:T_j≤T}. The sets C_n are disjoint, and their union has full P measure.
4. For every n and every measurable F:Hist_n×Path_T→ENNReal,

   ∫_{N_T=n} F(H_n(w),Z_T(w)) dP(w)
   =∫_{Δ_n(T)} F(K_n(t),Γ_n,T(t)) ρ_n,T(t) dm_n,T(t).

   In particular P(N_T=n)=∫ρ_n,T dm≤1. This is an unnormalized law, valid for zero-mass count events, and preserves whole-history and whole-path tests. It is not merely a terminal state law.

## Reuse audit and the real missing adapters

**88, actual_conditional_next_wait_survival:** its expanded statement lines59–80 allows every measurable duration d depending on the entire history. Survival is strictly u<τ, false on stopped records. The conclusion is an event-probability identity for every measurable history set A, not yet an arbitrary weighted-test identity. Set d=d_T and localize A by theorem92's strict guard. Equality on all measurable sets gives the restricted history measure; nonnegative integration then handles arbitrary F(H). Combine with 92's all-test law applied to F times the survival weight. This needs no fresh independence theorem and no random-depth restart.

**79, actual_fixed_reference_physical_time_cover:** expanded statement lines56–67 already gives, on one per-parameter full-measure event, unique interval index for every finite time, plus unique live record and its strict remaining-wait comparison. Thus coverage and uniqueness are not missing prerequisites. This is stronger than the cautious possibility recorded in the primary-first expectation.

**80, actual_physical_time_measurable_phase:** expanded statement lines55–78 gives a jointly Borel Z, a pointwise formula on every covered interval for arbitrary raw inputs, explicit initial-phase fallback on uncovered points, and a per-parameter AE event common to all finite times, including Z(0)=z₀. No new global phase-process existence proof is needed. The missing work is the finite prescribed-path adapter and equality of entire functions, using the pointwise formula.

**76 plus UnitExponentialProduct:** theorem76's last conjunct distinguishes zero thresholds from positive-clock strict finite updates, and its earlier conjuncts supply initialization, monotonicity, measurability and absorbing stop. UnitExponentialProduct's fourth conjunct supplies one AE event with all raw clocks positive. These are the genuine dependencies for relating strict prefixes to actual finite count; 79's unique interval alone does not exclude multiple simultaneous raw zero-clock events.

**Fixed-horizon atomlessness, derived from 92:** for each j≥1 and fixed finite T>0, on the positive-clock event, T_j=T implies the first j records lie in B_j(T+1). Apply 92 with horizon T+1 and the measurable history test that its final live time equals T. Its simplex pullback lies in the coordinate hyperplane t_j=T, which has product Lebesgue measure zero and therefore also zero q_j-weighted measure. At T=0, positive clocks and theorem76 strict updates already exclude finite events there. A countable union over j gives P(∃j≥1:T_j=T)=0. Stopped times are ∞; the initial T₀=0 must be excluded. This proves the endpoint adapter without assuming it. It has quantifiers **∀ fixed T, AE w**, not AE w,∀T; the latter would exclude all jumps and is false in general.

The total measurable count selector is defined for every raw sample, but its count interpretation is AE. For example raw threshold0 may create a jump at0; it is not legitimate to replace C₀(0) by all samples pointwise. Nevertheless P(C₀(0))=1, N₀=0 a.e., Z₀ is the constant initial path a.e., and the n=0,T=0 integral is exactly F(initial history,initial path). For n>0,T=0 both sides vanish. Using ≥ instead of strict terminal survival would allow a bounce at T and break the claimed whole-path terminal value unless that null boundary is explicitly removed.

## Source graph and remaining boundary

The proposed join consumes PREFIX92 and discharges SURV92, the fixed-horizon END92 adapter, COUNT92, and PATH92 for the explicit coordinate-measurable path carrier. It yields a fixed-count path law with a product of segment survival factors. This is a substantive source-implicit ingredient of A.7. It does not retroactively change the source-derived graph or claim accepted proof status.

ALG92 remains: prove that the n completed hazards plus the terminal hazard equal the integral of rate along Γ on [0,T], ignoring finitely many jump endpoints; identify each pre-jump rate with the left-limit rate. TERM92 in its exact printed full-hazard form then follows. A7 assembly still needs the countable partition/Tonelli passage and bounded signed-test justification (printed cap/simplex-volume route, or a separately checked mass-based alternative). The proposed candidate does not claim these closures.

The author does not specify a Skorokhod measurable carrier in A.7. The product path carrier above is an explicit completion sufficient for all coordinate-measurable path functionals. If the next seal instead promises every Borel functional on a cadlag/Skorokhod path space, it must also prove finite-path cadlag regularity and the relevant sigma-algebra/representation compatibility. That is a genuine additional dependency, not supplied by 88/79/80 and not silently included here. No random-depth restart, invariance, reversibility, mixing, expected cost or full-paper claim is proposed.
