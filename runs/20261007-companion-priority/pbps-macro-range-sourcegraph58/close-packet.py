from pathlib import Path
import subprocess, json, hashlib, datetime, time, os, sys, ctypes
OUT=Path(__file__).resolve().parent; start=time.time(); reads=[]; writes=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p,b):
    lf=b.replace(b'\r\n',b'\n'); return dict(path=str(p).replace('\\','/'),bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def read(p):
    b=p.read_bytes(); reads.append(pin(p,b)); return b
def write(n,d):
    p=OUT/n
    if isinstance(d,dict):
        d=dict(d); d['content_self_sha256']=sha(json.dumps(d,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()); b=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
    else: b=d
    p.write_bytes(b); receipt=pin(p,b); writes.append(receipt); return receipt
write('lease.open.json',dict(actor='/root/source_graph58',status='OPEN_FINAL_BOOKKEEPING_ONLY',python_pid=os.getpid(),started_utc=datetime.datetime.utcnow().isoformat()+'Z',foreground=True,compiler='NOT_STARTED_CLOSED'))
result=subprocess.run([sys.executable,str(OUT/'validate-packet.py')],capture_output=True,check=False)
write('validator.foreground.stdout.txt',result.stdout); write('validator.foreground.stderr.txt',result.stderr)
if result.returncode!=0:
    print(result.stderr.decode(errors='replace')); sys.exit(result.returncode)
validator=json.loads(read(OUT/'validator.json').decode()); sourcefirst=json.loads(read(OUT/'source-first-run.json').decode())
pins=[]
excluded=['output-manifest.json','run.json','complete.json','lease.json']
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name not in excluded: pins.append(pin(p,read(p)))
manifest=write('output-manifest.json',dict(actor='/root/source_graph58',status='EXACT_OUTPUT_RAW_LF_BYTE_MANIFEST',artifacts=pins,excluded_closure_artifacts=excluded,reason='Avoid circular file hashes; output manifest is pinned by run/complete, complete and run by final lease. All are native complete-self-digested.'))
resource=dict(wrapper_python_pid=os.getpid(),validator_python_pid=validator['resource']['pid'],foreground_validator_exit_code=result.returncode,validator_process_waited=True,wall_seconds=time.time()-start,cpu_user_seconds=os.times().user,cpu_system_seconds=os.times().system,read_operations=len(reads),read_bytes=sum(r['bytes'] for r in reads),write_operations=len(writes),write_bytes=sum(r['bytes'] for r in writes),validator_resource=validator['resource'])
run=write('run.json',dict(schema_version=1,actor='/root/source_graph58',status='SOURCE_FIRST_GRAPH_SIGNATURE_INDEX_COMPLETE_PENDING_INDEPENDENT_REVIEW',source_id='arXiv:2609.06905v1',own_nodes=25,own_edges=25,own_source_coverage=dict(total=365,NODE=205,EXCLUDED=160),inherited_source_coverage=dict(total=606,NODE=94,EXCLUDED=512),source58_original_670_adoption='Historical exact root source-only58 adoption retained; no rerun claim.',own_original_pin_count=dict(logged_dispositions=175,actual_successful_checks=172,strict_checks=165,full_row_temporal_maps=7,historical_live_skips=3),native_complete_self_digest_rule='Complete run object excluding only actual top-level content_self_sha256.',separate_named_payload='NONE_USED',outputs=manifest,source_first_run=pin(OUT/'source-first-run.json',read(OUT/'source-first-run.json')),validator=pin(OUT/'validator.json',read(OUT/'validator.json')),resource=resource,actual_foreground_commands=[dict(command='python build-sourcegraph.py',observed_tool_exit_code=0),dict(command='python finish-packet.py',observed_tool_exit_code=0),dict(command='python source-supplement.py',observed_tool_exit_code=0),dict(command='python index-signatures.py',observed_tool_exit_code=0),dict(command='python index-consumer.py',observed_tool_exit_code=0),dict(command=[sys.executable,str(OUT/'validate-packet.py')],actual_child_exit_code=result.returncode)],read_manifest=reads,write_manifest=writes,compiler='NOT_STARTED_CLOSED',root_proposition_elaboration='Root reported main/generic and Test proposition-only typecheck EXIT0 with compiler leases CLOSED; source extractor ran no Lean/compiler and does not re-certify those logs.',candidate58_implementation_read=False,public_main_scope='Actual canonical pullback range equality, mean transport and exact centered image equality.',test_only_scope='Actual57 scalar contraction transported via same actual55 operators to all centered macro f and squared defect gap; no public macro gap claim.',creator_validates_own_graph=False,independent_source_topology_review='PENDING_DISTINCT_REVIEWER',formal_admission=False,mathematical_truth_boundary='No source weakH1/Gamma-root/positivity/inverse/halfturn/main/cost/composition/four-paper completion.',no_shared_files_or_Git_or_background_ASTIS_or_Goal_mutation=True,finished_utc=datetime.datetime.utcnow().isoformat()+'Z'))
complete=write('complete.json',dict(actor='/root/source_graph58',status='SOURCE_PACKET_CLOSED_PENDING_INDEPENDENT_REVIEW',run=run,output_manifest=manifest,validator=pin(OUT/'validator.json',read(OUT/'validator.json')),validation_child_exit_code=result.returncode,compiler='NOT_STARTED_CLOSED',topology_review='PENDING',self_validation_prohibited=True))
# Final filesystem action is CLOSED lease. No file read/write follows this action.
write('lease.json',dict(actor='/root/source_graph58',status='CLOSED',compiler='NOT_STARTED_CLOSED',python='CLOSED_LAST_FOREGROUND',wrapper_python_pid=os.getpid(),validator_python_pid=validator['resource']['pid'],validator_actual_exit_code=result.returncode,validator_waited_and_completed=True,run=run,complete=complete,outputs=manifest,resource=resource,closed_utc=datetime.datetime.utcnow().isoformat()+'Z',last_filesystem_operation=True,independent_source_review_pending=True,creator_validation=False))
print(json.dumps(dict(status='CLOSED_LAST',actual_validator_exit=result.returncode,run=str(OUT/'run.json'),complete=str(OUT/'complete.json'),compiler='NOT_STARTED_CLOSED')))
