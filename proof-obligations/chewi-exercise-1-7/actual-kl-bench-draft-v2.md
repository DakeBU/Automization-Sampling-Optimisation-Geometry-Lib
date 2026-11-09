# Exercise 1.7: actual-law KL Bench draft, revision 2

An original restatement of the bounded centered specialization of
[Chewi (1.E.1)](https://chewisinho.github.io/main.pdf#page=55), not copied
textbook prose. Proposed public family: `chewi-lcs-2026-08-20-exercise-1-7`,
the same as the [compact PI draft](compact-pi-bench-draft-v2.md). These are
distinct mathematical tasks; near-duplicates and all views must stay in
the same split. No catalog admission, benchmark execution, or score yet.

## Prompt only

Let \(\mu\) be a probability measure on a measurable space, and let \(f\) be
a real a.e. strongly measurable function such that \(|f|\le M\) almost
everywhere for some finite \(M\) and \(\int f\,d\mu=0\). For real
\(\varepsilon\), put \(d\nu_\varepsilon=(1+\varepsilon f)_+\,d\mu\).

For probability laws, use canonical extended-real KL: it is \(+\infty\)
without absolute continuity; otherwise it is the extended integral
\(\int r\log r\,d\mu\), where \(r=d\nu/d\mu\) and \(0\log0=0\).
Prove that for all sufficiently small \(|\varepsilon|\), including zero,
\(\nu_\varepsilon\) is a probability and its canonical KL relative to
\(\mu\) is finite. For its ordinary real value \(K_\varepsilon\) after
this finiteness is established, prove
\[
 K_\varepsilon=\frac{\varepsilon^2}{2}\int f^2\,d\mu+o(\varepsilon^2)
 \qquad(\varepsilon\to0).
\]
Account for the actual probability law and justify passing the expansion
through the integral. The limit is two-sided.

Suggested prompt-only natural-language level: L3, provisional. One a.e.
bound controls law normalization and a single uniform scalar remainder.
The task checks the domain and constants rather than mere recall.

## Grader only: four binary criteria

Use the [reference proof](actual-kl-candidate-v1.md). Each criterion is 1
only when its evidence is present, otherwise 0. Report all four flags;
all four are necessary for a complete solution.

| Criterion | Required evidence for 1 |
| --- | --- |
| Local law | Justifies a measurable density up to a null set, eventual a.e. positivity including degenerate bounds, exact mass one, absolute continuity and the actual density relative to \(\mu\). An argument uniform in the bound need not treat \(M=0\) separately. |
| Finite canonical KL | Establishes the genuine extended-real finiteness from the domain and integrability of the density entropy, or an equivalent valid formula, before interpreting the real value. An identity for a totalized real conversion alone is insufficient. |
| Quadratic coefficient | Cancels the integrated linear term (with or without a compensated function) and establishes the \(1/2\) coefficient with a legitimate integrable envelope or uniform remainder. Finiteness alone is not this limit. |
| Full remainder | Proves the two-sided little-o and the zero remainder at \(\nu_0=\mu\); a proof applying the positive-side estimate also to \(-f\) is valid. An all-small-parameters argument may include zero implicitly. A quotient value assigned at zero is not convergence evidence. |

A scalar Taylor expansion without a uniform or dominated integral step,
a compensated integral alone without law identification, or a one-sided
limit alone is not a complete answer. Use any valid proof with the same
assumptions, domain and constant.

## Future tool profiles

Prompt-only prose supplies the mathematical prompt and definitions, no
external retrieval. Library-assisted prose uses separately pinned eligible
retrieval and is reported separately. Before an answer-excluded Lean run,
enforce the compiler, allowed imports and transitive context, search and
compiler permissions, and absence of finished answer sources from imports,
file search and retrieval. Strip all reference links, rubric, graph notes
and reviewer artifacts from agent-facing data. No restricted ATLAS material
is allowed. An open-web or answer-access profile is distinct; none of these
draft profiles has been run here.

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
