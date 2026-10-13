from pathlib import Path
import subprocess,sys
py=sys.executable;head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
checks=[('python-compile',['-m','py_compile','tools/astis.py']),('contributor',['tools/astis_contributor_contract.py','check','--base',head]),('publication',['tools/astis_publication.py','check','--base',head]),('semantic-cli',['tools/astis_semantic_roundtrip.py','check']),('frontier-cli',['tools/astis_frontier_cells.py','check'])]
for label,args in checks:
 subprocess.run([py,'-X','utf8','.astis/pbps-corrector71/foreground-integration71.py','integration71/'+label,py,'-X','utf8',*args],check=True)
print('PASS all small71 admission gates')
