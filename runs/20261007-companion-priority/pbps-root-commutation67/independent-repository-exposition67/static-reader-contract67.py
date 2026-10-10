from pathlib import Path
import json, hashlib, os, datetime
ROOT=Path('E:/Samplinglib');O=ROOT/'runs/20261007-companion-priority/pbps-root-commutation67/independent-repository-exposition67'
def sha(b):return hashlib.sha256(b).hexdigest()
def ld(p):return json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();v=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(v),'LF_sha256':sha(v)}
assert not (O/'lease.final.json').exists()
pre=ld(O/'SCI67-native-immutable-precheck.json');science=pre['nine_science_Lean_publication_lesson_audit_Git_bytes']
for s in science:assert pin(ROOT/s['repository_path'])['RAW_sha256']==s['Git_RAW']['RAW_sha256']
records=[];steps=[]
for slug in ['real-l2-positive-square-commutation','pbps-actual-root-inverse-commutation']:
 pubpath=ROOT/'website/content/publications'/f'{slug}.json';lessonpath=ROOT/'website/content/declaration_lessons'/f'{slug}.json'
 item=ld(pubpath)['items'][0];unit=ld(lessonpath)['units'][0];b=item['bindings'][0]
 assert unit['declaration']==b['declaration']
 assert unit['statement']==unit['lean_statement'] and item['statement'] and unit['statement'] and item['source']['attribution'] and item['source']['anchor']
 for i,s in enumerate(unit['steps'],1):
  z=s['lean_source_region'];p=ROOT/z['path'];raw=p.read_bytes();literal=b''.join(raw.splitlines(keepends=True)[z['start_line']-1:z['end_line']])
  assert sha(raw)==z['source_raw_sha256'] and sha(literal)==z['exact_code_raw_sha256'] and s['lean'].encode()==literal
  t=raw.decode('utf-8');before=b''.join(raw.splitlines(keepends=True)[:z['start_line']-1]).decode('utf-8');assert ':= by' in before
  assert s['formula'] and s['text'] and s['title']
  assert '\\\\' not in s['formula']
  steps.append({'publication':slug,'step':i,'title':s['title'],'text':s['text'],'formula':s['formula'],'literal_BODY_region':z,'literal_Lean_RAW':literal.decode('utf-8'),'source_file':pin(p),'formula_backslash_pairs':0,'literal_body_region_matches_lesson':True})
 records.append({'publication':slug,'publication_pin':pin(pubpath),'lesson_pin':pin(lessonpath),'declaration':b['declaration'],'cell':b['cell'],'full_attributed_publication_statement':item['statement'],'complete_lesson_statement':unit['statement'],'source':item['source'],'assumptions':unit['assumptions'],'formula':unit['formula'],'boundary':unit['boundary'],'steps':len(unit['steps']),'mathematics_review_reused_unchanged':True})
assert len(steps)==10 and [r['steps'] for r in records]==[4,6]
out={'schema':'repository67-stable-SCI-reader-contract-v1','actual_PID':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_STATIC_CONTRACT_ONLY','exact_SCI_commit':pre['SCI_commit'],'publications':records,'ten_literal_BODY_formula_steps':steps,'actual_browser_render_copy_download_not_yet_checked':True,'final_graph_or_cell_acceptance':False,'source_math_replay':False,'full_Exposition':False,'PURIFIED':False,'canonical_writes':False}
(O/'stable-static-reader-contract.json').write_bytes((json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
print(json.dumps({'actual_PID':os.getpid(),'status':out['status'],'complete_statements':2,'literal_BODY_formula_steps':10,'final_inputs_ready':False}))
