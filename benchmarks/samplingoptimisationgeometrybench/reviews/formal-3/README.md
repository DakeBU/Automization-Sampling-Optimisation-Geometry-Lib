# Paired editorial review: joint mass from one marginal

This round checks sogb-015, the L2 natural-language/Lean pair over the existing coupling-normalization lemma. It introduces no production theorem or Registry leaf.

1. The author froze the question, formula proof, rubric, exact task context and source bindings before review. The given context reproduces the actual public coupling definition; the target module is not imported.
2. `packets/anonymous-input.json` contains only the anonymous signature and minimal definition context, with owning namespace labels removed. `packets/coordinator-map.json` was kept from the decoder.
3. Fresh independent actor `/root/sog_blind_3` read only the anonymous input and wrote `decoder.json`. It reconstructed all seven slots, including arbitrary measurable spaces and the absence of a separate probability/finiteness assumption on the joint or second marginal.
4. `packets/reviewer-input.json` combines that independent reconstruction with the exact authored QA and source context. Fresh independent actor `/root/sog_paired_review_3` checked the public definition, actual theorem, Mathlib mass API, formula proof and rubric, and accepted the pair without repair.

The checked mathematical mechanism is the measurable first projection:

$$
\gamma(\alpha\times\beta)
 =(\gamma.\mathrm{fst})(\alpha)
 =\mu(\alpha)=1.
$$

No joint finiteness assumption is needed to use `Measure.fst_univ`. The second marginal equality is part of the given coupling contract but is unused in this calculation. The theorem returns a proof of the Prop-valued probability class; consumers can install it locally when a typeclass instance is needed. It does not globally register an instance or prove unbounded integrability, transport optimality or a moment bound.

Acceptance is **conclusion-only AI editorial evidence**, not canonical theorem publication, human expert consensus or empirical difficulty calibration. The provisional L2 label reflects a local pushforward-mass calculation, not the three-line tactic proof. Candidate/public-family history remains public; this is not an unseen test.

`tools/sog_bench_formal_review.py` checks distinct roles, exact anonymous target/definition bytes, decoder reconstruction, anti-anchored reviewer input, all seven comparison slots and current source/import/toolchain bindings. Reports are append-only and byte-preserved across platforms. Revisions become stale; overlapping rounds cannot silently replace decisions. Frozen legacy rounds retain their own adapters while new disjoint `formal-*` rounds use this shared implementation.
