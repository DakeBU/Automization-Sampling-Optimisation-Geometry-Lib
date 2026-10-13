import pathlib,json,hashlib,gzip,os,sys,subprocess,re
ROOT=pathlib.Path('E:/Samplinglib');os.chdir(ROOT);sys.path[:0]=[str(ROOT),str(ROOT/'tools'),str(ROOT/'website/scripts')]
R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect59';D=R/'repository-exposition-seal59';X=R/'exact-science-verification'
SCI='2d6cd0167adc4fae1d8d166068a2eda51cd3c3ad';HEAD='47a28adfa36bfa67ce201f9b3ff9823c85fc3b45'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def path(s):
 p=pathlib.Path(re.sub('/+','/',str(s).replace('\\','/')));return p if p.is_absolute() else ROOT/p
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def match(a,b):return a['raw_sha256']==b['raw_sha256'] and a['lf_sha256']==b['lf_sha256'] and a['bytes']==b.get('bytes',b.get('raw_bytes',a['bytes'])) and a['lf_bytes']==b.get('lf_bytes',a['lf_bytes'])
def key(x):return path(x['path']).as_posix(),x['raw_sha256'],x['lf_sha256']
def git(*a):return subprocess.check_output(['git',*a])
def pins(q):
 if isinstance(q,dict):
  if {'path','raw_sha256','lf_sha256'}<=q.keys():yield q
  for x in q.values():yield from pins(x)
 elif isinstance(q,list):
  for x in q:yield from pins(x)
assert git('rev-parse','HEAD').decode().strip()==HEAD and git('rev-parse','HEAD^').decode().strip()==SCI
notes=load(R/'integration.notes.json');assert notes['proof_commit']==SCI
adoption=load(R/'root.exact-verification59.adoption.json')
maps=[dict(original=x['original'],snapshot=x['exact_raw_snapshot'],reason='Exact independent preclosure/source audit/ledger history') for x in adoption['exact_historical_resolutions']]
for x in load(X/'current-audit-and-admin-bindings.json')['before_admin_mappings']:
 maps.append(dict(original=x['original'],snapshot=x['exact_snapshot'],reason='Exact science canonical admin-before snapshot'))
for x in notes['cell_administration_updates']:
 before=load(path(x['before']['path']));after=load(path(x['after']['path']));assert before['status']==after['status']=='independently_verified'
 assert before['target_statement']==after['target_statement']
 assert before['parents']==after['parents'] and before['source_anchor']==after['source_anchor']
 assert after['evidence']['serialized_shared_gate']['status']=='PASS'
 oldpin=dict(x['before'],path=path(x['after']['path']).as_posix())
 maps.append(dict(original=oldpin,snapshot=x['before'],reason='Exact postVERIFIED before-aggregate cell administration snapshot'))
 def diff(a,b,p=''):
  if type(a)!=type(b):return [p]
  if isinstance(a,dict):return [y for k in sorted(a.keys()|b.keys()) for y in ([p+'/'+k] if k not in a or k not in b else diff(a[k],b[k],p+'/'+k))]
  return [] if a==b else [p]
 assert set(diff(before,after))=={'/evidence/serialized_shared_gate','/graph_contribution/visual_review'}
write(D/'historical-mappings.json',dict(mappings=maps,count=len(maps),identity_rule='Full qualified original path plus original raw/LF hashes and lengths; no basename fallback'))
seen={};used={}
def checkpin(row):
 k=key(row)
 if k in seen:return
 p=path(row['path']);a=pin(p) if p.exists() else None;route='CURRENT_EXACT'
 if a is None or not match(a,row):
  matches=[x for x in maps if key(x['original'])==k and match(x['original'],row)]
  assert matches,('UNMAPPED_INPUT',row)
  candidates={key(x['snapshot']):x for x in matches};assert len(candidates)==1
  mapping=next(iter(candidates.values()));a=pin(mapping['snapshot']['path']);assert match(a,row);route='EXACT_HISTORICAL_SNAPSHOT';used[k]=mapping
 assert match(a,row);seen[k]=dict(original=row,resolved=a,route=route)

