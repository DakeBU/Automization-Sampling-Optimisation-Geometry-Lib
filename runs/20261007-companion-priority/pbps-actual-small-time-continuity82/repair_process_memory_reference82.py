from pathlib import Path
import json,subprocess,sys
r=Path(__file__).parent;p=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-small-time-continuity.json');x=json.loads(p.read_bytes())
old=x['learning_contract']['process_memory_ids'];assert len(old)==2 and all(i.startswith('ASTIS-DISC-') for i in old)
x['learning_contract']['process_memory_ids']=[]
x['learning_contract']['process_memory_checked']=True
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
(r/'process-memory-schema-diagnosis82.json').write_text(json.dumps(dict(failure_class='CONTROL_PLANE_REFERENCE_SCHEMA',failed_gate='frontier-before-proof82',cause='Discovery IDs belong to discovery ledger, not standing process-memory registry.',repair='Remove these IDs from standing process_memory_ids. Retrieval records retain both as process observations without mathematical authority.',retained_discovery_ids=old,statement_changed=False,proof_credit=False),indent=2)+'\n',encoding='utf8',newline='\n')
q=subprocess.run([sys.executable,'-X','utf8','tools/astis_frontier_cells.py','check'],capture_output=True)
(r/'frontier-before-proof82-repaired.stdout.log').write_bytes(q.stdout);(r/'frontier-before-proof82-repaired.stderr.log').write_bytes(q.stderr)
(r/'frontier-before-proof82-repaired.receipt.json').write_text(json.dumps(dict(exit_code=q.returncode,terminal_closed=True))+'\n',encoding='utf8')
print(q.stdout.decode('utf8',errors='replace')[-500:],q.stderr.decode('utf8',errors='replace')[-1000:]);sys.exit(q.returncode)
