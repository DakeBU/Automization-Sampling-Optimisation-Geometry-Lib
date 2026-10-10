from pathlib import Path
import json,hashlib,os,sys
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
PRE=R/'runs/20261007-companion-priority/pbps-bounce-rate-preproof74/independent-header-source74'
RUN=R/'runs/20261007-companion-priority/pbps-actual-bounce-rate74'
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(R).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
def write(n,x):
 p=O/n;assert not p.exists(),n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def get(p):return json.loads(p.read_bytes())
module=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean'
lesson=R/'website/content/declaration_lessons/pbps-actual-bounce-rate.json'
publication=R/'website/content/publications/pbps-actual-bounce-rate.json'
api=R/'AutoSamplingTheory/TechnicalLemmas/Analysis/QuadraticRegularization.lean'
mathfreeze=RUN/'mathematics-freeze74.json';imap=RUN/'implementation-source-map74.json'
source_header=PRE/'header74.proposed.exactraw.snapshot.lean'
raw=module.read_bytes();ls=raw.splitlines(keepends=True)
assert len(ls)==211 and len(raw)==10565 and sha(raw)=='fcec688033797683b44f279a4d22971598926e6af3e9682ad76493d37580937c'
assert b''.join(ls[:70])==source_header.read_bytes()
def span(a,z):
 b=b''.join(ls[a-1:z]);return {'start_line':a,'end_line':z,'RAW_start_inclusive':sum(map(len,ls[:a-1])),'RAW_end_exclusive':sum(map(len,ls[:z])),'exact_code_RAW_sha256':sha(b),'exact_code_LF_sha256':sha(b.replace(b'\r\n',b'\n')),'RAW_bytes':len(b)}
j=get(lesson);unit=j['units'][0];pub=get(publication)['items'][0]
assert len(j['units'])==1 and len(unit['steps'])==7
assert unit['statement']==pub['statement']==unit['lean_statement']
assert unit['helpers']==['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_statement']
assert 'ActualHarmonicFlow' not in ''.join(l.decode('utf-8') for l in ls[:3])
stepchecks=[];covered=[]
for idx,s in enumerate(unit['steps'],1):
 reg=s['lean_source_region'];a,z=reg['start_line'],reg['end_line'];b=b''.join(ls[a-1:z]);assert reg['source_raw_sha256']==sha(raw)
 assert sha(b)==reg['exact_code_raw_sha256'] and b.decode('utf-8')==s['lean']
 stepchecks.append({'step':idx,'title':s['title'],'text':s['text'],'formula':s['formula'],'source_region':span(a,z),'literal_BODY_exact':True,'source_review_status':'independent implementation/exposition preparation, final packet pending'})
 covered.extend(range(a,z+1))
assert covered==list(range(106,209))
sourcegraph=get(PRE/'source-proof-graph74.json');inventory=get(PRE/'source95-item-classification74.json');oldob=get(PRE/'source-obligations26.before-header74.json')
assert len(sourcegraph['nodes'])==28 and len(sourcegraph['edges'])==52 and len(inventory['rows'])==95

# Source-driven projection authored independently after the source contract was
# reaffirmed, not adopted from the root's implementation map.
nr={
 'N01':('same finite-dimensional arbitrary inputs; local universal y/xRef/z',[17,24,62,70,167,169]),
 'N02':('same hV C2 caller and internal r0 producer',[20,20,107,110]),
 'N03':('same two Hessian bounds and nonnegative constants',[20,23,107,110]),
 'N04':('same eta>0/betaeta<=1 retained; positivity used in H/radii',[24,24,162,187]),
 'N05':('gradient continuous internally via r0 hLip.continuous',[107,111]),
 'N06':('same actual residual in literal and proof',[26,26,73,73]),
 'N07':('same actual center in literal and proof',[25,25,72,72]),
 'N08':('same total reflection formula in literal and proof',[27,28,74,74]),
 'N09':('exact zero-safe extension, no nonzero-normal caller',[112,112,159,161]),
 'N10':('orthogonal reflection identity and all-normal algebra',[113,130]),
 'N11':('Borel total division/inner/norm bridge within hSmeas fun_prop',[131,133]),
 'N12':('same actual S defined and substituted, not arbitrary supplied bounce',[29,30,75,75,137,140]),
 'N13':('position fixed and actual involution',[137,140]),
 'N14':('same sqrteta positive-part rate',[31,32,76,77]),
 'N15':('rate nonnegative, flipped rate/difference and zero normal',[144,161]),
 'N16':('actual rate continuous and hence Borel',[134,136,165,166]),
 'N17':('actual joint Borel S in reference and phase',[131,133]),
 'N18':('same centered weighted SUM H',[33,34,78,79]),
 'N19':('same actual H bounce conservation',[141,143]),
 'N20':('H nonnegative and exact momentum/position energy radii',[162,187]),
 'N21':('internal canonical QuadReg r0 beta-Lipschitz producer',[106,111]),
 'N22':('actual residual growth from hLip plus triangle inequality',[188,197]),
 'N23':('positive-part Cauchy-Schwarz and nonnegative products',[198,208]),
 'N24':('exact same-energy-layer cap with same constants/center',[188,208]),
 'N25':('inherited flow source context, NOT asserted/imported/formal74 parent',[]),
 'N26':('actual random-path E0 conservation/cap remains open',[]),
 'N27':('clock/hazard/PDMP/nonexplosion/Markov Proposition3.1 remains open',[]),
 'N28':('terminal Borel H_y/K/r_rho/B27/B28 remains open',[])}
