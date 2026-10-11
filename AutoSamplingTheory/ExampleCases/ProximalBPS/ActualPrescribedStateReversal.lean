import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal

/-! Actual finite prescribed-state reversal and incoming-rate product for PBPS Appendix A.1.
The original six analytic hypotheses are retained. Incoming/post-event states are
separate; right-continuous trajectories are not identified pointwise at jumps. -/
namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal
open MeasureTheory InnerProductSpace
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2400000

private theorem finite_state_reversal {X : Type*} (n : ℕ)
    (Φ : ℝ → X → X) (S R : X → X)
    (hS : Function.Involutive S) (hR : Function.Involutive R)
    (hRS : ∀ x, R (S x) = S (R x))
    (hInv : ∀ u x, Φ u (Φ (-u) x) = x)
    (hRev : ∀ u x, R (Φ u (R x)) = Φ (-u) x)
    (d : Fin (n+1) → ℝ) (post barPost : Fin (n+1) → X)
    (hp : ∀ i : Fin n, post i.succ = S (Φ (d i.castSucc) (post i.castSucc)))
    (hb : ∀ i : Fin n, barPost i.succ = S (Φ (d i.castSucc.rev) (barPost i.castSucc)))
    (hz : barPost 0 = R (Φ (d (Fin.last n)) (post (Fin.last n)))) :
    ∀ j : Fin (n+1),
      barPost j = R (Φ (d j.rev) (post j.rev)) ∧
      Φ (d j.rev) (barPost j) = R (post j.rev) := by
  have hRR (x : X) : R (R x) = x := hR x
  have hSS (x : X) : S (S x) = x := hS x
  have hc (u : ℝ) (x : X) : R (Φ u x) = Φ (-u) (R x) := by
    simpa only [hRR] using hRev u (R x)
  have hcancel (u : ℝ) (x : X) : Φ u (R (Φ u x)) = R x := by
    rw [hc, hInv]
  intro j
  induction j using Fin.induction with
  | zero =>
    constructor
    · simpa only [Fin.rev_zero] using hz
    · rw [hz, Fin.rev_zero, hcancel]
  | succ i ih =>
    have hs : barPost i.succ = R (Φ (d i.succ.rev) (post i.succ.rev)) := by
      rw [hb, ih.2, Fin.rev_castSucc, hp, hRS, hSS, Fin.rev_succ]
    exact ⟨hs, by rw [hs, hcancel]⟩

private theorem incoming_rate_product {X : Type*} (n : ℕ) (S R : X → X)
    (rate : X → ℝ) (hRate : ∀ x, rate (R (S x)) = rate x)
    (post arrive barArrive : Fin (n+1) → X)
    (hp : ∀ i : Fin n, post i.succ = S (arrive i.castSucc))
    (hb : ∀ j : Fin (n+1), barArrive j = R (post j.rev)) :
    (∏ i : Fin n, rate (barArrive i.castSucc)) =
      ∏ i : Fin n, rate (arrive i.castSucc) := by
  have he (i : Fin n) : rate (barArrive i.castSucc) = rate (arrive i.rev.castSucc) := by
    rw [hb, Fin.rev_castSucc, hp, hRate]
  simp_rw [he]
  exact Equiv.prod_comp Fin.revPerm (fun i : Fin n => rate (arrive i.castSucc))


private theorem reversed_grid_gaps (n : ℕ) (T : ℝ) (t s : Fin n → ℝ)
    (hs : ∀ i, s i = T - t i.rev) :
    let grid : Fin (n+2) → ℝ := Fin.snoc (Fin.cons 0 t) T
    let barGrid : Fin (n+2) → ℝ := Fin.snoc (Fin.cons 0 s) T
    ∀ j : Fin (n+1),
      barGrid j.succ - barGrid j.castSucc =
        grid j.rev.succ - grid j.rev.castSucc := by
  intro grid barGrid j
  have hl : barGrid j.castSucc = T - grid j.rev.succ := by
    induction j using Fin.cases with
    | zero => simp [grid, barGrid]
    | succ i => simp only [grid, barGrid, Fin.rev_succ, Fin.succ_castSucc, Fin.snoc_castSucc, Fin.cons_succ, hs]
  have hr : barGrid j.succ = T - grid j.rev.castSucc := by
    induction j using Fin.lastCases with
    | last => simp [grid, barGrid]
    | cast i => simp only [grid, barGrid, Fin.rev_castSucc, Fin.succ_castSucc, Fin.snoc_castSucc, Fin.cons_succ, hs]
  rw [hl, hr]
  ring


