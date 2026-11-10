# Exercise 1.7: the actual-law KL expansion

See the [frozen scope and signature](actual-kl-statement-v1.md). This is
original exposition of (1.E.1), not a transcript of the source.

Let \(\mu\) be a probability measure and \(f\) a real a.e.-strongly-measurable
observable with \(|f|\le M\) almost everywhere and \(\int f\,d\mu=0\).
Put \(p_\varepsilon=1+\varepsilon f\). For example, choose parameters with
\(|\varepsilon|\,|M|<1/2\); no division by \(M\) is needed, even for \(M=0\).
Then \(1/2\le p_\varepsilon\le3/2\) almost everywhere and
\(\int p_\varepsilon\,d\mu=1+\varepsilon\int f\,d\mu=1\).
Thus \(\nu_\varepsilon=p_\varepsilon\mu\) is an actual probability law and
its Radon–Nikodym density is \(p_\varepsilon\) almost everywhere. The density
used in Lean is `ENNReal.ofReal p`; the bounds prevent clipping almost
everywhere in the relevant parameter neighborhood.

For \(k(t)=t\log t+1-t\), the bounded positive density makes \(k(p_\varepsilon)\)
integrable. The two compensation terms cancel on a probability law of mass
one, so
\[
 \mathrm{KL}(\nu_\varepsilon\,\|\,\mu)
 =\int p_\varepsilon\log p_\varepsilon\,d\mu
 =\int k(p_\varepsilon)\,d\mu<\infty .
\]
In Lean this is first an **extended-real** equality with `ofReal` of a finite
integral. Only then use the real value, using nonnegativity of \(k\).
The identity `toReal ∞ = 0` would make a bare real-limit claim insufficient.

For \(\varepsilon\ne0\), Taylor's integral remainder at one gives
\[
 \frac{k(1+\varepsilon f(x))}{\varepsilon^2}
 = f(x)^2\int_0^1\frac{1-s}{1+s\varepsilon f(x)}\,ds.
\]
The denominator is at least \(1/2\) throughout the segment almost everywhere.
The integrable bound \(f^2\) and the pointwise limit \(f^2/2\) give the
integral limit by dominated convergence. At zero \(\nu_0=\mu\) and
\(\mathrm{KL}(\nu_0\|\mu)=0\). In particular the remainder is zero there,
and the little-o claim holds in the full neighborhood of zero:
\[
 \mathrm{KL}(\nu_\varepsilon\,\|\,\mu)
 = \frac{\varepsilon^2}{2}\int f^2\,d\mu + o(\varepsilon^2).
\]

## Lean and source boundary

`AffinePerturbationKL.klDiv_affine_perturbation_second_order` directly uses
the existing owned `BoundedPerturbationLaw` for probability and the
extended-real identity, and `BoundedDensityPerturbation` for the real
compensated limit. The latter proves the scalar coefficient and bound using
genuine differentiation before dominated convergence. Mathlib supplies
`withDensity_one`, `klDiv_self`, and the relation between vanishing quotient
and little-o. The generic assumptions are supplied automatically by the
compact smooth centered test. The focused test also recovers the
positive-sided quotient used in Corollary 2.1.2.

This is the KL input used in that corollary, not a proof of its transport
bound or of T2 implies PI. The separate compact LSI-to-PI proof uses the
real compensated integral directly; it need not artificially import the
actual-law KL theorem to create a graph edge. Abstract semigroup and
closed-form domains remain open.
