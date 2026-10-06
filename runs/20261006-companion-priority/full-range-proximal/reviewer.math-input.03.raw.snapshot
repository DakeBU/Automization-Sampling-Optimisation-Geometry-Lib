# Actual standardized RGO: next dependency proposal

Status: source/API scheduling proposal only. No new SAU, sealed signature,
production proof, independent admission or complete Lemma 4.2 is claimed.

Primary: Chen, Chewi, Lu and Zhang, SPHMC arXiv:2609.06906v1,
Section 4.1, `S4.SS1.p4` and `S4.SS1.p5`, equations (4.6) and the two
gradient representations. The pinned raw source is
`runs/20261006-companion-priority/smoothed-hessian-lower-preread/source-primary.sphmc-v1.raw.html`,
SHA256 `ec485cdad5fe140114be35eef93d19398e0cafcf21abb3fff1bdbbf462e5f94d`.
The primary paragraphs were read before this bounded API search.

The source retains full Euclidean space, a genuine C2 potential with
beta=1 and alpha=kappa^-1, kappa>=1, and 0<eta<=1. The actual RGO is
R_y(dx) proportional to exp(-V(x)-||x-y||^2/(2eta))dx. Its actual proximal
point satisfies p_y+eta gradient V(p_y)=y and is the unique global
minimizer of that quadratic-regularized potential. Neither an assumed
Lipschitz proximal selector nor supplied posterior moment belongs in the
source Anchor.

The source standardized potential and law are

\[
\rho_y(u)=V(p_y+\sqrt\eta u)-V(p_y)
 -\sqrt\eta\langle\nabla V(p_y),u\rangle,\qquad
Q_y(u)=\tfrac12\|u\|^2+\rho_y(u),\qquad
\mathsf r_y=(x\mapsto(x-p_y)/\sqrt\eta)_\#R_y.
\]

The missing actual measure adapter must establish
\(\mathsf r_y=Z_{Q_y}^{-1}e^{-Q_y}du\), with positive finite
normalization, before consuming a moment theorem on this law. The proximal
equation cancels the linear term; the constant and affine Jacobian cancel
only through a real normalized change-of-variables proof. Pointwise equality
of potentials is insufficient to identify the probability measures.

The source has \(\nabla\rho_y(0)=0\) and
\(0\preceq D^2\rho_y\preceq\eta I\), hence
\(I\preceq D^2Q_y\preceq(1+\eta)I\). Actual integrability,
stationarity and covariance/position moments precede all expectation bounds.
The sharp position consequence needed in (4.6) is
\(\mathbb E_{\mathsf r_y}\|U\|^2\le d\). Finite Hilbert/Borel
representation including dimension zero would be a disclosed extension;
no unit-vector or Nontrivial-space premise is allowed.

Current exact APIs searched:

- `ProximalGaussianEstimator.proximal_gaussian_estimator` constructs a jointly
  measurable exact proximal oracle, real Gaussian output kernel and moments,
  but its public construction range is eta<=1/2. This is an explicit existing
  restriction, not the source's eta<=1 boundary.
- `ProximalEstimatorLipschitz.proximal_estimator_lipschitz` already derives
  actual input/noise Lipschitz bounds (4.4)-(4.5) on that same restricted range.
  Repeating those bounds would be duplicate work.
- `GibbsPositionMoment.gibbs_position_moment` already produces normalized
  probability, true noncompact integrability, the position-gradient identity
  and exact dimension/curvature position bound at an actual stationary point.
  The source standardized-law transport and stationary point adapter remain
  necessary consumers; no need to re-prove its IBP theorem.
- Shared `QuadraticRegularization`, `StrongConvexFirstOrder`,
  `MonotoneProximalMap`, and Mathlib compact/proper-space minimum APIs are
  candidate substrates for removing the proximal construction restriction.
  `QuadraticRegularizationTransfer.exists_minimizer_radius_and_accuracy`
  assumes an attained minimum of its original objective, so it cannot be
  substituted for the needed existence result without that dependency.
- `RadonNikodym.measurableEquiv_map_withDensity`, actual affine Gaussian
  density APIs and tilted-measure definitions supply concrete transport
  candidates. No map-of-tilted-law theorem has yet been admitted by this note.

A future exact statement must be independently sealed before proof search.
Candidate bounded route: construct actual proximal minimizers over the full
source eta range; establish their equation/unique minimum and measurable
nonexpansive selector; derive Q_y/rho_y C2 curvature and stationarity; prove
the literal normalized affine posterior law; then consume the existing sharp
position theorem. The final packet should contain an actual paper consumer,
not merely a generic argmin existence wrapper.

This does not prove Gaussian Talagrand/LSI, Fisher-to-W2, the eta^(3/2)*sqrt(d)
bias bound, Gaussian directional MGF, all higher cumulants/Caffarelli transport,
Picard accuracy, warmness, either main theorem or expected-cost composition.
Those boundaries remain independent. TV proximity never transfers unbounded
expected work; exact-gradient K, stochastic-exact-proximal Khat and
conditional-mean Kbar remain distinct.
