from pathlib import Path
import ast,hashlib,json,os
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR']); rows=[]
for name in ['adopt-math74.py','small-gates74.py']:
 p=Path('.astis/pbps-bounce74')/name;s=p.read_text(encoding='utf8')
 for a,b in [('pbps-actual-bounce-rate74','pbps-actual-hazard-clock75'),('pbps-bounce74','pbps-clock75'),('74','75')]:s=s.replace(a,b)
 dest=Path('.astis/pbps-clock75')/name.replace('74.','75.');assert not dest.exists();ast.parse(s);dest.write_text(s,encoding='utf8',newline='\n')
 rows.append(dict(source=p.as_posix(),source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),adapted=dest.as_posix(),adapted_RAW_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(out/'helper-adaptations.json').write_text(json.dumps(dict(actual_root_PID=os.getpid(),files=rows,canonical_mutations=False,mathematical_credit=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS75 bounded review helpers prepared; no verdict or canonical mutation.')
