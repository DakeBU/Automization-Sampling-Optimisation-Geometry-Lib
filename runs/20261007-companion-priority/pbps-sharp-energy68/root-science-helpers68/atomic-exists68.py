from pathlib import Path
import hashlib, json, re

p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean')
b=p.read_bytes(); s=b.decode('utf-8')
d=Path('runs/20261007-companion-priority/pbps-sharp-energy68/compiler-diagnosis68')
snapshot=d/'main.before-atomic-exists.raw.snapshot.lean'
assert not snapshot.exists(); snapshot.write_bytes(b)
pat=r'  let (\w+) := Classical\.choose parentSlice(\d+)\n  have parentSlice(\d+) := Classical\.choose_spec parentSlice\2'
names=[]
def change(m):
 assert int(m[3])==int(m[2])+1
 names.append(m[1])
 return f'  obtain ⟨{m[1]}, parentSlice{m[3]}⟩ := parentSlice{m[2]}'
s,n=re.subn(pat,change,s)
assert n==12,(n,names)
s=s.replace('stage7-','stage8-').replace('projection7-','projection8-')
tag='  unfold actual_sharp_corrector_bound_statement\n'
assert s.count(tag)==1
s=s.replace(tag,tag+'  run_tac do\n    let _ ← IO.FS.writeFile ".astis/pbps-sharp-energy68/reassembly8-unfold.log" "after target unfold\\n"\n    pure ()\n')
start=s.index('  refine ⟨hμ, ?_⟩')
end=s.index('  intro f hf',start)
piece=s[start:end]
count=0
out=[]
for line in piece.splitlines(keepends=True):
 out.append(line)
 if line.startswith('  refine '):
  count+=1
  if count==1 or count%5==0:
   out.extend(['  run_tac do\n',f'    let _ ← IO.FS.writeFile ".astis/pbps-sharp-energy68/reassembly8-{count:02}.log" "after constructor {count}\\n"\n','    pure ()\n'])
s=s[:start]+''.join(out)+s[end:]
p.write_text(s,encoding='utf-8',newline='\n')
record=dict(route='Keep bounded conjunction projections, but eliminate each of the12 existing existential witnesses atomically rather than introducing transparent Classical.choose aliases. Add bounded diagnostics after target unfold and during witness reconstruction.',
            previous_v7_run='focused-actual68-v7-projected-parent/receipt.json',previous_run_not_proof=True,
            selected_exact_parent_objects=names,existential_count=n,constructor_count=count,
            statement_unchanged=True,public_binders_unchanged=True,new_public_provider=False,
            before_raw_sha256=hashlib.sha256(b).hexdigest(),after_raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
(d/'atomic-existential-route.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Atomic existential route prepared:',n,'same witnesses;',count,'constructors; statement unchanged.')
