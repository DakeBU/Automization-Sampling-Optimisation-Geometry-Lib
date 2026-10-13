"""Record local aggregate only, after terminal checks and actual SVG viewing."""
from pathlib import Path
import hashlib,json,re
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80');out=r/'integration80'
load=lambda p:json.loads(Path(p).read_bytes())
receipt=load(out/'canonical-lean-gate/receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed']
jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',(out/'canonical-lean-gate/stdout.log').read_text(encoding='utf8'))];assert len(jobs)==2,jobs
assert load(out/'python-compile/receipt.json')['exit_code']==0
assert load(out/'static-svg/viewed.json')['viewed_by_root'] is True
science=load(out/'integration-scope.json')['science_commit']
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-physical-time-measurability.json');b=cp.read_bytes();c=json.loads(b);assert c['status']=='independently_verified'
(out/'cell.before-final-admin80.snapshot.json').write_bytes(b)
c['evidence']['serialized_shared_gate']=dict(evidence=(out/'canonical-lean-gate/receipt.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=529,status='PASS',proof_commit=science,scope='Current local source-bound aggregate only; reader visual/main/PURIFIED/live remain separate.')
c['graph_contribution']['visual_review']='Static existing module SVG rasterized and actually viewed by root. Coarse shared-root view readable; precise actual phase dependency graph generated separately. Actual page/interactive branch visual acceptance pending because the bound browser surface has no inspectable tab. No full Exposition Seal.'
c['blocked']=dict(status=False,reason='Actual total joint phase measurability and fixed-parameter common-AE interpolation/initialization independently verified and local root/Tests aggregate passed. Path regularity/adaptedness/Markov/kernel/invariance/main/error/cost/composition remain open. Actual page visual acceptance and main/PURIFIED/live are separate.')
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
p=Path('docs/companion-papers-handoff.md');raw=p.read_bytes();nl=b'\r\n' if b'\r\n' in raw else b'\n'
old='carries this VERIFIED child. Serialized aggregate/site/graph and page visual\nadmission remain pending for this new integration snapshot.'.encode().replace(b'\n',nl);assert raw.count(old)==1
new=(f'carries this VERIFIED child. Local aggregate80 passed (root{jobs[0]},\nTests{jobs[1]}, Registry529), including canonical tools/astis.py check, ATLAS and\nfake-closure scans; py_compile passed. Publication/site/graph checks are bound\nin80 integration.notes.json. Static SVG was actually viewed; generated HTML\ncontent/folding is checked separately. Actual page/interactive branch visual\nacceptance remains pending because the bound browser surface has no inspectable\ntab.').encode().replace(b'\n',nl)
p.write_bytes(raw.replace(old,new,1))
(out/'final-admin.json').write_text(json.dumps(dict(root_jobs=jobs[0],test_jobs=jobs[1],registry_count=529,cell_RAW_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),source_statement_proof_lesson_unchanged=True,static_svg_viewed_by_root=True,browser_page_visual_pending=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Final local aggregate metadata',jobs,'Registry529; browser visual pending')
