import AutoSamplingTheory.TechnicalLemmas.Analysis.NormalizedMass

open AutoSamplingTheory.TechnicalLemmas.Analysis.NormalizedMass

-- Exact anonymous proposition exported to the independent decoder.
example : ∀ {g b : ℝ}, 0 ≤ g → 0 ≤ b → 0 < g + b →
    b / (g + b) ≤ b + (1 - Real.sqrt g) ^ 2 ∧
      b + (1 - Real.sqrt g) ^ 2 ≤ b + (1 - g) ^ 2 :=
  @bad_mass_ratio_bounds

-- Both inequalities are exercised, including zero individual masses.
example {g b : ℝ} (hg : 0 ≤ g) (hb : 0 ≤ b) (hpos : 0 < g + b) :
    b / (g + b) ≤ b + (1 - g) ^ 2 :=
  (bad_mass_ratio_bounds hg hb hpos).1.trans (bad_mass_ratio_bounds hg hb hpos).2

example {b : ℝ} (hb : 0 < b) :
    b / (0 + b) ≤ b + (1 - Real.sqrt 0) ^ 2 :=
  (bad_mass_ratio_bounds (g := 0) le_rfl hb.le (by simpa using hb)).1

example {g : ℝ} (hg : 0 < g) :
    (0 : ℝ) + (1 - Real.sqrt g) ^ 2 ≤ 0 + (1 - g) ^ 2 :=
  (bad_mass_ratio_bounds hg.le (b := 0) le_rfl (by simpa using hg)).2

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.NormalizedMass.bad_mass_ratio_bounds
