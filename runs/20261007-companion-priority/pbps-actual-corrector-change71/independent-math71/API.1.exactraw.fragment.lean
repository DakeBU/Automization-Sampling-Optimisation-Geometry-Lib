
theorem adjoint_eq {A : E →L[𝕜] E} (hA : IsSelfAdjoint A) : A.adjoint = A :=
  hA

/-- Every self-adjoint operator on an inner product space is symmetric. -/
theorem isSymmetric {A : E →L[𝕜] E} (hA : IsSelfAdjoint A) : (A : E →ₗ[𝕜] E).IsSymmetric := by
  intro x y
  rw_mod_cast [← A.adjoint_inner_right, hA.adjoint_eq]

/-- Conjugating preserves self-adjointness. -/
theorem conj_adjoint {T : E →L[𝕜] E} (hT : IsSelfAdjoint T) (S : E →L[𝕜] F) :
