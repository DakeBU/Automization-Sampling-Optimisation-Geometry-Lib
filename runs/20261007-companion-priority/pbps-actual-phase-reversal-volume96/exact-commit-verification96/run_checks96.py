"""Run only after root dispatch, against an explicit immutable science SHA."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time,re
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent
C=sys.argv[1];BASE='45e1f1457b59446dc4d1774cea510775c331d590'
def head():return subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()
assert re.fullmatch('[0-9a-f]{40}',C) and head()==C
F=json.loads((O/'input-freeze96.json').read_bytes());assert F['status']=='PASS' and F['verified_commit']==C
PY=[sys.executable,'-X','utf8'];LAKE=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe')
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2'
def save(p,v):
 q=O/p;assert not q.exists(),str(q);q.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
witness=B/'independent-whole-math96/FreshExactSourceAndHeader96.lean'
checks=[('focused-module',[LAKE,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume']),('current-sealed-kernel',[LAKE,'env','lean',str(witness.relative_to(R))]),('contributor',PY+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',PY+['tools/astis_publication.py','check','--base',BASE]),('semantic',PY+['tools/astis_semantic_roundtrip.py','check']),('frontier',PY+['tools/astis_frontier_cells.py','check']),('committed-diff',['git','diff','--check',BASE,C])]
receipts=[]
for name,argv in checks:
 if name in ['focused-module','current-sealed-kernel'] and (O/'metadata-transfer96.json').exists():
  transfer=json.loads((O/'metadata-transfer96.json').read_bytes());rc=json.loads((O/(name+'.receipt.json')).read_bytes())
  assert transfer['status']=='PASS' and transfer['verified_commit']==C and rc['verified_commit']==C and rc['exit_code']==0 and rc['reused_successful_execution']
  assert hashlib.sha256((O/(name+'.stdout.log')).read_bytes()).hexdigest()==rc['stdout_sha256']
  assert hashlib.sha256((O/(name+'.stderr.log')).read_bytes()).hexdigest()==rc['stderr_sha256']
  receipts.append(name+'.receipt.json');print(name,'0 (unchanged exact evidence transferred)',flush=True);continue
 assert head()==C;start=time.time()
 with (O/(name+'.stdout.log')).open('xb') as out,(O/(name+'.stderr.log')).open('xb') as err:p=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
 save(name+'.receipt.json',dict(command=argv,verified_commit=C,exit_code=p.returncode,seconds=time.time()-start,ELAN_TOOLCHAIN_removed=True,terminal_closed=True));receipts.append(name+'.receipt.json');print(name,p.returncode,flush=True)
 assert p.returncode==0,name
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
from tools import astis
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws'
pub.check_advance([D],reviewed=True);save('publication-reviewed.json',dict(status='PASS',declaration=D,verified_commit=C))
hits=astis.forbidden_pattern_hits();save('fake-closure.json',dict(status='PASS' if not hits else 'FAIL',hits=hits));assert not hits
log=(O/'current-sealed-kernel.stdout.log').read_text(encoding='utf8');assert 'sorryAx' not in log
axes=re.findall(r"depends on axioms:\s*\[([^\]]*)\]",log)
assert axes and all(set(re.findall(r'[A-Za-z][A-Za-z.]*',a))<={'propext','Classical.choice','Quot.sound'} for a in axes),axes
save('axiom-scan96.json',dict(status='PASS',axiom_lists=axes,allowed=['propext','Classical.choice','Quot.sound']))
assert head()==C
save('checks-complete96.json',dict(status='PASS',verified_commit=C,receipts=receipts,reviewed_publication=True,fake_closure_hits=0,axiom_scan='axiom-scan96.json'))
