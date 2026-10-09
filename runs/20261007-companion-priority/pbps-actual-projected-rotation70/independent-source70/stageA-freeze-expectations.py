import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,datetime,os,collections
O=pathlib.Path(__file__).resolve().parent
B=pathlib.Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70')
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
J=lambda p:json.loads(p.read_bytes())
def save(n,v):
 p=O/n; assert not p.exists(), 'freeze is append-only: '+n
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');return {'name':n,'RAW_bytes':p.stat().st_size,'RAW_sha256':H(p.read_bytes())}
inputs=J(O/'stageA.input-manifest.json')['inputs']
for source,name,expected in [(B/'header0-proposed-expanded.lean','original-source-reviewed70.header.exactraw.lean','9261f488432664370ae1b1146b098bf86c17dfd476bfe2e149d3024a77529e19'),(B/'root.statement-seal70.json','original70.root.statement-seal.exactraw.json','80af59baba4ec696cb48f06170568904af553b50ec134a961610eaa1b82e7723')]:
 raw=source.read_bytes();assert H(raw)==expected
 lf=raw.replace(b'\r\n',b'\n');(O/name).write_bytes(raw);(O/(name+'.LF')).write_bytes(lf)
 inputs.append({'original_path':str(source),'snapshot':name,'RAW_bytes':len(raw),'RAW_sha256':H(raw),'LF_snapshot':name+'.LF','LF_bytes':len(lf),'LF_sha256':H(lf),'LF_recipe':'CRLF-only; no other byte change','original_mtime_ns':source.stat().st_mtime_ns})
source=pathlib.Path('E:/Samplinglib/tools/astis_semantic_roundtrip_core.py');raw=source.read_bytes();lines=raw.splitlines(keepends=True);part=b''.join(lines[33:78]);name='schema.semantic-seven-slots.exactraw.fragment.py';(O/name).write_bytes(part);(O/(name+'.LF')).write_bytes(part.replace(b'\r\n',b'\n'))
inputs.append({'original_path':str(source),'original_whole_RAW_bytes':len(raw),'original_whole_RAW_sha256':H(raw),'selection':'one-based inclusive lines34-78','original_RAW_range_end_exclusive':[sum(map(len,lines[:33])),sum(map(len,lines[:78]))],'snapshot':name,'RAW_bytes':len(part),'RAW_sha256':H(part),'LF_snapshot':name+'.LF','LF_bytes':len(part.replace(b'\r\n',b'\n')),'LF_sha256':H(part.replace(b'\r\n',b'\n')),'LF_recipe':'CRLF-only','schema_only_no_prior_verdict_read':True})
save('stageA.complete-primary-input-manifest.frozen.json',{'schema':'source70-stageA-complete-frozen-inputs-v1','actual_pid':os.getpid(),'input_count':len(inputs),'inputs':inputs,'RAW_LF_recipe':'CRLF-only for every text input; wholefile versus exact raw selection stated per entry','current70_BODY_read':False,'current70_publication_or_decoder_read':False})
inv=J(O/'stageA.primary419.reparsed-inventory.json');byid={x['id']:x for x in inv['math_items']}
graph=J(O/'prior83.frozen-source.source-proof-graph.json')
roles={n:'retained-source-ingredient-or-parent69-contract' for n in ['P0','P1','P2','P3','P4','P5','P6','P7','P8','P9','P10','P11']}
roles.update({n:'current70-actual-projection-rotation-and-pair-energy' for n in ['P12','P13','P14']})
roles.update({n:'real-primary-downstream-consumer-not-current70-conclusion' for n in ['P15','P16','P17','P18','P19','P20','P21']})
for n in graph['nodes']:
 n['current70_source_role']=roles[n['id']];n['formal_status']='current70-BODY-not-read-no-verdict'
 n['primary_math']=[byid[m['id']] for m in n['primary_math']]
 if n['id']=='P11':n['kind']='retained-parent69-all-micro-intertwining'
 if n['id']=='P13':n['internal_completion_obligation']='For actual g=U(Pf-(f-Pf)), mean(g)=mean(f)=0 from reflection-law invariance and conditional-expectation integral identity; never a caller premise.'
 if n['id']=='P14':
  n['kind']='current70-actual-projected-rotation-and-pair-energy'
  n['pair_energy_expectation']='||gP||^2+||gV||^2=||fP||^2+||fV||^2 for actual components, from selfadjoint commuting A0,GammaP0 and A0^2+GammaP0^2=I.'
  n['pair_energy_explicit_consumer_math']=byid['A2.SS3.p9.m2']
 if n['id']=='P19':n['actual_comparator_component_anchors']=[byid[i] for i in ['A2.SS3.p8.m4','A2.SS3.p8.m5','A2.SS3.p8.m6']]
