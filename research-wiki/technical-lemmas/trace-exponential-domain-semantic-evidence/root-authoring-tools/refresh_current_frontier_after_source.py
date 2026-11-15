from pathlib import Path
import hashlib,json,copy
r=Path.cwd();w=r/'.astis/huanjian-gc-trace-mgf-domain-20261115'
e=r/'research-wiki/technical-lemmas/trace-exponential-domain-semantic-evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def ident(p):return {'file':str(p.relative_to(r)),'sha256':sha(p)}
cp=r/'research-wiki/frontier-cells/ASTIS-SHARED-REAL-TRACE-EXPONENTIAL-DOMAIN.json'
before=e/'metadata-custody/frontier.before-native-source-refresh.original.json';assert not before.exists();before.write_bytes(cp.read_bytes())
c=json.loads(cp.read_text());assert c['status']=='claimed' and c['owner_id']=='huanjian_20261115_trace_exponential_domain'
pa=json.loads((r/'research-wiki/semantic-roundtrip/audits/huanjian-trace-exponential-domain.json').read_text())
ta=json.loads((e/'private-consumer-audit.source-reviewed.v2.json').read_text())
assert pa['state']==ta['state']=='source-reviewed'
assert pa['publication_binding_sha256']==ta['publication_binding_sha256']=='e44190bca918ce5a1e8f4ff5fc942c56ea400deb7a10af9929a698ef22a9d45c'
native=e/'independent-native-and-preproof-originals/readable-native-originals/native-mathematics-report.v1.json'
assert sha(native)=='51481e488bee3d6de641a61a5dced0bd9bfaa6f7666e64d5c36595f3b0c5c1ca'
mapping=e/'source-to-lean.correspondence.authored-v3.json';m=json.loads(mapping.read_text())
c['parents']=[]
c['parent_scope']='Independent immutable301728 type/value/kernel extraction confirms P has no external ASTIS value parents. Its Mathlib floor is real; empty parents does not mean no mathematical dependencies. Private T actually calls P, Radius and Structure.'
c['consumer_scope']['first_realistic_consumer']['state']='ACTUAL_COMPILED_MATERIAL_PRIVATE_CONSUMER; INDEPENDENT_SOURCE_AND_NATIVE_CHECKED'
c['consumer_scope']['compiled_consumer_credit']=True
c['shared_floor_audit']['status']='BOUNDED_REUSE_SEARCH_PLUS_ACTUAL_IMMUTABLE_NATIVE_PARENT_EXTRACTION'
c['shared_floor_audit']['classification_qualification']='One deterministic all-real strict-positive trace envelope; bounded exact-interface reuse search only, no whole-library absence assertion. Existing radius/structure and older Laplace/MGF results are not recounted.'
c['reuse_plan']['reused_declarations']=m['actual_compiled_value_parents']['private_T'][1:]
c['reuse_plan']['new_shared_declarations_status']='ACTUAL_IMMUTABLE_P_WITH_MATERIAL_T; INDEPENDENT_SOURCE_NATIVE_ACCEPTED; NORMAL_PL_V_PENDING'
c['reuse_plan']['planned_consumers']=[c['consumers'][1]]
c['reuse_plan']['decision_reason']='P supplies pointwise positive trace and exact card(I) envelope to literal T. Native extraction confirms no ASTIS value parent for P and exact P/Radius/Structure value parents for T. No extra public T edge.'
c['reuse_plan']['actual_parent_calls_pending']=False;c['reuse_plan']['actual_P_ASTIS_parents']=[]
c['reuse_plan']['public_P_input_plan']={'expected_floor':'Mathlib','exact_declarations':[
 'cfc_comp_const_mul','CFC.real_exp_eq_normedSpace_exp','cfc_isStrictlyPositive_iff',
 'Matrix.isStrictlyPositive_iff_posDef','Matrix.PosDef.trace_pos','cfc_le_algebraMap_iff',
 'IsometricContinuousFunctionalCalculus.norm_spectrum_le','Matrix.le_iff','Matrix.PosSemidef.trace_nonneg'],
 'status':'ACTUAL_SOURCE_API_USES; COMPLETE_NATIVE_DAG_RETAINED'}
