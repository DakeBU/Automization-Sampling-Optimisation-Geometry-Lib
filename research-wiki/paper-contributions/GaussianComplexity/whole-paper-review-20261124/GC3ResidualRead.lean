import GC3Unframe
import GC3AmbientKernel

/-! Recover the residual matrices on the original probability space and
transfer the full conditional product law to their tagged coordinates. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
set_option maxHeartbeats 1000000
open MeasureTheory ProbabilityTheory Matrix
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
variable {N k : ℕ}

def extractAt (d : Fin k → ℕ) (F : Frames k N) (A : Ambient k N) : ResidualTuple d :=
  fun j => readResidualAt (d j) (F j) (A j)

theorem measurable_extractAt (d : Fin k → ℕ) :
    Measurable (Function.uncurry (extractAt (N := N) d)) := by
  let Z := Frames k N × Ambient k N
  let f (p : Z) (j : Fin k) := readResidualAt (d j) (p.1 j) (p.2 j)
  change Measurable f
  apply measurable_pi_lambda f
  intro j
  have h1 : Measurable (fun F : Frames k N => F j) :=
    @measurable_pi_apply (Fin k) (fun _ => PublicFrame N) _ j
  have h2 : Measurable (fun W : Ambient k N => W j) :=
    @measurable_pi_apply (Fin k) (fun _ => O N) _ j
  let project (p : Z) : PublicFrame N × O N := (p.1 j,p.2 j)
  have hF : Measurable (fun p : Z => p.1 j) := h1.comp measurable_fst
  have hW : Measurable (fun p : Z => p.2 j) := h2.comp measurable_snd
  have hm : Measurable project := hF.prodMk hW
  let dec (p : PublicFrame N × O N) : O (d j) := readResidualAt (d j) p.1 p.2
  have hd : Measurable dec := measurable_readResidualAt (N := N) (d j)
  change Measurable (dec ∘ project)
  exact hd.comp hm

theorem extractAt_decode (F : Frames k N) (w : ResidualTuple (profile F)) :
    extractAt (profile F) F (decodeAt (profile F) F w) = w := by
  funext j
  change readResidualAt ((F j).1) (F j) (decodeAt _ F w j) = w j
  rw [decodeAt_match]
  exact readResidualAt_realize (F j).2 (w j)

def residualRead (F : Frames k N) (A : Ambient k N) : TaggedTuple k :=
  ⟨profile F, extractAt (profile F) F A⟩

private theorem measurable_tagTuple (d : Fin k → ℕ) : Measurable (Sigma.mk (β := ResidualTuple) d) := by
  intro s hs
  exact MeasurableSpace.measurableSet_iInf.mp hs d

theorem measurable_residualRead : Measurable (Function.uncurry (@residualRead N k)) := by
  let Z := Frames k N × Ambient k N
  have hm : Measurable (fun p : (Fin k → ℕ) × Z =>
      (⟨p.1, extractAt p.1 p.2.1 p.2.2⟩ : TaggedTuple k)) :=
    measurable_from_prod_countable_right (fun d => (measurable_tagTuple d).comp (measurable_extractAt d))
  exact hm.comp ((measurable_profile.comp measurable_fst).prodMk measurable_id)

def reconstructed (F : Frames k N) (A : Ambient k N) : Ambient k N :=
  decodeAt (profile F) F (extractAt (profile F) F A)

theorem measurable_reconstructed : Measurable (Function.uncurry (@reconstructed N k)) := by
  let Z := Frames k N × Ambient k N
  have hm : Measurable (fun p : (Fin k → ℕ) × Z =>
      decodeAt p.1 p.2.1 (extractAt p.1 p.2.1 p.2.2)) :=
    measurable_from_prod_countable_right (fun d => by
      let pair (p : Z) : Frames k N × ResidualTuple d := (p.1,extractAt d p.1 p.2)
      have hpair : Measurable pair :=
        (measurable_fst : Measurable (Prod.fst : Z → Frames k N)).prodMk (measurable_extractAt d)
      let dec (t : Frames k N × ResidualTuple d) := decodeAt d t.1 t.2
      have hd : Measurable dec := measurable_decodeAt d
      change Measurable (dec ∘ pair)
      exact hd.comp hpair)
  exact hm.comp ((measurable_profile.comp measurable_fst).prodMk measurable_id)

