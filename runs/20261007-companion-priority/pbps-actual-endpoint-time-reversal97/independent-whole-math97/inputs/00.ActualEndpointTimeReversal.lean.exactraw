import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume
import Mathlib.Data.Fin.Rev
import Mathlib.Order.Fin.Tuple

/-! Actual finite prescribed endpoint and time-tuple reversal for PBPS A.8.
Original six analytic assumptions; phase volume and ordered-simplex comap volume.
The right-continuous path itself is not asserted to reverse pointwise at events.
Gibbs density balance, stationary averaging, restart, and full invariance remain separate.
-/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal
open MeasureTheory InnerProductSpace
open scoped NNReal ENNReal Classical ContDiff
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2400000


private def delta (n : ℕ) (T : ℝ) : Set (Fin n → ℝ) :=
  {t | StrictMono (Fin.cons (0 : ℝ) t) ∧ ∀ i, t i < T}
private def reverseTime {n : ℕ} (T : ℝ) (t : Fin n → ℝ) : Fin n → ℝ :=
  fun i => T - t i.rev

private theorem reverseTime_involutive (n : ℕ) (T : ℝ) :
    Function.Involutive (reverseTime (n := n) T) := by
  intro t; funext i
  simp [reverseTime]

private theorem reverseTime_mem {n : ℕ} {T : ℝ} {t : Fin n → ℝ}
    (ht : t ∈ delta n T) : reverseTime T t ∈ delta n T := by
  obtain ⟨hpos, hmono⟩ := Fin.strictMono_cons.mp ht.1
  refine ⟨Fin.strictMono_cons.mpr ⟨?_, ?_⟩, ?_⟩
  · intro i
    exact sub_pos.mpr (ht.2 i.rev)
  · intro i j hij
    exact sub_lt_sub_left (hmono (Fin.rev_lt_rev.mpr hij)) T
  · intro i
    exact sub_lt_self T (hpos i.rev)

private theorem reverseTime_measurable (n : ℕ) (T : ℝ) :
    Measurable (reverseTime (n := n) T) := by
  apply measurable_pi_lambda
  intro i
  exact measurable_const.sub (measurable_pi_apply i.rev)

private theorem reverseTime_volume (n : ℕ) (T : ℝ) :
    MeasurePreserving (reverseTime (n := n) T) volume volume := by
  have hp := volume_measurePreserving_piCongrLeft (fun _ : Fin n => ℝ) Fin.revPerm
  have heq : (fun t : Fin n → ℝ => fun i : Fin n => t i.rev) =
      MeasurableEquiv.piCongrLeft (fun _ : Fin n => ℝ) Fin.revPerm := by
    funext t i
    symm
    simpa only [Fin.revPerm_apply, Fin.rev_rev] using
      (MeasurableEquiv.piCongrLeft_apply_apply (β := fun _ : Fin n => ℝ) Fin.revPerm t i.rev)
  rw [← heq] at hp
  have hc : MeasurePreserving (fun t : Fin n → ℝ => fun i => T - t i) volume volume :=
    volume_preserving_pi (fun _ : Fin n => (volume : Measure ℝ).measurePreserving_sub_left T)
  exact hc.comp hp

private def rho (n : ℕ) (T : ℝ) (t : delta n T) : delta n T :=
  ⟨reverseTime T t.val, reverseTime_mem t.property⟩

private theorem rho_measurable (n : ℕ) (T : ℝ) : Measurable (rho n T) :=
  ((reverseTime_measurable n T).comp measurable_subtype_coe).subtype_mk

private theorem rho_involutive (n : ℕ) (T : ℝ) : Function.Involutive (rho n T) := by
  intro t; apply Subtype.ext
  exact reverseTime_involutive n T t.val

private theorem rho_volume (n : ℕ) (T : ℝ) (hs : MeasurableSet (delta n T)) :
    MeasurePreserving (rho n T) (Measure.comap Subtype.val volume)
      (Measure.comap Subtype.val volume) := by
  have he : reverseTime (n := n) T ⁻¹' delta n T = delta n T := by
    ext t
    constructor
    · intro ht
      have hh := reverseTime_mem ht
      simpa only [reverseTime_involutive n T t] using hh
    · exact reverseTime_mem
  have hr := (reverseTime_volume n T).restrict_preimage hs
  rw [he] at hr
  have hcoe := measurePreserving_subtype_coe (μa := (volume : Measure (Fin n → ℝ))) hs
  refine ⟨rho_measurable n T, ?_⟩
  apply (MeasurableEmbedding.subtype_coe hs).map_injective
  rw [Measure.map_map measurable_subtype_coe (rho_measurable n T)]
  exact (hr.comp hcoe).map_eq.trans hcoe.map_eq.symm



