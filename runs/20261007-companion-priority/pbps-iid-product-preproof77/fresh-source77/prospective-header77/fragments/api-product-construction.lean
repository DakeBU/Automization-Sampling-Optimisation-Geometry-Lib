namespace Measure

open scoped Classical in
/-- The product measure of an arbitrary family of probability measures. It is defined as the unique
extension of the function which gives to cylinders the measure given by the associated product
measure.

It is defined via an `if ... then ... else` so that it can be manipulated without carrying
a proof that the measures are probability measures. -/
noncomputable def infinitePi : Measure (Π i, X i) :=
  if h : ∀ i, IsProbabilityMeasure (μ i) then
    (piContent μ).measure isSetSemiring_measurableCylinders
      generateFrom_measurableCylinders.ge (isSigmaSubadditive_piContent (hμ := h) μ)
    else 0

/-- The product measure is the projective limit of the partial product measures. This ensures
uniqueness and expresses the value of the product measure applied to cylinders. -/
theorem isProjectiveLimit_infinitePi :
    IsProjectiveLimit (infinitePi μ) (fun I : Finset ι ↦ (Measure.pi (fun i : I ↦ μ i))) := by
  intro I
  ext s hs
  rw [map_apply (measurable_restrict I) hs, infinitePi, dif_pos hμ, AddContent.measure_eq,
    ← cylinder, piContent_cylinder μ hs]
  · exact generateFrom_measurableCylinders.symm
  · exact cylinder_mem_measurableCylinders _ _ hs

/-- Restricting the product measure to a product indexed by a finset yields the usual
product measure. -/
theorem infinitePi_map_restrict {I : Finset ι} :
    (Measure.infinitePi μ).map I.restrict = Measure.pi fun i : I ↦ μ i :=
  isProjectiveLimit_infinitePi μ I

instance : IsProbabilityMeasure (infinitePi μ) := by
  constructor
  rw [← cylinder_univ ∅, cylinder, ← map_apply (measurable_restrict _) .univ,
    infinitePi_map_restrict, measure_univ]
