from pathlib import Path
import copy,datetime,hashlib,json
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent;S=B/'independent-source-first90'
def pin(p):
 p=Path(p);b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def load(p):return json.loads(Path(p).read_bytes())
def put(n,v):
 p=O/n
 with p.open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return pin(p)
def check(d):
 p=Path(d['path']);p=p if p.is_absolute() else R/p;q=pin(p)
 assert q['raw_sha256']==d.get('raw_sha256',d.get('sha256')) and q['bytes']==d['bytes'],p
 return q
gpath=S/'source-proof-graph90.native.json';cpath=S/'source-coverage90.native.json';mpath=S/'closed-raw-manifest.source-first90.native.json'
assert pin(gpath)['raw_sha256']=='d55dc5ebc98cde129607e173801c39b0571a83383f75d03b1bdcc12ef7af3d36'
assert pin(cpath)['raw_sha256']=='a8e026e8cea330e34ca620561fe1208e219ad810e565d5757b2e8e913cd2e2de'
assert pin(mpath)['raw_sha256']=='82eed8395f4ddcbeb984847a31e277c8980c171fd6a42c69a0ee9608ef6b845c'
g=load(gpath);c=load(cpath);native=load(mpath);actual=[check(d) for group in ['inputs','outputs'] for d in native[group]]
assert len(g['nodes'])==7 and len(g['edges'])==8 and len(g['AND_junctions'])==3 and len(c['items'])==22
assert sum(x['disposition']=='NODE' for x in c['items'])==14 and sum(x['disposition']=='EXCLUDED' for x in c['items'])==8
primary=Path(g['source']['primary']['path']).read_bytes();pm=load(S/'primary-source90.raw-manifest.native.json')
for span in pm['anchors']:assert hashlib.sha256(primary[span['byte_start_zero_based']:span['byte_end_exclusive']]).hexdigest()==span['raw_span_sha256']
GG=Path(g['global_graph_reused']['path']);GI=Path(g['global_inventory_reused']['path']);globalg=load(GG);globali=load(GI)
assert len(globalg['nodes'])==38 and len(globalg['edges'])==76 and len(globali['items'])==47
assert not g['creator_self_independent_topology_approval'] and not c['creator_self_independent_coverage_approval']
assert g['creator']=='/root/fresh_source87'
for a in g['AND_junctions']:
 assert set(a['all_of'])=={e['source'] for e in g['edges'] if e['target']==a['target']}
for path,name in [(gpath,'source-proof-graph90.original.exactraw.json'),(cpath,'source-coverage90.original.exactraw.json')]:
 q=O/name;assert not q.exists();q.write_bytes(path.read_bytes())
proposed=copy.deepcopy(g)
node=next(x for x in proposed['nodes'] if x['id']=='S90-A1');before_node=node['claim']
node['claim']='Actual flow and reflection are jointly Borel, including zero gradient normal. The integrated hazard, its threshold-crossing map and each finite stopped-recursion record/history are jointly Borel in the actual parameters and clock inputs; finite tuple/tag/time operations are Borel. These ingredients are derived internally or consumed from exact verified producers.'
edge=next(x for x in proposed['edges'] if x['source']=='S90-A1' and x['target']=='S90-M1');before_edge=edge['justification']
edge['justification']='Joint Borel flow/reflection and finite tuple/tag operations derive append and pair-lift measurability. Joint Borel hazard/threshold crossing and actual finite stopped-recursion measurability supply the separate actual H_(n+1) measurability clause. No measurability provider premise is added.'
candidate=put('source-proof-graph90.proposed-measurability-scope-overlay.json',proposed)
changes=[{'json_pointer':'/nodes/1/claim','before':before_node,'after':node['claim']},{'json_pointer':'/edges/1/justification','before':before_edge,'after':edge['justification']}]
proposal=put('proposed-topology-scope-overlay90.json',{
 'status':'PROPOSED_REQUIRES_DISTINCT_REVIEW_NOT_APPLIED','proposer_id':'/root/exact_verify77','original_graph':pin(gpath),'proposed_graph':candidate,'unchanged_coverage':pin(cpath),'changes':changes,
 'diagnosis':'S90-M1 claims actual H_(n+1) measurability as well as append measurability. Flow/reflection/finite products alone do not make the hazard-derived next-wait/actual record Borel. Appendix A.2 explicitly supplies integrated-hazard/threshold-crossing/finite-recursion Borel ingredients, and coverage item14 already includes them, but the incoming A1 node/edge scope omits them. Expand that existing dependency scope rather than adding a source premise or falsely reusing a density-law equality as a Borel proof.',
 'minimality':'Two strings only; all7nodes/8edges/3AND memberships,22dispositions, alternative routes, original source assumptions and OPEN boundaries unchanged. This records an existing source dependency, not a new mathematical assumption.',
 'no_self_acceptance':True,'no_canonical_mutations':True})
