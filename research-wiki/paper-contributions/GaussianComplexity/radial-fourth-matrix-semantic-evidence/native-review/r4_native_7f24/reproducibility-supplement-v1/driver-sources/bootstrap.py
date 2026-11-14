import subprocess, pathlib, hashlib, json, os, datetime, time, shutil, sys
REPO=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
ROOT=REPO/'.astis/semantic-neutral-20261111/r4_native_7f24'
CAND='69a3336dde302c4a34dbd88708ff6226b2bd0e87'
BASE='a7244d6ad6043e03c126be08d9d32e2ae19a9e41'
SNAP=ROOT/'candidate'
LOGS=ROOT/'execution'
LOGS.mkdir(parents=True,exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def save(p,obj):
 p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def run(label,args,cwd=REPO,env=None,check=True):
 n=len(list(LOGS.glob('*.receipt.json')))+1
 stem=LOGS/f'{n:03d}-{label}'
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 p=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 stem.with_suffix('.stdout').write_bytes(p.stdout);stem.with_suffix('.stderr').write_bytes(p.stderr)
 save(str(stem)+'.receipt.json',{'label':label,'argv':list(map(str,args)),'cwd':str(cwd),'start_utc':start,'elapsed_seconds':time.monotonic()-t,'returncode':p.returncode,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'LEAN_PATH':env.get('LEAN_PATH') if env else None})
 print(label,p.returncode,flush=True)
 if check and p.returncode: raise RuntimeError(f'{label} failed; preserved at {stem}')
 return p.stdout
P='AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumRadialFourthMoment.lean'
T='Tests/GaussianComplexityFixedSpectrumRadialFourthMoment.lean'
G='AutoSamplingTheory/TechnicalLemmas/StochasticProcesses/GaussianFourthMoment.lean'
SEAL='research-wiki/paper-contributions/GaussianComplexity/radial-fourth-matrix-statement-seal.json'
MAP='research-wiki/paper-contributions/GaussianComplexity/radial-fourth-matrix-semantic-evidence/source-lean-map.draft.json'
LESSON='website/content/declaration_lessons/huanjian-gaussian-radial-fourth-matrix.json'
PUB='website/content/publications/huanjian-gaussian-radial-fourth-matrix.json'
EXPECTED={P:'346fc4b30dd5252f422c803eb7f77160cf7657dabe74c67fc8f23de1d5e674f6',T:'9bb4d6223404f1d96a262d0d8c85a1c2edab31dae3cb6fc949a6d5abbbec2f24',G:'c3576c191c2fa7bafcdc2a30c5731d0ea60c88e96be9e58e52ae09e33013b65c',SEAL:'cc628d801ed367e1e57e99d69449d36a90b2803f7371986b964b4864409f6dec',MAP:'4215c8e8da2df765d7edb029c64f751a218cca5de0de6a04f462cdc19f185535','lake-manifest.json':'b83ca83b9cf7caa85fa8b023c2ff9a3fb7a7cce7e1c332e810c348535ec49c37'}
