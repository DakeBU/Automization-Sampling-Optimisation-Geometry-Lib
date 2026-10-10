import pathlib,json,hashlib,sys,subprocess,os
from datetime import datetime,timezone
ROOT=pathlib.Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-gaussian-reflected-mean52';OUT=P/'exact-verification52';COMMIT='a18cd1cf8e8310f228391d4c53a2ac8f1a8900ec';CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SHARED-gaussian-reflected-mean.json';ADV='ASTIS-SA-20261007-GaussianReflectedMean';VERIFIER='whole_math52'
sys.path.insert(0,str(ROOT))
from tools.astis_advance import transition_advance,current_advances
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,o):p.write_text(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
assert git('rev-parse','HEAD').decode().strip()==COMMIT
assert not git('status','--porcelain','--untracked-files=no').strip()
gates=read(OUT/'gate-summary.json');assert gates['all_pass'] and gates['focused']['exit_code']==0
assert 'Build completed successfully (3893 jobs).' in (OUT/'focused.log').read_text(encoding='utf-8')
inputs=read(OUT/'git.input-bindings.json')
for e in inputs['bindings']:assert pin(ROOT/e['current']['path'])==e['current']
for e in read(P/'math-freeze.json')['inputs']:assert pin(ROOT/e['path'])==e
assert read(OUT/'fake-closure-scan.json')['forbidden_hits']==[]
source=read(P/'source.0.review.json');admission=read(OUT/'source-admission-bindings.json');assert admission['current_context_exact_match']
native=[]
def validate_pin(e):
 p=pathlib.Path(e['path']);p=p if p.is_absolute() else ROOT/p
 a=pin(p)
 for k in ['raw_sha256','lf_sha256','bytes']:
  if k in e:assert a[k]==e[k],str(p)+' '+k
 return a
dec=read(P/'anonymous-decoder/run.json');dh=dec.pop('run_sha256');assert sha(json.dumps(dec,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode())==dh
assert sha(json.dumps(dec['run_binding_payload'],sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode())==dec['decoder_run_sha256']==source['decoder_run_sha256']
binding=read(P/'anonymous-decoder/binding-receipt.json')
for e in binding['output_artifacts']:native.append(validate_pin(e))
for n in ['reviewer.source.run.json','reviewer.source.lease.json','source.review.lease.json']:
 obj=read(P/n)
 for k in ['result','checks','review_result','run','root_closed_lease']:
  if isinstance(obj.get(k),dict) and 'path' in obj[k] and 'raw_sha256' in obj[k]:native.append(validate_pin(obj[k]))
states=current_advances();assert states[ADV]['state']=='PROVED_LOCAL'
stabilizing_before={k:v.get('state') for k,v in states.items() if v.get('state')=='STABILIZING'}
cell=read(CELL);assert cell['status']=='proved_locally'
(OUT/'cell.before.raw.snapshot.json').write_bytes(CELL.read_bytes())
receipt={
 'schema_version':1,'verifier_id':VERIFIER,'verified_commit':COMMIT,'advance_id':ADV,'verdict':'ACCEPT_EXACT_COMMIT_SCOPED_VERIFICATION','exact_commit_and_current_tree_bound':True,
 'mathematical_review_reuse':{'receipt':pin(P/'whole-proof-review52/receipt.json'),'run':pin(P/'whole-proof-review52/run.json'),'lease':pin(P/'whole-proof-review52/lease.json'),'reason':'The complete proof and both substantive Tests are byte-identical to the prior independent whole-mathematics review; all333 frozen originals pass. No reproof or transcript replay.'},
 'scientific_commit_evidence':pin(OUT/'git.input-bindings.json'),'strict_frozen333_evidence':pin(OUT/'freeze.input-bindings.json'),'strict_source347_evidence':pin(OUT/'source-admission-bindings.json'),
 'exact_signature':{'LF_bytes':497,'sha256':'50ca5c7e0b5aed0f892d2e686fd276b11a586b30745d8edd2d5c1256d7e09d11','header_and_complete_body_and_Test_hashes_unchanged':True},
 'source_gate':{'canonical_audit':'ASTIS-RT-20261007-GaussianReflectedMean','state':'accepted','verdict':'equivalent-after-elaboration','reviewer':source['reviewer'],'review_run_sha256':source['review_run_sha256'],'reviewer_packet_sha256':source['reviewer_packet_sha256'],'publication_binding_sha256':source['publication_binding_sha256'],'current_context_exact':True,'source_review':pin(P/'source.0.review.json'),'all_seven_slots':True,'deltas':[],'repairs':[],'excess':[],'blindness_boundary':'Anonymous statement/source-text-blind reconstruction with disclosed inherited general source identities; strict source-identity blindness is not claimed.'},
 'gate':gates,'fake_closure_scan':pin(OUT/'fake-closure-scan.json'),'axioms':'All three checked declarations depend only on propext, Classical.choice and Quot.sound.',
 'prior_native_hashes':pin(OUT/'prior-native-validation.json'),'additional_native_decoder_and_source_output_validation':native,'decoder_native_run_sha256':dh,'decoder_binding_payload_sha256':dec['decoder_run_sha256'],
 'whitespace':read(OUT/'authored-whitespace.status.json'),'whitespace_boundary':'Authored exact-commit diff passes with only94 explicitly diagnosed immutable evidence paths excluded; preserved gzip reproduces full staged exit2/787 findings. No full-staged whitespace PASS.',
 'remaining_truth_boundary':read(P/'proved-local.json')['truth_boundary'],
 'excluded_acceptance':['Shared-root/Tests aggregate and tools/astis.py check run later in the original serialized stabilization lane.','Source-volume all-y SAME-S adapter, literal Tf closed-gradient membership, rough B.13/Gamma/main/errors/nonexplosion/query-cost/composition remain separate.','Graph/site reader delivery and purification are not completed by this exact verification.'],
 'authorized_mutation':'Independent verifier alone records VERIFIED and changes only ASTIS-SHARED-gaussian-reflected-mean status/evidence. No production/Test/publication/root/Registry/othercell edits, no commit/push and no reads in active53 folder.',
 'compiler_lease':pin(OUT/'focused.lease.json'),'compiler_pid':gates['focused']['process_id'],'compiler_exit_code':0,'completed_utc':now(),'blockers':[]
}
write(OUT/'receipt.json',receipt)
evidence={
 'verifier_id':VERIFIER,'verified_commit':COMMIT,'result_kind':'theorem-edge','publication_declarations':read(P/'proved-local.json')['publication_declarations'],
 'gate':{'focused_lean':pin(OUT/'focused.status.json'),'publication_base_origin_main':pin(OUT/'publication.status.json'),'semantic':pin(OUT/'semantic.status.json'),'frontier':pin(OUT/'frontier.status.json'),'contributor_base_origin_main':pin(OUT/'contributor.status.json'),'authored_whitespace':pin(OUT/'authored-whitespace.status.json'),'result':'All exact focus/noncompiler gates passed. Shared-root/Tests/tools.astis aggregate intentionally later in original sole stabilization lane.'},
 'source_audit':{'audit_id':'ASTIS-RT-20261007-GaussianReflectedMean','source_review':pin(P/'source.0.review.json'),'verdict':source['verdict'],'source_review_run_sha256':source['review_run_sha256'],'publication_binding_sha256':source['publication_binding_sha256'],'strict_original_inputs':347,'bindings':pin(OUT/'source-admission-bindings.json')},
 'semantic_roundtrip_audit':'ASTIS-RT-20261007-GaussianReflectedMean accepted equivalent-after-elaboration; inherited source-identity metadata exposure disclosed, strict identity-blindness not claimed.',
 'fake_closure_scan':pin(OUT/'fake-closure-scan.json'),'independent_exact_commit_receipt':pin(OUT/'receipt.json'),'whole_math_receipt':pin(P/'whole-proof-review52/receipt.json'),
 'truth_boundary':receipt['remaining_truth_boundary'],'integration_notes':'Exact a18cd1c independent focused/source/publication verified only; source-volume adapter/Tf closure/full rough results and aggregate/site/purification remain separate. Original phase sole STABILIZING lane unchanged.'}
write(P/'verified.json',evidence)
transition_advance(ADV,'VERIFIED',worker_id=VERIFIER,modes=['independent-verification'],evidence=evidence)
cell['status']='independently_verified';cell['evidence']['independent_verification']={'verifier_id':VERIFIER,'verified_commit':COMMIT,'evidence':(P/'verified.json').relative_to(ROOT).as_posix(),'receipt':(OUT/'receipt.json').relative_to(ROOT).as_posix(),'gate':'Exact focused3893/compiler + publication --base origin/main/semantic/frontier/contributor --base origin/main/authored-whitespace all PASS; aggregate root/Tests later.','source_audit':'ASTIS-RT-20261007-GaussianReflectedMean accepted equivalent-after-elaboration; exact source0/native/context bindings verified.','fake_closure_scan':(OUT/'fake-closure-scan.json').relative_to(ROOT).as_posix()}
write(CELL,cell)
after=current_advances();assert after[ADV]['state']=='VERIFIED';assert {k:v.get('state') for k,v in after.items() if v.get('state')=='STABILIZING'}==stabilizing_before
write(OUT/'transition.status.json',{'advance_id':ADV,'before':'PROVED_LOCAL','after':'VERIFIED','worker_id':VERIFIER,'evidence':pin(P/'verified.json'),'verified_commit':COMMIT,'cell':pin(CELL),'cell_before':pin(OUT/'cell.before.raw.snapshot.json'),'cell_status':'independently_verified','stabilizing_lanes_unchanged':True,'sole_stabilizing_count':len(stabilizing_before),'completed_utc':now()})
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2'
post=[]
for label,cmd in [('frontier-post',[sys.executable,'tools/astis_frontier_cells.py','check']),('contributor-post',[sys.executable,'tools/astis_contributor_contract.py','check','--base','origin/main'])]:
 opened=now()
 with (OUT/(label+'.log')).open('wb') as f:
  p=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT);write(OUT/(label+'.lease.json'),{'status':'OPEN','command':cmd,'process_id':p.pid,'opened_utc':opened});rc=p.wait()
 status={'command':cmd,'process_id':p.pid,'exit_code':rc,'log':pin(OUT/(label+'.log')),'verified_commit':COMMIT,'finished_utc':now()};write(OUT/(label+'.status.json'),status);write(OUT/(label+'.lease.json'),{'status':'CLOSED','command':cmd,'process_id':p.pid,'exit_code':rc,'Python':'CLOSED','compiler':'NOT_STARTED_CLOSED','opened_utc':opened,'closed_utc':now()});post.append(status);assert rc==0
assert git('rev-parse','HEAD').decode().strip()==COMMIT
changed=git('diff','--name-only','HEAD').decode().splitlines();assert set(changed)=={'research-wiki/frontier-cells/ASTIS-SHARED-gaussian-reflected-mean.json','runs/substantive_advances.jsonl'},changed
for e in read(P/'math-freeze.json')['inputs']:assert pin(ROOT/e['path'])==e
write(OUT/'final-current-bindings.json',{'verified_commit':COMMIT,'current_HEAD_unchanged':True,'tracked_changes_exactly_authorized':changed,'tracked_mutation_bindings':[pin(ROOT/n) for n in changed],'verified_evidence':pin(P/'verified.json'),'frozen333_still_exact':True,'post_transition_gates':post,'remaining_boundary_unchanged':True})
outputs=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name not in ['run.json','lease.json']]
run={'schema_version':1,'verifier_id':VERIFIER,'verified_commit':COMMIT,'status':'VERIFIED_SCOPED','advance_id':ADV,'receipt':pin(OUT/'receipt.json'),'verified_evidence':pin(P/'verified.json'),'transition':pin(OUT/'transition.status.json'),'inputs':inputs,'outputs':outputs,'logical_hash_recipe':'SHA256 UTF8 sorted compact ensure_ascii=False JSON run minus run_sha256, no final newline. Exact raw/LF run pinned by final closed lease.','completed_utc':now()}
run['run_sha256']=sha(json.dumps(run,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode());write(OUT/'run.json',run)
lease=read(OUT/'lease.json');lease.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',read='CLOSED',write='CLOSED',closed_utc=now(),verified_commit=COMMIT,advance_state='VERIFIED',cell_status='independently_verified',run_sha256=run['run_sha256'],actual_final_outputs=[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='lease.json'],external_authorized_outputs=[pin(P/'verified.json'),pin(CELL),pin(ROOT/'runs/substantive_advances.jsonl')],final_operation='Actual review lease written last after all mutations, post-gates and native bindings.');write(OUT/'lease.json',lease)
print(json.dumps({'state':'VERIFIED','commit':COMMIT,'compiler_pid':receipt['compiler_pid'],'receipt':pin(OUT/'receipt.json'),'run':pin(OUT/'run.json'),'run_sha256':run['run_sha256'],'lease':pin(OUT/'lease.json'),'cell_status':'independently_verified','stabilizing_lanes_unchanged':True}))
