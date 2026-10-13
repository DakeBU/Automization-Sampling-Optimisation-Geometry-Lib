  let hp : MeasurePreserving (Prod.snd : E × E → E) J ν := ⟨measurable_snd,rfl⟩
  let M : Lp ℝ 2 ν →ₗᵢ[ℝ] Lp ℝ 2 J := Lp.compMeasurePreservingₗᵢ ℝ Prod.snd hp
  have hqOne : (qP : Lp ℝ 2 J)=
      AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.one J := by
    rw [show (qP : Lp ℝ 2 J)=M q from he q]
    apply Lp.ext
    have hqaPull : (fun z : E × E => q z.2)=ᵐ[J] (fun _ => (1 : ℝ)) :=
      hp.quasiMeasurePreserving.ae hqa
    exact (Lp.coeFn_compMeasurePreserving q hp).trans
      (hqaPull.trans (Lp.coeFn_const (p:=(2 : ℝ≥0∞)) (μ:=J) (c:=(1 : ℝ))).symm)
  have hqIntegral (g : Lp ℝ 2 J) : inner ℝ (qP : Lp ℝ 2 J) g=∫ z, g z ∂J := by
    rw [hqOne]
    exact AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.inner_one_eq_integral J g
  have hPq : P (qP : Lp ℝ 2 J)=qP := hPf qP
