from pathlib import Path
import re,json,hashlib
p=Path('Tests/ProximalBPSSharpCorrectorEnergy.lean');b=p.read_bytes();s=b.decode('utf-8')
d=Path('runs/20261007-companion-priority/pbps-sharp-energy68/compiler-diagnosis68')
snapshot=d/'test.before-atomic-exists.raw.snapshot.lean';assert not snapshot.exists();snapshot.write_bytes(b)
pat=r'  let (\w+) := Classical\.choose parentSlice(\d+)\n  have parentSlice(\d+) := Classical\.choose_spec parentSlice\2'
names=[]
def change(m):
 assert int(m[3])==int(m[2])+1
 names.append(m[1])
 return f'  obtain ⟨{m[1]}, parentSlice{m[3]}⟩ := parentSlice{m[2]}'
s,n=re.subn(pat,change,s);assert n==12
old='  obtain ⟨fP,hfP,hBf,hΓf,hPyth,hNormV,hBudget,hCorrector⟩ := hGlobal f hf'
assert s.count(old)==1
new='''  obtain ⟨fP,hGlobalFields⟩ := hGlobal f hf
  have hfP := hGlobalFields.1
  have hBf := hGlobalFields.2.1
  have hΓf := hGlobalFields.2.2.1
  have hPyth := hGlobalFields.2.2.2.1
  have hNormV := hGlobalFields.2.2.2.2.1
  have hBudget := hGlobalFields.2.2.2.2.2.1
  have hCorrector := hGlobalFields.2.2.2.2.2.2'''
s=s.replace(old,new)
p.write_text(s,encoding='utf-8',newline='\n')
(d/'test-atomic-route.json').write_text(json.dumps(dict(route='Reuse bounded parent and actual-input atomic existential eliminations and conjunction projections. All original witnesses/fields retained.',existing_parent_witness_names=names,statement_change=False,mathematical_change=False,before_raw_sha256=hashlib.sha256(b).hexdigest(),after_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),test_compiler_credit=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Test uses12 exact atomic parent existentials and1 exact global existential; no mathematical change.')
