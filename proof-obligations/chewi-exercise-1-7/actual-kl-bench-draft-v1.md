# Exercise 1.7: actual-law KL Bench draft

An original restatement of the bounded centered specialization of
[Chewi (1.E.1)](https://chewisinho.github.io/main.pdf#page=55), not copied
textbook prose. Proposed public family: `chewi-lcs-2026-08-20-exercise-1-7`,
the same as the [compact PI draft](compact-pi-bench-draft-v1.md). These are
distinct mathematical tasks; near-duplicates and all views must stay in
the same split. No catalog admission, benchmark execution, or score yet.

## Prompt only

Let \(\mu\) be a probability measure on a measurable space, and let \(f\) be
a real a.e. strongly measurable function such that \(|f|\le M\) almost
everywhere for some finite \(M\) and \(\int f\,d\mu=0\). For real
\(\varepsilon\), put
\(d\nu_\varepsilon=(1+\varepsilon f)_+\,d\mu\).

Prove that for all sufficiently small \(|\varepsilon|\), including zero,
\(\nu_\varepsilon\) is a probability and its canonical KL relative to \(\mu\)
is finite. Then prove the real-valued expansion
\[
 \mathrm{KL}(\nu_\varepsilon\|\mu)
  =\frac{\varepsilon^2}{2}\int f^2\,d\mu+o(\varepsilon^2)
 \qquad(\varepsilon\to0).
\]
Account for the actual probability law and justify passing the expansion
through the integral. The limit is two-sided.

Suggested natural-language level: L4, provisional. The reasoning combines
law normalization, extended-real divergence semantics and uniform remainder
control; it is not a question about recalling the coefficient. A closed-book
run supplies the prompt and mathematical definitions only. A library-assisted
run may supply a separately pinned retrieval context and must be reported
separately. No raw source PDF or reviewer artifacts enter the model prompt.

## Grader only

Use the [reference proof](actual-kl-candidate-v1.md). Accept any valid proof
with the same assumptions, two-sided scope, actual law and constants.

| Points | Required evidence |
| --- | --- |
| 2 | Proves uniform a.e. positivity for small parameters, including the degenerate bound, and explains why clipping does not alter the local law. |
| 2 | Uses probability and centering to obtain exact mass one and identifies the actual density relative to the reference measure. |
| 2 | Proves canonical KL is finite before converting to its real value; cancels the linear compensation or proves the corresponding entropy expansion directly. |
| 2 | Establishes the (1/2) coefficient and a legitimate integrable envelope or equivalent uniform remainder estimate. |
| 2 | Obtains the two-sided (o(\varepsilon^2)) statement with zero endpoint consistent with \(\nu_0=\mu\), without treating the value of a quotient at zero as evidence. |

Reject as a complete answer: a scalar Taylor formula without a domination or
uniform remainder argument; a proof of the compensated integral alone with
no law identification; deducing finite extended-real KL from its totalized
real value; or only proving a positive-sided expansion. A valid proof may
use the ordinary finite KL density formula after justifying its domain.

## Lean and graph boundary

The aligned candidate is the [frozen actual-law Lean signature](actual-kl-statement-v1.lean.txt).
A fixed-target environment may permit the actual-law identity and compensated
integral limit, but must exclude the completed exercise-answer module and its
proof from the agent environment. The checked reference must be exported
separately. This draft does not claim that a sealed evaluator for this task
has been registered or run.
Proposed library-assisted Lean level: L3, provisional. With those two producers
available, the work is to connect finite extended-real divergence, the real
limit, and the full-neighborhood endpoint; the scalar asymptotic itself is
already a permitted result.

A possible graph view compares the direct compiled PI and KL branches:
the compensated integral limit is shared; the actual-law identity belongs
to KL and the cutoff/energy steps belong to PI. This is a selected proof-body
occurrence question, not evidence of logical necessity. The source use of
(1.E.1) in Corollary 2.1.2 does not yet imply a compiled edge to that corollary.
