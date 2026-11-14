import Tests.GaussianComplexityFixedSpectrumCosineExpansion
import Lean

open scoped BigOperators
open Filter
open Lean Elab Command Meta

namespace FreshSourceKernelReview

def ExpectedProducer : Prop :=
∀ {κ : ℝ} (hκ : 2 ≤ κ),
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  (∀ θ : ℝ,
    2 / (κ + 1 + (κ - 1) * Real.cos θ) =
      (1 / Real.sqrt κ) *
        (1 + 2 * ∑' j : ℕ, (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ))) ∧
  (∀ θ : ℝ,
    Summable (fun j : ℕ => ‖(-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ)‖)) ∧
  TendstoUniformly
    (fun N : ℕ => fun θ : ℝ =>
      ∑ j ∈ Finset.range N, (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ))
    (fun θ : ℝ => ∑' j : ℕ, (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ))
    atTop

def ExpectedConsumer : Prop :=
∀ {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ) (n : ℕ),
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  (∑ i : Fin d, Real.cos ((n : ℝ) * θ i) / eigenvalue i) =
    (1 / Real.sqrt κ) *
      ((∑ i : Fin d, Real.cos ((n : ℝ) * θ i)) +
        2 * ∑' j : ℕ, (-r) ^ (j + 1) *
          (∑ i : Fin d, Real.cos ((n : ℝ) * θ i) *
            Real.cos (((j + 1 : ℕ) : ℝ) * θ i)))

partial def constSet (e : Expr) (s : Std.HashSet Name := {}) : Std.HashSet Name :=
  match e with
  | .const n _ => s.insert n
  | .app f a => constSet a (constSet f s)
  | .lam _ t b _ => constSet b (constSet t s)
  | .forallE _ t b _ => constSet b (constSet t s)
  | .letE _ t v b _ => constSet b (constSet v (constSet t s))
  | .mdata _ b => constSet b s
  | .proj _ _ b => constSet b s
  | _ => s

partial def exprNodes (e : Expr) : Nat :=
  match e with
  | .app f a => 1 + exprNodes f + exprNodes a
  | .lam _ t b _ => 1 + exprNodes t + exprNodes b
  | .forallE _ t b _ => 1 + exprNodes t + exprNodes b
  | .letE _ t v b _ => 1 + exprNodes t + exprNodes v + exprNodes b
  | .mdata _ b => 1 + exprNodes b
  | .proj _ _ b => 1 + exprNodes b
  | _ => 1

run_cmd do
  let env ← getEnv
  let producer := `AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion.actual_inverse_spectrum_cosine_expansion
  let relevant := env.constants.toList.filter fun (n, _) =>
    let s := n.toString
    s.startsWith "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion." ||
    s.startsWith "_private.AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion." ||
    s.startsWith "_private.Tests.GaussianComplexityFixedSpectrumCosineExpansion."
  unless relevant.length == 4 do throwError "Expected exactly 3 production declarations and 1 test declaration; got {relevant.length}"
  for (n, ci) in relevant do
    let .thmInfo ti := ci | throwError "Candidate declaration is not a theorem: {n}"
    let cs := (constSet ti.value).toList
    let publicParents := cs.filter fun n => n.toString.startsWith "AutoSamplingTheory."
    let privateParents := cs.filter fun n => n.toString.startsWith "_private.AutoSamplingTheory."
    logInfo m!"KERNEL_BODY {n} theorem=true nodes={exprNodes ti.value} directConstantCount={cs.length}"
    logInfo m!"DIRECT_PUBLIC_ASTIS {n}: {publicParents}"
    logInfo m!"DIRECT_PRIVATE_ASTIS {n}: {privateParents}"
    logInfo m!"DIRECT_ALL_CONSTANTS {n}: {cs}"
    if n == producer then
      unless publicParents.isEmpty do throwError "Producer unexpectedly depends on public ASTIS parents"
      let same ← liftTermElabM do isDefEq ti.type (mkConst ``ExpectedProducer)
      unless same do throwError "Producer type is not definitionally equal to exact phase2 anonymous type"
      logInfo "EXACT_ANONYMOUS_PRODUCER_TYPE true"
    if n.toString.endsWith ".actual_inverse_grid_cosine_series" then
      unless publicParents == [producer] do throwError "Private consumer lacks exactly one actual public producer parent"
      let same ← liftTermElabM do isDefEq ti.type (mkConst ``ExpectedConsumer)
      unless same do throwError "Private consumer type is not definitionally equal to exact phase2 anonymous type"
      logInfo "EXACT_ANONYMOUS_PRIVATE_CONSUMER_TYPE true"
    elabCommand (← `(#print axioms $(mkIdent n)))
    elabCommand (← `(#check $(mkIdent n)))

example : ExpectedProducer :=
  AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion.actual_inverse_spectrum_cosine_expansion

end FreshSourceKernelReview
