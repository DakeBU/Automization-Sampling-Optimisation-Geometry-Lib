import GC3PublicFrames

/-! A total measurable inverse on the image of each residual block embedding. -/
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarStabilizerBlock
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
variable {N m : ℕ}

private theorem injective_prefix (m r : ℕ) : Function.Injective (prefixEmbed m r) := by
  induction r with
  | zero => exact Function.injective_id
  | succ r ih =>
    intro a b h
    apply ih
    apply Subtype.ext
    ext i j
    exact congrArg (fun W : O ((m+r)+1) => W.val i.succ j.succ) h

private theorem prefix_embedding (m r : ℕ) : MeasurableEmbedding (prefixEmbed m r) :=
  ((continuous_prefixEmbed m r).isClosedEmbedding (injective_prefix m r)).measurableEmbedding

/-- Strip the identity prefix on its image and choose a fixed default elsewhere. -/
def stripPrefix (m r : ℕ) : O (m+r) → O m := (prefix_embedding m r).invFun

theorem measurable_stripPrefix (m r : ℕ) : Measurable (stripPrefix m r) :=
  (prefix_embedding m r).measurable_invFun

@[simp] theorem stripPrefix_embed (m r : ℕ) (w : O m) :
    stripPrefix m r (prefixEmbed m r w) = w := (prefix_embedding m r).leftInverse_invFun w

private def stripFrame (F : BlockFrame N m) (A : O N) : O m :=
  stripPrefix m F.rank (castOrthogonal F.fits.symm (F.range⁻¹ * A * F.domain))

private theorem stripFrame_realize (F : BlockFrame N m) (w : O m) : stripFrame F (F.realize w) = w := by
  rcases F with ⟨r,hr,D,R⟩
  subst N
  change stripPrefix m r (R⁻¹ * (R * prefixEmbed m r w * D⁻¹) * D) = w
  rw [show R⁻¹ * (R * prefixEmbed m r w * D⁻¹) * D = prefixEmbed m r w by group]
  exact stripPrefix_embed m r w

private def fixedFrame (m : ℕ) (hm : m ≤ N) (F : PublicFrame N) : BlockFrame N m :=
  ⟨N-m, by omega, F.2.domain, F.2.range⟩

private theorem fixedFrame_tag (h : m ≤ N) (F : BlockFrame N m) : fixedFrame m h ⟨m,F⟩ = F := by
  rcases F with ⟨r,hr,D,R⟩
  change (⟨N-m,_,D,R⟩ : BlockFrame N m) = ⟨r,hr,D,R⟩
  have e : N-m = r := by omega
  simp [e]

def readResidualAt (m : ℕ) (F : PublicFrame N) (A : O N) : O m :=
  if h : m ≤ N then stripFrame (fixedFrame m h F) A else 1

theorem measurable_readResidualAt (m : ℕ) :
    Measurable (Function.uncurry (@readResidualAt N m)) := by
  change Measurable (fun p : PublicFrame N × O N => readResidualAt m p.1 p.2)
  by_cases hm : m ≤ N
  · simp only [readResidualAt, dif_pos hm, stripFrame, fixedFrame]
    have hc {a b : ℕ} (e : a=b) : Measurable (castOrthogonal e) := by subst b; exact measurable_id
    have hp : Measurable (fun p : PublicFrame N × O N => p.1.2.range⁻¹ * p.2 * p.1.2.domain) :=
      (((PublicFrame.measurable_range.comp measurable_fst).inv.mul measurable_snd).mul
        (PublicFrame.measurable_domain.comp measurable_fst))
    exact (measurable_stripPrefix m (N-m)).comp ((hc (show N=m+(N-m) by omega)).comp hp)
  · simp only [readResidualAt,dif_neg hm]
    exact measurable_const

theorem readResidualAt_realize (F : BlockFrame N m) (w : O m) :
    readResidualAt m ⟨m,F⟩ (F.realize w) = w := by
  have hm : m ≤ N := by have h := F.fits; omega
  rw [readResidualAt, dif_pos hm, fixedFrame_tag, stripFrame_realize]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.AdaptivePosterior
