import Mathlib.Analysis.Convex.SpecificFunctions.Basic
import Mathlib.Analysis.Convex.Quasiconvex
import Mathlib.Analysis.Normed.Module.Convex
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.LinearAlgebra.FiniteDimensional.Defs

/-!
# Log-concavity leaves

Small convex-analysis API for Chewi-style log-concave sampling foundations.
This file intentionally starts with definition-level and one-dimensional
sanity leaves; density normalization and Prekopa--Leindler stay separate.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace Geometry
namespace LogConcavity

open Set

/-- A positive real-valued function is log-concave on `s` when its logarithm is
concave on `s`.

The positivity condition is explicit because Chewi-style density arguments
usually need it separately from the convex-analysis statement about
`Real.log ∘ f`.
-/
def LogConcaveOn {E : Type*} [AddCommMonoid E] [Module ℝ E]
    (s : Set E) (f : E → ℝ) : Prop :=
  (∀ x ∈ s, 0 < f x) ∧ ConcaveOn ℝ s (fun x => Real.log (f x))

theorem logConcaveOn_iff {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ} :
    LogConcaveOn s f ↔
      (∀ x ∈ s, 0 < f x) ∧ ConcaveOn ℝ s (fun x => Real.log (f x)) :=
  Iff.rfl

theorem logConcaveOn_of_concave_log {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hpos : ∀ x ∈ s, 0 < f x)
    (hlog : ConcaveOn ℝ s (fun x => Real.log (f x))) :
    LogConcaveOn s f :=
  ⟨hpos, hlog⟩

theorem LogConcaveOn.pos {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) {x : E} (hx : x ∈ s) :
    0 < f x :=
  hf.1 x hx

theorem LogConcaveOn.concaveOn_log {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) :
    ConcaveOn ℝ s (fun x => Real.log (f x)) :=
  hf.2

/-- The negative logarithm of a positive log-concave function is convex. -/
theorem LogConcaveOn.convexOn_neg_log {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) :
    ConvexOn ℝ s (fun x => - Real.log (f x)) := by
  change ConvexOn ℝ s (-(fun x => Real.log (f x)))
  exact hf.concaveOn_log.neg

/-- Sublevel sets of the negative-log potential of a positive log-concave
function are convex. -/
theorem LogConcaveOn.convex_sublevel_neg_log {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) (r : ℝ) :
    Convex ℝ {x ∈ s | - Real.log (f x) ≤ r} :=
  hf.convexOn_neg_log.quasiconvexOn r

theorem LogConcaveOn.convex_domain {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) :
    Convex ℝ s :=
  hf.concaveOn_log.1

/-- Superlevel sets of a positive log-concave function are convex within the
log-concavity domain. -/
theorem LogConcaveOn.convex_superlevel {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) (c : ℝ) :
    Convex ℝ {x ∈ s | c ≤ f x} := by
  by_cases hc : c ≤ 0
  · intro x hx y hy a b ha hb hab
    have hmid_s := hf.convex_domain hx.1 hy.1 ha hb hab
    exact ⟨hmid_s, le_of_lt (lt_of_le_of_lt hc (hf.pos (x := a • x + b • y) hmid_s))⟩
  · have hcpos : 0 < c := lt_of_not_ge hc
    intro x hx y hy a b ha hb hab
    have hmid_s := hf.convex_domain hx.1 hy.1 ha hb hab
    refine ⟨hmid_s, ?_⟩
    have hlogx : Real.log c ≤ Real.log (f x) :=
      Real.log_le_log hcpos hx.2
    have hlogy : Real.log c ≤ Real.log (f y) :=
      Real.log_le_log hcpos hy.2
    have hweighted :
        a * Real.log c + b * Real.log c ≤
          a * Real.log (f x) + b * Real.log (f y) :=
      add_le_add (mul_le_mul_of_nonneg_left hlogx ha) (mul_le_mul_of_nonneg_left hlogy hb)
    have hconst : a * Real.log c + b * Real.log c = Real.log c := by
      calc
        a * Real.log c + b * Real.log c = (a + b) * Real.log c := by ring
        _ = Real.log c := by rw [hab]; ring
    have hfloor : Real.log c ≤ a * Real.log (f x) + b * Real.log (f y) := by
      simpa [hconst] using hweighted
    have hconc :
        a * Real.log (f x) + b * Real.log (f y) ≤
          Real.log (f (a • x + b • y)) := by
      simpa [smul_eq_mul] using hf.concaveOn_log.2 hx.1 hy.1 ha hb hab
    exact (Real.log_le_log_iff hcpos (hf.pos (x := a • x + b • y) hmid_s)).mp
      (hfloor.trans hconc)

