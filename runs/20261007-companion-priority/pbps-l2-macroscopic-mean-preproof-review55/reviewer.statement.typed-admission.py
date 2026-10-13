from pathlib import Path
import json,hashlib,datetime,re
root=Path('E:/Samplinglib');p=Path(__file__).parent
pre=root/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean-preproof55'
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def fp(path,b=None):
 path=Path(path);b=path.read_bytes() if b is None else b
 return dict(path=str(path).replace('\\','/'),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
def load(path):return json.loads(Path(path).read_bytes())
def seal(x,k):x[k]=sha(canon(x));return x
def checklogical(x,k):v=dict(x);v.pop(k);assert sha(canon(v))==x[k]
def write(path,x):
 assert not path.exists(),str(path)
 b=(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8');path.write_bytes(b);return fp(path,b)
leasepath=p/'reviewer.statement.typed-admission.lease.json';lease=load(leasepath);assert lease['status']=='OPEN'
oldreview=load(p/'statement.signature-stage.review.json');oldrun=load(p/'statement.signature-stage.run.json');oldlease=load(p/'reviewer.statement.lease.json')
checklogical(oldreview,'review_run_sha256');checklogical(oldrun,'run_sha256');checklogical(oldlease,'lease_run_sha256')
assert oldreview['final_statement_seal_admitted']==False and oldreview['typing_status'].startswith('PENDING')
assert oldlease['status']==oldlease['read']==oldlease['write']==oldlease['Python']=='CLOSED'
assert oldreview['verdict']=='accepted-scoped-signature-only-pending-typecheck'
for x in oldreview['input_artifacts']:assert fp(x['path'])==x,x['path']
sig=(pre/'prospective-statement.txt').read_text(encoding='utf-8')
assert len(sig.encode())==2526 and sha(sig.encode())==oldreview['signature_sha256']=='0c4a69c99eb2dc8572af054133619442ccaf8e2e91ca19e130f4b1b5fc4cee3f'
src=pre/'statement-typecheck.lean';snapshot=pre/'statement.typecheck.0.source.raw.snapshot.lean'
assert src.read_bytes()==snapshot.read_bytes()
probe=src.read_text(encoding='utf-8');assert probe.count('#check fun ')==1
payload=probe.split('#check fun ',1)[1]
expected=sig.split('\n',1)[1]
assert expected.count(' :\n    let μ :=')==1
expected=expected.replace(' :\n    let μ :=',' =>\n    let μ :=',1)
assert payload==expected
assert not re.search(r'\b(sorry|admit|axiom|by)\b',probe)
assert not re.search(r'^\s*(theorem|def|lemma|instance)\b',probe,re.M)
status=load(pre/'statement.typecheck.0.status.json');cl=load(pre/'statement.typecheck.0.compiler.lease.json')
log=(pre/'statement.typecheck.0.log').read_bytes();logtext=log.decode('utf-8')
assert status['exit_code']==cl['exit_code']==0
assert status['process_id']==cl['process_id']==29656
assert cl['status']==cl['compiler']==cl['Python']=='CLOSED'
assert status['command']==cl['command'] and status['command'][:3]==['lake','env','lean']
assert status['source_raw_sha256']==cl['source_raw_sha256']==sha(src.read_bytes())
assert status['log_raw_sha256']==sha(log)
assert cl['opened_utc']<status['finished_utc']<=cl['closed_utc']
assert len(re.findall(r'^.*\.lean:\d+:\d+: warning:',logtext,re.M))==6 and logtext.count('is not explicitly referenced.')==6 and 'error:' not in logtext and '→ Prop' in logtext
paths=[p/'statement.signature-stage.review.json',p/'statement.signature-stage.run.json',p/'reviewer.statement.lease.json',p/'statement.input-bindings.json',pre/'statement.typecheck.0.status.json',pre/'statement.typecheck.0.log',pre/'statement.typecheck.0.compiler.lease.json',snapshot,src,p/'typed-admission.opening.lease.raw.snapshot.json']
inputs=oldreview['input_artifacts']+[fp(x) for x in paths]
snapdir=p/'typed-admission.raw.snapshots';assert not snapdir.exists();snapdir.mkdir()
rows=[]
for i,x in enumerate(inputs):
 b=Path(x['path']).read_bytes();t=snapdir/f'{i:02d}.raw.snapshot';t.write_bytes(b);rows.append(dict(original=x,snapshot=fp(t,b)))
invpin=write(p/'statement.typed-admission.input-bindings.json',dict(schema_version=1,input_artifacts=inputs,raw_snapshots=rows,original_signature_stage_and_primary_bytes_unchanged=True))
review=seal(dict(schema_version=1,reviewer='phase_source_reviewer_20261005',stage='DISTINCT_FINAL_TYPED_STATEMENT_ADMISSION55',status='ACCEPTED_SCOPED_PROSPECTIVE_STATEMENT_ONLY',verdict='accepted-scoped-statement-only',blocking=False,final_statement_seal_admitted=True,declaration=oldreview['declaration'],signature_sha256=oldreview['signature_sha256'],signature_LF_bytes=2526,original_pending_signature_review=fp(p/'statement.signature-stage.review.json'),original_pending_review_logical_sha256=oldreview['review_run_sha256'],original_pending_lease=fp(p/'reviewer.statement.lease.json'),primary_contract=oldreview['primary_contract'],primary_contract_logical_sha256=oldreview['primary_contract_logical_sha256'],semantic_slots=oldreview['semantic_slots'],binder_classification=oldreview['binder_classification'],explicit_extensions=oldreview['explicit_extensions'],deltas=[],repairs=[],source_excess=[],independent_from_future_formalizer=True,independent_from_future_decoder=True,input_artifacts=inputs,input_snapshot_inventory=invpin,type_elaboration={'actual_process_id':29656,'exit_code':0,'body_free_source_payload_equal':True,'mechanical_projection':'Remove theorem name line and replace ONLY the single theorem delimiter before let mu (colon) with fun arrow; all binders/definition/conclusions literal LF equal.', 'actual_source_raw_sha256':status['source_raw_sha256'],'actual_log_raw_sha256':status['log_raw_sha256'],'compiler_opened_utc':cl['opened_utc'],'compiler_closed_utc':cl['closed_utc'],'compiler_lease_actually_closed':True,'printed_type_ends_Prop':True,'warnings':'Exactly six unused hypothesis-name warnings from body-free proposition rendering. No error or mathematical premise removal.'},review_evidence='Distinct typed stage recomputed the original mathematical signature review logical hash, original CLOSED lease, all original source/API/proposal inputs and current exact2526 header. Actual anonymous #check fun payload differs only by syntactic theorem-to-function projection, with no proof/declaration/axiom/sorry/admit. Status/log/source/PID29656/CLOSED compiler evidence match exact raw bytes and actual EXIT0. Original pending receipt remains unchanged; this successor admits only the prospective exact StatementSeal, not SourceGraph or theorem proof.',actual_source_and_mathematical_scope_reused='Only unchanged seven-slot/binder review reused after strict original byte equality; every-y literal S vs ν-AE rough fibers/mean remains distinct. Internal probabilities/coherence/domains/norm-defect outputs, no gradient/H1/Gamma or certificate inputs.',source_topology_reviewed=False,implementation_or_proof_reviewed=False,compiler_started_by_reviewer=False,remaining_boundary=['Distinct source topology and actual implementation/full proof/source fidelity', 'Density/differences/closed-gradient/H1/Gamma/B13/halfturn/main/cost/composition/full reader'],hash_recipe='review_run_sha256=SHA256 sorted compact ensure_ascii=False UTF8 entire receipt minus review_run_sha256,allow_nan=False,no trailing newline.'),'review_run_sha256')
reviewpin=write(p/'statement.typed-admission.review.json',review)
for x in inputs:assert fp(x['path'])==x,x['path']
run=seal(dict(schema_version=1,reviewer=review['reviewer'],stage=review['stage'],opened_utc=lease['opened_utc'],completed_utc=now(),input_artifacts=inputs,output_artifacts=[reviewpin,invpin,fp(__file__)],actual_source_inputs_pre_post_equal=True,compiler_started=False,final_statement_seal_admitted=True,hash_recipe='run_sha256=SHA256 sorted compact ensure_ascii=False UTF8 entire run minus run_sha256,allow_nan=False,no newline.'),'run_sha256')
runpin=write(p/'statement.typed-admission.run.json',run)
lease.update(status='CLOSED',read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',compiler_started=False,closed_utc=now(),input_artifacts=inputs,outputs=[reviewpin,invpin,runpin],review_run_sha256=review['review_run_sha256'],run_sha256=run['run_sha256'],final_statement_seal_admitted=True,hash_recipe='lease_run_sha256=SHA256 sorted compact ensure_ascii=False UTF8 entire lease minus lease_run_sha256,allow_nan=False,no newline.')
seal(lease,'lease_run_sha256');b=(json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode();leasepin=fp(leasepath,b)
leasepath.write_bytes(b)
print(json.dumps(dict(review=reviewpin,review_logical=review['review_run_sha256'],run=runpin,run_logical=run['run_sha256'],lease=leasepin,all_roles_CLOSED=True,compiler='NOT_STARTED_CLOSED',final_statement_seal_admitted=True),ensure_ascii=False))
