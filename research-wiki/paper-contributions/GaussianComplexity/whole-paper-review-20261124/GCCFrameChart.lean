import GCCCompactSection
import GC43Exposed
import Mathlib.Analysis.InnerProductSpace.ProdL2
import Mathlib.Topology.Metrizable.Uniformity

/-! Measurable choices of ambient orthogonal frames from the source observations
P_E and O P_E on each fixed-rank stratum. -/
noncomputable section
open MeasureTheory Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames

abbrev Mat (N : ℕ) := Matrix (Fin N) (Fin N) ℝ

local instance matrixMeasurable (N : ℕ) : MeasurableSpace (Mat N) := borel _
local instance matrixBorel (N : ℕ) : BorelSpace (Mat N) := ⟨rfl⟩

local instance matrixSecond (N : ℕ) : SecondCountableTopology (Mat N) :=
  inferInstanceAs (SecondCountableTopology (Fin N → Fin N → ℝ))

def front (N r : ℕ) : Submodule ℝ (E N) where
  carrier := {x | ∀ i : Fin N, r ≤ i.val → x i = 0}
  zero_mem' := by simp
  add_mem' := by intro x y hx hy i hi; change x i + y i = 0; rw [hx i hi,hy i hi,add_zero]
  smul_mem' := by intro a x hx i hi; change a * x i = 0; rw [hx i hi,mul_zero]

theorem finrank_front {N r : ℕ} (hr : r ≤ N) : Module.finrank ℝ (front N r) = r := by
  let e : front N r ≃ₗ[ℝ] (Fin r → ℝ) := {
    toFun := fun x i => x.val ⟨i.val,i.isLt.trans_le hr⟩
    invFun := fun z => ⟨WithLp.toLp 2 (fun i => if h : i.val < r then z ⟨i.val,h⟩ else 0),
      fun i hi => dif_neg (not_lt.mpr hi)⟩
    map_add' := fun _ _ => rfl
    map_smul' := fun _ _ => rfl
    left_inv := by
      intro x
      apply Subtype.ext
      apply (WithLp.equiv 2 (Fin N → ℝ)).injective
      funext i
      change (if h : i.val < r then x.val ⟨i.val,h.trans_le hr⟩ else 0) = x.val i
      split
      · rfl
      · exact (x.property i (by omega)).symm
    right_inv := by intro x; funext i; exact dif_pos i.isLt }
  simpa using e.finrank_eq

def projectionMatrix {N : ℕ} (V : Submodule ℝ (E N)) : Mat N :=
  (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)).symm V.starProjection

private def align {N : ℕ} (U V : Submodule ℝ (E N)) (h : Module.finrank ℝ U = Module.finrank ℝ V) :
    U ≃ₗᵢ[ℝ] V := ((stdOrthonormalBasis ℝ U).reindex (finCongr h)).repr.trans
      (stdOrthonormalBasis ℝ V).repr.symm

