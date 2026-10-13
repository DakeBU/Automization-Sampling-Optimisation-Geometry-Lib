from pathlib import Path
import hashlib,json,re,subprocess,os,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;P=B.parent/'pbps-endpoint-time-reversal-preread97'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualEndpointTimeReversal.lean';H=P/'Header97.lean';S=P/'root.statement-seal97.json';F=B/'focused97/production2'
raw=M.read_bytes();assert sha(raw)=='01816c27c8371ba9f81e24217ef7732b6c541066cb0b0f37e6494ffd8c58d27a'
assert (F/'input.exactraw.lean').read_bytes()==raw
rc=load(F/'receipt.json');assert rc['exit_code']==0 and rc['input_raw_sha256']==sha(raw)
prod=M.read_text(encoding='utf8');header=H.read_text(encoding='utf8');seal=load(S)
assert info(H)['raw_sha256']==seal['header']['raw_sha256']=='2f27a049026ab398bfc85cecf1b2a450e8fef17c45e3a79e8b492c731343800b'
def norm(t):
 t=re.sub(r'/\-.*?\-/','',t,flags=re.S);t=re.sub(r'^private ', '',t,flags=re.M);return re.sub(r'\s+',' ',t).strip()
def decl(t,name):
 pat=r'^(?:private )?(?:def|theorem) '+re.escape(name)+r'(?=\s|\{)';s=re.search(pat,t,re.M);assert s,name
 e=re.search(r'^(?:(?:private )?(?:def|theorem) |#print|#check|end\b|set_option )',t[s.end():],re.M)
 return t[s.start():s.end()+e.start()] if e else t[s.start():]
sig=decl(prod,'actual_endpoint_time_reversal_statement');sig=sig[sig.index('{E : Type*}'):]
hsig=decl(header,'candidate');hsig=hsig[hsig.index('{E : Type*}'):]
sig=re.sub(r'\s*/\-\- Exact source-sealed actual endpoint/time reversal law\. \-/\s*$', '', sig)
assert sig.strip()==hsig.strip()==seal['expanded_literal_Prop'].strip()
fragment_rows=[]
sets=[('simplex','Simplex97.lean',['delta','reverseTime','reverseTime_involutive','reverseTime_mem','reverseTime_measurable','reverseTime_volume','rho','rho_measurable','rho_involutive','rho_volume']),('word','Word97.lean',['reverse_fold_cancel','fold_of_sequence','gaps','gaps_reversed','post','endpoint','endpoint_as_word','endpoint_reversed','preserving_fold','endpoint_volume']),('endpoint','ActualEndpoint97.lean',['endpoint_data'])]
for kind,file,names in sets:
 t=(B/file).read_text(encoding='utf8')
 for name in names:
  a=decl(prod,name);b=decl(t,name)
  if kind=='endpoint':a=a.replace('endpoint_data_statement','statement')
  assert norm(a)==norm(b),name
  fragment_rows.append(dict(fragment=kind,declaration=name,unchanged_modulo_private_visibility_and_endpoint_Prop_rename=True))
assert norm(decl(prod,'endpoint_data_statement').replace('endpoint_data_statement','statement'))==norm(decl((B/'ActualEndpoint97.lean').read_text(encoding='utf8'),'statement'))
paths=[M,H,S,F/'input.exactraw.lean',F/'receipt.json',F/'stdout.log',F/'stderr.log',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseReversalVolume.lean',R/'lean-toolchain',R/'lake-manifest.json']
for kind,file,_ in sets:
 paths += [B/file,B/'independent-fragment-math97'/kind/(kind+'-math-decision97.native.json'),B/'independent-fragment-math97'/kind/('closed-RAW-'+kind+'97.native.json')]
paths += [R/'.lake/packages/mathlib/Mathlib'/x for x in ['MeasureTheory/Measure/Prod.lean','MeasureTheory/Measure/Restrict.lean','MeasureTheory/Measure/Typeclasses/SFinite.lean']]
snap=O/'inputs';snap.mkdir(exist_ok=False);inputs=[]
for i,p in enumerate(paths):
 q=snap/(str(i).zfill(2)+'.'+p.name+'.exactraw');q.write_bytes(p.read_bytes());inputs.append(dict(**info(p),snapshot=q.relative_to(R).as_posix()))
binders=hsig[:hsig.index(': Prop := by')].rstrip()
body='\n'.join(line for line in header.splitlines() if not line.startswith('import '))
witness='\nnamespace IndependentWholeMath97\nopen MeasureTheory InnerProductSpace\nopen scoped NNReal ENNReal Classical ContDiff\nnoncomputable section\nset_option autoImplicit false\ntheorem sealed_header_witness\n    '+binders+' : PBPSEndpointReversalCandidate97.candidate hα hαβ hV hH hη hβη := by\n  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws hα hαβ hV hH hη hβη\nend\nend IndependentWholeMath97\n#print axioms AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws\n#print axioms IndependentWholeMath97.sealed_header_witness\n'
W=O/'FreshExactProductionAndHeader97.lean';W.write_bytes(raw+b'\n'+body.encode()+witness.encode());assert W.read_bytes().startswith(raw)
write('prepared-inputs97.native.json',dict(production=info(M),header=info(H),statement_seal=info(S),inputs=inputs,literal_statement_matches_exactly=True,unchanged_reviewed_fragment_declarations=fragment_rows,endpoint_private_statement_matches=True,kernel_input=info(W),full_exact_production_prefix=True,target_production_not_imported=True))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(W.relative_to(R))]
start=datetime.datetime.now(datetime.timezone.utc)
with (O/'fresh-kernel.stdout.log').open('xb') as out,(O/'fresh-kernel.stderr.log').open('xb') as err:q=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
write('fresh-kernel-receipt97.native.json',dict(argv=argv,exit_code=q.returncode,terminal_closed=True,utc=start.isoformat(),production_raw_sha256=sha(raw),kernel_input=info(W),header_raw_sha256=info(H)['raw_sha256'],ELAN_TOOLCHAIN_removed=True,full_fresh_production_elaboration=True,independent_sealed_header_witness=True))
print('Fresh exact production/sealed-header check exit',q.returncode,flush=True)
assert q.returncode==0
