import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseWork

/-! Algorithm 3.1 / D.2 / D.4: finite exact-real gradient-query execution.
Successful runs charge the actual interpreter tests and each noisy gradient.
Finite fuel is an execution certificate, not a source algorithm cost premise.
-/

noncomputable section
open MeasureTheory ProbabilityTheory InnerProductSpace
open scoped NNReal BigOperators

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.CountedPhaseProgram

private def collectQueries {E : Type*} :
    (m : ℕ) → (Fin m → Option (E × ℕ)) → Option ((Fin m → E) × ℕ)
  | 0, _ => some (Fin.elim0, 0)
  | m+1, f => do
    let r ← f 0
    let s ← collectQueries m (fun i => f i.succ)
    pure (Fin.cons r.1 s.1, r.2+s.2)

private theorem collectQueries_some {E : Type*} (m : ℕ)
    (f : Fin m → Option (E × ℕ)) (x : Fin m → E) (c : Fin m → ℕ)
    (hf : ∀ i, f i = some (x i,c i)) :
    collectQueries m f = some (x,∑ i, c i) := by
  have heq : f = fun i => some (x i,c i) := funext hf
  rw [heq]
  clear hf heq f
  induction m with
  | zero =>
    have hx : x = Fin.elim0 := funext fun i => Fin.elim0 i
    simp [collectQueries, hx]
  | succ m ih =>
    have hx : Fin.cons (x 0) (fun i : Fin m => x i.succ) = x := by
      funext i
      cases i using Fin.cases <;> simp
    simp [collectQueries, ih, Fin.sum_univ_succ, hx]

section Execution
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- Execute both finite query arrays in index order. Each successful proximal
call returns its own charged tests; evaluating the shifted gradient charges one
additional query. The second layer uses the first layer's returned gradients.
Failure at any insufficient-fuel call returns none; no cost is claimed for a
failed execution by this successful-return representation. -/
def phaseQuery {m : ℕ} (g : E → E) (eta eps h : ℝ)
    (t : Fin m → ℝ) (omega : Fin m → Fin m → ℝ)
    (positionWeight momentumWeight : Fin m → ℝ) (fuel : E → ℕ)
    (w : (E × E) × ((E × E) × ((Fin m → E) × (Fin m → E)))) :
    Option ((E × E) × ℕ) := do
  let P0 := Real.exp (-h/2) • w.1.2 + Real.sqrt (1-Real.exp (-h)) • w.2.1.1
  let Y0 := fun i => w.1.1 + t i • P0
  let r0 ← collectQueries m (fun i =>
    (ApproximateProximalExecution.proximalQuery g eta eps (Y0 i) (fuel (Y0 i)) (Y0 i)).map
      (fun r => (g (r.1+Real.sqrt eta • w.2.2.1 i),r.2+1)))
  let Y1 := fun i => Y0 i - ∑ j, omega i j • r0.1 j
  let r1 ← collectQueries m (fun i =>
    (ApproximateProximalExecution.proximalQuery g eta eps (Y1 i) (fuel (Y1 i)) (Y1 i)).map
      (fun r => (g (r.1+Real.sqrt eta • w.2.2.2 i),r.2+1)))
  pure ((w.1.1+h • P0-∑ j, positionWeight j • r1.1 j,
    Real.exp (-h/2) • (P0-∑ j, momentumWeight j • r1.1 j) +
      Real.sqrt (1-Real.exp (-h)) • w.2.1.2),r0.2+r1.2)

