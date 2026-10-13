import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualWeightedSector
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization

/-!
# Actual normalized endpoint-pair sector reversal

The fixed-count reversal and Gibbs averaging in arXiv:2609.06905v1,
Appendix A.1, with phase normalization from Eq. (3.1) made explicit.
The actual event density and deterministic endpoint map define a sector measure;
the flipped endpoint swap preserves its pushforward. This proves one fixed-count
measure identity, not countable assembly or process invariance.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

set_option linter.unusedVariables false in
private def actual_normalized_endpoint_sector_statement
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : Prop := by
  classical
  exact
    let c : E → E → E := fun y xRef => y - η • gradient V xRef
    let Φ : E → E → ℝ → (E × E) → (E × E) := fun y xRef t z =>
      (c y xRef + Real.cos t • (z.1 - c y xRef) +
          (Real.sqrt η * Real.sin t) • z.2,
       (-Real.sin t / Real.sqrt η) • (z.1 - c y xRef) + Real.cos t • z.2)
    let S : E → (E × E) → (E × E) := fun xRef z =>
      (z.1, z.2 - (2 * inner ℝ z.2 (gradient V z.1 - gradient V xRef) /
        ‖gradient V z.1 - gradient V xRef‖ ^ 2) • (gradient V z.1 - gradient V xRef))
    let rate : E → (E × E) → ℝ := fun xRef z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (gradient V z.1 - gradient V xRef))
    let Λ : E → E → (E × E) → ℝ≥0 → ℝ := fun y xRef z t =>
      ∫ s in (0 : ℝ)..(t : ℝ), rate xRef (Φ y xRef s z)
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
      {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
    let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
    let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
      Fin.induction z₀ (fun i z =>
        S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
    let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Hist n := fun y xRef z₀ n T t j =>
      Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
    let qReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ := fun y xRef z₀ n T t =>
      ∏ i : Fin n,
        rate xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
          (zAt y xRef z₀ n T t i.castSucc)) *
        Real.exp (-Λ y xRef (zAt y xRef z₀ n T t i.castSucc)
          (Real.toNNReal (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)))
    let q : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → ℝ≥0∞ := fun y xRef z₀ n T t =>
      ENNReal.ofReal (qReal y xRef z₀ n T t)
    let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
    let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
      fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
    let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
      fun y xRef r u => r.elim
        (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
    let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
    let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
      fun y xRef z₀ n T h s =>
        Fin.foldl (n + 1) (fun z j => (h j).elim
          (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
          (fun _ => z)) z₀
    let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
      fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
    let ρ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ≥0∞ :=
      fun y xRef z₀ n T t => q y xRef z₀ n T t *
        weight y xRef ((K y xRef z₀ n T t) ⟨n, Nat.lt_succ_self n⟩)
          (d n T (K y xRef z₀ n T t))
    let R : E × E → E × E := fun z => (z.1, -z.2)
    let Vy : E → E → ℝ := fun y x => V x + ‖x - y‖ ^ 2 / (2 * η)
    let piY : E → Measure E := fun y => (volume : Measure E).tilted (fun x => -Vy y x)
    let gamma : Measure E := ProbabilityTheory.stdGaussian E
    let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
      Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
    ∀ y r : E, ∀ n : ℕ, ∀ T : ℝ≥0,
      let A : (E × E) × Prefix n T → E × E :=
        fun q => Γ y r q.1 n T q.2 ⟨T, le_rfl⟩
      let B : (E × E) × Prefix n T → (E × E) × (E × E) := fun q => (q.1, A q)
      let sigma : Measure ((E × E) × Prefix n T) :=
        (((piY y).prod gamma).prod (m n T)).withDensity (fun q => ρ y r q.1 n T q.2)
      let L : Measure ((E × E) × (E × E)) := Measure.map B sigma
      let J : (E × E) × (E × E) → (E × E) × (E × E) :=
        fun p => (R p.2, R p.1)
      MeasurePreserving J L L


set_option maxHeartbeats 1600000
set_option maxRecDepth 10000
/-- Momentum-flipped reversal preserves every actual normalized fixed-count endpoint-pair measure. -/
theorem actual_normalized_endpoint_sector_reversal
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_normalized_endpoint_sector_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_normalized_endpoint_sector_statement
  intro c Φ S rate Λ Rec Hist Δ Prefix zAt K qReal q liveTime d weight Path Ψ Γ ρ R Vy piY gamma m y r n T A B sigma L J
  obtain ⟨rhoTime, hrho, h97⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws
      hα hαβ hV hH hη hβη n T
  obtain ⟨rho102, hrho102, h102⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualWeightedSector.actual_weighted_sector_lintegral
      hα hαβ hV hH hη hβη n T
  have halign : rho102 = rhoTime := by
    funext t
    apply Subtype.ext
    funext i
    exact (hrho102 t i).trans (hrho t i).symm
  subst rho102
  rcases h97 with ⟨hTimeM, hTimeI, hTimeP, hAformula, hAjoint, hAvolume,
    hArev, hThetajoint, hThetaI, hThetaP⟩
  let Theta : (E × E) × Prefix n T → (E × E) × Prefix n T :=
    fun q => (R (A q), rhoTime q.2)
  have hemb : Measurable (fun q : (E × E) × Prefix n T => (((y, r), q.1), q.2)) :=
    (measurable_const.prodMk measurable_fst).prodMk measurable_snd
  have hA : Measurable A := hAjoint.comp hemb
  have hB : Measurable B := measurable_fst.prodMk hA
  have hR : Measurable R := measurable_fst.prodMk measurable_snd.neg
  have hJ : Measurable J := (hR.comp measurable_snd).prodMk (hR.comp measurable_fst)
  have hTheta : Measurable Theta := hThetajoint.comp hemb
  have hinter (x : (E × E) × Prefix n T) : B (Theta x) = J (B x) := by
    apply Prod.ext
    · rfl
    · exact hArev y r x.1 x.2
  obtain ⟨Z, hZ⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law
      hα hαβ hV hH hη hβη
  have hρjoint : Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
      ρ p.1.1.1 p.1.1.2 p.1.2 n T p.2) := (hZ.2.2.2.2 n T).2.2.1
  have hρ := hρjoint.comp hemb
  have hρliteral : Measurable (fun x : (E × E) × Prefix n T => ρ y r x.1 n T x.2) := by
    simpa only [Function.comp_def] using hρ
  have hcons (i : Fin (n + 1)) :
      Measurable (fun t : Fin n → ℝ => (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) i) := by
    induction i using Fin.cases with
    | zero => exact measurable_const
    | succ i => exact measurable_pi_apply i
  have hs : MeasurableSet (Δ n T) := by
    change MeasurableSet {t : Fin n → ℝ |
      (∀ i j : Fin (n + 1), i < j → (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) i < (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) j) ∧
      ∀ i : Fin n, t i < (T : ℝ)}
    rw [Set.ofPred_and]
    apply MeasurableSet.inter
    · simpa only [← Set.ofPred_forall] using (MeasurableSet.iInter fun (i : Fin (n + 1)) =>
        MeasurableSet.iInter fun (j : Fin (n + 1)) =>
        MeasurableSet.iInter fun (_ : i < j) => measurableSet_lt (hcons i) (hcons j))
    · simpa only [← Set.ofPred_forall] using (MeasurableSet.iInter fun (i : Fin n) =>
        measurableSet_lt (measurable_pi_apply i) (measurable_const (a := (T : ℝ))))
  have hmσ : SigmaFinite ((m n T).map (fun t : Prefix n T => t.val)) := by
    change SigmaFinite ((Measure.comap (fun t : Prefix n T => t.val)
      (volume : Measure (Fin n → ℝ))).map (fun t : Prefix n T => t.val))
    rw [map_comap_subtype_coe hs]
    infer_instance
  letI : SigmaFinite (m n T) := SigmaFinite.of_map (m n T) measurable_subtype_coe.aemeasurable hmσ
  let U : E × E → ℝ := fun z => V z.1 + ‖z.1 - y‖ ^ 2 / (2 * η) + ‖z.2‖ ^ 2 / 2
  let w : E × E → ℝ := fun z => Real.exp (-U z)
  let ell : Measure (E × E) := (volume : Measure E).prod (volume : Measure E)
  let cNorm : ℝ≥0∞ := (∫⁻ z, ENNReal.ofReal (w z) ∂ell)⁻¹
  let W : (E × E) × Prefix n T → ℝ≥0∞ :=
    fun x => ENNReal.ofReal (w x.1) * ρ y r x.1 n T x.2
  have hU : Continuous U := by
    exact ((hV.continuous.comp continuous_fst).add
      (((continuous_fst.sub continuous_const).norm.pow 2).div_const (2 * η))).add
      ((continuous_snd.norm.pow 2).div_const 2)
  have hw : Measurable (fun z => ENNReal.ofReal (w z)) :=
    ENNReal.measurable_ofReal.comp (Real.continuous_exp.comp hU.neg).measurable
  have hW : Measurable W := (hw.comp measurable_fst).mul hρ
  have hf : Measurable (fun z => cNorm * ENNReal.ofReal (w z)) := measurable_const.mul hw
  have hphase : ell.withDensity (fun z => cNorm * ENNReal.ofReal (w z)) =
      (piY y).prod gamma :=
    (AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization
      hα hαβ hV hH hη hβη y).2.2.2.2.2.2
  have hsigma : sigma = (ell.prod (m n T)).withDensity (fun x => cNorm * W x) := by
    change (((piY y).prod gamma).prod (m n T)).withDensity
      (fun x => ρ y r x.1 n T x.2) = _
    rw [← hphase, prod_withDensity_left hf,
      ← withDensity_mul _
        (f := fun x : (E × E) × Prefix n T => cNorm * ENNReal.ofReal (w x.1))
        (g := fun x => ρ y r x.1 n T x.2) (hf.comp measurable_fst) hρliteral]
    congr 1
    funext x
    exact mul_assoc _ _ _
  have hsector : MeasurePreserving Theta sigma sigma := by
    refine ⟨hTheta, ?_⟩
    apply Measure.ext_of_lintegral
    intro F hF
    rw [lintegral_map hF hTheta, hsigma]
    rw [lintegral_withDensity_eq_lintegral_mul _
        (f := fun x => cNorm * W x) (g := fun x => F (Theta x))
        (measurable_const.mul hW) (hF.comp hTheta),
      lintegral_withDensity_eq_lintegral_mul _
        (f := fun x => cNorm * W x) (g := fun x => F x)
        (measurable_const.mul hW) hF]
    simp only [Pi.mul_apply, mul_assoc]
    rw [lintegral_const_mul cNorm (f := fun x => W x * F (Theta x))
        (hW.mul (hF.comp hTheta)),
      lintegral_const_mul cNorm (f := fun x => W x * F x) (hW.mul hF)]
    exact congrArg (fun a => cNorm * a) (h102 y r F hF)
  refine ⟨hJ, ?_⟩
  change Measure.map J (Measure.map B sigma) = Measure.map B sigma
  rw [Measure.map_map hJ hB]
  calc
    Measure.map (J ∘ B) sigma = Measure.map (B ∘ Theta) sigma := by
      congr 1
      funext x
      exact (hinter x).symm
    _ = Measure.map B (Measure.map Theta sigma) := (Measure.map_map hB hTheta).symm
    _ = Measure.map B sigma := by rw [hsector.map_eq]

#print axioms actual_normalized_endpoint_sector_reversal
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector
