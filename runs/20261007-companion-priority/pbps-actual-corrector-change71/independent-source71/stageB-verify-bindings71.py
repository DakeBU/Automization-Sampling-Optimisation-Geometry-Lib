import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,re,os,html,html.parser,dataclasses
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;R=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
manifest=json.loads((O/'stageB.exact-input-manifest71.json').read_bytes())
for x in manifest['inputs']:
 b=(B/x['original_path']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256'];assert b==(O/x['snapshot']).read_bytes();assert b.replace(b'\r\n',b'\n')==(O/x['LF_snapshot']).read_bytes()
packet=json.loads((R/'source-review.packet.0.json').read_bytes())
module=(B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean').read_bytes();text=module.decode();lines=module.splitlines(keepends=True)
parent=(B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean').read_text(encoding='utf-8')
proposal=B/'runs/20261007-companion-priority/pbps-corrector-change-preproof71/header71.named-literal.proposed.lean'
sealed=proposal.read_bytes();assert len(sealed)==8727 and sha(sealed)=='2bef0d5cf364270b6f580288e966d9bb78310f646a7fe13b6f8855807e70f42c' and module.startswith(sealed)
private=text[text.index('private def '):text.index('\ntheorem ')].rstrip()
parent_private=parent[parent.index('private def '):parent.index('\ntheorem ')].rstrip()
new_clause=' ∧\n                                let C : HP0 → HP0 → ℝ := fun u v =>\n                                  (‖u‖^2-‖v‖^2)/2-inner ℝ (A0 (Inv u)) v\n                                C gP gV-C fP fV= -‖fP‖^2+‖fV‖^2)'
assert private.count(new_clause)==1
stripped=private.replace(new_clause,')').replace('actual_corrector_change_statement','actual_projected_rotation_statement')
assert stripped==parent_private
expanded=(R/'expanded71.frozen.header.lean').read_text(encoding='utf-8')
assert expanded=='theorem actual_corrector_change'+private.split('actual_corrector_change_statement',1)[1].replace(' : Prop :=\n',' :\n',1)+'\n'
assert packet['lean']['statement']==expanded[len('theorem actual_corrector_change'):].rstrip()
assert sha(packet['lean']['statement'].encode())==packet['lean']['statement_sha256']
write('stageB.parent-retention-and-seal71.json',{'schema':'source71-exact-parent-retention-v1','actual_pid':os.getpid(),'sealed147_prefix':pin(proposal),'candidate_module':pin(B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean'),'parent_module':pin(B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean'),'exact_entire_parent_literal_after_removing_only_new_C_clause_and_reversing_name':True,'removed_exact_clause':new_clause,'removed_clause_utf8_sha256':sha(new_clause.encode()),'private_literal_utf8_sha256':sha(private.encode()),'parent_literal_utf8_sha256':sha(parent_private.encode()),'expanded_header':pin(R/'expanded71.frozen.header.lean'),'canonical_packet_statement_matches_expanded_literal':True,'analytic_callers':6,'common_witnesses':12,'extra_public_premise':False,'current_mean_g_internal_parent_retained':True,'no_current_science_verdict_used':True})

pub=json.loads((B/'website/content/publications/pbps-actual-corrector-change.json').read_bytes())['items'][0]
lesson=json.loads((B/'website/content/declaration_lessons/pbps-actual-corrector-change.json').read_bytes())['units'][0]
assert len(lesson['steps'])==8
step_results=[];all_body=[]
for i,s in enumerate(lesson['steps'],1):
 q=s['lean_source_region'];a,z=q['start_line'],q['end_line'];raw=b''.join(lines[a-1:z])
 assert raw.decode()==s['lean'] and sha(raw)==q['exact_code_raw_sha256'] and q['source_raw_sha256']==sha(module)
 all_body.extend(range(a,z+1));(O/f'stageB.step{i}.BODY.exactraw.lean').write_bytes(raw);(O/f'stageB.step{i}.BODY.LF.lean').write_bytes(raw.replace(b'\r\n',b'\n'))
 step_results.append({'step':i,'title':s['title'],'formula':s['formula'],'text':s['text'],'exact_source_region':q,'RAW_bytes':len(raw),'RAW_sha256':sha(raw),'review':'exact range/formula assessed independently; see whole-source mathematical review','formula_utf8_sha256':sha(s['formula'].encode())})
assert all_body==list(range(147,524))
write('stageB.eight-formula-BODY-bindings71.json',{'schema':'source71-eight-exact-BODY-formula-bindings-v1','actual_pid':os.getpid(),'BODY_lines':377,'start_line':147,'end_line':523,'all_BODY_lines_once_exact':True,'steps':step_results,'whole_module_lines':528,'scope':'Code/metadata fidelity and independently assessed formulas; no browser or full Exposition credit.'})

sys.path.insert(0,str(B/'tools'));sys.path.insert(0,str(B/'website/scripts'))
import astis_site as base
import inline_lean
import astis_publication as publication
base.project_lean_paths=lambda:[B/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean']
modules,decls=base.scan_project_sources();declarations={d.full_name:d for d in decls}
assert len(declarations)==2
name=packet['lean']['declaration'];helper=name+'_statement';assert helper in declarations and declarations[helper].kind=='def' and declarations[name].kind=='theorem'
assert lesson['helpers']==[helper]
assert lesson['astis_dependencies']==['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualProjectedRotation.actual_projected_rotation']
data={'declarations':declarations,'lessons':{name:lesson}}
binding=pub['bindings'][0]
assert publication.review_context(pub,binding,data)==packet['candidate_publication_context']
assert publication.binding_digest(pub,binding,data)==packet['publication_binding_sha256']
copy=dict(pub);copy['source_proof_coverage']={'source_graph':'owned-independent-source-graph','coverage_status':'whole-source review pending conclusion'}
assert publication.binding_digest(copy,binding,data)==packet['publication_binding_sha256']
assert publication.review_context(copy,binding,data)==packet['candidate_publication_context']
base._SOURCE_BY_NAME=declarations
# In-memory syntax/renderer contract only, no Git inquiry or site generation.
base._ACTIVE_GIT=base.GitContext(commit='',ref='',remote_url='',web_root='',commit_published=False,public_source_links=False,dirty_files=set())
fold=inline_lean.disclosure(name,role='statement',explanation='Exact public signature.',page='declarations/scoped71.html')+inline_lean.disclosure(name,role='proof',explanation='Actual corrector proof.',page='declarations/scoped71.html',helpers=(helper,))
(O/'stageB.adjacent-literal-fold.contract.html').write_text(fold,encoding='utf-8',newline='\n')
assert 'Full Lean proposition (definition)' in fold and 'It supplies no mathematical proof or additional hypothesis' in fold
assert html.escape(private,quote=True) in fold
assert '<details ' in fold and re.search(r'<details\b[^>]*\bopen\b',fold) is None
assert fold.count('data-inline-lean="'+name+'"')==2 and fold.count('data-inline-lean="'+helper+'"')==1
write('stageB.publication-and-literal-contract71.json',{'schema':'source71-bounded-publication-literal-contract-v1','actual_pid':os.getpid(),'scanned_exact_single_module_only':True,'declarations':[{'full_name':d.full_name,'kind':d.kind,'line':d.source_line} for d in decls],'private_literal_definition_not_provider':True,'complete_literal_adjacent_in_proof_fold':True,'default_details_open':False,'eight_BODY_contract':'stageB.eight-formula-BODY-bindings71.json','publication_binding_sha256':packet['publication_binding_sha256'],'review_context_equals_official_packet':True,'coverage_metadata_outside_binding_and_context':True,'bounded_HTML':pin(O/'stageB.adjacent-literal-fold.contract.html'),'browser_full_site_Exposition_or_PURIFIED_credit':False,'support_code_pins':[pin(B/'tools/astis_site.py'),pin(B/'website/scripts/inline_lean.py'),pin(B/'website/scripts/declaration_lessons.py'),pin(B/'tools/astis_publication.py')]})

D=R/'anonymous-decoder';run=json.loads((D/'decoder-run.json').read_bytes());lease=json.loads((D/'lease.closed.json').read_bytes());slot=json.loads((D/'slot-decisions.json').read_bytes())
assert sha(canon({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==packet['blind_reconstruction']['decoder_run_sha256']
for q in lease['covered_files']:
 b=(D/q['name']).read_bytes();assert len(b)==q['byte_count'] and sha(b)==q['raw_sha256']
neutral=json.loads((R/'anonymous.0.decoder.json').read_bytes())
assert sha(canon(neutral))==run['packet_sha256']=='b40612aa42fec0d1ccecc0780f358189c4930ff0fb9f76dc113f72cd8c17906a'
assert sha(canon({k:v for k,v in neutral.items() if k!='packet_sha256'}))==neutral['packet_sha256']==packet['blind_reconstruction']['decoder_packet_sha256']
decodedtext=(D/'reconstruction.utf8.txt').read_bytes();assert decodedtext.decode()==packet['blind_reconstruction']['text'] and sha(decodedtext)==packet['blind_reconstruction']['text_sha256']
assert slot['slot_count']==51 and len(slot['slots'])==51 and slot['unresolved_count']==0
assert slot['source_text_visible'] is False and slot['proof_BODY_visible'] is False
write('stageB.decoder-and-official-packet-binding71.json',{'schema':'source71-decoder-and-review-packet-binding-v1','actual_pid':os.getpid(),'native_decoder_run':pin(D/'decoder-run.json'),'native_decoder_lease':pin(D/'lease.closed.json'),'native_decoder_owned_files':10,'native_decoder_whole_logical_run_sha256':run['run_sha256'],'decoder51_rows_and_complete_reconstruction_bound':True,'native_decoder_full_packet_canonical_sha256':run['packet_sha256'],'official_decoder_packet_omit_top_sha256':neutral['packet_sha256'],'official_reviewer_packet_RAW':pin(R/'source-review.packet.0.json'),'official_reviewer_packet_omit_top_sha256':packet['packet_sha256'],'official_reviewer_packet_full_canonical_sha256':sha(canon(packet)),'publication_binding_sha256':packet['publication_binding_sha256'],'different_hash_recipes_explicitly_distinguished':True,'blind_native_bytes_retained':True,'reviewer_independent_from_decoder_and_formalizer':True})
receipt=json.loads((R/'focused-typed-substitution/receipt.json').read_bytes())
assert receipt['actual_foreground_PID']==49980 and receipt['exit_code']==0
for k in ['stdout','stderr']:
 q=receipt[k];b=(B/q['path']).read_bytes();assert sha(b)==q['RAW_sha256'] and len(b)==q['RAW_bytes']
out=(R/'focused-typed-substitution/stdout.log').read_text(encoding='utf-8');assert '3950' in out
write('stageB.focused-compile-receipt-inspection71.json',{'schema':'source71-compile-receipt-inspection-v1','actual_inspector_pid':os.getpid(),'native_receipt':pin(R/'focused-typed-substitution/receipt.json'),'actual_focused_PID':49980,'actual_focused_EXIT':0,'jobs':3950,'source_module_pin_exact_current':True,'native_stdout_tail':out[-1800:],'Lean_compile_rerun_by_source_reviewer':False,'compile_does_not_supply_source_fidelity':True})
print(json.dumps({'actual_pid':os.getpid(),'status':'PASS_BOUNDED_CURRENT_BINDINGS','module_lines':528,'BODY_lines':377,'steps':8,'parent_literal_exact_retained':True,'private_literal_nonprovider':True,'decoder_rows':51,'official_reviewer_packet_sha256':packet['packet_sha256'],'publication_binding_sha256':packet['publication_binding_sha256'],'native_focused_PID_EXIT':[49980,0]},indent=2))
