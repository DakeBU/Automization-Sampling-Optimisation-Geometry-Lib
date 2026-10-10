from verify import *
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis,astis_publication as pub,astis_advance as advance
assert git('rev-parse','HEAD')==COMMIT and load(O/'compiler.lease.json')['status']=='CLOSED'
native=[]
mathrun=load(B/'whole-proof-review54/run.json');native.append(selfcheck(B/'whole-proof-review54/run.json'))
assert logical(mathrun['run_binding_payload'])==mathrun['review_run_binding_sha256']=='c6d5c759f5b73d0ee685be12b9e8ca12dfa5bdccd138a01bfe172fcfc9ab277f'
for e in mathrun['actual_outputs']:assert equal(e),e['path']
for e in mathrun['actual_inputs']:assert equal(e),e['path']
mathlease=load(B/'whole-proof-review54/lease.json');assert mathlease['status']==mathlease['read']==mathlease['write']==mathlease['Python']==mathlease['compiler']=='CLOSED' and mathlease['exit_code']==0 and mathlease['actual_focused_compiler_pid']==37192
assert equal(mathlease['receipt']) and equal(mathlease['run']) and equal(mathlease['actual_compiler_CLOSED_lease'])
assert mathlease['run_logical_sha256']==mathrun['run_sha256']=='2cde558942a0498240f9168973abe93589dde07e9317da357bb8f50860c60cc5'
source=load(B/'source.0.review.json');sr=load(B/'reviewer.source.run.json');native.append(selfcheck(B/'reviewer.source.run.json'))
assert logical(sr['reviewer_run_binding_payload'])==sr['reviewer_run_binding_sha256']==source['review_run_sha256']=='c31132907ed4ec78df5d49212de76d3dbc559139b5d8ee2bd2497e5200b195da'
assert sr['verdict']==source['verdict']=='equivalent-after-elaboration' and source['independent_from_formalizer'] and source['independent_from_decoder'] and not source['repairs']
for e in sr['output_artifacts_before_run_and_leases']:assert equal(e),e['path']
closure=[]
for k,p in [('own','reviewer.source.lease.json'),('provided_root','source.review.lease.json')]:
 d=load(B/p);core={x:y for x,y in d.items() if x not in {'native_output_artifacts','native_run_artifact'}};assert core==sr['expected_final_lease_closure_cores'][k] and logical(core)==sr['expected_closure_core_logical_sha256'][k]
 assert d['status']=='CLOSED'
 for e in d['native_output_artifacts']:assert equal(e)
 assert equal(d['native_run_artifact']);closure.append(dict(input=pin(B/p),actual_core=core,core_logical_sha256=logical(core),recipe='Actual closed lease minus ONLY native_output_artifacts and native_run_artifact; exact full core equals native expected projection'))
