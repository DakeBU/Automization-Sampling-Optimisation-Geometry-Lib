# Hidden eigenbasis · Target test and a zero-query lower bound

For the cosine-grid precision family in Section 4 of Zhou and Suzuki, an exact target sample passes the paper's strict test with probability at least $9/10$ for **every** orientation of the eigenbasis. This holds throughout the dimension, condition-number and query-index range used in the proof of Theorem 4.1. [Paper, Section 4.3](https://arxiv.org/html/2610.20492v1#S4.SS3) · [Lean theorem](GC41Power.lean)

## The test

Fix $C>0$ and $0<\delta<1$. A single cutoff $d_0(C,\delta)$ works for every $d\ge d_0$, $2\le\kappa\le d^{1-\delta}$, and natural index $q\le (\delta/256)\sqrt\kappa\log d$. Put $n=2q+1$ and use the threshold

$$
\tau=C\left[(q+1)\sqrt{\frac{\log d}{d}}
 +\frac{(q+1)(q+1+\log d)\log d}{d}\right].
$$

The precision is $A=O\Lambda O^\top$, where $\Lambda$ has the midpoint cosine-grid eigenvalues from equation (11). With $T_n$ the first-kind Chebyshev polynomial, a point $x$ passes if

$$
(-1)^n x^\top T_n\!\left(\frac{2A-(\kappa+1)I}{\kappa-1}\right)x
>2\tau\|x\|^2.
$$

The statistic is jointly continuous in $A$ and $x$. Rotating a draw from the diagonal Gaussian gives the exact $N(0,A^{-1})$ law, preserves the norm, and sends the intrinsic event to its diagonal cosine form. In diagonal coordinates the two quadratics share the same draw. The covariance bound and Chebyshev's inequality give probability at most $1/10$ for the complementary event, including equality at the threshold. [Rotation and measurable event](GC41Target.lean) · [Uniform cutoff and probability estimate](GC41Asymptotic.lean)

## What this implies at zero queries

Use the grid in its original order for $A$ and in reverse order for $B$. Reversal replaces each grid angle $\theta$ by $\pi-\theta$, negating the cosine detector at every odd mode. The two strict passing events are disjoint. For the first mode, the same event has probability at least $9/10$ under $N(0,A^{-1})$ and at most $1/10$ under $N(0,B^{-1})$. Thus the target laws have total variation distance at least $4/5$. [Odd-mode reversal](GC41Reversal.lean) · [Event probability to total variation](GC41TwoPoint.lean)

Both inputs have the same characteristic polynomial, with every disclosed grid eigenvalue and its multiplicity. Any zero-query algorithm can use that polynomial and an independent random seed, giving a common output law on the two inputs. For every fixed $0<\delta<1$, all sufficiently large $d$, and $2\le\kappa\le d^{1-\delta}$, its total variation error on at least one of these explicit inputs is at least $2/5$. This two-input argument is a corollary of the target estimate. The full lower bound in Theorem 4.1 also requires control of the output of algorithms making positive numbers of adaptive queries. [Known-spectrum lower bound](GC41KnownSpectrum.lean)

## Verification

An independent example takes $\kappa=2$ and $\delta=1/2$. For every fixed nonnegative $q$ and all sufficiently large dimensions, a single strict test has false-negative and false-positive probabilities each at most $1/10$ for the two orientations. Here $q$ indexes the test frequency. [Classifier example](GC41ClassifierWitness.lean) · [Verification record](review.json)

Run the following command from the repository root. It checks the source hashes, builds the pinned library prerequisites and recompiles all review modules into a fresh directory.

```sh
python3 research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-target-power-review-20261123/replay.py
```