# Reuse complete immutable original evidence, checking every actual declared pin.
objects=[]
for p in [X/'run.json',X/'lease.json',X/'receipt.json',X/'inputs.final.json',X/'outputs.final.json',X/'readback.json',X/'pin-history-readback/run.json',X/'pin-history-readback/lease.json',X/'pin-history-readback/receipt.json',R/'root.exact-verification59.adoption.json',R/'independent-math-review/run.json',R/'independent-math-review/lease.json',R/'source-review59/run.json',R/'source-review59/lease.json',R/'source-review59/receipt.json',R/'anonymous-decoder/decoder-run.json',R/'anonymous-decoder/lease.json']:
 q=load(p);objects.append(pin(p))
 for row in pins(q):checkpin(row)
for row in load(X/'outputs.final.json')['artifacts']:
 p=path(row['path']);checkpin(row)
 if p.suffix=='.json':
  for x in pins(load(p)):checkpin(x)
for qpath,field,payload,pfield in [(X/'run.json','run_sha256','named_exact_verification_payload','named_exact_verification_payload_sha256'),(X/'pin-history-readback/run.json','run_sha256','named_pin_history_payload','named_pin_history_payload_sha256'),(R/'independent-math-review/run.json','run_sha256','mathematics_review_payload','mathematics_review_payload_sha256'),(R/'source-review59/run.json','run_sha256','named_source_review_payload','named_source_review_payload_sha256')]:
 q=load(qpath);assert sha(canon({k:v for k,v in q.items() if k!=field}))==q[field];assert sha(canon(q[payload]))==q[pfield]
for p in [X/'lease.json',X/'pin-history-readback/lease.json',R/'independent-math-review/lease.json']:
 q=load(p);assert sha(canon({k:v for k,v in q.items() if k!='lease_sha256'}))==q['lease_sha256'];assert q['status'] in ['CLOSED','CLOSEDLAST']
assert load(R/'source-review59/lease.json')['status']=='CLOSEDLAST'
assert load(R/'anonymous-decoder/lease.json')['status']=='CLOSEDLAST'
assert not load(R/'anonymous-decoder/decoder-run.json')['source_text_visible'] and not load(R/'anonymous-decoder/decoder-run.json')['source_identity_visible']
freeze=load(R/'math-freeze.json');assert len(freeze['inputs'])==27
for row in freeze['inputs']:checkpin(row)

# Every exact tracked integration entry is bound; next-source-scout records remain opaque bytes.
names=[x.decode() for x in git('diff','--name-only','-z',SCI,HEAD).split(b'\0') if x];tree={}
for row in git('ls-tree','-r','-z',HEAD).split(b'\0'):
 if row:
  a,n=row.split(b'\t',1);mode,kind,oid=a.decode().split();tree[n.decode()]=(mode,kind,oid)
blob=subprocess.run(['git','cat-file','--batch'],input=('\n'.join(tree[n][2] for n in names)+'\n').encode(),capture_output=True,check=True).stdout
off=0;entries=[]
for n in names:
 end=blob.index(b'\n',off);h=blob[off:end].decode().split();size=int(h[2]);b=blob[end+1:end+size+1];off=end+size+2
 a=pin(ROOT/n);assert sha(b.replace(b'\r\n',b'\n'))==a['lf_sha256'],n
 entries.append(dict(path=a['path'],git_oid=tree[n][2],git_bytes=size,git_raw_sha256=sha(b),git_lf_sha256=sha(b.replace(b'\r\n',b'\n')),working=a,review_scope='Opaque source-only future scout bytes, no mathematics/read/admission credit' if '/next-root-source-scout60/' in a['path'] else 'Exact integration owned entry'))
assert off==len(blob) and len(entries)==315
write(D/'integration.git-pins.json',dict(checked_science=SCI,checked_integration=HEAD,count=len(entries),entries=entries))
code=[path(freeze['inputs'][i]['path']) for i in [0,1]]
for p in code:
 b=p.read_bytes();assert git('show',SCI+':'+p.relative_to(ROOT).as_posix()).replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')
 assert git('show',HEAD+':'+p.relative_to(ROOT).as_posix()).replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')
 assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',b.decode())
