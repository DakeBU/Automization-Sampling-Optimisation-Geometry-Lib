from pathlib import Path
import hashlib,json,re
r=Path(__file__).parent;out=r/'integration86';load=lambda p:json.loads(Path(p).read_bytes())
receipt=load(out/'canonical-lean-gate/receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed']
jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',(out/'canonical-lean-gate/stdout.log').read_text(encoding='utf8'))];assert len(jobs)==2,jobs
assert load(out/'python-compile/receipt.json')['exit_code']==0
assert load(out/'static-svg/viewed.json')['viewed_by_root'] is True
science=load(out/'integration-scope.json')['science_commit']
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-first-event-law.json');b=cp.read_bytes();c=json.loads(b);assert c['status']=='independently_verified'
(out/'cell.before-final-admin86.snapshot.json').write_bytes(b)
c['evidence']['serialized_shared_gate']=dict(evidence=(out/'canonical-lean-gate/receipt.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=535,status='PASS',proof_commit=science,scope='Local source-bound aggregate; actual page visual/main/PURIFIED/live separate.')
c['graph_contribution']['visual_review']='Current coarse shared-root SVG rendered and actually viewed with RAW pins. New actual86 declaration admitted by checked reference graph; generated name-scanned references are incomplete signals. Four actual public producer parents and complete private/generated closure separately certified by independent kernel audit, unchanged by reviewed EOF cleanup. Actual reader/interactive visual pending; no full Exposition Seal.'
c['blocked']=dict(status=False,reason='First finite-event time density and same post-bounce marked law, finite subprobability mass and bounded Borel three-L1/integral theorem independently verified; local aggregate passed. Unused-tail/fullA7/path/reversal/invariance/Markov/allL2/main/implementation/error/unbounded costs/composition OPEN. Actual reader visual/main/PURIFIED/live separate.')
cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
p=Path('docs/companion-papers-handoff.md');raw=p.read_bytes();nl=b'\r\n' if b'\r\n' in raw else b'\n'
old='This VERIFIED child uses the existing sole stabilization lane. Local aggregate,\nactual reader/interactive graph, main merge/PURIFIED/live and complete-paper/Goal\ncompletion are distinct; no whole-paper completion is claimed.'.encode().replace(b'\n',nl);assert raw.count(old)==1
new=(f'This VERIFIED child uses the existing sole stabilization lane. Local aggregate86\npassed (root{jobs[0]}, Tests{jobs[1]}, Registry535), including tools/astis.py check,\nfake-closure scans and py_compile. Current contributor/publication/semantic/frontier/\ngraph/site checks are bound in86 integration.notes.json. The separately reviewed V4\nreader places complete exact literal statements before the roadmap, and all eleven\nproof steps retain adjacent initially folded exact Lean. The current coarse SVG was\nrendered and actually viewed. Generated name-scanned references remain distinct from\nindependently certified kernel dependencies. Actual reader/interactive graph visual\nacceptance, main merge/PURIFIED/live and complete-paper/Goal remain separate.').encode().replace(b'\n',nl)
p.write_bytes(raw.replace(old,new,1))
(out/'final-admin.json').write_text(json.dumps(dict(root_jobs=jobs[0],test_jobs=jobs[1],registry_count=535,cell_RAW_sha256=hashlib.sha256(cp.read_bytes()).hexdigest(),source_statement_proof_lesson_unchanged=True,static_svg_viewed_by_root=True,browser_page_visual_pending=True,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Final local aggregate metadata',jobs,'Registry535; actual browser visual pending')
