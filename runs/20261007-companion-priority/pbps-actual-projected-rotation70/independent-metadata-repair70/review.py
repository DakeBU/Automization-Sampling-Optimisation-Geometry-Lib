import os,sys,json,hashlib,datetime,re,subprocess,traceback
from pathlib import Path
ROOT=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;R=O.parent;P=R/'representation-metadata-repair70';M=R/'independent-math70';SOURCE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean';ACTOR='/root/exact_science63';STATUS='APPROVED_EXACT_TWO_FIELD_METADATA_OVERLAY_ONLY'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def get(n):return read(O/n)
def save(n,x):
 assert not(O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def check(q):assert pin(q['path'])==q,('exact RAW/LF mismatch',q['path'])
def logical(r):return sha(json.dumps({k:v for k,v in r.items() if k!='run_sha256'},sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def files():return sorted(p for p in O.rglob('*') if p.is_file())
def stable():
 for q in get('inputs.manifest.json')['inputs']:
  check(q['original'])
  for k in ['RAW_snapshot','LF_snapshot']:
   if k in q:check(q[k])
def freeze():
 save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),utc=now(),owned_scope=O.as_posix(),scope='Exact two-field process/reader metadata overlay only; no proof/source-final/VERIFIED/exposition or canonical writes.'))
 proposal=read(P/'proposal.json');assert proposal['status']=='PROPOSED_NOT_APPLIED' and len(proposal['changes'])==2
 core=[P/'proposal.json']+[ROOT/c[k] for c in proposal['changes'] for k in ['before','proposed']]+[SOURCE,R/'root.named-literal70.adoption.json',R/'compiler-diagnosis70/header-named-literal70.proposed.lean',ROOT/'runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70/header0-proposed-expanded.lean']+[ROOT/c['path'] for c in proposal['changes']]
 authority=[M/n for n in ['lease.final.json','run.json','decision.json','named-review.payload.json','outputs.manifest.json']];assert len(core)==11 and len(authority)==5
 rows=[]
 for i,p in enumerate(core+authority):
  q=dict(original=pin(p),storage='Exact native authority locator/pin; closed package not copied.' if i>=11 else 'Exact RAW and CRLF-only LF snapshot.')
  if i<11:
   for k,b in [('RAW',p.read_bytes()),('LF',p.read_bytes().replace(b'\r\n',b'\n'))]:
    dest=O/f'inputs/{i:02}.{k}.snapshot';dest.parent.mkdir(exist_ok=True);dest.write_bytes(b);q[k+'_snapshot']=pin(dest)
  rows.append(q)
 proc=subprocess.Popen(['git','rev-parse','HEAD'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=proc.communicate();assert proc.returncode==0
 save('git.observation.json',dict(actual_git_PID=proc.pid,actual_parent_PID=os.getpid(),exit_code=0,terminal_closed=True,HEAD=out.decode().strip(),stderr=err.decode(),qualification='Workspace BASE observation only; metadata proposal is local/unapplied, no new science-commit verification.'))
 save('inputs.manifest.json',dict(input_count=16,exact_snapshot_input_count=11,closed_native_authority_locator_count=5,inputs=rows,LF_recipe='Replace ONLY CRLF with LF; preserve bare CR and all other bytes. RAW authoritative.',finite_historical_maps=[],current_original_inputs_require_exact_equality=True,no_whole_ledger_or_native_package_copies=True))
 print(json.dumps(dict(status='PIN_COMPLETE',actual_PID=os.getpid(),input_count=16,snapshot_count=11,native_locator_count=5)))
def diff(a,b,path=''):
 if type(a)!=type(b):return [dict(pointer=path,before=a,after=b)]
 if isinstance(a,dict):
  assert set(a)==set(b),('object keys changed',path)
  return [x for k in sorted(a) for x in diff(a[k],b[k],path+'/'+k.replace('~','~0').replace('/','~1'))]
 if isinstance(a,list):
  assert len(a)==len(b),('list count changed',path)
  return [x for i,(v,w) in enumerate(zip(a,b)) for x in diff(v,w,path+'/'+str(i))]
 return [] if a==b else [dict(pointer=path,before=a,after=b)]
def review():
 stable();proposal=read(P/'proposal.json');changes=[]
 for c in proposal['changes']:
  before=ROOT/c['before'];after=ROOT/c['proposed'];current=ROOT/c['path'];bb=before.read_bytes();ab=after.read_bytes()
  assert sha(bb)==c['before_RAW_sha256'] and sha(ab)==c['proposed_RAW_sha256'] and current.read_bytes()==bb
  d=diff(read(before),read(after));assert d==[dict(pointer=c['JSON_pointer'],before=c['old'],after=c['new'])]
  assert bb.count(c['old'].encode())==1 and bb.replace(c['old'].encode(),c['new'].encode(),1)==ab
  changes.append(dict(current=pin(current),before=pin(before),proposed=pin(after),JSON_diff=d,RAW_change_is_exact_single_string_replacement=True))
 assert [c['JSON_pointer'] for c in proposal['changes']]==['/purification/dead_code_audit','/items/0/purification/dead_code_audit']
 expected='One public production theorem with an exact private literal statement definition; no proof provider or wrapper Test.';assert all(c['new']==expected for c in proposal['changes'])
 # Independently rebind the CLOSED121 mathematical authority; read hashes, not proof transcripts.
 lease=read(M/'lease.final.json');assert lease['status']=='CLOSED_LAST' and lease['owned_file_count']==121
 assert pin(M/'lease.final.json')['raw_sha256']=='cafa34e277b842fb18d0fa826fefaa882a4d777366265ca3cfb323c3fa3c1093'
 assert {p.relative_to(M).as_posix() for p in M.rglob('*') if p.is_file()}=={q['relative_path'] for q in lease['manifest']}|{'lease.final.json'}
 for q in lease['manifest']:check({k:v for k,v in q.items() if k!='relative_path'})
 mr=read(M/'run.json');assert logical(mr)==mr['run_sha256']=='ccac3218b60a3339a15038e9dd82768e9aa25b85114af3b34a04e27ac39357e0';check(mr['named_complete_RAW_payload'])
 md=read(M/'decision.json');assert md['mathematics_accepted'] and md['representation_accepted'] and not md['SAU_VERIFIED'];assert pin(SOURCE)==md['checked_source'] and pin(SOURCE)['raw_sha256']=='03a0721ae952f744d0bfdf568039b77f7035bec0a50642f8bc8ebc895273b998'
 # Inspect only the exact representation header and declaration counts, not unchanged proofs.
 b=SOURCE.read_bytes();text=b.decode();start=b.index(b'private def actual_projected_rotation_statement\n');end=b.index(b' := by\n',b.index(b'\ntheorem actual_projected_rotation\n',start));header=b[start:end]+b'\n';candidate=R/'compiler-diagnosis70/header-named-literal70.proposed.lean';assert header==candidate.read_bytes()
 assert header==(M/'public-header.exactraw.fragment.lean').read_bytes()
 private_names=re.findall(r'^private def ([^\s]+)',text,re.M);theorems=re.findall(r'^theorem ([^\s]+)',text,re.M);assert private_names==['actual_projected_rotation_statement'] and theorems==['actual_projected_rotation']
 adopter=read(R/'root.named-literal70.adoption.json');assert adopter['mathematical_provider'] is False and adopter['extra_public_premise'] is False and adopter['reader_requires_complete_adjacent_literal_fold']
 assert pin(candidate)['raw_sha256']==adopter['representation_overlay']['RAW_sha256']=='5014d6e596a33ac58479cb19c6adad075ce4a0ed45e54d9ceec38214a144c2f2'
 save('exact-diff-and-authority.json',dict(status='PASS',actual_PID=os.getpid(),changes=changes,changed_JSON_fields_total=2,changed_RAW_string_occurrences_total=2,closed_math_owned_files=121,closed_math_manifest_rows_checked=120,closed_math_logical=mr['run_sha256'],closed_math_named_RAW=mr['named_complete_RAW_payload'],closed_math_lease=pin(M/'lease.final.json'),canonical_source=pin(SOURCE),representation_candidate=pin(candidate),public_theorems=theorems,private_literal_Prop_definitions=private_names,mathematical_providers=0,no_new_binder_or_formula_or_BODY=True,no_wrapper_Test_in_current_unit=True,full_prior_proofs_replayed=False))
 payload=dict(schema='independent-metadata-repair70-complete-native-review-v1',actor=ACTOR,status=STATUS,actual_review_PID=os.getpid(),utc=now(),proposal=pin(P/'proposal.json'),input_count=16,snapshot_input_count=11,closed_native_authority_locator_count=5,LF_recipe=get('inputs.manifest.json')['LF_recipe'],independent_findings=['The old no-private-Prop planning text is stale: exact canonical header contains one complete private literal Prop definition and one public production theorem.','Both proposed JSON files differ only at their specified dead_code_audit pointers; even exact RAW files are solely the same one-string replacement. All other bytes, fields, assumptions, declarations, proof BODY and formulas are unchanged.','An exact private literal statement definition stores the proposition; it is not a proof provider or an additional public hypothesis. Canonical source equals the CLOSED121 accepted full theorem mathematics source and prior independently admitted literal representation.','No wrapper Test is introduced by this overlay or present as a declaration in the reviewed single production module. This wording does not claim absence of Tests elsewhere in the repository.','The proposed phrase accurately reports public/private representation and does not grant final source review, theorem VERIFIED, PURIFIED, full Exposition Seal or whole-paper completion.'],exact_changes=changes,checked_source=pin(SOURCE),closed_math_authority=dict(lease=pin(M/'lease.final.json'),run=pin(M/'run.json'),whole_logical_run_sha256=mr['run_sha256'],named_complete_RAW=mr['named_complete_RAW_payload'],decision=pin(M/'decision.json'),owned_file_count=121,all120_manifest_rows_exact=True),representation=pin(candidate),approval='Approve applying exactly these two strings only, then root must refresh publication binding/context and official source packet as proposed. No canonical application performed by this reviewer.',residuals=['Final whole-module source70 review and source admission remain separate.','Complete adjacent initially folded literal definition and proof exposition still require reader admission; no full Exposition Seal.','No exact SCI70 verification, SAU VERIFIED, aggregate/root/site or mathematical dependency credit is granted.'],canonical_writes=False,ledger_writes=False,Lean_compiler_run=False,proof_search=False,source_packet_writes=False,previous_closed_scopes_modified=False,evidence=pin(O/'exact-diff-and-authority.json'),closure_contract='Native complete named RAW payload separately hashed from whole logical run omitting only top-level run_sha256. Every owned input/helper/terminal/failure/self layer appears in final manifest/last lease. Read-only postclose performs no owned writes.')
 save('named-review.payload.json',payload);save('decision.json',dict(schema='independent-metadata-repair70-decision-v1',actor=ACTOR,status=STATUS,actual_PID=os.getpid(),utc=now(),proposal=pin(P/'proposal.json'),named_complete_RAW_payload=pin(O/'named-review.payload.json'),approved=True,approved_change_count=2,approved_scope='Exactly specified two single-string metadata changes.',source_final=False,SAU_VERIFIED=False,full_Exposition_Seal=False,canonical_applied=False,mathematical_or_source_assumption_repair=False))
 print(json.dumps(dict(status=STATUS,actual_PID=os.getpid(),changed_fields=2,named_complete_RAW_payload=pin(O/'named-review.payload.json'))))
def validate():
 stable();d=get('decision.json');assert d['approved'] and d['approved_change_count']==2 and not d['canonical_applied'];check(d['named_complete_RAW_payload']);assert get('exact-diff-and-authority.json')['status']=='PASS'
 for n in ['freeze','review']:
  t=get(n+'.terminal.json');assert t['exit_code']==0 and t['terminal_closed'];check(t['executed_helper_RAW'])
def finalize():
 validate();baseline=[dict(relative_path=p.relative_to(O).as_posix(),**pin(p)) for p in files() if p.name!='run.json' and not p.name.startswith('finalizer.')]
 r=dict(schema='independent-metadata-repair70-native-run-v1',actor=ACTOR,status=STATUS,actual_finalizer_PID=os.getpid(),utc=now(),complete_named_review=get('named-review.payload.json'),named_complete_RAW_payload=pin(O/'named-review.payload.json'),decision=get('decision.json'),inputs=get('inputs.manifest.json'),baseline_owned_files=baseline,stage_terminals={n:get(n+'.terminal.json') for n in ['freeze','review']},hash_contract='Canonical UTF8 logical JSON omits ONLY top-level run_sha256; complete named RAW is independently exact-byte hashed.',closure_contract='Final output manifest and last CLOSED_LAST lease bind all owned files including helper/terminal/failure/self layers. No write follows lease; external postclose reads lease RAW.')
 r['run_sha256']=logical(r);save('run.json',r);print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=r['run_sha256'])))
