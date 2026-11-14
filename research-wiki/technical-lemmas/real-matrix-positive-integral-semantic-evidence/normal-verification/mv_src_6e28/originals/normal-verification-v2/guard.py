from pathlib import Path
import os, stat, json, hashlib, zlib, subprocess, sys
from datetime import datetime, timezone

sys.dont_write_bytecode = True
ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
BASE = ROOT / '.astis/semantic-neutral-20261112/mv_src_6e28/normal-verification-v2'
PRIVATE = BASE / 'private'
ADV = 'ASTIS-SA-20261112-RealMatrixPositiveIntegral'
CELL = 'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json'
LEDGER = 'runs/substantive_advances.jsonl'
DISC = 'runs/substantive_discoveries.jsonl'
HELD = '5f69ac83737e497210d8d8ad9628c45d83089458'
INTAKE = ROOT / '.astis/huanjian-real-matrix-positive-integral-20261112/intake-controls.private.json'

def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT)

def blob(b):
    h = sha(b); p = PRIVATE / 'blobs' / (h + '.zlib')
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as f: f.write(zlib.compress(b, 6))
    return h

def file_record(rel):
    p = ROOT / rel; s = p.lstat()
    if stat.S_ISLNK(s.st_mode):
        b = os.readlink(p).encode(); kind = 'symlink'
    elif stat.S_ISREG(s.st_mode):
        b = p.read_bytes(); kind = 'regular'
    else: raise RuntimeError('Unsupported guarded filesystem kind')
    return {'mode': stat.S_IMODE(s.st_mode), 'kind': kind, 'bytes': len(b), 'sha256': blob(b)}

def regular(p):
    try: return stat.S_ISREG(p.lstat().st_mode)
    except FileNotFoundError: return False

def control_paths():
    intake = json.loads(INTAKE.read_bytes())
    paths = {str(p) for p in intake if regular(ROOT / p)}
    paths.update(str(p.relative_to(ROOT)) for p in (ROOT/'runs').rglob('*') if regular(p))
    paths.add('website/content/samplewiki_companion_frontiers.json')
    # Existing process-state files only; exclude verifier-private namespaces and package/source caches.
    excluded = [BASE.parent, ROOT/'.astis/semantic-neutral-20261113/psd_native_7b31']
    tokens = ('queue','control','goal','steer','execution')
    state_dirs = {'control','controls','queues','queue','runtime','harness','state','locks'}
    for current, dirs, files in os.walk(ROOT/'.astis', followlinks=False):
        d = Path(current)
        dirs[:] = [x for x in dirs if x not in {'.git','.lake','node_modules','__pycache__','site-packages'}
                   and not any((d/x).is_relative_to(e) for e in excluded)]
        if any(d.is_relative_to(e) for e in excluded): continue
        state_parent = any(part.lower() in state_dirs for part in d.relative_to(ROOT/'.astis').parts)
        for name in files:
            p = d/name
            if regular(p) and (state_parent or any(t in name.lower() for t in tokens)):
                paths.add(str(p.relative_to(ROOT)))
    return sorted(p for p in paths if regular(ROOT/p))

def snapshot(label):
    assert git('rev-parse','HEAD').decode().strip() == HELD
    sys.path.insert(0, str(ROOT/'tools'))
    import astis_advance as advance
    raw = (ROOT/LEDGER).read_bytes(); rows = [json.loads(l) for l in raw.splitlines() if l.strip()]
    dsraw = (ROOT/DISC).read_bytes(); dsrows = [json.loads(l) for l in dsraw.splitlines() if l.strip()]
    states = advance._replay_advances(rows)
    discoveries = advance._replay_discoveries(dsrows)
    foreign = {k:v for k,v in states.items() if k != ADV}
    assert len(foreign) == 309 and len(discoveries) == 43
    vcount = sum(r.get('advance_id')==ADV and r.get('event')=='transition' and r.get('to_state')=='VERIFIED' for r in rows)
    index_path = Path(git('rev-parse','--git-path','index').decode().strip())
    if not index_path.is_absolute(): index_path = ROOT/index_path
    index_raw = index_path.read_bytes()
    tracked = {}
    entries = git('ls-files','--stage','-z')
    for entry in entries.split(b'\0'):
        if not entry: continue
        fields, path = entry.split(b'\t',1); mode, oid, stage = fields.decode().split()
        rel = os.fsdecode(path); tracked[rel] = {'index_mode':mode,'index_oid':oid,'stage':stage,**file_record(rel)}
    foreign_cells = {str(p.relative_to(ROOT)): file_record(str(p.relative_to(ROOT)))
                     for p in (ROOT/'research-wiki/frontier-cells').rglob('*')
                     if regular(p) and str(p.relative_to(ROOT)) != CELL}
    assert len(foreign_cells) == 469
    controls = {p:file_record(p) for p in control_paths()}
    full = {'captured_utc':datetime.now(timezone.utc).isoformat(),'HEAD':HELD,
            'all_full_foreign_advance_states':foreign,'all_full_discoveries':discoveries,
            'own_advance':states[ADV],'own_V_history_count':vcount,
            'advance_raw':{'bytes':len(raw),'sha256':blob(raw)},
            'discovery_raw':{'bytes':len(dsraw),'sha256':blob(dsraw)},
            'tracked':tracked,'index':{'bytes':len(index_raw),'sha256':blob(index_raw)},
            'index_stage_raw':{'bytes':len(entries),'sha256':blob(entries)},
            'foreign_cells':foreign_cells,'controls':controls,'own_cell':file_record(CELL)}
    p = PRIVATE/(label+'.snapshot.private.json')
    with p.open('x') as f: f.write(json.dumps(full,indent=2,ensure_ascii=False)+'\n')
    summary = {'label':label,'HEAD':HELD,'foreign_full_advances':len(foreign),'full_discoveries':len(discoveries),
               'foreign_regular_frontier_files_including_README':len(foreign_cells),'tracked_files':len(tracked),
               'shared_control_files':len(controls),'own_V_history_count':vcount,
               'private_snapshot_sha256':sha(p.read_bytes()),'private_data_exported':False,
               'advance_raw_sha256':sha(raw),'discovery_raw_sha256':sha(dsraw),'index_raw_sha256':sha(index_raw),
               'qualified_control_scope':'Explicit original intake paths plus runs regular files and existing process-state .astis names/directories; excludes verifier-private namespaces and package/source cache directories.'}
    (BASE/(label+'.guard-summary.json')).write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    os.chdir(ROOT)
    snapshot(sys.argv[1])
