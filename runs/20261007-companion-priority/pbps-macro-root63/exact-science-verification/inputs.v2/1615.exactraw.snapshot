import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ImplementedPhaseKernel

open AutoSamplingTheory.ExampleCases.SmoothedPicardHMC
open ImplementedPhaseKernel InnerProductSpace MeasureTheory ProbabilityTheory
open scoped BigOperators NNReal

#check implemented_phase_kernel
#print axioms implemented_phase_kernel

-- Positive-dimensional, two-node law: both innovation arrays and both
-- half-refreshes survive in the exact transition formula. The Hessian premise
-- is the source's normalized potential class, not an output-law assumption.
example {V : ℝ → ℝ} (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : ℝ, ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖ ^ 2) :
    ∃ q : ℝ → ℝ, ∃ N : ℝ → ℕ, ∃ K : Kernel (ℝ × ℝ) (ℝ × ℝ),
      IsMarkovKernel K ∧ Measurable q ∧
      (∀ y, ApproximateProximalExecution.proximalQuery (gradient V) (3 / 4) (1 / 10)
        y (N y + 1) y = some (q y, N y + 1)) ∧
      (∀ s, K s Set.univ = 1) ∧
      K (0, 0) =
        (((stdGaussian ℝ).prod (stdGaussian ℝ)).prod
          ((Measure.pi (fun _ : Fin 2 => stdGaussian ℝ)).prod
            (Measure.pi (fun _ : Fin 2 => stdGaussian ℝ)))).map
          (fun z : (ℝ × ℝ) × ((Fin 2 → ℝ) × (Fin 2 → ℝ)) =>
            let P0 := Real.sqrt (1 - Real.exp (-1)) * z.1.1
            let Y0 := fun i : Fin 2 => (i.val : ℝ) * P0
            let Z0 := fun j => gradient V (q (Y0 j) + Real.sqrt (3 / 4) * z.2.1 j)
            let Y1 := fun i => Y0 i - ∑ j, (1 / 4 : ℝ) * Z0 j
            let Z1 := fun j => gradient V (q (Y1 j) + Real.sqrt (3 / 4) * z.2.2 j)
            (P0 - ∑ j, (1 / 4 : ℝ) * Z1 j,
              Real.exp (-1 / 2) * (P0 - ∑ j, (1 / 2 : ℝ) * Z1 j) +
                Real.sqrt (1 - Real.exp (-1)) * z.1.2)) := by
  have hH' : ∀ x v : ℝ, ((1 : ℝ≥0) : ℝ)⁻¹ * ‖v‖ ^ 2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖ ^ 2 := by simpa using hH
  obtain ⟨p, q, N, hp, hq, hN, hrun, hvar, hΦ, K, hK, hKs⟩ :=
    implemented_phase_kernel (E := ℝ) (ι := Fin 2) (κ := 1)
      (by norm_num) hV hH' (eta := 3 / 4) (c := 7 / 8) (eps := 1 / 10)
      (by norm_num) (by norm_num) (by norm_num) (by norm_num)
      1 (by norm_num) (fun i => i.val) (fun _ _ => 1 / 4)
      (fun _ => 1 / 4) (fun _ => 1 / 2)
  letI := hK
  refine ⟨q, N, K, hK, hq, fun y => (hrun y).2.2, fun s => measure_univ, ?_⟩
  simpa only [smul_eq_mul, mul_zero, zero_add, one_mul] using hKs (0, 0)
