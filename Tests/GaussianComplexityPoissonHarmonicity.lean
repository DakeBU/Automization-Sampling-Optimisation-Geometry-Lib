import AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.PoissonKernel

open AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.PoissonKernel

-- Actual book-dimension endpoint, at a point outside the unit ball.
example :
    let ζ : EuclideanSpace ℝ (Fin 2) := EuclideanSpace.single 0 1
    InnerProductSpace.HarmonicAt
      (fun x : EuclideanSpace ℝ (Fin 2) => (1 - ‖x‖ ^ 2) / ‖x - ζ‖ ^ 2)
      ((2 : ℝ) • ζ) := by
  dsimp only
  have hζ : ‖(EuclideanSpace.single 0 1 : EuclideanSpace ℝ (Fin 2))‖ = 1 := by simp
  apply poissonKernel_harmonicOnNhd (by norm_num) _ hζ
  simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
  intro h
  have hh := congrArg norm h
  norm_num [norm_smul, hζ] at hh

-- Actual Gaussian source dimension n=3, at the origin.
example :
    let ζ : EuclideanSpace ℝ (Fin 3) := EuclideanSpace.single 0 1
    InnerProductSpace.HarmonicAt
      (fun x : EuclideanSpace ℝ (Fin 3) => (1 - ‖x‖ ^ 2) / ‖x - ζ‖ ^ 3) 0 := by
  dsimp only
  have hζ : ‖(EuclideanSpace.single 0 1 : EuclideanSpace ℝ (Fin 3))‖ = 1 := by simp
  apply poissonKernel_harmonicOnNhd (by norm_num) _ hζ
  simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
  intro h
  have hh := congrArg norm h
  norm_num [hζ] at hh

-- A genuine closed-ball neighborhood consumer of the same literal kernel.
-- No mean-value or normalized-surface integral is assumed or concluded.
example {n : ℕ} (hn : 2 ≤ n) (ζ : EuclideanSpace ℝ (Fin n))
    (hζ : ‖ζ‖ = 1) {r : ℝ} (hr : r < 1) :
    InnerProductSpace.HarmonicOnNhd
      (fun x : EuclideanSpace ℝ (Fin n) => (1 - ‖x‖ ^ 2) / ‖x - ζ‖ ^ n)
      (Metric.closedBall 0 r) := by
  apply (poissonKernel_harmonicOnNhd hn ζ hζ).mono
  intro x hx
  have hnorm : ‖x‖ ≤ r := by simpa using hx
  simp only [Set.mem_compl_iff, Set.mem_singleton_iff]
  intro heq
  rw [heq, hζ] at hnorm
  exact (not_le_of_gt hr) hnorm

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.PoissonKernel.poissonKernel_harmonicOnNhd
