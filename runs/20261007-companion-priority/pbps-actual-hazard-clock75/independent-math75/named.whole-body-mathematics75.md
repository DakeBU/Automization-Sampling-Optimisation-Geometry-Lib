# Independent whole-body mathematics review 75

Reviewer: /root/header_math72. Status: ACCEPTED_MATHEMATICS_ONLY.
Checked repository parent: 526a6af98cf0380032a3aed52da01c5304de3bb8.
Exact candidate: AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean,
396 lines, 21771 bytes, RAW = CRLF-pairs-only LF SHA256
fd93d01583eec206285573c1f1631b94739f95471c50e1ff940e66080238e23d.

This is an independent review of the entire frozen statement and actual proof
body. It supplies no primary-source acceptance, source-blind decoding, VERIFIED
transition, reader acceptance, purification, Exposition Seal, process construction,
whole-paper or Goal completion. No mathematical repair is required.

## Exact statement and binder expansion

I checked the complete private Prop at lines 16–72 and the public declaration at
192–202 against the frozen v2 candidate and expanded literal. The private
predicate and public telescope are exact; there is no new clock-law provider or
certificate binder. E is an arbitrary finite-dimensional real inner-product
space with its Borel measurable structure. No positive dimension is required.
V : E → ℝ, α and β : ℝ≥0, η : ℝ. The six caller conditions remain:

1. hα: 0 < α, with α coerced to ℝ.
2. hαβ: α ≤ β.
3. hV: V is C² over ℝ.
4. hH: α‖v‖² ≤ D²V(x)[v,v] ≤ β‖v‖² for every x,v in E.
5. hη: 0 < η.
6. hβη: βη ≤ 1.

There is no extra cap, coercivity, regularity, hitting-time finiteness,
strictly-positive-rate, independent-randomness or path premise. The lower
curvature conditions and step-size upper bound are retained standing conditions;
the new integral/clock argument does not need a strict αη < 1. The actual rate
parent internally produces β-Lipschitzness of gradient V from hV/hH using
QuadraticRegularization with r = 0, rather than requiring a Lipschitz certificate
from this caller. The harmonic parent needs C¹ regularity and η > 0 for its
literal formulas; those follow from the retained conditions.

All eight definitions are the actual functions, at the same y, xRef and z=(x,p):

- c = y − η grad V(xRef).
- Φ_t(x,p) = (c + cos(t)(x−c) + √η sin(t)p,
  −sin(t)(x−c)/√η + cos(t)p).
- rate(xRef,(x,p)) = √η max(0, ⟨p, grad V(x)−grad V(xRef)⟩).
- H = (η⁻¹‖x−c‖² + ‖p‖²)/2, a weighted SUM, with the exact half factor.
- C = √η β √(2H) [√(2ηH) + ‖c−xRef‖].
- Λ(t) = ∫₀ᵗ rate(xRef, Φ_s z) ds for t : ℝ≥0, a real-valued integral.
- τ(e) is Mathlib hittingAfter on continuous time ℝ≥0 for the closed target
  [0,∞) of Λ(t)−e, starting at 0; its codomain is WithTop ℝ≥0.
- W is the pushforward of expMeasure (1 : ℝ) by e ↦ τ(Real.toNNReal e).

The nested products were expanded: the clock parameter has type
(E×E) × ((E×E)×ℝ≥0), represented by ((y,xRef),z,e). The joint Λ parameter
has type ((E×E)×(E×E))×ℝ≥0. Every projection in the continuity and
measurability compositions selects the intended y, xRef, z and time/threshold.
W is the actual first-clock law on extended nonnegative time. It is not a
terminal-state kernel or an assumed first-clock-law witness.

## Entire implementation inventory

Lines 1–15 supply imports, namespace and noncomputable/autoImplicit settings.
Lines 16–72 are the full private specification. Lines 74–189 prove the private
primitive helper; its six-definition telescope is explicit, and its output is
precisely groups 1, 2, 3, 4 and 9. Lines 191–265 state the public theorem, repeat
the eight literal definitions, expand the Prop with change, and apply that
proved private helper. Lines 266–390 prove crossing, infinity, first-hit
equality, positivity, zero threshold, measurability, the actual Exp law and
waiting bounds. Lines 391–396 assemble the ten groups and close the sections.
No body is a wrapper around an assumed conclusion. The helper is proved in this
module and only consumes the unchanged actual harmonic-flow and bounce/rate
parent theorems.

## Ten conclusion groups and proof audit

