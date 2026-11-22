import B4Protocol
import Mathlib.Data.List.OfFn

/-!
The sigma algebra on histories is the disjoint union of the ordinary finite
product sigma algebras. In particular a policy may be specified by an arbitrary
Borel function of the full chronological tuple at every fixed length.
-/

open MeasureTheory
open AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
open scoped AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol

variable {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]

private theorem measurable_ofFn (m : ℕ) : Measurable (@List.ofFn α m) := by
  induction m with
  | zero =>
    change Measurable (fun v : Fin 0 → α => List.ofFn v)
    simp only [List.ofFn_zero]
    exact measurable_const
  | succ m ih =>
    have ht : Measurable (fun v : Fin (m+1) → α => fun j : Fin m => v j.succ) :=
      measurable_pi_lambda _ fun j => measurable_pi_apply j.succ
    change Measurable (fun v : Fin (m+1) → α => List.ofFn v)
    simp only [List.ofFn_succ]
    exact measurable_list_cons (measurable_pi_apply (0 : Fin (m+1))) (ih.comp ht)

/-- Read the first slots, using the given value beyond the list boundary. -/
def tupleAt (a₀ : α) (m : ℕ) (h : List α) (i : Fin m) : α :=
  match h[i.val]? with | none => a₀ | some a => a

theorem measurable_tupleAt (a₀ : α) (m : ℕ) : Measurable (tupleAt a₀ m) := by
  apply measurable_pi_lambda
  intro i
  exact measurable_option_cases (fun h : List α => h[i.val]?) (measurable_trace_read _)
    (fun _ => a₀) measurable_const (fun _ a => a) measurable_snd

omit [MeasurableSpace α] in
theorem tupleAt_length (a₀ : α) (h : List α) :
    List.ofFn (tupleAt a₀ h.length h) = h := by
  have he : tupleAt a₀ h.length h = h.get := by
    funext i
    simp [tupleAt, List.get_eq_getElem]
  rw [he, List.ofFn_get]

/-- A map on histories is measurable precisely when it is measurable on each
finite Cartesian power of the record space. -/
theorem measurable_history_iff_ofFn (a₀ : α) (f : List α → β) :
    Measurable f ↔ ∀ m, Measurable (fun v : Fin m → α => f (List.ofFn v)) := by
  constructor
  · exact fun hf m => hf.comp (measurable_ofFn m)
  · intro hf
    let evaluate := fun (p : ℕ × List α) => f (List.ofFn (tupleAt a₀ p.1 p.2))
    have he : Measurable evaluate :=
      measurable_from_prod_countable_right fun m => (hf m).comp (measurable_tupleAt a₀ m)
    have h := he.comp (measurable_trace_length.prodMk measurable_id)
    change Measurable (fun l : List α => f (List.ofFn (tupleAt a₀ l.length l))) at h
    simpa only [tupleAt_length] using h

#print axioms measurable_history_iff_ofFn

end AutoSamplingTheory.ExampleCases.GaussianComplexity.HaarProtocol
