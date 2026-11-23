import GC43StartSpan
import GC43Exposed
import HaarOrientedSection

/-! A finite protocol of forward and inverse primitive queries on one actual rotation. -/
noncomputable section
open Matrix MeasureTheory ProbabilityTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarOrientedSection
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling

structure Program (N : ℕ) (State : Type*) [MeasurableSpace State] where
  back : ℕ → Bool
  vector : ℕ → State → Vec N
  update : ℕ → State → Vec N → State
  measurable_vector : ∀ t, Measurable (vector t)
  measurable_update : ∀ t, Measurable (Function.uncurry (update t))

structure Report (N : ℕ) (State : Type*) where
  priorState : State
  answer : Vec N
  start : E N
  priorDomain : O N
  priorRank : ℕ
  nextDomain : O N
  nextRank : ℕ

variable {N : ℕ} {State : Type*} [MeasurableSpace State]

def sectionQ (n : ℕ) := Classical.choose (exists_measurable_oriented_section n)

theorem sectionQ_meas (n : ℕ) : Measurable (sectionQ n) :=
  (Classical.choose_spec (exists_measurable_oriented_section n)).1

theorem sectionQ_col (n : ℕ) (z : S (n+2)) :
    (sectionQ n z).val *ᵥ Pi.single (0 : Fin (n+2)) 1 = z.val.ofLp :=
  ((Classical.choose_spec (exists_measurable_oriented_section n)).2 z).2

theorem sectionQ_det (n : ℕ) (z : S (n+2)) : (sectionQ n z).val.det = 1 :=
  ((Classical.choose_spec (exists_measurable_oriented_section n)).2 z).1

def ambientGaussian {m : ℕ} (F : BlockFrame N m) (x : E N) (z : S m) : E N :=
  WithLp.toLp 2 (castVec F.fits (gaussianize (castOrthogonal F.fits.symm F.domain)
    (WithLp.toLp 2 (castVec F.fits.symm x.ofLp)) z).ofLp)

theorem ambientGaussian_law {m : ℕ} [NeZero m] (F : BlockFrame N m) :
    ((stdGaussian (E N)).prod (sphereProbability m)).map (Function.uncurry (ambientGaussian F)) =
      stdGaussian (E N) := by
  rcases F with ⟨r,h,D,R⟩
  subst N
  exact gaussianize_law D

def perStepStart {m : ℕ} [NeZero m] (F : BlockFrame N m) (back : Bool)
    (v : Vec N) (noise : E N) (z : S m) : E N := by
  classical
  exact if back = true ∧ frameComplement F back v ≠ 0 then ambientGaussian F noise z else noise

def ambientAnswer {m : ℕ} (F : BlockFrame N m) (W : O m) (back : Bool) (v : Vec N) :=
  if back then act (F.realize W)⁻¹ v else act (F.realize W) v

def emit {m m' : ℕ} (F : BlockFrame N m) (F' : BlockFrame N m') (s : State)
    (y : Vec N) (g : E N) : Report N State :=
  ⟨s, y, g, F.domain, F.rank, F'.domain, F'.rank⟩

/-- Compute all the primitive answers and Gaussian starts on the same rotation,
using one independent ambient-coordinate Gaussian at every primitive time. -/
def walk (P : Program N State) (clock : ℕ) : (fuel : ℕ) → {m : ℕ} → BlockFrame N m →
    State → O m → (Fin fuel → E N) → Fin fuel → Report N State
  | 0, _, _, _, _, _ => Fin.elim0
  | k+1, 0, F, s, W, noise =>
    let v := P.vector clock s
    let y := ambientAnswer F W (P.back clock) v
    Fin.cons (emit F F s y (noise 0))
      (walk P (clock+1) k F (P.update clock s y) W (Fin.tail noise))
  | k+1, 1, F, s, W, noise =>
    let v := P.vector clock s
    let b := P.back clock
    let z := frameObservation F b v W
    let y := frameResponse F b v z
    Fin.cons (emit F F s y (perStepStart F b v (noise 0) z))
      (walk P (clock+1) k F (P.update clock s y) W (Fin.tail noise))
  | k+1, n+2, F, s, W, noise => by
    classical
    let v := P.vector clock s
    let b := P.back clock
    let u := frameUnit F b v
    let p := selectedHaarStep (sectionQ n) (sectionQ_col n) b u W
    let y := frameResponse F b v p.1
    let F' := frameAfter F (sectionQ n) b v p.1
    let s' := P.update clock s y
    exact if frameComplement F b v = 0 then
      Fin.cons (emit F F s y (noise 0)) (walk P (clock+1) k F s' W (Fin.tail noise))
    else Fin.cons (emit F F' s y (perStepStart F b v (noise 0) p.1))
      (walk P (clock+1) k F' s' p.2 (Fin.tail noise))
termination_by fuel => fuel

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCoupling
