from pathlib import Path
import json,hashlib
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;S=R/'runs/20261007-companion-priority/pbps-actual-phase-normalization103/next-primary104'
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert load(O/'fresh-header.receipt.json')['exit_code']==0
assert load(O/'api-corrected.receipt.json')['exit_code']==0
assert (O/'FreshHeader104.lean').read_bytes()==(O.parent/'Header104.lean').read_bytes()
route=load(O/'independent-route-before-graph104.native.json');check=load(O/'topology-binding-check104.native.json')
for row in route['inputs']:
 assert sha((R/row['path']).read_bytes())==row['sha256_raw']
save('header-math-decision104.native.json',{
 'decision':'ACCEPT_PROSPECTIVE_MATHEMATICAL_HEADER','reviewer':'/root/exact_verifier96','header':info(O.parent/'Header104.lean'),
 'route_frozen_before_creator_graph':info(O/'independent-route-before-graph104.native.json'),'fresh_typecheck':info(O/'fresh-header.receipt.json'),'API_validation':info(O/'api-corrected.receipt.json'),
 'original_six_binders':['positive alpha','alpha <= beta','C2 V','paired genuine Hessian bounds for every x,v','positive eta','beta*eta <= 1'],
 'literal_contract':'First20 actual94/102 definitions byte-equal after line-ending normalization. Five remaining outer definitions R,Vy,piY,gamma,m and inner A,B,sigma,L,J preserve actual phase-first product measure, actual terminal Gamma endpoint and true q*terminal-survival density.',
 'conclusion':'MeasurePreserving J L L for every y,r,n,T; no free density or law, no probability or finite sector mass assumption.',
 'mathematical_audit':[
 'The 103 tilted-position times standard Gaussian equality supplies exactly the actual normalized phase density with partition inverse; no missing scale or Gaussian constant.',
 'The density rewrite uses prod_withDensity_left with SFinite m. Literal Delta is a finite intersection of strict coordinate inequalities, so measurable; map_comap_subtype_coe gives restricted finite-dimensional volume and SigmaFinite.of_map supplies the needed instance.',
 '93 exports actual joint rho measurability; 97 exports actual A and Theta measurability and endpoint inverse. Neither private helper nor a merely inferred import can replace these public projections.',
 '97 and 102 each quantify an existential rho-time; equality follows coordinatewise from their identical T-t(i.rev) equation, including Fin0. The endpoint inverse and weighted identity therefore act on the same Theta.',
 'Measurable B follows from actual A. J is continuous flipped momentum swap. Endpoint inverse gives B(Theta q)=J(B q), with the first coordinate R(A q) and second R(q.z) in the correct order.',
 'Nonnegative test extensionality and constant multiplication require no finite sector mass or signed-integrability premise. No cancellation, subtraction or division by a density is used.',
 'All recorded degenerate cases remain viable; strict event times exclude a jump at T, so no incorrect pointwise reversal at jump instants is asserted.'
 ],
 'edge_cases':route['edge_cases'],'at_most_seven_step_route':route['route'],
 'actual_parent_boundary':['ActualFiniteCountPath.actual_finite_count_path_law','ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws','ActualWeightedSector.actual_weighted_sector_lintegral','ActualPhaseNormalization.actual_phase_gibbs_normalization'],
 'reuse_decision':'Bounded new actual measure integration theorem. Existing shared/local producers and pinned Mathlib suffice; no new external port or generic normalization theorem is needed.',
 'implementation_obligations':['Derive measurable Delta and sigma-finite m internally, without calling private97 endpoint_data.','Discharge all measurability and witness alignments explicitly.','Final compiled theorem must be checked against this exact expanded candidate.'],
 'defects':[],'proof_credit':False,'seal_claim_or_VERIFIED_transition':False,
 'remaining_boundary':'Prospective acceptance only. No countable sector assembly, full-process law identification, signed bilinear identity, invariant process probability, L2/semigroup, main merge or purification credit.'})
save('source-topology-admission104.native.json',{
 'decision':'ACCEPT_BASE_PLUS_104_DELTA_TOPOLOGY_AND_BOUNDED_COVERAGE','reviewer':'/root/exact_verifier96','creator':'/root/source_final96',
 'review_mode':'Independent noncreator validation after separately frozen header/primary mathematical reconstruction; inherited earlier graph context was known. No source-blind claim.',
 'graph':info(S/'source-proof-graph-delta104.native.json'),'coverage':info(S/'source-coverage-delta104.native.json'),'recommendation':info(S/'recommendation104.native.json'),'creator_closure':info(S/'closed-RAW-manifest104.native.json'),'exact_binding_and_effective_graph':info(O/'topology-binding-check104.native.json'),
 'effective_nodes':55,'effective_edges':96,'new_unique_edges':17,'acyclic':True,
 'admission_rationale':[
 '51 inherited nodes/79 edges plus four distinct nodes and 17 unique incidence edges. Three listed delta incidences already exist; retaining them as aggregate dependencies does not duplicate mathematical credit.',
 'ENDPOINT97 is a public existing theorem projection, distinct from TERM97 terminal-flow formula. Its explicit producer binding supplies the endpoint inverse; it is not inferred from THETA97 measure preservation or re-proved from H99/D99 alone.',
 'TIME97, THETA97 and ENDPOINT97 are sibling projections of one existential producer witness. ALIGN104 also consumes the coordinate conjunct of102 and actual definitions. No measure-preservation-to-coordinate inference occurs.',
 'SECTOR-MEASURE104 explicitly covers finite-inequality simplex measurability, sigma-finiteness, actual density measurability and two density/product API adapters. D99 supplies the literal simplex contract, not an assumed sigma-finiteness certificate.',
 'NORM remains analytically independent of102; it joins SECTOR102 only at normalized sector transport. SECTOR100 is an internal proof ingredient, not a new extra public conclusion.',
 'ENDPAIR104 consumes measurable endpoint intertwining and normalized sector preservation. Its edge to AVG100 remains future-only together with actual A7 identification; no full process or countable-sum credit.',
 'All21 primary spans match exact raw byte ranges and line ranges. The selected normalization/A7/A8/fixed-count matching slice is covered; eventwise path reversal, countable assembly, signed identity, invariance and L2 remain excluded.'
 ],'defects':[],'reviewer_probe_erratum':info(O/'reviewer-api-name-erratum104.native.json'),'certified_new_Lean_edges':False,'proof_credit':False})
inputs={}
for row in route['inputs']:
 p=R/row['path'];inputs[row['path']]=info(p)
for row in check['checked_source_bindings']:inputs[row['path']]=row
outputs=[info(p) for p in sorted(O.iterdir()) if p.is_file()]
save('closed-RAW-review104.native.json',{'kind':'closed independent prospective header/math/topology review','reviewer':'/root/exact_verifier96','inputs':list(inputs.values()),'outputs':outputs,'primary_storage':'Reference and SHA only; no full primary copy created.','shared_mutations':False,'production_implementation':False,'proof_or_VERIFIED_credit':False})
for n in ['header-math-decision104.native.json','source-topology-admission104.native.json','closed-RAW-review104.native.json']:print(n,info(O/n)['raw_sha256'])
