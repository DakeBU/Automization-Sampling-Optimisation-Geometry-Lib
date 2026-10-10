import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
py=sys.executable
checks=[('scope-graph-check-final',['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-projected-rotation']),('scope-site-check-final',['website/scripts/check_site.py']),('scope-publication-final',['tools/astis_publication.py','check','--base','origin/main']),('scope-frontier-final',['tools/astis_frontier_cells.py','check']),('scope-contributor-final',['tools/astis_contributor_contract.py','check','--base','origin/main']),('scope-semantic-final',['tools/astis_semantic_roundtrip.py','check'])]
def run(item):
 label,args=item
 subprocess.run([py,'-X','utf8','.astis/pbps-actual-rotation70/foreground-integration70.py','integration70/'+label,py,'-X','utf8',*args],check=True)
with ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(run,checks): pass
print('PASS bounded70 graph/site/publication/frontier/contributor/semantic after exact generated-sideeffect preservation')
