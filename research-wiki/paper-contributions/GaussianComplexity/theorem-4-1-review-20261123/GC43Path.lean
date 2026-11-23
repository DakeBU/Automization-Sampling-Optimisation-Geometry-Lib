import GC44GramUse
import GC32Algorithm

/-! # The deterministic query path and Krylov induction from Appendix C.1 -/
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior (precisionReply continuous_precisionReply)
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle (run)

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

variable {d q : ℕ} {κ : ℝ}

/-- Every start is allowed in this auxiliary span. The degree grows once per
actual or padded interaction, and reaches exactly the source degree q. -/
private def stage (κ : ℝ) (g : Starts d q) (t : ℕ) : Submodule ℝ (Fin d → ℝ) :=
  Submodule.span ℝ (Set.range (fun p : Fin (q+1) × Fin (t+1) =>
    (diagonalPrecision d κ ^ p.2.val) *ᵥ WithLp.ofLp (g p.1)))

private theorem stage_contains (g : Starts d q) (t : ℕ) (a : Fin (q+1)) :
    WithLp.ofLp (g a) ∈ stage κ g t := by
  apply Submodule.subset_span
  exact ⟨(a,0), by simp⟩

private theorem stage_succ (g : Starts d q) (t : ℕ) : stage κ g t ≤ stage κ g (t+1) := by
  apply Submodule.span_le.mpr
  rintro _ ⟨⟨a,j⟩,rfl⟩
  exact Submodule.subset_span ⟨(a,j.castSucc),rfl⟩

