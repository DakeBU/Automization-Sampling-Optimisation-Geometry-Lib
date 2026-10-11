import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedWeightedDensity
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal

/-!
# Actual PBPS weighted finite-sector substitution

An attributed ASTIS completion of the unnormalized change-of-variables step
in Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1 (A7/A8),
with target energy Eq.3.1. The original six analytic assumptions are unchanged.
The actual joint density and endpoint/time reversal yield the identity for
all measurable nonnegative extended-real tests, explicitly extending the
printed bounded-test argument without a finite-integral claim.
Normalized Gibbs averaging, countable sector assembly, invariant probability,
restart/Markovness, hypocoercivity, implementation error and cost remain separate.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualWeightedSector
open MeasureTheory InnerProductSpace
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option maxRecDepth 10000

private def actual_weighted_sector_statement
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
    let U : E → E × E → ℝ := fun y z =>
      V z.1 + ‖z.1 - y‖ ^ 2 / (2 * η) + ‖z.2‖ ^ 2 / 2
    let w : E → E × E → ℝ := fun y z => Real.exp (-U y z)
    let ell : Measure (E × E) := (volume : Measure E).prod (volume : Measure E)
    let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
      Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
    ∀ n : ℕ, ∀ T : ℝ≥0, ∃ rho : Prefix n T → Prefix n T,
      (∀ t : Prefix n T, ∀ i : Fin n, (rho t).val i = (T : ℝ) - t.val i.rev) ∧
      ∀ y r : E,
        let A : (E × E) × Prefix n T → E × E :=
          fun q => Γ y r q.1 n T q.2 ⟨T, le_rfl⟩
        let Theta : (E × E) × Prefix n T → (E × E) × Prefix n T :=
          fun q => (R (A q), rho q.2)
        let W : (E × E) × Prefix n T → ℝ≥0∞ :=
          fun q => ENNReal.ofReal (w y q.1) * ρ y r q.1 n T q.2
        ∀ F : (E × E) × Prefix n T → ℝ≥0∞, Measurable F →
          (∫⁻ q, W q * F (Theta q) ∂(ell.prod (m n T))) =
            ∫⁻ q, W q * F q ∂(ell.prod (m n T))


/-- Actual unnormalized finite-sector weighted substitution. -/
theorem actual_weighted_sector_lintegral
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_weighted_sector_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_weighted_sector_statement
  intro c Φ S rate Λ Rec Hist Δ Prefix zAt K qReal q liveTime d weight Path Ψ Γ ρ R U w ell m n T
  obtain ⟨rho, hrho, h97⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws
      hα hαβ hV hH hη hβη n T
  obtain ⟨rho101, hrho101, h101⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedWeightedDensity.actual_prescribed_weighted_density_balance
      hα hαβ hV hH hη hβη n T
  have halign : rho101 = rho := by
    funext t
    apply Subtype.ext
    funext i
    exact (hrho101 t i).trans (hrho t i).symm
  subst rho101
  refine ⟨rho, hrho, ?_⟩
  intro y r A Theta W F hF
  have hTheta : MeasurePreserving Theta (ell.prod (m n T)) (ell.prod (m n T)) :=
    h97.2.2.2.2.2.2.2.2.2 y r
  have hbalance (q : (E × E) × Prefix n T) : W q = W (Theta q) :=
    (h101 y r q.1 q.2).2
  obtain ⟨Z, hZ⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law
      hα hαβ hV hH hη hβη
  have hρjoint : Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
      ρ p.1.1.1 p.1.1.2 p.1.2 n T p.2) := (hZ.2.2.2.2 n T).2.2.1
  have hemb : Measurable (fun q : (E × E) × Prefix n T => (((y, r), q.1), q.2)) :=
    ((measurable_const.prodMk measurable_fst).prodMk measurable_snd)
  have hρ := hρjoint.comp hemb
  have hU : Continuous (U y) := by
    exact ((hV.continuous.comp continuous_fst).add
      (((continuous_fst.sub continuous_const).norm.pow 2).div_const (2 * η))).add
      ((continuous_snd.norm.pow 2).div_const 2)
  have hw : Continuous (w y) := Real.continuous_exp.comp hU.neg
  have hW : Measurable W :=
    (ENNReal.measurable_ofReal.comp (hw.measurable.comp measurable_fst)).mul hρ
  calc
    (∫⁻ q, W q * F (Theta q) ∂(ell.prod (m n T))) =
        ∫⁻ q, W (Theta q) * F (Theta q) ∂(ell.prod (m n T)) := by
      apply lintegral_congr
      intro q
      rw [hbalance q]
    _ = ∫⁻ q, W q * F q ∂(ell.prod (m n T)) := hTheta.lintegral_comp (hW.mul hF)

#print axioms actual_weighted_sector_lintegral
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualWeightedSector
