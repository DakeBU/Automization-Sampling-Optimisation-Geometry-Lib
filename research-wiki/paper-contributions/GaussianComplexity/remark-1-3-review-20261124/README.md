# Remark 1.3 · Sampling with a known minimizer

The Gaussian query lower bounds in Theorems 3.1 and 4.1 also hold for sampling from general twice continuously differentiable potentials $V$ satisfying $I\preceq\nabla^2 V\preceq\kappa I$, even when the algorithm learns the global minimizer before the first query. Each oracle call at $x$ returns $(V(x),\nabla V(x))$. The target measure has Lebesgue density $e^{-V(x)}/\int e^{-V}$. Accuracy is measured in total variation for every input, with a deterministic cap on the number of queries and an independent random seed. [Paper, Remark 1.3](https://arxiv.org/html/2610.20492v1#S1.Thmtheorem3) · [Model and lower bounds](GC13KnownMinimum.lean)

## Reduction

The algorithm can depend arbitrarily on the disclosed minimizer. On every centered quadratic $V_A(x)=\langle x,Ax\rangle/2$ the unique minimizer is zero, so one fixed member of that algorithm family must work for every admissible precision $A$. Its gradient is $Ax$ and its Hessian is the constant map $A$. Thus it receives the exact replies of the Gaussian value-and-gradient oracle on each adaptive run. The normalized target for that same potential is exactly $N(0,A^{-1})$. Both the budget and per-input error therefore transfer to the Gaussian model. [Quadratic geometry and oracle replies](GC13Geometry.lean) · [Gaussian–Gibbs identity](GC13Gibbs.lean)

For all potentials in the class, the lower Hessian bound and existence of a minimizer ensure the partition function is positive and finite. The output of every fixed-budget measurable algorithm is also a probability measure. [Normalization](GC13Normalizable.lean) · [Output law](GC13Output.lean)

## Consequences

For $d\ge 1$, $\kappa\ge4$ and $0<\varepsilon\le 1/16$, the known-minimizer query complexity is at least
$$
\frac{1}{256}\min\!\left\{d,\sqrt\kappa\log\!\left(1+\frac{d}{\sqrt\kappa\,\varepsilon}\right)\right\}.
$$
For every fixed $0<\delta<1$, all sufficiently large $d$, all $2\le\kappa\le d^{1-\delta}$, and $0<\varepsilon\le1/10$, it is at least $(\delta/256)\sqrt\kappa\log d$. The same bounds apply to algorithms that ignore the minimizer. [Gaussian Theorem 3.1](../theorem-3-1-review-20261123/GC31LowerBound.lean) · [Gaussian Theorem 4.1](../theorem-4-1-review-20261123/GC41LowerBound.lean)

At $\kappa=2$ and $\varepsilon=1/10$, every feasible natural query budget is eventually at least $(\sqrt{2}/512)\log d$. At $d=1$, $\kappa=4$ and $\varepsilon=1/16$, at least one query is required. [Logarithmic endpoint](GC13SourceChecks.lean) · [One-dimensional endpoint](GC13Output.lean)

## Verification

Run the following command at the repository root. It checks all source hashes, builds the pinned prerequisites and recompiles the review modules in dependency order in an empty directory. [Verification record](review.json)

```sh
python3 research-wiki/paper-contributions/GaussianComplexity/remark-1-3-review-20261124/replay.py
```
