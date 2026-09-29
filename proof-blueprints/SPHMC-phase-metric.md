# SPHMC twisted phase metric

Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, the display defining
`M_kappa` immediately before Theorem 4.5 and the proof of Lemma D.4.

For `z=(x,p)`, Samplinglib expands the exact paper quadratic form as

\[
q_\kappa(z)=\left(\frac1{2\kappa}+\frac12\right)\|x\|^2
  +\langle x,p\rangle+\|p\|^2.
\]

When `kappa >= 1`, Cauchy--Schwarz and the completed-square identity
`2a^2 - 6ab + 5b^2 = ((2a-3b)^2+b^2)/2` give the uniform comparison

\[
\frac16(\|x\|^2+\|p\|^2)\le q_\kappa(z)
\le\frac32(\|x\|^2+\|p\|^2).
\]

The lower bound implies that ordinary product quadratic cost is at most
six times the twisted cost.  Applying this to near-optimal twisted
couplings, then removing the positive excess, proves

\[
W_2^2(\mu,\nu)\le 6 W_{2,M_\kappa}^2(\mu,\nu).
\]

Combining this with the already compiled ordinary-metric phase moment theorem
gives

\[
\mathbb E_\mu[\|X-x_\star\|^2+\|P\|^2]
\le 2(M_X+M_P)+24r^2
\]

from `W_{2,M_kappa}^2(mu,nu) <= r^2`.  This is only the metric adapter used
after the paper's (D.3).  It does not prove (D.3), the uniform phase history,
(D.7), (D.8), or a main theorem.
