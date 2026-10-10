from pathlib import Path
import json,hashlib,datetime,sys
sys.stdout.reconfigure(encoding='utf-8')
p=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-rough-gradient-density-preread55')
def sha(b):return hashlib.sha256(b).hexdigest()
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def info(path):
 b=path.read_bytes();return {'path':str(path),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf(b)),'lf_sha256':sha(lf(b))}
def write(n,v):b=(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8');(p/n).write_bytes(b);return b
contract=json.loads((p/'source-contract.json').read_text(encoding='utf-8'))
contract['search_boundaries']['genuine_found'][0]='MeasureTheory.Lp.compMeasurePreservingₗᵢ'
write('source-contract.json',contract)
current_checks=[]
for f in ['parent-API-bindings.json','API-input-bindings.json']:
 for x in json.loads((p/f).read_text(encoding='utf-8')):
  path=Path(x['path']);b=path.read_bytes();current_checks.append({'path':str(path),'record':f,'raw_matches':sha(b)==x['whole_raw_sha256'],'lf_matches':sha(lf(b))==x['whole_lf_sha256']})
s=json.loads((p/'source-before-API.json').read_text(encoding='utf-8'));q=Path(s['primary_path']);b=q.read_bytes();current_checks.append({'path':str(q),'record':'source-before-API.json','raw_matches':sha(b)==s['primary_raw_sha256'],'lf_matches':sha(lf(b))==s['primary_lf_sha256']})
assert all(x['raw_matches'] and x['lf_matches'] for x in current_checks)
write('current-input-recheck.json',{'all_exact':True,'checks':current_checks,'semantic_body_reads':False,'compiler':'NOT_STARTED_CLOSED'})
lease_raw=(p/'lease.json').read_bytes();(p/'lease.open.snapshot.json').write_bytes(lease_raw)
closed=json.loads(lease_raw.decode('utf-8-sig'));closed.update(read='CLOSED',write='CLOSED',python='CLOSED',compiler='NOT_STARTED_CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),closure='Final filesystem operation of55; original54/53/sourcegraphs remain untouched; no compiler, proof, claim, SAU, Goal, graph, seal or canonical write')
closedbytes=(json.dumps(closed,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
outputs=[info(x) for x in sorted(p.iterdir()) if x.is_file() and x.name not in ['run.json','lease.json']]
run={'schema':'astis-source-only-native-preread-run/v1','owner':'/root/gaussian_noncompact_preread_42','scope':str(p),'result':'bounded source/API diagnosis and unproved smaller actual-L2 averaging producer recommendation','source_contract':info(p/'source-contract.json'),'source_first':info(p/'source-before-API.json'),'outputs':outputs,'actual_lease':{'path':str(p/'lease.json'),'raw_sha256':sha(closedbytes),'lf_sha256':sha(lf(closedbytes)),'all_closed':True,'compiler':'NOT_STARTED_CLOSED'},'history_open_lease':info(p/'lease.open.snapshot.json'),'exact_input_recheck':'current-input-recheck.json','raw_recipe':'SHA256 exact on-disk bytes','lf_recipe':'replace CRLF with LF then remaining CR with LF, SHA256','logical_recipe':'SHA256 UTF8 JSON of whole run object excluding run_sha256, sort_keys=True, ensure_ascii=False, separators=(comma,colon)','no_self_admission':True,'no_formal_theorem_credit':True}
logical=sha(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'));run['run_sha256']=logical;runbytes=write('run.json',run)
summary={'scope':str(p),'source_contract_rawLF':sha((p/'source-contract.json').read_bytes()),'run_rawLF':sha(runbytes),'run_logical':logical,'actual_closed_lease_rawLF':sha(closedbytes),'all_input_rawLF_match':True,'outputs':len(outputs),'recommendation':'Actual all-L2 same-law averaging bridge; full rough B.13 unproved and future54 prospective'}
# This is deliberately the LAST filesystem operation. No read, write, glob, stat or subprocess follows.
(p/'lease.json').write_bytes(closedbytes)
print(json.dumps(summary,ensure_ascii=False,indent=2))
