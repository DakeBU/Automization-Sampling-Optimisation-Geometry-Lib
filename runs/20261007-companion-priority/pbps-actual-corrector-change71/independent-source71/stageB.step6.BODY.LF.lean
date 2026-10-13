  have hCorrector (u v : HP0) :
      ((‖A0 u-ΓP0 v‖^2-‖ΓP0 u+A0 v‖^2)/2-
        inner ℝ (K (A0 u-ΓP0 v)) (ΓP0 u+A0 v))-
      ((‖u‖^2-‖v‖^2)/2-inner ℝ (K u) v)= -‖u‖^2+‖v‖^2 := by
    rw [norm_sub_sq_real,norm_add_sq_real,map_sub,inner_sub_left,
      inner_add_right,inner_add_right,hDiagL,hDiagR,hKΓ,hSwap2,hSwap]
    nlinarith only [hEnergy u,hEnergy v,hMixed u v]
