from pathlib import Path
import datetime, hashlib, json, subprocess, time

ROOT=Path.cwd();BASE=ROOT/'.astis/semantic-neutral-20261111/r4_src_6aef/normal-verification'
E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/radial-fourth-matrix-semantic-evidence'
OUT=E/'normal-verification/r4_src_6aef'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode()
def binding(p):
    b=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha(b)}
def head():return subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,check=True,capture_output=True,text=True).stdout.strip()
assert not (OUT/'recovery-check-only.receipt.json').exists()
(OUT/'execution-sources').mkdir(exist_ok=True)
for src,dst in [('preflight.py','preflight.original.py'),('transition_once.py','transition_once.original.py'),('execute_verified_transaction.py','execute_verified_transaction.original.py'),('recovery_check_only.py','recovery_check_only.py'),('run_recovery_capture.py','run_recovery_capture.py')]:
    (OUT/'execution-sources'/dst).write_bytes((BASE/src).read_bytes())

# This is the exact actual exec_command return, retained after it returned. The original
# wrapper had no self-emitted outer receipt; its child API and frontier receipts already existed.
combined='Traceback (most recent call last):\n  File "/Users/zhouhuanjian/ASTIS-GC/.astis/semantic-neutral-20261111/r4_src_6aef/normal-verification/execute_verified_transaction.py", line 148, in <module>\n    assert tracked_changed==[str(C.relative_to(ROOT))]\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError\n'
toolresult={'chunk_id':'bdcde1','wall_time_seconds':9.482766041,'exit_code':1,'original_token_count':80,'output':combined}
(OUT/'original-wrapper.combined-tool-output.txt').write_text(combined)
(OUT/'original-wrapper.actual-tool-receipt.json').write_bytes(enc({'kind':'exact actual exec_command result captured after return',
 'actual_tool_result':toolresult,'command':'/opt/anaconda3/bin/python -B .astis/semantic-neutral-20261111/r4_src_6aef/normal-verification/execute_verified_transaction.py',
 'cwd':str(ROOT),'capture_note':'The outer wrapper did not self-emit a receipt before its reporting assertion. This preserves the actual tool exit1 and exact combined tool output; no separate original stdout/stderr or start timestamp is invented. Original inner API and whole-frontier receipts/streams are preserved separately.',
 'original_wrapper_script':binding(OUT/'execution-sources/execute_verified_transaction.original.py')}))

gate_dir=OUT/'assessed-final-gates';gate_dir.mkdir(exist_ok=True)
for p in sorted((ROOT/'.astis/huanjian-resume-20261103').glob('20261111T173737*-radial-fourth-matrix-final-reviewed-*.receipt.json')):
    d=json.loads(p.read_bytes());log=Path(d['log']);assert sha(log.read_bytes())==d['log_sha256']
    (gate_dir/p.name).write_bytes(p.read_bytes());(gate_dir/log.name).write_bytes(log.read_bytes())
command=['/opt/anaconda3/bin/python','-B',str((BASE/'recovery_check_only.py').relative_to(ROOT))]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();h=head();t=time.monotonic()
run=subprocess.run(command,cwd=ROOT,capture_output=True)
(OUT/'recovery-check-only.stdout').write_bytes(run.stdout);(OUT/'recovery-check-only.stderr').write_bytes(run.stderr)
receipt={'argv':command,'cwd':str(ROOT),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':run.returncode,
 'HEAD_before':h,'HEAD_after':head(),'stdout_sha256':sha(run.stdout),'stderr_sha256':sha(run.stderr),
 'transition_API_calls':0,'canonical_state_writes':0,'scope':'Separate actual recovery/check-only execution; writes only bounded evidence reports.'}
(OUT/'recovery-check-only.receipt.json').write_bytes(enc(receipt))
if run.returncode!=0:
    print(run.stdout.decode());print(run.stderr.decode());raise SystemExit(run.returncode)
assert receipt['HEAD_before']==receipt['HEAD_after']=='3ba24f46ea74e4537e57824982dfee9f51aeac27'
entries=[]
for p in [E/'actual-VERIFIED-independent-decision.json',*sorted(OUT.rglob('*'))]:
    if p.is_file() and p.name!='portable-custody-manifest.json':
        row=binding(p);row.update({'destination':row['path'],'classification':'bounded-original-independent-normal-verification-evidence'});entries.append(row)
manifest={'schema_version':1,'advance_id':'ASTIS-SA-20261111-GaussianComplexityRadialFourthMatrix',
 'actor':'/root/radial_fourth_fresh_source_6aef','outcome':'VERIFIED',
 'metadata_HEAD':'3ba24f46ea74e4537e57824982dfee9f51aeac27','native_mathematical_candidate':'69a3336dde302c4a34dbd88708ff6226b2bd0e87',
 'normal_transition_API_calls':1,'recovery_transition_API_calls':0,'original_reporting_wrapper_actual_exit_code':1,'actual_recovery_check_only_exit_code':0,
 'entries':entries,'total_payload_bytes':sum(e['bytes'] for e in entries),
 'excluded':'Full303 foreign advance states,43 discovery states,complete original ledgers,tracked-tree/frontier snapshots and other full foreign/control state remain local-only. No full native environment/type/body dump or build artifact is exported. Existing independent native/source custody sets are referenced by exact hashes, not recopied.',
 'no_further_canonical_state_mutation_by_this_reviewer':True}
(OUT/'portable-custody-manifest.json').write_bytes(enc(manifest))
print(run.stdout.decode())
print(json.dumps({'decision_sha256':sha((E/'actual-VERIFIED-independent-decision.json').read_bytes()),
 'VERIFIED_evidence_sha256':sha((OUT/'VERIFIED-evidence.full.json').read_bytes()),
 'actual_append_sha256':sha((OUT/'actual-VERIFIED-append.exact.jsonl').read_bytes()),
 'actual_transaction_receipt_sha256':sha((OUT/'actual-VERIFIED-transaction.receipt.json').read_bytes()),
 'original_wrapper_actual_tool_receipt_sha256':sha((OUT/'original-wrapper.actual-tool-receipt.json').read_bytes()),
 'recovery_receipt_sha256':sha((OUT/'recovery-check-only.receipt.json').read_bytes()),
 'whole_frontier_receipt_sha256':sha((OUT/'post-VERIFIED-whole-frontier.receipt.json').read_bytes()),
 'preservation_report_sha256':sha((OUT/'hash-only-preservation-report.json').read_bytes()),
 'actual_outcome_sha256':sha((OUT/'actual-outcome.json').read_bytes()),
 'portable_manifest_sha256':sha((OUT/'portable-custody-manifest.json').read_bytes()),
 'portable_manifest_entries':len(entries),'portable_payload_bytes':manifest['total_payload_bytes'],
 'further_canonical_state_mutations':0},indent=2))
