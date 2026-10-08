from common import *
W(P/'lease.open.json',dict(status='OPEN_PHASE1',actor=ACTOR,actual_opener_PID=os.getpid(),scope='Bounded repository/exposition61; no compiler/generator/canonical/Git writes; final integration PHASE2 pending'))
plan=J(R/'publication-plan.json'); files=[path(x['path']) for x in J(R/'math-freeze.json')['inputs'][:3]]
for slug in plan['slugs']:
 files.extend([ROOT/f'website/content/publications/{slug}.json',ROOT/f'website/content/declaration_lessons/{slug}.json'])
for aid in plan['audit_ids']: files.append(ROOT/f'research-wiki/semantic-roundtrip/audits/{aid}.json')
for folder,names in [('independent-math61',['run.json','receipt.json','payload.json','lease.json']),('source-review61',['run.json','native.receipt.json','lease.json','source.0.review.json','source.1.review.json']),('anonymous-decoder',['decoder-native-run.json','decoder-native-run.payload.json','CLOSED_LAST.json']),('exact-science-verification',['run.json','receipt.json','payload.json','lease.json','readback.json','native.review.json'])]:
 files.extend([R/folder/n for n in names])
files.extend([R/'root.exact-verification61.adoption.json',R/'publication-plan.json',R/'integration61/visual-capture61/receipt.json'])
capture=ROOT/'.astis/pbps-real-defect-root61/visual61-cdp'; labels=['producer','producer-proof','producer-proof-late','consumer','consumer-proof','consumer-proof-late','branch-producer','branch-consumer']
files.append(capture/'capture.json')
for label in labels: files.extend([capture/(label+'.png'),capture/(label+'.inspect.json')])
files.extend([ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html',ROOT/'_site/lean-foundations.html',ROOT/'_site/assets/underlying-lean-graph.js',ROOT/'_site/assets/underlying-lean-graph.css',ROOT/'_site/assets/site.js',ROOT/'_site/data/underlying-lean-graph.json'])
rows=[snap(p,i) for i,p in enumerate(files)]; W(P/'phase1.inputs.json',dict(schema='native-repository-exposition61-phase1-inputs-v1',actor=ACTOR,actual_opener_PID=os.getpid(),science_commit=SCI,observed_HEAD=git('rev-parse','HEAD').decode().strip(),count=len(rows),qualified_original_snapshot_pairs=rows,timing='Exact stable61 source/metadata/native/render/capture bytes before exposition read; global mutable cells/ledger/handoff final admin pending PHASE2',no_active_observer_inputs=True))
print('PHASE1_FROZEN',len(rows),'qualified pairs',os.getpid())