payload=sr['reviewer_run_binding_payload'];packet=load(B/'source.0.reviewer-packet.json');assert payload['packet_raw_sha256']==pin(B/'source.0.reviewer-packet.json')['raw_sha256'] and payload['packet_internal_sha256']==source['reviewer_packet_sha256']==packet['packet_sha256']
assert payload['input_bindings_raw_sha256']==pin(B/'reviewer.source.input-bindings.json')['raw_sha256'] and payload['seven_slot_semantics_logical_sha256']==logical(source['semantic_slots']) and payload['publication_binding_sha256']==PUBSHA
assert equal(payload['current_production']) and equal(payload['current_Test'])
dr=load(B/'anonymous-decoder/run.json');res=load(B/'anonymous-decoder/result0.json');br=load(B/'anonymous-decoder/binding-receipt.json');dl=load(B/'anonymous-decoder/lease.json');native.append(selfcheck(B/'anonymous-decoder/run.json'))
assert logical(dr['decoder_binding_payload'])==dr['decoder_binding_sha256']==dr['decoder_run_sha256']==res['decoder_run_sha256']=='3b9a6f4630e65ce7bac453f1da176caa9eecbbbcb247f691b846d7fe2b31b57a'
dp=dr['decoder_binding_payload'];assert logical({k:v for k,v in res.items() if k not in dp['semantic_result_excluded_fields']})==dp['semantic_result_sha256']
assert isinstance(res['decoder'],str) and isinstance(res['reconstructed_theorem_text'],str) and sha(res['reconstructed_theorem_text'].encode())==res['reconstructed_text_sha256']
assert not res['source_text_visible'] and dr['source_text_blind'] and not dp['strict_source_identity_blind_claim'] and dl['status']=='CLOSED' and not dl['compiler_started']
for e in br['output_artifacts']:assert equal(e)
for e in dr['output_artifacts']:assert equal(e)
for e in dl['output_artifacts']:assert equal(e)
assert equal(br['actual_closed_lease']) and equal(br['actual_run'])
assert dl['complete_logical_run_sha256']==dr['run_sha256'] and dl['decoder_binding_sha256']==dr['decoder_binding_sha256']
audit=load(AUDIT);assert audit['state']==audit['source_review']['state']=='accepted' and audit['verdict']==source['verdict'] and audit['source_review']['review_run_sha256']==source['review_run_sha256'] and audit['source_review']['reviewer']==source['reviewer'] and not audit['repairs']
assert audit['semantic_slots']==source['semantic_slots'] and len(audit['deltas'])==len(source['deltas'])==3
assert {x['slot'] for x in audit['deltas']}=={'domains','scopes','conclusion'} and all(x['severity']=='informational' for x in audit['deltas'])
assert [x['native_delta'] for x in audit['deltas']]==source['deltas']
exposure=source['exposure_disclosure'];assert exposure['source_text_visible'] and not exposure['strict_source_identity_blindness'] and not exposure['whole_math_files_read'] and not exposure['indirect_verdict_used_or_replayed']
assessment=exposure['indirect_math_review_capsule_exposure'];assert sha(path(assessment['semantic_assessment_checkpoint']).read_bytes())==assessment['actual_raw_sha256']
pub.check_advance([TARGET],reviewed=True);item=next(i for i in pub.load() if any(b['declaration']==TARGET for b in i['bindings']));binding=next(b for b in item['bindings'] if b['declaration']==TARGET);bp=pub.binding_payload(item,binding);assert pub.binding_digest(item,binding)==PUBSHA==audit['publication_binding_sha256']==source['publication_binding_sha256']
dump('publication-binding.actual.json',dict(status='PASS',actual_full_payload=bp,actual_full_binding_sha256=PUBSHA,real_check_advance_reviewed=True,scope='Native full binding, not a projected review_context.'))
body='AutoSamplingTheory/ExampleCases/ProximalBPS/SourceMeanGradientDomain.lean';test='Tests/ProximalBPSSourceMeanGradientDomain.lean'
for p,n in [(body,'production.actual.raw.snapshot.lean'),(test,'Tests.actual.raw.snapshot.lean')]:
 assert path(p).read_bytes()==path(B/'whole-proof-review54'/n).read_bytes();(O/n).write_bytes(path(p).read_bytes())
b=path(body).read_bytes().replace(b'\r\n',b'\n');start=b.index(b'theorem literal_source_mean_in_closed_gradient');end=b.index(b' := by',start);header=b[start:end]+b'\n';assert len(header)==1448 and sha(header)=='19de42336148aa900917e6c77753325145d6010dfd1718c1625b2b9a8f7ce595'
scan=[]
for row in load(B/'whole-proof-review54/checks.json')['fake_closure_scan']:
 e=row['input'];assert equal(e);text=astis.strip_lean_comments_and_strings(path(e['path']).read_text(encoding='utf-8'));hits=[n for n,l in enumerate(text.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)];assert not hits;scan.append(dict(input=pin(e['path']),hits=hits))