private theorem phaseQuery_success {m : ℕ} (g q : E → E) (N fuel : E → ℕ)
    (eta eps h : ℝ) (t : Fin m → ℝ) (omega : Fin m → Fin m → ℝ)
    (positionWeight momentumWeight : Fin m → ℝ)
    (hrun : ∀ y, ApproximateProximalExecution.proximalQuery g eta eps y (fuel y) y =
      some (q y,N y+1))
    (w : (E × E) × ((E × E) × ((Fin m → E) × (Fin m → E)))) :
    let P0 := Real.exp (-h/2) • w.1.2 + Real.sqrt (1-Real.exp (-h)) • w.2.1.1
    let Y0 := fun i => w.1.1+t i • P0
    let Z0 := fun j => g (q (Y0 j)+Real.sqrt eta • w.2.2.1 j)
    let Y1 := fun i => Y0 i-∑ j, omega i j • Z0 j
    let Z1 := fun j => g (q (Y1 j)+Real.sqrt eta • w.2.2.2 j)
    phaseQuery g eta eps h t omega positionWeight momentumWeight fuel w =
      some ((w.1.1+h • P0-∑ j, positionWeight j • Z1 j,
        Real.exp (-h/2) • (P0-∑ j, momentumWeight j • Z1 j)+
          Real.sqrt (1-Real.exp (-h)) • w.2.1.2),
        2*m+∑ i, ((N (Y0 i)+1)+(N (Y1 i)+1))) := by
  classical
  dsimp only
  let P0 := Real.exp (-h/2) • w.1.2 + Real.sqrt (1-Real.exp (-h)) • w.2.1.1
  let Y0 := fun i => w.1.1+t i • P0
  let Z0 := fun j => g (q (Y0 j)+Real.sqrt eta • w.2.2.1 j)
  let Y1 := fun i => Y0 i-∑ j, omega i j • Z0 j
  let Z1 := fun j => g (q (Y1 j)+Real.sqrt eta • w.2.2.2 j)
  have h0 : collectQueries m (fun i =>
      (ApproximateProximalExecution.proximalQuery g eta eps (Y0 i) (fuel (Y0 i)) (Y0 i)).map
        (fun r => (g (r.1+Real.sqrt eta • w.2.2.1 i),r.2+1))) =
      some (Z0,∑ i, ((N (Y0 i)+1)+1)) := by
    apply collectQueries_some m _ Z0 (fun i => (N (Y0 i)+1)+1)
    intro i
    rw [hrun]
    rfl
  have h1 : collectQueries m (fun i =>
      (ApproximateProximalExecution.proximalQuery g eta eps (Y1 i) (fuel (Y1 i)) (Y1 i)).map
        (fun r => (g (r.1+Real.sqrt eta • w.2.2.2 i),r.2+1))) =
      some (Z1,∑ i, ((N (Y1 i)+1)+1)) := by
    apply collectQueries_some m _ Z1 (fun i => (N (Y1 i)+1)+1)
    intro i
    rw [hrun]
    rfl
  have hc : (∑ i, ((N (Y0 i)+1)+1))+(∑ i, ((N (Y1 i)+1)+1)) =
      2*m+∑ i, ((N (Y0 i)+1)+(N (Y1 i)+1)) := by
    simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
      Fintype.card_fin, smul_eq_mul, mul_one]
    omega
  unfold phaseQuery
  try dsimp only
  rw [h0]
  dsimp [Bind.bind, Option.bind]
  rw [h1]
  dsimp [Bind.bind, Option.bind, Pure.pure]
  rw [hc]

end Execution


