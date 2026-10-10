import pathlib,json,hashlib,subprocess,os,gzip
ROOT=pathlib.Path('E:/Samplinglib');D=ROOT/'runs/20261007-companion-priority/pbps-centered-defect59/repository-exposition-seal59';R=D.parent
SCI='2d6cd0167adc4fae1d8d166068a2eda51cd3c3ad';HEAD='47a28adfa36bfa67ce201f9b3ff9823c85fc3b45'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 p=pathlib.Path(str(p).replace('\\','/'));b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def verify(row):
 a=pin(row['path']);assert a['bytes']==row.get('bytes',a['bytes']) and a['raw_sha256']==row['raw_sha256'] and a['lf_sha256']==row['lf_sha256'];assert a['lf_bytes']==row.get('lf_bytes',a['lf_bytes']);return a
def pins(q):
 if isinstance(q,dict):
  if {'path','raw_sha256','lf_sha256'}<=q.keys():yield q
  for v in q.values():yield from pins(v)
 elif isinstance(q,list):
  for v in q:yield from pins(v)
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==HEAD
assert subprocess.check_output(['git','rev-parse','HEAD^'],cwd=ROOT).decode().strip()==SCI
n=load(D/'native-checks.json');g=load(D/'integration.git-pins.json');fresh=load(D/'graph-successor.json');old=load(D/'graph-freshness.negative.json')
rows={}
def add(row):
 a=verify(row);rows[(a['path'],a['raw_sha256'],a['lf_sha256'])]=a
for x in n['all_qualified_pin_readbacks']:add(x['resolved'])
for x in n['native_object_inputs']:add(x)
for x in g['entries']:add(x['working'])
for row in pins(fresh):
 if row['path'].replace('\\','/')=='E:/Samplinglib/_site/data/underlying-lean-graph.json' and row['raw_sha256']==old['qualified_original_to_snapshot_mapping']['original']['raw_sha256']:continue
 add(row)
extra=[]
for label in ['site-check-final-admin','integration-push','integration-remote-snapshot']:
 p=R/'integration59'/label/'receipt.json';q=load(p);assert q['checked_science_parent']==HEAD and q['exit_code']==0 and q['terminal_closed'];add(pin(p))
 for x in pins(q):add(x)
 extra.append(dict(label=label,receipt=pin(p),actual_pid=q['actual_foreground_pid'],exit_code=0,terminal_closed=True,command=q['command']))
remote=load(R/'integration59/integration-remote-snapshot/stdout.log')
current=[x for x in remote if x['headSha']==HEAD]
assert all(x['status']=='completed' and x['conclusion']=='success' for x in current)
expected={'ASTIS Lean formalization','ASTIS website','ASTIS contributor contract'}
# Preserve exact native workflow names rather than inventing aliases.
assert {37791236055,37791236039,37791236018}<={x['databaseId'] for x in current}
for p in [R/'integration59/staging-whitespace/diagnosis.json',R/'integration59/staging-whitespace/full-staged-immutable-negative.raw.gz',D/'graph-freshness.before-admin-refresh.exactraw.json.gz']:
 add(pin(p))
for p in D.iterdir():
 if p.is_file() and p.suffix in ['.py','.json','.snapshot'] and p.name not in ['run.json','receipt.json','payload.json','input.manifest.json','lease.json','outputs.final.json','readback.json','finalizer.status.json','readback.status.json']:add(pin(p))
