section NormedDivisionRing

variable [NormedDivisionRing 𝕜] [NormedDivisionRing 𝕜₂] {σ₁₂ : 𝕜 →+* 𝕜₂}
  [AddCommGroup E] [SeminormedAddCommGroup Eₗ] [NormedAddCommGroup F]
  [Module 𝕜 E] [Module 𝕜₂ F] [IsBoundedSMul 𝕜₂ F] [Module 𝕜 Eₗ] [IsBoundedSMul 𝕜 Eₗ]
  [CompleteSpace F]

variable (f : E →ₛₗ[σ₁₂] F) (e : E →ₗ[𝕜] Eₗ)

/-- Extension of a linear map `f : E →ₛₗ[σ₁₂] F` to a continuous linear map `Eₗ →SL[σ₁₂] F`,
where `E` is a normed space and `F` a complete normed space, using a dense map `e : E →ₗ[𝕜] Eₗ`
together with a bound `‖f x‖ ≤ C * ‖e x‖` for all `x : E`. -/
def extendOfNorm : Eₗ →SL[σ₁₂] F := (f.compLeftInverse e).extend (LinearMap.range e).subtypeL
