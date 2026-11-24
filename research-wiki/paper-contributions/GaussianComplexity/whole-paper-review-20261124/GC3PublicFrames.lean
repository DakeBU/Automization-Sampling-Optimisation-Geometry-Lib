import GC43FrameMeasurable
import GC43Flow
import B4HistorySpace

/-! History-measurable oriented frames for primitive orthogonal oracle records. -/
noncomputable section
open Matrix MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

instance blockFrameMeasurableSpace (N m : ℕ) : MeasurableSpace (BlockFrame N m) :=
  MeasurableSpace.comap (fun F => (F.domain, F.range)) inferInstance

abbrev PublicFrame (N : ℕ) := Σ m : ℕ, BlockFrame N m

namespace PublicFrame
variable {N m n k : ℕ} {H Y : Type*} [MeasurableSpace H] [MeasurableSpace Y]

theorem measurable_domain_fixed : Measurable (@BlockFrame.domain N m) :=
  measurable_fst.comp (measurable_iff_comap_le.mpr le_rfl : Measurable (fun F : BlockFrame N m => (F.domain, F.range)))

theorem measurable_range_fixed : Measurable (@BlockFrame.range N m) :=
  measurable_snd.comp (measurable_iff_comap_le.mpr le_rfl : Measurable (fun F : BlockFrame N m => (F.domain, F.range)))

theorem measurable_blockFrame {F : H → BlockFrame N m}
    (hD : Measurable (fun h => (F h).domain)) (hR : Measurable (fun h => (F h).range)) :
    Measurable F :=
  by
    rw [measurable_iff_comap_le, blockFrameMeasurableSpace, MeasurableSpace.comap_comp]
    exact (hD.prodMk hR).comap_le

theorem measurable_tag (m : ℕ) : Measurable (Sigma.mk (β := BlockFrame N) m) := by
  intro s hs
  exact MeasurableSpace.measurableSet_iInf.mp hs m

theorem measurable_of_fibers {f : PublicFrame N → Y}
    (hf : ∀ m, Measurable (fun F : BlockFrame N m => f ⟨m,F⟩)) : Measurable f := by
  intro s hs
  exact MeasurableSpace.measurableSet_iInf.mpr (fun m => hf m hs)

theorem measurable_profile : Measurable (fun F : PublicFrame N => F.1) :=
  measurable_of_fibers (fun _ => measurable_const)

theorem measurable_domain : Measurable (fun F : PublicFrame N => F.2.domain) :=
  measurable_of_fibers (fun _ => measurable_domain_fixed)

theorem measurable_range : Measurable (fun F : PublicFrame N => F.2.range) :=
  measurable_of_fibers (fun _ => measurable_range_fixed)

theorem measurable_rank : Measurable (fun F : PublicFrame N => F.2.rank) := by
  have he : (fun F : PublicFrame N => F.2.rank) = fun F => N-F.1 := by
    funext F
    have hh := F.2.fits
    omega
  rw [he]
  exact measurable_const.sub measurable_profile

/-- Work at one fixed residual profile inside an arbitrary measurable public context. -/
theorem measurable_cases (F : H → PublicFrame N) (hF : Measurable F)
    (f : H → PublicFrame N → Y)
    (hf : ∀ m (hm : m ≤ N), Measurable (fun h => f h ⟨m,
      ⟨N-m, by omega, (F h).2.domain, (F h).2.range⟩⟩)) :
    Measurable (fun h => f h (F h)) := by
  let profile (h : H) : Fin (N+1) := ⟨(F h).1, by have e := (F h).2.fits; omega⟩
  have hs : Measurable (fun x : ℕ => Fin.ofNat (N+1) x) := Measurable.of_discrete
  have hp : Measurable profile := by
    convert hs.comp (measurable_profile.comp hF) using 1
    funext h
    apply Fin.ext
    exact (Nat.mod_eq_of_lt (profile h).isLt).symm
  let atProfile (x : Fin (N+1) × H) := f x.2 ⟨x.1.val,
    ⟨N-x.1.val,by have he := x.1.isLt; omega,(F x.2).2.domain,(F x.2).2.range⟩⟩
  have hm : Measurable atProfile := measurable_from_prod_countable_right fun i => hf i.val (by omega)
  convert hm.comp (hp.prodMk measurable_id) using 1
  funext h
  apply congrArg (f h)
  have eta (s : PublicFrame N) : s = ⟨s.1,
      ⟨N-s.1,by have he := s.2.fits; omega,s.2.domain,s.2.range⟩⟩ := by
    rcases s with ⟨m,r,e,D,R⟩
    change ⟨m,⟨r,e,D,R⟩⟩ = (⟨m,⟨N-m,_,D,R⟩⟩ : PublicFrame N)
    have he : N-m=r := by omega
    simp only [he]
  exact eta (F h)

/-- The normalized complement of the actual answer in the output frame. -/
def observed {m : ℕ} [NeZero m] (F : BlockFrame N m) (back : Bool) (y : Vec N) : S m :=
  unitOrFirst (frameComplement F (!back) y)

