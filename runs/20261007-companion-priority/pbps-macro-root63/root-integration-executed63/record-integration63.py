from pathlib import Path
import datetime, hashlib, json, re, os
r=Path('runs/20261007-companion-priority/pbps-macro-root63')
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def w(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
labels=['mandatory-astis-check-final','python-regression-suite','python-compile','contributor','publication','semantic','frontier','website-ci-build','official-graph-ci-output','cell-graph-check','local-site-check','reader-cdp-capture','reader-copy-download-v2']
checks=[]
for label in labels:
 p=r/'integration63'/label/'receipt.json';x=load(p);assert x['exit_code']==0 and x['terminal_closed'],label
 checks.append(dict(label=label,receipt=pin(p),stdout=x['stdout'],stderr=x['stderr']))
jobs=[int(x) for x in re.findall(r'Build completed successfully \((\d+) jobs\)',(r/'integration63/mandatory-astis-check-final/stdout.log').read_text(encoding='utf-8'))]
assert jobs==[9170,9465],jobs
assert load(r/'root.exact-verification63.adoption.json')['native_verified']
assert 'Ran 296 tests' in (r/'integration63/python-regression-suite/stderr.log').read_text(encoding='utf-8')
visual=Path('.astis/pbps-macro-root63/visual63-cdp');capture=load(visual/'capture.json')
assert capture['ownedBrowserExit']['code']==0 and len(capture['records'])==10
copy=Path('.astis/pbps-macro-root63/visual63-copy-v2');probe=load(copy/'copy-and-download.inspect.json')
assert load(copy/'capture.json')['ownedBrowserExit']['code']==0
assert probe['initialFolded'] and probe['physicalOSClipboardTest'] is False
assert len(probe['panels'])==2 and all(p['callbackCalled'] and p['copiedExactly'] and p['status']=='Copied' for p in probe['panels'])
lesson=load('website/content/declaration_lessons/pbps-unique-positive-macroscopic-defect-root.json')['units'][0]
assert len(probe['steps'])==len(lesson['steps'])==8
for x,s in zip(probe['steps'],lesson['steps']):
 assert x['lean']==s['lean'] and x['initiallyFolded']
main=Path('AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicDefectRoot.lean').read_bytes()
assert len(probe['downloads'])==2
for x in probe['downloads']:
 assert x['status']==200 and x['text'].encode()==main
dest=r/'integration63/visual63';dest.mkdir(exist_ok=False);visualpins=[]
for source,prefix in [(visual,'render'),(copy,'copy')]:
 for p in source.iterdir():
  if p.is_file():
   q=dest/(prefix+'-'+p.name);q.write_bytes(p.read_bytes());visualpins.append(pin(q))
observations=['Complete attributed actual macro statement and all8 formula proof steps visually inspected in1440x1800 foreground headless Chrome; all adjacent Lean initially folded.','Both main statement/proof copy callbacks exactly match their displayed code; eight step code literals exactly match sealed lesson excerpts.','Two local main Lean download entries return200 and exact source RAW bytes.','Same Registry-backed declaration focus and actual source location visible; broad branch remains dense.']
debts=['Full main-paper/Chapter1.3 Exposition Seal and postmerge purification not granted.','Long branch labels/dense graph layout and tight existing disclosure/table spacing remain scoped reader debt.','Existing prose real scalar Gamma means an operator on scalar-valued real L2; independent source clarification retained.','Clipboard test uses isolated browser callback interception; no physical OS clipboard or deployed/live test.']
w(r/'visual.inspection.json',dict(status='SCOPED_ACTUAL_LOCAL_RENDER_COPY_DOWNLOAD_INSPECTED',viewed_by_root=True,actual_root_pid=os.getpid(),capture=capture,capture_files=visualpins,copy_callback_exact=True,eight_literal_step_matches=True,download_RAW_sha256=sha(main),observations=observations,debts=debts,full_exposition_seal=False,main_live_purified=False))
cid='ASTIS-SW-PBPS-unique-macroscopic-defect-root';p=Path('research-wiki/frontier-cells')/(cid+'.json');cell=load(p)
assert cell['status']=='independently_verified'
before=r/'integration63/cell.before-final-admin.exactraw.snapshot.json';before.write_bytes(p.read_bytes())
cell['evidence']['serialized_shared_gate']=dict(evidence=(r/'integration63/mandatory-astis-check-final/receipt.json').as_posix(),root_jobs=9170,test_jobs=9465,registry_count=508,status='PASS',proof_commit='4d02622332d02d0bd6c977d3cee48fd535ebf203',scope='Exact63 plus serialized local aggregate; remoteCI/repository reader admission/main/live/PURIFIED remain distinct.')
cell['graph_contribution']['visual_review']=(r/'visual.inspection.json').as_posix()
cell['blocked']=dict(status=False,reason='Focused, independent science/decoder/source, publication and local aggregate63 accepted within bounded macro-root/Gram scope.')
w(p,cell)
p=Path('docs/companion-papers-handoff.md');b=p.read_bytes();s=b.decode('utf-8');nl='\r\n' if b'\r\n' in b else '\n';s=s.replace('\r\n','\n')
marker='##';i=s.find(marker)
assert i>=0
append='\nSerialized local aggregate63: root9170, Tests9465, Registry508; all296 Python\nregressions,229 publication units, contributor/semantic/frontier/site and bounded\ngraph check PASS. Complete statement,8formula steps and same compiled branch\nwere visually inspected. Two copy callbacks and two local Lean downloads match\nexact source; all8folded step literals match sealed excerpts. Independent\nrepository/exposition admission, integration remote CI,main/live/PURIFIED and\nwhole-paper results remain open.\n\n'
next_heading=s.find('\n## ',i+2)
assert next_heading>0
s=s[:next_heading]+append+s[next_heading:];p.write_bytes(s.replace('\n',nl).encode('utf-8'))
pres=load(r/'integration63/generated-context-preservation-data/manifest.json')
w(r/'integration.notes.json',dict(status='SERIALIZED_SHARED_AGGREGATE_PASS_NOT_MAIN_NOT_PURIFIED',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),proof_commit='4d02622332d02d0bd6c977d3cee48fd535ebf203',registry_count=508,root_jobs=9170,test_jobs=9465,python_tests=296,publication_units=229,checks=checks,visual_inspection=(r/'visual.inspection.json').as_posix(),cell_before=pin(before),cell_after=pin(Path('research-wiki/frontier-cells')/(cid+'.json')),graph_delta='One public actual macroscopic defect-root integration; SAME canonical e/M/U/T and unique scalar/transported root; exact typed B:HP-to-joint Gram and all-alternative uniqueness. Four affected module graph artifacts and one enriched card; zero private providers. Centered64 order/inverse remains claimed scratch work, not a compiled graph dependency.',preserved_canonical_cards=len(pres['preserved_canonical_metadata']),unrelated_emitted_paths=len(pres['emitted_snapshots'])-4,remaining=debts+['B15/B16,H1,events/invariance/nonexplosion/hypocoercivity/main/errors/expectedcost/actual-input composition remain open.'],sole_stabilization_owner='ASTIS-SA-20261005-SPHMCImplementedPhaseKernel',self_VERIFIED=False,Goal_complete=False))
print('PASS local aggregate63:9170/9465/508,296tests,229pub;10viewed screenshots;2exactcopy callbacks/2exactRAW downloads/8literal folded steps. No full Exposition/main/live/Goal completion.')
