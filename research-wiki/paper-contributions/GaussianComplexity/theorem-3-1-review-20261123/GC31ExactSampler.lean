import GC31LowerBound
import Mathlib.Probability.Kernel.Representation

/-!
# An exact sampler with a finite first-order query budget

Query the standard basis in order to recover the precision matrix column by
column. A Borel sampler driven by one uniform seed then draws the Gaussian law
of that precision. This supplies a feasible budget even at zero tolerance.
-/

open MeasureTheory ProbabilityTheory Matrix
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior
open AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle (run)

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability

private theorem seeded_gaussian (d : ℕ) :
    ∃ sample : Precision d → unitInterval → E d, Measurable (Function.uncurry sample) ∧
      ∀ A, A.PosDef → volume.map (sample A) = targetLaw A := by
  classical
  let q (A : Precision d) (x : E d) := Real.sqrt A.det /
    (2 * Real.pi) ^ ((d : ℝ) / 2) * Real.exp (-((WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x)) / 2)
  let density (A : Precision d) :=
    (volume : Measure (E d)).withDensity (fun x => ENNReal.ofReal (q A x))
  have hq : Continuous (Function.uncurry q) := by dsimp only [q]; fun_prop
  have hd : Measurable density := measurable_withDensity (ENNReal.measurable_ofReal.comp hq.measurable)
  have hmass : Measurable (fun A => density A Set.univ) :=
    (Measure.measurable_coe MeasurableSet.univ).comp hd
  let K : Kernel (Precision d) (E d) :=
    ⟨fun A => if density A Set.univ = 1 then density A else Measure.dirac 0,
      Measurable.ite (hmass (measurableSet_singleton 1)) hd measurable_const⟩
  let : IsMarkovKernel K := ⟨fun A => by
    change IsProbabilityMeasure (if density A Set.univ = 1 then density A else Measure.dirac 0)
    split
    next h => exact ⟨h⟩
    next => infer_instance⟩
  obtain ⟨sample, hm, hl⟩ := K.exists_measurable_map_eq_unitInterval
  refine ⟨sample,hm,fun A hp => (hl A).trans ?_⟩
  have he : density A = targetLaw A := (multivariateGaussian_eq_withDensity_of_posDef A hp).symm
  change (if density A Set.univ = 1 then density A else Measure.dirac 0) = targetLaw A
  rw [he, measure_univ, if_pos rfl]

private abbrev SampleState (d : ℕ) := unitInterval × ℕ × Precision d

private noncomputable def direction (d c : ℕ) : E d :=
  WithLp.toLp 2 (fun i : Fin d => if i.val = c then 1 else 0)

private noncomputable def columnNext {d : ℕ} (s : SampleState d) : Unit ⊕ E d :=
  if s.2.1 < d then .inr (direction d s.2.1) else .inl ()

private def replaceColumn {d : ℕ} (B : Precision d) (c : ℕ) (v : E d) : Precision d :=
  Matrix.of fun i j => if j.val = c then v i else B i j

private def columnUpdate {d : ℕ} (s : SampleState d) (_ : E d) (reply : Reply d) : SampleState d :=
  (s.1, s.2.1+1, replaceColumn s.2.2 s.2.1 reply.2)

private theorem measurable_columnNext (d : ℕ) : Measurable (@columnNext d) := by
  have hc : Measurable (fun s : SampleState d => s.2.1) := measurable_fst.comp measurable_snd
  exact Measurable.ite (measurableSet_lt hc measurable_const)
    (measurable_inr.comp ((measurable_of_countable (direction d)).comp hc)) measurable_const

private theorem continuous_replaceColumn (d c : ℕ) :
    Continuous (fun p : Precision d × E d => replaceColumn p.1 c p.2) := by
  apply continuous_matrix
  intro i j
  by_cases h : j.val = c
  · simp only [replaceColumn, Matrix.of_apply, if_pos h]
    exact (continuous_apply i).comp ((PiLp.continuous_ofLp 2 _).comp
        (continuous_snd : Continuous (Prod.snd : Precision d × E d → E d)))
  · simpa only [replaceColumn, Matrix.of_apply, if_neg h] using
      (continuous_fst : Continuous (Prod.fst : Precision d × E d → Precision d)).matrix_elem i j

private theorem measurable_columnUpdate (d : ℕ) :
    Measurable (fun p : SampleState d × E d × Reply d => columnUpdate p.1 p.2.1 p.2.2) := by
  have hm : Measurable (fun p : ℕ × (Precision d × E d) => replaceColumn p.2.1 p.1 p.2.2) :=
    measurable_from_prod_countable_right fun c => (continuous_replaceColumn d c).measurable
  have hc : Measurable (fun p : SampleState d × E d × Reply d => p.1.2.1) :=
    measurable_fst.comp (measurable_snd.comp measurable_fst)
  have hB : Measurable (fun p : SampleState d × E d × Reply d => p.1.2.2) :=
    measurable_snd.comp (measurable_snd.comp measurable_fst)
  have hv : Measurable (fun p : SampleState d × E d × Reply d => p.2.2.2) :=
    measurable_snd.comp (measurable_snd.comp measurable_snd)
  exact (measurable_fst.comp measurable_fst).prodMk
    ((hc.add_const 1).prodMk (hm.comp (hc.prodMk (hB.prodMk hv))))

