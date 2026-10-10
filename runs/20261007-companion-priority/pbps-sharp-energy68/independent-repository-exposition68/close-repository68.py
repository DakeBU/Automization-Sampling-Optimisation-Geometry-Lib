from pathlib import Path
import json,hashlib,os,sys,datetime
sys.dont_write_bytecode=True
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-sharp-energy68/independent-repository-exposition68'
sha=lambda b:hashlib.sha256(b).hexdigest()
lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
canon=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(n):return json.loads((O/n).read_bytes())
def write(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(n):
 b=(O/n).read_bytes();return {'path':n,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf(b)),'LF_sha256':sha(lf(b))}
assert not (O/'lease.final.json').exists() and not (O/'owned-manifest.json').exists()
rb=read('final-native-readback.json');t=read('final-native-readback.terminal.json');assert rb['status']=='PASS' and t['actual_exit_code']==0 and t['actual_child_pid']==rb['actual_readback_pid'] and t['foreground'] and not t['detached']
for s in ['stdout','stderr']:assert sha((O/('final-native-readback.'+s+'.RAW.txt')).read_bytes())==t[s+'_raw_sha256']
r=read('review-run.json');r0=dict(r);h=r0.pop('run_sha256');assert h==sha(canon(r0))==rb['whole_logical_run_sha256'];a=read('complete-RAW-decision.json');assert a['review_run_sha256']==h
rows=[pin(p.relative_to(O).as_posix()) for p in sorted(O.rglob('*')) if p.is_file()]
assert all(e['path'] not in {'owned-manifest.json','lease.final.json'} for e in rows)
manifest={'schema':'bounded-repository-exposition68-finite-owned-manifest-v1','rows':rows,'entry_count':len(rows),'rows_canonical_sha256':sha(canon(rows)),'exclusions_exact':['owned-manifest.json','lease.final.json'],'manifest_bound_by_final_lease':True,'final_lease_self_hash_returned_in_authoritative_foreground_output':True,'LF_rule':'Replace CRLF with LF, then remaining CR with LF; byte projection also retained for binary snapshots.'}
write('owned-manifest.json',manifest)
for e in rows:assert pin(e['path'])==e
assert len([p for p in O.rglob('*') if p.is_file()])==len(rows)+1
lease={'schema':'independent-repository-exposition68-native-CLOSED_LAST-v1','status':'CLOSED_LAST','actor':'/root/independent_header_source68','owned_path':O.relative_to(R).as_posix(),'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_closing_pid':os.getpid(),'closing_terminal_authority':'Foreground tools.exec_command authoritative EXIT follows this final owned write; no invented pre-exit status. Post-close validator only reads.','whole_logical_run_sha256':h,'logical_rule':'Canonical sorted compact UTF8 whole review-run.json after deleting ONLY top-level run_sha256.','complete_named_RAW_review':pin('complete-RAW-review.json'),'whole_logical_run_file':pin('review-run.json'),'complete_named_RAW_decision':pin('complete-RAW-decision.json'),'complete_named_RAW_input_payload':pin('complete-RAW-input.json'),'owned_manifest':pin('owned-manifest.json'),'owned_rows_canonical_sha256':manifest['rows_canonical_sha256'],'total_owned_file_count_including_manifest_and_final_lease':len(rows)+2,'finite_input_count':176,'final_readback':pin('final-native-readback.json'),'actual_terminal_receipts':dict(rb['actual_terminal_receipts'],final_native_readback=t),'all18_reused_root_foreground_receipts':pin('reused-root-checks.terminal-map.json'),'checked_commit':a['checked_commit'],'acceptance':a['acceptance'],'decision_verdict':a['verdict'],'current_graph_RAW_sha256':a['current_graph_RAW_sha256'],'publication_inputs_sha256':a['publication_inputs_sha256'],'exact_final_cell_RAW':a['final_cell_RAW'],'native_source363_schema24_alias80_remain_CLOSED_unchanged':True,'corrected_verification74_reused_old131_negative_retained':True,'canonical_Git_ledger_or_Goal_writes':False,'compiler_started':False,'future69_candidate_read':False,'full_Exposition_Seal':False,'PURIFIED':False,'remoteCI_main_live':False,'wholeSAU_wholepaper_Goal_complete':False,'last_owned_write':'lease.final.json','postclose_policy':'Read-only. Do not reopen this owned scope.'}
write('lease.final.json',lease)
print('CLOSED_LAST',os.getpid(),'COUNT',len(rows)+2,'MANIFEST_ROWS',len(rows),'LOGICAL_RUN',h)
for n in ['complete-RAW-review.json','complete-RAW-decision.json','complete-RAW-input.json','owned-manifest.json','lease.final.json']:print(n,sha((O/n).read_bytes()))