1. Joint continuity of Λ in (y,xRef,z,t). The harmonic parent supplies joint
continuity of Φ and the rate parent supplies joint continuity of rate. Their
composition is jointly continuous in ((y,xRef,z),s). The parametric primitive
theorem on real intervals gives continuity in the parameters and upper endpoint;
composition with the continuous inclusion ℝ≥0 → ℝ gives exactly the statement.
This use needs no uniform global domination or additional derivative bounds.

2. Joint Borel measurability of Λ. It follows from the preceding continuity in
the stated finite-dimensional Borel product spaces. This is stronger than only
checking each separate y/xRef/z slice. No measurability is silently inferred for
an arbitrary non-Borel representative.

3. Finite-interval integrability. For each fixed y,xRef,z, the integrand is a
continuous real function of s on every finite real interval. The helper proves
interval integrability for arbitrary real endpoints a,b and specializes to 0,t.
This does not assert integrability on the whole nonnegative half-line.

4. Λ(0)=0, Λ(t)≥0 and monotonicity. The rate is nonnegative for every state;
the integral has nonnegative orientation because t is nonnegative. Monotonicity
compares nested [0,s] and [0,t] using the actual nonnegative integrand and finite
interval integrability. No real-time monotonicity for negative t is claimed.

5. Exact finite-time crossing identity τ(e) ≤ t iff e ≤ Λ(t). At lines 269–287,
the proof unfolds hittingAfter and splits on existence of a crossing. For a
nonempty set F={s≥0:e≤Λ(s)}, F is closed by continuity of Λ and bounded below by
0. Closed-set csInf membership makes q=inf F an actual crossing, so q≤t and
monotonicity imply e≤Λ(t). Conversely, t∈F gives inf F≤t. When F is empty,
τ=∞, both finite-time sides are false. This is a continuous-time closed-infimum
argument. It does not use the discrete well-founded-time hittingAfter lemmas or
WellFoundedLT. Closedness is essential here and is actually derived.

6. Infinity, finite first-hit equality, positive thresholds and zero threshold.
The defining infinity characterization is τ(e)=∞ iff Λ(t)<e for every finite t.
For finite τ=q, group 5 first gives e≤Λ(q). If e<Λ(q), the intermediate value
theorem on the real-order interval [0,q] in ℝ≥0 produces s≤q with Λ(s)=e,
using Λ(0)=0≤e. Strict overshoot forces s<q, while group 5 forces q≤s: a
contradiction. Thus Λ(q)=e. The proof uses untop only under τ≠∞ and then
identifies untopA in that branch. For e>0, τ≤0 would force e≤Λ(0)=0. For e=0,
group 5 immediately gives τ(0)=0. Plateaus of Λ, a finite limiting total hazard,
or a limit equal to e that is never attained cause no invalid finite-hit claim.
The result deliberately allows ∞.

7. Joint Borel measurability of τ in all y,xRef,z,e. The proof checks inverse
images of Iic b in WithTop ℝ≥0. For b=∞ the inverse image is the whole space;
for finite b=t it is exactly {e≤Λ(y,xRef,z,t)} by group 5. That set is Borel by
the already proved joint measurability and the continuous threshold coercion.
This proves Borel measurability, without asserting continuity of τ or a
stopping-time property relative to an unstated filtration.

8. Actual Exp(1) pushforward probability and strict survival. The rate parameter
1 is strictly positive, so Mathlib's expMeasure is a probability measure. The
threshold-to-clock map is measurable by group 7 and measurability of toNNReal,
and its pushforward is a probability measure on WithTop ℝ≥0. For every real e,
not just almost every e, group 5 and nonnegative Λ give

  τ(max(e,0)) > t  iff  Λ(t) < max(e,0)  iff  Λ(t) < e.

The final equivalence uses Λ(t)≥0. Therefore the exact inverse image of the
strict extended-time tail (t,∞] is the real interval (Λ(t),∞). The proof uses
the complement of the closed lower interval and the actual exponential CDF:

  W((t,∞]) = 1 − [1 − exp(−Λ(t))] = exp(−Λ(t)).

The strict/non-strict endpoints are correctly matched; at t=0 this gives mass
1 on positive extended time. No separate support or zero-atom lemma is claimed
or needed by this implementation. There is no implicit almost-sure finiteness;
mass at ∞ is compatible with every displayed equality. W is an exact defined
measure, not a hypothetical survival certificate.

