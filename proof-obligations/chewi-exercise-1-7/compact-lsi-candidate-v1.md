# Compact-test LSI extension: focused Lean candidate

Local implementation of the [existing scope and proof plan](compact-lsi-extension-plan-v1.md).
This is not a released declaration, Statement Seal, VERIFIED Frontier Cell,
registry entry, or admitted Bench question.

## The mathematical step

The Langevin formulation in [§2.1.1, printed p. 48 / PDF p. 60](https://chewisinho.github.io/main.pdf#page=60)
uses compactly supported smooth tests. The test \(u_\varepsilon=\sqrt{1+\varepsilon g}\)
for [Exercise 1.7, printed p. 43 / PDF p. 55](https://chewisinho.github.io/main.pdf#page=55)
is generally noncompact, even for a compactly supported \(g\). Centering a
function can itself destroy compact support without changing its gradient.

For a finite-dimensional real Hilbert space, put \(u_n=\chi_{n+1}u\), where
\(\chi_R\) is the library's smooth radial cutoff. Apply the given inequality
to each compactly supported \(u_n\). The mass integrands are dominated by
\(u^2\). Writing \(q=u^2\) and \(a=\chi_{n+1}^2\), the entropy integrands
are bounded in absolute value by \(|q\log q|+q\): use
\(a q\log(aq)=a(q\log q)+q(a\log a)\), with the continuous zero extension.
The gradient product rule gives an energy envelope
\(2\|\nabla u\|^2+2K^2u^2\) from \(\|D\chi_R\|\le K/R\) for \(R\ge1\).
At every point the cutoff is eventually one on a neighborhood, giving exact
eventual agreement of the gradients. Thus dominated convergence applies
to all three integrals. Continuity of \(q\mapsto q\log q\) transfers the
entropy normalization, including zero mass. Closedness of real order yields
the same LSI constant for \(u\).

## Lean evidence and boundary

- `LogSobolevCutoff.cutoff_integral_limits` relocates the existing Gaussian
  module's measure-generic private proof; it is not a second proof or new
  mathematical credit. This result does not require finite dimension or a
  finite measure. Both the new extension and the unchanged public Gaussian
  theorem call the shared result.
- `LogSobolevCutoff.logSobolev_of_compact_smooth_tests` uses finite dimension
  for compact support, not for the three limits. It uses the source's
  \(C^\infty\) test premise, not the stronger premise that the inequality
  already holds on all compact \(C^2\) tests. No positivity of \(u\),
  positive mass, or sign restriction on the supplied constant is assumed.
- `Tests/Shared/LogSobolevCutoff.lean` actually applies the extension to
  \(u_\varepsilon\). It derives the `MemLp` requirement for its gradient from
  the existing square-root perturbation producer, the Riesz isometry and
  continuity of the genuine gradient. This example is not a second theorem.
- Focused Lean 4.33.0 built the shared module, Gaussian consumer, and its
  `StandardizedRGOKLFisher` and `StandardizedRGOKLDimension` downstream modules
  (3827 jobs). `lake env lean Tests/Shared/LogSobolevCutoff.lean` passed; both
  new public signatures used only `propext`, `Classical.choice`, `Quot.sound`.
- A local `Lean.Expr.getUsedConstants` check read the compiled proof bodies.
  It confirmed both consumers' direct dependency on `cutoff_integral_limits`
  and the existing RGO theorem's direct dependency on the Gaussian LSI. These
  are not module-import or prose-based edges; the public graph was not updated.

The next exercise step still has to center an arbitrary compact smooth
input, identify the entropy of the mass-one affine tilt, divide by the
nonzero squared parameter and pass to the compensated entropy and energy
limits. The abstract form-domain or Markov semigroup result is separate.
The Gaussian module's old whole-source publication binding is stale on this
candidate even though its public statement is unchanged. Renew that audit
and the new declaration publications before integration; do not rebind a
historical verdict or change root tests, site status or Registry by hand.