c['reuse_plan']['private_T_dependency_status']='ACTUAL_TYPE_VALUE_PARENTS_CONFIRMED; ORIGINAL_PLANNED_LIST_RETAINED_AS_HISTORY'
c['reader_contract']['status']='Current five-step authored exposition/source semantics accepted; fresh isolated v2 static render and exact code/source/download bytes checked. Actual browser/visual acceptance pending.'
c['graph_contribution']['visual_review']='Pending actual desktop/mobile bounded graph UI. Isolated projection has one canonical public P and the private T module; dashed scanner references stay distinct from native value dependencies. No global graph update.'
c['graph_contribution']['classification_qualification']='Native confirms compiled P/T actual parents. Typed conceptual mechanism has independent raw review only; normal validation/global graph stabilization remain separate.'
c['learning_contract']['salvage']['reason']='Target P/T proofs passed first attempts. Two independent diagnostic harness failures are retained and corrected without changing P/T. Renderer missing citation scopes is a presentation implementation failure, not a mathematical negative result; exact six-field repair independently accepted.'
c['learning_contract']['parallelism']['expected_information_gain']='ROOT sole prover; distinct source-blind decoder, fresh raw-source-first semantic/wholemodule reviewer, native kernel reviewer, privacy custody review and reader preparation answer separate uncertainties.'
c['learning_contract']['parallelism']['direction_fingerprints']=['root-proof-CFC-envelope-and-literal-consumer','blind-statement-decoding','fresh-source-wholemodule-exposition','immutable-native-type-value-kernel','explicit-leaf-public-privacy-custody','isolated-reader-runtime']
c['learning_contract']['cross_route_blind_spot_audit']['selection_reason']='Only one target proof route implemented. Frozen sufficient OR alternatives are preserved, not counted as multiple verified routes. Actual CFC positivity/upper plus support-integral route independently reviewed; no quantitative lower envelope emitted.'
c['source_detail_audit']['gap']='The omitted scalar domain/regularity bridge has actual local narrow outputs and independent source/native acceptance. The full matrix-MGF and downstream uncited Bernstein invocation remain open/excluded.'
current_boundary='Only the deterministic finite nonempty REAL Hermitian all-real ordinary trace-exponential envelope and one private literal full-Gaussian four-family scalar domain are proved here: Integrable f, pointwise0<f<=r^2 exp(|s|dRstar), and ordinary0<integral f<=the same cap. All regularity/radius/Hermitian/normalization facts are discharged internally. No full matrix-valued MGF, independent-sum/Lieb/master-tail/Bernstein/norm-tail/Ex121/weighted p15.2/C6/complete Lemma4.4/main lower-bound or oracle/TV/precision/deterministic worst-query/expected-cost adapter follows. Ex121->p15.2 is source continuation only. Main/shared imports/Registry/sourceIndex/global graph/site integration, reader runtime, normal PL/V and purification remain separate.'
c['source_detail_audit']['fidelity_boundary']=current_boundary
c['statement_seal']['status']='EXACT_SIGNATURES_UNCHANGED_AFTER_ACTUAL_PROOF_AND_INDEPENDENT_SOURCE_NATIVE_REVIEW'
c['statement_seal']['definition_kind']='Literal private T lets; ordinary trace/matrix-algebra exp; actual Matrix.instL2OpNormedRing confirmed. No characterized fallback, extra theorem premise or duplicate public T.'
c['source_proof_coverage']['source_gap_status']=[
 {'id':'GAP:trace-domain','status':'NARROW_SCALAR_ALLREAL_OUTPUT_COMPILED_AND_SOURCE_REVIEWED; NOT_FULL_MATRIX_MGF'},
 {'id':'GAP:measurability','status':'REUSED_Z_REGULARITY_PLUS_INTERNAL_SCALAR_CONTINUITY_DOMINATION; NO_NEW_PUBLIC_MEASURABLE_LEAF'},
 {'id':'GAP:Bernstein-external','status':'OPEN_DOWNSTREAM_EXCLUDED'}]