log=path(O/'focused.log').read_text(encoding='utf-8');assert 'Build completed successfully (3898 jobs).' in log and 'Replayed Tests.ProximalBPSSourceMeanGradientDomain' in log and 'sorryAx' not in log
prints=re.findall(r"'([^']+)' depends on axioms: \[([^\]]+)\]",log);assert len(prints)==6 and all(set(re.findall(r'[A-Za-z_.]+',a))=={'propext','Classical.choice','Quot.sound'} for n,a in prints)
state=advance.current_advances();sa=state[ADV];assert sa['state']=='PROVED_LOCAL' and sa['owner_id']!='whole_math52';lane=[i for i,d in state.items() if d.get('state')=='STABILIZING'];assert lane==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
assert load(CELL)==load(O/'before.cell.raw.snapshot.json') and load(CELL)['status']=='proved_locally'
ws=load(B/'whitespace-diagnosis54/diagnosis.json');gz=path(ws['gzip']['path']).read_bytes();raw=gzip.decompress(gz);assert sha(gz)==ws['gzip']['raw_sha256'] and sha(raw)==ws['full_negative_raw_sha256'] and int.from_bytes(gz[4:8],'little')==0 and ws['full_staged_exit']==2
for e in ws['immutable_raw_artifacts']:assert equal(e)
parent=git('rev-parse','HEAD^');orig=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--check',parent,COMMIT],cwd=R,capture_output=True);assert orig.returncode==2 and orig.stdout==raw
cmd=['git','-c','core.whitespace=cr-at-eol','diff','--check',parent,COMMIT,'--','.']+[':(exclude)'+e['path'] for e in ws['immutable_raw_artifacts']];authored=subprocess.run(cmd,cwd=R,capture_output=True);(O/'authored-whitespace.log').write_bytes(authored.stdout+authored.stderr);assert authored.returncode==0
dump('native.checks.json',dict(status='PASS',checked_commit=COMMIT,actual_python_pid=os.getpid(),full_math_run=native[0],full_math_payload_sha256=mathrun['review_run_binding_sha256'],complete_math_native_outputs_unchanged=True,source_full_run=native[1],source_payload_sha256=source['review_run_sha256'],source_review=pin(B/'source.0.review.json'),source_native_closures=closure,source_three_information_deltas_preserved=True,source_exposure=exposure,decoder_full_run=native[2],decoder_payload_sha256=dr['decoder_binding_sha256'],decoder_plain_strings=True,source_text_blind=True,strict_identity_blind=False,source_review_verdict=source['verdict'],publication_binding_sha256=PUBSHA,source_audit=pin(AUDIT),fake_closure_scan=scan,signature_LF_bytes=1448,signature_LF_sha256=sha(header),production=pin(body),Tests=pin(test),axiom_prints=[dict(declaration=n,axioms=sorted(re.findall(r'[A-Za-z_.]+',a))) for n,a in prints],target_replayed_not_forced=True,current_SAU='PROVED_LOCAL',independent_verifier='whole_math52',proving_owner=sa['owner_id'],sole_STABILIZING=lane,whitespace=dict(diagnosis=pin(B/'whitespace-diagnosis54/diagnosis.json'),gzip=pin(ws['gzip']['path']),findings=ws['findings'] if isinstance(ws['findings'],int) else len(ws['findings']),exact_immutable_paths=len(ws['immutable_raw_artifacts']),full_staged_exit=2,authored_command=cmd,authored_exit=0,no_full_staged_PASS=True),whole_math_reused_without_replay=True))
strict('inputs.pre-admission.json');print(json.dumps(dict(status='PASS',whole_math_and_source_complete_native=True,source_accepted=True,publication_binding=PUBSHA,actual_focused_PID=7412,source_math_originals=1118,standard_axiom_prints=6,SAU='PROVED_LOCAL',actual_python_pid=os.getpid())))
