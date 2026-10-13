# Lean-Asymptotic-Statistical-Theory

- Public repo: https://github.com/junwei-lu/Lean-Asymptotic-Statistical-Theory
- Local checkout: `/home/nitanda_sub/mark/repos/outer_repos/sampling_theory_sde/Lean-Asymptotic-Statistical-Theory`
- Related paper: `Hypothesis-Disciplined Multi-Agent Automated Formalization of Asymptotic Statistical Theory`, https://arxiv.org/abs/2606.20642
- Local paper: `/home/nitanda_sub/mark/repos/outer_papers/sampling_theory_sde/Hypothesis-Disciplined-Asymptotic-Statistical-Theory/2606.20642.pdf`
- Toolchain observed in repo: Lean 4.29.1 / Mathlib 4.29.1.
- Observed local commit: `8e7f22c88cc3280e898005b6445d94c581dd8b4d`
  (`2026-06-09 15:57:20 -0400`).
- Role: external reference project and process model.  It is not an ASTIS Lake
  dependency and none of its theorems are callable until ported or reproved
  locally.

## Useful Code For Log-Concave Sampling

The repository contains a broad `AsymptoticStatistics/ForMathlib` layer.  The
following files are especially relevant to log-concave sampling
infrastructure:

- `AsymptoticStatistics/ForMathlib/PrekopaLeindler.lean` for
  Prekopa-Leindler and Brunn-Minkowski style convex-measure infrastructure.
- `AsymptoticStatistics/ForMathlib/Brunn1D.lean` for the one-dimensional
  Brunn-Minkowski boundary used by the Prekopa-Leindler development.
- `AsymptoticStatistics/ForMathlib/GaussianMGF.lean`,
  `PiGaussian.lean`, `PiWithDensity.lean`, `GaussianRealTV.lean`, and
  `GaussianShift.lean` for Gaussian density, product Gaussian, MGF, and
  finite-dimensional change-of-measure patterns.
- `AsymptoticStatistics/ForMathlib/RnDerivSqrt.lean`,
  `HellingerProduct.lean`, and `L2.lean` for RN derivative, square-root
  density, Hellinger, and L2-style proof patterns.
- `AsymptoticStatistics/ForMathlib/Contiguity.lean`,
  `Prohorov.lean`, `PortmanteauLscBridge.lean`, and weak-convergence files for
  probability-limit infrastructure.
- `AsymptoticStatistics/ForMathlib/MeasurableSelection*.lean`,
  `MarkovKernelProhorov.lean`, and kernel files for measurable-selection,
  tightness, and Markov-kernel proof style.

The first audit of these log-concave-sampling-relevant `ForMathlib` files found no `sorry`,
`axiom`, or `unsafe` hits in the selected port candidates.  ASTIS should still
reprove or port only the minimal Mathlib-ready leaves needed by the log-concave sampling tree.

## Process Lessons To Reuse

The associated paper proposes a hypothesis-disciplined multi-agent pipeline.
ASTIS should reuse the discipline, not the exact domain:

- every theorem hypothesis must be source-anchored, a Lean encoding adapter,
  source-implied, or explicitly rejected;
- concept-layer fields must not drift from the informal theorem;
- dependency graphs and side-by-side informal/Lean statements are useful
  review artifacts for long proof runs;
- "hypothesis laundering" is a failure mode: do not close a proof by adding
  assumptions that the source does not justify.

For `ASTIS-CHEWI-001`, this reference should guide the audit protocol for
textbook chapter extraction and Mathlib-ready leaf acceptance.
