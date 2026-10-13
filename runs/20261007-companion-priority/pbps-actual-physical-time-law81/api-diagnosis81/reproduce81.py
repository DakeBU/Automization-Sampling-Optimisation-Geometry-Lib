from pathlib import Path
import hashlib,json,subprocess,datetime,os
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-law81';O=B/'api-diagnosis81';SRC=B/'focused81-attempt3/source.snapshot.lean';s=SRC.read_text(encoding='utf-8')
def raw(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def save(n,d):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(d,f,ensure_ascii=False,indent=2);f.write('\n')
start=s.index('theorem ideal_half_turn_returned_position_kernel')
binder=s[s.index('    {E : Type*}',start):s.index(' :\n    ideal_half_turn',start)]
letstart=s.index('    let P')
letblock=s[letstart:s.index('    ∃ Z',letstart)]
prefix=s[:start]+'private theorem api_wait_composition\n'+binder+' :\n'+letblock+'''    ∀ y x : E, ∀ n : ℕ,
      Measurable (fun w : (E × E) × (ℕ → ℝ) =>
        τ y w.1.1
          ((record y w.1.1 (x, w.1.2) (ε w.2) n).elim id (fun _ => (0, (0, 0)))).2
          (ε w.2 n)) := by
'''
body=s[s.index('  classical',start):s.index('  have hgood (y x : E)',start)]
inner=s[s.index('    letI : IsProbabilityMeasure (q y)',s.index('  have hgood')):s.index('    have hbranchM',s.index('  have hgood'))]
inner='\n'.join(v[2:] if v.startswith('  ') else v for v in inner.rstrip().splitlines())+'\n'
tail='''  change Measurable (fun w : W => τ y w.1.1 (L n w).2 (ε w.2 n))
  exact hwaitM n
end
end AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel
'''
direct=prefix+body+'  intro y x n\n'+inner+tail
inferred=direct.replace('    exact hτM.comp haM','    have hcomp := hτM.comp haM\n    exact hcomp')
assert direct!=inferred
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
for name,text in [('api-reproducer.direct',direct),('api-reproducer.inferred',inferred)]:
 path=O/(name+'.lean')
 with path.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
 cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env',str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe'),str(path)]
 starttime=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(name+'.stdout.log')).open('xb') as out,(O/(name+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(cmd,cwd=R,env=env,stdout=out,stderr=err);print(name,'foreground PID',child.pid,flush=True);code=child.wait()
 save(name+'.receipt.json',dict(command_argv=cmd,cwd=str(R),actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=starttime,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),input=raw(path),stdout=raw(O/(name+'.stdout.log')),stderr=raw(O/(name+'.stderr.log')),scope='Strictly smaller actual tau composition API goal; retains original local actual definitions and prior kernel context, excludes downstream consumer proof.'))
 print(name,'EXIT',code,flush=True)
