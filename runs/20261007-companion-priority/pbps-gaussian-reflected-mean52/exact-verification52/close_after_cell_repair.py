import pathlib,json,hashlib,sys,subprocess,os
from datetime import datetime,timezone
ROOT=pathlib.Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-gaussian-reflected-mean52';OUT=P/'exact-verification52';COMMIT='a18cd1cf8e8310f228391d4c53a2ac8f1a8900ec';CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SHARED-gaussian-reflected-mean.json';ADV='ASTIS-SA-20261007-GaussianReflectedMean'
sys.path.insert(0,str(ROOT))
from tools.astis_advance import current_advances
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,o):p.write_text(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==COMMIT
assert current_advances()[ADV]['state']=='VERIFIED'
assert read(OUT/'frontier-post.status.json')['exit_code']==1
(OUT/'cell.before-representation-repair.raw.snapshot.json').write_bytes(CELL.read_bytes())
(OUT/'transition.before-representation-repair.raw.snapshot.json').write_bytes((OUT/'transition.status.json').read_bytes())
cell=read(CELL);details=cell['evidence']['independent_verification'];assert isinstance(details,dict)
cell['evidence']['independent_verification_details']=details
cell['evidence']['independent_verification']='whole_math52 independently verified exact scientific commit '+COMMIT+'; runs/20261007-companion-priority/pbps-gaussian-reflected-mean52/verified.json and exact-verification52/receipt.json bind actual focused3893/source/publication/semantic/frontier/contributor/authored-whitespace gates. Shared aggregate integration remains pending.'
write(CELL,cell)
write(OUT/'cell-representation-repair.json',{'classification':'IMPLEMENTATION_FAILED','scope':'Verifier-authored frontier evidence representation only','negative_gate':pin(OUT/'frontier-post.status.json'),'negative_log':pin(OUT/'frontier-post.log'),'diagnosis':'astis_frontier_cells._nonempty requires independent_verification to be a nonempty string. A structured dict was truthful but not schema-admissible.','repair':'Retain the full details separately and supply the expected evidence-path string. No mathematical/source/publication/commit change and no repeated VERIFIED transition.','before':pin(OUT/'cell.before-representation-repair.raw.snapshot.json'),'after':pin(CELL),'salvage':'Verified ledger transition, exact scientific commit, all focused/gate/source/native evidence retained.'})
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2'
post=[]
for label,cmd in [('frontier-post-repaired',[sys.executable,'tools/astis_frontier_cells.py','check']),('contributor-post',[sys.executable,'tools/astis_contributor_contract.py','check','--base','origin/main'])]:
 opened=now()
 with (OUT/(label+'.log')).open('wb') as f:
  p=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT);write(OUT/(label+'.lease.json'),{'status':'OPEN','command':cmd,'process_id':p.pid,'opened_utc':opened});rc=p.wait()
 status={'command':cmd,'process_id':p.pid,'exit_code':rc,'log':pin(OUT/(label+'.log')),'verified_commit':COMMIT,'finished_utc':now()};write(OUT/(label+'.status.json'),status);write(OUT/(label+'.lease.json'),{'status':'CLOSED','command':cmd,'process_id':p.pid,'exit_code':rc,'Python':'CLOSED','compiler':'NOT_STARTED_CLOSED','opened_utc':opened,'closed_utc':now()});post.append(status);assert rc==0
assert git('rev-parse','HEAD').decode().strip()==COMMIT
changed=git('diff','--name-only','HEAD').decode().splitlines();assert set(changed)=={'research-wiki/frontier-cells/ASTIS-SHARED-gaussian-reflected-mean.json','runs/substantive_advances.jsonl'},changed
for e in read(P/'math-freeze.json')['inputs']:assert pin(ROOT/e['path'])==e
before=read(OUT/'cell.before.raw.snapshot.json')
assert {k:v for k,v in before.items() if k not in ['status','evidence']}=={k:v for k,v in cell.items() if k not in ['status','evidence']}
for k,v in before['evidence'].items():assert cell['evidence'][k]==v
transition=read(OUT/'transition.status.json');transition.update(cell=pin(CELL),post_transition_gates=post,representation_repair=pin(OUT/'cell-representation-repair.json'),completed_utc=now());write(OUT/'transition.status.json',transition)
write(OUT/'final-current-bindings.json',{'verified_commit':COMMIT,'current_HEAD_unchanged':True,'tracked_changes_exactly_authorized':changed,'tracked_mutation_bindings':[pin(ROOT/n) for n in changed],'verified_evidence':pin(P/'verified.json'),'frozen333_still_exact':True,'post_transition_gates':post,'remaining_boundary_unchanged':True,'cell_only_status_and_added_verification_evidence_changed':True})
assert current_advances()[ADV]['state']=='VERIFIED' and cell['status']=='independently_verified'
outputs=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name not in ['run.json','lease.json']]
run={'schema_version':1,'verifier_id':'whole_math52','verified_commit':COMMIT,'status':'VERIFIED_SCOPED','advance_id':ADV,'receipt':pin(OUT/'receipt.json'),'verified_evidence':pin(P/'verified.json'),'transition':pin(OUT/'transition.status.json'),'inputs':read(OUT/'git.input-bindings.json'),'outputs':outputs,'post_transition_repair':pin(OUT/'cell-representation-repair.json'),'logical_hash_recipe':'SHA256 UTF8 sorted compact ensure_ascii=False JSON run minus run_sha256, no final newline. Exact raw/LF run pinned by final closed lease.','completed_utc':now()}
run['run_sha256']=sha(json.dumps(run,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode());write(OUT/'run.json',run)
lease=read(OUT/'lease.json');lease.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',read='CLOSED',write='CLOSED',closed_utc=now(),verified_commit=COMMIT,advance_state='VERIFIED',cell_status='independently_verified',run_sha256=run['run_sha256'],actual_final_outputs=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='lease.json'],external_authorized_outputs=[pin(P/'verified.json'),pin(CELL),pin(ROOT/'runs/substantive_advances.jsonl')],final_operation='Actual review lease written last after all mutations, repaired post-gates and native bindings.');write(OUT/'lease.json',lease)
print(json.dumps({'state':'VERIFIED','commit':COMMIT,'compiler_pid':read(OUT/'focused.status.json')['process_id'],'receipt':pin(OUT/'receipt.json'),'run':pin(OUT/'run.json'),'run_sha256':run['run_sha256'],'lease':pin(OUT/'lease.json'),'cell_status':'independently_verified','stabilizing_lanes_unchanged':True}))