projection=[{'item_id':q['item_id'],'source_classification_immutable':q['classification'],'source_node':q['source_node'],'source_id':q['source_id'],'implementation_projection':nr[q['source_node']][0] if q['source_node'] else 'source EXCLUDED remains outside implemented claim','line_ranges_inclusive_pairs':nr[q['source_node']][1] if q['source_node'] else [],'final_semantic_admission':False} for q in inventory['rows']]
nodeprojection=[{'node_id':n,'meaning':v[0],'line_ranges_inclusive_pairs':v[1],'scope':'current deterministic implementation' if n not in ['N25','N26','N27','N28'] else 'retained or open source context, no74 completion credit'} for n,v in nr.items()]
segments=[(1,3,'imports;74 uses QuadReg/Mathlib, not formal73 sibling parent'),(4,15,'attribution/namespace/options/blanks'),(16,24,'private literal declaration and original16 binders'),(25,34,'six source-exact local actual definitions'),(35,59,'ten complete source-reviewed conclusion clauses'),(60,70,'public signature and original16 binders; same literal return'),(71,79,'proof-local actual definitions, definitionally identical'),(80,105,'change to full literal target; no semantic/certificate premise'),(106,111,'internal completeness and r0 Lipschitz/gradient continuity producer'),(112,130,'zero-safe reflection identification/involution/norm/negative pairing'),(131,136,'actual S Borel and actual rate continuity'),(137,161,'actual S/H/rate identities and zero case'),(162,169,'H nonnegative; first9laws assembly and energy-layer intro'),(170,187,'same-energy radii without positive-energy restriction'),(188,208,'actual residual bound and exact pointwise cap'),(209,211,'blank and section/namespace closure')]
lineclass=[]
for i,line in enumerate(ls,1):
 matches=[(a,z,s) for a,z,s in segments if a<=i<=z];assert len(matches)==1
 lineclass.append({'line':i,'classification':matches[0][2],'RAW_sha256':sha(line)})
bridges=[{'node_id':n['node_id'],'source_obligation':n['meaning'],'actual_implementation':nr[n['node_id']][0],'line_ranges_inclusive_pairs':nr[n['node_id']][1],'new_public_premise':False,'final_admission_pending':True} for n in sourcegraph['nodes'] if 'INTERNAL_OBLIGATION' in n['kind']]
assert len(bridges)==13
obmap=[{'id':q['id'],'source_expectation':q['expectation'],'preparation_finding':'Current definitions/BODY and publication inspected against this expectation; final semantic packet comparison pending.','final_decision':None} for q in oldob['obligations']]

inputs=[module,lesson,publication,mathfreeze,imap,api]
snaps=[]
for idx,p in enumerate(inputs):
 b=p.read_bytes();base=f'prepacket-inputs.v0/{idx:02d}.'
 for ext,content in [('exactraw.snapshot',b),('CRLF-only-LF.snapshot',b.replace(b'\r\n',b'\n'))]:
  out=O/(base+ext);out.parent.mkdir(parents=True,exist_ok=True);assert not out.exists();out.write_bytes(content)
 snaps.append({'input':pin(p),'RAW_snapshot':pin(O/(base+'exactraw.snapshot')),'LF_snapshot':pin(O/(base+'CRLF-only-LF.snapshot'))})
