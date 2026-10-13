from pathlib import Path
import datetime,hashlib,json,re,os,subprocess
root=Path.cwd();r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66');load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def w(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
labels=['mandatory-astis-check-final','python-compile','contributor','publication','semantic','frontier','website-ci-build','official-graph-ci-output-final-v2','cell-graph-check-actual','local-site-check-final','reader-cdp-capture','reader-copy-download']
checks=[]
for label in labels:
 p=r/'integration66'/label/'receipt.json';x=load(p);assert x['exit_code']==0 and x['terminal_closed'],label;checks.append(dict(label=label,receipt=pin(p),stdout=x['stdout'],stderr=x['stderr']))
jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',(r/'integration66/mandatory-astis-check-final/stdout.log').read_text(encoding='utf-8'))];assert len(jobs)==2
proof=load(r/'root.exact-verification66.adoption.json');assert proof['native_verified'];head=proof['verified_commit']
unchanged=subprocess.check_output(['git','diff','--name-only','0aef19ca2711159eeaec86d42c9be142a94fa402',head,'--','tools','website/scripts'],text=True);assert not unchanged.strip()
regression=Path('runs/20261007-companion-priority/pbps-centered-root64/integration64/python-regression-suite/receipt.json');assert load(regression)['exit_code']==0
assert load(Path('runs/20261007-companion-priority/pbps-centered-root64/remote-ci64.accepted.json'))['status']=='EXACT_INT64_REMOTE_ALL_SUCCESS'
visual=Path('.astis/pbps-ambient-adjoint66/visual66-cdp');copy=Path('.astis/pbps-ambient-adjoint66/visual66-copy');capture=load(visual/'capture.json')
assert capture['ownedBrowserExit']['code']==0 and len(capture['records'])==8
assert load(copy/'capture.json')['ownedBrowserExit']['code']==0
probe=load(copy/'actual-copy-and-download.inspect.json');lesson=load(Path('website/content/declaration_lessons/pbps-ambient-adjoint-corrector.json'))['units'][0]
assert probe['initialFolded'] and probe['physicalOSClipboardTest'] is False and len(probe['panels'])==2
assert all(x['callbackCalled'] and x['copiedExactly'] and x['status']=='Copied' for x in probe['panels'])
assert len(probe['steps'])==len(lesson['steps'])==6
for x,step in zip(probe['steps'],lesson['steps']):assert x['lean']==step['lean'] and x['initiallyFolded']
source=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean').read_bytes();assert len(probe['downloads'])==2
for x in probe['downloads']:assert x['status']==200 and x['text'].encode()==source
dest=r/'integration66/visual66';dest.mkdir(exist_ok=False);pins=[]
for src,prefix in [(visual,'render'),(copy,'copy')]:
 for p in src.iterdir():
  if p.is_file():q=dest/(prefix+'-'+p.name);q.write_bytes(p.read_bytes());pins.append(pin(q))
debts=['Full whole-paper/Chapter1.3 Exposition Seal and postmerge purification remain open.','Existing dense graph labels and inherited reader spacing remain bounded reader debt.','The inherited full statement still uses plain Unicode/underscored notation and two reviewed literal private Prop representations; default placement of complete Lean disclosures remains part of the ungranted full Exposition Seal.','Copy callbacks are isolated page probes, not a physical OS clipboard or live/deployed test.']
w(r/'visual.inspection.json',dict(status='SCOPED_LOCAL_RENDER_COPY_DOWNLOAD_INSPECTED',viewed_by_root=True,actual_root_pid=os.getpid(),capture_files=pins,capture=capture,publications=[dict(publication='pbps-ambient-adjoint-corrector',panels=2,steps=6,downloads=2,source_RAW_sha256=sha(source))],observations=['Complete original-input attributed statement,all6 formula steps and exact actual branch inspected. Statement/proof/step Lean initially folded;two copy callbacks and two RAW source downloads exact.'],debts=debts,full_exposition_seal=False,merged_live_purified=False))
plan=load(r/'publication-plan.json');cp=Path('research-wiki/frontier-cells')/(plan['active_cells'][0]+'.json');cell=load(cp);assert cell['status']=='independently_verified'
(r/'integration66/cell.0.before-final-admin.exactraw.snapshot.json').write_bytes(cp.read_bytes());cell['evidence']['serialized_shared_gate']=dict(evidence=(r/'integration66/mandatory-astis-check-final/receipt.json').as_posix(),root_jobs=jobs[0],test_jobs=jobs[1],registry_count=512,status='PASS',proof_commit=head,scope='Exact66 plus serialized local aggregate only; independent repository/reader,remoteCI,main/live/PURIFIED remain distinct.')
cell['graph_contribution']['visual_review']=(r/'visual.inspection.json').as_posix();cell['blocked']=dict(status=False,reason='Focused and independent math/decoder/source/exact-commit, reviewed dependency catalogues, publication and local aggregate accepted within ambient-adjoint/global-centering scope.');w(cp,cell)
p=Path('docs/companion-papers-handoff.md');raw=p.read_bytes();s=raw.decode().replace('\r\n','\n');a=s.find('\n## ',s.find('\n## ')+1);assert a>0
append=f'\nSerialized local aggregate66:root{jobs[0]},Tests{jobs[1]},Registry512;233\npublication items and contributor/semantic/frontier/site/affected graph PASS.\nUnchanged tools/site-script Python296 regression evidence is reused from exact\nINT64 rather than reported as rerun. One complete statement,all6 formula steps\nand actual branch inspected;two copy callbacks/two RAW source downloads exact.\nIndependent repository/exposition admission,remoteCI/main/live/PURIFIED and\nwhole-paper results remain separate.\n\n'
s=s[:a]+append+s[a:];p.write_bytes(s.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode())
w(r/'integration.notes.json',dict(status='SERIALIZED_SHARED_AGGREGATE66_PASS_NOT_MAIN_NOT_PURIFIED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),proof_commit=head,registry_count=512,root_jobs=jobs[0],test_jobs=jobs[1],reused_python_tests=dict(count=296,exact_unchanged_tools_and_site_scripts=True,prior_receipt=pin(regression),rerun=False),publication_units=233,checks=checks,visual_inspection=(r/'visual.inspection.json').as_posix(),graph_delta='One actual ambient-adjoint/global-centering declaration/module and genuine global norm-budget Test; one affected card and current aggregate graph artifacts. Two literal Prop representations add no private mathematical provider or conceptual formal edge.',remaining=debts+['B20 corrector definition and sharp B23 energy estimate; actual root/inverse commutation and B21/halfturn/H1/dynamics/main/errors/expectedquerycost/composition remain open.'],sole_stabilization_owner='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',self_VERIFIED=False,Goal_complete=False))
print('PASS local aggregate66:',jobs,'Registry512/233pub;8viewed captures,2exact copy callbacks,2RAW downloads,6literal folded steps;unchanged296 Python evidence reused.')
