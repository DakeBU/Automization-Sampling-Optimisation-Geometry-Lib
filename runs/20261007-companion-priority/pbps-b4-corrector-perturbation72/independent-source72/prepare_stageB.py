from pathlib import Path
import hashlib,json,os,sys,traceback
ROOT=Path('E:/Samplinglib')
OWN=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72/independent-source72'
PRIOR=ROOT/'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/independent-header-source72'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,obj):
 (OWN/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
code=0
try:
 assert not (OWN/'lease.final.json').exists()
 names=['stageA.source-expectations72.before-header.frozen.json','stageA.source-proof-graph72.before-header.frozen.json','stageA.finite-source255-plus-supplemental-coverage72.frozen.json','stageA.target20-exact-RAW-formulas72.frozen.json','stageA.all27-source-header-obligations72.frozen.json','stageA.anti-anchoring-exposure72.frozen.json','lease.final.json']
 inputs=[]
 for name in names:
  b=(PRIOR/name).read_bytes();lf=b.replace(b'\r\n',b'\n')
  inputs.append({'path':(PRIOR/name).relative_to(ROOT).as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(lf),'lf_sha256':sha(lf),'lf_recipe':'bytewise CRLF-to-LF only','copied':False})
 assert inputs[0]['raw_sha256']=='23d8ddf1bb30a0114a82c58d46b8a8167af9576cac562f02853e3d3fdc8e8993'
 assert inputs[1]['raw_sha256']=='c832bc2e1810f680468591ff82de7a182642756168e9130760f2e8b9f2db9ce7'
 assert inputs[2]['raw_sha256']=='fba9f40905b5412f743daceafcb69ad551bbb206dcddb7afd93a731d0c5a58cc'
 assert inputs[-1]['raw_sha256']=='881322b8b2abbf6293294d26447d92422b7429190999a2243dacb662f9a70430'
 expected=json.loads((PRIOR/names[0]).read_text(encoding='utf-8'))
 assert expected['source_graph_nodes']==24 and expected['source_graph_edges']==53
 assert expected['primary_math_count']+expected['supplemental_unique_math_count']==361
 assert expected['target_formula_count']==20
 obligations=json.loads((PRIOR/names[4]).read_text(encoding='utf-8'))
 assert obligations['count']==27 and len(obligations['entries'])==27
 write('preparation.inputs.json',{'schema':'source72-StageB-preparation-finite-prior-inputs-v1','prior_closed_bundle':'CLOSED254 immutable; no full replay or duplication','inputs':inputs,'current72_BODY_publication_decoder_verdict_inputs':[]})
 plan={
  'schema':'source72-two-unit-StageB-preparation-v1',
  'status':'READY_AWAITING_TWO_OFFICIAL_REVIEWER_PACKETS',
  'source_expectations':'Reuse immutable primary-first StageA361 / 24 nodes / 53 edges / 20 formulas / 27 obligations; source graph and existing NODE/EXCLUDED classifications unchanged.',
  'preparation_input_manifest':'preparation.inputs.json',
  'anti_anchoring':{'source_blind':False,'prior_exposure':['70 and71 complete implementation/source/publication','prospective72 generic and actual headers','bounded B27 source/reuse diagnosis'],'not_read_in_this_preparation':['current72 generic/actual BODY','other math or header-math verdicts','decoder results','root publication draft'],'body_exposure_prior_to_packets':False},
  'units':[
   {'unit':'generic','announced_lines_unread':54,'question':'Does the complete real-Hilbert algebra implementation establish precisely C(u+Gamma r,v-A r)-C(u,v)=inner(u,Inv r)+norm(r)^2/2 under the sealed primitive operator hypotheses?',
    'checks':['whole module, declarations, hypotheses, definitions, every proof/math line and exact publication BODY/formula spans','same inverse, real inner-product transport, cancellation, coefficient one-half and signs','no B21/actual rotation/sharp-energy68 dependency or result-as-premise provider','generic hypotheses remain honest leaf inputs; no actual algorithm, r_rho, K or B27 credit']},
   {'unit':'actual','announced_lines_unread':440,'question':'Does the complete actual PBPS consumer internally obtain the generic ingredients and append only the sealed universal perturbation conclusion while retaining all parent71 content?',
    'checks':['all six original analytic callers, twelve same witnesses and every old clause retained','same J/P/U/positive root/centered inverse/polar V; all kerP, no onto premise; rank0 and alphaeta1 retained','actual g=U(Pf-(f-Pf)), internal centering, genuine condExpL2 gP and V*Rg gV','exact specialization at actual gP/gV; arbitrary r remains distinct from source-produced r and r_rho','private literal is complete proposition definition/nonprovider, adjacent reader helper exposes its complete exact statement','no arbitrary H/invariance/nonexplosion/cost/mean premise and no invented sharp-energy68 parent; real H/K/B27/B28 remain open']}
  ],
  'coverage_plan':{
   'source':'Reference all 361 immutable item identities/classifications and all 24 nodes/53 edges; add per-unit dispositions (established/inherited/not-used/open/outside) with reasons without rewriting the source graph or reclassifying open consumers as proved.',
   'obligations':'Account individually for all O00-O26 and all20 source formula anchors; distinguish generic proof ingredients, actual internally produced ingredients, inherited facts and still-open real-algorithm consumers.',
   'implementation':'Exhaustive finite line/declaration/math-role coverage of both complete current modules once packet-authorized; source graph remains separate from Lean dependency relationships.',
   'publication':'Exact whole statement/private literal, each authored formula and exact BODY range, adjacent code and truthful scope/dependency metadata; no aggregate/browser credit inferred.',
   'roundtrip':'Read the two official packets first after decoder adoption; independently author every canonical semantic slot, compare exact decoder reconstruction, classify every delta using the existing canonical allowed classifications and fields, and pin exact packets/runs/publication bindings/review contexts.'
  },
  'minimal_outputs':{
   'shared':['bounded synthesis','finite RAW/LF input manifest and snapshots only for new current inputs','reference-only pins to immutable StageA/CLOSED254','complete named review/decision/input payload with no recursive historical base64','foreground terminal receipts','finite owned manifest','native whole-logical run hash deleting ONLY top-level run_sha256','last-write CLOSED_LAST lease followed only by read-only checks'],
   'each_unit':['source.0.review.RAW.md','source.0.decision.json in existing canonical semantic-roundtrip schema','source.0.admission-fields.json containing audit_fields(state/verdict/semantic_slots/deltas/source_review/repairs), official_packet_sha256 and portable publication_source_proof_coverage locators','finite source/obligation/line/formula/BODY coverage tables'],
   'decision_schema_rule':'Use the current canonical schema at dispatch, not a competing custom decision adapter. Keep unit/packet/run binding evidence in native records where permitted; no invented canonical fields.'
  },
  'repair_policy':'Freeze any exact mathematical/statement/reader overlay separately in this owned OPEN scope, notify root and await its independently reviewed application plus refreshed official packet before final closure; never silently edit canonical inputs.',
  'authorization_boundary':{'start_final_review_now':False,'waiting_for_two_canonical_packets':True,'source_fidelity_verdict_now':False,'proof_compile_SAU_SCI_VERIFIED_fullB4_paper_Goal_credit':False,'canonical_Git_ledger_old_closed_writes':False}
 }
 write('preparation.plan.json',plan)
 write('lease.open.json',{'state':'OPEN_PREPARATION_ONLY','owned_scope':OWN.relative_to(ROOT).as_posix(),'awaiting':'two canonical reviewer packets after independent decoder adoption','old_closed_immutable':True,'final_source_review_started':False})
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'status':plan['status'],'plan_raw_sha256':sha((OWN/'preparation.plan.json').read_bytes()),'prior_input_manifest_raw_sha256':sha((OWN/'preparation.inputs.json').read_bytes()),'prior_inputs':len(inputs),'stageA':'361/24nodes53edges/20formulas/27obligations unchanged'},indent=2))
except BaseException:
 code=1;traceback.print_exc()
finally:
 write('preparation.terminal.json',{'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False,'read_scope':'own prior source-first StageA/CLOSED254 evidence only; no current72 implementation/publication/decoder inputs','writes_scope':OWN.relative_to(ROOT).as_posix()})
sys.exit(code)
