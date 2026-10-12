from pathlib import Path
import hashlib,json,os,subprocess,time
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;P=O.parent
S=R/'runs/20261007-companion-priority/pbps-actual-countable-endpoint105/next-primary106'
sha=lambda b:hashlib.sha256(b).hexdigest()
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def load(p):return json.loads(p.read_bytes())
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
H=P/'Header106.lean';raw=H.read_bytes();ht=raw.decode().replace('\r\n','\n')
assert sha(raw)=='6e995eb9308bf5c6d09fcd15b6ebb0e120b3fced62202572a4041cbfe19e7b9d'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCountableEndpointLaw.lean';mt=M.read_text(encoding='utf-8')
literal=load(S/'literal-definition-context106.native.json')
for stem in ['literal37','global_witness_prefix']:
 s=literal[stem+'_LF_text'];assert sha(s.encode())==literal[stem+'_LF_sha256'] and s in ht and s in mt
binders=ht.split('def candidate\n',1)[1].split(' : Prop := by',1)[0]
pb=mt.split('private def actual_countable_endpoint_statement\n',1)[1].split(' : Prop := by',1)[0]
assert binders==pb
assert len(__import__('re').findall(r'^    let ',literal['literal37_LF_text'],__import__('re').M))==37
fresh=O/'FreshHeader106.lean';assert not fresh.exists();fresh.write_bytes(raw)
inputs=[H,M,P/'typecheck106/receipt.json',S/'recommendation106.native.json',S/'literal-definition-context106.native.json',S/'independent-topology106/recommendation-math-review106.native.json',S/'independent-topology106/topology-admission106.native.json',S/'independent-topology106/closed-RAW106.native.json',R/'lean-toolchain',R/'lake-manifest.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
save('input-freeze106.native.json',{'inputs':[info(p) for p in inputs],'six_original_analytic_binders_text_equal':True,'literal37_and_global_Z_prefix_exact':True,'fresh_input':info(fresh),'proof':False})
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(fresh)];t=time.time();q=subprocess.run(argv,cwd=R,env=env,capture_output=True)
(O/'fresh-typecheck.stdout.log').write_bytes(q.stdout);(O/'fresh-typecheck.stderr.log').write_bytes(q.stderr)
save('fresh-typecheck106.receipt.json',{'argv':argv,'exit_code':q.returncode,'terminal_closed':True,'seconds':time.time()-t,'input':info(fresh),'stdout':info(O/'fresh-typecheck.stdout.log'),'stderr':info(O/'fresh-typecheck.stderr.log'),'proof':False})
print('TYPECHECK',q.returncode,flush=True)
