"""Mechanical binary three-way merge: keep canonical main's exact prefix.

No event is invented or edited. Append this proof branch's six original bytes
only after verifying disjoint advance identities against the new main suffix.
Binary merge is necessary here: text patch/newline normalization would risk
rewriting another actor's hash-pinned history.
"""
import hashlib
import json
from pathlib import Path
import subprocess

BASE='692973fcc6956caebbffe817f2250c44b8ba4dd0'
OWN='96004dd4c45f554c3247cd4ed0ee98514d251efb'
MAIN='994992ba220c1e7080eb184b1de662e857b9ff1c'
NAME='runs/substantive_advances.jsonl'
def git(*args):return subprocess.check_output(['git',*args])
def sha(raw):return hashlib.sha256(raw).hexdigest()
assert git('rev-parse','HEAD').decode().strip()==OWN
assert git('rev-parse','MERGE_HEAD').decode().strip()==MAIN
base=git('show',':1:'+NAME);own=git('show',':2:'+NAME);main=git('show',':3:'+NAME)
assert base==git('show',BASE+':'+NAME)
assert own==git('show',OWN+':'+NAME) and main==git('show',MAIN+':'+NAME)
assert own.startswith(base) and main.startswith(base)
suffix=own[len(base):]
assert suffix.endswith(b'\n') and b'\r\n' not in suffix
events=[json.loads(line) for line in suffix.splitlines()]
foreign=[json.loads(line) for line in main[len(base):].splitlines()]
assert len(events)==6
assert {e['advance_id'] for e in events}=={'ASTIS-SA-20261105-CompactGradientSqrtTest'}
assert not any(e['advance_id']==events[0]['advance_id'] for e in foreign)
assert len(main)==5120408 and sha(main)=='0aa3952eceda632c41a0d80c3655ac18b2bdbbadf04d3a79ea32d53baa490d62'
merged=main+suffix
assert sha(merged)=='1847e0164eaf3a6498ac9de42d75f3c44f386c8c9a5b0d2019297e95986352f2'
path=Path(NAME)
assert b'<<<<<<< HEAD' in path.read_bytes()  # only the actual conflicted file
path.write_bytes(merged)  # bulk mechanical merge, not a text/event rewrite
assert path.read_bytes()==merged and path.read_bytes().startswith(main)
record={'scope':'Mechanical integration, not a new mathematical or reviewer event',
    'base':BASE,'proof_branch':OWN,'canonical_main':MAIN,
    'canonical_main_bytes':len(main),'canonical_main_sha256':sha(main),
    'existing_main_suffix_events_preserved':len(foreign),
    'own_unchanged_appended_events':len(events),'own_suffix_bytes':len(suffix),
    'own_suffix_sha256':sha(suffix),'merged_bytes':len(merged),'merged_sha256':sha(merged),
    'registry_base':607,'registry_candidate':608,
    'boundary':'Original exact-head96004dd4 checks passed, but are not current-base CI. Both theorem/Registry/test contributions retained. No exercise/QA/paper completion.'}
Path('runs/20261105-compact-gradient-sqrt-test/current-main-merge.json').write_text(
    json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record))
