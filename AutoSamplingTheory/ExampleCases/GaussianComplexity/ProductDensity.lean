import AutoSamplingTheory.ExampleCases.GaussianComplexity.AveragedBlockLaw
import AutoSamplingTheory.ExampleCases.GaussianComplexity.MixtureDensities
import Mathlib.MeasureTheory.Measure.Haar.NormedSpace

open Matrix MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators
open AutoSamplingTheory.TechnicalLemmas.Probability.OrthogonalHaar
open AutoSamplingTheory.ExampleCases.GaussianComplexity.DeterminantFamily

/-!
# Actual product density of the averaged block Gaussian law

Zhou--Suzuki, arXiv:2610.20492v1, Appendix B.2.3 Ex70, from the actual
Eq6 law and actual single-block mixture density representatives. The literal
contiguous split preserves canonical Lebesgue volume; no isometry from the
ambient Euclidean norm to the ordinary Pi maximum norm is asserted.
The actual prior/Gaussian bind has the product density in both coordinate
spaces, with genuine L1 and mass one. The zero-dimensional residual has unit
density, implementing the source's omitted-factor convention.
Affinity tensorization Ex71, amplified TV Ex72 and the oracle lower bounds
remain separate mathematical obligations.
-/

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity
set_option autoImplicit false

