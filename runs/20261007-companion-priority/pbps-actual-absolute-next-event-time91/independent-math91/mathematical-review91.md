# Independent whole mathematical review 91

Reviewer: `/root/independent_math91`; proving-worker role: none. Scope: the single public declaration `AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_law` and its enclosing private literal proposition. Production RAW SHA-256: `8e28fb218233358a9b1c7a2b41689071ca3c410faa58a0883a0885243d588ab2`. Checked base HEAD: `204fd4eee61724db77963cb33ddaddbcd90b906d`. This review is not the blinded decoder, anti-anchored primary-source review, aggregate gate, science-commit verification, or a VERIFIED transition.

## Statement and binders

The complete 35-let proposition at production lines 17–129 is byte-normalized textually identical to `expanded_literal_Prop` in the pre-proof seal. The public theorem at lines 133 onward takes precisely the sealed carrier/type structures, V, alpha, beta, eta, and six analytic assumptions, then returns that proposition. The body begins by changing to the full literal proposition, so its use of a private name does not conceal a provider premise.

- TYPING: finite-dimensional real inner-product space E, its Borel measurable structure, potential V, NNReal alpha/beta and real eta. Finite-dimensionality does not impose positive rank.
- STANDING: hAlpha: positive alpha; hAlphaBeta: alpha <= beta; hV: global C2; hH: two-sided Hessian quadratic bounds at every x,v; hEta: positive eta; hBetaEta: beta*eta <= 1. hH is a conjunction of lower and upper source bounds, not a hidden implementation bundle.
- TYPING / observer domain: all y,xRef,z0 and deterministic n; all fixed measurable b: Hist -> NNReal; all jointly measurable G/F with values in ENNReal; every measurable old-history event A. These quantify the output family. No common bound on b, integrability, positive mass of A, finite waiting time, or clock independence is an assumption.
- EXCESS: none. Probability normalization is produced internally from the existing concrete exponential-product theorem.

All 35 definitions were read: c, Phi, S, rate, Lambda, tau, next, record, P, epsilon, history, waitObs, timeObs, density, Rec, Hist, HistNext, last, lastNext, H, Hnext, readTime, a, U, appendRel, appendAbs, liftAbs, d, mu, D, Brel, B, X, Y, nu. P is the actual infinite product of real Exp(1) laws, epsilon is coordinatewise toNNReal, and H/Hnext are the literal stopped recursion. U reads the next actual record's time. No independent U or history provider is supplied.

## Proof audit

1. Lines 249–294 reuse the complete-history extension90 to obtain next-history measurability, measurable total relative append and all old coordinates. H is the literal prefix of Hnext. Sum elimination supplies measurable readTime; composition gives a,U,appendAbs,liftAbs. Prefix preservation applies to every abstract history and real coordinate.
2. Lines 295–360 construct d(h)=max(b(h)-a(h),0), measurable D and Drel. The cutoff equivalence `a < a+s < b iff 0 < s < max(b-a,0)` is valid without b>a: positivity of s rules out the nonpositive max branch. Hence D(h,a+s)=Drel(h,s) for every h,s. Every-history density89 fiber bounds transfer by real Lebesgue translation. Nothing restricts this assertion to realizable histories or a.e. histories.
3. Lines 361–430 use the actual recursive next record. Stopped records remain stopped; their relative wait is zero and the live-event predicate is false. A live infinite wait produces a stopped successor and cannot be below finite d. A live finite wait v produces the exact successor `(T+v,S(Phi_v z))`; strict positivity excludes v=0. These cases prove Brel=B pointwise, the actual clock identity on B, and the whole-history absolute append identity there. Replacing U globally by a+timeObs would be false on a stopped successor, but the proof makes no such replacement outside B.
4. Lines 431–483 derive arbitrary G tests from90 by `Grel(hnext,s)=G(prefix(hnext),a(prefix(hnext))+s)`. The total prefix of appendRel is the old history, and the actual Hnext prefix is H definitionally. For each fixed h, translation by a(h) preserves real Lebesgue measure. The composition is jointly measurable. The per-h integral equality and parameter-integral measurability suffice; no separately packaged global shear theorem is needed. ENNReal integration allows infinite tests without an integrability premise.
5. Lines 484–514 obtain IsProbabilityMeasure P via `UnitExponentialProduct.unit_exponential_product_laws.1`, then for mu by measurable pushforward. Measure extensionality against all measurable ENNReal tests, the G identity with A=univ, Tonelli for mu product Lebesgue, and withDensity identify the actual restricted X law with nu. Guarded actual append identifies Y and Hnext pushforwards. The mass bound is the probability of B, not a renormalized conditional distribution.
6. Lines 515–527 obtain all F tests by composing F with liftAbs and using guarded equality Y=liftAbs(X). Every measurable A is allowed, including null A. There is no division by mu(A), conditional representative, or positivity assumption.

