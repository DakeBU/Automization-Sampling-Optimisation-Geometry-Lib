from pathlib import Path
import json,hashlib,copy,sys
sys.path.insert(0,str(Path.cwd()))
from tools import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-marginal-poincare57');q=r/'exact-verification57'
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def require_verified():
 d=j(q/'run.json');l=j(q/'lease.json');receipt=j(q/'receipt.json');v=j(r/'verified.json')
 for p,h in [(q/'lease.json','38744ab21ba17dc642d007401d7426f23233b4a44fd61f5d5a4a1ca279afce31'),(r/'verified.json','68584e2de3107b1826fbcf7933567a5626a64f17ad81ebf63d62ae28adb00256'),(q/'receipt.json','7fe2f0a6ee30dfe311502a1819594cb33e33156a9f5928c7caf7dafe74adad2e'),(q/'run.json','11382009190cd418505ea588baf6f5b563edc5934372b8190a7e11187107b451')]:assert sha(p.read_bytes())==h,p
 for obj,key in [(d,'run_sha256'),(l,'lease_sha256'),(receipt,'receipt_sha256'),(v,'verified_sha256')]:
  x=copy.deepcopy(obj);h=x.pop(key);assert sha(canon(x))==h,key
 assert d['run_sha256']==l['run_sha256']==v['complete_run_minus_run_sha256']=='2e2d10a65160ed08b332fab83a4bab6ee0c37bf3d5e1a5a523cf7d7561c53d76'
 assert sha(canon(d['verifier_binding_payload']))==d['verifier_binding_payload_sha256']==l['verifier_binding_payload_sha256']==v['verifier_binding_payload_sha256']=='8cb11f30d6bec7988e2721cb46634ec6f6a6d3812de453933d912039673c4669'
 assert l['status']==l['read']==l['write']==l['Python']==l['compiler']=='CLOSED' and l['actual_compiler_exit_code']==l['actual_foreground_exit_code']==0 and l['actual_compiler_PID']==37264
 before=l['exact_verified_admin_before_mappings'];assert len(before)==2
 shared=j(r/'verified-inputs.before-shared-integration.json')['mappings'] if (r/'verified-inputs.before-shared-integration.json').exists() else []
 prefix=l['ledger_before_prefix_mapping'];count=0
 def same(a,b):return Path(a['path']).resolve()==Path(b['path']).resolve() and all(a[k]==b[k] for k in ['bytes','raw_sha256','lf_sha256'])
 def check(row):
  nonlocal count
  target=row
  for m in before:
   if same(row,m['original']):target=m['exactraw_snapshot'];break
  for m in shared:
   if same(row,m['original']):target=m['snapshot'];break
  if same(row,prefix['original']):
   b=Path(row['path']).read_bytes()[:prefix['actual_preserved_prefix_bytes']]
   assert len(b)==row['bytes']==prefix['actual_preserved_prefix_bytes'] and sha(b)==row['raw_sha256']==prefix['actual_preserved_prefix_raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==row['lf_sha256']==prefix['actual_preserved_prefix_lf_sha256'];count+=1;return
  b=Path(target['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==target['bytes'] and sha(b)==target['raw_sha256'] and sha(lf)==target['lf_sha256'],target['path']
  if 'lf_bytes' in target:assert len(lf)==target['lf_bytes']
  assert all(row[k]==target[k] for k in ['bytes','raw_sha256','lf_sha256']);count+=1
 assert len(d['inputs'])==l['input_count']==1955 and d['science_entries']==l['actual_science_entries']==1923
 for row in d['inputs']+l['outputs']:check(row)
 for k in ['original_open','receipt','run','verified','readback']:check(l[k])
 check(d['compiler_lease']);check(receipt['noncompiler_gates'])
 outputs=j(q/'outputs.final.json');assert len(outputs['outputs'])==outputs['count']
 for row in outputs['outputs']:check(row)
 assert l['output_count']==len(l['outputs'])==52
 assert len(receipt['fake_closure_scan'])==10 and all(not x['authored_fake_closure_hits'] for x in receipt['fake_closure_scan'])
 assert len(receipt['axiom_closures'])==2 and all(set(x['axioms'])=={'propext','Classical.choice','Quot.sound'} for x in receipt['axiom_closures'])
 assert all(x['exit_code']==0 for x in j(q/'gates.json')['records'])
 assert d['checked_commit']==l['checked_commit']==receipt['checked_commit']==v['checked_commit']==v['verified_commit']=='e8a9044ba5a945eaa4b4aecd110b63494fe6c68e'
 assert v['status']=='VERIFIED' and v['verifier_id']=='whole_math52_exact57'
 states=adv.current_advances();assert states['ASTIS-SA-20261008-GaussianMarginalPoincare']['state']=='VERIFIED'
 assert [k for k,x in states.items() if x['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
 return dict(v,root_native_pin_checks=count)
if __name__=='__main__':
 v=require_verified();print('Native57 independent VERIFIED adopted',v['verified_commit'],v['root_native_pin_checks'])
