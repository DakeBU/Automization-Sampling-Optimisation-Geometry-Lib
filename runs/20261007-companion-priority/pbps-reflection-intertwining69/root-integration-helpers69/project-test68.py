from pathlib import Path
import hashlib,json

p=Path('Tests/ProximalBPSSharpCorrectorEnergy.lean');before=p.read_bytes();s=before.decode('utf-8')
a=s.index('  rcases hBase with\n');b=s.index('  let A : HP →L[ℝ] HP :=',a);old=s[a:b]
names=[z.strip() for z in old[old.index('⟨')+1:old.rindex('⟩')].replace('\n','').split(',')]
assert names[0]=='hμ' and names[-1]=='hGlobal' and len(names)==69 and len(set(names))==len(names)
exists={'S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R'}
lines=['  have parentSlice0 := hBase']
for i,name in enumerate(names):
 if i==len(names)-1:lines.append(f'  have {name} := parentSlice{i}')
 elif name in exists:lines.extend([f'  let {name} := Classical.choose parentSlice{i}',f'  have parentSlice{i+1} := Classical.choose_spec parentSlice{i}'])
 else:lines.extend([f'  have {name} := parentSlice{i}.1',f'  have parentSlice{i+1} := parentSlice{i}.2'])
s=s[:a]+'\n'.join(lines)+'\n'+s[b:]
d=Path('runs/20261007-companion-priority/pbps-sharp-energy68/compiler-diagnosis68')
assert not (d/'test.before-parent-projections.raw.snapshot.lean').exists()
(d/'test.before-parent-projections.raw.snapshot.lean').write_bytes(before)
p.write_text(s,encoding='utf-8',newline='\n')
(d/'test-parent-projection-route.json').write_text(json.dumps(dict(route_change='Reuse the diagnosed local parent projection implementation instead of nested rcases.',field_names=names,existing_existential_witness_names=sorted(exists),all_original_callers_literal_statement_and_mathematical_ingredients_unchanged=True,no_new_declaration_or_provider=True,before_RAW_sha256=hashlib.sha256(before).hexdigest(),after_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Test uses69 local parent fields and12 existing witnesses; no repeated flat-case attempt.')
