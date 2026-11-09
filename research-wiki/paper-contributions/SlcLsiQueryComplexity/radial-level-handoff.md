# Radial level marginal on the actual coefficient law

[Eq. (16) and footnote 2](https://arxiv.org/html/2611.05813v1#S4.E16)
supply the literal shell product. [The use of Fact 10 in §6.2](https://arxiv.org/html/2611.05813v1#S6.SS2)
states the actual level marginal, separately from the independence assertion.
`RadialLevel.radialLevel_hasLaw` proves this unconditioned one-location law
including the zero-block Dirac branch, with variance `n * C_i(x)^2 * v_i`.

The proof uses the exact unscaled rho quotients and all four breakpoints.
It proves that a zero block makes the cutoff product zero; otherwise
normalization produces unit vectors, then the existing
`AngularDegreeSum.angularDegreeSum_hasLaw` and Mathlib's Gaussian scaling
apply. There is no positive-cutoff premise, external port, new generic
wrapper, or new Functor transport. The source invokes the fixed-location
part of Lemma 4.4 (which cites the linear representation in Lemma 4.3).
The checked implementation instead sums the uncut components and scales;
these are different topology views, not competing theorem statements.

The exact signature and source topology were sealed at
`b506e3435`. Candidate
`0ffcf29fd` passed
`lake build Tests.SlcLsiRadialLevel` (3193 jobs), including the actual
field's zero mean and exact variance, with only the standard axioms.
The Cell `ASTIS-SW-SLC-LSI-radial-level` and semantic binding carry the
independent review and eventual integration evidence. No Registry or
deployment credit follows from this handoff alone.

## Next dependency-ready boundary

The fixed-location joint level law and the weighted Gaussian law, integrability
and exact exponential moment of [Eq. (51)](https://arxiv.org/html/2611.05813v1#S6.E51)
were independently verified on separate local branches at `4d64756d7` and
`a672b8d23`. They are not included in this release or credited as deployed.
Next prove the actual cutoff range and shell plateau, which feed both the
spatial integral of the first moment in §6 and the reference distribution in §7.
The prefix-measurable gate factor and conditional expectation identity for
Fact 10 are a separate obligation.

## Integration boundary

The exact reviewed marginal, test, reader and publication binding are
unchanged on the `cdd030149`-based release. The complete ASTIS Lean gate
(Tests: 9646 jobs), site inventory/link/formula check, declaration graph
check, and four-subject desktop/mobile browser tests passed. Local Registry
adds one entry (615); this is not a paper-completion claim. The spatial
normalizer, mass estimates, conditional law, two-point/derivative covariance,
admissibility and all main lower bounds remain open.
