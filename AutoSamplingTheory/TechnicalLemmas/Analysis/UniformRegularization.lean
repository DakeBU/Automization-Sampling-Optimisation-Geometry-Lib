import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle
import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationTransfer
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Algebra.Order.Floor.Ring

/-!
# A uniform finite-query regularization reduction

Chewi arXiv2605.07006v1 §1.1 and §4.1 Lemma4.2. One fixed strongly convex
solver is transformed into one fixed convex solver, using actual oracle runs.
The natural-valued budget, positive small-error regime and deterministic
finite-query semantics are explicit boundaries of this integration theorem.
-/
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.UniformRegularization
open Set QuadraticRegularizationOracle
open scoped NNReal

set_option backward.isDefEq.respectTransparency false in
/-- Uniform success and actual query bounds for the corrected program. The
callbacks and initial state are fixed before either objective is quantified.
No monotonicity of the natural-valued budget function is required. -/
theorem uniform_accuracy_and_query_bound
    {E S : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [ProperSpace E]
    (β : ℝ≥0) (u : E) {R ε : ℝ} (hR : 0 < R) (hε : 0 < ε)
    (hsmall : ε ≤ (β : ℝ)*R^2) (φ : ℝ → ℕ)
    (next : S → Sum E E) (update : S → E → (ℝ × E) → S) (s₀ : S) :
    let δ : ℝ≥0 := NNReal.mk (ε/R^2) (div_pos hε (sq_pos_of_pos hR)).le
    let N := ⌈(φ ((2*(β : ℝ))/(δ : ℝ)) : ℝ) *
      Real.log ((δ : ℝ)*R^2/(ε/2))⌉₊
    (∀ g : E → ℝ, Differentiable ℝ g → StrongConvexOn univ (δ : ℝ) g →
      LipschitzWith (2*β) (gradient g) → ∀ w : E,
      IsMinOn g univ w → ‖w-u‖ ≤ R →
      ∃ t x c, run next update (fun y => (g y, gradient g y)) N s₀ =
        ((t, some x), c) ∧ g x-g w ≤ ε/2) →
    let corrected := fun s y (a : ℝ × E) =>
      update s y (a.1+(δ : ℝ)/2*‖y-u‖^2, a.2+(δ : ℝ) • (y-u))
    ∀ f : E → ℝ, Differentiable ℝ f → ConvexOn ℝ univ f →
      LipschitzWith β (gradient f) → ∀ z : E,
      IsMinOn f univ z → ‖z-u‖ ≤ R →
      ∃ t x c, run next corrected (fun y => (f y, gradient f y)) N s₀ =
        ((t, some x), c) ∧ f x-f z ≤ ε ∧
        c ≤ ⌈(φ (2*(β : ℝ)*R^2/ε) : ℝ)*Real.log 2⌉₊ ∧
        c ≤ φ (2*(β : ℝ)*R^2/ε) := by
  dsimp only
  let δ : ℝ≥0 := NNReal.mk (ε/R^2) (div_pos hε (sq_pos_of_pos hR)).le
  let N := ⌈(φ ((2*(β : ℝ))/(δ : ℝ)) : ℝ)*
    Real.log ((δ : ℝ)*R^2/(ε/2))⌉₊
  intro hs f hd hc hL z hz hr
  let W := fun x => f x+(δ : ℝ)/2*‖x-u‖^2
  have hδβ : (δ : ℝ) ≤ β := (div_le_iff₀ (sq_pos_of_pos hR)).mpr hsmall
  obtain ⟨hWd,hsc,_,hWL⟩ :=
    QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness hd hc hL (δ := δ) u
  have hWL' : LipschitzWith (2*β) (gradient W) := by
    apply LipschitzWith.of_dist_le_mul
    intro x y
    calc
      dist (gradient W x) (gradient W y) ≤ ((β+δ : ℝ≥0) : ℝ)*dist x y :=
        hWL.dist_le_mul x y
      _ ≤ ((2*β : ℝ≥0) : ℝ)*dist x y := by
        apply mul_le_mul_of_nonneg_right _ dist_nonneg
        norm_num only [NNReal.coe_add, NNReal.coe_mul, NNReal.coe_ofNat]
        linarith
  obtain ⟨w,hw,hwR,haccuracy⟩ :=
    QuadraticRegularizationTransfer.exists_minimizer_radius_and_accuracy hd.continuous hz hR hε hr
  obtain ⟨t,x,c,hex,hgap⟩ := hs W hWd hsc hWL' w hw (hwR.trans hr)
  obtain ⟨heq,hcount⟩ :=
    QuadraticRegularizationOracle.simulate_regularized next update hd hc hL (δ := δ) u N s₀
  have hout : run next
      (fun s y (a : ℝ × E) => update s y
        (a.1+(δ : ℝ)/2*‖y-u‖^2,a.2+(δ : ℝ) • (y-u)))
      (fun y => (f y,gradient f y)) N s₀ = ((t,some x),c) := heq.trans hex
  have hcN : c ≤ N := by simpa only [hout] using hcount
  have hratio : 2*(β : ℝ)/(δ : ℝ) = 2*(β : ℝ)*R^2/ε := by
    change 2*(β : ℝ)/(ε/R^2) = 2*(β : ℝ)*R^2/ε
    field_simp [ne_of_gt hε, ne_of_gt hR]
  have hlog : (δ : ℝ)*R^2/(ε/2) = 2 := by
    change ε/R^2*R^2/(ε/2) = 2
    field_simp [ne_of_gt hε, ne_of_gt hR]
  have hN : N = ⌈(φ (2*(β : ℝ)*R^2/ε) : ℝ)*Real.log 2⌉₊ := by
    simp only [N, hratio, hlog]
  have hceil : N ≤ φ (2*(β : ℝ)*R^2/ε) := by
    rw [hN, Nat.ceil_le]
    have hl : Real.log 2 ≤ 1 := by
      have := Real.log_le_sub_one_of_pos (by norm_num : (0:ℝ)<2)
      linarith
    simpa using mul_le_mul_of_nonneg_left hl
      (Nat.cast_nonneg (φ (2*(β : ℝ)*R^2/ε)) : (0:ℝ) ≤ _)
  exact ⟨t,x,c,hout,haccuracy x hgap,by simpa only [← hN] using hcN,hcN.trans hceil⟩
end AutoSamplingTheory.TechnicalLemmas.Analysis.UniformRegularization
