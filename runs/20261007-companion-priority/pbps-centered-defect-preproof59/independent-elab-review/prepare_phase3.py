import pathlib,json,hashlib
d=pathlib.Path(__file__).resolve().parent;r=d.parent
def annotated(s):return s.replace('(1-T*T)','((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T)').replace('(1-T0*T0)','((1 : H0 →L[ℝ] H0)-T0*T0)')
for n in [0,1]:(d/f'header{n}.successor-proposed.lean').write_text(annotated((r/f'header{n}.lean').read_text(encoding='utf8')),encoding='utf8',newline='\n')
s=(d/'diagnose.py').read_text()
s=s.replace("D=R/'independent-elab-review';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-review'","D=R/'independent-elab-review/phase3';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-review/phase3'")
start=s.index('variants=');end=s.index('for name,content',start)
variants=r'''def annotated(s):return s.replace('(1-T*T)','((1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)-T*T)').replace('(1-T0*T0)','((1 : H0 →L[ℝ] H0)-T0*T0)')
typed=annotated(positive).replace('isSelfAdjoint_one.sub (by simpa only [pow_two] using hTs.pow 2)','(IsSelfAdjoint.one : IsSelfAdjoint (1 : Lp ℝ 2 ν →L[ℝ] Lp ℝ 2 ν)).sub (by simpa only [pow_two] using hTs.pow 2)').replace('isSelfAdjoint_one.sub (by simpa only [pow_two] using hT0s.pow 2)','(IsSelfAdjoint.one : IsSelfAdjoint (1 : H0 →L[ℝ] H0)).sub (by simpa only [pow_two] using hT0s.pow 2)')
typed=typed.replace('example\n','theorem diagnostic_positive_fragment59\n',1)
typed=typed.replace('\nend\nend AutoSamplingTheory','\n#print axioms diagnostic_positive_fragment59\nend\nend AutoSamplingTheory')
prefix=positive[:positive.index('example\n')]
def sig(h,name):
 h=h.replace('theorem '+h.split()[1],'def '+name,1);a,b=h.split(' :\n',1)
 return a+' : Prop :=\n'+b+'\n'
eq=prefix
for n in [0,1]:
 h=paths[n].read_text(encoding='utf8')
 eq+=sig(h,f'original_signature{n}')+sig(annotated(h),f'annotated_signature{n}')
 a=h.split(' :\n',1)[0];a=a.replace('theorem '+a.split()[1],f'theorem signatures{n}_definitionally_equal',1)
 eq+=a+f' : original_signature{n} hα hαβ hV hH hη hβη = annotated_signature{n} hα hαβ hV hH hη hβη := rfl\n'
 eq+=f'#print axioms signatures{n}_definitionally_equal\n'
eq+='\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator\n'
variants={'positive-all-identities-typed':typed,'sealed-successor-definitional-equality':eq}
'''
s=s[:start]+variants+s[end:]
(d/'diagnose.3.py').write_text(s,encoding='utf8')
