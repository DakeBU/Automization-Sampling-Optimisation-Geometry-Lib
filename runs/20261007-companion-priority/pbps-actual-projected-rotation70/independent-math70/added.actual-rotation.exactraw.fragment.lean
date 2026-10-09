 ∧
                              let g : Lp ℝ 2 J := U (P f-(f-P f))
                              (∫ z, g z ∂J)=0 ∧
                              ∃ gP : HP0,
                                HP0.subtypeL gP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le g ∧
                                let gperp : Hperp := R g
                                let gV : HP0 := V0.adjoint gperp
                                gP=A0 fP-ΓP0 fV ∧
                                gV=ΓP0 fP+A0 fV ∧
                                ‖gP‖^2+‖gV‖^2=‖fP‖^2+‖fV‖^2)
