import hashlib,json,subprocess,datetime,pathlib,sys
R=pathlib.Path('E:/Samplinglib'); D=R/'runs/20261007-companion-priority/pbps-path-law-preread86'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],cwd=R).decode('utf-8').strip()
def write(n,o): (D/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
old=json.loads((R/'runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/pre-fetch84.workspace-RAW.json').read_text(encoding='utf-8'))['tracked_modified']
assert len(old)==21 and all(sha(R/p)==h for p,h in old.items())
assert git('rev-parse','HEAD')=='8280ef700ea01a1e94c9e7a3cba05a26b4156b56'
assert not git('diff','--cached','--name-only')
write('post-push85.preservation.json',{'head':git('rev-parse','HEAD'),'all21_RAW_preserved':True,'Goal_complete':False})
m=json.loads((D/'source-only-run-manifest86.json').read_text(encoding='utf-8'))
checks=[]
for group in ('raw_inputs','raw_outputs'):
 for x in m[group]:
  p=R/x['path']; h=sha(p)
  if h==x['raw_sha256']: relation='exact-current'
  else:
   # The source-first run may retain earlier shared administrative inputs.
   assert x['path'] in ['docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json']
   relation='historical-administration-not-current-scheduler'
  checks.append(dict(x,current_raw_sha256=h,relation=relation))
write('root.source-only86.receipt.json',{'checks':checks,'current_scheduling_required':True,'no_proof_credit':True})
cells=[{'path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':sha(p)} for p in sorted((R/'research-wiki/frontier-cells').glob('*.json'))]
write('pre-fetch86.workspace-RAW.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'branch':git('branch','--show-current'),'commit':git('rev-parse','HEAD'),'status':git('status','--porcelain=v1'),'tracked_modified':old,'frontier_cells':cells,'execution':json.loads((R/'website/content/samplewiki_companion_frontiers.json').read_text(encoding='utf-8'))['execution'],'handoff_raw_sha256':sha(R/'docs/companion-papers-handoff.md')})
p=subprocess.run([sys.executable,'-X','utf8','tools/astis_advance.py','capsule','--max-advances','2','--max-discoveries','0','--max-cells','2'],cwd=R,capture_output=True)
(D/'capsule86.json').write_bytes(p.stdout); (D/'capsule86.stderr.txt').write_bytes(p.stderr)
assert p.returncode==0
print(json.dumps({'preserved':21,'pins':len(checks),'pin_relations':{r:sum(x['relation']==r for x in checks) for r in set(x['relation'] for x in checks)},'frontier_cells':len(cells),'execution':json.loads((D/'pre-fetch86.workspace-RAW.json').read_text(encoding='utf-8'))['execution']},ensure_ascii=False))
