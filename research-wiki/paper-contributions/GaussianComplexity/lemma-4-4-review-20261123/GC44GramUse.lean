import GC41Target
import AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylovRange
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.MeasureTheory.Measure.ProbabilityMeasure

/-! # From the two Gram bounds to the signed detector on every Krylov vector -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open scoped Matrix.Norms.L2Operator RealInnerProductSpace
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

abbrev Space (d : ℕ) := EuclideanSpace ℝ (Fin d)
abbrev Starts (d q : ℕ) := Fin (q+1) → Space d
abbrev Indices (q : ℕ) := Fin (q+1) × Fin (q+1)

def feature (d q : ℕ) (g : Starts d q) : Matrix (Fin d) (Indices q) ℝ := fun i a =>
  (Real.sqrt (d : ℝ))⁻¹ * g a.1 i *
    (if a.2.val = 0 then 1 else Real.sqrt 2 * Real.cos ((a.2.val : ℝ) * gridAngle d i))

def cosineDiag (d q : ℕ) : Matrix (Fin d) (Fin d) ℝ :=
  Matrix.diagonal (fun i => Real.cos (((2*q+1 : ℕ) : ℝ) * gridAngle d i))

def krylov (d q : ℕ) (κ : ℝ) (g : Starts d q) : Submodule ℝ (Fin d → ℝ) :=
  Submodule.span ℝ (Set.range (fun a : Indices q =>
    (diagonalPrecision d κ ^ a.2.val).mulVec (WithLp.ofLp (g a.1))))

def gramGood (d q : ℕ) (τ : ℝ) : Set (Starts d q) := {g |
  let B := feature d q g
  ‖B.transpose * B - 1‖ ≤ τ ∧ ‖B.transpose * cosineDiag d q * B‖ ≤ τ}

theorem measurableSet_gramGood (d q : ℕ) (τ : ℝ) : MeasurableSet (gramGood d q τ) := by
  have hc : Continuous (feature d q) := by
    refine continuous_matrix (fun i j => ?_)
    exact ((continuous_const.mul ((EuclideanSpace.proj i).continuous.comp
      (continuous_apply j.1))).mul continuous_const)
  exact (measurableSet_le ((hc.matrix_transpose.matrix_mul hc).sub continuous_const).norm.measurable
    measurable_const).inter (measurableSet_le (((hc.matrix_transpose.matrix_mul continuous_const).matrix_mul hc).norm.measurable)
    measurable_const)

theorem range_feature {d q : ℕ} {κ : ℝ} (hκ : 2 ≤ κ) (hq : 2*q+1 < d) (g : Starts d q) :
    Set.range (fun c => (feature d q g).mulVec c) = (krylov d q κ g : Set (Fin d → ℝ)) :=
  FixedSpectrumKrylovRange.actual_cosine_feature_krylov_range κ hκ hq
    (WithLp.toLp 2 (fun i : Fin d × Fin (q+1) => g i.2 i.1))

theorem dot_self {ι : Type*} [Fintype ι] (c : ι → ℝ) :
    c ⬝ᵥ c = ‖WithLp.toLp 2 c‖^2 := by
  rw [EuclideanSpace.real_norm_sq_eq]
  simp [dotProduct, pow_two]

theorem quadratic_op_bound {ι : Type*} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℝ) (c : ι → ℝ) : |c ⬝ᵥ (A *ᵥ c)| ≤ ‖A‖ * ‖WithLp.toLp 2 c‖^2 := by
  let v : EuclideanSpace ℝ ι := WithLp.toLp 2 c
  have hin : ⟪WithLp.toLp 2 (A *ᵥ c), v⟫ = c ⬝ᵥ (A *ᵥ c) := by
    simp [v, EuclideanSpace.inner_toLp_toLp]
  rw [← hin]
  calc
    _ ≤ ‖WithLp.toLp 2 (A *ᵥ c)‖ * ‖v‖ := abs_real_inner_le_norm _ _
    _ ≤ (‖A‖ * ‖v‖) * ‖v‖ := mul_le_mul_of_nonneg_right (A.l2_opNorm_mulVec v) (norm_nonneg _)
    _ = _ := by dsimp [v]; ring

