from pathlib import Path
import hashlib,json
r=Path(__file__).parent
source=r.parent/'pbps-actual-conditional-next-wait-survival88/check88.py'
p=r/'check89.py';assert not p.exists()
s=source.read_text(encoding='utf8').replace('checks88','checks89').replace('24210c17b36c608fec3c259f811430cc9fc148cf','7c108c3181cee58bb9305445f903c5f71efda9c5').replace('actual-conditional-next-wait-survival','actual-conditional-next-wait-density').replace('ActualConditionalNextWaitSurvival.lean','ActualConditionalNextWaitDensity.lean')
s=s.replace('Actual deterministic-depth history-dependent survival only;','Actual conditional strict finite next-wait density and genuine subprobability kernel only;')
p.write_text(s,encoding='utf8',newline='\n')
(r/'check89-template-provenance.json').write_text(json.dumps(dict(template=str(source),template_RAW_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),changes=['new receipt directory','exact pre89 base commit','new density cell/module','explicit bounded density scope'],canonical_tooling_modified=False),indent=2)+'\n',encoding='utf8',newline='\n')
