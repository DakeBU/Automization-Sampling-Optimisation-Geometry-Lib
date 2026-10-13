from pathlib import Path
import hashlib,json,os,sys,traceback,copy
from collections import Counter
ROOT=Path('E:/Samplinglib');RUN=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73';OWN=RUN/'independent-header-source73'
OLD=ROOT/'runs/20261007-companion-priority/pbps-half-turn-construction-preread73';GRAPH=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-sourcegraph73'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':'CRLF-to-LF only; preserve all other bytes'}
def write(n,x):
 p=OWN/n;assert not p.exists(),str(p);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

# Independent source-facing judgments. This table was written only after direct
# primary13/51 reading and without opening the candidate header or its hash.
NODE_JUDGMENTS={
'STAND-C2':'S1.p1 explicitly assumes V in C2 globally. Retain hV exactly; derive C1/gradient continuity internally.',
'STAND-MODULI':'Source0<alpha<=beta is a standing condition. NNReal carriers plus hAlpha/hAlphaBeta preserve it; beta>0 follows internally.',
'STAND-HESSIAN':'The source two operator inequalities expand to both Frechet quadratic-form bounds for every x,v; no arbitrary Hessian or stronger derivatives.',
'STAND-STEP':'S2 scale interval0<eta<=1/beta converts to eta>0,beta*eta<=1 using original beta>0; no strict cap or eta=0 extension.',
'PARAMETERS':'Prop3.1 and A1 fix arbitrary y,xRef and arbitrary initial x,p. Sampling xRef and Gaussian p0 is outside this deterministic arc; fixed xRef is constant in time.',
'CENTER':'Source3.4 uses y-eta gradientV(xRef), the same queried gradient as Algorithm1 line3. It is a definition, not a free center premise.',
'POSITION':'Source3.6 prints X_t-c=cos(t)(x-c)+sqrteta sin(t)p. This is the no-bounce arc, not the full event-driven return.',
'PHASE-FLOW':'Source4.5 and A1 print both components with the same c/eta/initial phase point; P_t=-(sin t/sqrteta)(x-c)+cos(t)p. No arbitrary supplied flow.',
'ODE-X':'Algorithm1 line5 prints dx/dt=sqrteta p. Derivative equality is a future conclusion from literal Phi, never a certificate input.',
'ODE-P':'Algorithm1 line5 prints dp/dt=-(X-y)/sqrteta -sqrteta gradientV(xRef), not gradientV(X). Center conversion requires original eta>0.',
'INIT':'Actual arc starts at its supplied x,p. Phi0=(x,p) is an omitted evaluation, produced internally with sin0/cos0.',
'GROUP':'Source4.5 gives restart formula; all-real additive group/inverse is a declared source-derived extension, not a quoted paper theorem. It needs explicit SCALE reciprocal cancellation in addition to trig.',
'HALF-TURN':'Source3.7 prints Phi_pi=(2c-x,-p); position loses temporary momentum for the no-bounce arc. This is not random Algorithm1 x_pi.',
'ENERGY':'A1.Ex4 defines one-half of eta^-1 times the squared E position displacement plus squared E momentum. It is a weighted SUM, not a product max-norm square.',
'FLOW-ENERGY':'A1.p3 says flow and bounce preserve energy. Only the flow part is selected; the bounce part and path induction are excluded.',
'ENERGY-NONNEG':'Omitted background order bridge, not new hypothesis: exact ENERGY definition plus eta>0 and squared-norm nonnegativity. Add ENERGY dependency explicitly.',
'SCALE':'Omitted scalar bridge: r=sqrteta>0, r^2=eta, eta^-1=r^-2 and reciprocal cancellation. Internal source ingredient, not extra eta/sqrt nonzero caller.',
'TRIG':'Sine/cosine derivatives, addition/zero/pi and square-sum identities are omitted background dependencies. Future proofs must invoke/establish them; none is a public assumption.',
'NORM-CANCEL':'Omitted real inner-product expansion cancels opposite mixed terms in normalized coordinates. It proves the weighted sum identity and does not assert Prod max-norm preservation.',
'DERIVATIVE':'Omitted differentiation and actual-center conversion prove both ODE equations. Same fixed gradient and eta coefficients must persist.',
'GRAD-CONT':'C2 lowers to C1; current canonical Calculus.Gradient.continuous_gradient_of_contDiff_one provides Continuous gradient on a complete real Hilbert space. Finite dimension supplies completeness internally. Existing producer, future73 application, no new regularity premise.',
'JOINT-CONT':'At fixed positive eta, literal formula and internally continuous gradient imply joint continuity in y,xRef,t,x,p, hence Borel. This strengthening is explicitly source-derived, not printed in selected13 ranges.',
'SELECTED-ANCHOR':'Bounded deterministic actual-flow interface only: literal definitions, continuity/Borel, initial/group/inverse/pi, exact two derivatives and nonnegative/invariant H. No Prop3.1/full algorithm completion.'}

