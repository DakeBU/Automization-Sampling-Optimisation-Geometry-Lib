  have hSquareApply (u : HP0) : A0 (A0 u)+ΓP0 (ΓP0 u)=u := by
    have h := DFunLike.congr_fun hSquare0 u
    simpa only [ContinuousLinearMap.add_apply,ContinuousLinearMap.mul_apply,
      ContinuousLinearMap.one_apply] using h
  have hKMixedVector (u : HP0) : A0 (K (A0 u))+ΓP0 (A0 u)=K u := by
    calc
      A0 (K (A0 u))+ΓP0 (A0 u)=K (A0 (A0 u))+K (ΓP0 (ΓP0 u)) :=
        congrArg₂ (fun x y : HP0 => x+y) (hKA (A0 u)).symm
          ((hCommEval u).symm.trans (hKΓ (ΓP0 u)).symm)
      _ = K (A0 (A0 u)+ΓP0 (ΓP0 u)) := (K.map_add _ _).symm
      _ = K u := congrArg K (hSquareApply u)
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
