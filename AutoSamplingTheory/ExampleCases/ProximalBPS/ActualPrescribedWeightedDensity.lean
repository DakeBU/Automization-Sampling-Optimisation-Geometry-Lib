import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathReversal
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival

/-!
# Actual prescribed PBPS weighted density

Faithful restatement of the pointwise weighted-density step in Appendix A.1
(Eqs. A7/A8) of arXiv:2609.06905v1, using the target energy of Eq. 3.1.
The original six analytic assumptions and actual density definitions are retained.
This is an unnormalized pointwise identity, not Gibbs invariance or an integral
change-of-variables theorem. The proof uses four public actual-path producers.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedWeightedDensity
open MeasureTheory InnerProductSpace
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false

/-- Literal sealed actual dynamics, densities and both weighted identities. -/
private def actual_prescribed_weighted_density_statement
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
    let P : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ :=
      fun y r z n T t => ∏ i : Fin n,
        rate r (Φ y r (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n+1) → ℝ) i.castSucc)
          (zAt y r z n T t i.castSucc))
    let I : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ :=
      fun y r z n T t => ∫ s in (0 : ℝ)..(T : ℝ),
        rate r (Γ y r z n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩)
    let dReal : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ :=
      fun y r z n T t => Real.exp (-I y r z n T t) * P y r z n T t
    ∀ n : ℕ, ∀ T : ℝ≥0, ∃ rho : Prefix n T → Prefix n T,
      (∀ t : Prefix n T, ∀ i : Fin n, (rho t).val i = (T : ℝ) - t.val i.rev) ∧
      ∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        let A : E × E := Γ y r z n T t ⟨T, le_rfl⟩
        w y z * dReal y r z n T t = w y (R A) * dReal y r (R A) n T (rho t) ∧
        ENNReal.ofReal (w y z) * ρ y r z n T t =
          ENNReal.ofReal (w y (R A)) * ρ y r (R A) n T (rho t)


/-- Weight matching under event-time and terminal momentum reversal. -/
theorem actual_prescribed_weighted_density_balance
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_prescribed_weighted_density_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_prescribed_weighted_density_statement
  intro c Φ S rate Λ Rec Hist Δ Prefix zAt K qReal q liveTime d weight Path Ψ Γ ρ R U w P I dReal n T
  obtain ⟨rho, hrho, h100⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathReversal.actual_prescribed_path_reversal_and_survival
      hα hαβ hV hH hη hβη n T
  obtain ⟨rho99, hrho99, h99⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal.actual_prescribed_state_reversal_and_rate_product
      hα hαβ hV hH hη hβη n T
  -- The public coordinate equations identify the independently produced witnesses.
  have halign : rho99 = rho := by
    funext t
    apply Subtype.ext
    funext i
    exact (hrho99 t i).trans (hrho t i).symm
  subst rho99
  refine ⟨rho, hrho, ?_⟩
  intro y r z t A
  -- Incoming rates, including zero factors, pair under finite state reversal.
  have hprod : P y r (R A) n T (rho t) = P y r z n T t := by
    simpa only [P, Fin.succ_castSucc, Fin.snoc_castSucc, Fin.cons_succ] using
      (h99 y r z t).2
  -- The reversed survival integral equals the momentum-flipped forward integral.
  have hint : I y r (R A) n T (rho t) =
      ∫ s in (0 : ℝ)..(T : ℝ), rate r (R (Γ y r z n T t
        ⟨min (Real.toNNReal s) T, min_le_right _ _⟩)) :=
    (h100 y r z t).2.2.2
  -- Gibbs survival balance and invariance of target energy under momentum flip.
  have hbal :=
    (AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival.actual_prescribed_gibbs_survival_balance
      hα hαβ hV hH hη hβη y r z n T t).2.2.2
  have hw : w y (R A) = w y A := by simp only [w, U, R, norm_neg]
  have hs : w y z * Real.exp (-I y r z n T t) =
      w y (R A) * Real.exp (-I y r (R A) n T (rho t)) := by
    rw [hw, hint]
    exact hbal
  -- Multiply by the common event product; no rate cancellation is used.
  have hreal : w y z * dReal y r z n T t =
      w y (R A) * dReal y r (R A) n T (rho t) := by
    dsimp only [dReal]
    rw [hprod, ← mul_assoc, ← mul_assoc, hs]
  refine ⟨hreal, ?_⟩
  -- Reconnect both real densities to the original algorithmic ENNReal density.
  have hd (a : E × E) (u : Prefix n T) :
      ρ y r a n T u = ENNReal.ofReal (dReal y r a n T u) := by
    simpa only [dReal, I, P, Fin.snoc_castSucc] using
      (AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite
      hα hαβ hV hH hη hβη y r a n T u).2.2.2
  rw [hd z t, hd (R A) (rho t), ← ENNReal.ofReal_mul (Real.exp_nonneg _),
    ← ENNReal.ofReal_mul (Real.exp_nonneg _), hreal]

#print axioms actual_prescribed_weighted_density_balance
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedWeightedDensity
