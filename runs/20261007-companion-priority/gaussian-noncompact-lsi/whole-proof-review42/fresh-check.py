import datetime,hashlib,json,os,pathlib,subprocess
ROOT=pathlib.Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/gaussian-noncompact-lsi/whole-proof-review42'
env=dict(os.environ,LEAN_NUM_THREADS='2',ELAN_TOOLCHAIN='leanprover/lean4:v4.33.0',PYTHONUTF8='1')
lp=OUT/'reviewer.math.lease.json';lease=json.loads(lp.read_text())
lease.update(compiler_lease='OPEN',compiler_started=True,compiler_lane='Exclusive serial foreground, root authorized; threads2')
lp.write_bytes((json.dumps(lease,indent=2)+'\n').encode())
(OUT/'compiler.lease.open.raw.snapshot.json').write_bytes(lp.read_bytes())
commands=[('focused',['lake','build','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianLogSobolev','Tests.GaussianLogSobolev']),('direct',['lake','env','lean','Tests/GaussianLogSobolev.lean']),('reachability',['lake','env','lean',str(OUT/'ReachabilityProbe.lean')])]
result=0
try:
 for label,cmd in commands:
  start=datetime.datetime.now(datetime.timezone.utc).isoformat()
  with (OUT/(label+'.log')).open('xb') as f:r=subprocess.run(cmd,cwd=str(ROOT),env=env,stdout=f,stderr=subprocess.STDOUT)
  b=(OUT/(label+'.log')).read_bytes()
  st=dict(label=label,command=cmd,exit_code=r.returncode,started_utc=start,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),log_raw_sha256=hashlib.sha256(b).hexdigest(),log_lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest(),environment={k:env[k] for k in ['LEAN_NUM_THREADS','ELAN_TOOLCHAIN','PYTHONUTF8']},lane='Exclusive serial foreground')
  with (OUT/(label+'.status.json')).open('xb') as f:f.write((json.dumps(st,indent=2)+'\n').encode())
  print(json.dumps(st),flush=True)
  if r.returncode:result=r.returncode;break
finally:
 lease=json.loads(lp.read_text());lease.update(compiler_lease='CLOSED',compiler_exit_code=result,compiler_closed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());lp.write_bytes((json.dumps(lease,indent=2)+'\n').encode())
 (OUT/'compiler.lease.closed.raw.snapshot.json').write_bytes(lp.read_bytes())
raise SystemExit(result)
