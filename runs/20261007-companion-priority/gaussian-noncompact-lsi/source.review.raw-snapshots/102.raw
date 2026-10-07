from pathlib import Path
import json,hashlib,datetime,re
O=Path(__file__).resolve().parent
R=O.parents[2]
def read(n):return json.loads((O/n).read_text(encoding='utf-8'))
def write(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
g=read('sourcegraph.base.json');nodes=g['nodes'];edges=g['edges'];sourceinputs=read('source-inputs.json')
def node(n,**k):nodes.append(dict(id=n,**k));return n
def edge(a,b,line,kind='authored-mathematical-ingredient'):
 edges.append(dict(id='edge:'+str(len(edges)+1),prerequisite=a,consumer=b,consumer_use_site=dict(source='authored-source-route',line_start=line,line_end=line),use_kind=kind,truth='source-dependency-only-no-compiled-edge'))
route=(O/'authored-source-route.md').read_text(encoding='utf-8').splitlines();route_loc={}
for n,l in enumerate(route,1):
 m=re.match(r'(R\d\d) (.+)',l)
 if not m:continue
 rid=m.group(1);route_loc[rid]=n
 kind='SOURCE_GAP' if rid in ['R05','R06','R07','R08','R09','R10','R11','R12','R13','R14','R15','R16','R18','R21','R22','R23','R24','R25'] else 'AUTHORED_SOURCE_STEP'
 node('route42:'+rid,kind=kind,formula_or_contract=m.group(2),source='authored-source-route',source_ranges=[[n,n]],
      provenance='authored sufficient route inferred from pinned primary/background, not printed SPHMC proof',
      obligation_status='unproved-in42' if kind=='SOURCE_GAP' else 'source-interface only')
target=node('target:GaussianLogSobolev42',kind='STATEMENT_SEALED_TARGET',source='Statement42',source_ranges=[[1,13]],
 statement_lf_sha256='ff9add5e7b7ce9ec01b1719574b8e80b843d3a469dd3026c6e40b831dab0a6ca',formal_truth='statement admission only; no42proof')
def es(a,b):edge(a,'route42:'+b,route_loc[b])
links={
 'R02':[],
 'R03':['route42:R02','source:MathlibL2:MemLp.integrable_sq','source:MathlibL2:memLp_two_iff_integrable_sq_norm'],
 'R04':['source:Cutoff:radialSmoothCutoff','source:Cutoff:radialSmoothCutoff_eq_one_of_norm_le','source:Cutoff:radialSmoothCutoff_mem_Icc','source:Cutoff:radialSmoothCutoff_contDiff','source:Cutoff:radialSmoothCutoff_hasCompactSupport','source:Cutoff:radialSmoothCutoff_fderiv_bound','source:Cutoff:radialSmoothCutoff_tendsto_one'],
 'R05':['route42:R01','route42:R02','route42:R04'],
 'R06':['route42:R04','route42:R05','source:MathlibProduct:fderiv_fun_mul','source:MathlibRiesz:toDual','source:MathlibGradient:gradient'],
 'R07':['route42:R04','route42:R06','source:MathlibGradient:Filter.EventuallyEq.gradient_eq'],
 'R08':['route42:R04','source:MathlibPhi:negMulLog_mul','source:MathlibPhi:negMulLog_eq_neg'],
 'R09':['route42:R04','source:MathlibPhi:self_sub_one_le_mul_log','source:MathlibPhi:negMulLog_nonneg'],
 'R10':['route42:R03','route42:R08','route42:R09'],
 'R11':['route42:R03','route42:R04','route42:R06'],
 'R12':['route42:R02','route42:R05','route42:R06','source:Gradient:continuous_gradient_of_contDiff_one','source:MathlibPhi:continuous_mul_log'],
 'R13':['route42:R03','route42:R04','route42:R12','source:MathlibDCT:tendsto_integral_of_dominated_convergence'],
 'R14':['route42:R08','route42:R10','route42:R12','source:MathlibPhi:continuous_mul_log','source:MathlibDCT:tendsto_integral_of_dominated_convergence'],
 'R15':['route42:R07','route42:R11','route42:R12','source:MathlibDCT:tendsto_integral_of_dominated_convergence'],
 'R16':['route42:R13','source:MathlibPhi:continuous_mul_log'],
 'R17':['route42:R05','parent:compact41-public'],
 'R18':['route42:R14','route42:R15','route42:R16','route42:R17','source:MathlibOrder:le_of_tendsto_of_tendsto'],
 'R20':['source:SLTcutoff:cutoff_product_rule','source:SLTcutoff:cutoff_gradient_error_bound','source:SLTcutoff:cutoff_gradient_extra_term','source:SLTcutoff:tendsto_cutoff_W12','source:SLToneDim:gaussian_logSobolev_W12_real','source:SLTtensor:gaussian_logSobolev_W12_pi'],
 'R21':['route42:R01','route42:R02','route42:R20'],
 'R22':['interface:actual32','interface:actual33'],
 'R23':[target,'route42:R22','interface:actual32','interface:actual33'],
 'R24':['route42:R23','primary:LSI-T2-invocation','primary:FIRST4.6'],
 'R25':['route42:R22','route42:R23','route42:R24']}
for b,aa in links.items():
 for a in aa:es(a,b)
application=node('application:actual32-domain-discharge',kind='CONSUMER_APPLICABILITY',source='authored-source-route',source_ranges=[[route_loc['R02'],route_loc['R02']]],
 statement='Actual32 produces42 domain premises for its posterior f; this is a downstream applicability fact, not a dependency needed for generic42 proof.')
edge('interface:actual32',application,route_loc['R02'],'consumer-domain-discharge')
edge('route42:R02',application,route_loc['R02'],'consumer-domain-discharge')
ids={n['id'] for n in nodes};assert len(ids)==len(nodes)
for e in edges:assert e['prerequisite'] in ids and e['consumer'] in ids,e
assert not any(e['consumer']==e['prerequisite'] for e in edges),'self edge'
routes=[dict(id='OR42:direct-C2-cutoff',logic='AND',parents=['route42:R01','route42:R02','route42:R18'],conclusion=target,
 source_use_site={'source':'authored-source-route','line_start':route_loc['R19'],'line_end':route_loc['R19']},
 obligation_status='chosen sufficient route, all SOURCE_GAPs must be internally proved; no proof credit'),
 dict(id='OR42:external-W12-mollification',logic='AND',parents=['route42:R20','route42:R21'],conclusion=target,
 source_use_site={'source':'authored-source-route','line_start':route_loc['R19'],'line_end':route_loc['R21']},
 obligation_status='alternative external-reference path, unresolved carrier/Sobolev adapter and imported/unexpanded providers; not callable local truth')]
coverage=read('source-coverage.json');cover=[c for c in coverage['entries'] if c['source'] not in ['authored-source-route','Statement42','SLTreusePolicy.current-append']];coverage['entries']=cover
for n,l in enumerate(route,1):
 m=re.match(r'(R\d\d) ',l)
 cover.append(dict(source='authored-source-route',line=n,disposition='NODE',node='route42:'+m.group(1)) if m else dict(source='authored-source-route',line=n,disposition='EXCLUDED',reason='authored route title/trivia'))
statement=(O/'Statement42.lf.snapshot').read_text(encoding='utf-8').splitlines()
for n in range(1,len(statement)+1):cover.append(dict(source='Statement42',line=n,disposition='NODE',node=target))
delta=read('policy-chronology.json')
for n in range(delta['current_append_lines'][0],delta['current_append_lines'][1]+1):cover.append(dict(source='SLTreusePolicy.current-append',line=n,disposition='EXCLUDED',reason='append-only administrative provenance/reuse status; not mathematical proof prerequisite'))
write('source-coverage.json',coverage)
actual=[]
for i in sourceinputs:
 if 'path' not in i:continue
 p=R/i['path']
 if not p.exists():continue
 b=p.read_bytes();lf=b.decode('utf-8').replace('\r\n','\n').replace('\r','\n').encode();raw=hashlib.sha256(b).hexdigest();lh=hashlib.sha256(lf).hexdigest()
 same=raw==i['raw_sha256'] and lh==i['lf_sha256'];policy=i['key']=='SLTreusePolicy'
 assert same or policy,(i['key'],'unexpected math input drift')
 actual.append(dict(source=i['key'],path=str(p),current_raw_sha256=raw,current_lf_sha256=lh,identical_to_historical_preread=same,mathematical_input=not i['key'].startswith(('SLTbackgroundRegistry','SLTreusePolicy','TechnicalPolicy')),policy_delta_record='policy-chronology.json' if policy else None))
write('current-input-bindings.json',dict(inputs=actual,historical_source_input_manifest='source-inputs.json',policy_only_delta=delta))
graph=dict(schema_version=1,schema='ASTIS-42-source-proof-graph-v1',creator='gaussian_noncompact_preread_42',
 status='independently-reconstructed-source-only-awaiting-distinct-topology-review',
 target=target,source_priorities=['primary2609.06906v1','exact691StatementSeal','public32/33/compact41','pinnedcanonical/Mathlib/SLTbackground'],
 nodes=nodes,edges=edges,alternative_routes=routes,root_route_logic='OR(direct-C2-cutoff, external-W12-mollification); never flatten into one AND',
 compiled_edges=[],no42implementation_input=True,source_coverage_file='source-coverage.json',named_use_inventory_file='named-use-inventory.json',
 qualified_api_resolution_file='qualified-api-resolution.json',scope_and_gaps_file='authored-source-route.md',
 pending=['distinct topology acceptance before proof','all authored SOURCE_GAP internal proofs','same33 witness consumer','GaussianT2/FIRST4.6/main/error/cost/reader/PURIFIED'])
write('sourcegraph.json',graph)
source_detail=read('SourceDetail42.lf.snapshot')
contract=dict(schema_version=1,creator=graph['creator'],status='SOURCE_GRAPH_AUTHOR_NOT_SELFVALIDATED',
 exact691signature_sha256=graph['nodes'][-26]['id'] if False else 'ff9add5e7b7ce9ec01b1719574b8e80b843d3a469dd3026c6e40b831dab0a6ca',
 source_first_exposure=source_detail['exposure'],primary='2609.06906v1 S4.E6/S4.SS1.p4.3',
 source_before_candidate_preread_sha256=hashlib.sha256((O/'SourceDetail42.raw.snapshot').read_bytes()).hexdigest(),
 statement_seal_sha256=sha(O/'StatementSeal42.raw.snapshot'),
 objects='actual finite realHilbert stdGaussian law, signed C2 f, actual global gradient',
 domains='C2/fL2/truegradientL2/PhiL1 are true background domains supplied by actual32; not new paper assumptions',
 internal_obligations='cutoff regularity, measurability, zeroaware entropy domination, true gradient calculus and actual mass/Phi/energy limits are dependency edges, not binders',
 constants='exact2; no dimension bound; internal C/R with C chosen before R; future same32/33energy factor1/4 yields futureKL factor1/2',
 endpoints='rank0 signed f f=0 chi=0 zero mass included; no massdivision/logdifferentiation',
 attribution='authored sufficient C2 source route for omitted primary GaussianLSI; distinct from upstream W12/tower/mollification/Fatou source and printed FIRST',
 alternatives=routes,API_identifier_boundary='All asserted identities have pinned source declaration locators and lexical namespace checks. Ambiguous methods/aliases/generated names remain exact source-token externalunexpanded, not asserted elaborated QNames.',
 theorem_approval=False,topology_selfvalidation=False,compiler_run=False,proof_search=False,current_policy_delta='policy-chronology.json; old exactprefix preserved; current append is administrative not mathematics')
write('sourcecontract.json',contract)
# Structural consistency only: not mathematical/topology admission.
expected={(i['key'],n) for i in sourceinputs for a,b in i['ranges'] for n in range(a,b+1)}
seen={};
for c in cover:
 t=(c['source'],c['line']);assert t not in seen,t;seen[t]=c
 assert c['disposition']=='EXCLUDED' and c.get('reason') or c['disposition']=='NODE' and c.get('node') in ids,c
assert expected.issubset(seen)
uses=read('named-use-inventory.json')['entries']
named=sum(u['disposition'] in ['named-use-edge','named-use-edge-unelaborated-token','opaque-source-token-edge'] for u in uses)
sourceedges=sum(e['use_kind'] in ['direct-named-source-use','direct-named-source-use-unelaborated','opaque-source-token-use'] for e in edges)
assert named==sourceedges
checks=dict(status='STRUCTURAL_CHECKS_ONLY_NOT_TOPOLOGY_VALIDATION',node_count=len(nodes),edge_count=len(edges),OR_route_count=len(routes),
 provider_count=len(g['providers']),selected_physical_lines=len(expected),partition_rows=len(cover),no_duplicate_partition=True,all_selected_lines_partitioned=True,
 named_source_use_occurrences=named,named_source_use_edges=sourceedges,compiled_edges=0,unexpected_mathematical_input_drift=False,policy_delta_separate=True)
write('structural-check.json',checks)
lease=read('lease.open.json') if (O/'lease.open.json').exists() else read('lease.json')
if (O/'lease.open.json').exists():(O/'lease.open.json').rename(O/'lease.initial.raw.snapshot.json')
lease.update(state='CLOSED',closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),outcome='sourcegraph reconstructed, awaiting distinct topology admission',
 sourcegraph_sha256=sha(O/'sourcegraph.json'),sourcecontract_sha256=sha(O/'sourcecontract.json'),compiler_run=False,topology_selfvalidation=False)
write('lease.json',lease)
art=['sourcegraph.json','source-coverage.json','named-use-inventory.json','qualified-api-resolution.json','source-inputs.json','current-input-bindings.json','sourcecontract.json','structural-check.json','policy-chronology.json','authored-source-route.md','lease.json']
write('sourcegraph-run.json',dict(creator=graph['creator'],status='sourcegraph-author-run-closed-no-selfvalidation',artifacts=[dict(path=str(O/n),raw_sha256=sha(O/n)) for n in art],
                                real_lease_state='CLOSED',no42body_test_lesson_blind_compiler_or_canonical_edits=True))
print(json.dumps(checks));print('graph_sha256',sha(O/'sourcegraph.json'));print('run_sha256',sha(O/'sourcegraph-run.json'))
