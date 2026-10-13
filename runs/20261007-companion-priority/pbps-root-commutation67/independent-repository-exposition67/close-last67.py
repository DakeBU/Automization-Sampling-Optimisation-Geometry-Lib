from pathlib import Path
import os,json,hashlib,datetime
O=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def ld(n):return json.loads((O/n).read_bytes())
def wr(n,j):(O/n).write_bytes((json.dumps(j,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'name':p.relative_to(O).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(l),'LF_sha256':sha(l)}
assert not (O/'lease.final.json').exists()
receipts={n:ld(n) for n in ['foreground-finalizer.receipt.json','foreground-readback.receipt.json','foreground-close-validator.receipt.json']}
for j in receipts.values():
 assert j['actual_exit']==0 and j['terminal_closed']
 for k in ['stdout','stderr']:assert sha((O/j[k]['name']).read_bytes())==j[k]['RAW_sha256']
b=ld('raw-payload-bindings.json');pid=os.getpid()
wr('close-last.prelease-result.json',{'schema':'repository67-prelease-actual-last-writer-record-v1','actual_lease_writer_PID':pid,'all_prior_foreground_exits_observed':0,'remaining_last_write':'lease.final.json','actual_lease_writer_exit':'External foreground exec observation required; never inferred here.'})
files=[p for p in sorted(O.rglob('*')) if p.is_file()]
manifest={'schema':'repository67-exhaustive-owned-RAW-LF-manifest-v1','owned_path':O.as_posix(),'owner':'/root/independent_source64','regular_file_entries':[pin(p) for p in files],'regular_file_count_excluding_self_and_final_lease':len(files),'total_owned_files_including_manifest_and_final_lease':len(files)+2,'self_boundary':'Exact manifest bytes are bound in final lease; lease self RAW returned externally. No other exception.','all_owned_negatives_scripts_inputs_self_payloads_and_actual_terminal_files_bound':True};wr('owned-manifest.json',manifest)
lease={'schema':'repository67-CLOSED_LAST-owned-lease-v1','status':'CLOSED_LAST','owner':'/root/independent_source64','owned_path':O.as_posix(),'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_SCI_commit':'3da29415011a971a65f749502a625e416213f487','SCI_parent_INT66':'eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176','whole_logical_run_sha256':b['whole_logical_run_sha256'],'COMPLETE_RAW_REVIEW':b['COMPLETE_RAW_REVIEW'],'COMPLETE_RAW_DECISION':b['COMPLETE_RAW_DECISION'],'SEPARATE_COMPLETE_RAW_INPUT':b['SEPARATE_COMPLETE_RAW_INPUT'],'owned_manifest':pin(O/'owned-manifest.json'),'all_owned_except_this_final_lease':[pin(p) for p in sorted(O.rglob('*')) if p.is_file()],'owned_file_count':len(files)+2,'actual_finalizer_PID':receipts['foreground-finalizer.receipt.json']['actual_foreground_PID'],'actual_finalizer_exit':0,'actual_readback_PID':receipts['foreground-readback.receipt.json']['actual_foreground_PID'],'actual_readback_exit':0,'actual_close_validator_PID':receipts['foreground-close-validator.receipt.json']['actual_foreground_PID'],'actual_close_validator_exit':0,'actual_lease_writer_PID':pid,'lease_writer_actual_exit':'External exec/capsule observation; never self-asserted.','last_owned_write':True,'postclose_writes_permitted':False,'postclose':'postclose-readonly67.py console only; actual PID/EXIT returned externally.','native_admission':'ACCEPT_SCOPED_CURRENT_FINAL_ADMIN','current_graph_freshness_admission':True,'historical_INT66_current_freshness_withheld_unchanged':True,'source_mathematical_repair':False,'full_Exposition':False,'PURIFIED':False,'main_live':False,'whole_Goal_complete':False,'canonical_Git_ledger_Lean_Registry_site_writes':False}
wr('lease.final.json',lease)
print(json.dumps({'actual_lease_writer_PID':pid,'lease_RAW_sha256':sha((O/'lease.final.json').read_bytes()),'manifest_RAW_sha256':sha((O/'owned-manifest.json').read_bytes()),'owned_file_count':lease['owned_file_count'],'whole_logical_run_sha256':lease['whole_logical_run_sha256'],'status':'CLOSED_LAST'}))
