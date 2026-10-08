from common import *
sys.dont_write_bytecode=True
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis, astis_publication as pub, astis_advance as advance
assert git('rev-parse','HEAD')==HEAD and git('rev-parse',HEAD+'^')==SCI
assert not git('diff','--name-only','HEAD')
originals=strict(); dump('original-inputs.pre.json',dict(status='PASS',math=552,source=566,total=1118,checks=originals))

# Validate complete immutable native runs and separate binding payloads.
native=[]; counts={}; inputchecks=[]; outputchecks=[]
mapping=load(B/'verified-inputs.before-shared-integration.json')
assert len(mapping['mappings'])==1 and mapping['mappings'][0]['original']['path']==CELL
before=mapping['mappings'][0]; assert equal(before['original'],before['snapshot']['path']) and equal(before['snapshot'])
for stage,payloadkey,payloadsha in [('whole-proof-review54','run_binding_payload','review_run_binding_sha256'),('exact-verification54','run_binding_payload','review_run_binding_sha256')]:
 run=load(B/stage/'run.json'); native.append(selfcheck(B/stage/'run.json'))
 assert logical(run[payloadkey])==run[payloadsha]
 for e in run['actual_inputs']:
  same=equal(e); replacement=None
  if not same:
   assert stage=='exact-verification54' and e['path'].replace('\\','/')==CELL
   assert equal(e,before['snapshot']['path']) and e['raw_sha256']==before['original']['raw_sha256']; replacement=pin(before['snapshot']['path'])
  inputchecks.append(dict(stage=stage,original=e,current=pin(e['path']),current_equal=same,explicit_BEFORE_shared_snapshot=replacement,ok=True))
 for e in run['actual_outputs']:
  assert equal(e),e['path']; outputchecks.append(dict(stage=stage,input=e,ok=True))
 counts[stage]=dict(inputs=len(run['actual_inputs']),outputs=len(run['actual_outputs']))
 lease=load(B/stage/'lease.json'); assert lease['status']==lease['read']==lease['write']==lease['Python']==lease['compiler']=='CLOSED' and lease['exit_code']==0
 assert lease['run_logical_sha256']==run['run_sha256'] and lease['review_payload_sha256']==run[payloadsha]
 for k in ['receipt','run','actual_compiler_CLOSED_lease']: assert equal(lease[k])
 compiler=load(lease['actual_compiler_CLOSED_lease']['path']); assert compiler['status']=='CLOSED' and compiler['exit_code']==0
 if stage=='exact-verification54': assert equal(lease['verified']) and run['checked_commit']==SCI and run['focused_build_invocations']==1 and not run['forced_rebuild']

source=load(B/'source.0.review.json'); sr=load(B/'reviewer.source.run.json'); native.append(selfcheck(B/'reviewer.source.run.json'))
assert logical(sr['reviewer_run_binding_payload'])==sr['reviewer_run_binding_sha256']==source['review_run_sha256']
assert sr['verdict']==source['verdict']=='equivalent-after-elaboration' and source['independent_from_formalizer'] and source['independent_from_decoder'] and not source['repairs']
for e in sr['output_artifacts_before_run_and_leases']: assert equal(e)
closure=[]
for k,p in [('own','reviewer.source.lease.json'),('provided_root','source.review.lease.json')]:
 d=load(B/p); core={x:y for x,y in d.items() if x not in {'native_output_artifacts','native_run_artifact'}}
 assert core==sr['expected_final_lease_closure_cores'][k] and logical(core)==sr['expected_closure_core_logical_sha256'][k] and d['status']=='CLOSED'
 for e in d['native_output_artifacts']: assert equal(e)
 assert equal(d['native_run_artifact'])
 closure.append(dict(input=pin(B/p),core_logical_sha256=logical(core),recipe='Complete actual CLOSED lease minus ONLY native_output_artifacts and native_run_artifact; compare exact full native expected core'))
sp=sr['reviewer_run_binding_payload']; packet=load(B/'source.0.reviewer-packet.json')
assert sp['packet_raw_sha256']==pin(B/'source.0.reviewer-packet.json')['raw_sha256'] and sp['packet_internal_sha256']==source['reviewer_packet_sha256']==packet['packet_sha256']
assert sp['input_bindings_raw_sha256']==pin(B/'reviewer.source.input-bindings.json')['raw_sha256'] and sp['seven_slot_semantics_logical_sha256']==logical(source['semantic_slots']) and sp['publication_binding_sha256']==PUBSHA
assert equal(sp['current_production']) and equal(sp['current_Test'])
dr=load(B/'anonymous-decoder/run.json'); res=load(B/'anonymous-decoder/result0.json'); br=load(B/'anonymous-decoder/binding-receipt.json'); dl=load(B/'anonymous-decoder/lease.json'); native.append(selfcheck(B/'anonymous-decoder/run.json'))
assert logical(dr['decoder_binding_payload'])==dr['decoder_binding_sha256']==dr['decoder_run_sha256']==res['decoder_run_sha256']
dp=dr['decoder_binding_payload']; assert logical({k:v for k,v in res.items() if k not in dp['semantic_result_excluded_fields']})==dp['semantic_result_sha256']
assert isinstance(res['decoder'],str) and isinstance(res['reconstructed_theorem_text'],str) and sha(res['reconstructed_theorem_text'].encode())==res['reconstructed_text_sha256']
assert not res['source_text_visible'] and dr['source_text_blind'] and not dp['strict_source_identity_blind_claim'] and dl['status']=='CLOSED' and not dl['compiler_started']
for d in [br,dr,dl]:
 for e in d['output_artifacts']: assert equal(e)
