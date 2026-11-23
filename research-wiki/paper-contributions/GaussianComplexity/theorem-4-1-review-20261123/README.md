# Theorem 4.1 · Gaussian sampling with a disclosed spectrum

Fix $0<\delta<1$. For all sufficiently large $d$, for every $2\le\kappa\le d^{1-\delta}$ and $0<\varepsilon\le1/10$, the worst-case first-order query complexity of centered Gaussian sampling satisfies

$$
Q_G(d,\kappa,\varepsilon)\ \ge\ \frac{\delta}{256}\sqrt{\kappa}\log d.
$$

The same lower bound holds when the algorithm receives the full spectrum with multiplicities before its first query. A single dimension cutoff works for the entire stated range of condition numbers and accuracies. [Paper, Theorem 4.1](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem1) · [Lean theorems](GC41LowerBound.lean)

## Oracle and accuracy

An admissible precision satisfies $I\preceq A\preceq\kappa I$ and $A=A^\top$. At $x$ the oracle returns $(x^\top A x/2,Ax)$. The algorithm may choose each query, stop early and return an arbitrary measurable output using its independent seed and all previous answers. A feasible natural budget caps every run. Accuracy at each input compares the seed-averaged output law to $N(0,A^{-1})$ in total variation. In the disclosure model, the entire algorithm may be selected as a function of the characteristic polynomial. For a real symmetric matrix this determines every eigenvalue with its multiplicity. Both variants have a finite upper bound of $d$ from exact column queries. [Disclosed budget definition](GC41Budget.lean) · [Minimax and finite bounds](GC41Minimax.lean) · [Exact sampler](../theorem-3-1-review-20261123/GC31ExactSampler.lean)

## The hidden-eigenbasis experiment

The hard precision is $A=O\Lambda O^\top$ for full Haar $O$. The diagonal $\Lambda$ has the deterministic midpoint-cosine spectrum of equation (11). Thus the disclosed polynomial is the same throughout the hard family. For $2q+1\le d$, an extension preserves the joint law of the true orientation and the actual returned point $X$. This includes the endpoint $2q+1=d$ as well as the paper’s range $2q+1<d$. On that extension there are $q+1$ independent standard Gaussian starts such that $O^\top X$ belongs almost surely to the span of $\Lambda^j g_a$ for $0\le j\le q$. The last start accounts for an output outside the span of the observed query points. The construction follows each inverse and forward revelation of the same rotation, preserving the Haar law on the unrevealed complement. [Paper, Appendix C.1](https://arxiv.org/html/2610.20492v1#A3.SS1) · [Joint representation](GC43Representation.lean) · [Actual first-order path](GC43ActualPath.lean)

For $n=2q+1$, the test accepts when

$$
(-1)^n x^\top T_n\left(\frac{2A-(\kappa+1)I}{\kappa-1}\right)x>2\tau\|x\|^2.
$$

For every hidden orientation, an exact target sample passes with probability at least $9/10$ throughout the query range used by the proof. Under the hard input prior the algorithm passes with probability at most $1/100$, because the uniform Krylov estimate controls every vector in the random span at once. Uniform per-input accuracy bounds the difference on this same event by $\varepsilon$ after averaging, while the two probability estimates give a difference of at least $89/100$. This excludes the proposed low budget. [Target estimate](../fixed-spectrum-target-power-review-20261123/GC41Power.lean) · [Uniform Krylov estimate](../lemma-4-4-review-20261123/GC44Uniform.lean) · [Per-input TV comparison](GC41Risk.lean)

## Boundary checks

At $d=3$ and $q=1$, a randomized example either stops at its seed point or returns the gradient it receives there. The extension preserves the joint law of the rotation and this explicit output, and supplies two independent Gaussian starts. A second check sets $\delta=1/2$, $\kappa=\sqrt d$ and $\varepsilon=1/10$. It obtains $d^{1/4}\log(d)/512$ as an eventual lower bound for both finite real query complexities. [Independent checks](GC41EndpointAudit.lean)

## Verification

Run the following command from the repository root. It verifies source hashes, builds the pinned library prerequisites and compiles the transitive review modules in a fresh directory with warnings treated as errors. [Verification record](review.json)

```sh
python3 research-wiki/paper-contributions/GaussianComplexity/theorem-4-1-review-20261123/replay.py
```
