# Phase 1 raw-source mathematical cognition

This is a source-only freeze by reviewer src_4e8f6a. It does not select an
implementation target, endorse a Lean proposition, admit a source theorem, or
author/review a proposed Source Proof Graph. The complete primary reading is
§2 (S2), §4 (S4) and Appendix C.4 (A3.SS4) of the pinned original HTML.
§1 (S1) was read as problem/main-result context. No other paper,
implementation, earlier audit or reconstruction was consulted.

The primary inventory is the 50 records in source_claims_seven_slots.json.
Every record preserves objects, quantifiers, domain, assumptions, conclusion,
use and failure boundary, while distinguishing literal formulas, definitions,
inferred standard bridges and deferred proof material. This synthesis
predates any anonymous Lean/reconstruction input.

## The global model

An input is a real symmetric **precision** matrix

\[
 A\in\mathcal A_{d,\kappa}
 =\{A=A^\top:I_d\preceq A\preceq\kappa I_d\},\quad d\ge1,\quad\kappa\ge1.
\]

It defines \(f_A(x)=x^\top Ax/2\) and \(\pi_A=N(0,A^{-1})\). The target
covariance is the inverse of the queried matrix. The exact first-order reply
is \((x^\top Ax/2,Ax)\). The source gives both simulations establishing equal
query complexity for exact value-and-gradient, gradient-only and matrix–vector
access. This does not specify inverse-matrix, noisy or finite-precision access.

Algorithms choose Borel queries, stopping decisions and an arbitrary Borel
output using prior responses and a seed independent of the input. A fixed
budget caps queries for **each input and each seed realization**. Accuracy is
different: the output law for a fixed input averages the seed. \(Q_G\) chooses
one algorithm and a capped integer budget before requiring TV accuracy
uniformly over the entire input class. It is not per-seed accuracy,
\(\forall A\exists\mathrm{Alg}\), or prior-average input accuracy.

The source expressly defines deterministic query caps, not expected query
cost. Remark 1.3's cited warm-start expected-gradient upper bound concerns
another general sampling result and does not define expected-cost \(Q_G\).
TV is the measurable-event supremum, its half-\(L^1\) formula, and the standard
bounded \([0,1]\)-test inequality. The lower bound eventually tests an event;
it does not apply that bounded-test inequality to an unbounded quadratic form.

## Local family versus full main theorem

The family is defined for \(d\ge2,\ \kappa\ge2\):

\[
 \theta_i=(i-\tfrac12)\pi/d,\quad
 \lambda_i=(\kappa+1)/2+(\kappa-1)\cos\theta_i/2,\quad
 \Lambda=\operatorname{diag}(\lambda_i),\quad A=O\Lambda O^\top.
\]

The input prior draws \(O\) from Haar probability on the **full** real
orthogonal group, independently of the private seed. The group includes both
determinant signs. Section 4 does not use a special-orthogonal or
determinant-conditioned law. The deterministic admissibility, calculus and
normalizer claims hold for every such \(O\), without needing a random draw.

The spectrum is fixed for fixed \(d,\kappa\) and may be revealed. The hidden
information is the eigenbasis. Theorem 4.1 adds restrictions absent from the
local definition: for each fixed \(\delta\in(0,1)\), some \(d_0(\delta)\)
works for all integer \(d\ge d_0\), \(2\le\kappa\le d^{1-\delta}\) and
\(0<\varepsilon\le1/10\), giving

\[
 Q_G(d,\kappa,\varepsilon)\ge(\delta/256)\sqrt\kappa\log d.
\]

This includes algorithms knowing the spectrum and gives no growth as
\(\varepsilon\to0\). The main-theorem asymptotic restrictions are not
hypotheses of every local elementary family fact.

The comparison to \(\kappa=2\) requires the **same rotation** in the two
matrices:

\[
 A_\kappa=(\kappa-1)A_2-(\kappa-2)I_d.
\]

Each exact reply at the same query determines the other because
\(\kappa-1\ne0\). This is a matched-instance identity and oracle simulation,
not a pointwise identity for separately drawn rotations. It does not identify
their target covariances or sampling laws. Full-\(O\) quantification and
same-\(O\) matching concern different issues.

## Four interfaces used in the proof

Lemma 4.3 handles an arbitrary output, rather than assuming it belongs to a
query/reply span. For integer \(q\ge0,\ 2q+1<d\), independent standard
Gaussian starts can represent the output on an extended experiment:

\[
 O^\top X\in\mathcal K_q
 =\operatorname{span}\{\Lambda^jg_a:
           1\le a\le q+1,\ 0\le j\le q\}\quad\text{a.s.}
\]

