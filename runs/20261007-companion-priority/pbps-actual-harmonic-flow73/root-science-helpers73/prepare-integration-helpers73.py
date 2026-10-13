from pathlib import Path
import hashlib,json
old=Path('.astis/pbps-perturbation72');new=Path('.astis/pbps-harmonic73');rows=[]
replacements=[('pbps-b4-corrector-perturbation72','pbps-actual-harmonic-flow73'),('pbps-perturbation72','pbps-harmonic73'),('ActualCorrectorPerturbation.actual_corrector_perturbation','ActualHarmonicFlow.actual_harmonic_flow_laws'),('ActualCorrectorPerturbation','ActualHarmonicFlow'),('actual-corrector-perturbation','actual-harmonic-flow'),('foreground72.py','foreground73.py'),('integration72','integration73'),('visual72','visual73'),('mandatory72','mandatory73')]
for name in ['inspect-cdp72.mjs','inspect-copy72.mjs']:
 p=old/name;s=p.read_text(encoding='utf8')
 for a,b in replacements:s=s.replace(a,b)
 dest=new/name.replace('72.','73.');assert not dest.exists(),dest;dest.write_text(s,encoding='utf8',newline='\n')
 rows.append(dict(source=p.as_posix(),source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),adapted=dest.as_posix(),adapted_RAW_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
checks=[('publication',['tools/astis_publication.py','check','--base','origin/main']),('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check']),('contributor',['tools/astis_contributor_contract.py','check','--base','origin/main'])]
code="import subprocess,sys\npy=sys.executable\nchecks="+repr(checks)+"\nfor label,args in checks:\n subprocess.run([py,'-B','-X','utf8','.astis/pbps-harmonic73/foreground73.py','integration73/'+label,py,'-B','-X','utf8',*args],check=True)\nprint('PASS73 four bounded admission gates')\n"
(new/'small-gates73.py').write_text(code,encoding='utf8',newline='\n')
checks=[('official-graph-final',['website/scripts/underlying_lean_graph.py']),('graph-check-final',['tools/astis_publication.py','graph-check','--cell','ASTIS-SW-PBPS-actual-harmonic-flow']),('site-check-final',['website/scripts/check_site.py']),('publication-final',['tools/astis_publication.py','check','--base','origin/main']),('frontier-final',['tools/astis_frontier_cells.py','check']),('contributor-final',['tools/astis_contributor_contract.py','check','--base','origin/main']),('semantic-final',['tools/astis_semantic_roundtrip.py','check'])]
code="import subprocess,sys\npy=sys.executable\nchecks="+repr(checks)+"\nfor label,args in checks:\n subprocess.run([py,'-B','-X','utf8','.astis/pbps-harmonic73/foreground73.py','integration73/'+label,py,'-B','-X','utf8',*args],check=True)\nprint('PASS73 final graph/site/publication/frontier/contributor/semantic gates')\n"
(new/'final-gates73.py').write_text(code,encoding='utf8',newline='\n')
(new/'integration-helper-adaptations73.json').write_text(json.dumps(dict(status='EXACT_TARGET_PATH_ADAPTATIONS_AND_DYNAMIC_ONE_UNIT_SIX_STEPS',files=rows,canonical_scripts_changed=False,source_math_unchanged=True,prior_unchanged_general_python_and_browser_regressions_reuse_planned=True),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS73 helpers prepared: one dynamic full statement/six BODY steps/copy/download/branch; no gate or canonical mutation.')
