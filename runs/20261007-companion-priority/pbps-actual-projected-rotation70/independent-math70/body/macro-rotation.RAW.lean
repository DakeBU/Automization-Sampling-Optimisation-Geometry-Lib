        _ = inner ℝ (P (ι u)) g := (hPself.isSymmetric _ _).symm
        _ = inner ℝ (ι u) g := by rw [hPι]
        _ = inner ℝ (U (ι u)) (ι fP-(fperp : Lp ℝ 2 J)) := by
          change inner ℝ (ι u) (U (P f-(f-P f)))=_
          rw [hInput]
          exact (hUs.isSymmetric _ _).symm
        _ = inner ℝ (A0 u) fP-inner ℝ (B0 u) fperp := by
          rw [hUι,inner_add_left,inner_sub_right,inner_sub_right,
            hOrth (A0 u) fperp,
            show inner ℝ (B0 u : Lp ℝ 2 J) (ι fP)=0 from
              (real_inner_comm _ _).trans (hOrth fP (B0 u))]
          change (inner ℝ (A0 u) fP-0)+(0-inner ℝ (B0 u) fperp)=_
          ring
        _ = inner ℝ u (A0 fP)-inner ℝ u (ΓP0 fV) := by
          have ha : inner ℝ (A0 u) fP=inner ℝ u (A0 fP) := hA0self.isSymmetric u fP
          have hb : inner ℝ (B0 u) fperp=inner ℝ u (ΓP0 fV) :=
            (B0.adjoint_inner_right u fperp).symm.trans
              (congrArg (fun z : HP0 => inner ℝ u z) hB0adjMicro)
          exact congrArg₂ (fun x y : ℝ => x-y) ha hb
        _ = inner ℝ u (A0 fP-ΓP0 fV) := (inner_sub_right _ _ _).symm
    have hgVformula : V0.adjoint (R g)=ΓP0 fP+A0 fV := by
      change V0.adjoint (R (U (P f-(f-P f))))=_
      rw [hInput,map_sub,map_sub,hRUm,map_sub,hVadjB]
      have hd := DFunLike.congr_fun hIntertwine fperp
      change V0.adjoint (D fperp)= -(A0 fV) at hd
      change ΓP0 fP-V0.adjoint (D fperp)=_
      rw [hd,sub_neg_eq_add]