graph.update({'schema':'source70-stageA-RAW-revalidated-primary-proof-graph-v1','built_from':'fixed primary RAW seven regions; immutable preimplementation22node49edge source topology reused, all97 exact anchors revalidated and current70 roles independently assessed before whole BODY','no_prior_graph_or_verdict_used':False,'prior_primary_source_only_graph_reused':True,'prior_source_or_math_verdict_substituted_for_current_review':False,'current70_BODY_read':False,'node_count':22,'edge_count':49,'source_dependency_edges_are_not_Lean_edges':True})
assert len(graph['nodes'])==22 and len(graph['edges'])==49
graph_record=save('stageA.source-proof-graph70.frozen.json',graph)
prior=J(O/'prior83.primary419-NODE-EXCLUDED70.json');old={e['id']:e for e in prior['entries']}
entries=[];added=[]
for e in inv['math_items']:
 p=old[e['id']];assert e['RAW_sha256']==p['RAW_sha256'] and e['source_RAW_range_end_exclusive']==p['source_RAW_range_end_exclusive']
 nodes=list(p['source_nodes']);classification=p['classification']
 if e['id'] in ['A2.SS3.p8.m5','A2.SS3.p8.m6']:
  classification='NODE';nodes=['P19'];added.append(e['id'])
 if classification=='NODE':
  reason='Primary-present formula or exact surrounding notation for '+','.join(nodes)+'. Current role(s): '+', '.join(sorted({roles[n] for n in nodes}))+'. Source membership is neither a public caller premise nor current Lean proof credit.'
 else:
  reason={'global-assumptions':'Informal main-result, warm-start, query-complexity or introduction comparison outside actual projected rotation70.', 'actual-joint-law':'Other conditional curvature/covariance, smoothing, proximal minimizer or RGO statement; no added premise for70.', 'conditional-reflection-blocks-B1':'Actual chain/half-turn branch context outside current ideal-reflection rotation; future consumer context does not prove it.', 'same-root-polar-B2':'Additional regularity/H1 estimate, quantitative proof detail or half-turn bound outside70; not an extra caller.', 'corrector-sharp-energy-and-consumers-B3':'Surrounding norm dissipation, corrector sharp estimate, Lyapunov equivalence/decay or notation outside current70 target and pinned source-graph consumer anchors.', 'corrector-change-B4-consumer-proof':'Other B4 error/Young/coercivity/decay detail or surrounding notation outside current70 and pinned real-consumer anchors.', 'real-L2-spectral-conventions-D1':'Additional generic Markov-density/chi-square convention beyond exact real-L2, projection/adjoint/root anchors; mean adapter derives from actual reflection law and conditional expectation.'}[e['region']]
 entries.append({**e,'classification':classification,'source_nodes':nodes,'reason':reason,'classification_basis':'immutable CLOSED83 source-only header coverage reused after independent RAW identity validation; current70 source role independently rechecked; two explicit B4 component-definition anchors promoted','source_ingredient_is_not_caller_binder':not bool(nodes==['P0'])})