Section 4.3 specifies preservation of the joint law of \((O,X)\). The extra
starting vector accounts for the output; degree-\(q\) polynomial coefficients
may depend on the entire extended experiment. Independence among Gaussian
starts does not alone authorize independence from all other random variables.
The C.1 proof is deferred and outside this assigned reading.

Lemma 4.4 uses \(n=2q+1\), \(D_n=\operatorname{diag}(\cos(n\theta_i))\) and
an absolute \(C>0\):

\[
 \tau_{d,q}=C\left[(q+1)\sqrt{\frac{\log d}{d}}
   +\frac{(q+1)(q+1+\log d)\log d}{d}\right].
\]

If \(\tau\le1/2\), with probability at least \(0.99\), simultaneously every
\(u\in\mathcal K_q\) satisfies
\(|u^\top D_nu|\le2\tau\|u\|^2\). This uniformity handles coefficients
depending on the full experiment. The nonconstant affine change between
\(\lambda_i\) and \(\cos\theta_i\) gives the equivalent cosine-polynomial
span and hence a \(\kappa\)-independent estimate. This reasoning needs a
nonzero slope; it cannot simply cover \(\kappa=1\). C.2 is deferred proof
material.

Lemma 4.5 takes \(U\sim N(0,\Lambda^{-1})\), \(1\le n<d\),
\(r=(\sqrt\kappa-1)/(\sqrt\kappa+1)\),
\(M=\mathbb E\|U\|^2\), \(\mu_n=\mathbb E[U^\top D_nU]\), and states

\[
 M=\frac d{\sqrt\kappa}\frac{1-r^{2d}}{1+r^{2d}},\qquad
 (-1)^n\mu_n=\frac d{\sqrt\kappa}
                 \frac{r^n-r^{2d-n}}{1+r^{2d}}.
\]

Both quadratic variances are at most \(2M\le2d/\sqrt\kappa\). With the
additional condition \(d-n\ge\sqrt\kappa\),

\[
 (1-e^{-4})e^{-3n/\sqrt\kappa}
 \le|\mu_n|/M\le e^{-2n/\sqrt\kappa}.
\]

The exact parity, finite-grid corrections and conditional domain are part of
the source. For each conditional exact sample \(Y\mid O\), \(U=O^\top Y\)
has the diagonal Gaussian law, and both the norm and rotated cosine statistic
are unchanged. C.3 is deferred proof material.

The printed Lemma 4.6 itself concludes only
\(I_d\preceq A\preceq\kappa I_d\) for every \(O\in O(d)\), under the local
family parameters. C.4 also contains distinct calculus and normalization
assertions, which cannot be silently folded into the printed short statement.

## C.4: calculus and normalizer assertions

The proof uses \(0<\theta_i<\pi\), hence
\(-1<\cos\theta_i<1\) and \(1<\lambda_i<\kappa\). Orthogonal conjugation
then yields the non-strict Loewner bounds. This compresses standard
diagonal-order/quadratic-form algebra; it is not already a formal proof.

The potential is called \(V_A\) in C.4 and \(f_A\) earlier. It is
\(C^\infty\) with Hessian \(A\), so it is 1-strongly convex and
\(\kappa\)-smooth under the usual Euclidean definitions. These are valid
bounds, not assertions of optimal constants. Also \(V_A(0)=0\) and
\(V_A(x)\ge\|x\|^2/2>0\) for \(x\ne0\); the origin is the unique minimizer.
This explains the subclass connection to general Hessian-bounded potentials
with a known minimizer.

The source identifies the target as \(N(0,A^{-1})\) and uses Gaussian
integration to give

\[
 Z_A=(2\pi)^{d/2}(\det A)^{-1/2}
     =(2\pi)^{d/2}(\det\Lambda)^{-1/2}.
\]

This is the normalizing integral, not the reciprocal density prefactor.
Expanding a standard bridge gives
\(\det A=(\det O)^2\det\Lambda=\det\Lambda\), including \(\det O=-1\).
This expansion is reviewer inference from determinant identities, not a
separately printed C.4 theorem. Positive definiteness, determinant positivity,
quadratic calculus and the Gaussian integral all need actual justification in
a formal proof. The source does not derive that integral here. For fixed
\(d,\kappa\), fixed \(\Lambda\) makes \(Z_A\) independent of \(O\) and known
from the public spectrum. It can change with \(d,\kappa\) or another spectrum.

## Full proof parameter and probability work

