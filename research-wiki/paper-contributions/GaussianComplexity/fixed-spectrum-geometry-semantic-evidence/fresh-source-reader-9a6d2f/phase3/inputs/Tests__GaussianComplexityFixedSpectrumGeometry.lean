import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic

open Matrix InnerProductSpace
open scoped ContDiff
set_option autoImplicit false

/- The actual same-input exact reply is Borel for each fixed source O.
The new producer supplies scalar continuity and genuine gradient continuity;
the canonical actual first-order result identifies that gradient with the
literal precision reply. This is not a whole adaptive or joint-in-O theorem. -/
private theorem actual_first_order_oracle_measurable {d : ℕ} (hd : 2 ≤ d)
    {κ : ℝ} (hκ : 2 ≤ κ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  let query : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) :=
    fun x => WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
  @Measurable (EuclideanSpace ℝ (Fin d))
    (ℝ × EuclideanSpace ℝ (Fin d))
    (borel (EuclideanSpace ℝ (Fin d)))
    (borel (ℝ × EuclideanSpace ℝ (Fin d)))
    (fun x => (f x, query x)) := by
  classical
  dsimp only
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let A : Matrix (Fin d) (Fin d) ℝ :=
    (O : Matrix (Fin d) (Fin d) ℝ) *
      Matrix.diagonal (fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)) *
      (O : Matrix (Fin d) (Fin d) ℝ).transpose
  let E := EuclideanSpace ℝ (Fin d)
  let f : E → ℝ := fun x => (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
  let query : E → E := fun x => WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
  have hgeometry := AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry hd hκ O
  have hcinfty : ContDiff ℝ ∞ f := hgeometry.1
  have hderivative (x : E) : HasFDerivAt (gradient f)
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) A) x := hgeometry.2.1 x
  have hscalar : Continuous f := hcinfty.continuous
  have hgradient : Continuous (gradient f) :=
    continuous_iff_continuousAt.mpr fun x => (hderivative x).continuousAt
  have hquery : query = gradient f := by
    funext x
    exact (AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder.actual_first_order_query hd hκ O x).1.gradient.symm
  change @Measurable E (ℝ × E) (borel E) (borel (ℝ × E)) (fun x => (f x, query x))
  rw [hquery]
  exact (hscalar.prodMk hgradient).borel_measurable

#check AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry
#print axioms AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry
#print axioms actual_first_order_oracle_measurable
