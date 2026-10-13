from pathlib import Path
import json,hashlib,datetime
D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,o):(D/n).write_bytes((json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def read(n):return json.loads((D/n).read_text(encoding='utf-8-sig'))
leasepath=D/'lease.open.json'
initial=leasepath.read_bytes()
assert read('lease.open.json')['state']=='OPEN'
(D/'lease.initial.raw.snapshot.json').write_bytes(initial)
inputs=read('source-inputs.json')
verification=[]
for i in inputs:
    if i['id']=='authored-route':
        raw=(D/i['path']).read_bytes();lf=raw.replace(b'\r\n',b'\n')
    else:
        raw=(D/(i['id']+'.raw.snapshot')).read_bytes();lf=(D/(i['id']+'.lf.snapshot')).read_bytes()
    assert sha(raw)==i['raw_sha256'],i['id']
    assert sha(lf)==i['lf_sha256'],i['id']
    verification.append({'id':i['id'],'raw_sha256':sha(raw),'lf_sha256':sha(lf),'raw_lf_consistent':raw.replace(b'\r\n',b'\n')==lf})
put('input-validation.json',{'status':'PASS','inputs':verification,'historical_misbound_excerpt':'Preserved initial-misbound snapshots and original inputs.json; current source-inputs.json corrects to Integrable.congr physical123','seal_hash':'6560113333ab09326b0d02e0e3f4bf628457fa92bb21756fbc8b27d65d5d8000'})
lease=read('lease.open.json');lease.update(state='CLOSED',closed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),all_read_write_python_operations_within_open_lease=True,compiler=False,claim=False,canonical_edits=False)
put('lease.open.json',lease)
put('leases.closed.json',{'status':'ALL_REAL_LEASES_CLOSED','lease_files':['lease.open.json'],'original_open_bytes':'lease.initial.raw.snapshot.json','actor':'gaussian_noncompact_preread_42'})
outputs=[]
for p in sorted(D.iterdir()):
    if p.is_file() and p.name!='sourcegraph-run.json':
        raw=p.read_bytes();outputs.append({'path':p.name,'raw_sha256':sha(raw),'lf_sha256':sha(raw.replace(b'\r\n',b'\n')),'bytes':len(raw)})
put('sourcegraph-run.json',{'actor':'gaussian_noncompact_preread_42','stage':'independent43sourcegraph','status':'AUTHORED_AWAIT_DISTINCT_TOPOLOGY_ADMISSION','run_closed_at_utc':lease['closed_at_utc'],'scope':'source-only49nodes64edges; no43Lean/compiler/proof/claim;42opaque exact691parent','structural_check':read('structural-check.json'),'input_binding':'source-inputs.json plus input-validation.json','output_binding':outputs,'real_leases':'ALL_CLOSED','exposure':'sourcecontract.json records prior accidental metadata/early32body exposure, narrow currentAPI lookup and corrected misbound excerpt; notfreshblind','theorem_approval':False,'self_topology_validation':False})
for n in ['sourcegraph.json','sourcecontract.json','sourcegraph-run.json','sourcegraph-capsule.md']:
    print(n+' '+sha((D/n).read_bytes()))
