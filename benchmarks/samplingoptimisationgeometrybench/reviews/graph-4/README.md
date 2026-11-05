# Explicit current-policy graph review

This round independently rechecks all five current structural questions: three source-import questions and two selected compiled-proof-body questions. It explicitly supersedes graph-1/2/3 for **current** admission; their inputs, actual decisions and raw hashes remain immutable historical evidence.

Reviewer: `agent-task:root/sog_snapshot_qa_review_4`, distinct from the author. The reviewer read the frozen current packet and original sources, independently replayed `python tools/sog_bench_compiled_graph.py check` and checked exact bindings, eligible-source boundaries, scorer edge cases and provisional difficulty. Previous verdicts and repair proposals were not supplied or consulted.

- Input SHA-256: `7fcb2eab5cdf5f3d56c2fcb659b36ab7ae868dd97aa5e0658aa998413915353f`.
- Actual report SHA-256: `31884d605c06fc1aa21e497734f6906c7abdfd4454b4af20be2e02991a2f8b04`.
- g001/g003/g004/g005: accept.
- g002: repair-required. The directly visible singleton common-parent lookup should use L1, consistently with the same reasoning demand in g004. This changes no mathematical source or graph answer.

The [separate exact repair review](../graph-5/README.md) covers only the later L2→L1 label/binding proposal. Current state is derived from the exact packet/source/scorer/policy and that separately accepted proposal, never by editing this report.

The compiler artifact selects public theorem constants from six eligible original source files. It omits unselected constants, private auxiliaries and Mathlib parents; it is not a full closure or a theorem-necessity certificate. An absent induced path does not prove full independence. A replay checks occurrence data, not model performance, calibrated difficulty or canonical theorem publication. Raw review records are audit-only and excluded from ML/reference bundles.
