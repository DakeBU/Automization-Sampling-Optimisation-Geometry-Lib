from pathlib import Path
import os,json,hashlib,stat,subprocess,sys,datetime,concurrent.futures
ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
S=ROOT/'.astis/semantic-neutral-20261111/kr_src_c47e12'
P=S/'phase5-normal-sourceV'
PRIVATE=S/'private-phase5-preservation'
W=ROOT/'.astis/huanjian-gc-fixed-spectrum-krylov-range-20261110'
ADV='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumKrylovRange'
FRONT='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json'
LEDGER='runs/substantive_advances.jsonl'
ACTOR='/root/krylov_fresh_source_c47e12'
OWNER='huanjian_gc_20261110_fixed_spectrum_krylov_range'
EXPECTED_HEAD='d4ff03bf3574da615cca39a812cd9b442dca47f0'
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(path,data):
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 os.chmod(path,0o600)
def git(args,label):
 env=dict(os.environ);env['GIT_OPTIONAL_LOCKS']='0'
 argv=['git']+args
 r=subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env)
 (PRIVATE/(label+'.stdout')).write_bytes(r.stdout);(PRIVATE/(label+'.stderr')).write_bytes(r.stderr)
 dump(PRIVATE/(label+'.receipt.json'),{'argv':argv,'cwd':str(ROOT),'exit_code':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)})
 if r.returncode:raise RuntimeError('readonly Git guard failed '+label)
 return r.stdout
def relpath(value):
 path=Path(value)
 if path.is_absolute():return str(path.relative_to(ROOT))
 return str(path)
def excluded_reason(rel,size):
 parts=Path(rel).parts;low=rel.lower()
 if rel.startswith(str(P.relative_to(ROOT)))or rel.startswith(str(PRIVATE.relative_to(ROOT))):return 'own-operational-output'
 if any('atlas'in part.lower()for part in parts):return 'forbidden-ATLAS-content-index-projection-derivatives-metadata-only'
 if 'c8'in low and size>8*1024*1024:return 'giant-C8-dump-metadata-only'
 if any((part.lower().startswith('private-')or'.private'in part.lower())for part in parts)and rel.startswith('.astis/'):return 'foreign-private-operational-snapshot-metadata-only'
 return None
def one_record(rel):
 path=ROOT/rel
 try:s=path.lstat()
 except FileNotFoundError:return {'kind':'absent'}
 mode=stat.S_IMODE(s.st_mode)
 reason=excluded_reason(rel,s.st_size)
 if reason:return {'kind':'excluded-metadata-only','reason':reason,'mode':mode,'size':s.st_size,'mtime_ns':s.st_mtime_ns}
 if stat.S_ISLNK(s.st_mode):return {'kind':'symlink-metadata-only','mode':mode,'target':os.readlink(path)}
 if stat.S_ISDIR(s.st_mode):return {'kind':'directory-or-nested-repository-metadata-only','mode':mode,'mtime_ns':s.st_mtime_ns}
 if not stat.S_ISREG(s.st_mode):return {'kind':'nonregular-metadata-only','mode':mode,'size':s.st_size}
 b=path.read_bytes()
 return {'kind':'regular','mode':mode,'bytes':len(b),'sha256':sha(b)}
def inventories(label):
 head=git(['rev-parse','HEAD'],label+'-head').decode().strip()
 assert head==EXPECTED_HEAD,('HEAD drift',head)
 raw=git(['ls-files','--stage','-z'],label+'-tracked')
 tracked={}
 nested={}
 for entry in raw.split(b'\0'):
  if not entry:continue
  meta,path=entry.split(b'\t',1);mode,blob,stage=meta.decode().split()
  rel=path.decode()
  if mode=='160000':nested[rel]={'mode':mode,'blob':blob,'stage':stage};continue
  tracked[rel]={'mode':mode,'blob':blob,'stage':stage}
 raw_un=git(['ls-files','--others','--exclude-standard','-z'],label+'-untracked')
 untracked=sorted(set(x.decode().rstrip('/')for x in raw_un.split(b'\0')if x and not excluded_reason(x.decode().rstrip('/'),0)=='own-operational-output'))
 old=json.loads((W/'intake-baseline.private.json').read_text())
 controls=set(relpath(x)for x in old['control_paths'])
 controls.update(str(x.relative_to(ROOT))for x in (ROOT/'research-wiki/frontier-cells').iterdir()if x.is_file())
 controls.update(str(x.relative_to(ROOT))for x in (ROOT/'.astis/locks').iterdir()if x.is_file())
 paths=(set(tracked)|set(untracked)|controls)-{LEDGER,FRONT}
 paths={x for x in paths if excluded_reason(x,0)!='own-operational-output'}
 with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:
  records=dict(zip(sorted(paths),pool.map(one_record,sorted(paths))))
 return {'head':head,'tracked_index_entries':tracked,'ordinary_untracked_paths':untracked,'control_paths':sorted(controls),'nested_repository_gitlink_metadata':nested,'records':records,'frontier_paths':sorted(str(x.relative_to(ROOT))for x in (ROOT/'research-wiki/frontier-cells').iterdir()if x.is_file())}
