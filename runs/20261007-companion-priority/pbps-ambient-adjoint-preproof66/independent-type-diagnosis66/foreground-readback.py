from pathlib import Path
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
