from pathlib import Path
import ast,json
old=Path('.astis/pbps-harmonic73');new=Path('.astis/pbps-bounce74')
def adapt(s):
 for a,b in [('pbps-actual-harmonic-flow73','pbps-actual-bounce-rate74'),('pbps-harmonic73','pbps-bounce74'),('73','74')]:s=s.replace(a,b)
 return s
s=adapt((old/'adopt-repository73.py').read_text(encoding='utf8'))
for a,b in [("d['formula_BODY_steps']==6","d['formula_BODY_steps']==7"),("d['independently_viewed_PNGs']==9","d['independently_viewed_PNGs']==10"),("d['Registry']==522","d['Registry']==523"),("d['publication_units']==243","d['publication_units']==244")]:s=s.replace(a,b)
ast.parse(s);p=new/'adopt-repository74.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
s=adapt((old/'commit-integration73.py').read_text(encoding='utf8'))
start=s.index('paths=list(dict.fromkeys(');end=s.index('\nassert all(Path(p).is_file()',start)
s=s[:start]+"paths=list(dict.fromkeys(shared+[p.as_posix() for p in r.rglob('*') if p.is_file() and not p.resolve().is_relative_to(active)]))"+s[end:]
s=s.replace("assert not any('preread74' in p or 'preproof74' in p or 'pbps-macro-root63' in p for p in paths)","assert not any(p.startswith((r.parent/'pbps-clock-preproof75').as_posix()+'/') or p.startswith((r.parent/'pbps-clock-construction-preread75').as_posix()+'/') or 'pbps-macro-root63' in p for p in paths)")
s=s.replace("p.startswith(r.as_posix()+'/') or p.startswith((r72/'reader-observation-correction72').as_posix()+'/') or p.startswith((r72/'safe-fetch-before74').as_posix()+'/')","p.startswith(r.as_posix()+'/')")
s=s.replace('future74_not_admitted','future75_not_admitted').replace('future74_not_staged','future75_not_staged').replace('Integrate independently verified PBPS harmonic flow','Integrate independently verified PBPS bounce and rate laws')
ast.parse(s);p=new/'commit-integration74.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
s=adapt((old/'github-integration73.py').read_text(encoding='utf8')).replace('bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19','e91f9b3acfeea172c33053b28d88b7fea6e61e9d').replace('Prove actual PBPS corrector algebra and harmonic flow','Prove actual PBPS flow, bounce and jump-rate laws')
ast.parse(s);p=new/'github-integration74.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
s=adapt((old/'safe-fetch-before-integration73.py').read_text(encoding='utf8'));ast.parse(s);p=new/'safe-fetch-before-integration74.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
print('PASS74 delivery helpers: scoped r74 only; future75 directories excluded; no canonical/Git mutation.')