def recordStep (F : PublicFrame N) (back : Bool) (v y : Vec N) : PublicFrame N := by
  classical
  exact match F with
    | ⟨0,F⟩ => ⟨0,F⟩
    | ⟨1,F⟩ => ⟨1,F⟩
    | ⟨n+2,F⟩ => if frameComplement F back v = 0 then ⟨n+2,F⟩ else
        ⟨n+1, frameAfter F (sectionQ n) back v (observed F back y)⟩

theorem recordStep_zero (F : BlockFrame N (n+2)) (back : Bool) (v y : Vec N)
    (hc : frameComplement F back v = 0) :
    recordStep ⟨n+2,F⟩ back v y = ⟨n+2,F⟩ := by simp [recordStep,hc]

theorem recordStep_informative (F : BlockFrame N (n+2)) (back : Bool) (v y : Vec N)
    (hc : frameComplement F back v ≠ 0) :
    recordStep ⟨n+2,F⟩ back v y =
      ⟨n+1,frameAfter F (sectionQ n) back v (observed F back y)⟩ := by simp [recordStep,hc]

theorem observed_response (F : BlockFrame N (n+2)) (back : Bool) (v : Vec N)
    (z : S (n+2)) (hc : frameComplement F back v ≠ 0) :
    observed F back (frameResponse F back v z) = z :=
  recovered_observation F back v z hc

theorem measurable_recordStep {F : H → PublicFrame N} {back : H → Bool} {v y : H → Vec N}
    (hF : Measurable F) (hb : Measurable back) (hv : Measurable v) (hy : Measurable y) :
    Measurable (fun h => recordStep (F h) (back h) (v h) (y h)) := by
  apply measurable_cases F hF (fun h s => recordStep s (back h) (v h) (y h))
  intro m hm
  let G (h : H) : BlockFrame N m := ⟨N-m,by omega,(F h).2.domain,(F h).2.range⟩
  have hD : Measurable fun h => (G h).domain := measurable_domain.comp hF
  have hR : Measurable fun h => (G h).range := measurable_range.comp hF
  change Measurable (fun h => recordStep ⟨m,G h⟩ (back h) (v h) (y h))
  cases m with
  | zero => exact (measurable_tag 0).comp (measurable_blockFrame hD hR)
  | succ m =>
    cases m with
    | zero => exact (measurable_tag 1).comp (measurable_blockFrame hD hR)
    | succ n =>
      have ho : Measurable (fun h => observed (G h) (back h) (y h)) :=
        (measurable_unitOrFirst (n+2)).comp
          (measurable_frameComplement hD hR ((Measurable.of_discrete : Measurable Bool.not).comp hb) hy)
      have hf := measurable_frameAfter (sectionQ n) (sectionQ_meas n) hD hR hb hv ho
      exact Measurable.ite ((measurable_frameComplement hD hR hb hv) (measurableSet_singleton 0))
        ((measurable_tag _).comp (measurable_blockFrame hD hR))
        ((measurable_tag _).comp (measurable_blockFrame hf.1 hf.2))

theorem step_rank_le (F : PublicFrame N) (back : Bool) (v y : Vec N) :
    (recordStep F back v y).2.rank ≤ F.2.rank + 1 := by
  obtain ⟨m,F⟩ := F
  cases m with
  | zero => exact Nat.le_succ _
  | succ m =>
    cases m with
    | zero => exact Nat.le_succ _
    | succ n =>
      by_cases h : frameComplement F back v = 0
      · rw [recordStep_zero _ _ _ _ h]; exact Nat.le_succ _
      · rw [recordStep_informative _ _ _ _ h]; rfl

def Oriented (F : PublicFrame N) := F.2.domain.val.det = 1 ∧ F.2.range.val.det = 1

theorem oriented_after (F : BlockFrame N (n+2)) (back : Bool) (v : Vec N) (z : S (n+2))
    (hD : F.domain.val.det = 1) (hR : F.range.val.det = 1) :
    Oriented ⟨n+1,frameAfter F (sectionQ n) back v z⟩ := by
  rcases F with ⟨r,e,D,R⟩
  subst N
  exact ⟨extendFrame_oriented hD (sectionQ_det _ _),extendFrame_oriented hR (sectionQ_det _ _)⟩

theorem step_oriented (F : PublicFrame N) (back : Bool) (v y : Vec N) (h : Oriented F) :
    Oriented (recordStep F back v y) := by
  obtain ⟨m,F⟩ := F
  cases m with
  | zero => exact h
  | succ m =>
    cases m with
    | zero => exact h
    | succ n =>
      by_cases hc : frameComplement F back v = 0
      · rw [recordStep_zero _ _ _ _ hc]; exact h
      · rw [recordStep_informative _ _ _ _ hc]; exact oriented_after _ _ _ _ h.1 h.2

end PublicFrame
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
