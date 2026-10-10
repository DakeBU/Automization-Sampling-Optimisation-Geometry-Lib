import json, hashlib, copy
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
B=Path('E:/Samplinglib'); P=B/'runs/20261007-companion-priority'
R=P/'pbps-outer-gradient-topology-overlay49'; A=P/'pbps-outer-gradient-sourcegraph49'; O=P/'pbps-outer-gradient-source-topology-review49'
def h(b): return hashlib.sha256(b).hexdigest()
def oldlf(b): return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def j(p): return json.loads(p.read_text(encoding='utf-8'))
def cj(d): return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def put(p,d):
 assert not p.exists();p.write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 b=p.read_bytes();return {'path':p.as_posix(),'raw_sha256':h(b),'lf_sha256':h(b.replace(b'\r\n',b'\n')),'bytes':len(b),'reviewer_lf_recipe':'replace CRLF with LF; isolated CR preserved'}
negative=j(O/'source-topology-review.json');assert h((O/'source-topology-review.json').read_bytes())=='73497919a8693a4e8e2b36bf9f66a20af9fc006f94becbd7cc185270f581f417'
original=j(A/'source-proof-graph.json');g=j(R/'source-proof-graph.after.json');delta=j(R/'overlay-delta.json');run=j(R/'run.json')
assert h((R/'run.json').read_bytes())=='f4758a87e0a803ef548d429544a6b08ea9667459d88a53932bc5fdff12c10ce0'
assert h((R/'lease.json').read_bytes())=='69e5014517ed58a8a9b677aeb88d673e14ed72615c4238604e1a498665d0c45e'
assert all(j(R/'lease.json')[k]=='CLOSED' for k in ['status','read','write','python','compiler'])
assert run['expected_closed_lease_sha256']==h((R/'lease.json').read_bytes())
for name,desc in run['output_files'].items():
 b=(R/name).read_bytes();assert h(b)==desc['raw_sha256'] and h(oldlf(b))==desc['lf_sha256'],name
assert {k:v for k,v in g.items() if k!='edges'}=={k:v for k,v in original.items() if k!='edges'}
assert len(g['nodes'])==78 and len(g['edges'])==296
changed=[i for i in range(280) if g['edges'][i]!=original['edges'][i]];assert changed==[244,252,253,254]
for i in changed:
 for k in ['from_node','to_node','caller']:
  assert g['edges'][i][k]==original['edges'][i][k]
assert g['edges'][244]['included_in_mathematical_prerequisites'] is False
for i in [252,253,254]:assert g['edges'][i]['included_in_mathematical_prerequisites'] is False
# Independently apply the exact declared JSON overlay; no undeclared mutation allowed.
files={n.replace('.after',''):j(A/n.replace('.after','')) for n in set(x['file'] for x in delta['operations'])}
for op in delta['operations']:
 key=op['file'].replace('.after','');d=files[key]; parts=op['path'].lstrip('/').split('/');parent=d
 for part in parts[:-1]:parent=parent[int(part)] if isinstance(parent,list) else parent[part]
 last=parts[-1];ix=int(last) if isinstance(parent,list) else last
 if op['op']=='replace':assert parent[ix]==op['before'];parent[ix]=copy.deepcopy(op['after'])
 elif op['op']=='add':
  if isinstance(parent,list):assert ix==len(parent);parent.append(copy.deepcopy(op['after']))
  else:assert ix not in parent;parent[ix]=copy.deepcopy(op['after'])
 else:raise AssertionError(op)
for name,d in files.items():assert d==j(R/name.replace('.json','.after.json'))
missing=j(O/'direct-call.checks.json')['missing_public_contract_references']
ci=j(R/'caller-inventory.after.json');ti=j(R/'selected-token-inventory.after.json');providers=j(R/'selected-providers.after.json')
assert len(ci['entries'])==167 and len(ti['entries'])==160
assert ci['provider_mathematical_proof_bodies_selected']==1 and ci['provider_mathematical_proof_bodies_semantically_expanded']==0
assert len(ci['entries'][151:])==len(ti['entries'][144:])==len(missing)==16
for i,m in enumerate(missing):
 e=g['edges'][280+i];c=ci['entries'][151+i];t=ti['entries'][144+i]
 assert e['negative_missing_reference_index0']==c['negative_missing_reference_index0']==t['negative_missing_reference_index0']==i
 assert e['from_node']==c['resolved_node']==m['from_node'] and e['to_node']==c['caller_node']==m['to_node']
 assert c==t and e['caller']['byte_interval0']==m['byte_interval0']
 assert [c['caller_start_utf8_byte0'],c['caller_end_utf8_byte0_exclusive']]==m['byte_interval0']
 assert c['caller_path']==m['path'] and c['token']==m['token'] and c['caller_physical_line1']==m['physical_line1']
 raw=Path(m['path']).read_bytes();lo,hi=m['byte_interval0'];assert raw[lo:hi]==m['token'].encode()
