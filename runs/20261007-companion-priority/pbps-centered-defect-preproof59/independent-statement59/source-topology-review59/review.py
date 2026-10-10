import os,sys,pathlib,json,hashlib,datetime,subprocess,re
from html.parser import HTMLParser
ROOT=pathlib.Path('E:/Samplinglib');os.chdir(ROOT)
R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59'
S=R/'independent-source-topology59';D=R/'independent-statement59/source-topology-review59'
ACTOR='/root/whole_math52';D.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def path(p):return pathlib.Path(p) if pathlib.Path(p).is_absolute() else ROOT/p
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
seen={}
def check(row):
 a=pin(row['path']);assert all(a[k]==row[k] for k in ['bytes','raw_sha256','lf_sha256']);seen[a['path']]=a;return a
def bind(p):a=pin(p);seen[a['path']]=a;return a
def selfcheck(q,k):assert sha(canon({a:b for a,b in q.items() if a!=k}))==q[k]
class Literal(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.math=0
 def handle_starttag(self,tag,attrs):
  if tag=='math':
   self.math+=1;self.parts.append(dict(attrs).get('alttext',''))
  elif not self.math:self.parts.append(' ')
 def handle_endtag(self,tag):
  if tag=='math':self.math-=1
  if not self.math:self.parts.append(' ')
 def handle_data(self,t):
  if not self.math:self.parts.append(t)
def norm(t):return ' '.join(t.split())
def literal(b):p=Literal();p.feed(b.decode('utf8'));return norm(' '.join(p.parts))
write(D/'lease.open.json',dict(actor=ACTOR,status='OPEN',pid=os.getpid(),compiler='NOT_STARTED',scope='Distinct literal source topology/coverage review only; original mathematical stage immutable'))
idx=load(S/'indexed-input.manifest.json');bind(S/'indexed-input.manifest.json')
for row in idx['inputs']:
 a=check(row['qualified_input']);b=check(row['qualified_immutable_snapshot']);assert a['raw_sha256']==b['raw_sha256']
for k in ['large_primary_reused_without_copy','own_source_before_current_candidate','source_graph_before_current_candidate']:check(idx[k])
top=load(S/'named-topology.payload.json');bind(S/'named-topology.payload.json')
for row in top['files']:check(row)
check(top['candidate_header0']);check(top['candidate_header1'])
q=load(S/'reviewer.primary.run.json');bind(S/'reviewer.primary.run.json');selfcheck(q,'run_sha256')
assert q['named_topology_payload']==top and sha(canon(top))==q['named_topology_payload_sha256']
lease=load(S/'lease.json');bind(S/'lease.json');check(lease['native_run'])
assert lease['status']=='CLOSEDLAST' and lease['foreground_readbacks_exit_code']==0 and lease['run_sha256']==q['run_sha256'] and not lease['source_topology_self_approved']
fb=load(S/'foreground-readbacks.json');bind(S/'foreground-readbacks.json');assert fb['actual_exit_code']==0
# Do not consume source-statement verdict/rationale, named-source payload, or its review.
g=load(S/'source-proof-graph.json');selfcheck(g,'source_graph_sha256')
c=load(S/'source-coverage.manifest.json')
for k in ['primary_regions','supplemental_regions','graph']:check(c[k])
primary=path(idx['large_primary_reused_without_copy']['path']).read_bytes();regions=[]
for f in ['primary.source-first.json','primary.supplemental-context.json']:
 p=load(S/f);check(p['primary'])
 for row in p['exact_regions']:
  b=primary[row['start_utf8_byte']:row['end_utf8_byte_exclusive']]
  assert len(b)==row['slice_bytes'] and sha(b)==row['slice_sha256'] and row['balanced']
  text=literal(b);assert text==norm(row['text']),(row['id'],text,norm(row['text']))
  regions.append(dict(id=row['id'],start_utf8_byte=row['start_utf8_byte'],end_utf8_byte_exclusive=row['end_utf8_byte_exclusive'],bytes=len(b),raw_sha256=sha(b),independently_decoded_literal=text))
assert len(regions)==31 and len({r['id'] for r in regions})==31
nodes={x['id']:x for x in g['nodes']};assert len(nodes)==19 and len(g['edges'])==23
assert len(c['items'])==54 and sum(i['disposition']=='NODE' for i in c['items'])==25 and sum(i['disposition']=='EXCLUDED' for i in c['items'])==29
assert len({i['item_id'] for i in c['items']})==54
for item in c['items']:
 assert not item['formal_completion_claim']
 if item['disposition']=='NODE':assert item['node'] in nodes and item['consumer_use_site']
 else:assert item['reason']
for edge in g['edges']:assert edge['from'] in nodes and edge['to'] in nodes and edge['consumer_use_site']
assert len(g['proof_routes'])==4 and all(r['operator']=='AND' and r['selected'] for r in g['proof_routes'])
assert 'source-correspondence-only' in next(e['truth'] for e in g['edges'] if e['from']=='S:D' and e['to']=='A:D0')
assert not g['Gamma_or_fullpaper_admission'] and not g['source_topology_self_approval'] and not g['implementation_read']
for f in ['statement-candidate.json','header0.lean','header1.lean']:bind(R/f)
bind(R/'independent-statement59/receipt.json');bind(R/'independent-statement59/run.json');bind(R/'independent-statement59/lease.json')
mr=load(R/'independent-statement59/run.json');selfcheck(mr,'run_sha256')
assert load(R/'independent-statement59/lease.json')['status']=='CLOSED'
head=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
assert head=='d9bff202c861985eb444e75d6aa65ec5d65c65cf'
assert not (ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean').exists()
assert not (ROOT/'Tests/ProximalBPSCenteredDefect.lean').exists()
texts={r['id']:r['independently_decoded_literal'] for r in regions}
assert 'Writing \\mathsf{U}^{2}=I in blocks gives' in texts['A2.SS1.p3']
incoming=[e['from'] for e in g['edges'] if e['to']=='S:D'];assert incoming==['S:A']
payload=dict(payload_name='independent-literal-source-topology-coverage59',checked_base=head,
 exact_source_graph=pin(S/'source-proof-graph.json'),exact_coverage_manifest=pin(S/'source-coverage.manifest.json'),
 graph_nodes=19,graph_edges=23,raw_regions=31,coverage_items=54,NODE_count=25,EXCLUDED_count=29,selected_route_hyperedges=4,
 coverage_verdict='ACCEPT_EXHAUSTIVE_BOUNDED_31_REGION_INVENTORY',
 topology_verdict='BLOCKED_SOURCE_B5_IDENTITY_INGREDIENT_EDGE',
 blocker=dict(id='SPG59-B5-1',classification='source-proof-graph-ingredient-omission',node='S:D',actual_incoming=incoming,
 literal_source_anchor='A2.SS1.p3 / A2.E5',literal_reason='Printed source derives B5 by writing U²=I in blocks. S:A states only the selfadjoint contraction A=PUP. This alone does not determine the off-diagonal B or prove B*B=I-A².',
 required_successor='Preserve original graph and add a separately reviewed explicit U involution/unitarity and block/projection ingredient route into S:D (direct S:U and S:P ingredients or a precise named block-identity derivation adapter). No signature or mathematical premise repair.',
 minimality='Selected actual scalar positivity route uses T/T0 contraction and is unaffected; mathematical two-header seal remains CLOSED accepted.'),
 independent_reconstruction=[
 'S1/S2/B12 retain original C2/Hessian/alpha/beta/eta cap and normalized Gibbs/independent Gaussian joint law.',
 'B1 conditional Y projection; B2 macro snd range versus excluded micro kernel; B3 generic joint operator notation is distinct from actual scalar T.',
 'B4 literal (x,2x-y) reflection; paragraph asserts selfadjoint/unitary then U²=I proves BOTH B5 identities. Second off-diagonal identity excluded explicitly.',
 'B8/B9 actual (Y+,Y-) and conditional mean support scalar adapter; variance identity is reused parent context, not a new59 theorem.',
 'D1 AE real L2, mean-zero domain, closed orthogonal projection, bounded adjoints/Loewner order. Spectral calculus and positive square root remain explicitly excluded.',
 'D2 stationary Markov observables and constants support actual law/mean adapter; density evolution/chi2 conclusions excluded.',
 'C1/C2 score covariance/Hessian/PI and density-closedness are earlier-parent context; C3/C4 centered marginal PI plus sharp energy yield rho. They are not new caller certificates.',
 'C4 spectral interval and later -1/2, C5 exchangeability/Gaussian PI, C6 difference estimates are excluded with separate entries.',
 'B10/B11/Gamma, B15 root gap, B16 centered Gamma inverse/polar and halfturn branch are excluded; IsUnit squared D0 supplies none of them.',
 'Citations DMS15/LW22 identify terminology and remain external; they provide no imported Lean theorem premise.',
 'All4 selected AND routes describe actual scalar compression/mean/restriction/coercivity-unit consequences. B5-to-scalar-defect edge is explicitly correspondence only and is not an additional AND parent.'
 ],
 remaining=['Exact B5 source-ingredient topology overlay requires distinct review before complete topology admission.','Source statement-fidelity verdict is separately owned and not read or adopted here.','No59 body/Lean theorem/VERIFIED/publication or Gamma/root/weakH1/polar/dynamics/main/cost/composition/fullpaper/PURIFIED admission.'])
write(D/'raw-source-regions.independent.json',dict(regions=regions,primary=pin(path(idx['large_primary_reused_without_copy']['path']))))
write(D/'topology-review.payload.json',payload)
write(D/'inputs.json',dict(inputs=list(seen.values()),count=len(seen)))
write(D/'checks.json',dict(status='CHECKS_COMPLETE_WITH_TYPED_TOPOLOGY_BLOCKER',actual_pid=os.getpid(),native_source_run_self=q['run_sha256'],native_topology_payload_sha256=q['named_topology_payload_sha256'],native_graph_self=g['source_graph_sha256'],strict_index_pairs=10,region_checks=31,coverage_checks=54,node_checks=19,edge_checks=23,selected_routes=4,source_verdict_read=False))
print(json.dumps(dict(status='COMPLETE_WITH_TYPED_TOPOLOGY_BLOCKER',pid=os.getpid(),inputs=len(seen),regions=31,coverage=54,payload_sha256=sha(canon(payload)))))
