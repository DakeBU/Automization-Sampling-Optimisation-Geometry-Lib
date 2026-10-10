from pathlib import Path
import json,hashlib,os,sys,datetime,subprocess
sys.dont_write_bytecode=True
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-sharp-energy68';O=B/'independent-repository-exposition68'
sha=lambda b:hashlib.sha256(b).hexdigest()
lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
canon=lambda a:json.dumps(a,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(n):return json.loads((O/n).read_bytes())
def write(n,a):(O/n).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
assert not (O/'lease.final.json').exists()
r=read('review-run.json');a=read('complete-RAW-decision.json');r0=dict(r);declared=r0.pop('run_sha256');assert sha(canon(r0))==declared=='039bb9c7f2c85e22263bf45ffaea3462faea42fed462a45299952ab119d8556c'
assert (O/'complete-RAW-review.json').read_bytes()==(O/'review-run.json').read_bytes()
a0=dict(a);assert a0.pop('review_run_sha256')==declared;assert a0==r['decision_without_external_run_reference']
expected={'repository_scoped_integration':True,'scoped_local_reader_with_explicit_debts':True,'current_graph_freshness_and_coverage':True,'source_mathematics_reused_exactly':True,'full_Exposition_Seal':False,'PURIFIED':False,'remoteCI_main_live':False,'wholeSAU_or_wholepaper_or_Goal_complete':False}
assert a['acceptance']==expected and a['blocking_findings']==[]
fixed={'complete-RAW-review.json':'a19b2fcce045cea24ad199ea6fc8a6c7b7cad5b4298284502420f04fc1c2cd3a','complete-RAW-decision.json':'59e432e5037f2250a3ede5c9590d7d26d9382c475ec3620b4c11097e4e30114e','complete-RAW-input.json':'38ed113855b2eb1bd2ac2ef04d0c71b1008b43064c3a223b3ea4c2cb3ac9aa81'}
for n,h in fixed.items():assert sha((O/n).read_bytes())==h
inp=read('complete-RAW-input.json');assert inp['entry_count']==len(inp['entries'])==176
for e in inp['entries']:
 b=(O/e['raw_snapshot']).read_bytes();l=(O/e['lf_snapshot']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'];assert l==lf(b) and len(l)==e['LF_bytes'] and sha(l)==e['LF_sha256'];assert (R/e['source_path']).read_bytes()==b
assert sha((R/'_site/data/underlying-lean-graph.json').read_bytes())==a['current_graph_RAW_sha256']
for e in a['final_cell_RAW']:
 b=(R/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['raw_sha256'] and sha(lf(b))==e['lf_sha256']
head=subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,check=True).stdout.decode().strip();assert head==a['checked_commit']=='3ad3b127b5a645be9cf71b3d14520b2d8fea3122'
receipts={}
for stem,pid in [('repository-graph-stage1',42052),('repository-reader-stage2',31924)]:
 t=read(stem+'.terminal.json');assert t['foreground'] and not t['detached'] and t['actual_child_pid']==pid and t['actual_exit_code']==0
 for s in ['stdout','stderr']:assert sha((O/(stem+'.'+s+'.RAW.txt')).read_bytes())==t[s+'_raw_sha256']
 receipts[stem]=t
for v,pid in [('v1',19944),('v2',44120)]:
 suffix='.'+v+'.exactraw.snapshot';t=read('repository-graph-stage1.terminal.json'+suffix);assert t['actual_child_pid']==pid and t['actual_exit_code']==1
 for s in ['stdout','stderr']:assert sha((O/('repository-graph-stage1.'+s+'.RAW.txt'+suffix)).read_bytes())==t[s+'_raw_sha256']
 receipts['negative-stage1-'+v]=t
root=read('reused-root-checks.terminal-map.json');assert len(root['entries'])==18 and all(e['exit_code']==0 and e['terminal_closed'] for e in root['entries'])
reuse=read('native-closures-reuse.json')
for e in reuse['closed']:
 p=B/e['folder'];assert sha((p/'lease.final.json').read_bytes())==e['lease_RAW_sha256'];native=json.loads((p/'lease.final.json').read_bytes());assert native['status']=='CLOSED_LAST' and native['whole_logical_run_sha256']==e['whole_logical_run_sha256'];assert sum(q.is_file() for q in p.rglob('*'))==e['count']
corrected=json.loads((B/'exact-science-verification68-corrected/lease.final.json').read_bytes());old=json.loads((B/'exact-science-verification/lease.final.json').read_bytes());assert corrected['status']=='CLOSED_LAST' and corrected['VERIFIED'] is True and old['status']=='CLOSED_LAST' and old['VERIFIED'] is False
assert sha((B/'exact-science-verification68-corrected/lease.final.json').read_bytes())==reuse['corrected_verification_CLOSED74']['native_lease_RAW_sha256']
assert sum(q.is_file() for q in (B/'exact-science-verification68-corrected').rglob('*'))==74 and sum(q.is_file() for q in (B/'exact-science-verification').rglob('*'))==131
for n in a['negative_receipts']:assert (O/n).is_file()
report={'schema':'bounded-repository-exposition68-final-native-readback-v1','status':'PASS','actual_readback_pid':os.getpid(),'HEAD':head,'whole_logical_run_sha256':declared,'logical_rule':'Canonical whole run after deleting ONLY top-level run_sha256','named_complete_RAW_sha256':fixed,'finite_input_rows_checked_RAW_LF_and_current':176,'all_inputs_still_exact_current':True,'current_graph_RAW_sha256':a['current_graph_RAW_sha256'],'publication_input_digest_already_independently_recomputed':a['publication_inputs_sha256'],'exact_final_cells':a['final_cell_RAW'],'original_native_closures_363_24_80_unchanged':True,'corrected_CLOSED74_verified_and_old_CLOSED131_negative_unchanged':True,'actual_terminal_receipts':receipts,'root_reused_foreground_EXIT0_count':18,'acceptance':expected,'canonical_writes':False,'compiler_started':False,'future69_candidate_read':False,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
write('final-native-readback.json',report)
print('FINAL_NATIVE_READBACK_EXIT0',os.getpid(),176,declared,'ALL_CURRENT_INPUTS_EXACT','NEGATIVES_RETAINED')
