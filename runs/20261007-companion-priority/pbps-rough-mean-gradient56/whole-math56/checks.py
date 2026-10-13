from common import *
os.environ['PYTHONUTF8']='1'
sys.stdout.reconfigure(encoding='utf-8')
rows=strict('inputs.post-analysis.json')
assert git('rev-parse','HEAD')==BASE
P=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean'
Q=R/'Tests/ProximalBPSRoughMeanGradient.lean'
parents=[R/'AutoSamplingTheory/ExampleCases/ProximalBPS'/x for x in ('SourceMeanGradientDomain.lean','L2MacroscopicMean.lean','MacroscopicEnergy.lean')]
text=P.read_text(encoding='utf-8'); signature=text[text.index('theorem actual_rough_mean_gradient'):text.index(' := by')]+ '\n'
seal=load(R/'runs/20261007-companion-priority/pbps-rough-mean-gradient-preproof56/statement-seals.accepted.json')['signatures'][0]
assert signature==seal['signature_text'] and len(signature.encode())==1755 and sha(signature.encode())==seal['signature_lf_sha256']
(O/'signature.exact.LF.txt').write_bytes(signature.encode())
(O/'production.raw.snapshot.lean').write_bytes(P.read_bytes())
(O/'Tests.raw.snapshot.lean').write_bytes(Q.read_bytes())
sys.path.insert(0,str(R/'tools'));import astis
fake=[]
for p in [P,Q,*parents]:
 code=astis.strip_lean_comments_and_strings(p.read_text(encoding='utf-8'))
 findings=[{'line':i,'code':s} for i,s in enumerate(code.splitlines(),1) if astis.FORBIDDEN_REGEX.search(s)]
 assert not findings,(str(p),findings)
 fake.append({'input':pin(p),'findings':findings})
