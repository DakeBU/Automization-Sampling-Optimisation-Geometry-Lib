import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Isometric
import Mathlib.Tactic.NoncommRing

noncomputable section
open MeasureTheory ProbabilityTheory
open scoped BigOperators Matrix.Norms.L2Operator MatrixOrder
open AutoSamplingTheory.ExampleCases.GaussianComplexity
open AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral
set_option autoImplicit false

namespace AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance

private theorem actual_source_centered_variance_bounds
    {d q : ℕ} (hq : 2 * q + 1 < d) :
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  (∀ i : Fin d, Integrable (fun ω => Z i ω * Z i ω) μ) ∧
    (∀ i : Fin d, Integrable (fun ω => (w i • Z i ω) * (w i • Z i ω)) μ) ∧
    ‖∑ i : Fin d, ∫ ω, Z i ω * Z i ω ∂μ‖ ≤ C ∧
    ‖∑ i : Fin d, ∫ ω, (w i • Z i ω) * (w i • Z i ω) ∂μ‖ ≤ C
 := by
  classical
  dsimp only
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)

  let N := Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ
  have raw := FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments hq
  change (∀ i : Fin d, Integrable (fun ω => Y i ω * Y i ω) μ) ∧
    (C • (1 : N) - ∑ i : Fin d, ∫ ω, Y i ω * Y i ω ∂μ).PosSemidef at raw
  have first := FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means hq
  have Y_integrable (i : Fin d) : Integrable (Y i) μ := first.1 i
  have Y_positive (i : Fin d) (ω : Ω) : (Y i ω).PosSemidef := by
    by_cases hc : ‖row i ω‖ ^ 2 ≤ L
    · let v : Fin (q + 1) × Fin (q + 1) → ℝ := fun a => row i ω a.1 * t i a.2
      have rank_positive : (Matrix.vecMulVec v v).PosSemidef := by
        simpa only [star_trivial] using Matrix.posSemidef_vecMulVec_self_star v
      have rank_eq : Y i ω = (d : ℝ)⁻¹ • Matrix.vecMulVec v v := by
        simp only [Y, if_pos hc]
        ext a b
        change (d : ℝ)⁻¹ * ((row i ω a.1 * row i ω b.1) * (t i a.2 * t i b.2)) =
          (d : ℝ)⁻¹ * ((row i ω a.1 * t i a.2) * (row i ω b.1 * t i b.2))
        ring
      rw [rank_eq]
      exact rank_positive.smul (inv_nonneg.mpr (Nat.cast_nonneg d))
    · simpa only [Y, if_neg hc] using (Matrix.PosSemidef.zero : (0 : N).PosSemidef)
  have mean_positive (i : Fin d) : (mean i).PosSemidef :=
    integral_posSemidef (Y i) (Y_integrable i) (Filter.Eventually.of_forall (Y_positive i))
  have Z_hermitian (i : Fin d) (ω : Ω) : (Z i ω).IsHermitian :=
    (Y_positive i ω).isHermitian.sub (mean_positive i).isHermitian
  have Z_square_positive (i : Fin d) (ω : Ω) : (Z i ω * Z i ω).PosSemidef := by
    simpa only [(Z_hermitian i ω).eq] using Matrix.posSemidef_conjTranspose_mul_self (Z i ω)
  have expansion (i : Fin d) :
      (fun ω => Z i ω * Z i ω) = fun ω =>
        ((Y i ω * Y i ω - Y i ω * mean i) - mean i * Y i ω) + mean i * mean i := by
    funext ω
    dsimp only [Z]
    noncomm_ring
  have Z_square_integrable (i : Fin d) : Integrable (fun ω => Z i ω * Z i ω) μ := by
    rw [expansion]
    exact (((raw.1 i).sub ((Y_integrable i).mul_const (mean i))).sub
      ((Y_integrable i).const_mul (mean i))).add (integrable_const _)
  have centered_mean (i : Fin d) :
      (∫ ω, Z i ω * Z i ω ∂μ) = (∫ ω, Y i ω * Y i ω ∂μ) - mean i * mean i := by
    rw [expansion]
    have hsub1 : Integrable (fun ω => Y i ω * Y i ω - Y i ω * mean i) μ :=
      (raw.1 i).sub ((Y_integrable i).mul_const (mean i))
    have hsub2 : Integrable (fun ω => Y i ω * Y i ω - Y i ω * mean i - mean i * Y i ω) μ :=
      hsub1.sub ((Y_integrable i).const_mul (mean i))
    rw [integral_add hsub2
      (integrable_const (mean i * mean i) : Integrable (fun _ : Ω => mean i * mean i) μ)]
    rw [integral_sub hsub1 ((Y_integrable i).const_mul (mean i))]
    rw [integral_sub (raw.1 i) ((Y_integrable i).mul_const (mean i))]
    rw [integral_mul_const_of_integrable (Y_integrable i),
      integral_const_mul_of_integrable (Y_integrable i)]
    simp only [integral_const, probReal_univ, one_smul]
    change (((∫ ω, Y i ω * Y i ω ∂μ) - mean i * mean i) - mean i * mean i) +
      mean i * mean i = _
    abel
  let A : Fin d → N := fun i => ∫ ω, Z i ω * Z i ω ∂μ
  have A_positive (i : Fin d) : (A i).PosSemidef :=
    integral_posSemidef _ (Z_square_integrable i)
      (Filter.Eventually.of_forall (Z_square_positive i))
  have A_sum_positive : (∑ i : Fin d, A i).PosSemidef :=
    Matrix.posSemidef_sum Finset.univ (fun i _ => A_positive i)
  have mean_square_positive (i : Fin d) : (mean i * mean i).PosSemidef := by
    simpa only [(mean_positive i).isHermitian.eq] using
      Matrix.posSemidef_conjTranspose_mul_self (mean i)
  have centered_sum : (∑ i : Fin d, A i) =
      (∑ i : Fin d, ∫ ω, Y i ω * Y i ω ∂μ) - ∑ i : Fin d, mean i * mean i := by
    simp only [A, centered_mean, Finset.sum_sub_distrib]
  have A_sum_upper : (C • (1 : N) - ∑ i : Fin d, A i).PosSemidef := by
    have h := raw.2.add (Matrix.posSemidef_sum Finset.univ (fun i _ => mean_square_positive i))
    rw [centered_sum]
    convert h using 1 <;> abel

  -- Weighting uses the actual deterministic cosine, hence 0 <= w_i^2 <= 1.
  have weight_le (i : Fin d) : (w i) ^ 2 ≤ 1 := by
    have hi := Real.cos_le_one (((2 * q + 1 : ℕ) : ℝ) * θ i)
    have lo := Real.neg_one_le_cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
    change (Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)) ^ 2 ≤ 1
    nlinarith
  have weighted_square (i : Fin d) (ω : Ω) :
      (w i • Z i ω) * (w i • Z i ω) = (w i) ^ 2 • (Z i ω * Z i ω) := by
    simp only [smul_mul_smul_comm, pow_two]
  have weighted_integrable (i : Fin d) :
      Integrable (fun ω => (w i • Z i ω) * (w i • Z i ω)) μ := by
    simp_rw [weighted_square]
    exact (Z_square_integrable i).smul ((w i) ^ 2)
  have weighted_mean (i : Fin d) :
      (∫ ω, (w i • Z i ω) * (w i • Z i ω) ∂μ) = (w i) ^ 2 • A i := by
    simp_rw [weighted_square]
    exact integral_smul _ _
  have weighted_sum_positive : (∑ i : Fin d, (w i) ^ 2 • A i).PosSemidef :=
    Matrix.posSemidef_sum Finset.univ (fun i _ => (A_positive i).smul (sq_nonneg _))
  have weighted_residual_positive :
      ((∑ i : Fin d, A i) - ∑ i : Fin d, (w i) ^ 2 • A i).PosSemidef := by
    have h := Matrix.posSemidef_sum Finset.univ
      (fun i _ => (A_positive i).smul (sub_nonneg.mpr (weight_le i)))
    convert h using 1
    simp only [sub_smul, one_smul, Finset.sum_sub_distrib]
  have weighted_sum_upper :
      (C • (1 : N) - ∑ i : Fin d, (w i) ^ 2 • A i).PosSemidef := by
    have h := A_sum_upper.add weighted_residual_positive
    convert h using 1 <;> abel

  -- The real matrix operator norm follows from real CFC and full PSD order.
  have C_nonneg : 0 ≤ C := by
    dsimp only [C, r]
    positivity
  have real_norm_bound (B : N) (hB : B.PosSemidef)
      (hupper : (C • (1 : N) - B).PosSemidef) : ‖B‖ ≤ C := by
    have hsa : IsSelfAdjoint B := hB.isHermitian.isSelfAdjoint
    have hlo : 0 ≤ B := Matrix.nonneg_iff_posSemidef.mpr hB
    have hup : B ≤ algebraMap ℝ N C := by
      apply Matrix.le_iff.mpr
      simpa only [Algebra.algebraMap_eq_smul_one] using hupper
    have slo := (StarOrderedRing.nonneg_iff_spectrum_nonneg (R := ℝ) B hsa).mp hlo
    have sup := (le_algebraMap_iff_spectrum_le (R := ℝ) (a := B) hsa).mp hup
    have hn : ‖cfc (id : ℝ → ℝ) B‖ ≤ C := norm_cfc_le C_nonneg (by
      intro x hx
      simpa only [id_eq, Real.norm_eq_abs, abs_of_nonneg (slo x hx)] using sup x hx)
    simpa only [cfc_id ℝ B hsa] using hn
  change (∀ i : Fin d, Integrable (fun ω => Z i ω * Z i ω) μ) ∧
    (∀ i : Fin d, Integrable (fun ω => (w i • Z i ω) * (w i • Z i ω)) μ) ∧
    ‖∑ i : Fin d, A i‖ ≤ C ∧
    ‖∑ i : Fin d, ∫ ω, (w i • Z i ω) * (w i • Z i ω) ∂μ‖ ≤ C
  refine ⟨Z_square_integrable, weighted_integrable,
    real_norm_bound _ A_sum_positive A_sum_upper, ?_⟩
  simp_rw [weighted_mean]
  exact real_norm_bound _ weighted_sum_positive weighted_sum_upper

end AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance

open Lean
def ExpectedCentered : Prop := ∀     {d q : ℕ} (hq : 2 * q + 1 < d),
  let D := EuclideanSpace ℝ (Fin d)
  let E := EuclideanSpace ℝ (Fin (q + 1))
  let Ω := Fin (q + 1) → D
  let μ : Measure Ω := Measure.pi (fun _ : Fin (q + 1) => stdGaussian D)
  let r : ℝ := ((q + 1 : ℕ) : ℝ)
  let L : ℝ := 2 * r + 3 * Real.log (1000 * (d : ℝ))
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 - 1 / 2) * Real.pi / (d : ℝ)
  let t : Fin d → Fin (q + 1) → ℝ := fun i k =>
    if k.val = 0 then 1 else Real.sqrt 2 * Real.cos ((k.val : ℝ) * θ i)
  let row : Fin d → Ω → E := fun i ω =>
    WithLp.toLp 2 (fun b : Fin (q + 1) => ω b i)
  let Y : Fin d → Ω →
      Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ := fun i ω =>
    if ‖row i ω‖ ^ 2 ≤ L then
      (d : ℝ)⁻¹ • Matrix.kronecker
        (Matrix.vecMulVec (WithLp.ofLp (row i ω)) (WithLp.ofLp (row i ω)))
        (Matrix.vecMulVec (t i) (t i))
    else 0
  let mean : Fin d → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i => ∫ ω, Y i ω ∂μ
  let Z : Fin d → Ω → Matrix (Fin (q + 1) × Fin (q + 1)) (Fin (q + 1) × Fin (q + 1)) ℝ :=
    fun i ω => Y i ω - mean i
  let w : Fin d → ℝ := fun i => Real.cos (((2 * q + 1 : ℕ) : ℝ) * θ i)
  let C : ℝ := 2 * r * (r + 2) / (d : ℝ)
  (∀ i : Fin d, Integrable (fun ω => Z i ω * Z i ω) μ) ∧
    (∀ i : Fin d, Integrable (fun ω => (w i • Z i ω) * (w i • Z i ω)) μ) ∧
    ‖∑ i : Fin d, ∫ ω, Z i ω * Z i ω ∂μ‖ ≤ C ∧
    ‖∑ i : Fin d, ∫ ω, (w i • Z i ω) * (w i • Z i ω) ∂μ‖ ≤ C