def exclusion_judgment(e):
 k=int(e['id'].split('-')[1])
 if k<=9:return 'Correctly outside deterministic arc: measure/augmentation/conditional distribution, citation or sampling-cost context supplies no public premise or new flow proof credit.'
 if k in [10,11,16,17,23,24,25,26,27,28,29,36]:return 'Correct future bounce/rate exclusion. Preserve R0=id, possible normal-zero discontinuity, and lambda=0 there. No continuous bounce/normal-nonzero hypothesis is licensed.'
 if k in [12,13,14,15,18,19,20,21,22]:return 'Correct algorithm/process exclusion. Fixed deterministic arc and its pi evaluation do not produce sampling, event-driven path, stationarity, a.s. terminal state or cost.'
 if 30<=k<=50:return 'Correct future hazard/clock/recursion/nonexplosion exclusion. Flow energy alone supplies neither path-wide bounds nor integrated-hazard thresholds, iid laws, SLLN application, Markov property or invariance.'
 return 'Correct future kernel/operator exclusion. Joint continuity of deterministic Phi does not construct a jointly Borel terminal half-turn kernel or selfadjoint L2 Markov contraction.'

code=0
try:
 assert not (OWN/'lease.final.json').exists()
 primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=primary.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 g=load(GRAPH/'source-proof-graph.json');c=load(GRAPH/'source.coverage.json');b=load(GRAPH/'binder-audit.json');src=load(GRAPH/'source.blocks.json')
 assert set(NODE_JUDGMENTS)=={n['id'] for n in g['nodes']}
 blockmap={z['block_id']:z for r in src['regions'] for z in r['blocks']};nodes={n['id']:n for n in g['nodes']};ex={e['id']:e for e in g['excluded_items']}
 items=[];blocks=[]
 for r in c['blocks']:
  z=blockmap[r['source_block_id']];a,bb=z['raw_byte_start_inclusive'],z['raw_byte_end_exclusive'];assert sha(raw[a:bb])==z['literal_span_raw_sha256']
  assert r['literal_source_anchor']['literal_span_raw_sha256']==z['literal_span_raw_sha256']
  for s in r['subitems']:
   why=NODE_JUDGMENTS[s['node_id']] if s['disposition']=='NODE' else exclusion_judgment(ex[s['excluded_id']])
   items.append({'source_block_id':r['source_block_id'],'semantic_subitem':s['semantic_subitem'],'source_claim':s['claim'],'original_disposition':s['disposition'],'independent_disposition':s['disposition'],'identity':s.get('node_id',s.get('excluded_id')),'direct_RAW_start':a,'direct_RAW_end_exclusive':bb,'direct_RAW_sha256':z['literal_span_raw_sha256'],'independent_source_comparison':why,'classification_accepted':True,'future_proof_credit':False})
  blocks.append({'source_block_id':r['source_block_id'],'direct_RAW_sha256':z['literal_span_raw_sha256'],'subitem_count':len(r['subitems']),'all_semantic_subitems_reviewed':True})
 assert len(items)==79 and len(blocks)==51 and Counter(x['independent_disposition'] for x in items)=={'NODE':24,'EXCLUDED':55}
 write('StageA.independent-source79-classification73.frozen.json',{'schema':'source73-distinct-independent-source-coverage-before-header-v1','source_coverage_input':pin(GRAPH/'source.coverage.json'),'primary':pin(primary),'region_count':13,'block_count':51,'semantic_item_count':79,'NODE':24,'EXCLUDED':55,'unclassified':0,'blocks':blocks,'items':items,'NODE_contract':'source relevant, not compiled/proved or source-topology accepted without the explicit dependency repair','outside_selected13':'Future AppendixA.1 stationarity remainder, A.2 proof and A.3 costs/caps, AppendixB H1/B2/B27/B28/main are not silently covered.'})
 edge_rows=[]
 for i,e in enumerate(g['edges']):
  assert e['producer'] in nodes and e['consumer'] in nodes
  edge_rows.append({'original_edge_index':i,'producer':e['producer'],'consumer':e['consumer'],'source_use_site':e['consumer_source_use_site'],'independent_decision':'ACCEPT_SOURCE_DEPENDENCY_NOT_COMPILED_LEAN_EDGE','source_comparison':e['use'],'hypothesis_to_binder_promoted':False})
 assert len(edge_rows)==35
 gap_rows=[]
 for s in g['source_gap_node_ids']:
  gap_rows.append({'node_id':s,'independent_meaning':NODE_JUDGMENTS[s],'status':'EXISTING_LOCAL_PRODUCER_FOUND_FUTURE_INTERNAL_APPLICATION' if s=='GRAD-CONT' else 'PAPER_OMITTED_BRIDGE_FUTURE_INTERNAL_PROOF_OBLIGATION','extra_public_binder_allowed':False,'compiled73_credit':False})
 write('StageA.independent-node23-edge35-gap7-review73.frozen.json',{'schema':'source73-independent-topology-before-header-v1','source_graph_input':pin(GRAPH/'source-proof-graph.json'),'nodes':[{'node_id':n['id'],'kind':n['kind'],'independent_source_comparison':NODE_JUDGMENTS[n['id']],'decision':'ACCEPT_NODE_AS_SOURCE_DEFINITION_HYPOTHESIS_QUANTIFIER_OR_INTERNAL_OBLIGATION','compiled73_credit':False} for n in g['nodes']],'original_edges':edge_rows,'source_gaps':gap_rows,'required_two_edge_overlay':pin(OWN/'sourcegraph-edge-overlay73/proposal.json'),'original35_edge_topology_approval':'NEEDS_TWO_EXPLICIT_DEPENDENCY_EDGES','prospective37_edge_topology_approval':'PENDING_DISTINCT_REPAIR_REVIEW; proposal author does not self-approve','graph_vs_header':'No current73 header or its hash has been read; this is source topology only.'})
 binderrows=[]
 for i,x in enumerate(b['items']):
  why=x['justification']
  if x['name']=='s,t':why='TYPING describes real time carrier only; all-real group/negative-time inverse is an explicitly reconstructed extension justified from literal trig formula, not printed source full process time. No added time premise.'
  elif x['classification']=='STANDING':why='Independently matches original source-wide field at listed exact source blocks. '+x['justification']
  elif x['classification']=='SOURCE':why='Independently matches arbitrary fixed-reference/initial-state quantification in Prop3.1/A1; no distribution premise. '+x['justification']
  else:why='Faithful representation of finite real Euclidean/Borel source carrier and its existing parameters. '+x['justification']
  binderrows.append({'prospective_item':i,'name':x['name'],'surface':x['exact_prospective_surface'],'classification':x['classification'],'source_anchors':x['source_anchors'],'independent_decision':'ACCEPT_PROSPECTIVE_CLASSIFICATION_ONLY','independent_source_comparison':why,'current73_binder_actually_read':False})
 assert len(binderrows)==20 and Counter(x['classification'] for x in binderrows)=={'SOURCE':4,'STANDING':6,'TYPING':10}
 write('StageA.independent-binder20-review73.frozen.json',{'schema':'source73-distinct-prospective-binder-source-contract-v1','source_binder_input':pin(GRAPH/'binder-audit.json'),'items':binderrows,'counts':{'SOURCE':4,'STANDING':6,'TYPING':10,'EXCESS':0},'all_source_wide_fields_expanded':True,'hH_expands':'both inequalities for all x,v; no derivative order beyond C2','current73_header_not_read':True,'must_never_be_new_binders':['gradient continuity','gradient beta-Lipschitzness','sqrteta or eta nonzero convenience premise','arbitrary center/flow/ODE/energy provider','Nontrivial E or positive rank','strict alphaeta<1 or betaeta<1','nonzero bounce normal','probability/reference normalization','PDMP/nonexplosion/invariance/terminal kernel','onto polar map or centered inverse or72 algebra certificate','higher derivatives']})

 reuse=load(GRAPH/'reuse.gradient-continuity.json');api=ROOT/reuse['producer']['path'];api_raw=api.read_bytes();assert sha(api_raw)==reuse['producer']['raw_sha256']
 aa,bb=reuse['raw_byte_start_inclusive'],reuse['raw_byte_end_exclusive'];assert sha(api_raw[aa:bb])==reuse['literal_span_raw_sha256']
 assert api_raw[aa:bb]==(GRAPH/'gradient-continuity.statement.exactraw.txt').read_bytes()
 consumers=[]
 for z in reuse['actual_existing_consumers']:
  p=ROOT/z['path'];r=p.read_bytes();assert sha(r)==z['whole_file_raw_sha256'];a0,b0=z['raw_byte_start_inclusive'],z['raw_byte_end_exclusive'];assert sha(r[a0:b0])==z['literal_span_raw_sha256'];assert r[a0:b0].decode()==z['exact_call_utf8'];consumers.append({'path':z['path'],'RAW_start':a0,'RAW_end_exclusive':b0,'RAW_sha256':z['literal_span_raw_sha256'],'exact_current_call':z['exact_call_utf8'],'whole_module_not_reaudited':True})
 write('StageA.gradient-producer-independent-check73.frozen.json',{'producer':pin(api),'declaration':reuse['declaration'],'signature_RAW_start':aa,'signature_RAW_end_exclusive':bb,'signature_RAW_sha256':reuse['literal_span_raw_sha256'],'exact_signature':api_raw[aa:bb].decode(),'proof_body_read':'exact toDual.symm.continuous.comp (hf.continuous_fderiv one_ne_zero); local namespace/import context read; no admitted mathematics','required_input':'ContDiff real1 V and CompleteSpace E; actual hV real2 lowers internally, finite dimension supplies completeness','existing_consumers':consumers,'73_compiler_run':False,'new73_proof_credit':False,'existing_API_source_verified':True,'future73_must_apply_internally':True})
 expectations={'schema':'source73-independent-before-header-expectations-v1','status':'FROZEN_SOURCE_EXPECTATIONS_BEFORE_CURRENT_HEADER_OR_HASH_READ','primary':pin(primary),'six_original_callers':['hα:0<(α:ℝ)','hαβ:α≤β','hV:ContDiff ℝ 2 V','hH:∀x v,α‖v‖²≤D²V(x)[v,v] ∧ D²V(x)[v,v]≤β‖v‖²','hη:0<η','hβη:(β:ℝ)*η≤1'],'center':'c=y−η•gradient V xRef; same actual cached gradient, no free center/provider','literal_flow':{'X':'c+cos(t)•(x−c)+(sqrt(η)*sin(t))•p','P':'(−sin(t)/sqrt(η))•(x−c)+cos(t)•p'},'ODE':{'Xprime':'sqrt(η)•P_t','Pprime':'−(sqrt(η))⁻¹•(X_t−y)−sqrt(η)•gradient V xRef','quantifiers':'fixed y,xRef,x,p; derivative with respect to real time only'},'energy':'H=(η⁻¹*‖x−c‖²+‖p‖²)/2, weighted SUM of E norm squares; H≥0 and H(Phi_t z)=H(z)','other_required_outputs':['joint continuous map(y,xRef,t,x,p) at fixed positive eta, hence Borel','Phi0(z)=z','Phi_(s+t)(z)=Phi_s(Phi_t(z)) for all real s,t, same inverse Phi_(-t)','Phi_pi(x,p)=(2•c−x,−p), no temporary momentum in position'],'source_derived_extensions_not_verbatim_paper':['joint full parameter continuity/Borel theorem','all-real group and inverse packaging','energy nonnegativity check'],'edge_overlay_required':pin(OWN/'sourcegraph-edge-overlay73/proposal.json'),'edge_overlay_admission':'distinct review pending, no self-approval','seven_omitted_bridges':'ENERGY-NONNEG,SCALE,TRIG,NORM-CANCEL,DERIVATIVE,GRAD-CONT,JOINT-CONT remain internal edges/obligations; existing gradient API resolved as source reuse, no fresh73 proof','rank0':'allowed zero-dimensional carrier; all vectors/gradient/norms0, phase singleton flow identity and energy0; no Nontrivial','alphaeta1':'allowed by original <= cap; no divide by1−alphaeta or strict endpoint','eta_positive':'required source scale; no extension at eta=0','zero_energy':'initial(c,0) fixed, no division by energy','future_zero_normal':'bounce excluded; preserve R0=id and rate0, possible discontinuity not joint continuity','future_exclusions':['random reference/momentum initialization','bounce/rate map and Borel-at-zero proofs','integrated hazards and threshold/clock measurability','iid Exp1 realization/finite-jump recursion/SLLN/nonexplosion/uniqueness/Markov','path-reversal/stationarity/invariance','actual terminal kernel H_y/augmented H/H1/B2/B27/B28','main/live/fullpaper/errors/caps/query-cost/composition/Goal'],'no72_parent':'selected deterministic phase flow is not derived from polar/corrector/72 perturbation algebra; no old twelve-witness inheritance is required','anti_anchoring':{'source_blind':False,'prior_exposure':['70/71 full source/BODY/publication','72 prospective and complete final source/implementation/publication review','earlier bounded B27 source/reuse diagnosis'],'current73_header_or_hash_read':False,'current73_BODY_read':False,'other73_verdicts_read':False,'new72_review_source_conclusions_read':False,'extractor_material':'Authorized independently extracted source graph/classifications read as claims to check, not topology authority'},'before_header_freeze_artifacts':['StageA.independent-source79-classification73.frozen.json','StageA.independent-node23-edge35-gap7-review73.frozen.json','StageA.independent-binder20-review73.frozen.json','StageA.gradient-producer-independent-check73.frozen.json'],'claims_granted_now':'Independent before-header source expectations/classifications only, subject to distinct two-edge repair admission; no header/proof/source-implementation/SAU/SCI/VERIFIED/PURIFIED/fullpaper credit'}
 write('StageA.source-expectations73.before-header.frozen.json',expectations)
 decision={'schema':'source73-distinct-independent-before-header-topology-decision-v1','status':'SOURCE_CLASSIFICATIONS_AND_BINDER_CONTRACT_ACCEPTED_TOPOLOGY_TWO_EDGE_REPAIR_PENDING','reviewer':'independent_primary69','extractor':'exact_science63','independent_from_extractor':True,'source_primary13regions51blocks79items_compared':True,'classification_counts':{'NODE':24,'EXCLUDED':55},'source_nodes':23,'original_source_edges_reviewed':35,'source_gaps':7,'prospective_binders':{'SOURCE':4,'STANDING':6,'TYPING':10,'EXCESS':0},'required_repairs':[{'producer':'SCALE','consumer':'GROUP'},{'producer':'ENERGY','consumer':'ENERGY-NONNEG'}],'repair_proposal':pin(OWN/'sourcegraph-edge-overlay73/proposal.json'),'repair_approved_by_this_author':False,'prospective37_edge_acceptance':'await independent reviewer-specific repair evidence, then adopt explicit finite overlay without rewriting CLOSED49','source_expectations':pin(OWN/'StageA.source-expectations73.before-header.frozen.json'),'source_classification':pin(OWN/'StageA.independent-source79-classification73.frozen.json'),'node_edge_gap_review':pin(OWN/'StageA.independent-node23-edge35-gap7-review73.frozen.json'),'binder_review':pin(OWN/'StageA.independent-binder20-review73.frozen.json'),'gradient_reuse':pin(OWN/'StageA.gradient-producer-independent-check73.frozen.json'),'exact_candidate_header_or_hash_read':False,'header_or_math_admission':False,'old_CLOSED_canonical_Git_ledger_Goal_writes':False,'scope_remains_OPEN':True}
 write('StageA.topology-decision73.before-header.frozen.json',decision)
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'expectations':pin(OWN/'StageA.source-expectations73.before-header.frozen.json'),'topology_decision':pin(OWN/'StageA.topology-decision73.before-header.frozen.json'),'classification':pin(OWN/'StageA.independent-source79-classification73.frozen.json'),'binder_review':pin(OWN/'StageA.independent-binder20-review73.frozen.json'),'two_edge_repair_pending':True,'header_or_hash_read':False},indent=2))
except BaseException:code=1;traceback.print_exc()
finally:
 p=OWN/'StageA.author-expectations.terminal.json';p.write_text(json.dumps({'actual_pid':os.getpid(),'exit_code':code,'argv':sys.argv,'background':False},indent=2)+'\n',encoding='utf-8',newline='\n')
sys.exit(code)
