import os,sys,pathlib,json,hashlib,datetime
sys.dont_write_bytecode=True
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean55';O=B/'repository-seal55'
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
def path(p):p=pathlib.Path(str(p).replace('\\','/'));return p if p.is_absolute() else R/p
def pin(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def load(p):return json.loads(path(p).read_text(encoding='utf-8'))
def dump(p,d):(O/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def equal(e):a=pin(e['path']);return a['raw_sha256']==e['raw_sha256'] and a['lf_sha256']==e['lf_sha256'] and a['bytes']==e['bytes']
assert not (O/'lease.json').exists()
dump('lease.json',dict(status='OPEN',actor='whole_math52',stage='independent scoped repository seal55 preparation',opened_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_python_PID=os.getpid(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED_CLOSED',compiler_started=False,scope='Only repository-seal55 outputs; no shared/proof/VERIFIED mutation or compiler; awaiting actual integration HEAD, twelve terminal gates and captures.'))
outputs=[];selfs=[];leases=[]
for folder,key in [('whole-math55','actual_output_pins'),('exact-verification55','actual_output_pins')]:
 m=load(B/folder/'outputs.json');assert len(m[key])==m['count'] and logical(m[key])==m['output_list_logical_sha256']
 for e in m[key]:assert equal(e),e['path'];outputs.append(e)
 r=load(B/folder/'run.json');assert logical({k:v for k,v in r.items() if k!='run_sha256'})==r['run_sha256'];assert logical(r['run_binding_payload'])==r['review_run_binding_sha256'];selfs.append(dict(run=pin(B/folder/'run.json'),full_run_minus_self_sha256=r['run_sha256'],separate_payload_sha256=r['review_run_binding_sha256']))
 l=load(B/folder/'lease.json');assert l['status']=='CLOSED' and l['exit_code']==0
 for k in ['receipt','run','actual_compiler_CLOSED_lease','actual_outputs_manifest','readback']:assert equal(l[k])
 leases.append(dict(lease=pin(B/folder/'lease.json'),native_fields=l))
science='4f71a36d56500fda7f86e8080f695a514913950a';assert load(B/'verified.json')['checked_commit']==science
for p in ['AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean','Tests/ProximalBPSL2MacroscopicMean.lean']:
 expected=next(e for e in load(B/'exact-verification55/committed-inputs.json')['bindings'] if e['path']==p)['current'];assert equal(expected)
dump('preparation.json',dict(status='READY_AWAITING_INTEGRATION_EVIDENCE_NOT_ACCEPTED',scientific_commit=science,native_checked_commit_alias='Exact receipt checked_commit is the scientific commit; integration commit will be separately bound.',strict_closed_output_checks=len(outputs),actual_closed_outputs=outputs,complete_native_run_recipes=selfs,actual_closed_original_leases=leases,source0_preserved='BLOCKED_METADATA_LOCATOR_ONLY',source1_accepted='ACCEPTED_SCOPED_SOURCE_FIDELITY_AFTER_METADATA_REPAIR',compiler_started=False,VERIFIED_transition=False,required_next_inputs=['Exact integration commit and actual Git delta/current LF','Twelve actual terminal PASS statuses/logs and actual root integration CLOSED lease','Four captures/DOM/inspection and actual capture lease CLOSED','Integration publication/graph/Registry496/import consumers and explicit remaining boundary','Precise immutable whitespace negative and exact diagnostic path exclusions'],remaining_boundary=['Actual all-L2 mean/typed differences/noncentered rank0 only','No rough-gradient/H1/B13/Gamma/main/cost/composition/live/PURIFIED credit']))
print(json.dumps(dict(status='READY_AWAITING_INTEGRATION_HEAD',scientific_commit=science,strict_original_closed_output_checks=len(outputs),original_closed_runs=2,compiler_started=False,repository_seal_acceptance=False)))
