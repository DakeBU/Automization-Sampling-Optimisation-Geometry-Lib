import AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.SphericalFlux

open MeasureTheory Metric Set Filter
open scoped Topology RealInnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis
noncomputable section
attribute [local instance] Classical.propDecidable

-- Dimension one is outside HFT's standing range. A nonzero constant field
-- checks the opposite endpoint orientations in the literal polar measure.
example : (∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin 1)) 1, ζ.1 0
    ∂(volume : Measure (EuclideanSpace ℝ (Fin 1))).toSphere) = 0 := by
  let e : EuclideanSpace ℝ (Fin 1) := EuclideanSpace.single 0 1
  have h := Calculus.BallFlux.ball_flux_eq_integral_divergence
    (fun _ : EuclideanSpace ℝ (Fin 1) => e) 0 2 (by norm_num)
    (fun _ _ => contDiffAt_const)
  have hd : Calculus.Divergence.coordinateDivergence
      (fun _ : EuclideanSpace ℝ (Fin 1) => e) = 0 := by
    funext x
    rw [Calculus.Divergence.coordinateDivergence_eq_sum_fderiv_apply_of_hasFDerivAt
      (hasFDerivAt_const e x)]
    simp
  simpa [hd, e, EuclideanSpace.inner_single_left] using h.2.2.symm

-- This field is only locally C1 near the selected closed ball. No global
-- regularity premise can replace the sealed local premise in this example.
example :
    let F : EuclideanSpace ℝ (Fin 3) → EuclideanSpace ℝ (Fin 3) :=
      fun x => if x ∈ ball 0 2 then x else 0
    IntegrableOn (Calculus.Divergence.coordinateDivergence F) (ball 0 1) ∧
    (∫ x in ball 0 1, Calculus.Divergence.coordinateDivergence F x) =
      ∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin 3)) 1, inner ℝ (F ζ.1) ζ.1
        ∂(volume : Measure (EuclideanSpace ℝ (Fin 3))).toSphere := by
  dsimp only
  let F : EuclideanSpace ℝ (Fin 3) → EuclideanSpace ℝ (Fin 3) :=
    fun x => if x ∈ ball 0 2 then x else 0
  have hF : ∀ x ∈ closedBall (0 : EuclideanSpace ℝ (Fin 3)) 1, ContDiffAt ℝ 1 F x := by
    intro x hx
    have hx2 : x ∈ ball (0 : EuclideanSpace ℝ (Fin 3)) 2 := by
      have h := mem_closedBall.mp hx
      rw [mem_ball]
      linarith
    apply ContDiffAt.congr_of_eventuallyEq
      (contDiffAt_id : ContDiffAt ℝ 1 (fun y : EuclideanSpace ℝ (Fin 3) => y) x)
    filter_upwards [isOpen_ball.mem_nhds hx2] with y hy
    simp only [F, if_pos hy, id_eq]
  have h := Calculus.BallFlux.ball_flux_eq_integral_divergence F 0 1 (by norm_num) hF
  exact ⟨h.1, by simpa only [zero_add, one_smul, one_pow, one_mul] using h.2.2⟩

-- The original representative jumps outside the parent ball. The theorem
-- must retain one extension that works at both radii, including the endpoint.
example :
    let u : EuclideanSpace ℝ (Fin 2) → ℝ :=
      fun x => if x ∈ closedBall 0 2 then 0 else 17
    let τ := (volume : Measure (EuclideanSpace ℝ (Fin 2))).toSphere
    ∃ v : EuclideanSpace ℝ (Fin 2) → ℝ,
      EqOn v u (closedBall 0 2) ∧
      Integrable (fun ζ : sphere (0 : EuclideanSpace ℝ (Fin 2)) 1 =>
        inner ℝ (gradient v ζ.1) ζ.1) τ ∧
      (∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin 2)) 1,
        inner ℝ (gradient v ζ.1) ζ.1 ∂τ) = 0 ∧
      Integrable (fun ζ : sphere (0 : EuclideanSpace ℝ (Fin 2)) 1 =>
        inner ℝ (gradient v ((2 : ℝ) • ζ.1)) ζ.1) τ ∧
      (∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin 2)) 1,
        inner ℝ (gradient v ((2 : ℝ) • ζ.1)) ζ.1 ∂τ) = 0 := by
  dsimp only
  let u : EuclideanSpace ℝ (Fin 2) → ℝ :=
    fun x => if x ∈ closedBall 0 2 then 0 else 17
  have hu : ∃ v : EuclideanSpace ℝ (Fin 2) → ℝ,
      InnerProductSpace.HarmonicOnNhd v (closedBall 0 2) ∧ EqOn v u (closedBall 0 2) := by
    refine ⟨fun _ => 0, InnerProductSpace.harmonicOnNhd_const 0, ?_⟩
    intro x hx
    simp only [u, if_pos hx]
  obtain ⟨v, _, hvu, hflux⟩ := Harmonic.SphericalFlux.harmonic_closedBall_zero_flux
    (by norm_num : 2 ≤ 2) u 0 2 (by norm_num) hu
  have h1 := hflux 1 (by norm_num) (by norm_num)
  have h2 := hflux 2 (by norm_num) le_rfl
  refine ⟨v, hvu, ?_, ?_, ?_, ?_⟩
  · simpa only [zero_add, one_smul] using h1.1
  · simpa only [zero_add, one_smul] using h1.2
  · simpa only [zero_add] using h2.1
  · simpa only [zero_add] using h2.2

#print axioms Calculus.BallFlux.ball_flux_eq_integral_divergence
#print axioms Harmonic.SphericalFlux.harmonic_closedBall_zero_flux
end
