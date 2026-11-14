#!/opt/anaconda3/bin/python
"""Process-only whole-control preservation. Full foreign data never goes portable."""
import hashlib,json,os,pathlib,stat,subprocess,sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
BASE=pathlib.Path(__file__).resolve().parent
PRIVATE=BASE.parent/'private-phase5-preservation'
ADV='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumCosineGram'
FRONTIER='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json'
LEDGER='runs/substantive_advances.jsonl'
def sha(data):return hashlib.sha256(data).hexdigest()
def restricted(path):
    # Nested restricted repositories and explicitly Atlas-named material/index/
    # projections are metadata-only. Never open or recurse their content.
    return any('atlas' in part.casefold() for part in pathlib.PurePosixPath(path).parts)
def describe(relative):
    path=ROOT/relative
    try: st=path.lstat()
    except FileNotFoundError:return {'kind':'missing'}
    basic={'mode':stat.S_IMODE(st.st_mode),'size':st.st_size}
    if restricted(relative):
        return {'kind':'restricted-metadata-only',**basic,'mtime_ns':st.st_mtime_ns,'inode':st.st_ino,'dev':st.st_dev}
    if stat.S_ISREG(st.st_mode):return {'kind':'regular','sha256':sha(path.read_bytes()),**basic}
    if stat.S_ISLNK(st.st_mode):return {'kind':'symlink','link':os.readlink(path),**basic}
    if stat.S_ISDIR(st.st_mode):
        # Includes all nested repositories reported by git. No child/stat/git
        # metadata traversal is performed, even to detect a nested .git.
        return {'kind':'directory-metadata-only',**basic,'mtime_ns':st.st_mtime_ns,'inode':st.st_ino,'dev':st.st_dev}
    return {'kind':'other-metadata-only',**basic,'mtime_ns':st.st_mtime_ns}
