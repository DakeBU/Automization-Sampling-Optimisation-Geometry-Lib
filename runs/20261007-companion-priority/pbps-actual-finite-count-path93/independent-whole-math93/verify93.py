import os, pathlib, hashlib, json, subprocess, time, re
ROOT=pathlib.Path('E:/Samplinglib')
OUT=pathlib.Path(__file__).parent
PROD=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
HEAD=ROOT/'runs/20261007-companion-priority/pbps-finite-count-path-preread93/Header93.lean'
def digest(p):
 b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':hashlib.sha256(b).hexdigest()}
def save(name,x): (OUT/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert digest(PROD)['raw_sha256']=='4926508e4b11b3d4823056e1068f601d4a95b6a5e1ec495b7902cc3c4a1d2943'
assert digest(HEAD)['raw_sha256']=='90bca17fbb11d9a8fea226bd0dca6494ef9a61f3db31beaf52c0ef2999cf9cfe'
p=PROD.read_text(encoding='utf-8'); h=HEAD.read_text(encoding='utf-8')
decl=h.split('def candidate_finite_count_path_statement',1)[1].split('\n#check',1)[0].rstrip()
actual=p.split('private def actual_finite_count_path_statement',1)[1].split('/-- Exact sealed',1)[0].rstrip()
assert decl==actual
inputs=[]
pending=[PROD,HEAD,ROOT/'lean-toolchain',ROOT/'lake-manifest.json',ROOT/'AGENTS.md',ROOT/'docs/theorem-publication-protocol.md',ROOT/'docs/proof-digestion-protocol.md',ROOT/'docs/evidence-routed-memory-protocol.md',ROOT/'docs/companion-papers-handoff.md',ROOT/'runs/20261007-companion-priority/pbps-actual-finite-count-path93/root.statement-seal93.json']
seen=set()
while pending:
 f=pending.pop()
 if f in seen: continue
 seen.add(f); inputs.append(digest(f))
 if f.suffix=='.lean':
  for imp in re.findall(r'^import\s+(AutoSamplingTheory[\w.]*)',f.read_text(encoding='utf-8'),re.M):
   pending.append(ROOT/(imp.replace('.','/')+'.lean'))
snap=OUT/'inputs';snap.mkdir(exist_ok=True)
for i,x in enumerate(inputs):
 f=ROOT/x['path']; target=snap/f'{i:03d}.{f.name}.RAW';target.write_bytes(f.read_bytes());x['snapshot']=target.relative_to(ROOT).as_posix()
save('input-manifest93.native.json',{'inputs':inputs,'literal_header_equal':True,'baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()})
body=h[h.index('namespace Candidate93'):]
binder=decl.split(' : Prop := by',1)[0]
witness=p+'\n'+body+'\nnamespace IndependentWholeMath93\nopen InnerProductSpace MeasureTheory ProbabilityTheory Filter\nopen scoped ContDiff NNReal ENNReal Topology Interval BigOperators\nnoncomputable section\nset_option autoImplicit false\n'
witness+='theorem sealed_header_witness'+binder+' : Candidate93.candidate_finite_count_path_statement hα hαβ hV hH hη hβη := by\n  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law hα hαβ hV hH hη hβη\n'
witness+='#check @AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law\n#print Candidate93.candidate_finite_count_path_statement\n#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law\n#print axioms sealed_header_witness\nend\nend IndependentWholeMath93\n'
(OUT/'WholeKernelWitness93.lean').write_text(witness,encoding='utf-8')
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
lake=str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe')
checks=[]
for name,src in [('fresh-production',PROD),('fresh-sealed-witness',OUT/'WholeKernelWitness93.lean')]:
 start=time.time();cmd=[lake,'env','lean',str(src)]
 with (OUT/(name+'.stdout.log')).open('wb') as stdout,(OUT/(name+'.stderr.log')).open('wb') as stderr:
  r=subprocess.run(cmd,cwd=ROOT,env=env,stdout=stdout,stderr=stderr)
 checks.append({'name':name,'command':cmd,'exit_code':r.returncode,'elapsed_seconds':time.time()-start,'source':digest(src),'ELAN_TOOLCHAIN_removed':True})
 save('kernel-receipt93.native.json',{'checks':checks})
 print(name,r.returncode,flush=True)
save('input-rehash93.native.json',{'all_unchanged':all(digest(ROOT/x['path'])['raw_sha256']==x['raw_sha256'] for x in inputs),'checked':len(inputs)})
