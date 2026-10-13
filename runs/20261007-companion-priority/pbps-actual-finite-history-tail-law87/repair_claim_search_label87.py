from pathlib import Path
import json,subprocess,sys,hashlib
R=Path('E:/Samplinglib');r=Path(__file__).parent;p=R/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-history-tail-law.json'
before=p.read_bytes();out=r/'frontier87.before-search-label-repair.exactraw.snapshot';assert not out.exists();out.write_bytes(before)
d=json.loads(before);label='Samplinglib: actual finite recursion/UnitExponentialProduct and shared Frontier Cells; exact search outputs below.'
assert label not in d['shared_floor_audit']['searched']
d['shared_floor_audit']['searched'].insert(0,label);d['reuse_plan']['searched_existing'].insert(0,label)
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
q=subprocess.run([sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'],cwd=R,capture_output=True)
(r/'frontier-after-search-label87.stdout.log').write_bytes(q.stdout);(r/'frontier-after-search-label87.stderr.log').write_bytes(q.stderr)
receipt={'exit_code':q.returncode,'terminal_closed':True,'diagnosis':'Existing search receipt paths lacked literal samplinglib classifier required by schema gate. Add truthful label to recorded actual searches. Exact statement/seal/reviews/source topology unchanged.','previous_cell_raw_sha256':hashlib.sha256(before).hexdigest(),'current_cell_raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(r/'frontier-after-search-label87.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
print(q.stdout.decode(errors='replace'));print(q.stderr.decode(errors='replace'));assert q.returncode==0
