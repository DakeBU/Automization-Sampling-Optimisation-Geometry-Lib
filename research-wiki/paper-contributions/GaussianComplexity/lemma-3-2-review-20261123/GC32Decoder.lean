import B4Protocol
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery
import Mathlib.Data.List.FinRange

/-!
# Primitive query batch for the actual determinant hard family

Zhou–Suzuki, arXiv:2610.20492v1, Appendix B.1, equations Ex33–Ex35.
A query in the ambient Euclidean space generates one forward and one transpose
query per full block. A sign-independent Borel decoder returns the potential
value and genuine gradient of the canonical precision matrix. On the final
identity coordinates it copies the input vector.
-/

open Matrix MeasureTheory InnerProductSpace
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderQuery
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarFrames
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior

/-- Consecutive matrix blocks followed by the residual identity coordinates. -/
def decoderCoordinates (d n : ℕ) :
    ((Fin n × Fin (d/n)) ⊕ Fin (d%n)) ≃ Fin d :=
  ((Equiv.sumCongr ((Equiv.prodComm (Fin n) (Fin (d/n))).trans finProdFinEquiv)
    (Equiv.refl (Fin (d%n)))).trans finSumFinEquiv).trans
      (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))

def blockInput (d n : ℕ) (x : E d) (j : Fin (d/n)) : Vec n :=
  fun v => x (decoderCoordinates d n (Sum.inl (v,j)))

def batchLabel (k : ℕ) : Fin (k+k) → Fin k := Fin.addCases id id

/-- Read the forward image on every label, then the transpose image on every label. -/
def batchPlan (d n : ℕ) (x : E d) : Fin (d/n+d/n) → Query (d/n) n :=
  Fin.addCases (fun j => (j, blockInput d n x j, false))
    (fun j => (j, blockInput d n x j, true))

theorem batchPlan_label (d n : ℕ) (x : E d) (s : Fin (d/n+d/n)) :
    (batchPlan d n x s).1 = batchLabel (d/n) s := by
  cases s using Fin.addCases <;> simp only [batchPlan, batchLabel, Fin.addCases_left, Fin.addCases_right, id_eq]

theorem count_batchLabel (k : ℕ) (j : Fin k) :
    (List.ofFn (batchLabel k)).countP (fun v => decide (v = j)) = 2 := by
  have h : List.ofFn (batchLabel k) = List.finRange k ++ List.finRange k := by
    rw [List.ofFn_add]
    have hleft : (fun i : Fin k => batchLabel k (i.castLE (Nat.le_add_right k k))) = id := by
      funext i
      exact Fin.addCases_left i
    have hright : (fun i : Fin k => batchLabel k (i.natAdd k)) = id := by
      funext i
      exact Fin.addCases_right i
    rw [hleft, hright, List.ofFn_id]
  rw [h, List.countP_append]
  have one : (List.finRange k).countP (fun v => decide (v = j)) = 1 := by
    simpa only [List.count_eq_countP, Bool.beq_eq_decide_eq] using List.count_finRange j
  rw [one]

private theorem continuous_blockInput {d n : ℕ} (j : Fin (d/n)) :
    Continuous (fun x : E d => blockInput d n x j) := by
  apply continuous_pi
  intro v
  exact (continuous_apply _).comp (PiLp.continuous_ofLp 2 (fun _ : Fin d => ℝ))

theorem measurable_batchPlan (d n : ℕ) (s : Fin (d/n+d/n)) :
    Measurable (fun x => batchPlan d n x s) := by
  cases s using Fin.addCases with
  | left j =>
    simp only [batchPlan, Fin.addCases_left]
    exact measurable_const.prodMk ((continuous_blockInput j).measurable.prodMk measurable_const)
  | right j =>
    simp only [batchPlan, Fin.addCases_right]
    exact measurable_const.prodMk ((continuous_blockInput j).measurable.prodMk measurable_const)

noncomputable def decodedGradient (d n : ℕ) (κ : ℝ) (x : E d)
    (answers : Fin (d/n+d/n) → Vec n) : E d :=
  let k := d/n
  let g := fun j : Fin k =>
    ((κ+1)/2) • WithLp.toLp 2 (blockInput d n x j) -
      ((κ-1)/4) • (WithLp.toLp 2 (answers (Fin.castAdd k j)) + WithLp.toLp 2 (answers (Fin.natAdd k j)))
  WithLp.toLp 2 (fun a => Sum.elim (fun ij => g ij.2 ij.1)
    (fun i => x (decoderCoordinates d n (Sum.inr i))) ((decoderCoordinates d n).symm a))

noncomputable def batchDecode (d n : ℕ) (κ : ℝ) (x : E d) (a : Fin (d/n+d/n) → Vec n) :
    ℝ × E d :=
  let g := decodedGradient d n κ x a
  (inner ℝ x g / 2, g)

/-- Value and actual gradient of the hard precision for this tuple. -/
noncomputable def actualReply {d n : ℕ} (κ : ℝ) (W : Fin (d/n) → O n) (x : E d) : ℝ × E d :=
  let A := blockPrecision κ W
  let f := fun y : E d => WithLp.ofLp y ⬝ᵥ (A *ᵥ WithLp.ofLp y) / 2
  (f x, gradient f x)

theorem batchDecode_oracleAnswer {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) (W : Fin (d/n) → O n) (x : E d) :
    batchDecode d n κ x (fun s => oracleAnswer W (batchPlan d n x s)) = actualReply κ W x := by
  have h := (actual_first_order_query hn hnd hκ W x).2.symm
  unfold batchDecode decodedGradient
  simp only [batchPlan, Fin.addCases_left, Fin.addCases_right]
  exact h

