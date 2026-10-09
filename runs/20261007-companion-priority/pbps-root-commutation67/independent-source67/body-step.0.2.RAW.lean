  have hGcNonneg : 0 ≤ Gc := (ContinuousLinearMap.nonneg_iff_isPositive Gc).mpr hGc
  have hRoot : CFC.sqrt (Gc*Gc)=Gc := CFC.sqrt_unique rfl hGcNonneg
  have hLift : Commute Gc Dc := by
    have h := hComplex.cfcₙ_nnreal NNReal.sqrt
    change Commute (CFC.sqrt (Gc*Gc)) Dc at h
    rwa [hRoot] at h
