namespace WithTop

variable {ι : Type*} [LinearOrder ι] [TopologicalSpace ι] [OrderTopology ι]

instance : MeasurableSpace (WithTop ι) := borel _

instance : BorelSpace (WithTop ι) := ⟨rfl⟩

variable [MeasurableSpace ι] [BorelSpace ι]

/-- Measurable equivalence between the non-top elements of `WithTop ι` and `ι`. -/
noncomputable
def MeasurableEquiv.neTopEquiv : { r : WithTop ι | r ≠ ⊤ } ≃ᵐ ι :=
  (WithTop.neTopHomeomorph ι).toMeasurableEquiv

lemma measurable_of_measurable_comp_coe {α : Type*} {mα : MeasurableSpace α}
    {f : WithTop ι → α} (h : Measurable fun p : ι ↦ f p) :
    Measurable f :=
  measurable_of_measurable_on_compl_singleton ⊤
    (MeasurableEquiv.neTopEquiv.symm.measurable_comp_iff.1 h)

lemma measurable_untopD (d : ι) : Measurable (untopD d) :=
  measurable_of_measurable_comp_coe measurable_id

lemma measurable_untopA [Nonempty ι] : Measurable (WithTop.untopA (α := ι)) :=
  measurable_untopD _

lemma measurable_coe : Measurable (fun x : ι ↦ (x : WithTop ι)) := continuous_coe.measurable

@[fun_prop]
lemma _root_.Measurable.withTop_coe {α} {mα : MeasurableSpace α} {f : α → ι} (hf : Measurable f) :
    Measurable (fun x ↦ (f x : WithTop ι)) :=
  measurable_coe.comp hf

@[fun_prop]
lemma _root_.Measurable.untopD {α} {mα : MeasurableSpace α} (d : ι)
    {f : α → WithTop ι} (hf : Measurable f) :
    Measurable (fun x ↦ (f x).untopD d) := (measurable_untopD d).comp hf