c['source_proof_coverage']['source_to_Lean_correspondence']=ident(mapping)
c['source_proof_coverage']['correspondence_delta_acceptance']=ident(e/'source-review/trace_exp_fresh_source_51c8/originals/phase2_correspondence_v3_delta_review.json')
c['source_proof_coverage']['portable_originals']=ident(e/'independent-native-and-preproof-originals/ROOT-original-reference-portable-resolution.v1.json')
c['proof_digestion']={'status':'ACTUAL_LOCAL_COMPILED_AND_INDEPENDENTLY_SOURCE_REVIEWED; PURIFICATION_PENDING',**m['proof_digestion']}
c['purification']['canonicalization']='Shared P with private material consumer; no separate T publication edge. Independent final integration/purification remains pending.'
c['purification']['reader_default_view']='Short formula statement; assumptions, five mathematical proof steps and exact adjacent P/T Lean folded in layers.'
c['semantic_roundtrip'].update(state='source-reviewed',qualification='Distinct source-blind decoder and raw-source-first wholemodule/seven-slot/lesson review accepted; original82c0 full review and independently reviewed six-citation-scope successor e441 retained.',publication_binding_sha256=pa['publication_binding_sha256'])
c['evidence']['native_type_value_review']=ident(native)
c['evidence']['source_blind_review']={'actor':'trace_domain_blind_decoder_8a39','source_visible':False,'originals':str((e/'decoder-originals/blind_decoder_8a39').relative_to(r))}
c['evidence']['fresh_source_semantic_review']={'actor':'trace_exp_fresh_source_51c8','public_verdict':pa['verdict'],'private_verdict':ta['verdict'],'binding':pa['publication_binding_sha256'],'raw_originals':str((e/'source-review/trace_exp_fresh_source_51c8/originals').relative_to(r))}
c['evidence']['reader_review']={'static_preview':'reader-preview-v2','preview_manifest_sha256':'d4a81e04b876d2366b884e729581c07efb03ada299c9c58bd83b12866a15b524','actual_browser_and_visual':'pending','first_renderer_failure':'retained exact KeyError scope; source/Lean unchanged; fixed six fields independently reviewed'}
c['evidence']['snapshot_counters']['qualification']='Historical pre-intake metadata-author counters only; actual current normal stage and actual proof/source/native evidence above supersede them.'
c['truth_boundary']=current_boundary
c['integration_notes']['status']='Canonical main/imports/Registry/sourceIndex/global graph/site integration held by original owners; isolated source/native/reader work and safe public progress are separate. No new Goal/reset or takeover.'
c['integration_notes']['main_observation_scope']='Actual Root git ls-remote toolabebd5 exit0: main9448a8b6692ec17408e99f5aadafcd321d0daedf, public f1d58. Actual immutable main ledger read tool86d5de confirms both original owners still STABILIZING. Local replay is not a release.'
c['phase_snapshot']='Actual immutable local P/T and independent native/source/decoder complete; one normal EXPLORING owner, PL0/V0. Six citation-scope display fields repaired with independent exact-delta review; isolated v2 static render passed. Actual browser/visual, normal PL/V, main/site/purification/full paper remain separate.'
dump(cp,c)
dump(e/'local-cycle-memory.json',{'normal_state':'EXPLORING','normal_PL_calls':0,'ROOT_V_calls':0,
 'mathematical_commit':'30172847ec40c24426f0b39afc4887719810eca0','native_report':ident(native),
 'current_source_binding':pa['publication_binding_sha256'],'source_review':'accepted',
 'current_correspondence':ident(mapping),'reader_runtime':'pending','main_integration':'held_original_owners',
 'full_main_lower_bounds_completed':0,'whole_Goal_complete':False})
print(json.dumps({'only_target_frontier_refreshed':True,'cell_status':c['status'],'normal_PL_calls':0,'normal_V_calls':0}))
