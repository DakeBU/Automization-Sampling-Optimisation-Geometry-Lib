import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath

/-! Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1:
finite prescribed-path hazard stitching, incoming limits and density rewrite.
The complete countable path-law sum and signed-observable convergence are separate. -/

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity

open MeasureTheory Set Filter
open scoped Topology


/-- Endpoint values may differ; open-arc agreement suffices for integration. -/
private theorem arc_integral {f g : ℝ → ℝ} {a b : ℝ} (hab : a ≤ b)
    (hg : Continuous g) (heq : EqOn f g (Ioo a b)) :
    IntervalIntegrable f volume a b ∧
      (∫ s in a..b, f s) = ∫ s in a..b, g s := by
  refine ⟨(hg.intervalIntegrable a b).congr_uIoo ?_,
    intervalIntegral.integral_congr_Ioo_of_le hab heq⟩
  rw [uIoo_of_le hab]
  exact heq.symm

/-- Agreement with the incoming continuous arc identifies the left limit. -/
private theorem incoming_left_limit {X : Type*} [TopologicalSpace X]
    {f g : ℝ → X} {a b : ℝ} (hab : a < b)
    (hg : Continuous g) (heq : EqOn f g (Ioo a b)) :
    Tendsto f (𝓝[<] b) (𝓝 (g b)) := by
  apply (hg.continuousAt.tendsto.mono_left nhdsWithin_le_nhds).congr'
  filter_upwards [Ioo_mem_nhdsLT hab] with s hs
  exact (heq hs).symm

/-- Finite adjacent arcs give integrability and the exact sum, even if some
    intervals have zero length. No agreement at the partition points is used. -/
private theorem finite_arc_integral (n : ℕ) (a : Fin (n + 1) → ℝ)
    (f : ℝ → ℝ) (g : Fin n → ℝ → ℝ) (ha : Monotone a)
    (hg : ∀ j, Continuous (g j))
    (heq : ∀ j, EqOn f (g j) (Ioo (a j.castSucc) (a j.succ))) :
    IntervalIntegrable f volume (a 0) (a (Fin.last n)) ∧
      (∫ s in a 0..a (Fin.last n), f s) =
        ∑ j : Fin n, ∫ s in a j.castSucc..a j.succ, g j s := by
  induction n with
  | zero => simp
  | succ n ih =>
    have hpre := ih (fun j => a j.castSucc) (fun j => g j.castSucc)
      (fun i j hij => ha (by simpa using hij)) (fun j => hg j.castSucc)
      (fun j => by simpa using heq j.castSucc)
    have hlast := arc_integral (ha (Fin.castSucc_le_succ (Fin.last n)))
      (hg (Fin.last n)) (heq (Fin.last n))
    refine ⟨hpre.1.trans hlast.1, ?_⟩
    rw [Fin.sum_univ_castSucc]
    simp only [Fin.succ_castSucc]
    rw [← hpre.2, ← hlast.2]
    exact (intervalIntegral.integral_add_adjacent_intervals hpre.1 hlast.1).symm



open MeasureTheory Set Filter
open scoped NNReal ENNReal Topology Classical

set_option maxRecDepth 4000
set_option maxHeartbeats 1600000

