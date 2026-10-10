from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def put(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode());assert json.loads(p.read_bytes())==v
assert not (O/'lease.json').exists()
env=dict(os.environ);env['PYTHONUTF8']='1'
p=subprocess.run([sys.executable,str(O/'verify_readbacks.py')],cwd=R,env=env,capture_output=True,encoding='utf8')
assert p.returncode==0,(p.stdout,p.stderr)
put('foreground-readbacks.json',{'actual_command':'python '+(O/'verify_readbacks.py').relative_to(R).as_posix(),
 'actual_exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'stdout_sha256':sha(p.stdout.encode()),
 'result':json.loads(p.stdout),'completed_at':now(),'compiler':'NOT_STARTED'})
topology={'payload_name':'independent-source59-topology-extraction-pending-distinct-review',
 'files':[pin(O/n) for n in ['primary.source-first.json','primary.supplemental-context.json',
 'source-graph.pre-candidate.json','source-proof-graph.json','source-coverage.manifest.json','indexed-input.manifest.json']],
 'candidate_header0':pin(O.parent/'header0.lean'),'candidate_header1':pin(O.parent/'header1.lean'),
 'self_approval':False}
source={'payload_name':'independent-source59-preproof-statement-fidelity',
 'files':[pin(O/n) for n in ['source-statement.preproof-review.json','review.payload.manifest.json']],
 'candidate':pin(O.parent/'statement-candidate.json'),'topology_accepted_by_self':False}
put('named-topology.payload.json',topology);put('named-source.payload.json',source)
run={'schema_version':1,'actor':'/root/next_primary59','status':'CLOSED_PREPROOF_SOURCE_REVIEW_TOPOLOGY_EXTRACTION_ONLY',
 'completed_at':now(),'named_topology_payload':topology,'named_topology_payload_sha256':sha(canon(topology)),
 'named_source_payload':source,'named_source_payload_sha256':sha(canon(source)),
 'all_output_files_before_run':[pin(p) for p in sorted(O.rglob('*')) if p.is_file()],
 'checks':{'author_foreground_exit_code':0,'readback_foreground_exit_code':p.returncode,
 'primary_regions':31,'indexed_snapshots':10,'graph_nodes':19,'graph_edges':23,'coverage_items':54,
 'NODE':25,'EXCLUDED':29},
 'source_statement_verdict':'ACCEPTED_PREPROOF_WITH_DISCLOSED_ELABORATION_NO_EXCESS',
 'source_topology_verdict':'NOT_SELF_APPROVED_PENDING_DISTINCT_WHOLE_MATH52_RAW_SOURCE_REVIEW',
 'proof_source_publication_verdict':'NOT_PERFORMED',
 'compiler':'NOT_STARTED_CLOSED','candidate59_implementation_read':False,
 'old_source_only59_immutable':True,'root_only_stabilization_unchanged':True,
 'native_run_hash_rule':'SHA256 canonical UTF8 JSON of entire run excluding ONLY run_sha256; separate named topology/source payload hashes do not substitute for run hash.',
 'final_lease_write':'CLOSEDLAST only after actual foreground readbacks EXIT0 and native run readback/hash assertion; no file edits after lease closure.',
 'memory_trace':'Historical quick pass from prior audit only; source/candidate live exact snapshots govern this review.'}
run['run_sha256']=sha(canon(run));put('reviewer.primary.run.json',run)
v=json.loads((O/'reviewer.primary.run.json').read_bytes());h=v.pop('run_sha256');assert sha(canon(v))==h
assert sha(canon(v['named_topology_payload']))==v['named_topology_payload_sha256']
assert sha(canon(v['named_source_payload']))==v['named_source_payload_sha256']
put('lease.json',{'schema_version':1,'actor':'/root/next_primary59','status':'CLOSEDLAST','closed_at':now(),
 'foreground_readbacks_exit_code':p.returncode,'compiler':'NOT_STARTED_CLOSED',
 'native_run':pin(O/'reviewer.primary.run.json'),'run_sha256':h,
 'source_topology_self_approved':False,'independent_coverage_reviewer':'/root/whole_math52',
 'scope':'Preproof statement source acceptance plus independent source extraction; no proof or formal admission.'})
print(json.dumps({'status':'CLOSEDLAST','run_sha256':h,
 'named_topology_payload_sha256':v['named_topology_payload_sha256'],
 'named_source_payload_sha256':v['named_source_payload_sha256'],
 'readback_actual_exit_code':p.returncode,'source_statement':'PREPROOF_ACCEPTED','topology':'PENDING_DISTINCT_REVIEW'}))
