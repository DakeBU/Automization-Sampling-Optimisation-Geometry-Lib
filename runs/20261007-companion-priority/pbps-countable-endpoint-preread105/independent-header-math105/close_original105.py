from pathlib import Path
import hashlib,json
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;S=R/'runs/20261007-companion-priority/pbps-actual-normalized-endpoint104/next-primary105'
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bound={}
def refs(v):
 if isinstance(v,dict):
  if 'path' in v and 'raw_sha256' in v:
   p=R/v['path'];b=p.read_bytes();assert sha(b)==v['raw_sha256'],v['path'];bound[v['path']]=info(p)
   if 'raw_span_sha256' in v:
    span=b''.join(b.splitlines(keepends=True)[v['line_start']-1:v['line_end']]);assert sha(span)==v['raw_span_sha256']
  for x in v.values():refs(x)
 elif isinstance(v,list):
  for x in v:refs(x)
for p in S.glob('*.json'):refs(load(p));bound[info(p)['path']]=info(p)
g=load(S/'source-proof-graph-delta105.native.json');base=load(R/g['independent_base_topology_binding']['path'])['effective_graph'];nodes=set(base['nodes']);edges={tuple(e) for e in base['edges']};assert(len(nodes),len(edges))==(55,96)
nodes|={x['id'] for x in g['new_nodes']}
groups={(a,x['target']) for x in g['AND_dependency_groups'] for a in x['parents']};producer={(x['source'],x['target']) for x in g['producer_edges']};assert groups==producer
edges|=producer|{(x['source'],x['target']) for x in g['future_consumer_edges']};assert all(a in nodes and b in nodes for a,b in edges)
todo=set(nodes);order=[]
while todo:
 ready=sorted(n for n in todo if not any(b==n and a in todo for a,b in edges));assert ready;todo.difference_update(ready);order+=ready
assert (len(nodes),len(edges))==(60,111)
cov=load(S/'source-coverage-delta105.native.json');primary=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=primary.read_bytes();lines=raw.splitlines(keepends=True)
assert len(cov['regions'])==21
for x in cov['regions']:assert sha(raw[x['byte_start']:x['byte_end_exclusive']])==x['raw_sha256']==sha(b''.join(lines[x['line_start']-1:x['line_end']]))
header=(O.parent/'Header105.lean').read_text(encoding='utf-8');p93=(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean').read_text(encoding='utf-8').split('private def actual_finite_count_path_statement',1)[1]
hdefs=header.split('    let c :',1)[1].split('    let R :',1)[0];pdefs=p93.split('    let c :',1)[1].split('    ∃ Z :',1)[0];assert hdefs==pdefs
hz=header.split('    ∃ Z :',1)[1].split('      (∀ y r : E, ∀ T',1)[0];pz=p93.split('    ∃ Z :',1)[1].split('      (∀ n : ℕ, ∀ T',1)[0];assert hz==pz
assert load(O/'fresh-type-api.receipt.json')['exit_code']==0
route=load(O/'independent-route-before-graph105.native.json')
save('header-math-decision105.native.json',{'decision':'ACCEPT_PROSPECTIVE_MATHEMATICAL_HEADER','reviewer':'/root/exact_verifier96','header':info(O.parent/'Header105.lean'),'fresh_type_API_check':info(O/'fresh-type-api.receipt.json'),'independent_pregraph_route':info(O/'independent-route-before-graph105.native.json'),'assumption_audit':'Exactly original six analytic assumptions; paired genuine Hessian binder; no supplied process/probability/integrability/joint-count/normalizer premise.','literal_binding':'All actual93 lets through rho exactly match Header105 after line-ending normalization; one global Z and its joint measurability/arc/fallback/AE-zero clauses exactly match public93 expanded contract. R,Vy,nu and sectors match accepted104/103 contracts.','same_Z':'One public93 existential witness is retained before every y,r,T, used in both process identification and actual Q. No second producer process witness or arbitrary reversible law substitutes for it.','count_partition':'For each fixed z, all Nat fibers of N form an everywhere disjoint measurable partition of Omega. The93 fixed-count all-test identity already handles exceptional clocks via its AE proof; no common exceptional set across z is inferred.','parameter_measurability':'Measurable Gamma/rho and sigma-finite exact subtype volume make each prescribed sector integral measurable in z. This is what lintegral_tsum integrates; joint N measurability is unnecessary.','normalization_probability':'Public103 gives actual nu probability; UnitExponentialProduct gives literal P probability and SFinite P for Tonelli. Measurable actual endpoint pushforward gives Q probability independently of countable sum finiteness.','reversal':'Public104 gives the same J preserving every L_n; map_sum plus Q=sum L_n yields J preservation.','route':route['route'],'edge_cases':route['edge_cases'],'reuse':'Four existing public producers93/103/104/UnitExponentialProduct plus pinned Mathlib measure adapters. No separate95 dependency or external port required.','header_defects':[],'graph_readiness':'Original graph needs the separately recorded clock-probability-to-assembly edge before topology admission.','proof_implementation':False,'source_or_kernel_theorem_acceptance':False})
save('source-topology-decision105.original.native.json',{'decision':'REJECT_ORIGINAL_TOPOLOGY_MISSING_ONE_REQUIRED_EDGE','reviewer':'/root/exact_verifier96','creator':g['author'],'graph':info(S/'source-proof-graph-delta105.native.json'),'coverage':info(S/'source-coverage-delta105.native.json'),'binding_checks':[v for v in bound.values()],'effective_graph':dict(nodes=sorted(nodes),edges=[list(e) for e in sorted(edges)],topological_order=order,node_count=60,edge_count=111),'all21_primary_spans_verified':True,'missing_edge':{'source':'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws','target':'ASSEMBLY105','reason':'Selected Tonelli step on nu.prod P requires SFinite P. This is derived from actual clock probability before assembly; current edge only targets final ENDPOINT-LAW105 and is not an assembly ancestor. Fresh pinned lintegral_prod signature confirms the requirement.'},'other_topology_findings':['All55 inherited nodes and96 edges retained exactly; new14 producer edges and one future consumer incidence are acyclic.','COUNT93 is explicitly bound to public93; H99/D99 are source-context roots, not claims that recursion definitions alone imply a process law.','COUNT93 and MEASDENS93 are sibling projections from same public93 witness; no joint N assumption is inserted.','SECTOR-INTEGRAL-MEAS105 explicitly discharges SFinite m and joint Gamma/rho endpoint tests.','ENDPOINT-LAW105 combines exact sector reversal, actual countable identification and probability. AVG100 remains a future signed consumer, with INV100/L2A3/RESTART unresolved.'],'minimal_repair':'Add exactly UnitExponentialProduct -> ASSEMBLY105 with probability-to-SFinite-P contract, preserving header and existing route.','header_accepted':True,'proof_credit':False})
save('closed-RAW-original105.native.json',{'kind':'closed prospective header acceptance and original topology rejection','inputs':list(bound.values())+route['inputs'],'outputs':[info(p) for p in sorted(O.iterdir()) if p.is_file()],'no_proof_implementation':True,'no_shared_mutation':True,'no_new_full_primary_archive':True})
for n in ['header-math-decision105.native.json','source-topology-decision105.original.native.json','closed-RAW-original105.native.json']:print(n,info(O/n)['raw_sha256'])
