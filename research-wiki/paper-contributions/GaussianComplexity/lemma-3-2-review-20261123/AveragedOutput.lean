import Mathlib.MeasureTheory.Measure.Prod

/-!
# Averaging an algorithm's output law over an input prior

Equation (7) of Zhou–Suzuki, Lemma 3.2, averages the distribution of the
randomized algorithm on each input matrix. The same measure is obtained
by sampling the random seed and the hidden input independently.
-/

open MeasureTheory

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

variable {S V A X : Type*} [MeasurableSpace S] [MeasurableSpace V]
  [MeasurableSpace A] [MeasurableSpace X]

/-- The output distribution at fixed input is a measurable function of that input. -/
theorem measurable_seed_output_law (ρ : Measure S) [SFinite ρ] (eval : S × A → X)
    (heval : Measurable eval) : Measurable (fun a : A => ρ.map (fun s => eval (s,a))) := by
  apply Measure.measurable_of_measurable_coe
  intro B hB
  have hs (a : A) : Measurable (fun s : S => eval (s,a)) := heval.comp measurable_prodMk_right
  simp_rw [Measure.map_apply (hs _) hB]
  exact measurable_measure_prodMk_right (heval hB)

/-- Push the latent prior through the input construction, then average the
algorithm's fixed-input output distribution. This equals the output law on
the product of the seed measure and the original latent prior. -/
theorem averaged_output_eq_seeded_pushforward (ρ : Measure S) (μ : Measure V)
    [SFinite ρ] [SFinite μ] (make : V → A) (hmake : Measurable make)
    (eval : S × A → X) (heval : Measurable eval) :
    (μ.map make).bind (fun a => ρ.map (fun s => eval (s,a))) =
      (ρ.prod μ).map (fun p => eval (p.1,make p.2)) := by
  have hk := measurable_seed_output_law ρ eval heval
  have hout : Measurable (fun p : S × V => eval (p.1,make p.2)) :=
    heval.comp (measurable_fst.prodMk (hmake.comp measurable_snd))
  ext B hB
  have hev : Measurable (fun a => ρ.map (fun s => eval (s,a)) B) :=
    (Measure.measurable_coe hB).comp hk
  rw [Measure.bind_apply hB hk.aemeasurable, Measure.map_apply hout hB,
    Measure.prod_apply_symm (hout hB), lintegral_map hev hmake]
  apply lintegral_congr
  intro v
  exact Measure.map_apply (heval.comp (measurable_prodMk_right (y := make v))) hB

#print axioms averaged_output_eq_seeded_pushforward

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
