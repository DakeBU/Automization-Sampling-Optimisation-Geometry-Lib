import pathlib,hashlib,json,re,os,subprocess,time,datetime
ROOT=pathlib.Path('E:/Samplinglib');OUT=pathlib.Path(__file__).resolve().parent
MODULE='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedPathExpansion.lean'
PRE='runs/20261007-companion-priority/pbps-bounded-path-expansion-preread95'
LAKE=ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'
inputs=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 p=ROOT/p;b=p.read_bytes();inputs.append({'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)});return b
def text(b):return b.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n')
def save(p,x):(OUT/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
module=read(MODULE);header=read(PRE+'/Header95.lean');seal=json.loads(read(PRE+'/root.statement-seal95.json'))
assert sha(module)=='c3d4bcf73990d704244225ea647f44ed21fcbd339db49bf2c45f21af5b90d689'
assert sha(header)=='2a9d3052c353ab8aab448de05a05beeadab320def15ee31b1d353abbb063d002'
(OUT/'module.exactraw.snapshot').write_bytes(module);(OUT/'header.exactraw.snapshot').write_bytes(header)
mt=text(module);ht=text(header)
prop=mt.split('private noncomputable def actual_bounded_path_statement',1)[1].split('/-- Full bounded',1)[0].strip()
hprop=ht.split('noncomputable def candidate_statement',1)[1].split('#check',1)[0].strip()
assert prop==hprop and prop==seal['expanded_literal_Prop'].strip()
binders=hprop.split(' : Prop := by',1)[0]
combined=mt+'\n'+ '\n'.join(line for line in ht.splitlines() if not line.startswith('import '))+'\nnamespace PBPSBoundedPathExpansionCandidate95\ntheorem independent_exact_sealed_witness'+binders+' : candidate_statement hα hαβ hV hH hη hβη := by\n  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion.actual_bounded_path_functional_expansion hα hαβ hV hH hη hβη\n#print axioms independent_exact_sealed_witness\nend PBPSBoundedPathExpansionCandidate95\n'
(OUT/'ExactSealedWitness95.lean').write_text(combined,encoding='utf-8',newline='\n')
for p in ['lean-toolchain','lake-manifest.json',PRE+'/independent-header-math95/decision.native.json','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean','AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Set.lean','.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean']:
 read(p)
save('inputs.native.json',inputs)
save('statement-equality.native.json',{'exact_literal_equal':True,'seal_literal_equal':True,'header_raw_sha256':sha(header),'module_raw_sha256':sha(module),'method':'Literal comparison after line-ending normalization; no other whitespace normalization. Fresh combined file includes full exact production text, independent sealed Header definition and a kernel witness of Header from production theorem.'})
save('initial-shell-trial.native.json',{'status':'parse-error-no-execution','reason':'PowerShell rejected shell brace path {Set,Basic}.lean; corrected by searching Bochner directory. No proof trial failed.'})
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
for label,path in [('fresh-production',ROOT/MODULE),('fresh-combined-sealed-witness',OUT/'ExactSealedWitness95.lean')]:
 argv=[str(LAKE),'env','lean',str(path.relative_to(ROOT))];start=time.time()
 with (OUT/(label+'.stdout.log')).open('wb') as stdout,(OUT/(label+'.stderr.log')).open('wb') as stderr:
  proc=subprocess.run(argv,cwd=ROOT,env=env,stdout=stdout,stderr=stderr)
 receipt={'argv':argv,'exit_code':proc.returncode,'seconds':time.time()-start,'ELAN_TOOLCHAIN_removed':True,'module_raw_sha256':sha(module),'terminal_closed':True}
 save(label+'.receipt.native.json',receipt);print(label,proc.returncode,flush=True)
 if proc.returncode:break
assert (ROOT/MODULE).read_bytes()==module
