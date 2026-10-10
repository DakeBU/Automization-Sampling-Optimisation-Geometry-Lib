"""Finalize local aggregate metadata only after actual SVG viewing."""
from pathlib import Path
import hashlib,json,re
r=Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78');out=r/'integration78'
load=lambda p:json.loads(Path(p).read_bytes())
receipt=load(out/'canonical-lean-gate/receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed']
jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',(out/'canonical-lean-gate/stdout.log').read_text(encoding='utf8'))];assert len(jobs)==2,jobs
assert load(out/'python-compile/receipt.json')['exit_code']==0
viewed=load(out/'static-svg/viewed.json');assert viewed['viewed_by_root'] is True
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-event-time-nonaccumulation.json');b=cp.read_bytes();c=json.loads(b);assert c['status']=='independently_verified'
(out/'cell.before-final-admin78.snapshot.json').write_bytes(b)
c['evidence']['serialized_shared_gate']=dict(evidence=(out/'canonical-lean-gate/receipt.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=527,status='PASS',proof_commit='bbcad09376c51bbf27c0ed4c16be0dc053bb01c5',scope='Current local source-bound aggregate only; reader visual/main/PURIFIED/live remain separate.')
c['graph_contribution']['visual_review']='Static existing module SVG rasterized and actually viewed by root; coarse shared-root view readable, individual actual source consumer is in separately generated precise graph. Browser page/interactive branch visual acceptance pending: discovered runtime had no inspectable browser tab. No full Exposition Seal.'
c['blocked']=dict(status=False,reason='Actual nonaccumulation independently verified and local root/Tests aggregate passed; downstream physical-time interval/trajectory/Markov/invariance/main/cost/composition remain open. Site checks and actual page visual acceptance are separate.')
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
p=Path('docs/companion-papers-handoff.md');raw=p.read_bytes();nl=b'\r\n' if b'\r\n' in raw else b'\n'
old='aggregate/site/graph and page visual admission remain pending for this new\nintegration snapshot.'.encode().replace(b'\n',nl);assert raw.count(old)==1
new=(f'local aggregate78 passed (root{jobs[0]}, Tests{jobs[1]}, Registry527), including\n'
 'canonical tools/astis.py check, ATLAS and fake-closure scans; py_compile passed.\n'
 'Publication/site/graph checks are recorded in78 integration.notes.json. Static\n'
 'module SVG was actually viewed; browser page/interactive branch visual\n'
 'acceptance remains pending because the available browser surface has no\n'
 'inspectable tab.').encode().replace(b'\n',nl)
p.write_bytes(raw.replace(old,new,1))
(out/'final-admin.json').write_text(json.dumps(dict(root_jobs=jobs[0],test_jobs=jobs[1],registry_count=527,cell_RAW_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),source_statement_proof_lesson_unchanged=True,static_svg_viewed_by_root=True,browser_page_visual_pending=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Final local aggregate metadata',jobs,'Registry527; browser visual pending')
