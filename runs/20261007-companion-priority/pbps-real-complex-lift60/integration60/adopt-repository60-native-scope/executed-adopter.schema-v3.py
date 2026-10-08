from pathlib import Path
import hashlib,json,subprocess
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-real-complex-lift60');d=r/'repository-exposition-seal60';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def path(s):
 p=Path(str(s).replace('\\','/'));return p if p.is_absolute() else root/p
def pin(p):
 p=path(p);raw=p.read_bytes();lf=raw.replace(b'\r\n',b'\n');return dict(path=p.relative_to(root).as_posix(),bytes=len(raw),lf_bytes=len(lf),raw_sha256=sha(raw),lf_sha256=sha(lf))
def key(q):return(path(q['path']).as_posix().lower(),q['raw_sha256'],q['lf_sha256'])
hm=load(d/'historical-mappings.json');maps={key(m['original']):m['snapshot'] for m in hm['available']};post=load(d/'post-input-ledger-mapping.json');maps[key(post['original'])]=post['exact_snapshot'];seen={};resolutions=[]
def check(q):
 current=pin(q['path']);effective=current
 if current['raw_sha256']!=q['raw_sha256'] or current['lf_sha256']!=q['lf_sha256']:
  assert key(q) in maps,q;effective=pin(maps[key(q)]['path']);resolutions.append(dict(original=q,effective=effective))
 assert all(effective[k]==q[k] for k in ['bytes','lf_bytes','raw_sha256','lf_sha256'] if k in q),q;seen[key(q)]=effective
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256','lf_sha256'}<=x.keys():check(x)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
run,lease,receipt,inputs,outputs,readback=[load(d/n) for n in ['run.json','lease.json','receipt.json','input.manifest.json','outputs.final.json','readback.json']]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==receipt['checked_integration_commit']=='63c74351566095343985d36dfcb13dca32a666b7'
assert lease['status']=='CLOSEDLAST' and lease['compiler']==lease['browser']=='NOT_STARTED_CLOSED'
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_run_sha256']=='0f86dc222c48806c7274c8f51cebadb91b9cbd0f4fe09812a9a8ba7d70cbb859'
assert sha(can(run['named_repository_exposition_payload']))==run['named_repository_exposition_payload_sha256']==lease['named_repository_exposition_payload_sha256']=='1242186fc0efadaa8f9f88fadfb992147fcc188d6a5c7de926f3736babcf2ba5'
assert sha(can({k:v for k,v in lease.items() if k!='lease_sha256'}))==lease['lease_sha256']=='f456bd48173ed544ad5b6b845b1b5128515b0912d4d82217c084da70f58fd6a5'
assert sha(can({k:v for k,v in outputs.items() if k!='outputs_sha256'}))==outputs['outputs_sha256']
assert pin(d/'receipt.json')['raw_sha256']=='884e91b4c8d7da0d99a582aebb8e6d7289c6135f261b5f17cd6cea9001dc35fe'
assert pin(d/'lease.json')['raw_sha256']=='a3f9787ee168288b318246ebd980143a14e875c997ac1251f1b6b26a916005f4'
assert receipt['verdict']=='ACCEPT_SCOPED_REPOSITORY_AND_EXPOSITION_NO_LOCAL_BLOCKER' and receipt['status']=='ACCEPTED_SCOPED'
assert inputs['qualified_count']==len(inputs['artifacts'])==readback['native_qualified_pins']==836
assert outputs['count']==len(outputs['artifacts'])==readback['output_count']==388
for x in [inputs,outputs,lease,run,receipt,load(d/'graph.input-pins.json')]:walk(x)
for k in ['actual_reader','actual_finalizer','actual_prepare_readback','actual_readback']:assert lease[k]['exit_code']==0
assert readback['status']=='PASS' and readback['checked_commit']=='63c74351566095343985d36dfcb13dca32a666b7'
out=dict(status='INDEPENDENT_SCOPED_REPOSITORY_EXPOSITION60_ACCEPTED',integration_commit=receipt['checked_integration_commit'],science_commit=receipt['checked_science_commit'],native_run=pin(d/'run.json'),native_lease=pin(d/'lease.json'),native_receipt=pin(d/'receipt.json'),native_actor=lease['actor'],native_run_sha256=run['run_sha256'],native_named_payload_sha256=run['named_repository_exposition_payload_sha256'],unique_qualified_readbacks=len(seen),effective_historical_resolutions=resolutions,counts=receipt['counts'],scope=run['scope'],presentation_debts=[run['named_repository_exposition_payload']['mathematical_reasons']['graph_debt'],receipt['remaining_boundary']],canonical_math_mutations=False,new_verified_transition=False,main_live_purified=False)
(r/'root.repository-exposition60.adoption.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print('Accepted independently closed scoped repo/exposition60;',len(seen),'exact qualified readbacks. No new mathematics/transition/main/live/PURIFIED.')
