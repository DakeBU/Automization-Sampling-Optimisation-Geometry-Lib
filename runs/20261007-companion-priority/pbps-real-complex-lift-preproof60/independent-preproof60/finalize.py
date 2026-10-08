import datetime,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path('E:/Samplinglib'); OUT=pathlib.Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
    return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def write(n,x): (OUT/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
write('author.foreground.receipt.json',dict(actual_author_pid=9564,exit_code=0,terminal_tool_chunk='0755e1',actual_foreground=True,no_compiler=True,scope='source evidence extraction and statement review',retained_negative=dict(tool_chunk='e38897',exit_code=1,error='Path.write_text newline parameter unsupported by this Python; author_review.failed0.py retained, changed to explicit UTF8 write_bytes before success')))
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (OUT/'readback.stdout.log').open('wb') as out,(OUT/'readback.stderr.log').open('wb') as err:
    proc=subprocess.Popen([sys.executable,str(OUT/'readback.py')],cwd=ROOT,stdout=out,stderr=err)
    pid=proc.pid; result=proc.wait()
assert result==0, (result,(OUT/'readback.stderr.log').read_text())
write('readback.receipt.json',dict(command=[sys.executable,str(OUT/'readback.py')],actual_foreground_pid=pid,exit_code=result,terminal_closed=True,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=pin(OUT/'readback.stdout.log'),stderr=pin(OUT/'readback.stderr.log'),scope='Independent native exact-byte/qualified-pin readback; no compiler or theorem proof'))
files=['author_review.py','author_review.failed0.py','readback.py','finalize.py','primary.exact-regions.json','source.coverage.json','source.graph.json','statement.review.json','named-preproof-source.payload.json','execution.snapshot.json','input.manifest.json','author.foreground.receipt.json','readback.stdout.log','readback.stderr.log','readback.receipt.json']
run=dict(schema_version=1,owner='/root/next_primary59',status='SOURCE_PREPROOF_REVIEW_CLOSED_NOT_PROVED',source_version='2609.06905v1',exact_header0_sha256=pin(ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift-preproof60/header0.lean')['raw_sha256'],exact_header1_sha256=pin(ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift-preproof60/header1.lean')['raw_sha256'],inputs_manifest=pin(OUT/'input.manifest.json'),output_pins=[pin(OUT/f) for f in files],named_payload_sha256=pin(OUT/'named-preproof-source.payload.json')['raw_sha256'],actual_foreground_readback=dict(pid=pid,exit_code=result,receipt=pin(OUT/'readback.receipt.json')),actual_foreground_finalizer_pid=os.getpid(),hash_recipe='SHA256 UTF8 JSON ensure_ascii=False sort_keys=True separators comma-colon over the entire run object excluding ONLY run_sha256; named payload is distinct actual raw file SHA256',excluded_from_whole_run_hash=['run_sha256'],derived_closure='lease.json is the last write and derives exact native run raw and logical hashes; it is not a hash self-reference',no_compiler=True,no_proof_body=True,no_canonical_mutation=True,no_source_blind_decoder_credit=True,no_formal_completion_credit=True)
run['run_sha256']=sha(canonical(run)); write('run.json',run)
check=json.loads((OUT/'run.json').read_bytes()); expected=check.pop('run_sha256'); assert sha(canonical(check))==expected
reviewpin=pin(OUT/'statement.review.json'); runpin=pin(OUT/'run.json')
print(json.dumps(dict(finalizer_pid=os.getpid(),readback_pid=pid,readback_exit_code=0,run_sha256=run['run_sha256'],named_payload_sha256=run['named_payload_sha256'],review_sha256=reviewpin['raw_sha256'],whole_run_raw_sha256=runpin['raw_sha256']),ensure_ascii=True),flush=True)
# CLOSED is deliberately the final filesystem operation, after an actual child EXIT0 readback.
write('lease.json',dict(status='CLOSED',closed_last=True,owner='/root/next_primary59',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),native_run_sha256=run['run_sha256'],run=runpin,named_payload_sha256=run['named_payload_sha256'],review=reviewpin,actual_foreground_readback_pid=pid,actual_foreground_readback_exit_code=0,actual_foreground_finalizer_pid=os.getpid(),scope='Preproof statement, binder and bounded source topology review only. Root adoption and all proof/source/publication verification remain separate.'))
