from pathlib import Path
import json,hashlib,datetime
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82/header-review82';S=R/'runs/20261007-companion-priority/pbps-process-regularity-preread82';B=O.parent
def load(p):return json.loads(p.read_text(encoding='utf8'))
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def sha_json(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def save(n,d):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
I=S/'source_inventory82.json';G=S/'source_proof_graph82.json';H=B/'header82.proposed.lean';P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
i=load(I);g=load(G);r=load(O/'independent-inventory-region-readback82.json');first=load(O/'independent-primary-readback82.json')
assert info(P)['RAW_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert info(H)['RAW_sha256']=='0333cf3e488effe1fa6f516553bb1e63a3bb650bfe09aca234ed20375cf85e64'
assert g['source_inventory_raw_sha256']==info(I)['RAW_sha256'] and len(i['items'])==36 and len(g['nodes'])==13 and len(g['edges'])==20
assert len(r['regions'])==36 and {x['inventory_id'] for x in r['regions']}=={x['id'] for x in i['items']}
old='Initialized stopped first record, T0=0, finite versus infinite nextwait';new='Initialized live first record with stopped alternative, T0=0, finite versus infinite nextwait'
assert next(n for n in g['nodes'] if n['id']=='G82-05')['obligation']==old
overlay=dict(kind='SOURCE_TOPOLOGY_TITLE_ONLY_CORRECTION',target=info(G),json_pointer='/nodes/4/obligation',node_id='G82-05',old_value=old,new_value=new,source_reason='A1.SS1.p2.1 initializes zeta0 at T0=0; A1.E2/A1.SS1.p2.2 stop only after infinite nextwait. Initial record is live, never already stopped.',changes=['One node title only'],unchanged=['All node/edge identities','All formulas/binders/quantifiers','All20 edges and their reasons','Original graph and inventory bytes','Header and target scope'],mathematical_statement_repair=False,source_author_acknowledgment='PENDING distinct source author exact-overlay acknowledgment before seal')
overlay_hash=sha_json(overlay)
node_findings={
'G82-01':'Six original standing assumptions and fixed deterministic parameters source-backed; intrinsic finite-dimensional Borel/rank0 carrier is a visible ASTIS adapter.',
'G82-02':'Literal harmonic flow is continuous at0 and Phi0=id. Expanded source crossreferences S3.E4/S3.E8/S4.E5 independently read; center and residual definitions are not trusted solely from inventory paraphrase.',
'G82-03':'Nonnegative continuous residual rate composed with actual flow gives finite continuous Lambda, Lambda0=0; A1.SS2.p3.1 directly supports time continuity. No rate-cap positivity is needed.',
'G82-04':'Exp1 first threshold plus deterministic integrated hazard yields exact firstwait survival, including possible infinity. This node needs no memorylessness/Markov theorem.',
'G82-05':'Literal first record is live at(0,z0); stopped is a guarded later infinite-wait branch. Exact title-only overlay corrects contradictory original wording; no header change.',
'G82-06':'Actual source halfopen arcs and inherited nonaccumulation support the allfinite representative retained by the header. This global inherited obligation is separate from firstwait survival. Source failed-limit zero versus ASTIS uncovered z0 is visible, not silently identified.',
'G82-07':'At t<firstwait the initial live interval forces actual Z_t=Phi_t(z0). At firstwait equality is not promised; use defect subset firstwait<=t. Infinite firstwait covers every finite t.',
'G82-08':'Borel sections make defect event measurable; containment plus exact firstwait complement gives upper bound, never event equality. Trivial bounces or later return to the same flow do not invalidate the inequality.',
'G82-09':'Vanishing firstevent probability follows from Lambda continuity at0. Optional finite cap/Ct estimate is an alternative quantitative strengthening, not a second required premise or added header conclusion.',
'G82-10':'Norm-tail stochastic continuity at0 is a faithful source-implicit intermediate consequence of flow continuity AND vanishing actual defect probability. Fixed parameters and delta>0 retained; not a source full L2 theorem.',
'G82-11':'Bounded continuous observable expectation convergence is an OPEN downstream candidate; the current header has no such conclusion. Source names Cc, while a future bounded-continuous generalization needs its own exact reviewed statement.',
'G82-12':'Full L2 contraction strongly continuous semigroup requires genuine source Markov/semigroup, invariance/Jensen, dominated convergence and Cc density. All are excluded from current admission; no backward implication from stochastic continuity.',
'G82-13':'Cadlag/alltime continuity, restart/Markov, path density/reversal, ideal-kernel composition and cost are explicit distinct/excluded boundaries; no current proof credit.'}
node_report=[dict(id=n['id'],source_ids=n['source_ids'],verdict='ACCEPTED_WITH_EXACT_TITLE_OVERLAY' if n['id']=='G82-05' else 'COVERED_SCOPED_SOURCE_NODE_OR_EXCLUSION',finding=node_findings[n['id']]) for n in g['nodes']]
edge_notes={
'E82-01':'Correct standing->actual flow regularity; broad assumptions may be retained without claiming minimality.',
'E82-02':'Correct genuine gradient regularity->continuous rate/hazard; no bounce continuity used.',
'E82-03':'Correct continuous monotone integrated hazard plus actual Exp input->firstwait law.',
'E82-04':'Compressed input/firstwait-to-initial-record interface: consume coordinate0/sourceE1 from G04, not survival probability as a hypothesis required to initialize a record. Initialization stays live per exact overlay.',
'E82-05':'Correct guarded finite update uses actual Phi and reflection; no phase evaluated at infinity.',
'E82-06':'Correct recurrence ingredient for representative; inherited nonaccumulation and measurability remain internal obligations of G06, not consequences of a bare recurrence alone.',
'E82-07':'Correct actual flow supplies arc values and Phi0 identity.',
'E82-08':'Correct n0 live interval at t<T1, finite/toptime both included.',
'E82-09':'Correct actual deterministic covered-arc agreement is needed; arbitrary process provider forbidden.',
'E82-10':'Correct defect subset first-event-by-t, including endpoint; reverse containment not asserted.',
'E82-11':'Correct exact firstwait law/Exp marginal supplies defect probability bound.',
'E82-12':'Correct representative measurability supplies sample-event measurability, independent from probability-law calculation.',
'E82-13':'Correct Lambda0=0 plus continuous hazard gives vanishing firstevent probability.',
'E82-14':'OPTIONAL_ROUTE_ONLY: cap estimate is an alternative route/quantitative strengthening; never AND-required with E13. Source cap zero case needs no division. Original reason already says optionally; this review fixes its interpretation explicitly.',
'E82-15':'Necessary flow-near-origin ingredient of stochastic continuity.',
'E82-16':'Necessary eventual norm-tail containment in actual/harmonic defect.',
'E82-17':'Necessary vanishing probability ingredient, conjunctive with flow continuity. E15-E17 are AND ingredients of stochastic continuity.',
'E82-18':'Future-substrate status correct; no current bounded-observable theorem credit.',
'E82-19':'Future-substrate status correct and separately requires invariance/contractivity/Markov-semigroup/DCT/density; no proof implication from current node alone.',
'E82-20':'Future-substrate only; no stochastic-continuity-to-Markov/path-law implication.'}
edges=[dict(id=e['id'],ingredient=e['ingredient'],consumer=e['consumer'],verdict='ACCEPTED_OPTIONAL_ROUTE_CONSTRAINT' if e['id']=='E82-14' else 'ACCEPTED_SCOPED_DIRECTION',finding=edge_notes[e['id']]) for e in g['edges']]
items=[]
for it in i['items']:
 n=int(it['id'].split('-')[1]);kind='NODE_OR_SOURCE_BOUNDARY'
 if n==1:kind='EXCLUDED_PROVENANCE_ONLY'
 elif n in {5,25,32,34}:kind='PARTIAL_NODE_WITH_EXPLICIT_GLOBAL_EXCLUSION'
 elif n in {26,27,28,29,30,31,36}:kind='EXCLUDED_OR_OPEN_DOWNSTREAM'
 elif n in {20,21,22}:kind='OPTIONAL_CAP_OR_ZERO_CAP_BOUNDARY'
 items.append(dict(id=it['id'],source_id=it['source_id'],classification=kind,mapped_nodes=it['source_graph_nodes'],direct_primary_reread=True,verdict='COVERED',scope_constraint='G05 title overlay applies to any initialized-record use' if 'G82-05' in it['source_graph_nodes'] else 'Current small-time ingredient versus inherited/excluded consumer remains explicit'))
extra=[]
for region in first['regions']:
 sid=region['id']
 excluded=sid.startswith('A1.SS1.SSS0.Px1.p1.') or sid.startswith('A1.SS1.SSS0.Px1.p2.') or sid.startswith('A1.SS1.SSS0.Px1.p3.') or sid.startswith('A1.SS1.SSS0.Px1.p4.') or sid.startswith('A1.SS1.SSS0.Px1.p5.') or sid.startswith('A1.SS1.SSS0.Px1.p7.') or sid in {'A1.Ex10','A1.Ex11','A1.Ex14','A1.Ex15','A1.Ex16','A1.Ex17','A1.Ex18','A1.Ex19','A1.Ex20','A1.Ex21','A1.Ex23','A1.E4','A1.E5','A1.E6','A1.E8','A1.EGx4'} or sid.startswith('A1.SS1.p4.')
 extra.append(dict(source_id=sid,coverage='EXCLUDED_GLOBAL_REVERSAL_OPERATOR_INGREDIENT' if excluded else 'NODE_OR_PARTIAL_CONTEXT',mapped_nodes=['G82-12','G82-13'] if excluded else ['G82-01','G82-02','G82-03','G82-04','G82-05','G82-06','G82-07','G82-08','G82-09','G82-10','G82-11','G82-12','G82-13'],reason='Generator/adjoint/trajectory density/reversal/invariance/Gaussian averaging not required or proved by current small-time edge.' if excluded else 'Directly reread context is covered by the detailed36item/13node assessment; full source theorem remains separate.'))
save('topology-review82.json',dict(status='ACCEPTED_SCOPED_TOPOLOGY_WITH_EXACT_TITLE_ONLY_OVERLAY_PENDING_SOURCE_AUTHOR_ACK',reviewer='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary=info(P),inventory=info(I),graph=info(G),header=info(H),own_primary_first_readback=info(O/'independent-primary-readback82.json'),own_topology_before_extractor_inventory=info(O/'independent-topology-before-inventory82.json'),all36_direct_primary_readback=info(O/'independent-inventory-region-readback82.json'),definition_crossreferences=info(O/'independent-definition-crossreferences82.json'),independence=dict(extractor_identity='/root/fresh_source78',reviewer_is_extractor=False,primary_reread_before_inventory_graph=True,candidate_header_seen_for_scope=True,candidate_BODY82_seen=False,implementation_Lean_used_to_determine_source_topology=False,extractor_private_freeze_script_read=False,extractor_rationale_read=False,source_review_verdict_read=False),item_coverage=items,node_coverage=node_report,edge_coverage=edges,additional_primary_context_regions=extra,counts=dict(inventory=36,nodes=13,edges=20),unmapped_inventory_items=[],unmapped_nodes=[],unmapped_edges=[],necessary_metadata_overlay=overlay,overlay_canonical_payload_sha256=overlay_hash,mathematical_header_repair_required=False,wrong_AND_OR_check='Core flow continuity AND defect probability vanishing are necessary together; E14 optional cap estimate remains optional OR quantitative strengthening; firstwait survival and raw Exp-CDF are alternate law routes; source direct mean1 SLLN versus parent sufficient indicator route stays an inherited OR boundary.',source_gap_audit='No missing mathematical assumption or source gap for the bounded prospective target. A norm-tail stochastic-continuity intermediate is source-implicit, explicitly smaller than the full Ex22-to-L2 strong-continuity package. Finite-dimensional Borel/rank0 and uncovered-z0 total representative are visible ASTIS adapters.',pending='Distinct source author must acknowledge exact title-only overlay before root seals. This is prospective source topology review, not blind decoder/final compiled-source BODY review, Statement Seal, proof acceptance or VERIFIED.',original_graph_inventory_header_unchanged=True))
save('topology-closed-manifest82.json',dict(status='CLOSED_ADDITIVE_INDEPENDENT_TOPOLOGY_REVIEW',reviewer='/root/exact_verify77',topology_review=info(O/'topology-review82.json'),original_header_math_closed_manifest=info(O/'closed-manifest82.json'),primary=info(P),inventory=info(I),graph=info(G),header=info(H),artifacts=[info(p) for p in sorted(O.iterdir()) if p.is_file()],self_hash_omitted=True,no_circular_hash='Original math run manifest is immutable and predates this additive review. This new manifest binds it and all subsequent topology artifacts, excluding only itself.',proof_or_state_credit=False))
for n in ['topology-review82.json','topology-closed-manifest82.json']:print(json.dumps(info(O/n)))
print('Exact reviewed overlay canonical payload SHA256',overlay_hash)
