import GC3RawPosterior
import GC3ResidualRead

/-! Zhou–Suzuki, Lemma B.3. Frames are Borel functions of the actual query and
reply records. In these frames the original matrices admit a measurable residual
factorization whose conditional law is the product of the specified determinant
components. The same functions define the frames and residuals for both signs. -/
noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open scoped ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
variable {N k : ℕ}

def historyResidual (h : Trace k N) (A : Ambient k N) : TaggedTuple k :=
  residualRead (PublicFrame.foldFrames h) A

def posterior (k N : ℕ) (b : ℝ) : Kernel (Trace k N) (TaggedTuple k) :=
  (residualKernel b).comap PublicFrame.foldFrames PublicFrame.measurable_foldFrames

/-- A complete posterior statement. The product kernel identity holds on every
history. The joint-law identity gives its conditional-law interpretation on the
original product-Haar probability space. -/
structure Factorization (b : ℝ) (μ : Measure (Ambient k N)) (history : Ambient k N → Trace k N) : Prop where
  measurable_domain : ∀ j, Measurable (fun h : Trace k N => (PublicFrame.foldFrames h j).2.domain)
  measurable_range : ∀ j, Measurable (fun h : Trace k N => (PublicFrame.foldFrames h j).2.range)
  measurable_rank : ∀ j, Measurable (fun h : Trace k N => (PublicFrame.foldFrames h j).2.rank)
  oriented : ∀ (h : Trace k N) j, PublicFrame.Oriented (PublicFrame.foldFrames h j)
  rank_bound : ∀ (h : Trace k N) j, (PublicFrame.foldFrames h j).2.rank ≤ blockCount j h
  remaining : ∀ (h : Trace k N) j,
    (PublicFrame.foldFrames h j).1 = N - (PublicFrame.foldFrames h j).2.rank
  measurable_residual : Measurable (Function.uncurry (@historyResidual N k))
  reconstruction : ∀ᵐ A ∂μ, ∀ j : Fin k,
    let F := PublicFrame.foldFrames (history A)
    let W := (historyResidual (history A) A).2 j
    A j = (F j).2.range *
      castOrthogonal (F j).2.fits (prefixEmbed (F j).1 (F j).2.rank W) * (F j).2.domain⁻¹
  product_kernel : ∀ h : Trace k N, posterior k N b h =
    (Measure.pi fun j => componentHaar (PublicFrame.foldFrames h j).1 b).map
      (Sigma.mk (β := ResidualTuple) (profile (PublicFrame.foldFrames h)))
  joint : μ.map (fun A => (history A, historyResidual (history A) A)) = (μ.map history) ⊗ₘ posterior k N b

/-- The adaptive posterior factorization for every Borel primitive algorithm at
every finite time, under the actual per-block cap. Both the block index and the
query sense may depend on the complete observed history. -/
theorem adaptive_posterior_factorization {N k T : ℕ} (hN : 2*T < N)
    (select : Trace k N → Option (Query k N)) (hs : Measurable select) (t : ℕ)
    (b : ℝ) (hb : b = -1 ∨ b = 1)
    (cap : ∀ᵐ A ∂(Measure.pi fun _ : Fin k => componentHaar N b),
      ∀ j, blockCount j (rawRun select t [] A) ≤ 2*T) :
    Factorization b (Measure.pi fun _ : Fin k => componentHaar N b) (rawRun select t []) := by
  let μ := Measure.pi fun _ : Fin k => componentHaar N b
  let h := rawRun select t []
  have hn : 0 < N := by omega
  let := isProbabilityMeasure_componentHaar hn hb
  let : IsProbabilityMeasure μ := by dsimp [μ]; infer_instance
  have hh : Measurable h := measurable_rawRun_fixed select hs t []
  have hpos (l : Trace k N) (j : Fin k) : 0 < (PublicFrame.foldFrames l j).1 :=
    PublicFrame.foldFrames_pos hn l j
  obtain ⟨joint,recon⟩ := residual_joint_of_ambient μ h hh PublicFrame.foldFrames
    PublicFrame.measurable_foldFrames hpos b hb (raw_ambient_posterior hN select hs t b hb cap)
  have hm (j : Fin k) : Measurable (fun l : Trace k N => PublicFrame.foldFrames l j) :=
    (measurable_pi_apply j).comp PublicFrame.measurable_foldFrames
  refine ⟨fun j => PublicFrame.measurable_domain.comp (hm j),
    fun j => PublicFrame.measurable_range.comp (hm j), fun j => PublicFrame.measurable_rank.comp (hm j),
    PublicFrame.foldFrames_oriented, PublicFrame.foldFrames_rank_le, ?_, ?_, ?_, ?_, joint⟩
  · intro l j
    have e := (PublicFrame.foldFrames l j).2.fits
    omega
  · exact measurable_residualRead.comp ((PublicFrame.measurable_foldFrames.comp measurable_fst).prodMk measurable_snd)
  · filter_upwards [recon] with A hA
    intro j
    have eqj := congrFun hA j
    change decodeAt _ _ _ j = A j at eqj
    rw [decodeAt_match] at eqj
    exact eqj.symm
  · intro l
    exact residualKernel_apply (PublicFrame.foldFrames l) (hpos l) b

#print axioms adaptive_posterior_factorization
end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
