from pathlib import Path
import sys,json,hashlib,gzip,subprocess,re,copy
sys.dont_write_bytecode=True;sys.path.insert(0,'tools')
import astis_advance as adv
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
D=Path('.astis/semantic-neutral-20261110/z_src_2f8a71/normal-sourceV')
E=Path('research-wiki/paper-contributions/GaussianComplexity/zero-query-separation-semantic-evidence')
O=E/'actual-source-V'
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-zero-query-separation.json')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261110-GaussianComplexityZeroQuerySeparation'
OWNER='huanjian_gc_20261110_zero_query_separation'
ACTOR='/root/zeroquery_fresh_source_2f8a71'
carrier='5754f5db8afa4599aad14b28c09475c901da90f3'
native='eed870294de059136900110ade59b4a292a126ad'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==carrier
assert not O.exists() and not (W/'complete-actual-sourceV-carry-commit.json').exists()
assert sha((D/'manifest.json').read_bytes())=='b948b3335ab480b425df89075d712ac8b6da008ac60d1ff8f23fb1da4eb899cf'
assert sha((D/'freeze.receipt.json').read_bytes())=='49e5cc66e48d1751dfd480bff1faeef6d6329d6996ddb5d3a839971c96da0756'
m=json.loads((D/'manifest.json').read_bytes());r=json.loads((D/'freeze.receipt.json').read_bytes())
assert r['actual_API_invocations']==1 and r['root_API_invocations_for_target']==0 and r['no_retry_or_replay']
assert r['metadata_verified_commit']==carrier and r['native_math_commit']==native and r['reader']=='QUALIFIED/HOLD unchanged'
files={}
entries=m.get('files',m.get('payload_files'));assert isinstance(entries,list) and len(entries)==48
for z in entries:
    p=D/z['path'];b=p.read_bytes()
    assert not p.is_symlink() and sha(b)==z['sha256'] and len(b)==z['bytes'] and p.stat().st_mode&0o777==0o444,p
    files[z['path']]=b
for n in ['manifest.json','freeze.receipt.json']:
    p=D/n;assert p.stat().st_mode&0o777==0o444;files[n]=p.read_bytes()
assert set(files)=={str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and not p.is_symlink()}
assert len(files)==50
for n,b in files.items():
    assert not re.search(rb'wxid_[a-z0-9]{8,}|/Library/Containers/com\.tencent',b,re.I),n
    assert 'PRIVATE' not in n
app=files['actual-new-event.raw.jsonl']
assert sha(app)=='5be3aca3df5ee43600f4c705734b7f9f87d9e1e8568bd5bbe6352d8d9d3ac3bf'
old=subprocess.check_output(['git','show',carrier+':'+str(L)]);now=L.read_bytes()
assert now==old+app and len(app.splitlines())==1 and now.splitlines().count(app.rstrip(b'\n'))==1
event=json.loads(app);e=event['evidence']
assert event['advance_id']==ADV and event['worker_id']==ACTOR and event['from_state']=='PROVED_LOCAL' and event['to_state']=='VERIFIED'
assert e['verifier_id']==ACTOR and e['verified_commit']==carrier and e['native_commit']==native
assert len(e)==21 and e==json.loads(files['verification_evidence.json'])
assert sha(files['verification_evidence.json'])=='395912123d0134cdbdeedc1df4c569cf9b16c3459557dc4ac0fcded93b4f8d3f'
before=adv._replay_advances([json.loads(z) for z in old.splitlines()])
after=adv._replay_advances([json.loads(z) for z in now.splitlines()])
assert after[ADV]['state']=='VERIFIED' and after[ADV]['owner_id']==OWNER and after[ADV]['latest_evidence']==e
assert {k:v for k,v in before.items() if k!=ADV}=={k:v for k,v in after.items() if k!=ADV}
assert all(e[k]==v for k,v in before[ADV]['latest_evidence'].items())
cb=json.loads(files['own-C.before.raw.json']);ca=json.loads(files['own-C.after.raw.json'])
assert files['own-C.before.raw.json']==subprocess.check_output(['git','show',carrier+':'+str(C)])
assert C.read_bytes()==files['own-C.after.raw.json']
assert cb['status']=='proved_locally' and ca['status']=='independently_verified'
assert 'integration_boundary' not in cb['evidence'] and 'integration_boundary' in ca['evidence']
rest=copy.deepcopy(ca);rest['status']=cb['status'];del rest['evidence']['integration_boundary'];assert rest==cb
post=json.loads(files['postguard.json'])
assert post['state']=='PASS' and post['ledger_exact_original_full_prefix_plus_one_new_event']
assert post['all_prior_historical_VERIFIED_event_raw_bytes_exact'] and post['all_prior_historical_VERIFIED_count']==314
assert post['all_foreign_current_states_deep_exact'] and post['all_foreign_latest_evidence_deep_exact'] and post['old_queued10_deep_exact']
assert post['own_C_only_two_fields_changed'] and post['reader_HOLD']=='PRESERVED'
for g in ['foreign_file_guards_before_C','foreign_file_guards_after_C']:
    assert post[g]['existing_protected_file_byte_mode_differences']==0 and post[g]['tracked_set_index_unchanged']
