from pathlib import Path
import datetime,hashlib,json,os,re,sys
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72')
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def new(p,x):
 p=Path(p);assert not p.exists(),p;p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def gate(label):
 p=r/'integration72'/label/'receipt.json';x=load(p);assert x['terminal_closed'] and x['exit_code']==0,label
 return dict(label=label,receipt=pin(p),stdout=x['stdout'],stderr=x['stderr'])
plan=load(r/'publication-plan.json');proof=load(r/'root.exact-verification72.adoption.json');assert proof['native_verified'];head=proof['verified_commit']
base=['mandatory-astis-check-final','python-compile','contributor','publication','semantic-cli','frontier-cli','website-ci-build','official-graph-before-visual','reader-cdp-capture','reader-copy-download','browser-full-current','python-regression-suite']
checks=[gate(s) for s in base];jobs=[int(s) for s in re.findall(r'Build completed successfully \((\d+) jobs\)',(r/'integration72/mandatory-astis-check-final/stdout.log').read_text(encoding='utf8'))];assert len(jobs)==2
if sys.argv[1]=='admin':
 visual=Path('.astis/pbps-perturbation72/visual72-cdp');copydir=Path('.astis/pbps-perturbation72/visual72-copy');capture=load(visual/'capture.json')
 assert capture['ownedBrowserExit']['code']==0 and len(capture['records'])==13 and load(copydir/'capture.json')['ownedBrowserExit']['code']==0
 evidence=[]
 for i,slug in enumerate(plan['slugs']):
  probe=load(copydir/f'unit{i}-copy-and-download.inspect.json');lesson=load(Path('website/content/declaration_lessons')/(slug+'.json'))['units'][0]
  assert probe['initialFolded'] and probe['physicalOSClipboardTest'] is False and len(probe['panels'])==len(probe['downloads'])==[2,3][i]
  assert all(x['callbackCalled'] and x['copiedExactly'] and x['status']=='Copied' for x in probe['panels'])
  assert len(probe['steps'])==len(lesson['steps'])==[6,4][i]
  for x,step in zip(probe['steps'],lesson['steps']):assert x['lean']==step['lean'] and x['initiallyFolded']
  source=Path(load(r/'claim.json')['proposed_files'][i]).read_bytes();assert all(x['status']==200 and x['text'].encode()==source for x in probe['downloads'])
  evidence.append(dict(publication=slug,panels=len(probe['panels']),steps=len(lesson['steps']),BODY_lines=sum(len(x['lean'].splitlines()) for x in lesson['steps']),downloads=len(probe['downloads']),source_RAW_sha256=sha(source)))
 dest=r/'integration72/visual72';dest.mkdir(exist_ok=False);pins=[]
 for folder,prefix in [(visual,'render'),(copydir,'copy')]:
  for p in folder.iterdir():
   if p.is_file():q=dest/(prefix+'-'+p.name);q.write_bytes(p.read_bytes());pins.append(pin(q))
 debts=['Full Chapter1.3/whole-paper Exposition Seal and postmerge purification remain open.','Inherited dense graph labels and complete-statement notation remain bounded reader debt.','The complete private actual Prop is adjacent folded representation, not a provider.','Copy callbacks are isolated page probes, not physical OS clipboard/device/live testing.']
 new(r/'visual.inspection.json',dict(status='SCOPED_LOCAL_RENDER_COPY_DOWNLOAD_INSPECTED',viewed_by_root=True,actual_root_PID=os.getpid(),capture_files=pins,capture=capture,publications=evidence,debts=debts,full_exposition_seal=False,merged_live_purified=False))
 for i,cid in enumerate(plan['active_cells']):
  p=Path('research-wiki/frontier-cells')/(cid+'.json');c=load(p);assert c['status']=='independently_verified';(r/f'integration72/cell.{i}.before-final-admin.exactraw.snapshot.json').write_bytes(p.read_bytes())
  c['evidence']['serialized_shared_gate']=dict(evidence=(r/'integration72/mandatory-astis-check-final/receipt.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=521,status='PASS',proof_commit=head,scope='ExactSCI72 and serialized local aggregate only; independent repository/reader,remoteCI,main/live/PURIFIED distinct.')
  c['graph_contribution']['visual_review']=(r/'visual.inspection.json').as_posix();c['blocked']=dict(status=False,reason='Bounded perturbation accepted by focused/math/decoder/source/exactcommit and local aggregate; actual H/K/r_rho/B27/B28 remain open.')
  p.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
 p=Path('docs/companion-papers-handoff.md');raw=p.read_bytes();text=raw.decode().replace('\r\n','\n');before='Serialized Registry521/imports/Tests and current reader/graph gates are pending\nagainst final admin state.';assert text.count(before)==1
 text=text.replace(before,f'Serialized local aggregate72:root{jobs[0]},Tests{jobs[1]},Registry521;242 publication units.\nTwo statements,6+4 exact formula/BODY steps and actual branch were inspected;\nfive isolated copy callbacks and five RAW downloads exact. Final graph/gates follow\nthese final cell writes and are recorded in72 integration.notes.json.')
 p.write_bytes(text.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode())
 new(r/'integration72/final-admin.json',dict(status='FINAL_CELL_ADMIN_WRITTEN_BEFORE_FINAL_GRAPH',proof_commit=head,cells=[pin(Path('research-wiki/frontier-cells')/(cid+'.json')) for cid in plan['active_cells']],root_jobs=jobs[0],test_jobs=jobs[1],registry_count=521,publication_units=242,final_graph_checks_pending=True))
 print('PASS final admin72 written; regenerate final graph before final checks; no further cell writes.')
elif sys.argv[1]=='final':
 for label in ['official-graph-final-admin-after-admin-recovery','graph-check-actual-final-after-admin-recovery','graph-check-generic-final-after-admin-recovery','site-check-final-after-admin-recovery','publication-final-admin-after-admin-recovery','frontier-final-admin-after-admin-recovery','contributor-final-admin-after-admin-recovery','semantic-final-admin-after-admin-recovery']:checks.append(gate(label))
 visual=load(r/'visual.inspection.json');assert visual['viewed_by_root'];admin=load(r/'integration72/final-admin.json')
 for z in admin['cells']:assert sha(Path(z['path']).read_bytes())==z['raw_sha256']
 sys.path.insert(0,str(root/'tools'));sys.path.insert(0,str(root/'website/scripts'));import publication_reader,underlying_lean_graph
 g=load('_site/data/underlying-lean-graph.json');assert g['publication_inputs_sha256']==publication_reader.graph_input_digest();underlying_lean_graph.validate(Path('_site'),g)
 assert all(any(n.get('id')=='decl:'+d for n in g['nodes']) for d in plan['mathematical_declarations'])
 new(r/'integration.notes.json',dict(status='SERIALIZED_SHARED_AGGREGATE72_AND_CURRENT_GRAPH_PASS_NOT_MAIN_NOT_PURIFIED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),proof_commit=head,registry_count=521,root_jobs=jobs[0],test_jobs=jobs[1],publication_units=242,checks=checks,visual_inspection=(r/'visual.inspection.json').as_posix(),final_cells=admin['cells'],current_graph=pin('_site/data/underlying-lean-graph.json'),publication_inputs_sha256=g['publication_inputs_sha256'],graph_delta='One generic Hilbert algebra leaf, one real actual original-input consumer and one full private statement; two connected cells/one SAU. No conceptual formal edge or fake consumer.',remaining=visual['debts']+['Actual H/K/r_rho/B27/B28,full dynamics/main/errors/caps/expected-querycost/actual-input composition remain open.'],sole_stabilization_owner='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',self_VERIFIED=False,Goal_complete=False))
 print('PASS aggregate72 final current graph/site/publication/source/frontier/contributor gates; no main/live/PURIFIED/fullpaper credit.')
else:raise ValueError(sys.argv[1])
