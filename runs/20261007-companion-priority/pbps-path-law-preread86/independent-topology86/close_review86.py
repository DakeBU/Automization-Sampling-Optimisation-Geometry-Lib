from pathlib import Path
import datetime, hashlib, json, re, subprocess

R=Path('E:/Samplinglib')
B=R/'runs/20261007-companion-priority/pbps-path-law-preread86'
O=Path(__file__).parent
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p): return json.loads(p.read_text('utf-8'))
def pin(p):
    raw=p.read_bytes()
    return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
def save(n,d):
    with (O/n).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')

manifest=load(B/'source-only-run-manifest86.json')
inventory=load(B/'source-inventory86.json')
graph=load(B/'source-proof-graph86.json')
candidate=load(B/'candidate-recommendation86.json')
anchors=load(O/'anchor-readback86.spaced-normalization.json')
assert len(anchors['rows'])==56 and all(x['hash_matches'] for x in anchors['rows'])
checks=[]
for section in ['raw_inputs','raw_outputs']:
    for p in manifest[section]:
        actual=pin(R/p['path'])
        checks.append(dict(section=section,expected=p,actual=actual,matches=actual['raw_sha256']==p['raw_sha256'] and actual['bytes']==p['bytes']))
assert all(x['matches'] for x in checks)
save('frozen-input-recheck86.json',dict(created_utc=now(),manifest=pin(B/'source-only-run-manifest86.json'),checks=checks,all_27_entries_match=True,private_extractor_scripts_hash_only_not_consulted=True))

save('reviewer-diagnostics86.json',dict(recorded_utc=now(),retrospective_observation=True,diagnostics=[
 dict(kind='optional_reader_dependency_missing',exit_code=1,error="ModuleNotFoundError: No module named 'bs4'",effect='No output/source writes; stdlib reader used.'),
 dict(kind='schema_int_not_list',exit_code=1,error="TypeError: 'int' object is not subscriptable",effect='Read-only summary assumed seal anchors was a list; corrected type-aware summary.'),
 dict(kind='private_definition_name_lookup',exit_code=1,error='ValueError: substring not found',effect='Actual75 private name is actual_integrated_hazard_clock_statement; corrected rg lookup.'),
 dict(kind='normalization_parser_spacing',exit_code=0,initial_matching=45,final_matching=56,effect='Both readbacks retained. Whitespace-separated text nodes match frozen normalization; primary RAW never changed.'),
 dict(kind='unintended_parent_BODY_display',tool_chunk_id='d8060e',exit_code=0,exact_command_basis="s.index('private def '); next '\\n/--' as terminator",files=['ActualHazardClock.lean','ActualHarmonicFlow.lean','ActualBounceRate.lean'],effect='Incorrect terminator displayed implementation bodies after private Props. Whole-run BODY invisibility is FALSE. No production change. Bodies excluded as basis for source topology and candidate interface conclusions.',chronology='After primary-first86.json, independent-reconstruction86.json, both56-anchor readbacks, and pre-leak omission report to parent.',time_boundary='Exact command wall-clock timestamp was not recorded; pre-leak artifacts carry creation timestamps. recorded_utc is diagnostic write time, not fabricated leak time.')],native_full_trace_files_claimed=False,source_first_evidence=[pin(O/'primary-first86.json'),pin(O/'independent-reconstruction86.json'),pin(O/'anchor-readback86.spaced-normalization.json')]))

# Read only private Prop and public signature here; delimit at the next actual declaration/option.
api=[]
names=['ActualHazardClock','ActualHarmonicFlow','ActualBounceRate']
for name in names:
    p=R/f'AutoSamplingTheory/ExampleCases/ProximalBPS/{name}.lean'
    s=p.read_text('utf-8');a=s.index('private def ')
    stops=[m.start() for m in re.finditer(r'(?m)^(?:set_option |(?:private )?theorem )',s) if m.start()>a]
    stop=min(stops);prop=s[a:stop].rstrip()
    public=re.search(r'(?ms)^theorem ([\s\S]*?) := by',s)
    # Public declarations with linebreak before := are covered by the non-greedy regex.
    api.append(dict(file=pin(p),private_prop=prop,private_prop_utf8_sha256=hashlib.sha256(prop.encode()).hexdigest(),public_signature=public.group(0).removesuffix(' := by') if public else None,scope='Statement/interface only. Previous accidental BODY display separately disclosed.'))
