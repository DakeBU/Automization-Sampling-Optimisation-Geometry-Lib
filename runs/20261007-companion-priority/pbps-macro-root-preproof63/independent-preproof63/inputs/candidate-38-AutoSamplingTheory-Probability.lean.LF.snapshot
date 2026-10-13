import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Order.Archimedean.Real.Basic
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.InformationTheory.KullbackLeibler.Basic
import Mathlib.MeasureTheory.Measure.LogLikelihoodRatio
import Mathlib.MeasureTheory.Measure.Tilted
import Mathlib.Probability.Kernel.Condexp
import Mathlib.Probability.Moments.IntegrableExpMul
import AutoSamplingTheory.Core

/-!
# Probability and functional-inequality contracts

The first implementation records the analytic interfaces needed by SALD and
RMFLD papers.  Heavy measure-theoretic proofs are intentionally represented as
contracts or proof obligations until they are ported from Mathlib/SLT or proved
locally.
-/

namespace AutoSamplingTheory

open MeasureTheory InformationTheory
open scoped ENNReal NNReal ProbabilityTheory Topology

/-- Pushforward-law equality from almost-everywhere equality of random variables.

This is the measure-level version of the endpoint-law bookkeeping used by the
SALD Euler--Maruyama interpolation blocks: once two process representatives
agree almost everywhere on the common probability space, their pushforward laws
are equal.  It does not construct the process, conditional drift, density, or
Fokker--Planck backend.
-/
theorem lawMapEqOfAEEq {Ω E : Type*} [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {X Y : Ω → E}
    (hXY : X =ᵐ[P] Y) :
    Measure.map X P = Measure.map Y P := by
  exact Measure.map_congr hXY

/-- Integrating a test against a pushforward law is the same as integrating
the composed test on the original probability space.

This is the weak-test bookkeeping used before differentiating EM
interpolation laws.  It does not prove any time differentiability, generator
identity, conditional law, density, or Fokker--Planck equation.
-/
theorem lawMapIntegral {Ω E B : Type*} [MeasurableSpace Ω]
    [MeasurableSpace E] [NormedAddCommGroup B] [NormedSpace ℝ B]
    {P : Measure Ω} {X : Ω → E} {φ : E → B}
    (hX : AEMeasurable X P)
    (hφ : AEStronglyMeasurable φ (Measure.map X P)) :
    (∫ x, φ x ∂Measure.map X P) = ∫ ω, φ (X ω) ∂P := by
  rw [integral_map hX hφ]

/-- Transport a supplied sample-space derivative to the corresponding
pushforward-law weak-test integral.

The analytic derivative is still an explicit hypothesis.  This lemma only
packages the `Measure.map` integral rewrite needed before applying a future
EM generator/Fokker--Planck theorem.
-/
theorem lawMapIntegralHasDerivAtOfSample {Ω E : Type*}
    [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {X : ℝ → Ω → E} {φ : E → ℝ} {s0 g : ℝ}
    (hX : ∀ s, AEMeasurable (X s) P)
    (hφ : ∀ s, AEStronglyMeasurable φ (Measure.map (X s) P))
    (hderiv : HasDerivAt (fun s => ∫ ω, φ (X s ω) ∂P) g s0) :
    HasDerivAt (fun s => ∫ x, φ x ∂Measure.map (X s) P) g s0 := by
  have hfun :
      (fun s => ∫ x, φ x ∂Measure.map (X s) P) =
        (fun s => ∫ ω, φ (X s ω) ∂P) := by
    funext s
    exact lawMapIntegral (hX s) (hφ s)
  simpa [hfun] using hderiv

/-- Transport a sample-space derivative to a named law path equal to a
`Measure.map` path.

This is the named-law variant used when a paper first writes
`hat rho_s = Law(hat X_s)` and the Lean target keeps `hatRhoS` as a separate
measure-valued path.  The only analytic derivative input remains the
sample-space derivative; this lemma just combines the named-law equality with
`lawMapIntegralHasDerivAtOfSample`.
-/
theorem lawIntegralHasDerivAtOfMeasureMapEqAndSample {Ω E : Type*}
    [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {X : ℝ → Ω → E} {ρ : ℝ → Measure E}
    {φ : E → ℝ} {s0 g : ℝ}
    (hρ : ∀ s, ρ s = Measure.map (X s) P)
    (hX : ∀ s, AEMeasurable (X s) P)
    (hφ : ∀ s, AEStronglyMeasurable φ (ρ s))
    (hderiv : HasDerivAt (fun s => ∫ ω, φ (X s ω) ∂P) g s0) :
    HasDerivAt (fun s => ∫ x, φ x ∂ρ s) g s0 := by
  have hφMap :
      ∀ s, AEStronglyMeasurable φ (Measure.map (X s) P) := by
    intro s
    simpa [hρ s] using hφ s
  have hmap :
      HasDerivAt
        (fun s => ∫ x, φ x ∂Measure.map (X s) P) g s0 :=
    lawMapIntegralHasDerivAtOfSample
      (P := P) (X := X) (φ := φ) hX hφMap hderiv
  have hfun :
      (fun s => ∫ x, φ x ∂ρ s) =
        fun s => ∫ x, φ x ∂Measure.map (X s) P := by
    funext s
    rw [hρ s]
  simpa [hfun] using hmap

/-- Transport a dominated pointwise derivative to a pushforward-law weak-test
derivative.

This is the first parametric-integral step below the cycle-79 law-map handoff:
Mathlib's dominated derivative-under-integral theorem proves the sample-space
weak-test derivative, and `lawMapIntegralHasDerivAtOfSample` transports it to
the mapped law.  The EM path derivative, neighborhood, and domination data stay
explicit.
-/
theorem lawMapIntegralHasDerivAtOfDominated {Ω E : Type*}
    [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {X : ℝ → Ω → E} {φ : E → ℝ} {s0 g : ℝ}
    {sampleDeriv : ℝ → Ω → ℝ} {neighborhood : Set ℝ}
    {bound : Ω → ℝ}
    (hX : ∀ s, AEMeasurable (X s) P)
    (hφ : ∀ s, AEStronglyMeasurable φ (Measure.map (X s) P))
    (hneighborhood : neighborhood ∈ 𝓝 s0)
    (hFMeas :
      ∀ᶠ s in 𝓝 s0, AEStronglyMeasurable (fun ω => φ (X s ω)) P)
    (hFInt : Integrable (fun ω => φ (X s0 ω)) P)
    (hDerivMeas : AEStronglyMeasurable (sampleDeriv s0) P)
    (hDerivBound :
      ∀ᵐ ω ∂P, ∀ s ∈ neighborhood, ‖sampleDeriv s ω‖ ≤ bound ω)
    (hBoundInt : Integrable bound P)
    (hPathDeriv :
      ∀ᵐ ω ∂P, ∀ s ∈ neighborhood,
        HasDerivAt (fun t => φ (X t ω)) (sampleDeriv s ω) s)
    (hDerivValue : (∫ ω, sampleDeriv s0 ω ∂P) = g) :
    HasDerivAt (fun s => ∫ x, φ x ∂Measure.map (X s) P) g s0 := by
  have hsample :
      HasDerivAt (fun s => ∫ ω, φ (X s ω) ∂P)
        (∫ ω, sampleDeriv s0 ω ∂P) s0 :=
    (hasDerivAt_integral_of_dominated_loc_of_deriv_le
      (F := fun s ω => φ (X s ω))
      (F' := sampleDeriv)
      (x₀ := s0)
      (s := neighborhood)
      (bound := bound)
      (μ := P)
      hneighborhood hFMeas hFInt hDerivMeas hDerivBound hBoundInt
      hPathDeriv).2
  rw [hDerivValue] at hsample
  exact lawMapIntegralHasDerivAtOfSample (P := P) (X := X) (φ := φ) hX hφ hsample

/-- Named-law version of `lawMapIntegralHasDerivAtOfDominated`.

If a paper keeps a named law path `ρ s` with `ρ s = Measure.map (X s) P`,
this combines the dominated sample-space derivative-under-integral step with
the named-law equality rewrite.
-/
theorem lawIntegralHasDerivAtOfMeasureMapEqAndDominated {Ω E : Type*}
    [MeasurableSpace Ω] [MeasurableSpace E]
    {P : Measure Ω} {X : ℝ → Ω → E} {ρ : ℝ → Measure E}
    {φ : E → ℝ} {s0 g : ℝ}
    {sampleDeriv : ℝ → Ω → ℝ} {neighborhood : Set ℝ}
    {bound : Ω → ℝ}
    (hρ : ∀ s, ρ s = Measure.map (X s) P)
    (hX : ∀ s, AEMeasurable (X s) P)
    (hφ : ∀ s, AEStronglyMeasurable φ (ρ s))
    (hneighborhood : neighborhood ∈ 𝓝 s0)
    (hFMeas :
      ∀ᶠ s in 𝓝 s0, AEStronglyMeasurable (fun ω => φ (X s ω)) P)
    (hFInt : Integrable (fun ω => φ (X s0 ω)) P)
    (hDerivMeas : AEStronglyMeasurable (sampleDeriv s0) P)
    (hDerivBound :
      ∀ᵐ ω ∂P, ∀ s ∈ neighborhood, ‖sampleDeriv s ω‖ ≤ bound ω)
    (hBoundInt : Integrable bound P)
    (hPathDeriv :
      ∀ᵐ ω ∂P, ∀ s ∈ neighborhood,
        HasDerivAt (fun t => φ (X t ω)) (sampleDeriv s ω) s)
    (hDerivValue : (∫ ω, sampleDeriv s0 ω ∂P) = g) :
    HasDerivAt (fun s => ∫ x, φ x ∂ρ s) g s0 := by
  have hφMap :
      ∀ s, AEStronglyMeasurable φ (Measure.map (X s) P) := by
    intro s
    simpa [hρ s] using hφ s
  have hmap :
      HasDerivAt
        (fun s => ∫ x, φ x ∂Measure.map (X s) P) g s0 :=
    lawMapIntegralHasDerivAtOfDominated
      (P := P) (X := X) (φ := φ) (sampleDeriv := sampleDeriv)
      (neighborhood := neighborhood) (bound := bound)
      hX hφMap hneighborhood hFMeas hFInt hDerivMeas hDerivBound
      hBoundInt hPathDeriv hDerivValue
  have hfun :
      (fun s => ∫ x, φ x ∂ρ s) =
        fun s => ∫ x, φ x ∂Measure.map (X s) P := by
    funext s
    rw [hρ s]
  simpa [hfun] using hmap

/-- Pushforward-law equality for paired random variables from componentwise
almost-everywhere equality.

This is a narrow endpoint-law helper for stitched EM paths: once two endpoint
representatives agree almost everywhere component by component, their joint
pushforward law agrees.  It does not construct conditional laws, densities, or
Fokker--Planck backends.
-/
theorem lawMapProdEqOfAEEq {Ω E F : Type*} [MeasurableSpace Ω]
    [MeasurableSpace E] [MeasurableSpace F]
    {P : Measure Ω} {X X' : Ω → E} {Y Y' : Ω → F}
    (hX : X =ᵐ[P] X') (hY : Y =ᵐ[P] Y') :
    Measure.map (fun ω => (X ω, Y ω)) P =
      Measure.map (fun ω => (X' ω, Y' ω)) P := by
  exact Measure.map_congr <| by
    filter_upwards [hX, hY] with ω hx hy
    simp [hx, hy]

/-- First marginal of a paired pushforward law.

This is endpoint-law bookkeeping for common-space EM arguments: after a joint
endpoint law has been represented as a paired pushforward, projecting the first
coordinate recovers the first endpoint law.  Measurability is explicit; the
lemma does not construct any process, density, or conditional law.
-/
theorem lawMapProdFst {Ω E F : Type*} [MeasurableSpace Ω]
    [MeasurableSpace E] [MeasurableSpace F]
    {P : Measure Ω} {X : Ω → E} {Y : Ω → F}
    (hX : Measurable X) (hY : Measurable Y) :
    Measure.map Prod.fst (Measure.map (fun ω => (X ω, Y ω)) P) =
      Measure.map X P := by
  rw [Measure.map_map measurable_fst (hX.prod hY)]
  rfl

/-- Second marginal of a paired pushforward law.

This is the right-endpoint analogue of `lawMapProdFst`; it keeps marginal-law
extraction separate from the conditional-drift and Fokker--Planck obligations.
-/
theorem lawMapProdSnd {Ω E F : Type*} [MeasurableSpace Ω]
    [MeasurableSpace E] [MeasurableSpace F]
    {P : Measure Ω} {X : Ω → E} {Y : Ω → F}
    (hX : Measurable X) (hY : Measurable Y) :
    Measure.map Prod.snd (Measure.map (fun ω => (X ω, Y ω)) P) =
      Measure.map Y P := by
  rw [Measure.map_map measurable_snd (hX.prod hY)]
  rfl

/-- Swap the coordinate order of a paired pushforward law.

Mathlib conditional-distribution APIs usually represent the joint law for
`Y | X` in the order `(X,Y)`.  Some paper proofs first name the joint law in the
opposite order.  This helper records only the `Measure.map` orientation
bookkeeping; it does not construct a conditional law.
-/
theorem lawMapProdSwap {Ω E F : Type*} [MeasurableSpace Ω]
    [MeasurableSpace E] [MeasurableSpace F]
    {P : Measure Ω} {X : Ω → E} {Y : Ω → F}
    (hX : Measurable X) (hY : Measurable Y) :
    Measure.map Prod.swap (Measure.map (fun ω => (X ω, Y ω)) P) =
      Measure.map (fun ω => (Y ω, X ω)) P := by
  rw [Measure.map_map measurable_swap (hX.prod hY)]
  rfl

/-- Mathlib orientation bridge between `condDistrib` and `condExpKernel`.

For the SALD conditional drift, instantiate `Y` with `X_k^eta` and `X` with
`hat X_s`: the conditional distribution of `X_k^eta` given `hat X_s` agrees
almost everywhere with the conditional-expectation kernel mapped by `X_k^eta`.
This is a local theorem from Mathlib's conditional-kernel backend, not a weak
Fokker--Planck or KL differentiability result.
-/
theorem condDistribAeEqCondExpKernelMap {Ω β γ : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [StandardBorelSpace Ω] [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {X : Ω → β} {Y : Ω → γ}
    (hX : Measurable X) (hY : Measurable Y) {s : Set γ}
    (hs : MeasurableSet s) :
    (fun a => ProbabilityTheory.condDistrib Y X μ (X a) s) =ᵐ[μ]
      fun a =>
        (ProbabilityTheory.condExpKernel μ
            ((inferInstance : MeasurableSpace β).comap X)).map Y a s := by
  exact ProbabilityTheory.condDistrib_apply_ae_eq_condExpKernel_map
    (μ := μ) (X := Y) (Y := X) hY hX hs

/-- Sample-space component-version bridge from `condExpKernel.map` to
`condDistrib`.

For the SALD `condC` field, this isolates the remaining Mathlib-facing
boundary after `condDistrib` and `condExpKernel.map` have been aligned as
measure-valued kernels almost everywhere.  It turns a selected
`condExpKernel.map` version of the component field into the displayed
`condDistrib` integral equality after composing with `hat X_s`.  The theorem
does not prove the measure-valued kernel equality or choose the component
version; those remain the smaller conditional-kernel obligations.
-/
theorem condDistribIntegralSampleAeEqOfCondExpKernelMap {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace Ω] [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {X : Ω → β} {Y : Ω → γ}
    {f : β × γ → F} {field : β → F}
    (hkernel :
      (fun a => ProbabilityTheory.condDistrib Y X μ (X a)) =ᵐ[μ]
        fun a =>
          (ProbabilityTheory.condExpKernel μ
            ((inferInstance : MeasurableSpace β).comap X)).map Y a)
    (hfield :
      (fun a => ∫ y, f (X a, y)
          ∂(ProbabilityTheory.condExpKernel μ
            ((inferInstance : MeasurableSpace β).comap X)).map Y a) =ᵐ[μ]
        fun a => field (X a)) :
    (fun a => ∫ y, f (X a, y)
        ∂ProbabilityTheory.condDistrib Y X μ (X a)) =ᵐ[μ]
      fun a => field (X a) := by
  filter_upwards [hkernel, hfield] with a hka hfa
  rw [hka, hfa]

/-- Strong measurability of a vector-valued conditional integral against
`condDistrib`.

This packages the Mathlib theorem in the orientation used by the SALD
component fields: conditioning variable `X`, sampled variable `Y`, and an
integrand on `(X,Y)`.  It does not prove the EM interpolation law or any weak
Fokker--Planck identity.
-/
theorem condDistribIntegralAEStronglyMeasurable {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {X : Ω → β} {Y : Ω → γ}
    {f : β × γ → F}
    (hX : AEMeasurable X μ) (hY : AEMeasurable Y μ)
    (hf : AEStronglyMeasurable f (μ.map fun a => (X a, Y a))) :
    AEStronglyMeasurable
      (fun a => ∫ y, f (X a, y) ∂ProbabilityTheory.condDistrib Y X μ (X a))
      μ := by
  exact hf.integral_condDistrib hX hY

/-- Integrability of a vector-valued conditional integral against
`condDistrib`.

For SALD this is the Mathlib-local handoff needed to turn integrable frozen
drift summands into integrable component conditional fields before the
existing `bar b_{k,s}` regularity wrappers are used.
-/
theorem condDistribIntegralIntegrable {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {X : Ω → β} {Y : Ω → γ}
    {f : β × γ → F}
    (hX : AEMeasurable X μ) (hY : AEMeasurable Y μ)
    (hf : Integrable f (μ.map fun a => (X a, Y a))) :
    Integrable
      (fun a => ∫ y, f (X a, y) ∂ProbabilityTheory.condDistrib Y X μ (X a))
      μ := by
  exact hf.integral_condDistrib hX hY

/-- Strong measurability of the state-space conditional integral under the
conditioning law `μ.map X`.

This is the law-space version needed for the SALD named `hat rho_s` field:
Mathlib's `condDistrib` backend already gives measurability of
`x ↦ ∫ y, f (x,y) ∂condDistrib Y X μ x` under the marginal law of the
conditioning variable.  It does not choose a SALD-specific version of the
conditional component field.
-/
theorem condDistribIntegralMapAEStronglyMeasurable {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {X : Ω → β} {Y : Ω → γ}
    {f : β × γ → F}
    (hY : AEMeasurable Y μ)
    (hf : AEStronglyMeasurable f (μ.map fun a => (X a, Y a))) :
    AEStronglyMeasurable
      (fun x => ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x)
      (μ.map X) := by
  exact hf.integral_condDistrib_map hY

/-- Integrability of the state-space conditional integral under the
conditioning law `μ.map X`.

For SALD this is the Mathlib-local input that turns an integrable frozen
drift or score summand on the joint law of `(hat X_s, X_k^eta)` into an
integrable canonical conditional field under `hat rho_s = Law(hat X_s)`.
-/
theorem condDistribIntegralMapIntegrable {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {X : Ω → β} {Y : Ω → γ}
    {f : β × γ → F}
    (hY : AEMeasurable Y μ)
    (hf : Integrable f (μ.map fun a => (X a, Y a))) :
    Integrable
      (fun x => ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x)
      (μ.map X) := by
  exact hf.integral_condDistrib_map hY

/-- Disintegrate an integral through the `condDistrib` kernel.

For the SALD conditional drift in `appendix.tex:1368-1377`, instantiate `X`
with `hat X_s`, `Y` with `X_k^eta`, and `f` with the weak test-gradient
pairing against one frozen component.  This proves the map-law
conditional-integral identity behind the canonical `condDistrib` component
generator action; it does not prove the weak Fokker--Planck equation,
boundary integration by parts, or log-ratio admissibility.
-/
theorem condDistribIntegralMapIntegral {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {X : Ω → β} {Y : Ω → γ}
    {f : β × γ → F}
    (hX : AEMeasurable X μ) (hY : AEMeasurable Y μ)
    (hf : Integrable f (μ.map fun a => (X a, Y a))) :
    (∫ x, ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x
        ∂μ.map X) =
      ∫ a, f (X a, Y a) ∂μ := by
  have hcomp := ProbabilityTheory.compProd_map_condDistrib
    (μ := μ) (X := X) (Y := Y) (mβ := inferInstance) hY
  have hfComp :
      Integrable f ((μ.map X) ⊗ₘ ProbabilityTheory.condDistrib Y X μ) := by
    rw [hcomp]
    exact hf
  calc
    (∫ x, ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x
        ∂μ.map X)
        = ∫ z, f z ∂((μ.map X) ⊗ₘ
            ProbabilityTheory.condDistrib Y X μ) := by
          exact (Measure.integral_compProd
            (μ := μ.map X) (κ := ProbabilityTheory.condDistrib Y X μ)
            hfComp).symm
    _ = ∫ a, f (X a, Y a) ∂μ := by
          rw [hcomp]
          rw [integral_map (hX.prodMk hY) hf.1]

/-- Named-law variant of `condDistribIntegralMapIntegral`.

This is the paper-oriented form for `\hat\rho_s = Law(\hat X_s)`.
-/
theorem condDistribIntegralNamedLawIntegral {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {hatRho : Measure β}
    {X : Ω → β} {Y : Ω → γ} {f : β × γ → F}
    (hhatRho : hatRho = μ.map X)
    (hX : AEMeasurable X μ) (hY : AEMeasurable Y μ)
    (hf : Integrable f (μ.map fun a => (X a, Y a))) :
    (∫ x, ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x
        ∂hatRho) =
      ∫ a, f (X a, Y a) ∂μ := by
  rw [hhatRho]
  exact condDistribIntegralMapIntegral hX hY hf

/-- Named-law variant of `condDistribIntegralMapAEStronglyMeasurable`.

Instantiate `hatRho` with `Law(hat X_s)`, `X` with `hat X_s`, and `Y` with
`X_k^eta`.  The hypothesis `hatRho = μ.map X` is the paper's
`\hat\rho_s = Law(\hat X_s)` line.
-/
theorem condDistribIntegralNamedLawAEStronglyMeasurable {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {hatRho : Measure β}
    {X : Ω → β} {Y : Ω → γ} {f : β × γ → F}
    (hhatRho : hatRho = μ.map X)
    (hY : AEMeasurable Y μ)
    (hf : AEStronglyMeasurable f (μ.map fun a => (X a, Y a))) :
    AEStronglyMeasurable
      (fun x => ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x)
      hatRho := by
  rw [hhatRho]
  exact condDistribIntegralMapAEStronglyMeasurable hY hf

/-- Named-law variant of `condDistribIntegralMapIntegrable`. -/
theorem condDistribIntegralNamedLawIntegrable {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {hatRho : Measure β}
    {X : Ω → β} {Y : Ω → γ} {f : β × γ → F}
    (hhatRho : hatRho = μ.map X)
    (hY : AEMeasurable Y μ)
    (hf : Integrable f (μ.map fun a => (X a, Y a))) :
    Integrable
      (fun x => ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x)
      hatRho := by
  rw [hhatRho]
  exact condDistribIntegralMapIntegrable hY hf

/-- Versioning theorem for a named conditional-integral component field.

If a SALD component field such as `condC_{k,s}` or `condScore_{k,s}` is chosen
as a `hatRho`-a.e. version of the canonical `condDistrib` integral, then the
Mathlib law-space conditional-integral lemmas give the component's
measurability and integrability under the named law.  This is still a
conditional-kernel component theorem, not a weak Fokker--Planck theorem.
-/
theorem condDistribIntegralNamedFieldRegularity {Ω β γ F : Type*}
    [MeasurableSpace Ω] [MeasurableSpace β] [MeasurableSpace γ]
    [NormedAddCommGroup F] [NormedSpace ℝ F]
    [StandardBorelSpace γ] [Nonempty γ]
    {μ : Measure Ω} [IsFiniteMeasure μ] {hatRho : Measure β}
    {X : Ω → β} {Y : Ω → γ} {f : β × γ → F} {field : β → F}
    (hhatRho : hatRho = μ.map X)
    (hY : AEMeasurable Y μ)
    (hfMeas : AEStronglyMeasurable f (μ.map fun a => (X a, Y a)))
    (hfInt : Integrable f (μ.map fun a => (X a, Y a)))
    (hfield :
      (fun x => ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x)
        =ᵐ[hatRho] field) :
    AEStronglyMeasurable field hatRho ∧ Integrable field hatRho := by
  have hmeas :
      AEStronglyMeasurable
        (fun x => ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x)
        hatRho :=
    condDistribIntegralNamedLawAEStronglyMeasurable hhatRho hY hfMeas
  have hint :
      Integrable
        (fun x => ∫ y, f (x, y) ∂ProbabilityTheory.condDistrib Y X μ x)
        hatRho :=
    condDistribIntegralNamedLawIntegrable hhatRho hY hfInt
  exact ⟨hmeas.congr hfield, hint.congr hfield⟩

/-- A named probability measure or time-indexed law in a paper proof. -/
structure MeasureContract where
  name : String
  stateSpace : String
  densityName : String := ""
  smoothness : String := ""
  source : SourceAnchor
deriving Repr, DecidableEq

/-- Forward KL divergence contract `KL(rho || pi)`. -/
structure KLContract where
  rho : String
  pi : String
  expression : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.contractOnly
deriving Repr, DecidableEq

/-- Fisher information contract `FI(rho || pi)`. -/
structure FIContract where
  rho : String
  pi : String
  expression : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.contractOnly
deriving Repr, DecidableEq

/-- Log-Sobolev inequality contract. -/
structure LSIContract where
  measureName : String
  constantName : String
  statement : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.obligation
deriving Repr, DecidableEq

/-- Poincare inequality contract. -/
structure PIContract where
  measureName : String
  constantName : String
  statement : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.obligation
deriving Repr, DecidableEq

/-- Transport velocity field satisfying a continuity equation. -/
structure TransportVelocityContract where
  pathName : String
  velocityName : String
  continuityEquation : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.contractOnly
deriving Repr, DecidableEq

/-- Guide tilt `pi_t proportional to p_t exp(-F_t)`. -/
structure GuidedTiltContract where
  basePath : String
  guideName : String
  guidedPath : String
  terminalTarget : String
  source : SourceAnchor
  status : ProofStatus := ProofStatus.contractOnly
deriving Repr, DecidableEq

/-- Source-cited interface for the Donsker--Varadhan entropy duality formula.

This is data, not a proof.  It records the exact analytic shape needed by the
SALD paper before theorem-specific finite-log-mgf witnesses instantiate it.
-/
structure DvVariationalFormulaInterface where
  source : SourceAnchor
  probabilityMeasures : String
  klFunctional : String
  testFunctionClass : String
  finiteLogMgfPredicate : String
  logMgfFunctional : String
  variationalFunctional : String
  supremumStatement : String
  oneSidedConsequence : String
  oneSidedScalarBridge : String
  citation : String
  status : ProofStatus := ProofStatus.sourceCited
deriving Repr, DecidableEq

/-- Donsker--Varadhan variational formula as a cited-result contract. -/
def dvVariationalObligation (source : SourceAnchor) : ProofObligation where
  id := "probability.dv_variational_formula"
  statement := "KL(nu || mu) = sup_Z { E_nu[Z] - log E_mu[exp Z] } under the paper's integrability assumptions."
  source := source
  status := ProofStatus.sourceCited
  note := "Port from Mathlib/SLT or keep as cited analytic dependency until formalized."

/-- Precise source-cited DV interface matching `appendix.tex:73-79`.

Downstream proof obligations may depend on this interface only as a cited
analytic result until an actual Lean proof or imported theorem replaces it.
-/
def dvVariationalFormulaInterface (source : SourceAnchor) :
    DvVariationalFormulaInterface where
  source := source
  probabilityMeasures := "mu and nu are probability distributions on the same measurable space."
  klFunctional := "KL(nu || mu), with the paper's absolute-continuity and finite-entropy side conditions supplied by each theorem block."
  testFunctionClass := "real-valued measurable random variables Z on the common space."
  finiteLogMgfPredicate := "log E_mu[exp(Z)] < +infty."
  logMgfFunctional := "Z |-> log E_mu[exp(Z)]."
  variationalFunctional := "Z |-> E_nu[Z] - log E_mu[exp(Z)]."
  supremumStatement := "KL(nu || mu) = sup_Z { E_nu[Z] - log E_mu[exp(Z)] }, where the supremum is over finite-log-mgf tests."
  oneSidedConsequence := "For every admissible Z, E_nu[Z] <= KL(nu || mu) + log E_mu[exp(Z)]."
  oneSidedScalarBridge := "AutoSamplingTheory.dvVariationalOneSidedConsequenceScalar proves the real-order rearrangement from E_nu[Z] - logMgf <= KL to E_nu[Z] <= KL + logMgf; AutoSamplingTheory.dvVariationalOneSidedFromSupremumScalar additionally proves the scalar step from admissible-test membership plus the source supremum identity to that one-sided bound; AutoSamplingTheory.dvVariationalTiltedRightOneSidedConsequence combines the Mathlib tilted backend with the scalar rearrangement under explicit selected-test hypotheses."
  citation := "Boucheron, Lugosi, and Massart, Concentration Inequalities, Corollary 4.15, cited by SALD appendix.tex:73."
  status := ProofStatus.sourceCited

/-- Pointwise square identity for the LSI density test `phi = sqrt(r)`.

In the SALD source step `main_body.tex:208-215`, this is the local scalar
part of replacing `phi^2` by the Radon-Nikodym density ratio `r = rho/pi`.
The measure-theoretic density and integral transport remain separate
obligations.
-/
theorem lsiKlFiSqrtDensitySquareScalar {r : Real} (hr : 0 ≤ r) :
    (Real.sqrt r) ^ 2 = r := by
  exact Real.sq_sqrt hr

/-- Pointwise entropy-integrand rewrite for `phi = sqrt(r)`.

This proves only the scalar rewrite
`phi^2 log(phi^2) = r log r` after nonnegativity of the density ratio is
available.  Integrability, zero-density conventions, and the KL integral
identity are still analytic obligations.
-/
theorem lsiKlFiSqrtDensityEntropyIntegrandScalar {r : Real} (hr : 0 ≤ r) :
    (Real.sqrt r) ^ 2 * Real.log ((Real.sqrt r) ^ 2) = r * Real.log r := by
  rw [lsiKlFiSqrtDensitySquareScalar hr]

/-- Scalar normalization handoff for the LSI test `phi = sqrt(r)`.

After an integral backend has shown that the mass of `phi^2` equals the mass of
the density ratio `r`, probability normalization of `r` gives the LSI test
normalization.  This does not prove the integral equality itself.
-/
theorem lsiKlFiSqrtDensityNormalizationScalar {densityMass testMass : Real}
    (htest : testMass = densityMass)
    (hdensity : densityMass = 1) :
    testMass = 1 := by
  rw [htest, hdensity]

/-- Radon-Nikodym mass normalization for the LSI density ratio.

For probability measures `rho << pi`, the density ratio `d rho / d pi` has
unit `pi`-mass.  This is the measure-level backend behind the source line
`int phi^2 d pi = int (rho/pi) d pi = 1` before converting to real integrals.
-/
theorem lsiKlFiRnDerivLIntegralMassOne {α : Type*} [MeasurableSpace α]
    (rho pi : Measure α) [IsProbabilityMeasure rho] [IsProbabilityMeasure pi]
    (hrho_pi : rho ≪ pi) :
    ∫⁻ x, rho.rnDeriv pi x ∂pi = 1 := by
  rw [Measure.lintegral_rnDeriv hrho_pi]
  simp

/-- Real-integral normalization of the Radon-Nikodym density ratio.

This supplies the real mass input used by the scalar normalization bridge for
the LSI test `phi=sqrt(d rho/d pi)`.
-/
theorem lsiKlFiRnDerivDensityMassOne {α : Type*} [MeasurableSpace α]
    (rho pi : Measure α) [IsProbabilityMeasure rho] [IsProbabilityMeasure pi]
    (hrho_pi : rho ≪ pi) :
    ∫ x, (rho.rnDeriv pi x).toReal ∂pi = 1 := by
  rw [Measure.integral_toReal_rnDeriv hrho_pi]
  simp

/-- Normalization of the source LSI test `phi=sqrt(d rho/d pi)`.

This combines the pointwise square identity for the square-root density test
with the Radon-Nikodym mass theorem.  Smooth/admissible-test and approximation
requirements remain separate analytic obligations.
-/
theorem lsiKlFiSqrtRnDerivTestMassOne {α : Type*} [MeasurableSpace α]
    (rho pi : Measure α) [IsProbabilityMeasure rho] [IsProbabilityMeasure pi]
    (hrho_pi : rho ≪ pi) :
    ∫ x, (Real.sqrt ((rho.rnDeriv pi x).toReal)) ^ 2 ∂pi = 1 := by
  rw [← lsiKlFiRnDerivDensityMassOne rho pi hrho_pi]
  refine integral_congr_ae ?_
  filter_upwards with x
  exact Real.sq_sqrt ENNReal.toReal_nonneg

/-- Entropy transport from the density-ratio integral to the KL log-likelihood integral.

For `rho << pi`, Mathlib's log-likelihood-ratio backend identifies
`int (d rho/d pi) log(d rho/d pi) d pi` with the paper's KL integrand
`int log(d rho/d pi) d rho`.  Finite-KL assumptions for theorem use remain
explicit downstream.
-/
theorem lsiKlFiRnDerivEntropyIntegral {α : Type*} [MeasurableSpace α]
    (rho pi : Measure α) [IsProbabilityMeasure rho] [IsProbabilityMeasure pi]
    (hrho_pi : rho ≪ pi) :
    ∫ x, (rho.rnDeriv pi x).toReal * Real.log (rho.rnDeriv pi x).toReal ∂pi =
      ∫ x, llr rho pi x ∂rho := by
  exact integral_rnDeriv_mul_log hrho_pi

/-- Entropy transport for the square-root density test used by LSI.

This rewrites the LSI entropy integrand for
`phi=sqrt(d rho/d pi)` and then uses the Radon-Nikodym entropy transport
identity.  It still does not prove admissibility of `phi` or the Fisher
chain-rule side of `eq:LSI-KL-FI`.
-/
theorem lsiKlFiSqrtRnDerivEntropyIntegral {α : Type*} [MeasurableSpace α]
    (rho pi : Measure α) [IsProbabilityMeasure rho] [IsProbabilityMeasure pi]
    (hrho_pi : rho ≪ pi) :
    ∫ x, (Real.sqrt ((rho.rnDeriv pi x).toReal)) ^ 2 *
        Real.log ((Real.sqrt ((rho.rnDeriv pi x).toReal)) ^ 2) ∂pi =
      ∫ x, llr rho pi x ∂rho := by
  rw [← lsiKlFiRnDerivEntropyIntegral rho pi hrho_pi]
  refine integral_congr_ae ?_
  filter_upwards with x
  exact lsiKlFiSqrtDensityEntropyIntegrandScalar ENNReal.toReal_nonneg

/-- One-dimensional pointwise Fisher-chain coefficient for the LSI test.

For a positive density ratio `r`, the source substitution
`phi=sqrt(r)` has differential coefficient
`d phi = (2*sqrt(r))^{-1} d r`, while
`d log r = r^{-1} d r`.  This scalar lemma proves the resulting
`1/4` factor in the Fisher integrand.  The vector-gradient and integral
versions remain separate analytic obligations.
-/
theorem lsiKlFiSqrtDensityFisherChainScalar {r dr : Real} (hr : 0 < r) :
    ((1 / (2 * Real.sqrt r)) * dr) ^ 2 =
      (1 / 4) * (r * (dr / r) ^ 2) := by
  have hsqrt_sq : (Real.sqrt r) ^ 2 = r := Real.sq_sqrt (le_of_lt hr)
  have hsqrt_ne : Real.sqrt r ≠ 0 := ne_of_gt (Real.sqrt_pos.2 hr)
  have hr_ne : r ≠ 0 := ne_of_gt hr
  field_simp [hsqrt_ne, hr_ne]
  nlinarith [hsqrt_sq]

/-- Pointwise Fisher-chain handoff with named derivative identities.

This packages the scalar part of
`nabla sqrt(r) = (2*sqrt(r))^{-1} nabla r` and
`nabla log r = r^{-1} nabla r`.  It does not prove differentiability,
gradient existence, or the vector norm/integral transport backend.
-/
theorem lsiKlFiSqrtDensityFisherChainOfDerivativesScalar
    {r dr dSqrt dLog : Real}
    (hr : 0 < r)
    (hdSqrt : dSqrt = (1 / (2 * Real.sqrt r)) * dr)
    (hdLog : dLog = dr / r) :
    dSqrt ^ 2 = (1 / 4) * (r * dLog ^ 2) := by
  rw [hdSqrt, hdLog]
  exact lsiKlFiSqrtDensityFisherChainScalar hr

/-- Finite-coordinate Fisher-chain handoff for the LSI density test.

This lifts the pointwise scalar identity for `phi=sqrt(r)` to a finite sum of
coordinate-square terms.  It is still not the vector Sobolev chain rule or the
integral identity for Fisher information; those analytic backends must supply
the coordinate derivative identities and the later integral transport.
-/
theorem lsiKlFiSqrtDensityFisherChainFiniteSumScalar
    {ι : Type*} [Fintype ι] {r : Real} {dr dSqrt dLog : ι → Real}
    (hr : 0 < r)
    (hdSqrt : ∀ i, dSqrt i = (1 / (2 * Real.sqrt r)) * dr i)
    (hdLog : ∀ i, dLog i = dr i / r) :
    (∑ i, dSqrt i ^ 2) = (1 / 4) * (r * ∑ i, dLog i ^ 2) := by
  calc
    (∑ i, dSqrt i ^ 2) = ∑ i, (1 / 4) * (r * dLog i ^ 2) := by
      refine Finset.sum_congr rfl ?_
      intro i _hi
      rw [hdSqrt i, hdLog i]
      exact lsiKlFiSqrtDensityFisherChainScalar hr
    _ = ∑ i, ((1 / 4) * r) * dLog i ^ 2 := by
      refine Finset.sum_congr rfl ?_
      intro i _hi
      ring
    _ = ((1 / 4) * r) * ∑ i, dLog i ^ 2 := by
      rw [Finset.mul_sum]
    _ = (1 / 4) * (r * ∑ i, dLog i ^ 2) := by
      ring

/-- Finite-coordinate handoff to the Dirichlet/Fisher identity.

Once a density backend identifies the Dirichlet term with the finite coordinate
sum of `d sqrt(r)` squares and the Fisher term with
`r * sum_i (d log r_i)^2`, this lemma supplies the exact
`dirichlet = (1/4)*FI` input consumed by the existing LSI/KL/FI scalar bridge.
It does not construct the Radon--Nikodym density, prove differentiability, or
integrate the identity.
-/
theorem lsiKlFiSqrtDensityFisherChainFiniteSumHandoffScalar
    {ι : Type*} [Fintype ι] {r dirichlet fisher : Real}
    {dr dSqrt dLog : ι → Real}
    (hr : 0 < r)
    (hdirichlet : dirichlet = ∑ i, dSqrt i ^ 2)
    (hfisher : fisher = r * ∑ i, dLog i ^ 2)
    (hdSqrt : ∀ i, dSqrt i = (1 / (2 * Real.sqrt r)) * dr i)
    (hdLog : ∀ i, dLog i = dr i / r) :
    dirichlet = (1 / 4) * fisher := by
  rw [hdirichlet, hfisher]
  exact lsiKlFiSqrtDensityFisherChainFiniteSumScalar hr hdSqrt hdLog

/-- Integral handoff for the finite-coordinate Fisher chain rule.

After a Sobolev backend supplies coordinate derivative identities almost
everywhere for `sqrt(r)` and `log r`, this pushes the cycle-38 finite-sum
coefficient through the `pi`-integral.  It is still below the full
vector-gradient/Fisher-information theorem: integrability, coordinate-to-vector
gradient equivalence, zero-density handling, and admissibility of `sqrt(r)`
remain separate obligations.
-/
theorem lsiKlFiSqrtDensityFisherChainIntegralFiniteSum
    {α ι : Type*} [MeasurableSpace α] [Fintype ι] (mu : Measure α)
    {r : α → Real} {dr dSqrt dLog : ι → α → Real}
    (hr : ∀ᵐ x ∂mu, 0 < r x)
    (hdSqrt : ∀ᵐ x ∂mu,
      ∀ i, dSqrt i x = (1 / (2 * Real.sqrt (r x))) * dr i x)
    (hdLog : ∀ᵐ x ∂mu, ∀ i, dLog i x = dr i x / r x) :
    ∫ x, (∑ i, dSqrt i x ^ 2) ∂mu =
      ∫ x, (1 / 4) * (r x * ∑ i, dLog i x ^ 2) ∂mu := by
  refine integral_congr_ae ?_
  filter_upwards [hr, hdSqrt, hdLog] with x hx hSqrt hLog
  exact lsiKlFiSqrtDensityFisherChainFiniteSumScalar hx hSqrt hLog

/-- Scalar Dirichlet/Fisher handoff after the integral finite-sum identity.

This packages the exact `dirichlet=(1/4)*FI` input consumed by the existing
LSI/KL/FI scalar bridges when the analytic backend represents the Dirichlet
and Fisher quantities by finite-coordinate integrals.  It does not identify
those finite-coordinate integrals with the paper's vector-gradient quantities.
-/
theorem lsiKlFiSqrtDensityFisherChainIntegralHandoffScalar
    {α ι : Type*} [MeasurableSpace α] [Fintype ι] (mu : Measure α)
    {r : α → Real} {dirichlet fisher : Real} {dr dSqrt dLog : ι → α → Real}
    (hdirichlet : dirichlet = ∫ x, (∑ i, dSqrt i x ^ 2) ∂mu)
    (hfisher : fisher = ∫ x, (r x * ∑ i, dLog i x ^ 2) ∂mu)
    (hr : ∀ᵐ x ∂mu, 0 < r x)
    (hdSqrt : ∀ᵐ x ∂mu,
      ∀ i, dSqrt i x = (1 / (2 * Real.sqrt (r x))) * dr i x)
    (hdLog : ∀ᵐ x ∂mu, ∀ i, dLog i x = dr i x / r x) :
    dirichlet = (1 / 4) * fisher := by
  rw [hdirichlet, hfisher]
  rw [← integral_const_mul]
  exact lsiKlFiSqrtDensityFisherChainIntegralFiniteSum mu hr hdSqrt hdLog

/-- Scalar rearrangement behind the one-sided use of the cited DV formula.

This is not a proof of Donsker--Varadhan.  It starts after a cited or
eventually formalized entropy-duality theorem has supplied the variational
upper bound for an admissible test.
-/
theorem dvVariationalOneSidedConsequenceScalar {kl expectation logMgf : Real}
    (hvar : expectation - logMgf ≤ kl) :
    expectation ≤ kl + logMgf := by
  exact sub_le_iff_le_add.mp hvar

/-- Scalar supremum step behind the one-sided use of the cited DV formula.

This does not prove Donsker--Varadhan.  It starts after a cited or eventually
formalized theorem has identified `kl` with the supremum of the admissible
variational values, and after the selected test has been shown admissible.
-/
theorem dvVariationalOneSidedFromSupremumScalar {admissibleValues : Set Real}
    {kl expectation logMgf testValue : Real}
    (hbounded : BddAbove admissibleValues)
    (hmem : testValue ∈ admissibleValues)
    (hsup : sSup admissibleValues = kl)
    (htest : testValue = expectation - logMgf) :
    expectation ≤ kl + logMgf := by
  have htest_le_sup : testValue ≤ sSup admissibleValues := le_csSup hbounded hmem
  have hvar : expectation - logMgf ≤ kl := by
    rw [← htest, ← hsup]
    exact htest_le_sup
  exact dvVariationalOneSidedConsequenceScalar hvar

/-- Finite-log-mgf monotonicity for the scaled tests used before DV.

If the exponential moment for `alpha0 * q` is integrable under a finite
measure, then the exponential moment for `alpha * q` is integrable for
`0 <= alpha <= alpha0`.  In SALD this is the local Mathlib-backed part of
turning an `alpha0`-complexity assumption into the finite-log-mgf hypothesis
for a selected DV test; it is not a proof of the DV formula itself.
-/
theorem dvFiniteLogMgfOfLeAlpha {Ω : Type*} [MeasurableSpace Ω]
    {mu : Measure Ω} [IsFiniteMeasure mu]
    {q : Ω → Real} {alpha alpha0 : Real}
    (hAlpha0 : Integrable (fun x ↦ Real.exp (alpha0 * q x)) mu)
    (hAlpha_nonneg : 0 ≤ alpha) (hAlpha_le : alpha ≤ alpha0) :
    Integrable (fun x ↦ Real.exp (alpha * q x)) mu := by
  exact ProbabilityTheory.integrable_exp_mul_of_nonneg_of_le (X := q) (u := alpha0)
    (t := alpha) hAlpha0 hAlpha_nonneg hAlpha_le

/-- Mathlib-backed one-sided Donsker--Varadhan inequality via exponential tilting.

This proves only the admissible-test upper bound
`E_nu[Z] - log E_mu[exp Z] <= KL(nu || mu)` under explicit Mathlib
measure-theoretic hypotheses.  It is not the Boucheron supremum equality from
`appendix.tex:73-79`.
-/
theorem dvVariationalOneSidedOfTiltedRight {α : Type*} [MeasurableSpace α]
    (nu mu : Measure α) [IsProbabilityMeasure nu] [IsProbabilityMeasure mu]
    [SigmaFinite mu] [SigmaFinite nu]
    (Z : α → Real)
    (hnu_mu : nu ≪ mu)
    (hZ_nu : Integrable Z nu)
    (hexp_mu : Integrable (fun x ↦ Real.exp (Z x)) mu)
    (hllr : Integrable (llr nu mu) nu) :
    (∫ x, Z x ∂nu) - Real.log (∫ x, Real.exp (Z x) ∂mu) ≤
      (klDiv nu mu).toReal := by
  let : IsProbabilityMeasure (mu.tilted Z) := isProbabilityMeasure_tilted hexp_mu
  have hmu_tilted : mu ≪ mu.tilted Z := absolutelyContinuous_tilted hexp_mu
  have hnu_tilted : nu ≪ mu.tilted Z := hnu_mu.trans hmu_tilted
  have hllr_tilted : Integrable (llr nu (mu.tilted Z)) nu :=
    integrable_llr_tilted_right (μ := nu) (ν := mu) (f := Z) hnu_mu hZ_nu hllr
      hexp_mu
  have hnonneg := integral_llr_add_sub_measure_univ_nonneg (μ := nu) (ν := mu.tilted Z)
    hnu_tilted hllr_tilted
  have hnonneg_llr : 0 ≤ ∫ x, llr nu (mu.tilted Z) x ∂nu := by
    simpa using hnonneg
  have htilted :=
    integral_llr_tilted_right (μ := nu) (ν := mu) (f := Z) hnu_mu hZ_nu hexp_mu
      hllr
  have hnonneg_rewrite :
      0 ≤ (∫ x, llr nu mu x ∂nu) - (∫ x, Z x ∂nu) +
        Real.log (∫ x, Real.exp (Z x) ∂mu) := by
    simpa [htilted] using hnonneg_llr
  have hineq :
      (∫ x, Z x ∂nu) - Real.log (∫ x, Real.exp (Z x) ∂mu) ≤
        ∫ x, llr nu mu x ∂nu := by
    linarith
  have hkl : (klDiv nu mu).toReal = ∫ x, llr nu mu x ∂nu := by
    simpa using toReal_klDiv_of_measure_eq (μ := nu) (ν := mu) hnu_mu (by simp)
  simpa [hkl] using hineq

/-- One-sided DV inequality for a SALD-style scaled selected test.

This packages the theorem-instance side conditions for tests of the form
`Z = alpha * q`.  The `alpha0` exponential-moment assumption supplies the
finite-log-mgf hypothesis by `dvFiniteLogMgfOfLeAlpha`, and the remaining
absolute-continuity, selected-test integrability, and log-likelihood
integrability hypotheses are kept explicit.  The Boucheron supremum equality
from `appendix.tex:73-79` remains source-cited.
-/
theorem dvVariationalOneSidedOfScaledTest {Ω : Type*} [MeasurableSpace Ω]
    (nu mu : Measure Ω) [IsProbabilityMeasure nu] [IsProbabilityMeasure mu]
    [SigmaFinite mu] [SigmaFinite nu]
    (q : Ω → Real) {alpha alpha0 : Real}
    (hAlpha_nonneg : 0 ≤ alpha) (hAlpha_le : alpha ≤ alpha0)
    (hnu_mu : nu ≪ mu)
    (hZ_nu : Integrable (fun x ↦ alpha * q x) nu)
    (hexp_alpha0_mu : Integrable (fun x ↦ Real.exp (alpha0 * q x)) mu)
    (hllr : Integrable (llr nu mu) nu) :
    (∫ x, alpha * q x ∂nu) - Real.log (∫ x, Real.exp (alpha * q x) ∂mu) ≤
      (klDiv nu mu).toReal := by
  have hexp_mu : Integrable (fun x ↦ Real.exp (alpha * q x)) mu :=
    dvFiniteLogMgfOfLeAlpha (mu := mu) (q := q) hexp_alpha0_mu hAlpha_nonneg
      hAlpha_le
  exact dvVariationalOneSidedOfTiltedRight (nu := nu) (mu := mu)
    (Z := fun x ↦ alpha * q x) hnu_mu hZ_nu hexp_mu hllr

/-- Energy form of the one-sided DV bound for a scaled selected test.

For SALD use sites, `q` is a squared velocity or residual norm.  This theorem
starts after the selected-test hypotheses have been supplied, applies the
compiled one-sided backend for `Z=alpha*q`, divides by `alpha > 0`, and
rewrites the log-mgf quotient as the supplied alpha-complexity density
`eAlpha`.  The Boucheron supremum equality from `appendix.tex:73-79` remains
source-cited.
-/
theorem dvVariationalScaledTestEnergyBound {Ω : Type*} [MeasurableSpace Ω]
    (nu mu : Measure Ω) [IsProbabilityMeasure nu] [IsProbabilityMeasure mu]
    [SigmaFinite mu] [SigmaFinite nu]
    (q : Ω → Real) {alpha alpha0 eAlpha : Real}
    (hAlpha_pos : 0 < alpha) (hAlpha_le : alpha ≤ alpha0)
    (hnu_mu : nu ≪ mu)
    (hq_nu : Integrable q nu)
    (hexp_alpha0_mu : Integrable (fun x ↦ Real.exp (alpha0 * q x)) mu)
    (hllr : Integrable (llr nu mu) nu)
    (heAlpha : eAlpha =
      alpha⁻¹ * Real.log (∫ x, Real.exp (alpha * q x) ∂mu)) :
    (∫ x, q x ∂nu) ≤ alpha⁻¹ * (klDiv nu mu).toReal + eAlpha := by
  have hZ_nu : Integrable (fun x ↦ alpha * q x) nu := by
    simpa [smul_eq_mul] using hq_nu.const_mul alpha
  have hdv := dvVariationalOneSidedOfScaledTest (nu := nu) (mu := mu)
    (q := q) hAlpha_pos.le hAlpha_le hnu_mu hZ_nu hexp_alpha0_mu hllr
  have hscaledIntegral :
      (∫ x, alpha * q x ∂nu) = alpha * ∫ x, q x ∂nu := by
    rw [integral_const_mul]
  have hscaled :
      alpha * (∫ x, q x ∂nu) ≤
        (klDiv nu mu).toReal + Real.log (∫ x, Real.exp (alpha * q x) ∂mu) := by
    have hvar :
        alpha * (∫ x, q x ∂nu) -
            Real.log (∫ x, Real.exp (alpha * q x) ∂mu) ≤
          (klDiv nu mu).toReal := by
      simpa [hscaledIntegral] using hdv
    exact sub_le_iff_le_add.mp hvar
  have hdiv :
      alpha⁻¹ * (alpha * (∫ x, q x ∂nu)) ≤
        alpha⁻¹ * ((klDiv nu mu).toReal +
          Real.log (∫ x, Real.exp (alpha * q x) ∂mu)) := by
    exact mul_le_mul_of_nonneg_left hscaled (inv_nonneg.mpr hAlpha_pos.le)
  calc
    (∫ x, q x ∂nu) = alpha⁻¹ * (alpha * (∫ x, q x ∂nu)) := by
      field_simp [ne_of_gt hAlpha_pos]
    _ ≤ alpha⁻¹ * ((klDiv nu mu).toReal +
          Real.log (∫ x, Real.exp (alpha * q x) ∂mu)) := hdiv
    _ = alpha⁻¹ * (klDiv nu mu).toReal + eAlpha := by
      rw [heAlpha]
      ring

/-- Coefficient-preserving energy form of the selected scaled-test DV bound.

This is the local algebraic shape used before Gronwall in SALD proofs after a
nonnegative prefactor, such as `(1/2)*dot{s}(t)^(-1)`, multiplies the
post-DV energy estimate.
-/
theorem dvVariationalScaledTestEnergyBoundWithCoeff {Ω : Type*} [MeasurableSpace Ω]
    (nu mu : Measure Ω) [IsProbabilityMeasure nu] [IsProbabilityMeasure mu]
    [SigmaFinite mu] [SigmaFinite nu]
    (q : Ω → Real) {alpha alpha0 eAlpha coeff : Real}
    (hAlpha_pos : 0 < alpha) (hAlpha_le : alpha ≤ alpha0)
    (hcoeff : 0 ≤ coeff)
    (hnu_mu : nu ≪ mu)
    (hq_nu : Integrable q nu)
    (hexp_alpha0_mu : Integrable (fun x ↦ Real.exp (alpha0 * q x)) mu)
    (hllr : Integrable (llr nu mu) nu)
    (heAlpha : eAlpha =
      alpha⁻¹ * Real.log (∫ x, Real.exp (alpha * q x) ∂mu)) :
    coeff * (∫ x, q x ∂nu) ≤
      (coeff * alpha⁻¹) * (klDiv nu mu).toReal + coeff * eAlpha := by
  have hbase := dvVariationalScaledTestEnergyBound (nu := nu) (mu := mu)
    (q := q) hAlpha_pos hAlpha_le hnu_mu hq_nu hexp_alpha0_mu hllr heAlpha
  have hmul :
      coeff * (∫ x, q x ∂nu) ≤
        coeff * (alpha⁻¹ * (klDiv nu mu).toReal + eAlpha) := by
    exact mul_le_mul_of_nonneg_left hbase hcoeff
  calc
    coeff * (∫ x, q x ∂nu) ≤
        coeff * (alpha⁻¹ * (klDiv nu mu).toReal + eAlpha) := hmul
    _ = (coeff * alpha⁻¹) * (klDiv nu mu).toReal + coeff * eAlpha := by
      ring

/-- One-sided Donsker--Varadhan consequence from the tilted backend.

This is the form consumed by SALD after a selected test has supplied the
explicit Mathlib hypotheses.  It remains a one-sided theorem only; the
Boucheron supremum equality in `appendix.tex:73-79` stays source-cited.
-/
theorem dvVariationalTiltedRightOneSidedConsequence {α : Type*} [MeasurableSpace α]
    (nu mu : Measure α) [IsProbabilityMeasure nu] [IsProbabilityMeasure mu]
    [SigmaFinite mu] [SigmaFinite nu]
    (Z : α → Real)
    (hnu_mu : nu ≪ mu)
    (hZ_nu : Integrable Z nu)
    (hexp_mu : Integrable (fun x ↦ Real.exp (Z x)) mu)
    (hllr : Integrable (llr nu mu) nu) :
    (∫ x, Z x ∂nu) ≤
      (klDiv nu mu).toReal + Real.log (∫ x, Real.exp (Z x) ∂mu) := by
  exact dvVariationalOneSidedConsequenceScalar
    (dvVariationalOneSidedOfTiltedRight (nu := nu) (mu := mu) (Z := Z)
      hnu_mu hZ_nu hexp_mu hllr)

/-- Log-Sobolev implies KL-FI comparison as a reusable proof target. -/
def lsiToKlFiObligation (source : SourceAnchor) : ProofObligation where
  id := "probability.lsi_to_kl_fi"
  statement := "If pi satisfies LSI with constant c_LSI, then KL(rho || pi) <= FI(rho || pi)/(2*c_LSI)."
  source := source
  status := ProofStatus.obligation

end AutoSamplingTheory
