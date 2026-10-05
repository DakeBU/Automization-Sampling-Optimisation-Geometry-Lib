# SPHMC tilted-KL explicit-integral bridge

## Source role

Lee--Shen--Tian, arXiv:2010.03106v4, Lemma 2, and SPHMC
arXiv:2609.06906v1, Lemma 4.17, pass from a relative-entropy quantity to an
explicit smooth log-density ratio before evaluating its score.  This packet
formalizes the measure-theoretic KL-to-explicit-representative step.  It is an
ASTIS supporting expansion, not a new source theorem or the LSI/T2 argument.

## Frozen declaration

`TiltedKL.finite_klDiv_and_toReal_eq_integral_normalizedLogRatio` takes a
sigma-finite nonzero base measure, two integrable exponential tilts, and
integrability of their displayed normalized log ratio under the left tilt.
It concludes both finite canonical `klDiv` and equality of its real value with
the integral of that displayed representative.

## Proof route

1. Normalize both tilts as probability measures.
2. Compose left-tilt-to-base and base-to-right-tilt absolute continuity.
3. Use `TiltedLogRatio.llr_tilted_tilted_ae` only to transfer integrability.
4. Apply Mathlib's finite-KL theorem and equal-mass integral formula.
5. Replace the canonical `llr` integral by the explicit representative using
   `integral_congr_ae`.

## Strict boundary

The packet assumes, rather than proves, integrability of the explicit ratio.
It does not transport gradients through a.e. equality, prove an LSI or T2
inequality, calculate relative Fisher information, or conclude W2 contraction.
