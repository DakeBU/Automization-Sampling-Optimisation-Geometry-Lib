from pathlib import Path
import json,hashlib
r=Path(__file__).parent;old=r.parent/'pbps-actual-conditional-next-wait-survival88';rows=[]
for name in ['refresh_graph','inspect_generated_reader','inspect_generated_bindings','record_integration','commit_integration','push_integration']:
 source=old/(name+'88.py');p=r/(name+'89.py');assert not p.exists()
 s=source.read_text(encoding='utf8')
 for a,b in [('survival88','density89'),('integration88','integration89'),('independent-math88','independent-math89'),('independent-source88','independent-source89'),('verification88','verification89'),('verified88','verified89'),('VERIFIED88','VERIFIED89'),('checks88','checks89'),('next-wait-preread88','next-wait-density-preread89'),('pre-fetch88','pre-fetch89'),('source-review88','source-review89'),('bindings88','bindings89'),('archives88','archives89'),('scope88','scope89'),('INTEGRATION88','INTEGRATION89'),('ActualConditionalNextWaitSurvival','ActualConditionalNextWaitDensity'),('actual-conditional-next-wait-survival','actual-conditional-next-wait-density'),('conditional next-wait survival','conditional finite next-wait density'),('2f509ce49343d349f7a9fb21d2f7b1697c1a6de942353f6cd8ff16d522911569','36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37'),('kernel-dependency-summary88.json','kernel-dependency89.json'),('registry_count=537','registry_count=538')]:s=s.replace(a,b)
 if name=='record_integration':
  s=s.replace("science_commit='456e13f9561abcf01a285133e91b3951bf2ed892'","science_commit=load(out/'integration-scope.json')['science_commit']")
  s=s.replace('One actual deterministic-depth history-dependent next-wait survival theorem. Exact kernel audit certifies actual87 history/tail law, actual75 integrated hazard and actual77 iid product as immediate public ASTIS parents; private/generated closure is certified separately.','One actual conditional strict finite next-wait density and genuine subprobability kernel theorem. Exact kernel audit certifies six immediate public ASTIS parents: actual87 history/tail, actual86 deterministic density, actual75 hazard, actual flow/rate and actual77 iid product; actual88 is not a dependency. Private/generated closure is certified separately.')
 if name=='commit_integration':
  s=s.replace("=='456e13f9561abcf01a285133e91b3951bf2ed892'","==load(out/'integration-scope.json')['science_commit']")
  s=s.replace("and not p.name.endswith('.text.txt')","and not p.name.endswith('.text.txt') and sha(p.read_bytes())!='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'")
 if name=='inspect_generated_reader':
  s=s.replace("==5","==6").replace("==11","==13").replace("exact_step_Lean_regions=5","exact_step_Lean_regions=6").replace("details_initially_folded=11","details_initially_folded=13").replace('actual88 unit: five','actual89 unit: six').replace('eleven initially','thirteen initially')
 p.write_text(s,encoding='utf8',newline='\n')
 rows.append(dict(path=p.as_posix(),template=source.as_posix(),template_RAW_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),status='PREPARED_NOT_EXECUTED_REQUIRES_VERIFIED_AND_SOLE_LANE'))
(r/'integration-helper89-provenance.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8',newline='\n')
print('Prepared sole-lane integration helpers; no shared mutation executed.')