assert not re.search(r'^import Tests',code[0].read_text(encoding='utf8'),re.M)
example=(ROOT/'AutoSamplingTheory/ExampleCases.lean').read_text(encoding='utf8');assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator' in example
assert not re.search(r'^(?:theorem|lemma|def|axiom)\s',example,re.M)
assert 'import Tests.ProximalBPSCenteredDefect' in (ROOT/'Tests.lean').read_text(encoding='utf8')
assert 'formalizedTechnicalLemmaCount = 501' in (ROOT/'Tests/Basic.lean').read_text(encoding='utf8')
registry=(ROOT/'AutoSamplingTheory/TechnicalLemmas/Registry.lean').read_text(encoding='utf8');assert registry.count('key := "pbps.actualCenteredSelfadjointDefect"')==1
assert 'Tests.ProximalBPSCenteredDefect.actual_centered_defect_coercive_and_unit' not in registry

gates=[]
for row in notes['checks']:
 for x in pins(row):checkpin(x)
 q=load(path(row['receipt']['path']));assert q['exit_code']==0 and q['terminal_closed'] and q['checked_science_parent']==SCI
 for x in pins(q):checkpin(x)
 gates.append(dict(label=row['label'],receipt=pin(row['receipt']['path']),actual_pid=q['actual_foreground_pid'],actual_exit_code=0,actual_terminal_closed=True,command=q['command'],stdout=q['stdout'],stderr=q['stderr']))
assert len(gates)==15
for s in notes['final_administrative_gate_receipts']:
 q=load(path(s));assert q['exit_code']==0 and q['terminal_closed']
 for x in pins(q):checkpin(x)
 gates.append(dict(label=path(s).parent.name,receipt=pin(path(s)),actual_pid=q['actual_foreground_pid'],actual_exit_code=0,actual_terminal_closed=True,command=q['command'],stdout=q['stdout'],stderr=q['stderr']))
assert len(gates)==18
rootlog=path(gates[1]['stdout']['path']).read_text(encoding='utf8');assert re.findall(r'Build completed successfully \((\d+) jobs\)',rootlog)==['9163','9454'] and 'ASTIS check passed' in rootlog
assert 'Build completed successfully (9455 jobs)' in path(gates[0]['stdout']['path']).read_text(encoding='utf8')
for name in freeze['mathematical_declarations']:
 m=re.search(re.escape(name)+r"' depends on axioms: \[([^]]*)\]",rootlog,re.S);assert m and set(x.strip() for x in m.group(1).replace('\n',' ').split(','))=={'propext','Classical.choice','Quot.sound'}
write(D/'terminal-gates.json',dict(actual_gates=gates,count=18,mandatory_root_jobs=9163,mandatory_Test_jobs=9454,combined_root_Test_jobs=9455,registry=501,independent_compiler='NOT_STARTED_CLOSED',science_remote_snapshot_not_integration_CI=True))

# Actual graphical/source inventory with preserved collaborator metadata, not proof implication.
import astis
inventorypath=ROOT/'research-wiki/retrieval-index/astis-lean-arsenal-module-graph.json';inventory=load(inventorypath)['modules'];actual=astis.lean_module_records();assert len(inventory)==len(actual)==509
lookup={x['module']:x for x in actual}
for q in inventory:
 a=lookup[q['module']]
 for k in ['path','imports','local_imports','declarations','exports']:assert q[k]==a[k],(q['module'],k)
preservepath=R/'integration59/generated-context-preservation/manifest.json';preserve=load(preservepath);restored=[]
for row in preserve['emitted_snapshots']:
 b=gzip.decompress(path(row['emitted_snapshot']).read_bytes());assert sha(b)==row['emitted_raw_sha256']
 if row['action']=='restored root-generated unrelated changes to exact HEAD bytes':
  baseline=git('show',SCI+':'+row['path']);assert sha(baseline)==row['baseline_raw_sha256'] and (ROOT/row['path']).read_bytes()==baseline
  restored.append(row['path'])
assert len(restored)==79 and len(preserve['preserved_canonical_metadata'])==62
for row in preserve['preserved_canonical_metadata']:
 b=git('show',SCI+':'+row['canonical_card']);assert sha(b)==row['card_raw_sha256']
 item=next(x for x in inventory if x['module']==row['module'])
 for k,v in row['metadata'].items():assert item[k]==v
