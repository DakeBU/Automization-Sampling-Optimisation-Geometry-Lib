import datetime, hashlib, json, os, pathlib, subprocess
root = pathlib.Path('E:/Samplinglib')
out = root / 'runs/20261007-companion-priority/gaussian-compact-hilbert-lsi/whole-proof-review'
env = dict(os.environ, LEAN_NUM_THREADS='2', ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0', PYTHONUTF8='1')
commands = [
 ('focused', ['lake', 'build', 'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactHilbertLogSobolev', 'Tests.GaussianCompactHilbertLogSobolev']),
 ('direct', ['lake', 'env', 'lean', 'Tests/GaussianCompactHilbertLogSobolev.lean'])]
leasepath=out/'lease.json'
lease=json.loads(leasepath.read_text(encoding='utf-8'));lease['compiler_started']=True
leasepath.write_bytes((json.dumps(lease,indent=2)+'\n').encode())
for label, command in commands:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (out/(label+'.log')).open('xb') as log:
  p=subprocess.run(command,cwd=str(root),env=env,stdout=log,stderr=subprocess.STDOUT)
 end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 raw=(out/(label+'.log')).read_bytes()
 status={'label':label,'command':command,'exit_code':p.returncode,'started_utc':start,'completed_utc':end,'environment':{k:env[k] for k in ['LEAN_NUM_THREADS','ELAN_TOOLCHAIN','PYTHONUTF8']},'log_raw_sha256':hashlib.sha256(raw).hexdigest(),'log_lf_sha256':hashlib.sha256(raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest(),'compiler_lane':'Independent exclusive serial foreground'}
 with (out/(label+'.status.json')).open('xb') as f:f.write((json.dumps(status,indent=2)+'\n').encode())
 print(json.dumps(status),flush=True)
 if p.returncode:raise SystemExit(p.returncode)
