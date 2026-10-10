  have hDiagL (u : HP0) : inner ℝ (K (A0 u)) (ΓP0 u)=‖A0 u‖^2 := by
    calc
      inner ℝ (K (A0 u)) (ΓP0 u)=inner ℝ (ΓP0 (K (A0 u))) u :=
        (hΓself.isSymmetric _ _).symm
      _ = inner ℝ (A0 (A0 u)) u := by rw [hΓK]
      _ = inner ℝ (A0 u) (A0 u) := hA0self.isSymmetric _ _
      _ = ‖A0 u‖^2 := real_inner_self_eq_norm_sq _
  have hDiagR (v : HP0) : inner ℝ (K (ΓP0 v)) (A0 v)=‖A0 v‖^2 := by
    rw [hKΓ,real_inner_self_eq_norm_sq]
  have hSwap (u v : HP0) : inner ℝ (ΓP0 u) (A0 v)=inner ℝ (A0 u) (ΓP0 v) :=
    (hCross u v).symm
  have hSwap2 (u v : HP0) : inner ℝ (A0 v) (ΓP0 u)=inner ℝ (A0 u) (ΓP0 v) :=
    (real_inner_comm _ _).trans (hSwap u v)
