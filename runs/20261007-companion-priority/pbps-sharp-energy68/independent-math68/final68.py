import sys,os,json,hashlib,re,subprocess,datetime,traceback,time
from pathlib import Path
import review68 as R
ROOT=R.ROOT;P=R.P;O=R.O;PRE=R.PRE;BASE=R.BASE;ACTOR=R.ACTOR
now=R.now;sha=R.sha;pin=R.pin;save=R.save;read=R.read;get=R.get
MAIN=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean'
TEST=ROOT/'Tests/ProximalBPSSharpCorrectorEnergy.lean'
NAMES={'main':'AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound','test':'Tests.ProximalBPSSharpCorrectorEnergy.genuine_actual_modified_energy_equivalence'}
def frozen(path):
 rows=get('final.inputs.manifest.json')['inputs'];q=next(x for x in rows if x['original']['path']==Path(path).as_posix());return Path(q['RAW_snapshot']['path'])
def stable():
 R.leafpins()
 resolved={x['canonical_path']:x for x in get('finite-input-resolution.json')['rows']} if (O/'finite-input-resolution.json').exists() else {}
 for q in get('final.inputs.manifest.json')['inputs']:
  if q['original']['path'] in resolved:
   d=resolved[q['original']['path']];assert d['original_frozen_input']==q['original'] and pin(d['explicit_before_snapshot']['path'])==d['explicit_before_snapshot'] and pin(d['explicit_after_snapshot']['path'])==d['explicit_after_snapshot'] and pin(q['original']['path'])==d['current_observed']
  else:assert pin(q['original']['path'])==q['original'],('final current input drift; explicit finite resolution required',q['original']['path'])
  assert pin(q['RAW_snapshot']['path'])==q['RAW_snapshot'] and pin(q['LF_snapshot']['path'])==q['LF_snapshot']
def freeze_final():
 R.leafpins();assert not (O/'lease.final.json').exists()
 f=read(P/'math-freeze.json');assert f['checked_base_commit']==BASE
 rows=[]
 for i,p in enumerate([P/'math-freeze.json']+[Path(q['path']) for q in f['inputs']]):
  b=p.read_bytes();pr=pin(p)
  if i:
   expected=f['inputs'][i-1];assert pr['raw_bytes']==expected['raw_bytes'] and pr['raw_sha256']==expected['raw_sha256'] and pr['lf_sha256']==expected['lf_sha256'],('root freeze mismatch',p.as_posix())
  rp=O/f'final-inputs/{i:03}.RAW.snapshot';lp=O/f'final-inputs/{i:03}.LF.snapshot';rp.parent.mkdir(exist_ok=True);rp.write_bytes(b);lp.write_bytes(b.replace(b'\r\n',b'\n'));rows.append(dict(original=pr,RAW_snapshot=pin(rp),LF_snapshot=pin(lp)))
 save('final.inputs.manifest.json',dict(status='PINNED_BEFORE_WHOLE_MODULE_REVIEW_AND_FRESH_COMPILERS',actual_PID=os.getpid(),utc=now(),checked_base=BASE,input_count=len(rows),inputs=rows,finite_historical_maps=[],decoder_source_verdicts_consumed=False,current_final_candidates_uncommitted=True))
 stable();print(json.dumps(dict(status='PINNED_FINAL_INPUTS',actual_PID=os.getpid(),input_count=len(rows))))
def compile_one(which):
 stable();path={'main':MAIN,'test':TEST}[which];cmd=['lake','env','lean',path.relative_to(ROOT).as_posix()]
 with (O/f'{which}.compiler.stdout.log').open('wb') as out,(O/f'{which}.compiler.stderr.log').open('wb') as err:
  start=now();p=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(event='FRESH_COMPILER_START',target=which,actual_foreground_lake_PID=p.pid)),flush=True)
  try:
   time.sleep(1)
   query=f"Get-CimInstance Win32_Process -Filter 'ParentProcessId = {p.pid}' | Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress"
   c=subprocess.run(['powershell','-NoProfile','-Command',query],capture_output=True,cwd=ROOT);(O/f'{which}.process-child.stdout.log').write_bytes(c.stdout);(O/f'{which}.process-child.stderr.log').write_bytes(c.stderr)
   proc=json.loads(c.stdout.decode('utf-8-sig')) if c.stdout.strip() else []
  except Exception as e:proc=dict(observer_error=repr(e))
  code=p.wait()
 txt=(O/f'{which}.compiler.stdout.log').read_text(encoding='utf-8')+(O/f'{which}.compiler.stderr.log').read_text(encoding='utf-8')
 receipt=dict(command=cmd,actual_parent_PID=os.getpid(),actual_foreground_lake_PID=p.pid,observed_child_processes=proc,started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,fresh_Lean=True,cache_replay_only=False,olean_output_requested=False,stdout=pin(O/f'{which}.compiler.stdout.log'),stderr=pin(O/f'{which}.compiler.stderr.log'))
 save(f'{which}.compiler.receipt.json',receipt)
 assert code==0 and not re.search(r': error:|error\(|sorryAx',txt)
 matches=re.findall(re.escape(NAMES[which])+r"' depends on axioms:\s*\[([^\]]+)\]",txt);assert len(matches)==1,('axiom prints',matches)
 ax=[x.strip() for x in matches[0].split(',')];assert len(ax)==3 and set(ax)=={'propext','Classical.choice','Quot.sound'}
 stable();save(f'{which}.compiler.result.json',dict(status='PASS',actual_PID=os.getpid(),receipt=receipt,exact_standard3=ax,pre_post_RAW_LF_unchanged=True,diagnostic_warnings=[x for x in txt.splitlines() if ': warning:' in x]))
 print(json.dumps(dict(status='PASS',target=which,actual_foreground_lake_PID=p.pid,axioms=ax)))
if __name__=='__main__':
 mode=sys.argv[1]
 try:
  if mode=='freeze-final':freeze_final()
  elif mode.startswith('compile-'):compile_one(mode[8:])
  else:raise ValueError(mode)
 except Exception as e:
  if not (O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else mode)+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),mode=mode,error=repr(e),traceback=traceback.format_exc()))
  raise
