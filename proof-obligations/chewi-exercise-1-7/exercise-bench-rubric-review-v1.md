# Exercise 1.7: independent Bench draft scoring review

**Disposition:** Accept the mathematical prompt/target alignment of both
drafts. Request scoring and prompt-package revisions before using either for
assessment, and revise the proposed natural-language KL level. This is a
bounded review of six local inputs, not a source audit, a blind formal
decoding, a Lean compile/replay, a model run or Bench admission.

## Exact inputs

SHA-256 over the raw bytes (no newline normalization):

| Input | SHA-256 |
| --- | --- |
| compact-pi-bench-draft-v1.md | bdc393c7e50fefbd158e8c51d99bd4149af4e7d39ea4f392f7909cfe99735110 |
| actual-kl-bench-draft-v1.md | f7e827dbcb92968b7048411f8c2e87dce7d3837350296b874f36c887b3327d67 |
| compact-pi-statement-v1.lean.txt | 43766c48f2ff7a0ffdd2e8005994d65246766329cef913be80a22ef4ce072714 |
| actual-kl-statement-v1.lean.txt | 21bee5da0f009cb6bcd1c0585ba1a32ddb4739113aa45cf96179d9a467119bfa |
| compact-pi-candidate-v1.md | f6006e2da730714ee0f43883bdf1d3356d97f7deafaccf60c7da7757438780cf |
| actual-kl-candidate-v1.md | 2e0820311771445362d82ab751ef01708009f30be9238667ca56c6e690b0bb50 |

## Compact PI

**Alignment accepted.** The real finite-dimensional Hilbert/Borel
probability setting matches the typed context (completeness is automatic
in finite dimension). Both inputs restrict the LSI and the output test to
smooth compactly supported functions, use the same entropy including at
zero and keep the same real constant C. Do not add a sign condition on C:
division is by the positive squared parameter, and taking limits on the
right commutes with multiplication by fixed 2C. The variance/energy
inequality and the three explicit integrability requests match the stated
variance/energy and admissibility conclusion. The NL prompt also prescribes
the square-root route; the Lean type certifies the conclusion and not a
proof method, a cutoff sequence or equality of optimal constants.

**Reference route accepted; make the domain evidence usable in grading.**
Bounded compact f is integrable; g = f − ∫ f is bounded, centered, and
has the same gradient as f. The gradient vanishes off the original
support and is continuous, so its squared norm is integrable. For small
parameters, p = 1 + εg lies in [1/2, 3/2], has integral one, and u = √p
has gradient ε∇g/(2√p). The inspected reference points to a separate
cutoff argument rather than spelling it out. A self-contained grader key
can record the following check: for a smooth cutoff χ_R equal to one
on the radius-R ball, supported on the radius-2R ball, with values in
[0,1] and gradient bounded by K/R, test LSI on χ_R u. Boundedness and
continuity of t log t on [0,3/2], including zero, give convergence of
the entropy integral and of the mass; the normalization term converges
by continuity. The gradient difference is (χ_R − 1)∇u + u∇χ_R;
the first term tends to zero in L² by domination, the second by the
K/R bound and bounded u on a probability space. Thus the actual LSI
test is justified. The entropy quotient tends to ∫g²/2 with envelope g²;
the energy quotient tends to ∫‖∇f‖²/4 with envelope ‖∇f‖²/2.
The two factors give the claimed C, not 2C or C/2.

**Rubric needs revision (draft rows at lines 53–57).**

- Make all three integrability conclusions explicit scoring evidence;
  the current rows can award all ten points without an explicit argument
  that the original f is integrable. A single boundedness/continuity
  argument covering all three counts; do not require three repeated proofs.
- Score normalization, linear-term cancellation and the limit, not the
  use of the named compensated function. Direct Taylor expansion of
  p log p and cancellation of ε∫g, or an equivalent integrated
  uniform remainder, earns the same credit. Likewise derivative support
  is a sufficient route to the requisite gradient bound, not a required
  phrase or proof step if the bound is otherwise established.
- Do not mark a proof complete if it applies compact-test LSI to u with
  no domain argument, or if it uses a stronger LSI/PI hypothesis, even
  if all later algebra is correct. In a library-assisted profile an
  allowed extension theorem plus verification of its hypotheses is a
  valid domain argument; an unexplained appeal is not. A positive-sided
  limit suffices here, and there is no standalone actual-law KL requirement.

## Actual-law KL

**Alignment accepted.** A real a.e.-strongly-measurable f, its finite a.e.
bound, probability reference and centering match the binders. An
existential real bound in prose is equivalent for this conclusion to
supplying the Lean bound witness. The clipped density is precisely the
nonnegative density represented by ENNReal.ofReal. The conjunction
requires probability and extended-real KL < ⊤ on a full neighborhood of
zero, and the real little-o remainder is two-sided. This is neither
the bare compensated integral limit nor a one-sided theorem.

