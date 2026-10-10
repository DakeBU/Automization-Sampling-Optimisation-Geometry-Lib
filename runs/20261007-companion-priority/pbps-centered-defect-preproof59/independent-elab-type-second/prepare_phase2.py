import pathlib
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59';D=R/'independent-elab-type-second';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second/phase2';P.mkdir(exist_ok=True)
base=(ROOT/'.astis/pbps-centered-defect59/full-header-negative-probe.lean').read_text(encoding='utf8');prefix=base[:base.index('theorem actual_centered_selfadjoint_defect')]
def inline(s):
 lines=s.splitlines(keepends=True)
 return ''.join(l for l in lines if 'let H0 : Submodule ℝ (Lp ℝ 2 ν) := (innerSL ℝ q).ker' not in l).replace('H0','((innerSL ℝ q).ker)')
headers=[]
for n in [0,1]:
 old=(R/f'independent-elab-review/header{n}.successor-proposed.lean').read_text(encoding='utf8');new=inline(old)
 (D/f'header{n}.inline-kernel-proposed.lean').write_text(new,encoding='utf8',newline='\n');headers.append((old,new))
consumer=prefix+headers[1][1].rstrip()+' := by\n  fail "HEADER_ELABORATED_INTENTIONAL_NO_PROOF"\n\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator\n'
def signature(h,name):
 a,b=h.split(' :\n',1);a=a.replace('theorem '+a.split()[1],'def '+name,1)
 return a+' : Prop :=\n'+b+'\n'
equiv=prefix
for n,(old,new) in enumerate(headers):
 equiv+=signature(old,f'let_kernel_signature{n}')+signature(new,f'inline_kernel_signature{n}')
 a=old.split(' :\n',1)[0];a=a.replace('theorem '+a.split()[1],f'theorem kernel_signatures{n}_definitionally_equal',1)
 equiv+=a+f' : let_kernel_signature{n} hα hαβ hV hH hη hβη = inline_kernel_signature{n} hα hαβ hV hH hη hβη := rfl\n#print axioms kernel_signatures{n}_definitionally_equal\n'
 # A separate kernel declaration control returns the exact whole inline target.
 # The additional premise is diagnostic ONLY and never a proposed source binder.
 a,b=new.split(' :\n',1);a=a.replace('theorem '+a.split()[1],f'theorem diagnostic_named_full_type{n}',1)
 equiv+=a+' (diagnostic_input :\n'+b+'\n) :\n'+b+' := diagnostic_input\n'+f'#print axioms diagnostic_named_full_type{n}\n'
equiv+='\nend\nend AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator\n'
variants={'consumer-inline-kernel-type':consumer,'full-inline-definition-equality-and-kernel-controls':equiv}
for name,content in variants.items():(P/(name+'.lean')).write_text(content,encoding='utf8',newline='\n')
s=(D/'diagnose.py').read_text().replace("D=R/'independent-elab-type-second';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second'","D=R/'independent-elab-type-second/phase2';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second/phase2'")
a=s.index('variants=');b=s.index('for name,content',a)
s=s[:a]+"variants={name:(P/(name+'.lean')).read_text(encoding='utf8') for name in ['consumer-inline-kernel-type','full-inline-definition-equality-and-kernel-controls']}\n"+s[b:]
(D/'diagnose.2.py').write_text(s,encoding='utf8')
