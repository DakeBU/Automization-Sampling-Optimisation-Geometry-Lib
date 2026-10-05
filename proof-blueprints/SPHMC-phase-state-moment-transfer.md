# SPHMC phase-state moment transfer

Source: Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, Lemma D.4 proof,
using the phase-law estimate (D.3) and initialization Lemma 4.16.

## Shared edge

If `g` is `b`-Lipschitz, its squared norm is integrable under a reference law
`nu`, and

\[
W_2^2(\mu,\nu)\le r^2,
\]

then

\[
\mathbb E_\mu\|g\|^2
\le 2\,\mathbb E_\nu\|g\|^2+2b^2r^2.
\]

The Lean proof selects couplings with cost arbitrarily close to the transport
infimum, proves integrability before using real integrals, and lets the excess
cost tend to zero.  It does not assume existence of an optimal coupling.

## SPHMC adapter

Apply the shared edge separately to

\[
g_X(x,p)=x-x_\star,\qquad g_P(x,p)=p.
\]

For the ordinary product metric this yields

\[
\mathbb E_\mu[\|X-x_\star\|^2+\|P\|^2]
\le 2(M_X+M_P)+4r^2.
\]

## Strict boundary

The paper uses the twisted metric induced by `M_kappa`, whereas Lean's ordinary
product norm is the max norm.  This packet does not identify those metrics or
prove (D.3), the uniform-in-phase history estimate, the layer-one/layer-two
center bounds, (D.7), (D.8), or a main theorem.  The next source-specific edge
is an explicit `M_kappa` norm definition and comparison certificate.
