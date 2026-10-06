import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher
import AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped RealInnerProductSpace NNReal
noncomputable section

#check (∀ {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {rho : E → ℝ} {L : ℝ≥0} (hrho : ContDiff ℝ 2 rho)
    (hrho0 : rho 0 = 0) (hgrad0 : gradient rho 0 = 0)
    (hH : ∀ u v : E, 0 ≤ fderiv ℝ (fderiv ℝ rho) u v v ∧
      fderiv ℝ (fderiv ℝ rho) u v v ≤ (L : ℝ)*‖v‖^2),
    let gamma := stdGaussian E
    let Z := ∫ u, Real.exp (-rho u) ∂gamma
    let q := fun u => Real.exp (-rho u)/Z
    let f := fun u => Real.exp (-rho u/2)/Real.sqrt Z
    let r := gamma.tilted (fun u => -rho u)
    0 < Z ∧ Z ≤ 1 ∧
      r = (volume : Measure E).tilted (fun u => -(‖u‖^2/2+rho u)) ∧
      r = gamma.withDensity (fun u => ENNReal.ofReal (q u)) ∧
      IsProbabilityMeasure r ∧
      (∀ u, 0 < q u ∧ f u^2 = q u) ∧
      (∫ u, q u ∂gamma) = 1 ∧
      ContDiff ℝ 2 f ∧ MemLp f 2 gamma ∧
      MemLp (gradient f) 2 gamma ∧ MemLp (gradient rho) 2 r ∧
      Integrable (fun u => q u*Real.log (q u)) gamma ∧
      (∀ u, gradient f u = -(f u/2) • gradient rho u) ∧
      (∀ u, gradient (fun z => Real.log (q z)) u = -gradient rho u) ∧
      (∫ u, ‖gradient f u‖^2 ∂gamma) =
        (1/4 : ℝ)*(∫ u, ‖gradient rho u‖^2 ∂r)
)

#check (∀ {E S : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [MeasurableSpace S] {V : E → ℝ} {κ : ℝ}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2)
    {eta : S → ℝ} {y : S → E} (heta : Measurable eta) (hy : Measurable y)
    (hpos : ∀ s, 0 < eta s),
    ∃ p : S → E, Measurable p ∧
      (∀ s, p s+eta s • gradient V (p s)=y s) ∧
      let rho := fun s u => V (p s+Real.sqrt (eta s) • u)-V (p s)-
        Real.sqrt (eta s)*inner ℝ (gradient V (p s)) u
      let mu := (volume : Measure E).tilted (fun x => -V x)
      let R := fun s => mu.tilted (fun x => -‖x-y s‖^2/(2*eta s))
      let r := fun s => (R s).map (fun x => (Real.sqrt (eta s))⁻¹ • (x-p s))
      let gamma := stdGaussian E
      let Z := fun s => ∫ u, Real.exp (-rho s u) ∂gamma
      let q := fun s u => Real.exp (-rho s u)/Z s
      let f := fun s u => Real.exp (-rho s u/2)/Real.sqrt (Z s)
      ∀ s, 0 < Z s ∧ Z s ≤ 1 ∧
        r s = gamma.tilted (fun u => -rho s u) ∧
        r s = gamma.withDensity (fun u => ENNReal.ofReal (q s u)) ∧
        IsProbabilityMeasure (r s) ∧
        (∀ u, 0 < q s u ∧ f s u^2 = q s u) ∧
        (∫ u, q s u ∂gamma) = 1 ∧
        ContDiff ℝ 2 (f s) ∧ MemLp (f s) 2 gamma ∧
        MemLp (gradient (f s)) 2 gamma ∧ MemLp (gradient (rho s)) 2 (r s) ∧
        Integrable (fun u => q s u*Real.log (q s u)) gamma ∧
        (∀ u, gradient (f s) u = -(f s u/2) • gradient (rho s) u) ∧
        (∀ u, gradient (fun z => Real.log (q s z)) u = -gradient (rho s) u) ∧
        (∫ u, ‖gradient (f s) u‖^2 ∂gamma) =
          (1/4 : ℝ)*(∫ u, ‖gradient (rho s) u‖^2 ∂r s)
)
