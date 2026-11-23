#!/bin/sh
set -eu

# Run from any directory in a checkout that has its pinned Lake dependencies.
package=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
base=$(dirname "$package")
cd "$package/../../../.."
lake build AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar \
  AutoSamplingTheory.TechnicalLemmas.Analysis.BatchedOracleSimulation \
  AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents \
  AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery \
  AutoSamplingTheory.ExampleCases.GaussianComplexity.TVAmplification \
  AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation \
  Mathlib.Probability.Kernel.Representation Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp Mathlib.Tactic

proof_out=$(mktemp -d)
trap 'rm -rf -- "$proof_out"' EXIT
lake env sh -eu -c '
  proof_out=$1
  base=$2
  package=$3
  export LEAN_PATH="$proof_out:${LEAN_PATH:-}"
  compile() {
    folder=$1
    shift
    for name do
      printf "Checking %s\n" "$name"
      lean -DwarningAsError=true -o "$proof_out/$name.olean" "$folder/$name.lean"
    done
  }
  compile "$base/lemma-b2-review-20261119" HaarStabilizerBlock HaarOrientedSection \
    ParameterizedPushforward B2MeasureCore B2JointLaw
  compile "$base/lemma-b3-query-update-review-20261122" B3ProductStep B3ResidualUpdate \
    B3HaarProduct B3HistoryUpdate B3AdaptiveResponse B3AdaptiveQuery B3FrameUpdate B3PrimitiveQuery
  compile "$base/lemma-b4-review-20261122" B4Mixture B4Frames B4Resample B4Protocol \
    B4FramedTuple B4Transcript B4HistorySpace
  compile "$base/lemma-3-2-review-20261123" AveragedOutput SeededTranscript GC32Replay \
    GC32Batch GC32Decoder GC32Algorithm GC32Indistinguishability
  compile "$package" GC33Target GC31Mixture GC31ZeroQuery GC31Budget GC31LowerBound \
    GC31BoundaryWitness GC31SourceChecks GC31ExactSampler
' sh "$proof_out" "$base" "$package"
