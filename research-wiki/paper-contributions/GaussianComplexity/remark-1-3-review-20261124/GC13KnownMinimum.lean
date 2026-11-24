import GC13Geometry
import GC13Normalizable
import GC41LowerBound

/-! Remark 1.3: restriction of an adaptive value-and-gradient algorithm on
strongly log-concave Gibbs targets to the centered Gaussian inputs, preserving
the deterministic query budget, seed, exact replies and disclosed minimizer. -/
noncomputable section
open MeasureTheory InnerProductSpace
open scoped ENNReal
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarConditional (E)
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarPosterior (precisionReply)
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FirstOrderIndistinguishability
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HiddenEigenbasis
open AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle (run)
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass

universe u v
variable {d : ℕ} {Seed : Type u} {State : Type v} [MeasurableSpace Seed] [MeasurableSpace State]

/-- Twice continuously differentiable potentials with the specified matrix Hessian bounds.
The disclosed point is a global minimizer. -/
structure PotentialInput (κ : ℝ) (V : E d → ℝ) (z : E d) : Prop where
  smooth : ContDiff ℝ 2 V
  curvature : ∀ x v : E d, ‖v‖^2 ≤ inner ℝ v (fderiv ℝ (gradient V) x v) ∧
    inner ℝ v (fderiv ℝ (gradient V) x v) ≤ κ * ‖v‖^2
  minimizes : ∀ x, V z ≤ V x

/-- The target law is a probability for every input satisfying the analytic class definition. -/
theorem PotentialInput.target_probability {κ : ℝ} {V : E d → ℝ} {z : E d}
    (h : PotentialInput κ V z) : IsProbabilityMeasure (gibbsLaw V) := by
  have hz := gibbsMass_of_hessian_lower h.smooth (fun x v => (h.curvature x v).1) z h.minimizes
  exact gibbsLaw_probability hz.1.ne' hz.2

def potentialOutputLaw (ρ : Measure Seed) (alg : Algorithm d Seed State) (q : ℕ)
    (V : E d → ℝ) : Measure (E d) :=
  ρ.map fun s => alg.output (run alg.next alg.update (fun x => (V x,gradient V x)) q (alg.start s)).1.1

/-- Choosing the algorithm after seeing z allows arbitrary use of the disclosed minimizer. -/
def FeasibleWithKnownMin (d : ℕ) (κ ε : ℝ) (q : ℕ) : Prop :=
  ∃ (Seed : Type u) (State : Type v) (_ : MeasurableSpace Seed) (_ : MeasurableSpace State)
    (ρ : Measure Seed) (_ : IsProbabilityMeasure ρ) (algs : E d → Algorithm d Seed State),
    ∀ (V : E d → ℝ) (z : E d), PotentialInput κ V z →
      eventTV (potentialOutputLaw ρ (algs z) q V) (gibbsLaw V) ≤ ε

def knownMinQueryComplexity (d : ℕ) (κ ε : ℝ) : ℝ≥0∞ :=
  ⨅ t : {q : ℕ // FeasibleWithKnownMin.{u,v} d κ ε q}, (t.val : ℝ≥0∞)

theorem quadratic_input {κ : ℝ} {A : Precision d} (ha : Admissible κ A) :
    PotentialInput κ (quadraticPotential A) 0 :=
  ⟨quadratic_contDiff A, quadratic_hessian_bounds ha, quadratic_minimizer_zero ha⟩

theorem quadratic_outputLaw {κ : ℝ} {A : Precision d} (ha : Admissible κ A)
    (ρ : Measure Seed) (alg : Algorithm d Seed State) (q : ℕ) :
    potentialOutputLaw ρ alg q (quadraticPotential A) = alg.outputLaw ρ q A := by
  unfold potentialOutputLaw
  rw [funext (quadratic_reply_eq_precisionReply ha.1)]
  rfl

theorem gaussian_budget_of_known_min {d q : ℕ} {κ ε : ℝ} (hf : FeasibleWithKnownMin.{u,v} d κ ε q) :
    FeasibleBudget.{u,v} d κ ε q := by
  obtain ⟨S,T,mS,mT,ρ,hρ,algs,h⟩ := hf
  refine ⟨S,T,mS,mT,ρ,hρ,algs 0, ?_⟩
  intro A ha
  have hV := h (quadraticPotential A) 0 (quadratic_input ha)
  rw [quadratic_outputLaw ha] at hV
  have he : targetLaw A = gibbsLaw (quadraticPotential A) := targetLaw_eq_gibbs ha
  rwa [he]

/-- A successful budget on the larger class with a known minimizer is a successful
budget on the whole centered Gaussian class, where every matrix has minimizer zero. -/
theorem gaussian_le_known_min (d : ℕ) (κ ε : ℝ) :
    gaussianQueryComplexity.{u,v} d κ ε ≤ knownMinQueryComplexity.{u,v} d κ ε := by
  apply le_iInf
  intro t
  exact iInf_le (fun x : {q : ℕ // FeasibleBudget.{u,v} d κ ε q} => (x.val : ℝ≥0∞))
    ⟨t.val,gaussian_budget_of_known_min t.property⟩

theorem known_min_query_bound {d : ℕ} {κ ε : ℝ} (hd : 1 ≤ d) (hκ : 4 ≤ κ)
    (hε : 0 < ε) (he : ε ≤ 1/16) :
    ENNReal.ofReal ((1/256 : ℝ) * min (d : ℝ)
      (Real.sqrt κ * Real.log (1 + (d : ℝ)/(Real.sqrt κ * ε)))) ≤
      knownMinQueryComplexity.{u,v} d κ ε :=
  (gaussian_query_complexity_lower_bound hd hκ hε he).trans (gaussian_le_known_min ..)

theorem known_min_query_bound_general_condition {δ : ℝ} (hδ : 0 < δ) (hlt : δ < 1) :
    ∃ d₀ : ℕ, ∀ d ≥ d₀, ∀ κ : ℝ, 2 ≤ κ → κ ≤ (d : ℝ)^(1-δ) →
      ∀ ε : ℝ, 0 < ε → ε ≤ 1/10 →
      ENNReal.ofReal (δ/256 * Real.sqrt κ * Real.log (d : ℝ)) ≤
        knownMinQueryComplexity.{u,v} d κ ε := by
  obtain ⟨D,hD⟩ := gaussian_query_lower_bound_with_disclosed_spectrum.{u,v} hδ hlt
  exact ⟨D,fun d hd κ hk hc ε he he' => (hD d hd κ hk hc ε he he').2.trans (gaussian_le_known_min ..)⟩

#print axioms gaussian_le_known_min
#print axioms known_min_query_bound
#print axioms known_min_query_bound_general_condition
end AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass
