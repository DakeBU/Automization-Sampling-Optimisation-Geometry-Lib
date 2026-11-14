# Exact read-range text views (math uses the pinned HTML alttext)

These views are for readability; raw-fragments.json binds the exact source bytes.

## S4.SS1

4.1 The Hard Family



We use a construction similar to that in [22, Section 9.2],
with a cosine eigenvalue grid (Chebyshev nodes) and a random orthogonal rotation, while extending the spectral
interval from $[1,2]$ to $[1,\kappa]$.
For $d\geq 2$ and $\kappa\geq 2$, define


$\theta_{i}=\frac{(i-\tfrac{1}{2})\pi}{d},\qquad\lambda_{i}=\frac{\kappa+1}{2}+\frac{\kappa-1}{2}\cos\theta_{i},\qquad\Lambda=\operatorname{diag}(\lambda_{1},\ldots,\lambda_{d}).$

(11)


Draw $O\sim\operatorname{Haar}(\mathrm{O}(d))$, independently
of the algorithm’s private randomness, and set $A=O\Lambda O^{\top}$.
The associated potential and target are
$f_{A}(x)=x^{\top}Ax/2$ and $\pi_{A}=N(0,A^{-1})$.


The spectrum is deterministic and may be supplied to the algorithm.
In particular, the Gaussian normalizing constant is known.
The unknown component is the random eigenbasis represented by $O$.


Remark 4.2 (Comparison with $\kappa=2$ case).


At $\kappa=2$, the spectrum in
Eq. (11) recovers the original construction in [22].
More generally, if $A_{2}$ denotes the original precision matrix
with the same rotation $O$, then
$A=(\kappa-1)A_{2}-(\kappa-2)I_{d}$.
Thus one matrix–vector reply for either matrix determines
the corresponding reply for the other.
The proof compares $\sum_{i}\cos(n\theta_{i})\langle x,Oe_{i}\rangle^{2}$ with $\|x\|^{2}$, where $n=2q+1$.
For the output of a $q$-query algorithm, the ratio is at most $d^{-\Omega(1)}$ in absolute value
(Lemma 4.4), whereas under the target the ratio of the means has absolute value
$e^{-\Theta(n/\sqrt{\kappa})}$ (Lemma 4.5).
Hence the test works for $n$ up to order $\sqrt{\kappa}\log d$, rather than $\log d$ as at
$\kappa=2$, which is the source of the factor $\sqrt{\kappa}$ in
Theorem 4.1.

## S4.SS2.SSS0.Px3

Target moments.



We now evaluate the same cosine statistic under the target Gaussian.


Lemma 4.5 (Moments under the target).


Let $\kappa\geq 2$, $U\sim N(0,\Lambda^{-1})$, and
$\varrho_{\kappa}=\tfrac{\sqrt{\kappa}-1}{\sqrt{\kappa}+1}$.
For an integer $1\leq n<d$, put
$D_{n}=\operatorname{diag}(\cos(n\theta_{i}))$,
$M=\mathbb{E}\|U\|^{2}$, and
$\mu_{n}=\mathbb{E}[U^{\top}D_{n}U]$.
Then


$\displaystyle M$
$\displaystyle=\frac{d}{\sqrt{\kappa}}\frac{1-\varrho_{\kappa}^{2d}}{1+\varrho_{\kappa}^{2d}},\quad\mbox{and }(-1)^{n}\mu_{n}=\frac{d}{\sqrt{\kappa}}\frac{\varrho_{\kappa}^{n}-\varrho_{\kappa}^{2d-n}}{1+\varrho_{\kappa}^{2d}}.$


Moreover, both $\operatorname{Var}(\|U\|^{2})$ and
$\operatorname{Var}(U^{\top}D_{n}U)$ are at most
$2M\leq 2d/\sqrt{\kappa}$.


If $d-n\geq\sqrt{\kappa}$, then


$(1-e^{-4})e^{-3n/\sqrt{\kappa}}\leq\frac{|\mu_{n}|}{M}\leq e^{-2n/\sqrt{\kappa}}.$


The proof is deferred to
Appendix C.3.
For an exact sample $Y\mid O\sim\pi_{A}$, the vector $U=O^{\top}Y$ has law $N(0,\Lambda^{-1})$, with
$\|Y\|^{2}=\|U\|^{2}$ and $Y^{\top}OD_{n}O^{\top}Y=U^{\top}D_{n}U$.
The lemma therefore gives the means and variances of $\|Y\|^{2}$ and $Y^{\top}OD_{n}O^{\top}Y$ under the target.

## A3.SS3

C.3 Proof of Lemma 4.5



Recall that
$\theta_{i}=(i-\tfrac{1}{2})\pi/d$ and
$\lambda_{i}=(\kappa+1)/2+(\kappa-1)\cos\theta_{i}/2$.
We first expand the inverse spectrum in cosine modes
and sum this expansion over the grid. We then bound
the variances and the normalized cosine bias.


Fact C.7 (Cosine expansion of the inverse spectrum).


For every $\theta\in\mathbb{R}$,


