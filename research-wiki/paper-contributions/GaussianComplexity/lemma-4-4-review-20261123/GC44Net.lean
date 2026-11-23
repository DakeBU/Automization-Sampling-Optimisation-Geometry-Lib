import GC44GramUse
import GC44Rayleigh
import Mathlib.Analysis.Normed.Module.Normalize
import Mathlib.Tactic

/-! # A finite normalized coordinate net for real symmetric quadratic forms -/
noncomputable section
open Matrix
open scoped Matrix.Norms.L2Operator RealInnerProductSpace
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

private abbrev Grid (r : ℕ) := Fin r → Fin (32*r+1)

private def rawPoint {r : ℕ} (a : Grid r) : Space r :=
  WithLp.toLp 2 (fun i => ((a i).val : ℝ)/(16*r) - 1)

/-- Nonzero grid points in the unit cube, normalized to the sphere. -/
def sphereNet (r : ℕ) : Finset (Space r) := by
  classical
  exact ((Finset.univ : Finset (Grid r)).filter (fun a => rawPoint a ≠ 0)).image
    (fun a => NormedSpace.normalize (rawPoint a))

theorem sphereNet_card_le (r : ℕ) : (sphereNet r).card ≤ (32*r+1)^r := by
  classical
  exact Finset.card_image_le.trans ((Finset.card_filter_le ..).trans_eq (by simp [Grid]))

theorem norm_of_mem_sphereNet {r : ℕ} {z : Space r} (hz : z ∈ sphereNet r) : ‖z‖ = 1 := by
  classical
  obtain ⟨a,ha,rfl⟩ := Finset.mem_image.mp hz
  exact NormedSpace.norm_normalize_eq_one_iff.mpr (Finset.mem_filter.mp ha).2

private theorem grid_close {r : ℕ} (hr : 0 < r) {x : Space r} (hx : ‖x‖ = 1) :
    ∃ a : Grid r, ‖x-rawPoint a‖ ≤ 1/8 := by
  let R : ℝ := r
  have hR : (1 : ℝ) ≤ R := by dsimp [R]; exact_mod_cast (show 1 ≤ r by omega)
  have hden : 0 < 16*R := by linarith
  have hxabs (i : Fin r) : |x i| ≤ 1 := by
    have h := Finset.single_le_sum (f := fun j : Fin r => (x j)^2)
      (fun j _ => sq_nonneg (x j)) (Finset.mem_univ i)
    rw [← EuclideanSpace.real_norm_sq_eq, hx] at h
    exact abs_le.mpr ⟨by nlinarith, by nlinarith⟩
  let t (i : Fin r) := (x i + 1) * (16*R)
  have ht (i : Fin r) : 0 ≤ t i :=
    mul_nonneg (by linarith [(abs_le.mp (hxabs i)).1]) hden.le
  have hfloor (i : Fin r) : ⌊t i⌋₊ < 32*r+1 := by
    have h1 := Nat.floor_le (ht i)
    have h2 : t i ≤ 32*R := by
      dsimp [t]; nlinarith [mul_nonneg (sub_nonneg.mpr (abs_le.mp (hxabs i)).2) hden.le]
    dsimp only [R] at h2
    exact Nat.lt_succ_of_le (by exact_mod_cast h1.trans h2)
  let a : Grid r := fun i => ⟨⌊t i⌋₊, hfloor i⟩
  refine ⟨a, ?_⟩
  let y := rawPoint a
  have hcoord (i : Fin r) : |((x-y) i)| ≤ 1/(16*R) := by
    change |x i - ((⌊t i⌋₊ : ℝ)/(16*R)-1)| ≤ _
    have h1 := Nat.floor_le (ht i)
    have h2 := Nat.lt_floor_add_one (t i)
    rw [abs_le]
    constructor <;> field_simp <;> dsimp [t] at h1 h2 <;> linarith
  have hsum : ‖x-y‖^2 ≤ R * (1/(16*R))^2 := by
    rw [EuclideanSpace.real_norm_sq_eq]
    calc
      _ ≤ ∑ i : Fin r, (1/(16*R))^2 := Finset.sum_le_sum fun i _ =>
        (sq_abs ((x-y) i)) ▸ pow_le_pow_left₀ (abs_nonneg _) (hcoord i) 2
      _ = _ := by simp [R]
  have hsmall : R * (1/(16*R))^2 ≤ (1/8 : ℝ)^2 := by
    have hRn : 0 < R := by linarith
    field_simp
    nlinarith
  nlinarith [hsum.trans hsmall, norm_nonneg (x-y)]

