import AutoSamplingTheory.TechnicalLemmas.StochasticProcesses.CarreDuChamp
import Mathlib.Analysis.Calculus.Deriv.Basic

/-!
# Diffusion chain rule for the carré du champ

Chewi Definition 2.2.13 characterizes diffusion semigroups by the scalar
functional-calculus identity

`Γ(φ ∘ f, g) = φ'(f) Γ(f,g)`.

The source quantifies over `φ : ℝ → ℝ` and writes its derivative `φ'` directly.
Lean cannot use that notation without derivative data, so this module keeps `φ`
arbitrary and makes the derivative field explicit via pointwise `HasDerivAt`
witnesses.  It does not impose a stronger global smoothness class that is not
stated in Definition 2.2.13.

Samplinglib's `CarreDuChamp.carreDuChamp` is intentionally a total algebraic
function, whereas the source statement is made on the domain of `Γ`.  This
module therefore keeps an explicit observable domain and records the scalar
composition closure needed to read the source identity on that domain.

The generator-form identity

`L (φ ∘ f) = φ'(f) L f + φ''(f) Γ(f,f)`

is not bundled into this interface.  Chewi states it as an equivalent
formulation and leaves the equivalence to Exercise 2.8; formalizing that
transport is a separate theorem cell.
-/

namespace AutoSamplingTheory
namespace TechnicalLemmas
namespace StochasticProcesses
namespace DiffusionChainRule

open Set

noncomputable section

/-- Source-normalized form of Chewi Definition 2.2.13 / Eq. (2.2.14).

`domain` is the declared domain on which the carré-du-champ calculus is meant
to be used.  Since the source writes `φ'` without separately formalizing its
domain, the Lean statement represents that derivative by an explicit function
`phiPrime` together with `HasDerivAt phi (phiPrime r) r` at every real `r`.

The property also records scalar-composition closure of the declared
observable domain.  No second-derivative generator identity is assumed here. -/
structure DiffusionChainRuleOn
    {X : Type*}
    (generator : (X → ℝ) →ₗ[ℝ] (X → ℝ))
    (domain : Set (X → ℝ)) : Prop where
  comp_mem :
    ∀ {f : X → ℝ}, f ∈ domain →
      ∀ {phi phiPrime : ℝ → ℝ},
        (∀ r : ℝ, HasDerivAt phi (phiPrime r) r) →
        (phi ∘ f) ∈ domain
  chain_rule :
    ∀ {f : X → ℝ}, f ∈ domain →
      ∀ {g : X → ℝ}, g ∈ domain →
        ∀ {phi phiPrime : ℝ → ℝ},
          (∀ r : ℝ, HasDerivAt phi (phiPrime r) r) →
          CarreDuChamp.carreDuChamp generator (phi ∘ f) g =
            fun x =>
              phiPrime (f x) *
                CarreDuChamp.carreDuChamp generator f g x

/-- Scalar functional calculus stays inside the declared carré-du-champ
domain whenever the derivative field appearing in the source formula exists. -/
theorem comp_mem
    {X : Type*}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {domain : Set (X → ℝ)}
    (h : DiffusionChainRuleOn generator domain)
    {f : X → ℝ} (hf : f ∈ domain)
    {phi phiPrime : ℝ → ℝ}
    (hphi : ∀ r : ℝ, HasDerivAt phi (phiPrime r) r) :
    (phi ∘ f) ∈ domain :=
  h.comp_mem hf hphi

/-- Function-valued form of the source chain rule
`Γ(φ ∘ f,g) = φ'(f) Γ(f,g)`. -/
theorem carreDuChamp_comp_left
    {X : Type*}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {domain : Set (X → ℝ)}
    (h : DiffusionChainRuleOn generator domain)
    {f g : X → ℝ} (hf : f ∈ domain) (hg : g ∈ domain)
    {phi phiPrime : ℝ → ℝ}
    (hphi : ∀ r : ℝ, HasDerivAt phi (phiPrime r) r) :
    CarreDuChamp.carreDuChamp generator (phi ∘ f) g =
      fun x =>
        phiPrime (f x) * CarreDuChamp.carreDuChamp generator f g x :=
  h.chain_rule hf hg hphi

/-- Pointwise extraction of the diffusion chain rule. -/
theorem carreDuChamp_comp_left_apply
    {X : Type*}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {domain : Set (X → ℝ)}
    (h : DiffusionChainRuleOn generator domain)
    {f g : X → ℝ} (hf : f ∈ domain) (hg : g ∈ domain)
    {phi phiPrime : ℝ → ℝ}
    (hphi : ∀ r : ℝ, HasDerivAt phi (phiPrime r) r)
    (x : X) :
    CarreDuChamp.carreDuChamp generator (phi ∘ f) g x =
      phiPrime (f x) * CarreDuChamp.carreDuChamp generator f g x := by
  exact congrFun (carreDuChamp_comp_left h hf hg hphi) x

/-- Self-pairing specialization `Γ(φ ∘ f,f) = φ'(f) Γ(f,f)`. -/
theorem carreDuChamp_comp_self
    {X : Type*}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {domain : Set (X → ℝ)}
    (h : DiffusionChainRuleOn generator domain)
    {f : X → ℝ} (hf : f ∈ domain)
    {phi phiPrime : ℝ → ℝ}
    (hphi : ∀ r : ℝ, HasDerivAt phi (phiPrime r) r) :
    CarreDuChamp.carreDuChamp generator (phi ∘ f) f =
      fun x =>
        phiPrime (f x) * CarreDuChamp.carreDuChamp generator f f x :=
  carreDuChamp_comp_left h hf hf hphi

/-- The exact scalar-composition specialization consumed in the proof of
Chewi Theorem 8.3.1:

`Γ(f' ∘ ρ, ρ) = f''(ρ) Γ(ρ,ρ)`.

Here `fPrime` and `fSecond` are explicit first- and second-derivative fields;
this theorem only uses the fact that `fSecond` is the derivative of `fPrime`.
It does not assume or prove the generator-form diffusion identity. -/
theorem carreDuChamp_fPrime_comp_self_apply
    {X : Type*}
    {generator : (X → ℝ) →ₗ[ℝ] (X → ℝ)}
    {domain : Set (X → ℝ)}
    (h : DiffusionChainRuleOn generator domain)
    {rho : X → ℝ} (hrho : rho ∈ domain)
    {fPrime fSecond : ℝ → ℝ}
    (hfPrime : ∀ r : ℝ, HasDerivAt fPrime (fSecond r) r)
    (x : X) :
    CarreDuChamp.carreDuChamp generator (fPrime ∘ rho) rho x =
      fSecond (rho x) *
        CarreDuChamp.carreDuChamp generator rho rho x := by
  exact carreDuChamp_comp_left_apply h hrho hrho hfPrime x

end

end DiffusionChainRule
end StochasticProcesses
end TechnicalLemmas
end AutoSamplingTheory
