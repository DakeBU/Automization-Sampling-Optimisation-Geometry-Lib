import subprocess,sys
py=sys.executable
checks=[('official-graph-final', ['website/scripts/underlying_lean_graph.py']), ('graph-check-final', ['tools/astis_publication.py', 'graph-check', '--cell', 'ASTIS-SW-PBPS-actual-finite-jump-recursion']), ('site-check-final', ['website/scripts/check_site.py']), ('publication-final', ['tools/astis_publication.py', 'check', '--base', 'origin/main']), ('frontier-final', ['tools/astis_frontier_cells.py', 'check']), ('contributor-final', ['tools/astis_contributor_contract.py', 'check', '--base', 'origin/main']), ('semantic-final', ['tools/astis_semantic_roundtrip.py', 'check'])]
for label,args in checks:
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-recursion76/foreground76.py','integration76/'+label,py,'-B','-X','utf8',*args],check=True)
print('PASS76 final graph/site/publication/frontier/contributor/semantic gates')