private theorem actual_arc
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
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
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ, ∀ T : ℝ≥0, ∀ t : Prefix n T,
      let grid : Fin (n + 2) → ℝ :=
        Fin.snoc (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ)) (T : ℝ)
      let γ : ℝ → E × E := fun s =>
        Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
      Monotone grid ∧ grid 0 = 0 ∧ grid (Fin.last (n+1)) = (T : ℝ) ∧
      ∀ j : Fin (n+1), EqOn γ
        (fun s => Φ y xRef (s - grid j.castSucc) (zAt y xRef z₀ n T t j))
        (Ioo (grid j.castSucc) (grid j.succ)) := by
  classical
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
  change
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ, ∀ T : ℝ≥0, ∀ t : Prefix n T,
      let grid : Fin (n + 2) → ℝ :=
        Fin.snoc (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ)) (T : ℝ)
      let γ : ℝ → E × E := fun s =>
        Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
      Monotone grid ∧ grid 0 = 0 ∧ grid (Fin.last (n+1)) = (T : ℝ) ∧
      ∀ j : Fin (n+1), EqOn γ
        (fun s => Φ y xRef (s - grid j.castSucc) (zAt y xRef z₀ n T t j))
        (Ioo (grid j.castSucc) (grid j.succ))
  intro y xRef z₀ n T t
  let a : Fin (n+1) → ℝ := Fin.cons 0 t.val
  let grid : Fin (n+2) → ℝ := Fin.snoc a (T : ℝ)
  let γ : ℝ → E × E := fun s =>
    Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
  change Monotone grid ∧ grid 0 = 0 ∧ grid (Fin.last (n+1)) = (T : ℝ) ∧ _
  have ham : StrictMono a := t.property.1
  have ha0 : a 0 = 0 := rfl
  have haT : ∀ j, a j ≤ (T : ℝ) := by
    intro j
    refine Fin.cases ?_ (fun i => ?_) j
    · simpa [a] using T.coe_nonneg
    · exact (t.property.2 i).le
  have hgrid : Monotone grid := by
    intro i j hij
    induction i using Fin.lastCases with
    | last =>
      have hj : j = Fin.last (n+1) := le_antisymm (Fin.le_last j) hij
      subst j
      exact le_rfl
    | cast i =>
      induction j using Fin.lastCases with
      | last => simpa [grid] using haT i
      | cast j => simpa [grid] using ham.monotone (show i ≤ j from hij)
  have hg0 : grid 0 = 0 := by simp [grid, a]
  have hgT : grid (Fin.last (n+1)) = (T : ℝ) := by simp [grid]
  refine ⟨hgrid, hg0, hgT, ?_⟩
  obtain ⟨Z, _, _, _, _, hlaw⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law
      hα hαβ hV hH hη hβη
  have harc := ((hlaw n T).2.2.2 y xRef z₀).2.2.2.2.1
  intro j s hs
  have hs0 : 0 ≤ s := by
    have := hgrid (show (0 : Fin (n+2)) ≤ j.castSucc from Fin.zero_le _)
    rw [hg0] at this
    exact (this.trans hs.1.le)
  have hsT : s ≤ (T : ℝ) := by
    have := hgrid (Fin.le_last j.succ)
    rw [hgT] at this
    exact hs.2.le.trans this
  have hclip : min (Real.toNNReal s) T = Real.toNNReal s :=
    min_eq_left (by exact_mod_cast (Real.toNNReal_le_iff_le_coe).2 hsT)
  have hclipcoe : ((min (Real.toNNReal s) T : ℝ≥0) : ℝ) = s := by
    rw [hclip, Real.coe_toNNReal s hs0]
  have hstart : a j ≤ s := by simpa [grid] using hs.1.le
  have hafter : ∀ k : Fin (n+1), j < k → s < a k := by
    intro k hjk
    have hidx : j.succ ≤ k.castSucc := by exact_mod_cast hjk
    have hle := hgrid hidx
    exact hs.2.trans_le (by simpa [grid] using hle)
  have hh := harc t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩ j
    (by simpa only [hclipcoe] using hstart)
    (by simpa only [hclipcoe] using hafter)
  simpa only [hclipcoe, Fin.snoc_castSucc] using hh