section ExpectedWork
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- A successful finite two-layer phase executes the full Gaussian update and
returns its actual gradient-query count. From the incoming state L2 budget,
that count is measurable and integrable under the same full phase law, with
all proximal terminal tests and all direct noisy gradients charged. -/
theorem implemented_phase_expected_query_work {m : ℕ} {V : E → ℝ} {κ : ℝ≥0}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹ * ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2)
    {eta c eps : ℝ} (heta : 0 < eta) (hec : eta ≤ c) (hc : c < 1) (heps : 0 < eps)
    (ν : Measure (E × E)) [IsProbabilityMeasure ν]
    (xstar : E) (hstar : gradient V xstar = 0)
    {h M S : ℝ} (hh : 0 ≤ h) (hM : 0 ≤ M) (hS : 0 ≤ S)
    (hstateI : Integrable (fun s : E × E => ‖s.1-xstar‖^2 + ‖s.2‖^2) ν)
    (hstate : (∫ s : E × E, ‖s.1-xstar‖^2 + ‖s.2‖^2 ∂ν) ≤ M)
    (t : Fin m → ℝ) (ht : ∀ i, |t i| ≤ 1) (omega : Fin m → Fin m → ℝ)
    (hrow : ∀ i, (∑ j, |omega i j|) ≤ S)
    (positionWeight momentumWeight : Fin m → ℝ) :
    let a := Real.exp (-h/2)
    let sigma := Real.sqrt (1-Real.exp (-h))
    let gi := Measure.pi (fun _ : Fin m => stdGaussian E)
    let γ := ((stdGaussian E).prod (stdGaussian E)).prod (gi.prod gi)
    let μ := ν.prod γ
    let MR := M + (1-Real.exp (-h)) * (Module.finrank ℝ E : ℝ)
    let B := 6*MR + 3*eps^2 + 3*eta*(Module.finrank ℝ E : ℝ)
    let C := 2 + (1+Real.log ((1-c)⁻¹))/(-Real.log c)
    let L0 := C*(1+Real.log (1+Real.sqrt (2*MR)/eps))
    let L1 := C*(1+Real.log (1+Real.sqrt (4*MR+2*S^2*B)/eps))
    ∃ p q : E → E, ∃ N : E → ℕ,
      Measurable p ∧ Measurable q ∧ Measurable N ∧
      (∀ y, p y + eta • gradient V (p y) = y ∧ ‖q y-p y‖ ≤ eps ∧
        ApproximateProximalExecution.proximalQuery (gradient V) eta eps y (N y+1) y =
          some (q y,N y+1)) ∧
      let P0 := fun w : (E × E) × ((E × E) × ((Fin m → E) × (Fin m → E))) =>
        a • w.1.2 + sigma • w.2.1.1
      let Y0 := fun i w => w.1.1 + t i • P0 w
      let Z0 := fun j w => gradient V (q (Y0 j w) + Real.sqrt eta • w.2.2.1 j)
      let Y1 := fun i w => Y0 i w - ∑ j, omega i j • Z0 j w
      let Z1 := fun j w => gradient V (q (Y1 j w) + Real.sqrt eta • w.2.2.2 j)
      let Φ := fun w => (w.1.1 + h • P0 w - ∑ j, positionWeight j • Z1 j w,
        a • (P0 w - ∑ j, momentumWeight j • Z1 j w) + sigma • w.2.1.2)
      let T := fun w => 2*m+∑ i, ((N (Y0 i w)+1)+(N (Y1 i w)+1))
      Measurable Φ ∧ Measurable T ∧
      (∃ K : Kernel (E × E) (E × E), IsMarkovKernel K ∧
        ∀ s, K s = γ.map (fun z => Φ (s,z))) ∧
      (∀ w, phaseQuery (gradient V) eta eps h t omega positionWeight momentumWeight
        (fun y => N y+1) w = some (Φ w,T w)) ∧
      Integrable (fun w => (T w : ℝ)) μ ∧
      (∫ w, (T w : ℝ) ∂μ) ≤ (m : ℝ)*(2+L0+L1) := by
  classical
  dsimp only
  let gi := Measure.pi (fun _ : Fin m => stdGaussian E)
  let γ := ((stdGaussian E).prod (stdGaussian E)).prod (gi.prod gi)
  let μ := ν.prod γ
  let MR := M+(1-Real.exp (-h))*(Module.finrank ℝ E : ℝ)
  let B := 6*MR+3*eps^2+3*eta*(Module.finrank ℝ E : ℝ)
  let C := 2+(1+Real.log ((1-c)⁻¹))/(-Real.log c)
  let L0 := C*(1+Real.log (1+Real.sqrt (2*MR)/eps))
  let L1 := C*(1+Real.log (1+Real.sqrt (4*MR+2*S^2*B)/eps))
  obtain ⟨p,q,N,hp,hq,hN,hall,hΦ,K,hK,hKlaw,hw0,hw1⟩ :=
    ImplementedPhaseWork.implemented_phase_query_moments_and_work hκ hV hH heta hec hc heps
      ν xstar hstar hh hM hS hstateI hstate t ht omega hrow positionWeight momentumWeight
  let P0 := fun w : (E × E) × ((E × E) × ((Fin m → E) × (Fin m → E))) =>
    Real.exp (-h/2) • w.1.2+Real.sqrt (1-Real.exp (-h)) • w.2.1.1
  let Y0 := fun i w => w.1.1+t i • P0 w
  let Z0 := fun j w => gradient V (q (Y0 j w)+Real.sqrt eta • w.2.2.1 j)
  let Y1 := fun i w => Y0 i w-∑ j, omega i j • Z0 j w
  let T := fun w => 2*m+∑ i, ((N (Y0 i w)+1)+(N (Y1 i w)+1))
  have hg : Measurable (gradient V) := by
    unfold gradient
    exact ((InnerProductSpace.toDual ℝ E).symm.continuous.comp
      (hV.continuous_fderiv (by norm_num))).measurable
  have hTm : Measurable T := by fun_prop
  have hi0 (i : Fin m) : Integrable (fun w => (N (Y0 i w) : ℝ)+1) μ :=
    (hw0 i).2.2.1
  have hi1 (i : Fin m) : Integrable (fun w => (N (Y1 i w) : ℝ)+1) μ :=
    (hw1 i).2.2.1
  have hsum : Integrable (fun w => ∑ i, (((N (Y0 i w) : ℝ)+1)+
      ((N (Y1 i w) : ℝ)+1))) μ :=
    integrable_finsetSum Finset.univ (fun i _ => (hi0 i).add (hi1 i))
  have hTex : (fun w => (T w : ℝ)) = fun w => 2*(m : ℝ)+
      ∑ i, (((N (Y0 i w) : ℝ)+1)+((N (Y1 i w) : ℝ)+1)) := by
    funext w
    simp only [T, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat, Nat.cast_sum, Nat.cast_one]
  have hTi : Integrable (fun w => (T w : ℝ)) μ := by
    rw [hTex]
    exact (integrable_const (2*(m : ℝ))).add hsum
  refine ⟨p,q,N,hp,hq,hN,hall,hΦ,hTm,⟨K,hK,hKlaw⟩,?_,hTi,?_⟩
  · intro w
    exact phaseQuery_success (gradient V) q N (fun y => N y+1) eta eps h t omega
      positionWeight momentumWeight (fun y => (hall y).2.2) w
  · change (∫ w, (T w : ℝ) ∂μ) ≤ (m : ℝ)*(2+L0+L1)
    rw [hTex, integral_add (integrable_const _) hsum]
    rw [integral_finsetSum (f := fun i w => ((N (Y0 i w) : ℝ)+1)+
      ((N (Y1 i w) : ℝ)+1)) Finset.univ (fun i _ => (hi0 i).add (hi1 i))]
    have hb : (∑ i : Fin m, ∫ w, (((N (Y0 i w) : ℝ)+1)+
        ((N (Y1 i w) : ℝ)+1)) ∂μ) ≤ ∑ _i : Fin m, (L0+L1) := by
      apply Finset.sum_le_sum
      intro i _
      rw [integral_add (hi0 i) (hi1 i)]
      exact add_le_add (hw0 i).2.2.2 (hw1 i).2.2.2
    calc
      _ ≤ (∫ _w, 2*(m : ℝ) ∂μ)+∑ _i : Fin m, (L0+L1) := add_le_add_right hb _
      _ = (m : ℝ)*(2+L0+L1) := by
        simp [integral_const, Finset.sum_const, nsmul_eq_mul]
        ring

end ExpectedWork

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.CountedPhaseProgram
