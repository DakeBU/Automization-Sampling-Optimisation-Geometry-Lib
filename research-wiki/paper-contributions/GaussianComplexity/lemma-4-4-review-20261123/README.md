# Lemma 4.4 · Uniform cosine bound on a Gaussian Krylov space

For any experiment carrying $q+1$ independent standard Gaussian vectors $g_a\in\mathbb R^d$, one event of probability at least $0.99$ controls the cosine quadratic form for **every** vector in their block Krylov space. Thus the coefficients of a tested vector may depend on all of the Gaussian draws. [Paper, Lemma 4.4](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem4) · [Lean theorem](GC44Uniform.lean)

## Quantifiers and constants

Let $q\ge0$, $2q+1<d$, and $\kappa\ge2$. Use the midpoint angles $\theta_i=(i-\tfrac12)\pi/d$ and the diagonal precision $\Lambda$ with entries $(\kappa+1)/2+(\kappa-1)\cos(\theta_i)/2$. Set $n=2q+1$ and $D_n=\operatorname{diag}(\cos(n\theta_i))$. The proof gives the absolute constant $C=2048$ in the paper's threshold

$$
\tau=C\left[(q+1)\sqrt{\frac{\log d}{d}}+
\frac{(q+1)(q+1+\log d)\log d}{d}\right].
$$

When $\tau\le1/2$, the simultaneous conclusion is

$$
|u^\top D_nu|\le 2\tau\|u\|^2
\qquad\text{for all }u\in\operatorname{span}\{\Lambda^j g_a:1\le a\le q+1,\ 0\le j\le q\}.
$$

The theorem covers starts specified by their joint product law and starts given as independent measurable maps on another probability space. The underlying measurable event controlling both Gram operators has probability at least $199/200$. [Uniform estimate and transfer to arbitrary starts](GC44Uniform.lean) · [Gram bounds and Krylov membership](GC44GramUse.lean)

## Proof

Write $u=Bc$ in the discrete cosine basis. The degree-$2q$ cosine projection reproduces every product of two basis functions of degree at most $q$. This expresses both $B^\top B-I$ and $B^\top D_nB$ in terms of smaller symmetric matrices indexed by the cosine grid. The row estimates for the projection control both the maximum absolute coefficient and the sum of squared coefficients. [Projection](GC44Projection.lean) · [Quadratic forms](GC44Symbol.lean) · [Gram identities](GC44Compression.lean)

For a fixed unit vector, each small matrix contributes a weighted sum of independent centered Gaussian squares. A scalar moment-generating-function bound controls both tails. A union bound covers the two weight families, all grid locations and a $1/4$-net of the unit sphere in $\mathbb R^{q+1}$. The net has at most $(32r+1)^r$ elements for $r=q+1$. The symmetric quadratic-form bound on this net gives an operator-norm bound with factor two. [Weighted Gaussian squares](GC44WeightedChiSquare.lean) · [Finite sphere net](GC44Net.lean) · [Simultaneous estimates](GC44Concentration.lean)

Applying this lemma to an adaptive algorithm's returned sample also requires the joint-law-preserving Krylov representation from Lemma 4.3. [Paper, Lemma 4.3](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem3)

## Verification

At $\kappa=2$ and $\delta=1/2$, every fixed query index $q$ satisfies the mode and threshold conditions in all sufficiently large dimensions. An independent example derives these conditions and checks the $0.99$ conclusion for arbitrary experiments carrying the prescribed Gaussian starts. [Boundary example](GC44BoundaryWitness.lean) · [Source hashes and verification record](review.json)

Run the following command from the repository root to check the hashes, build library prerequisites and compile all 13 review modules in a fresh directory with warnings treated as errors.

```sh
python3 research-wiki/paper-contributions/GaussianComplexity/lemma-4-4-review-20261123/replay.py
```
