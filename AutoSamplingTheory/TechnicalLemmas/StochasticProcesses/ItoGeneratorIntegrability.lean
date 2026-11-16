import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ProgressiveL2
import AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates
import Mathlib.Analysis.Calculus.ContDiff.Comp
import Mathlib.MeasureTheory.Integral.Prod

namespace AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoGeneratorIntegrability

open Filter MeasureTheory Set
open scoped BigOperators NNReal
open ProgressiveL2
open AutoSamplingTheory.TechnicalLemmas.Analysis.EuclideanBilinearCoordinates

private theorem integrable_continuousOn_mul
    {T : ℝ≥0} {W g : ℝ≥0 → ℝ}
    (hW : ContinuousOn W (Icc 0 T)) (hg : Integrable g (TimeMeasure.upTo T)) :
    Integrable (fun t => W t * g t) (TimeMeasure.upTo T) := by
  let ν := TimeMeasure.upTo T
  have hMem : ∀ᵐ t ∂ν, t ∈ Icc 0 T :=
    (TimeMeasure.ae_mem_Ioc_zero_upTo T).mono fun _ ht => ⟨ht.1.le, ht.2⟩
  have hRest : ν.restrict (Icc 0 T) = ν := Measure.restrict_eq_self_of_ae_mem hMem
  have hm : AEStronglyMeasurable W ν := by
    rw [← hRest]
    exact hW.aestronglyMeasurable measurableSet_Icc
  obtain ⟨C, hC⟩ := isCompact_Icc.bddAbove_image hW.norm
  exact hg.bdd_mul hm (hMem.mono fun t ht => hC ⟨t, ht, rfl⟩)

/-- Almost every continuous state path has integrable first- and second-order
Itô generator terms when the drift rows are pathwise integrable and the
progressive diffusion entries are square integrable in time and sample. -/
theorem ae_integrable_euclidean_generator_terms
    {Ω I J : Type*} [MeasurableSpace Ω]
    [Fintype I] [DecidableEq I] [Fintype J]
    {filtration : Filtration ℝ≥0 (inferInstance : MeasurableSpace Ω)}
    {μ : Measure Ω} [IsFiniteMeasure μ] {T : ℝ≥0}
    (η : I → J → ProgressiveL2Integrand filtration μ T)
    (b : I → ℝ≥0 → Ω → ℝ)
    (hbi : ∀ i, ∀ᵐ ω ∂μ, Integrable (fun t => b i t ω) (TimeMeasure.upTo T))
    (X : ℝ≥0 → Ω → EuclideanSpace ℝ I)
    (hX : ∀ᵐ ω ∂μ, ContinuousOn (fun t => X t ω) (Icc 0 T))
    {K : Set (EuclideanSpace ℝ I)}
    (hRange : ∀ᵐ ω ∂μ, ∀ t ≤ T, X t ω ∈ K)
    (f : EuclideanSpace ℝ I → ℝ) (hf : ∀ w ∈ K, ContDiffAt ℝ 2 f w) :
    let v (t : ℝ≥0) (ω : Ω) := WithLp.toLp 2 (fun i : I => b i t ω)
    let σ (j : J) (t : ℝ≥0) (ω : Ω) :=
      WithLp.toLp 2 (fun i : I => (η i j).process t ω)
    ∀ᵐ ω ∂μ,
      Integrable (fun t => fderiv ℝ f (X t ω) (v t ω)) (TimeMeasure.upTo T) ∧
      Integrable (fun t => (1 / 2 : ℝ) * ∑ j : J,
        fderiv ℝ (fderiv ℝ f) (X t ω) (σ j t ω) (σ j t ω)) (TimeMeasure.upTo T) := by
  intro v σ
  have hProducts : ∀ᵐ ω ∂μ, ∀ i k : I, ∀ j : J,
      Integrable (fun t => (η i j).process t ω * (η k j).process t ω) (TimeMeasure.upTo T) :=
    ae_all_iff.2 fun i => ae_all_iff.2 fun k => ae_all_iff.2 fun j =>
      ((η i j).memLp.integrable_mul (η k j).memLp).prod_right_ae
  filter_upwards [ae_all_iff.2 hbi, hX, hRange, hProducts] with ω hDrift hPath hK hProduct
  let E := EuclideanSpace ℝ I
  let e := EuclideanSpace.basisFun I ℝ
  let D (t : ℝ≥0) := fderiv ℝ f (X t ω)
  let H (t : ℝ≥0) := fderiv ℝ (fderiv ℝ f) (X t ω)
  have hm : MapsTo (fun t => X t ω) (Icc 0 T) K := fun _ ht => hK _ ht.2
  have hD : ContinuousOn D (Icc 0 T) :=
    (show ContinuousOn (fderiv ℝ f) K from fun w hw =>
      ((hf w hw).continuousAt_fderiv (by decide)).continuousWithinAt).comp hPath hm
  have hH : ContinuousOn H (Icc 0 T) :=
    (show ContinuousOn (fderiv ℝ (fderiv ℝ f)) K from fun w hw =>
      (((hf w hw).fderiv_right (m := 1) (by decide)).continuousAt_fderiv
        (by decide)).continuousWithinAt).comp hPath hm
  constructor
  · have hi (i : I) : Integrable (fun t => D t (e i) * b i t ω) (TimeMeasure.upTo T) :=
      integrable_continuousOn_mul (hD.clm_apply continuousOn_const) (hDrift i)
    refine (integrable_finsetSum Finset.univ (fun i _ => hi i)).congr
      (Eventually.of_forall fun t => ?_)
    change (∑ i : I, D t (e i) * b i t ω) = D t (v t ω)
    have hrepr : (∑ i : I, b i t ω • e i) = v t ω := by
      simpa only [v, e, EuclideanSpace.basisFun_repr] using e.sum_repr (v t ω)
    rw [← hrepr, map_sum]
    simp only [map_smul, smul_eq_mul, mul_comm]
  · have hi (j : J) (i k : I) :
        Integrable (fun t => H t (e i) (e k) *
          ((η i j).process t ω * (η k j).process t ω)) (TimeMeasure.upTo T) :=
      integrable_continuousOn_mul
        ((hH.clm_apply continuousOn_const).clm_apply continuousOn_const) (hProduct i k j)
    have hj (j : J) : Integrable (fun t => H t (σ j t ω) (σ j t ω))
        (TimeMeasure.upTo T) := by
      refine (integrable_finsetSum Finset.univ (fun i _ =>
        integrable_finsetSum Finset.univ (fun k _ => hi j i k))).congr
        (Eventually.of_forall fun t => ?_)
      change (∑ i : I, ∑ k : I, H t (e i) (e k) *
        ((η i j).process t ω * (η k j).process t ω)) = H t (σ j t ω) (σ j t ω)
      rw [euclidean_bilinear_eq_sum_basis]
      simp only [e, σ, mul_comm]
    exact (integrable_finsetSum Finset.univ (fun j _ => hj j)).const_mul _

end AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.ItoGeneratorIntegrability