run_cmd do
  let env := (← getEnv).setExporting false
  setEnv env
  let roots := env.constants.toList.filter (fun (n, _) =>
    n.toString.endsWith ".actual_source_centered_variance_bounds")
  unless roots.length == 1 do throwError "Actual centered private root not unique: {roots.map Prod.fst}"
  let (target, ci) := roots.head!
  match ci with
  | .thmInfo _ => pure ()
  | _ => throwError "Actual root is not a theorem"
  let some proof := ci.value? true | throwError "Actual proof absent"
  let isOwned := fun (n : Name) => target.isPrefixOf n
  let owned := env.constants.toList.filter fun (n, _) => isOwned n
  let some expected := env.find? `ExpectedCentered | throwError "Missing exact literal Prop"
  let some literal := expected.value? true | throwError "Missing exact literal body"
  unless ci.levelParams == [] && expected.levelParams == [] do
    throwError "Unexpected universe parameters"
  Lean.Elab.Command.liftCoreM <| addDecl <| Declaration.thmDecl {
    name := `ActualCenteredSealedTypeCheck
    levelParams := []
    type := mkConst `ExpectedCentered
    value := mkConst target
  }
  logInfo m!"ACTUAL_CENTERED_PRIVATE_ROOT {target}"
  logInfo m!"ACTUAL_CENTERED_SEALED_PROP_KERNEL_APPLICATION_PASS"
  logInfo m!"ACTUAL_CENTERED_RAW_LITERAL_EXPR_EQUALITY {ci.type == literal}"
  let mut pending := proof.getUsedConstants.toList
  let mut seen : NameSet := {}
  let mut parents : NameSet := {}
  while !pending.isEmpty do
    let u := pending.head!
    pending := pending.tail!
    unless seen.contains u do
      seen := seen.insert u
      if isOwned u then
        let some aci := env.find? u | throwError "Missing owned provider {u}"
        let some ap := aci.value? true | throwError "Missing owned body {u}"
        pending := ap.getUsedConstants.toList ++ aci.type.getUsedConstants.toList ++ pending
      else if u.toString.startsWith "AutoSamplingTheory." then
        parents := parents.insert u
  let allowed := [`propext, `Classical.choice, `Quot.sound]
  for (n, ci) in owned do
    match ci with
    | .thmInfo _ => pure ()
    | _ => throwError "Owned provider not theorem: {n}"
    let some body := ci.value? true | throwError "Owned proof absent: {n}"
    unless !ci.type.hasLooseBVars && !ci.type.hasFVar && !ci.type.hasMVar &&
        !body.hasLooseBVars && !body.hasFVar && !body.hasMVar do
      throwError "Unclosed owned theorem type/body {n}"
    unless n == target || seen.contains n do throwError "Unreachable owned provider {n}"
    let ax ← Lean.collectAxioms n
    unless ax.all allowed.contains do throwError "Unexpected axioms {n}: {ax}"
    logInfo m!"ACTUAL_CENTERED_OWNED_CLOSED_REACHABLE {n} axioms={ax}"
  let required := [
    `AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef,
    `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments,
    `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means]
  unless parents.toList.length == required.length && required.all parents.contains do
    throwError "Unexpected actual ASTIS parent boundary: {parents.toList}"
  logInfo m!"ACTUAL_CENTERED_ASTIS_PARENTS {parents.toList}"
  logInfo m!"ACTUAL_CENTERED_ALL_OWNED_COUNT {owned.length}"

#print axioms ActualCenteredSealedTypeCheck
#check (AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance.actual_source_centered_variance_bounds (d := 2) (q := 0) (by decide))