def readback():
 validate();r=get('run.json');assert logical(r)==r['run_sha256']
 for q in r['baseline_owned_files']:check({k:v for k,v in q.items() if k!='relative_path'})
 save('readback.json',dict(status='PASS',actual_PID=os.getpid(),utc=now(),run=pin(O/'run.json'),named_complete_RAW_payload=pin(O/'named-review.payload.json'),whole_logical_run_sha256=r['run_sha256']));print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid())))
def preclose():
 validate();r=get('run.json');assert logical(r)==r['run_sha256'];check(get('readback.json')['run'])
 for n in ['finalizer','readback']:assert get(n+'.terminal.json')['exit_code']==0
 print(json.dumps(dict(status='PRECLOSE_PASS',actual_PID=os.getpid())))
def postclose():
 l=get('lease.final.json');assert l['status']=='CLOSED_LAST';rows=l['manifest'];assert len(rows)==l['owned_file_count']-1;assert {p.relative_to(O).as_posix() for p in files()}=={q['relative_path'] for q in rows}|{'lease.final.json'}
 for q in rows:check({k:v for k,v in q.items() if k!='relative_path'})
 assert sha(json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==l['manifest_logical_sha256'];validate();r=get('run.json');assert logical(r)==r['run_sha256'];m=get('outputs.manifest.json');assert m['expected_owned_file_count']==l['owned_file_count']
 for q in m['files']:check({k:v for k,v in q.items() if k!='relative_path'})
 print(json.dumps(dict(status='POSTCLOSE_READONLY_PASS',actual_postclose_PID=os.getpid(),postclose_owned_writes=0,owned_file_count=l['owned_file_count'],whole_logical_run_sha256=r['run_sha256'],named_complete_RAW_payload=pin(O/'named-review.payload.json'),inputs_manifest_RAW=pin(O/'inputs.manifest.json'),outputs_manifest_RAW=pin(O/'outputs.manifest.json'),closure_manifest_logical_sha256=l['manifest_logical_sha256'],lease_RAW=pin(O/'lease.final.json'),foreground_terminals={n:dict(worker_PID=get(n+'.terminal.json')['actual_worker_PID'],runner_PID=get(n+'.terminal.json')['actual_runner_PID'],exit_code=get(n+'.terminal.json')['exit_code']) for n in ['freeze','review','finalizer','readback','close']})))
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
