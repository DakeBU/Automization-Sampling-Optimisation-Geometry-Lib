# Frozen candidate: compact Euclidean LSI implies PI

Statement ID: `chewi-ex1-7-compact-pi-v1`. The exact Lean signature in
[`compact-pi-statement-v1.lean.txt`](compact-pi-statement-v1.lean.txt) has SHA-256
`43766c48f2ff7a0ffdd2e8005994d65246766329cef913be80a22ef4ce072714` (LF).
This pins the local statement before proof work; it is not an official Cell or
publication transition.

Primary source: Sinho Chewi, *Log-Concave Sampling*, August 20, 2026, PDF
SHA-256 `8818e8fb40c07bd70651bafe10e8ec4500197c836928330b90025ca47da52fae`.
[Exercise 1.7, printed p. 43 / PDF p. 55](https://chewisinho.github.io/main.pdf#page=55)
asks for linearization, and [§2.1.1, printed pp. 48–49 / PDF pp. 60–61](https://chewisinho.github.io/main.pdf#page=60)
gives the compact Euclidean test classes and normalization. Use the existing
[independent source-topology review](source-topology-review-v2.json); its abstract
Chapter 1 boundary remains open.

For a Borel probability measure \(\mu\) on a finite-dimensional real Hilbert
space, suppose \(\operatorname{Ent}_\mu(v^2)\le 2C\int\|\nabla v\|^2\,d\mu\)
for each smooth compactly supported real test \(v\). Every such \(f\) then
satisfies \(\operatorname{Var}_\mu(f)\le C\int\|\nabla f\|^2\,d\mu\), with
the integrability of \(f\), its squared centered value and its gradient
energy derived. A generic real \(C\) suffices for this implication, so the
signature does not require the source's usual positive-constant convention.
It asserts neither optimality nor equality of the best constants.

Binder audit: the inner-product, complete, finite-dimensional Borel carrier is
`TYPING`; the probability measure, compact-smooth LSI, and compact-smooth test
are `SOURCE`. The gradient is genuine on smooth tests. `Poincare.variance`
is literally the integral of \((f-\int f\,d\mu)^2\), and `dirichletEnergy`
is literally the integral of the squared gradient norm. `Admissible` is an
explicit **output** discharging the three integrability obligations, not an
extra premise. Centering, boundedness, compact derivative support, nonnegative
tilt, mass one, the noncompact square-root LSI application, and the two limits
are internal proof edges. The separate actual-law KL statement (1.E.1) and
abstract semigroup or closed form-domain conclusions are not this Anchor.
