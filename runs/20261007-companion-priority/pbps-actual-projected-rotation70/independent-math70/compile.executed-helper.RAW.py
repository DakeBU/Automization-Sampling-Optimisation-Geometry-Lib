import os,sys,json,hashlib,datetime,re,traceback,subprocess
from pathlib import Path
ROOT=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;RUN=O.parent;PRE=ROOT/'runs/20261007-companion-priority/pbps-actual-projected-rotation-preproof70';SOURCE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean';ACTOR='/root/exact_science63';BASE='aa9dd2cf691489535aa8039850c2ee0bcdacdfb4';CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
def get(n):return read(O/n)
def save(n,v):
 assert not(O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(lf),lf_sha256=sha(lf))
def checkpin(q):assert pin(q['path'])==q,('RAW/LF mismatch',q['path'])
def logical(d):return sha(json.dumps({k:v for k,v in d.items() if k!='run_sha256'},sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def githead():return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
def stable():
 assert githead()==BASE
 for q in get('inputs.manifest.json')['inputs']:
  checkpin(q['RAW_snapshot']);checkpin(q['LF_snapshot'])
  if q['original']['path']!=CELL.as_posix():checkpin(q['original'])
 # Exactly this one cell is historical frozen metadata, as explicitly authorized by parent.
 # No other current input is excluded, and no fallback snapshot is selected adaptively.
def freeze():
 save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),utc=now(),owned_scope=O.as_posix(),scope='Independent theorem-only70 full mathematics review of exact uncommitted canonical candidate on fixed BASE, fresh Lean compile, no source final verdict/SAU VERIFIED/canonical/Git/ledger edits.'))
 assert githead()==BASE;f=read(RUN/'math-freeze.theorem-only70.json');assert len(f['inputs'])==18 and f['checked_base_commit']==BASE;rows=[]
 for i,q in enumerate(f['inputs']+[dict(path=(RUN/'math-freeze.theorem-only70.json').as_posix(),**{k:v for k,v in pin(RUN/'math-freeze.theorem-only70.json').items() if k!='path'})]):
  p=Path(q['path']);current=pin(p);assert current['raw_bytes']==q['raw_bytes'] and current['raw_sha256']==q['raw_sha256'] and current['lf_sha256']==q['lf_sha256'];row=dict(original=current,root_frozen_input=i<18)
  for kind,part in [('RAW',p.read_bytes()),('LF',p.read_bytes().replace(b'\r\n',b'\n'))]:
   dest=O/f'inputs/{i:02}.{kind}.snapshot';dest.parent.mkdir(exist_ok=True);dest.write_bytes(part);row[kind+'_snapshot']=pin(dest)
  row['authority']='Fixed original cell snapshot only: root may later make metadata publication overlays; no current-cell equality after pin is presumed.' if p==CELL else 'Exact current immutable theorem mathematics input, RAW/LF both frozen; must remain equal.'
  rows.append(row)
 tracked=subprocess.run(['git','ls-files','--stage','--',SOURCE.relative_to(ROOT).as_posix()],cwd=ROOT,capture_output=True);save('git.baseline.json',dict(checked_base_commit=BASE,actual_PID=os.getpid(),utc=now(),source=pin(SOURCE),git_ls_files_exit=tracked.returncode,git_ls_files_stdout=tracked.stdout.decode(),source_is_BASE_commit_review=False,limitation='This is current local theorem review on BASE, not exact SCI70 commit verification. No70 science commit is asserted.'))
 save('inputs.manifest.json',dict(root_frozen_input_count=18,input_count=len(rows),inputs=rows,LF_recipe='Replace ONLY CRLF with LF; preserve bare CR, UTF8 and all other bytes. RAW authoritative.',explicit_frozen_metadata_rows=[dict(path=CELL.as_posix(),row_index=17,snapshot=rows[17]['RAW_snapshot'],qualification='Fixed frozen cell input; later publication/process metadata is outside theorem proof review, not silently current.')],checked_base_commit=BASE,source_uncommitted_review=True,whole_ledger_copy=False))
 print(json.dumps(dict(status='PIN_COMPLETE',actual_PID=os.getpid(),root_frozen_input_count=18,input_count=len(rows),HEAD=BASE,source_RAW=pin(SOURCE)['raw_sha256'],frozen_cell_RAW=pin(CELL)['raw_sha256'])))
def compile():
 stable();pre=[q['original'] for q in get('inputs.manifest.json')['inputs'] if q['original']['path']!=CELL.as_posix()];cmd=['lake','env','lean',SOURCE.relative_to(ROOT).as_posix()];start=now()
 with (O/'compiler.stdout.log').open('wb') as out,(O/'compiler.stderr.log').open('wb') as err:
  p=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(event='FRESH_LEAN_START',actual_foreground_Lake_PID=p.pid,actual_parent_PID=os.getpid(),command=cmd)),flush=True);code=p.wait()
 stable();stdout=(O/'compiler.stdout.log').read_text(encoding='utf-8');m=re.findall(r"'AutoSamplingTheory\.ExampleCases\.ProximalBPS\.ActualProjectedRotation\.actual_projected_rotation' depends on axioms: \[([^\]]+)\]",stdout);axioms=[s.strip() for s in m[-1].split(',')] if m else [];record=dict(command=cmd,actual_foreground_Lake_PID=p.pid,actual_parent_PID=os.getpid(),started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,checked_base_commit=BASE,source_pre=pre[0],source_post=pin(SOURCE),pre_pins=pre,post_pins=[pin(q['path']) for q in pre],stdout=pin(O/'compiler.stdout.log'),stderr=pin(O/'compiler.stderr.log'),fresh_main_Lean_elaboration=True,dependency_oleans_reused=True,output_olean_requested=False,Lake_build_cache_replay=False,axioms=axioms,exact_standard3=axioms==['propext','Classical.choice','Quot.sound'],error_lines=[x for x in stdout.splitlines() if ': error:' in x],failed_no_axioms_output_credit=False)
 save('compiler.receipt.json',record);assert code==0 and record['exact_standard3'] and not record['error_lines'];print(json.dumps(dict(status='FRESH_LEAN_PASS_STANDARD3',actual_foreground_Lake_PID=p.pid,exit_code=code,axioms=axioms)))

if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
