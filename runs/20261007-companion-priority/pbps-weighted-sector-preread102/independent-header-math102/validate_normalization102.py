from prepare102 import *
def load(p):return json.loads(Path(p).read_bytes())
oldclosure=load(O/'closed-RAW-original-review102.native.json')
for x in oldclosure['inputs']+oldclosure['owned_artifacts']:assert info(R/x['path'])['raw_sha256']==x['raw_sha256'],x['path']
N=S/'graph-normalization102';overlay=load(N/'source-graph-normalization102.native.json');closure=load(N/'closed-RAW-graph-normalization102.native.json')
assert info(N/'source-graph-normalization102.native.json')['raw_sha256']=='f1252389fe9bcd1f364723a3d8277e847c7205da9f51731dd79f330c72ba3c99'
assert info(N/'closed-RAW-graph-normalization102.native.json')['raw_sha256']=='96b7501d98e3c3f428ea34978a0edb5efbf21878e82f7153a1182945a3a9194d'
for x in closure['inputs']+closure['artifacts']:assert info(R/x['path'])['raw_sha256']==x['raw_sha256']
g=load(S/'source-proof-graph-delta102.native.json');g101=load(R/g['base101']['path']);g99=load(R/g101['base_graph']['path']);d100=load(R/g101['prior_delta100']['path']);o100=load(R/g101['unchanged_overlay100']['path'])
nodes={n['id'] for n in g99['nodes']}|set(d100['new_required_slice'])|{'RHO99'}|{n['id'] for n in g101['nodes_added']}|{n['id'] for n in g['nodes_added']}
edges={(e['from'],e['to']) for e in g99['edges']}|{tuple(e) for e in d100['delta_edges']}|{(e['from'],e['to']) for e in o100['changes'][1]['edges']}
edges-={(a,'WEIGHT100') for a in ['GIBBS98','SURV100','PRODUCT99','RENERGY']};edges|={(e['from'],e['to']) for e in g101['required_AND_edges']}
edges-={('WEIGHT100','SECTOR100'),('THETA97','SECTOR100')};edges|={(e['source'],e['target']) for e in g['AND_edges']}
assert overlay['node_identity_normalization']['canonical_id']=='TIME97' and overlay['node_identity_normalization']['display_alias']=='RHO97'
oldnodes=set(nodes);oldedges=set(edges);nodes.remove('RHO97')
assert len(overlay['edge_operations'])==2
for op in overlay['edge_operations']:
 e=op['old'];old=(e['source'],e['target']);assert old in edges;edges.remove(old)
 if op['operation']=='replace':
  e=op['new'];edges.add((e['source'],e['target']))
 else:assert op['operation']=='remove-from-proof-dependency-edges'
assert oldnodes-nodes=={'RHO97'} and oldedges-edges=={('THETA97','RHO97'),('RHO97','ALIGN102')} and edges-oldedges=={('TIME97','ALIGN102')}
assert len(nodes)==42 and all(a in nodes and b in nodes for a,b in edges)
todo=set(nodes);order=[]
while todo:
 ready=sorted(n for n in todo if not any(b==n and a in todo for a,b in edges));assert ready;order+=ready;todo.difference_update(ready)
assert {a for a,b in edges if b=='ALIGN102'}=={'TIME97','RHO101','D99'}
assert {a for a,b in edges if b=='SECTOR102-UNNORM'}=={'THETA97','WEIGHT100','ALIGN102','WEIGHT-MEAS102','LINTEGRAL-MP102'}
contract=overlay['same_witness_contract'];assert set(contract['nodes'])=={'TIME97','THETA97'} and contract['same_witness_required'] and not contract['certified_Lean_edge']
assert contract['producer']==g['required_producers']['THETA97'] and contract['declaration'].endswith('.actual_endpoint_time_reversal_laws')
assert not overlay['self_topology_validation'] and not overlay['preservation']['header_or_mathematical_change']
save('source-topology-admission102.native.json',dict(kind='independent-final-prospective-base-plus-overlay-topology-admission102',reviewer='/root/exact_verifier96',decision='ACCEPT_BASE_PLUS_IDENTITY_NORMALIZATION_TOPOLOGY_AND_COVERAGE',header=info(P/'Header102.lean'),base_graph=info(S/'source-proof-graph-delta102.native.json'),overlay=info(N/'source-graph-normalization102.native.json'),overlay_closure=info(N/'closed-RAW-graph-normalization102.native.json'),original_finding=info(O/'source-topology-decision102.original.native.json'),original_closed_review=info(O/'closed-RAW-original-review102.native.json'),independent_math=info(O/'header-math-decision102.native.json'),fresh_type_compile=info(O/'fresh-type-receipt102.native.json'),review_mode='Noncreator independent validation after previously frozen pregraph mathematics; prior graph context explicit. Original source graph and header remain unchanged.',effective_graph=dict(nodes=len(nodes),edges=len(edges),acyclic=True,topological_order=order,canonical_coordinate_node='TIME97',display_alias_only='RHO97',new_nodes=6,removed_duplicate_node='RHO97',edge_delta=dict(removed=sorted(oldedges-edges),added=sorted(edges-oldedges))),same_witness_contract='TIME97 and THETA97 are sibling projections of the SAME public97 existential witness. Their link is producer binding, not a false inference of coordinates from measure preservation alone. ALIGN102 combines TIME97 and the bound public101 RHO101 witness using coordinate uniqueness.',source_coverage='All21 exact RAW source regions and original19 source IDs retained and independently rechecked in the immutable original review. All required mathematical dependencies present; only stable node identity normalized.',header_and_math_transfer='Exact Header102 and public93/97/101 inputs unchanged; original accepted header mathematics and fresh type-only elaboration reused without duplicate proof search.',required_actual_parents=['actual_endpoint_time_reversal_laws','actual_prescribed_weighted_density_balance','actual_finite_count_path_law'],remaining_findings=[],no_new_source_binders=True,no_public_provider_assumptions=True,no_implementation_coverage=True,no_proof_credit=True,no_self_validation=True,no_full_primary_copy=True))
save('closed-RAW-review102.native.json',dict(kind='closed-independent-prospective-header-math-and-corrected-topology102',inputs=oldclosure['inputs']+[info(N/'source-graph-normalization102.native.json'),info(N/'closed-RAW-graph-normalization102.native.json')],owned_artifacts=[info(p) for p in sorted(O.rglob('*')) if p.is_file() and '__pycache__' not in p.parts],header_math_accepted=True,corrected_topology_accepted=True,original_graph_finding_preserved=True,projection_ordinal_erratum_preserved=True,no_statement_seal=True,no_claim=True,no_proof_credit=True,no_VERIFIED=True,no_full_primary_snapshot=True,self_hash_intentionally_omitted=True))
for n in ['source-topology-admission102.native.json','closed-RAW-review102.native.json']:print(json.dumps(info(O/n)),flush=True)
