from pathlib import Path
import os,sys,json,hashlib,base64
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');OWN=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(name):return json.loads((OWN/name).read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
def dump(name,x):
 p=OWN/name;p.write_bytes((json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());return pin(p)
def complete(name):
 p=OWN/name;return {'pin':pin(p),'complete_RAW_base64':base64.b64encode(p.read_bytes()).decode('ascii')}
def main():
 assert not (OWN/'lease.final.json').exists(),'Never reopen CLOSED'
 from check75 import main as verify
 verify()
 im=load('inputs.manifest75.json');ex=load('source-first.expectations75.json');dec=load('decision75.json')
 core=['source-first.expectations75.json','source-proof-graph75.json','source-coverage-inventory75.json','source-RAW-partition75.json','exact-source-formulas75.json','API-bounded-review75.json','source-literal-vs-inherited-bridges75.json','internal-completion-analysis75.md','future-header-semantic-standards75.json','bounded-synthesis75.md','source-provenance-verification75.json','observer-negatives75.json']
 freeze={'schema':'pbps75-source-before-header-freeze/v1','actor':'/root/independent_primary69','actual_PID':os.getpid(),'actual_EXIT':0,'status':'SOURCE_FIRST_BASELINE_ONLY','no75_header_hash_statement_BODY_proof_read':True,'source_primary':im['inputs'][0],'CLOSED86_reference':next(x for x in im['inputs']if x['path'].endswith('/lease.final.json')),'counts':dec['counts'],'inputs_manifest':pin(OWN/'inputs.manifest75.json'),'core_artifacts':[pin(OWN/x)for x in core],'no_new_SAU_Lean_VERIFIED_source_header_acceptance':True,'before_candidate_order':'Fixed RAW+CLOSED86 read -> independent source inventory/graph/criteria authored -> this freeze. Future75 candidates excluded.'}
 freeze_sha=sha(canon(freeze));freeze['freeze_sha256']=freeze_sha
 freezepin=dump('stageA.freeze75.json',freeze)
 review={'schema':'pbps75-complete-independent-source-review-record/v1','scope':'Source-first baseline and future header standards only; no candidate/source-fidelity verdict','actor':'/root/independent_primary69','whole_named_core_RAW':[complete(x)for x in core],'freeze':freezepin,'no_other_agent_math_or_future75_verdict_used':True,'exposure':ex['exposure']}
 reviewpin=dump('review75.json',review)
 selected=[]
 for e in im['inputs']:
  if 'snapshot' in e:
   q=ROOT/e['snapshot']['path'];selected.append({'original_input':{k:v for k,v in e.items()if k!='snapshot'},'snapshot':e['snapshot'],'complete_RAW_base64':base64.b64encode(q.read_bytes()).decode('ascii')})
 supplements=[]
 for r in im['source_regions']:
  if r['origin'].startswith('Independent'):
   q=ROOT/r['RAW']['path'];supplements.append({'origin':r,'complete_RAW_base64':base64.b64encode(q.read_bytes()).decode('ascii')})
 inputpayload={'schema':'pbps75-complete-selected-input-RAW-payload/v1','complete_selected_RAW_inputs':selected,'complete_supplemental_primary_RAW_slices':supplements,'immutable_reference_only':[x for x in im['inputs']if 'snapshot'not in x],'reference_policy':'Full fixed1.48MB primary and oldCLOSED86 tree are exact finite reference pins; not recursively duplicated or represented as new objects. Complete RAW bytes for selected regions/API/planning/provenance JSONs and minimal supplements are included.','LF_recipe':im['LF_recipe']}
 ippin=dump('inputs.payload75.json',inputpayload)
 closereceipt={'schema':'pbps75-terminal-receipt/v1','actual_PID':os.getpid(),'actual_EXIT':0,'phase':'final finite verification and source-baseline native closure','build_actual_PID':40640,'build_actual_EXIT':0,'source_probe_actual_PID':47688,'source_probe_actual_EXIT':0,'corrected_RAW_probe_actual_PID':26964,'corrected_RAW_probe_actual_EXIT':0,'OPEN_external_readonly_actual_PID':50684,'OPEN_external_readonly_actual_EXIT':0,'negative_observer_actual_PID':48580,'negative_observer_actual_EXIT':1,'no_background_or_compile':True,'no_canonical_Git_ledger_Goal_or_oldCLOSED_writes':True,'next_and_last_owned_write_contract':'The final lease is written after whole-owned manifest. Subsequent checker invocation is read-only and stdout only.'}
 receiptpin=dump('terminal.close75.json',closereceipt)
 run={'schema':'pbps75-independent-source-baseline-run/v1','actor':'/root/independent_primary69','status':'SOURCE_FIRST_BASELINE_CLOSED_NO75_HEADER_ACCEPTANCE','source_review_kind':'prospective source-only baseline, distinct from proof/SAU/semantic roundtrip','counts':dec['counts'],'finite_input_count':im['input_count'],'input_manifest':pin(OWN/'inputs.manifest75.json'),'complete_selected_input_payload':ippin,'decision':pin(OWN/'decision75.json'),'complete_review':reviewpin,'source_before_candidate_freeze':freezepin,'freeze_logical_sha256':freeze_sha,'named_core_pins':[pin(OWN/x)for x in core],'actual_terminal_close':receiptpin,'remaining_truth_boundary':dec['remaining_truth_boundary'],'exposure':ex['exposure'],'RAW_LF_recipe':im['LF_recipe'],'wholelogical_recipe':'UTF8 JSON ensure_ascii=False sort_keys=True separators comma/colon allow_nan=False; delete ONLY top-level run_sha256. No other field omitted.','no_header_implementation_Lean_compile_SAU_VERIFIED_reader_PURIFIED_main_cost_wholeGoal_credit':True}
 runsha=sha(canon(run));run['run_sha256']=runsha;runpin=dump('run75.json',run)
 named={'schema':'pbps75-five-complete-named-RAW-payloads/v1','whole_logical_run_sha256':runsha,'named_payload_count':5,'named_payloads':[{'name':name,**complete(file)}for name,file in [('review','review75.json'),('decision','decision75.json'),('run','run75.json'),('input-manifest','inputs.manifest75.json'),('selected-input','inputs.payload75.json')]],'no_recursive_history_or_prior_native_payload':True}
 namedpin=dump('complete-named-RAW-payload75.json',named)
 members=sorted((x for x in OWN.rglob('*')if x.is_file() and x.name not in ('whole-owned.manifest75.json','lease.final.json')),key=lambda x:x.relative_to(ROOT).as_posix())
 manifest={'schema':'pbps75-whole-owned-manifest/v1','finite_closure':True,'owned_scope':OWN.relative_to(ROOT).as_posix(),'excluded_only':['whole-owned.manifest75.json (self)','lease.final.json (last writer/self-referential closure)'],'member_count':len(members),'files':[pin(p)for p in members],'whole_logical_run_sha256':runsha,'includes_all_helpers_inputs_supplements_negatives_terminal_payloads':True}
 manifestpin=dump('whole-owned.manifest75.json',manifest)
 all_except_lease=sorted((x for x in OWN.rglob('*')if x.is_file()),key=lambda x:x.relative_to(ROOT).as_posix())
 lease={'schema':'pbps75-source-baseline-lease/v1','actor':'/root/independent_primary69','status':'CLOSED_LAST','actual_last_writer_PID':os.getpid(),'actual_last_writer_EXIT':0,'owned_count':len(all_except_lease)+1,'all_owned_outputs_except_only_self':[pin(p)for p in all_except_lease],'whole_owned_manifest':manifestpin,'complete_named_RAW_payload':namedpin,'whole_logical_run_sha256':runsha,'source_before_candidate_freeze':freezepin,'finite_input_count':im['input_count'],'all_sessions_closed':True,'final_owned_write':True,'postclose_owned_writes':False,'source_only_baseline':True,'candidate75_header_seen':False,'Lean_compile':False,'SAU_claim':False,'VERIFIED':False,'reader_PURIFIED_main_cost_wholeGoal_credit':False,'canonical_Git_ledger_Goal_writes':False}
 leasepin=dump('lease.final.json',lease)
 print(json.dumps({'actual_PID':os.getpid(),'actual_EXIT':0,'status':'CLOSED_LAST','owned_count':lease['owned_count'],'all_except_only_self':len(all_except_lease),'manifest_members':len(members),'run':runpin,'whole_logical_run_sha256':runsha,'freeze':freezepin,'freeze_logical_sha256':freeze_sha,'decision':pin(OWN/'decision75.json'),'named_RAW_payload':namedpin,'manifest':manifestpin,'lease':leasepin},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