assert len(re.findall(r'^theorem ',text,re.M))==1
assert not re.search(r'^\s*(?:private\s+)?(?:def|axiom|instance|opaque|abbrev|lemma)\b',text,re.M)
for parent in load(B/'math-freeze.json')['actual_ASTIS_parents']:assert parent.rsplit('.',2)[-2]+'.'+parent.rsplit('.',1)[-1] in text
log=(O/'focused.log').read_text(encoding='utf-8')
assert 'Build completed successfully (3899 jobs)' in log and 'sorryAx' not in log
closures=re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]",log,re.S)
closures=[{'declaration':n,'axioms':re.findall(r'\b(?:propext|Classical.choice|Quot.sound|sorryAx)\b',a)} for n,a in closures]
expected=[TARGET,'Tests.ProximalBPSRoughMeanGradient.actual_joint_block_rough_difference','Tests.ProximalBPSRoughMeanGradient.actual_sharp_endpoint_zero_gradient']
own=[c for c in closures if c['declaration'] in expected]
assert {c['declaration'] for c in own}==set(expected) and all(set(c['axioms'])=={'propext','Classical.choice','Quot.sound'} for c in own)
status=load(O/'focused.status.json');assert status['exit_code']==0 and status['process_id']==9680 and equal(status['log']) and equal(status['production']) and equal(status['Tests'])
assert load(O/'compiler.lease.json')['status']=='CLOSED'
native=[]; leases=[]
for row in rows:
 p=path(row['path'])
 if p.suffix!='.json':continue
 d=load(p)
 if not isinstance(d,dict):continue
 if 'content_self_sha256' in d:
  h=logical({k:v for k,v in d.items() if k!='content_self_sha256'});assert h==d['content_self_sha256'],str(p)
  native.append({'input':pin(p),'self_field':'content_self_sha256','whole_logical_sha256':h,'recipe':'Entire object minus ONLY content_self_sha256, sorted compact UTF8 JSON, ensure_ascii=False, no newline'})
 if 'self_digest' in d:
  x=d['self_digest'];payload=json.dumps({k:v for k,v in d.items() if k!='self_digest'},sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
  nk='named_payload_sha256' if 'named_payload_sha256' in x else 'payload_sha256';bk='named_payload_bytes' if 'named_payload_bytes' in x else 'payload_bytes'
  assert sha(payload)==x[nk] and len(payload)==x[bk],str(p)
  native.append({'input':pin(p),'self_field':'self_digest','native_digest_schema':x,'whole_logical_sha256':sha(payload),'whole_logical_bytes':len(payload),'interpretation':'Native named_payload fields here hash entire remaining object, not an independently chosen projection; complete native recipe checked'})
 if p.name.endswith('lease.json'):
  assert d.get('status')=='CLOSED',str(p)
  leases.append({'input':pin(p),'actual_status':'CLOSED','resources':d.get('resources',{k:d[k] for k in ('compiler','Python','read','write') if k in d}),'exit_code':d.get('exit_code')})
attempts=[]
for n,code in [('production.0',1),('production.1',1),('production.2',0),('tests.0',1),('tests.1',0)]:
 d=load(B/(n+'.status.json'));l=load(B/(n+'.compiler.lease.json'));lp=pin(B/(n+'.log'))
 assert d['exit_code']==code and l['exit_code']==code and l['status']=='CLOSED' and lp['raw_sha256']==d['log_raw_sha256']
 snapshots=[e for e in rows if e['raw_sha256']==d['source_raw_sha256']];assert snapshots,(n,'missing actual source snapshot')
 attempts.append({'attempt':n,'exit_code':code,'process_id':d['process_id'],'status':pin(B/(n+'.status.json')),'log':lp,'lease':pin(B/(n+'.compiler.lease.json')),'actual_source_snapshot':snapshots})
assert 'sorryAx' in (B/'tests.0.log').read_text(encoding='utf-8')
topology=R/'runs/20261007-companion-priority/pbps-rough-mean-gradient-sourcegraph56'
neg=load(topology/'review56/topology.review.json');repair=load(topology/'edge-repair-review56/edge-repair.review.json')
assert neg['verdict']=='SOURCE_TOPOLOGY_BLOCKED_MISSING_INPUT_EDGES' and repair['verdict']=='ACCEPT_REPAIRED_SOURCE_TOPOLOGY_ONLY'
api_paths=[R/'.lake/packages/mathlib/Mathlib'/x for x in ('Analysis/Normed/Operator/Extend.lean','Topology/Algebra/Module/LinearPMap.lean','LinearAlgebra/LinearPMap.lean','Probability/Kernel/Composition/MeasureComp.lean')]
dump('checks.json',{'status':'PASS','checked_base_commit':BASE,'exact_signature':{'declaration':TARGET,'LF_bytes':1755,'LF_sha256':sha(signature.encode()),'snapshot':pin(O/'signature.exact.LF.txt')},'original_pin_count':418,'direct_original_checks':'All original current raw/LF/bytes exact; no mapping, exclusions or silent changed-file skips','source_and_full_body_fake_scan':fake,'scan_implementation':pin(R/'tools/astis.py'),'current_main_and_Test_axiom_closures':own,'actual_focused_build':status,'native_full_self_check_count':len(native),'native_full_self_checks':native,'actual_CLOSED_prior_leases_count':len(leases),'actual_CLOSED_prior_leases':leases,'retained_root_attempts':attempts,'source_topology_negative':pin(topology/'review56/topology.review.json'),'distinct_accepted_minimal_edge_repair':pin(topology/'edge-repair-review56/edge-repair.review.json'),'API_inputs':list(map(pin,api_paths)),'own_observability_negative':{'kind':'stdout-encoding','description':'One read-only stdin inspector exited1 when default GBK stdout could not print a source unicode symbol; rerun with PYTHONUTF8=1 printed successfully. No compiler/mathematical failure, source mutation or discarded evidence.'}})
print(json.dumps({'status':'PASS','original_pin_count':418,'native_self_count':len(native),'prior_closed_leases':len(leases),'axiom_closures':len(own),'actual_compiler_PID':9680,'exit_code':0},ensure_ascii=False))