counts=dict(collections.Counter(e['classification'] for e in entries));assert len(entries)==419 and sum(counts.values())==419
coverage_record=save('stageA.primary419-NODE-EXCLUDED70.frozen.json',{'schema':'source70-stageA-finite-primary-NODE-EXCLUDED-v1','count':419,'counts':counts,'unclassified':0,'source_regions':7,'source_graph_nodes':22,'source_graph_edges':49,'prior_header_classification_counts':prior['counts'],'current_source_only_promotions':added,'entries_canonical_sha256':H(C(entries)),'entries':entries,'all_classified_does_not_mean_proved':True,'whole_paper_coverage':False})
obligations=[
 ('O00','P0','source-callers','Exactly six original analytic conditions hα,hαβ,hV,hH,hη,hβη; finite real Hilbert/Borel representation; no positive-rank requirement.'),
 ('O01','P1,P2','actual-definition-and-AE-transport','Same J actual normalized Gibbs-Gaussian joint law and same U pullback by F(x,y)=(x,2x-y), as L2 classes with valid AE representative transport.'),
 ('O02','P2,P13','internal-mean-adapter','Derive integral(Uh)=integral(h) for all L2 h from actual F preserving J and U h = h∘F AE; L2 integrable since J probability. Alternate U1=1+selfadjoint route also requires actual AE link.'),
 ('O03','P3,P12,P13','internal-conditional-expectation-adapter','Derive integral(P h)=integral(h) using actual condExpL2 and probability/integrability; P=PstarProjection and R canonical complement, not arbitrary projection.'),
 ('O04','P3,P4','canonical-compression','R h inclusion=h-P h; D=R∘U∘Hperp.subtypeL and actual D h inclusion=U h-P(U h). all kerP inputs retained, not only range V.'),
 ('O05','P4,P5,P6,P7,P8,P9,P10,P11','retained69-complete-result','Retain all original69 conclusions and the12 SAME common witnesses S,e,U,T,Gamma,q,GammaP0,Inv,A0,B0,V0,R before ∀f. Definitions, root identity, centered inverse, polar and all-micro intertwining must not be replaced by fresh unrelated witnesses.'),
 ('O06','P5,P7','same-root-domains','A0 and GammaP0 are exact centered restrictions; Gamma is nonnegative sqrt(I-A²); selfadjoint commuting A0/GammaP0 and square-sum identity. Inv is two-sided inverse only on HP0.'),
 ('O07','P8,P12','no-surjectivity','V0*V0=I on HP0 is into-isometry; fV=V0*Rf, with norm contraction. Never infer V0V0*=I, onto V0 or fperp=V0 fV.'),
 ('O08','P12','actual-original-components','Every original f:L2(J) with integral f=0; produce fP:HP0 with inclusion=actual condExpL2 f. fperp=Rf and fV=V0* fperp, same f and same common witnesses.'),
 ('O09','P13','actual-update-definition','g must be definitionally the actual U(P f-(f-P f)), not supplied coefficients or a separately chosen centered function.'),
 ('O10','P2,P3,P13','internal-mean-completion','integral(g)=integral(U(Pf-(f-Pf)))=integral(Pf)-[integral(f)-integral(Pf)]=integral(f)=0. Produce internally; not mean_g caller, witness property assumption or unproved adapter.'),
 ('O11','P3,P13','actual-new-macro-component','After mean(g)=0, produce gP:HP0 with inclusion=actual condExpL2 g; domain/centeredness from integral_condExp. Do not define gP as rotation RHS.'),
 ('O12','P3,P8,P13','actual-new-micro-component','gperp=R g in all kerP; gV=V0.adjoint gperp in HP0. Do not define gV by coefficient RHS.'),
 ('O13','P9,P12,P13,P14','macro-rotation-transport','Actual Pg=P U(fP-fperp)=A0 fP-GammaP0 fV after explicit HP0/L2 inclusion and adjoint transport.'),
 ('O14','P8,P11,P12,P13,P14','micro-rotation-transport','R U(fP-fperp)=B0 fP-D fperp; V0*B0=GammaP0 and same inherited all-kerP V0*D=-A0 V0*. Thus actual gV=GammaP0 fP+A0 fV.'),
 ('O15','P14','exact-signs','Macro minus GammaP0 fV and micro plus A0 fV; signs follow actual P-Pperp update and negative intertwining.'),
 ('O16','P5,P7,P14','real-Hilbert-pair-energy','Expand sum of squared norms, cancel cross terms using real inner product/selfadjointness/commutation, use A0²+GammaP0²=I. No inverse needed for this final algebra, but same centered witnesses retained.'),
 ('O17','P14','actual-pair-energy','Conclude ||gP||²+||gV||²=||fP||²+||fV||² for actual components. Mere algebra for arbitrary u,v is a reusable ingredient, not replacement for actual-input semantics.'),
 ('O18','P16,P17','future-corrector-consumer','B20/B21 consumes actual rotation in C(gP,gV)-C(fP,fV)=-||fP||²+||fV||². This is a downstream consumer, not a70 conclusion or a68sharp-energy parent.'),
 ('O19','P19,P20','real-B4-consumer','Same actual comparator g in B4 has (Kf)P=gP+GammaP0 rρ and (Kf)V=gV-A0 rρ; B28 adds B21. No new rho/omega/c0 restriction on70.'),
 ('O20','P21','explicit-energy-consumer','A2.SS3.p9.m2 uses exact pair energy as ||gP||²<=||fP||²+||fV||² in B4; B17/B30/B31/full decay remain separate obligations.'),
 ('O21','P0,P6','endpoint-and-strengthening-boundary','Retain rank0/HP0={0}, alphaeta=1/betaeta=1; no ontoV, global inverse, H1/smooth f, extra V derivatives, rho/omega/small c0 or sharp-energy68 premise.'),
 ('O22','P12,P13,P14','reader-representation-obligation','Named private literal Prop is exact complete statement representation, not provider. Future reader must expose full literal adjacent to public signature and six BODY/code formulas with exact current hashes.'),
 ('O23','P12,P13,P14','future-anti-anchored-comparison','Only after official reviewer packet: compare full module/all literal formula BODY lines and publication, seven canonical semantic slots and blind reconstruction against this freeze; classify every delta with current native schema; independent math verdict does not substitute.')
]
obligation_rows=[{'id':a,'source_nodes':b.split(','),'type':c,'source_expectation':d,'current70_implementation_status':'not-read-not-judged','public_caller_premise_permitted':c=='source-callers'} for a,b,c,d in obligations]
obligation_record=save('stageA.exhaustive-finite-obligations70.frozen.json',{'schema':'source70-stageA-finite-obligation-freeze-v1','count':len(obligation_rows),'obligations':obligation_rows,'source_ingredients_are_dependency_edges_not_binders':True,'all_current70_implementation_statuses_pending':True})
exposure={'schema':'source70-stageA-prior-exposure-disclosure-v1','prior_type_ascription_review':'source representation only; failed compiler ascription did not fix unknown free variable','prior_named_literal_review':'exact sealed107-line return expression compared to named literal, six public binders preserved; reader obligation recorded','prior_BODY_exposure':{'kind':'opaque whole-byte reads and mechanical equality, no proof mathematics parsed/reviewed','old_canonical_RAW_sha256':'ee29967305ee9c811ebc0ff7bc5058a7f4f3de7f2ed5928f025f2a8a43b2bbd6','old_canonical_RAW_bytes':25504,'scratch_named_literal_RAW_sha256':'b0baff9d9feb94e6a509d707231edc6fe9d93673e1cde71e7658a9dcc603b77e','scratch_named_literal_RAW_bytes':26168,'operation':'replace exact original header with exact named-literal header and one unfold line, assert remaining BODY/trailer byte equality','minimal_displayed_postheader_syntax':[' := by','  classical','  let μ := (volume : Measure','  unfold actual_projected_rotation_statement'],'not_strictly_byte_unexposed':True,'no_whole70_BODY_mathematical_source_read':True},'current70_BODY_read_before_this_freeze':False,'current70_publication_or_blind_decoder_read_before_this_freeze':False,'prior_SOURCE69_acceptance_or_math70_verdict_used_as_current_verdict':False,'console_pre_owned_discovery_failure':{'exit':1,'reason':'UnicodeEncodeError GBK while printing source tag; source data unchanged','actual_pid':'not captured by exploratory exec; not invented','retained_in_conversation':True},'retired_readview_v1':'HTML stripping after TeX insertion could swallow less-than inequalities; v1 retained as retired aid. All seven RAW regions and419 alttext/annotation identities remained exact; corrected placeholder-protected v2 reread.'}
exposure_record=save('stageA.anti-anchoring-exposure70.frozen.json',exposure)
slots={
 'objects':'Actual J, same actual pullback U, condExp P, R canonical kerP complement, SAME centered A0/GammaP0/Inv/B0/V0 and original fP/fV plus actual g/gP/gV. Private literal represents complete statement and is not provider.',
 'domains':'Real L2(J) AE classes; HP=range condExp, HP0=HP∩mean-zero, Hperp=kerP. D acts on ALL Hperp, inverse only HP0; f and g globally centered; gP/fP/gV/fV allHP0. Probability/integrability/AE adapters internal.',
 'quantifiers':'Original six analytic callers and structural finite real Hilbert/Borel binders. Twelve common SAME witnesses before every globally centered f; actual per-f fP and gP existentials. No mean_g, projection/rotation/intertwining or onto-V caller.',
 'assumptions':'Exactly hα:0<α,hαβ:α≤β,hV:C2,hH:global two-sided Hessian,hη:η>0,hβη:βη≤1. Ingredients from actual-law,condExp,root/centered inverse/polar and69 parent must be produced; retain rank0 andαη=1.',
 'conclusion':'Preserve full69 original result; add actual g definition, internal mean(g)=0, actual condExp gP,actual gV=V0*Rg; gP=A0fP-GammaP0fV,gV=GammaP0fP+A0fV; pair squared-norm conservation. No B21/B4/main/fullpaper conclusion.',
 'scopes':'All restriction,representative,inclusion,subtype and inverse scopes exact. Same f and same witnesses throughout. Source graph ingredients are proof obligations; reader full literal adjacent folded code required; whole BODY/source verdict pending official packet.',
 'constant_dependencies':'Only original α,β,η and V/E assumptions. No new rho,omega,c0,H1 bound,extra smoothness,68sharp-energy or positive rank. Pair-energy algebra uses SAME selfadjoint commuting A0,GammaP0; prior inverse contracts retained not replaced.'
}
expectations={'schema':'source70-stageA-primary-first-expectations-v1','freeze_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_pid':os.getpid(),'status':'STAGE_A_FROZEN_NOT_FINAL_SOURCE_VERDICT','current70_BODY_or_publication_seen':False,'official_source_reviewer_packet_received':False,'blind70_reconstruction_seen':False,'fixed_primary':{'RAW_bytes':1482128,'RAW_sha256':H((O/'primary-pbps.exactraw.snapshot.html').read_bytes())},'source_graph':graph_record,'finite_primary_coverage':coverage_record,'finite_obligations':obligation_record,'prior_exposure_disclosure':exposure_record,'canonical_semantic_slots_source_expectations':slots,'public_callers_count':6,'common_witness_count':12,'source_nodes':22,'source_edges':49,'source_math_items':419,'source_regions':7,'mean_g_status':'internal source-law completion required, not caller premise','real_consumers':['P16','P17','P19','P21 pair-energy budget'],'forbidden':['components defined by rotation RHS','mean_g caller','ontoV/coisometry','global-root inverse','sharp-energy68 parent','rho/omega/c0 for70','H1 or smooth f','higher derivatives onV','positive rank','B21/B4/main/fullpaper/Goal completion'],'future_reader_obligation':'Full exact literal Prop adjacent folded statement; private literal is representation, not provider. No reader or current70 source admission now.','no_proof_search_compile_SAU_claim_or_VERIFIED_credit':True}
record=save('stageA.source-expectations70.before-current-BODY.frozen.json',expectations)
print(json.dumps({'actual_pid':os.getpid(),'expectations':record,'graph':graph_record,'coverage':coverage_record,'coverage_counts':counts,'obligations':obligation_record,'input_count':len(inputs),'official_packet_pending':True,'current70_BODY_read':False},ensure_ascii=True))
