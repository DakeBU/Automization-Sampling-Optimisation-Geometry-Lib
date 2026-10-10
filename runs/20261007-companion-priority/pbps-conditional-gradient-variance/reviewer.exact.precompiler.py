from pathlib import Path
import json,hashlib,subprocess,shutil
r=Path('E:/Samplinglib');p=r/'runs/20261007-companion-priority/pbps-conditional-gradient-variance';commit='53f65a50263c13823aef5da7d9a3279de3514243'
sha=lambda b:hashlib.sha256(b).hexdigest();lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r).decode().strip()==commit
freeze=json.loads((p/'math-freeze.json').read_text());assert len(freeze['inputs'])==36
rows=[]
for x in freeze['inputs']:
 b=(r/x['path']).read_bytes();assert len(b)==x['bytes'] and sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256'];bc=subprocess.check_output(['git','show',commit+':'+x['path']],cwd=r);assert lf(b)==lf(bc)
 rows.append({**x,'Git_blob_raw_sha256':sha(bc),'Git_blob_LF_identical':True,'status':'PASS_STRICT_CURRENT'})
imports=json.loads((p/'whole-proof-review48/reachable-local-imports.json').read_text());assert len(imports)==63
local=[]
for path,x in imports.items():
 b=(r/path).read_bytes();assert sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256'];bc=subprocess.check_output(['git','show',commit+':'+path],cwd=r);assert lf(b)==lf(bc)
 local.append({'path':path,**x,'Git_blob_raw_sha256':sha(bc),'status':'PASS_STRICT_CURRENT'})
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r/'.lake/packages/mathlib').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
out={'checked_commit':commit,'freeze36':rows,'recursive_local_imports63':local,'Lean':'4.33.0','Mathlib':'db584cd6d46c92f209a44c0f1c829460d327499d','lake_executable':shutil.which('lake'),'status':'PASS_COMPILER_INPUTS_BOUND'}
(p/'reviewer.exact.precompiler.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':out['status'],'freeze':len(rows),'recursive_local_imports':len(local),'lake':out['lake_executable']}))
