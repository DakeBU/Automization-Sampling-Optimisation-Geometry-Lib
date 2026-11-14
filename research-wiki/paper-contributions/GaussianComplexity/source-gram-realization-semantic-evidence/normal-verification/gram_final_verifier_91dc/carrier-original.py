"""Carry an independent actor's exact completed V; never replay the API."""
from pathlib import Path
import hashlib,json,subprocess,tarfile
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
R=Path('.astis/semantic-neutral-20261113/gram_final_verifier_91dc')
N=Path('.astis/semantic-neutral-20261113/gram_native_6a27')
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-gram-realization-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-gram-realization.json')
L=Path('runs/substantive_advances.jsonl')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
cfg=json.loads((W/'VERIFIED-carrier-inputs.json').read_bytes())
held='f7a38f36c080883d6c936ae90157a40548797e1b'
assert git('rev-parse','HEAD').decode().strip()==held
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
assert sha(C.read_bytes())==cfg['cell_after_sha256']
ap=(R/'actual-VERIFIED-append.exact.jsonl').read_bytes()
payload=(R/'VERIFIED-evidence.full.json').read_bytes()
assert sha(ap)==cfg['append_sha256'] and sha(payload)==cfg['payload_sha256']
assert L.read_bytes()==git('show',f'{held}:{L}')+ap
event=json.loads(ap);v=json.loads(payload)
assert event['advance_id']=='ASTIS-SA-20261113-GaussianComplexitySourceGramRealization'
assert event['to_state']=='VERIFIED' and event['evidence']==v
assert v['verifier_id']=='gram_final_verifier_91dc'
pl=json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes())
assert len(pl)==26
cell=json.loads(C.read_bytes())
assert isinstance(cell['evidence']['independent_verification'],str)
assert cell['owner_id']=='huanjian_gc_20261113_source_gram_realization'
for k,x in pl.items():
 assert v[k]==x and cell['evidence']['independent_verification_details'][k]==x
allow=R/'ROOT-CARRIER-ALLOWLIST.json'
assert sha(allow.read_bytes())==cfg['portable_allowlist_sha256']
d=E/'normal-verification/gram_final_verifier_91dc'
for x in json.loads(allow.read_bytes())['files']:
 rel=Path(x['relative_destination']);assert not rel.is_absolute() and '..' not in rel.parts
 assert not any('.private.' in part for part in rel.parts)
 p=R/rel;assert p==Path(x['source']);b=p.read_bytes()
 assert len(b)==x['bytes'] and sha(b)==x['sha256']
 create(d/rel,b)
create(d/allow.name,allow.read_bytes())
archive=d/cfg['verifier_archive_name']
assert sha(archive.read_bytes())==cfg['verifier_archive_sha256']
with tarfile.open(archive,'r:gz') as tf:
 members=tf.getmembers();assert len(members)==cfg['verifier_archive_regular_members']
 assert all(x.isfile() and not Path(x.name).is_absolute() and '..' not in Path(x.name).parts for x in members)
for x in cfg['native_bounded_summaries']:
 rel=Path(x['path']);assert not rel.is_absolute() and '..' not in rel.parts
 b=(N/rel).read_bytes();assert sha(b)==x['sha256']
 create(E/'final-native-reader-summary'/rel,b)
memory=json.loads((W/'completed-local-cycle-memory.draft.json').read_bytes())
owner_record=W/'original-owner-current-after-final-reader.json'
assert sha(owner_record.read_bytes())==cfg['latest_owner_record_sha256']
create(d/'original-owner-current-after-final-reader.original.json',owner_record.read_bytes())
memory['latest_owner_observation']={'file':str(d/'original-owner-current-after-final-reader.original.json'),
 'sha256':sha(owner_record.read_bytes()),'original_owner_released':False}
memory['independent_normal_V']='VERIFIED_LOCAL_ONLY; exactly one independent normal transition'
memory['actual_V_append_sha256']=sha(ap)
memory['actual_V_payload_sha256']=sha(payload)
memory['final_reader_acceptance']=cfg['final_reader_boundary']
memory['complete_independent_verifier_archive']={'file':str(archive),
 'sha256':sha(archive.read_bytes()),'regular_members':len(members),
 'exact_peer_native_archive_included_once':cfg['exact_native_archive_sha256']}
create(E/'local-cycle-memory.json',dump(memory))
readme='''# Actual source Gram realization: local cycle

On the original inclusive all-row truncation event, the public theorem proves
the two actual identities sum Z = B^T B - a I and sum w Z = B^T diag(w) B.
The private deterministic consumer proves the two Gram norm bounds from the
same-outcome centered-sum bounds, for every real threshold. It derives the
needed a <= 1 internally. It is not a probability theorem or public API node.
The sole source regime and q=0 are retained; no proof ingredient was added as
a source hypothesis. The exact mean, cosine-frame and Gaussian-moment nodes
are reused, with no duplicate aggregate-mean public node.

Actual math candidate: 60ec0e08. Reviewed reader: d35db1ad.
Exactly one normal PROVED_LOCAL and one independent normal VERIFIED transition
occurred. All 26 original PL fields remain inline unchanged in V and cell
details, including historical pending-reader strings. Actual final reader
closure is separately evidenced below. ROOT made no VERIFIED call.

The independent verifier checked the immutable f7a38f36 metadata and original
source/native/reader evidence, preserving all protected foreign states,
frontiers, artifacts, discoveries and held index entries. Complete selected
native evidence is included once inside the verifier archive. Full private
preservation/index/control/state maps remain local and are excluded.

'''+cfg['final_reader_boundary']+'\n\n'+'''All candidate CSS remains globally unapplied. The original stabilization owner
is not released. Formal integration, production publication and purification
remain held. Matrix Bernstein, the two main lower bounds, true oracle/TV/
precision/query-cap/cost adaptation and the whole Goal remain unfinished.
The next Bernstein source assessment is preparation only and is separately
qualified against already compiled private variance/radius consumers.
'''
create(E/'README.md',readme.encode())
create(d/'carrier-original.py',Path(__file__).read_bytes())
create(d/'carrier-inputs.original.json',(W/'VERIFIED-carrier-inputs.json').read_bytes())
paths=[C,L,E/'local-cycle-memory.json',E/'README.md',
 *[p for p in sorted(d.rglob('*')) if p.is_file()],
 *[p for p in sorted((E/'final-native-reader-summary').rglob('*')) if p.is_file()]]
spec=W/'verified-carrier.private.nul'
create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(L),str(E/'README.md')],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry independent Gaussian Gram verification and complete selected evidence'],check=True)
head=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{head}:{p}')==p.read_bytes()
out={'verification_carrier_commit':head,'checked_metadata_commit':held,
 'actual_V_append_sha256':sha(ap),'all_original_PL_fields_inline_unchanged':len(pl),
 'ROOT_V_calls':0,'normal_API_replay':False,'exact_owned_files':len(paths),
 'private_guards_exported':False,'integration_publication_purification_wholeGoal':'HOLD'}
create(W/'actual-VERIFIED-carrier-commit.json',dump(out))
print(json.dumps(out))
