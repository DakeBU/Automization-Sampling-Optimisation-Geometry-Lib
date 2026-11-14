import AutoSamplingTheory.ExampleCases.GaussianComplexity.BlockFamily
import Mathlib.Probability.Distributions.Gaussian.Multivariate

/-!
# The actual conditional block Gaussian law

Zhou--Suzuki, arXiv:2610.20492v1, Section 3.1 Eq4--Eq6 and the
regularity producer in Appendix B.3. This supplies the implicit fixed-tuple
Gaussian product-law ingredient. The source prints the prior-averaged Eq6;
its actual averaging, density, tensorization and amplification remain separate.
-/

open Matrix MeasureTheory ProbabilityTheory
open scoped RealInnerProductSpace
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianBlockLaw
set_option autoImplicit false

theorem actual_conditional_block_product {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ)
    (O : Fin (d / n) → Matrix.orthogonalGroup (Fin n) ℝ) :
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let split : EuclideanSpace ℝ (Fin d) →
        (Fin (d / n) → EuclideanSpace ℝ (Fin n)) × EuclideanSpace ℝ (Fin (d % n)) :=
      fun x => (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
        WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
    (multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) (blockPrecision κ O)⁻¹).map split =
      (Measure.pi (fun j => multivariateGaussian (0 : EuclideanSpace ℝ (Fin n))
        (singleBlockPrecision κ (O j))⁻¹)).prod
          (stdGaussian (EuclideanSpace ℝ (Fin (d % n)))) := by
  classical
  dsimp only
  let E := EuclideanSpace ℝ (Fin d)
  let En := EuclideanSpace ℝ (Fin n)
  let Er := EuclideanSpace ℝ (Fin (d % n))
  let F := (Fin (d / n) → En) × Er
  let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
    ((Equiv.sumCongr
      ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
      (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
      (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
  let B := Matrix.fromBlocks (Matrix.blockDiagonal (fun j => singleBlockPrecision κ (O j)))
    0 0 (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ)
  let C := Matrix.fromBlocks
    (Matrix.blockDiagonal (fun j => (singleBlockPrecision κ (O j))⁻¹))
    0 0 (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ)
  have hp (j : Fin (d / n)) : (singleBlockPrecision κ (O j)).PosDef := by
    have hr := singleBlockPrecision_regular hn hκ (O j)
    apply Matrix.posDef_iff_dotProduct_mulVec.mpr
    refine ⟨hr.1, fun v hv => ?_⟩
    have hdot : 0 < v ⬝ᵥ v := by
      simpa only [star_trivial] using (dotProduct_star_self_pos_iff.mpr hv)
    simpa only [star_trivial] using lt_of_lt_of_le hdot (hr.2 v).1
  have hBC : B * C = 1 := by
    dsimp only [B, C]
    rw [Matrix.fromBlocks_multiply, ← Matrix.blockDiagonal_mul]
    simp only [Matrix.mul_zero, Matrix.zero_mul, add_zero, zero_add, Matrix.mul_one]
    have hmul : (fun j => singleBlockPrecision κ (O j) *
        (singleBlockPrecision κ (O j))⁻¹) = 1 := by
      funext j
      exact Matrix.mul_nonsing_inv _ ((Matrix.isUnit_iff_isUnit_det _).mp (hp j).isUnit)
    rw [hmul, Matrix.blockDiagonal_one]
    exact Matrix.fromBlocks_one
  have hAdef : blockPrecision κ O = Matrix.reindex e e B := rfl
  have hInv : (blockPrecision κ O)⁻¹ = Matrix.reindex e e C := by
    rw [hAdef, Matrix.inv_reindex, Matrix.inv_eq_right_inv hBC]
  have hpd : (blockPrecision κ O).PosDef := by
    have hr := blockPrecision_regular hn hnd hκ O
    apply Matrix.posDef_iff_dotProduct_mulVec.mpr
    refine ⟨hr.1, fun v hv => ?_⟩
    have hdot : 0 < v ⬝ᵥ v := by
      simpa only [star_trivial] using (dotProduct_star_self_pos_iff.mpr hv)
    simpa only [star_trivial] using lt_of_lt_of_le hdot (hr.2 v).1
  let split : E → F := fun x =>
    (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
      WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
  let Tlin : E →ₗ[ℝ] F :=
    { toFun := split
      map_add' := by intro x y; ext i j <;> rfl
      map_smul' := by intro a x; ext i j <;> rfl }
  let T : E →L[ℝ] F := Tlin.toContinuousLinearMap
  let μ := multivariateGaussian (0 : E) (blockPrecision κ O)⁻¹
  let νj (j : Fin (d / n)) := multivariateGaussian (0 : En)
    (singleBlockPrecision κ (O j))⁻¹
  let νr := multivariateGaussian (0 : Er)
    (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ)
  change μ.map split = (Measure.pi νj).prod (stdGaussian Er)
  rw [← multivariateGaussian_zero_one (ι := Fin (d % n))]
  change μ.map T = (Measure.pi νj).prod νr
  apply Measure.ext_of_charFunDual
  funext L
  rw [charFunDual_map, charFunDual_prod, charFunDual_pi]
  let Lb := L.comp (ContinuousLinearMap.inl ℝ (Fin (d / n) → En) Er)
  let Lj (j : Fin (d / n)) :=
    Lb.comp (ContinuousLinearMap.single ℝ (fun _ : Fin (d / n) => En) j)
  let Lr := L.comp (ContinuousLinearMap.inr ℝ (Fin (d / n) → En) Er)
  let vj (j : Fin (d / n)) : En := (InnerProductSpace.toDual ℝ En).symm (Lj j)
  let vr : Er := (InnerProductSpace.toDual ℝ Er).symm Lr
  let w : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) → ℝ :=
    Sum.elim (fun ij => vj ij.2 ij.1) (fun i => vr i)
  let v : E := WithLp.toLp 2 (fun i => w (e.symm i))
  have heval (i) : v (e i) = w i := by simp [v]
  have hinner (x : E) :
      ⟪v, x⟫ = (∑ j, ⟪vj j, (split x).1 j⟫) + ⟪vr, (split x).2⟫ := by
    change (∑ i : Fin d, x i * v i) =
      (∑ j, ∑ i : Fin n, (split x).1 j i * vj j i) +
        ∑ i : Fin (d % n), (split x).2 i * vr i
    rw [← e.sum_comp (fun i => x i * v i)]
    simp only [heval, Fintype.sum_sum_type, Fintype.sum_prod_type, w,
      Sum.elim_inl, Sum.elim_inr]
    dsimp only [split]
    congr 1
    exact Finset.sum_comm
  have hvfunctional : L.comp T = InnerProductSpace.toDual ℝ E v := by
    ext x
    change L (split x) = ⟪v, x⟫
    rw [hinner]
    simp_rw [vj, vr, InnerProductSpace.toDual_symm_apply]
    rw [show (∑ j, (Lj j) ((split x).1 j)) = Lb (split x).1 from
      ContinuousLinearMap.sum_comp_single ℝ _ Lb (split x).1]
    exact (L.comp_inl_add_comp_inr (split x)).symm
  have hvec (z : Fin n × Fin (d / n) → ℝ) (i : Fin n) (j : Fin (d / n)) :
      (Matrix.blockDiagonal (fun j => (singleBlockPrecision κ (O j))⁻¹) *ᵥ z) (i, j) =
        ((singleBlockPrecision κ (O j))⁻¹ *ᵥ (fun a => z (a, j))) i := by
    simp [Matrix.mulVec, dotProduct, Fintype.sum_prod_type, Matrix.blockDiagonal_apply,
      ite_mul]
  have hchange (M : Matrix ((Fin n × Fin (d / n)) ⊕ Fin (d % n))
      ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ℝ) :
      WithLp.ofLp v ⬝ᵥ (Matrix.reindex e e M *ᵥ WithLp.ofLp v) =
        (WithLp.ofLp v ∘ e) ⬝ᵥ (M *ᵥ (WithLp.ofLp v ∘ e)) := by
    change WithLp.ofLp v ⬝ᵥ (M.submatrix e.symm e.symm *ᵥ WithLp.ofLp v) = _
    rw [Matrix.submatrix_mulVec_equiv]
    exact dotProduct_comp_equiv_symm _ _ e
  have hy : WithLp.ofLp v ∘ e = w := by
    funext i
    exact heval i
  have hquad : WithLp.ofLp v ⬝ᵥ ((blockPrecision κ O)⁻¹ *ᵥ WithLp.ofLp v) =
      (∑ j, WithLp.ofLp (vj j) ⬝ᵥ
        ((singleBlockPrecision κ (O j))⁻¹ *ᵥ WithLp.ofLp (vj j))) +
          WithLp.ofLp vr ⬝ᵥ WithLp.ofLp vr := by
    rw [hInv, hchange, hy]
    simp only [C, Matrix.fromBlocks_mulVec, Matrix.zero_mulVec, Matrix.one_mulVec,
      add_zero, zero_add]
    rw [Matrix.dotProduct_block]
    congr 1
    simp only [dotProduct, Fintype.sum_prod_type, Function.comp_apply, w,
      Sum.elim_inl, hvec]
    exact Finset.sum_comm
  have hG {m : ℕ} (S : Matrix (Fin m) (Fin m) ℝ) (hS : S.PosSemidef)
      (K : EuclideanSpace ℝ (Fin m) →L[ℝ] ℝ) :
      charFunDual (multivariateGaussian (0 : EuclideanSpace ℝ (Fin m)) S) K =
        Complex.exp (-((WithLp.ofLp ((InnerProductSpace.toDual ℝ
          (EuclideanSpace ℝ (Fin m))).symm K) ⬝ᵥ (S *ᵥ
          WithLp.ofLp ((InnerProductSpace.toDual ℝ
            (EuclideanSpace ℝ (Fin m))).symm K)) : ℝ) : ℂ) / 2) := by
    rw [← charFun_toDual_symm_eq_charFunDual, charFun_multivariateGaussian hS]
    simp [neg_div]
  have hw : (InnerProductSpace.toDual ℝ E).symm (L.comp T) = v := by
    rw [hvfunctional]
    exact (InnerProductSpace.toDual ℝ E).symm_apply_apply v
  have hb (j : Fin (d / n)) : charFunDual (νj j) (Lj j) =
      Complex.exp (-((WithLp.ofLp (vj j) ⬝ᵥ
        ((singleBlockPrecision κ (O j))⁻¹ *ᵥ WithLp.ofLp (vj j)) : ℝ) : ℂ) / 2) :=
    hG _ (hp j).inv.posSemidef (Lj j)
  have hr : charFunDual νr Lr =
      Complex.exp (-((WithLp.ofLp vr ⬝ᵥ WithLp.ofLp vr : ℝ) : ℂ) / 2) := by
    simpa only [Matrix.one_mulVec] using
      hG (1 : Matrix (Fin (d % n)) (Fin (d % n)) ℝ) Matrix.PosSemidef.one Lr
  change charFunDual μ (L.comp T) = (∏ j, charFunDual (νj j) (Lj j)) * charFunDual νr Lr
  rw [hG _ hpd.inv.posSemidef (L.comp T), hw, hr]
  simp_rw [hb]
  rw [← Complex.exp_sum, ← Complex.exp_add]
  congr 1
  rw [hquad]
  push_cast
  simp only [← Finset.sum_div, Finset.sum_neg_distrib]
  ring

end AutoSamplingTheory.ExampleCases.GaussianComplexity.GaussianBlockLaw
