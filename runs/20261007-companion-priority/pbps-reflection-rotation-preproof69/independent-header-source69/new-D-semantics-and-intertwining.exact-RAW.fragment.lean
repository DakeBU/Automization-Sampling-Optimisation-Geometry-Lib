                          let D : Hperp →L[ℝ] Hperp :=
                            R ∘L U.toContinuousLinearMap ∘L Hperp.subtypeL
                          (∀ h : Hperp, (D h : Lp ℝ 2 J)=
                            U (h : Lp ℝ 2 J)-P (U (h : Lp ℝ 2 J))) ∧
                          V0.adjoint ∘L D = -(A0 ∘L V0.adjoint) ∧