/-- On the joint Gram event the cosine statistic is controlled for the whole
Krylov space, permitting coefficients selected after observing all starts. -/
theorem bound_on_krylov {d q : ℕ} {κ τ : ℝ} (hκ : 2 ≤ κ) (hq : 2*q+1 < d)
    (hτ : τ ≤ 1/2) {g : Starts d q} (hg : g ∈ gramGood d q τ)
    {u : Fin d → ℝ} (hu : u ∈ krylov d q κ g) :
    |u ⬝ᵥ (cosineDiag d q *ᵥ u)| ≤ 2*τ*‖WithLp.toLp 2 u‖^2 := by
  let B := feature d q g
  let D := cosineDiag d q
  obtain ⟨hG,hW⟩ := hg
  have h0 : 0 ≤ τ := (norm_nonneg _).trans hG
  have hmem : u ∈ Set.range (fun c => B.mulVec c) := (range_feature hκ hq g) ▸ hu
  obtain ⟨c,rfl⟩ := hmem
  have hWform : c ⬝ᵥ ((B.transpose * D * B) *ᵥ c) = B.mulVec c ⬝ᵥ (D *ᵥ B.mulVec c) := by
    rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, Matrix.dotProduct_transpose_mulVec, dotProduct_comm]
  have hGform : c ⬝ᵥ ((B.transpose * B - 1) *ᵥ c) = ‖WithLp.toLp 2 (B *ᵥ c)‖^2 - ‖WithLp.toLp 2 c‖^2 := by
    rw [Matrix.sub_mulVec, Matrix.one_mulVec, dotProduct_sub, ← Matrix.mulVec_mulVec,
      Matrix.dotProduct_transpose_mulVec, dot_self, dot_self]
  have h₁ := (quadratic_op_bound (B.transpose * B - 1) c).trans
    (mul_le_mul_of_nonneg_right hG (sq_nonneg _))
  rw [hGform] at h₁
  have hc : ‖WithLp.toLp 2 c‖^2 ≤ 2*‖WithLp.toLp 2 (B *ᵥ c)‖^2 := by
    have h := (abs_le.mp h₁).1
    nlinarith [mul_nonneg (sub_nonneg.mpr hτ) (sq_nonneg ‖WithLp.toLp 2 c‖)]
  have h₂ := (quadratic_op_bound (B.transpose * D * B) c).trans
    (mul_le_mul_of_nonneg_right hW (sq_nonneg _))
  rw [hWform] at h₂
  linarith [mul_le_mul_of_nonneg_left hc h0]

/-- Strict detector event on the joint orientation and output. -/
def jointDetectorEvent (d q : ℕ) (κ τ : ℝ) : Set (Matrix.orthogonalGroup (Fin d) ℝ × Space d) :=
  {p | p.2 ∈ detectorEvent κ (2*q+1) τ (hiddenPrecision κ p.1)}

theorem measurableSet_jointDetectorEvent (d q : ℕ) (κ τ : ℝ) :
    MeasurableSet (jointDetectorEvent d q κ τ) := by
  have hp : Continuous (fun O : Matrix.orthogonalGroup (Fin d) ℝ => hiddenPrecision κ O) := by
    unfold hiddenPrecision
    exact (continuous_subtype_val.matrix_mul continuous_const).matrix_mul
      continuous_subtype_val.matrix_transpose
  exact measurableSet_lt measurable_const
    ((continuous_detectorStatistic κ (2*q+1) τ).comp ((hp.comp continuous_fst).prodMk continuous_snd)).measurable

