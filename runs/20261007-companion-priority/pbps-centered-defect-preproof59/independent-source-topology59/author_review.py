from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, json, sys
sys.stdout.reconfigure(encoding='utf8')
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;C=O.parent
OLD=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57'
OWN=R/'runs/20261007-companion-priority/phase-pbps-next-primary59'
sha=lambda b:hashlib.sha256(b).hexdigest()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),
 'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def put(n,x):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());assert json.loads(p.read_bytes())==x;return pin(p)
candidate=json.loads((C/'statement-candidate.json').read_bytes())
for x in candidate['headers']:
 assert pin(R/x['path'])==x
 assert b':= by' not in (R/x['path']).read_bytes()
assert pin(OWN/'source.contract.json')==candidate['primary_source_contract']
inputs=[OWN/'source.contract.json',OWN/'primary.anchors.json',C/'statement-candidate.json',
 C/'header0.lean',C/'header1.lean',R/'AutoSamplingTheory/TechnicalLemmas/Measure/L2Expectation.lean',
 R/'.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean',
 R/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean',
 R/'docs/proof-digestion-protocol.md',R/'docs/theorem-publication-protocol.md']
(O/'inputs').mkdir(exist_ok=True)
indexed=[]
for i,p in enumerate(inputs):
 op=O/'inputs'/f'{i:03d}.{p.name}.exactraw.snapshot';assert not op.exists();op.write_bytes(p.read_bytes())
 indexed.append({'index':i,'qualified_input':pin(p),'qualified_immutable_snapshot':pin(op),
 'copy_exact':p.read_bytes()==op.read_bytes()})
put('indexed-input.manifest.json',{'schema_version':1,'inputs':indexed,
 'large_primary_reused_without_copy':pin(OLD/'primary-pbps.exactraw.snapshot.html'),
 'own_source_before_current_candidate':pin(O/'primary.source-first.json'),
 'source_graph_before_current_candidate':pin(O/'source-graph.pre-candidate.json')})