private theorem actual_analysis
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
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
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ, ∀ T : ℝ≥0, ∀ t : Prefix n T,
      let grid : Fin (n + 2) → ℝ :=
        Fin.snoc (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ)) (T : ℝ)
      let γ : ℝ → E × E := fun s =>
        Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
      IntervalIntegrable (fun s => rate xRef (γ s)) volume 0 (T : ℝ) ∧
      (∫ s in (0 : ℝ)..(T : ℝ), rate xRef (γ s)) =
        ∑ j : Fin (n + 1), Λ y xRef (zAt y xRef z₀ n T t j)
          (Real.toNNReal (grid j.succ - grid j.castSucc)) ∧
      (∀ i : Fin n,
        Tendsto γ (𝓝[<] (t.val i))
          (𝓝 (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))) ∧
        Tendsto (fun s => rate xRef (γ s)) (𝓝[<] (t.val i))
          (𝓝 (rate xRef (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))))) := by
  classical
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
  change
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ, ∀ T : ℝ≥0, ∀ t : Prefix n T,
      let grid : Fin (n + 2) → ℝ :=
        Fin.snoc (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ)) (T : ℝ)
      let γ : ℝ → E × E := fun s =>
        Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
      IntervalIntegrable (fun s => rate xRef (γ s)) volume 0 (T : ℝ) ∧
      (∫ s in (0 : ℝ)..(T : ℝ), rate xRef (γ s)) =
        ∑ j : Fin (n + 1), Λ y xRef (zAt y xRef z₀ n T t j)
          (Real.toNNReal (grid j.succ - grid j.castSucc)) ∧
      (∀ i : Fin n,
        Tendsto γ (𝓝[<] (t.val i))
          (𝓝 (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))) ∧
        Tendsto (fun s => rate xRef (γ s)) (𝓝[<] (t.val i))
          (𝓝 (rate xRef (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc)))))
  intro y xRef z₀ n T t
  let grid : Fin (n+2) → ℝ := Fin.snoc (Fin.cons (0 : ℝ) t.val) (T : ℝ)
  let γ : ℝ → E × E := fun s =>
    Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
  change IntervalIntegrable (fun s => rate xRef (γ s)) volume 0 (T : ℝ) ∧ _
  obtain ⟨hgrid, hg0, hgT, harc⟩ :=
    actual_arc hα hαβ hV hH hη hβη y xRef z₀ n T t
  change ∀ j : Fin (n+1), EqOn γ
    (fun s => Φ y xRef (s-grid j.castSucc) (zAt y xRef z₀ n T t j))
    (Ioo (grid j.castSucc) (grid j.succ)) at harc
  have hΦ : Continuous (fun a : (E × E) × ℝ × (E × E) =>
      Φ a.1.1 a.1.2 a.2.1 a.2.2) :=
    (AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws
      hα hαβ hV hH hη hβη).1
  have hRate : Continuous (fun a : E × (E × E) => rate a.1 a.2) :=
    (AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws
      hα hαβ hV hH hη hβη).2.1
  have hphase (j : Fin (n+1)) :
      Continuous (fun s : ℝ => Φ y xRef (s-grid j.castSucc) (zAt y xRef z₀ n T t j)) :=
    by
      have harg : Continuous (fun s : ℝ =>
          ((y,xRef), s-grid j.castSucc, zAt y xRef z₀ n T t j)) :=
        continuous_const.prodMk ((continuous_id.sub continuous_const).prodMk continuous_const)
      exact hΦ.comp harg
  have hr (j : Fin (n+1)) : Continuous (fun s : ℝ =>
      rate xRef (Φ y xRef (s-grid j.castSucc) (zAt y xRef z₀ n T t j))) :=
    hRate.comp (continuous_const.prodMk (hphase j))
  have heq (j : Fin (n+1)) : EqOn (fun s => rate xRef (γ s))
      (fun s => rate xRef (Φ y xRef (s-grid j.castSucc) (zAt y xRef z₀ n T t j)))
      (Ioo (grid j.castSucc) (grid j.succ)) := fun s hs => congrArg (rate xRef) (harc j hs)
  have hint := finite_arc_integral (n+1) grid
    (fun s => rate xRef (γ s))
    (fun j s => rate xRef (Φ y xRef (s-grid j.castSucc) (zAt y xRef z₀ n T t j)))
    hgrid hr heq
  change grid 0 = 0 at hg0
  change grid (Fin.last (n+1)) = (T : ℝ) at hgT
  rw [hg0, hgT] at hint
  refine ⟨hint.1, hint.2.trans ?_, ?_⟩
  · apply Finset.sum_congr rfl
    intro j _
    change (∫ s in grid j.castSucc..grid j.succ,
      rate xRef (Φ y xRef (s-grid j.castSucc) (zAt y xRef z₀ n T t j))) =
      ∫ s in (0 : ℝ)..((Real.toNNReal (grid j.succ-grid j.castSucc) : ℝ≥0) : ℝ),
        rate xRef (Φ y xRef s (zAt y xRef z₀ n T t j))
    rw [intervalIntegral.integral_comp_sub_right
      (f := fun s => rate xRef (Φ y xRef s (zAt y xRef z₀ n T t j))), sub_self,
      Real.coe_toNNReal _ (sub_nonneg.mpr (hgrid (Fin.castSucc_le_succ j)))]
  · intro i
    have hi : grid i.castSucc.castSucc < t.val i := by
      simpa [grid] using t.property.1 (Fin.castSucc_lt_succ (i := i))
    have hnext : grid i.castSucc.succ = t.val i := by
      simp only [grid, Fin.succ_castSucc, Fin.snoc_castSucc, Fin.cons_succ]
    have hleft : Tendsto γ (𝓝[<] t.val i)
        (𝓝 (Φ y xRef (t.val i-grid i.castSucc.castSucc)
          (zAt y xRef z₀ n T t i.castSucc))) :=
      incoming_left_limit hi (hphase i.castSucc)
        (by simpa only [hnext] using harc i.castSucc)
    refine ⟨hleft, ?_⟩
    exact (hRate.comp (continuous_const.prodMk continuous_id)).continuousAt.tendsto.comp hleft


