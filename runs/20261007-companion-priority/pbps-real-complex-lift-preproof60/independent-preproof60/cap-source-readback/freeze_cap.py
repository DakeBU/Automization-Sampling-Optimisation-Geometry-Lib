import datetime,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path('E:/Samplinglib'); OUT=pathlib.Path(__file__).resolve().parent
OUT.mkdir(exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes(); l=b.replace(b'\r\n',b'\n')
    return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def write(n,x): (OUT/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def canonical(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
supp=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59/independent-source-topology59/primary.supplemental-context.json'
doc=json.loads(supp.read_bytes()); region=next(x for x in doc['exact_regions'] if x['id']=='A2.Thmtheorem1.p1')
primary=ROOT/doc['primary']['path']; raw=primary.read_bytes(); assert sha(raw)==doc['primary']['raw_sha256']
fragment=raw[region['start_utf8_byte']:region['end_utf8_byte_exclusive']]
assert len(fragment)==region['slice_bytes'] and sha(fragment)==region['slice_sha256']
assert 'Assume' in region['text'] and '\\beta\\eta\\leq 1' in region['text']
p=OUT/'primary-cap.raw.html'; p.write_bytes(fragment)
main=OUT.parent/'run.json'; mainraw=main.read_bytes(); mainobj=json.loads(mainraw); digest=mainobj.pop('run_sha256'); assert sha(canonical(mainobj))==digest
assert digest=='acdb686187465251ef1588205cf2c3b413bb2db0b02871a3076012739aa644af'
write('cap.source.supplement.json',dict(kind='source-coverage-index-supplement-no-header-repair',primary=pin(primary),source_region=region,raw_snapshot=pin(p),supplemental_context=pin(supp),immutable_main_run=pin(main),main_native_run_sha256=digest,coverage_item=dict(id='A2.Thmtheorem1.p1:1',classification='NODE',target='standing-step-size-cap',description='Literal Assume beta eta<=1 is the existing actual consumer hβη binder; not a caller positivity/CFC premise. Alpha eta=1 remains legal.'),excluded_overlap='rho/gamma definitions and gamma lower-bound note in this same paragraph remain excluded centered-root results; already indexed by main run B12/B15/B16 exclusions.',graph_delta=dict(node='standing-step-size-cap',edge=dict(parent='standing-step-size-cap',child='actual-lift',kind='original printed source binder, reused actual59 internally')),combined_coverage='Main22 regions43 items + this separate cap paragraph1 binder item; no replacement of the immutable main extraction/decision.'))
reader='''import hashlib,json,pathlib,sys
r=pathlib.Path('E:/Samplinglib'); p=pathlib.Path(sys.argv[1]); x=json.loads(p.read_bytes())
for k in ['primary','raw_snapshot','supplemental_context','immutable_main_run']:
 q=x[k]; b=(r/q['path']).read_bytes(); l=b.replace(b'\\r\\n',b'\\n'); assert len(b)==q['bytes'] and hashlib.sha256(b).hexdigest()==q['raw_sha256']; assert hashlib.sha256(l).hexdigest()==q['lf_sha256']
b=(r/x['primary']['path']).read_bytes(); z=x['source_region']; assert b[z['start_utf8_byte']:z['end_utf8_byte_exclusive']]==(r/x['raw_snapshot']['path']).read_bytes()
print(json.dumps({'qualified_pins':4,'primary_cap_literal':True,'main_closed_artifacts_unchanged':True,'scope':'source index supplement only; exact headers accepted unchanged'}))
'''
(OUT/'readback.py').write_bytes(reader.encode())
with (OUT/'readback.stdout.log').open('wb') as out,(OUT/'readback.stderr.log').open('wb') as err:
    proc=subprocess.Popen([sys.executable,str(OUT/'readback.py'),str(OUT/'cap.source.supplement.json')],cwd=ROOT,stdout=out,stderr=err); pid=proc.pid; code=proc.wait()
assert code==0
write('readback.receipt.json',dict(actual_foreground_pid=pid,exit_code=code,terminal_closed=True,stdout=pin(OUT/'readback.stdout.log'),stderr=pin(OUT/'readback.stderr.log'),no_compiler=True))
files=['freeze_cap.py','readback.py','primary-cap.raw.html','cap.source.supplement.json','readback.stdout.log','readback.stderr.log','readback.receipt.json']
payload=dict(kind='distinct-named-cap-coverage-payload',source=pin(OUT/'cap.source.supplement.json'),unchanged_main_native_run_sha256=digest)
write('named-cap.payload.json',payload)
run=dict(status='CLOSED_SOURCE_INDEX_SUPPLEMENT_NOT_PROOF',owner='/root/next_primary59',inputs=dict(primary=pin(primary),supplemental=pin(supp),main_run=pin(main)),outputs=[pin(OUT/f) for f in files],named_payload_sha256=pin(OUT/'named-cap.payload.json')['raw_sha256'],actual_foreground_finalizer_pid=os.getpid(),actual_foreground_readback_pid=pid,actual_foreground_readback_exit_code=code,hash_recipe='SHA256 canonical UTF8 JSON sort_keys=True ensure_ascii=False separators comma-colon over entire run excluding ONLY run_sha256',excluded_from_hash=['run_sha256'],header_or_math_repair=False)
run['run_sha256']=sha(canonical(run)); write('run.json',run)
runpin=pin(OUT/'run.json'); payloadpin=pin(OUT/'named-cap.payload.json')
print(json.dumps(dict(actual_foreground_pid=os.getpid(),readback_pid=pid,readback_exit_code=0,run_sha256=run['run_sha256'],named_payload_sha256=payloadpin['raw_sha256'])),flush=True)
# Last write after actual foreground child EXIT0; original CLOSED main artifacts untouched.
write('lease.json',dict(status='CLOSED',closed_last=True,owner='/root/next_primary59',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),run=runpin,native_run_sha256=run['run_sha256'],named_payload=payloadpin,actual_foreground_readback_pid=pid,actual_foreground_readback_exit_code=0))
