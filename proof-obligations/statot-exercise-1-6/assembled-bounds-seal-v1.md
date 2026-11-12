# Statement seal v1 — Statistical Optimal Transport Exercise 6, assembled bounds

Sinho Chewi, Jonathan Niles-Weed and Philippe Rigollet, *Statistical Optimal
Transport*, July 2024 preface, public 290-page PDF, [§1.8 Exercise 6, printed
p. 44 / PDF p. 50](https://chewisinho.github.io/st_flour.pdf#page=50).
PDF SHA-256 `639ff16e79f4a32ade9c0595b0ed1d95490eb7e402949168895b6a6194a9c02f`.
Original mathematical restatement; no copied prose or source-redistribution grant.

## Exact interface

[Type-only probe](assembled-bounds-signature-v1.lean.txt) for
`AutoSamplingTheory.TechnicalLemmas.Measure.GaussianMixtureWasserstein.wassersteinDistance_gaussianMixtures_bounds`.
For every real \(m>0\), let \(G_a=\mathcal N(a,1)\) be the real Borel Gaussian
law with mean \(a\) and variance one. For
\[
\mu=\tfrac12G_{-m}+\tfrac12G_m,\qquad
\nu=\tfrac14G_{-m}+\tfrac34G_m,
\]
the quadratic Wasserstein distance obeys \(m/2\le W_2(\mu,\nu)\le m\).
These are explicit sufficient constants for the source's comparison up to
absolute constants, not claimed optimal. They are represented as ENNReal via
`ofReal`; \(m>0\) makes both endpoints nonnegative.

- \(m\) and \(0<m\): exact source parameter and hypothesis.
- The real Borel laws and their weights are literal local definitions, not
  extra function/measure binders. Their mass, first and second moments,
  the Lipschitz test, the feasible plan and cost are proof ingredients.
- Use the existing \(W_2\) definition and the existing infimum bridge. No
  assumptions of optimality, positivity of a general density, bounded support,
  or exact value of \(W_2\).

## Source topology and boundaries

- **NODE T**: a uniform two-sided comparison. Both the lower and upper
  branches must reach it for the same pair of laws and the same \(m>0\).
- **NODE L**: the lower hint requires the comparison
  \(\mathbb E_\mu f-\mathbb E_\nu f\le W_1\le W_2\) for a real
  1-Lipschitz test. The finite-moment conventions are in §1.2.
- **SOURCE_GAP L1**: normalize both literal mixtures, establish their second
  moments, and calculate their expectations. With \(f(x)=-x\) the correctly
  oriented signed difference is \(m/2\).
- **NODE U / SOURCE_GAP U1**: use a feasible coupling. Keep the common mass at
  each center and transport the remaining quarter by shared-noise translation
  through distance \(2m\); cost \(m^2\). The quadratic infimum is no larger.
- **EXCLUDED**: exact cost of an unknown optimizer, optimal constants,
  optimality of the chosen witness, a dual equality, adjacent exercises,
  or a newly admitted Bench task.

The two support packets were independently verified. The original focused
anonymous example at `53eae1c63f7305a11fa70556be49aa1927a106f5` assembled
them and proved the missing moments and means. This packet promotes that
assembly once as a canonical named source theorem with a focused consumer;
it does not turn a wrapper over a supplied bound into a new result.