write('prepacket.inputs.v0.json',{'phase':'IMPLEMENTATION_PREPARATION_BEFORE_OFFICIAL_SEMANTIC_PACKET','actual_PID':os.getpid(),'EXIT':0,'inputs':snaps,'LF_recipe':'CRLF pairs -> LF only; preserve bare CR and every other byte','mutable_audit_cell_globalledger_not_read_or_pinned':True,'mathematics_freeze_and_implementation_map_are_context_not_independent_verdict':True,'other_math_review_or_decoder_not_read':True,'module_first70_lines_exactly_equal_sealed_prospective_header':True,'no_final_admission':True})
write('prepacket.whole211line-coverage74.json',{'phase':'PREPARATION_ONLY_NO_FINAL_SOURCE_VERDICT','module':pin(module),'source_graph_unchanged':pin(PRE/'source-proof-graph74.json'),'source_inventory_unchanged':pin(PRE/'source95-item-classification74.json'),'95_source_item_projection':projection,'28_source_node_projection':nodeprojection,'52_source_edges_unchanged_source_only':True,'211_line_classification':lineclass,'7_BODY_formula_checks':stepchecks,'all_proof_core_lines106to208_exactly_covered_once':True,'26_obligations':obmap,'13_bridges':bridges,'six_callers_retained_no_new_premise':True,'joint_S_continuity_not_claimed':True,'pointwise_layer_not_actual_path_cap':True,'rank0_alphaeta1_preserved':True,'73_sibling_not_formal_parent':True,'internal_QuadReg_r0_producer':{'API':pin(api),'declaration':'AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic','actual_arguments':'m=alpha,L=beta,r=0,U=V,u=0; hV,hH; CompleteSpace from finite dimension','why_exact':'r=0 makes regularized potential exactly V and L+r exactly beta; no beta+eta^-1 weakening or certificate premise.'}})
finding={'phase':'PREPARATION_ONLY','mathematical_source_blocker_observed_so_far':None,'final_verdict_pending_official_packet_and_decoder':True,'reader_metadata_issue':{'input':pin(publication),'JSON_pointer':'/items/0/purification/dead_code_audit','current':'Pending one actual theorem implementation.','proposed':'One implemented public theorem uses a complete private literal Prop definition as its statement record; the private definition is not a provider or proof certificate. This audit grants no PURIFIED or full-paper credit.','classification':'process-reader stale status only; no statement/BODY/formula/source repair','proposal_not_applied_or_self_approved':True,'mutable_cell_shadow_not_read_or_guessed':True},'source_proof_coverage_currently_prospective_header_only':'This is honestly labeled in publication; final whole-source coverage field requires current final packet admission rather than credit from the header.','exact_seven_steps_and_helper':'Current all7 BODY snippets match source spans and complete literal helper identity; no local browser/renderer admission is given.'}
write('prepacket.preparation-findings74.json',finding)
write('terminal.preparation74.receipt.json',{'actual_PID':os.getpid(),'EXIT':0,'argv':sys.argv,'input_snapshots':len(snaps),'module_lines':211,'lesson_steps_exact':7,'source_rows_projected':95,'internal_bridges':13,'no_Lean_rerun_or_canonical_write':True,'still_OPEN_waiting_final_packet':True})
write('lease.open.json',{'state':'OPEN_PREPARATION_COMPLETE_WAITING_OFFICIAL_PACKET','source_baseline_reaffirmed_before_BODY':pin(O/'source-baseline-reaffirmation74.json'),'prepacket_inputs_v0':pin(O/'prepacket.inputs.v0.json'),'coverage_preparation':pin(O/'prepacket.whole211line-coverage74.json'),'findings':pin(O/'prepacket.preparation-findings74.json'),'no_final_source_admission':True,'no_CLOSED':True})
print(json.dumps({'actual_PID':os.getpid(),'EXIT':0,'coverage':pin(O/'prepacket.whole211line-coverage74.json'),'inputs':pin(O/'prepacket.inputs.v0.json'),'source_rows':95,'whole_module_lines':211,'exact_steps':7,'still_OPEN':True},ensure_ascii=True))