$\frac{2}{\kappa+1+(\kappa-1)\cos\theta}=\frac{1}{\sqrt{\kappa}}\left(1+2\sum_{j\geq 1}(-\varrho_{\kappa})^{j}\cos(j\theta)\right).$


The series converges absolutely and uniformly in $\theta$.


Proof.


Since $0<\varrho_{\kappa}<1$, the geometric-series
identity gives


$\displaystyle 1+2\sum_{j\geq 1}(-\varrho_{\kappa})^{j}\cos(j\theta)$
$\displaystyle=1-\frac{\varrho_{\kappa}e^{i\theta}}{1+\varrho_{\kappa}e^{i\theta}}-\frac{\varrho_{\kappa}e^{-i\theta}}{1+\varrho_{\kappa}e^{-i\theta}}$


$\displaystyle=\frac{1-\varrho_{\kappa}^{2}}{1+2\varrho_{\kappa}\cos\theta+\varrho_{\kappa}^{2}}.$


The definition of $\varrho_{\kappa}$ implies


$\frac{1-\varrho_{\kappa}}{1+\varrho_{\kappa}}=\frac{1}{\sqrt{\kappa}},\qquad\frac{1+2\varrho_{\kappa}\cos\theta+\varrho_{\kappa}^{2}}{(1-\varrho_{\kappa})^{2}}=\frac{\kappa+1+(\kappa-1)\cos\theta}{2}.$


Combining these identities proves the expansion.
Finally,


$\sum_{j\geq 1}\left|(-\varrho_{\kappa})^{j}\cos(j\theta)\right|\leq\sum_{j\geq 1}\varrho_{\kappa}^{j}=\frac{\varrho_{\kappa}}{1-\varrho_{\kappa}},$


which proves absolute and uniform convergence.
∎


Fact C.8 (Exact finite-grid moments).


For $1\leq n<d$,


$M=\frac{d}{\sqrt{\kappa}}\frac{1-\varrho_{\kappa}^{2d}}{1+\varrho_{\kappa}^{2d}},\qquad(-1)^{n}\mu_{n}=\frac{d}{\sqrt{\kappa}}\frac{\varrho_{\kappa}^{n}-\varrho_{\kappa}^{2d-n}}{1+\varrho_{\kappa}^{2d}}.$


Proof.


For every integer $k$,


$\sum_{i=1}^{d}\cos(k\theta_{i})=\begin{cases}d(-1)^{a},&k=2ad,\quad a\in\mathbb{Z},\\
0,&k\notin 2d\mathbb{Z}.\end{cases}$


Indeed, if $k\notin 2d\mathbb{Z}$, the finite cosine sum is
$\sin(k\pi)/(2\sin(k\pi/(2d)))=0$.
If $k=2ad$, then
$\cos(k\theta_{i})=\cos(2ai\pi-a\pi)=(-1)^{a}$.


Since $\mathbb{E}U_{i}^{2}=1/\lambda_{i}$,


$M=\sum_{i}\frac{1}{\lambda_{i}},\qquad\mu_{n}=\sum_{i}\frac{\cos(n\theta_{i})}{\lambda_{i}}.$


Fact C.7 allows us to
interchange the absolutely convergent series with
the finite grid sum.


For $M$, only the terms with $j=2ad$, $a\geq 1$,
survive. Thus


$\displaystyle M$
$\displaystyle=\frac{d}{\sqrt{\kappa}}\left(1+2\sum_{a\geq 1}(-1)^{a}\varrho_{\kappa}^{2ad}\right)$


$\displaystyle=\frac{d}{\sqrt{\kappa}}\left(1-\frac{2\varrho_{\kappa}^{2d}}{1+\varrho_{\kappa}^{2d}}\right)$


$\displaystyle=\frac{d}{\sqrt{\kappa}}\frac{1-\varrho_{\kappa}^{2d}}{1+\varrho_{\kappa}^{2d}}.$


For $\mu_{n}$, we have $\sum_{i}\cos(n\theta_{i})=0$.
Using the product-to-sum identity gives


$\mu_{n}=\frac{1}{\sqrt{\kappa}}\sum_{j\geq 1}(-\varrho_{\kappa})^{j}\left[\sum_{i}\cos((j-n)\theta_{i})+\sum_{i}\cos((j+n)\theta_{i})\right].$


The first inner sum is nonzero precisely when $j=n$
or $j=2ad+n$ with $a\geq 1$; its value is respectively
$d$ or $d(-1)^{a}$.
The second inner sum is nonzero precisely when
$j=2ad-n$ with $a\geq 1$, and then equals $d(-1)^{a}$.
These three classes are disjoint because $1\leq n<d$.
Moreover,
$(-\varrho_{\kappa})^{2ad\pm n}=(-1)^{n}\varrho_{\kappa}^{2ad\pm n}$.
Consequently,


$\displaystyle(-1)^{n}\mu_{n}$
$\displaystyle=\frac{d}{\sqrt{\kappa}}\left[\varrho_{\kappa}^{n}+\sum_{a\geq 1}(-1)^{a}\left(\varrho_{\kappa}^{2ad+n}+\varrho_{\kappa}^{2ad-n}\right)\right]$


