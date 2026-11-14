from pathlib import Path
import sys,json,hashlib,gzip,subprocess,re,copy
sys.dont_write_bytecode=True;sys.path.insert(0,'tools')
import astis_advance as adv
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
D=Path('.astis/semantic-neutral-20261110/tl_src_e028af/normal-sourceV')
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-target-law-semantic-evidence')
O=E/'actual-source-V';C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-target-law.json');L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumTargetLaw';OWNER='huanjian_gc_20261110_fixed_spectrum_target_law';ACTOR='/root/targetlaw_fresh_source_9c7d21';carrier='56dbffcda73fa78539777059f26a964d9b53fa0c'
sha=lambda b:hashlib.sha256(b).hexdigest();dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==carrier and not O.exists() and not (W/'complete-actual-sourceV-carry-commit.json').exists()
assert sha((D/'manifest.json').read_bytes())=='5db42c52500126673e68dbe181e457b5dc881a198df9b4b237179144bd729a5d'
assert sha((D/'freeze_receipt.json').read_bytes())=='41b4b2dfe666961740f9e9d19cfcb3a2186d4e0b3addf35628cb472d25404475'
m=json.loads((D/'manifest.json').read_bytes());r=json.loads((D/'freeze_receipt.json').read_bytes());assert m['normal_API_calls']==r['normal_API_calls']==1 and r['normal_API_success']
files={}
for z in m['files']:
    p=D/z['path'];b=p.read_bytes();assert sha(b)==z['sha256'] and len(b)==z['bytes'] and p.stat().st_mode&0o777==0o444,p
    files[z['path']]=b
for n in ['manifest.json','freeze_receipt.json']:files[n]=(D/n).read_bytes()
actual={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and not p.is_symlink()};assert set(files)==actual
assert len(m['files'])==74 and sum(n.endswith(('.log','.log.gz')) for n in files)==13
for n,b in files.items():
    assert not re.search(rb'wxid_[a-z0-9]{8,}|/Library/Containers/com\.tencent',b,re.I),n
    assert 'PRIVATE-normal-sourceV-baseline/' not in n
app=files['actual-normal-VERIFIED-append.exact.jsonl'];assert sha(app)=='7a9f444ddfe6f7a420f1aada2803cdf8615a87a3d21418580ed1d57cab061340'
old=subprocess.check_output(['git','show',carrier+':'+str(L)]);now=L.read_bytes();assert now==old+app and len(app.splitlines())==1 and now.splitlines().count(app.rstrip(b'\n'))==1
event=json.loads(app);e=event['evidence'];assert len(e)==28 and event['worker_id']==ACTOR and e['verifier_id']==ACTOR and event['to_state']=='VERIFIED'
assert e==json.loads(files['actual-original-V-evidence.all-keys.json'])==json.loads(files['actual-original-V-evidence.exact.json'])
assert sha(files['actual-original-V-evidence.exact.json'])=='46bec60bb1b79a683475e00bbf13870ce85e75979f5ef6afc9bed0f70f54bc86'
assert json.loads(files['actual-normal-API-event.full-object.json'])==event
before=adv._replay_advances([json.loads(z) for z in old.splitlines()]);after=adv._replay_advances([json.loads(z) for z in now.splitlines()]);assert after[ADV]['state']=='VERIFIED' and after[ADV]['owner_id']==OWNER
assert {k:v for k,v in before.items() if k!=ADV}=={k:v for k,v in after.items() if k!=ADV}
assert after[ADV]['latest_evidence']==e
cb=json.loads(files['frontier.before.exact.json']);ca=json.loads(files['frontier.after.exact.json']);assert files['frontier.before.exact.json']==subprocess.check_output(['git','show',carrier+':'+str(C)]) and C.read_bytes()==files['frontier.after.exact.json']
assert cb['status']=='proved_locally' and ca['status']=='independently_verified' and 'integration_boundary' not in cb['evidence'] and 'integration_boundary' in ca['evidence']
rest=copy.deepcopy(ca);rest['status']=cb['status'];del rest['evidence']['integration_boundary'];assert rest==cb
assert r['all_foreign_states_frontiers_original_V_evidence_tracked_and_existing_queue_guards_passed'] and not r['private_raw_foreign_data_included']
def nodes(x):return 1+sum(nodes(v) for v in x.values()) if isinstance(x,dict) else 1+sum(nodes(v) for v in x) if isinstance(x,list) else 1
for n,b in files.items():
    p=O/n;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists();p.write_bytes(b);p.chmod(0o444)
