import GC41Risk
import Mathlib.Probability.Independence.Basic

/-! Extract the starts at inverse-query times and integrate fixed-seed bounds. -/
noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRotation
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

def evenIndex (q : ℕ) (i : Fin (q+1)) : Fin (2*q+1) := ⟨2*i.val, by have := i.isLt; omega⟩

theorem evenIndex_injective (q : ℕ) : Function.Injective (evenIndex q) := by
  intro i j h
  apply Fin.ext
  have := congrArg Fin.val h
  dsimp [evenIndex] at this
  omega

theorem select_product {X I J : Type*} [MeasurableSpace X] [Fintype I] [Fintype J]
    (ν : Measure X) [IsProbabilityMeasure ν] (u : J → I) (hu : Function.Injective u) :
    MeasurePreserving (fun (z : I → X) (j : J) => z (u j))
      (Measure.pi (fun _ : I => ν)) (Measure.pi (fun _ : J => ν)) := by
  have hi : iIndepFun (fun (i : I) (z : I → X) => z i) (Measure.pi (fun _ : I => ν)) :=
    iIndepFun_pi (X := fun _ => id) (fun _ => measurable_id.aemeasurable)
  have h := hi.precomp hu
  refine ⟨measurable_pi_lambda _ (fun j => measurable_pi_apply (u j)), ?_⟩
  rw [h.map_fun_eq_pi_map (fun j => (measurable_pi_apply (u j)).aemeasurable)]
  simp_rw [fun j => (measurePreserving_eval (fun _ : I => ν) (u j)).map_eq]

theorem even_starts_law (d q : ℕ) :
    MeasurePreserving (fun (z : Fin (2*q+1) → Space d) i => z (evenIndex q i))
      (Measure.pi (fun _ : Fin (2*q+1) => stdGaussian (Space d))) (gaussianStarts d q) :=
  select_product _ _ (evenIndex_injective q)

variable {d q : ℕ} {Seed State : Type*} [MeasurableSpace Seed] [MeasurableSpace State]

/-- The fixed-seed experiment keeps the true Haar orientation in its first component. -/
def fixedPair (κ : ℝ) (q : ℕ) (alg : Algorithm d Seed State) (s : Seed)
    (O : Matrix.orthogonalGroup (Fin d) ℝ) := experimentPair κ q alg (s,O)

theorem measurable_fixedPair (κ : ℝ) (q : ℕ) (alg : Algorithm d Seed State) (s : Seed) :
    Measurable (fixedPair κ q alg s) :=
  (measurable_experimentPair κ q alg).comp (measurable_prodMk_left (x := s))

theorem integrate_fixed_seed_bound (κ τ : ℝ) (ρ : Measure Seed) [IsProbabilityMeasure ρ]
    (alg : Algorithm d Seed State)
    (hf : ∀ s : Seed, ((orthogonalHaar d).map (fixedPair κ q alg s)).real
      (jointDetectorEvent d q κ τ) ≤ 1/100) :
    (experimentLaw κ q ρ alg).real (jointDetectorEvent d q κ τ) ≤ 1/100 := by
  let H := jointDetectorEvent d q κ τ
  let U := orthogonalHaar d
  let F := experimentPair κ q alg
  have hH : MeasurableSet H := measurableSet_jointDetectorEvent ..
  have hF : Measurable F := measurable_experimentPair ..
  let : IsProbabilityMeasure U := (orthogonalHaar_spec d).1
  have hB : ((ρ.prod U).map F) H ≤ ENNReal.ofReal (1/100 : ℝ) := by
    rw [Measure.map_apply hF hH, Measure.prod_apply (hF hH)]
    calc
      _ ≤ ∫⁻ _ : Seed, ENNReal.ofReal (1/100 : ℝ) ∂ρ := by
        apply lintegral_mono
        intro s
        have hm := measurable_fixedPair κ q alg s
        let : IsProbabilityMeasure (U.map (fixedPair κ q alg s)) := Measure.isProbabilityMeasure_map hm.aemeasurable
        have h := (ENNReal.le_ofReal_iff_toReal_le (measure_ne_top (U.map (fixedPair κ q alg s)) H)
          (by norm_num : (0:ℝ) ≤ 1/100)).mpr (hf s)
        rw [Measure.map_apply hm hH] at h
        exact h
      _ = _ := by simp
  exact (ENNReal.toReal_mono (by simp) hB).trans (by rw [ENNReal.toReal_ofReal (by norm_num)])

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
