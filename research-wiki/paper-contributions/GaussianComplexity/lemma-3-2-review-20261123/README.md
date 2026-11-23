# Lemma 3.2 · Indistinguishability of randomized first-order outputs

For the Gaussian hard family of Zhou and Suzuki, every randomized first-order sampling algorithm with query budget $2T<n$ has the same averaged output law under the two determinant signs. The equality concerns the returned sample in $\mathbb R^d$, after averaging over both the hidden precision matrix and the algorithm's independent randomness. [Paper, Lemma 3.2 and equation (7)](https://arxiv.org/html/2610.20492v1#S3.Thmtheorem2) · [Lean theorem](GC32Indistinguishability.lean)

Fix $\kappa\ge4$ and $3\le n\le d$. Draw $k=\lfloor d/n\rfloor$ independent matrices from Haar probability on $O(n)$ conditioned on determinant $b$. Each contributes a precision block $A_O=(\kappa+1)I/2-(\kappa-1)(O+O^\top)/4$. The last $d-kn$ coordinates have identity precision. Write $\mathcal D_b$ for the resulting law on precision matrices, and $\rho_A$ for the law of the returned sample when the precision is fixed to $A$. The public theorem `averaged_first_order_indistinguishability` proves

$$\int \rho_A\,\mathcal D_{+1}(dA)=\int \rho_A\,\mathcal D_{-1}(dA).$$

In Lean these integrals are `Measure.bind`. The algorithm can store the seed and every previous query and reply in its state. Its measurable rule either stops or chooses the next point. It may read its output after an early stop or after the last permitted answer. The constructor `Algorithm.ofHistory` gives this representation directly for complete-history rules. [Algorithm, fixed-input sample and output law](GC32Algorithm.lean)

## Proof

1. At a query point $x$, send the coordinates of $x$ in each full block to both $O_j$ and $O_j^\top$. The known affine combination reconstructs the complete gradient $Ax$, including the original coordinates in the identity tail. The value is $\langle x,Ax\rangle/2$. This recovers the genuine first-order reply for every hidden tuple and every $x$. [Batch and Euclidean gradient](GC32Decoder.lean)
2. Run those primitive queries in a fixed order within each batch. The next first-order query may depend on all earlier replies. From the chronological primitive record and the initial state, the algorithm recovers its actual final state, including the response that used the last unit of budget. Every executed first-order query costs exactly two queries per block, giving the pathwise bound $2T$. [Execution from the record](GC32Replay.lean) · [Batch simulation and counts](GC32Batch.lean)
3. At fixed seed, Lemma B.4 gives equality of the padded primitive transcript laws. Integrate over the common seed law while retaining the seed in the record. The returned sample is a measurable function of this pair, so its law agrees as well. [Lemma B.4](../lemma-b4-review-20261122/README.md) · [Seed and output](SeededTranscript.lean)
4. Push the product Haar prior through the actual precision construction. Averaging the fixed-precision output law gives the same measure as drawing an independent seed and hidden matrix tuple and running the algorithm. This identifies the two sides with equation (7). [Averaging identity](AveragedOutput.lean)

## Checks

The randomized example takes $n=5$, $d=11$, and $T=2$. A fair bit selects early stopping after one query or a second query whose point depends on both the first function value and the first gradient. The initial vector has a nonzero coordinate in the identity tail. The example proves the exact returned vector on each path and applies the theorem to the two averaged output laws. Separate decoder checks cover a nonempty identity tail and an exact block tiling. [Randomized adaptive example](GC32AdaptiveWitness.lean) · [Decoder checks](DecoderConsumer.lean) · [Verification record](review.json)

## Replay

Run these commands at the repository root with its pinned Lean and Mathlib versions. All review modules are compiled into a fresh directory.

```sh
lake build AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar \
  AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents \
  AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery \
  AutoSamplingTheory.TechnicalLemmas.Analysis.BatchedOracleSimulation
proof_base=research-wiki/paper-contributions/GaussianComplexity
proof_out=$(mktemp -d)
lake env sh -c '
  set -eu
  proof_base=$1
  proof_out=$2
  export LEAN_PATH="$proof_out:${LEAN_PATH:-}"
  build_review() {
    folder=$1
    shift
    for name do
      lean -o "$proof_out/$name.olean" "$proof_base/$folder/$name.lean"
    done
  }
  build_review lemma-b2-review-20261119 HaarStabilizerBlock HaarOrientedSection \
    ParameterizedPushforward B2MeasureCore B2JointLaw
  build_review lemma-b3-query-update-review-20261122 B3ProductStep B3ResidualUpdate \
    B3HaarProduct B3HistoryUpdate B3AdaptiveResponse B3AdaptiveQuery B3FrameUpdate B3PrimitiveQuery
  build_review lemma-b4-review-20261122 B4Mixture B4Frames B4Resample B4Protocol \
    B4FramedTuple B4Transcript B4HistorySpace
  build_review lemma-3-2-review-20261123 AveragedOutput SeededTranscript GC32Replay \
    GC32Batch GC32Decoder GC32Algorithm GC32Indistinguishability DecoderConsumer GC32AdaptiveWitness
' sh "$proof_base" "$proof_out"
```

This review snapshot proves Lemma 3.2 for the original first-order oracle. Integrating the output-law equality with the target separation and the quantitative parameter choices in the main lower bound remains separate work.