theorem actual_product_density {d n : ℕ} (hn : 3 ≤ n) (hnd : n ≤ d)
    {κ : ℝ} (hκ : 4 ≤ κ) {b : ℝ} (hb : b = 1 ∨ b = -1) :
    letI : MeasurableSpace (Matrix (Fin d) (Fin d) ℝ) := borel _
    let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
      ((Equiv.sumCongr
        ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
        (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
        (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
    let split : EuclideanSpace ℝ (Fin d) →
        (Fin (d / n) → EuclideanSpace ℝ (Fin n)) × EuclideanSpace ℝ (Fin (d % n)) :=
      fun x => (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
        WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
    let ν := (2 : ℝ≥0∞) • (orthogonalHaar n).restrict
      {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = b}
    let D := (Measure.pi (fun _ : Fin (d / n) => ν)).map (blockPrecision κ)
    let γ : Matrix (Fin d) (Fin d) ℝ → Measure (EuclideanSpace ℝ (Fin d)) :=
      fun A => multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
    let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
      fun O x => Real.sqrt (singleBlockPrecision κ O).det /
        (2 * Real.pi) ^ ((n : ℝ) / 2) *
        Real.exp (-((WithLp.ofLp x) ⬝ᵥ
          (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
    let pb : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂ν
    let φ : EuclideanSpace ℝ (Fin (d % n)) → ℝ :=
      fun z => (2 * Real.pi) ^ (-((d % n : ℕ) : ℝ) / 2) * Real.exp (-‖z‖ ^ 2 / 2)
    let q : (Fin (d / n) → EuclideanSpace ℝ (Fin n)) ×
        EuclideanSpace ℝ (Fin (d % n)) → ℝ :=
      fun y => (∏ j, pb (y.1 j)) * φ y.2
    MeasurePreserving split volume volume ∧
      (∀ y, 0 ≤ q y) ∧ Measurable q ∧ Integrable q volume ∧ (∫ y, q y) = 1 ∧
      (D.bind γ).map split = volume.withDensity (fun y => ENNReal.ofReal (q y)) ∧
      D.bind γ = volume.withDensity (fun x => ENNReal.ofReal (q (split x))) ∧
      (d % n = 0 → ∀ z, φ z = 1) := by
  classical
  dsimp only
  let : MeasurableSpace (Matrix (Fin d) (Fin d) ℝ) := borel _
  let e : ((Fin n × Fin (d / n)) ⊕ Fin (d % n)) ≃ Fin d :=
    ((Equiv.sumCongr
      ((Equiv.prodComm (Fin n) (Fin (d / n))).trans finProdFinEquiv)
      (Equiv.refl (Fin (d % n)))).trans finSumFinEquiv).trans
      (finCongr (by simpa [Nat.mul_comm] using Nat.div_add_mod d n))
  let split : EuclideanSpace ℝ (Fin d) →
      (Fin (d / n) → EuclideanSpace ℝ (Fin n)) × EuclideanSpace ℝ (Fin (d % n)) :=
    fun x => (fun j => WithLp.toLp 2 (fun i => x (e (Sum.inl (i, j)))),
      WithLp.toLp 2 (fun i => x (e (Sum.inr i))))
  let ν := (2 : ℝ≥0∞) • (orthogonalHaar n).restrict
    {O : Matrix.orthogonalGroup (Fin n) ℝ | (O : Matrix (Fin n) (Fin n) ℝ).det = b}
  let D := (Measure.pi (fun _ : Fin (d / n) => ν)).map (blockPrecision κ)
  let γ : Matrix (Fin d) (Fin d) ℝ → Measure (EuclideanSpace ℝ (Fin d)) :=
    fun A => multivariateGaussian (0 : EuclideanSpace ℝ (Fin d)) A⁻¹
  let p : Matrix.orthogonalGroup (Fin n) ℝ → EuclideanSpace ℝ (Fin n) → ℝ :=
    fun O x => Real.sqrt (singleBlockPrecision κ O).det /
      (2 * Real.pi) ^ ((n : ℝ) / 2) *
      Real.exp (-((WithLp.ofLp x) ⬝ᵥ
        (singleBlockPrecision κ O *ᵥ WithLp.ofLp x)) / 2)
  let pb : EuclideanSpace ℝ (Fin n) → ℝ := fun x => ∫ O, p O x ∂ν
  let φ : EuclideanSpace ℝ (Fin (d % n)) → ℝ :=
    fun z => (2 * Real.pi) ^ (-((d % n : ℕ) : ℝ) / 2) * Real.exp (-‖z‖ ^ 2 / 2)
  let q : (Fin (d / n) → EuclideanSpace ℝ (Fin n)) ×
      EuclideanSpace ℝ (Fin (d % n)) → ℝ :=
    fun y => (∏ j, pb (y.1 j)) * φ y.2
  let : BorelSpace (Matrix (Fin d) (Fin d) ℝ) := ⟨rfl⟩
  let k := d / n
  let En := EuclideanSpace ℝ (Fin n)
  let Er := EuclideanSpace ℝ (Fin (d % n))
  let X := (Fin k → En) × Er
  let cur : (Fin n × Fin k → ℝ) ≃ᵐ (Fin k → Fin n → ℝ) :=
    { toEquiv :=
        { toFun := fun f j i => f (i,j)
          invFun := fun f ij => f ij.2 ij.1
          left_inv := fun _ => rfl
          right_inv := fun _ => rfl }
      measurable_toFun := by
        change Measurable (fun f : (Fin n × Fin k → ℝ) => fun j i => f (i,j))
        fun_prop
      measurable_invFun := by
        change Measurable (fun f : (Fin k → Fin n → ℝ) => fun ij : Fin n × Fin k => f ij.2 ij.1)
        fun_prop }
  have hcurv : MeasurePreserving cur volume volume := by
    change MeasurePreserving (fun f : (Fin n × Fin k → ℝ) => fun j i => f (i,j)) volume volume
    let L : (Fin n × Fin k → ℝ) ≃ₗ[ℝ] (Fin k → Fin n → ℝ) :=
      { toFun := fun f j i => f (i,j)
        invFun := fun f ij => f ij.2 ij.1
        left_inv := fun _ => rfl
        right_inv := fun _ => rfl
        map_add' := fun _ _ => rfl
        map_smul' := fun _ _ => rfl }
    have hLm : Measurable L := L.toContinuousLinearEquiv.continuous.measurable
    have : Measure.IsAddHaarMeasure (volume : Measure (Fin n → ℝ)) := inferInstance
    have : Measure.IsAddHaarMeasure (volume : Measure (Fin k → Fin n → ℝ)) :=
      Measure.pi.isAddHaarMeasure (fun _ : Fin k => (volume : Measure (Fin n → ℝ)))
    let : Measure.IsAddHaarMeasure
        ((volume : Measure (Fin n × Fin k → ℝ)).map L) := inferInstance
    have hc := Measure.isAddLeftInvariant_eq_smul
      ((volume : Measure (Fin n × Fin k → ℝ)).map L)
      (volume : Measure (Fin k → Fin n → ℝ))
    have hflat : (volume : Measure (Fin n × Fin k → ℝ)) (Set.Icc 0 1) = 1 := by
      simp [← Set.pi_univ_Icc, volume_pi_pi]
    have hnested : (volume : Measure (Fin k → Fin n → ℝ)) (Set.Icc 0 1) = 1 := by
      simp [← Set.pi_univ_Icc, volume_pi_pi]
    have hpre : L ⁻¹' Set.Icc 0 1 = Set.Icc 0 1 := by
      ext f
      change ((∀ j i, 0 ≤ f (i,j)) ∧ (∀ j i, f (i,j) ≤ 1)) ↔
        ((∀ ij, 0 ≤ f ij) ∧ (∀ ij, f ij ≤ 1))
      constructor
      · rintro ⟨h0,h1⟩
        exact ⟨fun ij => h0 ij.2 ij.1, fun ij => h1 ij.2 ij.1⟩
      · rintro ⟨h0,h1⟩
        exact ⟨fun j i => h0 (i,j), fun j i => h1 (i,j)⟩
    have heval := congrArg (fun M : Measure (Fin k → Fin n → ℝ) => M (Set.Icc 0 1)) hc
    rw [Measure.map_apply hLm measurableSet_Icc, hpre, hflat,
      Measure.smul_apply, hnested] at heval
    have heval' : (1 : ℝ≥0∞) =
        (((volume : Measure (Fin n × Fin k → ℝ)).map L).addHaarScalarFactor
          (volume : Measure (Fin k → Fin n → ℝ)) : ℝ≥0∞) := by
      simpa only [ENNReal.smul_def, smul_eq_mul, mul_one] using heval
    have hc1 : ((volume : Measure (Fin n × Fin k → ℝ)).map L).addHaarScalarFactor
        (volume : Measure (Fin k → Fin n → ℝ)) = 1 := ENNReal.coe_eq_one.mp heval'.symm
    have hLfun : (L : (Fin n × Fin k → ℝ) → (Fin k → Fin n → ℝ)) =
        (fun f j i => f (i,j)) := rfl
    refine ⟨hLm, ?_⟩
    rw [hc1, one_smul, hLfun] at hc
    exact hc
  let em : EuclideanSpace ℝ (Fin d) ≃ᵐ X :=
    (MeasurableEquiv.toLp 2 (Fin d → ℝ)).symm.trans <|
      (MeasurableEquiv.piCongrLeft (fun _ : Fin d => ℝ) e).symm.trans <|
      (MeasurableEquiv.sumPiEquivProdPi (fun _ => ℝ)).trans <|
      (cur.prodCongr (MeasurableEquiv.refl (Fin (d % n) → ℝ))).trans
        ((MeasurableEquiv.piCongrRight (fun _ : Fin k =>
          MeasurableEquiv.toLp 2 (Fin n → ℝ))).prodCongr
          (MeasurableEquiv.toLp 2 (Fin (d % n) → ℝ)))
  have hem : (em : EuclideanSpace ℝ (Fin d) → X) = split := rfl
  have hvol : MeasurePreserving em volume volume := by
    exact ((volume_preserving_pi (fun _ : Fin k =>
      PiLp.volume_preserving_toLp (Fin n))).prod
      (PiLp.volume_preserving_toLp (Fin (d % n)))).comp
      ((hcurv.prod (MeasurePreserving.id volume)).comp
        ((volume_measurePreserving_sumPiEquivProdPi (fun _ => ℝ)).comp
          ((volume_measurePreserving_piCongrLeft (fun _ : Fin d => ℝ) e).symm.comp
            (PiLp.volume_preserving_ofLp (Fin d)))))
  have hsplit : MeasurePreserving split volume volume := by rw [← hem]; exact hvol
  -- Actual single-block densities are supplied by the same canonical producer.
  let P := ν.bind (fun O => multivariateGaussian (0 : En) (singleBlockPrecision κ O)⁻¹)
  have hpb : (∀ x, 0 ≤ pb x) ∧ Measurable pb ∧ Integrable pb volume ∧
      (∫ x, pb x) = 1 ∧ P = volume.withDensity (fun x => ENNReal.ofReal (pb x)) := by
    have hm := MixtureDensities.actual_mixture_densities hn hκ
    rcases hm with ⟨h0,hmp,hmn,hip,hin,hp1,hn1,hdp,hdn⟩
    rcases hb with rfl | rfl
    · exact ⟨fun x => (h0 x).1, hmp, hip, hp1, hdp⟩
    · exact ⟨fun x => (h0 x).2, hmn, hin, hn1, hdn⟩
  have hEq6 := AveragedBlockLaw.actual_averaged_block_product hn hnd hκ hb
  let : IsProbabilityMeasure P := hEq6.2.2.1
  let : IsProbabilityMeasure (D.bind γ) := hEq6.2.2.2.1
  let : IsProbabilityMeasure ((volume : Measure En).withDensity
      (fun x => ENNReal.ofReal (pb x))) := hpb.2.2.2.2 ▸ inferInstance
  -- The standard residual density is valid in every finite dimension.
  have hnormal : ((Real.sqrt (2 * Real.pi))⁻¹) ^ (d % n) =
      (2 * Real.pi) ^ (-((d % n : ℕ) : ℝ) / 2) := by
    calc
      _ = 1 / (2 * Real.pi) ^ (((d % n : ℕ) : ℝ) / 2) := by
        rw [inv_pow, ← Real.rpow_natCast, Real.sqrt_eq_rpow,
          ← Real.rpow_mul (by positivity : 0 ≤ 2 * Real.pi)]
        simp only [show (2 : ℝ)⁻¹ * ((d % n : ℕ) : ℝ) =
          ((d % n : ℕ) : ℝ) / 2 by ring, one_div]
      _ = _ := by rw [neg_div, Real.rpow_neg, one_div]; positivity
  have hφd : stdGaussian Er = (volume : Measure Er).withDensity
      (fun z => ENNReal.ofReal (φ z)) := by
    simpa only [Real.sqrt_one, one_smul, Measure.map_id', mul_one,
      finrank_euclideanSpace, Fintype.card_fin, hnormal, φ, Er] using
      (AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity
        (E := Er) 1 zero_lt_one)
  have hφ0 (z : Er) : 0 ≤ φ z := by dsimp [φ]; positivity
  have hφm : Measurable φ := by dsimp [φ]; fun_prop
  have hq0 (y : X) : 0 ≤ q y :=
    mul_nonneg (Finset.prod_nonneg (fun j _ => hpb.1 (y.1 j))) (hφ0 y.2)
  have hqm : Measurable q :=
    (Finset.measurable_prod _ (fun j _ =>
      hpb.2.1.comp ((measurable_pi_apply j).comp measurable_fst))).mul
      (hφm.comp measurable_snd)
  have hblocks : Measure.pi (fun _ : Fin k => P) =
      (volume : Measure (Fin k → En)).withDensity
        (fun y => ENNReal.ofReal (∏ j, pb (y j))) := by
    rw [hpb.2.2.2.2,
      ← AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.pi_withDensity_prod
        (μ := fun _ : Fin k => (volume : Measure En))
        (f := fun _ : Fin k => fun x : En => ENNReal.ofReal (pb x))
        (fun _ : Fin k => ENNReal.measurable_ofReal.comp hpb.2.1),
      ← volume_pi]
    congr 1
    funext y
    exact (ENNReal.ofReal_prod_of_nonneg (fun j _ => hpb.1 (y j))).symm
  -- The actual Eq6 law, rather than a stipulated product law, is consumed here.
  have hdensity : (D.bind γ).map split = (volume : Measure X).withDensity
      (fun y => ENNReal.ofReal (q y)) := by
    rw [hEq6.2.2.2.2, hblocks, hφd,
      prod_withDensity (f := fun y : Fin k → En => ENNReal.ofReal (∏ j, pb (y j)))
        (g := fun z : Er => ENNReal.ofReal (φ z))
        (ENNReal.measurable_ofReal.comp
          (Finset.measurable_prod Finset.univ (fun j _ => hpb.2.1.comp (measurable_pi_apply j))))
        (ENNReal.measurable_ofReal.comp hφm)]
    apply withDensity_congr_ae
    exact Filter.Eventually.of_forall fun y =>
      (ENNReal.ofReal_mul (Finset.prod_nonneg (fun j _ => hpb.1 (y.1 j)))).symm
  have hmassNN : (∫⁻ y : X, ENNReal.ofReal (q y)) = 1 := by
    have hu := congrArg (fun M : Measure X => M Set.univ) hdensity
    simpa only [Measure.map_apply hsplit.measurable MeasurableSet.univ,
      Set.preimage_univ, measure_univ, withDensity_apply _ MeasurableSet.univ,
      Measure.restrict_univ] using hu.symm
  have hqi : Integrable q volume :=
    (lintegral_ofReal_ne_top_iff_integrable hqm.aestronglyMeasurable
      (Filter.Eventually.of_forall hq0)).mp (by rw [hmassNN]; exact ENNReal.one_ne_top)
  have hmass : (∫ y, q y) = 1 := by
    rw [integral_eq_lintegral_of_nonneg_ae (Filter.Eventually.of_forall hq0)
      hqm.aestronglyMeasurable, hmassNN]
    simp
  -- Volume transport gives the density on the original ambient Euclidean space.
  have hback : ((volume : Measure (EuclideanSpace ℝ (Fin d))).withDensity
      (fun x => ENNReal.ofReal (q (em x)))).map em =
      (volume : Measure X).withDensity (fun y => ENNReal.ofReal (q y)) := by
    rw [AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.measurableEquiv_map_withDensity em volume
        (f := fun x : EuclideanSpace ℝ (Fin d) => ENNReal.ofReal (q (em x)))
        (ENNReal.measurable_ofReal.comp (hqm.comp em.measurable)), hvol.map_eq]
    congr 1
    funext y
    simp only [em.apply_symm_apply]
  have hambient : D.bind γ = volume.withDensity
      (fun x => ENNReal.ofReal (q (split x))) := by
    apply em.measurableEmbedding.map_injective
    rw [hem] at hback ⊢
    exact hdensity.trans hback.symm
  have hunit (hr : d % n = 0) (z : Er) : φ z = 1 := by
    let : IsEmpty (Fin (d % n)) := ⟨fun i => (Nat.not_lt_zero i.val) (hr ▸ i.isLt)⟩
    have hz : z = 0 := Subsingleton.elim _ _
    simp only [φ, hz, norm_zero, ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true,
      zero_pow, neg_zero, zero_div, Real.exp_zero, mul_one, hr, Nat.cast_zero,
      Real.rpow_zero]
  exact ⟨hsplit, hq0, hqm, hqi, hmass, hdensity, hambient, hunit⟩

end AutoSamplingTheory.ExampleCases.GaussianComplexity.ProductDensity