/-- Positive log-concave functions are quasiconcave: all superlevel sets are convex. -/
theorem LogConcaveOn.quasiconcaveOn {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) :
    QuasiconcaveOn ℝ s f :=
  fun c => hf.convex_superlevel c

theorem LogConcaveOn.subset {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s t : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) (hts : t ⊆ s) (ht : Convex ℝ t) :
    LogConcaveOn t f :=
  ⟨fun x hx => hf.pos (x := x) (hts hx), hf.concaveOn_log.subset hts ht⟩

/-- Restricting a positive log-concave function to one of its superlevel sets
preserves log-concavity. -/
theorem LogConcaveOn.restrict_superlevel {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) (c : ℝ) :
    LogConcaveOn {x ∈ s | c ≤ f x} f :=
  hf.subset (fun _ hx => hx.1) (hf.convex_superlevel c)

/-- Precomposition by a linear map preserves log-concavity on the preimage domain. -/
theorem LogConcaveOn.comp_linearMap {E F : Type*}
    [AddCommMonoid E] [Module ℝ E] [AddCommMonoid F] [Module ℝ F]
    {s : Set F} {f : F → ℝ}
    (hf : LogConcaveOn s f) (g : E →ₗ[ℝ] F) :
    LogConcaveOn (g ⁻¹' s) (fun x : E => f (g x)) := by
  refine ⟨fun x hx => hf.pos (x := g x) hx, ?_⟩
  simpa [Function.comp_def] using hf.concaveOn_log.comp_linearMap g

/-- Precomposition by an affine map preserves log-concavity on the preimage domain. -/
theorem LogConcaveOn.comp_affineMap {E F : Type*}
    [AddCommGroup E] [Module ℝ E] [AddCommGroup F] [Module ℝ F]
    {s : Set F} {f : F → ℝ}
    (hf : LogConcaveOn s f) (g : E →ᵃ[ℝ] F) :
    LogConcaveOn (g ⁻¹' s) (fun x : E => f (g x)) := by
  refine ⟨fun x hx => hf.pos (x := g x) hx, ?_⟩
  simpa [Function.comp_def] using hf.concaveOn_log.comp_affineMap g

/-- The pointwise product of two positive log-concave functions on the same
domain is log-concave. -/
theorem LogConcaveOn.mul {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f g : E → ℝ}
    (hf : LogConcaveOn s f) (hg : LogConcaveOn s g) :
    LogConcaveOn s (fun x => f x * g x) := by
  refine ⟨fun x hx => mul_pos (hf.pos (x := x) hx) (hg.pos (x := x) hx), ?_⟩
  have hsum :
      ConcaveOn ℝ s ((fun x => Real.log (f x)) + fun x => Real.log (g x)) :=
    hf.concaveOn_log.add hg.concaveOn_log
  refine hsum.congr ?_
  intro x hx
  simpa using (Real.log_mul (hf.pos (x := x) hx).ne' (hg.pos (x := x) hx).ne').symm

/-- A nonnegative real power of a positive log-concave function is log-concave. -/
theorem LogConcaveOn.rpow {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ} {p : ℝ}
    (hf : LogConcaveOn s f) (hp : 0 ≤ p) :
    LogConcaveOn s (fun x => (f x) ^ p) := by
  refine ⟨fun x hx => Real.rpow_pos_of_pos (hf.pos (x := x) hx) p, ?_⟩
  have hscaled : ConcaveOn ℝ s (fun x => p • Real.log (f x)) :=
    hf.concaveOn_log.smul hp
  refine hscaled.congr ?_
  intro x hx
  simpa [smul_eq_mul] using (Real.log_rpow (hf.pos (x := x) hx) p).symm

/-- Product-domain tensorization: the product of log-concave factors on
convex domains is log-concave on the Cartesian product. -/
theorem LogConcaveOn.prod {E F : Type*}
    [AddCommMonoid E] [Module ℝ E] [AddCommMonoid F] [Module ℝ F]
    {s : Set E} {t : Set F} {f : E → ℝ} {g : F → ℝ}
    (hf : LogConcaveOn s f) (hg : LogConcaveOn t g) :
    LogConcaveOn (s ×ˢ t) (fun x : E × F => f x.1 * g x.2) := by
  refine ⟨fun x hx => mul_pos (hf.pos (x := x.1) hx.1) (hg.pos (x := x.2) hx.2), ?_⟩
  refine ⟨hf.convex_domain.prod hg.convex_domain, ?_⟩
  intro x hx y hy a b ha hb hab
  have hF := hf.concaveOn_log.2 hx.1 hy.1 ha hb hab
  have hG := hg.concaveOn_log.2 hx.2 hy.2 ha hb hab
  have hsum := add_le_add hF hG
  have hmid : a • x + b • y ∈ s ×ˢ t :=
    (hf.convex_domain.prod hg.convex_domain) hx hy ha hb hab
  calc
    a • Real.log (f x.1 * g x.2) + b • Real.log (f y.1 * g y.2)
        = (a • Real.log (f x.1) + b • Real.log (f y.1)) +
            (a • Real.log (g x.2) + b • Real.log (g y.2)) := by
          rw [Real.log_mul (hf.pos (x := x.1) hx.1).ne' (hg.pos (x := x.2) hx.2).ne',
            Real.log_mul (hf.pos (x := y.1) hy.1).ne' (hg.pos (x := y.2) hy.2).ne']
          simp [smul_eq_mul]
          ring
    _ ≤ Real.log (f (a • x.1 + b • y.1)) + Real.log (g (a • x.2 + b • y.2)) := hsum
    _ = Real.log (f (a • x.1 + b • y.1) * g (a • x.2 + b • y.2)) := by
          rw [Real.log_mul (hf.pos (x := a • x.1 + b • y.1) hmid.1).ne'
            (hg.pos (x := a • x.2 + b • y.2) hmid.2).ne']
    _ = Real.log (f (a • x + b • y).1 * g (a • x + b • y).2) := by simp

/-- Multiplication by a positive constant preserves log-concavity. -/
theorem LogConcaveOn.const_mul {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {f : E → ℝ}
    (hf : LogConcaveOn s f) {c : ℝ} (hc : 0 < c) :
    LogConcaveOn s (fun x => c * f x) := by
  refine ⟨fun x hx => mul_pos hc (hf.pos (x := x) hx), ?_⟩
  have hconst : ConcaveOn ℝ s (fun _ : E => Real.log c) :=
    concaveOn_const (Real.log c) hf.convex_domain
  have hsum :
      ConcaveOn ℝ s ((fun _ : E => Real.log c) + fun x => Real.log (f x)) :=
    hconst.add hf.concaveOn_log
  refine hsum.congr ?_
  intro x hx
  simpa using (Real.log_mul hc.ne' (hf.pos (x := x) hx).ne').symm

/-- A positive constant function is log-concave on every convex domain. -/
theorem logConcaveOn_const {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {c : ℝ} (hc : 0 < c) (hs : Convex ℝ s) :
    LogConcaveOn s (fun _ : E => c) :=
  ⟨fun _ _ => hc, concaveOn_const (Real.log c) hs⟩

/-- If `V` is convex, then the unnormalized Gibbs shape `exp (-V)` is
log-concave. -/
theorem logConcaveOn_exp_neg_of_convexOn {E : Type*} [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {V : E → ℝ} (hV : ConvexOn ℝ s V) :
    LogConcaveOn s (fun x => Real.exp (-V x)) := by
  refine ⟨fun _ _ => Real.exp_pos _, ?_⟩
  exact hV.neg.congr fun _ _ => by simp

/-- A positive multiple of the Gibbs shape of a convex potential is
log-concave.  This is the convex-analytic part of normalized Gibbs-density
bookkeeping; the measure/integral normalization proof is a separate leaf. -/
theorem logConcaveOn_const_mul_exp_neg_of_convexOn {E : Type*}
    [AddCommMonoid E] [Module ℝ E]
    {s : Set E} {V : E → ℝ} {c : ℝ}
    (hV : ConvexOn ℝ s V) (hc : 0 < c) :
    LogConcaveOn s (fun x => c * Real.exp (-V x)) :=
  (logConcaveOn_exp_neg_of_convexOn hV).const_mul hc

/-- The absolute value is convex on the real line. -/
theorem convexOn_univ_abs :
    ConvexOn ℝ (Set.univ : Set ℝ) (fun x : ℝ => |x|) := by
  change ConvexOn ℝ Set.univ (norm : ℝ → ℝ)
  exact convexOn_univ_norm

/-- Nonnegative absolute-linear real potentials are convex. -/
theorem convexOn_univ_const_mul_abs_add {a b : ℝ} (ha : 0 ≤ a) :
    ConvexOn ℝ (Set.univ : Set ℝ) (fun x : ℝ => a * |x| + b) := by
  have h := convexOn_univ_abs.smul ha
  change ConvexOn ℝ Set.univ ((fun x : ℝ => a * |x|) + fun _ => b)
  simpa only [smul_eq_mul] using h.add_const b

/-- The Gibbs shape of a nonnegative absolute-linear real potential is
log-concave. -/
theorem logConcaveOn_exp_neg_abs_linear {a b : ℝ} (ha : 0 ≤ a) :
    LogConcavity.LogConcaveOn (Set.univ : Set ℝ)
      (fun x : ℝ => Real.exp (-(a * |x| + b))) := by
  simpa using logConcaveOn_exp_neg_of_convexOn
    (convexOn_univ_const_mul_abs_add (a := a) (b := b) ha)

/-- Positive scalar normalization preserves log-concavity of absolute-linear
Laplace shapes. -/
theorem logConcaveOn_const_mul_exp_neg_abs_linear {a b c : ℝ}
    (ha : 0 ≤ a) (hc : 0 < c) :
    LogConcavity.LogConcaveOn (Set.univ : Set ℝ)
      (fun x : ℝ => c * Real.exp (-(a * |x| + b))) := by
  simpa using logConcaveOn_const_mul_exp_neg_of_convexOn
    (convexOn_univ_const_mul_abs_add (a := a) (b := b) ha) hc

/-- The explicitly normalized one-dimensional absolute-linear Laplace density
is log-concave as a real-valued density shape. -/
theorem logConcaveOn_explicit_abs_linear_normalized_density {a b : ℝ} (ha : 0 < a) :
    LogConcavity.LogConcaveOn (Set.univ : Set ℝ)
      (fun x : ℝ => (2 * Real.exp (-b) / a)⁻¹ * Real.exp (-(a * |x| + b))) := by
  have hZpos : 0 < 2 * Real.exp (-b) / a := by
    positivity
  exact logConcaveOn_const_mul_exp_neg_abs_linear
    (a := a) (b := b) (c := (2 * Real.exp (-b) / a)⁻¹) ha.le
    (inv_pos.mpr hZpos)

/-- The squared norm is convex on any real normed vector space. -/
theorem convexOn_univ_norm_sq {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] :
    ConvexOn ℝ (Set.univ : Set E) (fun x : E => ‖x‖ ^ 2) := by
  refine ⟨convex_univ, ?_⟩
  intro x _ y _ a b ha hb hab
  have hnorm : ‖a • x + b • y‖ ≤ a * ‖x‖ + b * ‖y‖ := by
    calc
      ‖a • x + b • y‖ ≤ ‖a • x‖ + ‖b • y‖ := norm_add_le _ _
      _ = a * ‖x‖ + b * ‖y‖ := by
        rw [norm_smul, norm_smul, Real.norm_of_nonneg ha, Real.norm_of_nonneg hb]
  have hnonneg : 0 ≤ a * ‖x‖ + b * ‖y‖ :=
    add_nonneg (mul_nonneg ha (norm_nonneg _)) (mul_nonneg hb (norm_nonneg _))
  have hsq : ‖a • x + b • y‖ ^ 2 ≤ (a * ‖x‖ + b * ‖y‖) ^ 2 := by
    exact (sq_le_sq₀ (norm_nonneg _) hnonneg).2 hnorm
  have hjensen : (a * ‖x‖ + b * ‖y‖) ^ 2 ≤ a * ‖x‖ ^ 2 + b * ‖y‖ ^ 2 := by
    have hdiff_nonneg : 0 ≤ a * b * (‖x‖ - ‖y‖) ^ 2 := by
      exact mul_nonneg (mul_nonneg ha hb) (sq_nonneg _)
    have hident :
        a * ‖x‖ ^ 2 + b * ‖y‖ ^ 2 - (a * ‖x‖ + b * ‖y‖) ^ 2 =
          a * b * (‖x‖ - ‖y‖) ^ 2 := by
      nlinarith [hab]
    nlinarith
  exact hsq.trans hjensen

/-- Nonnegative quadratic norm potentials are convex. -/
theorem convexOn_univ_const_mul_norm_sq_add
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {a b : ℝ} (ha : 0 ≤ a) :
    ConvexOn ℝ (Set.univ : Set E) (fun x : E => a * ‖x‖ ^ 2 + b) := by
  have h := (convexOn_univ_norm_sq (E := E)).smul ha
  change ConvexOn ℝ Set.univ ((fun x : E => a * ‖x‖ ^ 2) + fun _ => b)
  simpa only [smul_eq_mul] using h.add_const b

/-- The Gibbs shape of a nonnegative quadratic norm potential is log-concave. -/
theorem logConcaveOn_exp_neg_quadratic_norm
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {a b : ℝ} (ha : 0 ≤ a) :
    LogConcaveOn (Set.univ : Set E) (fun x : E => Real.exp (-(a * ‖x‖ ^ 2 + b))) := by
  simpa using logConcaveOn_exp_neg_of_convexOn
    (convexOn_univ_const_mul_norm_sq_add (E := E) (a := a) (b := b) ha)

/-- Positive multiples of nonnegative quadratic Gibbs shapes are log-concave. -/
theorem logConcaveOn_const_mul_exp_neg_quadratic_norm
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {a b c : ℝ} (ha : 0 ≤ a) (hc : 0 < c) :
    LogConcaveOn (Set.univ : Set E)
      (fun x : E => c * Real.exp (-(a * ‖x‖ ^ 2 + b))) := by
  simpa using logConcaveOn_const_mul_exp_neg_of_convexOn
    (convexOn_univ_const_mul_norm_sq_add (E := E) (a := a) (b := b) ha) hc

/-- The explicitly normalized finite-dimensional quadratic Gibbs density is log-concave. -/
theorem logConcaveOn_explicit_quadratic_normalized_density
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    {a b : ℝ} (ha : 0 < a) :
    LogConcaveOn (Set.univ : Set E)
      (fun x : E =>
        (Real.exp (-b) * (Real.pi / a) ^ ((Module.finrank ℝ E : ℝ) / 2))⁻¹ *
          Real.exp (-(a * ‖x‖ ^ 2 + b))) := by
  have hZpos : 0 < Real.exp (-b) * (Real.pi / a) ^ ((Module.finrank ℝ E : ℝ) / 2) := by
    exact mul_pos (Real.exp_pos _) (Real.rpow_pos_of_pos (div_pos Real.pi_pos ha) _)
  exact logConcaveOn_const_mul_exp_neg_quadratic_norm (E := E) (a := a) (b := b)
    ha.le (inv_pos.mpr hZpos)

/-- Shifted nonnegative quadratic norm potentials are convex. -/
theorem convexOn_univ_const_mul_norm_sub_sq_add
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {a b : ℝ} (m : E) (ha : 0 ≤ a) :
    ConvexOn ℝ (Set.univ : Set E) (fun x : E => a * ‖x - m‖ ^ 2 + b) := by
  let shift : E →ᵃ[ℝ] E :=
    { toFun := fun x => x - m
      linear := LinearMap.id
      map_vadd' := by
        intro p v
        simp [sub_eq_add_neg, add_assoc] }
  have h :=
    (convexOn_univ_const_mul_norm_sq_add (E := E) (a := a) (b := b) ha).comp_affineMap
      shift
  change ConvexOn ℝ Set.univ
    ((fun x : E => a * ‖x‖ ^ 2 + b) ∘ shift)
  exact h

/-- The Gibbs shape of a shifted nonnegative quadratic norm potential is log-concave. -/
theorem logConcaveOn_exp_neg_shifted_quadratic_norm
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {a b : ℝ} (m : E) (ha : 0 ≤ a) :
    LogConcaveOn (Set.univ : Set E)
      (fun x : E => Real.exp (-(a * ‖x - m‖ ^ 2 + b))) := by
  simpa using logConcaveOn_exp_neg_of_convexOn
    (convexOn_univ_const_mul_norm_sub_sq_add (E := E) (a := a) (b := b) m ha)

/-- Positive multiples of shifted nonnegative quadratic Gibbs shapes are log-concave. -/
theorem logConcaveOn_const_mul_exp_neg_shifted_quadratic_norm
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {a b c : ℝ} (m : E) (ha : 0 ≤ a) (hc : 0 < c) :
    LogConcaveOn (Set.univ : Set E)
      (fun x : E => c * Real.exp (-(a * ‖x - m‖ ^ 2 + b))) := by
  simpa using logConcaveOn_const_mul_exp_neg_of_convexOn
    (convexOn_univ_const_mul_norm_sub_sq_add (E := E) (a := a) (b := b) m ha) hc

/-- The explicitly normalized shifted finite-dimensional quadratic Gibbs density is log-concave. -/
theorem logConcaveOn_explicit_shifted_quadratic_normalized_density
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    {a b : ℝ} (m : E) (ha : 0 < a) :
    LogConcaveOn (Set.univ : Set E)
      (fun x : E =>
        (Real.exp (-b) * (Real.pi / a) ^ ((Module.finrank ℝ E : ℝ) / 2))⁻¹ *
          Real.exp (-(a * ‖x - m‖ ^ 2 + b))) := by
  have hZpos : 0 < Real.exp (-b) * (Real.pi / a) ^ ((Module.finrank ℝ E : ℝ) / 2) := by
    exact mul_pos (Real.exp_pos _) (Real.rpow_pos_of_pos (div_pos Real.pi_pos ha) _)
  exact logConcaveOn_const_mul_exp_neg_shifted_quadratic_norm
    (E := E) (a := a) (b := b) m ha.le (inv_pos.mpr hZpos)

/-- The two-point quadratic potential `(x, y) ↦ a‖x-y‖^2+b` is convex. -/
theorem convexOn_univ_const_mul_norm_fst_sub_snd_sq_add
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {a b : ℝ} (ha : 0 ≤ a) :
    ConvexOn ℝ (Set.univ : Set (E × E))
      (fun z : E × E => a * ‖z.1 - z.2‖ ^ 2 + b) := by
  let diff : E × E →ₗ[ℝ] E := LinearMap.fst ℝ E E - LinearMap.snd ℝ E E
  have h :=
    (convexOn_univ_const_mul_norm_sq_add (E := E) (a := a) (b := b) ha).comp_linearMap
      diff
  change ConvexOn ℝ Set.univ
    ((fun x : E => a * ‖x‖ ^ 2 + b) ∘ diff)
  exact h

/-- The two-point quadratic Gibbs kernel shape `(x, y) ↦ exp (-(a‖x-y‖^2+b))`
is log-concave on the product space. -/
theorem logConcaveOn_exp_neg_pair_sub_quadratic_norm
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {a b : ℝ} (ha : 0 ≤ a) :
    LogConcaveOn (Set.univ : Set (E × E))
      (fun z : E × E => Real.exp (-(a * ‖z.1 - z.2‖ ^ 2 + b))) := by
  simpa using logConcaveOn_exp_neg_of_convexOn
    (convexOn_univ_const_mul_norm_fst_sub_snd_sq_add (E := E) (a := a) (b := b) ha)

/-- Positive multiples of two-point quadratic Gibbs kernel shapes are log-concave. -/
theorem logConcaveOn_const_mul_exp_neg_pair_sub_quadratic_norm
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]
    {a b c : ℝ} (ha : 0 ≤ a) (hc : 0 < c) :
    LogConcaveOn (Set.univ : Set (E × E))
      (fun z : E × E => c * Real.exp (-(a * ‖z.1 - z.2‖ ^ 2 + b))) := by
  simpa using logConcaveOn_const_mul_exp_neg_of_convexOn
    (convexOn_univ_const_mul_norm_fst_sub_snd_sq_add (E := E) (a := a) (b := b) ha) hc

/-- The finite-dimensional Gaussian-kernel normalizing constant times
`exp (-(a‖x-y‖^2+b))` is log-concave as a function of `(x, y)`.

This is a geometry/kernel-shape leaf.  It does not claim that the function is a
probability density on the full product space. -/
theorem logConcaveOn_explicit_pair_sub_quadratic_kernel
    {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    {a b : ℝ} (ha : 0 < a) :
    LogConcaveOn (Set.univ : Set (E × E))
      (fun z : E × E =>
        (Real.exp (-b) * (Real.pi / a) ^ ((Module.finrank ℝ E : ℝ) / 2))⁻¹ *
          Real.exp (-(a * ‖z.1 - z.2‖ ^ 2 + b))) := by
  have hZpos : 0 < Real.exp (-b) * (Real.pi / a) ^ ((Module.finrank ℝ E : ℝ) / 2) := by
    exact mul_pos (Real.exp_pos _) (Real.rpow_pos_of_pos (div_pos Real.pi_pos ha) _)
  exact logConcaveOn_const_mul_exp_neg_pair_sub_quadratic_norm
    (E := E) (a := a) (b := b) ha.le (inv_pos.mpr hZpos)

/-- The identity density on the positive ray is log-concave. -/
theorem logConcaveOn_id_Ioi :
    LogConcaveOn (Ioi (0 : ℝ)) (fun x : ℝ => x) :=
  ⟨fun _ hx => hx, strictConcaveOn_log_Ioi.concaveOn⟩

end LogConcavity
end Geometry
end TechnicalLemmas
end AutoSamplingTheory