**Reference route accepted.** Work on the common full-measure set where
the bound holds and use a measurable representative for the density if
needed. For example, |ε| < 1/(2(1 + |M|)) gives p ∈ [1/2,3/2]
a.e. and also covers M = 0 without a separate case. Boundedness implies
integrability of f and f²; centering gives mass one and the local density
is p itself a.e. The RN formula with integrable p log p gives genuine
finite extended-real KL before interpreting its real value. The
reference's bounded Taylor-integrand argument yields the coefficient.
Equivalently the third derivative of t log t is bounded on [1/2,3/2],
so the integrated remainder is bounded by a constant times
|ε|³ ∫|f|³, after the linear term integrates to zero. Both proofs
give the signed-parameter limit, with ν₀ = μ and zero remainder there.

**Prompt/rubric need revision (draft lines 18–27, 43–53).**

- For the prompt-only package, state the canonical extended-real KL
  convention for probability laws (RN log integral when absolutely
  continuous, +∞ otherwise), and denote its real value explicitly in
  the expansion after local finiteness. This is a convention, not a
  solution hint about why the actual law has finite KL.
- Make density measurability up to a null set, absolute continuity with
  the stated density, and the integrability/finiteness bridge explicit
  evidence in the law and KL rows. Citing the ordinary RN formula is
  fine when its conditions are shown. A proof of a limit after real
  totalization, where ∞ can map to zero, cannot establish finiteness.
  Do not duplicate the same Taylor evidence in the finiteness and limit
  criteria.
- Accept a uniform choice that implicitly handles M = 0 and a proof
  whose all-small-parameters formula already gives the zero endpoint;
  neither needs a separately headed case. Accept a positive-side argument
  applied also to −f when the negative side is explicitly recovered.
  A punctured quotient limit plus the zero remainder gives the full
  neighborhood statement; a value assigned to the quotient at zero
  does not establish any limit.

## Evaluation profiles, difficulty and isolation

- **Scoring format:** The ten-point lists are usable as draft checklists,
  not the Bench's four binary prose criteria. For an eventual Bench
  packet, one grouping is PI: integrability/centering/normalization,
  valid LSI domain, justified entropy limit, and energy limit/final
  inequality; KL: local law, finite KL identification, controlled
  quadratic coefficient, and two-sided remainder/endpoint. Define
  partial credit separately if the ten-point format is kept for local
  experiments. Missing an essential component precludes a complete
  answer. Lean scoring should be by an isolated fixed-target verifier,
  not by prose points, proof-text keywords or checking for the reference's
  exact calls.
- **Tools:** Accept the drafts' distinction between prompt-only prose,
  library assistance and fixed-target Lean. Before any run, record and
  enforce the actual tool policy: closed-book has no external retrieval;
  assisted prose uses pinned eligible retrieval material; Lean pins the
  compiler, allowed imports and transitive context and provides only
  declared search/compiler tools. Do not put the whole draft in the prompt:
  strip source/answer links, rubric, dependency hints, cross-task
  comparison and reviewer material. Exclude finished target modules and
  direct answer copies from answer-excluded profiles, including via
  transitive imports, file search and retrieval. Permit genuine alternative
  proofs with the declared tools. An answer-access/open-web experiment,
  if separately declared, is not comparable to an answer-excluded run.
  No restricted ATLAS material belongs in these contexts.
- **Provisional levels:** PI prose L4 is defensible for the stated
  prompt-only profile: adapting the compact test domain and joining two
  distinct controlled limits is real composition. PI Lean L4 is
  defensible only if the pinned helper signatures leave the actual
  centering/admissibility, domain and normalized limit joins to the solver;
  reassess if prepackaged. KL prose should be L3 rather than L4: mass
  and RN identification are short consequences of one a.e. bound, then
  a single uniform scalar Taylor estimate suffices on the same interval.
  KL Lean L3 is plausible with the stated law and limit producers if the
  extended-real/real and neighborhood bridges remain; lower or remove the
  reconstruction claim if only a final wrapper call remains. Assess
  assisted profiles separately. None of these is empirical calibration.
- **Family and graph:** Accept the proposed common family
  chewi-lcs-2026-08-20-exercise-1-7. Keep both distinct results, their
  prose/Lean/graph views and near-answer derivatives in the same public-dev
  exposure group if released; no sibling becomes an unseen private
  evaluation sample. A general reusable lemma need not be an exercise
  duplicate, but a permitted lookup must not disclose an answer contrary
  to the profile. For any later graph task, require a separately replayed
  source-bound induced proof-body slice and exact structural answer;
  a supplied direct shared-parent lookup is L1-like, not a mathematical
  L4 proof. Neither absence nor presence in the slice proves logical
  independence or necessity. No graph edge or source attribution was
  independently certified in this review.
