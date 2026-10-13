import pathlib,json,subprocess,os,sys,time,hashlib
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
C=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip();BASE='2ebf4ad2e323ad26f62fcf0c9859e66579549536'
PY=[sys.executable,'-X','utf8'];LAKE=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe')
def save(p,v):(O/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None)
# Reuse the independently assembled source+literal-header witness by exact bytes; fresh kernel execution.
witness=O.parent/'independent-whole-math95/ExactSealedWitness95.lean'
checks=[('focused-module',[LAKE,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion']),('current-sealed-kernel',[LAKE,'env','lean',str(witness.relative_to(R))]),('contributor',PY+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',PY+['tools/astis_publication.py','check','--base',BASE]),('semantic',PY+['tools/astis_semantic_roundtrip.py','check']),('frontier',PY+['tools/astis_frontier_cells.py','check']),('committed-diff',['git','diff','--check',BASE,C])]
receipts=[]
for name,argv in checks:
 start=time.time()
 with (O/(name+'.stdout.log')).open('wb') as out,(O/(name+'.stderr.log')).open('wb') as err:p=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
 rc={'command':argv,'verified_commit':C,'exit_code':p.returncode,'seconds':time.time()-start,'ELAN_TOOLCHAIN_removed':True,'terminal_closed':True};save(name+'.receipt.json',rc);receipts.append(name+'.receipt.json');print(name,p.returncode,flush=True)
 if p.returncode:break
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
from tools import astis
decl='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBoundedPathExpansion.actual_bounded_path_functional_expansion'
pub.check_advance([decl],reviewed=True);save('publication-reviewed.json',{'status':'PASS','declaration':decl,'verified_commit':C})
hits=astis.forbidden_pattern_hits();save('fake-closure.json',{'status':'PASS' if not hits else 'FAIL','hits':hits})
assert not hits and all(json.loads((O/x).read_text())['exit_code']==0 for x in receipts)
save('checks-complete95.json',{'status':'PASS','verified_commit':C,'receipts':receipts,'reviewed_publication':True,'fake_closure_hits':0})
