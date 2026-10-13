import hashlib,json,os,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/phase-pbps-next-primary58'
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf8'))
def pin(p):
 p=Path(p).resolve();b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(l),'lf_sha256':sha(l)}
def check(q):assert pin(q['path'])==q,q['path']
def selfcheck(x,key='content_self_sha256'):assert x[key]==sha(canon({k:v for k,v in x.items() if k!=key}))
def write(n,x,key='content_self_sha256'):
 assert not (O/n).exists();assert key not in x;x=dict(x);x[key]=sha(canon(x));(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'));assert load(O/n)==x;selfcheck(load(O/n),key);return x
assert (O/'lease.json').read_bytes()==(O/'lease.open.json').read_bytes()
assert load(O/'lease.json')['status']=='OPEN'
inputs=[]
for n in ['input.manifest.json','supplemental.input.manifest.json']:
 m=load(O/n);selfcheck(m);assert len(m['inputs'])==m['count']
 for row in m['inputs']:
  for receipt in row.values():check(receipt)
 inputs+=m['inputs']
assert len(inputs)==56
for n in ['source.contract.json','reuse.inventory.json','next-edge.blueprint.json','publication.actual.packet.json','collection.correction.json','collection.process.json','publication.bounded.packet.json']:selfcheck(load(O/n))
primary=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57'
for n in ['primary.contract.json','source.precision-addendum.json','next-consumer.blueprint.json','lease.json']:selfcheck(load(primary/n))
write('process.status.json',{'schema_version':1,'native_schema':'foreground-source-only-diagnosis-process-receipts','collection':{'actual_native_exec_chunk':'102824','actual_exit_code':0,'actual_pid':39368,'script':pin(O/'collect_inputs.py')},'author':{'actual_native_exec_chunk':'ce50ec','actual_exit_code':0,'script':pin(O/'author_diagnosis.py'),'pid':'Not printed by author; no invented PID'},'open_author_scope_correction':{'actual_native_exec_chunk':'9281b7','actual_exit_code':0,'script':pin(O/'correct_author_scope.py'),'scope':'Only unexecuted own author script corrected before diagnosis output generation; no immutable source artifact changed.'},'operational_negatives':['e423ca GBK console Unicode EXIT1 preserved by collection.process chronology.','79c017 capsule subprocess GBK EXIT1 stdout/stderr/script preserved; explicitUTF8 corrected collection102824 EXIT0.','Wrong publication wrapper projection preserved; distinct actual native items[0] packet and correction.','Earlier negative says snapshots rewritten; collection.correction records actual check-without-rewrite.','d1783c PowerShell ParserError, nonexistent guessed API paths and failed apply_patch request before changes; no proof search/compiler.'],'compiler_started':False})
out=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
for q in out:check(q)
write('manifest.json',{'schema_version':1,'native_schema':'nonrecursive-source-only-pre-run-output-manifest','actor':'/root/next_primary56','artifacts':out,'count':len(out),'exclusions':'Own manifest and outputs authored later; final output.readbacks and CLOSED resource lease pin their preceding DAG, never themselves recursively.'})
run=write('reviewer.primary.run.json',{'schema_version':1,'native_schema':'independent-source-only-next-edge-diagnosis-run','actor':'/root/next_primary56','result_kind':'source-only-candidate-diagnosis','source_contract':pin(O/'source.contract.json'),'blueprint':pin(O/'next-edge.blueprint.json'),'reuse_inventory':pin(O/'reuse.inventory.json'),'input_manifests':[pin(O/'input.manifest.json'),pin(O/'supplemental.input.manifest.json')],'exact_native_input_count':56,'all_actual_raw_lf_and_snapshot_readbacks_match':True,'own_primary57_complete_objects_verified':True,'process_status':pin(O/'process.status.json'),'preceding_output_manifest':pin(O/'manifest.json'),'science_commit_checked':'e8a9044ba5a945eaa4b4aecd110b63494fe6c68e','source57_scope':'Actualcompact-gradientclosurePI/SAMEscalarconsumer, notsourceweakH1/fullB13/Gamma/papercomplete','recommendation':'Exactactual sndM macro/centered range plus actualH_P0 squareddefectgap integration; rootseparate.','candidate58_statement_or_proof_exposure':'NONE','existing_parent_Test_body_and_incidental_fragments_exposed':True,'strict_provider_body_blindness':False,'whole_math_verdict_read':False,'compiler':'NOT_STARTED_CLOSED','formal_admission':False,'hash_recipe':'Complete JSON object minus ONLY run_sha256, sorted compact ensure_ascii=False UTF8 no newline. Distinct exact raw and only CRLF->LF receipts include byte counts.'},'run_sha256')
write('complete.json',{'schema_version':1,'native_schema':'source-only-next-edge-diagnosis-complete','actor':'/root/next_primary56','native_run':pin(O/'reviewer.primary.run.json'),'native_run_complete_minus_run_sha256':run['run_sha256'],'source_contract':pin(O/'source.contract.json'),'blueprint':pin(O/'next-edge.blueprint.json'),'inventory':pin(O/'reuse.inventory.json'),'inputs':56,'candidate_or_proof_or_statement_seal':False,'compiler_started':False,'formal_source_or_math_admission':False,'resource_closure':'Original OPEN own lease will be CLOSED LAST after this foreground sealing process actually returns EXIT0; final closer performs only readback after that write.'})
out=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
for q in out:check(q)
write('output.readbacks.json',{'schema_version':1,'native_schema':'actual-source-only-output-readbacks','artifacts':out,'count':len(out),'all_match':True,'self_exclusion':'Own readback JSON is itself pinned in final CLOSED lease; nonrecursive.'})
print(json.dumps({'status':'SEALED_SOURCE_ONLY_DIAGNOSIS_PENDING_LEASE','pid':os.getpid(),'inputs':56,'outputs_before_readbacks':len(out),'run':pin(O/'reviewer.primary.run.json'),'run_sha256':run['run_sha256'],'source_contract':pin(O/'source.contract.json'),'blueprint':pin(O/'next-edge.blueprint.json'),'compiler':'NOT_STARTED_CLOSED'},ensure_ascii=False))
