from pathlib import Path
old=Path('.astis/pbps-root-commutation67');new=Path('.astis/pbps-sharp-energy68')
replacements=[('pbps-root-commutation67','pbps-sharp-energy68'),('integration67','integration68'),('verification67','verification68'),('repository67','repository68'),('visual67','visual68'),('record-integration67','record-integration68'),('root-integration-helpers67','root-integration-helpers68'),('ASTIS-SHARED-l2-real-positive-square-commutation','ASTIS-SHARED-hilbert-corrector-square-bound'),('ASTIS-SW-PBPS-actual-root-inverse-commutation','ASTIS-SW-PBPS-sharp-corrector-energy'),('AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute','AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound'),('AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation','AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy'),('3da29415011a971a65f749502a625e416213f487','3ad3b127b5a645be9cf71b3d14520b2d8fea3122')]
for name in ['record-integration67.py','commit-integration67.py']:
 text=(old/name).read_text(encoding='utf-8')
 for a,b in replacements:text=text.replace(a,b)
 text=text.replace('514','516').replace('235','237')
 if name.startswith('record'):
  text=text.replace("== 13","== 14").replace('[4, 6][i]','[5, 6][i]')
  text=text.replace('all ten formula/BODY','all eleven formula/BODY').replace('ten exact formula steps','eleven exact formula steps')
  text=text.replace("anchor = 'Serialized Registry516/imports/Tests and current reader/graph gates are pending.'","anchor = 'Serialized Registry516/imports/Tests/current reader/graph gates for\\nthis cycle are pending and must be recorded against final admin state.'")
  text=text.replace('same-root/inverse commutation scope','sharp corrector energy scope')
  text=text.replace('SERIALIZED_SHARED_AGGREGATE67','SERIALIZED_SHARED_AGGREGATE68').replace('aggregate67','aggregate68').replace('admin67','admin68')
  text=text.replace('One generic positive-square commutation leaf, one same-actual-root/inverse theorem and genuine coefficient consumer; exact compiled edges and two cards only. No conceptual formal edge.','One generic sharp Hilbert quadratic leaf, the same-actual PBPS sharp corrector theorem and genuine modified-energy Test consumer; one evidenced PBPS route, exact compiled edges and two cards only. No conceptual formal edge.')
  text=text.replace('Sharp B23/LemmaB3 energy/B21/H1/dynamics/main/errors/expectedquerycost/composition remain open.','B21/H1/B4 dynamics/invariance/nonexplosion/main/errors/caps/expectedquerycost/actual-input composition remain open.')
 else:
  text=text.replace("shared+=['research-wiki/frontier-cells/","shared += ['website/content/declaration_lessons/hilbert-sharp-quadratic-corrector-bound.json', 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound.json']\nshared+=['research-wiki/frontier-cells/")
  text=text.replace('pbps-sharp-energy-preproof68','pbps-reflection-rotation-preproof69').replace('future68','future69')
  text=text.replace('Integrate verified PBPS root commutation and corrector coefficient geometry','Integrate verified PBPS sharp corrector bound and modified energy equivalence')
 destination=new/name.replace('67','68');assert not destination.exists();destination.write_text(text,encoding='utf-8',newline='\n')
print('Prepared record/commit68 helpers; no canonical or Git writes.')
