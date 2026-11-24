import GC3PublicFrames
import B3TaggedUpdate

/-! Conditional product Haar in public ambient frames. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
set_option maxHeartbeats 800000
open MeasureTheory ProbabilityTheory Matrix
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
variable {N k m : ℕ}
abbrev Frames (k N : ℕ) := Fin k → PublicFrame N
abbrev Ambient (k N : ℕ) := Fin k → O N

def profile (F : Frames k N) : Fin k → ℕ := fun j => (F j).1

theorem measurable_profile : Measurable (@profile N k) :=
  measurable_pi_lambda _ fun j => PublicFrame.measurable_profile.comp (measurable_pi_apply j)

def readFrame (F : PublicFrame N) (m : ℕ) (w : O m) : O N :=
  if h : m ≤ N then (⟨N-m,by omega,F.2.domain,F.2.range⟩ : BlockFrame N m).realize w else 1

theorem readFrame_tag (F : BlockFrame N m) (w : O m) :
    readFrame ⟨m,F⟩ m w = F.realize w := by
  rcases F with ⟨r,e,D,R⟩
  subst N
  simp [readFrame]

private theorem castMeas {a b : ℕ} (e : a=b) : Measurable (castOrthogonal e) := by
  subst b; exact measurable_id

theorem measurable_readFrame (m : ℕ) :
    Measurable (fun p : PublicFrame N × O m => readFrame p.1 m p.2) := by
  by_cases hm : m ≤ N
  · let r := N-m
    have e : m+r=N := by dsimp [r]; omega
    have hc := castMeas e
    have hh := (PublicFrame.measurable_range.comp (measurable_fst (β := O m))).mul
      (hc.comp ((continuous_prefixEmbed m r).measurable.comp measurable_snd))
    simp only [readFrame, dif_pos hm, BlockFrame.realize]
    exact hh.mul (PublicFrame.measurable_domain.comp measurable_fst).inv
  · simp only [readFrame,dif_neg hm]; exact measurable_const

def decodeAt (d : Fin k → ℕ) (F : Frames k N) (w : ResidualTuple d) : Ambient k N :=
  fun j => readFrame (F j) (d j) (w j)

theorem measurable_decodeAt (d : Fin k → ℕ) :
    Measurable (Function.uncurry (decodeAt (N := N) d)) := by
  let Z := Frames k N × ResidualTuple d
  let f (p : Z) (j : Fin k) := readFrame (p.1 j) (d j) (p.2 j)
  change Measurable f
  apply measurable_pi_lambda f
  intro j
  have h1 : Measurable (fun F : Frames k N => F j) :=
    @measurable_pi_apply (Fin k) (fun _ => PublicFrame N) _ j
  have h2 : Measurable (fun w : ResidualTuple d => w j) :=
    @measurable_pi_apply (Fin k) (fun l => O (d l)) _ j
  have hF : Measurable (fun p : Z => p.1 j) := h1.comp measurable_fst
  have hW : Measurable (fun p : Z => p.2 j) := h2.comp measurable_snd
  let project (p : Z) : PublicFrame N × O (d j) := (p.1 j,p.2 j)
  have hpr : Measurable project := hF.prodMk hW
  let dec (u : PublicFrame N × O (d j)) : O N := readFrame u.1 (d j) u.2
  have hd : Measurable dec := measurable_readFrame _
  change Measurable (dec ∘ project)
  exact hd.comp hpr

theorem decodeAt_match (F : Frames k N) (w : ResidualTuple (profile F)) (j : Fin k) :
    decodeAt (profile F) F w j = (F j).2.realize (w j) :=
  readFrame_tag (F j).2 (w j)

theorem tupleProb {d : Fin k → ℕ} (hd : ∀ j, 0 < d j) {b : ℝ} (hb : b = -1 ∨ b = 1) :
    IsProbabilityMeasure (tupleHaar d b) := by
  let : ∀ j, IsProbabilityMeasure (componentHaar (d j) b) := fun j =>
    isProbabilityMeasure_componentHaar (hd j) hb
  unfold tupleHaar; infer_instance

def fixedKernel (d : Fin k → ℕ) (b : ℝ) : Kernel (Frames k N) (Ambient k N) :=
  if ∀ j, 0 < d j then kernel (tupleHaar d b) (decodeAt d) else Kernel.const _ (Measure.dirac 1)

def ambientKernel (b : ℝ) : Kernel (Frames k N) (Ambient k N) :=
  selectHistoryKernel profile measurable_profile (fun d => fixedKernel d b)

theorem ambientKernel_apply (F : Frames k N) (hd : ∀ j, 0 < (F j).1) {b : ℝ}
    (hb : b = -1 ∨ b = 1) :
    ambientKernel b F = (tupleHaar (profile F) b).map (decodeAt (profile F) F) := by
  change ∀ j, 0 < profile F j at hd
  let := tupleProb hd hb
  change fixedKernel (profile F) b F = _
  rw [fixedKernel, if_pos hd, kernel_apply _ _ (measurable_decodeAt _) F]

theorem markov_ambientKernel {b : ℝ} (hb : b = -1 ∨ b = 1) :
    IsMarkovKernel (ambientKernel (N := N) (k := k) b) := by
  apply markov_selectHistoryKernel
  intro d
  by_cases h : ∀ j, 0 < d j
  · rw [fixedKernel, if_pos h]
    let := tupleProb h hb
    exact isMarkovKernel_kernel _ _ (measurable_decodeAt _)
  · rw [fixedKernel, if_neg h]; infer_instance

end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
