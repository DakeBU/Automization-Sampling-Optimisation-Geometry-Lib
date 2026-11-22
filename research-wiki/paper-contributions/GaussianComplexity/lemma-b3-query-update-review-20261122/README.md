# Adaptive Gaussian queries and their residual Haar laws

For a block represented by $O=R\,\mathrm{diag}(I_r,W)D^\top$, the Lean proofs compute the response to an actual ambient vector $v$ under either $O$ or $O^\top$. They give the conditional law of **all** updated residual blocks and iterate that law for policies which keep track of the current residual dimensions. These are steps in the proofs of Lemmas B.3 and B.4 of Zhou and Suzuki. [On Complexity of Gaussian Sampling, Appendix B](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem3)

## What one query reveals

Read $v$ in its input frame and call its residual part $c$. When $c=0$, the answer is already determined and all residual matrices keep their values. When $c\ne0$, write $u=c/\|c\|$. In the forward case the response reveals $z=Wu$. In the inverse case it reveals $z=W^\top u$. Encoding $z$ gives the exact ambient answer, and decoding that answer recovers $z$.

Choose the same Borel oriented completion $Q$ for both signs, as in Lemma B.2. In the forward case the new residual is the lower block of $Q_z^\top W Q_u$. In the inverse case it is the transpose of the lower block of $Q_z^\top W^\top Q_u$, and the updated domain and range frames swap the roles of $Q_u$ and $Q_z$. Both frame updates reconstruct the original ambient matrix for every draw. [B.2 completion and conditional law](../lemma-b2-review-20261119/README.md) · [Frame reconstruction](B3FrameExtraction.lean)

The joint law of the unit observation and the new labeled residual tuple is the sphere probability times the product of the updated component Haar measures. Only the queried block loses a dimension. For an ambient response, push the sphere probability through the history-dependent response map. Its kernel is common to both determinant signs. The cap $2T<N$ supplies at least two residual coordinates before each available query, and the rank update preserves $r_j\leq\ell_j\leq 2T$. [Ambient response law](B3PrimitiveQuery.lean) · [Branch selection and rank bounds](B3PrimitiveChart.lean)

## What can be iterated

A dimension profile $d$ specifies a product of groups $O(d_j)$. Attaching $d$ to its tuple puts all such products in a single measurable space. A history can select the block, dimension profile and update rule from a countable family. The informative, determined and terminal updates each provide a response kernel. [History-selected updates](B3TaggedUpdate.lean)

For a policy in this representation, `TaggedQueryPolicy.Fits` says its initial dimensions agree with the input dimensions and the dimensions left by each step agree with those read by the next, almost everywhere for the common history law. At every finite time the joint pushforward of the original draw has the product Haar posterior at those dimensions. The actual histories of the policy have equal laws for the two determinant signs. [Finite-time posterior and transcript theorems](B3TaggedInduction.lean)

The remaining source-level work is to construct such a policy from every deterministic capped primitive-query algorithm, carry the frames and counts from its actual transcript, and identify its stopped and padded transcript with the chart run. The complete source Lemmas B.3 and B.4 and the two main lower bounds remain open. This directory is a review snapshot.

## Replay

Use the project's pinned Lean and Mathlib from the repository root. The first loop builds the reviewed B.2 dependencies in a fresh directory. The second builds this snapshot, including the concrete ambient-query and inverse-transpose checks.

```sh
lake build AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar \
  AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents
proof_base=research-wiki/paper-contributions/GaussianComplexity
proof_out=$(mktemp -d)
lake env sh -c '
  set -eu
  export LEAN_PATH="$2:${LEAN_PATH:-}"
  for module in HaarStabilizerBlock HaarOrientedSection ParameterizedPushforward \
      B2MeasureCore B2JointLaw HaarConditional
  do
    lean -o "$2/$module.olean" "$1/lemma-b2-review-20261119/$module.lean"
  done
  for module in B3ResidualUpdate B3FrameUpdate B3FrameExtraction B3ProductStep \
      B3HaarProduct B3HistoryUpdate B3AdaptiveResponse B3AdaptiveQuery B3PrimitiveQuery \
      B3TaggedUpdate B3PrimitiveChart B3HistoryInduction B3TaggedInduction \
      PrimitiveWitness TransposeWitness TaggedFiniteConsumer
  do
    lean -o "$2/$module.olean" "$1/lemma-b3-query-update-review-20261122/$module.lean"
  done
' sh "$proof_base" "$proof_out"
```

The two-block example varies the query sense and actual ambient vector with the history, fixes determinant sign $-1$, and reaches a one-dimensional selected residual. The inverse regression uses a planar quarter-turn and proves that omitting the transpose changes the reconstructed matrix. [Two-block query](PrimitiveWitness.lean) · [Inverse regression](TransposeWitness.lean) · [Replay and review record](review.json)

A second example starts with two blocks of dimension three. The hemisphere of the first observation determines whether the policy makes an inverse query on the other block or records the fixed sphere point $e_0$ as padding. It verifies the dimension compatibility at every time and proves equality of the two transcript laws. [Adaptive two-block policy](TaggedFiniteConsumer.lean)