p=R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean';s=p.read_text('utf-8');a=s.index('private def ');z=s.index('\n/--',a)
api.append(dict(file=pin(p),private_prop=s[a:z].rstrip(),scope='Statement/interface only'))
save('definition-api-review86.json',dict(created_utc=now(),interfaces=api,
 six_binders=['hα','hαβ','hV','hH','hη','hβη'],literal_identity='Actual75 c/Phi/rate/Lambda/tau/W and UnitExp P/X/epsilon; candidate source E1 is actual coordinate0. Total S is actual BounceRate R0=I.',
 conclusion='75 already gives continuous monotone Lambda, finite-hitting equivalence, positive-threshold wait>0, tau0=0, top characterization and W tail exp(-Lambda). It does not give the finite density or marked integral. Actual73 supplies continuous/Borel Phi; BounceRate supplies Borel S and continuous rate; UnitExp supplies coordinate0 marginal and positivity.',
 public_parents_are_dependencies_never_extra_binders=True,no_compilation_or_new_proof_attempt=True))

# Exact minimal proposed changes. No effective graph/inventory is written or adopted here.
nodes={n['id']:n for n in graph['nodes']};items={i['id']:i for i in inventory['items']}
ops=[]
def op(file,action,ident,field,before,after,reason):
    ops.append(dict(file=file,action=action,id=ident,field=field,before=before,after=after,reason=reason))
op('graph','replace','G86-02','title',nodes['G86-02']['title'],'Literal jointly Borel actual harmonic flow and total reflection, with continuous nonnegative rate','Source A1.SS2.p3.1 explicitly gives jointly Borel flow/reflection, including zero normal. Marking needs measurability despite possible bounce discontinuity.')
op('graph','replace','G86-02','source_ids',nodes['G86-02']['source_ids'],nodes['G86-02']['source_ids']+['A1.SS2.p3.1'],'Bind the Borel ingredient to its primary source statement.')
for route in graph['junctions'][0]['routes']:
    op('graph','replace','G86-10',f"junction.routes[{route['route']}].ingredients",route['ingredients'],route['ingredients']+['G86-02'],'Each sufficient density route AND-needs the Borel S∘Phi mark; the two background routes remain OR.')
new_edges=[
 ('E86-67','G86-02','G86-10','REQUIRED_MARKING','Borel actual post-bounce marking is common to both sufficient time-density routes.'),
 ('E86-68','G86-11','G86-14','FUTURE_OPEN_CONDITIONAL_SURVIVAL','Inventory I86-21 explicitly needs the fresh unused-clock conditional law after the last prescribed jump.'),
 ('E86-69','G86-02','G86-37','FUTURE_OPEN_DENSITY_ALGEBRA','Literal S fixes position and preserves momentum norm, including zero normal.'),
 ('E86-70','G86-33','G86-37','FUTURE_OPEN_DENSITY_ALGEBRA','Exact phase density depends on position and momentum squared norm.'),
 ('E86-71','G86-37','G86-22','FUTURE_OPEN_SURVIVAL_WEIGHT','Arcwise log-density integration must telescope through bounce points using rho(Sz)=rho(z). Volume preservation alone does not imply this identity.')]
for ident,fr,to,route,reason in new_edges:
    op('graph','append',ident,None,None,dict(id=ident,**{'from':fr,'to':to},classification='INGREDIENT',route=route,dependency_edge=True,reason=reason),reason)
op('graph','append','G86-37',None,None,dict(id='G86-37',title='Actual bounce preserves the exact Gibbs phase-density value',classification='SOURCE_REQUIRED_OPEN',source_ids=['A1.Ex3','S3.E1','A1.SS1.SSS0.Px1.p5.1']),'Make the already-inventoried I86-31 ingredient explicit; rho(Sz)=rho(z) is distinct from Lebesgue preservation and from process invariance. It remains OPEN.')
op('inventory','replace','I86-31','nodes',items['I86-31']['nodes'],items['I86-31']['nodes']+['G86-37'],'Associate its existing density-value argument with the explicit node; preserve all original mappings.')
coverage_map={'I86-09':['A1.SS1.p3.1','A1.SS1.p3.2','A1.SS1.p3.3','A1.SS1.p3.4'],'I86-10':['A1.SS1.p3.5','A1.SS1.p3.6'],'I86-26':['A1.SS1.SSS0.Px1.p3.1'],'I86-25':['A1.SS1.SSS0.Px1.p3.2'],'I86-33':['A1.SS1.SSS0.Px1.p3.3'],'I86-18':['A1.SS1.SSS0.Px1.p4.1'],'I86-40':['A1.E3'],'I86-37':['A1.Ex22']}
for ident,extra in coverage_map.items():
    op('inventory','replace',ident,'source_ids',items[ident]['source_ids'],items[ident]['source_ids']+extra,'Directly cover already-frozen source anchor(s); preserve existing item semantics and classifications. A3 remains excluded global boundary.')
