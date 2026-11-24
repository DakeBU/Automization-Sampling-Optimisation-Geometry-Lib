import GCCRevelationLaw
import GC43FrameMeasurable
import GCCExposedRank
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

theorem axis_sq (u : S 1) : u.val.ofLp 0 ^ 2 = 1 := by
  have h := EuclideanSpace.real_norm_sq_eq u.val
  rw [mem_sphere_zero_iff_norm.mp u.property] at h
  simpa using h.symm

/-- In a one-dimensional residual space the image of a unit input determines
the whole residual matrix. Inverse and forward observations use the same sign. -/
def lastDecode (u z : S 1) : O 1 :=
  ⟨Matrix.of (fun _ _ => z.val.ofLp 0 * u.val.ofLp 0),by
    apply (Matrix.mem_orthogonalGroup_iff (Fin 1) ℝ).mpr
    ext i j
    have hi := Subsingleton.elim i (0 : Fin 1)
    have hj := Subsingleton.elim j (0 : Fin 1)
    subst i; subst j
    simp only [Matrix.mul_apply, Fintype.sum_unique, Matrix.transpose_apply,Matrix.of_apply,Matrix.one_apply_eq]
    nlinarith [axis_sq z,axis_sq u,sq_nonneg (z.val.ofLp 0 - u.val.ofLp 0),
      mul_self_eq_one_iff.mp (by simpa [pow_two] using axis_sq z)]
  ⟩

theorem measurable_lastDecode : Measurable (fun p : S 1 × S 1 => lastDecode p.1 p.2) := by
  have c : Continuous (fun z : S 1 => z.val.ofLp (0 : Fin 1)) :=
    (continuous_apply (0 : Fin 1)).comp ((PiLp.continuous_ofLp 2 _).comp continuous_subtype_val)
  exact ((continuous_matrix fun _ _ => (c.comp continuous_snd).mul (c.comp continuous_fst)).subtype_mk _).measurable

theorem lastDecode_reveal (b : Bool) (u : S 1) (W : O 1) :
    lastDecode u (rotate (if b then W⁻¹ else W) u) = W := by
  apply Subtype.ext
  ext i j
  have hi := Subsingleton.elim i (0 : Fin 1)
  have hj := Subsingleton.elim j (0 : Fin 1)
  subst i; subst j
  change (rotate (if b then W⁻¹ else W) u).val.ofLp 0 * u.val.ofLp 0 = W.val 0 0
  rw [rotate_val]
  have h0 (R : O 1) : (R.val *ᵥ u.val.ofLp) 0 = R.val 0 0 * u.val.ofLp 0 := by
    simp [Matrix.mulVec, dotProduct]
  rw [h0,mul_assoc,← sq,axis_sq,mul_one]
  cases b <;> rfl

theorem measurable_realize_family {H : Type*} [MeasurableSpace H] {N m : ℕ}
    {F : H → BlockFrame N m} {W : H → O m}
    (hD : Measurable fun h => (F h).domain) (hR : Measurable fun h => (F h).range)
    (hW : Measurable W) : Measurable (fun h => (F h).realize (W h)) := by
  apply measurable_frameFamily F (fun h f => f.realize (W h))
  intro r e; subst N
  exact (hR.mul ((continuous_prefixEmbed m r).measurable.comp hW)).mul hD.inv

def fullFrame {N : ℕ} (A : O N) : BlockFrame N 0 := ⟨N,Nat.zero_add _,1,A⟩

theorem fullFrame_realize {N : ℕ} (A : O N) : (fullFrame A).realize 1 = A := by
  change A * castOrthogonal (Nat.zero_add N) (prefixEmbed 0 N 1) * (1 : O N)⁻¹ = A
  rw [map_one]
  have h {m n : ℕ} (e : m=n) : castOrthogonal e 1 = 1 := by cases e; rfl
  simp [h]

theorem zero_law {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H] (μ : Measure Ω)
    [IsFiniteMeasure μ] {h : Ω → H} (hh : Measurable h) :
    LawGiven μ h (fun _ => (1 : O 0)) (orthogonalHaar 0) := by
  refine ⟨hh.prodMk measurable_const,?_⟩
  rw [orthogonalHaar_zero,Measure.prod_dirac,Measure.map_map measurable_prodMk_right hh]
  rfl

#print axioms lastDecode_reveal
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
