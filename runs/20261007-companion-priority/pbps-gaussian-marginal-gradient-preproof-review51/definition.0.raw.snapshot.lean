
/-- A `LinearPMap σ E F` or `E →ₛₗ.[σ] F` is a (semi)linear map from a submodule of `E` to `F`. -/
structure LinearPMap {R S : Type*} [Ring R] [Ring S] (σ : R →+* S) (E : Type*)
    [AddCommGroup E] [Module R E] (F : Type*) [AddCommGroup F] [Module S F] where
  /-- The domain of the (semi)linear map. -/
  domain : Submodule R E
  /-- The (semi)linear map itself. -/
  toFun : domain →ₛₗ[σ] F

@[inherit_doc] notation:25 E " →ₛₗ.[" σ:25 "] " F:0 => LinearPMap σ E F

/-- `E →ₗ.[R] F` is the notation for `E →ₛₗ.[RingHom.id R] F`. -/
notation:25 E " →ₗ.[" R:25 "] " F:0 => LinearPMap (RingHom.id R) E F

variable {R S T : Type*} [Ring R] [Ring S] [Ring T] {σ : R →+* S} {τ : S →+* T} {E : Type*}