/-- Cancellation of a finite word against its reverse under a common reversing map. -/
private theorem reverse_fold_cancel {X : Type*} (C : X → X) (n : ℕ)
    (f : Fin n → X → X) (hf : ∀ i x, f i (C (f i x)) = C x) (x : X) :
    Fin.foldr n f (C (Fin.foldl n (fun z i => f i z) x)) = C x := by
  induction n generalizing x with
  | zero => simp
  | succ n ih =>
    rw [Fin.foldl_succ, Fin.foldr_succ]
    rw [ih (fun i => f i.succ) (fun i => hf i.succ)]
    exact hf 0 x

/-- Finite recursion is the corresponding left fold, without assuming an endpoint. -/
private theorem fold_of_sequence {X : Type*} (n : ℕ) (f : Fin n → X → X)
    (r : Fin (n + 1) → X) (x : X) (hzero : r 0 = x)
    (hstep : ∀ i : Fin n, r i.succ = f i (r i.castSucc)) :
    Fin.foldl n (fun z i => f i z) x = r (Fin.last n) := by
  induction n with
  | zero => simpa using hzero.symm
  | succ n ih =>
    rw [Fin.foldl_succ_last]
    have ht := ih (fun i => f i.castSucc) (fun i => r i.castSucc) hzero
      (fun i => hstep i.castSucc)
    rw [ht]
    exact (hstep (Fin.last n)).symm

private def gaps {n : ℕ} (T : ℝ) (t : Fin n → ℝ) (i : Fin (n + 1)) : ℝ :=
  (Fin.snoc t T : Fin (n + 1) → ℝ) i - (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) i

private theorem gaps_reversed (n : ℕ) (T : ℝ) (t : Fin n → ℝ) (i : Fin (n + 1)) :
    gaps T (fun j => T - t j.rev) i = gaps T t i.rev := by
  have hl : (Fin.cons (0 : ℝ) (fun j : Fin n => T - t j.rev) : Fin (n + 1) → ℝ) i = T - (Fin.snoc t T : Fin (n + 1) → ℝ) i.rev := by
    induction i using Fin.cases with
    | zero => simp
    | succ j => simp [Fin.rev_succ]
  have hr : (Fin.snoc (fun j : Fin n => T - t j.rev) T : Fin (n + 1) → ℝ) i = T - (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) i.rev := by
    induction i using Fin.lastCases with
    | last => simp
    | cast j => simp [Fin.rev_castSucc]
  unfold gaps
  rw [hl, hr]
  ring

private def post {X : Type*} (Φ : ℝ → X → X) (S : X → X) (n : ℕ)
    (t : Fin n → ℝ) (z : X) : Fin (n + 1) → X :=
  Fin.induction z (fun i x => S (Φ (t i -
    (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) i.castSucc) x))

private def endpoint {X : Type*} (Φ : ℝ → X → X) (S : X → X) (n : ℕ)
    (T : ℝ) (t : Fin n → ℝ) (z : X) : X :=
  Φ (T - (Fin.cons (0 : ℝ) t : Fin (n + 1) → ℝ) (Fin.last n))
    (post Φ S n t z (Fin.last n))

private theorem endpoint_as_word {X : Type*} (Φ : ℝ → X → X) (S : X → X)
    (hS : Function.Involutive S) (n : ℕ) (T : ℝ) (t : Fin n → ℝ) (z : X) :
    endpoint Φ S n T t z =
      Fin.foldl (n + 1) (fun x i => Φ (gaps T t i) (S x)) (S z) := by
  have hSS (x : X) : S (S x) = x := hS x
  let r : Fin (n + 2) → X := Fin.snoc (fun i => S (post Φ S n t z i))
    (endpoint Φ S n T t z)
  have hzero : r 0 = S z := by
    change S (post Φ S n t z 0) = S z
    rfl
  have hstep (i : Fin (n + 1)) : r i.succ = Φ (gaps T t i) (S (r i.castSucc)) := by
    induction i using Fin.lastCases with
    | last =>
      simp only [r, Fin.succ_last, Fin.snoc_last, Fin.snoc_castSucc, endpoint, gaps, hSS]
    | cast j =>
      simp only [r, Fin.succ_castSucc, Fin.snoc_castSucc, post, Fin.induction_succ, gaps, hSS]
  have hf := fold_of_sequence (n + 1) (fun i x => Φ (gaps T t i) (S x)) r (S z) hzero hstep
  simpa only [r, Fin.snoc_last] using hf.symm

