import hashlib,json,os,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf8')
O=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-next-primary58')
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf8')
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf8'))
def pin(p):
 p=Path(p).resolve();b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(l),'lf_sha256':sha(l)}
def check(q):assert pin(q['path'])==q,q['path']
def selfcheck(x,key='content_self_sha256'):assert x[key]==sha(canon({k:v for k,v in x.items() if k!=key}))
assert len(sys.argv)==3;chunk=sys.argv[1];seal_pid=int(sys.argv[2]);assert chunk and seal_pid>0
assert (O/'lease.json').read_bytes()==(O/'lease.open.json').read_bytes();closed=load(O/'lease.open.json');assert closed['status']=='OPEN'
control=load(O/'mutable-control-observation.json');selfcheck(control)
historical={z['original_actual_read_receipt']['path']:z for z in control['observations']}
for z in control['observations']:
 for k in ['original_exactraw_snapshot','original_LF_snapshot','current_exactraw_snapshot','current_LF_snapshot','exact_text_diff']:check(z[k])
inputs=[]
for n in ['input.manifest.json','supplemental.input.manifest.json']:
 m=load(O/n);selfcheck(m)
 for row in m['inputs']:
  for key,q in row.items():
   if key=='actual_input' and q['path'] in historical:
    z=historical[q['path']];assert q==z['original_actual_read_receipt']
    assert all(q[k]==z['original_exactraw_snapshot'][k] for k in ['bytes','raw_sha256','lf_bytes','lf_sha256'])
   else:check(q)
 inputs+=m['inputs']
r=load(O/'output.readbacks.json');selfcheck(r)
for q in r['artifacts']:check(q)
run=load(O/'reviewer.primary.run.json');selfcheck(run,'run_sha256');selfcheck(load(O/'complete.json'))
outputs=[pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='lease.json']
for q in outputs:check(q)
for k in ['status','read_lease','write_lease','Python_lease']:closed[k]='CLOSED'
closed.update({'native_schema':'independent-source-only-diagnosis-resource-lease-v1','actor':'/root/next_primary56','compiler_lease':'NOT_STARTED_CLOSED','compiler_started':False,'original_OPEN_snapshot':pin(O/'lease.open.json'),'input_manifests':[pin(O/'input.manifest.json'),pin(O/'supplemental.input.manifest.json')],'exact_native_input_count':56,'actual_all_input_and_snapshot_readbacks':True,'readtime_control_policy':'53 original inputs current-strict;3 original controls exact historical-snapshot-bound;3 separately observed current controls, total59 actual read events across56 unique input paths. Mutable control paths need not remain unchanged.','control_observation':pin(O/'mutable-control-observation.json'),'actual_read_events':59,'actual_output_artifacts':outputs,'exact_output_count':len(outputs),'all_output_readbacks_match':True,'native_run':pin(O/'reviewer.primary.run.json'),'native_run_complete_minus_run_sha256':run['run_sha256'],'source_contract':pin(O/'source.contract.json'),'blueprint':pin(O/'next-edge.blueprint.json'),'actual_sealing_foreground_process':{'native_exec_chunk':chunk,'actual_exit_code':0,'actual_pid':seal_pid,'script':pin(O/'seal_diagnosis.py')},'foreground_closer':{'actual_pid':os.getpid(),'script':pin(O/'close_lease.py'),'detached':False,'post_write':'Readonly actual lease/self-hash assertions and stdout only; returned exit code reported externally.'},'candidate58_math_or_statement_or_proof_exposure':'NONE','existing_provider_fragments_and_actual57Test_exposure':'Disclosed, no strict provider-body blindness claim; previous56/57 finalbody exposure retained.','whole_math_verdict_read':False,'formal_admission':False,'recommended_next_edge':'Exactactual sndM onto macro/centered range and actualH_P0 squared-defectgap integration; noGamma/root/Loewner/inverse admission.','negative_chronology':'All collection negatives/corrections/failed scripts retained as pinned own outputs; original57 and56 CLOSED evidence unchanged.','hash_recipe':'Complete JSON object minus ONLY content_self_sha256, sorted compact ensure_ascii=False UTF8 no newline. Exact raw and CRLF->LF hashes/byte counts distinct.','final_write':'This lease.json CLOSED is the final filesystem write; itself excluded from output list to avoid recursive self receipt.'})
closed['content_self_sha256']=sha(canon(closed))
# Final filesystem write. No output or script is modified afterward.
(O/'lease.json').write_bytes((json.dumps(closed,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
assert load(O/'lease.json')==closed;selfcheck(load(O/'lease.json'))
assert all(closed[k]=='CLOSED' for k in ['status','read_lease','write_lease','Python_lease'])
print(json.dumps({'status':'CLOSED_LAST','pid':os.getpid(),'inputs':56,'outputs':len(outputs),'lease':pin(O/'lease.json'),'lease_complete_minus_content_self_sha256':closed['content_self_sha256'],'run_sha256':run['run_sha256'],'compiler':'NOT_STARTED_CLOSED','formal_admission':False},ensure_ascii=False))
