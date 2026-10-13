from pathlib import Path
import json,hashlib,os,sys,datetime,types,re
sys.dont_write_bytecode=True
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-sharp-energy68';S=B/'independent-source68';P=B/'energy-alias-overlay68';O=B/'independent-energy-alias-overlay68'
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
rows=[];order=[]
def freeze(p,label,json_value=True):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');i=len(rows);raw=f'inputs/{i:02d}.RAW.snapshot';ln=f'inputs/{i:02d}.LF.snapshot';(O/raw).write_bytes(b);(O/ln).write_bytes(lf);rows.append({'source_path':p.relative_to(R).as_posix(),'label':label,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf),'raw_snapshot':raw,'lf_snapshot':ln});order.append({'ordinal':i,'label':label,'source_path':p.relative_to(R).as_posix(),'RAW_sha256':sha(b),'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});return json.loads(b) if json_value else b
lease=freeze(S/'lease.final.json','IMMUTABLE_SOURCE_CLOSED363');assert rows[-1]['RAW_sha256']=='e5962c11b38f64e3d782175c959e2c25c4b5e2bcad750eaf963cf4f547c89aeb' and lease['status']=='CLOSED_LAST'
manifest=freeze(S/'owned-manifest.json','SOURCE_CLOSED363_FINITE_MANIFEST');assert len([p for p in S.rglob('*') if p.is_file()])==363;assert sha((S/'owned-manifest.json').read_bytes())==lease['owned_manifest']['RAW_sha256']
for e in manifest['all_regular_owned_files_excluding_manifest_self_and_final_lease']:
 b=(S/e['path']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256']
run=freeze(S/'review-run.json','WHOLE_NATIVE_SOURCE_LOGICAL_RUN');assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']=='e987d89be0647776605af9fdd96c49ce309355540bf927823ae1fda9f7d534ce'
full=freeze(S/'complete-RAW-decision.json','COMPLETE_SOURCE_DECISIONS');assert full['review_run_sha256']==run['run_sha256']
native=freeze(S/'source.0.decision.json','ORIGINAL_GENERIC_SEVEN_SLOT_NATIVE_DECISION');assert native['verdict']=='equivalent-after-elaboration'
expect=freeze(S/'primary-first-expectations.json','SOURCE_EXPECTATIONS_PRECEDING_ALL68_CANDIDATES')
coverage=freeze(S/'primary344.readback.json','EXACT344_SOURCE_COVERAGE_REUSE');primary=freeze(S/'inputs/000.RAW.snapshot','EXACT_FROZEN_PRIMARY_RAW',False);assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for e in coverage['items']:
 a,b=e['source_RAW_range_end_exclusive'];assert sha(primary[a:b])==e['RAW_sha256'] and e['alt_annotation_exact']
assert len(coverage['items'])==344 and coverage['missing_items']==0 and len(coverage['six_regions'])==6
limit=freeze(S/'nonblocking-exposition-limitation-S-T.json','EXACT_ALIAS_LIMITATION_TO_BE_CLOSED')
binding=freeze(S/'packet-bindings-and-context.readback.json','ORIGINAL_PACKET_BINDING_CONTEXT_MAP')
body=freeze(S/'eleven-literal-BODY-spans.readback.json','EXACT11_ORIGINAL_FORMULA_BODY_MAP')
oldpacket=freeze(S/'final-inputs/000.RAW.snapshot','EXACT_ORIGINAL_GENERIC_SOURCE_PACKET')
oldlesson=freeze(S/'final-inputs/current004.RAW.snapshot','EXACT_ORIGINAL_GENERIC_LESSON')
oldactual=freeze(S/'final-inputs/current006.RAW.snapshot','EXACT_OTHER_SIX_STEP_LESSON')
modules=[]
for e in binding['entries']:
 p=(S/f"final-inputs/{e['packet_index']:03d}.RAW.snapshot");pk=json.loads(p.read_bytes());m=freeze(R/pk['lean']['file'],'UNCHANGED_LEAN_MODULE_'+str(e['packet_index']),False);assert sha(m)==e['full_module_raw_sha256'];modules.append(m)
proposal=freeze(P/'proposal.json','EXACT_ALIAS_ONLY_PROPOSAL');assert rows[-1]['RAW_sha256']=='901cbad61d84c46c42df8ee5b8613b12ba9fa1c1b4598d1f1a8b85e82d4c5c03'
bl=freeze(P/'0.before.exactraw.snapshot.json','BEFORE_LESSON');al=freeze(P/'0.after.context-only.exactraw.snapshot.json','AFTER_LESSON');ba=freeze(P/'1.before.exactraw.snapshot.json','BEFORE_AUDIT_HISTORICAL_REVIEW_NOT_SOURCE_EVIDENCE');aa=freeze(P/'1.after.context-only.exactraw.snapshot.json','AFTER_AUDIT_HISTORICAL_REVIEW_NOT_NEW_ACCEPTANCE');packet=freeze(P/'proposed.reviewer-packet.json','NEW_EXACT_PACKET')
for ch in proposal['changes']:
 assert sha((P/ch['before_snapshot']).read_bytes())==ch['before_RAW_sha256'];assert sha((P/ch['proposed_context_snapshot']).read_bytes())==ch['proposed_context_RAW_sha256']
for p in [R/'tools/astis_semantic_roundtrip_core.py',R/'tools/astis_publication.py',R/'website/scripts/declaration_lessons.py']:freeze(p,'OFFICIAL_FINITE_SCHEMA_AND_BINDING_CODE',False)
publication=freeze(R/'website/content/publications/hilbert-sharp-quadratic-corrector-bound.json','UNCHANGED_GENERIC_PRODUCTION_PUBLICATION')
freeze(R/'lean-toolchain','FIXED_TOOLCHAIN',False);freeze(R/'lake-manifest.json','FIXED_DEPENDENCIES',False)
actual=freeze(R/'website/content/declaration_lessons/pbps-sharp-corrector-energy.json','CURRENT_OTHER_SIX_STEP_LESSON');currentlesson=freeze(R/'website/content/declaration_lessons/hilbert-sharp-quadratic-corrector-bound.json','CANONICAL_LESSON_STILL_BEFORE_APPLICATION');currentaudit=freeze(R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound.json','CANONICAL_AUDIT_STILL_BEFORE_APPLICATION')
assert bl==oldlesson==currentlesson and actual==oldactual and ba==currentaudit
newtext='Set S=‖u‖²+‖v‖² and T=‖u-Kv‖²+‖Ku+v‖²=‖Du‖²+‖Dv‖² throughout this five-step proof. Triangle inequality and the inner-product bound control E. The operator norm controls each D component.'
assert proposal['new_text']==al['units'][0]['steps'][2]['text']==newtext
assert newtext=='Set S=‖u‖²+‖v‖² and T=‖u-Kv‖²+‖Ku+v‖²=‖Du‖²+‖Dv‖² throughout this five-step proof. '+proposal['old_text']
def diff(a,b,path=''):
 if type(a)!=type(b):return [{'pointer':path,'before':a,'after':b}]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append({'pointer':path+'/'+k,'before':a.get(k,'__ABSENT__'),'after':b.get(k,'__ABSENT__')})
   else:out+=diff(a[k],b[k],path+'/'+k)
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [{'pointer':path,'before':a,'after':b}]
  out=[]
  for i,(x,y) in enumerate(zip(a,b)):out+=diff(x,y,path+'/'+str(i))
  return out
 return [] if a==b else [{'pointer':path,'before':a,'after':b}]
ld=diff(bl,al);ad=diff(ba,aa);pd=diff(oldpacket,packet)
assert [x['pointer'] for x in ld]==['/units/0/steps/2/text'];assert {x['pointer'] for x in ad}=={'/publication_binding_sha256','/publication_context/lesson/steps/2/text'};assert {x['pointer'] for x in pd}=={'/publication_binding_sha256','/candidate_publication_context/lesson/steps/2/text','/packet_sha256'}
assert aa['source_review']==ba['source_review'];assert aa['source_review']['reviewer_packet_sha256']==oldpacket['packet_sha256']!=packet['packet_sha256'];assert packet['packet_sha256']==proposal['new_reviewer_packet_sha256']=='11395879d5ba081c9b57d10f64b62067d42cdbf9d35480e23c89c62bfab347a7';assert sha(canon({k:v for k,v in packet.items() if k!='packet_sha256'}))==packet['packet_sha256']
sys.path[:0]=[str(R/'tools'),str(R/'website/scripts')]
import astis_semantic_roundtrip_core as core
import astis_publication as pub
assert core.semantic_reviewer_packet(aa)==packet and core.semantic_reviewer_packet(ba)==oldpacket
assert core.decoder_packet(aa)==core.decoder_packet(ba);assert packet['source']==oldpacket['source'] and packet['lean']==oldpacket['lean'] and packet['blind_reconstruction']==oldpacket['blind_reconstruction'];assert all(v is False for v in packet['anti_anchoring'].values())
item=publication['items'][0];bind=item['bindings'][0];lesson=al['units'][0];data={'declarations':{packet['lean']['declaration']:types.SimpleNamespace(source_file=packet['lean']['file'])},'lessons':{packet['lean']['declaration']:lesson}}
assert pub.review_context(item,bind,data)==packet['candidate_publication_context'];assert pub.binding_digest(item,bind,data)==packet['publication_binding_sha256']==proposal['proposed_binding']=='2e92da3e346ebabd5920ad2104a8d3b71e40c1bc07c680c1aa1043e19aae6fdd'
assert packet['candidate_publication_context']['current_lean_module'].encode()==modules[0]
assert len(body['steps'])==11
for s in body['steps']:
 e=s['region'];b=(R/e['path']).read_bytes();assert sha(b)==e['source_raw_sha256'];literal=b''.join(b.splitlines(keepends=True)[e['start_line']-1:e['end_line']]);assert sha(literal)==e['exact_code_raw_sha256']
for before,after in zip(bl['units'][0]['steps'],al['units'][0]['steps']):
 assert before['formula']==after['formula'] and before['lean']==after['lean'] and before['lean_source_region']==after['lean_source_region']
# The T equality is exactly the already-reviewed hBlock, preceding alias introduction at step3.
assert 'have hBlock : ‖u-K v‖^2+‖K u+v‖^2=‖D u‖^2+‖D v‖^2' in modules[0].decode();assert limit['missing_explicit_definitions']['S']=='‖u‖²+‖v‖²';assert limit['missing_explicit_definitions']['T']=='‖u−K v‖²+‖K u+v‖² = ‖D u‖²+‖D v‖²'
write('finite-diffs-and-unchanged-bindings.audit.json',{'status':'EXACT_ONE_PROSE_FIELD_PLUS_DERIVED_BINDING_CONTEXT_PACKET_CHANGE_ONLY','actual_pid':os.getpid(),'lesson_diff':ld,'audit_diff':ad,'packet_diff':pd,'unchanged_source_Lean_full_private_Props_reconstruction_decoder_packet':True,'all11_formulas_LITERAL_BODY_source_regions_unchanged':True,'no_new_blind_decode_required':'Exact same neutral decoder packet, complete Lean signature/module and existing reconstruction. Only prose aliases for already explicit quantities changed.','historical_source_review_preserved_but_stale':True,'historical_source_review_consumed_as_new_acceptance':False,'new_packet_canonical_sha256':packet['packet_sha256'],'new_packet_RAW_sha256':sha((P/'proposed.reviewer-packet.json').read_bytes()),'new_binding_sha256':packet['publication_binding_sha256'],'new_context_canonical_sha256':sha(canon(packet['candidate_publication_context'])),'old_packet_canonical_sha256':oldpacket['packet_sha256'],'old_binding_sha256':oldpacket['publication_binding_sha256'],'old_context_canonical_sha256':sha(canon(oldpacket['candidate_publication_context']))})
slots=json.loads(json.dumps(native['semantic_slots']));reuse={}
for k,v in slots.items():
 reuse[k]={'native_relation':v['relation'],'exact_unchanged_source_and_Lean':True,'native_source_run_sha256':run['run_sha256'],'native_packet_sha256':oldpacket['packet_sha256'],'bounded_overlay_check':'No source/Lean/binder/quantifier/domain/constant/conclusion/scope change; exact original independent seven-slot decision reused.'}
slots['objects']['evidence']+=' Alias-only reader clarification: S is the existing sum ‖u‖²+‖v‖²; T is existing block sum ‖u−Kv‖²+‖Ku+v‖². Equality to ‖Du‖²+‖Dv‖² is hBlock from preceding step2. Both are real nonnegative energy aliases valid under unchanged H,K,D,c,u,v throughout the five-step proof, not new objects/binders/providers.'
reuse['objects']['bounded_overlay_check']='Exact prefix defines missing S,T with already explicit norm sums; second T expression follows exact hBlock. No new mathematical premise, product-max-norm claim, or change in source constant.'
write('complete-RAW-input-payload.json',{'schema':1,'actual_pid':os.getpid(),'entries':rows,'entry_count':len(rows),'source_first_native344_reuse_before_new_proposed_packet':True,'first_input_order':order,'no_CLOSED_source_or_adapter_folder_modified':True})
a={'schema':'independent-energy-alias-overlay68-native-decision-v1','reviewer':'/root/independent_header_source68','independent_from_formalizer':True,'independent_from_decoder':True,'audit_id':aa['id'],'verdict':'equivalent-after-elaboration','decision':'APPROVED_EXACT_ALIAS_PREFIX_AND_REFRESHED_PACKET_BINDING_CONTEXT','reviewer_packet_sha256':packet['packet_sha256'],'reviewer_packet_RAW_sha256':sha((P/'proposed.reviewer-packet.json').read_bytes()),'publication_binding_sha256':packet['publication_binding_sha256'],'candidate_context_canonical_sha256':sha(canon(packet['candidate_publication_context'])),'proposal_RAW_sha256':sha((P/'proposal.json').read_bytes()),'native_source_run_sha256':run['run_sha256'],'native_source_lease_RAW_sha256':sha((S/'lease.final.json').read_bytes()),'native_complete_RAW_decision_sha256':sha((S/'complete-RAW-decision.json').read_bytes()),'native_generic_decision_RAW_sha256':sha((S/'source.0.decision.json').read_bytes()),'approved_exact_text':newtext,'approved_direct_field':'units[0].steps[2].text','approved_derived_fields':['publication_binding_sha256','publication_context.lesson.steps[2].text','candidate_publication_context.lesson.steps[2].text','packet_sha256'],'semantic_slots':slots,'seven_slot_reuse_and_bounded_object_check':reuse,'deltas':[{'slot':'objects','severity':'informational','description':'Introduce exact S,T real energy aliases in step3 prose throughout existing five-step proof.','evidence':'S=‖u‖²+‖v‖²; T=‖u−Kv‖²+‖Ku+v‖²=‖Du‖²+‖Dv‖². Exact hBlock already proven in preceding step2; all norm sums, formulas, Lean and witnesses unchanged.'}],'repairs':[],'blocking_deltas':[],'source_mathematical_repair':False,'alias_limitation_closed_conditionally_on_exact_application':True,'specified_aliases_only':True,'original_other_nonblocking_limits_and_residuals_retained':native['nonblocking_limits'],'full_Exposition_Seal':False,'PURIFIED':False,'VERIFIED_transition_claim':False,'full_paper_or_Goal_complete':False,'own_compiler_started':False,'canonical_Git_ledger_proof_Goal_writes':False,'source_review_refresh_required':'Proposed audit keeps historical old source_review; it must be refreshed to this independently accepted new packet/run before application/admission. Historical source_review is never evidence of new packet acceptance.','review_evidence':'Original CLOSED363 independent primary-first source review and exact unchanged all-seven-slot reuse, plus fresh bounded S,T object/formula-scope review, exact new anti-anchored packet and official production binding/context recomputation. Entire source/Lean/private Props/decoder reconstruction unchanged; eleven exact BODY spans verified.','actual_author_pid':os.getpid()}
r={'schema':'whole-logical-independent-energy-alias-overlay68-v1','decision_without_external_run_reference':a,'complete_input_payload_RAW_sha256':sha((O/'complete-RAW-input-payload.json').read_bytes()),'finite_diffs_RAW_sha256':sha((O/'finite-diffs-and-unchanged-bindings.audit.json').read_bytes()),'actual_author_pid':os.getpid(),'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};r['run_sha256']=sha(canon(r));write('review-run.json',r);a['review_run_sha256']=r['run_sha256'];a['source_review_refresh_provenance']={'state':'accepted','reviewer':a['reviewer'],'independent_from_formalizer':True,'independent_from_decoder':True,'evidence':a['review_evidence'],'review_run_sha256':r['run_sha256'],'reviewer_packet_sha256':packet['packet_sha256'],'run_artifact':'runs/20261007-companion-priority/pbps-sharp-energy68/independent-energy-alias-overlay68/review-run.json','original_native_source_run_sha256':run['run_sha256'],'original_source_lease_RAW_sha256':sha((S/'lease.final.json').read_bytes()),'exact_new_publication_binding_sha256':packet['publication_binding_sha256'],'exact_new_context_canonical_sha256':a['candidate_context_canonical_sha256']};write('complete-RAW-decision.json',a)
print('ENERGY_ALIAS_OVERLAY_APPROVED_EXIT0',os.getpid(),len(rows),'INPUTS','7_SLOTS','11_UNCHANGED_BODY',r['run_sha256']);print('PACKET_RAW',a['reviewer_packet_RAW_sha256']);print('NEW_CONTEXT',a['candidate_context_canonical_sha256']);print('RAW_DECISION',sha((O/'complete-RAW-decision.json').read_bytes()));print('RAW_INPUT',sha((O/'complete-RAW-input-payload.json').read_bytes()))
