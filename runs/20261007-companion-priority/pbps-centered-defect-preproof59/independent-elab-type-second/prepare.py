import pathlib
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59';D=R/'independent-elab-type-second';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second';D.mkdir(exist_ok=True);P.mkdir(exist_ok=True)
base=(ROOT/'.astis/pbps-centered-defect59/full-header-negative-probe.lean').read_text(encoding='utf8')
start=base.index('    let μ :=');end=base.index(' := by\n  fail',start);target=base[start:end]
variants={'full-type-baseline':base,'full-type-expected-Prop':base[:start]+'    (show Prop from\n'+target+'\n    )'+base[end:],
 'full-type-recdepth':base.replace('set_option maxHeartbeats 1600000','set_option maxHeartbeats 1600000\nset_option maxRecDepth 10000')}
for name,s in variants.items():(P/(name+'.lean')).write_text(s,encoding='utf8',newline='\n')
runner=(R/'independent-elab-review/diagnose.py').read_text()
runner=runner.replace("D=R/'independent-elab-review';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-review'","D=R/'independent-elab-type-second';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second'")
a=runner.index('variants=');b=runner.index('for name,content',a)
runner=runner[:a]+"variants={name:(P/(name+'.lean')).read_text(encoding='utf8') for name in ['full-type-baseline','full-type-expected-Prop','full-type-recdepth']}\n"+runner[b:]
runner=runner.replace("paths=[R/'header0.lean'", "paths=[R/'header0.lean'")
(D/'diagnose.py').write_text(runner,encoding='utf8')