assert equal(br['actual_closed_lease']) and equal(br['actual_run']) and dl['complete_logical_run_sha256']==dr['run_sha256'] and dl['decoder_binding_sha256']==dr['decoder_binding_sha256']

audit=load(AUDIT); assert audit['state']==audit['source_review']['state']=='accepted' and audit['verdict']==source['verdict'] and audit['source_review']['review_run_sha256']==source['review_run_sha256'] and not audit['repairs']
assert audit['semantic_slots']==source['semantic_slots'] and len(audit['deltas'])==len(source['deltas'])==3 and {x['slot'] for x in audit['deltas']}=={'domains','scopes','conclusion'}
assert all(x['severity']=='informational' for x in audit['deltas']) and [x['native_delta'] for x in audit['deltas']]==source['deltas']
exposure=source['exposure_disclosure']; assert exposure['source_text_visible'] and not exposure['strict_source_identity_blindness'] and not exposure['whole_math_files_read'] and not exposure['indirect_verdict_used_or_replayed']
assess=exposure['indirect_math_review_capsule_exposure']; assert sha(path(assess['semantic_assessment_checkpoint']).read_bytes())==assess['actual_raw_sha256']
pub.check_advance([TARGET],reviewed=True)
item=next(i for i in pub.load() if any(b['declaration']==TARGET for b in i['bindings'])); binding=next(b for b in item['bindings'] if b['declaration']==TARGET)
bp=pub.binding_payload(item,binding); assert pub.binding_digest(item,binding)==PUBSHA==audit['publication_binding_sha256']==source['publication_binding_sha256']
dump('publication-binding.actual.json',dict(status='PASS',actual_full_payload=bp,actual_full_binding_sha256=PUBSHA,real_reviewed_check_advance=True))

body='AutoSamplingTheory/ExampleCases/ProximalBPS/SourceMeanGradientDomain.lean'; test='Tests/ProximalBPSSourceMeanGradientDomain.lean'
for p,n in [(body,'production.actual.raw.snapshot.lean'),(test,'Tests.actual.raw.snapshot.lean')]:
 assert path(p).read_bytes()==path(B/'whole-proof-review54'/n).read_bytes()==path(B/'exact-verification54'/n).read_bytes(); (O/n).write_bytes(path(p).read_bytes())
b=path(body).read_bytes().replace(b'\r\n',b'\n'); start=b.index(b'theorem literal_source_mean_in_closed_gradient'); end=b.index(b' := by',start); header=b[start:end]+b'\n'
assert len(header)==1448 and sha(header)=='19de42336148aa900917e6c77753325145d6010dfd1718c1625b2b9a8f7ce595'
scan=[]
for row in load(B/'whole-proof-review54/checks.json')['fake_closure_scan']:
 e=row['input']; assert equal(e); text=astis.strip_lean_comments_and_strings(path(e['path']).read_text(encoding='utf-8'))
 hits=[n for n,l in enumerate(text.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)]; assert not hits; scan.append(dict(input=pin(e['path']),hits=hits))
focused=path(B/'exact-verification54/focused.log').read_text(encoding='utf-8')
assert 'Build completed successfully (3898 jobs).' in focused and 'sorryAx' not in focused
prints=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",focused); assert len(prints)==6 and all(set(re.findall(r'[A-Za-z_.]+',a))=={'propext','Classical.choice','Quot.sound'} for n,a in prints)

# Exact scientific810 and integration-owned paths, using actual Git blobs.
parent=git('rev-parse',SCI+'^'); sciencepaths=git('diff','--name-only',parent,SCI).splitlines(); integrationpaths=git('diff','--name-only',SCI,HEAD).splitlines()
assert len(sciencepaths)==810 and not any(re.search(r'(?i)(?:^|/)[^/]*55(?:/|$)',p) for p in sciencepaths+integrationpaths)
prior=load(B/'exact-verification54/git-owned-file-bindings.json'); assert prior['count']==810
old={e['current']['path']:e for e in prior['bindings']}; assert set(old)==set(sciencepaths)
requests=[(SCI,p) for p in sciencepaths]+[(HEAD,p) for p in sorted(set(sciencepaths+integrationpaths))]
batch=subprocess.run(['git','cat-file','--batch'],cwd=R,input=''.join(c+':'+p+'\n' for c,p in requests).encode(),capture_output=True,check=True)
buf=batch.stdout; pos=0; blobs={}
for c,p in requests:
 stop=buf.index(b'\n',pos); h=buf[pos:stop].split(); assert len(h)==3 and h[1]==b'blob'; size=int(h[2]); pos=stop+1; blob=buf[pos:pos+size]; pos+=size; assert buf[pos:pos+1]==b'\n'; pos+=1; blobs[(c,p)]=blob
