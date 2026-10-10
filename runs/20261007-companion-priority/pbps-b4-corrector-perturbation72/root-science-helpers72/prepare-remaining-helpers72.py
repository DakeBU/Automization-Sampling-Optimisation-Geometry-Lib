from pathlib import Path
old=Path('.astis/pbps-corrector71');new=Path('.astis/pbps-perturbation72')
changes=[('pbps-actual-corrector-change71','pbps-b4-corrector-perturbation72'),('pbps-corrector71','pbps-perturbation72'),('ActualCorrectorChange.actual_corrector_change','ActualCorrectorPerturbation.actual_corrector_perturbation'),('ActualCorrectorChange','ActualCorrectorPerturbation'),('actual-corrector-change','actual-corrector-perturbation'),('root.exact-verification71','root.exact-verification72'),('root.repository71','root.repository72'),('root.source71','root.source72'),('integration71','integration72'),('visual71','visual72'),('helpers71','helpers72'),('SCI71','SCI72'),('PASS71','PASS72'),('Registry519','Registry521'),('registry_count=519','registry_count=521'),('240publication','242publication')]
for name in ['narrow-generated-scope71.py','commit-integration71.py','safe-fetch-before-integration71.py','github-integration71.py']:
 s=(old/name).read_text(encoding='utf8')
 for a,b in changes:s=s.replace(a,b)
 if name=='narrow-generated-scope71.py':
  needle="'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.md']"
  assert needle in s;s=s.replace(needle,"'research-wiki/sampling-sde-library/cards/AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.md','research-wiki/sampling-sde-library/cards/AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorPerturbation.md']")
 if name=='commit-integration71.py':
  s=s.replace("assert head=='4e7ce5d2996ffe1d1b0ab570778e02425c6be34e'","assert head==load(r/'root.exact-verification72.adoption.json')['verified_commit']")
  s=s.replace('future72','future73').replace('preproof72','preread73').replace('actual corrector change','actual corrector perturbation')
 if name=='github-integration71.py':
  s=s.replace("assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()=='4e7ce5d2996ffe1d1b0ab570778e02425c6be34e'","assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()==json.loads((r/'root.exact-verification72.adoption.json').read_bytes())['verified_commit']")
  s=s.replace("before=='d8342abe2747438af6738b03a06224c85bad08b3'","before=='1e9d2feb727919ebaa17ee1a67b629a0b85b0ba9'")
  s=s.replace('pr315-body71.md','pr315-body72.md').replace('Prove PBPS actual projected rotation and exact corrector change','Prove actual PBPS corrector change and perturbation')
 dest=new/name.replace('71.','72.');assert not dest.exists();dest.write_text(s,encoding='utf8',newline='\n')
print('PASS prepared remaining72 finite Git/generated-scope helpers; no execution or canonical changes.')