theorem measurable_batchDecode (d n : ℕ) (κ : ℝ) :
    Measurable (fun p : E d × (Fin (d/n+d/n) → Vec n) => batchDecode d n κ p.1 p.2) := by
  have hgrad : Continuous (fun p : E d × (Fin (d/n+d/n) → Vec n) =>
      decodedGradient d n κ p.1 p.2) := by
    apply (PiLp.continuous_toLp 2 (fun _ : Fin d => ℝ)).comp
    apply continuous_pi
    intro a
    generalize (decoderCoordinates d n).symm a = pos
    cases pos with
    | inr i =>
      exact (continuous_apply _).comp ((PiLp.continuous_ofLp 2 (fun _ : Fin d => ℝ)).comp continuous_fst)
    | inl ij =>
      change Continuous (fun p : E d × (Fin (d/n+d/n) → Vec n) =>
        ((κ+1)/2) * blockInput d n p.1 ij.2 ij.1 - ((κ-1)/4) *
        (p.2 (Fin.castAdd (d/n) ij.2) ij.1 + p.2 (Fin.natAdd (d/n) ij.2) ij.1))
      have hx := (continuous_apply ij.1).comp ((continuous_blockInput ij.2).comp
        (continuous_fst (X := E d) (Y := (Fin (d/n+d/n) → Vec n))))
      have hv (s : Fin (d/n+d/n)) : Continuous (fun p : E d × (Fin (d/n+d/n) → Vec n) =>
          p.2 s ij.1) := (continuous_apply ij.1).comp ((continuous_apply s).comp continuous_snd)
      exact (continuous_const.mul hx).sub (continuous_const.mul ((hv _).add (hv _)))
  exact (((continuous_fst.inner hgrad).div_const 2).prodMk hgrad).measurable

/-- The precision-response map used to average the algorithm law on matrices. -/
noncomputable def precisionReply {d : ℕ} (A : Matrix (Fin d) (Fin d) ℝ) (x : E d) : ℝ × E d :=
  let g := WithLp.toLp 2 (A *ᵥ WithLp.ofLp x)
  (inner ℝ x g / 2, g)

theorem continuous_precisionReply (d : ℕ) :
    Continuous (Function.uncurry (@precisionReply d)) := by
  have hg : Continuous (fun p : Matrix (Fin d) (Fin d) ℝ × E d =>
      WithLp.toLp 2 (p.1 *ᵥ WithLp.ofLp p.2)) :=
    (PiLp.continuous_toLp 2 _).comp (continuous_fst.matrix_mulVec
      ((PiLp.continuous_ofLp 2 _).comp continuous_snd))
  exact (((continuous_snd.inner hg).div_const 2).prodMk hg)

theorem continuous_blockPrecision (d n : ℕ) (κ : ℝ) :
    Continuous (fun W : Fin (d/n) → O n => blockPrecision κ W) := by
  unfold blockPrecision singleBlockPrecision
  fun_prop

/-- For the symmetric hard precision, matrix multiplication is the genuine
gradient of the quadratic, and its potential value is the accompanying scalar. -/
theorem precisionReply_eq_actualReply {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) (W : Fin (d/n) → O n) (x : E d) :
    precisionReply (blockPrecision κ W) x = actualReply κ W x := by
  let A := blockPrecision κ W
  let L : E d →L[ℝ] E d := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d) A
  have hself : IsSelfAdjoint A := (blockPrecision_regular hn hnd hκ W).1
  have hs : L.IsSymmetric :=
    ContinuousLinearMap.isSelfAdjoint_iff_isSymmetric.mp (hself.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)))
  let f := fun y : E d => WithLp.ofLp y ⬝ᵥ (A *ᵥ WithLp.ofLp y) / 2
  have hf : f = fun y => (1 / 2 : ℝ) * inner ℝ y (L y) := by
    funext y
    rw [show inner ℝ y (L y) = _ from Matrix.inner_toEuclideanCLM A y y]
    unfold f
    ring
  have hgrad : HasGradientAt f (L x) x := by
    have hraw := ((hasFDerivAt_id x).inner ℝ L.hasFDerivAt).const_mul (1 / 2 : ℝ)
    have hlin : (1 / 2 : ℝ) •
        ((fderivInnerCLM ℝ (x, L x)).comp ((ContinuousLinearMap.id ℝ (E d)).prod L)) =
        toDual ℝ (E d) (L x) := by
      ext v
      change (1 / 2 : ℝ) * (inner ℝ x (L v) + inner ℝ v (L x)) = inner ℝ (L x) v
      rw [← hs.apply_clm x v, (real_inner_comm v (L x)).symm]
      ring
    apply hasGradientAt_iff_hasFDerivAt.mpr
    rw [hf, ← hlin]
    exact hraw
  change (inner ℝ x (L x) / 2, L x) = (f x, gradient f x)
  exact Prod.ext (congrArg (fun a : ℝ => a / 2) (Matrix.inner_toEuclideanCLM A x x)) hgrad.gradient.symm

theorem batchDecode_precisionReply {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) (W : Fin (d/n) → O n) (x : E d) :
    batchDecode d n κ x (fun s => oracleAnswer W (batchPlan d n x s)) =
      precisionReply (blockPrecision κ W) x :=
  (batchDecode_oracleAnswer hn hnd hκ W x).trans (precisionReply_eq_actualReply hn hnd hκ W x).symm

#print axioms batchDecode_precisionReply
#print axioms batchDecode_oracleAnswer
#print axioms measurable_batchDecode
end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
