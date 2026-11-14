from pathlib import Path
from datetime import datetime, timezone
import os, sys, json, hashlib, subprocess, stat, copy, tarfile, gzip, traceback
sys.dont_write_bytecode=True
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC');sys.path.insert(0,str(ROOT))
from tools import astis_advance as api
OUT=Path(__file__).resolve().parent
PRIVATE=OUT.parent/'PRIVATE-normal-sourceV-baseline'
ADV='ASTIS-SA-20261110-GaussianComplexityZeroQuerySeparation'
ACTOR='/root/zeroquery_fresh_source_2f8a71'
OWNER='huanjian_gc_20261110_zero_query_separation'
HEAD='5754f5db8afa4599aad14b28c09475c901da90f3'
NATIVE='eed870294de059136900110ade59b4a292a126ad'
BASE='37eea55086ce04651d5b8f8a7348bc16d1b157cb'
LEDGER=ROOT/'runs/substantive_advances.jsonl'
C=ROOT/'research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-zero-query-separation.json'
E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/zero-query-separation-semantic-evidence'
ND=ROOT/'.astis/huanjian-gc-zero-query-20261110/independent-native-reader-6c82f1'
CONFIG=ROOT/'.astis/huanjian-gc-zero-query-20261110/sourceV-exact-foreign-control-paths.json'
MARKER=OUT/'PERMANENT-API-ONCE.marker.json'
def digest(b):return hashlib.sha256(b).hexdigest()
def readj(p):return json.loads(p.read_text())
def writej(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.now(timezone.utc).isoformat()
def git(*args):
 r=subprocess.run(['git',*args],cwd=ROOT,capture_output=True)
 assert r.returncode==0,(args,r.stderr.decode());return r.stdout
def ledger_state(b):
 assert b.endswith(b'\n');rows=[json.loads(x) for x in b.splitlines() if x];return rows,api._replay_advances(rows)
def finfo(p):
 s=p.lstat()
 if stat.S_ISLNK(s.st_mode):return {'kind':'symlink','target':os.readlink(p),'mode':stat.S_IMODE(s.st_mode)}
 if stat.S_ISDIR(s.st_mode):
  rel=str(p.relative_to(ROOT));entry=git('ls-files','--stage','--',rel).decode()
  actualroot=Path(git('-C',str(p),'rev-parse','--show-toplevel').decode().strip())
  assert actualroot.resolve()==p.resolve(),'Only an actual nested Git repository may be a directory entry'
  gd=Path(git('-C',str(p),'rev-parse','--absolute-git-dir').decode().strip())
  refs={}
  meta=[gd/'HEAD',gd/'packed-refs']
  if (gd/'refs').is_dir():meta.extend(q for q in (gd/'refs').rglob('*') if q.is_file())
  for q in meta:
   if q.is_file():refs[str(q.relative_to(gd))]={'bytes':q.stat().st_size,'sha256':digest(q.read_bytes())}
  indexstat=None
  if (gd/'index').exists():
   t=(gd/'index').stat();indexstat={'bytes':t.st_size,'mtime_ns':t.st_mtime_ns,'inode':t.st_ino,'mode':stat.S_IMODE(t.st_mode)}
  return {'kind':'tracked-gitlink' if entry.startswith('160000 ') else 'foreign-untracked-nested-repository','index_entry':entry,'actual_HEAD':git('-C',str(p),'rev-parse','HEAD').decode().strip(),'directory_identity':{'dev':s.st_dev,'inode':s.st_ino,'mtime_ns':s.st_mtime_ns,'mode':stat.S_IMODE(s.st_mode)},'Git_HEAD_refs_metadata':refs,'Git_index_stat_only':indexstat,'scope':'Explicit authorized exception: directory identity plus Git HEAD/refs metadata and index stat only; no ATLAS body, semantic inventory/index/projections or nested worktree content read/hash/glob'}
 assert stat.S_ISREG(s.st_mode),str(p)
 b=p.read_bytes();return {'kind':'regular','bytes':len(b),'sha256':digest(b),'mode':stat.S_IMODE(s.st_mode)}
def excluded(rel):
 return rel in {str(C.relative_to(ROOT)),str(LEDGER.relative_to(ROOT))} or rel.startswith(str(OUT.relative_to(ROOT))+'/') or rel.startswith(str(PRIVATE.relative_to(ROOT))+'/')
def inventory(paths):
 return {x:finfo(ROOT/x) for x in sorted(set(paths)) if not excluded(x)}
def tracked_paths():return git('ls-files','-z').decode().strip('\0').split('\0')
def untracked_paths():
 b=git('ls-files','--others','--exclude-standard','-z');return [x for x in b.decode().split('\0') if x]
def replay_guard(before,after):
 a={k:v for k,v in before.items() if k!=ADV};b={k:v for k,v in after.items() if k!=ADV}
 return {'all_foreign_replayed_states_deep_exact':a==b,
  'all_foreign_latest_evidence_deep_exact':{k:v.get('latest_evidence') for k,v in a.items()}=={k:v.get('latest_evidence') for k,v in b.items()}}
def inputs():
 assert git('rev-parse','HEAD').decode().strip()==HEAD
 assert digest(CONFIG.read_bytes())=='929a41d3a5286edba03022b8bc5559b4fa9c29e7cc604622041bf0f8521eac62'
 config=readj(CONFIG)
 assert len(config['old10_queued_advance_ids'])==10 and len(config['exact_existing_foreign_control_paths'])==696
 p3=OUT.parent/'phase3';proposal=readj(p3/'source_review_proposal.json')
 assert digest((p3/'source_review_proposal.json').read_bytes())=='d0ad989c10877211b93a73cecb6be3714fc3ffb15ecb442577f813a98ded6ac6'
 auditpath=ROOT/'research-wiki/semantic-roundtrip/audits/huanjian-zero-query-separation.json';audit=readj(auditpath)
 assert {k:audit[k] for k in proposal}==proposal
 immutable=[
  'AutoSamplingTheory/ExampleCases/GaussianComplexity/ZeroQuerySeparation.lean',
  'Tests/GaussianComplexityZeroQuerySeparation.lean',
  'website/content/declaration_lessons/huanjian-zero-query-separation.json',
  'website/content/publications/huanjian-zero-query-separation.json',
  'research-wiki/paper-contributions/GaussianComplexity/zero-query-separation-statement-seal.json',
  str((E/'source-to-lean-map-v1.json').relative_to(ROOT)),
  'lake-manifest.json','lean-toolchain']
 hashes={}
 for rel in immutable:
  a=(ROOT/rel).read_bytes();assert a==git('show',HEAD+':'+rel)==git('show',NATIVE+':'+rel);hashes[rel]=digest(a)
 assert hashes[immutable[0]]=='daa1be30e9478fdc744b0dce75e7accd0859dcc67123cfa5a411eed5045a2a92'
 assert hashes[immutable[1]]=='2df4300e09f0ee12ee9448a68517d7dc0b5b01e41f644797bf1bf6f7d71a4406'
 assert (C.read_bytes())==git('show',HEAD+':'+str(C.relative_to(ROOT)))
 nm=readj(ND/'manifest.json');assert digest((ND/'manifest.json').read_bytes())=='ece9f8b0d701ee77fe68a1c758e1d479200c494f03368e5dbd8e578d0f859af5'
 assert digest((ND/'freeze.receipt.json').read_bytes())=='72536a68929170162a582e39f3cdadec991b564ebc3dbae623e0bf4e1b103406'
 assert len(nm['raw_files'])==256 and nm['symlinks']==[]
 for r in nm['raw_files']:
  p=ND/r['path'];assert p.stat().st_size==r['bytes'] and digest(p.read_bytes())==r['sha256'];assert stat.S_IMODE(p.stat().st_mode)==0o444
 judgment=readj(ND/'judgment.json');assert judgment['candidate']==NATIVE and judgment['native_judgment']=='PASS within exact candidate scope'
 assert 'HOLD' in judgment['static_judgment'] and 'no adjacent T source/download' in judgment['static_limit']
 archives=[('independent-full-source-all-phases.lossless-file-bytes.tar.gz','23b8a9d52bfe1434f18ca4791f56d6026517b165ab653a55e6709a1e05e71215',OUT.parent,191),('independent-native-fullmodule-static.lossless-file-bytes.tar.gz','c4fc46c6e8017c38ef4a6f96b12284718c3e7b31694af1997c285deb876f36c0',ND,258)]
 archivechecks=[]
 for name,h,origin,n in archives:
  p=E/name;assert digest(p.read_bytes())==h
  with tarfile.open(p,'r:gz') as t:
   members=t.getmembers();assert len(members)==n
   for m in members:
    assert m.isfile() and not Path(m.name).is_absolute() and '..' not in Path(m.name).parts
    assert t.extractfile(m).read()==(origin/m.name).read_bytes()
  archivechecks.append({'archive':str(p.relative_to(ROOT)),'sha256':h,'members':n,'all_original_bytes_exact':True})
 gates=[]
 for name in ['20261110T141454565300Z-zero-query-reviewed-publication','20261110T141454564049Z-zero-query-reviewed-semantic','20261110T141454564893Z-zero-query-reviewed-frontier','20261110T141454565275Z-zero-query-reviewed-contributor']:
  rp=ROOT/'.astis/huanjian-resume-20261103'/ (name+'.receipt.json');r=readj(rp);log=Path(r['log']).read_bytes()
  assert r['exit_code']==0 and r['head_before']==r['head_after']==NATIVE and digest(log)==r['log_sha256']
  if 'publication' in name or 'contributor' in name:assert r['command'][-2:]==['--base',BASE]
  (OUT/(name+'.receipt.raw.json')).write_bytes(rp.read_bytes());(OUT/(name+'.log.raw')).write_bytes(log)
  gates.append({'receipt':name+'.receipt.raw.json','receipt_sha256':digest(rp.read_bytes()),'log_sha256':digest(log),'actual_exit_code':0,'observed_head':NATIVE})
 # Independently preserve source/native judgments and procedural selector; no full foreign snapshots here.
 (OUT/'source_review_proposal.raw.json').write_bytes((p3/'source_review_proposal.json').read_bytes())
 (OUT/'native-judgment.raw.json').write_bytes((ND/'judgment.json').read_bytes())
 (OUT/'native-manifest.raw.json').write_bytes((ND/'manifest.json').read_bytes())
 (OUT/'native-freeze.receipt.raw.json').write_bytes((ND/'freeze.receipt.json').read_bytes())
 # Selector contains foreign paths, so its full bytes remain PRIVATE.
 (PRIVATE/'foreign-selector.raw.json').write_bytes(CONFIG.read_bytes())
 writej(OUT/'input-checks.json',{'checked_at':now(),'metadata_commit':HEAD,'native_math_commit':NATIVE,'immutable_hashes':hashes,'applied_five_field_proposal_deep_exact':True,'archive_checks':archivechecks,'gates':gates,'control_selector_sha256':digest(CONFIG.read_bytes()),'source_actor':ACTOR,'native_actor':'/root/zeroquery_native_reader_6c82f1','reader':'QUALIFIED/HOLD preserved; no delivery credit'})
 return config,audit,judgment

def preflight():
 assert not MARKER.exists(),'Permanent API-once marker exists; do not replay'
 assert not (PRIVATE/'baseline.json').exists(),'Baseline exists; inspect instead of replacing'
 config,audit,judgment=inputs()
 before=LEDGER.read_bytes();rows,state=ledger_state(before);own=state[ADV]
 assert own['state']=='PROVED_LOCAL' and own['owner_id']==OWNER
 assert not [r for r in rows if r.get('advance_id')==ADV and r.get('to_state')=='VERIFIED']
 assert all(state[x]['state']=='VERIFIED' for x in config['old10_queued_advance_ids'])
 tp=tracked_paths();up=untracked_paths()
 frontiers=[str(p.relative_to(ROOT)) for p in (ROOT/'research-wiki/frontier-cells').rglob('*') if p.is_file()]
 controls=config['exact_existing_foreign_control_paths']
 assert all((ROOT/p).is_file() and (ROOT/p).stat().st_size<=config['max_selected_file_bytes'] for p in controls)
 allpaths=tp+up+frontiers+controls
 protected=inventory(allpaths)
 # Full foreign snapshots are PRIVATE. Never glob ignored dirs or huge Expr output.
 (PRIVATE/'ledger.before.raw.jsonl').write_bytes(before)
 writej(PRIVATE/'states.before.full.json',state)
 writej(PRIVATE/'protected-files.before.full.json',protected)
 writej(PRIVATE/'git-tracked-paths.before.json',tp);writej(PRIVATE/'git-untracked-paths.before.json',up)
 (PRIVATE/'git-status.before.raw').write_bytes(git('status','--porcelain=v1','-z','--untracked-files=all'))
 (PRIVATE/'git-index.before.raw').write_bytes(git('ls-files','--stage','-z'))
 snap=PRIVATE/'control-frontier-original-bytes';snap.mkdir()
 for p in sorted(set(controls+frontiers)):
  if excluded(p):continue
  q=ROOT/p
  if q.is_file() and not q.is_symlink():(snap/digest(p.encode())).write_bytes(q.read_bytes())
 baseline={'head':HEAD,'ledger_sha256':digest(before),'ledger_bytes':len(before),'ledger_rows':len(rows),'own':own,'own_C':readj(C),'protected':protected,'tracked_paths':tp,'untracked_paths':up,'frontier_paths':frontiers,'control_paths':controls,'old10':config['old10_queued_advance_ids']}
 writej(PRIVATE/'baseline.json',baseline)
 (OUT/'own-C.before.raw.json').write_bytes(C.read_bytes())
 (OUT/'own-events.before.raw.jsonl').write_bytes(b''.join(line+b'\n' for line in before.splitlines() if json.loads(line).get('advance_id')==ADV))
 # Real current reviewed publication/source gate, not a manual green flag.
 from tools.astis_publication import check_advance
 check_advance(list(own['publication_declarations']),reviewed=True)
 assert LEDGER.read_bytes()==before and readj(C)==baseline['own_C']
 diffs=[p for p,info in protected.items() if not (ROOT/p).exists() or finfo(ROOT/p)!=info]
 assert not diffs,('preflight foreign changes',len(diffs))
 writej(OUT/'preflight.json',{'state':'PASS','actual_at':now(),'metadata_HEAD':HEAD,'native_commit':NATIVE,'target_before':'PROVED_LOCAL','proof_owner':OWNER,'verifier':ACTOR,'target_prior_VERIFIED_events':0,'root_target_VERIFIED_events':0,'old_queued_packet_count':10,'old_queued_all_VERIFIED':True,'all_library_current_VERIFIED_count':sum(v.get('state')=='VERIFIED' for v in state.values()),'historical_VERIFIED_raw_event_count':sum(r.get('to_state')=='VERIFIED' for r in rows),'ledger_prefix_sha256':digest(before),'ledger_prefix_bytes':len(before),'ledger_rows':len(rows),'all_foreign_latest_evidence_snapshot_deep':True,'protected_existing_entries':len(protected),'nested_repository_exception':'Actual ordinary-untracked .atlas-upstream/ is not a tracked gitlink. Protect directory identity and Git HEAD/refs metadata plus Git index stat only; do not claim nested worktree-body byte hashes. Root explicitly authorized this limited non-mathematical preservation guard; no ATLAS body/semantic inventory/index/projection read/hash/glob. All other tracked/ordinary regular-untracked/control/frontier files retain exact byte/mode guards.','foreign_frontier_files':len([p for p in frontiers if not excluded(p)]),'ignored_control_files':len(controls),'existing_foreign_untracked_entries':len([p for p in up if not excluded(p)]),'private_baseline_sha256':digest((PRIVATE/'baseline.json').read_bytes()),'reviewed_check_advance_actual_pass':True,'preflight_foreign_differences':0,'permanent_marker_not_yet_created':True,'api_calls':0,'reader_HOLD':judgment['static_judgment'],'global_integration':'OPEN; no STAB/global/source-index/graph/browser/purification/Goal authority'})
 print(json.dumps(readj(OUT/'preflight.json'),ensure_ascii=False,indent=2))

def guard(baseline,allow_ledger_change=False):
 assert git('rev-parse','HEAD').decode().strip()==HEAD
 bad=[p for p,info in baseline['protected'].items() if not (ROOT/p).exists() or finfo(ROOT/p)!=info]
 assert not bad,('Foreign byte/mode guard failed',len(bad),digest(json.dumps(bad).encode()))
 assert git('ls-files','--stage','-z')==(PRIVATE/'git-index.before.raw').read_bytes(),'Git index changed'
 assert set(tracked_paths())==set(baseline['tracked_paths']),'Tracked path set changed'
 if not allow_ledger_change:assert LEDGER.read_bytes()==(PRIVATE/'ledger.before.raw.jsonl').read_bytes()
 return {'existing_protected_file_byte_mode_differences':0,'tracked_set_index_unchanged':True,'new_conflict_free_untracked_count':len(set(untracked_paths())-set(baseline['untracked_paths']))}

def execute():
 assert readj(OUT/'preflight.json')['state']=='PASS'
 b=readj(PRIVATE/'baseline.json');guard(b);assert readj(C)==b['own_C']
 prior=copy.deepcopy(b['own']['latest_evidence']);evidence=copy.deepcopy(prior)
 extra={
  'verifier_id':ACTOR,'verified_commit':HEAD,'native_commit':NATIVE,
  'gate':{'source':'Own independent raw-first/full-code semantic proposal accepted, original actor preserved and exact five fields applied','native':'Independent6c82f1 strict fresh compiler+kernel PASS at eed870; cached normal build not used as fresh evidence','metadata':'Four actual reviewed publication/semantic/frontier/contributor checks PASS; current reviewed check_advance passed preflight and runs within actual API','reader':'QUALIFIED/HOLD: privateT lacks adjacent source/download; TsourceHTML lacks download action. No full delivery credit'},
  'source_audit':readj(OUT/'source_review_proposal.raw.json'),
  'fake_closure_scan':{'independent_native_judgment':readj(OUT/'native-judgment.raw.json'),'all_owned_handwritten':2,'generated':0,'all_reachable':True,'recursive_axioms':['propext','Classical.choice','Quot.sound'],'producer_ASTIS_parents':[],'consumer_ASTIS_parents':['AutoSamplingTheory.ExampleCases.GaussianComplexity.ZeroQuerySeparation.actual_zero_query_gaussian_event_gap']},
  'normal_sourceV_layers':{'metadata_verified_commit':HEAD,'mathematical_native_commit':NATIVE,'proof_owner_unchanged':OWNER,'source_verifier_actual_actor':ACTOR,'source_proposal_sha256':'d0ad989c10877211b93a73cecb6be3714fc3ffb15ecb442577f813a98ded6ac6','preflight_sha256':digest((OUT/'preflight.json').read_bytes()),'input_checks_sha256':digest((OUT/'input-checks.json').read_bytes()),'old_PL_evidence_all_topkeys_nested_values_preserved':True,'historical_source_VERIFIED_or_global_false_is_retained_PL_metadata':True,'no_root_sourceV_or_role_substitution':True},
  'reader_delivery_boundary':{'state':'HOLD','private_T_adjacent_source_download':'HOLD','T_source_HTML_download_action':'HOLD','global_site_source_index_graph':'OPEN','browser_desktop_mobile_MathJax':'OPEN','purification_Exposition_Seal':'OPEN','whole_Goal':'OPEN','artifact_existence_is_not_delivery':True},
  'integration_boundary':{'local_only':True,'common_probability_law_not_algorithm_model':True,'Borel_seed_stopping_output_deterministic_cap_adapter':'OPEN','source_precision_class_uniform_accuracy_instantiation':'OPEN','T_ge_one_QG_complete_Theorem3_1':'OPEN','known_spectrum':'NOT_PROVED; pair has different spectra','separate_conditional_integer_branch':'OPEN','original_proof_owner':OWNER,'foreign_integration_owner':'Preserved; existing stabilizing lane occupied, no takeover','STAB_global_merge_release_push':'NOT_AUTHORIZED','reader_HOLD_preserved':True},
  'original_VERIFIED_evidence_preservation_contract':'This entire initial VERIFIED evidence object is the original V record. Preserve every topkey and nested value; only this verifier may later append post_integration, never shrink to a whitelist.'
 }
 assert not set(prior)&set(extra),'New evidence would overwrite original PL topkey'
 evidence.update(extra);assert all(evidence[k]==v for k,v in prior.items())
 writej(OUT/'verification_evidence.json',evidence)
 # Marker is permanent even on exception or failed postguard. Exclusive creation
 # occurs before the one API call. No code path deletes it or retries the API.
 fd=os.open(MARKER,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o444)
 with os.fdopen(fd,'w') as f:
  json.dump({'created_at':now(),'advance':ADV,'actor':ACTOR,'metadata_commit':HEAD,'native_commit':NATIVE,'evidence_sha256':digest((OUT/'verification_evidence.json').read_bytes()),'authorization':'Exactly one PROVED_LOCAL->VERIFIED call; never replay after uncertainty'},f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 error=None
 try:
  api.transition_advance(ADV,'VERIFIED',worker_id=ACTOR,modes=['independent-source-review','independent-native-evidence-acceptance'],evidence=evidence)
 except BaseException:
  error=traceback.format_exc();(OUT/'api.exception.raw.txt').write_text(error)
 after=LEDGER.read_bytes();(PRIVATE/'ledger.after-api.raw.jsonl').write_bytes(after)
 rows,state=ledger_state(after);before=(PRIVATE/'ledger.before.raw.jsonl').read_bytes();oldrows,oldstate=ledger_state(before)
 appended=after[len(before):] if after.startswith(before) else b''
 newrows=[json.loads(x) for x in appended.splitlines() if x]
 writej(OUT/'api-result.json',{'actual_after':now(),'api_invocations':1,'exception':bool(error),'full_ledger_prefix_exact':after.startswith(before),'before_bytes':len(before),'after_bytes':len(after),'before_sha256':digest(before),'after_sha256':digest(after),'appended_rows':len(newrows),'actual_target_state':state.get(ADV,{}).get('state'),'no_replay_permitted':True})
 assert after.startswith(before) and len(newrows)==1,'Inspect actual PRIVATE ledger: prefix/newrow unexpected; never replay'
 row=newrows[0];assert row['advance_id']==ADV and row['from_state']=='PROVED_LOCAL' and row['to_state']=='VERIFIED' and row['worker_id']==ACTOR and row['evidence']==evidence
 assert state[ADV]['owner_id']==OWNER and state[ADV]['last_actor']==ACTOR and state[ADV]['latest_evidence']==evidence
 (OUT/'actual-new-event.raw.jsonl').write_bytes(appended)
 foreign=replay_guard(oldstate,state);assert all(foreign.values())
 oldV=[x for x in before.splitlines(keepends=True) if json.loads(x).get('to_state')=='VERIFIED']
 afterprefixV=[x for x in after[:len(before)].splitlines(keepends=True) if json.loads(x).get('to_state')=='VERIFIED'];assert oldV==afterprefixV
 pg=guard(b,True);assert all(state[x]==oldstate[x] for x in b['old10'])
 assert not error,'API exception occurred; actual ledger inspected; no replay or C write'
 # Only two authorized C semantic fields change; every other nested value stays.
 cb=copy.deepcopy(b['own_C']);ca=copy.deepcopy(cb);ca['status']='independently_verified'
 ca['evidence']['integration_boundary']={'verified_commit':HEAD,'native_commit':NATIVE,'normal_source_verifier':ACTOR,'original_proof_owner':OWNER,'actual_VERIFIED_event_sha256':digest(appended),'event_evidence_sha256':digest((OUT/'verification_evidence.json').read_bytes()),'local_scope':'Accepted signed Gaussian event-gap auxiliary and private arbitrary-common-probability-law TV obstruction only','source_algorithm_model_T_ge_1_QG':'OPEN; genuine Borel seed/stopping/output/cap/common-law and precision-class/uniform-accuracy adapters remain','known_spectrum':'NOT_PROVED; two inputs have different spectra','reader':'QUALIFIED/HOLD on privateT adjacent source/download and TsourceHTML download action; no complete delivery','global_site_source_index_graph_browser_desktop_mobile':'OPEN','purification_Exposition_Seal_Goal':'OPEN','integration_owner':'Foreign occupied lane preserved; no STAB/takeover/global/release/push','historical_evidence':'All preexisting C evidence and original V evidence preserved verbatim; later only original verifier may append post_integration without shrinking any nested value'}
 writej(C,ca);(OUT/'own-C.after.raw.json').write_bytes(C.read_bytes())
 ca_check=readj(C);tmp=copy.deepcopy(ca_check);tmp['status']=cb['status'];tmp['evidence'].pop('integration_boundary')
 original=copy.deepcopy(cb);original['evidence'].pop('integration_boundary',None)
 assert tmp==original
 writej(OUT/'frontier-two-field-diff.json',{'allowed_paths_only':['status','evidence.integration_boundary'],'status':{'before':cb['status'],'after':ca_check['status']},'integration_boundary':{'before_present':'integration_boundary' in cb['evidence'],'before':cb['evidence'].get('integration_boundary'),'after':ca_check['evidence']['integration_boundary']},'all_other_nested_values_exact':True})
 final=LEDGER.read_bytes();assert final==after
 _,finalstate=ledger_state(final);assert all(replay_guard(oldstate,finalstate).values())
 pg2=guard(b,True)
 writej(PRIVATE/'states.after.full.json',finalstate)
 (PRIVATE/'git-status.after.raw').write_bytes(git('status','--porcelain=v1','-z','--untracked-files=all'))
 writej(OUT/'postguard.json',{'state':'PASS','completed_at':now(),'actual_event':{'advance_id':ADV,'from_state':row['from_state'],'to_state':row['to_state'],'worker_id':row['worker_id'],'proof_owner_after':finalstate[ADV]['owner_id'],'created_at':row['created_at'],'raw_event_sha256':digest(appended)},'ledger_exact_original_full_prefix_plus_one_new_event':True,'all_prior_historical_VERIFIED_event_raw_bytes_exact':True,'all_prior_historical_VERIFIED_count':len(oldV),'all_foreign_current_states_deep_exact':foreign['all_foreign_replayed_states_deep_exact'],'all_foreign_latest_evidence_deep_exact':foreign['all_foreign_latest_evidence_deep_exact'],'old_queued10_deep_exact':True,'foreign_file_guards_before_C':pg,'foreign_file_guards_after_C':pg2,'own_C_only_two_fields_changed':True,'all_original_PL_evidence_nested_values_carried_into_V':True,'api_invocations':1,'root_target_API_count':0,'private_snapshots_exported':False,'reader_HOLD':'PRESERVED','STAB_global_site_graph_browser_purification_Goal':'OPEN and unauthorized'})
 print(json.dumps(readj(OUT/'postguard.json'),ensure_ascii=False,indent=2))

if __name__=='__main__':
 assert len(sys.argv)==2 and sys.argv[1] in {'preflight','execute'}
 {'preflight':preflight,'execute':execute}[sys.argv[1]]()
