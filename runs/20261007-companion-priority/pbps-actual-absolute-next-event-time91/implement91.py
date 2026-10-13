"""Create the sealed production statement and first bounded proof block."""
from pathlib import Path
import hashlib

run = Path(__file__).parent
pre = run.parent / "pbps-ordered-history-iteration-preread91"
header = (pre / "header91.proposed.lean").read_text(encoding="utf-8")
assert hashlib.sha256(header.encode()).hexdigest() == "b8bba160f6134c7927167a0a34d99971ce75023ef7ea04f738a91b6862da2680"
binders = header[header.index("    {E : Type*}"):header.index("    let c :")]
model = header[header.index("    let c :"):header.index("    ∀ y xRef :")]
target = header[header.index("    ∀ y xRef :"):header.index("\nend\n")]
locals_ = target[target.index("      let Rec :="):target.index("      Measurable H ∧")]
cutoff_locals = target[target.index("        let d :"):target.index("        Measurable (Function.uncurry D)")]
def indent(s, spaces):
    return "\n".join((" " * spaces) + line[4:] if line.startswith("    ") else line for line in s.splitlines()) + "\n"
proof = """
set_option maxHeartbeats 2400000 in
theorem actual_absolute_next_event_time_law
""" + binders.replace(" : Prop :=\n", " :\n") + """    actual_absolute_next_event_time_statement hα hαβ hV hH hη hβη := by
  classical
""" + indent(model, 2) + """  change
""" + target + """
  have h90 := ActualFiniteHistoryExtension.actual_finite_history_extension
    hα hαβ hV hH hη hβη
  have h89 := ActualConditionalNextWaitDensity.actual_conditional_next_wait_density
    hα hαβ hV hH hη hβη
  intro y xRef z₀ n
""" + indent(locals_, 0) + """  change Measurable H ∧ Measurable Hnext ∧ Measurable a ∧ Measurable U ∧
    Measurable appendAbs ∧ Measurable liftAbs ∧
    (∀ p : Hist × ℝ, ∀ j : Fin (n + 1), appendAbs p j.castSucc = p.1 j) ∧ _
  have hnext : Measurable Hnext := (h90 y xRef z₀ n).1
  have hrel : Measurable appendRel := (h90 y xRef z₀ n).2.1
  have hprefix (p : Hist × ℝ) (j : Fin (n + 1)) : appendRel p j.castSucc = p.1 j :=
    (h90 y xRef z₀ n).2.2.2.1 p j
  have hhistory : Measurable H := by
    apply measurable_pi_lambda
    intro j
    exact (measurable_pi_apply j.castSucc).comp hnext
  have hread : Measurable readTime := by
    change Measurable (Sum.elim (fun q : ℝ≥0 × (E × E) => (q.1 : ℝ))
      (fun _ : Unit => (0 : ℝ)))
    exact (measurable_coe_nnreal_real.comp measurable_fst).sumElim measurable_const
  have ha : Measurable a := hread.comp (measurable_pi_apply last)
  have hU : Measurable U := hread.comp ((measurable_pi_apply lastNext).comp hnext)
  have happend : Measurable appendAbs :=
    hrel.comp (measurable_fst.prodMk (measurable_snd.sub (ha.comp measurable_fst)))
  have hlift : Measurable liftAbs := happend.prodMk measurable_snd
  refine ⟨hhistory, hnext, ha, hU, happend, hlift,
    (fun p j => hprefix (p.1, p.2 - a p.1) j), ?_⟩
  intro b hb
""" + "\n".join(line[6:] if line.startswith("      ") else line for line in cutoff_locals.splitlines()) + """
  change Measurable (Function.uncurry D) ∧
    (∀ h : Hist, (∫⁻ u : ℝ, D h u) ≤ 1) ∧ _
  have hd : Measurable d := measurable_real_toNNReal.comp
    ((measurable_coe_nnreal_real.comp hb).sub ha)
  have hrho : Measurable (density y xRef) := (h89 y xRef z₀ n).2.1
  have hD : Measurable (Function.uncurry D) := by
    have hguard : MeasurableSet {p : Hist × ℝ |
        a p.1 < p.2 ∧ p.2 < (b p.1 : ℝ)} :=
      (measurableSet_lt (ha.comp measurable_fst) measurable_snd).inter
        (measurableSet_lt measurable_snd
          (measurable_coe_nnreal_real.comp (hb.comp measurable_fst)))
    exact (hrho.comp (((measurable_pi_apply last).comp measurable_fst).prodMk
      (measurable_snd.sub (ha.comp measurable_fst)))).piecewise hguard measurable_const
  refine ⟨hD, ?_⟩
"""
production = Path("AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean")
assert not production.exists()
production.write_text(header[:header.index("\nend\n")] + proof +
    "\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime\n",
    encoding="utf-8", newline="\n")
print("Sealed statement retained; first proof block created. Remaining proof goal intentionally OPEN, no proof credit.")
