  have hPIBase :=
    AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare
      (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  dsimp only at hPIBase
  rcases hPIBase with ⟨_,G,_,hClose,hClosed,hGraph,hPI⟩
  have hRoughBase := RoughMeanGradient.actual_rough_mean_gradient
    (E:=E) (V:=V) (α:=α) (β:=β) (η:=η) hα hαβ hV hH hη hβη
  dsimp only at hRoughBase
  rcases hRoughBase with ⟨_,G',_,_,_,hGraph',Tr,K,hRough⟩
  have hSameG : G'=G := LinearPMap.eq_of_eq_graph (by
    ext p
    rcases p with ⟨u,v⟩
    exact (hGraph' u v).trans (hGraph u v).symm)
  subst G'
  have hSameT : Tr=T := by
    apply ContinuousLinearMap.ext
    intro u
    apply Lp.ext
    filter_upwards [(hRough u).2.2.1,(hAll u).2.1] with y hr ht
    exact hr.trans ((congrArg (fun m : Measure E => ∫ x,u x ∂m) (hSd y)).symm.trans ht.symm)
  subst Tr
