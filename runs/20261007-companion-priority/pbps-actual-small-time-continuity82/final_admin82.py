from pathlib import Path
import hashlib,json,re
r=Path(__file__).parent;out=r/'integration82';load=lambda p:json.loads(Path(p).read_bytes())
receipt=load(out/'canonical-lean-gate/receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed']
jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',(out/'canonical-lean-gate/stdout.log').read_text(encoding='utf8'))];assert len(jobs)==2,jobs
assert load(out/'python-compile/receipt.json')['exit_code']==0
assert load(out/'static-svg/viewed.json')['viewed_by_root'] is True
science=load(out/'integration-scope.json')['science_commit']
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-small-time-continuity.json');b=cp.read_bytes();c=json.loads(b);assert c['status']=='independently_verified'
(out/'cell.before-final-admin82.snapshot.json').write_bytes(b)
c['evidence']['serialized_shared_gate']=dict(evidence=(out/'canonical-lean-gate/receipt.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=531,status='PASS',proof_commit=science,scope='Current local source-bound aggregate only; actual reader visual/main/PURIFIED/live separate.')
c['graph_contribution']['visual_review']='Current affected coarse shared-root SVG rendered and actually viewed, with exact RAW input/output pins. Precise new actual small-time dependency graph generated and checked. Actual page/interactive visual acceptance still pending; no full Exposition Seal.'
c['blocked']=dict(status=False,reason='Actual first-event phase-flow defect and zero-time stochastic continuity independently verified and local aggregate passed. Full L2/Markov/restart/semigroup/invariance/hypocoercivity/main/implementation/error/cost/composition remain open. Reader actual visual/main/PURIFIED/live separate.')
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
p=Path('docs/companion-papers-handoff.md');raw=p.read_bytes();nl=b'\r\n' if b'\r\n' in raw else b'\n'
old='This VERIFIED child uses the sole existing stabilization lane. Local aggregate,\nreader visual/main merge/PURIFIED/live and full-paper/Goal completion are separate.'.encode().replace(b'\n',nl);assert raw.count(old)==1
new=(f'This VERIFIED child uses the sole existing stabilization lane. Local aggregate82\npassed (root{jobs[0]}, Tests{jobs[1]}, Registry531), including tools/astis.py check,\nATLAS/fake-closure scans and py_compile. Current publication/semantic/frontier/site\n/graph checks are bound in82 integration.notes.json. Generated HTML content and\ninitially folded exact Lean regions passed. Current affected static SVG was rendered\nand actually viewed with exact RAW pins. Actual reader page/interactive visual acceptance, main\nmerge/PURIFIED/live and full-paper/Goal completion remain separate.').encode().replace(b'\n',nl)
p.write_bytes(raw.replace(old,new,1))
(out/'final-admin.json').write_text(json.dumps(dict(root_jobs=jobs[0],test_jobs=jobs[1],registry_count=531,cell_RAW_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),source_statement_proof_lesson_unchanged=True,static_svg_viewed_by_root=True,browser_page_visual_pending=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Final local aggregate metadata',jobs,'Registry531; actual browser visual pending')