s=(OLD/'extract_and_freeze_primary.py').read_text();d={'HTMLParser':HTMLParser};exec(s[s.index('class Parser'):s.index('b=(OLD/')],d)
raw=(OLD/'primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
t=raw.decode();p=d['Parser']();pos=0
for l in t.splitlines(keepends=True):p.offsets.append(pos);pos+=len(l)
p.feed(t)
ids=['S1.p1','S2.E6','S2.E7','A2.SS1.p1','A2.SS1.p2','A2.SS1.p3',
 'A2.E8','A2.E9','A2.Thmtheorem1.p1','A2.E12','A3.SS1.p1','A3.SS1.p2','A3.SS1.p3']
rows=[]
for id in ids:
 n=next(n for n in p.nodes if n['attrs'].get('id')==id);b=t[n['start']:n['end']].encode()
 rows.append({'id':id,'start_utf8_byte':len(t[:n['start']].encode()),'end_utf8_byte_exclusive':len(t[:n['end']].encode()),
 'slice_bytes':len(b),'slice_sha256':sha(b),'balanced':True,'text':' '.join(d['txt'](n).split())})
put('primary.supplemental-context.json',{'schema_version':1,'primary':pin(OLD/'primary-pbps.exactraw.snapshot.html'),
 'exact_regions':rows,'reason':'Complete meaning-carrying model/conditional-density/source proof context for the already selected source slice; no59 implementation read.',
 'current_candidate_headers_read':True,'implementation_read':False})

g=json.loads((O/'source-graph.pre-candidate.json').read_bytes())
g.pop('source_graph_sha256')
g['status']='INDEPENDENT_EXTRACTION_ONLY_PENDING_DISTINCT_COVERAGE_REVIEW'
g['parent_source_only_graph']=pin(O/'source-graph.pre-candidate.json')
g['candidate_headers_read_after_primary_graph']=True;g['candidate_read']=True
g['source_topology_self_approval']=False
g['source_definition_dictionary']={
 'source_generic_mathsfT':'Generic operator in B3, distinct from local scalar conditional T.',
 'source_macroA':'U_PP=PUP acting on H_P; ambient joint PUP uses P in its defect, not full ambient identity.',
 'local_scalarT':'Same conditional mean transported by actual isometric snd M; MT=AM.',
 'local_q':'AE class1, source D1 real L2 convention. Existing L2Expectation.one supplies it after actual probability is derived.',
 'local_H0':'ker(innerSL real q), exact integral-zero scalar L2; not unbounded gradient domain.',
 'local_T0':'Actual whole-domain bounded restriction to H0, not a projected surrogate.',
 'D_D0':'Literal1-T*T and1-T0*T0; no eta scalar, no gradient or resolvent.',
 'Gamma':'Excluded actual nonnegative root, not defined by current signatures.'}
for node in g['nodes']:
 if node['id']=='S:model':node['anchor']='S1.p1/(1.1),S2.E6/E7,B12 cap'
 if node['id']=='S:A':node['anchor']='A2.SS1.p2/p3, B3/B4/B5'
 if node['id']=='S:M':node['current_use']='Actual59 needs forward PM=M/isometry;58 independently supplies reverse/full macro range for sharp Test transport. No new59 onto theorem claimed.'
 if node['id']=='A:D0':node['statement']='Authored actual positive full D=I-T² and positive centered D0=I-T0², exact subtype restriction and quadratic norm defects.'
 for e in g['edges']:
  pass
for e in g['edges']:
 e['consumer_use_site']={
 'A:T':'header0 IsSelfAdjoint T and PM=M,MT=AM',
 'A:mean':'header0 literal AE Tu and integralTu=integralu/q constant pairing',
 'A:T0':'header0 exact H0 membership/T0 subtype action/selfadjointness',
 'A:D0':'header0 full/centered IsPositive and quadratic identities',
 'A:delta':'header1 SAME actual centered normrho and delta quadratic bound',
 'A:unitD0':'header1 IsUnit(1-T0*T0)',
 'S:Gamma':'EXCLUDED root construction/B11',
 'S:rootgap':'EXCLUDED Gamma Loewner bound/B15',
 'S:polar':'EXCLUDED Gamma inverse/polar B16'}.get(e['to'],'Printed source '+e['to'])
 e['conditional_discharge']='Original source standing binders retained; operator/probability/centering facts proved internally from actual parents, not public premises.'
 if e['from']=='S:D' and e['to']=='A:D0':
  e['truth']='source-correspondence-only, not a required AND premise: actual scalar positivity route uses selfadjoint contractions'
g['proof_routes']=[
 {'id':'route:actual-scalar-defect','operator':'AND','parents':['A:T','A:T0'],'conclusion':'A:D0',
 'consumer_use_site':'header0 positive D,D0 and norm defects','selected':True,
 'meaning':'Actual selfadjoint contractive scalar operators yield positive squared defects. B5 is source correspondence, not an additional required proof input.'},
 {'id':'route:stationary-mean','operator':'AND','parents':['S:stationary','A:T'],
 'conclusion':'A:mean','consumer_use_site':'header0 integralTu identity','selected':True,
 'discharge':'Actual55 Lambda.IsCondKernel S, Lambda.fst=Lambda.snd=nu and L2L1 supply stationarity/integrability internally.'},
 {'id':'route:actual58-sharp','operator':'AND','parents':['S:rho','A:T0','A:D0'],
 'conclusion':'A:delta','consumer_use_site':'header1 exact rho/delta on actual centered H0','selected':True,
 'discharge':'Same U from literal reflection AE, same M from snd AE, same T via injective M/conditional mean; actual58 allmacro contraction already produces S:rho.'},
 {'id':'route:centered-squared-unit','operator':'AND','parents':['A:delta','S:realL2'],
 'conclusion':'A:unitD0','consumer_use_site':'header1 IsUnitD0','selected':True,
 'discharge':'H0 is complete kernel of continuous mean; delta>0 fromoriginalalphaeta, no Nontrivial assumption.'}]
g['route_semantics']='Edges express source ingredients/correspondence with explicit selected route hyperedges; do not turn the nonselected block-correspondence edge into a false AND.'
g['source_graph_sha256']=sha(canon(g));put('source-proof-graph.json',g)

# Every mathematical claim/definition/display/citation/substantive region in the bounded selected context is NODE or EXCLUDED.
coverage=[]
def node(i,a,k,n,use):coverage.append({'item_id':i,'source_anchor':a,'source_kind':k,'disposition':'NODE','node':n,'consumer_use_site':use,'formal_completion_claim':False})
def excluded(i,a,k,reason):coverage.append({'item_id':i,'source_anchor':a,'source_kind':k,'disposition':'EXCLUDED','reason':reason,'formal_completion_claim':False})
node('model-mu-V','S1.p1','definition/standing-assumptions','S:model','Both headers original V/C2/alpha/beta/Hessian binders and defined actual mu')
excluded('model-kappa','S1.E1','defined-parameter','Condition number kappa is not consumed or concluded by59.')
node('actual-joint-density','S2.E6','source-definition','S:model','mu/J/nu in both headers; pushforward form uses (2.7).')
node('actual-independent-augmentation','S2.E7','source-definition','S:model','Literal Gaussian-product map, no caller law or normalization.')
excluded('ideal-chain-K','A2.SS1.p1/(3.11)','definition/reused-display','Ideal PBPS transition K/halfturn mixing is not constructed or claimed.')
excluded('halfturn-proposition3.2','A2.SS1.p1','reused-result','Halfturn branch not used by current scalar/reflection adapter.')
excluded('observable-K','A2.SS1.p1','operator-definition','K observable/law distinction retained as context only; no59 dynamics.')
node('conditional-P-B1','A2.E1','source-definition/display','S:P','header0 exact conditionalY projection P; actual55 conditional representation parent.')
node('macro-range-B2','A2.E2','source-definition/display','S:M','header0 M/PM=M; exact reverse-range from58 used by Test, not reproved here.')
excluded('micro-kernel-B2','A2.E2','source-definition','Microspace kerP/ran(I-P) remains background context; current signature has no micro operator.')
excluded('micro-macro-decomposition','A2.SS1.p1','substantive-definition','Joint orthogonal decomposition is source context; no59 new decomposition theorem.')
excluded('hypocoercivity-citation14','bib.bib18','external-citation','DMS15 only accompanies source terminology here; no theorem imported as spectral/root premise.')
excluded('hypocoercivity-citation21','bib.bib19','external-citation','LW22 only accompanies source terminology here; no theorem imported as spectral/root premise.')
node('macro-block-B3','A2.E3','source-definition/display','S:A','header0 PUP scalar intertwining; source generic mathsfT not local scalarT.')
excluded('other-three-blocks-B3','A2.E3','source-definition/display','Other block maps and all off-diagonal domain labels are not new59 conclusions; source types retained.')
node('reflection-B4','A2.E4','source-definition/display','S:U','header0 SAME actual AE reflection U.')
node('reflection-unitary-adjoint','A2.SS1.p3','substantive-operator-claim','S:U','actual55 U isometry/involution/selfadjoint; no new premise.')
node('macro-selfadjoint-contraction','A2.SS1.p3','substantive-proof-step','S:A','Actual scalarT real-inner transport, then bounded centered restriction.')
node('positive-block-defect-B5','A2.E5-first-identity','reused-display/identity','S:D','Correspondence for positive squared defect; current route derives via scalar symmetry/norm.')
excluded('offdiagonal-block-B5','A2.E5-second-identity','reused-display/identity','B*U_perpperp=-A*B* is not consumed or proved by59.')
node('Yplus-Yminus-B8','A2.E8','source-definition/display','S:stationary','Actual Lambda law of(Y+,Y-), both marginalsnu; stationarity internally from55.')
node('conditional-scalar-B9','A2.E9-first-identity','source-characterization','A:T','header0/header1 literal conditional mean after SAME actual S density.')
excluded('conditional-variance-B9','A2.E9-second-identity','source-identity','Already actual55/58 norm defect parent context; no new59 variance theorem.')
node('literal-reflected-density','A3.SS1.p2-first-density','source-definition','A:T','Exact -V((y+u)/2)-norm(y-u)^2/(8eta) in both headers.')
excluded('score-gradient-C1','A3.SS1.p2-score/C1','definition/estimate','Source score/conditional covariance derivative not used as a new59 proof;56/57/58 supply already admitted sharp parent.')
excluded('smooth-density-gradient','A3.SS1.p1','substantive-proof-step','Weighted weakH1/density/closedness is not newly proved or identified by59.')
excluded('conditional-Hessian-C2','A3.SS1.p3','substantive-estimates','Conditional PI/score-Jacobian/Cauchy-Schwarz/density proof belongs earlier56/57 parent, not59.')
node('C2-parent-reuse','A3.SS1.p3/(C.2)','reused-display','S:rho','Already57/58 sharp parent; never a caller gradient/PI certificate.')
node('real-L2-D1','A4.SS1/DefinitionD1','source-definition','S:realL2','AE quotient L2(real), norm/inner; q canonical AE1 and pairing.')
node('mean-zero-D2formula','A4.SS1/(D.2)','source-definition','S:centered','Exact H0=ker(innerSL q) membership=integralzero, bounded complete subspace.')
node('closed-orthogonal-projection','A4.SS1/DefinitionD1','source-definition','S:P','Actual P orthogonal projection; no caller projection certificate.')
node('bounded-adjoint-conventions','A4.SS1/DefinitionD1','source-definition','S:A','Selfadjoint T/T0 and bounded whole-domain norm contractions.')
node('unitary-involution-convention','A4.SS1/DefinitionD1','source-definition','S:U','Actual U from55; no standalone new general lemma.')
node('Loewner-positive-D3','A4.SS1/(D.3)','source-definition','S:D','IsPositive D/D0 equals nonnegative quadratic form over realHilbert; no Gamma sqrt.')
excluded('spectral-Borel-calculus','A4.SS1/DefinitionD1','source-background-convention','Source spectral/Borel calculus/unique positive root not constructed or supplied in59.')
node('stationary-Markov-D4','A4.SS1/DefinitionD2/(D.4)','source-definition/convention','S:stationary','Actual stationary S from disintegration gives bounded mean and fixes q.')
node('Markov-constants-adjoint','A4.SS1/DefinitionD2','substantive-claim','A:mean','Tq=q and mean preservation discharged internally using actual law; selfadjoint not merely constants.')
excluded('density-adjoint-evolution','A4.SS1/DefinitionD2','substantive-claim','No density evolution/Markov K* theorem in59.')
excluded('chi2-D5','A4.SS1/(D.5)','display/claim','No chi2/mixing estimate or target-distance conclusion.')
node('source-centered-C3','A3.SS1.p4/(C.3)','substantive-step/reused-display','S:rho','Centering+actualnu PI belongs57/58. Current59 mean preservation separately explicit and no new PI proof.')
node('source-rho-C4','A3.SS1.p4/(C.4)','source-conclusion/display','S:rho','header1 consumes58 SAME real macro contraction with exact rho.')
excluded('spectral-interval-after-C4','A3.SS1.p4','substantive-consequence','No59 Loewner interval theorem A in[-rho,rho] or spectral calculus.')
excluded('negative-half-bound','A3.SS1.p4/A2.Thmtheorem1.p3/(B.14)','substantive-source-claim','A>=-I/2 independent later branch; neither header claims or assumes it.')
excluded('exchangeability-C5','A3.SS1.p4/(C.5)','display/claim','Later Gaussian difference/negative-spectrum bound branch, no59 new result.')
excluded('Gaussian-PI-unnumbered','A3.SS1.p4-after-C5','substantive-unnamed-estimate','Conditional Gaussian-gradient estimate is outside59 edge; no added gradient premise.')
excluded('difference-C6','A3.SS1.p4/(C.6)','display/claim','Independent H1 negative-spectrum branch excluded.')
node('rho-gamma-constants-B12','A2.Thmtheorem1.p1/A2.E12','source-constant-definition','S:rho','rho exact; delta=1-rho²=4t/(1+t)² is authored algebraic consequence. gamma constant retained only as excluded future root interpretation.')
excluded('rough-gradient-B13','A2.Thmtheorem1.p2','source-claim','Full sourceH1 equivalence and Gamma B13 are not current59 conclusions.')
excluded('Gamma-B10','A2.SS2.p3/A2.E10','source-definition/display','Gamma unique nonnegative allmacro root, no eta; current D is squared defect only.')
excluded('Gamma-B11','A2.SS2.p3/A2.E11','source-display/conclusion','Root norm equality B11 is not proved by D positivity alone.')
excluded('microscopic-transfer-paragraph','A2.SS2.p3-after-B11','substantive-interpretation','No new59 positive-root microscopic-direction size result.')
excluded('Gamma-gap-B15','A2.Thmtheorem1.p3/A2.E15','source-conclusion/display','header1 delta lower bound concerns D0, not Gamma Loewner lower bound.')
excluded('Gamma-inverse-B16','A2.SS2.p5/A2.E16','source-definition/display/conclusion','IsUnit D0 does not defineGamma inverse/polar V; B16 isometry only into micro remains open.')
excluded('halfturn-direction-paragraph','A2.SS2.p5-after-B16','substantive-claim','Halfturn spectral/inverse/domain result remains excluded.')
put('source-coverage.manifest.json',{'schema_version':1,
 'status':'EXHAUSTIVE_BOUNDED_EXTRACTION_PENDING_DISTINCT_REVIEW','scope':'Exact source regions in primary.source-first and primary.supplemental-context; requested B1-B5,D1-D2,C3-C4,B10/B11/B15/B16 plus meaning-carrying dictionary contexts. No whole-paper coverage claim.',
 'primary_regions':pin(O/'primary.source-first.json'),'supplemental_regions':pin(O/'primary.supplemental-context.json'),
 'graph':pin(O/'source-proof-graph.json'),'items':coverage,'item_count':len(coverage),
 'NODE_count':sum(x['disposition']=='NODE' for x in coverage),'EXCLUDED_count':sum(x['disposition']=='EXCLUDED' for x in coverage),
 'extractor':'/root/next_primary59','self_approval':False,'distinct_reviewer_expected':'/root/whole_math52',
 'exclusions_outside_direct_raw_selected_regions':'B13/H1/full algorithm/dynamics/cost source obligations remain open; no completion credit inferred from no raw in-scope proof.',
 'compiler_admission':False})

definition_audit=[
 {'object':'mu/J/nu/Lambda/F','kind':'literal','assessment':'Normalized exp(-V) target and actual independentGaussian augmentation; Lambda reflected pair, nu same actual marginal. Probabilities are outputs.'},
 {'object':'P','kind':'literal/quotient','assessment':'Actual conditional-Y projection on real joint L2 classes; condExpL2/lpMeas structural producer; not arbitrary projection input.'},
 {'object':'S','kind':'characterized/normalized-law','assessment':'Uniform existential Markov kernel with EVERY-y literal tiltedvolume conditional density; matches source C1 density up to normalization. No supplied law certificate.'},
 {'object':'U/M/T','kind':'quotient/representative','assessment':'AE actions on actual measures characterize unique bounded L2 maps. Source rough fibers need AE mean only; no every-y representative agreement. Uniform choices precede all inputs.'},
 {'object':'q','kind':'quotient/representative','assessment':'AE1 forces unique L2 class; canonical L2Expectation.one is existing producer, not an invented fallback. Explicit pairing and Tq=q conclusions.'},
 {'object':'H0','kind':'literal','assessment':'Exact let kernel(innerSL real q); membership integralzero concluded. CompleteSpace_ker is structural closed-kernel background, not finiteL2/Nontrivial/callerclosedness.'},
 {'object':'T0','kind':'characterized','assessment':'Existential bounded map wholeH0 domain with pointwise subtype actionTu, hence actual restriction; no projected or independently chosen surrogate.'},
 {'object':'D/D0','kind':'literal','assessment':'1-T*T /1-T0*T0, exact subtype restriction and selfadjoint quadratic defect; constants kill fullD.'},
 {'object':'IsUnitD0','kind':'literal-conclusion','assessment':'Real centered squared-defect invertibility only, via delta bound and completeH0; not Gamma root/inverse, not fullD inverse.'}]
binder_audit=[
 {'binder':'E NormedAddCommGroup/InnerProductSpace real/MeasurableSpace/BorelSpace','class':'TYPING','assessment':'Printed real Euclidean carrier conventions; finite real Hilbert/Borel abstraction with rank0 explicit local extension.'},
 {'binder':'FiniteDimensional real E','class':'TYPING','assessment':'Only ambient state E finite; L2/closed H0 not assumed finite dimensional.'},
 {'binder':'V alpha beta eta','class':'TYPING','assessment':'alpha,beta NNReal encode nonnegative parameters; strict loweralpha in hα andalpha<=beta retained.'},
 {'binder':'hα,hαβ,hV,hH','class':'SOURCE','assessment':'Exact S1.p1 C2 and global two Hessian form bounds; no higher smoothness.'},
 {'binder':'hη,hβη','class':'STANDING','assessment':'Positive eta/cap matches S2 scale and B12 betaeta<=1; full endpoint included.'}]
review={'schema_version':1,'actor':'/root/next_primary59',
 'status':'PREPROOF_SOURCE_STATEMENT_ACCEPTED_WITH_DISCLOSED_ELABORATION',
 'verdict_scope':'Exact header0/header1 source fidelity and binder/definition/domain review only; no proof/compilation/postproof/publication/admission verdict.',
 'candidate':pin(C/'statement-candidate.json'),'exact_header0':pin(C/'header0.lean'),'exact_header1':pin(C/'header1.lean'),
 'own_primary_before_candidate':pin(O/'primary.source-first.json'),
 'binder_audit':binder_audit,'EXCESS_count':0,'definition_audit':definition_audit,
 'statement_assumption_deltas':[
 {'kind':'generalization','source':'Printed Euclidean real R^d','candidate':'Finite real Hilbert/Borel E includingrank0','blocking':False,'reason':'Disclosed ambient coordinate-invariant extension; not finiteL2.'},
 {'kind':'source-implicit','source':'L2 AE classes and centered subspace D1/D2','candidate':'Actual AEq1, continuousinner kernel, boundedT0 restriction with literal action','blocking':False,'reason':'Explicit representation/domain elaboration, no new public hypotheses.'},
 {'kind':'authored-background-consequence','source':'B5 positive defect/C4 normrho/B15 future sqrt','candidate':'Positive scalarD,D0; delta coerciveD0; IsUnitD0','blocking':False,'reason':'Source-backed squared-defect prerequisite; inverseD0 statement is not printed Gamma theorem.'}],
 'quantifiers':'One actualS/U/M/T/q/T0 before every rough input. All-L2 selfadjointT/mean/positiveD; wholeH0 boundedT0; sharp bound/IsUnit restrictedH0. H0 representation exact and q uniqueAE1.',
 'constant_endpoint_audit':{'t':'alphaeta in(0,1] from source binders','rho':'(1-t)/(1+t)',
 'delta':'4t/(1+t)^2=1-rho²>0','t1':'rho0/T0zero/D0identity permitted; no dividing1-t',
 'rank0':'H0 can be zero/subsingleton; no Nontrivial premise or choosingnonzero vector',
 'fullD':'Tq=q andDq=0 explicitly; no full-space inverse/coercivity asserted',
 'Gamma':'no eta prefactor and no square root result in these signatures'},
 'production_test_boundary':'header0 actual55 + existingL2Expectation only; header1 realTest uses59+verified58 SAME sharp macro estimate. No productionTests import. Required SAME U/M/T identification remains proof obligation, not a caller binder.',
 'source_topology_status':'EXTRACTION_ONLY_PENDING_DISTINCT_REVIEW by whole_math52. This source statement acceptance does not self-approve my topology coverage.',
 'typed_issues':[],'blocking_statement_issue':False,
 'future_proof_obligations':['Derive actualS meanpreservation with integrability andstationary disintegration; no all-y rough C1.',
 'Transport Tselfadjoint from actualPUP/SAME realM, derive qfix andwholeH0 restriction.',
 'Derive positivefullD andpositivecenteredD0 with exactsubtype action.',
 'Identify59T/U/M with58 sourceactions before transporting sharpdelta; apply completeH0/coerciveAPI internally.'],
 'explicit_exclusions':'Gamma positivity/uniqueness/B11/LoewnerB15/Gamma inverse/polarB16; sourceweakH1; negativehalfbound/C5-C7; halfturn/dynamics/nonexplosion/hypocoercivity/main/errors/cost/actualPBPS-SPHMCcomposition/fullGoal/PURIFIED.',
 'chronology':{'source_graph_frozen_before_current_candidate':True,'only_current59_headers_read':True,
 'current59_proof_body_read':False,'compiler_started_by_reviewer':False,
 'old_provider_mathlib_body_exposure':'Historical source-only59 and current L2Expectation/Mathlib background body exposure disclosed; source graph never reconstructed from59 implementation.',
 'root_elaboration_receipts':'Candidate reports Prop elaboration EXIT0; no independently rerun compiler or proof claim.',
 'old58_pending_wording':'Earlier immutable audit pending58 wording retained; current named58 science8c8847/integrationa7caf/pushd9bff are root-supplied/currentcandidate metadata, not independentGit verification here.'},
 'diagnostics_preserved':['Requested exactheader0/1 names absent; candidate-qualified header0/1 read instead.',
 'L2Expectation under Measure, not Probability; exact existing canonical path recovered.',
 'PowerShellrg wildcard folder path failed; exact folder search recovered completeSpace_ker.'],
 'formal_admission':False,'compiler':'NOT_STARTED'}
put('source-statement.preproof-review.json',review)
put('review.payload.manifest.json',{'schema_version':1,'payload_name':'independent-source59-preproof-statement',
 'candidate':pin(C/'statement-candidate.json'),'header0':pin(C/'header0.lean'),'header1':pin(C/'header1.lean'),
 'source_review':pin(O/'source-statement.preproof-review.json'),
 'topology_payload_name':'independent-source59-extraction-for-distinct-coverage-review',
 'topology_files':[pin(O/n) for n in ['primary.source-first.json','primary.supplemental-context.json','source-graph.pre-candidate.json','source-proof-graph.json','source-coverage.manifest.json','indexed-input.manifest.json']],
 'self_topology_approval':False})
print(json.dumps({'status':'PREPROOF_SOURCE_STATEMENTS_ACCEPTED_TOPOLOGY_EXTRACTION_ONLY',
 'original_regions':18,'supplemental_regions':len(rows),'graph_nodes':len(g['nodes']),
 'graph_edges':len(g['edges']),'coverage_items':len(coverage),'NODE':sum(x['disposition']=='NODE' for x in coverage),
 'EXCLUDED':sum(x['disposition']=='EXCLUDED' for x in coverage),'compiler':'NOT_STARTED'}))
