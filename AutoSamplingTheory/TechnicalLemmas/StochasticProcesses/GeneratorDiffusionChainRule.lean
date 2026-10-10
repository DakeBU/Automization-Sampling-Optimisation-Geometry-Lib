import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# Generator form of the diffusion chain rule

Immediately after Chewi Definition 2.2.13, Eq. (2.2.15) gives the equivalent
source formulation

`L (φ ∘ f) = φ'(f) L f + φ''(f) Γ(f,f)`.

The source definition quantifies over scalar maps `φ : ℝ → ℝ` and writes the
first and second derivatives directly; it does not explicitly add a global
`ContDiff` hypothesis there.  Lean cannot use paper derivative notation without
data, so this module keeps `φ` arbitrary and makes the named derivative fields
explicit through pointwise `HasDerivAt` witnesses for `φ` and `φ'`.

Chewi leaves the equivalence between this identity and the carré-du-champ
composition rule Eq. (2.2.14) to Exercise 2.8.  This module therefore records
the generator formulation as its own explicit property.  It does not derive it
from `DiffusionChainRuleOn` and does not claim the Exercise 2.8 equivalence.

As in the carré-du-champ formulation, Samplinglib keeps the observable domain
explicit because the underlying Lean functions `generator` and
`carreDuChamp` are total even when the mathematical operator domain is not.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace GeneratorDiffusionChainRule

open Set

noncomputable section

/-- Source-normalized generator form of Chewi Eq. (2.2.15).

For every observable `f` in `domain`, scalar map `phi`, and explicit first and
second derivative fields `phiPrime` and `phiSecond`, scalar functional calculus
stays in the domain and

`L(phi ∘ f) = phiPrime(f) Lf + phiSecond(f) Gamma(f,f)`.

The two pointwise derivative families are the Lean representation of the
paper's `phi'` and `phi''` notation; no stronger global smoothness class is
silently added. -/
structure GeneratorDiffusionChainRuleOn
    {X : Type*}
    (generator : (X → ℝ) →ₗ[ℝ] (X → ℝ))
    (domain : Set (X → ℝ)) : Prop where
  comp_mem :
    ∀ {f : X → ℝ}, f ∈ domain →
      ∀ {phi phiPrime phiSecond : ℝ → ℝ},
        (∀ r : ℝ, HasDerivAt phi (phiPrime r) r) →
        (∀ r : ℝ, HasDerivAt phiPrime (phiSecond r) r) →
        (phi ∘ f) ∈ domain
  chain_rule :
    ∀ {f : X → ℝ}, f ∈ domain →
      ∀ {phi phiPrime phiSecond : ℝ → ℝ},
        (∀ r : ℝ, HasDerivAt phi (phiPrime r) r) →
        (∀ r : ℝ, HasDerivAt phiPrime (phiSecond r) r) →
        generator (phi ∘ f) =
          fun x =>
            phiPrime (f x) * generator f x +
              phiSecond (f x) *
                CarreDuChamp.carreDuChamp generator f f x

/-- Scalar functional calculus stays inside the declared generator domain when
the first and second derivative fields appearing in the source formula exist. -/
theorem comp_mem
    {X : Type*}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {domain : Set (X → ℝ)}
    (h : GeneratorDiffusionChainRuleOn generator domain)
    {f : X → ℝ} (hf : f ∈ domain)
    {phi phiPrime phiSecond : ℝ → ℝ}
    (hphiPrime : ∀ r : ℝ, HasDerivAt phi (phiPrime r) r)
    (hphiSecond : ∀ r : ℝ, HasDerivAt phiPrime (phiSecond r) r) :
    (phi ∘ f) ∈ domain :=
  h.comp_mem hf hphiPrime hphiSecond

/-- Function-valued generator diffusion chain rule from Chewi Eq. (2.2.15). -/
theorem generator_comp_eq
    {X : Type*}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {domain : Set (X → ℝ)}
    (h : GeneratorDiffusionChainRuleOn generator domain)
    {f : X → ℝ} (hf : f ∈ domain)
    {phi phiPrime phiSecond : ℝ → ℝ}
    (hphiPrime : ∀ r : ℝ, HasDerivAt phi (phiPrime r) r)
    (hphiSecond : ∀ r : ℝ, HasDerivAt phiPrime (phiSecond r) r) :
    generator (phi ∘ f) =
      fun x =>
        phiPrime (f x) * generator f x +
          phiSecond (f x) *
            CarreDuChamp.carreDuChamp generator f f x :=
  h.chain_rule hf hphiPrime hphiSecond

/-- Pointwise extraction of the generator diffusion chain rule. -/
theorem generator_comp_apply_eq
    {X : Type*}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {domain : Set (X → ℝ)}
    (h : GeneratorDiffusionChainRuleOn generator domain)
    {f : X → ℝ} (hf : f ∈ domain)
    {phi phiPrime phiSecond : ℝ → ℝ}
    (hphiPrime : ∀ r : ℝ, HasDerivAt phi (phiPrime r) r)
    (hphiSecond : ∀ r : ℝ, HasDerivAt phiPrime (phiSecond r) r)
    (x : X) :
    generator (phi ∘ f) x =
      phiPrime (f x) * generator f x +
        phiSecond (f x) *
          CarreDuChamp.carreDuChamp generator f f x := by
  exact congrFun (generator_comp_eq h hf hphiPrime hphiSecond) x

/-- Paper-shaped alias emphasizing that `phiPrime` and `phiSecond` are the
named derivative fields appearing in Eq. (2.2.15). -/
theorem generator_comp_apply_eq_of_named_derivatives
    {X : Type*}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {domain : Set (X → ℝ)}
    (h : GeneratorDiffusionChainRuleOn generator domain)
    {f : X → ℝ} (hf : f ∈ domain)
    {phi phiPrime phiSecond : ℝ → ℝ}
    (hphiPrime : ∀ r : ℝ, HasDerivAt phi (phiPrime r) r)
    (hphiSecond : ∀ r : ℝ, HasDerivAt phiPrime (phiSecond r) r)
    (x : X) :
    generator (phi ∘ f) x =
      phiPrime (f x) * generator f x +
        phiSecond (f x) *
          CarreDuChamp.carreDuChamp generator f f x :=
  generator_comp_apply_eq h hf hphiPrime hphiSecond x

end

end GeneratorDiffusionChainRule
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
