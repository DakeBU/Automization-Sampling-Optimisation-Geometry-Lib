lemma _root_.measurePreserving_eval_infinitePi (i : ι) :
    MeasurePreserving (Function.eval i) (infinitePi μ) (μ i) where
  measurable := by fun_prop
  map_eq := by
    ext s hs
    have : @Function.eval ι X i =
        (@Function.eval ({i} : Finset ι) (fun j ↦ X j) ⟨i, by simp⟩) ∘
        (Finset.restrict {i}) := by ext; simp
    rw [this, ← map_map, infinitePi_map_restrict, (measurePreserving_eval _ _).map_eq]
    all_goals fun_prop

lemma infinitePi_map_eval (i : ι) :
    (infinitePi μ).map (fun x ↦ x i) = μ i :=
  (measurePreserving_eval_infinitePi μ i).map_eq