assert r['private_directory_exported'] is False and r['original_source_phases_byte_mode_exact']
for n in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/ZeroQuerySeparation.lean','Tests/GaussianComplexityZeroQuerySeparation.lean','website/content/declaration_lessons/huanjian-zero-query-separation.json','website/content/publications/huanjian-zero-query-separation.json','lake-manifest.json','lean-toolchain']:
    assert Path(n).read_bytes()==subprocess.check_output(['git','show',native+':'+n])==subprocess.check_output(['git','show',carrier+':'+n]),n
def nodes(x):
    return 1+sum(nodes(v) for v in x.values()) if isinstance(x,dict) else 1+sum(nodes(v) for v in x) if isinstance(x,list) else 1
for n,b in files.items():
    p=O/n;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists();p.write_bytes(b);p.chmod(0o444)
q=E/'root-actual-source-V-exact-byte-carry.json';assert not q.exists()
record={'scope':'Root exact-byte carry/readback only, not a new source verdict or normal transition.','actual_original_source_actor':ACTOR,'actual_source_API_calls':1,'root_source_API_calls':0,'metadata_checked_commit':carrier,'native_mathematical_commit':native,'raw_actual_event_sha256':sha(app),'all_original_top_level_evidence_keys':list(e),'original_top_level_evidence_key_count':len(e),'all_recursive_JSON_nodes_including_root':nodes(e),'all_original_nested_values_equal_actual_event_and_replayed_state':True,'all_original_PROVED_LOCAL_nested_values_retained_in_original_V':True,'only_authorized_two_frontier_fields_changed':True,'exact_original_postguard':post,'exact_original_freeze':r,'all50_original_portable_regular_files_exact':True,'selected_original_files':[{'source_relative_to_portable_root':n,'destination':str(O/n),'bytes':len(b),'sha256':sha(b)} for n,b in sorted(files.items())],'private_full_foreign_baselines_not_carried':True,'explicit_force_staging_overrides_log_ignores':True,'static_reader_neighbor_HOLD_retained':True,'global_site_browser_remote_publication_purification_or_Goal_credit':False}
q.write_bytes(dump(record))
sp=E/'root-local-process-scripts/carry_actual_sourceV.py';assert not sp.exists();sp.write_bytes(Path(__file__).read_bytes())
rp=Path('.astis/huanjian-resume-20261103/20261110T141517692926Z-zero-query-immutable-accepted-reviews-static-HOLD-carrier.receipt.json')
x=json.loads(rp.read_bytes());log=Path(x['log']).read_bytes();assert x['exit_code']==0 and sha(log)==x['log_sha256']
extra=[]
for p,b in [(E/'actual-review-layer-checks'/rp.name,rp.read_bytes()),(E/'actual-review-layer-checks'/(rp.stem+'.log.gz'),gzip.compress(log,mtime=0))]:
    assert not p.exists();p.write_bytes(b);extra.append(p)
paths=[L,C,q,sp]+extra+[O/n for n in files];raws={str(p):p.read_bytes() for p in paths}
assert not subprocess.check_output(['git','diff','--cached','--name-only'])
assert set(subprocess.check_output(['git','diff','--name-only'],text=True).splitlines())=={str(L),str(C)}
subprocess.run(['git','add','-f','--']+list(raws),check=True)
staged=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert staged==set(raws),(staged^set(raws))
for n,b in raws.items():assert subprocess.check_output(['git','show',':'+n])==b,n
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-m','Carry original Gaussian event-gap verification and preserve reader HOLD'],check=True)
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for n,b in raws.items():assert subprocess.check_output(['git','show',commit+':'+n])==b,n
receipt={'complete_actual_sourceV_carry_commit':commit,'parent_metadata_carrier':carrier,'native_mathematical_commit':native,'all50_original_portable_files_exact_in_Git_tree':True,'all_original_evidence_keys':len(e),'all_recursive_JSON_nodes_including_root':nodes(e),'raw_event_sha256':sha(app),'root_sourceV_API_calls':0,'reader_neighbor_HOLD_retained':True,'no_global_public_push_or_Goal_credit':True}
(W/'complete-actual-sourceV-carry-commit.json').write_bytes(dump(receipt));print(json.dumps(receipt))