save('proposed-topology-overlay86.json',dict(schema='astis.independent-proposed-topology-overlay86.v1',status='PROPOSED_REQUIRES_DISTINCT_PRIMARY_FIRST_REVIEW_NOT_SELF_ACCEPTED',reviewer_id='/root/exact_verify77',created_utc=now(),original_graph=pin(B/'source-proof-graph86.json'),original_inventory=pin(B/'source-inventory86.json'),operations=ops,prospective_counts=dict(inventory=40,nodes=37,relations=71,dependency_edges=68,excluded_associations=3),no_original_or_shared_mutations=True,scope_deviation_disclosed_in='reviewer-diagnostics86.json',distinct_review_requirement='Another reviewer must reread primary and audit exact overlay AND complete effective graph before root adoption, not rely on this whole run being BODY blind.'))

coverage=[]
for row in anchors['rows']:
    ident=row['source_id'];mapped=[x['id'] for x in inventory['items'] if ident in x['source_ids']]
    proposed=[item for item,extra in coverage_map.items() if ident in extra]
    coverage.append(dict(source_id=ident,normalized_sha256=row['actual_normalized_sha256'],raw_primary_match=True,original_items=mapped,proposed_additional_items=proposed,review='Source text read independently; equation/paragraph context and NODE/EXCLUDED classification retained.'))
save('source-coverage-review86.json',dict(created_utc=now(),all_56_hashes_match=True,original_direct_inventory_mapping=44,original_unmapped_frozen_anchors=12,all_56_directly_covered_if_distinct_overlay_accepted=True,rows=coverage,original_40_item_review=[dict(id=x['id'],title=x['title'],classification=x['classification'],review='Content source-faithful within bounded scope; source gaps and future OPEN retained.',needs_overlay=x['id'] in coverage_map or x['id'] in ['I86-04','I86-21','I86-31']) for x in inventory['items']],
 graph_review=dict(nodes=36,edges=66,dependency_edges=63,excluded_associations=3,all_nodes_and_edges_inspected=True,correct_AND_OR='G10 backgrounds are alternatives; each AND-needs clock, stopped hazard, differentiability, generic transport/FTC AND Borel mark. FullA7 AND finite factors, residual survival, nonaccumulation/path conventions; fixedstate cap/simplex estimate remains OPTIONAL sufficient analytic route. G24/G25/G30 conjunctions retain all constituents.',excluded='E64 probability-kernel representation not necessary for invariance; E65 Borel kernel not Markov/CK; E66 formal exponentiation not a rigorous route.',open_omissions='Residual conditional survival and density preservation require proposed explicit edges; no future node receives proof credit.'),
 full_primary_context='Primary-first reader also read heuristic generator discussion and A2/A3 context beyond the56 frozen anchors. Those are excluded boundaries, not inferred from implementation.'))

save('candidate-math-review86.json',dict(created_utc=now(),candidate=pin(B/'candidate-recommendation86.json'),status='ACCEPT_PROSPECTIVE_MATHEMATICAL_SCOPE_ONLY',no_header_or_seal_or_claim_or_proof=True,
 strict_new_edge='Finite first-wait subprobability has Lebesgue density lambda(Phi_s z)*exp(-Lambda(s)); push through Borel s↦(s,S(Phi_s z)). This follows from CDF plus derived FTC/measure equality; 75 tail/CDF alone is not recredited.',
 six_original_assumptions_only=True,extra_public_providers=False,
 mathematical_checks=[
 'Hazard derivative derives from continuous actual rate along actual real-time flow; no supplied hazard regularity, positive rate, strict increase or differentiable inverse.',
 'Actual product coordinate0 marginal is Exp1. toNNReal changes no positive threshold AE; zero/nonpositive raw thresholds are null. tau0=0 is excluded by A_T positive-wait restriction.',
 'A_T={0<u<=T} forces u finite; any default finite projection must be used only after that fact. Infinity is no finite bounce and must not contribute an artificial mark at0.',
 'Continuous finite CDF gives no finite-time atoms. Source simplex0<t1<...<tn<t versus candidate(0,T] is harmless only with an explicit endpoint-null argument. Flat hazard intervals do not acquire atoms.',
 'Finite mass is1-exp(-Lambda(T)) in[0,1]; remaining mass includes beyondT and infinity. No renormalization, no assertion all waits finite.',
 'T0 gives empty restriction and zero RHS. M0 gives zero tests. Rank0/zero normal/zero rate gives identity bounce and zero density, positive-threshold infinity. No division by rate cap.',
 'Bounded Borel real h and nonnegative density on finite interval give both L1 bounds by M*finite_mass. No outer exp(cap*T) integrability or stationarity needed.',
 'The n1 rate factor and postbounce state are genuine A7 consumers. To obtain exactly-one-event term also requires residual survival. Iteration requires independent unused clock tail at random poststates and measurable recursion, all separately OPEN.',
 'Fixed parameters only. No uniform-parameter AE event or arbitrary correlated random initialization substitution.'
 ],
 required_later_work=['Exact whole-Prop header and definition identity review before Seal.','Derive C1 real hazard primitive and finite density measure equality; then Borel marking/integral map.','Endpoint/null-event and top projection branch lemmas.','Independent decoder/final source review only after actual complete theorem exists.'],
 remaining_OPEN=candidate['explicit_OPEN'],source_vs_ASTIS=candidate['source_vs_ASTIS'],
 implementation_visibility='Parent BODY accidentally displayed after pre-leak primary reconstruction and omissions; candidate interface conclusion uses only exact private Props/public signatures. No claim whole-run implementation blindness.'))

