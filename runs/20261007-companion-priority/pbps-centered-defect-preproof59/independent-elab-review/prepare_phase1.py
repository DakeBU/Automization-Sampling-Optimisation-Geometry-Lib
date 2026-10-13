import pathlib
d=pathlib.Path(__file__).resolve().parent
s=(d/'diagnose.py').read_text()
s=s.replace("D=R/'independent-elab-review';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-review'","D=R/'independent-elab-review/phase1';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-review/phase1'")
start=s.index('variants=');end=s.index('for name,content',start)
variants="""variants={
'positive-qualified':positive.replace('(1-T*T).IsPositive','ContinuousLinearMap.IsPositive (1-T*T)').replace('(1-T0*T0).IsPositive','ContinuousLinearMap.IsPositive (1-T0*T0)'),
'positive-qualified-typed':positive.replace('(1-T*T).IsPositive','ContinuousLinearMap.IsPositive ((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T)').replace('(1-T0*T0).IsPositive','ContinuousLinearMap.IsPositive ((1 : H0 →L[ℝ] H0)-T0*T0)')}
"""
s=s[:start]+variants+s[end:]
(d/'diagnose.1.py').write_text(s,encoding='utf8')
