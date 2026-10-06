# Gaussian square-root density and energy domains

Status: focused compilation passed; independent review and exact-commit admission
are tracked in the SAU run, not inferred from this note.

- Canonical declaration:
  `AutoSamplingTheory.TechnicalLemmas.Measure.GaussianSqrtDensityDomain.gaussian_sqrt_density_domain`.
- File: `AutoSamplingTheory/TechnicalLemmas/Measure/GaussianSqrtDensityDomain.lean`.
- Real compiled paper consumer:
  `AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity.standardized_rgo_sqrt_density_domain`.
- Exact sealed statements, assumptions and definitions:
  `runs/20261007-companion-priority/gaussian-sqrt-density-domain/preproof/statement-seals.accepted.json`.
- Mathematical formula proof authored once:
  `website/content/declaration_lessons/gaussian-sqrt-density-domain.json`.
- Source anchor: SPHMC arXiv2609.06906v1 S4.Ex8 and S4.SS1.p4.2-p4.3 before
  FIRST S4.E6; this is authored omitted analytic background, not a printed
  standalone theorem or completion of its inequality.
- Minimal imports cover existing isotropic Gaussian density, Gaussian second
  moment, curvature/first-order convexity, Hilbert gradient and genuine tilts;
  no external SLT theorem is used or credited.

The corresponding Measure/Gibbs, Probability.StdGaussianMoment and
Analysis.Calculus.Gradient module cards, Probability/SDE contracts, canonical
technical-lemma index and pinned Mathlib APIs were searched before implementation.
Actual reused declarations are exhaustive in the canonical lesson and cell.

Hidden regularities are conclusions from the unchanged sealed inputs:
positive finite actual partition; actual probability; ordinary Gaussian-volume
quadratic integrability; continuous/strongly measurable density and gradients;
f and gradientf L2 under the covariance-identity Gaussian; gradientrho L2 under
the same actual tilted law; qlogq L1; pointwise explicit square-root/log-density
derivatives; finite energies with their exact coefficient. Dimension zero and
L=0 are allowed. There is no caller-supplied partition, regularity, moment,
gradient identity, LSI/T2 or final-output certificate.

Proof route: see the seven-step bounded blueprint
`proof-blueprints/gaussian-sqrt-density-domain.md` and the canonical formula lesson.
The initial API/elaboration failures and their strict fixes remain immutable in
the run. An unchanged route is frozen after the prescribed repeated fingerprint;
the sealed public statement changes only after separately reviewed mathematical
diagnosis. No such public-statement change occurred here.

Downstream use is limited to honest explicit-representative domains. Arbitrary
canonical RN versions may not be differentiated pointwise merely from a.e.
density equality. Actual KL/weak-Sobolev/LSI/T2 adapters remain separate. The
log-concave-sampling Gaussian/proximal route is planned reuse only; it is not a
second compiled consumer or an actual functional inequality producer.
