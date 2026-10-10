"""Check generated content only; deliberately does not certify a browser view."""
from pathlib import Path
import hashlib,json,importlib.util
r=Path(__file__).parent
old=r.parent/'pbps-actual-finite-first-event-law86/inspect_reader_html86.py'
# Reuse the reviewed bounded unit parser without executing its old top-level checks.
source=old.read_text(encoding='utf8').split("run = Path(",1)[0]
source=source.replace('pbps-actual-finite-first-event-law','pbps-actual-conditional-next-wait-density')
ns={};exec(compile(source,str(old),'exec'),ns)
load=lambda p:json.loads(Path(p).read_bytes())
gate=load(r/'checks89/site-build/receipt.json');assert gate['terminal_closed'] and gate['exit_code']==0
page=Path('_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html')
p=ns['Unit']();p.feed(page.read_text(encoding='utf8'))
lesson=load('website/content/declaration_lessons/pbps-actual-conditional-next-wait-density.json')['units'][0]
assert p.found and p.steps==len(lesson['steps'])==6
assert len(p.details)==13 and all('open' not in d for d in p.details)
decl=lesson['declaration'];spec=decl+'_statement'
assert p.events[:3]==[('lean',decl,'inline-lean inline-lean-statement'),('lean',spec,'inline-lean inline-lean-proof'),('roadmap','','')]
assert sum(e[1]==spec for e in p.events)==1
for step in lesson['steps']:assert any(step['lean'].strip()==code.strip() for code in p.codes),step['title']
out=r/'integration89/offline-reader.json';assert not out.exists()
out.write_text(json.dumps(dict(status='PASS_GENERATED_HTML_CONTENT_ONLY',page=page.as_posix(),page_RAW_sha256=hashlib.sha256(page.read_bytes()).hexdigest(),exact_step_Lean_regions=6,details_initially_folded=13,literal_statement_adjacent_before_roadmap=True,actual_browser_page_viewed=False,interactive_branch_viewed=False,remaining='Browser connection currently exposes no tabs; visual acceptance, live deployment and postmerge purification remain open.'),indent=2)+'\n',encoding='utf8',newline='\n')
print('Generated actual89 unit: six exact BODY regions, thirteen initially folded disclosures; no browser credit.')