for c in ci['entries']:
 if 'caller_start_utf8_byte0' in c:
  raw=Path(c['caller_path']).read_bytes();assert raw[c['caller_start_utf8_byte0']:c['caller_end_utf8_byte0_exclusive']]==c['token'].encode()
coverage=j(R/'source-coverage.after.json')['rows'];oldrows=j(A/'source-coverage.json')['rows']
assert len(coverage)==229 and Counter(x['classification'] for x in coverage)=={'NODE':146,'EXCLUDED':83}
assert [(x['path'],x['physical_line1'],x['physical_line_raw_sha256']) for x in coverage]==[(x['path'],x['physical_line1'],x['physical_line_raw_sha256']) for x in oldrows]
for x in coverage:
 raw=Path(x['path']).read_bytes().splitlines(keepends=True)[x['physical_line1']-1];assert h(raw)==x['physical_line_raw_sha256']
 if 'FDeriv/Measurable.lean' in x['path'].replace('\\','/') and 361<=x['physical_line1']<=368:
  assert x['classification']=='EXCLUDED' and x['node_ids']==[] and x['semantic_proof_expansion'] is False
 if x['physical_line1']==4574:
  assert x['classification']=='NODE' and x['node_ids']==['S.compact','R.rough','R.operator']
# All unchanged original37 source/fragment contracts still match; this does not read parent bodies.
for x in j(A/'input-bindings.json'):
 raw=Path(x['path']).read_bytes();assert h(raw)==x['whole_raw_sha256'] and h(raw.replace(b'\r\n',b'\n'))==x['whole_lf_sha256']
 for suffix,key in [('.raw','fragment_raw_sha256'),('.lf','fragment_lf_sha256')]:assert h((A/(x['snapshot']+suffix)).read_bytes())==x[key]
inputs=[];historical=[]
for x in j(R/'input-bindings.json'):
 raw=Path(x['path']).read_bytes();resolved=Path(x['path'])
 if x['id']=='overlay-opening-lease.json':
  resolved=R/x['raw_snapshot'];raw=resolved.read_bytes();historical.append({'id':x['id'],'literal_path':x['path'],'resolved_retained_opening_snapshot':resolved.as_posix(),'reason':x['role'],'current_closed_lease_bound_separately':pin(R/'lease.json')})
 if 'raw_sha256' in x:
  selected=raw;rh=x['raw_sha256'];lh=x['lf_sha256']
 else:
  assert h(raw)==x['whole_raw_sha256'] and h(oldlf(raw))==x['whole_lf_sha256'];selected=raw.splitlines(keepends=True)[x['physical_line1']-1];rh=x['fragment_raw_sha256'];lh=x['fragment_lf_sha256']
 assert h(selected)==rh and h(oldlf(selected))==lh
 assert (R/x['raw_snapshot']).read_bytes()==selected and (R/x['lf_snapshot']).read_bytes()==oldlf(selected)
 inputs.append({'literal_binding':x,'resolved_path':resolved.as_posix(),'recorded_lf_recipe':'Historical overlay recipe: CRLF->LF then isolated CR->LF; not normalized retrospectively','checked_raw_sha256':rh,'checked_recipe_lf_sha256':lh})
extra=[]
for name in ['source-proof-graph.after.json','source-coverage.after.json','caller-inventory.after.json','selected-token-inventory.after.json','selected-providers.after.json','schema-and-boundary.after.md','sourcecontract.json','overlay-delta.json','input-bindings.json','run.json','lease.json']:
 p=R/name;extra.append(pin(p));dest=O/('repaired-frozen-'+name);assert not dest.exists();dest.write_bytes(p.read_bytes())
