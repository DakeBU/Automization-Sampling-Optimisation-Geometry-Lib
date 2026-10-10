from pathlib import Path
import datetime,hashlib,json,re,os,subprocess
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-centered-root64');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def w(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
labels=['mandatory-astis-check-final','python-regression-suite','python-compile','contributor','publication','semantic-v2','frontier-v2','website-ci-build','official-graph-ci-output','cell-graph-check-actual','cell-graph-check-shared','local-site-check','reader-cdp-capture','reader-copy-download']
checks=[]
for label in labels:
 p=r/'integration64'/label/'receipt.json';x=load(p);assert x['exit_code']==0 and x['terminal_closed'],label;checks.append(dict(label=label,receipt=pin(p),stdout=x['stdout'],stderr=x['stderr']))
jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',(r/'integration64/mandatory-astis-check-final/stdout.log').read_text(encoding='utf-8'))];assert len(jobs)==2
assert load(r/'root.exact-verification64.adoption.json')['native_verified'];assert 'Ran 296 tests' in (r/'integration64/python-regression-suite/stderr.log').read_text(encoding='utf-8')
visual=Path('.astis/pbps-centered-root64/visual64-cdp');capture=load(visual/'capture.json');assert capture['ownedBrowserExit']['code']==0 and len(capture['records'])==16
copy=Path('.astis/pbps-centered-root64/visual64-copy');assert load(copy/'capture.json')['ownedBrowserExit']['code']==0
copy_rows=[]
for i,(prefix,slug) in enumerate([('shared','real-l2-positive-square-order'),('actual','pbps-centered-root-order-inverse')]):
 probe=load(copy/f'{prefix}-copy-and-download.inspect.json');lesson=load(Path('website/content/declaration_lessons')/f'{slug}.json')['units'][0]
 assert probe['initialFolded'] and probe['physicalOSClipboardTest'] is False
 assert len(probe['panels'])==2 and all(p['callbackCalled'] and p['copiedExactly'] and p['status']=='Copied' for p in probe['panels'])
 assert len(probe['steps'])==len(lesson['steps'])==[3,9][i]
 for x,step in zip(probe['steps'],lesson['steps']):assert x['lean']==step['lean'] and x['initiallyFolded']
 source=Path(load(r/'claim.json')['proposed_files'][i]).read_bytes();assert len(probe['downloads'])==2
 for x in probe['downloads']:assert x['status']==200 and x['text'].encode()==source
 copy_rows.append(dict(publication=slug,panels=2,steps=len(probe['steps']),downloads=2,source_RAW_sha256=sha(source)))
dest=r/'integration64/visual64';dest.mkdir(exist_ok=False);visualpins=[]
for source,prefix in [(visual,'render'),(copy,'copy')]:
 for p in source.iterdir():
  if p.is_file():q=dest/(prefix+'-'+p.name);q.write_bytes(p.read_bytes());visualpins.append(pin(q))
debts=['Full Chapter1.3/whole-paper Exposition Seal and postmerge purification remain ungranted.','Existing dense graph labels and disclosure/table spacing remain reader debt.','Clipboard probes intercept isolated-page callbacks; no physical OS clipboard or deployed/live test.']
w(r/'visual.inspection.json',dict(status='SCOPED_LOCAL_RENDER_COPY_DOWNLOAD_INSPECTED',viewed_by_root=True,actual_root_pid=os.getpid(),capture_files=visualpins,capture=capture,publications=copy_rows,observations=['Two complete attributed statements,3+9 formula proof steps and two same-declaration branches inspected in bounded foreground headless Chrome.','Both statements/proofs and all12 exact step excerpts initially folded;4copy callbacks and4RAW source downloads match.'],debts=debts,full_exposition_seal=False,merged_live_purified=False))
plan=load(r/'publication-plan.json')
for i,cid in enumerate(plan['active_cells']):
 p=Path('research-wiki/frontier-cells')/f'{cid}.json';cell=load(p);assert cell['status']=='independently_verified';before=r/'integration64'/f'cell.{i}.before-final-admin.exactraw.snapshot.json';before.write_bytes(p.read_bytes())
 cell['evidence']['serialized_shared_gate']=dict(evidence=(r/'integration64/mandatory-astis-check-final/receipt.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=510,status='PASS',proof_commit='59fff63d320aa5e3dc4b45e81e40e2029ce42734',scope='Exact64 plus serialized local aggregate only; repository/reader admission, remoteCI/main/live/PURIFIED remain distinct.')
 cell['graph_contribution']['visual_review']=(r/'visual.inspection.json').as_posix();cell['blocked']=dict(status=False,reason='Focused and independent science/decoder/source/finite metadata/publication plus local aggregate64 accepted within bounded square-order/centered inverse scope.');w(p,cell)
p=Path('docs/companion-papers-handoff.md');raw=p.read_bytes();s=raw.decode().replace('\r\n','\n');a=s.find('\n## ',s.find('\n## ')+1);assert a>0
append=f'\nSerialized local aggregate64:root{jobs[0]},Tests{jobs[1]},Registry510;296 Python\nregressions,231 publication items,contributor/semantic/frontier/site and both\nbounded graph checks PASS. Two attributed statements,3+9 formula steps and\ntwo actual branches inspected. Four isolated copy callbacks/four RAW source\ndownloads/all12 folded literals match. Independent repository/exposition\nadmission,remoteCI/main/live/PURIFIED and whole-paper results remain separate.\n\n'
s=s[:a]+append+s[a:];p.write_bytes(s.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode())
w(r/'integration.notes.json',dict(status='SERIALIZED_SHARED_AGGREGATE64_PASS_NOT_MAIN_NOT_PURIFIED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),proof_commit='59fff63d320aa5e3dc4b45e81e40e2029ce42734',registry_count=510,root_jobs=jobs[0],test_jobs=jobs[1],python_tests=296,publication_units=231,checks=checks,visual_inspection=(r/'visual.inspection.json').as_posix(),graph_delta='One canonical real-L2 square-order node with genuine actual PBPS consumer; one actual centered-root order/inverse integration of SAME macro root/rough mean/marginal Poincare. Two affected module cards and four aggregate graph artifacts, zero private providers. Next B16 polar remains unproved; no conceptual overlay promoted to a formal dependency.',remaining=debts+['B16,H1/B13/B14,dynamics/nonexplosion/invariance/hypocoercivity/main/errors/expectedcost/actual-input composition remain open.'],sole_stabilization_owner='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',self_VERIFIED=False,Goal_complete=False))
print('PASS local aggregate64:',jobs,'Registry510,296tests,231pub;16viewed captures,4exactcopy callbacks,4RAW downloads,12literal folded steps. No full Exposition/main/live/Goal claim.')
