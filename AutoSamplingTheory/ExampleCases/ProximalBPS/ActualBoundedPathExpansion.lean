import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity
import Mathlib.MeasureTheory.Integral.Bochner.Set

/-! Chen--Chewi--Lu--Zhang, arXiv:2609.06905v1, Appendix A.1 (A.7).
Bounded real path functionals on the coordinate-product measurable path space.
The mass-partition proof is an explicit ASTIS completion of countable signed assembly. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion
open InnerProductSpace MeasureTheory ProbabilityTheory Set Filter
open scoped NNReal ENNReal Topology Interval BigOperators Classical
set_option autoImplicit false

private theorem signed_sector
    {X U J Y : Type*} [MeasurableSpace X] [MeasurableSpace U]
    [MeasurableSpace J] [MeasurableSpace Y]
    {μ : Measure X} {ν : Measure U} {H : X → J} {Z : X → Y}
    {K : U → J} {Γ : U → Y} {ρ : U → ℝ≥0∞} {wgt : U → ℝ}
    (hH : Measurable H) (hZ : Measurable Z) (hK : Measurable K)
    (hΓ : Measurable Γ) (hρ : Measurable ρ)
    (hw : ∀ t, 0 ≤ wgt t) (heq : ∀ t, ρ t = ENNReal.ofReal (wgt t))
    (hlaw : Measure.map (fun x => (H x, Z x)) μ =
      Measure.map (fun t => (K t, Γ t)) (ν.withDensity ρ))
    {F : Y → ℝ} (hF : Measurable F) (hi : Integrable (fun x => F (Z x)) μ) :
    Integrable (fun t => F (Γ t) * wgt t) ν ∧
      (∫ x, F (Z x) ∂μ) = ∫ t, F (Γ t) * wgt t ∂ν := by
  have hG : Measurable (fun q : J × Y => F q.2) := hF.comp measurable_snd
  have hiMap : Integrable (fun q : J × Y => F q.2)
      (Measure.map (fun x => (H x, Z x)) μ) :=
    (integrable_map_measure hG.aestronglyMeasurable
      (hH.prodMk hZ).aemeasurable).2 hi
  rw [hlaw] at hiMap
  have hiW : Integrable (fun t => F (Γ t)) (ν.withDensity ρ) :=
    (integrable_map_measure hG.aestronglyMeasurable
      (hK.prodMk hΓ).aemeasurable).1 hiMap
  have htop : ∀ᵐ t ∂ν, ρ t < ⊤ := Filter.Eventually.of_forall
    (fun t => by rw [heq]; exact ENNReal.ofReal_lt_top)
  have hreal (t : U) : (ρ t).toReal = wgt t := by
    rw [heq, ENNReal.toReal_ofReal (hw t)]
  refine ⟨?_, ?_⟩
  · simpa only [hreal, smul_eq_mul, mul_comm] using
      (integrable_withDensity_iff_integrable_smul' hρ htop).1 hiW
  · calc
      (∫ x, F (Z x) ∂μ) = ∫ q : J × Y, F q.2
          ∂Measure.map (fun x => (H x, Z x)) μ :=
        (integral_map (hH.prodMk hZ).aemeasurable hG.aestronglyMeasurable).symm
      _ = ∫ q : J × Y, F q.2
          ∂Measure.map (fun t => (K t, Γ t)) (ν.withDensity ρ) := by rw [hlaw]
      _ = ∫ t, F (Γ t) ∂ν.withDensity ρ :=
        integral_map (hK.prodMk hΓ).aemeasurable hG.aestronglyMeasurable
      _ = ∫ t, F (Γ t) * wgt t ∂ν := by
        simpa only [hreal, smul_eq_mul, mul_comm] using
          integral_withDensity_eq_integral_toReal_smul hρ htop (fun t => F (Γ t))

private theorem signed_count_partition {X : Type*} [MeasurableSpace X]
    {μ : Measure X} {N : X → ℕ} (hN : Measurable N)
    {f : X → ℝ} (hi : Integrable f μ) :
    Summable (fun n : ℕ => |∫ x in {x | N x = n}, f x ∂μ|) ∧
      (∫ x, f x ∂μ) = ∑' n : ℕ, ∫ x in {x | N x = n}, f x ∂μ := by
  have hU : (⋃ n : ℕ, {x | N x = n}) = univ := by ext x; simp
  have hd : Pairwise (fun i j : ℕ => Disjoint {x | N x = i} {x | N x = j}) := by
    intro i j hij
    exact Set.disjoint_left.mpr (fun x hi hj => hij (hi.symm.trans hj))
  have hsum := hasSum_integral_iUnion
    (fun n : ℕ => measurableSet_eq_fun hN measurable_const) hd hi.integrableOn
  rw [hU, Measure.restrict_univ] at hsum
  exact ⟨hsum.summable.abs, hsum.tsum_eq.symm⟩

private noncomputable def actual_bounded_path_statement
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
    let τ : E → E → (E × E) → ℝ≥0 → WithTop ℝ≥0 := fun y xRef z e =>
      MeasureTheory.hittingAfter
        (fun t : ℝ≥0 => fun a : (E × E) × (E × E) × ℝ≥0 =>
          Λ a.1.1 a.1.2 a.2.1 t - (a.2.2 : ℝ))
        (Set.Ici (0 : ℝ)) 0 ((y, xRef), z, e)
    let next : E → E → ℝ≥0 → ((ℝ≥0 × (E × E)) ⊕ Unit) →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef e r =>
      match r with
      | Sum.inr _ => Sum.inr ()
      | Sum.inl a =>
        if τ y xRef a.2 e = ⊤ then Sum.inr () else
          Sum.inl (a.1 + (τ y xRef a.2 e).untopD 0,
            S xRef (Φ y xRef (((τ y xRef a.2 e).untopD 0 : ℝ≥0) : ℝ) a.2))
    let record : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ →
        ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef z₀ e n =>
      Nat.rec (Sum.inl (0, z₀)) (fun k r => next y xRef (e k) r) n
    let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
    let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun w k => Real.toNNReal (w k)
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
    let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
      fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
        (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
    let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
      fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
        (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
    let Path : ℝ≥0 → Type _ := fun T => {s : ℝ≥0 // s ≤ T} → E × E
    let Ψ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Hist n → Path T :=
      fun y xRef z₀ n T h s =>
        Fin.foldl (n + 1) (fun z j => (h j).elim
          (fun a => if a.1 ≤ s.val then Φ y xRef ((s.val - a.1 : ℝ≥0) : ℝ) a.2 else z)
          (fun _ => z)) z₀
    let Γ : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → Path T :=
      fun y xRef z₀ n T t => Ψ y xRef z₀ n T (K y xRef z₀ n T t)
    let wgt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ :=
      fun y xRef z₀ n T t =>
        Real.exp (-(∫ s in (0 : ℝ)..(T : ℝ),
          rate xRef (Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩))) *
        ∏ i : Fin n,
          rate xRef (Φ y xRef (t.val i -
            (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
            (zAt y xRef z₀ n T t i.castSucc))
    ∃ Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E),
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
        Z a.1.1.1 a.1.1.2 a.1.2 a.2.1 a.2.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E), w ∈ I y xRef z₀ s n →
          record y xRef z₀ (ε w) n = Sum.inl a →
          Z y xRef z₀ s w = Φ y xRef ((s - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        (¬ ∃ n, w ∈ I y xRef z₀ s n) → Z y xRef z₀ s w = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ w ∂P, Z y xRef z₀ 0 w = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,
        let ZT : (ℕ → ℝ) → Path T := fun u s => Z y xRef z₀ s.val u
        ∀ F : Path T → ℝ, Measurable F → ∀ M : ℝ, 0 ≤ M →
          (∀ p : Path T, |F p| ≤ M) →
          Integrable (fun u => F (ZT u)) P ∧
          (∀ n : ℕ, Integrable (fun t : Prefix n T =>
            F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t) (m n T)) ∧
          Summable (fun n : ℕ => |∫ t : Prefix n T,
            F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t ∂m n T|) ∧
          (∫ u, F (ZT u) ∂P) = ∑' n : ℕ, ∫ t : Prefix n T,
            F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t ∂m n T)

/-- Full bounded signed path expansion for the actual stopped-clock process. -/
theorem actual_bounded_path_functional_expansion
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) :
    actual_bounded_path_statement hα hαβ hV hH hη hβη := by
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
  let τ : E → E → (E × E) → ℝ≥0 → WithTop ℝ≥0 := fun y xRef z e =>
    MeasureTheory.hittingAfter
      (fun t : ℝ≥0 => fun a : (E × E) × (E × E) × ℝ≥0 =>
        Λ a.1.1 a.1.2 a.2.1 t - (a.2.2 : ℝ))
      (Set.Ici (0 : ℝ)) 0 ((y, xRef), z, e)
  let next : E → E → ℝ≥0 → ((ℝ≥0 × (E × E)) ⊕ Unit) →
      ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef e r =>
    match r with
    | Sum.inr _ => Sum.inr ()
    | Sum.inl a =>
      if τ y xRef a.2 e = ⊤ then Sum.inr () else
        Sum.inl (a.1 + (τ y xRef a.2 e).untopD 0,
          S xRef (Φ y xRef (((τ y xRef a.2 e).untopD 0 : ℝ≥0) : ℝ) a.2))
  let record : E → E → (E × E) → (ℕ → ℝ≥0) → ℕ →
      ((ℝ≥0 × (E × E)) ⊕ Unit) := fun y xRef z₀ e n =>
    Nat.rec (Sum.inl (0, z₀)) (fun k r => next y xRef (e k) r) n
  let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))
  let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun w k => Real.toNNReal (w k)
  let history : E → E → (E × E) → (n : ℕ) → (ℕ → ℝ) →
      (Fin (n + 1) → ((ℝ≥0 × (E × E)) ⊕ Unit)) :=
    fun y xRef z₀ n w j => record y xRef z₀ (ε w) j.val
  let Rec := (ℝ≥0 × (E × E)) ⊕ Unit
  let Hist : ℕ → Type _ := fun n => Fin (n + 1) → Rec
  let readTime : Rec → ℝ := fun r => match r with
    | Sum.inl q => (q.1 : ℝ)
    | Sum.inr _ => 0
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
  let A : (n : ℕ) → ℝ≥0 → Set (Hist n) := fun n T =>
    {h | (∀ j, ∃ a : ℝ≥0 × (E × E), h j = Sum.inl a) ∧
      StrictMono (fun j => readTime (h j)) ∧
      ∀ i : Fin n, readTime (h i.succ) < (T : ℝ)}
  let eventTime : E → E → (E × E) → (ℕ → ℝ) → ℕ → WithTop ℝ≥0 :=
    fun y xRef z₀ w j => (record y xRef z₀ (ε w) j).elim
      (fun a => (a.1 : WithTop ℝ≥0)) (fun _ => ⊤)
  let I : E → E → (E × E) → ℝ≥0 → ℕ → Set (ℕ → ℝ) :=
    fun y xRef z₀ T n => {w | eventTime y xRef z₀ w n ≤ (T : WithTop ℝ≥0) ∧
      (T : WithTop ℝ≥0) < eventTime y xRef z₀ w (n + 1)}
  let N : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → ℕ := fun y xRef z₀ T w =>
    if h : ∃ n, w ∈ I y xRef z₀ T n then Nat.find h else 0
  let liveTime : Rec → ℝ≥0 := fun r => r.elim Prod.fst (fun _ => 0)
  let d : (n : ℕ) → ℝ≥0 → Hist n → ℝ≥0 :=
    fun n T h => T - liveTime (h ⟨n, Nat.lt_succ_self n⟩)
  let survival : E → E → Rec → ℝ≥0 → ℝ → Prop :=
    fun y xRef r u e => r.elim
      (fun a => (u : WithTop ℝ≥0) < τ y xRef a.2 (Real.toNNReal e)) (fun _ => False)
  let weight : E → E → Rec → ℝ≥0 → ℝ≥0∞ :=
    fun y xRef r u => r.elim
      (fun a => ENNReal.ofReal (Real.exp (-Λ y xRef a.2 u))) (fun _ => 0)
  let C : E → E → (E × E) → (n : ℕ) → ℝ≥0 → Set (ℕ → ℝ) :=
    fun y xRef z₀ n T => {w | history y xRef z₀ n w ∈ A n T ∧
      survival y xRef (record y xRef z₀ (ε w) n) (d n T (history y xRef z₀ n w)) (w n)}
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
  let wgt : E → E → (E × E) → (n : ℕ) → (T : ℝ≥0) → Prefix n T → ℝ :=
    fun y xRef z₀ n T t =>
      Real.exp (-(∫ s in (0 : ℝ)..(T : ℝ),
        rate xRef (Γ y xRef z₀ n T t ⟨min (Real.toNNReal s) T, min_le_right _ _⟩))) *
      ∏ i : Fin n,
        rate xRef (Φ y xRef (t.val i -
          (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) i.castSucc)
          (zAt y xRef z₀ n T t i.castSucc))
  change
    ∃ Z : E → E → (E × E) → ℝ≥0 → (ℕ → ℝ) → (E × E),
      Measurable (fun a : ((E × E) × (E × E)) × ℝ≥0 × (ℕ → ℝ) =>
        Z a.1.1.1 a.1.1.2 a.1.2 a.2.1 a.2.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        ∀ n : ℕ, ∀ a : ℝ≥0 × (E × E), w ∈ I y xRef z₀ s n →
          record y xRef z₀ (ε w) n = Sum.inl a →
          Z y xRef z₀ s w = Φ y xRef ((s - a.1 : ℝ≥0) : ℝ) a.2) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ w : ℕ → ℝ, ∀ s : ℝ≥0,
        (¬ ∃ n, w ∈ I y xRef z₀ s n) → Z y xRef z₀ s w = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ᵐ w ∂P, Z y xRef z₀ 0 w = z₀) ∧
      (∀ y xRef : E, ∀ z₀ : E × E, ∀ T : ℝ≥0,
        let ZT : (ℕ → ℝ) → Path T := fun u s => Z y xRef z₀ s.val u
        ∀ F : Path T → ℝ, Measurable F → ∀ M : ℝ, 0 ≤ M →
          (∀ p : Path T, |F p| ≤ M) →
          Integrable (fun u => F (ZT u)) P ∧
          (∀ n : ℕ, Integrable (fun t : Prefix n T =>
            F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t) (m n T)) ∧
          Summable (fun n : ℕ => |∫ t : Prefix n T,
            F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t ∂m n T|) ∧
          (∫ u, F (ZT u) ∂P) = ∑' n : ℕ, ∫ t : Prefix n T,
            F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t ∂m n T)

  obtain ⟨Z, hZM, hZarc, hZfallback, hZzero, hAll⟩ :=
    ActualFiniteCountPath.actual_finite_count_path_law hα hαβ hV hH hη hβη
  refine ⟨Z, hZM, hZarc, hZfallback, hZzero, ?_⟩
  intro y xRef z₀ T
  let ZT : (ℕ → ℝ) → Path T := fun u s => Z y xRef z₀ s.val u
  dsimp only
  intro F hF M hM hbound
  letI : IsProbabilityMeasure P :=
    AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws.1
  have hbase := (hAll 0 T).2.2.2 y xRef z₀
  have hZT : Measurable ZT := hbase.2.1
  have hN : Measurable (N y xRef z₀ T) := hbase.2.2.1
  have hi : Integrable (fun u => F (ZT u)) P :=
    ⟨(hF.comp hZT).aestronglyMeasurable,
      HasFiniteIntegral.of_bounded (Filter.Eventually.of_forall
        (fun u => by simpa only [Real.norm_eq_abs] using hbound (ZT u)))⟩
  have hsector (n : ℕ) :
      Integrable (fun t : Prefix n T => F (Γ y xRef z₀ n T t) *
        wgt y xRef z₀ n T t) (m n T) ∧
      (∫ u in {u | N y xRef z₀ T u = n}, F (ZT u) ∂P) =
        ∫ t : Prefix n T, F (Γ y xRef z₀ n T t) * wgt y xRef z₀ n T t ∂m n T := by
    have hn := hAll n T
    obtain ⟨hHM, hZTM, hNM, hCM, hinterp, hident, hAE, hdisj, hcover,
      hlaw, htests, hmass, hmassbound⟩ := hn.2.2.2 y xRef z₀
    have hΓ : Measurable (Γ y xRef z₀ n T) := hn.2.1.comp
      (f := fun t : Prefix n T => (((y,xRef),z₀),t))
      (measurable_const.prodMk measurable_id)
    have hρ : Measurable (ρ y xRef z₀ n T) := hn.2.2.1.comp
      (f := fun t : Prefix n T => (((y,xRef),z₀),t))
      (measurable_const.prodMk measurable_id)
    have hK : Measurable (K y xRef z₀ n T) :=
      (ActualOrderedPrefix.actual_ordered_prefix_law hα hαβ hV hH hη hβη n T).2.2.1.comp
        (f := fun t : Prefix n T => (((y,xRef),z₀),t))
        (measurable_const.prodMk measurable_id)
    have hw (t : Prefix n T) : 0 ≤ wgt y xRef z₀ n T t := by
      apply mul_nonneg (Real.exp_nonneg _)
      exact Finset.prod_nonneg (fun i _ => mul_nonneg (Real.sqrt_nonneg _) (le_max_left _ _))
    have heq (t : Prefix n T) :
        ρ y xRef z₀ n T t = ENNReal.ofReal (wgt y xRef z₀ n T t) := by
      have hd := (ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite
        hα hαβ hV hH hη hβη y xRef z₀ n T t).2.2.2
      simpa only [Fin.snoc_castSucc] using hd
    exact signed_sector hHM hZTM hK hΓ hρ hw heq hlaw hF hi.integrableOn
  have hsum := signed_count_partition hN hi
  have heq (n : ℕ) := (hsector n).2
  refine ⟨hi, fun n => (hsector n).1, ?_, ?_⟩
  · simpa only [heq] using hsum.1
  · simpa only [heq] using hsum.2

#print axioms actual_bounded_path_functional_expansion

end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion
