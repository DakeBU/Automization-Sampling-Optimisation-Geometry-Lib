# Chebyshev-Lobatto integrated coefficients

Status: in-progress. Canonical leaf: AutoSamplingTheory.TechnicalLemmas.Analysis.ChebyshevLobattoQuadrature.chebyshev_lobatto_coefficients. Proposed minimal imports: Mathlib.LinearAlgebra.Lagrange, Topology.Algebra.Polynomial, Topology.Order.Compact, Trigonometric.Basic and Integrals.Basic. Source: SPHMC2609.06906v1,3.6/B1/B2,1684-1713.

Exact assumptions: natural J>=2 and real h>0. Fin J zero-based actual nodes t_i=h/2(1-cos(i*pi/(J-1))). Lagrange.basis over Finset.univ. Lambda is the actual compact supremum sum_j|ell_j(s)| on[0,h], not an assumed external envelope. Continuous polynomials and compactness discharge measurability, integrability and boundedness. Lebesgue interval integral; no decay or conditional representative.

Search: ASTIS Analysis/Calculus cards and SPHMC modules; Mathlib Lagrange cardinal and sum_basis, Real.injOn_cos, IsCompact.bddAbove_image/le_csSup, intervalIntegral.integral_finsetSum/integral_mono_on/norm_integral_le_integral_norm/integral_id. No SLT/ATLAS port.

Route:1. Prove actual nodes in[0,h], endpoints and cosine injectivity.2. Reuse cardinal Lagrange/partition identities.3. Bound actual Lebesgue supremum by compactness and derive Lambda>=1.4. Charge absolute integral rows by integral of sum absolute polynomials.5. Monotone integrate(t_i-s)*Lambda to t_i^2 Lambda/2<=h^2 Lambda/2.6. Integrate the constant partition to sum momentum weights=h.7. Plug exact arrays into the actual counted-phase paper consumer.

Failure: two or three same-shape failures trigger mathematical/API diagnosis; do not assume missing coefficient bounds or claim all B1. LogarithmicLambda/nonnegative weights/B2 remainder remain independent exact source obligations. Real consumers: current SPHMC Algorithm3.1 counted depth2 and source AlgorithmE1 exact depthK (planned, not compiled).
