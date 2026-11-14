"""Carry exact independent current source reviews; no ROOT fidelity judgment."""
from pathlib import Path
import hashlib,json,subprocess,sys,tarfile
sys.path.insert(0,'tools')
import astis_semantic_roundtrip as rt
import astis_publication as pub
import astis_frontier_cells as frontiers
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
R=Path('.astis/semantic-neutral-20261113/structure_src_c24d')
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-semantic-evidence')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-structure.json')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-structure.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
assert git('rev-parse','HEAD').decode().strip()=='37c228612fc3773c0dc1021cb6d7128cd0b55cfa'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
critical={'P-audit-overlay.v3.json':'fdce27f4e8cf62c50e8ad04403c32d250731e5e8c00b7758e0d4aa6bed5cb2e4','T-audit-overlay.v3.json':'1de251e339ded3cd805788e0fc135fb06c3db6b5f1c061c6efaebae9e25a3821','EXPOSITION-SOURCE-MAP-CONCEPTUAL-REVIEW.v3.json':'f0d00e0b5b6e565b62d807e8638122257a4b436e228f1b9d5143eb04bc917747','phase3-closed-manifest.json':'1bc46c1c1c37d742e44ebeef833ea138f082a2e62508ab7d711f7029e5e5290e'}
for n,h in critical.items():assert sha((R/n).read_bytes())==h
mf=json.loads((R/'phase3-closed-manifest.json').read_bytes())
for x in mf['files']:
 b=(R/x['path']).read_bytes();assert len(b)==x['size'] and sha(b)==x['sha256']
dest=E/'source-review/structure_src_c24d';dest.mkdir(parents=True,exist_ok=False)
files={}
for p in sorted(R.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts:
  assert not p.is_symlink() and not any('private' in s.lower() and 'private-consumer' not in s.lower() for s in p.parts if s.startswith('.PRIVATE'))
  files[str(p)]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
archive=dest/'complete-source-originals.tar.gz'
with tarfile.open(archive,'x:gz') as tf:
 for p in files:tf.add(p,arcname=p,recursive=False)
with tarfile.open(archive,'r:gz') as tf:
 assert len(tf.getmembers())==len(files)
 for n,x in files.items():
  b=tf.extractfile(n).read();assert len(b)==x['bytes'] and sha(b)==x['sha256']
create(dest/'complete-source-originals.manifest.json',dump({'files':files,'archive_sha256':sha(archive.read_bytes()),'phase3_indexed_files':len(mf['files']),'private_foreign_guards_exported':False}))
for n in critical:create(dest/n,(R/n).read_bytes())
audits=[json.loads(A.read_bytes()),json.loads((W/'private-consumer-audit.reconstructed.v3.json').read_bytes())]
fields=['state','semantic_slots','deltas','verdict','repairs','source_review']
for a,n in zip(audits,['P-audit-overlay.v3.json','T-audit-overlay.v3.json']):
 o=json.loads((R/n).read_bytes());assert o['id']==a['id'] and o['state']==o['source_review']['state']=='accepted'
 assert o['source_review']['reviewer_packet_sha256']==rt.semantic_reviewer_packet(a)['packet_sha256']
 assert o['source_review']['reviewer'] not in [a['lean']['formalizer'],a['reconstruction']['decoder']]
 assert set(o['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
 for k in fields:a[k]=o[k]
 a['actual_math_commit']='9ed997b7fda8631deb5bc1397d021495d53c4d41';a['reader_commit']='37c228612fc3773c0dc1021cb6d7128cd0b55cfa'
 a['independent_original_overlay']={'path':str(dest/n),'sha256':critical[n]}
A.write_bytes(dump(audits[0]));create(E/'private-consumer-source-reviewed.bounded.json',dump(audits[1]))
cell=json.loads(C.read_bytes())
cell['evidence']['independent_source_review']={'public_P_overlay':audits[0]['independent_original_overlay'],'private_T_overlay':audits[1]['independent_original_overlay'],'private_T_decision':{'file':str(E/'private-consumer-source-reviewed.bounded.json'),'sha256':sha((E/'private-consumer-source-reviewed.bounded.json').read_bytes())},'complete_original_archive':{'file':str(archive),'sha256':sha(archive.read_bytes()),'files':len(files)},'public_P_run_sha256':audits[0]['source_review']['review_run_sha256'],'private_T_run_sha256':audits[1]['source_review']['review_run_sha256'],'source_review_scope':'Independent rawfirst, wholecode, fresh7slots, exactcontext37c228, actualsource/code spans, all6folds, conceptualnonefound. Native/runtime/globalintegration separate.'}
cell['conceptual_mirror_audit']={'status':'none-found','discovery_ids':[],'authored_audit':str(E/'conceptual-mirror-audit.authored-v1.json'),'independent_review':{'file':str(dest/'EXPOSITION-SOURCE-MAP-CONCEPTUAL-REVIEW.v3.json'),'sha256':critical['EXPOSITION-SOURCE-MAP-CONCEPTUAL-REVIEW.v3.json']}}
cell['statement_seal']['status']='EXACT_UNCHANGED_STANDARD_BOREL_TYPES;LOCAL_COMPILED;INDEPENDENT_SOURCE_ACCEPTED;READER_NATIVE_SEPARATE'
cell['reader_contract']['status']='Source-reviewed exact148P+108privateT lines in6folds, all assumptions/formulas/source spans accepted at37c228. Native/runtime/sourceindex/graph integration separate.'
cell['learning_contract']['reader_backpressure']['assumptions_preserved']=True
cell['graph_contribution']['visual_review']='Exact P3material canonical parents and privateT→P accepted in source-to-code review. Runtime bounded graph and globalintegration separate.'
cell['reuse_plan']['known_consumers']=[audits[1]['lean']['declaration']]
C.write_bytes(dump(cell));pub.check_advance([audits[0]['lean']['declaration']],reviewed=True)
assert not frontiers.validate_cells(frontiers.load_cells())
create(dest/'transfer.json',dump({'canonical_fields_copied_verbatim':fields,'ROOT_fidelity_verdicts':0,'ledger_calls':0,'checked_source_commit':'37c228612fc3773c0dc1021cb6d7128cd0b55cfa','original_phase3_manifest_files':len(mf['files']),'complete_task_archive_files':len(files),'archive_members_exactly_match_manifest':True}))
create(dest/'carry-original-source-script.py',Path(__file__).read_bytes())
paths=[A,C,E/'private-consumer-source-reviewed.bounded.json',*[p for p in sorted(dest.rglob('*')) if p.is_file()]]
spec=W/'source-carrier.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(A),str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry independent actual Gaussian structure source and exposition reviews'],check=True)
head=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{head}:{p}')==p.read_bytes()
out={'source_carrier_commit':head,'source_reader_commit':'37c228612fc3773c0dc1021cb6d7128cd0b55cfa','complete_source_originals':len(files),'phase3_originals':len(mf['files']),'ledger_mutations':0,'ROOT_fidelity_verdicts':0,'publication_reviewed_admission':'PASS','frontier_schema':'PASS'}
create(W/'actual-independent-source-carrier-commit.json',dump(out));print(json.dumps(out))
