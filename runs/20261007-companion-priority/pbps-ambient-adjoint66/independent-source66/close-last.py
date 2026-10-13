from pathlib import Path
import json,hashlib,os,subprocess,sys,datetime
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
def read(n):return json.loads((O/n).read_bytes())
def put(n,d):(O/n).write_bytes((json.dumps(d,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode())
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(name=p.name,RAW_bytes=len(b),RAW_sha256=H(b),LF_bytes=len(lf),LF_sha256=H(lf))
assert not (O/'lease.final.json').exists()
p=subprocess.Popen([sys.executable,str(O/'close-validate.py')],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1'));out,err=p.communicate()
(O/'foreground-close-validator.stdout.log').write_bytes(out);(O/'foreground-close-validator.stderr.log').write_bytes(err)
receipt=dict(schema='source66-actual-foreground-terminal-receipt-v1',label='close-validator',actual_foreground_pid=p.pid,actual_exit=p.returncode,actual_wrapper_pid=os.getpid(),detached=False,observed_by_communicate=True,stdout=pin(O/'foreground-close-validator.stdout.log'),stderr=pin(O/'foreground-close-validator.stderr.log'));put('foreground-close-validator.receipt.json',receipt)
sys.stdout.buffer.write(out);sys.stderr.buffer.write(err)
if p.returncode:sys.exit(p.returncode)
run=read('review-run.json');pins=read('review-payload-pins.json');final=read('foreground-finalize.receipt.json');back=read('foreground-readback.receipt.json')
entries=[pin(f) for f in sorted(O.iterdir()) if f.is_file() and f.name not in ['owned-manifest.json','lease.final.json']]
manifest=dict(schema='source66-exhaustive-owned-RAW-LF-manifest-v1',owner='/root/independent_source64',owned_path=str(O).replace('\\','/'),regular_file_entries=entries,bound_regular_files=len(entries),total_owned_files_including_self_and_final_lease=len(entries)+2,complete_regular_file_manifest=True,self_boundary=dict(manifest='owned-manifest.json exact RAW bytes pinned by lease.final.json',lease='lease.final.json exact RAW bytes pinned by final external read-only postclose output/capsule; no circular self-hash claim'),all_negative_observer_artifacts_included=True,all_scripts_inputs_outputs_terminals_included=True,postclose_writes_permitted=False)
put('owned-manifest.json',manifest)
lease=dict(schema='source66-CLOSED_LAST-owned-lease-v1',status='CLOSED_LAST',owner='/root/independent_source64',owned_path=str(O).replace('\\','/'),closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),last_owned_write=True,postclose_writes_permitted=False,owned_file_count=len(entries)+2,manifest_RAW_sha256=H((O/'owned-manifest.json').read_bytes()),whole_logical_run_sha256=run['run_sha256'],COMPLETE_RAW_REVIEW=pins['COMPLETE_RAW_REVIEW'],COMPLETE_RAW_DECISION=pins['COMPLETE_RAW_DECISION'],SEPARATE_COMPLETE_RAW_INPUT=pins['SEPARATE_COMPLETE_RAW_INPUT'],native_semantic_decision=pins['native_semantic_decision'],actual_finalizer_pid=final['actual_foreground_pid'],actual_finalizer_exit=final['actual_exit'],actual_readback_pid=back['actual_foreground_pid'],actual_readback_exit=back['actual_exit'],actual_close_validator_pid=p.pid,actual_close_validator_exit=p.returncode,actual_lease_writer_pid=os.getpid(),lease_writer_exit_observation='External foreground tool observes actual EXIT after this last write; see final closure capsule',postclose_observation='Read-only external postclose-readonly.py output/capsule; no receipt may be written inside the closed folder',reviewer_packet_sha256=read('decision.json')['reviewer_packet_sha256'],publication_binding_sha256=read('decision.json')['publication_binding_sha256'],publication_context_sha256=read('decision.json')['publication_context_sha256'],source_mathematical_repair=False,full_Exposition=False,PURIFIED=False)
put('lease.final.json',lease)
# No owned write, including receipts or log capture, is allowed below this line.
print(json.dumps(dict(schema='source66-external-lease-writer-completion-v1',actual_lease_writer_pid=os.getpid(),actual_close_validator_pid=p.pid,actual_close_validator_exit=p.returncode,owned_file_count=len(entries)+2,lease=pin(O/'lease.final.json'),manifest=pin(O/'owned-manifest.json'),whole_logical_run_sha256=run['run_sha256'],status='CLOSED_LAST'),sort_keys=True))
