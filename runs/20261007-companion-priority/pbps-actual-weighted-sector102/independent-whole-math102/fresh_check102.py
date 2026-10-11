from pathlib import Path
import hashlib,json,re,subprocess,os,sys,difflib,time
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;P=B.parent/'pbps-weighted-sector-preread102'
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(p):return json.loads(Path(p).read_bytes())
def save(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualWeightedSector.lean';H=P/'Header102.lean';S=P/'root.statement-seal102.json';F=B/'focused102/production1'
raw=M.read_bytes();assert info(M)['raw_sha256']=='9fa8aee0014fc558c455f0350ffab8c43804645d2878b19d7704c8b6bea5f92b'
assert load(F/'receipt.json')['input_raw_sha256']==info(M)['raw_sha256'] and load(F/'receipt.json')['exit_code']==0 and (F/'input.exactraw.lean').read_bytes()==raw
assert info(H)['raw_sha256']=='fcd8cded492e47481dfa5dca20f55a3e19f7d630ebeccfe2a0d8903b31794f3d'
assert info(S)['raw_sha256']=='53a4f942841eb1c8cd4f5bf99338bd3279ddc5cac6f1f0e755938c253cc62e51'
p=M.read_text(encoding='utf8');h=H.read_text(encoding='utf8');seal=load(S)
def decl(t,n):
 s=re.search(r'^(?:private )?(?:def|theorem) '+re.escape(n)+r'(?=\s|\{)',t,re.M);assert s,n
 e=re.search(r'^(?:(?:private )?(?:def|theorem) |#print|#check|end\b|open |set_option )',t[s.end():],re.M)
 return re.sub(r'/\-.*?\-/','',t[s.start():s.end()+e.start()] if e else t[s.start():],flags=re.S).strip()
hs=decl(h,'candidate');hs=hs[hs.index('{E : Type*}'):]
ps=decl(p,'actual_weighted_sector_statement');ps=ps[ps.index('{E : Type*}'):]
assert hs==ps==seal['expanded_literal_Prop'].strip()
assert len(re.findall(r'^    let ',ps,re.M))==25 and len(re.findall(r'^        let ',ps,re.M))==3
paths=[M,H,S,P/'independent-header-math102/header-math-decision102.native.json',P/'independent-header-math102/source-topology-admission102.native.json',P/'independent-header-math102/closed-RAW-review102.native.json',P/'independent-header-math102/pregraph-projection-erratum102.native.json',B/'Assembly102.lean',B/'Diagnostic102.lean',B/'route-diagnosis102.json',R/'lean-toolchain',R/'lake-manifest.json',R/'tools/astis.py']
trials=['assembly1','assembly2','diagnostic1','assembly3-explicit-embedding','assembly4-continuous-exp','production1']
trialrows=[]
for trial in trials:
 d=B/'focused102'/trial;rc=load(d/'receipt.json');assert info(d/'input.exactraw.lean')['raw_sha256']==rc['input_raw_sha256']
 trialrows.append(dict(name=trial,receipt=info(d/'receipt.json'),exit_code=rc['exit_code'],input=info(d/'input.exactraw.lean')))
 for n in ['receipt.json','input.exactraw.lean','stdout.log','stderr.log']:paths.append(d/n)
for trial in ['assembly1','assembly2','assembly3-explicit-embedding']:assert load(B/'focused102'/trial/'receipt.json')['exit_code']!=0
for trial in ['assembly4-continuous-exp','production1']:assert load(B/'focused102'/trial/'receipt.json')['exit_code']==0
for n in ['ActualEndpointTimeReversal','ActualPrescribedWeightedDensity','ActualFiniteCountPath']:paths.append(M.parent/(n+'.lean'))
for q in ['MeasureTheory/Integral/Lebesgue/Map.lean','MeasureTheory/Function/SpecialFunctions/Basic.lean','MeasureTheory/Constructions/BorelSpace/Real.lean','MeasureTheory/Group/Arithmetic.lean','Analysis/Complex/Exponential.lean']:paths.append(R/'.lake/packages/mathlib/Mathlib'/q)
snap=O/'inputs';snap.mkdir();inputs=[]
for i,x in enumerate(paths):
 q=snap/(str(i).zfill(2)+'.'+x.name+'.exactraw');q.write_bytes(x.read_bytes());inputs.append(dict(**info(x),snapshot=q.relative_to(R).as_posix()))
save('preserved-trials102.native.json',dict(kind='preserved-negative-elaboration-and-API-evidence',trials=trialrows,diagnosis=info(B/'route-diagnosis102.json'),first_two='whnf elaboration timeouts; failed trials are not proof evidence',diagnostic='Localized joint-density composition inference; the explicit typed measurable embedding resolves elaboration cost without changing mathematical route.',third='Remaining Continuous.exp API mismatch; corrected to Real.continuous_exp.comp hU.neg.',fourth='Explicit embedding and actual continuous-exp API compile under400k heartbeats.',statement_unchanged=True,no_hypothesis_or_route_repair=True))
binders=hs[:hs.index(': Prop := by')].rstrip();body='\n'.join(v for v in h.splitlines() if not v.startswith('import '))
witness='\nnamespace IndependentWholeMath102\nopen MeasureTheory InnerProductSpace\nopen scoped NNReal ENNReal Classical ContDiff\nnoncomputable section\nset_option autoImplicit false\ntheorem sealed_header_witness\n    '+binders+' : PBPSWeightedSectorCandidate102.candidate hα hαβ hV hH hη hβη := by\n  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualWeightedSector.actual_weighted_sector_lintegral hα hαβ hV hH hη hβη\nend\nend IndependentWholeMath102\n#print axioms IndependentWholeMath102.sealed_header_witness\n'
W=O/'FreshExactProductionAndHeader102.lean';W.write_bytes(raw+b'\n'+body.encode()+witness.encode());assert W.read_bytes().startswith(raw)
assert not re.search(r'^import .*\.ActualWeightedSector\s*$',W.read_text(encoding='utf8'),re.M)
save('prepared-inputs102.native.json',dict(inputs=inputs,production=info(M),header=info(H),seal=info(S),kernel_input=info(W),literal_statement_matches_exactly=True,full_exact_production_prefix=True,target_production_not_imported=True,private_statement_visibility=True,no_top_level_auxiliary_helpers=True))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(W.relative_to(R))];start=time.time()
with (O/'fresh-kernel.stdout.log').open('xb') as out,(O/'fresh-kernel.stderr.log').open('xb') as err:q=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
save('fresh-kernel-receipt102.native.json',dict(argv=argv,exit_code=q.returncode,seconds=time.time()-start,terminal_closed=True,production_raw_sha256=info(M)['raw_sha256'],kernel_input=info(W),header_raw_sha256=info(H)['raw_sha256'],ELAN_TOOLCHAIN_removed=True,full_fresh_production_elaboration=True,independent_sealed_header_witness=True))
assert q.returncode==0 and M.read_bytes()==raw
sys.path.insert(0,str(R/'tools'));import astis
hits=astis.forbidden_pattern_hits();local=[f'{i}:{line}' for i,line in enumerate(astis.strip_lean_comments_and_strings(p).splitlines(),1) if astis.FORBIDDEN_REGEX.search(line)]
out=(O/'fresh-kernel.stdout.log').read_text(encoding='utf8');axioms=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',out)
assert len(axioms)==2 and all({s.strip() for s in a.split(',')}=={'propext','Classical.choice','Quot.sound'} for a in axioms)
assert not hits and not local and '_private.' not in p
save('fake-closure-and-axioms102.native.json',dict(status='PASS',production=info(M),repository_forbidden_pattern_hits=hits,exact_module_pattern_hits=local,mangled_private_API_calls=False,fresh_axiom_lists=axioms,standard_allowed_axioms=['propext','Classical.choice','Quot.sound'],sealed_header_witness=True))
print('Fresh whole kernel, exact sealed Header102 witness and native fake-closure PASS',flush=True)
