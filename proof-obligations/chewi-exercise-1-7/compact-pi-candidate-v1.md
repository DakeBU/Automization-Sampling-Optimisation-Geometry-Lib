# Exercise 1.7: compact Euclidean proof candidate

Scope and exact signature: [compact-pi-statement-v1](compact-pi-statement-v1.md).
This is original exposition of the bounded proof route, not a reproduction of
the textbook prose or a statement about a closed Dirichlet-form domain.

## Proof

Fix a smooth compactly supported \(f\), and let
\(g=f-\int f\,d\mu\). The original function is bounded by continuity and
compact support; hence \(g\) is bounded as well. It has mean zero because
\(\mu\) is a probability measure. Centering need not preserve compact support,
but \(Dg=Df\) does have compact support. In particular \(g^2\) and
\(\|\nabla f\|^2\) are integrable: the first is bounded on a finite measure,
and the second is continuous with compact support.

For sufficiently small \(|\varepsilon|\), set
\(p_\varepsilon=1+\varepsilon g\) and \(u_\varepsilon=\sqrt{p_\varepsilon}\).
The boundedness of \(g\) ensures \(1/2\le p_\varepsilon\le3/2\), so
\(u_\varepsilon\) is genuinely smooth. It need not be compactly supported;
the [cutoff extension](compact-lsi-candidate-v1.md) supplies the right domain
for the LSI. Its integrability hypotheses are supplied by the existing
square-root perturbation result. In particular the Fréchet derivative norm
equals the gradient norm by the Riesz isometry.

Since \(\int p_\varepsilon\,d\mu=1\), the normalization term in
\(\operatorname{Ent}_\mu(u_\varepsilon^2)\) is zero. The compensation terms
also cancel after integration. Thus with \(k(t)=t\log t+1-t\),

\[
 \int k(p_\varepsilon)\,d\mu
   = \operatorname{Ent}_\mu(u_\varepsilon^2)
   \le 2C\int\|\nabla u_\varepsilon\|^2\,d\mu.
\]

Divide by \(\varepsilon^2>0\) and approach zero through nonzero parameters.
The entropy numerator divided by \(\varepsilon^2\) tends to
\(\tfrac12\int g^2\,d\mu\). Indeed \(k(1)=k'(1)=0\) and \(k''(t)=1/t\),
so Taylor's formula with integral remainder gives
\[
 \frac{k(1+\varepsilon g(x))}{\varepsilon^2}
 = g(x)^2\int_0^1\frac{1-s}{1+s\varepsilon g(x)}\,ds.
\]
The denominator is at least \(1/2\) throughout the segment, so this is
bounded by \(g(x)^2\) and tends pointwise to \(g(x)^2/2\). The Lean
producer establishes the same scalar limit and domination separately.
The genuine square-root derivative
gives the pointwise energy quotient
\(\|\nabla g\|^2/(4p_\varepsilon)\), dominated by
\(\|\nabla g\|^2/2\). Its integral tends to
\(\tfrac14\int\|\nabla g\|^2\,d\mu\). Passing the inequality to the limit,

\[
 \frac12\operatorname{Var}_\mu(f)
 \le 2C\cdot\frac14\int\|\nabla f\|^2\,d\mu,
\]

which gives PI with the same constant, not equality of the optimal constants.

## Lean correspondence

The declaration is
`CompactLogSobolevPoincare.variance_le_of_compact_logSobolev`. The finite
domain is an explicit `Poincare.Admissible` conclusion. The proof calls the
owned square-root domain, cutoff LSI, compensated-integral limit, and
square-root energy limit. Mathlib supplies ordinary integration, genuine
differentiation and Riesz isometry, and closedness of real inequalities
under convergence. `Tests/Shared/CompactLogSobolevPoincare.lean` uses the
existing compact Gaussian LSI at constant one and checks the resulting PI.

This proof uses a real compensated entropy integral, not a claim about a
chosen RN representative or an extended-real probability KL. The separate
standalone actual-law expansion in (1.E.1), the closure/core step, and the
abstract Chapter 1 implication must not be marked complete from this result.
