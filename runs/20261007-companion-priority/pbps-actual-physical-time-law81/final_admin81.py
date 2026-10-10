"""Record local aggregate only, after terminal checks and actual SVG viewing."""
from pathlib import Path
import hashlib,json,re
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');out=r/'integration81'
load=lambda p:json.loads(Path(p).read_bytes())
receipt=load(out/'canonical-lean-gate/receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed']
jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',(out/'canonical-lean-gate/stdout.log').read_text(encoding='utf8'))];assert len(jobs)==2,jobs
assert load(out/'python-compile/receipt.json')['exit_code']==0
assert load(out/'static-svg/viewed.json')['viewed_by_root'] is True
science=load(out/'integration-scope.json')['science_commit']
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-ideal-half-turn-kernel.json');b=cp.read_bytes();c=json.loads(b);assert c['status']=='independently_verified'
(out/'cell.before-final-admin81.snapshot.json').write_bytes(b)
c['evidence']['serialized_shared_gate']=dict(evidence=(out/'canonical-lean-gate/receipt.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=530,status='PASS',proof_commit=science,scope='Current local source-bound aggregate only; reader visual/main/PURIFIED/live remain separate.')
c['graph_contribution']['visual_review']='Static existing module SVG rasterized and actually viewed by root. Coarse shared-root view readable; precise ideal initialized-kernel dependency graph generated separately. Actual page/interactive branch visual acceptance pending because the bound browser surface has no inspectable tab. No full Exposition Seal.'
c['blocked']=dict(status=False,reason='Ideal exact-reference returned-position probability kernel, actual independent product initialization and terminal live-arc agreement independently verified and local root/Tests aggregate passed. Random-input all-time/version uniqueness, process Markov/semigroup/invariance/mixing/implementation/main/error/cost/composition remain open. Actual page visual acceptance and main/PURIFIED/live are separate.')
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
p=Path('docs/companion-papers-handoff.md');raw=p.read_bytes();nl=b'\r\n' if b'\r\n' in raw else b'\n'
old='child; serialized aggregate/site/graph and reader visual acceptance are pending\nfor this snapshot.'.encode().replace(b'\n',nl);assert raw.count(old)==1
new=(f'child. Local aggregate81 passed (root{jobs[0]}, Tests{jobs[1]}, Registry530),\nincluding canonical tools/astis.py check, ATLAS and fake-closure scans; py_compile\npassed. Publication/site/graph checks are bound in81 integration.notes.json.\nStatic SVG was actually viewed and generated HTML content/folding checked. Actual\npage/interactive branch visual acceptance remains pending because the bound\nbrowser surface has no inspectable tab.').encode().replace(b'\n',nl)
p.write_bytes(raw.replace(old,new,1))
(out/'final-admin.json').write_text(json.dumps(dict(root_jobs=jobs[0],test_jobs=jobs[1],registry_count=530,cell_RAW_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),source_statement_proof_lesson_unchanged=True,static_svg_viewed_by_root=True,browser_page_visual_pending=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Final local aggregate metadata',jobs,'Registry530; browser visual pending')