private theorem endpoint_reversed {X : Type*} (Φ : ℝ → X → X) (S R : X → X)
    (hS : Function.Involutive S) (hR : Function.Involutive R)
    (hRS : ∀ x, R (S x) = S (R x))
    (hInv : ∀ u x, Φ u (Φ (-u) x) = x)
    (hRev : ∀ u x, R (Φ u (R x)) = Φ (-u) x)
    (n : ℕ) (T : ℝ) (t : Fin n → ℝ) (z : X) :
    endpoint Φ S n T (fun i => T - t i.rev) (R (endpoint Φ S n T t z)) = R z := by
  have hSS (x : X) : S (S x) = x := hS x
  have hRR (x : X) : R (R x) = x := hR x
  have hcomm (u : ℝ) (x : X) : R (Φ u x) = Φ (-u) (R x) := by
    simpa only [hRR] using hRev u (R x)
  let C : X → X := fun x => S (R x)
  let f : Fin (n + 1) → X → X := fun i x => Φ (gaps T t i) (S x)
  have hf (i : Fin (n + 1)) (x : X) : f i (C (f i x)) = C x := by
    dsimp [f, C]
    rw [hSS, hcomm, hInv, hRS]
  rw [endpoint_as_word Φ S hS]
  simp_rw [gaps_reversed]
  change Fin.foldl (n + 1) (fun x i => f i.rev x) (C (endpoint Φ S n T t z)) = R z
  rw [Fin.foldl_rev, endpoint_as_word Φ S hS]
  exact (reverse_fold_cancel C (n + 1) f hf (S z)).trans (by dsimp [C]; rw [hRS, hSS])

private theorem preserving_fold {X : Type*} [MeasurableSpace X] (μ : Measure X)
    (n : ℕ) (f : Fin n → X → X) (hf : ∀ i, MeasurePreserving (f i) μ μ) :
    MeasurePreserving (fun x => Fin.foldl n (fun z i => f i z) x) μ μ := by
  induction n with
  | zero =>
    simp only [Fin.foldl_zero]
    exact ⟨measurable_id, Measure.map_id'⟩
  | succ n ih =>
    simpa only [Fin.foldl_succ_last, Function.comp_def] using
      (hf (Fin.last n)).comp (ih (fun i => f i.castSucc) (fun i => hf i.castSucc))

private theorem endpoint_volume {X : Type*} [MeasurableSpace X] (μ : Measure X)
    (Φ : ℝ → X → X) (S : X → X) (hS : Function.Involutive S)
    (hSM : MeasurePreserving S μ μ) (hΦ : ∀ u, MeasurePreserving (Φ u) μ μ)
    (n : ℕ) (T : ℝ) (t : Fin n → ℝ) : MeasurePreserving (endpoint Φ S n T t) μ μ := by
  have he : endpoint Φ S n T t =
      (fun x => Fin.foldl (n + 1) (fun z i => Φ (gaps T t i) (S z)) x) ∘ S := by
    funext z
    exact endpoint_as_word Φ S hS n T t z
  rw [he]
  exact (preserving_fold μ (n + 1) (fun i z => Φ (gaps T t i) (S z))
    (fun i => (hΦ _).comp hSM)).comp hSM


set_option maxHeartbeats 2400000
private def endpoint_data_statement
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
    ∀ n : ℕ, ∀ T : ℝ≥0,
      MeasurableSet (Δ n T) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2 ⟨T, le_rfl⟩) ∧
      (∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        Γ y r z n T t ⟨T, le_rfl⟩ = Φ y r ((T : ℝ) -
          (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) (Fin.last n))
          (zAt y r z n T t (Fin.last n)))

