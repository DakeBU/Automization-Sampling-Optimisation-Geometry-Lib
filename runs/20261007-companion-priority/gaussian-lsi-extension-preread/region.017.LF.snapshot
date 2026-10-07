lemma sum_expected_condEnt_le_grad_norm (n : ℕ) (g : (Fin n → ℝ) → ℝ)
    (hg : MemW12GaussianPi n g (GaussianMeasure.stdGaussianPi n))
    (hg_diff : Differentiable ℝ g)
    (hg_grad_cont : ∀ i, Continuous (fun x => partialDeriv i g x))
    (hg_log_int : Integrable (fun x => (g x)^2 * log ((g x)^2)) (GaussianMeasure.stdGaussianPi n)) :
    ∑ i : Fin n,
        ∫ x, SubAddEnt.condEntExceptCoord (μs := fun _ : Fin n => gaussianReal 0 1) i
          (fun z => (g z)^2) x ∂(GaussianMeasure.stdGaussianPi n) ≤
      2 * ∫ x, gradNormSq n g x ∂(GaussianMeasure.stdGaussianPi n) := by
