from pathlib import Path
import ast, re
old=Path('.astis/pbps-bounce74');new=Path('.astis/pbps-clock75')
def adapt(s):
 for a,b in [('pbps-actual-bounce-rate74','pbps-actual-hazard-clock75'),('pbps-bounce74','pbps-clock75'),('ActualBounceRate.actual_bounce_rate_energy_laws','ActualHazardClock.actual_integrated_hazard_clock_laws'),('ActualBounceRate','ActualHazardClock'),('actual-bounce-rate','actual-hazard-clock')]:s=s.replace(a,b)
 s=re.sub(r'74(?![0-9a-f])','75',s)
 return s.replace('523','524').replace('244','245').replace('211','396')
for name in ['prepare-generated-scope74.py','record-viewed74.py','record-integration74.py','freeze-final-reader74.py','commit-integration74.py','adopt-repository74.py']:
 s=adapt((old/name).read_text(encoding='utf8'))
 if name=='record-viewed74.py':
  s=s.replace('==10','==12').replace('TEN_CURRENT','TWELVE_CURRENT').replace('seven BODY','nine BODY').replace('ten-PNG','twelve-PNG')
 if name=='record-integration74.py':
  s=s.replace("len(capture['records'])==9","len(capture['records'])==11").replace("len(lesson['steps'])==7","len(lesson['steps'])==9").replace("len(viewed['images'])==10","len(viewed['images'])==12").replace('formula_BODY_steps=7','formula_BODY_steps=9').replace('seven formula/BODY','nine formula/BODY')
  s=s.replace('Deterministic bounce/rate/energy-layer laws accepted','Actual first-hazard clock laws accepted').replace('Actual clock/recursive PDMP/invariance/nonexplosion remain open','Actual recursive PDMP/invariance/nonexplosion remain open')
  s=s.replace('One actual deterministic bounce/rate/energy-layer theorem; internal canonical gradient-Lipschitz producer and pinned Mathlib reflection dependencies. No conceptual formal edge or stochastic consumer claim.','One actual integrated-hazard/first-clock theorem with actual flow and bounce/rate formal parents, internal primitive/closed-hitting/Exp pushforward APIs. No conceptual formal edge, full recursive path or invariance claim.')
  s=s.replace('Actual clocks/recursive PDMP/nonexplosion/invariance','Recursive PDMP/nonexplosion/invariance')
 if name=='freeze-final-reader74.py':
  s=s.replace('formula_BODY_steps=7','formula_BODY_steps=9').replace('actual_captures=10','actual_captures=12')
  s=s.replace('root.reader-metadata-overlay75.adoption.json','root.review-input-metadata75.adoption.json').replace('source-review.packet.json','source-review.clean.packet.json')
  s=s.replace("'integration75/generator-sideeffects/receipt.json',",'')
  s=s.replace("paths.extend(p for p in (r/'integration75/generator-line-ending-diagnosis').iterdir() if p.is_file())",'')
  start=s.index("for label in ['narrow-generated-scope'");end=s.index("paths.extend((r/'integration75').glob",start);s=s[:start]+s[end:]
  s=s.replace("paths.extend((r/'integration75').glob", "paths.extend(r/'integration75/affected-module-graph'/p for p in ['receipt.json','stdout.log','stderr.log','affected-graph.receipt.json'])\npaths.extend((r/'integration75').glob")
 if name=='adopt-repository74.py':
  s=s.replace("d['formula_BODY_steps']==7","d['formula_BODY_steps']==9").replace("d['independently_viewed_PNGs']==10","d['independently_viewed_PNGs']==12")
 if name=='commit-integration74.py':
  s=s.replace('future75_not_admitted','future76_not_admitted').replace('future75_not_staged','future76_not_staged')
  s=s.replace("r.parent/'pbps-clock-preproof75'","r.parent/'pbps-recursive-path-preread76'").replace("r.parent/'pbps-clock-construction-preread75'","r.parent/'pbps-recursive-preproof76'")
  s=s.replace('Integrate independently verified PBPS bounce and rate laws','Integrate independently verified PBPS first hazard clock')
 ast.parse(s);dest=new/name.replace('74.','75.');assert not dest.exists(),dest;dest.write_text(s,encoding='utf8',newline='\n')
print('PASS75 six bounded delivery helpers prepared; no canonical mutation or validation credit.')
