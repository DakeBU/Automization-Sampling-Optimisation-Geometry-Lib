from pathlib import Path
import hashlib,json
r=Path(__file__).parent;out=r/'integration93';load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=r.parent/'pbps-actual-finite-first-event-law86/inspect_reader_html86.py'
source=old.read_text(encoding='utf8').split('run = Path(',1)[0]
ns={};exec(compile(source.replace('pbps-actual-finite-first-event-law','pbps-actual-finite-count-path'),str(old),'exec'),ns)
gate=load(r/'checks93/integration-site-build-current-gate/receipt.json');assert gate['terminal_closed'] and gate['exit_code']==0
page=Path('_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html')
p=ns['Unit']();p.feed(page.read_text(encoding='utf8'))
lesson=load('website/content/declaration_lessons/pbps-actual-finite-count-path.json')['units'][0]
assert p.found and p.steps==len(lesson['steps'])==9
assert p.details and all('open' not in d for d in p.details)
decl=lesson['declaration'];spec=decl.removesuffix('_law')+'_statement'
assert p.events[:3]==[('lean',decl,'inline-lean inline-lean-statement'),('lean',spec,'inline-lean inline-lean-proof'),('roadmap','','')]
assert sum(e[1]==spec for e in p.events)==1
normalize_text = lambda text: text.replace('\r\n', '\n').strip()
for step in lesson['steps']:assert any(normalize_text(step['lean'])==normalize_text(code) for code in p.codes),step['title']
module=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean');download=Path('_site/downloads/lean')/module
assert module.read_bytes()==download.read_bytes()
assert sha(module)=='5467078f497e0d40e1916550b2e5e9a5be992a69b20fc143bda06dd988d86d9d'
graph=load('_site/data/underlying-lean-graph.json');nodes=[x for x in graph['nodes'] if x['id']=='decl:'+decl];assert len(nodes)==1
data=dict(status='PASS_GENERATED_CONTENT_ONLY',page=page.as_posix(),page_raw_sha256=sha(page),exact_step_Lean_regions=9,html_text_comparison='CRLF normalized to LF only; source/download retain exact RAW byte comparison',details_initially_folded=len(p.details),literal_statement_adjacent_before_roadmap=True,Lean_download=download.as_posix(),Lean_download_raw_sha256=sha(download),graph_node=nodes[0],graph_contract='Name-scan references are not exhaustive kernel dependencies; exact dependencies are certified by independent review.',actual_browser_page_viewed=False,interactive_branch_viewed=False,full_Exposition_Seal=False,Goal_complete=False)
(out/'offline-reader.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf8',newline='\n')
print('Generated nine-step reader and exact Lean download checked; no browser credit.')
