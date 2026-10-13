from pathlib import Path
import json,hashlib,sys
r=Path('runs/20261007-companion-priority/pbps-root-commutation67');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();claim=load(r/'claim.json');p=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');d=r/'canonical-floor-metadata67';d.mkdir();old=p.read_bytes();(d/'cell.before.exactraw.snapshot.json').write_bytes(old);x=json.loads(old);x['shared_floor_audit'].update(canonical_declaration=claim['target_declarations'][1],canonical_shared_cell=claim['frontier_cell']);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');after=p.read_bytes()
(d/'repair.json').write_text(json.dumps(dict(kind='AUTHOR_METADATA_CANONICAL_TARGET_ID',changed_fields=['shared_floor_audit.canonical_declaration','shared_floor_audit.canonical_shared_cell'],before_RAW_sha256=sha(old),after_RAW_sha256=sha(after),reason='New cell canonical target must be its actual declaration,not the already reused parent;previous publication gate rejected exact inherited parent ID.',Lean_statement_formula_changed=False,publication_binding_unchanged=True),indent=2)+'\n',encoding='utf-8',newline='\n')
freeze=r/'math-freeze.json';b=freeze.read_bytes();(r/'math-freeze.0.before-canonical-floor.json').write_bytes(b);f=json.loads(b)
for pin in f['inputs']:
 if Path(pin['path']).resolve()==p.resolve():pin.update(raw_bytes=len(after),raw_sha256=sha(after),lf_sha256=sha(after.replace(b'\r\n',b'\n')))
f['metadata_resolution']=(d/'repair.json').as_posix();freeze.write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_publication as pub;pub.check_advance(claim['target_declarations'][:2],reviewed=False)
print('PASS67 focused publication freeze after exact two canonical target fields;bindings/code/formulas unchanged;old freeze/gate negative retained.')
