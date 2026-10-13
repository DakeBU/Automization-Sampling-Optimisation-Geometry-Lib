# Independent prospective mathematics and type-contract review 76

Reviewer: /root/header_math72. This is a prospective header review only.
No full target proof, proof search, implementation, SAU, source acceptance,
decoder acceptance, PROVED_LOCAL or VERIFIED credit is supplied.

The original 6763-byte header, RAW/LF SHA256
d076b2712eafb04f22540a54c06cc0f79660042e6dba068de54c64fb6074962b,
has mathematically correct intended definitions and ten conclusion groups, but
fails Lean type elaboration at two NNReal-to-Real coercion sites. It should not
be sealed in that form. The exact minimal reliable type overlay below gives the
6787-byte owned v3 candidate, RAW/LF SHA256
996b8a89ffe84cfef8faf75551f962f2378db221841f5e1a38137eb81281d015.
That complete v3 header is accepted mathematically and as a type contract only.
The root original header is unchanged. Distinct source review/adoption remains
required; the accepted file still deliberately ends with an unproved `:= by`.

## Exact type defect and minimal overlay

At original lines 53 and 68, the expressions used as real flow times are:

```
((τ y xRef a.2 e).untopD 0 : ℝ)
((τ y xRef a.2 (e n)).untopD 0 : ℝ)
```

The outer expected type ℝ makes elaboration instantiate WithTop.untopD on ℝ,
although τ has type WithTop ℝ≥0. Both original predicate-only and complete
public-telescope type drivers fail with that exact mismatch. The minimum
reliable repair first constrains the entire finite extraction to ℝ≥0:

```
(((τ y xRef a.2 e).untopD 0 : ℝ≥0) : ℝ)
(((τ y xRef a.2 (e n)).untopD 0 : ℝ≥0) : ℝ)
```

Each replacement occurs exactly once. Every other byte, all public binders and
every mathematical formula remain unchanged. The inserted inner ascription is
only a type constraint followed by the intended finite coercion. It introduces
no certificate, cap, premise, theorem weakening or phase at infinity.

The intermediate v2 proposal annotated only the zero default as `(0 : ℝ≥0)`.
That was insufficient: under the outer real expected type Lean coerced the
default to ℝ and retained the same wrong WithTop base type. Both negative v2
drivers and their full terminal outputs are preserved. v2 is not accepted. No
further proof route or mathematical change was needed for v3.

## Expanded telescope and data scope

E has NormedAddCommGroup, real InnerProductSpace, FiniteDimensional ℝ,
MeasurableSpace and BorelSpace instances. These are the finite-dimensional real
Hilbert/Borel setting, with no Nontrivial or positive-dimensional premise.
V:E→ℝ, α β:ℝ≥0 and η:ℝ are implicit analytic data. The public and private
telescopes retain exactly the same six explicit conditions:

1. hα: 0 < (α:ℝ).
2. hαβ: α≤β.
3. hV: ContDiff ℝ 2 V.
4. hH: for every x,v, α‖v‖² ≤ D²V(x)[v,v] ≤ β‖v‖².
5. hη: 0<η.
6. hβη: βη≤1.

There is no EXCESS analytic condition. In particular, gradient Lipschitzness,
joint Borel flow/bounce/clock laws, the original-energy envelope and waiting
bounds are internal consequences of the actual73/74/75 parents, not public
provider premises. The six retained callers are ordinary standing analytic
conditions; the recursion is not disguised as a conclusion assumed from them.

y,xRef,z₀ and the arbitrary threshold sequence e:ℕ→ℝ≥0 are universally
quantified data inside the conclusion. For each finite n, the record and event
time are measurable jointly in ((y,xRef),(z₀,e)), where the sequence carries the
canonical product measurable structure. No probability measure, iid hypothesis,
positive-threshold assumption or integrability/mean certificate is imposed on
this deterministic sequence. e n corresponds to the source E_(n+1); the first
successor uses e 0. Threshold zero is an explicit deterministic extension.

## All eleven literal definitions

1. c(y,xRef)=y−η grad V(xRef).
2. Φ_t is the exact actual73 harmonic arc: position
   c+cos(t)(x−c)+√η sin(t)p and momentum −sin(t)(x−c)/√η+cos(t)p.
