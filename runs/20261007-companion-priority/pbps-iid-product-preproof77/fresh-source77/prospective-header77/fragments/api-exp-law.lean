/-- The pdf of the exponential distribution depending on its rate -/
noncomputable
def exponentialPDFReal (r x : ℝ) : ℝ :=
  gammaPDFReal 1 r x

/-- The pdf of the exponential distribution, as a function valued in `ℝ≥0∞` -/
noncomputable
def exponentialPDF (r x : ℝ) : ℝ≥0∞ :=
  ENNReal.ofReal (exponentialPDFReal r x)

lemma exponentialPDF_eq (r x : ℝ) :
    exponentialPDF r x = ENNReal.ofReal (if 0 ≤ x then r * exp (-(r * x)) else 0) := by
