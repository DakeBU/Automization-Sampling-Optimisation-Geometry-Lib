from pathlib import Path
import json,hashlib,subprocess,os,datetime,re
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/independent-whole-math94'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def write(n,b):
 p=D/n;assert not p.exists();p.write_bytes(b);return p
def js(n,j):return write(n,(json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode())
old=(D/'ExactSealedWholeWitness94.lean').read_bytes()
marker=b'namespace IndependentWholeWitness94'
assert old.count(marker)==1
new=old.replace(marker,b'open MeasureTheory Set Filter\nopen scoped NNReal ENNReal Topology Classical\n'+marker)
w=write('ExactSealedWholeWitness94.trial2.lean',new)
js('trial1-witness-failure.native.json',dict(status='FAILED_RETAINED',failure='Reviewer witness outside the production namespace omitted notation opens; parser expected token at NNReal notation. Production exact snapshot compiled EXIT0. No source/type/body change required.',repair='Only add open MeasureTheory Set Filter and scoped NNReal ENNReal Topology Classical before witness namespace in new trial2 file.',prior_receipt=info(D/'sealed-whole.receipt.native.json')))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(w)]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
r=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out=write('sealed-whole-trial2.stdout.exactraw.log',r.stdout);err=write('sealed-whole-trial2.stderr.exactraw.log',r.stderr)
rec=dict(command=cmd,exit_code=r.returncode,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ELAN_TOOLCHAIN_removed=True,input=info(w),stdout=info(out),stderr=info(err))
js('sealed-whole-trial2.receipt.native.json',rec)
assert r.returncode==0,r.stdout.decode(errors='replace')
axs=re.findall(r"'([^']+)' depends on axioms: \[([^]]+)\]",r.stdout.decode('utf8'))
assert len(axs)==8
for d,a in axs:assert set(re.split(r',\s*',a.strip()))=={'propext','Classical.choice','Quot.sound'},(d,a)
js('sealed-whole-trial2.axioms.native.json',dict(declarations=[dict(declaration=d,axioms=re.split(r',\s*',a.strip())) for d,a in axs]))
js('fresh-checks94.native.json',dict(status='PASS_WITH_RETAINED_REVIEWER_WITNESS_TRIAL',checked_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),mathlib_commit=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=R).decode().strip(),source=json.loads((D/'literal-transfer94.native.json').read_bytes())['inputs'][0],checks=[json.loads((D/'production.receipt.native.json').read_bytes()),rec]))
print(json.dumps(dict(status='PASS',witness=info(w))))