private theorem match_projection {N : ℕ} (U V : Submodule ℝ (E N))
    (h : Module.finrank ℝ U = Module.finrank ℝ V) :
    ∃ D : O N, D.val * projectionMatrix U * D⁻¹.val = projectionMatrix V := by
  have hu := U.finrank_add_finrank_orthogonal
  have hv := V.finrank_add_finrank_orthogonal
  let e := align U V h
  let k := align Uᗮ Vᗮ (by omega)
  let Q := U.orthogonalDecomposition.trans ((e.withLpProdCongr 2 k).trans V.orthogonalDecomposition.symm)
  let u := Unitary.linearIsometryEquiv.symm Q
  let M := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)
  let D : O N := ⟨M.symm u.val,Unitary.map_mem M.symm u.property⟩
  have huD : M D.val = u.val := M.apply_symm_apply _
  have huDi : M D⁻¹.val = star u.val := by
    change M (star D.val) = _
    rw [map_star,huD]
  have hQ (z : E N) : Q (U.starProjection z) = V.starProjection (Q z) := by
    have h1 (a : V) (b : Vᗮ) : V.starProjection ((a : E N)+(b : E N)) = a := by
      rw [map_add,V.starProjection_eq_self_iff.mpr a.property,
        V.starProjection_apply, V.orthogonalProjectionOnto_apply_of_mem_orthogonal b.property]
      simp
    simp only [Q, LinearIsometryEquiv.trans_apply, Submodule.orthogonalDecomposition_apply,
      LinearIsometryEquiv.withLpProdCongr_apply,Submodule.orthogonalDecomposition_symm_apply]
    change ((e (U.orthogonalProjectionOnto (U.starProjection z)) : V) : E N) +
      ((k (Uᗮ.orthogonalProjectionOnto (U.starProjection z)) : Vᗮ) : E N) = _
    have hz : U.starProjection z ∈ U := (U.orthogonalProjectionOnto z).property
    rw [h1, Uᗮ.orthogonalProjectionOnto_apply_of_mem_orthogonal (by simp [hz]), map_zero]
    simp only [ZeroMemClass.coe_zero, add_zero]
    change ((e (U.orthogonalProjectionOnto (↑(U.orthogonalProjectionOnto z) : E N)) : V) : E N) = _
    rw [U.orthogonalProjectionOnto_mem_subspace_eq_self]
    rfl
  refine ⟨D,M.injective ?_⟩
  rw [map_mul,map_mul]
  change M D.val * M (M.symm U.starProjection) * M D⁻¹.val = M (M.symm V.starProjection)
  rw [huD,huDi,M.apply_symm_apply,M.apply_symm_apply]
  change u.val * U.starProjection * (star u.val) = V.starProjection
  have heq : u.val * U.starProjection = V.starProjection * u.val :=
    ContinuousLinearMap.ext hQ
  rw [heq,mul_assoc,show u.val * star u.val = 1 from u.property.2, mul_one]

def frameObservation {N : ℕ} (r : ℕ) (p : O N × O N) : Mat N × Mat N :=
  (p.1.val * projectionMatrix (front N r) * p.1⁻¹.val,
   p.2.val * projectionMatrix (front N r) * p.1⁻¹.val)

theorem continuous_frameObservation {N r : ℕ} : Continuous (@frameObservation N r) := by
  unfold frameObservation
  fun_prop

/-- A rank-r subspace and its known partial action yield measurable domain and range
frames. Only the projection and the partial action are required to be measurable.
The orthogonal extension supplied by the experiment may vary arbitrarily. -/
theorem measurable_frame_pair {N r : ℕ} (hr : r ≤ N) {H : Type*} [MeasurableSpace H]
    (V : H → Submodule ℝ (E N)) (A : H → O N) (rank : ∀ h, Module.finrank ℝ (V h) = r)
    (hP : Measurable (fun h => projectionMatrix (V h)))
    (hT : Measurable (fun h => (A h).val * projectionMatrix (V h))) :
    ∃ p : H → O N × O N, Measurable p ∧ ∀ h,
      frameObservation r (p h) = (projectionMatrix (V h),(A h).val * projectionMatrix (V h)) := by
  let : MetricSpace (O N × O N) := TopologicalSpace.metrizableSpaceMetric _
  apply measurable_lift _ continuous_frameObservation _ (hP.prodMk hT)
  intro h
  obtain ⟨D,hD⟩ := match_projection (front N r) (V h) ((finrank_front hr).trans (rank h).symm)
  refine ⟨(D,A h*D),Prod.ext hD ?_⟩
  change ((A h).val*D.val)*projectionMatrix (front N r)*D⁻¹.val = _
  rw [← hD]
  simp only [mul_assoc]