def git_private(label,argv):
    proc=subprocess.run(argv,cwd=ROOT,capture_output=True)
    (PRIVATE/(label+'.stdout')).write_bytes(proc.stdout)
    (PRIVATE/(label+'.stderr')).write_bytes(proc.stderr)
    r={'argv':argv,'returncode':proc.returncode,'stdout_bytes':len(proc.stdout),'stderr_bytes':len(proc.stderr),
       'stdout_sha256':sha(proc.stdout),'stderr_sha256':sha(proc.stderr),'capture_scope':'private outside portable output'}
    with (PRIVATE/'actual-private-commands.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
    assert proc.returncode==0,argv
    return proc.stdout
def states(raw):
    sys.path.insert(0,str(ROOT));from tools import astis_advance
    return astis_advance._replay_advances([json.loads(line) for line in raw.splitlines() if line.strip()])
def capture_before():
    PRIVATE.mkdir(exist_ok=True,mode=0o700)
    old=json.loads((PRIVATE/'intake-baseline.private.json').read_text())
    inherited=json.loads((PRIVATE/'intake-tracked-private-preservation.json').read_text())
    tracked=[p.decode() for p in git_private('git-tracked-before',['git','ls-files','-z']).split(b'\0') if p]
    ordinary=[p.decode() for p in git_private('git-ordinary-untracked-before',['git','ls-files','--others','--exclude-standard','-z']).split(b'\0') if p]
    # Snapshot exact old controls plus current frontier files and all ordinary
    # untracked regular files; ignored .astis is never globbed or inventoried.
    control=set(old['control_paths'])|set(old['foreign_control_hashes'])
    control.update(str(p.relative_to(ROOT)) for p in (ROOT/'research-wiki/frontier-cells').glob('*.json'))
    excluded={LEDGER,FRONTIER}
    snapshot={'tracked':{p:describe(p) for p in tracked if p not in excluded},
              'ordinary_untracked':{p:describe(p) for p in ordinary if p not in excluded},
              'controls':{p:describe(p) for p in sorted(control) if p not in excluded}}
    raw=(ROOT/LEDGER).read_bytes()
    assert raw==(PRIVATE/'ledger-before.raw.jsonl').read_bytes(),'Ledger changed during read-only preflight; no API permitted.'
    current=states(raw);foreign={k:v for k,v in current.items() if k!=ADV}
    assert foreign==inherited['all_foreign_states'],'Inherited whole foreign states changed before V.'
    snapshot['foreign_states']=foreign
    snapshot['all_prior_VERIFIED_records']=[r for r in map(json.loads,raw.splitlines()) if r.get('event')=='transition' and r.get('to_state')=='VERIFIED']
    snapshot['ledger_sha256']=sha(raw);snapshot['ledger_bytes']=len(raw)
    # Original foreign control files are checked against the supplied old
    # hashes when regular. Restricted/directory exceptions remain metadata-only.
    inherited_control_matches=0
    for p,expected in old['foreign_control_hashes'].items():
        observed=describe(p)
        if observed['kind']=='regular' and isinstance(expected,str) and len(expected)==64:
            assert observed['sha256']==expected,'A historical foreign control changed (details kept private): '+sha(p.encode())
            inherited_control_matches+=1
    path=PRIVATE/'guard-before.private.json';path.write_text(json.dumps(snapshot,ensure_ascii=False,sort_keys=True)+'\n')
    summary={'tracked_paths_guarded':len(snapshot['tracked']),
             'ordinary_untracked_paths_guarded':len(snapshot['ordinary_untracked']),
             'ordinary_untracked_REGULAR_files_guarded':sum(v['kind']=='regular' for v in snapshot['ordinary_untracked'].values()),
             'control_paths_guarded':len(snapshot['controls']),
             'historical_foreign_control_hash_matches':inherited_control_matches,
             'foreign_current_states_deep_snapshotted':len(foreign),
             'prior_VERIFIED_events_all_repository':len(snapshot['all_prior_VERIFIED_records']),
             'metadata_only_exceptions':{group:sum(v['kind'].endswith('metadata-only') for v in snapshot[group].values()) for group in ['tracked','ordinary_untracked','controls']},
             'full_private_guard_bytes':path.stat().st_size,'full_private_guard_sha256':sha(path.read_bytes()),
             'private_full_snapshots_outside_portable_output':True,'ignored_astis_globbed':False,
             'restricted_nested_contents_indices_projections_read_or_hashed':False}
    (BASE/'preservation-before-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary
def verify_preserved(*,allow_own_append=False):
    before=json.loads((PRIVATE/'guard-before.private.json').read_text())
    differences=[]
    for group in ['tracked','ordinary_untracked','controls']:
        for relative,value in before[group].items():
            if describe(relative)!=value:differences.append((group,relative))
    if differences:
        (PRIVATE/'guard-differences.private.json').write_text(json.dumps(differences,indent=2)+'\n')
        raise AssertionError('Protected paths changed: '+str(len(differences))+'; details are private.')
    oldraw=(PRIVATE/'ledger-before.raw.jsonl').read_bytes();now=(ROOT/LEDGER).read_bytes()
    assert now.startswith(oldraw),'Raw ledger prefix changed.'
    suffix=now[len(oldraw):]
    appended=[json.loads(line) for line in suffix.splitlines() if line.strip()]
    if allow_own_append:
        assert len(appended)==1 and appended[0]['advance_id']==ADV
        assert appended[0]['event']=='transition' and appended[0]['to_state']=='VERIFIED'
    else:assert not suffix,'Ledger changed before once-only API.'
    allstates=states(now);foreign={k:v for k,v in allstates.items() if k!=ADV}
    assert foreign==before['foreign_states'],'Deep foreign current state/latest_evidence changed.'
    prior=[r for r in map(json.loads,now.splitlines()) if r.get('event')=='transition' and r.get('to_state')=='VERIFIED']
    expected=before['all_prior_VERIFIED_records']
    assert prior[:len(expected)]==expected,'Any prior VERIFIED event changed.'
    assert len(prior)==len(expected)+(1 if allow_own_append else 0)
    return {'all_tracked_except_own_ledger_frontier_preserved':len(before['tracked']),
            'all_ordinary_untracked_original_paths_preserved':len(before['ordinary_untracked']),
            'all_foreign_controls_preserved':len(before['controls']),
            'all_foreign_current_states_and_latest_evidence_preserved':len(foreign),
            'all_prior_VERIFIED_events_preserved':len(expected),'whole_ledger_prior_prefix_bytes_preserved':len(oldraw),
            'actual_own_appended_event_count':len(appended),'ledger_after_sha256':sha(now),
            'restricted_metadata_exceptions_preserved':True}
if __name__=='__main__':print(json.dumps(capture_before(),indent=2))
