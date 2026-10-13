  have ha0 : 0 < (α : ℝ)*η := mul_pos hα hη
  have ha1 : (α : ℝ)*η ≤ 1 :=
    (mul_le_mul_of_nonneg_right (by exact_mod_cast hαβ) hη.le).trans hβη
  have hd : 0 < 1+(α : ℝ)*η := by positivity
  let ρ : ℝ := (1-(α : ℝ)*η)/(1+(α : ℝ)*η)
  let γ : ℝ := 2*Real.sqrt ((α : ℝ)*η)/(1+(α : ℝ)*η)
  have hρ : 0 ≤ ρ := div_nonneg (sub_nonneg.mpr ha1) hd.le
  have hγ : 0 < γ := by dsimp [γ]; positivity
  have hγSq : γ^2=1-ρ^2 := by
    dsimp [γ,ρ]
    rw [div_pow,mul_pow,Real.sq_sqrt ha0.le]
    field_simp [ne_of_gt hd]
    ring
  have hCon (u : Lp ℝ 2 ν) (hu : (∫ y,u y ∂ν)=0) : ‖T u‖ ≤ ρ*‖u‖ := by
    obtain ⟨hPair,_,_,_,hSharp,_⟩ := hRough u
    let z : G.closure.domain := ⟨T u,G.closure.mem_domain_of_mem_graph hPair⟩
    have hz : (∫ x,(z : Lp ℝ 2 ν) x ∂ν)=0 := (hAll u).2.2.trans hu
    have hK : G.closure z=K u := G.closure.mem_graph_snd_inj (G.closure.mem_graph z) hPair rfl
    have hC3 := hPI z hz
    change ((α : ℝ)/(1+(α : ℝ)*η))*‖T u‖^2 ≤ ‖G.closure z‖^2 at hC3
    rw [hK] at hC3
    have hP : (α : ℝ)*‖T u‖^2 ≤ (1+(α : ℝ)*η)*‖K u‖^2 := by
      calc
        _ ≤ ‖K u‖^2*(1+(α : ℝ)*η) :=
          (div_le_iff₀ hd).mp (by simpa only [div_mul_eq_mul_div] using hC3)
        _ = _ := mul_comm _ _
    have hs : η*‖K u‖^2 ≤
        ((1-(α : ℝ)*η)^2*(‖u‖^2-‖T u‖^2))/(4*(1+(α : ℝ)*η)) := by
      simpa only [div_mul_eq_mul_div] using hSharp
    have hs' := (le_div_iff₀ (show 0<4*(1+(α : ℝ)*η) from by positivity)).mp hs
    have hSharp' : 4*(1+(α : ℝ)*η)*η*‖K u‖^2 ≤
        (1-(α : ℝ)*η)^2*(‖u‖^2-‖T u‖^2) := by nlinarith [hs']
    have hSq : (1+(α : ℝ)*η)^2*‖T u‖^2 ≤ (1-(α : ℝ)*η)^2*‖u‖^2 := by
      nlinarith [mul_le_mul_of_nonneg_left hP (show 0≤4*η from by positivity)]
    have hSq' : ‖T u‖^2 ≤ (ρ*‖u‖)^2 := by
      dsimp [ρ]
      rw [mul_pow,div_pow,div_mul_eq_mul_div]
      apply (le_div_iff₀ (sq_pos_of_pos hd)).2
      nlinarith [hSq]
    exact (sq_le_sq₀ (norm_nonneg _) (mul_nonneg hρ (norm_nonneg _))).mp hSq'
