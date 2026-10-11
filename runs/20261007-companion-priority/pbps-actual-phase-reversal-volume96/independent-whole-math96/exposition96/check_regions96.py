from pathlib import Path
import hashlib,json
root=Path('E:/Samplinglib');out=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,o):
 p=out/n;assert not p.exists(),p;p.write_bytes((json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())
paths=['website/content/declaration_lessons/pbps-actual-phase-reversal-volume.json','website/content/publications/pbps-actual-phase-reversal-volume.json','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseReversalVolume.lean','runs/20261007-companion-priority/pbps-actual-phase-reversal-volume96/independent-whole-math96/whole-math-decision96.native.json','runs/20261007-companion-priority/pbps-actual-phase-reversal-volume96/independent-whole-math96/closed-RAW-manifest96.native.json']
(out/'inputs').mkdir(exist_ok=False)
inputs=[]
for i,p in enumerate(paths):
 b=(root/p).read_bytes();snap=out/'inputs'/f'{i:02d}.{Path(p).name}.exactraw';snap.write_bytes(b)
 inputs.append({'path':p,'raw_sha256':sha(b),'bytes':len(b),'snapshot':snap.relative_to(root).as_posix()})
u=json.loads((root/paths[0]).read_bytes())['units'][0];pub=json.loads((root/paths[1]).read_bytes())['items'][0]
assert inputs[2]['raw_sha256']=='4b144dfa25d9521803e37518b8a6386fff08396c5804e410e9be593d46833a7b'
assert u['statement']==u['lean_statement']==pub['statement']
assert u['assumptions']==pub['assumptions']
assert len(u['steps'])==7
lines=(root/paths[2]).read_bytes().decode().splitlines(keepends=True)
checks=[]
for i,s in enumerate(u['steps'],1):
 pin=s['lean_source_region'];a=pin['start_line'];b=pin['end_line']
 region=''.join(lines[a-1:b]);code=s['lean']
 check={'step':i,'title':s['title'],'start_line':a,'end_line':b,'source_sha_matches':pin['source_raw_sha256']==inputs[2]['raw_sha256'],'literal_code_matches_source':region==code,'code_sha_matches':sha(code.encode())==pin['exact_code_raw_sha256'],'code_raw_sha256':sha(code.encode())}
 assert all(check[k] for k in ['source_sha_matches','literal_code_matches_source','code_sha_matches']),check
 checks.append(check)
write('exact-region-checks96.native.json',{'status':'PASS','inputs':inputs,'seven_regions':checks,'complete_statements_identical':True,'assumptions_identical':True,'publication_source_coverage_status':pub['source_proof_coverage']['coverage_status']})
print(json.dumps({'inputs':inputs[:3],'regions_checked':len(checks),'coverage_status':pub['source_proof_coverage']['coverage_status']},indent=2))