3. S(xRef,(x,p))=(x,p−[2⟨p,h⟩/‖h‖²]h), h=grad V(x)−grad V(xRef).
   This expands the actual74 zero-safe reflection; Lean's division convention
   gives S=(x,p) at h=0. No continuity of S at h=0 is assumed or claimed.
4. rate=√η max(0,⟨p,h⟩), the actual rate, not a new arbitrary function.
5. H=(η⁻¹‖x−c‖²+‖p‖²)/2, the inherited weighted SUM with exact half factor.
6. C=√η β√(2H)[√(2ηH)+‖c−xRef‖], computed from the actual state.
7. Λ(t)=∫₀ᵗ rate(xRef,Φ_s z) ds, for nonnegative finite t.
8. τ(e) is the exact actual75 hittingAfter of the closed upper half-line for
   Λ−e, from time zero, valued in WithTop ℝ≥0. No finiteness is assumed.
9. next acts on R=(ℝ≥0×(E×E))⊕Unit. A stopped right record remains stopped.
   For an active (T,z), τ=∞ returns stopped. Only a finite wait produces
   (T+τ,S(Φ_τ z)). The v3 coercions explicitly pass finite NNReal values to Φ.
10. record is Nat.rec from Sum.inl(0,z₀), with the k-th update next(e k).
11. eventTime eliminates an active record to its finite T coerced to WithTop;
    a stopped record has event time ∞.

The sum has its native measurable structure. An active record always stores a
finite time and an actual phase. A stopped record stores only Unit, so there is
no phase at infinity or evaluation of Φ at infinity. Although untopD is a total
map with default zero, the top branch stops before selecting the finite update.
Its default therefore has no physical-time interpretation at an infinite wait.

## Ten conclusion groups: mathematical correctness

1. Base record. The Nat.rec base is exactly active (0,z₀), with no draw or
initial-law assumption.

2. Successor and active-branch characterization. Nat.rec gives the displayed
successor with e n. Given an active predecessor, the successor is stopped iff
that actual τ is top; a non-top τ yields exactly the finite-time, actual
postbounce update. The Sum constructors are disjoint. No arbitrary produced
state is substituted for this recurrence.

3. Joint Borel next. Actual75 gives joint Borel τ; the set τ=∞ is Borel. The
finite extraction untopD 0 is Borel, even though it is not continuous at top.
Finite addition, the NNReal-to-real inclusion, actual73 joint continuous Φ and
actual74 joint Borel S compose to a Borel finite update. A measurable if and
native sum elimination with the constant stopped branch give the exact joint
map in (y,xRef,e,r). The required API is available in the pinned imports:
WithTop.measurable_untopD/Measurable.untopD, Measurable.ite,
Measurable.sumElim and measurable_fun_sum. A claim of joint continuity of S,
next or τ would be unjustified; this header makes none.

4. Joint Borel record for every finite n. The base depends measurably on z₀.
Each successor composes group 3 with the preceding record and the measurable
coordinate evaluation e↦e n. Induction therefore gives the displayed map on
the full product-sequence space for each n. It needs no distribution on the
threshold sequence and no finite-support restriction. On the countable product
of NNReal spaces this is the expected product Borel setting.

5. Joint Borel eventTime for every finite n. The active projection T, its
WithTop coercion and the constant ∞ stopped branch are measurable. Compose
their sum elimination with group 4. No undefined phase projection from the
stopped constructor occurs.

6. Initial time and monotonicity. T₀=0. From an active record, a finite wait is
nonnegative and adds to T; an infinite wait changes event time to ∞. A stopped
record stays at ∞. Thus successor event times are nondecreasing and hence the
whole ℕ-indexed event-time function is Monotone. Strict growth is intentionally
not required for arbitrary sequences containing zero thresholds.

7. Absorbing stop. If record n is stopped, next is stopped at every later
step regardless of the thresholds. Induction on k proves record(n+k) stopped,
including k=0. No all-time stochastic nonexplosion conclusion follows.

8. Original-energy inheritance and outgoing arcs. Inductively, every active
phase has H=H(z₀): the base is immediate; an active successor is S(Φ_s z), so
actual73 conservation and actual74 bounce conservation preserve exactly H.
For each finite outgoing arc time t<τ, actual73 again preserves that original
energy. Actual rate nonnegativity and actual74's same-energy-layer bound then
give 0≤rate(Φ_t z)≤C(z₀). The layer cap is computed once from the actual initial
energy, not assumed for a hypothetical sequence of states. The finite-arc
restriction creates no phase at ∞. For τ=0 its strict-before interval is empty;
the active state's energy assertion remains meaningful and true.

