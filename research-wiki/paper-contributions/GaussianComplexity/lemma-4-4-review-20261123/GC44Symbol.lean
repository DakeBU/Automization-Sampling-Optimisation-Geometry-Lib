import GC44Projection
import GC44Rayleigh
import GC44GramUse
import Mathlib.Analysis.InnerProductSpace.Rayleigh

/-!
# Compression to a matrix indexed by Gaussian starts
The product of two q-mode cosine features is reproduced by the 2q-mode
grid projection. Thus the centered Gram operator is the compression of
a block-diagonal operator with one small block per grid point.
-/

noncomputable section
open Matrix
open scoped BigOperators Matrix.Norms.L2Operator RealInnerProductSpace
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection

abbrev Small (q : ℕ) := Matrix (Fin (q+1)) (Fin (q+1)) ℝ
def energyLift {d q : ℕ} (H : Fin d → Small q) : Matrix (Indices q) (Indices q) ℝ :=
  fun x y => (∑ i, frame d q i x.2 * frame d q i y.2 * H i x.1 y.1)/(d : ℝ)

def symbol {d q : ℕ} (H : Fin d → Small q) (i : Fin d) : Small q :=
  ∑ j, projection d (2*q) i j • H j

theorem lift_symbol {d q : ℕ} (hf : 2*(2*q)+1 < d) (H : Fin d → Small q) :
    energyLift (symbol H) = energyLift H := by
  ext a b
  simp only [energyLift,symbol,Matrix.sum_apply,Matrix.smul_apply,smul_eq_mul,Finset.mul_sum]
  congr 1
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  have hs (i : Fin d) : projection d (2*q) i j = projection d (2*q) j i :=
    congrArg (fun M : Matrix (Fin d) (Fin d) ℝ => M j i) (projection_transpose d (2*q))
  simp_rw [hs]
  calc
    _ = (∑ i, projection d (2*q) j i * (frame d q i a.2 * frame d q i b.2)) * H j a.1 b.1 := by
      rw [Finset.sum_mul]
      apply Finset.sum_congr rfl
      intro i _
      ring
    _ = _ := by rw [reproduce_product hf]

/-- Values of a coefficient array at one grid point, one value per start. -/
def evalCoeffs {d q : ℕ} (c : Indices q → ℝ) (i : Fin d) (a : Fin (q+1)) : ℝ :=
  ∑ k, c (a,k) * frame d q i k

private theorem lift_form {d q : ℕ} (H : Fin d → Small q) (c : Indices q → ℝ) :
    c ⬝ᵥ (energyLift H *ᵥ c) =
      (∑ i, evalCoeffs c i ⬝ᵥ (H i *ᵥ evalCoeffs c i))/(d : ℝ) := by
  classical
  simp only [energyLift,evalCoeffs,Matrix.mulVec,dotProduct,Fintype.sum_prod_type]
  simp only [div_eq_mul_inv, Finset.sum_mul, Finset.mul_sum]
  conv_lhs => enter [2, a, 2, k, 2, b]; rw [Finset.sum_comm]
  conv_lhs => enter [2, a, 2, k]; rw [Finset.sum_comm]
  conv_lhs => enter [2, a]; rw [Finset.sum_comm]
  rw [Finset.sum_comm]
  conv_lhs => enter [2, i, 2, a]; rw [Finset.sum_comm]
  conv_lhs => enter [2, i, 2, a, 2, b]; rw [Finset.sum_comm]
  repeat' (apply Finset.sum_congr rfl; intro _ _)
  ring

theorem lift_one {d q : ℕ} (h : 2*q+1 < d) : energyLift (d := d) (q := q) (fun _ => 1) = 1 := by
  have hd : (d : ℝ) ≠ 0 := by exact_mod_cast (show d ≠ 0 by omega)
  ext x y
  obtain ⟨a,k⟩ := x
  obtain ⟨b,l⟩ := y
  have he := congrArg (fun M : Small q => M k l) (frame_data h).1
  change (∑ i, frame d q i k * frame d q i l) = (d : ℝ) * (if k = l then 1 else 0) at he
  change (∑ i, frame d q i k * frame d q i l * (1 : Small q) a b) / (d : ℝ) =
    (1 : Matrix (Indices q) (Indices q) ℝ) (a,k) (b,l)
  rw [← Finset.sum_mul,he]
  by_cases hab : a=b <;> by_cases hkl : k=l <;> simp [Matrix.one_apply,hab,hkl,hd]

theorem norm_lift_le {d q : ℕ} (hf : 2*q+1 < d) (H : Fin d → Small q)
    {t : ℝ} (ht : 0 ≤ t) (hA : (energyLift H).IsHermitian) (hb : ∀ i, ‖H i‖ ≤ t) :
    ‖energyLift H‖ ≤ t := by
  apply opNorm_le_of_form _ hA ht
  intro c
  have hd : 0 < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have energy := lift_form (d := d) (fun _ => (1 : Small q)) c
  rw [lift_one hf,Matrix.one_mulVec] at energy
  simp only [Matrix.one_mulVec] at energy
  rw [dot_self] at energy
  rw [lift_form, abs_div, abs_of_pos hd]
  calc
    _ ≤ (∑ i : Fin d, |evalCoeffs c i ⬝ᵥ (H i *ᵥ evalCoeffs c i)|)/(d : ℝ) :=
      div_le_div_of_nonneg_right (Finset.abs_sum_le_sum_abs _ _) hd.le
    _ ≤ (∑ i : Fin d, t * (evalCoeffs c i ⬝ᵥ evalCoeffs c i))/(d : ℝ) := by
      apply div_le_div_of_nonneg_right _ hd.le
      apply Finset.sum_le_sum
      intro i _
      rw [dot_self]
      exact (quadratic_op_bound (H i) _).trans
        (mul_le_mul_of_nonneg_right (hb i) (sq_nonneg _))
    _ = _ := by rw [← Finset.mul_sum, mul_div_assoc, ← energy]

end AutoSamplingTheory.ExampleCases.GaussianComplexity.CosineProjection
