import Mathlib.MeasureTheory.Constructions.BorelSpace.Metrizable
import Mathlib.MeasureTheory.Constructions.BorelSpace.Real
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Tactic

/-! Borel frames may be selected from compact metrizable families:
a continuous parametrization admits a Borel section on its range. -/
open Set Filter Topology MeasureTheory Metric
noncomputable section
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames

variable {X Y : Type*} [MetricSpace X] [CompactSpace X] [Nonempty X]
  [MeasurableSpace X] [BorelSpace X] [TopologicalSpace Y] [T2Space Y] [MeasurableSpace Y] [BorelSpace Y]

private def cell (x : ℕ → X) : List ℕ → Set X
  | [] => univ
  | k::l => cell x l ∩ closedBall (x k) ((1/2 : ℝ)^l.length)

omit [CompactSpace X] [Nonempty X] [MeasurableSpace X] [BorelSpace X] in
private theorem closed_cell (x : ℕ → X) (l : List ℕ) : IsClosed (cell x l) := by
  induction l with
  | nil => exact isClosed_univ
  | cons k l h => exact h.inter isClosed_closedBall

/-- No measurability assumption on a supplied right inverse is needed. The construction
chooses nested closed balls and uses compactness of their images. -/
theorem continuous_surjection_borel_section (f : X → Y) (hf : Continuous f) (hs : Function.Surjective f) :
    ∃ g : Y → X, Measurable g ∧ Function.RightInverse g f := by
  classical
  obtain ⟨x, hx⟩ := TopologicalSpace.exists_dense_seq X
  let F (l : List ℕ) := f '' cell x l
  have hclosed (l : List ℕ) : IsClosed (F l) := ((closed_cell x l).isCompact.image hf).isClosed
  have hnext (l : List ℕ) (y : Y) : ∃ k : ℕ, y ∉ F l ∨ y ∈ F (k::l) := by
    by_cases hy : y ∈ F l
    · obtain ⟨z,hz,rfl⟩ := hy
      obtain ⟨k,hk⟩ := Metric.denseRange_iff.mp hx z ((1/2 : ℝ)^l.length) (by positivity)
      exact ⟨k, Or.inr ⟨z,⟨hz,hk.le⟩,rfl⟩⟩
    · exact ⟨0,Or.inl hy⟩
  let pick (l : List ℕ) (y : Y) := Nat.find (hnext l y)
  have hp (l : List ℕ) : Measurable (pick l) := measurable_find (hnext l)
    (fun k => (hclosed l).measurableSet.compl.union (hclosed (k::l)).measurableSet)
  let : MeasurableSpace (List ℕ) := ⊤
  have : MeasurableSingletonClass (List ℕ) := ⟨fun _ => trivial⟩
  let path (y : Y) : ℕ → List ℕ := Nat.rec [] (fun _ l => pick l y :: l)
  have hpath (n : ℕ) : Measurable (fun y => path y n) := by
    induction n with
    | zero => exact measurable_const
    | succ n ih =>
      have hm : Measurable (fun p : List ℕ × Y => pick p.1 p.2) := measurable_from_prod_countable_right hp
      have hcons : Measurable (fun p : ℕ × List ℕ => p.1::p.2) := measurable_of_countable _
      exact hcons.comp ((hm.comp (ih.prodMk measurable_id)).prodMk ih)
  have valid (y : Y) (n : ℕ) : y ∈ F (path y n) := by
    induction n with
    | zero => obtain ⟨z,rfl⟩ := hs y; exact ⟨z,mem_univ _,rfl⟩
    | succ n ih => exact (Nat.find_spec (hnext (path y n) y)).resolve_left (not_not.mpr ih)
  have hlen (y : Y) (n : ℕ) : (path y n).length = n := by induction n <;> simp_all [path]
  let A (y : Y) (n : ℕ) := cell x (path y n) ∩ f ⁻¹' {y}
  have hA (y : Y) : (⋂ n, A y n).Nonempty := by
    have hcl (n : ℕ) : IsClosed (A y n) := (closed_cell _ _).inter (isClosed_singleton.preimage hf)
    apply IsCompact.nonempty_iInter_of_sequence_nonempty_isCompact_isClosed _ _ _ (hcl 0).isCompact hcl
    · intro n z h; exact ⟨h.1.1,h.2⟩
    · intro n
      obtain ⟨z,hz,hy⟩ := valid y n
      exact ⟨z,hz,hy⟩
  let g (y : Y) := (hA y).choose
  have hg (y : Y) (n : ℕ) : g y ∈ A y n := mem_iInter.mp (hA y).choose_spec n
  refine ⟨g, ?_, fun y => (hg y 0).2⟩
  let approx (n : ℕ) (y : Y) := x (pick (path y n) y)
  apply measurable_of_tendsto_metrizable (f := approx)
  · intro n
    have hm : Measurable (fun p : List ℕ × Y => pick p.1 p.2) := measurable_from_prod_countable_right hp
    exact (measurable_of_countable x).comp (hm.comp ((hpath n).prodMk measurable_id))
  · apply tendsto_pi_nhds.mpr
    intro y
    apply tendsto_iff_dist_tendsto_zero.mpr
    apply squeeze_zero (fun _ => dist_nonneg) _ (tendsto_pow_atTop_nhds_zero_of_lt_one
      (by norm_num : 0 ≤ (1/2:ℝ)) (by norm_num))
    intro n
    have h := (hg y (n+1)).1.2
    change dist (g y) (approx n y) ≤ (1/2 : ℝ)^(path y n).length at h
    rwa [dist_comm,hlen] at h

/-- Lift any measurable family of observations through a continuous compact frame chart.
Membership in the range is purely pointwise. -/
theorem measurable_lift {Ω : Type*} [MeasurableSpace Ω] (f : X → Y) (hf : Continuous f)
    (a : Ω → Y) (ha : Measurable a) (hex : ∀ ω, a ω ∈ Set.range f) :
    ∃ b : Ω → X, Measurable b ∧ ∀ ω, f (b ω) = a ω := by
  obtain ⟨g,hg,hr⟩ := continuous_surjection_borel_section (Set.rangeFactorization f)
    (hf.subtype_mk _) (Set.rangeFactorization_surjective (f := f))
  exact ⟨fun ω => g ⟨a ω,hex ω⟩, hg.comp ha.subtype_mk, fun ω => congrArg Subtype.val (hr ⟨a ω,hex ω⟩)⟩

#print axioms measurable_lift
end AutoSamplingTheory.ExampleCases.GaussianComplexity.MeasurableFrames
