import subprocess,sys
py=sys.executable;head='origin/main'
checks=[('official-graph-final-admin',['website/scripts/underlying_lean_graph.py']),('graph-check-actual-final',['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-corrector-perturbation']),('graph-check-generic-final',['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-hilbert-corrector-perturbation']),('site-check-final',['website/scripts/check_site.py']),('publication-final-admin',['tools/astis_publication.py','check','--base',head]),('frontier-final-admin',['tools/astis_frontier_cells.py','check']),('contributor-final-admin',['tools/astis_contributor_contract.py','check','--base',head]),('semantic-final-admin',['tools/astis_semantic_roundtrip.py','check'])]
for label,args in checks:
 subprocess.run([py,'-X','utf8','.astis/pbps-perturbation72/foreground72.py','integration72/'+label,py,'-X','utf8',*args],check=True)
print('PASS final72 official graph/site/publication/frontier/contributor/semantic gates')
