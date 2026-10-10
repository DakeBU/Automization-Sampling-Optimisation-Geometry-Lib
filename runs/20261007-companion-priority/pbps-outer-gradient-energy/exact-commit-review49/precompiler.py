import pathlib,json,hashlib,subprocess,sys,datetime,os
r=pathlib.Path('E:/Samplinglib');run=r/'runs/20261007-companion-priority/pbps-outer-gradient-energy';out=run/'exact-commit-review49';commit='5ba91a1c9a553b13a38d48f02f0725a69af146a4';parent='8cacef16fb16b9a1258c365f5c2024f58392326d'
def H(b):return hashlib.sha256(b).hexdigest()
def LF(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def read(p):return json.loads(pathlib.Path(p).read_text('utf-8'))
def bind(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':str(p.relative_to(r)).replace('\\','/'),'bytes':len(b),'raw_sha256':H(b),'lf_sha256':H(LF(b))}
def git(*a):return subprocess.check_output(['git',*a],cwd=r)
assert git('rev-parse','HEAD').decode().strip()==commit and git('rev-parse',commit+'^').decode().strip()==parent
sys.path[:0]=[str(r),str(r/'tools')];from tools import astis_advance
states=astis_advance.current_advances();s=states['ASTIS-SA-20261007-PBPSConditionalGradientEnergy'];assert s['state']=='PROVED_LOCAL';stabilizing={k:v.get('owner_id')for k,v in states.items()if v.get('state')=='STABILIZING'};assert list(stabilizing)==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
leases=[]
for name in ['probability.0.compiler.lease.json','production.0.compiler.lease.json','production.1.compiler.lease.json','production.2.compiler.lease.json','tests.0.compiler.lease.json','tests.1.compiler.lease.json','whole-proof-review49/lease.json','source.review.lease.json','reviewer.source.lease.json','source.review.primary-first.lease.json','anonymous-decoder/lease.json']:
 p=run/name;assert read(p)['status']=='CLOSED';leases.append(bind(p))
freeze=read(run/'math-freeze.json');rows=[]
for x in freeze['inputs']:
 p=r/x['path'];d=bind(p);assert all(d[k]==x[k]for k in ['bytes','raw_sha256','lf_sha256']),x['path'];blob=git('show',commit+':'+x['path']);assert blob in (p.read_bytes(),LF(p.read_bytes()));rows.append({**d,'Git_blob_raw_sha256':H(blob),'status':'PASS_STRICT_CURRENT'})
assert len(rows)==45
reach=read(run/'whole-proof-review49/astis-import-reachability.json');local=[]
for x in reach['modules']:
 p=pathlib.Path(x['path']);d=bind(p);assert all(d[k]==x[k]for k in ['raw_sha256','lf_sha256']);blob=git('show',commit+':'+d['path']);assert blob in (p.read_bytes(),LF(p.read_bytes()));local.append({**d,'Git_blob_raw_sha256':H(blob)})
assert len(local)==65
seal=read(run.parent/'pbps-outer-gradient-preproof49/statement-seals.accepted.json')['signatures'][0];prod=(r/'AutoSamplingTheory/ExampleCases/ProximalBPS/ConditionalGradientEnergy.lean').read_bytes();text=LF(prod).decode();a=text.index('theorem reflected_conditional_gradient_energy');z=text.index(' := by',a);header=text[a:z]+'\n';assert header==seal['signature_text'] and len(header.encode())==1795 and H(header.encode())==seal['signature_lf_sha256']
assert (r/'lean-toolchain').read_text('utf-8').strip()=='leanprover/lean4:v4.33.0';manifest=read(r/'lake-manifest.json');mathlib=next(x for x in manifest['packages']if x['name']=='mathlib');assert mathlib['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d';assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r/'.lake/packages/mathlib').decode().strip()==mathlib['rev']
packet={'status':'PASS_COMPILER_INPUTS_BOUND','checked_commit':commit,'parent':parent,'SAU_state':s['state'],'sole_STABILIZING':stabilizing,'freeze45':rows,'local_imports65':local,'header1795_LF_sha256':H(header.encode()),'actual_closed_parent_leases':leases,'Lean':'4.33.0','Mathlib':mathlib['rev'],'lake_executable':bind(pathlib.Path('C:/Users/admin/.elan/bin/lake.EXE')) if False else 'C:/Users/admin/.elan/bin/lake.EXE'};(out/'precompiler.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n','utf-8');(out/'state.before.json').write_text(json.dumps({'SAU':s,'sole_STABILIZING':stabilizing},ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps({'state':s['state'],'freeze':len(rows),'local_imports':len(local),'header':1795,'closedleases':len(leases)}))
