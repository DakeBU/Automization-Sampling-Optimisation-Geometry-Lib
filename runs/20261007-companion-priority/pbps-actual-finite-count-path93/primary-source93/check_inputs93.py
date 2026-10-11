from pathlib import Path
import json,hashlib,re
root=Path('E:/Samplinglib')
base=root/'runs/20261007-companion-priority/pbps-actual-finite-count-path93'
p=json.loads((base/'anti-anchored.review93.v2.json').read_text(encoding='utf-8-sig'))
canon=lambda x:hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
src=(root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean').read_text(encoding='utf-8-sig')
l=json.loads((root/'website/content/declaration_lessons/pbps-actual-finite-count-path.json').read_text(encoding='utf-8-sig'))['units'][0]
pub=json.loads((root/'website/content/publications/pbps-actual-finite-count-path.json').read_text(encoding='utf-8-sig'))['items'][0]
old=json.loads((base/'anti-anchored.review93.json').read_text(encoding='utf-8-sig'))
checks={'packet_digest':canon({k:v for k,v in p.items() if k!='packet_sha256'}),'declared_digest':p['packet_sha256'],'context_module_matches':p['candidate_publication_context']['current_lean_module']==src,'source_text_matches_publication':p['source']['original_text']==pub['statement'],'lesson_statement_matches_publication':l['statement']==pub['statement'],'statement_unchanged':p['lean']['statement']==old['lean']['statement'],'reconstruction_unchanged':p['blind_reconstruction']==old['blind_reconstruction'],'private_theorem_count':len(re.findall(r'^private theorem ',src,re.M)),'private_def_count':len(re.findall(r'^private def ',src,re.M)),'public_theorem_count':len(re.findall(r'^theorem ',src,re.M)),'placeholder_token_scan':re.findall(r'\b(?:sorry|admit|axiom)\b',src)}
regions=[]
for i,step in enumerate(l['steps']):
    body=step['lean']; start=src.find(body)
    regions.append({'step':i+1,'title':step['title'],'exact_contiguous_module_substring':start>=0,'start_line':src[:start].count('\n')+1 if start>=0 else None,'end_line':src[:start+len(body)].count('\n')+1 if start>=0 else None,'body_utf8_sha256':hashlib.sha256(body.encode()).hexdigest(),'body_bytes':len(body.encode()),'formula':step['formula'],'exposition':step['text']})
checks['regions']=regions
(base/'primary-source93/input-and-body-checks93.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in checks.items() if k!='regions'},indent=2))
for r in regions: print(r['step'],r['exact_contiguous_module_substring'],r['start_line'],r['end_line'],r['body_utf8_sha256'])
print('context fields', list(p['candidate_publication_context'].keys()))
print('context lesson type',type(p['candidate_publication_context']['lesson']).__name__)
