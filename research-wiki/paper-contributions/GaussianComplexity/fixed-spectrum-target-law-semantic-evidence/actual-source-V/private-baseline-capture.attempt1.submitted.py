from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json,subprocess,sys,base64,os,stat
sys.dont_write_bytecode=True
from tools import astis_advance as adv
root=Path('.astis/semantic-neutral-20261110/tl_src_e028af').resolve();pub=root/'normal-sourceV';priv=root/'PRIVATE-normal-sourceV-baseline';priv.mkdir(exist_ok=False)
aid='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumTargetLaw'
cp='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-target-law.json'
ledger=Path('runs/substantive_advances.jsonl');raw=ledger.read_bytes();assert raw.endswith(b'\n')
records=[json.loads(x) for x in raw.splitlines() if x.strip()]
states=adv._replay_advances(records);own=states[aid];foreign={k:v for k,v in states.items() if k!=aid}
assert len(foreign)==296 and own['state']=='PROVED_LOCAL' and own['owner_id']=='huanjian_gc_20261110_fixed_spectrum_target_law'
priorV=[x for x in records if x.get('event')=='transition' and x.get('to_state')=='VERIFIED']
assert len(priorV)==9
pre=json.loads(Path('.astis/huanjian-gc-fixed-spectrum-target-law-20261110/preproof-baseline.private.json').read_bytes())
oldforeign=pre['all296_foreign_states'];assert foreign==oldforeign
tracked=subprocess.run(['git','ls-files','-z'],capture_output=True,check=True).stdout.split(b'\0')
def file_record(p):
 q=Path(p)
 if q.is_symlink():return {'kind':'symlink','target':os.readlink(q)}
 if q.is_file():
  b=q.read_bytes();return {'kind':'regular','bytes':len(b),'sha256':sha256(b).hexdigest(),'mode':stat.S_IMODE(q.stat().st_mode)}
 return {'kind':'missing'}
protected={p.decode():file_record(p.decode()) for p in tracked if p and p.decode() not in [str(ledger),cp]}
frontiers={str(p):{'sha256':sha256(p.read_bytes()).hexdigest(),'value':json.loads(p.read_bytes())} for p in sorted(Path('research-wiki/frontier-cells').rglob('*.json')) if str(p)!=cp}
untrackedraw=subprocess.run(['git','ls-files','--others','--exclude-standard','-z'],capture_output=True,check=True).stdout
untracked={p.decode():file_record(p.decode()) for p in untrackedraw.split(b'\0') if p}
ownCraw=Path(cp).read_bytes();ownC=json.loads(ownCraw)
base={'PRIVATE_FULL_FOREIGN_RAW_DO_NOT_PUBLISH':True,'created_utc':datetime.now(timezone.utc).isoformat(),'head':subprocess.run(['git','rev-parse','HEAD'],capture_output=True,check=True).stdout.decode().strip(),'ledger_path':str(ledger),'ledger_prefix_bytes':len(raw),'ledger_prefix_sha256':sha256(raw).hexdigest(),'foreign_states':foreign,'prior_VERIFIED_events_all_keys_all_nested_values':priorV,'protected_tracked_files':protected,'foreign_frontiers_all_values':frontiers,'foreign_untracked_queue_raw_base64':base64.b64encode(untrackedraw).decode(),'foreign_untracked_files':untracked,'own_state':own,'own_frontier_path':cp,'own_frontier_value':ownC,'own_frontier_raw_base64':base64.b64encode(ownCraw).decode(),'preproof_foreign_states_equal':True}
(priv/'ledger-prefix.raw.jsonl').write_bytes(raw)
(priv/'baseline.private.json').write_text(json.dumps(base,ensure_ascii=False,indent=2)+'\n')
(priv/'DO-NOT-PUBLISH.txt').write_text('PRIVATE FULL FOREIGN RAW. Never copy this directory or its files into E, public evidence, portable archives, commits, or public reports. It is only a read-only preservation baseline.\n')
for p in priv.iterdir():p.chmod(0o444)
summary={'private_baseline_outside_portable_directory':True,'private_baseline_published':False,'baseline_sha256':sha256((priv/'baseline.private.json').read_bytes()).hexdigest(),'raw_ledger_prefix_bytes':len(raw),'raw_ledger_prefix_sha256':sha256(raw).hexdigest(),'foreign_state_count':len(foreign),'prior_VERIFIED_event_count':len(priorV),'foreign_frontier_count':len(frontiers),'protected_tracked_count':len(protected),'foreign_untracked_count':len(untracked),'preproof_foreign_states_equal':True,'target_state':own['state'],'proof_owner':own['owner_id'],'own_frontier_top_keys':list(ownC),'own_frontier_status':ownC.get('status'),'own_frontier_evidence_keys':list(ownC.get('evidence',{}))}
(pub/'private-baseline-public-safe-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
