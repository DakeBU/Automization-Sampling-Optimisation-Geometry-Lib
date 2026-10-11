from pathlib import Path
import hashlib,json,re,subprocess,os,datetime,sys
R=Path('E:/Samplinglib'); O=Path(__file__).resolve().parent; B=O.parent; P=B.parent/'pbps-finite-path-reversal-preread100'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(p):return json.loads(p.read_bytes())
def save(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathReversal.lean';H=P/'Header100.lean';S=P/'root.statement-seal100.json';F=B/'focused100/production1-sealed-target'
raw=M.read_bytes();assert info(M)['raw_sha256']=='59d3131209605d2df34e74abb098f42d41338ae44f7e4f4bee4d75ac7bc0a3c8'
assert load(F/'receipt.json')['input_raw_sha256']==info(M)['raw_sha256'] and load(F/'receipt.json')['exit_code']==0
assert (F/'input.exactraw.lean').read_bytes()==raw
assert info(H)['raw_sha256']=='94ada767874180a727bfa7627c4e40629da5a77f523895ca30e0d5e0e74008b9'
assert info(S)['raw_sha256']=='830f6b01d3d82168085e7e081a123c3152043090ebd7f0b91410e076cb96c108'
p=M.read_text(encoding='utf8');h=H.read_text(encoding='utf8');seal=load(S)
def decl(t,n):
 s=re.search(r'^(?:private )?(?:def|theorem) '+re.escape(n)+r'(?=\s|\{)',t,re.M);assert s,n
 e=re.search(r'^(?:(?:private )?(?:def|theorem) |#print|#check|end\b|open |set_option )',t[s.end():],re.M)
 return (t[s.start():s.end()+e.start()] if e else t[s.start():]).strip()
hs=decl(h,'candidate');hs=hs[hs.index('{E : Type*}'):]
ps=decl(p,'actual_prescribed_path_reversal_statement');ps=ps[ps.index('{E : Type*}'):]
assert hs==ps==seal['expanded_literal_Prop'].strip()
norm=lambda s:re.sub(r'\s+',' ',re.sub(r'^private ','',s,flags=re.M)).strip()
arc=(B/'ArcReversal100.lean').read_text(encoding='utf8')
for n in ['active_arc','path_reversal']:assert norm(decl(p,n))==norm(decl(arc,n))
paths=[M,H,S,F/'receipt.json',F/'input.exactraw.lean',F/'stdout.log',F/'stderr.log',B/'ArcReversal100.lean',B/'independent-fragment-math100/arc/arc-math-decision100.native.json',B/'independent-fragment-math100/arc/closed-RAW-arc100.native.json',P/'independent-header-math100/header-math-decision100.native.json',P/'independent-header-math100/topology-overlay100/source-topology-admission100.native.json',P/'independent-header-math100/topology-overlay100/closed-RAW-topology-admission100.native.json',R/'lean-toolchain',R/'lake-manifest.json',R/'tools/astis.py']
for n in ['ActualPrescribedStateReversal','ActualFiniteCountPath','ActualPhaseReversalVolume','ActualHarmonicFlow','ActualPrescribedPathDensity']:paths.append(M.parent/(n+'.lean'))
paths += [R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Typeclasses/NullSingletonClass.lean']
snap=O/'inputs';snap.mkdir();inputs=[]
for i,x in enumerate(paths):
 q=snap/(str(i).zfill(2)+'.'+x.name+'.exactraw');q.write_bytes(x.read_bytes());inputs.append(dict(**info(x),snapshot=q.relative_to(R).as_posix()))
binders=hs[:hs.index(': Prop := by')].rstrip()
body='\n'.join(v for v in h.splitlines() if not v.startswith('import '))
witness='\nnamespace IndependentWholeMath100\nopen MeasureTheory InnerProductSpace\nopen scoped NNReal ENNReal Classical ContDiff\nnoncomputable section\nset_option autoImplicit false\ntheorem sealed_header_witness\n    '+binders+' : PBPSFinitePathReversalCandidate100.candidate hα hαβ hV hH hη hβη := by\n  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathReversal.actual_prescribed_path_reversal_and_survival hα hαβ hV hH hη hβη\nend\nend IndependentWholeMath100\n#print axioms IndependentWholeMath100.sealed_header_witness\n'
W=O/'FreshExactProductionAndHeader100.lean';W.write_bytes(raw+b'\n'+body.encode()+witness.encode())
save('prepared-inputs100.native.json',dict(inputs=inputs,production=info(M),header=info(H),seal=info(S),kernel_input=info(W),literal_statement_matches_exactly=True,unchanged_reviewed_helpers=['active_arc','path_reversal'],comparison_exceptions='private visibility and whitespace only',full_exact_production_prefix=True,target_production_not_imported=True))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(W.relative_to(R))]
with (O/'fresh-kernel.stdout.log').open('xb') as out,(O/'fresh-kernel.stderr.log').open('xb') as err:q=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
save('fresh-kernel-receipt100.native.json',dict(argv=argv,exit_code=q.returncode,terminal_closed=True,production_raw_sha256=info(M)['raw_sha256'],kernel_input=info(W),header_raw_sha256=info(H)['raw_sha256'],ELAN_TOOLCHAIN_removed=True,full_fresh_production_elaboration=True,independent_sealed_header_witness=True))
print((O/'fresh-kernel.stdout.log').read_text(encoding='utf8'))
assert q.returncode==0 and M.read_bytes()==raw
sys.path.insert(0,str(R/'tools'));import astis
hits=astis.forbidden_pattern_hits()
local=[f'{i}:{line}' for i,line in enumerate(astis.strip_lean_comments_and_strings(p).splitlines(),1) if astis.FORBIDDEN_REGEX.search(line)]
out=(O/'fresh-kernel.stdout.log').read_text(encoding='utf8');axioms=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',out)
assert len(axioms)==2 and all({s.strip() for s in a.split(',')}=={'propext','Classical.choice','Quot.sound'} for a in axioms)
assert not hits and not local and '_private.' not in p
save('fake-closure-and-axioms100.native.json',dict(status='PASS',production=info(M),repository_forbidden_pattern_hits=hits,exact_module_pattern_hits=local,mangled_private_API_calls=False,fresh_axiom_lists=axioms,standard_allowed_axioms=['propext','Classical.choice','Quot.sound'],sealed_header_witness=True))
print('Fresh whole kernel, exact sealed witness, native fake-closure PASS')