packet=put('topology-repair-review-packet90.json',{
 'purpose':'Distinct exact two-field source graph dependency-scope review before adoption','primary':g['source']['primary'],'primary_anchors':['A1.E1','A1.E2','A1.E7','A1.SS2 proof integrated hazard/threshold crossing and finite recursion Borel paragraph'],
 'original_graph_snapshot':pin(O/'source-proof-graph90.original.exactraw.json'),'original_coverage_snapshot':pin(O/'source-coverage90.original.exactraw.json'),'proposal':proposal,'exact_candidate_graph':candidate,
 'review_contract':'Read primary first; compare original graph target S90-M1 with its incoming A1 scope. Assess whether the precise two-string expansion captures a necessary source Borel dependency without adding source binders, extra formal parents or changing any route. Do not inherit prior acceptance/source verdicts. Proposer cannot approve own overlay.',
 'no_header_BODY_or_SAU_approval':True})
assessments=[
 'Standing C2/curvature six binders agree with primary S1; no append-measurability premise is licensed.',
 'Eta range agrees with source positive eta and beta eta<=1.',
 'Center and gradient-difference definitions agree with3.4; finite update must retain them.',
 'Actual flow/reflection with zero-normal identity are Borel; no continuity of reflection at zero is asserted.',
 'Fresh Exp law is inherited through89, not assumed independent of arbitrary histories.',
 'Actual integrated-hazard next wait and raw-coordinate convention belong to literal recursion.',
 'New cumulative time is old time plus actual finite wait, preserving every old coordinate.',
 'New phase is actual S(Phi_wait z), not arbitrary mark or supplied append equality.',
 'Infinity terminates/stops; strict event excludes it, so no fictitious finite phase/time is claimed.',
 'Between-jump flow determines finite pre-bounce state; complete continuous path is not supplied.',
 'Strict ordered simplex motivates positive next-relative wait; no endpoint mass substitution.',
 'One append/transport bridge is source-implicit; subsequent ordered-time iteration stays OPEN.',
 'Joint Borel flow/rate/reflection is a genuine required ingredient and is already in A1 scope.',
 'Coverage correctly includes Borel hazard/threshold/finite recursion, but graph A1 incoming scope must explicitly include it to derive actual H_(n+1) measurability. Exact two-string repair proposed, not self-approved.',
 'Full bounded signed path-functional claim excluded; current nonnegative extended finite-history tests use Tonelli rather than signed integrability.',
 'Products of all factors/final survival/count partition/full series excluded, preserving remaining I5/A7.',
 'Rate-cap/simplex-volume summability excluded from one finite submeasure pushforward; no global normalization.',
 'All-time nonexplosive terminal limit excluded because only a finite-depth tuple is observed.',
 'Physical-time residual memorylessness/random restart/Markovness excluded; fixed n does not provide random-index independence.',
 'No-atom/strict-versus-closed mass equality excluded;89 already supplies a strict finite measure.',
 'Unrestricted next-history law and stopped/infinite/outside-cutoff mass excluded, not silently normalized away.',
 'Global/external source branches remain in unchanged exhaustive47-item inventory and38-node/76-relation graph; not deleted or closed by local result.'
]
coverage_audit=put('coverage90.independent-audit.json',{'reviewer_id':'/root/exact_verify77','original_coverage':pin(cpath),'all22_independent_assessments':[dict(index=i+1,item=x['item'],disposition=x['disposition'],assessment=assessments[i]) for i,x in enumerate(c['items'])],
 'all8_original_edges_reviewed':[dict(source=e['source'],target=e['target'],assessment='Accepted prerequisite in stated sufficient route; not sufficient alone.' if i!=1 else 'Append part accepted; actual-next-history measurability needs precise A2 crossing/finite-recursion dependency scope expansion.') for i,e in enumerate(g['edges'])],
 'three_AND_junctions':'Membership matches incoming graph edges; literal model+Borel substrate=>append, literal recursion+append=>guarded identity,89density+measurableappend+guardedidentity=>actual transported law. No alternative route promoted to AND.',
 'OR_preservation':'Preferred89 transport and optional direct87/86 section calculation remain alternatives. Exact Borel producer reuse vs direct construction is another alternative, not an extra supplied premise. Existing global CDF vs hazard-transport sufficient routes and optional summability/nonexplosion routes unchanged.',
 'global_pins':[pin(GG),pin(GI)],'no_false_survival88_noatom_AND':True,'source_implicit_bridges_remain_unproved':['S90-M1','S90-R1','S90-T'],'whole_I5_G86_11_A7_remain_OPEN':True})
