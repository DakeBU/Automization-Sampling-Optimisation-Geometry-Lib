# Supporting vectors and an actual conditional-resampling kernel

This bounded round covers sogb-019 and sogb-021. Their fixed Lean targets are the existing global supporting-vector norm bound and finite-measure heat-bath invariance theorem, not wrappers around assumed conclusions. The second context supplies the actual kernel definition only. Neither task imports its owning theorem module.

Actual independent roles:

- Author/coordinator: `agent-task:root`.
- Source-blind decoder: `agent-task:/root/sog_blind_7`.
- Anti-anchored source reviewer: `agent-task:/root/sog_source_review_7`.
- Exact-proposal reviewer: `agent-task:/root/sog_exact_repair_7`.

The source reviewer confirmed all seven semantic slots, source hypotheses and provisional NL L3 / Lean L2 labels, but required a scoring repair: questions permitting any valid counterexample must not demand the reference example. Only the fourth rubric criterion of each core changed. The questions, proof steps, definitions, assumptions, source, Lean target/reference and earlier evidence remain unchanged. The fresh exact-proposal reviewer accepted these repairs with no open request. This is **conclusion-only** formal coverage: the explanatory constrained-support and nonconvergence counterexamples are not separately formalized.

Immutable SHA-256 evidence:

- Anonymous input: `2799631107ebdca6a0197362dac33db24896d4cffc676707d228469a5c998a76`.
- Decoder report: `b7eb9b4fd4bc61b5b9e2d3bf1453bf65f8ed80c5b68d072105c5bf10f1048cbe`.
- Source input: `e6d049882615b38bf1cf59d9d2965500cb069c84b73bffb0e52ab0ffd86b4150`.
- Original source report (repair required): `bc22cf3d4349a8f7ad608a38cc57da4c6ad2faaed70725d1bd0506276746e289`.
- Exact repair input: `e80118b55a3ea126da26805b2ac94d4da02e9f2ade2e38e3d5dd18fd8f457bde`.
- Repair report: `01e79bb99d9749d690f38dc2c7ddb3ac07d93969fa85b6385c7285ab28297819`.

The norm estimate bounds supplied global supports, not constrained normals or a constructed oracle. The kernel result permits finite zero targets and requires only the stated standard-Borel/nonempty resampled coordinate; invariance is not convergence, reversibility or a continuous-time Gibbs theorem. Optlib notices remain in the extracted norm reference. Both trusted references compiled under fixed Lean 4.33.0, separately from these editorial decisions. There is no empirical calibration, model score, new Registry leaf or paper-completion credit.

Current admission is derived from exact content/source/context bindings and the separate repair overlay. A changed QA/source becomes stale. Historical reports are audit only and excluded from ML/reference bundles.