$\displaystyle=\frac{d}{\sqrt{\kappa}}\left[\varrho_{\kappa}^{n}-\frac{\varrho_{\kappa}^{2d+n}+\varrho_{\kappa}^{2d-n}}{1+\varrho_{\kappa}^{2d}}\right]$


$\displaystyle=\frac{d}{\sqrt{\kappa}}\frac{\varrho_{\kappa}^{n}-\varrho_{\kappa}^{2d-n}}{1+\varrho_{\kappa}^{2d}}.$


∎


Proof of Lemma 4.5.


Fact C.8 gives the
two asserted means.


Variance bounds.
Since $\Lambda$ is diagonal, the coordinates of $U$
are independent. Each $U_{i}$ is centered Gaussian with
variance $1/\lambda_{i}$, so
$\mathbb{E}U_{i}^{4}=3/\lambda_{i}^{2}$ and
$\operatorname{Var}(U_{i}^{2})=2/\lambda_{i}^{2}$.
Also,
$\lambda_{i}\geq(\kappa+1)/2-(\kappa-1)/2=1$.
Hence


$\displaystyle\operatorname{Var}(\|U\|^{2})$
$\displaystyle=2\sum_{i}\frac{1}{\lambda_{i}^{2}}\leq 2\sum_{i}\frac{1}{\lambda_{i}}=2M,$


$\displaystyle\operatorname{Var}(U^{\top}D_{n}U)$
$\displaystyle=2\sum_{i}\frac{\cos^{2}(n\theta_{i})}{\lambda_{i}^{2}}\leq 2M.$


The exact formula for $M$ gives $M\leq d/\sqrt{\kappa}$.


Normalized bias.
Since $n<d$ and $0<\varrho_{\kappa}<1$,
we have
$\varrho_{\kappa}^{n}>\varrho_{\kappa}^{2d-n}$.
Thus $(-1)^{n}\mu_{n}>0$, and dividing the two moment
formulas yields


$\frac{|\mu_{n}|}{M}=\varrho_{\kappa}^{n}\frac{1-\varrho_{\kappa}^{2(d-n)}}{1-\varrho_{\kappa}^{2d}}.$


Because
$0<\varrho_{\kappa}^{2d}<\varrho_{\kappa}^{2(d-n)}<1$,
the fraction satisfies


$1-\varrho_{\kappa}^{2(d-n)}\leq\frac{1-\varrho_{\kappa}^{2(d-n)}}{1-\varrho_{\kappa}^{2d}}\leq 1.$


To bound the powers of $\varrho_{\kappa}$, observe that


$\displaystyle\log\frac{1}{\varrho_{\kappa}}$
$\displaystyle=\log\frac{\sqrt{\kappa}+1}{\sqrt{\kappa}-1}$


$\displaystyle=2\int_{0}^{1/\sqrt{\kappa}}\frac{dt}{1-t^{2}}$


$\displaystyle=\frac{2}{\sqrt{\kappa}}+2\int_{0}^{1/\sqrt{\kappa}}\frac{t^{2}}{1-t^{2}}\,dt.$


The last integral is nonnegative, giving
$\log(1/\varrho_{\kappa})\geq 2/\sqrt{\kappa}$.
Throughout the integration interval,
$1-t^{2}\geq 1-\kappa^{-1}$, so


$\displaystyle\log\frac{1}{\varrho_{\kappa}}$
$\displaystyle\leq\frac{2}{\sqrt{\kappa}}+\frac{2}{1-\kappa^{-1}}\int_{0}^{1/\sqrt{\kappa}}t^{2}\,dt$


$\displaystyle=\frac{2}{\sqrt{\kappa}}\left(1+\frac{1}{3(\kappa-1)}\right)\leq\frac{8}{3\sqrt{\kappa}}<\frac{3}{\sqrt{\kappa}}.$


Here we used $\kappa\geq 2$.
Exponentiating these bounds gives


$e^{-3n/\sqrt{\kappa}}\leq\varrho_{\kappa}^{n}\leq e^{-2n/\sqrt{\kappa}}.$


If $d-n\geq\sqrt{\kappa}$, the lower bound on
$\log(1/\varrho_{\kappa})$ also gives


$\varrho_{\kappa}^{2(d-n)}=\exp\!\left(-2(d-n)\log\frac{1}{\varrho_{\kappa}}\right)\leq e^{-4(d-n)/\sqrt{\kappa}}\leq e^{-4}.$


Consequently,
$(1-e^{-4})\varrho_{\kappa}^{n}\leq|\mu_{n}|/M\leq\varrho_{\kappa}^{n}$.
Combining this with the bounds on $\varrho_{\kappa}^{n}$
proves


$(1-e^{-4})e^{-3n/\sqrt{\kappa}}\leq\frac{|\mu_{n}|}{M}\leq e^{-2n/\sqrt{\kappa}}.$


∎