chronology=put('review90.chronology.json',{'reviewer_id':'/root/exact_verify77','source_first_frozen':pin(O/'primary-first90.chronology.json'),'independent_reconstruction_closed_before_creator_graph_read':pin(O/'primary-reconstruction90.closed-RAW-manifest.json'),'creator_comparison_tool_chunks':['38863a','22892f'],'global_OR_comparison_chunk':'8d99d9','supplemental_primary_standing_eta_center_read_after_independent_topology_freeze':'d44e23','creator_script_contents_not_read':'Only manifest descriptor RAW hashed; no private extractor script/rationale consulted.','header90_or_BODY90_read':False,'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
decision=put('decision90.json',{
 'status':'CONDITIONAL_ACCEPTANCE_SOURCE_TOPOLOGY_REQUIRES_DISTINCT_EXACT_SCOPE_OVERLAY_REVIEW','reviewer_id':'/root/exact_verify77','graph_creator_id':'/root/fresh_source87','primary_first_reconstruction':pin(O/'independent-primary-math-reconstruction90.json'),'source':g['source'],'original_graph':pin(gpath),'original_coverage':pin(cpath),'original_closed_source_manifest':pin(mpath),'counts':{'nodes':7,'edges':8,'AND_junctions':3,'coverage_items':22,'NODE':14,'EXCLUDED':8},
 'independent_source_topology_assessment':coverage_audit,'mathematical_candidate_scope':'Feasible bounded source-implicit actual full finite-history append/guarded identity/joint restricted law/marginal/all joint nonnegative tests. Genuine actual constructor and recursion identification required internally; no arbitrary supplied Measurable append or identity binder.',
 'required_repairs':[{'type':'Missing explicit source Borel dependency scope for actual H_(n+1) measurability','proposal':proposal,'exact_candidate':candidate,'distinct_review':'Required, not granted by proposer'}],
 'accepted_original_parts':'All literal source construction, strict finite guarded identity, unnormalized transport, tests,22dispositions except the explicit graph scope residual,3AND membership and all OR/futureOPEN boundaries are independently checked. Original files remain unmodified.',
 'cases':'n0/rank0/stopped/infinite wait/zero or cutoff endpoint/nullA/infinite ENNReal tests/unbounded-across-history finite d and abstract impossible histories require no added analytic condition. Off-support total append is a disclosed definition convention, not source truth or new premise.',
 'no_header_approval':True,'no_Lean_proof_search_or_BODY_read':True,'no_SAU_claim_or_VERIFIED':True,'no_canonical_changes':True,'remaining_OPEN':['Distinct exact-overlay review/adoption','Prospective full header mathematical/type/source review and StatementSeal','Actual compiled proof and source-blind/full source/publication/exact-science review','Remaining I5/G86-11/fullA7 ordered-time/final-survival/path/count assembly','Global/Markov/invariance/L2/cost/main/composition/fullpaper/Goal']})
run=put('run90.json',{'status':'CLOSED_SOURCE_ONLY_CONDITIONAL_DECISION_EXACT_PROPOSAL_NOT_APPLIED','reviewer_id':'/root/exact_verify77','decision':decision,'chronology':chronology,'primary_read_terminal':'61f8ba','primary_reconstruction_terminal':'8d9687','creator_input_output_RAW_descriptors_rechecked':len(actual),'all7exact_author_source_spans_match_primary':True,'all22coverage_dispositions_reviewed':True,'no_native_reasoning_trajectory_fabricated':True,'private_extracts_excluded_publication':[pin(O/'.private.primary90.full-A1-A2.exact-spans.json')['path']]})
inputs=actual+[pin(mpath),pin(gpath),pin(cpath),pin(S/'source-first90.native.json'),pin(S/'primary-source90.raw-manifest.native.json'),pin(S/'chronology.source-first90.native.jsonl'),pin(GG),pin(GI)]
inputs=list({(x['path'],x['raw_sha256']):x for x in inputs}.values())
outputs=[pin(p) for p in sorted(O.iterdir()) if p.is_file()]
manifest=put('closed-RAW-manifest90.json',{'status':'CLOSED_NONCIRCULAR_SOURCE_ONLY_REPAIR_PROPOSAL_REQUIRES_DISTINCT_REVIEW','reviewer_id':'/root/exact_verify77','frozen_inputs':inputs,'owned_artifacts':outputs,'decision':decision,'run':run,'proposal':proposal,'clean_repair_review_packet':packet,'original_files_unchanged':True,'self_hash_intentionally_omitted':True,'privacy':'Long original primary extracts are private local .private.* and excluded from public publication/archive. No source theorem/graph is mutated.'})
assert pin(gpath)['raw_sha256']=='d55dc5ebc98cde129607e173801c39b0571a83383f75d03b1bdcc12ef7af3d36' and pin(cpath)['raw_sha256']=='a8e026e8cea330e34ca620561fe1208e219ad810e565d5757b2e8e913cd2e2de'
print(json.dumps({'decision':decision,'closed_manifest':manifest,'proposal':proposal,'proposed_graph':candidate,'clean_review_packet':packet},indent=2))