private theorem actual_column {d : ℕ} (A : Precision d) (j : Fin d) (i : Fin d) :
    ((precisionReply A (direction d j.val)).2) i = A i j := by
  have he : WithLp.ofLp (direction d j.val) = Pi.single j 1 := by
    funext k
    by_cases h : k = j
    · subst k; simp [direction]
    · have hh : k.val ≠ j.val := fun hv => h (Fin.ext hv)
      simp [direction, hh, h]
  change (A *ᵥ WithLp.ofLp (direction d j.val)) i = A i j
  rw [he, Matrix.mulVec_single_one]
  rfl

private theorem columns_recovered {d : ℕ} (A : Precision d) (u : unitInterval) (fuel c : ℕ)
    (B : Precision d) (h : c+fuel=d) (hB : ∀ i j : Fin d, j.val < c → B i j = A i j) :
    (run columnNext columnUpdate (precisionReply A) fuel (u,c,B)).1.1 = (u,d,A) := by
  induction fuel generalizing c B with
  | zero =>
    have he : B = A := by ext i j; exact hB i j (by omega)
    have hc : c = d := by omega
    subst c B
    simp [run, columnNext]
  | succ t ih =>
    have hc : c < d := by omega
    rw [run]
    simp only [columnNext, if_pos hc, columnUpdate]
    refine ih _ _ (by omega) ?_
    intro i j hj
    by_cases e : j.val = c
    · simp only [replaceColumn, Matrix.of_apply, if_pos e]
      exact e ▸ actual_column A j i
    · simp only [replaceColumn, Matrix.of_apply, if_neg e]
      exact hB i j (by omega)

/-- A dimension-d first-order algorithm attains the exact target on every
admissible precision with budget d and one independent uniform random seed. -/
theorem exists_exact_sampler (d : ℕ) :
    ∃ alg : Algorithm d unitInterval (unitInterval × ℕ × Precision d),
      ∀ κ A, Admissible κ A → alg.outputLaw volume d A = targetLaw A := by
  obtain ⟨sample, hm, hsample⟩ := seeded_gaussian d
  let alg : Algorithm d unitInterval (SampleState d) := {
    start := fun u => (u,0,0)
    next := columnNext
    update := columnUpdate
    output := fun s => sample s.2.2 s.1
    measurable_start := measurable_id.prodMk measurable_const
    measurable_next := measurable_columnNext d
    measurable_update := measurable_columnUpdate d
    measurable_output := hm.comp ((measurable_snd.comp measurable_snd).prodMk measurable_fst) }
  refine ⟨alg, ?_⟩
  intro κ A hA
  have hp : A.PosDef := by
    apply Matrix.posDef_iff_dotProduct_mulVec.mpr
    refine ⟨hA.1, ?_⟩
    intro v hv
    have hnorm : 0 < v ⬝ᵥ v := by
      simpa only [star_trivial] using dotProduct_star_self_pos_iff.mpr hv
    simpa only [star_trivial] using lt_of_lt_of_le hnorm (hA.2 v).1
  have he : alg.sample d A = sample A := by
    funext u
    have hr := columns_recovered A u d 0 (0 : Precision d) (by omega) (by simp)
    change sample (run columnNext columnUpdate (precisionReply A) d (u,0,0)).1.1.2.2
      (run columnNext columnUpdate (precisionReply A) d (u,0,0)).1.1.1 = _
    rw [hr]
  rw [Algorithm.outputLaw, he, hsample A hp]

/-- The exact sampler supplies a finite upper bound on the same query
complexity used in Theorem 3.1. -/
theorem gaussian_query_complexity_le_dimension (d : ℕ) (κ : ℝ) {ε : ℝ} (hε : 0 ≤ ε) :
    gaussianQueryComplexity.{0,0} d κ ε ≤ (d : ℝ≥0∞) := by
  obtain ⟨alg, halg⟩ := exists_exact_sampler d
  have hf : FeasibleBudget.{0,0} d κ ε d := by
    refine ⟨unitInterval, unitInterval × ℕ × Precision d, inferInstance, inferInstance,
      volume, inferInstance, alg, ?_⟩
    intro A hA
    rw [halg κ A hA, eventTV]
    apply csSup_le
    · exact ⟨0, ∅, MeasurableSet.empty, by simp⟩
    · rintro z ⟨B, _, rfl⟩
      simpa only [sub_self, abs_zero] using hε
  exact iInf_le (fun t : {T : ℕ // FeasibleBudget.{0,0} d κ ε T} => (t.val : ℝ≥0∞)) ⟨d,hf⟩

/-- Theorem 3.1 on the finite real-valued query complexity of the concrete
measurable algorithm class. -/
theorem gaussian_query_complexity_lower_bound_real {d : ℕ} {κ ε : ℝ}
    (hd : 1 ≤ d) (hκ : 4 ≤ κ) (hε : 0 < ε) (hsmall : ε ≤ 1/16) :
    (1/256 : ℝ) * min (d : ℝ) (Real.sqrt κ * Real.log (1 + (d : ℝ)/(Real.sqrt κ * ε))) ≤
      (gaussianQueryComplexity.{0,0} d κ ε).toReal := by
  have hfinite := (gaussian_query_complexity_le_dimension d κ hε.le).trans_lt
    (ENNReal.natCast_lt_top d)
  have h := ENNReal.toReal_mono hfinite.ne (gaussian_query_complexity_lower_bound hd hκ hε hsmall)
  rw [ENNReal.toReal_ofReal'] at h
  exact (le_max_left _ _).trans h

#print axioms gaussian_query_complexity_lower_bound_real
#print axioms exists_exact_sampler
#print axioms gaussian_query_complexity_le_dimension

end AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
