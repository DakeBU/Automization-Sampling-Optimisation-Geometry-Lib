# Statement seal v1 — Statistical Optimal Transport Exercise 6, lower comparison

Source: Sinho Chewi, Jonathan Niles-Weed and Philippe Rigollet,
*Statistical Optimal Transport*, 290-page public PDF, July 2024 preface.
[Chapter 1 §1.8 Exercise 6, printed p. 44 / PDF p. 50](https://chewisinho.github.io/st_flour.pdf#page=50).
PDF SHA-256: `639ff16e79f4a32ade9c0595b0ed1d95490eb7e402949168895b6a6194a9c02f`.
This is an attributed mathematical restatement, not copied source prose.

## Exact interface

[Elaboration probe](lower-comparison-signature-v1.lean.txt)
for `AutoSamplingTheory.TechnicalLemmas.Measure.WassersteinLipschitzLower.expectation_sub_le_linearCost_and_le_wassersteinDistance` on the repository's pinned Lean.
For Borel probability measures μ, ν on ℝ with finite second moment, and
every real 1-Lipschitz f, compare the expectation difference to the
infimum of linear costs, and that infimum to the canonical quadratic
Wasserstein distance. The real difference is embedded by `ENNReal.ofReal`
which clips negative differences to zero. Since the distances are
nonnegative, this has exactly the source's one-sided order semantics.
No supplied integrability of f, plan, optimizer, coupling estimate,
duality theorem or sign restriction on the difference.

- μ, ν and f: source objects for the comparison in the lower hint.
- Probability and Borel carrier: standing conventions of §1.2.
- `MemLp id 2`: finite second moment, the domain where the source's W₂ is
  a finite Wasserstein distance. Both literal exercise mixtures belong to
  this class; verify it in the consumer, not by adding a source premise.
- `LipschitzWith 1`: the printed test-function condition.
- W₁ is the existing Kantorovich infimum evaluated at the literal cost
  `|x-y|`; W₂ is the existing square root of the quadratic infimum.
  These are not supplied unknown quantities.

## Source-only coverage

- **NODE L**: lower hint requires proving the expectation-to-W₁ inequality
  and W₁-to-W₂ comparison for arbitrary real 1-Lipschitz tests.
- **SOURCE_GAP L1**: the lower hint does not give the proof of the test
  integrability or the two comparisons. This is the sealed theorem's scope.
- **SOURCE_GAP L2**: choose and evaluate a test on the two actual mixtures.
  A focused consumer should use the negative identity and derive the needed
  Gaussian moment/mean facts. This is separate from the generic conclusion.
- **NODE U** and **SOURCE_GAP U1**: feasible-plan upper hint and concrete
  witness; handled by the separate upper packet, not supplied to L1.
- **NODE T**: two-sided comparison. L1 supplies L, L and the law-specific
  calculation L2 give the lower estimate, which together with U feeds T.
- **EXCLUDED**: the adjacent Exercises 5, 7 and 8 are separate. The source
  does not require exact distance, optimizer existence, or the converse
  Kantorovich–Rubinstein duality inequality for this exercise.

No source edge is a compiled Lean dependency, and a bound for one feasible
plan does not by itself prove an infimum lower bound.
