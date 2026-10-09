import subprocess,sys
py=sys.executable
checks=[('publication', ['tools/astis_publication.py', 'check', '--base', 'origin/main']), ('semantic', ['tools/astis_semantic_roundtrip.py', 'check']), ('frontier', ['tools/astis_frontier_cells.py', 'check']), ('contributor', ['tools/astis_contributor_contract.py', 'check', '--base', 'origin/main'])]
for label,args in checks:
 subprocess.run([py,'-B','-X','utf8','.astis/pbps-harmonic73/foreground73.py','integration73/'+label,py,'-B','-X','utf8',*args],check=True)
print('PASS73 four bounded admission gates')
