from pathlib import Path
import hashlib,json,subprocess,datetime,os
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/pbps-actual-physical-time-law81/api-diagnosis81'
def raw(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
change='''  change ∀ y x : E, ∀ n : ℕ,
    Measurable (fun w : W => τ y w.1.1
      ((record y w.1.1 (x, w.1.2) (ε w.2) n).elim id (fun _ => (0, (0, 0)))).2
      (ε w.2 n))
'''
save('probe-extraction-diagnosis81.json',dict(status='IMPLEMENTATION_DIAGNOSTIC_FIXED',cause='The reduced API statement begins with fifteen local let bindings. Direct intro y x n introduced those let-bound objects instead of the intended E/E/Nat forall binders, producing y:Measure and cascading type errors. This is a diagnostic extraction error, not source mathematics or evidence that the composition is ill-typed.',repair='Explicit change to the same closed forall API proposition using the already established body local definitions, before intro. Preserve both original negative probe files/logs/receipts.'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
for variant in ['inferred','direct']:
 old=O/('api-reproducer.'+variant+'.lean');s=old.read_text(encoding='utf-8');assert s.count('  intro y x n\n')==1
 path=O/('api-reproducer.'+variant+'.closed-lets.lean')
 with path.open('x',encoding='utf-8',newline='\n') as f:f.write(s.replace('  intro y x n\n',change+'  intro y x n\n'))
 name='api-reproducer.'+variant+'.closed-lets';cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(path)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(name+'.stdout.log')).open('xb') as out,(O/(name+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(name,'foreground PID',child.pid,flush=True);code=child.wait()
 save(name+'.receipt.json',dict(command_argv=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),input=raw(path),stdout=raw(O/(name+'.stdout.log')),stderr=raw(O/(name+'.stderr.log')),scope='Strictly smaller API target; fifteen let binders explicitly exposed before forall intro, original actual definitions/parent context preserved, unchanged1600000HB.'))
 print(name,'EXIT',code,flush=True)
