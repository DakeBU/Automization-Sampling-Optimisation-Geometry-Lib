from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-actual-prescribed-gibbs-survival98');out=r/'integration98/current-main';load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=r.parent/'pbps-actual-finite-first-event-law86/inspect_reader_html86.py'
source=old.read_text(encoding='utf8').split('run = Path(',1)[0]
ns={};exec(compile(source.replace('pbps-actual-finite-first-event-law','pbps-actual-prescribed-gibbs-survival'),str(old),'exec'),ns)
gate=load(r/'checks98/current-main-site-build/receipt.json');assert gate['terminal_closed'] and gate['exit_code']==0
page=Path('_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html')
p=ns['Unit']();p.feed(page.read_text(encoding='utf8'))
lesson=load('website/content/declaration_lessons/pbps-actual-prescribed-gibbs-survival.json')['units'][0]
assert p.found and p.steps==len(lesson['steps'])==6
assert p.details and all('open' not in d for d in p.details)
decl=lesson['declaration']
literal = decl.rsplit('.',1)[0]+'.actual_prescribed_gibbs_survival_statement'
assert p.events[:4]==[('lean',decl,'inline-lean inline-lean-statement'),('lean',literal,'inline-lean inline-lean-proof'),('roadmap','',''),('lean',decl,'inline-lean inline-lean-proof')],p.events[:4]
assert 'Full Lean proposition (definition) · actual_prescribed_gibbs_survival_statement' in page.read_text(encoding='utf8')
assert 'It supplies no mathematical proof or additional hypothesis' in page.read_text(encoding='utf8')
norm=lambda text:text.replace('\r\n','\n').strip()
for step in lesson['steps']:assert any(norm(step['lean'])==norm(code) for code in p.codes),step['title']
module=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedGibbsSurvival.lean');download=Path('_site/downloads/lean')/module
assert module.read_bytes()==download.read_bytes()
assert sha(module)=='f4856a5f059ef9875e481830cbd1a6152d7bc7de690ed325a71390a791098b95'
graph=load('_site/data/underlying-lean-graph.json');nodes=[x for x in graph['nodes'] if x['id']=='decl:'+decl];assert len(nodes)==1
data=dict(status='PASS_GENERATED_CONTENT_ONLY',page=page.as_posix(),page_raw_sha256=sha(page),exact_step_Lean_regions=6,details_initially_folded=len(p.details),reader_order='Exact folded signature and separately folded full proposition definition after mathematical statement; roadmap then exact folded full proof; six adjacent formula/Lean proof steps.',Lean_download=download.as_posix(),Lean_download_raw_sha256=sha(download),graph_node=nodes[0],graph_contract='Scanned references are not exhaustive kernel dependencies; independent exact science verification certifies actual parents.',actual_browser_page_viewed=False,interactive_branch_viewed=False,full_Exposition_Seal=False,Goal_complete=False)
(out/'offline-reader98.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf8',newline='\n')
print('Six exact proof regions, folded adjacent statement/proof, download and graph node checked. Browser acceptance pending.')
