import subprocess,sys
py=sys.executable;head='origin/main'
checks=[('official-graph-final-admin',['website/scripts/underlying_lean_graph.py']),('graph-check-actual-final',['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-corrector-change']),('site-check-final',['website/scripts/check_site.py']),('publication-final-admin',['tools/astis_publication.py','check','--base',head]),('frontier-final-admin',['tools/astis_frontier_cells.py','check']),('contributor-final-admin',['tools/astis_contributor_contract.py','check','--base',head]),('semantic-final-admin',['tools/astis_semantic_roundtrip.py','check'])]
for label,args in checks:
 subprocess.run([py,'-X','utf8','.astis/pbps-corrector71/foreground-integration71.py','integration71/'+label,py,'-X','utf8',*args],check=True)
print('PASS final71 official graph/site/publication/frontier/contributor/semantic gates')
