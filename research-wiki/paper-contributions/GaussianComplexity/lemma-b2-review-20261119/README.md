# Gaussian Complexity — Lemma B.2

`HaarConditional.lean` proves the spherical marginal and regular conditional
law for a single forward or transpose observation. One Borel choice of
oriented completion works for both determinant signs and every fixed unit
vector. The ambient dimension is $m=n+2$, so the residual dimension
$m-1=1$ is covered at the lower endpoint. [On Complexity of Gaussian
Sampling, Lemma B.2](https://arxiv.org/html/2610.20492v1#A2.Thmtheorem2)

Let $\sigma$ be the normalized Euclidean sphere measure, and let
$\mu_{k,b}$ be twice the restriction of full Haar probability on $O(k)$
to determinant $b\in\{-1,1\}$. Choose $Q_z$ Borel with
$Q_z e_0=z$ and $\det Q_z=1$. The conditional kernel at $z$ is the
pushforward of $\mu_{m-1,b}$ by
$V\mapsto Q_z\operatorname{diag}(1,V)Q_u^\top$. Both observed joint laws
equal the composition product of $\sigma$ and this Markov kernel. The
kernel is a chosen regular conditional version and assigns probability
one to the observation fiber at every $z$.

The construction first uses full Haar in the residual dimension.
The orthogonal cocycle fixes $e_0$, so its residual block translates the
residual Haar law while the first coordinate rotates the sphere law.
Skew-product invariance and uniqueness of full Haar give the full group
law. The determinant identity then transports the restriction to sign
$b$ through the product. Inversion preserves that restriction and
supplies the transpose experiment.

| File | Proof ingredient |
| --- | --- |
| [HaarOrientedSection.lean](HaarOrientedSection.lean) | Borel oriented completion of every sphere point |
| [HaarStabilizerBlock.lean](HaarStabilizerBlock.lean) | Stabilizer block decomposition, continuity, and determinant |
| [B2MeasureCore.lean](B2MeasureCore.lean) | Normalized measures, spherical rotation, and Haar transport |
| [B2JointLaw.lean](B2JointLaw.lean) | Assembly and both determinant-conditioned joint laws |
| [ParameterizedPushforward.lean](ParameterizedPushforward.lean) | Parameterized pushforward kernel and composition product |
| [HaarConditional.lean](HaarConditional.lean) | Full source-sized conditional law and marginals |

## Replay

Use the repository's pinned Lean 4.33.0 and Mathlib manifest. Build the
ordinary imports and compile the review modules from the repository root.

```sh
lake build AutoSamplingTheory.TechnicalLemmas.Probability.SphereHaar \
  AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantComponents
proof_dir=research-wiki/paper-contributions/GaussianComplexity/lemma-b2-review-20261119
proof_out=$(mktemp -d)
lake env sh -c '
  set -eu
  proof_dir=$1
  proof_out=$2
  export LEAN_PATH="$proof_out:${LEAN_PATH:-}"
  for module in HaarStabilizerBlock HaarOrientedSection ParameterizedPushforward \
      B2MeasureCore B2JointLaw HaarConditional
  do
    lean -o "$proof_out/$module.olean" "$proof_dir/$module.lean"
  done
' sh "$proof_dir" "$proof_out"
```

This is a review snapshot. Repository admission and the adaptive posterior
factorization of Lemma B.3 are separate remaining work.
