from pathlib import Path
import datetime, hashlib, json, os, re
out=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
p=json.loads((out/'candidate-input01.raw').read_text(encoding='utf-8'))
dispatch=json.loads((out/'candidate-dispatch.freeze76.raw.json').read_text(encoding='utf-8'))
q={k:v for k,v in p.items() if k!='packet_sha256'}
canonical=sha(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert canonical==p['packet_sha256']==dispatch['canonical_reviewer_packet_sha256']
assert p['publication_binding_sha256']==dispatch['publication_binding_sha256']
assert sha(p['lean']['statement'].encode())==p['lean']['statement_sha256']
assert sha(p['source']['original_text'].encode())==p['source']['text_sha256']
assert sha(p['blind_reconstruction']['text'].encode())==p['blind_reconstruction']['text_sha256']
module=(out/'candidate-input03.raw').read_bytes()
assert module==(out/'candidate-input04.raw').read_bytes()
assert p['candidate_publication_context']['current_lean_module'].encode()==module
assert p['candidate_publication_context']['file']==sha(module)
header=(out/'candidate-input05.raw').read_bytes()
assert header.decode().strip()=='theorem '+p['lean']['declaration'].split('.')[-1]+p['lean']['statement']
assert p['candidate_publication_context']['toolchain']==sha((out/'candidate-input07.raw').read_bytes().replace(b'\r\n',b'\n'))
assert p['candidate_publication_context']['dependencies']==sha((out/'candidate-input08.raw').read_bytes().replace(b'\r\n',b'\n'))
units=json.loads((out/'candidate-input14.raw').read_text(encoding='utf-8'))['units']
assert len(units)==1
lesson=p['candidate_publication_context']['lesson']
assert all(units[0][k]==v for k,v in lesson.items())
assert set(units[0])-set(lesson)=={'boundary'}
lines=module.splitlines(keepends=True)
assert len(lines)==412
body=[];last=192
for i,s in enumerate(lesson['steps'],1):
    r=s['lean_source_region']; a=r['start_line']; b=r['end_line']
    data=b''.join(lines[a-1:b])
    assert a==last+1 and data==s['lean'].encode()
    assert sha(data)==r['exact_code_raw_sha256']
    assert r['source_raw_sha256']==sha(module)
    body.append({'step':i,'title':s['title'],'start_line':a,'end_line':b,'exact_code_raw_sha256':sha(data),'contiguous':True,'current_code_exact':True})
    last=b
assert len(body)==10 and last==409
neutral=json.loads((out/'candidate-input06.raw').read_text(encoding='utf-8'))
remap=[]
for group in ['callers','literal_definitions','conclusion_groups']:
    for x in neutral[group]:
        literal=x.get('header_literal',x.get('literal','')).encode()
        start=header.index(literal)
        stop=start+len(literal)
        old=x['header_RAW_range']
        old_match=header[old[0]:old[1]]==literal
        remap.append({'id':x['id'],'group':group,'current_expanded_header_RAW_range':[start,stop],'provided_neutral_header_RAW_range':old,'provided_range_matches_current_header':old_match,'literal_matches_current_header':True,'meaning':'Fresh exact coordinates computed from current pinned expanded header; supplied old offsets are not used.'})
assert neutral['counts']=={'callers':6,'conclusion_groups':10,'literal_definitions':11,'typing':5}
scan=re.sub(r'/\-[\s\S]*?\-/','',module.decode())
scan=re.sub(r'--[^\n]*','',scan)
for pattern in [r'\b(?:sorry|admit)\b',r'(?m)^\s*(?:private\s+)?axiom\b',r'Prop\s*:=\s*True',r':=\s*trivial\b']:
    assert not re.search(pattern,scan)
direct=json.loads((out/'direct-review76.foreground-exit.json').read_text(encoding='utf-8'))
assert direct['exit_code']==0 and direct['source_module_raw_sha256']==sha(module)
stdout=(out/'direct-review76.stdout.raw').read_text(encoding='utf-8')
assert 'depends on axioms: [propext,' in stdout and 'Classical.choice,' in stdout and 'Quot.sound]' in stdout
assert (out/'direct-review76.stderr.raw').read_bytes()==b''
put={'status':'PASS_CANDIDATE_ARTIFACT_AND_BODY_BINDING','pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'packet_sha256':canonical,'publication_binding_sha256':p['publication_binding_sha256'],'whole_module_RAW_sha256':sha(module),'module_lines':412,'BODY_steps':body,'neutral_binder_fresh_coordinates':remap,'neutral_stale_coordinate_count':sum(not x['provided_range_matches_current_header'] for x in remap),'neutral_coordinate_status':'Literal content is correct; stale ranges in the auxiliary neutral inventory are not evidence. Fresh coordinates here bind the actual frozen header.','direct_Lean_PID':direct['actual_foreground_PID'],'direct_Lean_exit':direct['exit_code'],'axioms':['propext','Classical.choice','Quot.sound'],'fake_closure_scan':'PASS_CURRENT_MODULE','source_only_freeze_unchanged':sha((out/'source-only.freeze76.json').read_bytes())=='b543f6543f3d6c8e22bea1986427c41e9b10a45e0f732f143c59c4d75a3f771f','mathematical_status':'Semantic source verdict is authored independently; these integrity checks alone do not confer source fidelity.'}
assert put['source_only_freeze_unchanged']
(out/'candidate-checks76.json').write_text(json.dumps(put,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in put.items() if k not in ['BODY_steps','neutral_binder_fresh_coordinates']},ensure_ascii=False,indent=2))