def replay(raw):
 from tools.astis_advance import _replay_advances
 assert not raw or raw.endswith(b'\n'),'incomplete ledger EOF would be recovered by API'
 rows=[json.loads(x)for x in raw.splitlines()if x.strip()]
 assert all(isinstance(x,dict)for x in rows)
 return rows,_replay_advances(rows)
def capture():
 PRIVATE.mkdir(mode=0o700,exist_ok=False)
 raw=(ROOT/LEDGER).read_bytes();rows,state=replay(raw)
 assert state[ADV]['state']=='PROVED_LOCAL'and state[ADV]['owner_id']==OWNER
 assert not any(r.get('advance_id')==ADV and r.get('to_state')=='VERIFIED'for r in rows)
 (PRIVATE/'old-ledger.raw').write_bytes(raw);os.chmod(PRIVATE/'old-ledger.raw',0o600)
 (PRIVATE/'old-own-frontier.raw').write_bytes((ROOT/FRONT).read_bytes());os.chmod(PRIVATE/'old-own-frontier.raw',0o600)
 d=inventories('before')
 d.update({'ledger_bytes':len(raw),'ledger_sha256':sha(raw),'all_foreign_states':{k:v for k,v in state.items()if k!=ADV},'own_state':state[ADV],'all_existing_VERIFIED_objects':[r for r in rows if r.get('to_state')=='VERIFIED'],'complete_existing_records':rows,'own_frontier_value':json.loads((ROOT/FRONT).read_text()),'scope':'Fresh complete private baseline: all tracked index entries/regular bytes; ordinary nonignored untracked; old+current frontiers and control paths; complete raw ledger prefix/full foreign state/latest_evidence/all existing VERIFIED objects. Explicit ATLAS/C8/private/nested exclusions are metadata-only; no private baseline is exported.'})
 dump(PRIVATE/'full-baseline.private.json',d)
 return summary(d)
def summary(d):
 kinds={}
 for r in d['records'].values():kinds[r['kind']]=kinds.get(r['kind'],0)+1
 return {'tracked_index_entries':len(d['tracked_index_entries']),'ordinary_untracked_paths':len(d['ordinary_untracked_paths']),'control_paths':len(d['control_paths']),'frontier_paths':len(d['frontier_paths']),'record_kinds':kinds,'foreign_states_full_values':len(d['all_foreign_states']),'all_existing_VERIFIED_objects':len(d['all_existing_VERIFIED_objects']),'old_ledger_bytes':d['ledger_bytes'],'old_ledger_sha256':d['ledger_sha256'],'private_baseline_sha256':sha((PRIVATE/'full-baseline.private.json').read_bytes()),'full_private_values_exported':False}
def check(stage,after=False):
 d=json.loads((PRIVATE/'full-baseline.private.json').read_text())
 now=inventories(stage)
 for key in ['head','tracked_index_entries','ordinary_untracked_paths','control_paths','nested_repository_gitlink_metadata','records','frontier_paths']:
  assert now[key]==d[key],('preservation changed',key)
 raw=(ROOT/LEDGER).read_bytes();old=(PRIVATE/'old-ledger.raw').read_bytes()
 assert raw.startswith(old),'old ledger raw prefix changed'
 rows,state=replay(raw)
 assert {k:v for k,v in state.items()if k!=ADV}==d['all_foreign_states'],'foreign state/latest_evidence drift'
 assert state[ADV]['owner_id']==OWNER
 prior_vs=[r for r in rows[:len(d['complete_existing_records'])]if r.get('to_state')=='VERIFIED']
 assert prior_vs==d['all_existing_VERIFIED_objects'],'existing VERIFIED object changed'
 if after:
  tail=raw[len(old):];events=[json.loads(x)for x in tail.splitlines()if x.strip()]
  assert len(events)==1
  e=events[0];assert e['advance_id']==ADV and e['from_state']=='PROVED_LOCAL'and e['to_state']=='VERIFIED'and e['worker_id']==ACTOR
  assert e['evidence']['verifier_id']==ACTOR
  assert state[ADV]['state']=='VERIFIED'
  return summary(d)|{'old_ledger_prefix_exact':True,'all_foreign_states_latest_evidence_and_existing_V_complete_values_exact':True,'single_new_VERIFIED':True,'new_event':e,'append_raw':tail}
 assert raw==old,'ledger changed before one normal attempt'
 assert state[ADV]==d['own_state']
 assert (ROOT/FRONT).read_bytes()==(PRIVATE/'old-own-frontier.raw').read_bytes()
 return summary(d)|{'preflight_preservation_exact':True}