theorem reconstructed_ae (F : Frames k N) (hd : ∀ j, 0 < (F j).1) {b : ℝ}
    (hb : b = -1 ∨ b = 1) :
    ∀ᵐ A ∂ambientKernel b F, reconstructed F A = A := by
  rw [ambientKernel_apply F hd hb]
  apply (ae_map_iff (measurable_decodeAt _ |>.of_uncurry_left.aemeasurable)
    (measurableSet_eq_fun measurable_reconstructed.of_uncurry_left measurable_id)).mpr
  exact Filter.Eventually.of_forall (fun w => by simp [reconstructed,extractAt_decode])

def residualKernel (b : ℝ) : Kernel (Frames k N) (TaggedTuple k) :=
  selectHistoryKernel profile measurable_profile (fun d =>
    if ∀ j, 0 < d j then Kernel.const _ (taggedHaar d b) else
      Kernel.const _ (Measure.dirac (⟨fun _ => 0,fun _ => 1⟩ : TaggedTuple k)))

theorem residualKernel_apply (F : Frames k N) (hd : ∀ j, 0 < (F j).1) (b : ℝ) :
    residualKernel b F = taggedHaar (profile F) b := by
  change ∀ j, 0 < profile F j at hd
  simp [residualKernel,selectHistoryKernel, hd]

theorem markov_residualKernel {b : ℝ} (hb : b = -1 ∨ b = 1) :
    IsMarkovKernel (residualKernel (N := N) (k := k) b) := by
  apply markov_selectHistoryKernel
  intro d
  by_cases h : ∀ j, 0 < d j
  · rw [if_pos h]
    let := probability_taggedHaar h hb
    infer_instance
  · rw [if_neg h]; infer_instance

theorem read_ambient_kernel (F : Frames k N) (hd : ∀ j, 0 < (F j).1) {b : ℝ}
    (hb : b = -1 ∨ b = 1) :
    (ambientKernel b F).map (residualRead F) = residualKernel b F := by
  rw [ambientKernel_apply F hd hb, Measure.map_map measurable_residualRead.of_uncurry_left
    (measurable_decodeAt _).of_uncurry_left, residualKernel_apply F hd, taggedHaar]
  congr 1
  funext w
  simp [Function.comp_apply,residualRead,extractAt_decode]

variable {H : Type*} [MeasurableSpace H]

theorem residual_joint_of_ambient (μ : Measure (Ambient k N)) [IsProbabilityMeasure μ]
    (trace : Ambient k N → H) (ht : Measurable trace) (F : H → Frames k N) (hF : Measurable F)
    (hp : ∀ h j, 0 < (F h j).1) (b : ℝ) (hb : b = -1 ∨ b = 1)
    (hj : μ.map (fun W => (trace W,W)) = (μ.map trace) ⊗ₘ (ambientKernel b).comap F hF) :
    μ.map (fun W => (trace W, residualRead (F (trace W)) W)) =
        (μ.map trace) ⊗ₘ (residualKernel b).comap F hF ∧
      ∀ᵐ W ∂μ, reconstructed (F (trace W)) W = W := by
  let := markov_ambientKernel (N := N) (k := k) hb
  let := markov_residualKernel (N := N) (k := k) hb
  let := Measure.isProbabilityMeasure_map (μ := μ) ht.aemeasurable
  let op (p : H × Ambient k N) := (p.1, residualRead (F p.1) p.2)
  have hm : Measurable op := measurable_fst.prodMk
    (measurable_residualRead.comp ((hF.comp measurable_fst).prodMk measurable_snd))
  have ht' : Measurable (fun W => (trace W,W)) := ht.prodMk measurable_id
  constructor
  · change μ.map (op ∘ (fun W => (trace W,W))) = _
    rw [← Measure.map_map hm ht',hj]
    ext s hs
    rw [Measure.map_apply hm hs,Measure.compProd_apply (hm hs),Measure.compProd_apply hs]
    apply lintegral_congr
    intro h
    simp only [Kernel.comap_apply]
    have hslice := measurable_prodMk_left (x := h) hs
    rw [← read_ambient_kernel (F h) (hp h) hb,
      Measure.map_apply measurable_residualRead.of_uncurry_left hslice]
    rfl
  · let P (p : H × Ambient k N) := reconstructed (F p.1) p.2 = p.2
    have hP : MeasurableSet {p | P p} := measurableSet_eq_fun
      (measurable_reconstructed.comp ((hF.comp measurable_fst).prodMk measurable_snd)) measurable_snd
    apply (ae_map_iff ht'.aemeasurable hP).mp
    rw [hj,Measure.ae_compProd_iff hP]
    exact Filter.Eventually.of_forall (fun h => reconstructed_ae (F h) (hp h) hb)

#print axioms residual_joint_of_ambient
end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
