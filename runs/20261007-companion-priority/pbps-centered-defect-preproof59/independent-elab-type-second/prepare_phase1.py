import pathlib
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59';D=R/'independent-elab-type-second';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second/phase1';P.mkdir(exist_ok=True)
base=(ROOT/'.astis/pbps-centered-defect59/full-header-negative-probe.lean').read_text(encoding='utf8')
inline=base.replace('              let H0 : Submodule ℝ (Lp ℝ 2 ν) := (innerSL ℝ q).ker\n','').replace('H0','((innerSL ℝ q).ker)')
cut=base.index('              ∃ T0 :');end=base.index(' := by\n  fail',cut)
truncated=base[:cut].rstrip();assert truncated.endswith('∧');truncated=truncated[:-1].rstrip()+base[end:]
prefix=base[:base.index('theorem actual_centered_selfadjoint_defect')]
consumer=prefix+(R/'independent-elab-review/header1.successor-proposed.lean').read_text(encoding='utf8').rstrip()+' := by\n  fail "HEADER_ELABORATED_INTENTIONAL_NO_PROOF"\n\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator\n'
variants={'full-type-inline-kernel':inline,'full-type-no-centered-tail':truncated,'consumer-complete-type':consumer}
for name,content in variants.items():(P/(name+'.lean')).write_text(content,encoding='utf8',newline='\n')
s=(D/'diagnose.py').read_text().replace("D=R/'independent-elab-type-second';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second'","D=R/'independent-elab-type-second/phase1';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second/phase1'")
a=s.index('variants=');b=s.index('for name,content',a)
s=s[:a]+"variants={name:(P/(name+'.lean')).read_text(encoding='utf8') for name in ['full-type-inline-kernel','full-type-no-centered-tail','consumer-complete-type']}\n"+s[b:]
(D/'diagnose.1.py').write_text(s,encoding='utf8')
