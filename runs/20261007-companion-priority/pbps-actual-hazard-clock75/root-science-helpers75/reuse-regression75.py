from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-hazard-clock75');r72=r.parent/'pbps-b4-corrector-perturbation72'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
old='bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19'
paths=['tools','website/scripts','website/static','.github/workflows','lean-toolchain','lake-manifest.json']
assert not subprocess.check_output(['git','diff',old,'--name-only','--',*paths],text=True).strip()
assert not subprocess.check_output(['git','ls-files','--others','--exclude-standard','--',*paths],text=True).strip()
packet=load(r72/'final-reader-repository-packet72.json');records=[]
for label in ['python-regression-suite','browser-full-current']:
 d=r72/'integration72'/label;q=load(d/'receipt.json');assert q['terminal_closed'] and q['exit_code']==0
 for name in ['receipt.json','stdout.log','stderr.log']:
  p=(d/name).resolve();z=next(x for x in packet['inputs'] if Path(x['path']).resolve()==p);assert sha(p.read_bytes())==z['RAW_sha256']
 records.append(dict(label=label,receipt=pin(d/'receipt.json'),stdout=pin(d/'stdout.log'),stderr=pin(d/'stderr.log'),fresh_for75=False))
earliest=min(datetime.datetime.fromisoformat(load(r72/'integration72'/x/'receipt.json')['started_utc']).timestamp() for x in ['python-regression-suite','browser-full-current'])
runtime=[]
for name in [sys.executable,'C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe','C:/Program Files/Google/Chrome/Application/chrome.exe']:
 p=Path(name);assert p.stat().st_mtime<earliest;runtime.append(dict(current_pin=pin(p),mtime_predates_reused_runs=True,historical_RAW_hash_not_recorded=True))
out=r/'integration75/unchanged-regression-reuse.json';assert not out.exists()
out.write_text(json.dumps(dict(status='REUSED_PRIOR_COMPLETE_REGRESSIONS_CURRENT_SCOPED_BROWSER_REQUIRED',actual_root_PID=os.getpid(),source_baseline=old,reused_exact_unchanged_helpers_with_runtime_continuity_evidence=True,helper_regions=paths,unchanged_Git_and_workspace=True,records=records,current_runtime_pins=runtime,runtime_qualification='Same executable paths; current executable last-write times predate prior tests. Historical executable RAW hashes were not recorded, so no historical RAW-byte identity claim.',fresh_full_suite_or_full_browser_for75=False,current_target_render_copy_download_required=True,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS75 unchanged test/helper regions; reused72 complete regressions with explicit runtime qualification; fresh scoped75 browser still required.')
