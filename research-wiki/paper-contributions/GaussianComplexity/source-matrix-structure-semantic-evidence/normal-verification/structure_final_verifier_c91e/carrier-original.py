"""Carry original independent normal V and lossless selected evidence; no API replay."""
from pathlib import Path
import hashlib,json,subprocess,tarfile
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
R=Path('.astis/semantic-neutral-20261113/structure_final_verifier_c91e')
N=Path('.astis/semantic-neutral-20261113/structure_final_native_f30b')
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-structure.json')
L=Path('runs/substantive_advances.jsonl')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
held='cf75c5f89a8f93b79c255fb43a942f6d1b7d49e4'
assert git('rev-parse','HEAD').decode().strip()==held
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
assert sha(C.read_bytes())=='ed1a6193a08ae64e50f5ae3e3e91dfe8a918868210df4bbd7f61b149eab00cab'
ap=(R/'actual-VERIFIED-append.exact.jsonl').read_bytes()
assert sha(ap)=='9469feb2ad5a0593b061859a64920419ad53ddd21d8a40061ed0cc4e53261580'
assert L.read_bytes()==git('show',f'{held}:{L}')+ap
payload=(R/'VERIFIED-evidence.full.json').read_bytes()
assert sha(payload)=='4d7ad12f3eb3bc1e3d335ac1e4054872f9dbde45147604fa77f97aae0ec3ffa2'
event=json.loads(ap);v=json.loads(payload);assert event['to_state']=='VERIFIED' and event['evidence']==v
pl=json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes());assert len(pl)==26
cell=json.loads(C.read_bytes())
for k,x in pl.items():assert v[k]==x and cell['evidence']['independent_verification_details'][k]==x
allow=R/'PORTABLE-EXPORT-ALLOWLIST.json';assert sha(allow.read_bytes())=='1841361cf650417c38c4d8faf666df4ec0e8f1ffba451e494f425ffbdcaeb407'
d=E/'normal-verification/structure_final_verifier_c91e'
for x in json.loads(allow.read_bytes())['files']:
 p=R/x['path'];b=p.read_bytes();assert len(b)==x['bytes'] and sha(b)==x['sha256']
 assert not Path(x['path']).is_absolute() and '..' not in Path(x['path']).parts
 create(d/x['path'],b)
create(d/allow.name,allow.read_bytes())
archive=d/'complete-verifier-evidence.tar.gz'
with tarfile.open(archive,'r:gz') as tf:
 assert len(tf.getmembers())==43 and all(x.isfile() for x in tf.getmembers())
 assert all(not Path(x.name).is_absolute() and '..' not in Path(x.name).parts for x in tf.getmembers())
bounded={'reader-assessment.json':'6e116efc9f407c4ddb2239c968672c3319ffc4c18f978c92ca784aa546d8da74','gate-summary.json':'eb631585985bb8e72c4737cd4df8d4da6c31d5003920f57da048910fe902356e','JUDGMENT.md':'c473a52d60cf688447bd297c202f847d442396dbe57247c63689c9ef02e85082','archive-closure.json':'ba168ab2de1ae28ea3e4fd1104313ea1e34663d5a619d0a0d4159ad1d43ef0dc'}
for n,h in bounded.items():
 b=(N/n).read_bytes();assert sha(b)==h;create(E/'final-native-reader-summary'/n,b)
memory=json.loads((W/'completed-local-cycle-memory.draft.json').read_bytes())
memory['complete_independent_verifier_archive']={'file':str(archive),'sha256':sha(archive.read_bytes()),'regular_members':43,'indexed_payload_members':41,'extra_members':'manifest and seal','exact_peer_native_archive_included_once':'b37c5a0a7d0ddb64332709849743762e5cb48e9adbb01a6fdde61a97c9fdb8ad'}
create(E/'local-cycle-memory.json',dump(memory))
create(E/'README.md',b'''# Actual centered Gaussian matrix structure: local cycle

The public theorem proves measurability, joint independence, Bochner integrability,
actual integral zero and pointwise real self-adjointness of the original centered
matrix family. Its complete private cosine-weighted consumer uses all five outputs.
The sole source regime and q=0 are retained. Each family is independent separately.

The actual math candidate is 9ed997b7; the reviewed reader is 7c364dbe.
One normal PROVED_LOCAL and one independent normal VERIFIED transition occurred.
All 26 original PL fields remain inline unchanged in V and cell details.
The independent verifier checked the immutable cf75c5f8 metadata, preserving every
protected foreign state, frontier, artifact, discovery and held index entry.

Original mobile CSS fails one clipped assumption table. The exact separate CSS
candidate passes real runtime, positive scrolling and independent visual review;
it remains globally unapplied. Mobile source-L13 fixed-header overlap is explicit
reader debt. The original stabilization owner is not released. Full integration,
publication, purification, matrix Bernstein, both main lower bounds and the Goal
remain unfinished. The next Ex125/126 packet is source/type/topology preparation.

Use the explicit verifier export allowlist. Complete native math/reader evidence
is included once inside the verifier archive. Full preservation/index/control/
foreign snapshots remain private and are excluded from repository artifacts.
''')
create(d/'carrier-original.py',Path(__file__).read_bytes())
paths=[C,L,E/'local-cycle-memory.json',E/'README.md',*[p for p in sorted(d.rglob('*')) if p.is_file()],*[p for p in sorted((E/'final-native-reader-summary').rglob('*')) if p.is_file()]]
spec=W/'verified-carrier.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(L),str(E/'README.md')],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry one independent Gaussian structure verification and complete evidence'],check=True)
head=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{head}:{p}')==p.read_bytes()
out={'verification_carrier_commit':head,'checked_metadata_commit':held,'actual_V_append_sha256':sha(ap),'all_original_PL_fields_inline_unchanged':26,'ROOT_V_calls':0,'normal_API_replay':False,'exact_owned_files':len(paths),'private_guards_exported':False,'integration_publication_purification_wholeGoal':'HOLD'}
create(W/'actual-VERIFIED-carrier-commit.json',dump(out));print(json.dumps(out))
