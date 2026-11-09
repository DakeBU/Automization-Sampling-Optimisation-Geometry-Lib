# Formal round 13: a common Markov kernel preserves an event error budget

`sogb-037` is an original two-track L3 exercise in the public
`adaptive-hybrid-cost-boundary` family. It explains the abstract data-processing
step used in the [SPHMC v1 proof of Theorem 1.3, §7.2](https://arxiv.org/html/2609.06906v1#S7.SS2).
It is not a textbook quotation, construction of the paper's actual kernel,
or a cost transfer for unbounded work.

- [Anonymous signature](packets/anonymous-input.json) and [independent reconstruction](decoder.json).
- [Exact source review input](packets/reviewer-input.json) and [independent source review](source-review.json).
- [Focused Lean 4.33.0 trusted-reference receipt](trusted-reference-receipt.json).
- [Selected compiled proof occurrences](compiled-proof-occurrences.json): the common-suffix proof calls both conditional error averaging and the common-kernel contraction. These edges record proof-body occurrences only, not a full closure, mathematical necessity or a new graph task.

The [predecessor review](predecessor-repair-required/source-review.json) and
its exact packet are retained unchanged with an [adjacent upstream notice](predecessor-repair-required/NOTICE.md).
The accepted revision explicitly credits valid alternative
proofs and retains the Mathlib author and adaptation notice in the extracted
Lean file. The same inequality is displayed on three lines for narrow screens.
Only the eventwise bound is an aligned Lean conclusion; the sharpness and
different-kernel counterexamples are prose. These are separate editorial,
reference-compilation and graph evidence, not measured model scores.