theorem exists_mem_sphereNet_close {r : ℕ} (hr : 0 < r) {x : Space r} (hx : ‖x‖ = 1) :
    ∃ z ∈ sphereNet r, ‖x-z‖ ≤ 1/4 := by
  classical
  obtain ⟨a,ha⟩ := grid_close hr hx
  let y := rawPoint a
  have hy : y ≠ 0 := by intro h; change ‖x-y‖ ≤ _ at ha; rw [h, sub_zero, hx] at ha; norm_num at ha
  let z := NormedSpace.normalize y
  have hz : ‖z‖ = 1 := NormedSpace.norm_normalize_eq_one_iff.mpr hy
  refine ⟨z, Finset.mem_image.mpr ⟨a, Finset.mem_filter.mpr ⟨Finset.mem_univ _,hy⟩,rfl⟩, ?_⟩
  have hdiff : y-z = (‖y‖ - 1) • z := by
    rw [sub_smul, one_smul, NormedSpace.norm_smul_normalize]
  have hlen : ‖y-z‖ ≤ ‖x-y‖ := by
    rw [hdiff, norm_smul, hz, mul_one, Real.norm_eq_abs, ← hx, abs_sub_comm]
    exact abs_norm_sub_norm_le _ _
  have htri : ‖x-z‖ ≤ ‖x-y‖+‖y-z‖ := by simpa only [dist_eq_norm] using dist_triangle x y z
  linarith

private theorem bilinear_bound {r : ℕ} (H : Matrix (Fin r) (Fin r) ℝ) (x y : Space r) :
    |WithLp.ofLp x ⬝ᵥ (H *ᵥ WithLp.ofLp y)| ≤ ‖H‖*‖x‖*‖y‖ := by
  rw [← Matrix.inner_toEuclideanCLM H]
  calc
    _ ≤ ‖x‖ * ‖Matrix.toEuclideanCLM (𝕜 := ℝ) H y‖ := abs_real_inner_le_norm _ _
    _ ≤ ‖x‖ * (‖H‖ * ‖y‖) := mul_le_mul_of_nonneg_left (H.l2_opNorm_mulVec y) (norm_nonneg _)
    _ = _ := by ring

/-- Testing a real symmetric matrix on the fixed net controls its operator norm. -/
theorem opNorm_le_of_sphereNet {r : ℕ} (hr : 0 < r) (H : Matrix (Fin r) (Fin r) ℝ)
    (hH : H.IsHermitian) {t : ℝ} (ht : 0 ≤ t)
    (hb : ∀ z ∈ sphereNet r, |WithLp.ofLp z ⬝ᵥ (H *ᵥ WithLp.ofLp z)| ≤ t) : ‖H‖ ≤ 2*t := by
  let Q (x : Space r) := WithLp.ofLp x ⬝ᵥ (H *ᵥ WithLp.ofLp x)
  have hunit (x : Space r) (hx : ‖x‖ = 1) : |Q x| ≤ t + ‖H‖/2 := by
    obtain ⟨z,hz,hd⟩ := exists_mem_sphereNet_close hr hx
    have hzn := norm_of_mem_sphereNet hz
    have hdiff : Q x - Q z = WithLp.ofLp (x-z) ⬝ᵥ (H *ᵥ WithLp.ofLp x) +
        WithLp.ofLp z ⬝ᵥ (H *ᵥ WithLp.ofLp (x-z)) := by
      change _ = (WithLp.ofLp x - WithLp.ofLp z) ⬝ᵥ _ + _ ⬝ᵥ (H *ᵥ (WithLp.ofLp x - WithLp.ofLp z))
      rw [sub_dotProduct, Matrix.mulVec_sub, dotProduct_sub]
      dsimp [Q]
      ring
    have h₁ := bilinear_bound H (x-z) x
    have h₂ := bilinear_bound H z (x-z)
    rw [hx, mul_one] at h₁
    rw [hzn, mul_one] at h₂
    have hδ : ‖H‖*‖x-z‖ ≤ ‖H‖/4 := by linarith [mul_le_mul_of_nonneg_left hd (norm_nonneg H)]
    have hbound := (abs_add_le ..).trans (add_le_add h₁ h₂)
    rw [← hdiff] at hbound
    calc
      |Q x| = |Q x - Q z + Q z| := by rw [sub_add_cancel]
      _ ≤ |Q x - Q z| + |Q z| := abs_add_le ..
      _ ≤ _ := by linarith [hb z hz]
  have hsmul (a : ℝ) (x : Space r) : Q (a • x) = a^2 * Q x := by
    change (a • WithLp.ofLp x) ⬝ᵥ (H *ᵥ (a • WithLp.ofLp x)) = _
    rw [Matrix.mulVec_smul, smul_dotProduct, dotProduct_smul]
    dsimp only [Q, smul_eq_mul]
    ring
  have h : ‖H‖ ≤ t+‖H‖/2 := by
    apply CosineProjection.opNorm_le_of_form H hH (by positivity)
    intro v
    let x : Space r := WithLp.toLp 2 v
    change |Q x| ≤ (t+‖H‖/2)*‖x‖^2
    by_cases hx : x=0
    · simp [hx,Q]
    have hy := hunit (NormedSpace.normalize x) (NormedSpace.norm_normalize_eq_one_iff.mpr hx)
    have he := hsmul ‖x‖ (NormedSpace.normalize x)
    rw [NormedSpace.norm_smul_normalize] at he
    rw [he,abs_mul,abs_of_nonneg (sq_nonneg _),mul_comm]
    exact mul_le_mul_of_nonneg_right hy (sq_nonneg _)
  linarith

#print axioms opNorm_le_of_sphereNet

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
