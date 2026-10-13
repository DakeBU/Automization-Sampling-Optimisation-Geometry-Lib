from pathlib import Path
import subprocess,os,time,json,hashlib
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def info(p):return dict(path=p.relative_to(R).as_posix(),sha256_raw=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
p=O/'API104-corrected.lean';assert not p.exists()
p.write_bytes((O/'API104.lean').read_bytes().replace(b'MeasureTheory.Measure.withDensity_mul',b'MeasureTheory.withDensity_mul').replace(b'MeasureTheory.map_comap_subtype_coe',b'map_comap_subtype_coe'))
save('reviewer-api-name-erratum104.native.json',{'scope':'Reviewer-owned probe only; not a header/sourcegraph defect','original':info(O/'API104.lean'),'negative_receipt':info(O/'api.receipt.json'),'corrections':['MeasureTheory.Measure.withDensity_mul -> MeasureTheory.withDensity_mul','MeasureTheory.map_comap_subtype_coe -> global map_comap_subtype_coe'],'reason':'Original review probe overqualified two declarations. Creator retrieval already named both correctly. Preserve original negative and compile corrected probe only.','corrected':info(p),'header_unchanged':True})
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p)];t=time.time();q=subprocess.run(cmd,cwd=R,env=env,capture_output=True)
for ext,b in [('stdout',q.stdout),('stderr',q.stderr)]:(O/('api-corrected.'+ext+'.log')).write_bytes(b)
save('api-corrected.receipt.json',dict(command=cmd,exit_code=q.returncode,elapsed_seconds=time.time()-t,input=info(p),stdout=info(O/'api-corrected.stdout.log'),stderr=info(O/'api-corrected.stderr.log')))
print(q.returncode)
