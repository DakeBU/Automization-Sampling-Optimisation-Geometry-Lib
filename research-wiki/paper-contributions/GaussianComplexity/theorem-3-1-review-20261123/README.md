# Theorem 3.1 · Gaussian sampling query lower bound

Let $d\ge 1$, $\kappa\ge 4$, and $0<\varepsilon\le 1/16$. For centered Gaussian targets with unknown precision $I\preceq A\preceq\kappa I$, the minimum fixed query budget for sampling to total variation error $\varepsilon$ satisfies

$$
Q_G(d,\kappa,\varepsilon)\ \ge\ \frac{1}{256}
\min\!\left\{ d,\ \sqrt{\kappa}\log\!\left(1+\frac{d}{\sqrt{\kappa}\,\varepsilon}\right)\right\}.
$$

Each oracle query at $x$ returns $(x^\top Ax/2,Ax)$. The algorithm may use an independent random seed, choose queries from earlier replies, stop early, and use its last permitted reply to produce a sample. Accuracy is required on each admissible input after averaging over the algorithm's seed. $Q_G$ is the infimum of the natural query caps for which such an algorithm exists. [Zhou and Suzuki, equations (2) and (3)](https://arxiv.org/html/2610.20492v1#S3.Thmtheorem1) · [Algorithm and infimum theorems](GC31LowerBound.lean) · [Finite real-valued inequality](GC31ExactSampler.lean)

## Proof

1. **Rule out zero queries.** The returned sample at budget zero depends only on the seed. For $A=I$ and $A=\operatorname{diag}(\kappa,1,\ldots,1)$, the target probabilities of $\{|x_1|\le 1/2\}$ differ by more than $1/8$. A common output within $1/16$ of both targets would give a gap at most $1/8$. This also handles the endpoint. [Zero-query argument](GC31ZeroQuery.lean)
2. **Compare the two priors.** Set $n=2T+1$. When $n\le d$, the two determinant signs produce the same averaged algorithm output by Lemma 3.2. For each measurable event, integrate its fixed-input probability over each prior. The uniform accuracy assumption bounds the discrepancy from the common output by $\varepsilon$ on either side. The averaged target laws are therefore within $2\varepsilon$ in total variation. On those very same precision priors, the existing proof of Lemma 3.3 gives the lower bound $1-\exp[-(k/8)\exp(-10n/\sqrt\kappa)]$, where $k=\lfloor d/n\rfloor$. [Lemma 3.2](../lemma-3-2-review-20261123/README.md) · [Mixing and comparison](GC31Mixture.lean) · [Target laws and Lemma 3.3](GC33Target.lean)
3. **Convert separation to query count.** Combining the two bounds gives $k\exp(-10n/\sqrt\kappa)\le32\varepsilon$. The floor estimate $d\le 2nk$ and $n\le 3T$ give $d\le192\varepsilon T\exp(30T/\sqrt\kappa)$. Using $t\le\sinh t$ for $t\ge0$ and concavity of $\log$ yields $\sqrt\kappa\log(1+d/(\sqrt\kappa\varepsilon))\le192T$. When $2T+1>d$, integrality gives $d\le2T$. The claimed minimum follows in both cases. [Budget estimates](GC31Budget.lean)
4. **Take the infimum.** The lower bound holds for every feasible natural cap and hence for their infimum. Finiteness also has a direct witness. Querying the $d$ standard basis vectors recovers all columns of $A$. A measurable Gaussian sampler then returns the exact law $N(0,A^{-1})$ using one uniform seed. This proves $Q_G\le d$ and yields the finite real-valued form of (3). [Infimum over budgets](GC31LowerBound.lean) · [Exact sampler](GC31ExactSampler.lean)

## Checks and replay

The input-class check proves equivalence with the two positive-semidefinite inequalities in the paper. The boundary examples specialize the result at $d=1$, $\kappa=4$, $\varepsilon=1/16$, and show that at $d=513$, $\kappa=513^2$, every two-query algorithm exceeds error $1/16$ on some admissible precision. [Source-class equivalence and endpoint](GC31SourceChecks.lean) · [Algorithm examples](GC31BoundaryWitness.lean)

From the repository root, run the following command with the pinned Lean and Mathlib toolchain. The script builds the library prerequisites and recompiles the review modules in a fresh temporary directory. [Verification record](review.json)

```sh
sh research-wiki/paper-contributions/GaussianComplexity/theorem-3-1-review-20261123/replay.sh
```

This package covers the general first-order oracle of Theorem 3.1. Theorem 4.1 concerns a different experiment in which the algorithm receives the spectrum in advance.
