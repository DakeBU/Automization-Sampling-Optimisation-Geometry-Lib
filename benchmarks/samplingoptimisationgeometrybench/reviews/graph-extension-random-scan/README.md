# Random-scan heat-bath proof slice

[Frozen input](input.json) · [Independent structural review](source-review.json)

`sogb-g009` is provisional L2 and shares the public development family of
`sogb-043`. The exact Lean 4.33.0 replay selected 11 theorem rows and eight
direct occurrences. In the displayed eight-node slice, the scan singleton
formula reaches the one-block pointwise law via the conditional law; the
unselected-site equality uses it directly. The fixed-site invariance and
random-scan reversibility targets do not reach that interface *in this slice*.

The separately replayed, [trusted private witness](PrivateBalanceTrace.lean)
shows a real occurrence route from the public reversibility theorem through
its private balance helper to the singleton formula. It is operator evidence,
not an edge in the question, an answer to the scored reachability task, or
evidence of mathematical necessity. From the repository root,
`lake env lean benchmarks/samplingoptimisationgeometrybench/reviews/graph-extension-random-scan/PrivateBalanceTrace.lean`
prints the operator witness; compare the JSON against
`proof_occurrence_witness.observed` in the exact input.

The [earlier review](preflight-answer-binding/source-review.json) preserved the
graph and score but rejected the old public answer-bound fingerprint: 32
guesses recovered the gold without reading any edges. The final review first
solved the public question, then confirmed answer-independent prompt and
Harbor projections. Its offline JSONL caveat was subsequently addressed by
rejecting duplicate keys and non-finite constants before scoring. Canonical
operator bindings and the score rule are unchanged. None of this makes a
public-development exercise a hidden test or a measured model result.
