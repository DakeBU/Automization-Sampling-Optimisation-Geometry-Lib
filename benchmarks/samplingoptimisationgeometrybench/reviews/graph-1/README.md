# Structural graph QA: original independent review

The frozen input and actual report belong to `agent-task:root/sog_graph_review_1`, distinct from the corpus author. The reviewer read the three listed original Lean sources and checked source hashes, consumer→import arrows, omitted-import boundaries, reference node sets, scorer behavior, family/split and provisional levels.

- Input SHA-256: `e692cc075b97740e766caaea9d16633b341fed9977698f0505642f6bb0a7d738`.
- Report SHA-256: `44f02160b9ed7d71620f0fd0e46f9a7e4b2a6c8971e2d8a934cbbfb9a9ac9809`.
- sogb-g001/g002 accepted. Initial sogb-g003 L3 label required repair; its source/answer/scoring were not rejected.

An [L2 proposal](../graph-2/README.md) was independently rejected as still overstated. The [final L1 proposal](../graph-3/README.md) received a separate independent decision. Do not edit or train on these historical reports as reference gold; current admission is derived by `tools/sog_bench_graph_review.py` from exact packets and raw report hashes. Label repairs add no questions or formal mathematics.

The isolated scorer checks are software self-tests, not measured AI scores. Neither this review nor import reachability certifies mathematical necessity, theorem entailment, full difficulty calibration or held-out generalization.
