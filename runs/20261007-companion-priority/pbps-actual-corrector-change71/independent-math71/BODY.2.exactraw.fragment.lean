  let K : HP0 →L[ℝ] HP0 := A0 ∘L Inv
  have hInvΓ (u : HP0) : Inv (ΓP0 u)=u := by
    have h := DFunLike.congr_fun hLeft u
    simpa only [ContinuousLinearMap.mul_apply,ContinuousLinearMap.one_apply] using h
  have hΓInv (u : HP0) : ΓP0 (Inv u)=u := by
    have h := DFunLike.congr_fun hRight u
    simpa only [ContinuousLinearMap.mul_apply,ContinuousLinearMap.one_apply] using h
  have hCommEval (u : HP0) : A0 (ΓP0 u)=ΓP0 (A0 u) :=
    DFunLike.congr_fun hComm0.eq u
  have hCommInvEval (u : HP0) : A0 (Inv u)=Inv (A0 u) :=
    DFunLike.congr_fun hCommInv.eq u
  have hKΓ (u : HP0) : K (ΓP0 u)=A0 u := congrArg A0 (hInvΓ u)
  have hΓK (u : HP0) : ΓP0 (K u)=A0 u := by
    change ΓP0 (A0 (Inv u))=A0 u
    calc
      ΓP0 (A0 (Inv u))=A0 (ΓP0 (Inv u)) := (hCommEval (Inv u)).symm
      _ = A0 u := congrArg A0 (hΓInv u)
  have hKA (u : HP0) : K (A0 u)=A0 (K u) := by
    change A0 (Inv (A0 u))=A0 (A0 (Inv u))
    exact congrArg A0 (hCommInvEval u).symm
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
