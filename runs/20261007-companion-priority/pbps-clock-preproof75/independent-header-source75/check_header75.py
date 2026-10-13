from pathlib import Path
import json,hashlib,base64,os,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');OWN=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def checkpin(e):
 b=(ROOT/e['path']).read_bytes();assert len(b)==e['RAW_bytes'] and sha(b)==e['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==e['LF_sha256'],e['path'];return b
def main():
 im=load(OWN/'inputs.manifest75.json');mapping=load(OWN/'exact-API-overlay75.finite-map.json');exp=load(OWN/'complete-header-expansion75.json');cov=load(OWN/'header-source-coverage75.json');dec=load(OWN/'decision75.json');review=load(OWN/'review75.json')
 for q in im['current_inputs']+im['reused_StageA_inputs']:
  b=checkpin(q)
  if'snapshot'in q:assert b==checkpin(q['snapshot'])
 assert im['current_input_count']==26 and im['reused_StageA_input_count']==22
 api=load(OWN/'exact-API-context75.json')
 for q in api['regions']:
  parent=checkpin(q['whole_source']);fragment=checkpin(q['fragment']);a,b=q['RAW_line_range'];assert b''.join(parent.splitlines(keepends=True)[a-1:b])==fragment
 before=checkpin(mapping['before']);after=checkpin(mapping['proposed']);old=mapping['old_literal_UTF8'].encode();new=mapping['new_literal_UTF8'].encode()
 assert before.count(old)==1 and before.replace(old,new)==after and len(after)-len(before)==11
 a,b=mapping['old_RAW_range'];c,d=mapping['new_RAW_range'];assert before[:a]==after[:c] and before[b:]==after[d:]
 assert sha(before[:a])==mapping['prefix_RAW_sha256']and sha(before[b:])==mapping['suffix_RAW_sha256']
 for q in [exp['private_literal'],exp['public_header']]+exp['eight_let_definitions']+exp['ten_top_conjunctions']:
  a,b=q['RAW_range'];assert sha(after[a:b])==q['RAW_sha256']
 cursor=0
 for q in exp['all_header_lines']:
  a,b=q['RAW_range'];assert a==cursor and b>a and sha(after[a:b])==q['RAW_sha256'];cursor=b
 assert cursor==len(after)and len(exp['all_header_lines'])==83 and len(exp['ten_top_conjunctions'])==10 and len(exp['eight_let_definitions'])==8
 b=exp['binders'];a1,a2=b['private_RAW_range'];c1,c2=b['public_RAW_range'];assert after[a1:a2]==after[c1:c2]and sha(after[a1:a2])==b['RAW_sha256']
 assert len(b['six_callers'])==6 and len(b['five_typing_classes'])==5
 baseline=load(ROOT/cov['baseline_inventory']['path']);graph=load(ROOT/cov['baseline_source_graph']['path']);checkpin(cov['baseline_inventory']);checkpin(cov['baseline_source_graph'])
 assert len(cov['source_items'])==137 and len(cov['source_nodes'])==32 and len(cov['source_edges'])==67 and len(cov['future_obligations'])==32
 for a,b in zip(cov['source_items'],baseline['items']):
  assert a['item_id']==b['item_id']and a['source_RAW_sha256']==b['RAW_sha256']and a['StageA_classification']==b['classification']and a['StageA_reason_retained']==b['reason']
 assert [q['source_node']for q in cov['source_nodes']]==[q['id']for q in graph['nodes']]
 assert [q['source_edge']for q in cov['source_edges']]==[q['id']for q in graph['edges']]
 assert len(dec['semantic_slots'])==7 and dec['semantic_slots']==review['semantic_slots'] and dec['blocking_count']==0 and dec['required_repairs']==[]
 assert all(set(q)=={'slot','severity','description','evidence'}and q['severity']=='informational'for q in dec['deltas'])
 overlay=load(OWN/'exact-API-overlay75.decision.json');assert overlay['decision']=='ACCEPT_EXACT_PROPOSAL_ONLY'
 status={'status':'OPEN_READ_ONLY_HEADER_SOURCE_CHECK_PASS'}
 if(OWN/'lease.final.json').exists():
  lease=load(OWN/'lease.final.json');assert lease['status']=='CLOSED_LAST'
  allfiles=[p for p in OWN.rglob('*')if p.is_file()];assert len(allfiles)==lease['owned_count']
  assert {p.relative_to(ROOT).as_posix()for p in allfiles}=={q['path']for q in lease['all_owned_outputs_except_only_self']}|{(OWN/'lease.final.json').relative_to(ROOT).as_posix()}
  for q in lease['all_owned_outputs_except_only_self']:checkpin(q)
  manifest=load(OWN/'whole-owned.manifest75.json');checkpin(lease['whole_owned_manifest']);assert len(manifest['files'])==manifest['member_count']
  for q in manifest['files']:checkpin(q)
  run=load(OWN/'run75.json');claimed=run.pop('run_sha256');assert sha(canon(run))==claimed==lease['whole_logical_run_sha256']
  adm=load(OWN/'admission-fields75.json');template=run['exact_admission_template'];actual=json.loads(json.dumps(adm));del actual['source_header_admission']['review_run_sha256'];assert actual==template and adm['source_header_admission']['review_run_sha256']==claimed
  payload=load(OWN/'complete-five-named-RAW-payload75.json');checkpin(lease['complete_named_RAW_payload']);assert len(payload['named_payloads'])==5
  for q in payload['named_payloads']:assert base64.b64decode(q['complete_RAW_base64'],validate=True)==checkpin(q['pin'])
  assert all(p.stat().st_mtime_ns<=(OWN/'lease.final.json').stat().st_mtime_ns for p in allfiles)
  status={'status':'POSTCLOSE_READ_ONLY_PASS','owned_count':len(allfiles),'lease_members':len(lease['all_owned_outputs_except_only_self']),'manifest_members':len(manifest['files']),'whole_logical_run_sha256':claimed,'lease_RAW_sha256':sha((OWN/'lease.final.json').read_bytes()),'postclose_owned_writes':0}
 print(json.dumps({'actual_PID':os.getpid(),'actual_EXIT':0,**status,'current_input_entries':26,'distinct_current_files':len({q['path']for q in im['current_inputs']}),'reused_StageA_pins':22,'header_lines':83,'source_items':137,'source_nodes':32,'source_edges':67,'public_callers':6,'lets':8,'conjuncts':10,'semantic_slots':7,'source_blockers':0,'compile_or_75_BODY_review':False},sort_keys=True))
if __name__=='__main__':main()