write(D/'module-inventory-check.json',dict(current_index=pin(inventorypath),helper=pin(ROOT/'tools/astis.py'),actual_module_count=509,source_import_declaration_inventory_equal=True,preserved_manifest=pin(preservepath),restored_unrelated_exact_science_paths=restored,restored_count=79,canonical_metadata_count=62,actual59_module=preserve['new_actual_module'],graph_edges_not_proof_certificates=True))
whitespace=load(R/'integration59/staging-whitespace/diagnosis.json');gz=R/'integration59/staging-whitespace/full-staged-immutable-negative.raw.gz';negative=gzip.decompress(gz.read_bytes());assert sha(negative)==whitespace['negative_raw_sha256']
assert len(whitespace['findings'])==274 and len(whitespace['exact_immutable_raw_paths'])==10 and whitespace['authored_complement_exit']==0 and not whitespace['full_staged_called_PASS']

visual=load(R/'visual.inspection.json');capture=load(R/'integration59/visual59/capture.json');assert len(capture['records'])==8 and capture['ownedBrowserExit']['code']==0
for x in pins(visual):checkpin(x)
for row in visual['capture_files']:checkpin(row)
write(D/'scoped-exposition-observation.json',dict(actor='/root/whole_math52',images_actually_viewed=['producer.png','producer-proof.png','producer-proof-late.png','consumer.png','consumer-proof.png','consumer-proof-late.png','branch-producer.png','branch-consumer.png'],actual_view_image_tools=['functions.exec with view_image, four images each, 7d3123/7bdc6a associated text outputs'],capture=pin(R/'integration59/visual59/capture.json'),capture_files=visual['capture_files'],DOM_records=[dict(label=x['label'],closedLeanDetails=x['closedLeanDetails'],mathContainers=x['mathContainers'],bodyVisibility=x['bodyVisibility'],bodyDisplay=x['bodyDisplay']) for x in capture['records']],independent_observations=['Complete original input assumptions and scope disclaimer readable, including rank0 and potentially infinite L2.', 'Six producer and four real-consumer formula steps render, with closed step disclosures and named statement/proof disclosures visible.', 'Exact rho/delta and centered-domain bounded inverse are described; full-space inverse/Gamma/main claims excluded.', 'Producer graph COMPILED/Registry-backed; Test graph PARTIAL/source-present remains conservative.', 'Graph edges explicitly distinguish solid module/import ownership from dashed incomplete references/correspondence.'],presentation_debts=['Dense duplicated inline complete statements and assumptions remain.', 'Long declaration labels wrap; tall branch requires zoom.', 'Existing broad full-reader/Chapter1.3 obligations remain separate.'],scoped_exposition_acceptance=True,full_Exposition_Seal_or_PURIFIED=False,no_new_browser=True,archived_browser_exit_code=0,archived_browser_PID=capture['pid'],HTTP_closure_evidence='Pinned capture implementation finally awaits server.close; root foreground exit reported; no new HTTP/browser process by reviewer'))
from tools import astis_advance as advance,astis_publication as pub
states=advance.current_advances();assert states['ASTIS-SA-20261008-PBPSCenteredDefectOperator']['state']=='VERIFIED'
assert [k for k,v in states.items() if v.get('state')=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
pub.check_advance(freeze['mathematical_declarations'],reviewed=True)
for row in maps:checkpin(row['snapshot'])
write(D/'native-checks.json',dict(native_object_inputs=objects,qualified_unique_pin_count=len(seen),all_qualified_pin_readbacks=list(seen.values()),used_historical_maps=list(used.values()),used_historical_map_count=len(used),math_frozen_count=27,complete_run_self_checks=4,distinct_native_payload_checks=4,prior_closed_lease_self_checks=3,root_publication_reviewed_gate=True,science_code_unchanged=[pin(p) for p in code],authored_fake_closure_count=0,source_fidelity_scope='Unchanged independent accepted two seven-slot source and complete mathematics reviews reused',root_capture_implementation=pin(R/'root-executed59/inspect-cdp59.mjs'),integration_notes=pin(R/'integration.notes.json'),visual_inspection=pin(R/'visual.inspection.json')))
print(json.dumps(dict(status='BOUNDED_REPOSITORY_AND_SCOPED_EXPOSITION_CHECKS_PASS_PENDING_FRESH_GRAPH',actual_reader_pid=os.getpid(),integration_entries=315,math_originals=27,native_pin_identities=len(seen),historical_maps_used=len(used),actual_terminal_gates=18,module_inventory=509,restored_unrelated_paths=79,canonical_metadata=62,images_viewed=8)),flush=True)
