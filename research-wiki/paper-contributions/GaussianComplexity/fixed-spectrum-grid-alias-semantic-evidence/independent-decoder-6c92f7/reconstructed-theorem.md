# Reconstructed theorem

For every natural number \(d\) satisfying \(2\le d\), and for every integer \(k\), define the real numbers
\[
\theta_i=\frac{(i+\tfrac12)\pi}{d},\qquad i=0,1,\ldots,d-1.
\]
Then the real finite sum satisfies
\[
\sum_{i=0}^{d-1}\cos(k\theta_i)
=
\begin{cases}
 d\,(-1)^{\,k/(2d)},& 2d\mid k,\\
 0,& 2d\nmid k.
\end{cases}
\]
Here divisibility and the quotient \(k/(2d)\) are taken in the integers. In the divisible case, the quotient is the unique integer \(m\) such that \(k=2dm\). The power \((-1)^m\) is a real integer power, including inverse powers when \(m<0\).

Equivalently, for each admissible \(d\), the value is \(d\) when \(k=4dn\) for an integer \(n\), is \(-d\) when \(k=2d(2n+1)\) for an integer \(n\), and is \(0\) for every other integer \(k\). These cases exhaust all integer values of \(k\).

## Quantifiers, objects, and domains

The quantifier order is: choose any \(d\in\mathbb N\); assume \(2\le d\); then choose any \(k\in\mathbb Z\). Within that scope, \(\theta\) is the uniquely specified function from \(\operatorname{Fin}(d)\) to \(\mathbb R\), determined by \(d\) alone. Each index has the natural value \(i\in\{0,\ldots,d-1\}\), and the sum includes each such index exactly once. Natural and integer quantities used in the angles and the real product on the right are cast to real numbers. The \(1/2\) in the angle is the real number one half, not integer division. The angle uses the standard real constant \(\pi\), and cosine is the standard real cosine.

The only hypothesis is \(d\in\mathbb N\) with \(d\ge2\). There is no restriction on the sign, parity, or size of \(k\). In particular, \(2d\) is a positive, nonzero integer, so the integer quotient in the divisible branch is exact, including for negative \(k\). No quotient is needed to describe the nondivisible branch.

## Zero, positive, and negative frequencies

At \(k=0\), the quotient is \(0\), the integer power is \((-1)^0=1\), and the asserted sum is \(d\).

For \(k>0\), if \(k=2dm\) with \(m>0\), the asserted sum is \(d\) for even \(m\) and \(-d\) for odd \(m\). Every positive \(k\) not divisible by \(2d\) has asserted sum \(0\).

For \(k<0\), if \(k=-2dn\) with \(n>0\), the integer exponent is \(-n\). The asserted sum is \(d\) for even \(n\) and \(-d\) for odd \(n\). Every negative \(k\) not divisible by \(2d\) has asserted sum \(0\). Thus the stated value at a negative integer is the same as at its positive opposite. All odd integers are in the zero-valued branch; an even integer is in a nonzero branch exactly when it is divisible by \(2d\).

## Scope and constants

The statement covers every integer \(k\) for each fixed natural dimension \(d\ge2\), with the same explicitly specified angles. It makes no assertion for \(d=0\) or \(d=1\), or for noninteger frequencies. There are no auxiliary parameters, unspecified constants, error terms, limiting statements, or further regularity assumptions. The amplitude is exactly the real cast of \(d\); the fixed numerical constants are \(0\), \(1\), \(2\), \(1/2\), \(-1\), and \(\pi\). The equivalent parity formulation introduces \(4\) only as \(2\cdot2\). This reconstruction states the mathematical content and its scope, without a proof or a claim about any source identity or source fidelity.
