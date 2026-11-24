import Mathlib.Algebra.MvPolynomial.Equiv
import Mathlib.Topology.Algebra.MvPolynomial
import Mathlib.Algebra.Polynomial.Roots
import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Probability.ProductMeasure

/-! A nonzero polynomial evaluated on the scalar coordinates of independent standard
Gaussian starting vectors is nonzero almost surely (Lemma 4.7). -/

open MeasureTheory ProbabilityTheory
noncomputable section

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSaturation

/-- Fubini induction on the variables. A surviving coefficient guarantees that the
polynomial in the remaining scalar variable has only finitely many roots. -/
private theorem ae_eval_fin {n : ℕ} (μ : Measure ℝ) [IsProbabilityMeasure μ]
    [NullSingletonClass μ] (p : MvPolynomial (Fin n) ℝ) (hp : p ≠ 0) :
    ∀ᵐ x ∂Measure.pi (fun _ : Fin n => μ), MvPolynomial.eval x p ≠ 0 := by
  classical
  induction n with
  | zero =>
    let e := MvPolynomial.isEmptyRingEquiv ℝ (Fin 0)
    have h : e p ≠ 0 := by simpa only [ne_eq, EmbeddingLike.map_eq_zero_iff] using hp
    have he : MvPolynomial.C (e p) = p := by
      rw [← MvPolynomial.isEmptyRingEquiv_symm_apply]
      exact e.symm_apply_apply p
    exact .of_forall fun x => by rwa [← he, MvPolynomial.eval_C]
  | succ n ih =>
    let P := MvPolynomial.finSuccEquiv ℝ n p
    have hP : P ≠ 0 := by
      exact (EmbeddingLike.map_eq_zero_iff (f := MvPolynomial.finSuccEquiv ℝ n)).not.mpr hp
    have hc : P.coeff P.natDegree ≠ 0 := Polynomial.leadingCoeff_ne_zero.mpr hP
    let e := MeasurableEquiv.piFinSuccAbove (fun _ : Fin (n+1) => ℝ) 0
    let Q (y : (Fin n → ℝ) × ℝ) := MvPolynomial.eval (Fin.cons y.2 y.1) p
    have hm : Measurable Q := p.continuous_eval.measurable.comp
      (show Measurable (fun y : (Fin n → ℝ) × ℝ => Fin.cons (α := fun _ : Fin (n+1) => ℝ) y.2 y.1) by
        apply measurable_pi_lambda
        intro i
        cases i using Fin.cases with
        | zero => exact measurable_snd
        | succ i => exact (measurable_pi_apply i).comp measurable_fst)
    have hall : ∀ᵐ y ∂(Measure.pi (fun _ : Fin n => μ)).prod μ, Q y ≠ 0 := by
      apply (Measure.ae_prod_iff_ae_ae ((measurableSet_singleton (0 : ℝ)).compl.preimage hm)).2
      filter_upwards [ih (P.coeff P.natDegree) hc] with x hx
      let f := P.map (MvPolynomial.eval x)
      have hf : f ≠ 0 := by
        intro hf
        apply hx
        rw [← Polynomial.coeff_map, show P.map (MvPolynomial.eval x) = 0 from hf, Polynomial.coeff_zero]
      have hfinite := (Polynomial.finite_setOfPred_isRoot hf).measure_zero μ
      have ha : ∀ᵐ t ∂μ, f.eval t ≠ 0 := by
        simpa only [ae_iff, not_not, Polynomial.IsRoot] using hfinite
      filter_upwards [ha] with t ht
      change MvPolynomial.eval (Fin.cons t x) p ≠ 0
      rwa [MvPolynomial.eval_eq_eval_mv_eval']
    have hE := (Measure.measurePreserving_swap (μ := μ) (ν := Measure.pi (fun _ : Fin n => μ))).comp
      (measurePreserving_piFinSuccAbove (fun _ : Fin (n+1) => μ) (0 : Fin (n+1)))
    filter_upwards [hE.quasiMeasurePreserving.ae hall] with x hx
    change MvPolynomial.eval (Fin.cons (x 0) (Fin.tail x)) p ≠ 0 at hx
    rwa [Fin.cons_self_tail] at hx

/-- Atomless independent coordinates with a common law almost surely avoid the zero set
of a nonzero polynomial, including the case of an empty finite index. -/
theorem ae_eval_ne_zero_of_atomless {ι : Type*} [Fintype ι] (μ : Measure ℝ)
    [IsProbabilityMeasure μ] [NullSingletonClass μ] (p : MvPolynomial ι ℝ) (hp : p ≠ 0) :
    ∀ᵐ x ∂Measure.pi (fun _ : ι => μ), MvPolynomial.eval x p ≠ 0 := by
  classical
  let e := Fintype.equivFin ι
  let P := MvPolynomial.renameEquiv ℝ e p
  have hP : P ≠ 0 :=
    (EmbeddingLike.map_eq_zero_iff (f := MvPolynomial.renameEquiv ℝ e)).not.mpr hp
  have hE := measurePreserving_piCongrLeft (α := fun _ : Fin (Fintype.card ι) => ℝ)
    (fun _ => μ) e
  filter_upwards [hE.quasiMeasurePreserving.ae (ae_eval_fin μ P hP)] with x hx
  simp only [P, MvPolynomial.renameEquiv_apply, MvPolynomial.eval_rename] at hx
  have hcomp : ((MeasurableEquiv.piCongrLeft (fun _ : Fin (Fintype.card ι) => ℝ) e) x) ∘ e = x := by
    funext i
    exact MeasurableEquiv.piCongrLeft_apply_apply (β := fun _ => ℝ) e x i
  rwa [hcomp] at hx

theorem ae_mvPolynomial_ne_zero {ι : Type*} [Fintype ι] (p : MvPolynomial ι ℝ) (hp : p ≠ 0) :
    ∀ᵐ x ∂Measure.pi (fun _ : ι => gaussianReal 0 1), MvPolynomial.eval x p ≠ 0 := by
  let := nullSingletonClass_gaussianReal (μ := (0 : ℝ)) (v := 1) one_ne_zero
  exact ae_eval_ne_zero_of_atomless _ p hp

/-- Flatten Gaussian columns in the order (spatial coordinate, starting vector). -/
theorem flatten_gaussian_starts (d k : ℕ) :
    MeasurePreserving (fun (g : Fin k → EuclideanSpace ℝ (Fin d)) (ia : Fin d × Fin k) => g ia.2 ia.1)
      (Measure.pi (fun _ : Fin k => stdGaussian (EuclideanSpace ℝ (Fin d))))
      (Measure.pi (fun _ : Fin d × Fin k => gaussianReal 0 1)) := by
  let γ := gaussianReal 0 1
  let γd := Measure.pi (fun _ : Fin d => γ)
  have hcol : MeasurePreserving (WithLp.ofLp : EuclideanSpace ℝ (Fin d) → (Fin d → ℝ))
      (stdGaussian (EuclideanSpace ℝ (Fin d))) γd := by
    have hh : MeasurePreserving (MeasurableEquiv.toLp 2 (Fin d → ℝ)) γd
        (stdGaussian (EuclideanSpace ℝ (Fin d))) :=
      ⟨(MeasurableEquiv.toLp 2 (Fin d → ℝ)).measurable, map_pi_eq_stdGaussian⟩
    exact hh.symm
  have hcols := measurePreserving_pi (fun _ : Fin k => stdGaussian (EuclideanSpace ℝ (Fin d)))
    (fun _ : Fin k => γd) (fun _ => hcol)
  have hflat : MeasurePreserving (MeasurableEquiv.curry (Fin k) (Fin d) ℝ).symm
      (Measure.pi (fun _ : Fin k => γd)) (Measure.pi (fun _ : Fin k × Fin d => γ)) := by
    refine ⟨(MeasurableEquiv.curry (Fin k) (Fin d) ℝ).symm.measurable, ?_⟩
    simpa only [Measure.infinitePi_eq_pi] using
      Measure.infinitePi_map_curry_symm (fun (_ : Fin k) (_ : Fin d) => γ)
  exact (measurePreserving_piCongrLeft (α := fun _ : Fin d × Fin k => ℝ)
    (fun _ => γ) (Equiv.prodComm (Fin k) (Fin d))).comp (hflat.comp hcols)

theorem ae_eval_gaussian_starts {d k : ℕ} (p : MvPolynomial (Fin d × Fin k) ℝ) (hp : p ≠ 0) :
    ∀ᵐ g ∂Measure.pi (fun _ : Fin k => stdGaussian (EuclideanSpace ℝ (Fin d))),
      MvPolynomial.eval (fun ia => g ia.2 ia.1) p ≠ 0 :=
  (flatten_gaussian_starts d k).quasiMeasurePreserving.ae (ae_mvPolynomial_ne_zero p hp)

#print axioms ae_eval_gaussian_starts
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSaturation
