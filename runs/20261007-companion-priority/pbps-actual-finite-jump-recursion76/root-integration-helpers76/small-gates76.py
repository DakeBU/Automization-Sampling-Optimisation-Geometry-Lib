import subprocess,sys
py=sys.executable
checks=[('publication', ['tools/astis_publication.py', 'check', '--base', 'origin/main']), ('semantic', ['tools/astis_semantic_roundtrip.py', 'check']), ('frontier', ['tools/astis_frontier_cells.py', 'check']), ('contributor', ['tools/astis_contributor_contract.py', 'check', '--base', 'origin/main'])]
for label,args in checks:
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-recursion76/foreground76.py','integration76/'+label,py,'-B','-X','utf8',*args],check=True)
print('PASS76 four bounded admission gates')
