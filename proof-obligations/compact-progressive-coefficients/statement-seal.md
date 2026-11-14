# Continuous coefficients along a compact-state progressive process

Let X be a jointly measurable, strongly progressive process taking values in a compact second-countable pseudometrizable Borel state space S. Let c be a continuous real function of nonnegative time and state. Then the coefficient evaluated along X is strongly progressive. For each finite nonnegative horizon its time section is integrable at every sample. With a finite sample measure, the sample-first product representative belongs to $L^p$ for every exponent p in the extended nonnegative reals.

- The sample space carries a finite measure and a filtration indexed by nonnegative time. The horizon T is nonnegative and finite. The integrability exponent p is any extended nonnegative real, including zero and infinity.
- The state space S is compact, second countable and pseudometrizable, with its Borel sigma-algebra. The process is jointly measurable and strongly progressive.
- The real coefficient c is jointly continuous on nonnegative time times S. The horizon time measure is Lebesgue time restricted to [0,T] on the nonnegative real axis.

\[
b(t,\omega)=c(t,X_t(\omega)),\quad b(\cdot,\omega)\in L^1(\ell_T)\ \ (\forall\omega),\quad [(\omega,t)\mapsto b(t,\omega)]\in L^p(\mu\otimes\ell_T).
\]

The claim is coefficient regularity and finite-horizon integrability for a given process. Progressive measurability is global; the time-section and product bounds are local to the chosen horizon.

Samplinglib supplementary stochastic-analysis lemma, Lean 4.33.0. Original Samplinglib compact-state coefficient lemma, statement seal; Mathlib MemLp.of_bound provides the product-space bound.
