"""Consolidate internal proved ingredients and assemble the unchanged sealed target."""
from pathlib import Path
import re
run=Path(__file__).resolve().parent
files=['WeightedPrefix93.lean','ActualPathIdentification93.lean','CountInterfaces93.lean',
       'InterpolationFormula93.lean','ActualCountEvent93.lean']
blocks={}
for file in files:
    s=(run/file).read_text(encoding='utf8')
    matches=list(re.finditer(r'^private theorem (\w+)',s,re.M))
    for j,m in enumerate(matches):
        name=m.group(1)
        if name in blocks: continue
        end=matches[j+1].start() if j+1<len(matches) else len(s)
        block=s[m.start():end]
        block=re.split(r'^#print|^end\b|^attribute \[|^open scoped|^noncomputable section',block,flags=re.M)[0]
        block=re.sub(r'^set_option .*\n','',block,flags=re.M)
        blocks[name]=block.strip()
# Drop unused prototype-only set-law helpers. The localized helper actually used remains.
for name in ['survival_history_measure','survival_history_all_tests']:
    assert sum(len(re.findall(r'\b'+name+r'\b',b)) for k,b in blocks.items() if k!=name)==0 or name=='survival_history_measure'
    blocks.pop(name)
header=(run.parent/'pbps-finite-count-path-preread93/Header93.lean').read_text(encoding='utf8')
statement=header[header.index('def candidate_finite_count_path_statement'):header.index('#check candidate_finite_count_path_statement')].strip()
statement=statement.replace('def candidate_finite_count_path_statement','private def actual_finite_count_path_statement',1)
sig=header.split('def candidate_finite_count_path_statement',1)[1].split(' : Prop := by',1)[0]
lets,conclusion=header.split('  exact\n',1)[1].split('    ∃ Z :',1)
conclusion='    ∃ Z :'+conclusion.split('\n#check',1)[0].rstrip()
body='''
  obtain ⟨Z, hZM, hZarc, hZfallback, hZzero, hZpath⟩ :=
    actual_history_path_identification hα hαβ hV hH hη hβη
  refine ⟨Z, hZM, hZarc, hZfallback, hZzero, ?_⟩
  intro n T
  have hΨ := actual_history_interpolation_measurable hα hαβ hV hH hη hβη n T
  have hW := actual_terminal_weighted_prefix_tests hα hαβ hV hH hη hβη n T
  refine ⟨hΨ, hW.1, hW.2.1, ?_⟩
  intro y xRef z₀
  let H := history y xRef z₀ n
  let ZT : (ℕ → ℝ) → Path T := fun w s => Z y xRef z₀ s.val w
  have hWL := hW.2.2 y xRef z₀
  have hHM : Measurable H :=
    ((AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law
      hα hαβ hV hH hη hβη n T).2.2.2.2 y xRef z₀).1
  have hZT : Measurable ZT := by
    apply measurable_pi_lambda
    intro s
    exact hZM.comp (f := fun w : ℕ → ℝ => (((y,xRef),z₀),(s.val,w)))
      (measurable_const.prodMk (measurable_const.prodMk measurable_id))
  have hNM : Measurable (N y xRef z₀ T) :=
    (actual_count_selector_measurable hα hαβ hV hH hη hβη).comp
      (f := fun w : ℕ → ℝ => (((y,xRef),z₀),(T,w)))
      (measurable_const.prodMk (measurable_const.prodMk measurable_id))
  have hc := actual_count_event_identification hα hαβ hV hH hη hβη y xRef z₀ T
  have heq : {w | N y xRef z₀ T w = n} =ᵐ[P] C y xRef z₀ n T := by
    filter_upwards [hc.2.1] with w hw
    exact propext (hw.2.1 n)
  have hr : P.restrict {w | N y xRef z₀ T w = n} = P.restrict (C y xRef z₀ n T) :=
    Measure.restrict_congr_set heq
  have hp : ∀ w ∈ C y xRef z₀ n T, Ψ y xRef z₀ n T (H w) = ZT w :=
    hZpath n T y xRef z₀
  refine ⟨hHM, hZT, hNM, hWL.1,
    actual_prescribed_path_interpolation hα hαβ hV hH hη hβη n T y xRef z₀,
    hp, hc.2.1, hc.2.2.1, hc.2.2.2, ?_, ?_, ?_, ?_⟩
  · rw [hr]
    calc
      Measure.map (fun w => (H w, ZT w)) (P.restrict (C y xRef z₀ n T)) =
          Measure.map (fun w => (H w, Ψ y xRef z₀ n T (H w))) (P.restrict (C y xRef z₀ n T)) := by
        apply Measure.map_congr
        exact ae_restrict_of_forall_mem hWL.1 (fun w hw => Prod.ext rfl (hp w hw).symm)
      _ = _ := hWL.2.2.2.1
  · intro F hF
    rw [hr]
    calc
      (∫⁻ w, F (H w, ZT w) ∂P.restrict (C y xRef z₀ n T)) =
          ∫⁻ w, F (H w, Ψ y xRef z₀ n T (H w)) ∂P.restrict (C y xRef z₀ n T) := by
        apply lintegral_congr_ae
        exact ae_restrict_of_forall_mem hWL.1 (fun w hw => congrArg (fun z => F (H w,z)) (hp w hw).symm)
      _ = _ := hWL.2.2.1 F hF
  · exact hWL.2.2.2.2.1.trans (measure_congr heq).symm
  · rw [measure_congr heq]
    exact hWL.2.2.2.2.2
'''
preamble='''import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival
import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability
import Mathlib.Data.Set.Card
import Mathlib.Order.Interval.Set.Nat
import Mathlib.MeasureTheory.Constructions.Pi

/- Internal full-target assembly. Not yet independently verified or published. -/
namespace FullTarget93
open InnerProductSpace MeasureTheory ProbabilityTheory Filter
open scoped ContDiff NNReal ENNReal Topology Interval BigOperators
noncomputable section
set_option autoImplicit false
set_option maxHeartbeats 2400000
attribute [local instance] Classical.propDecidable

'''
out=preamble+'\n\n'.join(blocks.values())+'\n\n'+statement+'\n\n'
out+='private theorem actual_finite_count_path_law'+sig+' :\n    actual_finite_count_path_statement hα hαβ hV hH hη hβη := by\n  classical\n'
out+='\n'.join(line[2:] if line.startswith('  ') else line for line in lets.rstrip().splitlines())+'\n'
out+='  change\n'+conclusion+body+'\n#print axioms actual_finite_count_path_law\nend\nend FullTarget93\n'
(run/'FullTarget93.lean').write_text(out,encoding='utf8',newline='\n')
print('consolidated helper declarations',len(blocks),'lines',len(out.splitlines()))