## Boundary and counterexample probes

- b(h)<=a(h), including b=0: D(h,u)=0 for all u and the positive relative interval is empty. The cutoff equivalence remains true.
- Stopped last record: density is zero on the entire fiber, append stays stopped, and actual B is false. readTime=0 is an auxiliary totalization.
- Live top wait: actual next record is stopped, U=0; the finite-event guard excludes it. No atom at top is silently removed from a claimed full probability law.
- Zero wait: current and next records can be live with equal absolute times; strict a<U excludes them. The proof does not require or infer a no-atom lemma.
- Rank zero or a vanishing bounce direction: no nonzero-dimensional or denominator-nonzero assumption appears. Lean's total division yields the defined reflection, and the rate is zero. A positive exponential threshold never hits a zero hazard; raw nonpositive thresholds can give a zero wait, which is excluded. The restricted law can legitimately have zero mass.
- Abstract histories need not be realizable, ordered, or start at zero: every-history fiber statements depend only on the last tagged record and the chosen cutoff. Prefix preservation is literal Fin.snoc. Actual-law claims alone use the pushforward mu.
- n=0: Hist still has its initial record and oldPrefix is defined on Fin 1. No empty-history special case or predecessor index is used.
- Infinite ENNReal tests, including top on zero-density regions: ENNReal multiplication/integration semantics and Tonelli are the correct nonnegative conventions; no signed cancellation or infinity subtraction is used.
- Null old-history events: unnormalized restricted integrals remain meaningful and vanish with the restriction; no conditional version is selected.
- Negative auxiliary absolute/relative coordinates: appendAbs is a measurable total map using raw negative flow and clipped NNReal time increment. Physical identification is only asserted on B, where u-a>0.

No counterexample or missing binder was found. The mathematical result accepted here is only the strict finite next absolute-time coordinate law. Ordered iteration, final-survival multiplication, endpoint conversion, event-count/path identification, full A.7, physical-time restart, invariance and whole-paper completion remain outside this theorem.

## Source topology versus implementation

Read the accepted successor source graph and pre-proof authorization. The chosen route is existing complete-history90 plus internally derived coordinate translation, with direct density89 for Borel/fiber facts. The canonical exponential-product normalization is a genuine direct implementation dependency. It supplies no new source premise and does not make survival88, no-atom conversion, memorylessness, or nonaccumulation an additional AND parent for this bounded theorem. The current review did not independently reconstruct the primary-source topology and does not claim to replace the distinct source-review lane.

## Evidence

`statement-scan.native.json` records exact seal equality and absence of fake-closure syntax. `input-hashes.native.json` pins native inputs. `FreshWholeSourceKernelClosure91.lean` consists of the exact production bytes followed by kernel inspection commands, without altered production proof. `kernel.receipt.native.json`, `kernel.stdout.log` and `kernel.stderr.log` record the fresh terminal run, axiom report, direct/transitive ASTIS constants and full private-proposition expansion. Final acceptance and exact dependency findings are recorded in `decision91.native.json` after checking that run.

## Final kernel and exposition outcome

The fresh exact-production-source kernel probe succeeded with terminal exit 0 in 17.922 seconds. Axioms: propext, Classical.choice, Quot.sound only. The kernel walk found exactly three direct public ASTIS parents (history90, density89, exponential product), 15 reachable owned compiler constants and 106 transitive ASTIS constants; none lacked a value. The private proposition expansion includes the full final G/F and measurable A quantifiers. The failed first inspection used unsupported `pp.maxDepth`; this was solely an inspection-suffix error, retained under `attempt1-unsupported-pretty-option/`, and corrected with `pp.deepTerms true`. No mathematical retry or production edit occurred.

At the coordinator's request I also reviewed the complete authored statement, formulas and seven explanatory steps in the declaration lesson and publication item. They faithfully explain the mathematical theorem and its auxiliary totalizations. All seven adjacent Lean excerpts have exact raw hashes and exhaustively partition body lines 142–527. The one requested metadata correction, `Measurable.lintegral_prod_right` to `Measurable.lintegral_prod_right'`, is present in the final lesson. Both append and clock identities are guarded in the surrounding text; the formula's comma is understood inside the implication, with no new unguarded mathematical claim. Final exposition hashes are in `exposition-final.native.json`. Visual rendering and independent primary-source fidelity are outside this review.

Decision: ACCEPT for the exact local mathematical theorem, whole proof, axiom cleanliness, actual dependencies and mathematical exposition at the recorded hashes. This is not a VERIFIED transition and is not a claim that source, aggregate, science-commit, publication or purification admission is complete.
