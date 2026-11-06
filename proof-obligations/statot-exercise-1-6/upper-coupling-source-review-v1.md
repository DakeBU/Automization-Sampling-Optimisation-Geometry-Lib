# Independent source-topology pre-proof review — Exercise 6 upper witness v1

**Verdict: PASS for the bounded upper-coupling witness (U1) only.** This is a source-to-statement review, not proof verification or approval of a theorem for the full exercise.

## Inputs reviewed

| Repository-relative input | SHA-256 |
| --- | --- |
| `proof-obligations/statot-exercise-1-6/upper-coupling-seal-v1.md` | `bfa5e5cc97911ebd95779f81a258785e23093f8946093448399471780870262b` |
| `proof-obligations/statot-exercise-1-6/upper-coupling-signature-v1.lean.txt` | `811e6db71ea8758d9d06f4e8115a9135cbfcf1248209618a3e76ee2f23895ca3` |
| `.astis/sog-bench/tmp/pdfs/statot-intake-20261104/st_flour.pdf` | `639ff16e79f4a32ade9c0595b0ed1d95490eb7e402949168895b6a6194a9c02f` |

The pinned page was inspected visually (Chapter 1, §1.8, Exercise 6; PDF page 50, printed page 44). Review used the sealed proposition and its elaborated signature; no Lean implementation, proof, or broader transcript was consulted. The interpretations of the imported predicates and cost are those recorded in the seal; their definitions were not independently unfolded in this review.

## Alignment and boundary

- The source has `m > 0`, with real Gaussian laws `N(-m, 1)` and `N(+m, 1)`. The means, unit component variances, and ordered weights agree: `μ` has `(1/2, 1/2)` and `ν` has `(1/4, 3/4)` at the negative and positive means, respectively. The signature uses actual Gaussian measures with those fixed weights and a plan on `ℝ × ℝ`, in source order (`μ` first, `ν` second). The source does not assert unit variance for the mixtures themselves.
- `∀ m : ℝ` extends only the witness domain. Restricting to the printed `m > 0` recovers the relevant source domain; at zero the two laws coincide and zero cost is consistent, and negative `m` reverses the signs of the component means without changing the squared displacement scale. No positivity, integrability, optimality, supplied coupling, or supplied law is a binder assumption. The signature claims both feasibility and the exact finite cost of that witness, in the form of a nonnegative integral equal to `ENNReal.ofReal (m ^ 2)`.
- The page asks for `W₂(μ, ν) ≍ m`. It asks for an exhibited coupling for the upper bound, but supplies neither a coupling nor its cost. The exact witness cost `m²` is the bounded target selected for U1, not an equality printed in the source or an assertion that `W₂² = m²`. Via the infimum over feasible plans, U1 can feed the upper comparison (`W₂ ≤ m` on the source domain); the upper comparison is not itself in the signature and does not require a minimizing plan.
- The lower hint is separately quantified over every real 1-Lipschitz `f : ℝ → ℝ`, with the printed sign `E_μ f − E_ν f ≤ W₁(μ, ν) ≤ W₂(μ, ν)`. The hint asks that comparison be proved and used. The test selection, expectation/integrability justifications, general comparison, and resulting lower bound are outside the witness. A single feasible plan cannot replace the all-coupling/infimum argument in that branch.

## Coverage and direction

The source graph has the correct direction: S0 supplies the laws to U1 and L1; U1 supplies the plan and cost to U, while L1 supplies the separate justification needed by L; U and L together support T. The seal covers U1 only. Neither the lower branch nor the final two-sided comparison is discharged by the seal, and no source edge licenses an implementation-level dependency. The preceding centering/optimality questions and Exercises 5 and 7 are separate, with no stated dependency from Exercise 6; the following Exercise 8 is likewise separate. No source-attribution error, missing prerequisite assumption in the bounded interface, or reversed edge was found.
