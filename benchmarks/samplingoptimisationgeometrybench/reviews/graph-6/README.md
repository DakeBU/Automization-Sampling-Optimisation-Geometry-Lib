# Initial statement-profile graph audit: source-pin gap

The independent actor `agent-task:/root/sog_flow_graph_review_6` accepted g001–g005 and required a source-provenance repair for g006–g007. Both fresh compiler replays and the structural answers passed; this did **not** prove adequate later freshness detection.

The flow selection includes an isolated midpoint theorem in `Geometry.StrongConvexity`, outside the anchor core's ancestor chain. Its local import `Geometry.LogConcavity` was not pinned by the selected-source list or anchor context. The reviewer independently mocked that ancestor's LF hash and observed that the old `recorded()` still admitted the same snapshot. This is a provenance/admission gap, not a false Lean theorem or an incorrect current graph answer.

Immutable evidence:

- Input SHA-256: `ff4458947510f6ff211a279ff6232e867eab48ab5591c229742020cd5314cbc3`.
- Reviewer report SHA-256: `be3c0bdb673d3dfca59c28a75fb759c1793f1592bd9a37c1cccff1b55fca08a6`.
- `compiler-before.py`, `compiled-transport-before.json` and `compiled-flow-before.json` preserve the actual pre-repair extractor and snapshots. The extractor LF hash matches their generator provenance; the raw snapshot hash matches its frozen question context. They are inert audit evidence, not production tools or ML/reference gold.

The correction pins the union of the local import closures of **all** selected modules, rather than assuming they all lie beneath one mathematical anchor. Current artifacts are regenerated; a distinct actor audits the new exact graph-7 packet from scratch. This report/input and the pre-repair evidence are not overwritten, and current admission cannot be inferred from this historical partial acceptance.
