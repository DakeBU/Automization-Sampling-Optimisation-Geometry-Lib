# Independent source-only review v1 — Exercise 6 lower comparison

**Verdict: ACCEPT the v1 sealed signature and the lower source topology with the explicit §1.2 source-ingredient annotation below.** This approves a pre-proof boundary, not a Lean proof or a completion claim for the exercise. No implementation or prior review verdict was consulted.

## Exact reviewed inputs

| Repository-relative input | SHA-256 |
| --- | --- |
| `.astis/sog-bench/tmp/pdfs/statot-intake-20261104/st_flour.pdf` | `639ff16e79f4a32ade9c0595b0ed1d95490eb7e402949168895b6a6194a9c02f` |
| `proof-obligations/statot-exercise-1-6/lower-comparison-seal-v1.md` | `fc7be88bd6b01aa7d99c5556e77e9c9f5afd7243a01249996c67c9143ab092a8` |
| `proof-obligations/statot-exercise-1-6/lower-comparison-signature-v1.lean.txt` | `46ce27b0d04f03374c59559d3f68d1a6fad73c296233c87cf8ef4f4cea3f29c0` |

Anchors in Chewi, Niles-Weed and Rigollet, *Statistical Optimal Transport*, pinned 290-page PDF, July 2024 preface: [§1.8 Exercise 6, printed p. 44 / PDF p. 50](https://chewisinho.github.io/st_flour.pdf#page=50); [§1.2, printed pp. 15–17 / PDF pp. 21–23](https://chewisinho.github.io/st_flour.pdf#page=21); [§1.1 (KOT), printed p. 11 / PDF p. 17](https://chewisinho.github.io/st_flour.pdf#page=17).

## Statement and binder check

The lower hint explicitly gives both inequalities in this order: `E_μ f − E_ν f ≤ W₁(μ,ν) ≤ W₂(μ,ν)` for every real 1-Lipschitz `f`. The signature gives their conjunction, with the same sign and orientation. The exercise prints these for its previously specified laws; the seal factors out the law-independent comparison on the standing Wasserstein domain. It does not recharacterize the two-mixture exercise as a theorem about arbitrary laws.

| Lean binder or choice | Classification and source justification |
| --- | --- |
| `μ ν : Measure ℝ`, `f : ℝ → ℝ` | `TYPING`: standard Borel real carrier and real tests; §1.1 formulates the marginal conditions on Borel sets, and Exercise 6 works on `ℝ`. |
| `[IsProbabilityMeasure μ]`, `[IsProbabilityMeasure ν]` | `STANDING`: §1.2 defines `P_p` as a class of probability measures; mass one is not an added transport estimate. |
| `MemLp (id : ℝ → ℝ) 2 μ`, likewise for `ν` | `STANDING`: §1.2 places `W₂` on `P₂`. For the measurable identity on `ℝ` this is precisely finite second moment, and on probability measures it also gives finite first moment for the `W₁` domain. The concrete Gaussian mixtures must be shown to satisfy it at the consumer. |
| `LipschitzWith 1 f` | `SOURCE`: the printed 1-Lipschitz test condition; no sign, boundedness or extra test-integrability hypothesis. |

No `EXCESS` binder was found. Test integrability is a derived obligation: `f` is continuous and `|f(x)| ≤ |f(0)| + |x|`. The local `W₁` is a defined cost, not an extra binder. The literal real-line transport cost is `|x−y|` (power one, no square or factor); §1.1 (KOT) and §1.2 give its coupling infimum and the quadratic Wasserstein value, respectively. The square root of the infimum of quadratic costs represents the same value as the infimum of their square roots by monotonicity and continuity. The source first uses an infimum and then records attainment in Definition 1.2; attainment need not be an input or a proof route for this comparison.

For real `a = E_μ f − E_ν f` and nonnegative finite `b = W₁(μ,ν)`, `ofReal a ≤ ofReal b` is equivalent to `a ≤ b`: if `a < 0`, both are automatic, and otherwise the embedding preserves and reflects the order. Thus clipping the *signed difference after subtraction* does not strengthen it to an absolute difference, change its orientation, or require nonnegativity of `a`. The standing domain supplies the finiteness relevant to the source interpretation.

## Source coverage and use sites

- **NODE L — Exercise 6 lower hint.** Uses the §1.1 coupling/cost setup and §1.2 `P₁`, `P₂`, `W₁`, `W₂` definitions, specialized to the real line. It asks to prove and use the two comparisons. The relevant lower infimum needs the inequality for every feasible coupling (or another justified infimum-lower-bound route), not a bound at a single feasible plan.
- **Existing source ingredient at L — §1.2, printed p. 17 / PDF p. 23, immediately after Example 1.4.** The text already states `W_p ≤ W_q` for `p ≤ q`, citing the ordering of `Lᵖ` norms. Its `p = 1, q = 2` specialization feeds the *second* inequality at L on the `P₂` domain. The exercise hint itself supplies no detailed proof. Record this preceding source claim and mechanism explicitly: the second comparison is not wholly absent from the source. This is a source edge, not a supplied premise or a claim about a compiled dependency.
- **SOURCE_GAP L1 — proof of L.** The hint leaves test integrability and the expectation-to-linear-infimum comparison to the reader; it does not spell out the probability-`Lᵖ` and infimum reasoning for the second comparison. These are proof obligations of the sealed generic declaration, not its hypotheses. No need to use an optimal plan, prove the reverse dual inequality, or compute an exact distance.
- **SOURCE_GAP L2 — lower consumer after L.** The exercise says to use L but does not supply the test or its evaluation. With the displayed weights and Gaussian means, `E_μ x = 0` and `E_ν x = m/2`, so `f(x) = −x` gives the required signed difference `m/2`. Discharge Lipschitzness, probability, and finite-second-moment membership for these literal laws in the concrete consumer; do not put the mixture parameter, laws, moment facts or test evaluation into L1.
- **NODE U / SOURCE_GAP U1 — separate upper branch.** The hint calls for a feasible coupling of the literal laws; its construction and cost feed the upper bound. U1 is not a dependency of L1. **NODE T — final exercise target:** combine the lower consequence from L and L2 with the upper bound from U/U1 to obtain `W₂(μ,ν) ≍ m` for `m > 0`. Neither L nor L1 alone discharges T.
- **EXCLUDED:** Exercises 5, 7 and 8 are separate. The introductory comment about the difficulty of an optimal map motivates the bounds; it imposes no existence, attainment, optimal-map, uniqueness or duality subgoal. Other §1.2 results are not required merely because they neighbor the definitions or monotonicity observation.

This review adds the explicit §1.2 use-site annotation without altering either sealed input. Elaboration, actual dependencies, concrete consumer proofs and full-exercise closure remain outside this verdict.
