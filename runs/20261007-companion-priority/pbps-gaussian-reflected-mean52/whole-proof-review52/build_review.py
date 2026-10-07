import hashlib, json, os, pathlib, shutil, subprocess, sys
from datetime import datetime, timezone

ROOT = pathlib.Path('E:/Samplinglib')
OUT = ROOT / 'runs/20261007-companion-priority/pbps-gaussian-reflected-mean52/whole-proof-review52'
FREEZE = OUT.parent / 'math-freeze.json'
def now(): return datetime.now(timezone.utc).isoformat()
def dig(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':dig(b),'lf_sha256':dig(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def write(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def verify(label):
    frozen=json.loads(FREEZE.read_text(encoding='utf-8'))
    actual=[]; errors=[]
    for entry in frozen['inputs']:
        p=ROOT/entry['path']
        if not p.is_file(): errors.append({'path':entry['path'],'error':'missing'}); continue
        a=pin(p); actual.append(a)
        for key in ('raw_sha256','lf_sha256','bytes'):
            if a[key]!=entry[key]: errors.append({'path':entry['path'],'key':key,'expected':entry[key],'actual':a[key]})
    obj={'checked_utc':now(),'label':label,'freeze':pin(FREEZE),'count':len(frozen['inputs']),'unique_paths':len(set(x['path'] for x in frozen['inputs'])),'actual_inputs':actual,'errors':errors,'strict_all_pins_pass':not errors and len(actual)==333 and len(frozen['inputs'])==333}
    write(OUT/(label+'.input-bindings.json'),obj)
    if not obj['strict_all_pins_pass']: raise RuntimeError('Frozen input pin verification failed')
    return obj

OUT.mkdir(parents=True,exist_ok=True)
write(OUT/'lease.json',{'status':'OPEN','owner':'whole_math52','opened_utc':now(),'scope':'Independent whole mathematical proof review; no canonical writes','Python_pid':os.getpid()})
pre=verify('pre')
env=os.environ.copy()
old=env.pop('ELAN_TOOLCHAIN',None)
env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1'
toolchain=(ROOT/'lean-toolchain').read_text().strip()
if toolchain!='leanprover/lean4:v4.33.0': raise RuntimeError('Wrong repository toolchain')
lake=shutil.which('lake',path=env.get('PATH'))
v=subprocess.run([lake,'env','lean','--version'],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(OUT/'toolchain.log').write_bytes(v.stdout)
if v.returncode or b'4.33.0' not in v.stdout: raise RuntimeError('Compiler version validation failed')
sources=[]
for name in ['AutoSamplingTheory/TechnicalLemmas/Measure/GaussianReflectedMean.lean','Tests/ProximalBPSGaussianReflectedMean.lean']:
    sources.append(pin(ROOT/name))
    (OUT/(pathlib.Path(name).stem+'.source.raw.snapshot.lean')).write_bytes((ROOT/name).read_bytes())
cmd=[lake,'build','Tests.ProximalBPSGaussianReflectedMean']
opened=now()
with (OUT/'compiler.log').open('wb') as stream:
    p=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT)
    lease={'status':'OPEN','compiler':'OPEN','Python':'OPEN','opened_utc':opened,'command':cmd,'process_id':p.pid,'Python_pid':os.getpid(),'source_inputs':sources,'ELAN_TOOLCHAIN_unset':True,'inherited_override_was_set':old is not None,'LEAN_NUM_THREADS':'2','PYTHONUTF8':'1'}
    write(OUT/'compiler.lease.json',lease)
    rc=p.wait()
closed=now()
status={'command':cmd,'process_id':p.pid,'Python_pid':os.getpid(),'exit_code':rc,'opened_utc':opened,'finished_utc':closed,'log':pin(OUT/'compiler.log'),'source_inputs':sources,'toolchain':toolchain,'toolchain_version_exit_code':v.returncode,'toolchain_version_output':v.stdout.decode('utf-8','replace').strip(),'toolchain_version_log':pin(OUT/'toolchain.log'),'lake_manifest':pin(ROOT/'lake-manifest.json'),'ELAN_TOOLCHAIN_unset':True,'LEAN_NUM_THREADS':'2','PYTHONUTF8':'1'}
write(OUT/'compiler.status.json',status)
lease.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',closed_utc=closed,exit_code=rc)
write(OUT/'compiler.lease.json',lease)
post=verify('post')
print(json.dumps({'pin_count':pre['count'],'strict_pre':pre['strict_all_pins_pass'],'strict_post':post['strict_all_pins_pass'],'compiler_pid':p.pid,'exit_code':rc,'log_sha256':status['log']['raw_sha256'],'toolchain':status['toolchain_version_output']}))
