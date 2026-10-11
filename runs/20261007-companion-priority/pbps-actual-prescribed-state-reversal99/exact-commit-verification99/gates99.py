from verify99 import *
import os,time
assert head()==C
f=load(O/'input-freeze99.json');assert f['status']=='PASS' and f['verified_commit']==C
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['PYTHONUTF8']='1';env['LEAN_NUM_THREADS']='2';env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
PY=[sys.executable,'-X','utf8']
# Exact fresh-source kernel/public-header/axiom evidence was already independently produced.
# Its RAW inputs and archive closure were rechecked by verify99; avoid duplicate compilation.
whole=load(B/'independent-whole-math99/whole-math-decision99.native.json')
for x in whole['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],('changed fresh-kernel input',x['path'])
rc=load(B/'independent-whole-math99/fresh-kernel-receipt99.native.json');assert rc['exit_code']==0 and rc['production_raw_sha256']==info(M)['raw_sha256']
axes=re.findall(r"depends on axioms:\s*\[([^\]]*)\]",(B/'independent-whole-math99/fresh-kernel.stdout.log').read_text(encoding='utf8'))
assert len(axes)==2 and all(set(re.findall(r'[A-Za-z][A-Za-z.]*',a))=={'propext','Classical.choice','Quot.sound'} for a in axes)
save('kernel-transfer99.json',dict(status='PASS',verified_commit=C,production=info(M),independent_fresh_kernel=info(B/'independent-whole-math99/fresh-kernel-receipt99.native.json'),independent_whole_math=info(B/'independent-whole-math99/whole-math-decision99.native.json'),original_header_witness=True,reason='Exact unchanged production, all reviewed helpers, source parent modules, header and pinned toolchain/library inputs bound by current Git blobs or lossless archives; no mathematical change since fresh full-source witness.',duplicate_compilation=False))
save('axiom-scan99.json',dict(status='PASS',verified_commit=C,axiom_lists=axes,allowed=['propext','Classical.choice','Quot.sound']))
checks=[('focused-module',[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal']),('contributor',PY+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',PY+['tools/astis_publication.py','check','--base',BASE]),('semantic',PY+['tools/astis_semantic_roundtrip.py','check']),('frontier',PY+['tools/astis_frontier_cells.py','check']),('committed-diff',['git','diff','--check',BASE,C])]
receipts=[]
for name,argv in checks:
 assert head()==C;start=time.time()
 with (O/(name+'.stdout.log')).open('xb') as out,(O/(name+'.stderr.log')).open('xb') as err:p=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
 save(name+'.receipt.json',dict(command=argv,verified_commit=C,exit_code=p.returncode,seconds=time.time()-start,ELAN_TOOLCHAIN_removed=True,terminal_closed=True));receipts.append(name+'.receipt.json');print(name,p.returncode,flush=True)
 assert p.returncode==0,name
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
from tools import astis
pub.check_advance([D],reviewed=True);save('publication-reviewed99.json',dict(status='PASS',verified_commit=C,declaration=D))
hits=astis.forbidden_pattern_hits();save('fake-closure99.json',dict(status='PASS' if not hits else 'FAIL',verified_commit=C,hits=hits));assert not hits
assert head()==C
save('checks-complete99.json',dict(status='PASS',verified_commit=C,receipts=receipts,reviewed_publication=True,fake_closure_hits=0,axiom_scan='axiom-scan99.json',kernel_transfer='kernel-transfer99.json'))
