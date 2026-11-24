import GC44GramUse
import Mathlib.LinearAlgebra.Vandermonde

/-! A maximal nonzero minor for a block Krylov matrix with distinct nodes. -/
noncomputable section
open Matrix
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

def minorSize (d q : ℕ) : ℕ := min d ((q+1)^2)

def minorRow (d q : ℕ) (n : Fin (minorSize d q)) : Fin d :=
  ⟨n.val, n.isLt.trans_le (min_le_left _ _)⟩

def minorColumn (d q : ℕ) (n : Fin (minorSize d q)) : Indices q :=
  (⟨n.val / (q+1), (Nat.div_lt_iff_lt_mul (by omega : 0 < q+1)).2
    (by simpa [pow_two] using n.isLt.trans_le (min_le_right _ _))⟩,
   ⟨n.val % (q+1), Nat.mod_lt _ (by omega)⟩)

def monomialMatrix {d q : ℕ} (node : Fin d → ℝ) (g : Starts d q) :
    Matrix (Fin d) (Indices q) ℝ :=
  fun i j => node i ^ j.2.val * g j.1 i

def minorDet {d q : ℕ} (node : Fin d → ℝ) (g : Starts d q) : ℝ :=
  ((monomialMatrix node g).submatrix (minorRow d q) (minorColumn d q)).det

/-- The successive start vectors pick consecutive blocks of powers of the nodes. -/
def monomialWitness {d : ℕ} (q : ℕ) (node : Fin d → ℝ) : Starts d q :=
  fun a => WithLp.toLp 2 (fun i => node i ^ ((q+1)*a.val))

theorem minor_witness_eq_vandermonde {d : ℕ} (q : ℕ) (node : Fin d → ℝ) :
    (monomialMatrix node (monomialWitness q node)).submatrix (minorRow d q) (minorColumn d q) =
      vandermonde (node ∘ minorRow d q) := by
  ext i j
  change node (minorRow d q i) ^ (j.val % (q+1)) *
    node (minorRow d q i) ^ ((q+1) * (j.val / (q+1))) = node (minorRow d q i) ^ j.val
  rw [← pow_add, Nat.mod_add_div]

theorem witness_minor_ne_zero {d q : ℕ} (node : Fin d → ℝ) (hnodes : Function.Injective node) :
    minorDet node (monomialWitness q node) ≠ 0 := by
  rw [minorDet, minor_witness_eq_vandermonde, det_vandermonde_ne_zero_iff]
  exact hnodes.comp (fun _ _ h => Fin.ext (congrArg (fun i : Fin d => i.val) h))

#print axioms witness_minor_ne_zero
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
