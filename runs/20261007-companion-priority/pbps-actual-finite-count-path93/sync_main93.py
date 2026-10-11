"""Merge a disjoint fetched upstream change without touching any dirty input."""
from pathlib import Path
import subprocess,hashlib,json
R=Path.cwd();r=Path(__file__).parent;out=r/'integration93'
def git(*a):return subprocess.check_output(['git',*a])
sha=lambda b:hashlib.sha256(b).hexdigest()
assert json.loads((r/'checks93/integration-site-build-final/receipt.json').read_bytes())['terminal_closed']
assert not git('diff','--cached','--name-only').strip()
head=git('rev-parse','HEAD').decode().strip();up=git('rev-parse','origin/main').decode().strip()
assert head=='8ec33d055fb8a9b3ba376d4113e388b00882026f'
base=git('merge-base','HEAD','origin/main').decode().strip()
changed=set(git('diff','--name-only',base,'origin/main').decode().splitlines())
dirty=set(git('diff','--name-only').decode().splitlines())
untracked=set(git('ls-files','--others','--exclude-standard').decode().splitlines())
assert not changed.intersection(dirty|untracked)
before={p:sha(Path(p).read_bytes()) for p in dirty if Path(p).is_file()}
report=dict(before_head=head,upstream=up,merge_base=base,upstream_changed=sorted(changed),preserved_dirty_inputs=before)
(out/'main-sync-before.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n')
q=subprocess.run(['git','merge','--no-ff','--no-edit','origin/main'],capture_output=True)
(out/'main-sync.stdout.log').write_bytes(q.stdout);(out/'main-sync.stderr.log').write_bytes(q.stderr)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
for p,h in before.items():assert sha(Path(p).read_bytes())==h,p
report.update(merge_commit=git('rev-parse','HEAD').decode().strip(),status='DISJOINT_UPSTREAM_MERGED_ALL_DIRTY_RAW_PRESERVED',source_proof_changed=False,site_recheck_required=True)
(out/'main-sync.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n')
print(report['status'],report['merge_commit'])