For a hypothetical capped sampler with
\(q\le(\delta/256)\sqrt\kappa\log d\), define

\[
 S_A(x)=(-1)^n x^\top T_n\!\left(
       \frac{2A-(\kappa+1)I}{\kappa-1}\right)x-2\tau\|x\|^2,
 \qquad E_A=\{x:S_A(x)>0\}.
\]

The first-kind Chebyshev polynomial transforms the normalized \(A\) to
\(OD_nO^\top\). For \(x\ne0\), energy fractions along eigenvectors give the
weighted-cosine interpretation. At zero, use \(S_A(0)=0\) directly.
The polynomial in \(A\) defines the event without choosing an eigenbasis
representative.

The proof discharges the conditional lemma hypotheses internally. Uniformly
in allowed \(\kappa,q\), large \(d\) gives
\(q+1\le d^{(1-\delta)/2}\log d\), \(n=o(d)\), and
\(\tau\lesssim d^{-\delta/2}(\log d)^3\to0\). Thus \(n<d\) and
\(\tau\le1/2\). The joint random-input/algorithm experiment fails the test
except with probability at most \(0.01\). That rejection probability is not
claimed separately for each fixed input.

For the target, the source verifies \(d-n\ge\sqrt\kappa\) and derives, with
\(\beta=|\mu_n|/M\), \(b=(1-e^{-4})e^{-3}\),

\[
 \beta\ge b d^{-\delta/4},\quad
 M\ge d^{(1+\delta)/2}/2,\quad
 \tau/\beta\to0,\quad M\beta^2\ge(b^2/2)\sqrt d\to\infty.
\]

One \(d_0(\delta)\), uniform in the stated range, ensures all earlier
conditions, \(\tau\le\beta/4\), and \(M\beta^2\ge320\).
For every fixed family input and target sample, \(Z=S_A(Y)\) then has
\(\mathbb EZ\ge\beta M/2\), \(\operatorname{Var}Z\le8M\).
The centered \(L^2\) triangle inequality requires no independence between
the two quadratic forms. Chebyshev gives \(\pi_A(E_A)\ge0.9\).

The per-input TV bound controls that input's event \(E_A\), and averaging
gives \(0.89\le\varepsilon\le0.1\), a contradiction. There is no direct TV
comparison of prior-marginal output laws. Event-kernel measurability, uniform
asymptotic threshold selection, padding an at-most-\(q\) algorithm if needed,
and standard algebraic bridges remain obligations of a rigorous implementation,
rather than assumptions to append to the public source theorem.

## Method limitations and unfinished boundary

Lemma 4.7 states
\(\dim\mathcal K_q=\min\{d,(q+1)^2\}\) almost surely for every integer
\(q\ge0\), using the distinct spectrum. This lemma is stated but not proved
in the assigned §4/C.4 slice; no \(2q+1<d\) restriction is in its printed
statement. Once the space is full, and \(1\le n<d\),
\(\sum_i\cos^2(n\theta_i)=d/2\) gives a coordinate Rayleigh quotient at least
\(1/\sqrt2\). Thus this enlarged-space uniform strategy loses the small
separation needed on the desired query scale, around
\(\kappa\gtrsim d/\log^2d\).

A scope detail is preserved: the limitation prose says the separating uniform
bound must be at most \(1/2\), while Lemma 4.4 literally concludes
\(\le2\tau\) under \(\tau\le1/2\). The main proof's stronger separation
regime has \(2\tau\le\beta/2\le1/2\). Do not rewrite the literal lemma to
match that prose.

For accuracy, this uniform-bound/mean-variance certificate needs \(t\ge a\)
for the algorithm and \(t<\beta\) for the target. The source cites the
Bernstein calculation in Fact C.6 for \(a\ge c/\sqrt d\), while
\(\beta\le e^{-2(2q+1)/\sqrt\kappa}\). Logarithms bound
\(q=O(\sqrt\kappa\log d)\) independently of \(\varepsilon\). The cited Fact
C.6 calculation was not inspected and is recorded as a source-attributed
boundary, not independently proved. The source explicitly leaves stronger
lower bounds for this same fixed-spectrum family open. These limitations
concern this proof strategy, not all possible tests, analyses or the truth of
accuracy-dependent hardness.

## Frozen next-phase boundary

This cognition was formed without a Lean candidate, target declaration, author
proof, proposed acceptance conclusion, older audit, private reviewer rationale
or blind reconstruction. Later comparison must pin anonymous inputs and compare
selectively against these clauses. Whole-module/reader context and fresh Lean
checks belong after that staged comparison. None has been performed here.
