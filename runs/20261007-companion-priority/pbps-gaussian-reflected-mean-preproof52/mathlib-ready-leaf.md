# Literal reflected Gaussian mean: prospective analytic leaf

This is a source/API packet, not a compiled theorem. The typed signature is
independently sealed; independent source topology admission is still required
before claim and implementation. No paper theorem is complete.

Proposed canonical declaration:
`AutoSamplingTheory.TechnicalLemmas.Measure.GaussianReflectedMean.gaussian_reflected_mean_c1`
in `AutoSamplingTheory/TechnicalLemmas/Measure/GaussianReflectedMean.lean`.
Use the already verified GaussianConvolutionRegularity import and only needed
public Mathlib dominated-calculus/Bochner/map/tilt facts; no copied parent proof.

For arbitrary probability mu on a finite real Hilbert/Borel space and eta>0,
R_y = mu.tilted(-||x-y||^2/(2 eta)), S_y = R_y.map(x -> 2x-y).
For signed compact C1 f, produce C1 of the actual function
y -> integral f(u) dS_y(u). There is no supplied moment, density, partition,
integrability, derivative bound/continuity or gradient-closure certificate.

The source uses smooth compact f and its Gibbs mu. The any-probability input,
C1 observer and finite Hilbert/rank0 formulation is an attributed authored
background generalization. Fixed PBPSv1 C.1 A3.Ex1 is physical4581-4587,
A3.Ex2 physical4589-4595 and normalized differentiation A3.E1 physical4597-4604;
use the independently sealed primary52 contract and original preread52 with its
two immutable coordinate errata. The source's actual Gibbs reflection carries
the 1/(8 eta) density scale and 1/(4 eta) parameter-score scale. Neither is
silently replaced by a Gaussian likelihood convention.

Canonical search/cards are in root.retrieval-boundary.json and preread52.
Selected public contracts: GaussianConvolutionRegularity positive C2Z;
Mathlib hasFDerivAt_integral_of_dominated_of_fderiv_le,
continuous_of_dominated, contDiff_one_iff_hasFDerivAt, integral_map and
MeasureTheory.integral_tilted. The existing Probability law derivative
adapter has a different scalar-parameter conclusion; no library-wide absence
is claimed. Private Gaussian bounds and the existing local source-density
reflection argument are exposure only and cannot be called as public exports.

All hidden conditions must be produced internally: f and fderiv continuous
and globally bounded from compact C1; Gaussian weight and parameter derivative
measurable with an integrable uniform bound against mu; genuine L1 before
map/tilt/real normalization; every-y strictly positive finite partition;
continuous integrated Frechet derivative; exact normalized mean, not an
arbitrary AE conditional version. Rank0 has no centering requirement.

Source-backed planned route (no tactic/proof search has begun):

1. Derive finite global bounds Mf and Mf' for f and its actual Frechet derivative.
2. Differentiate K(y,x)=exp(-||y-x||^2/(2 eta)) and F(y,x)=f(2x-y)K(y,x);
   bound the actual derivative by the probability-integrable constant
   Mf' + Mf(1+2 eta)/eta. Both negative derivative terms are retained.
3. Prove genuine measurability/L1 and apply dominated parameter differentiation
   to N(y)=integral F(y,x) dmu(x).
4. Use the same domination and pointwise continuous derivative to obtain a
   continuous integrated derivative and hence C1N.
5. Obtain positive C2Z from the admitted actual Gaussian producer; prove actual
   every-y posterior/reflection mean=N/Z and conclude C1 by quotient calculus.
6. Exercise actual input probability and rank0/noncentered semantics in Tests.
7. Leave the source-density SAME-S pointwise adapter and subsequent actual Tf
   closure membership as named downstream consumers, not outputs of this leaf.

Failure policy: freeze a route after unchanged repeats; diagnose missing
regularity, false statement, representative mismatch, pinned API mismatch or
oversized target. Retain compiled fragments and exact negatives. A strictly
smaller C1 numerator target requires a newly sealed statement and reviewed
source boundary; no premise supplying domination or derivative continuity is
allowed. Full rough B.13, Gamma, half-turn, main results, errors, costs and
actual-input composition remain open.
