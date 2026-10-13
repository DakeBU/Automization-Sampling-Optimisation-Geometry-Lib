import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity

/-! Actual finite prescribed PBPS path reversal away from internal jumps and
survival-integral substitution. Faithful mathematical restatement of the
Appendix A.1 reversal component in arXiv:2609.06905v1. This module does not
establish the weighted path law or stationary invariance. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathReversal
open MeasureTheory Set InnerProductSpace
open scoped ContDiff NNReal ENNReal Classical Interval
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2400000

private theorem active_arc (n : ℕ) (a : Fin (n+1) → ℝ) (ha : a 0 = 0)
    (s : ℝ) (hs : 0 ≤ s) :
    ∃ j, a j ≤ s ∧ ∀ k, j < k → s < a k := by
  let q : Finset (Fin (n+1)) := Finset.univ.filter (fun j => a j ≤ s)
  have hq : q.Nonempty := ⟨0, by simp [q, ha, hs]⟩
  refine ⟨q.max' hq, (Finset.mem_filter.mp (Finset.max'_mem q hq)).2, ?_⟩
  intro k hk
  by_contra h
  have hm : k ∈ q := by simp [q, le_of_not_gt h]
  exact (not_le_of_gt hk) (Finset.le_max' q k hm)

private theorem path_reversal {X : Type*} (n : ℕ) (T : ℝ)
    (a b : Fin (n+2) → ℝ) (ha : Monotone a)
    (hb0 : b 0 = 0) (hbT : b (Fin.last (n+1)) = T)
    (hbl : ∀ j : Fin (n+1), b j.castSucc = T - a j.rev.succ)
    (hbr : ∀ j : Fin (n+1), b j.succ = T - a j.rev.castSucc)
    (Φ : ℝ → X → X) (R : X → X) (hR : Function.Involutive R)
    (hgroup : ∀ u v x, Φ (u+v) x = Φ u (Φ v x))
    (hrev : ∀ u x, R (Φ u (R x)) = Φ (-u) x)
    (post barPost : Fin (n+1) → X) (f g : ℝ → X)
    (hstate : ∀ j, barPost j =
      R (Φ (a j.rev.succ - a j.rev.castSucc) (post j.rev)))
    (hf : ∀ s, 0 ≤ s → s ≤ T → ∀ j : Fin (n+1),
      a j.castSucc ≤ s → (∀ k, j < k → s < a k.castSucc) →
      f s = Φ (s-a j.castSucc) (post j))
    (hg : ∀ s, 0 ≤ s → s ≤ T → ∀ j : Fin (n+1),
      b j.castSucc ≤ s → (∀ k, j < k → s < b k.castSucc) →
      g s = Φ (s-b j.castSucc) (barPost j)) :
    ∀ s, 0 ≤ s → s ≤ T → (∀ i : Fin n, s ≠ b i.succ.castSucc) →
      g s = R (f (T-s)) := by
  intro s hs0 hsT hne
  obtain ⟨j, hj, hjafter⟩ := active_arc n (fun j => b j.castSucc) (by simpa using hb0) s hs0
  have hnext : s ≤ b j.succ := by
    induction j using Fin.lastCases with
    | last => simpa only [Fin.succ_last, hbT] using hsT
    | cast i =>
      simpa only [Fin.succ_castSucc] using (hjafter i.succ Fin.castSucc_lt_succ).le
  have hstart : a j.rev.castSucc ≤ T-s := by
    rw [hbr] at hnext
    linarith
  have hafter : ∀ k : Fin (n+1), j.rev < k → T-s < a k.castSucc := by
    intro k hk
    have hstrict : b j.castSucc < s := by
      induction j using Fin.cases with
      | zero => simpa only [Fin.rev_zero, not_lt_of_ge (Fin.le_last k)] using hk
      | succ i => exact lt_of_le_of_ne hj (hne i).symm
    have hidx : j.rev.succ ≤ k.castSucc := by
      exact_mod_cast hk
    have ham := ha hidx
    rw [hbl] at hstrict
    linarith
  have hRR (x : X) : R (R x) = x := hR x
  have hc (u : ℝ) (x : X) : Φ u (R x) = R (Φ (-u) x) := by
    simpa only [hRR] using congrArg R (hrev u x)
  rw [hg s hs0 hsT j hj hjafter,
    hf (T-s) (sub_nonneg.mpr hsT) (by linarith) j.rev hstart hafter,
    hstate, hc, ← hgroup]
  congr 2
  rw [hbl]
  ring

private theorem scalar_reflection (T : ℝ) (hT : 0 ≤ T) (f g : ℝ → ℝ)
    (N : Set ℝ) (hN : N.Finite)
    (he : ∀ s ∈ Icc 0 T, s ∉ N → g s = f (T-s))
    (hg : IntervalIntegrable g volume 0 T) :
    IntervalIntegrable f volume 0 T ∧
      (∫ s in (0 : ℝ)..T, g s) = ∫ s in (0 : ℝ)..T, f s := by
  have hae : g =ᵐ[volume.restrict (Ι (0 : ℝ) T)] (fun s => f (T-s)) := by
    filter_upwards [ae_restrict_mem measurableSet_uIoc,
      hN.countable.ae_notMem (volume.restrict (Ι (0 : ℝ) T))] with s hs hn
    rw [uIoc_of_le hT] at hs
    exact he s ⟨hs.1.le, hs.2⟩ hn
  have hi : IntervalIntegrable (fun s => f (T-s)) volume 0 T := hg.congr_ae hae
  have hf : IntervalIntegrable f volume 0 T := by
    simpa using (hi.comp_sub_left T).symm
  refine ⟨hf, ?_⟩
  rw [intervalIntegral.integral_congr_ae_restrict hae]
  simpa using intervalIntegral.integral_comp_sub_left f T (a := (0 : ℝ)) (b := T)

set_option linter.unusedVariables false in
private def actual_prescribed_path_reversal_statement
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
    let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
    let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
    let Δ : (n : ℕ) → ℝ≥0 → Set (Fin n → ℝ) := fun n T =>
      {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < (T : ℝ)}
    let Prefix : (n : ℕ) → ℝ≥0 → Type := fun n T => {t : Fin n → ℝ // t ∈ Δ n T}
    let m : (n : ℕ) → (T : ℝ≥0) → Measure (Prefix n T) := fun n T =>
      Measure.comap (fun t : Prefix n T => t.val) (volume : Measure (Fin n → ℝ))
    let zAt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Fin (n + 1) → (E × E) := fun y xRef z₀ n T t =>
      Fin.induction z₀ (fun i z =>
        S xRef (Φ y xRef (t.val i - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc) z))
    let K : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) →
        Prefix n T → Hist n := fun y xRef z₀ n T t j =>
      Sum.inl (Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) j), zAt y xRef z₀ n T t j)
    let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
    let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
      fun y xRef z₀ n T h s =>
        Fin.foldl (n + 1) (fun z j => (h j).elim
          (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
          (fun _ => z)) z₀
    let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
      fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
    let R : E × E → E × E := fun z => (z.1, -z.2)
    let rate : E → E × E → ℝ := fun r z =>
      Real.sqrt η * max 0 (inner ℝ z.2 (gradient V z.1 - gradient V r))
    ∀ n : ℕ, ∀ T : ℝ≥0, ∃ rho : Prefix n T → Prefix n T,
      (∀ t : Prefix n T, ∀ i : Fin n, (rho t).val i = (T : ℝ) - t.val i.rev) ∧
      ∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        let A : E × E := Γ y r z n T t ⟨T, le_rfl⟩
        let gamma : ℝ → E × E := fun s =>
          Γ y r z n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
        let barGamma : ℝ → E × E := fun s =>
          Γ y r (R A) n T (rho t) ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
        (∀ s : ℝ, 0 ≤ s → s ≤ (T : ℝ) →
          (∀ i : Fin n, s ≠ (rho t).val i) →
          barGamma s = R (gamma ((T : ℝ) - s))) ∧
        IntervalIntegrable (fun s => rate r (barGamma s)) volume 0 (T : ℝ) ∧
        IntervalIntegrable (fun s => rate r (R (gamma s))) volume 0 (T : ℝ) ∧
        (∫ s in (0 : ℝ)..(T : ℝ), rate r (barGamma s)) =
          ∫ s in (0 : ℝ)..(T : ℝ), rate r (R (gamma s))


theorem actual_prescribed_path_reversal_and_survival
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_prescribed_path_reversal_statement hα hαβ hV hH hη hβη := by
  classical
  unfold actual_prescribed_path_reversal_statement
  intro c Φ S Rec Hist Δ Prefix m zAt K Path Ψ Γ R rate n T
  obtain ⟨rho, hrho, h99⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal.actual_prescribed_state_reversal_and_rate_product
      hα hαβ hV hH hη hβη n T
  refine ⟨rho, hrho, ?_⟩
  intro y r z t A gamma barGamma
  let grid : Fin (n+2) → ℝ := Fin.snoc (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n+1) → ℝ) (T : ℝ)
  let barGrid : Fin (n+2) → ℝ := Fin.snoc (Fin.cons (0 : ℝ) (rho t).val) (T : ℝ)
  let post := zAt y r z n T t
  let barPost := zAt y r (R A) n T (rho t)
  have hpair : ∀ j : Fin (n+1), barPost j =
      R (Φ y r (grid j.rev.succ-grid j.rev.castSucc) (post j.rev)) :=
    fun j => ((h99 y r z t).1 j).1
  have hbl (j : Fin (n+1)) : barGrid j.castSucc = (T : ℝ) - grid j.rev.succ := by
    induction j using Fin.cases with
    | zero => simp [grid, barGrid]
    | succ i => simp only [grid, barGrid, Fin.rev_succ, Fin.succ_castSucc,
        Fin.snoc_castSucc, Fin.cons_succ, hrho]
  have hbr (j : Fin (n+1)) : barGrid j.succ = (T : ℝ) - grid j.rev.castSucc := by
    induction j using Fin.lastCases with
    | last => simp [grid, barGrid]
    | cast i => simp only [grid, barGrid, Fin.rev_castSucc, Fin.succ_castSucc,
        Fin.snoc_castSucc, Fin.cons_succ, hrho]
  have hgrid : Monotone grid := by
    have htT : ∀ j : Fin (n+1), (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n+1) → ℝ) j ≤ (T : ℝ) := by
      intro j
      refine Fin.cases ?_ (fun i => ?_) j
      · simpa using T.coe_nonneg
      · exact (t.property.2 i).le
    intro i j hij
    induction i using Fin.lastCases with
    | last =>
      have hj : j = Fin.last (n+1) := le_antisymm (Fin.le_last j) hij
      subst j
      exact le_rfl
    | cast i =>
      induction j using Fin.lastCases with
      | last => simpa [grid] using htT i
      | cast j => simpa [grid] using t.property.1.monotone (show i ≤ j from hij)
  obtain ⟨Z, _, _, _, _, hlaw⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law
      hα hαβ hV hH hη hβη
  have harc (w : E × E) (u : Prefix n T) (s : ℝ) (hs0 : 0 ≤ s) (hsT : s ≤ (T : ℝ))
      (j : Fin (n+1)) (hj : (Fin.cons (0 : ℝ) (u.val : Fin n → ℝ) : Fin (n+1) → ℝ) j ≤ s)
      (hn : ∀ k : Fin (n+1), j < k → s < (Fin.cons (0 : ℝ) (u.val : Fin n → ℝ) : Fin (n+1) → ℝ) k) :
      Γ y r w n T u ⟨min (Real.toNNReal s) T, min_le_right _ _⟩ =
        Φ y r (s - (Fin.cons (0 : ℝ) (u.val : Fin n → ℝ) : Fin (n+1) → ℝ) j) (zAt y r w n T u j) := by
    have hclip : min (Real.toNNReal s) T = Real.toNNReal s :=
      min_eq_left (by exact_mod_cast (Real.toNNReal_le_iff_le_coe).2 hsT)
    have hcoe : ((min (Real.toNNReal s) T : ℝ≥0) : ℝ) = s := by
      rw [hclip, Real.coe_toNNReal s hs0]
    have hp := ((hlaw n T).2.2.2 y r w).2.2.2.2.1
      u ⟨min (Real.toNNReal s) T, min_le_right _ _⟩ j
      (by simpa only [hcoe] using hj) (by simpa only [hcoe] using hn)
    change Γ y r w n T u ⟨min (Real.toNNReal s) T, min_le_right _ _⟩ =
      Φ y r (((min (Real.toNNReal s) T : ℝ≥0) : ℝ) - (Fin.cons (0 : ℝ) (u.val : Fin n → ℝ) : Fin (n+1) → ℝ) j)
        (zAt y r w n T u j) at hp
    simpa only [hcoe] using hp
  obtain ⟨_, _, _, hgroup, _⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws
      hα hαβ hV hH hη hβη
  obtain ⟨_, _, _, _, _, _, _, _, hR, hrev, _⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws
      hα hαβ hV hH hη hβη
  have hoff : ∀ s : ℝ, 0 ≤ s → s ≤ (T : ℝ) →
      (∀ i : Fin n, s ≠ (rho t).val i) → barGamma s = R (gamma ((T : ℝ)-s)) := by
    have hp := path_reversal n (T : ℝ) grid barGrid hgrid
      (by simp [barGrid]) (by simp [barGrid]) hbl hbr (Φ y r) R hR
      (hgroup y r) (hrev y r) post barPost gamma barGamma hpair
      (fun s hs0 hsT j hj hn => by
        simpa only [gamma, grid, post, Fin.snoc_castSucc] using
          harc z t s hs0 hsT j (by simpa only [grid, Fin.snoc_castSucc] using hj)
            (by simpa only [grid, Fin.snoc_castSucc] using hn))
      (fun s hs0 hsT j hj hn => by
        simpa only [barGamma, barGrid, barPost, Fin.snoc_castSucc] using
          harc (R A) (rho t) s hs0 hsT j (by simpa only [barGrid, Fin.snoc_castSucc] using hj)
            (by simpa only [barGrid, Fin.snoc_castSucc] using hn))
    intro s hs0 hsT hn
    exact hp s hs0 hsT (by simpa only [barGrid, Fin.snoc_castSucc, Fin.cons_succ] using hn)
  have hi : IntervalIntegrable (fun s => rate r (barGamma s)) volume 0 (T : ℝ) :=
    (AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite
      hα hαβ hV hH hη hβη y r (R A) n T (rho t)).1
  have hs := scalar_reflection (T : ℝ) T.coe_nonneg
    (fun s => rate r (R (gamma s))) (fun s => rate r (barGamma s))
    (Set.range (rho t).val) (Set.finite_range _) (by
      intro s hs hn
      exact congrArg (rate r) (hoff s hs.1 hs.2 (fun i he => hn ⟨i, he.symm⟩))) hi
  exact ⟨hoff, hi, hs⟩

#print axioms actual_prescribed_path_reversal_and_survival

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathReversal
