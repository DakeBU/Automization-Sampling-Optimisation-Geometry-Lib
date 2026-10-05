import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationFirstOrder

/-!
# Counted adaptive oracle simulation

Chewi arXiv2605.07006v1 §1.1 and Lemma4.2: one genuine first-order reply
implements a reply for the quadratically regularized function. The counter
below counts oracle interactions, not local arithmetic or machine runtime.
This finite deterministic interface does not assert class-uniform complexity.
-/
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle
open Set
open scoped NNReal

/-- A query-fuel interpreter. `next` either halts with an output or requests a
query. Each reply updates the state and costs one query. Halting is inspected
even at zero fuel. `none` marks exhaustion, never a successful output. -/
def run {S Q A X : Type*} (next : S → Sum X Q) (update : S → Q → A → S)
    (oracle : Q → A) : ℕ → S → (S × Option X) × ℕ
  | fuel, s => match next s with
    | .inl x => ((s, some x), 0)
    | .inr q => match fuel with
      | 0 => ((s, none), 0)
      | n+1 =>
        let answer := oracle q
        let tail := run next update oracle n (update s q answer)
        (tail.1, tail.2+1)

set_option backward.isDefEq.respectTransparency false in
/-- Correct each original value/gradient reply using known quadratic data.
For every adaptive program and fuel, this preserves the actual regularized
execution, including its state, halt/exhaustion outcome and query count. -/
theorem simulate_regularized
    {E S X : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]
    (next : S → Sum X E) (update : S → E → (ℝ × E) → S)
    {f : E → ℝ} (hd : Differentiable ℝ f) (hc : ConvexOn ℝ univ f)
    {β δ : ℝ≥0} (hL : LipschitzWith β (gradient f)) (u : E) (fuel : ℕ) (s : S) :
    let W := fun x => f x + (δ : ℝ)/2*‖x-u‖^2
    let corrected := fun s x (a : ℝ × E) =>
      update s x (a.1 + (δ : ℝ)/2*‖x-u‖^2, a.2 + (δ : ℝ) • (x-u))
    let base := run next corrected (fun x => (f x, gradient f x)) fuel s
    let target := run next update (fun x => (W x, gradient W x)) fuel s
    base = target ∧ base.2 ≤ fuel := by
  dsimp only
  have hg := (QuadraticRegularizationFirstOrder.curvature_gradient_and_smoothness
    hd hc hL (δ := δ) u).2.2.1
  induction fuel generalizing s with
  | zero => cases h : next s <;> simp [run, h]
  | succ n ih =>
    cases h : next s with
    | inl x => simp [run, h]
    | inr x =>
      have step (upd : S → E → (ℝ × E) → S) (O : E → ℝ × E) :
          run next upd O (n+1) s =
            let tail := run next upd O n (upd s x (O x))
            (tail.1, tail.2+1) := by rw [run, h]
      simp only [step, hg]
      obtain ⟨he, hn⟩ := ih (update s x
        (f x + (δ : ℝ)/2*‖x-u‖^2, gradient f x + (δ : ℝ) • (x-u)))
      refine ⟨?_, Nat.succ_le_succ hn⟩
      simpa only [hg] using congrArg (fun r => (r.1, r.2+1)) he
end AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularizationOracle
