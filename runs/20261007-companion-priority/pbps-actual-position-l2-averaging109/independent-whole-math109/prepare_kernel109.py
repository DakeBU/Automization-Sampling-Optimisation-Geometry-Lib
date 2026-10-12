from pathlib import Path
import hashlib,json,subprocess,os,time,sys
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent
P=R/'runs/20261007-companion-priority/pbps-actual-position-l2-preread109'
M=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPositionL2Averaging.lean'
sha=lambda b:hashlib.sha256(b).hexdigest()
def path(p):return R/str(p).replace('\\','/').removeprefix('E:/Samplinglib/')
def info(p):
 p=path(p);return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def save(n,v):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
raw=M.read_bytes();header=(P/'Header109.lean').read_bytes();ht=header.decode().replace('\r\n','\n');mt=raw.decode().replace('\r\n','\n');seal=json.loads((P/'root.statement-seal109.json').read_bytes())
assert sha(raw)=='21c6b4e95b729b41f555eecf6a42185ab2f63bff7bcab3f6dc2ab82da171e85e'
assert sha((P/'root.statement-seal109.json').read_bytes())=='d17001eb1349c6cd4c8711e8c729816570c88811f60a7bb2007ad0985680f8e9'
literal=ht.split('def candidate\n',1)[1].split('\n\n#check candidate',1)[0].strip()
prod=mt.split('private def actual_position_l2_statement\n',1)[1].split('\nset_option maxHeartbeats',1)[0].strip()
assert literal==prod==seal['expanded_literal_Prop'];assert sha(header)==seal['header']['raw_sha256']
rows=[]
for x in seal['all_bound_RAW_inputs_rehashed']:
 p=path(x['path']);observed=sha(p.read_bytes());rows.append(dict(**x,observed_raw_sha256=observed));assert observed==x['raw_sha256'],x
assert len(rows)==115
save('sealed-input-rehash109.native.json',dict(status='PASS',count=len(rows),bindings=rows))
binders=ht.split('def candidate\n',1)[1].split(' : Prop := by',1)[0]
candidate='\n'.join(line for line in ht.splitlines() if not line.startswith('import '))
witness='''\nnamespace IndependentExactHeader109
open MeasureTheory InnerProductSpace ProbabilityTheory
open scoped ContDiff NNReal ENNReal Classical
noncomputable section
set_option autoImplicit false
theorem sealed_header_witness
'''+binders+''' : PBPSActualPositionL2Candidate109.candidate hα hαβ hV hH hη hβη := by
  exact AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging.actual_position_l2_averaging hα hαβ hV hH hη hβη
#print axioms sealed_header_witness
end
end IndependentExactHeader109
'''
p=O/'FreshExactProductionAndHeader109.lean';assert not p.exists();p.write_bytes(raw+b'\n'+candidate.encode()+b'\n'+witness.encode());assert p.read_bytes()[:len(raw)]==raw
assert b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPositionL2Averaging' not in p.read_bytes()
inputs=[M,P/'Header109.lean',P/'root.statement-seal109.json',R/'lean-toolchain',R/'lake-manifest.json',R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualL2FlipDuality.lean',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
inputs += [path(seal[k]['path']) for k in ['independent_math_header','independent_source_header','independent_topology','source_graph','source_coverage']]
save('prepared-inputs109.native.json',dict(reviewer='/root/exact_verifier96',inputs=[info(x) for x in inputs],production_exact_prefix=info(p),literal_header_seal_privateProp_equal=True,imports_target_module=False,production_prefix_bytes=len(raw),publication_not_used=True))
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis
hits=astis.forbidden_pattern_hits();clean=astis.strip_lean_comments_and_strings(mt);local=[(i,l) for i,l in enumerate(clean.splitlines(),1) if astis.FORBIDDEN_REGEX.search(l)]
save('fake-closure-scan109.native.json',dict(production=info(M),repository_hits=hits,module_hits=local,decision='PASS' if not hits and not local else 'FAIL'));assert not hits and not local
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p)];t=time.time();q=subprocess.run(cmd,cwd=R,env=env,capture_output=True)
(O/'fresh-kernel.stdout.log').write_bytes(q.stdout);(O/'fresh-kernel.stderr.log').write_bytes(q.stderr)
save('fresh-kernel-receipt109.native.json',dict(command=cmd,exit_code=q.returncode,elapsed_seconds=time.time()-t,production=info(M),input=info(p),stdout=info(O/'fresh-kernel.stdout.log'),stderr=info(O/'fresh-kernel.stderr.log'),terminal_closed=True))
print('KERNEL',q.returncode,flush=True)
