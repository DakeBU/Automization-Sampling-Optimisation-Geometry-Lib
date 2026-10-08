import pathlib,json,hashlib,os,subprocess
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-real-defect-root61';D=R/'independent-math61'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
manifest=load(D/'input.manifest.json');assert manifest['frozen_count']==27 and manifest['selected_API_count']==9
reads=0
for x in manifest['artifacts']:
 for key in ['original','raw_snapshot','LF_snapshot']:
  assert pin(x[key]['path'])==x[key];reads+=1
 assert x['original']['raw_sha256']==x['raw_snapshot']['raw_sha256'];assert x['original']['lf_sha256']==x['LF_snapshot']['raw_sha256']
for x in manifest['selected_API_inputs']:
 assert pin(x['original']['path'])==x['original'];assert pin(x['selected_LF_bytes']['path'])==x['selected_LF_bytes'];reads+=2
run=load(D/'run.json');pay=load(D/'payload.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
assert sha(canon(pay['named_mathematics_payload']))==pay['named_mathematics_payload_sha256']==run['named_mathematics_payload_sha256'];assert pay['named_mathematics_payload']==run['named_mathematics_payload']
for k in ['receipt','payload_file','inputs']:assert pin(run[k]['path'])==run[k]
outputs=load(D/'outputs.final.json');assert sha(canon({k:v for k,v in outputs.items() if k!='outputs_sha256'}))==outputs['outputs_sha256']
for x in outputs['artifacts']:assert pin(x['path'])==x
assert load(D/'compiler-wrapper.status.json')['exit_code']==0 and load(D/'review-finalizer.status.json')['exit_code']==0
assert load(D/'compiler.validation.json')['actual_compiler']['exit_code']==0 and load(D/'compiler.validation.json')['actual_compiler']['terminal_closed']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==run['checked_base_commit']
q=dict(status='PASS',actual_PID=os.getpid(),checked_base_commit=run['checked_base_commit'],frozen_originals=27,original_raw_LF_and_snapshot_readbacks=reads,selected_API_ranges=9,output_count=outputs['count'],outputs_sha256=outputs['outputs_sha256'],whole_run_sha256=run['run_sha256'],distinct_named_mathematics_payload_sha256=run['named_mathematics_payload_sha256'],compiler_exit0_CLOSED=True,current_source_decoder_not_read=True,canonical_Git_state_unchanged_by_reviewer=True)
(D/'readback.json').write_bytes((json.dumps(q,indent=2)+'\n').encode());print(json.dumps(q),flush=True)