extra.extend([pin(O/'source-topology-review.json'),pin(O/'direct-call.checks.json'),pin(O/'coverage.byte-checks.json')])
checks={'declared_69_operations_exactly_reproduce_successors':True,'original78_nodes_and_all_nonedge_fields_unchanged':True,'only_original_edge_positions_reclassified_one_based':[245,253,254,255],'sixteen_missing_references_added_exact_bytes':True,'row_union_and_all_row_raw_hashes_unchanged':True,'counts':{'nodes':78,'edges':296,'rows':229,'NODE':146,'EXCLUDED':83,'callers':167,'configured_tokens':160,'strict_original_inputs':37,'overlay_bindings':82,'primary_balanced_anchors_reused':20},'T1':{'raw_unrelated_proof_exposure':1,'semantic_proof_expansion':0,'unrelated_rows361_368_excluded':True,'line364_reference_preserved_as_excluded':True},'T3':{'row4574_substantive_boundary':True,'old_source_use_endpoints_citation_spans_retained':True,'rough_operator_not_premises':True},'historical_opening_lease_resolution':historical,'author_output_hash_checks':len(run['output_files']),'author_run_hash_recipe':run['hash_recipe'],'canonical_statement_lf_bytes':1795,'canonical_statement_lf_sha256':'f37b4a07e62e16d22f4ecbc1fba9c38fd80d42f947011b38ded7c5153e0bea1d','no_math_public_assumption_route_change':True}
put(O/'reviewer.topology.repaired.checks.json',checks)
slots=copy.deepcopy(negative['semantic_slots'])
for s in slots.values():s['relation']='faithful-bounded-source-contract; exact requested representation repairs accepted independently'
slots['scopes']['evidence']='T1/T2/T3 exact overlay checked; compact integrated C.2 target preserves rough B.13/outer operator closure boundaries.'
receipt={'schema_version':1,'actor':'phase_source_reviewer_20261005','status':'ACCEPTED_SCOPED_SOURCE_ONLY_TOPOLOGY','verdict':'accepted-scoped','blocking':False,'scope':'Independent renewed source-only49 topology after representation-only overlay; no theorem/implementation/source-fidelity admission','independent_from_graph_creator':True,'independent_from_overlay_creator':True,'independent_from_formalizer':True,'independent_from_decoder':True,'prior_negative':pin(O/'source-topology-review.json'),'original_topology_and_primary_review_reuse':'Original full source contract,20 balanced primary anchors,30 provider contracts,229-row union and37 exact frozen inputs reused only after unchanged bytes checked; current69 declared operations reviewed independently.','source_primary_before_target':True,'exposure':negative['exposure'],'semantic_slots':slots,'source_excess':[],'mathematical_statement_deltas':[],'deltas':[],'repairs':[],'accepted_representation_overlay':['T1 honest raw exposure1/semantic0 and unrelated proof exclusion','T2 sixteen literal public/typing references with edges/inventory','T3 substantive compact/B.13 target boundary classification; no rough/operator premise'],'graph_sha256':h((R/'source-proof-graph.after.json').read_bytes()),'graph_lf_sha256':h(oldlf((R/'source-proof-graph.after.json').read_bytes())),'overlay_creator_run_sha256':h((R/'run.json').read_bytes()),'overlay_creator_closed_lease_sha256':h((R/'lease.json').read_bytes()),'review_evidence':'Exact69 declared overlay operations independently reproduce all five JSON successor artifacts. All78 nodes and graph nonedge fields are unchanged; only original edges245/253-255 are reclassified and sixteen exact requested reference edges appended. All82 binding recipes including the historical retained OPEN lease, all37 original live source/fragment pins,20 primary spans and unchanged1795 signature are preserved.229 raw row identities remain unchanged;146NODE/83EXCLUDED faithfully distinguish incidental theorem/proof exposure and actual B.13 compact reduction. Every appended byte interval, plain map/variance and expectation notation resolves to the actual already-selected semantic provider; no implementation calls or public premises are invented. Original BLOCKED receipt is unchanged. No49 body/Test/blind/math-verdict read and no compiler started.','review_checks':checks,'input_artifacts':inputs,'additional_current_artifacts':extra,'remaining_boundary':negative['remaining_boundary'],'compiler_started':False,'review_completed_utc':datetime.now(timezone.utc).isoformat()}
receipt['review_run_sha256']=h(cj(receipt));put(O/'source-topology-review.repaired.json',receipt)
# Final read hash checks; actual lease closure is the last filesystem mutation.
for x in extra:assert h(Path(x['path']).read_bytes())==x['raw_sha256']
lease=j(O/'reviewer.topology.repaired.lease.json');lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','python_lease':'CLOSED','compiler_lease':'CLOSED','compiler_started':False,'closed_utc':datetime.now(timezone.utc).isoformat(),'result':pin(O/'source-topology-review.repaired.json'),'review_run_sha256':receipt['review_run_sha256'],'input_artifacts':inputs,'additional_current_artifacts':extra})
lease['lease_run_sha256']=h(cj(lease));(O/'reviewer.topology.repaired.lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'result':pin(O/'source-topology-review.repaired.json'),'review_run_sha256':receipt['review_run_sha256'],'lease':pin(O/'reviewer.topology.repaired.lease.json'),'status':'CLOSED'},ensure_ascii=False))