9. Original cap, uniform increments and zero-cap stop. C(z₀)≥0 follows from
the actual energy formula and nonnegative factors. For an active record, group
8 implies C(z_n)=C(z₀), since the center/reference are fixed and C depends on
the phase only through H. Actual75 then supplies τ(e n)≥toNNReal(e n/C₀)
under C₀>0. A finite successor gives T_(n+1)=T_n+τ and the stated inequality;
an infinite successor makes its right side top. For an already stopped record,
both event times are top, and top plus the finite NNReal increment is top, so
the displayed inequality also holds. C₀=0 with e n>0 implies infinite τ by
actual75 and hence stop. There is no division-by-zero branch and no silent
C₀>0 standing assumption.

10. Zero threshold and strict finite positive-threshold growth. Actual75 gives
τ(0)=0, actual73 gives Φ₀=id, and next therefore keeps T and updates phase to
S(z). For a positive threshold, an active successor implies τ is finite; the
actual75 positivity result makes its finite value strictly positive, so its
addition strictly increases T. An infinite wait is correctly excluded only by
the active-successor premise, not by an extra finiteness assumption.

These arguments establish that the prospective statement is true and
dependency-ready given the exact compiled actual73/74/75 mathematical APIs.
They are natural mathematical review, not a Lean implementation of the target.
The current actual75 source admission remains a distinct pending prerequisite.

## Degenerate cases and remaining boundary

Rank zero is allowed: vectors, H, C and rate vanish. Positive thresholds stop
with infinite waiting time; zero thresholds give a zero-time identity update.
More generally, H(z₀)=0 forces x=c and p=0 because η>0; actual flow and bounce
leave that phase fixed, C₀=0, and the same threshold distinction holds.

A zero residual at one state makes the actual bounce the identity and the
instantaneous rate zero, but does not alone imply a zero rate on a future arc;
the header makes no such claim. αη=1 remains allowed; no factor 1−αη or strict
endpoint exclusion appears. η=0 remains excluded by the original condition.
If all thresholds are zero, times may all equal zero and phases may alternate
under an involutive bounce; they are indexed records, not a unique physical-time
phase. Consequently this packet must not be presented as a stitched process.

All finite n are quantified, but no limit T_n→∞, iid exponential product law,
positive thresholds almost surely, SLLN, random-process construction, cadlag or
PDMP property, Markov property, invariance/reversal, terminal half-turn kernel,
H/K/r_rho/B27/B28, mixing, cost/composition, full-paper or Goal credit follows.
The selected source contract's old prospective75/no-header76 wording records
its historical pre-read stage; it is not a new mathematical condition.

## Type evidence and finite closure

Fixed Lean 4.33.0 and the pinned lake-manifest were checked. Both drivers use the
original Lake-selected import roots and direct Lean source elaboration, with no
Lake cache replay and no canonical output write. The predicate driver includes
the exact private definition and closes the two open sections. The public driver
preserves that definition and elaborates the complete public telescope as a
universally quantified Prop-valued definition, not a proof of that proposition.
Its #print output retains the exact six conditions. The API #checks are only
signature checks; no recursive theorem proof was implemented.

- Original candidate: predicate PID17652 EXIT1; public telescope PID48108 EXIT1.
- Insufficient default-only v2: predicate PID48272 EXIT1; public PID50760 EXIT1.
- Accepted inner-ascription v3: predicate PID29384 EXIT0; public PID48688 EXIT0.

Complete RAW drivers, stdout/stderr and actual terminal receipts are retained
for every type probe. An unrelated initial lookup of an optional historical75
driver filename failed because that guessed path did not exist; its exact error
and absent PID capture are explicitly preserved. It was not used as an input,
was not retried, and does not affect the current exact76 result.

Thirteen finite inputs have exact RAW snapshots, including the actual75 source
fd93d015...e23d and the actual imported75 olean, true73/74 sources, current
toolchain/manifest and minimal relevant Mathlib Borel/product APIs. LF pins
replace CRLF byte pairs only. All owned files are included in the final native
manifest; the lease is the last owned write. Postclose verification is strictly
read-only. Mathematical repair: none. Type repair: exactly the two inner NNReal
ascriptions above. v3 header acceptance supplies no theorem-proof credit.
