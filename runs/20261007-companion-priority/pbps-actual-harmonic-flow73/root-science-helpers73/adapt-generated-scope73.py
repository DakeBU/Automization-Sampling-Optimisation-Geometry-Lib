from pathlib import Path
import hashlib,json
old=Path('.astis/pbps-perturbation72');new=Path('.astis/pbps-harmonic73');rows=[]
changes=[('pbps-b4-corrector-perturbation72','pbps-actual-harmonic-flow73'),('pbps-perturbation72','pbps-harmonic73'),('ActualCorrectorPerturbation','ActualHarmonicFlow'),('actual-corrector-perturbation','actual-harmonic-flow'),('root.exact-verification72','root.exact-verification73'),('integration72','integration73'),('BOUNDED72','BOUNDED73'),('pre-generator72','pre-generator73'),('PASS72','PASS73')]
for name in ['prepare-generated-scope72.py','narrow-generated-scope72.py']:
 p=old/name;s=p.read_text(encoding='utf8')
 for a,b in changes:s=s.replace(a,b)
 s=s.replace(",'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.md'",'')
 dest=new/name.replace('72.','73.');assert not dest.exists();dest.write_text(s,encoding='utf8',newline='\n')
 rows.append(dict(source=p.as_posix(),source_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),adapted=dest.as_posix(),adapted_RAW_sha256=hashlib.sha256(dest.read_bytes()).hexdigest()))
(new/'generated-scope-helper-adaptations73.json').write_text(json.dumps(dict(status='ONE_CURRENT_BRANCH_GENERATOR_SCOPE_WITH_BACKUP_ONLY',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS73 prepared one-branch generator scope helpers; no generator/canonical writes.')
