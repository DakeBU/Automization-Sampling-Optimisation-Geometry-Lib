from pathlib import Path
import hashlib,json,re,subprocess,os,sys,difflib
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;P=B.parent/'pbps-weighted-density-preread101'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(p):return json.loads(p.read_bytes())
def save(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedWeightedDensity.lean';H=P/'Header101.lean';S=P/'root.statement-seal101.json';F=B/'focused101/production2-private'
raw=M.read_bytes();assert info(M)['raw_sha256']=='b9c6e8ed0655b9c607eff38ecf74eb3a4555ff90184475e8dfc554bb96dcb3c0'
assert load(F/'receipt.json')['input_raw_sha256']==info(M)['raw_sha256'] and load(F/'receipt.json')['exit_code']==0 and (F/'input.exactraw.lean').read_bytes()==raw
assert info(H)['raw_sha256']=='95693f5ab9b8da50fabdc4da9deeaf6f4950cc4cdd4d60e0a53e0412bfa31c27'
assert info(S)['raw_sha256']=='cdd05195156722be3b65c56fc09fe48971e021df81afadb48968dbab50c81d59'
p=M.read_text(encoding='utf8');h=H.read_text(encoding='utf8');seal=load(S)
def decl(t,n):
 s=re.search(r'^(?:private )?(?:def|theorem) '+re.escape(n)+r'(?=\s|\{)',t,re.M);assert s,n
 e=re.search(r'^(?:(?:private )?(?:def|theorem) |#print|#check|end\b|open |set_option )',t[s.end():],re.M)
 return re.sub(r'/\-.*?\-/','',t[s.start():s.end()+e.start()] if e else t[s.start():],flags=re.S).strip()
hs=decl(h,'candidate');hs=hs[hs.index('{E : Type*}'):]
ps=decl(p,'actual_prescribed_weighted_density_statement');ps=ps[ps.index('{E : Type*}'):]
assert hs==ps==seal['expanded_literal_Prop'].strip()
public1=(B/'focused101/production1/input.exactraw.lean').read_text(encoding='utf8');assert public1.replace('\ndef actual_prescribed_weighted_density_statement','\nprivate def actual_prescribed_weighted_density_statement')==p
paths=[M,H,S,P/'independent-header-math101/header-math-decision101.native.json',P/'independent-header-math101/source-topology-decision101.native.json',P/'independent-header-math101/closed-RAW-review101.native.json',B/'Assembly101.lean',R/'lean-toolchain',R/'lake-manifest.json',R/'tools/astis.py']
for trial in ['assembly1','assembly2','production1','production2-private']:
 d=B/'focused101'/trial;rc=load(d/'receipt.json');assert info(d/'input.exactraw.lean')['raw_sha256']==rc['input_raw_sha256']
 for n in ['receipt.json','input.exactraw.lean','stdout.log','stderr.log']:paths.append(d/n)
assert load(B/'focused101/assembly1/receipt.json')['exit_code']!=0
for n in ['ActualPrescribedPathDensity','ActualPrescribedGibbsSurvival','ActualPrescribedStateReversal','ActualPrescribedPathReversal']:paths.append(M.parent/(n+'.lean'))
for q in ['Data/ENNReal/Real.lean','Analysis/Complex/Exponential.lean','Analysis/Normed/Group/Basic.lean']:paths.append(R/'.lake/packages/mathlib/Mathlib'/q)
snap=O/'inputs';snap.mkdir();inputs=[]
for i,x in enumerate(paths):
 q=snap/(str(i).zfill(2)+'.'+x.name+'.exactraw');q.write_bytes(x.read_bytes());inputs.append(dict(**info(x),snapshot=q.relative_to(R).as_posix()))
one=(B/'focused101/assembly1/input.exactraw.lean').read_text(encoding='utf8');two=(B/'focused101/assembly2/input.exactraw.lean').read_text(encoding='utf8')
save('preserved-trials101.native.json',dict(first_trial='negative elaboration evidence only',correction='Public94 density equality is the fourth right-associated conjunct, .2.2.2; .2 selected a conjunction and failed. No target change.',assembly_diff=''.join(difflib.unified_diff(one.splitlines(True),two.splitlines(True))),production_visibility_only_change=True,old_production=info(B/'focused101/production1/input.exactraw.lean'),reviewed_production=info(M)))
binders=hs[:hs.index(': Prop := by')].rstrip();body='\n'.join(v for v in h.splitlines() if not v.startswith('import '))
witness='\nnamespace IndependentWholeMath101\nopen MeasureTheory InnerProductSpace\nopen scoped NNReal ENNReal Classical ContDiff\nnoncomputable section\nset_option autoImplicit false\ntheorem sealed_header_witness\n    '+binders+' : PBPSWeightedDensityCandidate101.candidate hα hαβ hV hH hη hβη := by\n  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedWeightedDensity.actual_prescribed_weighted_density_balance hα hαβ hV hH hη hβη\nend\nend IndependentWholeMath101\n#print axioms IndependentWholeMath101.sealed_header_witness\n'
W=O/'FreshExactProductionAndHeader101.lean';W.write_bytes(raw+b'\n'+body.encode()+witness.encode())
save('prepared-inputs101.native.json',dict(inputs=inputs,production=info(M),header=info(H),seal=info(S),kernel_input=info(W),literal_statement_matches_exactly=True,full_exact_production_prefix=True,target_production_not_imported=True,private_statement_visibility=True,no_top_level_auxiliary_helpers=True))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(W.relative_to(R))]
with (O/'fresh-kernel.stdout.log').open('xb') as out,(O/'fresh-kernel.stderr.log').open('xb') as err:q=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
save('fresh-kernel-receipt101.native.json',dict(argv=argv,exit_code=q.returncode,terminal_closed=True,production_raw_sha256=info(M)['raw_sha256'],kernel_input=info(W),header_raw_sha256=info(H)['raw_sha256'],ELAN_TOOLCHAIN_removed=True,full_fresh_production_elaboration=True,independent_sealed_header_witness=True))
assert q.returncode==0 and M.read_bytes()==raw
sys.path.insert(0,str(R/'tools'));import astis
hits=astis.forbidden_pattern_hits();local=[f'{i}:{line}' for i,line in enumerate(astis.strip_lean_comments_and_strings(p).splitlines(),1) if astis.FORBIDDEN_REGEX.search(line)]
out=(O/'fresh-kernel.stdout.log').read_text(encoding='utf8');axioms=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',out)
assert len(axioms)==2 and all({s.strip() for s in a.split(',')}=={'propext','Classical.choice','Quot.sound'} for a in axioms)
assert not hits and not local and '_private.' not in p
save('fake-closure-and-axioms101.native.json',dict(status='PASS',production=info(M),repository_forbidden_pattern_hits=hits,exact_module_pattern_hits=local,mangled_private_API_calls=False,fresh_axiom_lists=axioms,standard_allowed_axioms=['propext','Classical.choice','Quot.sound'],sealed_header_witness=True))
print('Fresh whole kernel, exact sealed Header101 witness and native fake-closure PASS')
