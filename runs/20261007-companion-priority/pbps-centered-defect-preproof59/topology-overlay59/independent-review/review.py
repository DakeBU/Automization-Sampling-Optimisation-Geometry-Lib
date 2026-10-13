import pathlib,json,hashlib,os
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59';O=R/'topology-overlay59';D=O/'independent-review';D.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def path(p):return pathlib.Path(p) if pathlib.Path(p).is_absolute() else ROOT/p
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
seen={}
def bind(p):a=pin(p);seen[a['path']]=a;return a
def check(q):
 a=bind(q['path']);assert all(a[k]==q[k] for k in ['bytes','raw_sha256','lf_sha256']);return a
def selfcheck(q,k):assert sha(canon({a:b for a,b in q.items() if a!=k}))==q[k]
proposal=load(O/'exact-proposal.json');bind(O/'exact-proposal.json')
assert proposal['created_by']!='whole_math52' and proposal['repair_id']=='SPG59-B5-1'
for k in ['parent_graph','parent_coverage','negative_review','successor_graph','successor_coverage']:check(proposal[k])
for row in proposal['unchanged']['headers']:check(row)
original=load(path(proposal['parent_graph']['path']));successor=load(path(proposal['successor_graph']['path']))
selfcheck(original,'source_graph_sha256');selfcheck(successor,'source_graph_sha256')
graph_changed={k for k in set(original)|set(successor) if original.get(k)!=successor.get(k)}
assert graph_changed=={'status','edges','proof_routes','repair_parent_graph','repair_id','source_graph_sha256'}
assert successor['repair_parent_graph']==proposal['parent_graph'] and successor['repair_id']=='SPG59-B5-1'
assert successor['nodes']==original['nodes'] and len(original['nodes'])==19
assert successor['edges'][:23]==original['edges'] and len(original['edges'])==23 and len(successor['edges'])==25
newedges=successor['edges'][23:];assert [(e['from'],e['to']) for e in newedges]==[('S:U','S:D'),('S:P','S:D')]
assert 'U squared is identity' in newedges[0]['conditional_discharge']
assert 'B=(I-P)UP' in newedges[1]['conditional_discharge']
assert successor['proof_routes'][:4]==original['proof_routes'] and len(original['proof_routes'])==4 and len(successor['proof_routes'])==5
route=successor['proof_routes'][4]
assert route['id']=='route:printed-B5-block-identity' and route['operator']=='AND' and route['parents']==['S:U','S:P','S:A'] and route['conclusion']=='S:D' and not route['selected']
assert 'identity on macro' in route['meaning'] and 'does not claim identity on the full joint space' in route['meaning']
assert sum(r['selected'] for r in successor['proof_routes'])==4
a=load(path(proposal['parent_coverage']['path']));b=load(path(proposal['successor_coverage']['path']))
coverage_changed={k for k in set(a)|set(b) if a.get(k)!=b.get(k)}
assert coverage_changed=={'status','graph','parent_coverage'} and b['parent_coverage']==proposal['parent_coverage'] and b['graph']==proposal['successor_graph']
assert a['items']==b['items'] and len(b['items'])==54 and b['NODE_count']==25 and b['EXCLUDED_count']==29
negative=load(path(proposal['negative_review']['path']));assert negative['verdict']=='BLOCKED_SOURCE_B5_IDENTITY_INGREDIENT_EDGE'
N=R/'independent-statement59/source-topology-review59'
for f in ['run.json','lease.json','raw-source-regions.independent.json']:bind(N/f)
oldrun=load(N/'run.json');selfcheck(oldrun,'run_sha256');assert load(N/'lease.json')['status']=='CLOSED'
raw=load(N/'raw-source-regions.independent.json');check(raw['primary']);primary=path(raw['primary']['path']).read_bytes()
source=[]
for row in raw['regions']:
 if row['id'] in ['A2.SS1.p3','A2.E5']:
  actual=primary[row['start_utf8_byte']:row['end_utf8_byte_exclusive']]
  assert len(actual)==row['bytes'] and sha(actual)==row['raw_sha256'];source.append(row)
assert len(source)==2
assert 'Writing \\mathsf{U}^{2}=I in blocks gives' in next(r['independently_decoded_literal'] for r in source if r['id']=='A2.SS1.p3')
assert not successor['Gamma_or_fullpaper_admission'] and not successor['implementation_read'] and not successor['source_topology_self_approval']
assert 'source-correspondence-only' in next(e['truth'] for e in successor['edges'] if e['from']=='S:D' and e['to']=='A:D0')
assert not (ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean').exists()
assert not (ROOT/'Tests/ProximalBPSCenteredDefect.lean').exists()
payload=dict(payload_name='independent-exact-B5-topology-overlay59',repair_id='SPG59-B5-1',verdict='ACCEPT_EXACT_TOPOLOGY_OVERLAY_NO_BLOCKER',
 proposal=pin(O/'exact-proposal.json'),successor_graph=proposal['successor_graph'],successor_coverage=proposal['successor_coverage'],
 graph_json_changes=sorted(graph_changed),coverage_json_changes=sorted(coverage_changed),appended_edges=newedges,appended_nonselected_AND_route=route,
 unchanged=dict(nodes=19,old_edges=23,selected_routes=4,coverage_items=54,NODE=25,EXCLUDED=29,header_count=2),
 source_evidence=source,
 mathematical_reason='For the orthogonal projection P and selfadjoint involution U, A=PUP and B=(I-P)UP satisfy B*B=P U(I-P)UP=P U²P-(PUP)²=P-A² on the ambient joint Hilbert space. On ran(P), P is the identity, giving exactly B*B=I_macro-A². The two new ingredient edges and explicit nonselected printed-source AND route encode this derivation. They resolve the original missing ingredient without making B5 a required scalar-defect parent.',
 prior_negative_preserved=proposal['negative_review'],
 scope='Exact source-topology metadata repair only; reuses CLOSED bounded coverage and mathematical StatementSeal59. No source-statement fidelity verdict, implementation, compiler, VERIFIED, Gamma/root/weakH1/polar/dynamics/main/cost/composition/fullpaper/PURIFIED credit.',
 blockers=[])
write(D/'repair.payload.json',payload);write(D/'inputs.json',dict(inputs=list(seen.values()),count=len(seen)))
write(D/'checks.json',dict(status='PASS_EXACT_OVERLAY',actual_pid=os.getpid(),graph_change_keys=sorted(graph_changed),coverage_change_keys=sorted(coverage_changed),source_slice_checks=2,raw_lf_inputs=len(seen),native_parent_run_self=oldrun['run_sha256'],native_successor_graph_self=successor['source_graph_sha256']))
print(json.dumps(dict(status='PASS_EXACT_OVERLAY',actual_pid=os.getpid(),inputs=len(seen),repair_payload_sha256=sha(canon(payload)))))
