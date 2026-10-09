from pathlib import Path
import hashlib,json
old=Path('.astis/pbps-actual-rotation70');new=Path('.astis/pbps-corrector71')
replacements=[('pbps-actual-projected-rotation70','pbps-actual-corrector-change71'),('pbps-actual-rotation70','pbps-corrector71'),('ActualProjectedRotation.actual_projected_rotation','ActualCorrectorChange.actual_corrector_change'),('ActualProjectedRotation','ActualCorrectorChange'),('actual-projected-rotation','actual-corrector-change'),('integration70','integration71'),('visual70','visual71'),('foreground-integration70','foreground-integration71'),('mandatory70','mandatory71'),('small70','small71'),('final70','final71'),('bounded70','bounded71')]
rows=[]
for name in ['small-gates70.py','final-gates70.py','scope-gates70.py','inspect-cdp70.mjs','inspect-copy70.mjs','run-browser70.py','python-regression70.py']:
 p=old/name;text=p.read_text(encoding='utf8')
 for a,b in replacements:text=text.replace(a,b)
 dest=new/name.replace('70.','71.');assert not dest.exists();dest.write_text(text,encoding='utf8',newline='\n')
 rows.append(dict(source=p.as_posix(),source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),adapted=dest.as_posix(),adapted_RAW_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
p=new/'integration-helper-adaptations71.json';assert not p.exists();p.write_text(json.dumps(dict(status='UNCHANGED_REVIEWED_LOGIC_ONLY_TARGET_PATH_AND_LABEL_ADAPTATION',replacements=replacements,files=rows,canonical_scripts_changed=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS prepared target71 integration observers/browser/regression using reviewed70 logic.')
