from pathlib import Path
import datetime,hashlib,json,os,re,sys
r=Path('runs/20261007-companion-priority/pbps-actual-bounce-rate74')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def new(p,x):
 p=Path(p);assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def gate(label):
 p=r/'integration74'/label/'receipt.json';q=load(p);assert q['terminal_closed'] and q['exit_code']==0,label
 return dict(label=label,receipt=pin(p),stdout=q['stdout'],stderr=q['stderr'])
base=['mandatory-astis-check-final','python-compile','publication','semantic','frontier','contributor','website-ci-build','official-graph-before-visual','reader-render-current','reader-copy-download']
checks=[gate(s) for s in base];proof=load(r/'root.exact-verification74.adoption.json');head=proof['verified_commit'];assert proof['native_verified']
jobs=[int(s) for s in re.findall(r'Build completed successfully \((\d+) jobs\)',(r/'integration74/mandatory-astis-check-final/stdout.log').read_text(encoding='utf8'))];assert len(jobs)==2
reuse=load(r/'integration74/unchanged-regression-reuse.json');assert reuse['reused_exact_unchanged_helpers_with_runtime_continuity_evidence']
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');assert len(plan['slugs'])==1
if sys.argv[1]=='admin':
 render=Path('.astis/pbps-bounce74/visual74-cdp');copy=Path('.astis/pbps-bounce74/visual74-copy');capture=load(render/'capture.json');probe=load(copy/'unit0-copy-and-download.inspect.json')
 assert capture['ownedBrowserExit']['code']==0 and len(capture['records'])==9 and load(copy/'capture.json')['ownedBrowserExit']['code']==0
 lesson=load('website/content/declaration_lessons/pbps-actual-bounce-rate.json')['units'][0]
 assert probe['initialFolded'] and not probe['physicalOSClipboardTest'] and len(probe['panels'])==len(probe['downloads'])==3 and len(probe['steps'])==len(lesson['steps'])==7
 assert all(x['callbackCalled'] and x['copiedExactly'] and x['status']=='Copied' for x in probe['panels'])
 for x,s in zip(probe['steps'],lesson['steps']):assert x['lean']==s['lean'] and x['initiallyFolded']
 source=Path(claim['proposed_files'][0]).read_bytes();assert all(x['status']==200 and x['text'].encode()==source for x in probe['downloads'])
 viewed=load(r/'root.viewed-captures74.json');assert viewed['viewed_by_root'] and len(viewed['images'])==10
 for z in viewed['images']:assert sha(Path(z['path']).read_bytes())==z['RAW_sha256']
 dest=r/'integration74/visual74';dest.mkdir(exist_ok=False);pins=[]
 for folder,prefix in [(render,'render'),(copy,'copy')]:
  for p in folder.iterdir():
   if p.is_file():q=dest/(prefix+'-'+p.name);q.write_bytes(p.read_bytes());pins.append(pin(q))
 debts=['Full Chapter1.3/whole-paper Exposition Seal and postmerge purification remain open.','Dense graph labels and complete-statement plain notation remain bounded reader debt.','Copy callbacks are isolated page probes; physical OS clipboard and live-site testing were not performed.']
 new(r/'visual.inspection.json',dict(status='SCOPED_LOCAL_RENDER_COPY_DOWNLOAD_INSPECTED',viewed_by_root=True,actual_root_PID=os.getpid(),capture_files=pins,root_viewed=pin(r/'root.viewed-captures74.json'),capture=capture,formula_BODY_steps=7,copy_callbacks=3,RAW_downloads=3,source_RAW_sha256=sha(source),debts=debts,full_exposition_seal=False,merged_live_purified=False))
 cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounce-rate.json');c=load(cp);assert c['status']=='independently_verified'
 (r/'integration74/cell.before-final-admin.exactraw.snapshot.json').write_bytes(cp.read_bytes())
 c['evidence']['serialized_shared_gate']=dict(evidence=(r/'integration74/mandatory-astis-check-final/receipt.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=523,status='PASS',proof_commit=head,scope='ExactSCI74 and serialized local aggregate; independent repository/reader, remoteCI, main/live/PURIFIED distinct.')
 c['graph_contribution']['visual_review']=(r/'visual.inspection.json').as_posix();c['blocked']=dict(status=False,reason='Deterministic bounce/rate/energy-layer laws accepted by focused/math/decoder/source/exactcommit and local aggregate. Actual clock/recursive PDMP/invariance/nonexplosion remain open.')
 cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 p=Path('docs/companion-papers-handoff.md');raw=p.read_bytes();text=raw.decode().replace('\r\n','\n');old='Serialized Registry523/imports/Tests, current reader/graph and mandatory\naggregate gates are pending against final admin state.';assert text.count(old)==1
 text=text.replace(old,f'Serialized local aggregate74: root{jobs[0]}, Tests{jobs[1]}, Registry523;244 publication units.\nOne statement and seven formula/BODY steps plus the actual branch were inspected;\nthree isolated copy callbacks and three RAW downloads were exact.\nFinal current graph/gates are recorded in74 integration.notes.json.')
 p.write_bytes(text.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode())
 new(r/'integration74/final-admin.json',dict(status='FINAL_CELL_ADMIN_BEFORE_FINAL_GRAPH',proof_commit=head,cells=[pin(cp)],root_jobs=jobs[0],test_jobs=jobs[1],registry_count=523,publication_units=244,final_graph_checks_pending=True))
 print('PASS74 final admin before final graph; no further cell writes.')
elif sys.argv[1]=='final':
 checks.extend(gate(s) for s in ['official-graph-final','graph-check-final','site-check-final','publication-final','frontier-final','contributor-final','semantic-final'])
 admin=load(r/'integration74/final-admin.json');visual=load(r/'visual.inspection.json')
 for z in admin['cells']:assert sha(Path(z['path']).read_bytes())==z['RAW_sha256']
 sys.path.insert(0,str(Path.cwd()/'tools'));sys.path.insert(0,str(Path.cwd()/'website/scripts'));import publication_reader,underlying_lean_graph
 g=load('_site/data/underlying-lean-graph.json');assert g['publication_inputs_sha256']==publication_reader.graph_input_digest();underlying_lean_graph.validate(Path('_site'),g)
 assert any(n.get('id')=='decl:'+plan['mathematical_declarations'][0] for n in g['nodes'])
 new(r/'integration.notes.json',dict(status='SERIALIZED_SHARED_AGGREGATE74_AND_CURRENT_GRAPH_PASS_NOT_MAIN_NOT_PURIFIED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),proof_commit=head,registry_count=523,root_jobs=jobs[0],test_jobs=jobs[1],publication_units=244,checks=checks,regression_reuse=pin(r/'integration74/unchanged-regression-reuse.json'),visual_inspection=(r/'visual.inspection.json').as_posix(),final_cells=admin['cells'],current_graph=pin('_site/data/underlying-lean-graph.json'),publication_inputs_sha256=g['publication_inputs_sha256'],graph_delta='One actual deterministic bounce/rate/energy-layer theorem; internal canonical gradient-Lipschitz producer and pinned Mathlib reflection dependencies. No conceptual formal edge or stochastic consumer claim.',remaining=visual['debts']+['Actual clocks/recursive PDMP/nonexplosion/invariance and full mains/errors/expected-querycost/actual-input composition remain open.'],sole_stabilization_owner='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',Goal_complete=False))
 print('PASS74 final aggregate/current graph/site/publication/source/frontier/contributor gates; independent scoped reader pending.')
else:raise ValueError(sys.argv[1])
