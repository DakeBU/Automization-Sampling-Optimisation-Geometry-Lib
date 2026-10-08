from pathlib import Path
import json,hashlib,copy,sys,subprocess
sys.path.insert(0,str(Path('tools').resolve()))
import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-macroscopic-centered-range58');q=r/'exact-verification58';j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));H=lambda b:hashlib.sha256(b).hexdigest();canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def w(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def selfcheck(d,k):x=copy.deepcopy(d);h=x.pop(k);assert H(canon(x))==h,k;return h
def require_verified():
 d=j(q/'run.json');l=j(q/'lease.json');receipt=j(q/'receipt.json');v=j(r/'verified.json');im=j(q/'inputs.final.json');of=j(q/'outputs.final.json');rb=j(q/'readback.json')
 for p,h in [(q/'receipt.json','267016240d383e27669c1fcda5e72a1e2eac8eaab94637fce0846b20cd7f0f22'),(q/'run.json','c593499af41ab630ae98ab383600960be8b712f4bc7894b3a70ed5416827b302'),(q/'lease.json','a15e52103fcee01e5555cd08a1072b781be564be4f17f0636a940da0cc7fa0cd'),(r/'verified.json','434011a529c95b24dfdc7dd7e8ec86eac80ff3dc2b52e5954221d676703bdcc1')]:assert H(p.read_bytes())==h,p
 assert selfcheck(d,'run_sha256')==l['complete_run_minus_run_sha256']=='ccc639f14715885636deb9350a11cd18dde9c815ca36e830ad34847012377666'
 for x,k in [(l,'lease_sha256'),(receipt,'receipt_sha256'),(v,'verified_sha256'),(of,'content_self_sha256'),(rb,'content_self_sha256')]:selfcheck(x,k)
 assert H(canon(d['verifier_binding_payload']))==d['verifier_binding_payload_sha256']==l['verifier_binding_payload_sha256']==v['verifier_binding_payload_sha256']=='c60232bece66a6449fe28e16b58f43f51afff12bcb3f965cfc150692db2d88ab'
 assert all(l[k]=='CLOSED' for k in ['status','read','write','compiler','Python']) and l['actual_compiler_exit_code']==l['actual_worker_exit_code']==0 and l['actual_compiler_PID']==30908 and l['actual_worker_PID']==53352 and l['actual_closer_PID']==8612
 assert d['checked_commit']==v['verified_commit']==l['checked_commit']==receipt['checked_commit']=='8c8847715c1d4c3033224b069d8dd694f2a4bd30'
 assert receipt['science_entries']==1185 and receipt['strict_math_originals']==72 and receipt['actual_native_pin_checks']==4346 and receipt['native_self_component_checks']==36 and receipt['focused_invocations']==1 and receipt['standard_axiom_closures']==3 and receipt['fake_closure_findings']==0 and receipt['source_reviews']==3
 before=im['exact_verified_admin_before_mappings'];assert len(before)==6;extra=j(r/'verified-inputs.before-shared-integration.json')['mappings'] if (r/'verified-inputs.before-shared-integration.json').exists() else [];prefix=im['ledger_prefix'];count=0
 def same(a,b):return Path(a['path']).resolve()==Path(b['path']).resolve() and all(a[k]==b[k] for k in ['bytes','raw_sha256','lf_sha256'])
 def check(row):
  nonlocal count
  target=row
  for m in before:
   if same(row,m['original']):target=m['exactraw_snapshot'];break
  for m in extra:
   if same(row,m['original']):target=m['snapshot'];break
  if Path(row['path']).resolve()==Path('runs/substantive_advances.jsonl').resolve() and row['raw_sha256']==prefix['raw_sha256']:
   assert Path(row['path']).read_bytes().startswith(Path(prefix['path']).read_bytes());target=prefix
  b=Path(target['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==target['bytes'] and H(b)==target['raw_sha256'] and len(lf)==target['lf_bytes'] and H(lf)==target['lf_sha256'],target['path'];assert all(row[k]==target[k] for k in ['bytes','raw_sha256','lf_bytes','lf_sha256']);count+=1
 assert len(d['inputs'])==l['input_count']==rb['input_count']==1223 and len(l['outputs'])==l['output_count']==54 and len(of['outputs'])==of['count']==52
 for row in d['inputs']+l['outputs']+of['outputs']+rb['inputs']+rb['outputs']:check(row)
 for k in ['run','receipt','verified','readback','output_manifest','actual_worker_terminal_evidence']:check(l[k])
 assert j(q/'gates.json')['status']=='PASS' and j(q/'gates.json')['no_duplicate_compiler']
 states=adv.current_advances();assert states[v['advance_id']]['state']=='VERIFIED' and [k for k,x in states.items() if x['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
 return dict(verified_commit=v['verified_commit'],native_verified=True,actual_root_native_pin_checks=count,whole_run_sha256=d['run_sha256'],distinct_verifier_payload_sha256=d['verifier_binding_payload_sha256'],native_raw_run_sha256=H((q/'run.json').read_bytes()),scope=receipt['scope'] if 'scope' in receipt else j(r/'publication-plan.json')['remaining_boundary'])
if __name__=='__main__':
 v=require_verified();p=r/'root.exact-verification58.adoption.json';assert not p.exists();w(p,v)
 plan=j(r/'publication-plan.json');edits=set(['AutoSamplingTheory/TechnicalLemmas/Registry.lean','AutoSamplingTheory/TechnicalLemmas/Measure.lean','AutoSamplingTheory/ExampleCases.lean','Tests.lean','Tests/Basic.lean','docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/technical-lemma-memory/technical_lemma_registry.jsonl','runs/substantive_advances.jsonl']+['research-wiki/frontier-cells/'+x+'.json' for x in plan['active_cells']])
 mappings=[];seen=set();out=r/'shared-before58';out.mkdir(exist_ok=False)
 for row in j(q/'run.json')['inputs']:
  source=Path(row['path']);rel=source.resolve().relative_to(Path.cwd().resolve()).as_posix();key=(rel,row['raw_sha256'])
  if rel not in edits or key in seen:continue
  b=source.read_bytes()
  if H(b)!=row['raw_sha256']:continue
  seen.add(key);snap=out/(str(len(mappings)).zfill(3)+'.'+source.name+'.raw.snapshot');snap.write_bytes(b);mappings.append(dict(original=row,snapshot=dict(path=snap.as_posix(),bytes=len(b),lf_bytes=len(b.replace(b'\r\n',b'\n')),raw_sha256=H(b),lf_sha256=H(b.replace(b'\r\n',b'\n')))))
 w(r/'verified-inputs.before-shared-integration.json',dict(mappings=mappings,scope='Only exact native input pins that planned root shared integration will mutate; old preadmin pins remain under native before mappings.'))
 print('Independent exact58 strictly adopted',v['verified_commit'],'root raw/LF pin checks',v['actual_root_native_pin_checks'],'current mutable before maps',len(mappings))
