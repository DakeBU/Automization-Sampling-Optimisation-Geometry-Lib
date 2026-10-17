# Actual averaged half-turn: calculation and local Lean proof

The exact production module and focused test compiled locally (3251 jobs,
standard three axioms only). Independent mathematical/direct-compiler proof
checking passed; see actual-half-turn-reversibility-independent-proof-check.json.
The post-proof source-blind roundtrip and source/exposition admission passed:
ASTIS-RT-20261017-PBPSActualHalfTurnReversibility, equivalent-after-elaboration
in all seven slots. The independent reviewer published VERIFIED after explicit
human authorization; see actual-half-turn-reversibility-independent-verification.json.
Canonical aggregate integration, browser acceptance and purification are separate.
The exact statement passed source-first prereview before implementation; digest
`45ea5cc6ba2706069de8d6ad70a03a686de81e5aaaf9e1cc4b373a5fa2af4dd2`.
Local compilation alone did not justify VERIFIED and no full paper is counted.

Fix y. Write q=q_y, gamma=stdGaussian(E), P=Exp(1)^N and
nu=q product gamma. All factors are probability measures, supplied internally
by the existing conditional-Gibbs/actual-process producers, not theorem inputs.
Let H be the SAME existing returned-position kernel. For measurable A,B put
F(x,p)=1_A(x), G(x,p)=1_B(x).

## 1. Identify the literal process and laws

The two existential process witnesses satisfy identical raw covered-arc and
fallback prescriptions. Prove equality pointwise by the covered/uncovered
split; do not merely identify their laws informally. Rewrite the exact H fiber
using that process. Identify q with volume.tilted(-V_y), so the phase law in
the fixed-reference duality is exactly nu, not only a proportional density.

## 2. Discharge finite-measure integration first

F,G are measurable and bounded by1. Joint raw Z measurability makes

\[
 (x,r,p,w)\longmapsto
  1_A(x)1_B\bigl(\operatorname{fst}Z(y,r,(x,p),\pi,w)\bigr)
\]

measurable and bounded by1 on q product q product gamma product P.
Its absolute integral is at most1. The reused Borel-expectation parent also
supplies bounded clock integrability and measurable expectations. Derive these
facts before signed Fubini; do not rely on totalized-integral notation alone.
There is no integration over y and no unbounded reference-energy moment here.

## 3. Use fixed-reference bounded phase duality

For every fixed r, put T=T_pi^(y,r). The actual phase duality gives

\[
 \int F\,TG\,d\nu
 =\int (RG)\,T(RF)\,d\nu
 =\int G\,TF\,d\nu,
\]

because the momentum flip R leaves both position tests unchanged.
The source bounded-test identity is A.1 lines819--820. This avoids requiring
a semigroup or an unproved all-L2 averaged operator as a premise. The source
operator route via self-adjoint Gaussian compression remains separately
recorded in the Source Proof Graph.

## 4. Average an independent reference

Fubini identifies the finite real flux associated to H with

\[
 \int q(dr)\int\nu(d(x,p))\,
  1_A(x)\int P(dw)\,
  1_B\bigl(\operatorname{fst}Z(y,r,(x,p),\pi,w)\bigr).
\]

The reference law q(dr) does not depend on x; this is essential. Integrate
the fixed-r identity from Step3. The resulting expression is unchanged when
A and B are exchanged. No common clock-null event for all parameters is used.

## 5. Return to Mathlib's exact reversibility predicate

All fluxes are nonnegative and at most1. Justify the real-indicator versus
ENNReal set-lintegral conversion using finite probability mass. Conclude

\[
 \int_A^- H(y,x)(B)\,q(dx)
 =\int_B^- H(y,x)(A)\,q(dx).
\]

These are all measurable rectangles, not singleton masses; the local
countable-only singleton-balance lemma is inapplicable. The result is
`Kernel.IsReversible` for x -> H(y,x). Its existing Markov-kernel implication
then gives invariance without inventing another ASTIS wrapper.

Remaining outside this packet: restart/Chapman--Kolmogorov/semigroup,
augmented-space all-L2 realization, hypocoercive rate, capped implementation,
actual-input expected cost, global warm start, composition and complete papers.

## Reading the Lean proof

The public declaration is `ActualHalfTurnReversibility.actual_half_turn_reversible`
in `AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHalfTurnReversibility.lean`.
It has exactly the sealed six analytic binders and retains all raw-path,
joint-kernel, local-initialization and half-turn outputs from its kernel parent.

- `flux_ofReal` uses Mathlib's indicator integral and finite kernel masses to
  identify a real pairing with the ENNReal rectangle flux. It is private, not
  a separately counted mathematical leaf.
- `reversible_of_bounded_pairing` tests only measurable indicators. This works
  on atomless spaces and does not use a countable-state singleton shortcut.
- `pairing_eq_reference_average` first derives the measurable clock expectation
  and its absolute bound1. Bounded products are integrable under the probability
  factors. Only then does signed Fubini swap the input and independent reference.
- `reversible_of_reference_average` integrates the fixed-reference symmetric
  pairing and invokes the preceding exact rectangle criterion.
- The public proof identifies `Zb=Z` pointwise by covered/fallback cases. A dead
  record cannot bracket a finite time, since top cannot be below that time.
  The existing reference kernel supplies probability of q_y. Position lifts of
  f,g remove both momentum flips from the actual signed phase duality. Finally,
  `hqeq` identifies the two literally written Gibbs potentials by real algebra.

The generic private helpers have explicit finite/probability-law hypotheses;
the public theorem supplies them internally from its existing actual producers.
They are not new assumptions on the paper. The focused import/axiom test is
`Tests/ProximalBPSActualHalfTurnReversibility.lean`; it is not a mathematical
consumer. The future actual augmented half-turn operator is the planned paper
consumer, not an invented existing Lean dependency. Registry565 currently
excludes this new candidate; independent source fidelity and integration remain.
