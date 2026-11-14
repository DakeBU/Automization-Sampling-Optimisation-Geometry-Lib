from pathlib import Path
import json,hashlib,difflib,copy,sys
from datetime import datetime,timezone
sys.dont_write_bytecode=True
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/metadata-schema-correction';CELL='research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json';ORIG=B/'inputs/C23.original.exact.json'
def h(a):return hashlib.sha256(a).hexdigest()
def wr(n,d):
 with (B/n).open('x') as f:f.write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
raw=ORIG.read_bytes();assert (R/CELL).read_bytes()==raw;c=json.loads(raw);assert (json.dumps(c,indent=2,ensure_ascii=False)+'\n').encode()==raw
old=copy.deepcopy(c['evidence']['independent_verification']);assert isinstance(old,dict) and 'independent_verification_details' not in c['evidence']
D='research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/normal-verification/mv_src_6e28/originals/normal-verification-v2/'
refs=[('original full V payload','VERIFIED-evidence.full.json','e1f9b9ab79aa965c4234756f6016bab0584402a7f98731cbc667cb9b32ff435a'),('original independent decision','independent-decision.json','012e5318bc9ff0828f9b5d9c7e8f2534983adbb4e297cbebfb75c47054d8016f'),('original exact VERIFIED append','actual-VERIFIED-append.exact.jsonl','24cc7ea161d32a42a78e3b2e4d10a091faffe604bb1d1c419ee4b943d6d1ab78'),('original normal API receipt','normal-API-receipt.json','ce5184dd8489f10a9ba46ccbbee9f50d88262ab16c08dc0f9dd68e07f3f71065')]
for label,name,sha in refs:assert h((R/(D+name)).read_bytes())==sha
reference='S original normal independent verification by /root/mv_fresh_source_6e28; actual mathematical commit9964c33c4599f85d27dc8687e8bd6fdb5c44ff49; original verification metadata HEAD5f69ac83737e497210d8d8ad9628c45d83089458. '+'; '.join(label+': '+D+name+' SHA256 '+sha for label,name,sha in refs)+'. Original normal API calls1/failures0, historical S V0->1. Complete original dict preserved unmodified in evidence.independent_verification_details. This is only a schema serialization correction, with no V replay or mathematical/source/status/owner change.'
proposed=copy.deepcopy(c);ev={}
for key,val in c['evidence'].items():
 if key=='independent_verification':ev[key]=reference;ev['independent_verification_details']=copy.deepcopy(old)
 else:ev[key]=copy.deepcopy(val)
proposed['evidence']=ev;new=(json.dumps(proposed,indent=2,ensure_ascii=False)+'\n').encode();(B/'C23.proposed.exact.json').write_bytes(new)
# Every other object value and the original serialized value body must remain exact.
restored=copy.deepcopy(proposed);restored['evidence']['independent_verification']=copy.deepcopy(restored['evidence'].pop('independent_verification_details'));assert (json.dumps(restored,indent=2,ensure_ascii=False)+'\n').encode()==raw
assert proposed['evidence']['independent_verification_details']==old
for key in ['status','owner_id','advance_id','target_statement','source_anchor','statement_seal','truth_boundary']:assert proposed[key]==c[key]
def value_bytes(text,key):
 s=text.index(json.dumps(key)+': ')+len(json.dumps(key)+': ');_,n=json.JSONDecoder().raw_decode(text[s:]);return text[s:s+n].encode()
assert value_bytes(raw.decode(),'independent_verification')==value_bytes(new.decode(),'independent_verification_details')
wr('independent-verification-dict.original.json',old)
(B/'C23.proposed.unified.diff').write_text(''.join(difflib.unified_diff(raw.decode().splitlines(True),new.decode().splitlines(True),fromfile=CELL+' (original exact)',tofile=CELL+' (PROPOSED ONLY; NOT APPLIED)')))
wr('proposed-json-pointer-diff.json',{'changes':[{'pointer':'/evidence/independent_verification','operation':'replace','before_type':'dict','after_type':'nonempty string','after':reference},{'pointer':'/evidence/independent_verification_details','operation':'add','value':'Exact original independent_verification dict, including all original .astis references retained as historical detail.'}],'all_other_values_byte_restorable_to_original':True,'original_dict_raw_JSON_value_byte_equal_after_move':True,'original_sha256':h(raw),'proposed_sha256':h(new)})
# Actual schema validation of ONLY original/proposed own S; never load dirty R9 cells.
sys.path.insert(0,str(R/'tools'));import astis_frontier_cells as frontier
before=copy.deepcopy(c);after=copy.deepcopy(proposed);before['__path__']=CELL;after['__path__']=CELL
errors_before=frontier.validate_cells([before]);errors_after=frontier.validate_cells([after]);expected=CELL+': status independently_verified requires independent_verification';assert errors_before==[expected],errors_before;assert errors_after==[],errors_after
assert frontier._nonempty(old) is False and frontier._nonempty(reference) is True
wr('isolated-schema-validation.json',{'actual_schema_function':'tools.astis_frontier_cells.validate_cells','scope':'Exactly one own S object at a time; load_cells not called, no R9/C22/AP or whole-repository validation','original_errors':errors_before,'proposed_errors':errors_after,'original_dict_nonempty_predicate':False,'proposed_string_nonempty_predicate':True,'process_memory_read_by_validator':'Existing IDs only inside read-only validate_cells; no process memory or other cell mutated/exported','normal_API_calls':0,'shared_cell_changed':(R/CELL).read_bytes()!=raw})
assert (R/CELL).read_bytes()==raw
wr('independent-correction-decision.json',{'recorded_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'/root/mv_fresh_source_6e28','decision':'SUPPORT_PROPOSED_METADATA_SCHEMA_SERIALIZATION_CORRECTION_ONLY_NOT_APPLIED','cause':'My original normal S verifier serialized a rich dict into the legacy schema nonempty-string field. validate_cells uses _nonempty string-only. This is a verifier-owned metadata shape error, not a new proof failure or a ROOT/R9 introduction.','exact_allowed_delta':['Replace evidence.independent_verification with portable-original evidence reference string and exact hashes','Preserve original entire dict, raw JSON value body byte-identical, under evidence.independent_verification_details'],'original_C23_sha256':h(raw),'proposed_C23_sha256':h(new),'original_V_payload_sha256':refs[0][2],'original_decision_sha256':refs[1][2],'original_V_append_sha256':refs[2][2],'original_API_receipt_sha256':refs[3][2],'original_API_history_unchanged':'Original once call1/fail0 and V0->1 remain the frozen record; correction APIcalls0. No replay, append, transition or new verification credit.','portable_original_references_exist_and_hash_checked':True,'proposal_schema_passes_isolated_actual_validate_cells':True,'status_owner_advance_math_source_target_unchanged':True,'shared_C23_ledger_git_modified':False,'normal_API_replay_authorized_or_attempted':False,'other_dirty_R9_files':'Not inspected or modified; outside this proposal.','apply_authorization':'No shared apply is performed in this phase. Any later carrier must apply only this independently authored exact proposed byte payload under separate instruction; never rerun V.','prior_verification_freezes_rewritten':False})
print(json.dumps({'original_C23_sha256':h(raw),'proposed_C23_sha256':h(new),'proposed_bytes':len(new),'isolated_original_schema_errors':errors_before,'isolated_proposed_schema_errors':errors_after,'shared_C23_still_original':True},indent=2))
