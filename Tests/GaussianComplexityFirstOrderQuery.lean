import AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery
import Lean.Util.FoldConsts
open Matrix InnerProductSpace
open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity
set_option autoImplicit false

-- Actual two-input observational-equivalence consumer for any actual queried x.
-- Both hidden tuples and all primitive answers are the real source objects.
-- This is one-query math, with no adaptive/cap/TV/expected-cost claim.
example {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d) {κ : ℝ} (hκ : 4 ≤ κ)
    (Os1 Os2 : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ) :
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let A1 := blockPrecision κ Os1
    let A2 := blockPrecision κ Os2
    let f1 : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      (WithLp.ofLp x) ⬝ᵥ (A1 *ᵥ WithLp.ofLp x) / 2
    let f2 : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
      (WithLp.ofLp x) ⬝ᵥ (A2 *ᵥ WithLp.ofLp x) / 2
    let query1 : Fin (d / n) → EuclideanSpace ℝ (Fin n) → Bool →
        EuclideanSpace ℝ (Fin n) := fun j v inverse =>
      WithLp.toLp 2 (if inverse then
        (Os1 j : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp v
      else (Os1 j : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp v)
    let query2 : Fin (d / n) → EuclideanSpace ℝ (Fin n) → Bool →
        EuclideanSpace ℝ (Fin n) := fun j v inverse =>
      WithLp.toLp 2 (if inverse then
        (Os2 j : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp v
      else (Os2 j : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp v)
    let xb : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
        EuclideanSpace ℝ (Fin n) := fun x j =>
      WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j))))
    ∀ x : EuclideanSpace ℝ (Fin d),
      (∀ j inverse, query1 j (xb x j) inverse = query2 j (xb x j) inverse) →
      (f1 x, gradient f1 x) = (f2 x, gradient f2 x) := by
  classical
  dsimp only
  let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
    ((Equiv.sumCongr
      ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
      (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
      (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
  let A1 := blockPrecision κ Os1
  let A2 := blockPrecision κ Os2
  let f1 : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A1 *ᵥ WithLp.ofLp x) / 2
  let f2 : EuclideanSpace ℝ (Fin d) → ℝ := fun x =>
    (WithLp.ofLp x) ⬝ᵥ (A2 *ᵥ WithLp.ofLp x) / 2
  let query1 : Fin (d / n) → EuclideanSpace ℝ (Fin n) → Bool →
      EuclideanSpace ℝ (Fin n) := fun j v inverse =>
    WithLp.toLp 2 (if inverse then
      (Os1 j : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp v
    else (Os1 j : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp v)
  let query2 : Fin (d / n) → EuclideanSpace ℝ (Fin n) → Bool →
      EuclideanSpace ℝ (Fin n) := fun j v inverse =>
    WithLp.toLp 2 (if inverse then
      (Os2 j : Matrix (Fin n) (Fin n) ℝ).transpose *ᵥ WithLp.ofLp v
    else (Os2 j : Matrix (Fin n) (Fin n) ℝ) *ᵥ WithLp.ofLp v)
  let xb : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
      EuclideanSpace ℝ (Fin n) := fun x j =>
    WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j))))
  let gb1 : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
      EuclideanSpace ℝ (Fin n) := fun x j =>
    ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) •
      (query1 j (xb x j) false + query1 j (xb x j) true)
  let gb2 : EuclideanSpace ℝ (Fin d) → Fin (d / n) →
      EuclideanSpace ℝ (Fin n) := fun x j =>
    ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) •
      (query2 j (xb x j) false + query2 j (xb x j) true)
  let g1 : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) := fun x =>
    WithLp.toLp 2 (fun a => Sum.elim
      (fun ij => gb1 x ij.2 ij.1)
      (fun i => x (e (Sum.inr i))) (e.symm a))
  let g2 : EuclideanSpace ℝ (Fin d) → EuclideanSpace ℝ (Fin d) := fun x =>
    WithLp.toLp 2 (fun a => Sum.elim
      (fun ij => gb2 x ij.2 ij.1)
      (fun i => x (e (Sum.inr i))) (e.symm a))
  intro x hObs
  have h1 := FirstOrderQuery.actual_first_order_query hn hnd hκ Os1
  have h2 := FirstOrderQuery.actual_first_order_query hn hnd hκ Os2
  dsimp only at h1 h2
  have r1 : (f1 x, gradient f1 x) = (inner ℝ x (g1 x) / 2, g1 x) := (h1 x).2
  have r2 : (f2 x, gradient f2 x) = (inner ℝ x (g2 x) / 2, g2 x) := (h2 x).2
  have hb (j : Fin (d / n)) : gb1 x j = gb2 x j := by
    change ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) •
      (query1 j (xb x j) false + query1 j (xb x j) true) =
      ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) •
      (query2 j (xb x j) false + query2 j (xb x j) true)
    exact congrArg (fun y : EuclideanSpace ℝ (Fin n) =>
      ((κ + 1) / 2) • xb x j - ((κ - 1) / 4) • y)
      (congrArg₂ (fun u v : EuclideanSpace ℝ (Fin n) => u + v)
        (hObs j false) (hObs j true))
  have hg : g1 x = g2 x := by
    simp only [g1, g2, hb]
  exact r1.trans ((congrArg (fun y : EuclideanSpace ℝ (Fin d) =>
    (inner ℝ x y / 2, y)) hg).trans r2.symm)

#print axioms FirstOrderQuery.actual_first_order_query
open Lean in
run_cmd do
  let env ← getEnv
  let some info := env.find? `AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery.actual_first_order_query | throwError "Missing actual source query theorem"
  let some proof := info.value? (allowOpaque := true) | throwError "Missing actual query proof"
  let parents := proof.getUsedConstants.filter fun n => n.toString.startsWith "AutoSamplingTheory"
  logInfo m!"ACTUAL COMPILED SOURCE PARENTS {parents}"