set_option linter.unusedVariables false in
private def actual_prescribed_state_reversal_statement
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
        let grid : Fin (n+2) → ℝ := Fin.snoc (Fin.cons (0 : ℝ) t.val) (T : ℝ)
        let post : Fin (n+1) → E × E := zAt y r z n T t
        let arrive : Fin (n+1) → E × E := fun j =>
          Φ y r (grid j.succ - grid j.castSucc) (post j)
        let A : E × E := Γ y r z n T t ⟨T, le_rfl⟩
        let barGrid : Fin (n+2) → ℝ := Fin.snoc (Fin.cons (0 : ℝ) (rho t).val) (T : ℝ)
        let barPost : Fin (n+1) → E × E := zAt y r (R A) n T (rho t)
        let barArrive : Fin (n+1) → E × E := fun j =>
          Φ y r (barGrid j.succ - barGrid j.castSucc) (barPost j)
        (∀ j : Fin (n+1), barPost j = R (arrive j.rev) ∧ barArrive j = R (post j.rev)) ∧
        (∏ i : Fin n, rate r (barArrive i.castSucc)) =
          ∏ i : Fin n, rate r (arrive i.castSucc)


theorem actual_prescribed_state_reversal_and_rate_product
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hαβ : α ≤ β) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ) * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ) * ‖v‖ ^ 2)
    (hη : 0 < η) (hβη : (β : ℝ) * η ≤ 1) : actual_prescribed_state_reversal_statement hα hαβ hV hH hη hβη := by
  unfold actual_prescribed_state_reversal_statement
  intro c Φ S Rec Hist Δ Prefix m zAt K Path Ψ Γ R rate n T
  obtain ⟨rho, hrho, _, _, _, hend, _⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws
      hα hαβ hV hH hη hβη n T
  obtain ⟨_, _, _, _, _, _, hInv, hS, hR, hRev, hRS, hRate, _⟩ :=
    AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws
      hα hαβ hV hH hη hβη
  refine ⟨rho, hrho, ?_⟩
  intro y r z t grid post arrive A barGrid barPost barArrive
  let d : Fin (n+1) → ℝ := fun j => grid j.succ - grid j.castSucc
  have hg : ∀ j : Fin (n+1), barGrid j.succ - barGrid j.castSucc = d j.rev :=
    reversed_grid_gaps n (T : ℝ) t.val (rho t).val (hrho t)
  have hp (i : Fin n) : post i.succ = S r (arrive i.castSucc) := by
    simp only [post, arrive, grid, zAt, Fin.succ_castSucc,
      Fin.snoc_castSucc, Fin.cons_succ, Fin.induction_succ]
  have hb0 (i : Fin n) : barPost i.succ = S r (barArrive i.castSucc) := by
    simp only [barPost, barArrive, barGrid, zAt, Fin.succ_castSucc,
      Fin.snoc_castSucc, Fin.cons_succ, Fin.induction_succ]
  have hb (i : Fin n) : barPost i.succ =
      S r (Φ y r (d i.castSucc.rev) (barPost i.castSucc)) := by
    rw [hb0]
    change S r (Φ y r (barGrid i.castSucc.succ - barGrid i.castSucc.castSucc)
      (barPost i.castSucc)) = _
    rw [hg]
  have hz : barPost 0 = R (Φ y r (d (Fin.last n)) (post (Fin.last n))) := by
    change R A = R (arrive (Fin.last n))
    congr 1
    simpa only [arrive, d, grid, post, Fin.succ_last, Fin.snoc_last,
      Fin.snoc_castSucc] using hend y r z t
  have hstates := finite_state_reversal n (Φ y r) (S r) R
    (fun q => hS r q) (fun q => hR q) (fun q => hRS r q)
    (fun u q => (hInv y r u q).2) (fun u q => hRev y r u q)
    d post barPost hp hb hz
  have hpair (j : Fin (n+1)) :
      barPost j = R (arrive j.rev) ∧ barArrive j = R (post j.rev) := by
    refine ⟨(hstates j).1, ?_⟩
    change Φ y r (barGrid j.succ - barGrid j.castSucc) (barPost j) = _
    rw [hg]
    exact (hstates j).2
  refine ⟨hpair, ?_⟩
  exact incoming_rate_product n (S r) R (rate r) (fun q => hRate r q)
    post arrive barArrive hp (fun j => (hpair j).2)

#print axioms actual_prescribed_state_reversal_and_rate_product
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal
