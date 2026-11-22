# Lemma B.4 · Transcript indistinguishability

Let $O_1,\ldots,O_k$ be independent Haar orthogonal matrices in dimension $N$, all drawn from the determinant component $b$. A deterministic Borel algorithm reads its complete history and chooses a block $j$, an ambient vector $v$, and either the forward query $O_jv$ or the inverse query $O_j^\top v$. It may also stop. If each block receives at most $2T<N$ queries, the complete transcript padded to $M=2Tk$ slots has the same law for $b=+1$ and $b=-1$. **This is Lemma B.4 of Zhou and Suzuki.** [Paper statement](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem4) · [Lean theorem](B4Transcript.lean)

The theorem `padded_transcript_indistinguishability` starts from the empty history and evaluates the algorithm on the actual matrix tuple. An active slot records the block label, input vector, query direction and returned ambient vector. A separate symbol fills every slot after stopping. The public theorem accepts a per-block bound that holds almost surely on the actual run under each sign. The fixed-length formulation gives equality on the ordinary product space of all $M$ records. [Primitive oracle and recording rule](B4Protocol.lean) · [Measurable history space](B4HistorySpace.lean) · [Fixed-length theorem](B4TimeCoordinates.lean)

## Proof

Fix a public history and the remaining query budget. Represent each original block in fixed domain and range frames, with a residual orthogonal matrix of dimension $d_j$. Maintain the strict inequality between the remaining budget of block $j$ and $d_j$. It holds initially because $2T<N$. A query on a label with positive budget therefore has at least two residual coordinates to work with.

In a queried block, expose the image $z$ of a unit residual direction, using the transpose in the inverse case. Under either sign the law of $z$ is the same uniform sphere probability. Given $z$ and a fresh, one-dimension-smaller residual of the specified sign, the reconstruction recovers the correct distribution of the **entire original tuple**. For every value of the fresh tuple it preserves every ambient matrix and gives the true query answer. When the query has zero residual component, an auxiliary unit direction can still be exposed. The returned answer is then constant in $z$, and the algorithm sees only its actual answer. [Resampling law](B4Resample.lean) · [One-block reconstruction](B4Frames.lean) · [All labeled blocks](B4FramedTuple.lean)

Induct backwards on the length of the remaining transcript. At a fixed $z$, the next recorded slot, ambient frames and remaining budgets are common to both signs, so induction gives equality for the suffix. Integrating over the common law of $z$ proves equality for the full continuation. Terminal continuations consist entirely of padding. A temporary budget check in the induction agrees pathwise with the original oracle whenever its actual counts satisfy the cap. The proof keeps the same original matrices through the entire adaptive run. [Mixture identity](B4Mixture.lean) · [Backward induction and removal of the budget check](B4Transcript.lean) · [Padding after the total cap](ProtocolHorizon.lean)

## Independent example

With two three-dimensional blocks and $T=1$, the algorithm sends the first coordinate vector to block 0. If the first coordinate of its answer is positive, the algorithm sends that **answer vector** to the transpose of block 1. Otherwise it stops. The example checks both exact four-slot transcripts, including padding, proves its own per-block cap, and applies the public theorem. [Verified two-block example](B4RawWitness.lean)

## Replay

From the repository root, use the pinned Lean 4.33.0 toolchain and Mathlib manifest. The following commands compile only the necessary B.2 and B.3 review dependencies, then the B.4 proof and its checks, into a fresh directory.

```sh
lake build AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar \
  AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents
proof_base=research-wiki/paper-contributions/GaussianComplexity
proof_out=$(mktemp -d)
lake env sh -c '
  set -eu
  export LEAN_PATH="$2:${LEAN_PATH:-}"
  build_review() {
    folder=$1
    shift
    for name do
      lean -o "$proof_out/$name.olean" "$proof_base/$folder/$name.lean"
    done
  }
  proof_base=$1
  proof_out=$2
  build_review lemma-b2-review-20261119 HaarStabilizerBlock HaarOrientedSection \
    ParameterizedPushforward B2MeasureCore B2JointLaw
  build_review lemma-b3-query-update-review-20261122 B3ProductStep B3ResidualUpdate \
    B3HaarProduct B3HistoryUpdate B3AdaptiveResponse B3AdaptiveQuery B3FrameUpdate B3PrimitiveQuery
  build_review lemma-b4-review-20261122 B4Mixture B4Frames B4Resample B4Protocol \
    B4FramedTuple B4Transcript B4HistorySpace B4TimeCoordinates ProtocolHorizon B4RawWitness
' sh "$proof_base" "$proof_out"
```

This review snapshot establishes the transcript law. Lemma B.3's full conditional factorization with history-measurable frames, the randomized first-order reduction and the main lower bounds remain separate work. [Verification record](review.json)
