# -*- coding: utf-8 -*-
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,json,sys,datetime
sys.stdout.reconfigure(encoding='utf-8')
BASE=Path('E:/Samplinglib/runs/20261007-companion-priority')
SRC=BASE/'pbps-outer-gradient-sourcegraph49'
NEG=BASE/'pbps-outer-gradient-source-topology-review49'
OUT=BASE/'pbps-outer-gradient-topology-overlay49'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def blob(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def write(name,v): (OUT/name).write_bytes(blob(v))
def read(p): return json.loads(p.read_text(encoding='utf-8'))
bindings=[]
def pin(p,label,role):
 b=p.read_bytes(); n=lf(b)
 (OUT/(label+'.raw')).write_bytes(b);(OUT/(label+'.lf')).write_bytes(n)
 bindings.append(dict(id=label,path=str(p),role=role,raw_sha256=sha(b),lf_sha256=sha(n),raw_bytes=len(b),lf_bytes=len(n),raw_snapshot=label+'.raw',lf_snapshot=label+'.lf'))
 return b
before_files=['source-proof-graph.json','source-coverage.json','caller-inventory.json','selected-token-inventory.json','selected-providers.json','input-bindings.json','primary-balanced-inventory.json','hypothesis-contract.json','sourcecontract.json','source-before-candidate.contract.json','schema-and-boundary.md','capsule.md','run.json','lease.json']
for n in before_files: pin(SRC/n,'original-'+n,'immutable original creator packet, not retrospectively admitted')
negraw=pin(NEG/'source-topology-review.json','negative-source-topology-review.json','independent CLOSED blocking receipt, retained unchanged')
assert sha(negraw)=='73497919a8693a4e8e2b36bf9f66a20af9fc006f94becbd7cc185270f581f417'
checkraw=pin(NEG/'direct-call.checks.json','negative-direct-call.checks.json','exact T1/T2 independent coordinate findings')
pin(NEG/'reviewer.topology.lease.json','negative-reviewer.topology.lease.json','original independent CLOSED reviewer leases')
target=BASE/'pbps-outer-gradient-preproof49/prospective-statement.txt'
t=pin(target,'target-prospective-statement.txt','unchanged exact target; no49proof or binder alteration')
assert len(lf(t))==1795 and sha(lf(t))=='f37b4a07e62e16d22f4ecbc1fba9c38fd80d42f947011b38ded7c5153e0bea1d'
pin(OUT/'lease.json','overlay-opening-lease.json','actual read/write/Python OPEN before overlay reads, compiler CLOSED unused')
providers=read(SRC/'selected-providers.json')
provider_lookup={p['id']:p for p in providers}
current_hash_checks=[]
for p in providers:
 # Raw-byte hashing is not semantic proof-body inspection; selected public prefixes only are expanded.
 current=Path(p['path']).read_bytes()
 assert sha(current)==p['whole_raw_sha256'],p['id']
 assert sha(lf(current))==p['whole_lf_sha256'],p['id']
 current_hash_checks.append(dict(id=p['id'],path=p['path'],raw_sha256=sha(current),lf_sha256=sha(lf(current)),semantic_scope=p['selection_scope'] if 'selection_scope' in p else 'same original selected fragment'))
 for suffix in ['raw','lf']:
  raw=pin(SRC/(p['snapshot']+'.'+suffix),'selected-'+p['id']+'.'+suffix,'original exact selected provider fragment; no new mathematical body selection')
  assert sha(raw)==p['fragment_'+suffix+'_sha256'],p['id']
primary=Path('E:/Samplinglib/runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html')
pb=primary.read_bytes();assert sha(pb)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
# Only the existing selected physical row needed by T3 is expanded here.
row4574=pb.splitlines(keepends=True)[4573]
pin(SRC/'selected-P.fderiv-context2.raw','incidental-fderiv-context2-exact.raw','same raw fragment, unrelated theorem/proof361-368 EXCLUDED')
(OUT/'primary-row4574.raw').write_bytes(row4574);(OUT/'primary-row4574.lf').write_bytes(lf(row4574))
bindings.append(dict(id='primary-row4574',path=str(primary),role='existing selected B.13 target/compact reduction boundary',whole_raw_sha256=sha(pb),whole_lf_sha256=sha(lf(pb)),whole_raw_bytes=len(pb),physical_line1=4574,fragment_raw_sha256=sha(row4574),fragment_lf_sha256=sha(lf(row4574)),raw_snapshot='primary-row4574.raw',lf_snapshot='primary-row4574.lf'))
g0=read(SRC/'source-proof-graph.json');c0=read(SRC/'source-coverage.json');i0=read(SRC/'caller-inventory.json');tok0=read(SRC/'selected-token-inventory.json')
g,c,inv,tok,prov=map(deepcopy,[g0,c0,i0,tok0,providers])
assert len(g['nodes'])==78 and len(g['edges'])==280
operations=[]
def replace(container,key,value,file,pointer,reason):
 old=deepcopy(container[key]);container[key]=value
 operations.append(dict(op='replace',file=file,path=pointer,before=old,after=deepcopy(value),repair=reason))
def add(container,key,value,file,pointer,reason):
 assert key not in container
 container[key]=value;operations.append(dict(op='add',file=file,path=pointer,after=deepcopy(value),repair=reason))
# T1: preserve source bytes and edge endpoints, explicitly exclude unrelated theorem/proof.
e=deepcopy(g['edges'][244]);assert e['caller']['line1']==364 and e['caller']['byte_interval0']==[20319,20325]
e.update(relation='excluded-incidental-fragment-reference',classification='EXCLUDED-incidental-unrelated-theorem-reference',included_in_mathematical_prerequisites=False,semantic_role='Raw byte reference retained as exposure boundary; not a typing prerequisite or49proof call',repair_id='T1')
replace(g['edges'],244,e,'source-proof-graph.after.json','/edges/244','T1 one-based edge245, preserve exact raw caller and endpoints, remove mathematical dependency status')
for ix,r in enumerate(c['rows']):
 if r['path'].endswith('FDeriv\\Measurable.lean') and 361<=r['physical_line1']<=368:
  n=deepcopy(r);n.update(classification='EXCLUDED',node_ids=[],reason='T1 incidental unrelated measurableSet_of_differentiableAt_of_isComplete theorem/comment/proof; exact raw bytes retained, no typing or mathematical prerequisite',incidental_raw_exposure=True,semantic_proof_expansion=False,repair_id='T1')
  replace(c['rows'],ix,n,'source-coverage.after.json','/rows/'+str(ix),'T1 physical361-368 excluded, no raw fragment change')
assert sum(o['file']=='source-coverage.after.json' for o in operations)==8
for data,name in [(inv,'caller-inventory.after.json'),(tok,'selected-token-inventory.after.json')]:
 for ix,x in enumerate(data['entries']):
  if x.get('caller_selected_provider')=='selected-P.fderiv-context2' and x.get('caller_physical_line1')==364:
   n=deepcopy(x);n.update(classification='EXCLUDED-incidental-fragment-reference',active_semantic_dependency=False,raw_fragment_contains_unrelated_proof=True,semantic_proof_expansion=False,repair_id='T1')
   replace(data['entries'],ix,n,name,'/entries/'+str(ix),'T1 raw fderiv/DifferentiableAt occurrences retained as excluded exposure; no typing self-loop')
replace(inv,'provider_mathematical_proof_bodies_selected',1,'caller-inventory.after.json','/provider_mathematical_proof_bodies_selected','T1 correct original zero count: one unrelated proof is physically in raw selected context')
add(inv,'provider_mathematical_proof_bodies_selected_count_scope','raw selected bytes, includes one unrelated EXCLUDED fragment; zero semantic proof expansion','caller-inventory.after.json','/provider_mathematical_proof_bodies_selected_count_scope','T1 distinguish physical exposure from semantic proof selection')
add(inv,'provider_mathematical_proof_bodies_semantically_expanded',0,'caller-inventory.after.json','/provider_mathematical_proof_bodies_semantically_expanded','T1 excluded proof is not a proof ingredient')
for ix,p in enumerate(prov):
 if p['id']=='selected-P.fderiv-context2':
  n=deepcopy(p);n.update(kind='typing-context-with-incidental-excluded-unrelated-proof',selection_scope='Exact original raw358-370 retained;361-368 unrelated theorem/proof EXCLUDED,358-359/370 typing remains NODE; blanks EXCLUDED',raw_mathematical_proof_exposure_count=1,semantic_proof_expansion_count=0,excluded_physical_lines1=[361,368],repair_id='T1')
  replace(prov,ix,n,'selected-providers.after.json','/'+str(ix),'T1 accurate provider semantic selection without changing fragment/hash/range')
# T3: line4574 is genuine source mathematics and a reduction/target boundary, not layout.
for ix,r in enumerate(c['rows']):
 if r['path']==str(primary).replace('/','\\') and r['physical_line1']==4574:
  n=deepcopy(r);n.update(classification='NODE',node_ids=['S.compact','R.rough','R.operator'],reason='T3 printed B.13 target citation and It suffices compact-smooth reduction; all-L2/H1 closure and operator adapters remain typed outside-target boundaries, not assumed or proved',repair_id='T3')
  replace(c['rows'],ix,n,'source-coverage.after.json','/rows/'+str(ix),'T3 genuine mathematics in A3.SS1.p1.1, not HTML layout')
assert sum(o['file']=='source-coverage.after.json' for o in operations)==9
for ix in [252,253,254]:
 old=g['edges'][ix];assert old['caller']['line1']==4574 and old['reference']=='A2.E13'
 n=deepcopy(old);n.update(relation='printed-source-target-and-compact-reduction-boundary-reference',classification='source-mathematical-target-reduction-boundary',included_in_mathematical_prerequisites=False,semantic_role='B.13 names the broader target; compact-smooth proof reduction does not supply the rough-domain or operator adapter as a proved premise',repair_id='T3')
 replace(g['edges'],ix,n,'source-proof-graph.after.json','/edges/'+str(ix),'T3 one-based edges253-255 keep exact source/reference/endpoints, honest target boundary semantics')
# T2: exactly the sixteen independently identified references; original provider scope unchanged.
missing=json.loads(checkraw.decode('utf-8'))['missing_public_contract_references'];assert len(missing)==16
nodes={n['id']:n for n in g['nodes']}
byte_checks=[]
for k,m in enumerate(missing):
 p=provider_lookup[m['provider_id']];b=Path(m['path']).read_bytes();a,z=m['byte_interval0'];assert b[a:z].decode('utf-8')==m['token']
 assert p['start_utf8_byte0']<=a<z<=p['end_utf8_byte0_exclusive']
 line1=b[:a].count(b'\n')+1;assert line1==m['physical_line1']
 linestart=b.rfind(b'\n',0,a)+1;column=len(b[linestart:a].decode('utf-8'))
 fromnode=m['from_node'];tonode=m['to_node'];assert fromnode!=tonode
 entry=dict(caller_selected_provider=m['provider_id'],caller_node=tonode,caller_path=m['path'],caller_physical_line1=line1,caller_column0_unicode=column,caller_start_utf8_byte0=a,caller_end_utf8_byte0_exclusive=z,token=m['token'],resolved_node=fromnode,classification=m['kind'],compiled49caller=False,provider_body_selected=False,active_semantic_dependency=True,reference_semantics='typing/public contract reference, not an implementation invocation',repair_id='T2',negative_missing_reference_index0=k)
 if 'qualified_id' in nodes[fromnode]: entry['qualified_id']=nodes[fromnode]['qualified_id']
 else: entry['resolved_family']=nodes[fromnode]['notation_or_family_id'];entry['exact_type_token']=m['token']
 if m['token']=='μ[X': entry['notation_semantics']='Expectation notation μ[X...] is integral under μ; exact recorded prefix bytes are not a declaration name'
 for data,name in [(inv,'caller-inventory.after.json'),(tok,'selected-token-inventory.after.json')]:
  ix=len(data['entries']);data['entries'].append(deepcopy(entry));operations.append(dict(op='add',file=name,path='/entries/'+str(ix),after=deepcopy(entry),repair='T2 missing selected public/typing reference '+str(k)))
 edge=dict(from_node=fromnode,to_node=tonode,relation='selected-public-contract-typing-reference' if m['kind']=='typing-reference' else 'selected-public-contract-mathematical-reference',caller=dict(path=m['path'],line1=line1,byte_interval0=[a,z],provider_id=m['provider_id']),classification=m['kind'],included_in_mathematical_prerequisites=True,not_implementation_call=True,repair_id='T2',negative_missing_reference_index0=k)
 ix=len(g['edges']);g['edges'].append(edge);operations.append(dict(op='add',file='source-proof-graph.after.json',path='/edges/'+str(ix),after=deepcopy(edge),repair='T2 exact selected public/typing ingredient '+str(k)))
 byte_checks.append(dict(index0=k,provider=m['provider_id'],path=m['path'],byte_interval0=[a,z],physical_line1=line1,token=m['token'],selected_fragment_contains_exact_bytes=True,current_raw_sha256=sha(b),current_lf_sha256=sha(lf(b)),not_implementation_call=True))
assert g['nodes']==g0['nodes']
changed=[j for j in range(280) if g['edges'][j]!=g0['edges'][j]];assert changed==[244,252,253,254]
assert len(g['edges'])==296 and len(inv['entries'])==167 and len(tok['entries'])==160
counts=Counter(r['classification'] for r in c['rows']);assert counts==dict(NODE=146,EXCLUDED=83)
assert len(c['rows'])==229
assert all(c['rows'][j]['physical_line_raw_sha256']==c0['rows'][j]['physical_line_raw_sha256'] for j in range(229))
assert g['schema_version']==g0['schema_version'] and g['status']==g0['status']
write('source-proof-graph.after.json',g);write('source-coverage.after.json',c);write('caller-inventory.after.json',inv);write('selected-token-inventory.after.json',tok);write('selected-providers.after.json',prov)
schema=(SRC/'schema-and-boundary.md').read_text(encoding='utf-8')
schema=schema.replace('Mathematical proof bodies selected: zero.','Physical raw selected bytes contain one unrelated Mathlib theorem/proof at361-368, retained unchanged and explicitly EXCLUDED; semantic provider proof expansion is zero. The original zero-body exposure statement is corrected by T1, not erased from the preserved original.')
schema += '\nThis representation-only overlay preserves all78 node records and the original280 edge positions; only edges245/253-255 change classification/role fields, and16 exact missing public/typing references are appended. Edge245 is an excluded raw-exposure boundary. Edges253-255 record the B.13 target and compact proof reduction, not rough/operator prerequisites. The physical selected-row partition is229 rows:146 NODE/83 EXCLUDED. Named reference totals include excluded occurrences:167 callers/160 configured tokens, of which two in each inventory are excluded T1 exposures. No mathematical statement, assumption, source route, primitive contract or proof is added. Distinct review is pending.\n'
(OUT/'schema-and-boundary.after.md').write_bytes(schema.encode('utf-8'))
write('input-bindings.json',bindings);write('current-selected-input-hash-checks.json',current_hash_checks);write('exact-reference-byte-checks.json',byte_checks)
write('overlay-delta.json',dict(schema_version='representation-repair-overlay49-v1',status='CREATOR_OVERLAY_AWAITING_DISTINCT_REVIEW',original_graph_raw_sha256=sha((SRC/'source-proof-graph.json').read_bytes()),original_negative_raw_sha256=sha(negraw),operations=operations,index_convention='JSON pointers/array indices zero based; review edge numbers one based; UTF8 intervals zero based end exclusive; physical source lines one based',unchanged_nodes=78,unchanged_original_edge_positions=276,reviewed_changed_original_edge_positions0=changed,appended_edges=16,mathematical_statement_delta=[],public_assumption_delta=[],compiler_used=False,self_admission=False))
write('creator-structural-checks.json',dict(status='MECHANICAL_COORDINATE_AND_PREFIX_CHECKS_ONLY_NOT_TOPOLOGY_ADMISSION',nodes_equal=True,original_edge_prefix_equal_except_reviewed_positions0=changed,coverage_rows=229,coverage_counts=dict(counts),raw_line_hashes_unchanged=True,original_provider_count=len(providers),selected_fragments_unchanged=True,exact_missing_reference_byte_checks=16,caller_entries=167,token_entries=160,excluded_caller_entries=2,excluded_token_entries=2,total_edges=296,excluded_incidental_edge_count=1,source_target_boundary_edge_count=3,remaining_edges=292,all_actual_selected_whole_inputs_match_original_raw_lf=True,original_negative_preserved=True,source_uncertainty='No new mathematical uncertainty resolved; original topology negative remains the historical receipt. Overlay awaits distinct reviewer.'))
write('sourcecontract.json',dict(schema_version='source-representation-overlay49-v1',status='CREATOR_ONLY_DISTINCT_REVIEW_REQUIRED',negative_original_sha256=sha(negraw),target_lf_bytes=1795,target_lf_sha256=sha(lf(t)),scope='Only T1-T3 representation repairs requested by root after independently CLOSED negative topology review',mathematical_source_route_unchanged=True,source_hypotheses_unchanged=True,all_originals_preserved=True,body49_exists_or_read=False,compiler_used=False,known_exposures=['Prior48 body/wholeproof review was authorized and remains disclosed; this is not a fresh blind role.','Exact original FDeriv Measurable358-370 raw fragment physically contains unrelated theorem/proof361-368. Those bytes remain pinned and EXCLUDED.','Negative topology receipt/direct-call report and original graph metadata are authorized repair inputs; no49 proof/Tests/review body is read.'],boundaries=['B.13 full all-L2 to weighted H1 compact density/outer closed gradient extension remains outside49.','Literal P/U/A/B/Gamma operator adapters remain outside scalar outer variance defect target.','Fiber D_y is not outer gradient domain.','No C.3 coercivity, half-turn subsectionC.2, paper main or cost claim.'],no_self_topology_admission=True))
capsule='''# Minimal representation overlay49 — distinct review pending

The overlay repairs exactly T1–T3 from the CLOSED negative topology receipt. It preserves the original graph, inventories, capsule and negative receipt byte for byte. The1795-LF statement, public assumptions,78 node records and mathematical route remain unchanged. No49 implementation, compiler, proof search or claim occurred.

T1 retains the original FDeriv/Measurable358–370 raw fragment. Its unrelated theorem/comment/proof361–368 is explicitly EXCLUDED. The fderiv and DifferentiableAt references at364 remain recorded as incidental exposure, with no typing self-loop. One-based edge245 retains its original caller bytes/endpoints but becomes an excluded exposure boundary. Raw proof exposure is one; semantic proof expansion is zero. The original false zero-exposure field remains visible in the preserved before packet.

T2 appends exactly the16 independently identified byte references: mean integral; map/probability; compact support; Mathlib variance/expectation; five finite-Hilbert/Borel typing tokens in each of the Gibbs and GaussianReflection parent contexts. These are references within already selected public contracts, not invented49 implementation calls. Each exact byte interval, line and selected-fragment containment is checked and pinned. No new producer or certificate premise is introduced.

T3 classifies primary4574 as a genuine B.13 target/compact-reduction boundary. Existing one-based edges253–255 keep their source coordinates and references while recording that role. They do not use full rough-domain H1 or operator adapters as proved prerequisites. Those residuals remain outside this signed compact49 ingredient.

After counts:78 nodes;296 edge records (original280 positions retained, four explicitly reclassified,16 appended);229 physical rows partitioned146 NODE/83 EXCLUDED;167 caller records and160 configured token records, each including two excluded T1 occurrences. The graph has one excluded exposure edge and three mathematical target/reduction-boundary records;292 other records remain. Coverage is exhaustive only within the unchanged selected-source union, not the whole library or paper.

`overlay-delta.json` lists exact before/after JSON-pointer operations. `creator-structural-checks.json` reports mechanical prefix/byte/count checks; it is not topology admission. The negative original SHA73497919a8693a4e8e2b36bf9f66a20af9fc006f94becbd7cc185270f581f417 remains immutable. Distinct overlay review is required before root proof work.

The chosen SAME R/S disintegration/reflection route and real probability/L2/L1/gradient/variance outputs are unchanged. Full B.13 rough closure and operator adapters remain typed residuals; fiber D_y does not supply the outer gradient domain. Prior authorized48 body exposure and the incidental unrelated Mathlib proof exposure are disclosed in `sourcecontract.json`.
'''
(OUT/'capsule.md').write_bytes(capsule.encode('utf-8'))
print(json.dumps(dict(status='OVERLAY_WRITTEN_LEASES_STILL_OPEN',counts=dict(counts),nodes=78,edges=296,callers=167,tokens=160,operations=len(operations),bindings=len(bindings)),ensure_ascii=False))
