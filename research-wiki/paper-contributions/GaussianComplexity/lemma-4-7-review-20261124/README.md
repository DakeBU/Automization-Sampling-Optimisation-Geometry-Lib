# The dimension of the random Krylov space

Lemma 4.7 of Zhou and Suzuki gives the exact dimension of the span used in the hidden-eigenbasis argument. For $q+1$ independent $N(0,I_d)$ vectors $g_a$ and the midpoint-grid diagonal precision $\Lambda$, let
$$
\mathcal K_q=\operatorname{span}\{\Lambda^j g_a: 1\le a\le q+1,\ 0\le j\le q\}.
$$
Then $\dim\mathcal K_q=\min\{d,(q+1)^2\}$ almost surely, for every natural $q$. The proof works on any probability space carrying the specified independent starts. The paper assumes $d\ge2$ and $\kappa\ge2$. The Lean statement allows all natural dimensions and every $\kappa\ne1$, which keeps the grid eigenvalues distinct. At $\kappa=1$ the precision is the identity and its powers repeat each start. [Paper, Lemma 4.7](https://arxiv.org/html/2610.20492v1#S4.Thmtheorem7) · [Dimension theorem](GC47Dimension.lean) · [Grid and rank](GC47Rank.lean)

## Why the maximal rank is attained

Write $r=q+1$ and $s=\min\{d,r^2\}$. The matrix of generators has row $i$, column $(a,j)$ equal to $\lambda_i^j g_a(i)$, with $a,j$ indexed from zero. Choose the deterministic starts $g_a(i)=\lambda_i^{ra}$. The first $s$ rows and the columns with $ra+j=0,\ldots,s-1$ give a Vandermonde matrix on distinct eigenvalues. Its determinant is nonzero. [Explicit minor](GC47Witness.lean) · [Polynomial in the starts](GC47MinorPolynomial.lean)

That same determinant is a nonzero polynomial in the Gaussian coordinates. Its zero set has probability zero. The formal proof uses induction on the number of scalar coordinates. Almost every choice of the other coordinates leaves a nonzero univariate polynomial, whose finite root set has measure zero. The law of the coordinates of the independent Gaussian vectors is exactly the required product law. [Gaussian zero-set proof](GC47GaussianZero.lean)

## Consequence for the cosine test

When $r^2\ge d$, the span is the entire space almost surely. If $n=2q+1<d$ as well, the midpoint grid has mean squared cosine $1/2$ at frequency $n$. A single fixed unit coordinate vector therefore belongs to the span almost surely and satisfies
$$
 |u^\top D_n u|\ge 1/\sqrt{2},\qquad D_n=\operatorname{diag}(\cos(n\theta_i)).
$$
This prevents a uniform upper bound of $1/2$ for this statistic in the saturated regime. [Section 4.4](https://arxiv.org/html/2610.20492v1#S4.SS4) · [Coordinate bound](GC47Coordinate.lean) · [Almost-sure obstruction](GC47Limitation.lean)

## Simultaneous Gram concentration

Appendix C.2, Fact C.6 gives both Gram bounds on a single event of probability at least $199/200$. With the same constant $C=2048$ in the paper's threshold, the result holds throughout $2q+1<d$, including thresholds larger than $1/2$. The proof uses the degree-$2q$ reproducing cosine projection when $4q+1<d$. In the remaining dimensions, the identity matrix on the grid reproduces every row and satisfies the same coefficient bounds. The weighted Gaussian estimate then applies in both cases. [Paper, Fact C.6](https://arxiv.org/html/2610.20492v1#A3.Thmtheorem6) · [Full probability bound](GC47FullGram.lean)

## Verification

The examples check the dimension for $q=2$ in $d=8,9,10$, the one-dimensional span of a single Gaussian start in $d=7$, the repeated-eigenvalue case, and the Gram bound at $d=4,q=1$, where $\tau>1/2$. [Dimension examples](GC47Boundary.lean) · [Degenerate spectra](GC47RankBoundary.lean) · [Gram example](GC47GramBoundary.lean) · [Sources and hashes](review.json)

Run the following command at the repository root to check the source hashes and compile the proof and its review dependencies into an empty directory using the pinned Lean and Mathlib versions.

```sh
python3 research-wiki/paper-contributions/GaussianComplexity/lemma-4-7-review-20261124/replay.py
```
