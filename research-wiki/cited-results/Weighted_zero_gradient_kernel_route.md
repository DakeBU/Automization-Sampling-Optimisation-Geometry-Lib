# Zero ordinary weak gradient: a separate kernel-constants route

2026-10-06. Root discovery, raw/unvalidated planning only; no Lean theorem,
independent source verdict, new SAU or complete Poincare/BL result is recorded.

PBPS arXiv:2609.06905v1 Appendix C.1 omitted full-space domain/Poincare route
and SPHMC2609.06906v1 Section4.1 BL dependency motivate a separate kernel
boundary in a later centered-epsilon resolvent proof. It need not wait for H2:
if a volume-locally-integrable scalar u on a finite real Hilbert space has
integral u Dpsi[v]=0 for every C1 compact psi and every v, it should be volume
ae constant. This statement is proposed, not a callable local declaration.

Pinned Mathlib db584cd6d46c92f209a44c0f1c829460d327499d was searched first.
Analysis/Calculus/BumpFunction/Convolution.lean supplies
ContDiffBump.ae_convolution_tendsto_right_of_locallyIntegrable with actual
shrinking outer radii and bounded outer/inner ratio. MeanValue.lean supplies
is_const_of_fderiv_eq_zero for genuine differentiable mollifications. Existing
ASTIS WeightedGradientDistribution and the true conditional gradient supply
ordinary volume weak-gradient identities for the original closed graph.

Proposed route (not yet compiled):
1. Construct normalized actual compact mollifiers with rOut=2*rIn tending0.
2. Differentiate their convolution with locally integrable u using the compact
   left kernel; translated C1 compact weak tests make every derivative zero.
3. Actual differentiability and zero Frechet derivative make each convolution
   constant on the connected full Hilbert space.
4. Genuine volume ae mollifier convergence yields u ae constant: choose one
   point in the full-measure convergence set (volume is nonzero), and compare
   the same constant sequence at all other ae points.
5. A later actual Gibbs adapter must prove volume/positive-tilted ae transfer,
   zero closed-gradient representative transfer, and mean-zero normalization.

The initial kernel leaf uses ordinary volume and genuine local integrability;
weighted classes are not volume-integrable by definition. Dimension0 remains
included. The source operator is the same original D, not a replacement.
No global H2/core/Bochner, spectral gap, zero-epsilon limit or measurable fiber
selector follows from this planning note. Reflected/RGO laws/operators and
Dirichlet scales remain independent. It can reduce a later residual-kernel
obligation, but does not bypass the separate global Bochner/coercivity proof.

No matching existing Discovery or Frontier Cell for zero weak gradient was
found in the bounded search. This is a lemma proposal, not a conceptual mirror
or certified formal dependency. Do not include it in current source completion.
