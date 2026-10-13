from pathlib import Path
import json,hashlib,subprocess,os,sys,time,re,gzip,functools
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-centered-root64';OUT=BASE/'repository-exposition64';INT=BASE/'integration64';ACTOR='/root/exact_science63';COMMIT='0aef19ca2711159eeaec86d42c9be142a94fa402';SCI='59fff63d320aa5e3dc4b45e81e40e2029ce42734';PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
LABELS=['mandatory-astis-check-final','python-regression-suite','python-compile','contributor-final-admin','publication-final-admin','semantic-v2','frontier-final-admin','website-ci-build','official-graph-ci-output','cell-graph-check-actual','cell-graph-check-shared','local-site-check','reader-cdp-capture','reader-copy-download','frontier','semantic']
SCIENCE=['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareOrder.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean','Tests/ProximalBPSCenteredRootOrderInverse.lean'];ROOTS=['AutoSamplingTheory/ExampleCases.lean','AutoSamplingTheory/TechnicalLemmas.lean','AutoSamplingTheory/TechnicalLemmas/Registry.lean','Tests.lean','Tests/Basic.lean'];GRAPHS=['docs/assets/astis_lean_arsenal_module_graph.svg','docs/module-graph.svg','research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json','research-wiki/sampling-sde-library/lean-leaf-module-graph.md'];CARDS=['research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.md']
def sha(b):return hashlib.sha256(b).hexdigest()
def compact(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(Path(p).read_bytes().decode('utf-8-sig'))
def write(n,v):p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode());return p
def pth(s):p=Path(str(s).replace('\\','/'));return p if p.is_absolute() else ROOT/p
def pin(p):p=pth(p);b=p.read_bytes();return {'path':p.as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def validate(x,p=None):
 p=pth(p or x['path']);b=p.read_bytes();assert sha(b)==x['raw_sha256'],str(p)
 if 'lf_sha256'in x:assert sha(b.replace(b'\r\n',b'\n'))==x['lf_sha256']
 for k in ['bytes','raw_bytes']:
  if k in x:assert len(b)==x[k]
 return b
@functools.lru_cache(maxsize=None)
def blob(c,p):return subprocess.check_output(['git','show',c+':'+p],cwd=ROOT,stderr=subprocess.DEVNULL)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT).decode().strip()
def freeze():
 assert not (OUT/'lease.json').exists();assert git('rev-parse',COMMIT+'^')==SCI
 files={ROOT/p for p in SCIENCE+ROOTS+GRAPHS+CARDS+['lean-toolchain','lake-manifest.json']}
 for slug in ['real-l2-positive-square-order','pbps-centered-root-order-inverse']:
  for category in ['publications','declaration_lessons']:files.add(ROOT/f'website/content/{category}/{slug}.json')
 for name in ['integration.notes.json','visual.inspection.json','root.exact-verification64.adoption.json','verified.json','exact-science-verification/run.json','exact-science-verification/lease.json','exact-science-verification/named-verification.payload.json']:files.add(BASE/name)
 for label in LABELS:
  receipt=INT/label/'receipt.json';files.add(receipt);r=load(receipt)
  for k in ['stdout','stderr']:files.add(pth(r[k]['path']))
 for n in ['newline-preservation.json','generated-card-cache64.json','staging-whitespace/diagnosis.json','generated-context-preservation-data/manifest.json','owned-before.json','cell.0.before-final-admin.exactraw.snapshot.json','cell.1.before-final-admin.exactraw.snapshot.json']:files.add(INT/n)
 for p in (INT/'visual64').iterdir():
  if p.is_file():files.add(p)
 for x in load(INT/'owned-before.json')['owned']:files.add(ROOT/x['exact_snapshot'])
 rows=[]
 for p in sorted(files):
  assert p.stat().st_size<10_000_000,p
  rel=p.relative_to(ROOT).as_posix();b=blob(COMMIT,rel);w=p.read_bytes();assert b.replace(b'\r\n',b'\n')==w.replace(b'\r\n',b'\n'),rel
  rows.append(dict(pin(p),committed_RAW_sha256=sha(b),Git_vs_working_RAW_equal=b==w,Git_vs_working_LF_equal=True))
 write('lease.json',{'status':'OPEN','actor':ACTOR,'checked_commit':COMMIT,'science_parent':SCI,'actual_freeze_pid':os.getpid(),'allowed_writes':'Only this new review prefix; no canonical/Git/ledger/source/math writes or VERIFIED transition.','unrelated65_tail':'Excluded from exact64 judgment; no whole ledger copy or whole historical recursive snapshots.'})
 write('input.manifest.json',{'checked_commit':COMMIT,'science_parent':SCI,'actual_freeze_pid':os.getpid(),'exact_inputs':rows,'storage':'Exact committed Git blobs and existing immutable native evidence; no duplicate snapshots.','push_remote_active_outputs_excluded':True,'current_HEAD_at_freeze':git('rev-parse','HEAD')});print(json.dumps({'status':'FROZEN','actual_pid':os.getpid(),'inputs':len(rows),'checked_commit':COMMIT}))
if __name__=='__main__':freeze()
