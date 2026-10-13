from pathlib import Path
import hashlib,json,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;M=O.parent;P=M.parent
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
old=P.parent/'pbps-actual-endpoint-time-reversal97/next-primary98/source-proof-graph98.v2.native.json';new=P/'source-proof-graph98.v3.native.json';header=P/'Header98.lean'
assert info(new)['raw_sha256']=='c04c64a8fab1768f95542626f7f0e8f31db3874acd02fbcbe9776624e801b71a'
assert info(old)['raw_sha256']=='6a532895561a70ead461a84c8561de82dcfb000f1814aa1113670a4f40bcf929'
assert info(header)['raw_sha256']=='50c6999fe069f4cf648832a804b71bb8e447b7a3aea0f0c42a836f81650c6ad0'
a=load(old);b=load(new);extra=[e for e in b['edges'] if e not in a['edges']]
assert len(extra)==1 and b['edges']==a['edges']+extra
e=extra[0];assert e['from']=='B98' and e['to']=='WEIGHT99' and e['logic']=='AND' and not e['certified_lean_edge']
assert 'U_y(R A)=U_y(A)' in e['projection'] and 'w_y(R A)=w_y(A)' in e['projection']
assert b['predecessor_graph']==dict(path=info(old)['path'],raw_sha256=info(old)['raw_sha256'])
c=dict(b);c['edges']=a['edges'];c.pop('predecessor_graph');c.pop('independent_revision_reason');assert c==a
prior=load(M/'closed-RAW-manifest98.native.json')
for x in prior['files']:assert info(R/x['path'])['raw_sha256']==x['raw_sha256'],x['path']
inputs=[];snap=O/'inputs';snap.mkdir()
for i,p in enumerate([old,new,header,M/'header-math-decision98.native.json',M/'graph-v2-negative98.native.json',M/'closed-RAW-manifest98.native.json']):
 q=snap/(str(i).zfill(2)+'.'+p.name+'.exactraw');q.write_bytes(p.read_bytes());inputs.append(dict(**info(p),snapshot=q.relative_to(R).as_posix()))
write('source-topology-decision98.native.json',dict(kind='independent-graph-only-correction-validation',reviewer='/root/exact_verifier96',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),decision='ACCEPT_EXACT_GRAPH_V3_CORRECTION',review_mode='Nonblind topology validation against prior independent mathematical/source audit; not a second source reconstruction',graph=info(new),predecessor=info(old),header=info(header),exact_added_edge=e,all_original_nodes_and_edges_preserved=True,only_other_changes=['predecessor_graph','independent_revision_reason'],mathematical_reason='FINITE98 balances exp(-U(z)) against exp(-U(A)); the later Theta-weight comparison requires exp(-U(RA)). The added edge correctly consumes the R-invariance projection of B98 at WEIGHT99. The proof is pointwise norm-neg invariance of the momentum energy; no Jacobian, pathwise jump equality, or new public provider assumption is introduced.',bounded98_subgraph_unchanged=True,prior_negative_evidence_preserved=True,prior_header_math_acceptance_transfers=True,required_repairs=[],inputs=inputs,scope='Accepts this exact graph correction and prospective finite98 mathematical plan. Later INV99/L2EXT remain schematic obligations subject to explicit contracts when promoted. No Lean implementation, Statement Seal, source final admission, SAU transition or proof credit.'))
write('closed-RAW-topology98.native.json',dict(kind='closed-independent-v3-topology98-validation',hash_recipe='SHA256 of exact original bytes without newline normalization',self_hash_omitted=True,inputs=inputs,files=[info(p) for p in sorted(O.rglob('*')) if p.is_file()]))
for n in ['source-topology-decision98.native.json','closed-RAW-topology98.native.json']:print(json.dumps(info(O/n)))