assert pos==len(buf)
rows=[]; changed=[]
for p in sciencepaths:
 raw=blobs[(SCI,p)]; assert sha(raw)==old[p]['Git_blob_raw_sha256'] and sha(raw.replace(b'\r\n',b'\n'))==old[p]['Git_blob_LF_sha256']
 same=raw.replace(b'\r\n',b'\n')==path(p).read_bytes().replace(b'\r\n',b'\n')
 if not same: assert p in integrationpaths; changed.append(p)
 rows.append(dict(scientific_path=p,science_Git_blob_raw_sha256=sha(raw),science_Git_blob_LF_sha256=sha(raw.replace(b'\r\n',b'\n')),matches_closed_exact_Git_binding=True,current=pin(p),current_science_LF_equal=same,explicit_integration_change=not same))
headrows=[]
for p in sorted(set(sciencepaths+integrationpaths)):
 blob=blobs[(HEAD,p)]; assert blob.replace(b'\r\n',b'\n')==path(p).read_bytes().replace(b'\r\n',b'\n'),p
 headrows.append(dict(current=pin(p),HEAD_Git_blob_raw_sha256=sha(blob),HEAD_Git_blob_LF_sha256=sha(blob.replace(b'\r\n',b'\n')),current_HEAD_LF_equal=True))
assert body not in changed and test not in changed and AUDIT not in changed and not any('/publications/' in p or '/declaration_lessons/' in p for p in changed)
dump('git-bindings.json',dict(status='PASS',science=SCI,science_parent=parent,integration=HEAD,integration_parent=SCI,science_count=810,integration_count=len(integrationpaths),current_union_count=len(headrows),exact_integration_paths=integrationpaths,explicit_science_paths_changed_by_integration=changed,science_bindings=rows,current_HEAD_bindings=headrows))
diff=subprocess.check_output(['git','diff',SCI,HEAD,'--',*changed],cwd=R); (O/'shared-metadata.actual.diff').write_bytes(diff)

state=advance.current_advances(); sa=state[ADV]; assert sa['state']=='VERIFIED' and sa['owner_id']!='whole_math52'
lane=[i for i,d in state.items() if d.get('state')=='STABILIZING']; assert lane==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
cell=load(CELL); oldcell=load(before['snapshot']['path']); assert cell['status']==oldcell['status']=='independently_verified'
assert isinstance(cell['evidence']['independent_verification'],str) and cell['evidence']['independent_verification']==oldcell['evidence']['independent_verification']
delta={k:dict(before=oldcell.get(k),current=cell.get(k)) for k in set(oldcell)|set(cell) if oldcell.get(k)!=cell.get(k)}
dump('cell-integration-delta.json',dict(status='NEEDS_SEMANTIC_INSPECTION',before_mapping=before,current=pin(CELL),changed_keys=sorted(delta),exact_delta=delta))
ledger=[json.loads(l) for l in path('runs/substantive_advances.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
transitions=[d for d in ledger if d.get('advance_id')==ADV and d.get('state')=='VERIFIED']; dump('ledger54.verified.actual.json',transitions)
dump('native.checks.json',dict(status='PASS',checked_science=SCI,checked_integration=HEAD,counts=counts,complete_full_runs=native,math_payload_sha256=load(B/'whole-proof-review54/run.json')['review_run_binding_sha256'],exact_payload_sha256=load(B/'exact-verification54/run.json')['review_run_binding_sha256'],source_payload_sha256=source['review_run_sha256'],decoder_payload_sha256=dr['decoder_binding_sha256'],source_closure_core_checks=closure,actual_native_input_checks=inputchecks,actual_native_output_checks=outputchecks,source_three_informational_elaborations=True,source_exposure=exposure,decoder_source_text_blind=True,decoder_strict_identity_blind=False,publication_binding_sha256=PUBSHA,source_audit=pin(AUDIT),fake_closure_scan=scan,exact_signature_LF_bytes=len(header),exact_signature_LF_sha256=sha(header),production=pin(body),Tests=pin(test),standard_axiom_closures=6,prior_exact_compiler_PID=7412,prior_whole_math_compiler_PID=37192,new_compiler_invocations=0,current_SAU='VERIFIED',sole_STABILIZING=lane,mathematical_analysis_reused_without_reproof=True))
print(json.dumps(dict(status='PASS',math_originals=552,source_originals=566,native_stage_counts=counts,science_owned=810,integration_owned=len(integrationpaths),current_union=len(headrows),changed_science_paths=changed,cell_changed_keys=sorted(delta),complete_runs=len(native),new_compilers=0)))
