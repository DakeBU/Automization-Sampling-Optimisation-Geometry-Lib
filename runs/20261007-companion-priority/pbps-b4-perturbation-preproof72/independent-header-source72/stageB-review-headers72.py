import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,re,datetime
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;R=O.parent;REL=O.relative_to(B).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
manifest=json.loads((O/'stageB.exact-header-input-manifest72.json').read_bytes())
for q in manifest['inputs']:
 b=(B/q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256']
 if 'snapshot' in q:assert b==(O/q['snapshot']).read_bytes() and b.replace(b'\r\n',b'\n')==(O/q['LF_snapshot']).read_bytes()
 for f in q.get('fragments',[]):assert b[f['RAW_start']:f['RAW_end_exclusive']]==(O/f['snapshot']).read_bytes() and sha((O/f['snapshot']).read_bytes())==f['RAW_sha256']
generic=(R/'header72.generic.proposed.lean').read_text(encoding='utf-8');actual=(R/'header72.actual.named-literal.proposed.lean').read_text(encoding='utf-8');parent=(O/'stageB.parent71.literal.exactraw.fragment.lean').read_text(encoding='utf-8').rstrip()
a=actual.index('private def ');z=actual.index('\ntheorem ',a);literal=actual[a:z].rstrip();public=actual[z+1:].rstrip();parentpublic=(O/'stageB.parent71.public.exactraw.fragment.lean').read_text(encoding='utf-8').rstrip()
append=' ∧\n                                (∀ u v r : HP0,\n                                  C (u+ΓP0 r) (v-A0 r)-C u v=\n                                    inner ℝ u (Inv r)+‖r‖^2/2))'
assert literal.count(append)==1
stripped=literal.replace(append,')').replace('actual_corrector_perturbation_statement','actual_corrector_change_statement');assert stripped==parent
assert public.replace('actual_corrector_perturbation','actual_corrector_change')==parentpublic
assert public.endswith(':= by') and not actual[actual.index(':= by',z)+len(':= by'):].strip()
assert ':= by' not in generic and not any(t in generic+actual for t in ['sorry','axiom ','admit','Prop := True'])
witnesses=re.findall(r'∃\s+(\S+)\s*:',literal);assert witnesses==['S','e','U','T','Γ','q','ΓP0','Inv','A0','B0','V0','R','fP','gP']
assert literal.index('∃ R :')<literal.index('(∀ f : Lp')<literal.index('∃ fP :')<literal.index('∃ gP :')<literal.index('(∀ u v r : HP0,')
gdef='let g : Lp ℝ 2 J := U (P f-(f-P f))';assert gdef in literal and '(∫ z, g z ∂J)=0 ∧' in literal
assert 'HP0.subtypeL gP=condExpL2 ℝ ℝ (μ:=J) measurable_snd.comap_le g' in literal and 'let gV : HP0 := V0.adjoint gperp' in literal
assert 'let C : HP0 → HP0 → ℝ := fun u v =>' in literal and '(‖u‖^2-‖v‖^2)/2-inner ℝ (A0 (Inv u)) v' in literal
assert 'C (u + G r) (v - A r) - C u v =' in generic and 'inner ℝ u (Inv r) + ‖r‖^2/2' in generic
generic_hypotheses=['hA','hG','hInv','hAInv','hInvG','hGInv','hSquares']
assert re.findall(r'\((h\w+)\s*:',generic)==generic_hypotheses
assert 'ActualCorrectorChange' not in generic and 'B21' not in generic and '68' not in generic
actual_binders=re.findall(r'\((h\w+)\s*:',public);assert actual_binders==['hα','hαβ','hV','hH','hη','hβη']
retention={'schema':'source72-exact-header-parent-retention-and-scope-v1','actual_pid':os.getpid(),'generic':pin(R/'header72.generic.proposed.lean'),'actual':pin(R/'header72.actual.named-literal.proposed.lean'),'literal_exact_parent_after_removing_only_append_and_reversing_name':True,'exact_new_clause':append,'exact_new_clause_utf8_sha256':sha(append.encode()),'all_six_public_binders_exact_parent':True,'public_header_exact_after_only_name_reversal':True,'common_global_witnesses':witnesses[:12],'local_actual_fP_gP':witnesses[12:],'same_C_Inv_Gamma_A_actualg_scope':True,'actualgP_gV_instantiation':'Universalforall uvr over SAME HP0 andsame C logically allows u=gP,v=gV,with actualgP/gV already produced in this exact scope. Header does not literally print that specialization and does not identify arbitraryr withrrho.','uncompiled_no_proofBODY':True,'private_literal_definition_not_provider':True,'generic_leaf_imports_no_B21_parent':True,'source_graph_generic_S15_independent_B21_preserved':True}
write('stageB.exact-retention-and-scope72.json',retention)
primitive_map=[
('hA','A self-adjoint','A0 IsSelfAdjoint retainedparent conclusion','B1compression self-adjoint;D1adjoint'),
('hG','G self-adjoint','ΓP0.IsPositive internally yields IsSelfAdjoint ΓP0; no new analyticcaller','B2same positive centeredroot;D1spectralconventions'),
('hInv','Inv self-adjoint','SameInv IsSelfAdjoint retainedparent conclusion','B3 samecenteredinverse andcommutingAInv'),
('hAInv','A commutes Inv','Commute A0 Inv retainedparent conclusion','B3commutation/samecenteredrootinverse'),
('hInvG','InvG=I','Inv*ΓP0=1 retainedparent conclusion','B3inverse onlyonHP0'),
('hGInv','GInv=I','ΓP0*Inv=1 retainedparent conclusion','Same two-sided centered inverse; redundant for shortest scalar expansion but source-present'),
('hSquares','A²+G²=I','A0*A0+ΓP0*ΓP0=1 retainedparent conclusion','B3p5.m20/B2positive root definition')]
write('stageB.generic-primitives-to-internal-actual-facts72.json',{'schema':'source72-generic-versus-actual-premise-map-v1','count':7,'entries':[{'generic_binder':a,'meaning':b,'actual_internal_producer':c,'source':d,'new_actual_public_premise':False} for a,b,c,d in primitive_map],'G_positive_not_required_by_pure_leaf':True,'A_G_commutation_not_missing':'AInv commutation and invertibility implyAGcommutation ifneeded; the direct linear-term derivation uses only adjointA/Inv,squaresum,InvG=I.','generic_complete_H':'Real Hilbert/CompleteSpace ambient context matches paper; noFiniteDimensional premise for leaf.'})
ob=json.loads((O/'stageA.all27-source-header-obligations72.frozen.json').read_bytes())['entries']
evidence={
'O00':'47724 frozenStageA run/expectations/graph/361coverage preceded14640 authorizedheaders read.',
'O01':'Frozen exposure record states sourceblind=false and71source/BODY/publication exposure; no72BODY/mathverdict/sourceplan read.',
'O02':'Generic exactC formula andactual completeparentliteral C unchanged; exact half/negativeAInvcross term.',
'O03':'GenericH realInnerProductSpace CompleteSpace;actualforalluvr:HP0 inside same localCscope.',
'O04':'Seven meaningful operatorprimitive facts in generic leaf; no corrector-identity certificate assumed.',
'O05':'Actualpublicsixcallers unchanged; allgenericfacts match internal retainedparentconclusions,ΓP0SA followspositive.',
'O06':'hA/hG/hSquares support normsum; actualpositiveΓP0 plusA0SAandhSquares retained, noonto/rankpremise.',
'O07':'Exact newclause and generic shift plusΓr,minusAr.',
'O08':'InvG=1 supportsAInvG r=A r; realinner symmetry cancelsv terms; genericheader supplies facts,implementation pending.',
'O09':'RHS inner ℝ u (Inv r),sameInv; sourceEx32/33 signs/order exact.',
'O10':'RHS +‖r‖^2/2 exactly; sourceEx34.',
'O11':'Generic importsMathlibAdjoint only; noB21; actual71 import retains originalclauses as integrationparent.',
'O12':'Exactuniversalforalluvr over sameHP0/localC directly instantiatesu=gP,v=gV already genuinely produced underoriginalf; no literalactualg-specializationclause is claimed.',
'O13':'Exactstrippedliteral equals entireparent;publicbinders6,witnesses12global+localfP/gP unchanged.',
'O14':'Exactparentactualg definition,condExpL2g constraintandV0*Rg unchanged; notRHSdefined.',
'O15':'Mean_g remains concluded insideoriginalglobalf implication; no caller added. Parentinternals previouslyreviewed; no72proofread/credit.',
'O16':'Headerquantifiesarbitraryr:HP0; noactualrrho/H/K isdefinedorasserted; source r_source/rrho distinction explicitreviewboundary.',
'O17':'ActualH/K/rrho adapter notclaimed byheader andremainsopen; no arbitraryH/K semantics invented.',
'O18':'Genericr istypedHP0;actualr_source/rrho centeredness notasserted andremainsseparatecodomainadapter.',
'O19':'NoB27 actualoutputclaim innewheader; universalr identity isnotrepresented asactualKcomponents.',
'O20':'B21 clause retainedseparately; B28combinedactualKchange notasserted; genericB21dependencyforbiddenandabsent.',
'O21':'Noρ/c0/ω/Λ bindsactualpublicorleaf. AllfullB4conditions remainexternalfutureconsumer.',
'O22':'GenericrealHilbert allowszero;actualsamefiniteDim E withnorankpositive/strictalphaeta/onto/higherregularity/68premise.',
'O23':'EntireparentpositiveΓP0/Inv/e/V literals exact,InvonlyHP0,fullkerP Dretained.',
'O24':'NoB29-B31/error/normequivalence/fullB4/main/costconclusion added; sourcegraphopenconsumers remainopen.',
'O25':'ExactcompleteprivateProp inspectable inheader; publicliteral namebindsall6callers. Futureadjacentfullliteral foldstillpublicationobligation,noprovider.',
'O26':'Bothheaders uncompiled/noBODY,actualempty:=byonly; decisionprospectiveheaderonly.'}
decisions=[{**x,'status':'SATISFIED_PROSPECTIVE_HEADER_ONLY' if x['id'] not in {'O17','O18','O19','O20','O24','O25'} else 'BOUNDARY_PRESERVED_OR_FUTURE_ADAPTER_OPEN','evidence':evidence[x['id']],'blocking':False,'implementation_or_compile_credit':False} for x in ob]
write('stageB.all27-source-header-decisions72.json',{'schema':'source72-all-frozen-obligations-header-comparison-v1','count':len(decisions),'entries':decisions,'blocking_count':0,'required_repairs':[],'open_adapter_obligations_not_discharged':True})
lines=[]
for label,text in [('generic',generic),('actual',actual)]:
 offset=0
 for n,line in enumerate(text.splitlines(keepends=True),1):
  b=line.encode();code=line.strip();is_math= bool(code) and not code.startswith(('import ','namespace ','noncomputable ','open ','set_option ','/-!','# ','Chen--','B.4 ','actual projected','The reflected','inputs and','-/'))
  lines.append({'candidate':label,'line':n,'RAW_start':offset,'RAW_end_exclusive':offset+len(b),'RAW_sha256':sha(b),'text':line,'classification':'NODE' if is_math else 'EXCLUDED','reason':'Completeprospectivestatement/binder/definition/source-facingclaimreviewed; noBODY proofcredit.' if is_math else 'Import/namespace/options/attribution/comment/blank machinery; bounded scope inspected.'});offset+=len(b)
write('stageB.every-header-line72.json',{'schema':'source72-complete-prospective-header-line-review-v1','count':len(lines),'counts':{k:sum(x['classification']==k for x in lines) for k in ['NODE','EXCLUDED']},'entries':lines,'unclassified':0,'proof_BODY_lines':0})
review='''Prospective source-header review72: accept both exact proposed headers as source-facing algebra plus original-input integration, with no blocking header delta and no required mathematical repair. This is not implementation source-fidelity, compilation, proof, SAU claim, SCI or VERIFIED admission.

StageA was independently frozen from fixed arXiv:2609.06905v1 RAW d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760 before either72 header was opened. The four regions contain255 independently reparsed items (142NODE113EXCLUDED). A finite necessary B1/operator-framework and B2/domain-root supplement contains106 unique items (97NODE9EXCLUDED). Every361 item has exact RAW offsets/hash and a source role or exclusion reason. The independent source graph has24nodes53edges,20exactformula anchors and27typed review obligations. NODE includes retained background and explicitly OPEN actual adapters/real consumers; it does not mean formal proof completion.

Exposure is disclosed: this reviewer previously read complete70/71 BODY,71source/publication and reconstruction. The same six-caller/twelve-witness background is honestly reused. No72 BODY exists or was read; no independent math72 verdict or other-agent sourceplan was read. Prior CLOSED71 bytes were pinned unchanged, not reopened for writing or used to infer72 acceptance.

The generic761-byte header d1435ac883ab1ba0d2b763a8094664d3eba18970a0fa8ff9cd051dc2966fdd8a is a real Hilbert algebra leaf. It assumes bounded A,G,Inv with A/G/Inv self-adjoint, A commuting withInv, both inverse products, and A²+G²=I. These are meaningful source operator primitives, not a corrector-change certificate. CompleteSpace matches the real Hilbert setting; finite dimension, positivity/gap, onto and rank assumptions are unnecessary for this pure algebra leaf and absent. NoB21 import or premise appears.

Its C is exactly (||u||²-||v||²)/2-inner(A(Invu),v). The perturbations are u+Gr and v-Ar, with exact result inner(u,Inv r)+||r||²/2. Independent algebra check: the norm differences contribute inner(u,Gr)+inner(v,Ar)+(||Gr||²-||Ar||²)/2. Expanding the negative cross term contributes +inner(AInvu,Ar)-inner(AInvGr,v)+inner(AInvGr,Ar). InvG=I gives AInvGr=Ar, real symmetry cancels both v terms, and the quadratic terms become (||Gr||²+||Ar||²)/2=||r||²/2. Self-adjoint A andInv move the remaining linear term to inner(u,(G+InvA²)r). The squaresum and InvG=I imply G+InvA²=Inv, so the stated result follows. No missing A-G commutation premise is needed for this direct derivation; invertibility and AInv commutation also imply it if another route uses it. GInv=I is source-present though redundant in this short calculation.

The actual9016-byte header bb6eaa684a81dbf74d7778e8fa6e98f15c1b443fa3c1e0ec4d2b36560b1ab88d preserves the entire current71 literal after deleting only the appended forall u v r clause and reversing the declaration name. The public header is likewise exact after name reversal. The six analytic callers, all twelve global witnesses S,e,U,T,Gamma,q,GammaP0,Inv,A0,B0,V0,R and local produced fP/gP remain identical. Every original probability/kernel/root/inverse/polar/actual rotation/pair-energy/norm-budget/mean/intertwining/B21 clause remains. No extra public premise, proof provider, sharp-energy68 parent or new witness is introduced.

The appended universal identity is in the SAME HP0, SAME local C, SAME A0/GammaP0/Inv scope, after the actual f/g and gP/gV have been produced. It does not literally print a specialization u=gP,v=gV; universal elimination gives that original-input consumer directly, with no new hypotheses or semantic adapter. This suffices for the bounded original-input perturbation integration. It does not define components by rotation RHS and does not identify arbitraryr with the source residuals. g remains U(Pf-(f-Pf)), gP is actual condExpL2g, gV is V0*Rg and mean(g)=0 remains an internal conclusion. ΓP0 positivity supplies its self-adjointness internally; all other generic operator facts are explicit unchanged parent conclusions, never added analytic callers.

The primary source distinction is essential. Source Ex27 defines r_source=V*(I+Hmicro)fperp and rrho=V*[I+(1-rho)Hmicro]fperp=rho fV+(1-rho)r_source. B27 requires the SAME actual conditional half-turn H, actual Markov K=B7, polar/all-kerP intertwining and output projection semantics. These are not present as new conclusions in the72 header and remain explicit open adapters. Arbitrary r in the generic leaf/actual universal clause is a centered perturbation vector, not an asserted actual rrho. B21 is a retained actual integration parent and participates only in the downstream B28 sum. It is not a source dependency of the generic perturbation algebra.

The exact signs/half/order match B20 and B4 Ex28-Ex34: linear inner(gP,Invrrho) and positive half normrrho² after actual B27 specialization. B28 additionally consumes B21. The source rho regime, c0<=1/16, gamma<=1/2, Lambda/omega restrictions and B29-B31 residual estimates belong to separate actual dynamics/decay consumers. They are not needed by this identity and do not become six-caller premises. Rank zero and alpha eta=1 remain legal; V is an embedding into all kerP with no onto premise; no higher smoothness is introduced.

The private literal is a proposition definition/nonprovider, not a proof or input certificate. Its complete content is inspectable here; future publication must expose the complete exact literal adjacent to its public theorem fold as already required for71. There is no72 publication/reader acceptance in this review. The generic file has a header only; the actual file ends at empty :=by. Neither is compiled, and no proof search or Lean invocation was performed by this reviewer.

All27 frozen obligations are individually compared. Actual H/K/rrho/B27/B28 and later fullB4/main/errors/cost/composition boundaries are preserved as open, not discharged by header inspection. All candidate header lines are recorded with exact RAW offsets/hash and review classification. Canonical files, Git, ledgers, Goal and old CLOSED directories were not written. Named payload remains small and uses exact finite input/source/closure pins without recursive historical base64. Native wholelogical removes ONLY top-levelrun_sha256; LF changes ONLY byteCRLF toLF. Final native lease is last owned write, with actual foreground terminal receipts and subsequent read-only verification.
'''
(O/'source-header72.review.RAW.md').write_text(review,encoding='utf-8',newline='\n')
decision={'schema':'source72-independent-prospective-header-admission-decision-v1','decision':'accept_prospective_headers_source_facing_only','reviewer':'independent-primary-source-reviewer-72','independent_from_formalizer_and_math_reviewer':True,'actual_author_pid':os.getpid(),'generic_header':pin(R/'header72.generic.proposed.lean'),'actual_header':pin(R/'header72.actual.named-literal.proposed.lean'),'source_expectations_frozen_before_headers':pin(O/'stageA.source-expectations72.before-header.frozen.json'),'source_graph_frozen_before_headers':pin(O/'stageA.source-proof-graph72.before-header.frozen.json'),'all27_obligation_decisions':pin(O/'stageB.all27-source-header-decisions72.json'),'exact_parent_retention':pin(O/'stageB.exact-retention-and-scope72.json'),'generic_actual_primitive_map':pin(O/'stageB.generic-primitives-to-internal-actual-facts72.json'),'full_RAW_review':pin(O/'source-header72.review.RAW.md'),'blocking_deltas':[],'required_repairs':[],'generic_B21_dependency':False,'actual_universal_direct_gP_gV_instantiation_source_meaningful':True,'actual_rrho_H_K_B27_B28_not_claimed':True,'all6callers12witnesses_oldclauses_retained':True,'rank0_alphaeta1_noonto_no68_nohigherregularity':True,'sourceblind':False,'uncompiled_no_proofBODY_no_proofsearch':True,'truth_boundary':'Prospective statement/binder/definition/source-header admission only. No implementation fidelity,Leanproof/compile,SAUclaim,SCI,VERIFIED,actualH/K/rrho/B27/B28/fullB4/main/errors/cost/composition/Exposition/PURIFIED/live/paper/Goal completion.'}
records=['stageA.freeze.run72.json','stageA.source-expectations72.before-header.frozen.json','stageA.source-proof-graph72.before-header.frozen.json','stageA.finite-source255-plus-supplemental-coverage72.frozen.json','stageA.target20-exact-RAW-formulas72.frozen.json','stageA.all27-source-header-obligations72.frozen.json','stageA.anti-anchoring-exposure72.frozen.json','stageB.exact-header-input-manifest72.json','stageB.exact-retention-and-scope72.json','stageB.generic-primitives-to-internal-actual-facts72.json','stageB.all27-source-header-decisions72.json','stageB.every-header-line72.json','source-header72.review.RAW.md']
run={'schema':'source72-native-independent-prospective-header-review-run-v1','actual_pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision_complete':decision,'records':[pin(O/n) for n in records],'StageA_whole_logical_run_sha256':json.loads((O/'stageA.freeze.run72.json').read_bytes())['run_sha256'],'counts':{'primary':255,'primary_NODE':142,'primary_EXCLUDED':113,'supplement':106,'supplement_NODE':97,'supplement_EXCLUDED':9,'source_nodes':24,'source_edges':53,'source_formulas':20,'obligations':27,'candidate_header_lines':len(lines),'blocking':0,'repairs':0},'no_canonical_Git_ledger_Goal_old_CLOSED_writes':True,'whole_logical_recipe':'Canonical sorted compact UTF8 JSON deleting ONLY top-level run_sha256; no other field removed.'};run['run_sha256']=sha(canon(run));write('source-header72.run.json',run)
decision['review_run_sha256']=run['run_sha256'];write('source-header72.decision.json',decision)
synth={'schema':'source72-bounded-header-source-admission-synthesis-v1','decision':decision['decision'],'blocking':0,'required_repairs':[],'exact_headers':[decision['generic_header'],decision['actual_header']],'source_coverage_counts':run['counts'],'same6callers12witnesses_allparent_clauses':True,'generic_leaf_no_B21parent':True,'actual_specialization_by_same_scope_universal_instantiation':True,'open_actual_H_K_rrho_B27_B28':True,'sourceblind':False,'whole_logical_run_sha256':run['run_sha256'],'native_decision':pin(O/'source-header72.decision.json'),'truth_boundary':decision['truth_boundary']};write('source-header72.bounded-synthesis.json',synth)
payload={'schema':'source72-small-complete-named-header-review-decision-input-payload-v1','complete_RAW_review_utf8':review,'complete_native_run':json.loads((O/'source-header72.run.json').read_bytes()),'complete_decision':decision,'complete_bounded_synthesis':synth,'complete_exact_candidate_parent_input_manifest':manifest,'complete_all27_obligation_decisions':decisions,'generic_actual_primitive_map':json.loads((O/'stageB.generic-primitives-to-internal-actual-facts72.json').read_bytes()),'immutable_StageA_named_payload':pin(O/'stageA.complete-named-expectations-input-payload72.json'),'immutable_primary_source_manifest':pin(O/'stageA.primary-input-manifest72.json'),'all_named_record_RAW_LF_refs':[pin(O/n) for n in records],'materialization':'Exact RAW/LF headers and exact bounded parent fragments are owned snapshots. Fixed primary/oldnative are pinned,not recursively copied; complete finite source coverage is named by hash. Finalownedmanifest binds allhelpers/failures/receipts/snapshots; finallease last.'};write('complete-named-review-decision-input-payload72.json',payload)
print(json.dumps({'actual_pid':os.getpid(),'decision':decision['decision'],'obligations':27,'blocking':0,'repairs':0,'header_lines':len(lines),'whole_logical_run_sha256':run['run_sha256'],'decision_artifact':pin(O/'source-header72.decision.json'),'small_named_payload':pin(O/'complete-named-review-decision-input-payload72.json')},indent=2))
