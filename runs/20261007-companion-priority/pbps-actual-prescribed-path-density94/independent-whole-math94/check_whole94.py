from pathlib import Path
import hashlib,json,subprocess,os,datetime,re
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94';D=B/'independent-whole-math94'
S=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean'
P=R/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def write(n,b):
 p=D/n;assert not p.exists(),str(p);p.write_bytes(b);return p
def js(n,j):return write(n,(json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode())
paths=[S,P/'Header94.lean',P/'root.statement-seal94.json',P/'independent-header-math94/header-math-audit94.native.json',P/'independent-header-math94/closed-RAW-manifest94.native.json',B/'independent-fragment-math94/ActualAnalysis94.exactraw.lean',B/'independent-fragment-math94/fragment-math-decision94.native.json',B/'independent-fragment-math94/closed-RAW-fragment94.native.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',R/'lean-toolchain',R/'lake-manifest.json']
inputs=[info(p) for p in paths]
assert inputs[1]['raw_sha256']=='283fef6c66240aec21c4f34c72442d85e25db3f95dde1104a96cb3fe7d04e832'
assert inputs[5]['raw_sha256']=='ff2a0d8881e34e3ff9d7f9c8397a4cf4e7fa8f915f988e955e0f6f5e65ced18f'
snapshot=write('ActualPrescribedPathDensity.exactraw.lean',S.read_bytes())
s=S.read_text(encoding='utf8');h=(P/'Header94.lean').read_text(encoding='utf8');fragment=paths[5].read_text(encoding='utf8')
seal=json.loads((P/'root.statement-seal94.json').read_bytes())
assert h.split('noncomputable def candidate_statement',1)[1].split('\n#check',1)[0]==seal['expanded_literal_Prop']
params=h.split('noncomputable def candidate_statement\n',1)[1].split(' : Prop := by',1)[0]
body=h.split('  exact\n',1)[1].split('\n#check',1)[0].rstrip()
expected=params+' :\n'+body
actual=s.split('theorem actual_prescribed_path_density_rewrite\n',1)[1].split(' := by\n',1)[0]
assert actual==expected
names=['arc_integral','incoming_left_limit','finite_arc_integral','actual_arc','actual_analysis']
def extract(text,name):
 start=re.search(r'^(?:private )?theorem '+name+r'\b',text,re.M).start()
 part=text[start:]
 stop=re.search(r'\n(?:/--|open |(?:private )?theorem |#print |end |namespace )',part)
 if stop:part=part[:stop.start()]
 return part.rstrip()
def normalize(t):
 for prefix in ['PBPSFiniteArcAnalysis94.','PBPSActualArc94.','PBPSActualAnalysis94.']:t=t.replace(prefix,'')
 return t.removeprefix('private ')
transfer=[]
for name in names:
 old,new=extract(fragment,name),extract(s,name)
 assert normalize(old)==normalize(new),name
 transfer.append(dict(name=name,comparison='Literal text after newline decoding, removal of declaration-private keyword, and removal of the three scratch namespace qualifiers only.',equivalent=True,old_text_sha256=hashlib.sha256(old.encode()).hexdigest(),new_text_sha256=hashlib.sha256(new.encode()).hexdigest()))
decls=re.findall(r'^(private )?theorem (\w+)',s,re.M)
assert len(decls)==7 and sum(bool(p) for p,n in decls)==6
for bad in [r'\bsorry\b',r'\badmit\b',r'^\s*axiom\b',r'\bnative_decide\b',r'\bunsafe\b',r'\bimplemented_by\b',r'Prop\s*:=\s*True',r':=\s*trivial']:
 assert not re.search(bad,s,re.M),bad
js('literal-transfer94.native.json',dict(status='PASS',inputs=inputs,exact_full_seal_type_match=True,header_comparison='Python universal newline decoding only; exact params and let-expanded body from original Header94.',fragment_transfer=transfer,declarations=[dict(private=bool(p),name=n) for p,n in decls],fake_closure_scan='PASS; no forbidden closure constructs found'))
namespace='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity'
extra='\nnamespace '+namespace+'\n'+'\n'.join('#print axioms '+n for n in names+['product_survival'])+'\nend '+namespace+'\n'
witness='\nnamespace IndependentWholeWitness94\ntheorem exact_sealed_whole\n'+expected+' := by\n  exact '+namespace+'.actual_prescribed_path_density_rewrite hα hαβ hV hH hη hβη\n#print axioms exact_sealed_whole\nend IndependentWholeWitness94\n'
w=write('ExactSealedWholeWitness94.lean',snapshot.read_bytes()+extra.encode()+witness.encode())
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);receipts=[]
for label,p in [('production',snapshot),('sealed-whole',w)]:
 cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p)]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 run=subprocess.run(cmd,cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 out=write(label+'.stdout.exactraw.log',run.stdout);err=write(label+'.stderr.exactraw.log',run.stderr)
 rec=dict(command=cmd,exit_code=run.returncode,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),ELAN_TOOLCHAIN_removed=True,input=info(p),stdout=info(out),stderr=info(err))
 js(label+'.receipt.native.json',rec);receipts.append(rec)
 assert run.returncode==0,run.stdout.decode(errors='replace')
 axioms=re.findall(r"'([^']+)' depends on axioms: \[([^]]+)\]",run.stdout.decode('utf8'))
 assert len(axioms)==(1 if label=='production' else 8),axioms
 for decl,ax in axioms:assert set(re.split(r',\s*',ax.strip()))=={'propext','Classical.choice','Quot.sound'},(decl,ax)
 js(label+'.axioms.native.json',dict(declarations=[dict(declaration=d,axioms=re.split(r',\s*',a.strip())) for d,a in axioms]))
js('fresh-checks94.native.json',dict(status='PASS',checked_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip(),mathlib_commit=subprocess.check_output(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],cwd=R).decode().strip(),source=inputs[0],checks=receipts))
print(json.dumps(dict(status='PASS',source=inputs[0],checks=[r['exit_code'] for r in receipts]),indent=2))
