"""Check every scoped science Git blob against the declared RAW staging recipe."""
from pathlib import Path
import subprocess,json,hashlib,sys
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;C=sys.argv[1]
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
assert git('rev-parse','HEAD').decode().strip()==C
stage=json.loads((B/'science-staging96.json').read_bytes());archives={x['raw_path']:x for x in stage['raw_archives']}
paths=stage['files']+[(B/'science-staging96.json').relative_to(R).as_posix(),(B/'reuse-parent-metadata-repair96.json').relative_to(R).as_posix()];rows=[]
tree={line.split('\t',1)[1]:line.split()[2] for line in git('ls-tree','-r',C).decode().splitlines()}
for name in paths:
 raw=(R/name).read_bytes();expected=raw
 if name in archives:
  expected=raw.replace(b'\r\n',b'\n')
  if name.startswith('runs/') and expected:expected=b'\n'.join(x.rstrip(b' \t') for x in expected.split(b'\n')).rstrip(b'\n')+b'\n'
 bb=git('cat-file','blob',tree[name]);assert bb==expected,name
 rows.append(dict(path=name,raw_sha256=sha(raw),git_blob_sha256=sha(bb),recipe='exact RAW' if bb==raw else 'declared text normalization; original RAW separately archived'))
changed=set(git('diff-tree','--no-commit-id','--name-only','-r',C).decode().splitlines());assert changed<=set(paths),changed-set(paths)
out=dict(status='PASS',verified_commit=C,scoped_files=len(paths),changed_files=len(changed),all_git_blobs_bound=True,records=rows)
p=O/'science-scope96.json';assert not p.exists();p.write_bytes((json.dumps(out,indent=2)+'\n').encode());print('PASS',len(paths),'scoped Git blobs')
