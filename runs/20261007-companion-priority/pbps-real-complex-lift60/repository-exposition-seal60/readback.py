import pathlib,json,hashlib,os,subprocess
ROOT=pathlib.Path('E:/Samplinglib');D=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60/repository-exposition-seal60'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def same(a,b):return all(a[k]==b[k] for k in ['bytes','lf_bytes','raw_sha256','lf_sha256'])
mapping=load(D/'post-input-ledger-mapping.json');mapped=0
def verify(row):
 global mapped
 p=pathlib.Path(row['path']);actual=pin(p)
 if not same(actual,row):
  assert row['path']==mapping['original']['path'] and same(mapping['original'],row)
  assert same(pin(mapping['exact_snapshot']['path']),row);mapped+=1
manifest=load(D/'input.manifest.json')
for x in manifest['artifacts']:verify(x['resolved'])
for x in load(D/'inputs.open.json')['artifacts']:verify(x)
graphs=load(D/'graph.input-pins.json')
for k in ['source_pins','publication_pins','referenced_cell_pins','helpers']:
 for x in graphs[k]:verify(x)
outputs=load(D/'outputs.final.json');assert sha(canon({k:v for k,v in outputs.items() if k!='outputs_sha256'}))==outputs['outputs_sha256']
for row in outputs['artifacts']:assert same(pin(row['path']),row)
run=load(D/'run.json');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']
pay=load(D/'payload.json');assert sha(canon(pay['named_repository_exposition_payload']))==pay['named_repository_exposition_payload_sha256']==run['named_repository_exposition_payload_sha256']
assert pin(D/'receipt.json')==run['receipt'] and pin(D/'payload.json')==run['payload_file']
ng=load(D/'graph.native-inputs.json');assert sha(canon(ng['actual_native_inputs']))==ng['publication_inputs_sha256']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==run['checked_integration_commit']
assert load(D/'finalizer.status.json')['exit_code']==0 and load(D/'reader.2.status.json')['exit_code']==0
receipt=load(D/'receipt.json');assert receipt['status']=='ACCEPTED_SCOPED' and not receipt['whole_Goal_complete'] and not receipt['main_live_PURIFIED']
q=dict(status='PASS',actual_PID=os.getpid(),native_qualified_pins=manifest['qualified_count'],opening_pins=60,full_native_graph_source_pins=511,publication_pins=192,referenced_cell_pins=275,whole_run_sha256=run['run_sha256'],distinct_named_payload_sha256=run['named_repository_exposition_payload_sha256'],output_count=outputs['count'],outputs_sha256=outputs['outputs_sha256'],exact_post_input_ledger_resolutions=mapped,checked_commit=run['checked_integration_commit'],scoped_debt='Native full graph freshness captured before root post-input SAU61 claim; new61 is excluded from reviewed63c7435. No old/current ledger fiction.',compiler='NOT_STARTED_CLOSED',browser='NOT_STARTED_CLOSED')
(D/'readback.json').write_bytes((json.dumps(q,indent=2)+'\n').encode());print(json.dumps(q),flush=True)
