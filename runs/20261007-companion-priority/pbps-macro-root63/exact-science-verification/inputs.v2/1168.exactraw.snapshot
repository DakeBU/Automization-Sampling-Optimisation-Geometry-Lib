import hashlib,json,os,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def put(name,d):(OUT/name).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
reader=subprocess.run([sys.executable,'-X','utf8',str(OUT/'read_finalizer63.py')],capture_output=True)
assert reader.returncode==0 and not reader.stderr,reader.stderr
(OUT/'reader.stdout.txt').write_bytes(reader.stdout)
readback=json.loads(reader.stdout.decode('utf-8'));readback['actual_reader_exit_code']=reader.returncode
put('terminal.readback.json',readback)
# No output-manifest self reference. The candidate lease binds it at the next layer.
excluded=['output.manifest.json','proposed-lease.closed.json','lease.json']
manifest={'status':'COMPLETE_OWNED_OUTPUT_MANIFEST','self_layer_exclusions':excluded,'owned_outputs':{str(p.relative_to(OUT)).replace('\\','/'):sha(p.read_bytes()) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in excluded}}
put('output.manifest.json',manifest)
closed={'status':'CLOSED_LAST','reviewer':'/root/independent_source63','prepared_utc':datetime.now(timezone.utc).isoformat(),'actual_preparer_pid':os.getpid(),'whole_run_sha256':readback['whole_run_sha256'],'named_complete_payload_RAW_sha256':readback['named_complete_payload_RAW_sha256'],'actual_foreground_finalizer_and_read_only_reader':readback,'output_manifest_RAW_sha256':sha((OUT/'output.manifest.json').read_bytes()),'complete_owned_outputs':{str(p.relative_to(OUT)).replace('\\','/'):sha(p.read_bytes()) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name not in ['lease.json','proposed-lease.closed.json']},'self_hash_exclusions':['lease.json','proposed-lease.closed.json'],'self_binding':'lease.json must equal proposed-lease.closed.json byte for byte; complete output manifest and all other owned files are pinned. Only lease.json is written at commit closure.','compiler_started':False,'canonical_VERIFIED':False,'full_paper_complete':False,'rendered_Exposition_Seal_granted':False,'final_write_rule':'After actual foreground read-only candidate CLOSED binding check passes, commit_closure63.py writes ONLY lease.json. No owned writes follow.'}
put('proposed-lease.closed.json',closed)
print(json.dumps({'status':'CLOSED_CANDIDATE_PREPARED','actual_read_only_reader_exit_code':reader.returncode,'whole_run_sha256':closed['whole_run_sha256'],'payload_RAW_sha256':closed['named_complete_payload_RAW_sha256'],'complete_owned_output_count':len(closed['complete_owned_outputs'])+2},indent=2))
