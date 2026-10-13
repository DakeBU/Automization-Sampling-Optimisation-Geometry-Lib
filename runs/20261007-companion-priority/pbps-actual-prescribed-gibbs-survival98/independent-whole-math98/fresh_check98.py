from pathlib import Path
import hashlib,json,re,subprocess,os,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;P=B.parent/'pbps-prescribed-gibbs-survival-preread98'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def write(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedGibbsSurvival.lean';H=P/'Header98.lean';S=P/'root.statement-seal98.json';F=B/'checks98/production1'
raw=M.read_bytes();assert sha(raw)=='f4856a5f059ef9875e481830cbd1a6152d7bc7de690ed325a71390a791098b95'
assert (F/'input.lean').read_bytes()==raw;rc=load(F/'receipt.json');assert rc['exit_code']==0 and rc['target_raw_sha256']==sha(raw)
p=M.read_text(encoding='utf8');h=H.read_text(encoding='utf8');seal=load(S);assert info(H)['raw_sha256']==seal['header']['raw_sha256']=='50c6999fe069f4cf648832a804b71bb8e447b7a3aea0f0c42a836f81650c6ad0'
def decl(t,n):
 s=re.search(r'^(?:private )?(?:def|theorem) '+re.escape(n)+r'(?=\s|\{)',t,re.M);assert s,n
 e=re.search(r'^(?:(?:private )?(?:def|theorem) |#print|#check|end\b|open |set_option )',t[s.end():],re.M)
 v=t[s.start():s.end()+e.start()] if e else t[s.start():]
 return re.sub(r'/\-.*?\-/','',v,flags=re.S).strip()
def norm(t):return re.sub(r'\s+',' ',re.sub(r'^private ','',t,flags=re.M)).strip()
hs=decl(h,'candidate');hs=hs[hs.index('{E : Type*}'):];ps=decl(p,'actual_prescribed_gibbs_survival_statement');ps=ps[ps.index('{E : Type*}'):]
assert hs==ps==seal['expanded_literal_Prop'].strip()
frags=[('arc','Arc98.lean','actual_arc_energy'),('finite','FiniteBalance98.lean','finite_energy_balance')]
for kind,file,name in frags:assert norm(decl(p,name))==norm(decl((B/file).read_text(encoding='utf8'),name)),name
paths=[M,H,S,F/'input.lean',F/'receipt.json',F/'stdout.log',F/'stderr.log',R/'lean-toolchain',R/'lake-manifest.json']
for kind,file,name in frags:paths += [B/file,B/'independent-fragment-math98'/kind/(kind+'-math-decision98.native.json'),B/'independent-fragment-math98'/kind/('closed-RAW-'+kind+'98.native.json')]
for n in ['ActualHarmonicFlow','ActualBounceRate','ActualFiniteCountPath','ActualEndpointTimeReversal']:paths.append(R/'AutoSamplingTheory/ExampleCases/ProximalBPS'/(n+'.lean'))
paths += [R/'.lake/packages/mathlib/Mathlib'/v for v in ['MeasureTheory/Integral/IntervalIntegral/Basic.lean','MeasureTheory/Integral/IntervalIntegral/FundThmCalculus.lean','Analysis/Calculus/Deriv/Comp.lean']]
snap=O/'inputs';snap.mkdir();inputs=[]
for i,x in enumerate(paths):
 q=snap/(str(i).zfill(2)+'.'+x.name+'.exactraw');q.write_bytes(x.read_bytes());inputs.append(dict(**info(x),snapshot=q.relative_to(R).as_posix()))
binders=hs[:hs.index(': Prop := by')].rstrip();body='\n'.join(v for v in h.splitlines() if not v.startswith('import '))
witness='\nnamespace IndependentWholeMath98\nopen MeasureTheory InnerProductSpace\nopen scoped NNReal ENNReal Classical ContDiff\nnoncomputable section\nset_option autoImplicit false\ntheorem sealed_header_witness\n    '+binders+' : PBPSPrescribedGibbsSurvivalCandidate98.candidate hα hαβ hV hH hη hβη := by\n  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival.actual_prescribed_gibbs_survival_balance hα hαβ hV hH hη hβη\nend\nend IndependentWholeMath98\n#print axioms IndependentWholeMath98.sealed_header_witness\n'
W=O/'FreshExactProductionAndHeader98.lean';W.write_bytes(raw+b'\n'+body.encode()+witness.encode())
write('prepared-inputs98.native.json',dict(production=info(M),header=info(H),statement_seal=info(S),inputs=inputs,literal_statement_matches_exactly=True,unchanged_reviewed_fragment_declarations=[x[2] for x in frags],comparison_exceptions='private visibility and enclosing namespace only',kernel_input=info(W),full_exact_production_prefix=True,target_production_not_imported=True))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(W.relative_to(R))];start=datetime.datetime.now(datetime.timezone.utc)
with (O/'fresh-kernel.stdout.log').open('xb') as out,(O/'fresh-kernel.stderr.log').open('xb') as err:q=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
write('fresh-kernel-receipt98.native.json',dict(argv=argv,exit_code=q.returncode,terminal_closed=True,utc=start.isoformat(),production_raw_sha256=sha(raw),kernel_input=info(W),header_raw_sha256=info(H)['raw_sha256'],ELAN_TOOLCHAIN_removed=True,full_fresh_production_elaboration=True,independent_sealed_header_witness=True))
print('Fresh production/header witness exit',q.returncode,flush=True);assert q.returncode==0
