from pathlib import Path
import hashlib,json,re,subprocess,os,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;P=B.parent/'pbps-finite-state-reversal-preread99';sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedStateReversal.lean';H=P/'Header99.minimal-import.lean';S=P/'root.statement-seal99.json';F=B/'focused99/production1';raw=M.read_bytes();assert sha(raw)=='687ff485725aaf3e03e67f57e16df6632e085d129d4cbd30f8a4ab0ce356a3e5'
rc=load(F/'receipt.json');assert rc['exit_code']==0 and rc['input_raw_sha256']==sha(raw)
assert info(H)['raw_sha256']=='ee79c6079b533ff9bb374aae08a09dee7ea2efc5b7abb3cd1bb0c3fe131060e7';assert info(S)['raw_sha256']=='e802ac728d137274917cc707fa84b0f4b99004e1834fe889e10f0f9f0de8351e'
p=M.read_text(encoding='utf8');h=H.read_text(encoding='utf8');seal=load(S)
def decl(t,n):
 s=re.search(r'^(?:private )?(?:def|theorem) '+re.escape(n)+r'(?=\s|\{)',t,re.M);assert s,n
 e=re.search(r'^(?:(?:private )?(?:def|theorem) |#print|#check|end\b|open |set_option )',t[s.end():],re.M)
 v=t[s.start():s.end()+e.start()] if e else t[s.start():]
 return re.sub(r'/\-.*?\-/','',v,flags=re.S).strip()
def norm(t):return re.sub(r'\s+',' ',re.sub(r'^private ','',t,flags=re.M)).strip()
hs=decl(h,'candidate');hs=hs[hs.index('{E : Type*}'):];ps=decl(p,'actual_prescribed_state_reversal_statement');ps=ps[ps.index('{E : Type*}'):];assert hs==ps==seal['expanded_literal_Prop'].strip()
for n in ['finite_state_reversal','incoming_rate_product']:assert norm(decl(p,n))==norm(decl((B/'FiniteStates99.lean').read_text(encoding='utf8'),n))
assert norm(decl(p,'reversed_grid_gaps'))==norm(decl((B/'Grid99.lean').read_text(encoding='utf8'),'reversed_grid_gaps'))
paths=[M,H,S,F/'receipt.json',F/'stdout.log',F/'stderr.log',B/'FiniteStates99.lean',B/'Grid99.lean',B/'independent-fragment-math99/finite-state/finite-state-math-decision99.native.json',B/'independent-fragment-math99/finite-state/closed-RAW-finite-state99.native.json',B/'focused99/grid3/receipt.json',R/'lean-toolchain',R/'lake-manifest.json']
# Resolve the actual named successful Grid receipt without guessing a trial filename.
paths=[x for x in paths if x.exists()]
for x in sorted((B/'focused99').glob('grid*/receipt.json')):paths.append(x)
for n in ['ActualEndpointTimeReversal','ActualPhaseReversalVolume']:paths.append(R/'AutoSamplingTheory/ExampleCases/ProximalBPS'/(n+'.lean'))
paths += [R/'.astis/toolchain/lean-4.33.0-windows/src/lean/Init/Data/Fin/Lemmas.lean',R/'.lake/packages/mathlib/Mathlib/Algebra/BigOperators/Group/Finset/Defs.lean',P/'independent-header-math99/minimal-import99/minimal-import-transfer99.native.json',P/'independent-header-math99/topology99/source-topology-decision99.native.json']
snap=O/'inputs';snap.mkdir();inputs=[]
for i,x in enumerate(dict.fromkeys(paths)):
 q=snap/(str(i).zfill(2)+'.'+x.name+'.exactraw');q.write_bytes(x.read_bytes());inputs.append(dict(**info(x),snapshot=q.relative_to(R).as_posix()))
binders=hs[:hs.index(': Prop := by')].rstrip();body='\n'.join(v for v in h.splitlines() if not v.startswith('import '))
witness='\nnamespace IndependentWholeMath99\nopen MeasureTheory InnerProductSpace\nopen scoped NNReal ENNReal Classical ContDiff\nnoncomputable section\nset_option autoImplicit false\ntheorem sealed_header_witness\n    '+binders+' : PBPSFiniteStateReversalCandidate99.candidate hα hαβ hV hH hη hβη := by\n  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal.actual_prescribed_state_reversal_and_rate_product hα hαβ hV hH hη hβη\nend\nend IndependentWholeMath99\n#print axioms IndependentWholeMath99.sealed_header_witness\n'
W=O/'FreshExactProductionAndHeader99.lean';W.write_bytes(raw+b'\n'+body.encode()+witness.encode())
save('prepared-inputs99.native.json',dict(production=info(M),header=info(H),statement_seal=info(S),inputs=inputs,literal_statement_matches_exactly=True,unchanged_reviewed_fragment_declarations=['finite_state_reversal','incoming_rate_product'],grid_helper_exact_from_successful_scratch=True,comparison_exceptions='private visibility and enclosing namespace only',kernel_input=info(W),full_exact_production_prefix=True,target_production_not_imported=True))
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH'];argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(W.relative_to(R))];start=datetime.datetime.now(datetime.timezone.utc)
with (O/'fresh-kernel.stdout.log').open('xb') as out,(O/'fresh-kernel.stderr.log').open('xb') as err:q=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
save('fresh-kernel-receipt99.native.json',dict(argv=argv,exit_code=q.returncode,terminal_closed=True,utc=start.isoformat(),production_raw_sha256=sha(raw),kernel_input=info(W),header_raw_sha256=info(H)['raw_sha256'],ELAN_TOOLCHAIN_removed=True,full_fresh_production_elaboration=True,independent_sealed_header_witness=True));print('Fresh full production and sealed-header witness',q.returncode,flush=True);assert q.returncode==0 and M.read_bytes()==raw
