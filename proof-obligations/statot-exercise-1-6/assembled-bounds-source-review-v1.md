# Independent source review — Statistical Optimal Transport Exercise 6, assembled bounds v1

**Verdict: ACCEPT (source-to-statement and proof topology only).**

I visually checked Exercise 6 on printed p. 44 / PDF p. 50 of Sinho Chewi,
Jonathan Niles-Weed, and Philippe Rigollet, *Statistical Optimal Transport*,
and §1.2, printed pp. 15–16 / PDF pp. 21–22, for the moment and distance
conventions. I compared those pages with the two sealed inputs below. I did
not inspect the earlier example, implementation, drafts, or prior reviews;
this is not a proof or a Lean elaboration verdict.

## Reviewed bytes (SHA-256)

- `.astis/sog-bench/tmp/pdfs/statot-intake-20261104/st_flour.pdf`: `639ff16e79f4a32ade9c0595b0ed1d95490eb7e402949168895b6a6194a9c02f`
- `proof-obligations/statot-exercise-1-6/assembled-bounds-seal-v1.md`: `52047166268bfee06bd76826d027865e849ad47b5be9dee0b2f5ff020e6a1b04`
- `proof-obligations/statot-exercise-1-6/assembled-bounds-signature-v1.lean.txt`: `4f11af4b8a85d334d7eb6c629e304bb53a3c3381adfeb488c2cbda362ce83a9f`

## Statement fidelity

The literal real laws agree, in the source's order: the weights at the
centers \((-m,+m)\) are \((1/2,1/2)\) for \(\mu\) and \((1/4,3/4)\) for
\(\nu\). Both components have variance one, not variance depending on \(m\).
The only input beyond \(m\in\mathbb R\) is \(0<m\); in particular there is
no large-separation threshold. The signature fixes the laws locally rather
than quantifying over laws, tests, couplings, or supplied bounds. Its two
inequalities, with the nonnegative real endpoints embedded by `ENNReal.ofReal`,
give absolute constants \(1/2\) and \(1\) for the source's uniform
\(W_2(\mu,\nu)\asymp m\). The target is the distance, not its square. These
constants do not assert an exact value, sharpness, or an optimizer.

## Branch and obligation check

- **L — signed Lipschitz lower bound.** The source specifically asks to
  establish and use the signed comparison through \(W_1\) for any real
  1-Lipschitz test. The seal retains that branch. The two mixtures must
  first be probability laws (nonnegative weights summing to one) with
  finite second moments (each component has second moment \(1+m^2\)); this
  also gives finite first moments and integrability of any such test by
  its at-most-linear growth. The first-moment check is \(0\) under \(\mu\)
  and \(m/2\) under \(\nu\). Thus the test \(f(x)=-x\) gives the positive
  signed difference \(m/2\) in the source's orientation; \(f(x)=x\)
  would give the wrong sign. Both comparison links must be justified by
  the lower-branch support, not added as hypotheses. At the topology level
  their inputs are exactly the Lipschitz inequality under each coupling
  and the first-cost versus root-second-cost inequality for a probability
  coupling.
- **U — feasible coupling upper bound.** The witness keeps a quarter at
  the negative center and a half at the positive center with identical
  coordinates, and pairs the remaining quarter from the negative center
  to the positive center using the same Gaussian noise on both sides.
  The row masses are \((1/2,1/2)\) and the column masses \((1/4,3/4)\),
  so both marginal laws, not just total mass, match the literal target.
  Only the moved quarter has nonzero squared displacement, yielding
  quadratic cost \((1/4)(2m)^2=m^2\). The feasible-plan/infimum step and
  \(\sqrt{m^2}=m\) give the distance bound without identifying a minimizer.

Both branches meet at the same pair of laws for every \(m>0\). The mass,
moment, expectation, coupling-marginal, cost, and distance-bridge checks
are proof obligations, not omitted premises. No density condition,
bounded-support restriction, dual equality, or optimality claim is needed.
