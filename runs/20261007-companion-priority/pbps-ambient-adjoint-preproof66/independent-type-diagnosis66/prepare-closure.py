from pathlib import Path
O=Path(__file__).parent
scripts={}
scripts['foreground-finalizer.py']=r'''from pathlib import Path
import json,hashlib,datetime,os
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest()
def read(n):return json.loads((O/n).read_bytes())
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(name=str(p.relative_to(O)).replace('\\','/'),RAW_bytes=len(b),RAW_sha256=H(b),LF_bytes=len(lf),LF_sha256=H(lf))
def put(n,d):(O/n).write_bytes((json.dumps(d,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode())
assert not (O/'lease.final.json').exists()
core=dict(schema='diagnosis66-complete-logical-review-run-v1',owned_path=str(O).replace('\\','/'),owner='/root/independent_source64',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_finalizer_pid=os.getpid(),stage='TYPE-only elaboration diagnosis and separately reviewed process representation overlay; no proof or source candidate admission',summary=read('diagnosis-summary.json'),complete_decisions=read('complete-RAW-decisions.json'),exact_representation_overlay=read('proposed-representation-overlay.json'),complete_probe_results=read('probe-results.json'),exact_binder_conclusion_comparison=read('exact-binder-conclusion-comparison.json'),prior_type_credit_correction=read('prior-type-credit-correction.json'),root_mode_observations=read('root-mode-observations.json'),closed_parent_reuse_pins=read('closed-parent-reuse-pins.json'),pinned_Lean_option_sources=read('lean-option-source-map.json'),complete_RAW_INPUT=read('RAW-input-payload.json'),scope_negatives=read('scope-negatives.json'),observer_negatives=[read('runner-output-encoding-negative.json'),read('package-binder-index-negative.json')],named_payload_roles=dict(COMPLETE_RAW_REVIEW='review-run.json including both complete seven-slot decisions and all process diagnosis/overlay facts, no deletion for RAW hash',COMPLETE_RAW_DECISION='complete-RAW-decisions.json including both full seven-slot process decisions; no deletion for RAW hash',SEPARATE_RAW_INPUT='RAW-input-payload.json finite original-input and root-mode/pinned-local-source maps; contains no candidate decision'),logical_hash_rule='SHA256 of UTF-8 json.dumps(entire parsed review-run object minus ONLY top-level run_sha256, sort_keys=True,separators=(comma,colon),ensure_ascii=False). No other field omitted.',closure_binding_rule='Later actual finalizer/readback/close terminal receipts and this whole RAW review are exhaustively bound in owned-manifest.json; manifest RAW hash is bound in CLOSED_LAST lease.final.json; manifest/lease self bytes are externally read back after closure, without circular self hash.',pre_finalizer_all_owned_file_bindings=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()])
core['run_sha256']=H(json.dumps(core,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
put('review-run.json',core)
res=dict(schema='diagnosis66-foreground-finalizer-result-v1',actual_foreground_pid=os.getpid(),logical_run_sha256=core['run_sha256'],COMPLETE_RAW_REVIEW=pin(O/'review-run.json'),COMPLETE_RAW_DECISION=pin(O/'complete-RAW-decisions.json'),SEPARATE_RAW_INPUT=pin(O/'RAW-input-payload.json'),assertions_passed=True)
put('foreground.finalizer.result.json',res);print(json.dumps(res,sort_keys=True),flush=True)
'''
scripts['foreground-readback.py']=r'''from pathlib import Path
import json,hashlib,datetime,os
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest()
def read(n):return json.loads((O/n).read_bytes())
d=read('review-run.json');expected=d.pop('run_sha256');assert H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())==expected
assert d['complete_decisions']==read('complete-RAW-decisions.json')
assert len(d['complete_decisions']['decisions'])==2
for dec in d['complete_decisions']['decisions']:
 assert set(dec['seven_semantic_slots'])==set(['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']);assert dec['semantic_deltas']==[];assert not dec['kernel_proof_credit'];assert not dec['repairs']['source_mathematical_repair']
for x in d['pre_finalizer_all_owned_file_bindings']:
 b=(O/x['name']).read_bytes();assert H(b)==x['RAW_sha256'];assert H(b.replace(b'\r\n',b'\n'))==x['LF_sha256']
for p in d['closed_parent_reuse_pins']['parents']:assert H(Path(p['path']).read_bytes())==p['RAW_sha256']
probes=d['complete_probe_results']['results'];assert len(probes)==18
for n in ['proposed-private-adapter0','proposed-private-adapter1']:
 q=next(x for x in probes if x['probe']==n);assert q['actual_exit_code']==1 and q['valid_deliberate_BODY_reached'] and not q['free_variable_error'];assert len(q['errors'])==1
assert d['root_mode_observations']['observations'][0]['Elab_async_false_in_prelude']==False
assert d['root_mode_observations']['observations'][1]['Elab_async_false_in_prelude']==True
res=dict(schema='diagnosis66-foreground-readback-result-v1',actual_foreground_pid=os.getpid(),logical_run_hash_recomputed=True,logical_run_sha256=expected,COMPLETE_RAW_REVIEW_sha256=H((O/'review-run.json').read_bytes()),COMPLETE_RAW_DECISION_sha256=H((O/'complete-RAW-decisions.json').read_bytes()),SEPARATE_RAW_INPUT_sha256=H((O/'RAW-input-payload.json').read_bytes()),full_seven_slots_both_decisions=True,private_adapter_terminal_results_checked=True,all_pre_finalizer_owned_files_verified=True,closed_parent_pins_unchanged=True,source_math_repair=False,kernel_proof_credit=False)
(O/'foreground.readback.result.json').write_bytes((json.dumps(res,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(res,sort_keys=True),flush=True)
'''
scripts['foreground-close-validator.py']=r'''from pathlib import Path
import json,hashlib,os
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest();d=json.loads((O/'review-run.json').read_bytes());v=d.pop('run_sha256');assert H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())==v
for n in ['foreground.finalizer.receipt.json','foreground.readback.receipt.json']:
 q=json.loads((O/n).read_bytes());assert q['actual_exit_code']==0 and q['terminal_closed']
for x in d['pre_finalizer_all_owned_file_bindings']:assert H((O/x['name']).read_bytes())==x['RAW_sha256']
assert not (O/'lease.final.json').exists();assert not (O/'owned-manifest.json').exists();print(json.dumps(dict(schema='diagnosis66-foreground-close-validator-v1',actual_foreground_pid=os.getpid(),all_assertions_passed=True,logical_run_sha256=v,no_existing_closed_lease=True),sort_keys=True),flush=True)
'''
scripts['run-finalizer-readback.py']=r'''from pathlib import Path
import json,subprocess,hashlib,datetime,os,sys
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest()
for label,script in [('finalizer','foreground-finalizer.py'),('readback','foreground-readback.py')]:
 started=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen([sys.executable,str(O/script)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=str(O));out,err=p.communicate();(O/('foreground.'+label+'.stdout.log')).write_bytes(out);(O/('foreground.'+label+'.stderr.log')).write_bytes(err);d=dict(schema='diagnosis66-actually-observed-foreground-terminal-v1',label=label,actual_foreground_pid=p.pid,actual_exit_code=p.returncode,terminal_closed=True,observer_pid=os.getpid(),started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout_RAW_sha256=H(out),stderr_RAW_sha256=H(err));(O/('foreground.'+label+'.receipt.json')).write_bytes((json.dumps(d,sort_keys=True,indent=2)+'\n').encode());print(json.dumps(d,sort_keys=True),flush=True);print(out.decode(),flush=True)
 if p.returncode:print(err.decode(),flush=True);sys.exit(p.returncode)
'''
scripts['close-last.py']=r'''from pathlib import Path
import json,subprocess,hashlib,datetime,os,sys
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(name=str(p.relative_to(O)).replace('\\','/'),RAW_bytes=len(b),RAW_sha256=H(b),LF_bytes=len(lf),LF_sha256=H(lf))
def read(n):return json.loads((O/n).read_bytes())
def put(n,d):(O/n).write_bytes((json.dumps(d,sort_keys=True,indent=2)+'\n').encode())
p=subprocess.Popen([sys.executable,str(O/'foreground-close-validator.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=str(O));out,err=p.communicate();(O/'foreground.close-validator.stdout.log').write_bytes(out);(O/'foreground.close-validator.stderr.log').write_bytes(err);receipt=dict(schema='diagnosis66-actually-observed-foreground-terminal-v1',label='close-validator',actual_foreground_pid=p.pid,actual_exit_code=p.returncode,terminal_closed=True,observer_lease_writer_pid=os.getpid(),stdout_RAW_sha256=H(out),stderr_RAW_sha256=H(err));put('foreground.close-validator.receipt.json',receipt);assert p.returncode==0,err.decode()
files=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()];manifest=dict(schema='diagnosis66-exhaustive-owned-RAW-LF-manifest-v1',owned_path=str(O).replace('\\','/'),file_entries=files,total_final_owned_files=len(files)+2,coverage='All owned regular files including scripts, originals, negatives, private/public diagnostic candidates, source slices, root mode logs, COMPLETE RAW INPUT/DECISION/REVIEW and actual finalizer/readback/close terminal receipts. Self and lease use explicit external readback boundary below.',self_and_last_lease_binding=dict(manifest='owned-manifest.json RAW hash pinned in lease.final.json',last_lease='lease.final.json RAW hash observed by external postclose read-only terminal and returned capsule',no_impossible_recursive_self_hash=True));put('owned-manifest.json',manifest)
lease=dict(schema='diagnosis66-CLOSED_LAST-owned-lease-v1',status='CLOSED_LAST',owned_path=str(O).replace('\\','/'),owner='/root/independent_source64',last_owned_write=True,postclose_writes_permitted=False,closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),whole_logical_run_sha256=read('review-run.json')['run_sha256'],COMPLETE_RAW_REVIEW=pin(O/'review-run.json'),COMPLETE_RAW_DECISION=pin(O/'complete-RAW-decisions.json'),SEPARATE_RAW_INPUT=pin(O/'RAW-input-payload.json'),owned_manifest=pin(O/'owned-manifest.json'),owned_file_count=len(files)+2,actual_finalizer_pid=read('foreground.finalizer.receipt.json')['actual_foreground_pid'],actual_finalizer_exit=read('foreground.finalizer.receipt.json')['actual_exit_code'],actual_readback_pid=read('foreground.readback.receipt.json')['actual_foreground_pid'],actual_readback_exit=read('foreground.readback.receipt.json')['actual_exit_code'],actual_close_validator_pid=p.pid,actual_close_validator_exit=p.returncode,actual_lease_writer_pid=os.getpid(),lease_writer_exit_requires_external_foreground_observation=True);put('lease.final.json',lease)
print(json.dumps(dict(lease=lease,lease_RAW_sha256=H((O/'lease.final.json').read_bytes()),actual_lease_writer_pid=os.getpid()),sort_keys=True),flush=True)
'''
for name,s in scripts.items():(O/name).write_bytes(s.encode('ascii'))
print('Prepared '+str(len(scripts))+' bounded closure scripts')