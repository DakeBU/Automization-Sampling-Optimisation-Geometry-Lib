import hashlib,json,pathlib,subprocess,sys,traceback
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC');sys.path.insert(0,str(ROOT))
from tools import astis_advance as advance
OUT=pathlib.Path(__file__).resolve().parent;E=OUT.parents[1];sha=lambda b:hashlib.sha256(b).hexdigest()
T='ASTIS-SA-20261112-GaussianComplexitySourceRowLaw';W='/root/row_law_fresh_source_3dd4';L=ROOT/'runs/substantive_advances.jsonl';C=ROOT/'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-row-law.json'
pre=json.loads((OUT/'pre-invariants.json').read_text());full=json.loads((OUT/'actual-VERIFIED-evidence.full.json').read_text());old=L.read_bytes()
assert sha(old)==pre['ledger']['sha256'] and len(old)==pre['ledger']['bytes']
assert subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,check=True,capture_output=True).stdout.decode().strip()==pre['head']
rows=[json.loads(x) for x in old.splitlines() if x.strip()];state=advance._replay_advances(rows)[T]
assert state['state']=='PROVED_LOCAL' and not any(r.get('advance_id')==T and r.get('to_state')=='VERIFIED' for r in rows)
assert full['verifier_id']==W and full['verified_commit']=='d0654e9bbed44ab852fc44598560799949d8bd12'
sentinel=OUT/'normal-api-call-attempted.json'
with sentinel.open('x') as f:json.dump({'method':'tools.astis_advance.transition_advance','advance_id':T,'to_state':'VERIFIED','worker_id':W,'attempts':1,'automatic_retry':False},f,indent=2);f.write('\n')
api_error=None
try:
 advance.transition_advance(T,'VERIFIED',worker_id=W,evidence=full)
except BaseException:
 api_error=traceback.format_exc()
now=L.read_bytes();rs=[json.loads(x) for x in now.splitlines() if x.strip()];own=advance._replay_advances(rs)[T];suffix=now[len(old):] if now.startswith(old) else b''
outcome={'normal_API_calls':1,'api_returned_successfully':api_error is None,'actual_state':own['state'],'actual_target_VERIFIED_events':sum(r.get('advance_id')==T and r.get('to_state')=='VERIFIED' for r in rs),'ledger_prefix_preserved':now.startswith(old),'append_bytes':len(suffix),'append_sha256':sha(suffix),'error':api_error,'retry':'No replay under any outcome.'}
(OUT/'normal-api-outcome.json').write_text(json.dumps(outcome,indent=2)+'\n')
print(json.dumps(outcome,indent=2),flush=True)
if api_error is not None:raise RuntimeError('Normal API error; actual outcome saved; never replay.')
assert now.startswith(old) and len(suffix.splitlines())==1
record=json.loads(suffix);assert record['advance_id']==T and record['from_state']=='PROVED_LOCAL' and record['to_state']=='VERIFIED' and record['worker_id']==W and record['evidence']==full
assert own['state']=='VERIFIED' and outcome['actual_target_VERIFIED_events']==1
(OUT/'actual-VERIFIED-append.original.jsonl').write_bytes(suffix)
cell=json.loads(C.read_text());rest=json.loads(json.dumps(cell));rest.pop('status');rest['evidence'].pop('independent_verification')
canonical=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
assert sha(canonical(rest))==pre['own_cell']['rest_sha256'] and cell['status']=='proved_locally' and cell['evidence']['independent_verification']==''
cell['status']='independently_verified';cell['evidence']['independent_verification']=str((E/'actual-VERIFIED-independent-decision.json').relative_to(ROOT))
C.write_text(json.dumps(cell,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'cell_status':cell['status'],'only_authorized_cell_fields_changed':['status','evidence.independent_verification'],'VERIFIED_append_raw_sha256':sha(suffix),'full_V_payload_raw_sha256':sha((OUT/'actual-VERIFIED-evidence.full.json').read_bytes()),'decision_raw_sha256':sha((E/'actual-VERIFIED-independent-decision.json').read_bytes())},indent=2))