q=E/'root-actual-source-V-exact-byte-carry.json';assert not q.exists();record={'scope':'Root exact-byte carry/readback only, not an independent source verdict or new normal transition.','actual_original_source_actor':ACTOR,'actual_source_API_calls':1,'root_source_API_calls':0,'actual_metadata_checked_commit':carrier,'actual_native_mathematical_commit':'8ee639d3aced826aa5b4e39fa6f8bedd3b830327','raw_actual_event_sha256':sha(app),'all_original_top_level_evidence_keys':list(e),'original_top_level_evidence_key_count':len(e),'all_recursive_JSON_nodes_including_root':nodes(e),'all_original_nested_values_equal_actual_event_and_replayed_state':True,'only_authorized_two_frontier_fields_changed':True,'all296_foreign_states_and_complete_raw_ledger_prefix_preserved':True,'original_private_baselines_not_carried':True,'all13_raw_or_gzip_logs_explicitly_included':True,'selected_original_files':[{'source_relative_to_portable_root':n,'destination':str(O/n),'bytes':len(b),'sha256':sha(b)} for n,b in sorted(files.items())],'force_stage_exact_own_files_to_override_Git_log_ignores':True,'global_site_browser_remote_publication_purification_or_Goal_credit':False};q.write_bytes(dump(record))
sp=E/'root-local-process-scripts/carry_actual_sourceV.py';assert not sp.exists();sp.write_bytes(Path(__file__).read_bytes())
rp=Path('.astis/huanjian-resume-20261103/20261110T115148436151Z-target-law-create-reviewed-metadata-carrier-exact-Git-tree.receipt.json');x=json.loads(rp.read_bytes());log=Path(x['log']).read_bytes();assert x['exit_code']==0 and sha(log)==x['log_sha256']
extra=[]
for p,b in [(E/'actual-review-layer-checks'/rp.name,rp.read_bytes()),(E/'actual-review-layer-checks'/(rp.stem+'.log.gz'),gzip.compress(log,mtime=0))]:assert not p.exists();p.write_bytes(b);extra.append(p)
frp=Path('.astis/huanjian-resume-20261103/20261110T121445067648Z-target-law-actual-sourceV-complete-exact-byte-carry-force-selected-logs.receipt.json');fx=json.loads(frp.read_bytes());flog=Path(fx['log']).read_bytes();assert fx['exit_code']==1 and sha(flog)==fx['log_sha256']
for p,b in [(E/'actual-review-layer-checks'/frp.name,frp.read_bytes()),(E/'actual-review-layer-checks'/(frp.stem+'.log.gz'),gzip.compress(flog,mtime=0))]:assert not p.exists();p.write_bytes(b);extra.append(p)
dp=E/'root-sourceV-carry-replay-field-diagnostic.json';assert not dp.exists();dp.write_bytes(dump({'class':'IMPLEMENTATION_FAILED','scope':'Root readback incorrectly expected replayed state.evidence; actual control-plane field is latest_evidence. The readonly first carry stopped before any copy/stage/commit, and before any source API (root never invokes it). Inspected actual state keys and changed only the root readback field. Original sourceV event and all original evidence remain unchanged; no API replay.','normal_source_API_calls_by_root':0}));extra.append(dp)
paths=[L,C,q,sp]+extra+[O/n for n in files];raws={str(p):p.read_bytes() for p in paths}
assert not subprocess.check_output(['git','diff','--cached','--name-only'])
subprocess.run(['git','add','-f','--']+list(raws),check=True)
staged=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines());assert staged==set(raws),(staged^set(raws))
for n,b in raws.items():assert subprocess.check_output(['git','show',':'+n])==b,n
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-m','Carry original independent Gaussian target-law verification and exact evidence'],check=True)
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for n,b in raws.items():assert subprocess.check_output(['git','show',commit+':'+n])==b,n
receipt={'complete_actual_sourceV_carry_commit':commit,'parent_metadata_carrier':carrier,'native_mathematical_commit':'8ee639d3aced826aa5b4e39fa6f8bedd3b830327','all76_original_portable_files_exact_in_Git_tree':len(files)==76,'all13_raw_or_gzip_logs_in_Git_tree':True,'actual_original_evidence_keys':len(e),'all_recursive_JSON_nodes_including_root':nodes(e),'raw_event_sha256':sha(app),'root_sourceV_API_calls':0,'no_global_or_public_push_or_Goal_credit':True};(W/'complete-actual-sourceV-carry-commit.json').write_bytes(dump(receipt));print(json.dumps(receipt))