private theorem stage_mul (g : Starts d q) (t : ℕ) {u : Fin d → ℝ} (hu : u ∈ stage κ g t) :
    (diagonalPrecision d κ) *ᵥ u ∈ stage κ g (t+1) := by
  have h : stage κ g t ≤ (stage κ g (t+1)).comap (diagonalPrecision d κ).mulVecLin := by
    apply Submodule.span_le.mpr
    rintro _ ⟨⟨a,j⟩,rfl⟩
    apply Submodule.subset_span
    refine ⟨(a,j.succ), ?_⟩
    simp only [Fin.val_succ,pow_succ',Matrix.mulVecLin_apply,Matrix.mulVec_mulVec]
  exact h hu

/-- Each new preimage belongs to the previous space plus one fresh Gaussian
start. The forward revelation can add its Λ-image. The preimage of the final
output requires its own start, but never an additional matrix power. -/
theorem krylov_of_revelations (κ : ℝ) (g : Starts d q) (E : ℕ → Submodule ℝ (Fin d → ℝ))
    (u : Fin q → (Fin d → ℝ)) (xback : Fin d → ℝ)
    (h₀ : E 0 = ⊥)
    (hu : ∀ i : Fin q, u i ∈ E i.val ⊔ Submodule.span ℝ {WithLp.ofLp (g i.castSucc)})
    (hE : ∀ i : Fin q, E (i.val+1) ≤ (E i.val ⊔ Submodule.span ℝ {u i}) ⊔
      Submodule.span ℝ {diagonalPrecision d κ *ᵥ u i})
    (hx : xback ∈ E q ⊔ Submodule.span ℝ {WithLp.ofLp (g (Fin.last q))}) :
    xback ∈ krylov d q κ g := by
  have hstage : ∀ t ≤ q, E t ≤ stage κ g t := by
    intro t
    induction t with
    | zero => intros; rw [h₀]; exact bot_le
    | succ t ih =>
      intro ht
      let i : Fin q := ⟨t,by omega⟩
      have hle := ih (show t ≤ q by omega)
      have hus : u i ∈ stage κ g t :=
        (sup_le hle ((Submodule.span_singleton_le_iff_mem ..).mpr (stage_contains g t i.castSucc))) (hu i)
      exact (hE i).trans (sup_le (sup_le (hle.trans (stage_succ g t))
          ((Submodule.span_singleton_le_iff_mem ..).mpr (stage_succ g t hus)))
        ((Submodule.span_singleton_le_iff_mem ..).mpr (stage_mul g t hus)))
  exact (sup_le (hstage q le_rfl) ((Submodule.span_singleton_le_iff_mem ..).mpr
    (stage_contains g q (Fin.last q)))) hx

variable {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]

/-- A stopped program contributes the dummy zero query. -/
def queryOrZero (alg : Algorithm d Seed State) (s : State) : Space d :=
  (alg.next s).elim (fun _ => 0) id

/-- A single observed gradient vector supplies the full value-and-gradient
reply. The halted state stays fixed throughout padding. -/
def observedStep (alg : Algorithm d Seed State) (s : State) (w : Space d) : State :=
  match alg.next s with
  | .inl _ => s
  | .inr x => alg.update s x (inner ℝ x w / 2,w)

theorem measurable_queryOrZero (alg : Algorithm d Seed State) : Measurable (queryOrZero alg) :=
  (measurable_const.sumElim measurable_id).comp alg.measurable_next

theorem measurable_observedStep (alg : Algorithm d Seed State) : Measurable (Function.uncurry (observedStep alg)) := by
  let Z := State × Space d
  have hd : Measurable (fun z : Z => (MeasurableEquiv.prodSumDistrib Z Unit (Space d)) (z,alg.next z.1)) :=
    (MeasurableEquiv.prodSumDistrib Z Unit (Space d)).measurable.comp
      (measurable_id.prodMk (alg.measurable_next.comp measurable_fst))
  have h₀ : Measurable (fun z : Z × Unit => z.1.1) := measurable_fst.comp measurable_fst
  have hi : Measurable (fun z : Z × Space d => inner ℝ z.2 z.1.2) :=
    (continuous_fst.inner continuous_snd : Continuous (fun p : Space d × Space d => inner ℝ p.1 p.2)).measurable.comp
      (measurable_snd.prodMk (measurable_snd.comp measurable_fst))
  have h₁ : Measurable (fun z : Z × Space d => alg.update z.1.1 z.2 (inner ℝ z.2 z.1.2 / 2, z.1.2)) := by
    exact alg.measurable_update.comp ((measurable_fst.comp measurable_fst).prodMk (measurable_snd.prodMk
      ((hi.div_const _).prodMk
        (measurable_snd.comp measurable_fst))))
  convert (h₀.sumElim h₁).comp hd using 1
  funext z
  obtain ⟨s,w⟩ := z
  cases h : alg.next s <;> simp [Function.uncurry,Function.comp_apply,observedStep,h] <;> rfl

private theorem run_zero_state (alg : Algorithm d Seed State) (A : Precision d) (s : State) :
    (run alg.next alg.update (precisionReply A) 0 s).1.1 = s := by
  cases h : alg.next s <;> simp [run,h]

/-- Algebraic equivalence for an additional query, including early stopping. -/
private theorem run_state_succ (alg : Algorithm d Seed State) (A : Precision d) (t : ℕ) (s : State) :
    let y := (run alg.next alg.update (precisionReply A) t s).1.1
    (run alg.next alg.update (precisionReply A) (t+1) s).1.1 =
      observedStep alg y (precisionReply A (queryOrZero alg y)).2 := by
  induction t generalizing s with
  | zero =>
    dsimp only
    rw [run_zero_state]
    cases h : alg.next s with
    | inl u => simp [run,h,observedStep]
    | inr x =>
      rw [run,h]
      simp only [queryOrZero,observedStep,h,Sum.elim_inr,id_eq]
      apply run_zero_state
  | succ t ih =>
    dsimp only
    cases h : alg.next s with
    | inl u => simp [run,h,observedStep]
    | inr x =>
      let y := alg.update s x (precisionReply A x)
      have he (k : ℕ) : (run alg.next alg.update (precisionReply A) (k+1) s).1.1 =
          (run alg.next alg.update (precisionReply A) k y).1.1 := by rw [run,h]
      rw [he (t+1), he t]
      exact ih y

/-- Actual state at the end of t interactions, also during padding. -/
def paddedState (alg : Algorithm d Seed State) (A : Precision d) (t : ℕ) (s : Seed) : State :=
  (run alg.next alg.update (precisionReply A) t (alg.start s)).1.1

theorem paddedState_zero (alg : Algorithm d Seed State) (A : Precision d) (s : Seed) :
    paddedState alg A 0 s = alg.start s := run_zero_state alg A _

theorem paddedState_succ (alg : Algorithm d Seed State) (A : Precision d) (t : ℕ) (s : Seed) :
    paddedState alg A (t+1) s = observedStep alg (paddedState alg A t s)
      (precisionReply A (queryOrZero alg (paddedState alg A t s))).2 := run_state_succ alg A t _

set_option backward.isDefEq.respectTransparency false in
set_option maxHeartbeats 800000 in
theorem measurable_paddedState (alg : Algorithm d Seed State) (t : ℕ) :
    Measurable (fun p : Seed × Precision d => paddedState alg p.2 t p.1) := by
  have hm : Measurable (Function.uncurry (@precisionReply d)) := (continuous_precisionReply d).measurable
  have hi : Measurable (fun p : Seed × Precision d => (p.2, alg.start p.1)) :=
    measurable_snd.prodMk (alg.measurable_start.comp measurable_fst)
  let exec (p : Precision d × State) : State := (run alg.next alg.update (precisionReply p.1) t p.2).1.1
  have hrun : Measurable exec := alg.measurable_run_state (@precisionReply d) hm t
  change Measurable (exec ∘ (fun p : Seed × Precision d => (p.2,alg.start p.1)))
  exact hrun.comp hi

/-- In the hidden basis the true gradient reply has exactly the forward image
of Λ times the revealed preimage. -/
theorem gradient_hiddenPrecision (κ : ℝ) (O : Matrix.orthogonalGroup (Fin d) ℝ) (x : Space d) :
    (precisionReply (hiddenPrecision κ O) x).2 =
      WithLp.toLp 2 (O.val *ᵥ (diagonalPrecision d κ *ᵥ (O.val.transpose *ᵥ WithLp.ofLp x))) := by
  simp only [precisionReply,hiddenPrecision,Matrix.mulVec_mulVec,Matrix.mul_assoc]

/-- The first q preimages are padded query points. The last preimage is the
actual returned vector, so asking for it consumes no additional oracle call. -/
def paddedPoint (alg : Algorithm d Seed State) (A : Precision d) (q : ℕ) (i : Fin (q+1)) (s : Seed) : Space d :=
  let state := paddedState alg A i.val s
  if i.val = q then alg.output state else queryOrZero alg state

theorem paddedPoint_query (alg : Algorithm d Seed State) (A : Precision d) (i : Fin q) (s : Seed) :
    paddedPoint alg A q i.castSucc s = queryOrZero alg (paddedState alg A i.val s) := by
  simp [paddedPoint, Nat.ne_of_lt i.isLt]

theorem paddedPoint_last (alg : Algorithm d Seed State) (A : Precision d) (s : Seed) :
    paddedPoint alg A q (Fin.last q) s = alg.sample q A s := by simp [paddedPoint,Algorithm.sample,paddedState]

theorem measurable_paddedPoint (alg : Algorithm d Seed State) (q : ℕ) (i : Fin (q+1)) :
    Measurable (fun p : Seed × Precision d => paddedPoint alg p.2 q i p.1) := by
  unfold paddedPoint
  split_ifs
  · exact alg.measurable_output.comp (measurable_paddedState alg _)
  · exact (measurable_queryOrZero alg).comp (measurable_paddedState alg _)

#print axioms krylov_of_revelations
#print axioms paddedState_succ

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
