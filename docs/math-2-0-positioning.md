# Samplinglib contributions to Math 2.0

Samplinglib connects readable mathematics, a living network of papers and textbooks, and reusable Lean proofs for sampling, optimisation, and geometry. Its purpose is to help people understand and extend the mathematics they can verify.

[Terence Tao's October 2026 Math 2.0 lecture](https://teorth.github.io/tao-web/slides/math-2-0-caltech-2026.pdf) describes a transition from scarce proofs toward abundant proofs. His central proposal is to strengthen the connections between mathematics and human understanding. Slides 22 and 25–26 give nine relevant examples; the numbering below organizes those examples for our project and does not imply an endorsement.

## Foundations and reader value

The living knowledge network (2) and high-quality formal library (3) are our foundations. Exact sources, hypotheses, Lean declarations and reviewed dependencies connect books and frontier papers. Open exposition problems (1) and interactive teaching (8) are their human purpose: a learner should see the theorem, why it matters, the recurring mechanism, its assumptions, and a readable proof before opening the exact Lean.

The Functor Hypergraph records candidate mechanisms shared across spaces, divergences and dynamics. It can guide explanations and research questions; only separately checked transport theorems create formal Lean edges. Compression must retain a drill-down to complete proofs, assumptions and provenance. Graph shape alone cannot rank a paper's originality or importance.

## Research experiments

| Direction | Samplinglib experiment | Required evidence |
|---|---|---|
| 4. New principles and methods | Compare curvature, entropy dissipation, gradient-flow and mixing arguments across routes. | A precise proposed mechanism, hypothesis maps, and a reviewed explanation; a new formal claim also needs Lean evidence. |
| 5. Proof ablation | Freeze a theorem's conclusion and source assumptions, remove a selected theory or proof ingredient, and search for an alternative proof. | Dependency audit, explicit forbidden inputs, full alternative proof and independent review. Encoder–denoiser checks semantic fidelity; it does not by itself perform ablation. |
| 6. Theorem neighborhoods | Vary regularity, curvature, oracle or approximation assumptions and state what conclusion survives. | Separate exploratory contracts, compiled positive results or checked counterexamples. A timeout or unavailable API is not a refutation. |
| 7. Interpretable mathematical models | Align our own or appropriately licensed explanations, Lean proofs, graph structure and typed failures for retrieval, evaluation and model research. | Per-artifact licensing, provenance and evaluation records. A Lean proof is an inspectable certificate, not a transcript of a model's internal reasoning or a safety guarantee. |
| 9. Model boundaries and failure modes | Audit the gap between ideal samplers and approximate gradients, discretization, finite precision, tails or distribution assumptions. | Explicit model-to-application assumptions and concrete failure examples. Lean checks implications within the stated model; empirical evidence and domain judgment assess its fit to reality. |

These experiments build on existing graph, source-review, proof-digestion and evidence-memory machinery. A contribution becomes a completed result only when its own acceptance evidence exists. Preserve failed attempts, resource costs and typed obstructions alongside successes.

## Public presentation

Use the shared mission “human-understanding infrastructure for Math 2.0”, followed by the domain and a concrete capability. Label existing infrastructure, active work and research plans separately. Cite Tao's lecture as inspiration; attribute source authors accurately.

README and home pages should introduce the library's purpose and provide three immediate routes: learn the mathematics, explore proof mechanisms, inspect Lean evidence. The nine directions belong on a dedicated page with links to current material and a specific next contribution. Mathematical pages retain the existing statement, readable proof, assumptions, source mapping and folded Lean publication contract.

External references are not automatically model-development data. In particular, the ATLAS v1 restrictions recorded in [Attribution](attribution.md) remain binding; exclude that material from training, fine-tuning, distillation, evaluation and model development. Never advertise the entire reference collection as a freely usable training corpus.

## Roles across the three libraries

- Samplinglib supplies the probability, geometry, optimisation and sampling perspective.
- BanditRLlib supplies sequential feedback, information, regret and decision-theory perspectives.
- QuantumComputinglib / ASPBE supplies state/operator contracts, constructive quantum semantics, circuit certificates and resource perspectives.

Cross-library connections are proposed mechanisms until compatible imports or independently compiled adapters establish them. Shared publicity does not create shared formal truth.