/-- The positive source detector is incompatible with the uniform Gram bounds
whenever the hidden coordinates of the actual output belong to the Krylov space. -/
theorem not_pass_on_gramGood {d q : ℕ} {κ τ : ℝ} (hκ : 2 ≤ κ) (hq : 2*q+1 < d)
    (hτ : τ ≤ 1/2) {g : Starts d q} (hg : g ∈ gramGood d q τ)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) (x : Space d)
    (hu : O.val.transpose *ᵥ WithLp.ofLp x ∈ krylov d q κ g) :
    (O,x) ∉ jointDetectorEvent d q κ τ := by
  let u := O.val.transpose *ᵥ WithLp.ofLp x
  have h := bound_on_krylov hκ hq hτ hg hu
  have hnorm : ‖WithLp.toLp 2 u‖^2 = ‖x‖^2 := by
    calc
      _ = u ⬝ᵥ u := (dot_self _).symm
      _ = WithLp.ofLp x ⬝ᵥ (O.val *ᵥ u) := Matrix.dotProduct_transpose_mulVec O.val u (WithLp.ofLp x)
      _ = _ := by rw [show O.val *ᵥ u = WithLp.ofLp x by
              dsimp [u]; rw [Matrix.mulVec_mulVec, (Matrix.mem_orthogonalGroup_iff _ _).mp O.property,
                Matrix.one_mulVec]]; exact dot_self _
  have hdiag : u ⬝ᵥ (cosineDiag d q *ᵥ u) =
      ∑ i : Fin d, Real.cos (((2*q+1 : ℕ) : ℝ) * gridAngle d i) * (u i)^2 := by
    simp only [cosineDiag, dotProduct, Matrix.mulVec_diagonal]
    apply Finset.sum_congr rfl
    intro i _
    ring
  change |u ⬝ᵥ (cosineDiag d q *ᵥ u)| ≤ 2*τ*‖WithLp.toLp 2 u‖^2 at h
  rw [hnorm,hdiag] at h
  intro hx
  have hh := (mem_detectorEvent_hiddenPrecision_iff (by omega) hκ O (2*q+1) τ x).mp hx
  have hz (z : ℝ) : (-1 : ℝ)^(2*q+1) * z ≤ |z| := by
    simpa only [abs_mul, abs_pow, abs_neg, abs_one, one_pow, one_mul] using
      (le_abs_self ((-1 : ℝ)^(2*q+1) * z))
  linarith only [hh, (hz _).trans h]

def gaussianStarts (d q : ℕ) : Measure (Starts d q) :=
  Measure.pi (fun _ => stdGaussian (Space d))

/-- Transfer the joint Gaussian-start estimate through any extension which
preserves the actual joint law of the orientation and the returned point. -/
theorem detector_rare_of_krylov_coupling {d q : ℕ} {κ τ : ℝ}
    (hκ : 2 ≤ κ) (hq : 2*q+1 < d) (hτ : τ ≤ 1/2)
    (hgood : 99/100 ≤ (gaussianStarts d q).real (gramGood d q τ))
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (law : Measure (Matrix.orthogonalGroup (Fin d) ℝ × Space d))
    (pair : Ω → Matrix.orthogonalGroup (Fin d) ℝ × Space d) (starts : Ω → Starts d q)
    (hp : MeasurePreserving pair μ law) (hs : MeasurePreserving starts μ (gaussianStarts d q))
    (hmem : ∀ᵐ ω ∂μ, (pair ω).1.val.transpose *ᵥ WithLp.ofLp (pair ω).2 ∈ krylov d q κ (starts ω)) :
    law.real (jointDetectorEvent d q κ τ) ≤ 1/100 := by
  let E := jointDetectorEvent d q κ τ
  let G := gramGood d q τ
  have hG := measurableSet_gramGood d q τ
  have hpre : pair ⁻¹' E ≤ᵐ[μ] starts ⁻¹' Gᶜ := by
    filter_upwards [hmem] with ω hm hE hW
    exact not_pass_on_gramGood hκ hq hτ hW (pair ω).1 (pair ω).2 hm hE
  have hle : μ.real (pair ⁻¹' E) ≤ μ.real (starts ⁻¹' Gᶜ) :=
    ENNReal.toReal_mono (measure_ne_top μ _) (measure_mono_ae hpre)
  have hμ : IsProbabilityMeasure (gaussianStarts d q) := by unfold gaussianStarts; infer_instance
  rw [hp.measureReal_preimage (measurableSet_jointDetectorEvent d q κ τ).nullMeasurableSet,
    hs.measureReal_preimage hG.compl.nullMeasurableSet, probReal_compl_eq_one_sub hG] at hle
  linarith

#print axioms bound_on_krylov
#print axioms detector_rare_of_krylov_coupling

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