private theorem endpoint_data
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : endpoint_data_statement hα hαβ hV hH hη hβη := by
  classical
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
  change
    ∀ n : ℕ, ∀ T : ℝ≥0,
      MeasurableSet (Δ n T) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2 ⟨T, le_rfl⟩) ∧
      (∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        Γ y r z n T t ⟨T, le_rfl⟩ = Φ y r ((T : ℝ) -
          (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) (Fin.last n))
          (zAt y r z n T t (Fin.last n)))
  obtain ⟨Z, hZM, hZarc, hZfallback, hZzero, hdata⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law
      hα hαβ hV hH hη hβη
  have hprefix := AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law
    hα hαβ hV hH hη hβη
  intro n T
  have hGM : Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
      Γ p.1.1.1 p.1.1.2 p.1.2 n T p.2) := (hdata n T).2.1
  refine ⟨(hprefix n T).1, hGM, (measurable_pi_apply (⟨T, le_rfl⟩ : {s : ℝ≥0 // s ≤ T})).comp hGM, ?_⟩
  intro y r z t
  have hd := (hdata n T).2.2.2 y r z
  have hlast : (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ)
      (Fin.last n) ≤ (T : ℝ) := by
    induction n with
    | zero => simpa using T.coe_nonneg
    | succ n =>
      change t.val (Fin.last n) ≤ (T : ℝ)
      exact (t.property.2 (Fin.last n)).le
  exact hd.2.2.2.2.1 t ⟨T, le_rfl⟩ (Fin.last n) hlast
    (fun k hk => False.elim (not_lt_of_ge (Fin.le_last k) hk))

private def actual_endpoint_time_reversal_statement
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
    let R : (E × E) → (E × E) := fun z => (z.1, -z.2)
    let ell : Measure (E × E) := (volume : Measure E).prod (volume : Measure E)
    ∀ n : ℕ, ∀ T : ℝ≥0, ∃ rho : Prefix n T → Prefix n T,
      (∀ t : Prefix n T, ∀ i : Fin n, (rho t).val i = (T : ℝ) - t.val i.rev) ∧
      Measurable rho ∧ Function.Involutive rho ∧ MeasurePreserving rho (m n T) (m n T) ∧
      let A : E → E → (E × E) → Prefix n T → (E × E) :=
        fun y r z t => Γ y r z n T t ⟨T, le_rfl⟩
      let Theta : E → E → ((E × E) × Prefix n T) → ((E × E) × Prefix n T) :=
        fun y r q => (R (A y r q.1 q.2), rho q.2)
      (∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        A y r z t = Φ y r ((T : ℝ) -
          (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) (Fin.last n))
          (zAt y r z n T t (Fin.last n))) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        A p.1.1.1 p.1.1.2 p.1.2 p.2) ∧
      (∀ y r : E, ∀ t : Prefix n T,
        MeasurePreserving (fun z => A y r z t) ell ell) ∧
      (∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        A y r (R (A y r z t)) (rho t) = R z) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        Theta p.1.1.1 p.1.1.2 (p.1.2, p.2)) ∧
      (∀ y r : E, Function.Involutive (Theta y r)) ∧
      (∀ y r : E, MeasurePreserving (Theta y r) (ell.prod (m n T)) (ell.prod (m n T)))


/-- Exact source-sealed actual endpoint/time reversal law. -/
theorem actual_endpoint_time_reversal_laws
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_endpoint_time_reversal_statement hα hαβ hV hH hη hβη := by
  classical
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
  let R : (E × E) → (E × E) := fun z => (z.1, -z.2)
  let ell : Measure (E × E) := (volume : Measure E).prod (volume : Measure E)
  change
    ∀ n : ℕ, ∀ T : ℝ≥0, ∃ rho : Prefix n T → Prefix n T,
      (∀ t : Prefix n T, ∀ i : Fin n, (rho t).val i = (T : ℝ) - t.val i.rev) ∧
      Measurable rho ∧ Function.Involutive rho ∧ MeasurePreserving rho (m n T) (m n T) ∧
      let A : E → E → (E × E) → Prefix n T → (E × E) :=
        fun y r z t => Γ y r z n T t ⟨T, le_rfl⟩
      let Theta : E → E → ((E × E) × Prefix n T) → ((E × E) × Prefix n T) :=
        fun y r q => (R (A y r q.1 q.2), rho q.2)
      (∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        A y r z t = Φ y r ((T : ℝ) -
          (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) (Fin.last n))
          (zAt y r z n T t (Fin.last n))) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        A p.1.1.1 p.1.1.2 p.1.2 p.2) ∧
      (∀ y r : E, ∀ t : Prefix n T,
        MeasurePreserving (fun z => A y r z t) ell ell) ∧
      (∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        A y r (R (A y r z t)) (rho t) = R z) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        Theta p.1.1.1 p.1.1.2 (p.1.2, p.2)) ∧
      (∀ y r : E, Function.Involutive (Theta y r)) ∧
      (∀ y r : E, MeasurePreserving (Theta y r) (ell.prod (m n T)) (ell.prod (m n T)))

  have hed := endpoint_data hα hαβ hV hH hη hβη
  obtain ⟨hΦM, hSM, hRateM, hΦP, hSP, hRP, hΦI, hSI, hRI, hRΦ, hRS, hRate, hInt⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws
      hα hαβ hV hH hη hβη
  intro n T
  let rho₀ : Prefix n T → Prefix n T := rho n (T : ℝ)
  have hrM : Measurable rho₀ := rho_measurable n (T : ℝ)
  have hrI : Function.Involutive rho₀ := rho_involutive n (T : ℝ)
  have hrP : MeasurePreserving rho₀ (m n T) (m n T) := rho_volume n (T : ℝ) (hed n T).1
  refine ⟨rho₀, (fun t i => rfl), hrM, hrI, hrP, ?_⟩
  let A : E → E → (E × E) → Prefix n T → (E × E) :=
    fun y r z t => Γ y r z n T t ⟨T, le_rfl⟩
  let Theta : E → E → ((E × E) × Prefix n T) → ((E × E) × Prefix n T) :=
    fun y r q => (R (A y r q.1 q.2), rho₀ q.2)
  change
      (∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        A y r z t = Φ y r ((T : ℝ) -
          (Fin.cons (0 : ℝ) (t.val : Fin n → ℝ) : Fin (n + 1) → ℝ) (Fin.last n))
          (zAt y r z n T t (Fin.last n))) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        A p.1.1.1 p.1.1.2 p.1.2 p.2) ∧
      (∀ y r : E, ∀ t : Prefix n T,
        MeasurePreserving (fun z => A y r z t) ell ell) ∧
      (∀ y r : E, ∀ z : E × E, ∀ t : Prefix n T,
        A y r (R (A y r z t)) (rho₀ t) = R z) ∧
      Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
        Theta p.1.1.1 p.1.1.2 (p.1.2, p.2)) ∧
      (∀ y r : E, Function.Involutive (Theta y r)) ∧
      (∀ y r : E, MeasurePreserving (Theta y r) (ell.prod (m n T)) (ell.prod (m n T)))

  have hAm : Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
      A p.1.1.1 p.1.1.2 p.1.2 p.2) := (hed n T).2.2.1
  have hAid (y r : E) (z : E × E) (t : Prefix n T) :
      A y r z t = endpoint (Φ y r) (S r) n (T : ℝ) t.val z := (hed n T).2.2.2 y r z t
  have hAP (y r : E) (t : Prefix n T) : MeasurePreserving (fun z => A y r z t) ell ell := by
    have he : (fun z => A y r z t) = endpoint (Φ y r) (S r) n (T : ℝ) t.val := funext (fun z => hAid y r z t)
    rw [he]
    exact endpoint_volume ell (Φ y r) (S r) (hSI r) (hSP r) (hΦP y r) n (T : ℝ) t.val
  have hAI (y r : E) (z : E × E) (t : Prefix n T) :
      A y r (R (A y r z t)) (rho₀ t) = R z := by
    rw [hAid, hAid]
    exact endpoint_reversed (Φ y r) (S r) R (hSI r) hRI (hRS r)
      (fun u z => (hΦI y r u z).2) (hRΦ y r) n (T : ℝ) t.val z
  have hThetaM : Measurable (fun p : ((E × E) × (E × E)) × Prefix n T =>
      Theta p.1.1.1 p.1.1.2 (p.1.2, p.2)) :=
    (hRP.measurable.comp hAm).prodMk (hrM.comp measurable_snd)
  refine ⟨(hed n T).2.2.2, hAm, hAP, hAI, hThetaM, ?_, ?_⟩
  · intro y r q
    apply Prod.ext
    · change R (A y r (R (A y r q.1 q.2)) (rho₀ q.2)) = q.1
      rw [hAI]
      exact hRI q.1
    · exact hrI q.2
  · intro y r
    have hs := (hed n T).1
    have hmσ : SigmaFinite ((m n T).map (fun t : Prefix n T => t.val)) := by
      change SigmaFinite ((Measure.comap (fun t : Prefix n T => t.val)
        (volume : Measure (Fin n → ℝ))).map (fun t : Prefix n T => t.val))
      rw [map_comap_subtype_coe hs]
      infer_instance
    letI : SigmaFinite (m n T) := SigmaFinite.of_map (m n T) measurable_subtype_coe.aemeasurable hmσ
    have hm : Measurable (fun q : (E × E) × Prefix n T => R (A y r q.1 q.2)) :=
      hRP.measurable.comp (hAm.comp
        (((measurable_const : Measurable (fun _ : (E × E) × Prefix n T => (y, r))).prodMk
          measurable_fst).prodMk measurable_snd))
    have hp := hrP.skew_product (g := fun t z => R (A y r z t)) (hm.comp measurable_swap)
      (Filter.Eventually.of_forall fun t => (hRP.comp (hAP y r t)).map_eq)
    have hout := (Measure.measurePreserving_swap (μ := m n T) (ν := ell)).comp
      (hp.comp (Measure.measurePreserving_swap (μ := ell) (ν := m n T)))
    exact hout

end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal
