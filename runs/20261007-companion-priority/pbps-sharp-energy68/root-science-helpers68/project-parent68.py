from pathlib import Path
import hashlib,json,re

p=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean')
s=p.read_text(encoding='utf-8');before=p.read_bytes()
a=s.index('  rcases hBase with\n');b=s.index('  run_tac do\n',a)
old=s[a:b];names=re.findall(r'\w+|ΓP0|ΓPSq|ΓPq|ΓSq|ΓP|Γ',old[old.index('⟨')+1:old.rindex('⟩')])
# Unicode word matching keeps hΓ, q and all existing identifiers exactly.
names=[z.strip() for z in old[old.index('⟨')+1:old.rindex('⟩')].replace('\n','').split(',')]
assert names[0]=='hμ' and names[-1]=='hGlobal' and len(names)==len(set(names))
exists={'S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R'}
assert exists<=set(names)
lines=['  have parentSlice0 := hBase']
for i,name in enumerate(names):
 if i==len(names)-1:
  lines.append(f'  have {name} := parentSlice{i}')
 elif name in exists:
  lines.extend([f'  let {name} := Classical.choose parentSlice{i}',f'  have parentSlice{i+1} := Classical.choose_spec parentSlice{i}'])
 else:
  lines.extend([f'  have {name} := parentSlice{i}.1',f'  have parentSlice{i+1} := parentSlice{i}.2'])
 if i in [10,23,34,48,61]:
  lines.extend(['  run_tac do',f'    let _ ← IO.FS.writeFile ".astis/pbps-sharp-energy68/projection7-{i:02}.log" "parent field {i} extracted\\n"','    pure ()'])
replacement='\n'.join(lines)+'\n'
s=s[:a]+replacement+s[b:]
s=s.replace('stage6-','stage7-').replace('before-parent-rcases','before-parent-projections').replace('after-parent-rcases','after-parent-projections')
d=Path('runs/20261007-companion-priority/pbps-sharp-energy68/compiler-diagnosis68')
assert not (d/'main.before-parent-projections.raw.snapshot.lean').exists()
(d/'main.before-parent-projections.raw.snapshot.lean').write_bytes(before)
p.write_text(s,encoding='utf-8',newline='\n')
(d/'parent-projection-route.json').write_text(json.dumps(dict(route_change='Replace the single deeply nested rcases elimination by local proof projections and choice of the exact existing existential witnesses.',field_names=names,existential_witness_names=sorted(exists),all_original_callers_and_literal_statement_unchanged=True,no_new_Lean_declaration=True,no_new_provider=True,not_a_mathematical_statement_repair=True,before_RAW_sha256=hashlib.sha256(before).hexdigest(),after_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Parent projection implementation route prepared:',len(names),'fields;',len(exists),'existing existential witnesses; statement unchanged.')
