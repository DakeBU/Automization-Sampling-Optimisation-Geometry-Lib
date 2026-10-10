from pathlib import Path
import copy,hashlib,json,os,sys,traceback
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73';OWN=BASE/'independent-source73';OLD=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/independent-header-source73'
LF='CRLF byte pairs -> LF only; preserve bare CR and every other byte'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':LF}
def member(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def write(n,x):
 p=OWN/n;assert not p.exists(),str(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def check(r):
 p=ROOT/r['path'];b=p.read_bytes();assert sha(b)==r['RAW_sha256'] and len(b)==r['RAW_bytes'];assert sha(b.replace(b'\r\n',b'\n'))==r['LF_sha256']
try:
 assert not(OWN/'lease.final.json').exists()
 # This small spec is authored only after the distinct reviewer and actual root apply receipts arrive.
 authority=load(OWN/'reader-metadata-overlay73/final-authority.json')
 assert authority['independent_repair_accepted'] is True and authority['root_actual_application_completed'] is True
 assert authority['proposal_author_is_not_repair_approver'] is True
 for r in authority['authority_input_pins']:check(r)
 proposal=load(OWN/'reader-metadata-overlay73/proposal.json');assert proposal['author_self_approval'] is False
 frozen=load(OWN/'StageB.finite-current-inputs73.json');packet=load(BASE/'source-review.packet.json')
 assert packet['packet_sha256']==frozen['canonical_packet_sha256']
 version_rows=[];current_pins=[]
 for r in frozen['current_frozen_inputs']:
  p=ROOT/r['path'];current=pin(p)
  if p.as_posix() in [str(ROOT/c['canonical_path']).replace('\\','/') for c in proposal['changes']]:
   c=next(c for c in proposal['changes'] if ROOT/c['canonical_path']==p)
   assert current['RAW_sha256']==c['proposed']['RAW_sha256']
   original=(ROOT/c['before']['path']).read_bytes();assert sha(original)==r['RAW_sha256']
   a=json.loads(original);b=load(p)
   if c['JSON_pointer'].startswith('/items/'):
    assert b['items'][0]['purification']['dead_code_audit']==c['proposed_value'];b['items'][0]['purification']['dead_code_audit']=c['old_value']
   else:
    assert b['purification']['dead_code_audit']==c['proposed_value'];b['purification']['dead_code_audit']=c['old_value']
   assert a==b
   i=len(version_rows);out=OWN/'final-inputs';out.mkdir(exist_ok=True)
   (out/f'{i}.exactraw.snapshot').write_bytes(p.read_bytes());(out/f'{i}.LF.snapshot').write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
   version_rows.append({'canonical_path':r['path'],'JSON_pointer':c['JSON_pointer'],'historical':r,'current':current,'proposal':c['proposed'],'only_change':{'before':c['old_value'],'after':c['proposed_value']},'current_RAW_snapshot':f'final-inputs/{i}.exactraw.snapshot','current_LF_snapshot':f'final-inputs/{i}.LF.snapshot'})
  else:check(r)
  current_pins.append(current)
 assert len(version_rows)==2
 for r in frozen['protocol_and_freeze_inputs']:check(r)
 for r in load(OWN/'preparation.source-contract-inputs73.json')['inputs']:check(r)
 write('final-current-input-version-map73.json',{'status':'EXACT_TWO_FIELD_METADATA_OVERLAY_ONLY','historical_frozen_inputs':pin(OWN/'StageB.finite-current-inputs73.json'),'changed_current_inputs':2,'unchanged_current_inputs':6,'version_rows':version_rows,'current_inputs':current_pins,'publication_binding_sha256':packet['publication_binding_sha256'],'review_context_canonical_sha256':sha(canon(packet['candidate_publication_context'])),'anonymous_packet_or_module_or_lesson_or_formula_changed':False,'repair_authority':authority,'own_proposal_self_approved':False,'source_mathematics_changed':False})
 # Exact actual publication payload, without a project/site scan.
 pub=load(ROOT/'website/content/publications/pbps-actual-harmonic-flow.json')['items'][0];lesson=load(ROOT/'website/content/declaration_lessons/pbps-actual-harmonic-flow.json')['units'][0];binding=pub['bindings'][0];module=(ROOT/packet['lean']['file']).read_bytes()
 payload={'file':sha(module),'current_lean_module':module.decode(),'toolchain':sha((ROOT/'lean-toolchain').read_bytes().decode().replace('\r\n','\n').encode()),'dependencies':sha((ROOT/'lake-manifest.json').read_bytes().decode().replace('\r\n','\n').encode()),'source':pub['source'],'statement':pub['statement'],'formulae':pub['formulae'],'assumptions':pub['assumptions'],'obligations':pub['obligations'],'lesson':lesson,'binding':{k:v for k,v in binding.items() if k not in {'audit_id','legacy_audit_debt'}}}
 assert sha(canon(payload))==packet['publication_binding_sha256']
 context=copy.deepcopy(payload);context['binding']={k:context['binding'][k] for k in ('declaration','role','supports')};context['lesson']={k:v for k,v in context['lesson'].items() if k not in {'boundary','source_history_boundary'}};context['candidate_assumptions']=[{k:r[k] for k in ('source','lean')} for r in binding['assumption_deltas']]
 assert context==packet['candidate_publication_context']
 judgment=load(OWN/'source.0.semantic-judgments73.frozen.json')
 assert len(judgment['semantic_slots'])==7 and len(judgment['deltas'])==10 and judgment['blocking_mathematical_deltas']==0
 write('source-proof-coverage73.json',{'schema':'astis-independent-whole-source73-coverage-index/v1','source_graph':pin(OLD/'source-proof-graph73.reviewed-projection.json'),'source_inventory':pin(OLD/'StageA.independent-source79-classification73.frozen.json'),'source_expectations_before_header_and_BODY':pin(OLD/'StageA.source-expectations73.before-header.frozen.json'),'current_module':pin(ROOT/packet['lean']['file']),'source79_current_map':pin(OWN/'source79-current-coverage73.json'),'source_nodes_edges_bridges_current_map':pin(OWN/'source-proof-implementation-coverage73.json'),'whole_module_line_coverage':pin(OWN/'whole178-line-coverage73.json'),'callers_definitions_conclusions':pin(OWN/'caller-definition-nine-conclusion-review73.json'),'lesson_formula_BODY_coverage':pin(OWN/'six-step-formula-exposition-review73.json'),'source_URL_anchor_accuracy':pin(OWN/'StageB.source-URL-anchor-accuracy73.json'),'current_version_mapping':pin(OWN/'final-current-input-version-map73.json'),'counts':{'module_lines':178,'source_regions':13,'source_blocks':51,'source_items':79,'NODE':24,'EXCLUDED':55,'source_nodes':23,'source_edges':37,'internal_bridges_produced':7,'source_callers':6,'conclusions':9,'lesson_steps':6},'unclassified':0,'source_graph_is_not_Lean_graph':True,'all_source_classifications_unchanged':True,'local_source_math_exposition_accepted':True,'full_Exposition_Seal_or_stochastic_full_paper_credit':False})
 core_inputs={'final_current_inputs':current_pins,'historical_versions':frozen['current_frozen_inputs'],'protocol_and_freeze_inputs':frozen['protocol_and_freeze_inputs'],'immutable_source_contract_inputs':load(OWN/'preparation.source-contract-inputs73.json')['inputs'],'primary_reference':frozen['primary_reference'],'repair_authority_inputs':authority['authority_input_pins']}
 write('source.0.input-manifest.json',{'schema':'astis-finite-source73-inputs-and-versions/v1',**core_inputs,'new_large_source_or_history_copies':False,'current_input_count':len(current_pins),'historical_input_count':len(frozen['current_frozen_inputs']),'source_contract_input_count':17,'version_map':pin(OWN/'final-current-input-version-map73.json'),'LF_recipe':LF})
 supplemental='\n\nThe separate two-field reader/process metadata repair is now independently approved and actually applied by the root writer. The exact authority pins and actual receipts are in reader-metadata-overlay73/final-authority.json; the two current publication/cell RAW replacements are mapped against the original exact snapshots in final-current-input-version-map73.json. Only purification.dead_code_audit changed. All candidate mathematics, the blind reconstruction, official source packet, publication binding and review context remain exact. I authored the proposal and did not approve that repair myself. This completes the reader metadata condition for this source admission, without granting a theorem repair, Exposition Seal, PURIFIED or VERIFIED.\n'
 (OWN/'source.0.review.RAW.md').write_bytes((OWN/'source.0.math-source-review.RAW.md').read_bytes()+supplemental.encode())
 write('observer-negatives73.json',{'observations':[{'operation':'Initial combined packet/freeze/map stdout','tool_chunk':'9887b7','effect':'Tool output truncated; exact inputs were subsequently frozen/parsed and complete module/publication/lesson/decoder/source rows read in bounded views','input_mutation':False},{'operation':'rg for schema and a nonexistent tools/astis_publication_core.py','effect':'Missing-file OS error2; corrected to actual tools/astis_publication.py after rg --files','actual_PID':'not exported by observation tool; not invented','source_or_mathematical_failure':False,'input_mutation':False},{'operation':'Verbose old79-row source print','effect':'Stdout truncated; all79 current rows then printed in a concise complete view; final finite coverage has no omissions','input_mutation':False}],'productive_commands_have_actual_PID_EXIT_receipts':True})
 write('source.0.close.terminal.json',{'actual_pid':os.getpid(),'exit_code':0,'argv':sys.argv,'background':False,'no_Lean_site_or_graph_rerun':True})
 review_run={'schema':'astis-independent-whole-source-review73-native/v1','reviewer':'/root/independent_primary69','status':'WHOLE_IMPLEMENTATION_SOURCE_AND_LOCAL_EXPOSITION_REVIEW_COMPLETE','owned_scope':OWN.relative_to(ROOT).as_posix(),'canonical_packet_sha256':packet['packet_sha256'],'official_packet_RAW':pin(BASE/'source-review.packet.json'),'publication_binding_sha256':packet['publication_binding_sha256'],'review_context_canonical_sha256':sha(canon(context)),'source_verdict':judgment['verdict'],'semantic_slots':judgment['semantic_slots'],'deltas':judgment['deltas'],'repairs':[],'coverage':pin(OWN/'source-proof-coverage73.json'),'review':pin(OWN/'source.0.review.RAW.md'),'input_manifest':pin(OWN/'source.0.input-manifest.json'),'reader_metadata_overlay':authority,'prior_source_native_CLOSED52':pin(OLD/'lease.final.json'),'whole_source_graph_rederived':False,'fresh_math_compile_or_other_verdict_used':False,'terminal_receipts':[pin(OWN/n) for n in ['preparation.terminal.json','StageB.freeze-current.terminal.json','coverage-authoring.terminal.json','semantic-authoring.terminal.json','reader-metadata-overlay73/proposal.terminal.json','reader-metadata-overlay73/authority.terminal.json','source.0.close.terminal.json']],'credit_boundary':{'implementation_source_fidelity':True,'local_formula_proof_exposition':True,'independent_SCI':False,'VERIFIED':False,'repository_integration':False,'Exposition_Seal':False,'PURIFIED':False,'main_live':False,'whole_paper':False,'Goal':False},'whole_logical_hash_recipe':'SHA256 canonical JSON UTF8 ensure_ascii=False sort_keys=True separators=(comma,colon); delete ONLY top-level run_sha256'}
 review_run['run_sha256']=sha(canon(review_run));write('source.0.run.json',review_run)
 source_review={'state':'accepted','reviewer':'/root/independent_primary69','independent_from_formalizer':True,'independent_from_decoder':True,'evidence':(OWN/'source.0.review.RAW.md').relative_to(ROOT).as_posix(),'review_run_sha256':review_run['run_sha256'],'reviewer_packet_sha256':packet['packet_sha256'],'run_artifact':(OWN/'source.0.decision.json').relative_to(ROOT).as_posix()}
 audit_fields={'state':'source-reviewed','verdict':judgment['verdict'],'semantic_slots':judgment['semantic_slots'],'deltas':judgment['deltas'],'source_review':source_review,'repairs':[]}
 decision={**audit_fields,'reviewer':'/root/independent_primary69','independent_from_formalizer':True,'independent_from_decoder':True,'review_evidence':source_review['evidence'],'review_run_sha256':review_run['run_sha256'],'reviewer_packet_sha256':packet['packet_sha256'],'official_packet_RAW_sha256':frozen['packet_RAW_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'blocking_semantic_deltas':0,'whole_module_source_coverage':pin(OWN/'source-proof-coverage73.json'),'reader_metadata_repair_separate_authority':authority,'no_VERIFIED_transition_or_canonical_write':True}
 write('source.0.decision.json',decision)
 coverage={'source_graph':(OLD/'source-proof-graph73.reviewed-projection.json').relative_to(ROOT).as_posix(),'source_inventory':(OLD/'StageA.independent-source79-classification73.frozen.json').relative_to(ROOT).as_posix(),'coverage_report':pin(OWN/'source-proof-coverage73.json'),'coverage_status':'Independent whole178-line implementation/source and six exact formula/BODY steps reviewed:13regions51blocks79items24NODE55EXCLUDED; unchanged23nodes37edges;7 omitted-source bridges produced internally; same6callers/all9conclusions. Local source/math exposition only; no stochastic kernel/nonexplosion/invariance, full Exposition Seal, PURIFIED, main/live, full-paper or Goal credit.'}
 admission={'official_packet_sha256':packet['packet_sha256'],'official_packet_RAW_sha256':frozen['packet_RAW_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'audit_fields':audit_fields,'cell_source_proof_coverage':coverage,'publication_source_proof_coverage':copy.deepcopy(coverage),'canonical_writes_by_reviewer':False}
 write('source.0.admission-fields.json',admission)
 sys.path.insert(0,str(ROOT/'tools'));import astis_semantic_roundtrip_core as semantic
 audit=load(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json');before=semantic.semantic_reviewer_packet(audit);assert before==packet
 after=copy.deepcopy(audit);after.update(copy.deepcopy(audit_fields));assert semantic.semantic_reviewer_packet(after)==before
 protocol={k:'required' for k in ['decoder_blindness','decoder_context_content_scan','independent_source_review','source_review_packet_binding','independent_repair_review','repair_review_packet_binding']};protocol['semantic_slots']=list(semantic.SEMANTIC_SLOTS);protocol['decoder_allowed_inputs']=list(semantic.DECODER_INPUT_ARTIFACTS)
 errors=semantic.validate_registry({'schema_version':1,'protocol':protocol,'audits':[after]});assert not errors,errors
 # Coverage is top-level metadata excluded by the exact reviewed payload recipe.
 proposed_pub=copy.deepcopy(pub);proposed_pub['source_proof_coverage']=copy.deepcopy(coverage)
 payload_after=copy.deepcopy(payload);payload_after.update({k:proposed_pub[k] for k in ('source','statement','formulae','assumptions','obligations')});assert canon(payload_after)==canon(payload)
 write('canonical-admission-contract-check73.json',{'actual_pid':os.getpid(),'exit_code':0,'canonical_semantic_registry_schema_errors':errors,'audits_checked':1,'whole_registry_other_verdicts_read':False,'semantic_reviewer_packet_before_after_exact_equal':True,'canonical_packet_sha256':packet['packet_sha256'],'publication_binding_sha256_unchanged':packet['publication_binding_sha256'],'review_context_sha256_unchanged':sha(canon(context)),'coverage_metadata_does_not_enter_current_binding_or_context':True,'portable_repository_relative_evidence_and_coverage_paths':True,'canonical_mutation_performed':False})
 named=[]
 for n in ['source.0.review.RAW.md','source.0.decision.json','source.0.input-manifest.json','source.0.run.json','source.0.admission-fields.json']:
  p=OWN/n;named.append({'name':n,'pin':pin(p),'complete_RAW_UTF8':p.read_bytes().decode()})
 write('complete-named-review-decision-input-payload.json',{'schema':'astis-small-complete-named-whole-source73/v1','named_payload_count':5,'named_payloads':named,'whole_logical_run_sha256':review_run['run_sha256'],'all_additional_owned_evidence':'whole-owned.manifest.json and last lease enumerate exact complete evidence','prior_CLOSED_history':'immutable finite referenced pins only; no recursive historical payload or base64 copies'})
 files=sorted(p for p in OWN.rglob('*') if p.is_file());write('whole-owned.manifest.json',{'schema':'astis-owned-source73-manifest/v1','scope':OWN.relative_to(ROOT).as_posix(),'count':len(files),'files':[member(p) for p in files],'excludes':['whole-owned.manifest.json (self)','lease.final.json (last closure)'],'LF_recipe':LF})
 files=sorted(p for p in OWN.rglob('*') if p.is_file())
 # LAST OWNED WRITE. All later operations must be external read-only.
 write('lease.final.json',{'schema':'astis-CLOSED-LAST-source73/v1','status':'CLOSED_LAST','owned_scope':OWN.relative_to(ROOT).as_posix(),'actual_close_PID':os.getpid(),'exit_code':0,'background':False,'owned_file_count_including_self':len(files)+1,'member_count_except_self':len(files),'all_files_except_self':[member(p) for p in files],'whole_owned_manifest':pin(OWN/'whole-owned.manifest.json'),'whole_logical_run_sha256':review_run['run_sha256'],'LF_recipe':LF,'close_order':'lease.final.json last owned write; postclose read-only','canonical_Git_ledger_or_old_CLOSED_written':False,'VERIFIED_or_full_paper_credit':False})
 print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'owned_file_count':len(files)+1,'whole_logical_run_sha256':review_run['run_sha256'],'decision':pin(OWN/'source.0.decision.json'),'admission_fields':pin(OWN/'source.0.admission-fields.json'),'payload':pin(OWN/'complete-named-review-decision-input-payload.json'),'manifest':pin(OWN/'whole-owned.manifest.json'),'lease':pin(OWN/'lease.final.json')},indent=2))
except BaseException:
 traceback.print_exc();sys.exit(1)
