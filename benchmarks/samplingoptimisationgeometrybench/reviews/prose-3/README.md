# Finite-run subgradient energy: unpaired prose review

This round covers only sogb-020. The source reviewer `agent-task:/root/sog_source_review_7` independently checked the actual recurrence, squared-distance telescope, finite minimum, positive denominator, exact step-size constant and zero cases against the local Apache-2.0 Optlib port. No equivalent Lean QA was provided or certified.

The original report required two repairs: lower the provisional difficulty from L4 to L3 (a standard multi-step estimate, not a new cross-module composition) and derive the support-vector norm bound in this page rather than referring to a preceding exercise. The author changed only the first proof step and difficulty fields. The distinct exact-proposal reviewer `agent-task:/root/sog_exact_repair_7` accepted that exact change; earlier inputs/reports remain immutable.

SHA-256 evidence:

- Original input: `de1be00658424c9671921af270f005490f132b4f035898d87833c529053b468d`.
- Original report (repair required): `63d89203fd5e49b40e2b2e5d1e450ee5f7907aa2858355a740d3bda780cc7f21`.
- Exact repair input: `0bba68940c8360c60e5e4043c5173a86476ffff1d78d88d2260a42d162b82fef`.
- Repair report: `67c87571a96f9649c98b1a34ee6dc8f0d8f8084c2c2b6e822381986c86bdf3d5`.

The page folds the unchanged full supporting Lean module directly beneath the natural-language proof, retaining imports, namespace, copyright and modification notes. It can be copied/downloaded but is not a task template or a trusted-reference certificate for this whole QA. The local module proves norm control, weighted energy and best-iterate existence; the explicit step optimization and degenerate-case explanation remain prose. Sharing the subgradient family with sogb-019 prevents pretending these are independent split families.

Current acceptance is content/source-bound and **no-aligned-view**, not measured difficulty, theorem publication, model performance or Registry credit. The repair validator permits only proof/difficulty fields here, preserves the original question/assumptions/rubric/source, requires a fresh actor and rejects open repairs. Source drift makes admission stale; frozen audit bytes are never rewritten to conceal a failed review.
