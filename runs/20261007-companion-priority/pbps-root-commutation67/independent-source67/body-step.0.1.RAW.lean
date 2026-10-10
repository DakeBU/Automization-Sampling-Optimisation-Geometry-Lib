  have hReal (u : Lp ℝ 2 μ) : G (G (D u)) = D (G (G u)) :=
    congrArg (fun A : Lp ℝ 2 μ →L[ℝ] Lp ℝ 2 μ => A u) hCommute.eq
  have hComplex : Commute (Gc*Gc) Dc := by
    apply ContinuousLinearMap.ext
    intro g
    change Gc (Gc (Dc g)) = Dc (Gc (Gc g))
    calc
      Gc (Gc (Dc g)) = ι (G (G (D (R g)))) + Complex.I • ι (G (G (D (Q g)))) := by
        rw [hDf g, map_add, map_smul, hGi, hGi, map_add, map_smul, hGi, hGi]
      _ = ι (D (G (G (R g)))) + Complex.I • ι (D (G (G (Q g)))) := by
        rw [hReal (R g),hReal (Q g)]
      _ = Dc (Gc (Gc g)) := by
        rw [hGf g,map_add,map_smul,hGi,hGi,map_add,map_smul,hDi,hDi]