/-- The rank strata of a measurable orthogonal projection are measurable. -/
theorem measurable_finrank {N : ℕ} {H : Type*} [MeasurableSpace H] (V : H → Submodule ℝ (E N))
    (hP : Measurable (fun h => projectionMatrix (V h))) : Measurable (fun h => Module.finrank ℝ (V h)) := by
  let M := Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin N)
  let L : Mat N →ₗ[ℝ] ℝ := (LinearMap.trace ℝ (E N)).comp
    ((ContinuousLinearMap.coeLM ℝ).comp M.toAlgEquiv.toLinearMap)
  have htrace (h : H) : L (projectionMatrix (V h)) = (Module.finrank ℝ (V h) : ℝ) := by
    have hproj : LinearMap.IsProj (V h) (V h).starProjection.toLinearMap :=
      ⟨fun z => ((V h).orthogonalProjectionOnto z).property,fun _ hz => (V h).starProjection_eq_self_iff.mpr hz⟩
    change LinearMap.trace ℝ (E N) (M (M.symm (V h).starProjection)).toLinearMap = _
    rw [M.apply_symm_apply]
    exact hproj.trace
  have hm : Measurable (fun h => L (projectionMatrix (V h))) :=
    L.continuous_of_finiteDimensional.measurable.comp hP
  apply measurable_to_nat
  intro y
  let r := Module.finrank ℝ (V y)
  have e : {h | Module.finrank ℝ (V h) = r} = (fun h => L (projectionMatrix (V h))) ⁻¹' {(r : ℝ)} := by
    ext h
    change _ ↔ L (projectionMatrix (V h)) = (r : ℝ)
    rw [htrace,Nat.cast_inj]
    rfl
  change MeasurableSet {h | Module.finrank ℝ (V h) = r}
  rw [e]
  exact hm (measurableSet_singleton _)

/-- One measurable choice across all ranks. The observable subspace is specified
by its orthogonal projector and the observed action by the partial matrix OP_E. -/
theorem measurable_frames_all_ranks {N : ℕ} {H : Type*} [MeasurableSpace H]
    (V : H → Submodule ℝ (E N)) (A : H → O N)
    (hP : Measurable (fun h => projectionMatrix (V h)))
    (hT : Measurable (fun h => (A h).val * projectionMatrix (V h))) :
    ∃ p : H → O N × O N, Measurable p ∧ ∀ h,
      frameObservation (Module.finrank ℝ (V h)) (p h) =
        (projectionMatrix (V h),(A h).val * projectionMatrix (V h)) := by
  classical
  let k (h : H) := Module.finrank ℝ (V h)
  have hk := measurable_finrank V hP
  have branch (r : ℕ) : ∃ p : H → O N × O N, Measurable p ∧ ∀ h, k h = r →
      frameObservation r (p h) = (projectionMatrix (V h),(A h).val * projectionMatrix (V h)) := by
    let s := {h | k h = r}
    have hs : MeasurableSet s := hk (measurableSet_singleton r)
    by_cases hr : r ≤ N
    · obtain ⟨f,hf,he⟩ := measurable_frame_pair hr (fun h : s => V h) (fun h : s => A h)
        (fun h => h.property) (hP.comp measurable_subtype_coe) (hT.comp measurable_subtype_coe)
      let g (h : H) := if h' : h ∈ s then f ⟨h,h'⟩ else (1,1)
      refine ⟨g,measurable_of_restrict_of_restrict_compl hs ?_ ?_,?_⟩
      · have e : s.domRestrict g = f := funext (fun h => dif_pos h.property)
        rwa [e]
      · have e : sᶜ.domRestrict g = (fun _ => (1,1)) := funext (fun h => dif_neg h.property)
        rw [e]; exact measurable_const
      · intro h hh
        change h ∈ s at hh
        simpa only [g,dif_pos hh] using he ⟨h,hh⟩
    · refine ⟨fun _ => (1,1),measurable_const,?_⟩
      intro h hh
      have hdim := (V h).finrank_le
      rw [finrank_euclideanSpace_fin] at hdim
      exact (hr (hh ▸ hdim)).elim
  choose p hp he using branch
  have hm : Measurable (fun t : ℕ × H => p t.1 t.2) := measurable_from_prod_countable_right hp
  exact ⟨fun h => p (k h) h,hm.comp (hk.prodMk measurable_id),fun h => he _ h rfl⟩

#print axioms measurable_frames_all_ranks
#print axioms measurable_frame_pair
end AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
