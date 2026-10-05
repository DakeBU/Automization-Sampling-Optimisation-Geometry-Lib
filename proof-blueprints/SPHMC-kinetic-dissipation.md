# SPHMC actual full-dimensional kinetic drift dissipation

Primary source: arXiv:2609.06906v1 §4.3, Proposition4.7 proof, (4.14)-(4.15), HTML597-611. One bounded source matrix edge; full nonlinear kernel contraction remains open.

For κ≥1 put α=1/(2κ). The real symmetric linear H satisfies α||v||²≤⟨v,Hv⟩≤||v||² for every v. The source matrices act by A_H(x,p)=(p,-Hx-p) and Mκ(x,p)=((α+1/2)x+p/2,x/2+p). Their exact quadratic form is Qκ=(α+1/2)||x||²+⟨x,p⟩+||p||², with -2⟨Mκz,A_Hz⟩=D_H=⟨x,Hx⟩+2⟨p,Hx⟩-2α⟨x,p⟩+||p||². The target is D_H≥α Qκ/4=Qκ/(8κ), for every x,p in the whole finite-dimensional real inner-product space, including dimension0.

1. For α≤λ≤1, λ-(λ-α)²-α=(λ-α)(1+α-λ)≥0.
2. Set t=1-α/2>0 and Δ=(λ-α/2)t-(λ-α)²≥0, using the preceding determinant estimate and λ≤1. Multiplying the residual quadratic form by t yields (tv+(λ-α)u)²+Δu²≥0. Therefore Dλ≥α(u²+v²)/2.
3. Qλ=(α+1/2)u²+uv+v²≤2(u²+v²) from α≤1/2 and (u-v)²≥0. Thus Dλ≥αQλ/4.
4. Obtain Mathlib's finite orthonormal eigenbasis from actual H symmetry. Evaluate the full all-vector source bounds at each unit b_i to derive α≤λ_i≤1. No eigenbasis or coercivity certificate is a hypothesis.
5. Use symmetry directly: ⟨b_i,Hx⟩=⟨Hb_i,x⟩=λ_i⟨b_i,x⟩. Parseval and finite inner-product summation identify all five exact coefficient sums, including ⟨x,Hx⟩ and ⟨p,Hx⟩. Sum the scalar inequalities to obtain full-E D_H≥αQκ/4.
6. Specialize α and keep the precise source1/(8κ) factor. Two private proof helpers share the public whole-module review, without separate leaf/progress credit.

Pinned Mathlib APIs searched and used: LinearMap.IsSymmetric.eigenvectorBasis/apply_eigenvectorBasis, OrthonormalBasis.norm_eq_one/sum_inner_mul_inner, Finset.sum_le_sum, real inner algebra. Existing ASTIS PhaseMetric private quadratic/phaseCost remain untouched; no duplicate public norm or fake sampler consumer. Retired repr-coordinate simplification route after polymorphic real/WithLp API errors; direct symmetry solves the needed identity without changing the proposition.

Focused input: actual E=R²,H=I/2,κ2 with independently derived all-vector spectral bounds, all x,p; empty dimension retained. Focused PASS3183, independent fresh mathematical review and blind reconstruction pass. Publication140 validates current lesson/binding. Current anti-anchored whole-module source review accepted equivalent-after-elaboration after docstring clarification only; independent exact-commit VERIFIED passes at 3dcc65cfe1e6029ca8b0df80d7813ddfe7cc2e2d; shared aggregate/reader admission remains separate. No assumed contraction recurrence.

Conceptual mirror audit: none-found. This closes the exact source spectral drift inequality; the existing metric-gradient-flow family is preserved without equating first-order kinetic drift to an overdamped gradient flow.

Remaining consumer: Proposition4.7 exact deterministic smoothed-gradient K contraction, requiring actual positive integral b weights/averaged Hessian, first-order expansion/remainder and step restriction. Khat exact-proximal stochastic phase, Kbar conditional mean, histories/D3/D7/D8, main sampling results and PBPS/composition remain independent unfinished boundaries. No probability-law, TV-to-cost, invariance or kernel-accuracy claim. Original single root stabilization lane only.
