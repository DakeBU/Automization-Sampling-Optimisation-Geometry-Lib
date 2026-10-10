  have hBAdj : B0.adjoint=ΓP0 ∘L V0.adjoint := by
    calc
      B0.adjoint = (V0 ∘L ΓP0).adjoint :=
        congrArg (fun C : HP0 →L[ℝ] Hperp => C.adjoint) hFactor
      _ = ΓP0.adjoint ∘L V0.adjoint := ContinuousLinearMap.adjoint_comp V0 ΓP0
      _ = ΓP0 ∘L V0.adjoint :=
        congrArg (fun C : HP0 →L[ℝ] HP0 => C ∘L V0.adjoint)
          hPosLocal.isSelfAdjoint.adjoint_eq
