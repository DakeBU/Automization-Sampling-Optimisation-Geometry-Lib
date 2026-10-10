  have hMixed (u v : HP0) :
      inner ℝ (K (A0 u)) (A0 v)+inner ℝ (A0 u) (ΓP0 v)=inner ℝ (K u) v := by
    calc
      inner ℝ (K (A0 u)) (A0 v)+inner ℝ (A0 u) (ΓP0 v)=
          inner ℝ (A0 (K (A0 u))) v+inner ℝ (ΓP0 (A0 u)) v :=
        congrArg₂ (fun x y : ℝ => x+y)
          (hA0self.isSymmetric (K (A0 u)) v).symm
          (hΓself.isSymmetric (A0 u) v).symm
      _ = inner ℝ (A0 (K (A0 u))+ΓP0 (A0 u)) v := (inner_add_left _ _ _).symm
      _ = inner ℝ (K u) v := by rw [hKMixedVector]
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
  have hCorrector (u v : HP0) :
      ((‖A0 u-ΓP0 v‖^2-‖ΓP0 u+A0 v‖^2)/2-
        inner ℝ (K (A0 u-ΓP0 v)) (ΓP0 u+A0 v))-
      ((‖u‖^2-‖v‖^2)/2-inner ℝ (K u) v)= -‖u‖^2+‖v‖^2 := by
    rw [norm_sub_sq_real,norm_add_sq_real,map_sub,inner_sub_left,
      inner_add_right,inner_add_right,hDiagL,hDiagR,hKΓ,hSwap2,hSwap]
    nlinarith only [hEnergy u,hEnergy v,hMixed u v]
