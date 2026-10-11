from pathlib import Path
import hashlib,json,subprocess,os,datetime,re
R=Path('E:/Samplinglib')
D=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/independent-fragment-math94'
S=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/ActualAnalysis94.lean'
H=R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/Header94.lean'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def write(n,b):
 p=D/n;assert not p.exists();p.write_bytes(b);return p
def js(n,j):return write(n,(json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode())
inputs=[info(p) for p in [S,H,R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/root.statement-seal94.json',R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/independent-header-math94/header-math-audit94.native.json',R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/independent-header-math94/closed-RAW-manifest94.native.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',R/'lean-toolchain',R/'lake-manifest.json',R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/checks94/actual-analysis3-explicit-api/receipt.json']]
assert inputs[1]['raw_sha256']=='283fef6c66240aec21c4f34c72442d85e25db3f95dde1104a96cb3fe7d04e832'
snapshot=write('ActualAnalysis94.exactraw.lean',S.read_bytes())
h=H.read_text(encoding='utf8')
s=S.read_text(encoding='utf8')
seal=json.loads((R/inputs[2]['path']).read_bytes())
assert h.split('noncomputable def candidate_statement',1)[1].split('\n#check',1)[0] == seal['expanded_literal_Prop']
params=h.split('noncomputable def candidate_statement\n',1)[1].split(' : Prop := by',1)[0]
body=h.split('  exact\n',1)[1].split('\n#check',1)[0]
firstthree=body.rsplit(' ∧\n      ρ ',1)[0]
expected=params+' :\n'+firstthree
actual=s.split('theorem actual_analysis\n',1)[1].split(' := by\n',1)[0]
assert actual==expected
for bad in ['sorry','admit','axiom ','native_decide','unsafe','implemented_by']:
 assert not re.search(r'\b'+re.escape(bad),s),bad
js('input-and-literal-check94.native.json',dict(status='PASS',inputs=inputs,exact_header_seal_text_match=True,exact_first_three_type_text_match=True,comparison_recipe='Python universal newline decoding only; no whitespace normalization; remove final rho conjunct from exact sealed header.',fake_closure_lexical_scan=['sorry','admit','axiom declaration','native_decide','unsafe','implemented_by'],scan_matches=[]))
witness='\nnamespace IndependentFragmentWitness94\ntheorem sealed_first_three\n'+expected+' := by\n  exact PBPSActualAnalysis94.actual_analysis hα hαβ hV hH hη hβη\n#print axioms sealed_first_three\nend IndependentFragmentWitness94\n'
w=write('SealedFirstThreeWitness94.lean',snapshot.read_bytes()+witness.encode())
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
receipts=[]
for label,p in [('fragment',snapshot),('sealed-first-three',w)]:
 cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 run=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out=write(label+'.stdout.exactraw.log',run.stdout);err=write(label+'.stderr.exactraw.log',run.stderr)
 rec=dict(command=cmd,exit_code=run.returncode,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ELAN_TOOLCHAIN_removed=True,input=info(p),stdout=info(out),stderr=info(err))
 js(label+'.receipt.native.json',rec);receipts.append(rec)
 assert run.returncode==0,run.stdout.decode(errors='replace')
 text=run.stdout.decode('utf8')
 axioms=re.findall(r"'([^']+)' depends on axioms: \[([^]]+)\]",text)
 assert len(axioms)==(5 if label=='fragment' else 6),axioms
 for decl,ax in axioms:assert set(re.split(r',\s*',ax.strip()))=={'propext','Classical.choice','Quot.sound'},(decl,ax)
 js(label+'.axioms.native.json',dict(declarations=[dict(declaration=d,axioms=re.split(r',\s*',a.strip())) for d,a in axioms]))
js('fresh-checks94.native.json',dict(status='PASS',checked_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),mathlib_commit=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=R).decode().strip(),source=inputs[0],checks=receipts))
print(json.dumps(dict(status='PASS',source=inputs[0],checks=[r['exit_code'] for r in receipts]),indent=2))
