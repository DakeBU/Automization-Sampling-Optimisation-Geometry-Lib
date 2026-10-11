import ast, collections, difflib, gzip, hashlib, json, pathlib, re, subprocess, sys
ROOT=pathlib.Path('E:/Samplinglib')
RUN=ROOT/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94'
OUT=RUN/'integration-reconciliation-review94'
MERGE='ae17ebb1bb4cb46a47e1674373e9c317665152a1'
OURS='d39449f5b6fd6ebe05eb092f843d1b14c54623b1'
THEIRS='07fb78dd00550902ba2344edf5d6ac94d93d2044'
inputs=[]; checks=[]
def sha(b): return hashlib.sha256(b).hexdigest()
def save(p,v): (OUT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
def blob(ref,p):
 b=git('show',ref+':'+p); inputs.append({'path':p,'commit':ref,'raw_sha256':sha(b),'bytes':len(b)}); return b
def read(p):
 p=pathlib.Path(p); p=p if p.is_absolute() else ROOT/p
 b=p.read_bytes(); inputs.append({'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}); return b
def check(name,cond,**details):
 checks.append({'name':name,'pass':bool(cond),**details})
def norm(b): return b.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def events(b): return [json.loads(x) for x in norm(b).splitlines() if x.strip()]
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def subseq(a,b):
 it=iter(b); return all(any(y==x for y in it) for x in a)
OUT.mkdir(parents=True,exist_ok=True)
check('merge parents',git('rev-parse',MERGE+'^1').decode().strip()==OURS and git('rev-parse',MERGE+'^2').decode().strip()==THEIRS)
BASE=git('merge-base',OURS,THEIRS).decode().strip()
res=json.loads(read(RUN/'integration94/main-reconciliation/resolution.json'))
diffs=[]
for i,rec in enumerate(res['records']):
 p=rec['path']; versions={}
 for label,ref in [('base',BASE),('ours',OURS),('theirs',THEIRS)]:
  b=blob(ref,p); archive=read(RUN/f'integration94/main-reconciliation/{i}.{label}.raw.gz')
  check(f'archive {i} {label}',gzip.decompress(archive)==b and sha(b)==rec['inputs'][label])
  versions[label]=b
 b=blob(MERGE,p); versions['merged']=b
 check(f'merged resolution {i}',sha(b)==rec['result_raw_sha256'])
 if p.endswith('.py') or 'Registry' in p or p=='Tests/Basic.lean':
  for parent in ['ours','theirs']:
   diffs.extend(difflib.unified_diff(norm(versions[parent]).splitlines(True),norm(b).splitlines(True),fromfile=parent+':'+p,tofile='merged:'+p,n=3))
 if p.endswith('Registry.lean'):
  keys={k:re.findall(r'key\s*:=\s*"([^"]+)"',norm(v)) for k,v in versions.items()}
  check('Registry exact union no duplicates count544',set(keys['merged'])==set(keys['ours'])|set(keys['theirs']) and len(keys['merged'])==len(set(keys['merged']))==544,counts={k:len(v) for k,v in keys.items()},added_to_ours=sorted(set(keys['merged'])-set(keys['ours'])),added_to_theirs=sorted(set(keys['merged'])-set(keys['theirs'])))
 if p=='Tests/Basic.lean': check('Basic count544','= 544' in norm(b))
 if p.endswith('substantive_advances.jsonl'):
  es={k:[canon(x) for x in events(v)] for k,v in versions.items()}
  check('ledger exact event multiset union',collections.Counter(es['merged'])==collections.Counter(es['ours'])|collections.Counter(es['theirs']),counts={k:len(v) for k,v in es.items()})
  check('ledger preserves both branch orders',subseq(es['ours'],es['merged']) and subseq(es['theirs'],es['merged']))
  current=events(read(p)); check('current ledger retains merge prefix',current[:len(es['merged'])]==events(b),postmerge_events=current[len(es['merged']):])
 if p.endswith('test_astis_publication.py'):
  def funcs(v): return {n.name:ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(norm(v))) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
  fs={k:funcs(v) for k,v in versions.items()}
  check('Python tests exact method union',set(fs['merged'])==set(fs['ours'])|set(fs['theirs']))
  changed={par:[name for name in fs[par] if name in fs['merged'] and fs[par][name]!=fs['merged'][name]] for par in ['ours','theirs']}
  checks.append({'name':'Python changed methods for manual order-marker review','pass':True,'changed':changed})
(OUT/'normalized-parent-diffs.patch').write_text(''.join(diffs),encoding='utf-8')
for p in ['Tests.lean','Tests/Basic.lean']:
 v={ref:norm(blob(ref,p)) for ref in [OURS,THEIRS,MERGE]}
 imports={ref:re.findall(r'^import (.+)$',s,re.M) for ref,s in v.items()}
 check('import union '+p,set(imports[MERGE])==set(imports[OURS])|set(imports[THEIRS]) and len(imports[MERGE])==len(set(imports[MERGE])),counts={ref:len(x) for ref,x in imports.items()})
 check('import order '+p,subseq(imports[OURS],imports[MERGE]) and subseq(imports[THEIRS],imports[MERGE]))
prior=json.loads(read(RUN/'exact-commit-verification94/closed-RAW-manifest94.json'))
collaborators=prior['preserved_collaborator_inputs']; save('collaborator-contract.json',collaborators)
for rec in collaborators:
 b=read(rec['path']); check('collaborator '+rec['path'],sha(b)==rec['raw_sha256'])
check('all21 collaborators enumerated',len(collaborators)==21)
for rec in prior['checked_science_inputs'][:4]:
 p=rec['path']; a=blob(MERGE,p); b=read(p)
 check('science unchanged '+p,sha(a)==rec['raw_sha256'] and a==b)
for rec in json.loads(read(RUN/'integration94/text-normalization94.json')):
 checks.append({'name':'normalization record pending schema inspection','pass':True,'record':rec})
read(RUN/'integration94/sole-lane-acquisition94.json')
read(RUN/'integration94/main-reconciliation/root-test-line-endings.json')
save('checks.initial.json',{'merge':MERGE,'base':BASE,'checks':checks})
save('inputs.initial.json',inputs)
print(json.dumps({'checks':len(checks),'failures':[x for x in checks if not x['pass']],'collaborator_schema':collaborators[0]},indent=2))