open scoped NNReal ENNReal

private theorem product_survival (n : ℕ) (r : Fin n → ℝ) (h : Fin (n+1) → ℝ) :
    (∏ i : Fin n, r i * Real.exp (-h i.castSucc)) * Real.exp (-h (Fin.last n)) =
      Real.exp (-(∑ j : Fin (n+1), h j)) * ∏ i : Fin n, r i := by
  rw [Finset.prod_mul_distrib, ← Real.exp_sum, mul_assoc,
    ← Real.exp_add, Fin.sum_univ_castSucc, neg_add, Finset.sum_neg_distrib]
  ring


theorem actual_prescribed_path_density_rewrite
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
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
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ, ∀ T : ℝ≥0, ∀ t : Prefix n T,
      let grid : Fin (n + 2) → ℝ :=
        Fin.snoc (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ)) (T : ℝ)
      let γ : ℝ → E × E := fun s =>
        Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
      IntervalIntegrable (fun s => rate xRef (γ s)) volume 0 (T : ℝ) ∧
      (∫ s in (0 : ℝ)..(T : ℝ), rate xRef (γ s)) =
        ∑ j : Fin (n + 1), Λ y xRef (zAt y xRef z₀ n T t j)
          (Real.toNNReal (grid j.succ - grid j.castSucc)) ∧
      (∀ i : Fin n,
        Tendsto γ (𝓝[<] (t.val i))
          (𝓝 (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))) ∧
        Tendsto (fun s => rate xRef (γ s)) (𝓝[<] (t.val i))
          (𝓝 (rate xRef (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))))) ∧
      ρ y xRef z₀ n T t = ENNReal.ofReal
        (Real.exp (-(∫ s in (0 : ℝ)..(T : ℝ), rate xRef (γ s))) *
          ∏ i : Fin n, rate xRef (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))) := by
  classical
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
  change
    ∀ y xRef : E, ∀ z₀ : E × E, ∀ n : ℕ, ∀ T : ℝ≥0, ∀ t : Prefix n T,
      let grid : Fin (n + 2) → ℝ :=
        Fin.snoc (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ)) (T : ℝ)
      let γ : ℝ → E × E := fun s =>
        Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
      IntervalIntegrable (fun s => rate xRef (γ s)) volume 0 (T : ℝ) ∧
      (∫ s in (0 : ℝ)..(T : ℝ), rate xRef (γ s)) =
        ∑ j : Fin (n + 1), Λ y xRef (zAt y xRef z₀ n T t j)
          (Real.toNNReal (grid j.succ - grid j.castSucc)) ∧
      (∀ i : Fin n,
        Tendsto γ (𝓝[<] (t.val i))
          (𝓝 (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))) ∧
        Tendsto (fun s => rate xRef (γ s)) (𝓝[<] (t.val i))
          (𝓝 (rate xRef (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))))) ∧
      ρ y xRef z₀ n T t = ENNReal.ofReal
        (Real.exp (-(∫ s in (0 : ℝ)..(T : ℝ), rate xRef (γ s))) *
          ∏ i : Fin n, rate xRef (Φ y xRef (t.val i - grid i.castSucc.castSucc)
            (zAt y xRef z₀ n T t i.castSucc)))
  intro y xRef z₀ n T t
  let grid : Fin (n+2) → ℝ := Fin.snoc (Fin.cons (0 : ℝ) t.val) (T : ℝ)
  let γ : ℝ → E × E := fun s =>
    Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩
  obtain ⟨hint, hsum, hleft⟩ :=
    actual_analysis hα hαβ hV hH hη hβη y xRef z₀ n T t
  refine ⟨hint, hsum, hleft, ?_⟩
  change ρ y xRef z₀ n T t = ENNReal.ofReal
    (Real.exp (-(∫ s in (0 : ℝ)..(T : ℝ), rate xRef (γ s))) *
      ∏ i : Fin n, rate xRef (Φ y xRef (t.val i-grid i.castSucc.castSucc)
        (zAt y xRef z₀ n T t i.castSucc)))
  let r : Fin n → ℝ := fun i =>
    rate xRef (Φ y xRef (t.val i-grid i.castSucc.castSucc) (zAt y xRef z₀ n T t i.castSucc))
  let h : Fin (n+1) → ℝ := fun j =>
    Λ y xRef (zAt y xRef z₀ n T t j) (Real.toNNReal (grid j.succ-grid j.castSucc))
  have hsum' : (∫ s in (0 : ℝ)..(T : ℝ), rate xRef (γ s)) = ∑ j, h j := hsum
  have hstep (i : Fin n) : grid i.castSucc.succ = t.val i := by
    simp only [grid, Fin.succ_castSucc, Fin.snoc_castSucc, Fin.cons_succ]
  have hq : qReal y xRef z₀ n T t = ∏ i : Fin n, r i * Real.exp (-h i.castSucc) := by
    apply Finset.prod_congr rfl
    intro i _
    simp only [r, h, hstep, grid, Fin.snoc_castSucc]
  have hlast0 : 0 ≤ (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n+1) → ℝ) (Fin.last n) := by
    have hh := t.property.1.monotone (Fin.zero_le (Fin.last n))
    simpa only [Fin.cons_zero] using hh
  have hlastT : (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n+1) → ℝ) (Fin.last n) ≤ (T : ℝ) := by
    cases n with
    | zero => simpa using T.coe_nonneg
    | succ n => simpa using (t.property.2 (Fin.last n)).le
  have htail : T - Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n+1) → ℝ) (Fin.last n)) =
      Real.toNNReal ((T : ℝ) - (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n+1) → ℝ) (Fin.last n)) := by
    apply NNReal.eq
    rw [NNReal.coe_sub ((Real.toNNReal_le_iff_le_coe).2 hlastT),
      Real.coe_toNNReal _ hlast0, Real.coe_toNNReal _ (sub_nonneg.mpr hlastT)]
  have hweight : weight y xRef ((K y xRef z₀ n T t) ⟨n, Nat.lt_succ_self n⟩)
      (d n T (K y xRef z₀ n T t)) = ENNReal.ofReal (Real.exp (-h (Fin.last n))) := by
    change ENNReal.ofReal (Real.exp (-Λ y xRef (zAt y xRef z₀ n T t (Fin.last n))
      (T - Real.toNNReal ((Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n+1) → ℝ) (Fin.last n))))) = _
    rw [htail]
    simp only [h, grid, Fin.succ_last, Fin.snoc_last, Fin.snoc_castSucc]
  change ENNReal.ofReal (qReal y xRef z₀ n T t) * _ = _
  rw [hweight, ← ENNReal.ofReal_mul' (Real.exp_pos _).le, hq,
    product_survival, hsum']


#print axioms actual_prescribed_path_density_rewrite
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity
