"""Private full guards; return bounded counts only, never export snapshots/index."""
from pathlib import Path
import hashlib,json,os,stat,subprocess,sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
ROOT=Path.cwd()
W=Path('.astis/huanjian-gc-source-matrix-structure-20261113')
ADV='ASTIS-SA-20261113-GaussianComplexitySourceMatrixStructure'
LEDGER='runs/substantive_advances.jsonl'
sha=lambda b:hashlib.sha256(b).hexdigest()
def fingerprint(p):
    st=p.lstat()
    if stat.S_ISLNK(st.st_mode):return {'mode':stat.S_IMODE(st.st_mode),'kind':'symlink','target':os.readlink(p)}
    assert stat.S_ISREG(st.st_mode)
    return {'mode':stat.S_IMODE(st.st_mode),'kind':'regular','bytes':st.st_size,'sha256':sha(p.read_bytes())}
def index(raw):
    return {row.split('\t',1)[1]:row.split('\t',1)[0] for row in raw.split('\0') if row}
def check(expected_state):
    b=json.loads((W/'preproof-baseline.private.json').read_bytes())
    raw=Path(LEDGER).read_bytes()
    states=advance._replay_advances([json.loads(x) for x in raw.splitlines()])
    own=states.pop(ADV);assert own['state']==expected_state
    assert states==b['all_foreign_states'],'foreign state mismatch'
    for p,h in b['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes())==h,'foreign frontier mismatch'
    discovery=Path('runs/substantive_discoveries.jsonl').read_bytes()
    assert sha(discovery)==json.loads((W/'preproof-discoveries.private.json').read_bytes())['ledger_sha256']
    oldidx=index(b['tracked_git_index']);newidx=index(subprocess.check_output(['git','ls-files','--stage','-z']).decode())
    for p,x in oldidx.items():
        if p!=LEDGER:assert newidx.get(p)==x,'existing index mismatch'
    fps={**b['all_existing_tracked_fingerprints'],**b['actual_control_fingerprints']}
    for p,fp in fps.items():
        if p!=LEDGER:assert fingerprint(Path(p))==fp,'existing artifact mismatch'
    return {'foreign_full_states':len(states),'foreign_regular_frontier_files':len(b['all_existing_frontier_hashes']),'foreign_discovery_full_states':43,'all_existing_tracked_fingerprints':len(b['all_existing_tracked_fingerprints']),'historical_and_control_artifact_fingerprints':len(b['actual_control_fingerprints']),'control_count_qualification':'All captured files under historical runs and named control roots; not a literal queue count.','private_guards_exported':False,'existing_index_preserved_except_exact_own_ledger_append':True,'new_owned_files_not_miscounted_as_old_foreign_paths':True}
