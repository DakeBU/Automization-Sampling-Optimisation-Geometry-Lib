import AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery
import Lean.Util.FoldConsts
open Matrix InnerProductSpace
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity
set_option autoImplicit false

-- Exact supplied expansion, with every source-facing project definition expanded.
example :
∀ {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ)
    (Os : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ),
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let B : Fin (d / n) → Matrix (Fin n) (Fin n) ℝ := fun j =>
      ((κ + 1) / 2) • (1 : Matrix (Fin n) (Fin n) ℝ) -
        ((κ - 1) / 4) • ((Os j : Matrix (Fin n) (Fin n) ℝ) +
          (Os j : Matrix (Fin n) (Fin n) ℝ).transpose)
    let A := Matrix.reindex e e
      (Matrix.fromBlocks (Matrix.blockDiagonal B) 0 0
        (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ))
    let f : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) / 2
    let query : Fin (d / n) → EuclideanSpace ℝ (Fin n) → Bool →
        EuclideanSpace ℝ (Fin n) := fun j v inverse =>
      WithLp.toLp 2 (if inverse then
        (Os j : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp v
      else (Os j : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp v)
    let xb : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
        EuclideanSpace ℝ (Fin n) := fun x j =>
      WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j))))
    let gb : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
        EuclideanSpace ℝ (Fin n) := fun x j =>
      ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) •
        (query j (xb x j) false + query j (xb x j) true)
    let g : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) := fun x =>
      WithLp.toLp 2 (fun a => Sum.elim
        (fun ij => gb x ij.2 ij.1)
        (fun i => x (e (Sum.inr i))) (e.symm a))
    ∀ x : EuclideanSpace ℝ (Fin d),
      HasGradientAt f (g x) x ∧
      (f x, gradient f x) = (inner ℝ x (g x) / 2, g x) := by
  exact FirstOrderQuery.actual_first_order_query

-- Symbolically inspect genuine derivative definitions, literal source matrix definitions,
-- approved coordinate and oracle meanings, and compiler proof constants/axioms.
#print AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily.singleBlockPrecision
#print AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily.blockPrecision
#print HasGradientAt
#print gradient
#print Matrix.blockDiagonal
#print Matrix.reindex
#print finProdFinEquiv
#print finSumFinEquiv
#print axioms FirstOrderQuery.actual_first_order_query
#print axioms blockPrecision_regular
#print axioms singleBlockPrecision_regular
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery.actual_first_order_query | throwError "target absent"
  let some proof := info.value? (allowOpaque := true) | throwError "proof absent"
  let parents := proof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  logInfo m!"INDEPENDENT COMPILED SOURCE PARENTS {parents}"