9. Nonnegative actual energy cap and Λ(t)≤Ct. The helper takes energy
conservation H(Φ_s z)=H(z) from actual73. It applies actual74's same-energy-layer
rate bound to the actual state Φ_s z, with the unchanged center, gradient and
reference point. Thus rate(Φ_s z)≤C for every real s. Nonnegative factors give
C≥0; integral comparison with the constant C yields Λ(t)≤Ct. The factors
√η, β, √(2H), √(2ηH), the displacement ‖c−xRef‖ and the half in H are exact.
No arbitrary envelope premise has been substituted for this derived C.

10. Waiting-time lower bound and zero-cap branch. If C>0 and τ=∞, the bound
toNNReal(e/C)≤τ is immediate. If τ=q is finite, group 6 and group 9 give
e=Λ(q)≤Cq, and division by the genuinely positive C gives e/C≤q. Coercion via
toNNReal and WithTop preserves that comparison. There is no division by C=0.
If C=0 and e>0, group 9 implies Λ(t)≤0<e for every finite t, so τ=∞ by group 6.
The separate e=0 branch remains τ(0)=0; it is not incorrectly included in the
zero-cap positive-threshold assertion.

## Degenerate and boundary cases

The rank-zero real inner-product space is allowed. All vectors then vanish,
H=C=rate=Λ=0, τ(0)=0 and τ(e)=∞ for e>0. The exponential pushforward is mass
one at ∞, consistently with survival exp(0)=1 for each finite t.

For any dimension, H=0 and η>0 force p=0 and x=c. The literal harmonic state is
constant (c,0); the rate, integrated hazard and cap vanish. The same conclusions
hold, even if grad V(c)−grad V(xRef) is not zero. An instantaneous zero normal or
zero rate by itself does not assert a zero hazard along the entire future arc;
the actual proof makes no such inference. A zero cap is sufficient and is
handled explicitly.

αη=1 is allowed whenever the six conditions hold: no denominator 1−αη, strict
step-size endpoint or positive-dimensional argument occurs. η=0 is correctly
excluded by the original hη. e=0 is included throughout, with first-hit equality
and τ(0)=0. Arbitrary plateaus, finite total integrated hazard and unbounded
waiting times are admitted. Nothing in this theorem proves recursive jump
construction, independent exponential draws, nonexplosion or invariance.

## Independent compiler, axioms, negative evidence and limits

Fresh direct elaboration used the actual fixed Lean 4.33.0 executable with the
original Lake-selected search roots, writing the new olean only to this owned
directory. The exact whole module was elaborated by foreground Lean PID 18716,
terminal EXIT0. A second direct source run of the exact module plus only
#print axioms for the public declaration ran as PID 21324, EXIT0, and reported
exactly propext, Classical.choice and Quot.sound. Neither run is a Lake build
cache replay; existing parent/import oleans are normal fixed search-root
dependencies, not a substitute for elaborating this module's proof bodies.
The executable and full search roots, driver, stdout, stderr, output olean and
closed terminal receipts are pinned in fresh-compiler.json.

The literal/fake-closure audit ran as PID 37128, EXIT0. It found zero forbidden
closures after stripping Lean comments and strings, one public theorem, one
genuinely proved private helper, one private specification, exact sealed public
and private signatures, and no use of WellFoundedLT or the inappropriate
discrete-time hit-membership shortcuts. There were no failed probes in this
bounded body-review run. The earlier header-only expMeasure1 failure is an
already resolved historical preproof issue, not a failure of this exact module;
this capsule does not copy or alter that CLOSED history.

Fourteen finite source/contract/runtime-configuration inputs have exact RAW
snapshots. Only CRLF byte pairs are replaced for LF pins; all other bytes remain
significant. The frozen candidate is byte-identical to the canonical source.
The fixed parent commit, toolchain, manifest, actual73/74 parents, sealed v2
header/expansion and four directly relevant Mathlib source files are bound.
No primary paper source, decoder verdict or independent final source-review
decision was read. The combined header adoption was checked only as an opaque
freeze pin. No optional mutable lesson/publication metadata is bound as if it
were part of the immutable mathematical candidate.

The introductory module comment at lines 8–9 still says prospective statement
only and no theorem proof. It is stale historical documentation retained in the
sealed bytes. Record that as a documentation debt, separately from the correct
compiled mathematics; do not mutate the frozen candidate as part of this review.

Final decision: all ten groups are mathematically correct under exactly the
retained original six conditions; minimum mathematical repair is empty. This
review supplies bounded independent mathematics and fresh Lean evidence only.
