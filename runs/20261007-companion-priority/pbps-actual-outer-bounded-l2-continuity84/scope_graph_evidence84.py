"""Correct graph evidence scope; retain all earlier native observations."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path(__file__).parent
out=r/'integration84/cell-admission-correction/graph-scope'
out.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),RAW_bytes=len(b))
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
cell=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json')
note=r/'integration.corrected.notes.json'
before=dict(cell=pin(cell),note=pin(note),graph=pin('_site/data/underlying-lean-graph.json'))
(out/'cell.before.json').write_bytes(cell.read_bytes())
(out/'note.before.json').write_bytes(note.read_bytes())
c=load(cell)
scope='Current affected coarse shared-root SVG rendered and actually viewed, with RAW pins. The generated Lean reference view and focused coverage check use incomplete name-scanned reference signals, not elaborated theorem dependencies; scanner false positives are possible. The four actual producer parents are certified separately by independent-math84/kernel-dependency-summary84.json. Actual page/interactive visual acceptance pending; no full Exposition Seal.'
assert c['publication']['visual_review'].startswith('Current affected coarse') if 'publication' in c and 'visual_review' in c['publication'] else True
def change(x):
 if isinstance(x,dict):
  for k,v in x.items():
   if k=='visual_review' and isinstance(v,str) and v.startswith('Current affected coarse'):
    x[k]=scope;return 1
   if isinstance(v,(dict,list)) and change(v):return 1
 elif isinstance(x,list):
  for v in x:
   if change(v):return 1
 return 0
assert change(c)==1
save(cell,c)
env=os.environ.copy();env['PYTHONUTF8']='1';env.pop('ELAN_TOOLCHAIN',None)
env['PATH']=str(Path('.astis/toolchain/lean-4.33.0-windows/bin').resolve())+os.pathsep+env['PATH']
checks=[]
for label,args in [('refresh-reference-graph',['website/scripts/underlying_lean_graph.py']),('correct84-graph',['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity']),('publication',['tools/astis_publication.py','check','--base','5186f92607df617c4e4a8a90d0c5e6b5fc611090']),('frontier',['tools/astis_frontier_cells.py','check']),('semantic',['tools/astis_semantic_roundtrip.py','check']),('site-check',['website/scripts/check_site.py'])]:
 q=subprocess.run([sys.executable,'-X','utf8',*args],capture_output=True,env=env)
 for stream in ('stdout','stderr'):(out/(label+'.'+stream+'.log')).write_bytes(getattr(q,stream))
 receipt=dict(command=args,exit_code=q.returncode,terminal_closed=True,stdout=pin(out/(label+'.stdout.log')),stderr=pin(out/(label+'.stderr.log')))
 save(out/(label+'.receipt.json'),receipt)
 assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-6000:]
 checks.append(dict(label=label,receipt=pin(out/(label+'.receipt.json'))));print(label,'PASS',flush=True)
kernel=r/'independent-math84/kernel-dependency-summary84.json'
assert load(kernel)['expected_four_parent_frontier_exact']
module=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean')
assert pin(module)['RAW_sha256']=='8fd35db26717f46313fc53dd90691828b11c9d78cdcc4a62f68c8d59273cc2bd'
page=Path('_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html')
assert pin(page)['RAW_sha256']==load(r/'integration84/offline-reader.json')['page_RAW_sha256']
n=load(note)
n['graph_delta']='Generated source-name reference view refreshed and its SAU84 contribution coverage checked. These incomplete scanner signals may include false positives and are not elaborated proof dependencies. Separately, the independent Lean kernel audit certifies exactly four actual producer parents for the bounded-test outer square-integral theorem. No new conceptual mirror.'
n['kernel_dependency_evidence']=pin(kernel)
n['current_graph']=pin('_site/data/underlying-lean-graph.json')
n['publication_inputs_sha256']=load('_site/data/underlying-lean-graph.json')['publication_inputs_sha256']
n['graph_scope_correction']=dict(before=before,after_cell=pin(cell),checks=checks,math_or_source_or_BODY_changed=False,HTML_unchanged=pin(page))
n['reused_same_local_source_evidence']='Root/Tests/check/pycompile/site-build and full-base publication evidence reused for unchanged Lean, source, publication and eight-step HTML bytes. Current cell display wording now distinguishes scanner coverage from the separate kernel proof dependency certificate; the generated reference graph, focused84 graph, publication, frontier, semantic and site checks were refreshed after this wording change. Earlier observations are preserved.'
save(note,n)
save(out/'scope-correction.json',dict(before=before,after=dict(cell=pin(cell),note=pin(note),graph=pin('_site/data/underlying-lean-graph.json')),checks=checks,kernel=pin(kernel),source_unchanged=pin(module),HTML_unchanged=pin(page)))
