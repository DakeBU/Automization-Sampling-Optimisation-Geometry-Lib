from pathlib import Path
import hashlib,json
old=Path('.astis/pbps-perturbation72');new=Path('.astis/pbps-harmonic73');rows=[]
changes=[('pbps-b4-corrector-perturbation72','pbps-actual-harmonic-flow73'),('pbps-perturbation72','pbps-harmonic73'),('root.exact-verification72','root.exact-verification73'),('root.repository72','root.repository73'),('integration72','integration73'),('safe-fetch-before-integration72','safe-fetch-before-integration73'),('pr315-body72','pr315-body73'),('1e9d2feb727919ebaa17ee1a67b629a0b85b0ba9','bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19'),('Prove actual PBPS corrector change and perturbation','Prove actual PBPS corrector algebra and harmonic flow')]
for name in ['safe-fetch-before-integration72.py','github-integration72.py']:
 p=old/name;s=p.read_text(encoding='utf8')
 for a,b in changes:s=s.replace(a,b)
 dest=new/name.replace('72.','73.');assert not dest.exists();dest.write_text(s,encoding='utf8',newline='\n')
 rows.append(dict(source=p.as_posix(),source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),adapted=dest.as_posix(),adapted_RAW_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(new/'git-helper-adaptations73.json').write_text(json.dumps(dict(status='REGULAR_FAST_FORWARD_PUSH_ONLY_EXISTING_PR315',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS73 safe fetch/ordinary push/existingPR helpers prepared; no network mutation executed.')
