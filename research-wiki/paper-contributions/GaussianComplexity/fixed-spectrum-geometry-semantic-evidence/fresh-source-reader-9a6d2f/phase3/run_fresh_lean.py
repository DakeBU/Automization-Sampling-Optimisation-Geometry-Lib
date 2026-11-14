from pathlib import Path
import subprocess,os,hashlib,json,datetime
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');OUT=ROOT/'.astis/semantic-neutral-20261109/src_9a6d2f/phase3';FRESH=OUT/'fresh-olean';FRESH.mkdir(exist_ok=True)
BIN=Path('/Users/zhouhuanjian/.elan/toolchains/leanprover--lean4---v4.33.0/bin/lean')
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1';env['GIT_OPTIONAL_LOCKS']='0'
libs=[FRESH]+sorted((ROOT/'.lake/packages').glob('*/.lake/build/lib/lean'))+[ROOT/'.lake/build/lib/lean'];env['LEAN_PATH']=':'.join(map(str,libs))
pins=json.loads((ROOT/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-semantic-evidence/full-review-input-pins.json').read_text())
res={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_binary':str(BIN),'lean_binary_sha256':hashlib.sha256(BIN.read_bytes()).hexdigest(),'LEAN_PATH':env['LEAN_PATH'],'package_revisions':[],'runs':[]}
res['version']=subprocess.run([str(BIN),'--version'],cwd=ROOT,env=env,text=True,capture_output=True).stdout.strip()
manifest=json.loads((ROOT/'lake-manifest.json').read_text())
for pkg in manifest['packages']:
 p=ROOT/'.lake/packages'/pkg['name'];r=subprocess.run(['git','-C',str(p),'rev-parse','HEAD'],cwd=ROOT,env=env,text=True,capture_output=True)
 res['package_revisions'].append({'name':pkg['name'],'expected':pkg['rev'],'actual':r.stdout.strip(),'returncode':r.returncode,'matches':r.stdout.strip()==pkg['rev']})
assert all(x['matches'] for x in res['package_revisions']),res['package_revisions']
mods=['AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAdmissibility','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumFirstOrder','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry','Tests.GaussianComplexityFixedSpectrumGeometry']
for mod in mods:
 rel=Path(*mod.split('.'));src=ROOT/rel.with_suffix('.lean');target=FRESH/rel.with_suffix('.olean');target.parent.mkdir(parents=True,exist_ok=True)
 assert hashlib.sha256(src.read_bytes()).hexdigest()==pins['exact_inputs'][str(src.relative_to(ROOT))]
 cmd=[str(BIN),'-R',str(ROOT),'-o',str(target),'-i',str(target.with_suffix('.ilean')),str(src)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();r=subprocess.run(cmd,cwd=ROOT,env=env,text=True,capture_output=True);log=OUT/'lean-evidence'/(mod.replace('.','__')+'.log');log.write_text(r.stdout+r.stderr)
 rec={'module':mod,'command':cmd,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'started_utc':start,'returncode':r.returncode,'log':str(log.relative_to(OUT)),'olean':str(target.relative_to(OUT))}
 if target.exists():rec['olean_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
 res['runs'].append(rec);(OUT/'lean-evidence/fresh-compilation.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'module':mod,'returncode':r.returncode,'output':r.stdout+r.stderr}),flush=True)
 if r.returncode:raise SystemExit(r.returncode)
print('FRESH_COMPILE_PASS',flush=True)
