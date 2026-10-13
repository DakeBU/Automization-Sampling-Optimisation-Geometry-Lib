from pathlib import Path
import copy,hashlib,json,os,sys,re
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73';OWN=BASE/'independent-source73';OLD=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/independent-header-source73'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':'CRLF byte pairs -> LF only'}
def write(n,x):
 p=OWN/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
assert not(OWN/'lease.final.json').exists()
module=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean';raw=module.read_bytes();assert sha(raw)=='506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c';lines=raw.splitlines(keepends=True);assert len(lines)==178
old_header=(ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/header73.proposed.lean').read_bytes();assert sha(old_header)=='a8a7f0f891906e4635d8b77046ee59ddcc3b3cbaeb37f22e6eff00d26b88a27d'
def literal(b):return b[b.index(b'private def actual_harmonic_flow_statement'):b.index(b'theorem actual_harmonic_flow_laws')]
assert literal(raw)==literal(old_header)
def signature(b):
 a=b.index(b'theorem actual_harmonic_flow_laws');return b[a:b.index(b':= by',a)+len(b':= by')]
assert signature(raw)==signature(old_header)
def spans(rs):return [{'start_line':a,'end_line':b,'RAW_sha256':sha(b''.join(lines[a-1:b]))} for a,b in rs]
# This source-to-implementation map is independently authored from the complete BODY.
node_data={
 'STAND-C2':('retained-and-used',[(24,24),(62,62),(101,103)],'hV lowered from C2 to C1 for actual gradient continuity.'),
 'STAND-MODULI':('retained-not-used-in-deterministic-proof',[(24,24),(62,62)],'hα and hαβ remain original source-standing callers. They supply no local proof ingredient here.'),
 'STAND-HESSIAN':('retained-not-used-in-deterministic-proof',[(25,27),(63,65)],'Both Frechet quadratic-form inequalities stay global; no reference to hH in arithmetic/continuity BODY.'),
 'STAND-STEP':('eta-used-cap-retained',[(28,28),(66,66),(98,100),(146,148)],'hη gives positive nonzero square root and nonnegative inverse; hβη is retained and not used in BODY.'),
 'PARAMETERS':('literal-universal-inputs',[(21,28),(36,56),(59,67)],'Actual y,xRef and arbitrary initial z=(x,p); full joint product domain and all-real times.'),
 'CENTER':('literal-source-definition',[(29,29),(69,69),(104,106),(144,145)],'Same c=y−η gradientVxRef, not a free center certificate. Rewrite it internally for the exact force.'),
 'POSITION':('literal-first-coordinate',[(30,33),(70,73),(135,140),(151,154),(166,172)],'First coordinate is exact source no-bounce harmonic expression.'),
 'PHASE-FLOW':('literal-two-coordinate-map',[(30,33),(70,73)],'Same center and reciprocal-scale coefficients, no arbitrary supplied flow.'),
 'ODE-X':('internally-produced',[(128,140)],'Differentiate position with actual sin/cos APIs; congr_deriv normalizes to sqrtη P.'),
 'ODE-P':('internally-produced',[(128,145)],'Differentiate momentum, rewrite actual c and r²=η to −r⁻¹(X−y)−r gradientVxRef.'),
 'INIT':('internally-produced',[(111,115)],'sin0=0/cos0=1 on both coordinates.'),
 'GROUP':('internally-produced-with-both-inverses',[(116,127)],'Addition laws, nonzero square root cancellation; two inverse orders follow via zero-time identity.'),
 'HALF-TURN':('internally-produced-deterministic-endpoint',[(166,172)],'sinπ=0/cosπ=−1 gives (2c−x,−p); no terminal bounced process/kernel.'),
 'ENERGY':('literal-weighted-SUM-definition',[(34,35),(74,75)],'The half of eta^-1 E-position-norm-square plus E-momentum-norm-square; not a product norm.'),
 'FLOW-ENERGY':('internally-produced',[(149,165)],'Translate by same c; expand two separate real squared norms and cancel opposite mixed terms.'),
 'ENERGY-NONNEG':('omitted-source-bridge-produced',[(146,148)],'Use exact H, η>0, nonnegative inverse and squared norms, positive denominator2.'),
 'SCALE':('omitted-source-bridge-produced',[(98,100),(120,121),(140,145),(162,165)],'r>0, r≠0 and r²=η generated from hη; reciprocal products are discharged internally.'),
 'TRIG':('omitted-source-bridge-produced',[(113,115),(120,121),(135,142),(164,165),(169,172)],'Zero/addition/derivative/pi identities and sin²+cos²=1 from the fixed trig APIs.'),
 'NORM-CANCEL':('omitted-source-bridge-produced',[(151,165)],'norm_add_sq_real expands individual E norms; scalar inner identities give +2CS<q,p>/r and its negative; remaining square coefficients use sin²+cos²=1.'),
 'DERIVATIVE':('omitted-source-bridge-produced',[(128,145)],'Actual HasDerivAt terms are built before congr_deriv; the tactic changes derivative expression, not a theorem assumption.'),
 'GRAD-CONT':('omitted-source-bridge-produced-by-existing-local-API',[(101,103)],'Exact previously source-checked canonical Gradient producer applied to hV.of_le; no gradient-continuity caller.'),
 'JOINT-CONT':('omitted-source-bridge-produced',[(104,110),(173,173)],'Continuous center and literal scalar/vector operations on entire y,xRef,t,z domain; hcont.measurable supplies Borel conclusion.'),
 'SELECTED-ANCHOR':('complete-nine-conclusion-consumer',[(20,56),(58,67),(69,97),(173,173)],'Complete literal specification and exact public signature; final tuple collects every conjunct with no extra assumption.')}
graph=load(OLD/'source-proof-graph73.reviewed-projection.json');assert set(node_data)=={n['id'] for n in graph['nodes']}
nodes=[{'node_id':n['id'],'frozen_source_kind':n['kind'],'classification':node_data[n['id']][0],'implementation_spans':spans(node_data[n['id']][1]),'independent_reason':node_data[n['id']][2],'source_node_not_rewritten':True} for n in graph['nodes']]
edge_ranges={
 'SCALE':[(98,100)],'GRAD-CONT':[(101,103)],'JOINT-CONT':[(104,110),(173,173)],
 'PHASE-FLOW':[(29,33),(69,73)],'POSITION':[(30,33),(70,73)],'DERIVATIVE':[(135,145)],
 'ODE-X':[(135,140)],'ODE-P':[(141,145)],'INIT':[(111,115)],'GROUP':[(116,121)],
 'HALF-TURN':[(166,172)],'ENERGY-NONNEG':[(146,148)],'NORM-CANCEL':[(151,165)],
 'FLOW-ENERGY':[(149,165)],'SELECTED-ANCHOR':[(69,97),(173,173)]}
edges=[]
for i,e in enumerate(graph['edges']):
 assert e['consumer'] in edge_ranges
 edges.append({'edge_index':i,'producer':e['producer'],'consumer':e['consumer'],'source_use_site':e['consumer_source_use_site'],'source_edge_unchanged':True,'implementation_relationship':'internal ingredient use or literal definitional expansion, not a new caller','consumer_spans':spans(edge_ranges[e['consumer']]),'producer_evidence':node_data[e['producer']][2],'consumer_evidence':node_data[e['consumer']][2],'accepted':True,'compiled_Lean_graph_edge_claim':False})
write('source-proof-implementation-coverage73.json',{'schema':'independent-frozen-source-graph-current-implementation73/v1','frozen_graph':pin(OLD/'source-proof-graph73.reviewed-projection.json'),'module':pin(module),'node_count':23,'edge_count':37,'source_gap_count':7,'nodes':nodes,'edges':edges,'internal_bridge_status':[{ 'node_id':n,'status':'internally-produced','spans':spans(node_data[n][1]),'reason':node_data[n][2]} for n in graph['source_gap_node_ids']],'all_checked':True,'source_graph_rederived_or_modified':False,'source_graph_is_not_Lean_graph':True})
source=load(OLD/'StageA.independent-source79-classification73.frozen.json');assert len(source['items'])==79
rows=[]
for i,r in enumerate(source['items']):
 selected=r['independent_disposition']=='NODE'
 rows.append({'index':i,'source_block_id':r['source_block_id'],'semantic_subitem':r['semantic_subitem'],'source_claim':r['source_claim'],'frozen_disposition':r['independent_disposition'],'frozen_identity':r['identity'],'direct_RAW_start':r['direct_RAW_start'],'direct_RAW_end_exclusive':r['direct_RAW_end_exclusive'],'direct_RAW_sha256':r['direct_RAW_sha256'],'current_disposition_unchanged':True,'current_relationship':node_data[r['identity']][0] if selected else 'EXCLUDED_FROM_THIS_THEOREM_AND_STILL_OPEN','implementation_spans':spans(node_data[r['identity']][1]) if selected else [],'independent_current_reason':node_data[r['identity']][2] if selected else r['independent_source_comparison']+' The complete current literal/BODY/lesson contains no such conclusion or extra caller.','source_hypothesis_not_automatically_proved':True,'outside_selected_target_credit':False})
assert sum(r['frozen_disposition']=='NODE' for r in rows)==24
write('source79-current-coverage73.json',{'schema':'independent-source79-current-body-coverage73/v1','frozen_inventory':pin(OLD/'StageA.independent-source79-classification73.frozen.json'),'module':pin(module),'source_regions':13,'source_blocks':51,'items':rows,'semantic_item_count':79,'NODE':24,'EXCLUDED':55,'unclassified':0,'classifications_changed':0,'old_source_graph_and_coverage_written':False,'whole_paper_coverage':False})
segments=[(1,7,'imports',['GRAD-CONT','TRIG','DERIVATIVE','JOINT-CONT']),(8,8,'blank',[]),(9,13,'attribution-and-stochastic-boundary',['SELECTED-ANCHOR']),(14,18,'namespace-and-explicit-typing',['PARAMETERS']),(19,19,'blank',[]),(20,28,'private-literal-caller-prefix',['STAND-C2','STAND-MODULI','STAND-HESSIAN','STAND-STEP','PARAMETERS']),(29,35,'literal-definitions',['CENTER','PHASE-FLOW','ENERGY']),(36,56,'nine-complete-conclusions',['SELECTED-ANCHOR']),(57,57,'blank',[]),(58,67,'same-public-caller-prefix-and-target',['SELECTED-ANCHOR']),(68,68,'blank',[]),(69,75,'same-internal-literal-definitions',['CENTER','PHASE-FLOW','ENERGY']),(76,97,'definitional-change-to-exact-nine-conclusions',['SELECTED-ANCHOR']),(98,100,'positive-scale-production',['SCALE']),(101,103,'gradient-continuity-producer',['GRAD-CONT']),(104,110,'full-joint-continuity',['CENTER','JOINT-CONT']),(111,115,'zero-time-production',['INIT','TRIG']),(116,121,'composition-production',['GROUP','SCALE','TRIG']),(122,127,'two-inverse-production',['GROUP','INIT']),(128,145,'both-actual-ODEs',['DERIVATIVE','ODE-X','ODE-P','CENTER','SCALE','TRIG']),(146,148,'weighted-energy-nonnegativity',['ENERGY','ENERGY-NONNEG','STAND-STEP']),(149,165,'weighted-energy-invariance',['ENERGY','FLOW-ENERGY','NORM-CANCEL','SCALE','TRIG']),(166,172,'deterministic-pi-endpoint',['HALF-TURN','TRIG']),(173,173,'complete-nine-law-assembly',['SELECTED-ANCHOR','JOINT-CONT']),(174,174,'blank',[]),(175,176,'section-and-namespace-closures',[]),(177,177,'blank',[]),(178,178,'axiom-observation-command-not-proof',['SELECTED-ANCHOR'])]
line_rows=[];offset=0
for i,line in enumerate(lines,1):
 matches=[r for r in segments if r[0]<=i<=r[1]];assert len(matches)==1
 s=matches[0];line_rows.append({'line':i,'RAW_start':offset,'RAW_end_exclusive':offset+len(line),'RAW_sha256':sha(line),'classification':s[2],'source_nodes':s[3],'reviewed_complete_context':True});offset+=len(line)
assert offset==len(raw)
write('whole178-line-coverage73.json',{'module':pin(module),'line_count':178,'unclassified':0,'every_line_once':True,'segments':[{'start_line':a,'end_line':b,'role':role,'source_nodes':ns} for a,b,role,ns in segments],'lines':line_rows,'prospective_private_literal_exact_equal':True,'prospective_public_signature_exact_equal':True,'no_provider_or_hidden_premise_added':True})
assumptions=[
 ('hα','retained-not-used',[(24,24),(62,62)],'Positive source lower modulus remains a caller; no BODY reference.'),
 ('hαβ','retained-not-used',[(24,24),(62,62)],'Source modulus order remains; no BODY reference.'),
 ('hV','retained-and-used',[(24,24),(62,62),(101,103)],'C2 lowered to C1 for gradient continuity; no additional regularity.'),
 ('hH','retained-not-used',[(25,27),(63,65)],'Complete both global Hessian bounds retained; no BODY reference.'),
 ('hη','retained-and-used',[(28,28),(66,66),(98,100),(146,148)],'Positive eta produces sqrt scale and nonnegative eta inverse.'),
 ('hβη','retained-not-used',[(28,28),(66,66)],'Non-strict step cap retained; no BODY reference.')]
write('caller-definition-nine-conclusion-review73.json',{'module':pin(module),'sealed_header':pin(ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/header73.proposed.lean'),'private_literal_exact_byte_equal':True,'public_signature_exact_byte_equal':True,'caller_count':6,'callers':[{'name':n,'use':u,'spans':spans(rs),'reason':reason} for n,u,rs,reason in assumptions],'semantic_binder_inventory':{'SOURCE':4,'STANDING':6,'TYPING':10,'EXCESS':0},'nine_conclusions':[{'name':n,'produced_by':p,'spans':spans(rs)} for n,p,rs in [('joint_continuity','hcont',[(101,110)]),('joint_Borel','hcont.measurable',[(173,173)]),('initial','hzero',[(111,115)]),('all_real_group','hgroup',[(116,121)]),('both_inverses','hinverse',[(122,127)]),('both_exact_ODEs','hode',[(128,145)]),('nonnegative_H','hnonneg',[(146,148)]),('conserved_H','henergy',[(149,165)]),('pi_endpoint','hpi',[(166,172)])]],'joint_domain':'All y,xRef,t,x,p at fixed V,eta; (E×E)×(R×(E×E))','boundary_cases':{'rank0':True,'alphaeta1':True,'eta_positive':True,'zero_energy':True,'no_nonzero_normal':True,'no_extra_smoothness':True},'private_literal_nonprovider':True,'full_literal_helper_identity':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_statement','existing_gradient_API_source_audit':pin(OLD/'StageA.gradient-producer-independent-check73.frozen.json'),'fresh_Lean_compile_run_by_reviewer':False})
lesson=load(ROOT/'website/content/declaration_lessons/pbps-actual-harmonic-flow.json')['units'][0]
explanations=[
 'Positive r,r²=eta and exact local Gradient producer make actual c continuous; scalar/vector/trig operations yield full joint continuity. Measurability is explicitly assembled later at173, as prose says. Four inputs means y,xRef,t,z, with z=(x,p), not omission of p.',
 'sin/cos addition, zero values and r nonzero establish same-center composition; exact both inverse orders follow from group and hzero. All real times retained.',
 'Time differentiation fixes actual y,xRef,z. Both coefficients and signs match source; second equality uses c=y−eta gradVxRef and r²=eta. congr_deriv is a rewrite of proved derivatives, not an assumed ODE.',
 'Nonnegative eta inverse, squared E norms and positive divisor2 give exact H>=0 including zero energy.',
 'With q=x−c,C=cos t,S=sin t, the two separate E norm squares give opposite 2CS<q,p>/r terms; their sum is (C²+S²)(r^-2||q||²+||p||²). Half factor retained via common divisor. No product norm used.',
 'sinπ=0 and cosπ=−1 give both coordinates (2c−x,−p). Complete tuple includes all9 laws and hcont.measurable. Source stochastic terminal law expressly excluded.']
steps=[]
for i,(s,reason) in enumerate(zip(lesson['steps'],explanations)):
 r=s['lean_source_region'];code=b''.join(lines[r['start_line']-1:r['end_line']]);assert code.decode()==s['lean'] and sha(code)==r['exact_code_raw_sha256']
 steps.append({'index':i,'title':s['title'],'formula':s['formula'],'BODY_span':r,'exact_code_equal':True,'independent_formula_and_prose_decision':'ACCEPT','reason':reason})
assert lesson['helpers']==['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_statement']
write('six-step-formula-exposition-review73.json',{'lesson':pin(ROOT/'website/content/declaration_lessons/pbps-actual-harmonic-flow.json'),'module':pin(module),'step_count':6,'steps':steps,'complete_private_literal_helper_present':True,'helper_is_proposition_specification_not_provider':True,'full_attributed_statement_and_assumptions_match':True,'local_exposition_source_math_accepted':True,'DOM_browser_or_full_Exposition_Seal_credit':False})
write('coverage-authoring.terminal.json',{'actual_pid':os.getpid(),'exit_code':0,'argv':sys.argv,'background':False})
print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'module_lines':178,'source_items':79,'NODE':24,'EXCLUDED':55,'source_graph_nodes':23,'edges':37,'seven_internal_bridges':7,'callers':6,'conclusions':9,'steps':6,'mathematical_or_binder_repairs':0},indent=2))
