from pathlib import Path
import json,hashlib,copy,gzip
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;D=O.parent/'source-graph-repair105'
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bound={}
def refs(v):
 if isinstance(v,dict):
  if 'path' in v and 'raw_sha256' in v:
   p=R/v['path'];assert sha(p.read_bytes())==v['raw_sha256'];bound[v['path']]=info(p)
  for x in v.values():refs(x)
 elif isinstance(v,list):
  for x in v:refs(x)
expected={'repair-proposal105.native.json':'2022d7fc96578a4b3f90984fdf5e751e63aff850141475b12824c96b80722749','source-proof-graph-delta105.v2.native.json':'97fc1255c8a70c879070734d36d72db785c73d6c5b7bf73a3b284351c70e5bc9','source-coverage-repair105.native.json':'756ca5cbafb68c1d8800c181aae0364fbafb98a41e3c80fa7919aaba8f85683e','closed-RAW-graph-repair105.native.json':'af7de22bed75d62b93bdcc8de80314ec66e5c44840331242bcc680e1b7e3a0f9'}
for n,h in expected.items():
 p=D/n;assert sha(p.read_bytes())==h;refs(load(p));bound[info(p)['path']]=info(p)
for p in D.glob('*.gz'):assert gzip.decompress(p.read_bytes())==Path(str(p).removesuffix('.raw.gz')).read_bytes();bound[info(p)['path']]=info(p)
proposal=load(D/'repair-proposal105.native.json');old=load(R/proposal['original_graph']['path']);v2=load(D/'source-proof-graph-delta105.v2.native.json');want=copy.deepcopy(old)
u='AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws';group=next(x for x in want['AND_dependency_groups'] if x['target']=='ASSEMBLY105');assert u not in group['parents'];group['parents'].append(u)
edit=proposal['exact_edits'][2];assert group['mechanism']==edit['before'];group['mechanism']=edit['after']
edge=dict(source=u,target='ASSEMBLY105',logic='AND',certified_Lean_edge=False);assert edge not in want['producer_edges'];want['producer_edges'].append(edge);assert want==v2
original=load(O/'source-topology-decision105.original.native.json');eff=original['effective_graph'];nodes=set(eff['nodes']);edges={tuple(x) for x in eff['edges']};assert (u,'ASSEMBLY105') not in edges;edges.add((u,'ASSEMBLY105'))
assert (len(nodes),len(edges))==(60,112)
todo=set(nodes);order=[]
while todo:
 ready=sorted(n for n in todo if not any(b==n and a in todo for a,b in edges));assert ready,'cycle';todo.difference_update(ready);order+=ready
oldclosure=load(O/'closed-RAW-original105.native.json')
for x in oldclosure['inputs']+oldclosure['outputs']:
 p=R/x['path'];assert sha(p.read_bytes())==x['raw_sha256']
save('source-topology-admission105.native.json',{
 'decision':'ACCEPT_BASE_PLUS_V2_TOPOLOGY_AND_COVERAGE','reviewer':'/root/exact_verifier96','creator':'/root/source_final96',
 'mode':'Independent noncreator validation; original mathematical reconstruction frozen before105 creator graph was read. Earlier inherited context known. This repair validation is not a second blind reconstruction.',
 'header':info(O.parent/'Header105.lean'),'positive_header_decision':info(O/'header-math-decision105.native.json'),'original_negative':info(O/'source-topology-decision105.original.native.json'),'original_closure':info(O/'closed-RAW-original105.native.json'),
 'proposal':info(D/'repair-proposal105.native.json'),'v2_graph':info(D/'source-proof-graph-delta105.v2.native.json'),'coverage_overlay':info(D/'source-coverage-repair105.native.json'),'creator_repair_closure':info(D/'closed-RAW-graph-repair105.native.json'),
 'exact_delta':'Only append existing UnitExponentialProduct identity to ASSEMBLY105 AND parents, append its corresponding edge, append the stated probability-to-SFinite-P mechanism sentence. No node/header/other-edge/source-slice change.',
 'effective_graph':{'node_count':60,'edge_count':112,'nodes':sorted(nodes),'edges':[list(e) for e in sorted(edges)],'topological_order':order},
 'coverage':{'source_regions':21,'base_nodes':55,'base_edges':96,'new_nodes':5,'new_producer_edges':15,'future_consumer_edges':1,'missing_required_edges':[]},
 'mathematical_admission':'Clock probability is established before Tonelli, supplying SFinite P for the actual nu.prod P measure. Other regularity and witness contracts remain as independently reviewed; no joint-in-z N premise or new source hypothesis appears.',
 'execution_order_clarification':'The independent pregraph route grouped probability at step6; its clock-probability substep must be available before step5 Tonelli. The creator seven-step route already puts both probability instances at step2. This is scheduling of existing proof ingredients, not a mathematical route or statement change.',
 'ready_route':[
 'Take the single global actual93 Z and retain all identification clauses; derive the actual M endpoint map measurability.',
 'Use103 and UnitExponentialProduct for actual nu/P probabilities and clock SFinite P; obtain Q probability from measurable pushforward.',
 'For fixed z, measurable Nat fibers partition all clocks;93 endpoint tests give each exact prescribed sector integral.',
 'Derive SFinite m from the literal measurable simplex; joint Gamma/rho gives measurable sector integrals in initial z.',
 'Tonelli and nonnegative lintegral_tsum identify integrals against Q and sum L_n; apply measure extensionality.',
 'Apply104 for each literal normalized endpoint sector and the same globally measurable flipped swap J.',
 'Use map_sum and Q=sum L_n to obtain preservation by J; package all three conclusions for the same actual Z.'
 ],
 'source_boundary':'Countable nonnegative actual endpoint-law assembly selected. Signed bounded bilinear AVG100, marginal INV100, L2, restart/Markov/semigroup and costs remain separate.',
 'all_old_RAW_preserved':True,'new_proof_implementation':False,'certified_new_Lean_edges':False,'VERIFIED_or_claim_or_seal':False,'defects':[]})
save('closed-RAW-review105.native.json',{'kind':'closed prospective header and corrected topology acceptance','reviewer':'/root/exact_verifier96','original_closure':info(O/'closed-RAW-original105.native.json'),'repair_inputs':list(bound.values()),'outputs':[info(p) for p in sorted(O.iterdir()) if p.is_file()],'no_shared_mutation':True,'no_proof_implementation':True,'no_new_primary_archive':True})
for n in ['source-topology-admission105.native.json','closed-RAW-review105.native.json']:print(n,info(O/n)['raw_sha256'])
