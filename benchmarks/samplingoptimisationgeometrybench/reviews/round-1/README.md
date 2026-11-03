# Independent editorial review: round 1

Scope: original mathematical QA cores sogb-001–007, not canonical theorem publication, human expert consensus, empirical difficulty calibration or a model benchmark run. New cores sogb-008–014 and the graph tasks are outside this round.

The coordinator authored the QA but did not author the independent verdicts:

1. `packets/anonymous-input.json` contains only three anonymous Lean targets and necessary definition context. `/root/sog_blind_decoder_round1` received that input alone and produced `decoder.json`, reconstructing seven semantic slots. It could not see source identities, questions, gold proofs or earlier verdicts. `packets/coordinator-map.json` was not given to it.
2. `packets/reviewer-input.json` combines the independent reconstructions with the original seven QA cores and exact context bindings. `/root/sog_source_reviewer_round1` produced `source-review.json`: six accepted; sogb-003 required a repair. It received no preferred reviewer verdict.
3. `packets/repair-input.json` gives the exact before/after proposal, not the earlier verdict or a preferred classification. `/root/sog_exact_repair_reviewer_round1` produced `repair-review.json`, accepting the narrowly scoped explanation correction after independently checking it.

The issue was in **our own exposition**: positive strong convexity and Gaussian comparison are one sufficient normalization route, not necessary conditions for every Gibbs law. On the real line, \(V(x)=|x|\) has \(\int e^{-|x|}\,dx=2\), without a positive global strong-convexity modulus. Only the fourth explanation paragraph changed. Lean targets, reference proofs, theorem assumptions and mathematical conclusions were unchanged; no source-textbook erratum is asserted.

Inputs and actor reports are append-only audit evidence, pinned by raw-byte SHA-256; Git attributes preserve their bytes across Windows/Linux. **Some frozen inputs contain rejected wording. They are not training gold.** Use the generated `reviewed-reference.jsonl` for the current corrected accepted subset. Do not edit a report to make a later revision pass; use new evidence or let the status become stale.

`tools/sog_bench_review.py` verifies distinct roles, exact packet/proposal hashes, current QA/local-import/toolchain bindings, the correction's minimality and the formal boundary. The three paired targets cover their stated conclusions only, not all surrounding examples, counterexamples or consumer discussion. The independent reports list these unformalized parts. No Registry entry, paper completion status or canonical VERIFIED transition is changed by this review.