head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
assert head=='8280ef700ea01a1e94c9e7a3cba05a26b4156b56'
save('decision86.json',dict(schema='astis.independent-source-topology-review86.v1',created_utc=now(),reviewer_id='/root/exact_verify77',checked_workspace_commit=head,
 status='ACCEPT_CANDIDATE_SCOPE_ONLY_TOPOLOGY_REPAIR_PENDING_DISTINCT_REVIEW',
 topology_verdict='ORIGINAL_GRAPH_NOT_ADMITTED_UNCHANGED',candidate_verdict='MATHEMATICALLY_ADMISSIBLE_PROSPECTIVE_STRICT_NEW_EDGE',
 source_first_basis=[pin(O/'primary-first86.json'),pin(O/'independent-reconstruction86.json'),pin(O/'anchor-readback86.spaced-normalization.json')],
 input_manifest=pin(B/'source-only-run-manifest86.json'),candidate=pin(B/'candidate-recommendation86.json'),primary=pin(R/inventory['primary']['path']),
 required_repairs=['Borel mark as common AND ingredient of both G10 background routes.','Conditional unused-clock dependency G11→G14, matching I21.','Explicit bounce phase-density preservation ingredient feeding G22, distinct from volume/process invariance.','Direct inventory association of12 currently unmapped frozen anchors.'],
 proposed_overlay=pin(O/'proposed-topology-overlay86.json'),
 independence_limit='Whole-run parent BODY invisibility is false due reviewer extraction error. Primary-first reconstruction,56-anchor readbacks and omission diagnosis preceded it. A distinct primary-first reviewer must review exact overlay and whole effective graph before adoption. Parent bodies never certify source coverage.',
 no_source_theorem_or_Lean_changes=True,no_Statement_Seal_or_completion_or_VERIFIED=True,compile_status='NOT_RUN_SOURCE_ONLY_NO_HEADER',remaining='A7 iteration/path law/reversal/phase invariance/AE-safe Jensen/allL2 density/semigroup/cost/main paper remain OPEN.'))

# Close all actual scientific content reads and hash-only artifact observations separately.
content_paths=[B/n for n in ['source-only-run-manifest86.json','source-inventory86.json','source-proof-graph86.json','candidate-recommendation86.json','source-first-seal86.json','source-only-closure86.json','statement-api-retrieval86.json']]
content_paths += [R/inventory['primary']['path']]
content_paths += [R/f'AutoSamplingTheory/ExampleCases/ProximalBPS/{n}.lean' for n in names]
content_paths += [R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',R/'.agents/skills/astis-substantive-advance/SKILL.md',R/'.agents/skills/astis-semantic-roundtrip/SKILL.md']
artifacts=[pin(p) for p in sorted(O.iterdir()) if p.is_file()]
save('closed-RAW-manifest86.json',dict(schema='astis.closed-independent-review-raw-manifest86.v1',status='CLOSED_NONCIRCULAR',created_utc=now(),reviewer_id='/root/exact_verify77',actual_content_reads=[pin(p) for p in content_paths],hash_only_observations=checks,owned_artifacts=artifacts,self_hash_omitted=True,run_scope_deviation_retained=True,originals_unchanged=True))
print(json.dumps(dict(status=load(O/'decision86.json')['status'],decision=pin(O/'decision86.json'),manifest=pin(O/'closed-RAW-manifest86.json'),overlay=pin(O/'proposed-topology-overlay86.json')),indent=2))