negative=gzip.decompress((D/'graph-freshness.before-admin-refresh.exactraw.json.gz').read_bytes());assert sha(negative)==old['qualified_original_to_snapshot_mapping']['original']['raw_sha256']
write(D/'input.manifest.json',dict(artifacts=list(rows.values()),count=len(rows),qualified_historical_readbacks=pin(D/'native-checks.json'),original_to_exact_snapshot_maps=pin(D/'historical-mappings.json'),graph_negative_exact_gzip_map=old['qualified_original_to_snapshot_mapping'],identity_rule='Full qualified path plus raw/LF SHA256 and bytes; original historical pins remain explicit and effective snapshots checked; no basename fallback'))
payload=dict(verdict='ACCEPT_SCOPED_REPOSITORY_AND_EXPOSITION_NO_MATHEMATICAL_OR_SOURCE_BLOCKER',checked_science_commit=SCI,checked_integration_commit=HEAD,
 exact_scope='Repository admission of actual59 centered selfadjoint squared-defect producer and centered bounded-inverse consumer; scoped readability of these two declarations only. No new VERIFIED transition or full Exposition/PURIFIED seal.',
 reasons=['Science code and sealed signatures exactly preserved across science/integration/current; complete prior mathematics/source/anonymous evidence remains CLOSED and strict native bindings check.',
 'Declaration-free shared leaf import, actual root Test consumer and one producer Registry entry preserve original probability/stationarity, full closed centered domain and same-operator sharp contraction route.',
 'Actual aggregate logs and standard3 closures support compiled claims; no authored fake closure or production import of Tests.',
 'Eight actual desktop captures independently viewed: full assumptions, six producer/four consumer formula steps and initially closed exact Lean disclosures readable; Test graph intentionally PARTIAL/source-present.',
 'Post-administration stale graph was rejected and archived exactly; independent successor comparison changes only publication_inputs_sha256, with all nodes/edges identical and full native digest matching current metadata.'],
 counts=dict(integration_committed_entries=315,math_originals=27,native_qualified_pin_identities=n['qualified_unique_pin_count'],historical_maps_used=n['used_historical_map_count'],complete_native_run_self_checks=4,distinct_native_payload_checks=4,original_terminal_gates=18,fresh_graph_and_site_successor_gates=4,total_terminal_gate_records=22,operational_push_and_current_remote_records=2,mandatory_root_jobs=9163,mandatory_Test_jobs=9454,combined_root_Test_jobs=9455,Registry=501,module_inventory=509,restored_unrelated_exact_paths=79,preserved_canonical_metadata=62,actual_images_viewed=8,authored_fake_closures=0),
 current_remote_success=current,remote_boundary='Exact integration workflows completed SUCCESS; does not establish merge/main/live deployment or reader purification.',
 fresh_graph=pin(D/'graph-successor.json'),current_native_graph_digest=fresh['native_full_graph_input_digest'],historical_negative=pin(D/'graph-freshness.negative.json'),
 unchanged_source_scope=n['source_fidelity_scope'],source_and_decoder_identity_roles_separate=True,
 residuals=['Gamma/root/polar/full weakH1/dynamics/main/error/cost/composition/full-paper/Goal obligations remain open.', 'Main merge/live/PURIFIED and full Chapter1.3 reader delivery are not granted.', 'Dense duplicated statements/assumptions, wrapped graph labels and tall branch layout remain presentation debts.', 'Name-scanned references are incomplete; LogConcaveOn.prod scanner hit is not a certified theorem edge; solid module/import ownership differs from dashed source references.', 'Full-staged whitespace remains NEGATIVE: 274 findings in10 exact immutable paths, gzip preserved; authored complement alone PASS.'],
 resources=dict(compiler='NOT_STARTED_CLOSED',browser='NOT_STARTED_CLOSED_BY_REVIEWER',HTTP='NOT_STARTED_CLOSED_BY_REVIEWER',actual_independent_reader_pids=[33572,45424],actual_negative_archive_pid=35192),
 publication_reviewed_actual=True,canonical_mutations=False,new_state_transition=False)
write(D/'payload.json',payload)
receipt=dict(verdict=payload['verdict'],checked_science_commit=SCI,checked_integration_commit=HEAD,scope=payload['exact_scope'],counts=payload['counts'],mathematics_blockers=[],source_blockers=[],presentation_debts=payload['residuals'],named_repository_exposition_payload_sha256=sha(canon(payload)),actual_finalizer_pid=os.getpid(),inputs=pin(D/'input.manifest.json'),payload=pin(D/'payload.json'),evidence=[pin(D/x) for x in ['native-checks.json','integration.git-pins.json','terminal-gates.json','module-inventory-check.json','scoped-exposition-observation.json','graph-successor.json','graph-freshness.negative.json']],additive_terminal_records=extra)
write(D/'receipt.json',receipt)
run=dict(schema='native-scoped-repository-exposition59-v1',actor='/root/whole_math52/repository-exposition59',checked_science_commit=SCI,checked_integration_commit=HEAD,actual_finalizer_pid=os.getpid(),independent_foreground_processes=[dict(pid=35192,exit_code=0,tool_chunk='9df594',scope='archive exact negative'),dict(pid=33572,exit_code=0,tool_chunk='0be31b',scope='bounded original repository/source/native checks'),dict(pid=45424,exit_code=0,tool_chunk='580373',scope='fresh graph native full digest and exact successor check')],input_manifest=pin(D/'input.manifest.json'),receipt=pin(D/'receipt.json'),named_repository_exposition_payload=payload,named_repository_exposition_payload_sha256=sha(canon(payload)),hash_recipes=dict(run_sha256='SHA256 of sorted compact UTF8 JSON complete run excluding ONLY top-level run_sha256',named_repository_exposition_payload_sha256='SHA256 of sorted compact UTF8 JSON named_repository_exposition_payload only',raw='SHA256 actual file bytes',LF='SHA256 actual bytes replacing CRLF pairs with LF only'),compiler='NOT_STARTED_CLOSED',final_close='Actual wrapper waits for finalizer/readback EXIT0 before writing lease CLOSEDLAST as final file mutation')
run['run_sha256']=sha(canon(run));write(D/'run.json',run)
print(json.dumps(dict(status='FINAL_OBJECTS_WRITTEN',pid=os.getpid(),inputs=len(rows),run_sha256=run['run_sha256'],payload_sha256=run['named_repository_exposition_payload_sha256'])),flush=True)
