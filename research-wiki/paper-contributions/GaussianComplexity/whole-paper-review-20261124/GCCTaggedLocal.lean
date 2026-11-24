import GCCTaggedState
open MeasureTheory ProbabilityTheory
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
open AutoSamplingTheory.TechnicalLemmas.Probability.ParameterizedPushforward
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
noncomputable section
set_option maxHeartbeats 800000
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation

variable {Ω H : Type*} [MeasurableSpace Ω] [MeasurableSpace H]
  {N m : ℕ} {μ : Measure Ω} [IsFiniteMeasure μ] {h : Ω → H} {A : Ω → O N}

def atRank (m : ℕ) (hm : m ≤ N) (F : PublicFrame N) : BlockFrame N m :=
  ⟨N-m, by omega, F.2.domain, F.2.range⟩

theorem tag_atRank {F : PublicFrame N} (hm : m ≤ N) (he : F.1 = m) :
    (⟨m,atRank m hm F⟩ : PublicFrame N) = F := by
  rcases F with ⟨m',r,e,D,R⟩
  change m' = m at he; subst m'
  have hr : N-m = r := by omega
  simp [atRank,hr]

theorem measurable_atRank {F : H → PublicFrame N} (hF : Measurable F) (hm : m ≤ N) :
    Measurable (fun a => atRank m hm (F a)) :=
  PublicFrame.measurable_blockFrame (PublicFrame.measurable_domain.comp hF)
    (PublicFrame.measurable_range.comp hF)

theorem TaggedState.fixed {F : H → BlockFrame N m}
    (st : TaggedState μ h A (fun a => ⟨m,F a⟩)) :
    HaarState μ h A F (fun ω => readResidualAt m ⟨m,F (h ω)⟩ (A ω)) := by
  let := (orthogonalHaar_spec m).1
  let G := fun a => (⟨m,F a⟩ : PublicFrame N)
  let f := fun a => (F a).realize
  let make := fun p : H × O m => (p.1, f p.1 p.2)
  let read := fun p : H × O N => readResidualAt m (G p.1) p.2
  let pair := fun ω => (h ω,A ω)
  have hd : Measurable (fun a => (F a).domain) := PublicFrame.measurable_domain.comp st.frame
  have hr : Measurable (fun a => (F a).range) := PublicFrame.measurable_range.comp st.frame
  have hf : Measurable (fun p : H × O m => f p.1 p.2) :=
    measurable_realize_family (hd.comp measurable_fst) (hr.comp measurable_fst) measurable_snd
  have hmake : Measurable make := measurable_fst.prodMk hf
  have args : Measurable (fun p : H × O N => (G p.1,p.2)) := (st.frame.comp measurable_fst).prodMk measurable_snd
  have hread : Measurable read := by
    change Measurable (Function.uncurry (@readResidualAt N m) ∘ (fun p : H × O N => (G p.1,p.2)))
    exact (measurable_readResidualAt m).comp args
  have hp : Measurable pair := st.history.prodMk st.ambient
  let := isMarkovKernel_kernel (orthogonalHaar m) f hf
  have law : condDistrib A h μ =ᵐ[μ.map h] kernel (orthogonalHaar m) f := by
    filter_upwards [st.law] with a ha
    exact ha.trans (kernel_apply _ _ hf a).symm
  have joint : μ.map pair = ((μ.map h).prod (orthogonalHaar m)).map make :=
    ((condDistrib_ae_eq_iff_measure_eq_compProd h st.ambient.aemeasurable _).mp law).trans
      (map_prod_eq_compProd _ _ _ hf).symm
  have inv (a : H) (w : O m) : read (a, f a w) = w := readResidualAt_realize (F a) w
  refine ⟨hd,hr,st.ambient,?_,?_⟩
  · have hm : Measurable (fun p : H × O N => (p.1,read p)) := measurable_fst.prodMk hread
    refine ⟨hm.comp hp,?_⟩
    change μ.map ((fun p : H × O N => (p.1,read p)) ∘ pair) = _
    rw [← Measure.map_map hm hp,joint,Measure.map_map hm hmake]
    have he : ((fun p : H × O N => (p.1,read p)) ∘ make) = id := by
      funext p; exact Prod.ext rfl (inv p.1 p.2)
    rw [he,Measure.map_id]
  · let args := fun p : H × O N => (p.1,read p)
    have hargs : Measurable args := measurable_fst.prodMk hread
    have hfn : Measurable (Function.uncurry f) := hf
    have hcmp : Measurable (Function.uncurry f ∘ args) := hfn.comp hargs
    have snd' : Measurable (Prod.snd : H × O N → O N) := measurable_snd
    have hset : MeasurableSet {p : H × O N | p.2 = f p.1 (read p)} :=
      measurableSet_eq_fun snd' hcmp
    have hfull : ∀ᵐ p ∂μ.map pair, p.2 = f p.1 (read p) := by
      rw [joint]
      apply (ae_map_iff hmake.aemeasurable hset).mpr
      exact ae_of_all _ fun p => congrArg (f p.1) (inv p.1 p.2).symm
    exact (ae_map_iff hp.aemeasurable hset).mp hfull

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarRevelation
