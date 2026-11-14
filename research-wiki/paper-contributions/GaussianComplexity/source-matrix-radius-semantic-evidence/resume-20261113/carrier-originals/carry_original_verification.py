"""Commit the already executed independent V and sealed originals, never replay it."""
from pathlib import Path
import hashlib,json,subprocess,tarfile
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
R=Path('.astis/semantic-neutral-20261113/radius_src_73c1/resume_normal_v_v1')
N=Path('.astis/semantic-neutral-20261113/radius_native_5bf8')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
L=Path('runs/substantive_advances.jsonl')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip();assert head=='9e5ee5685d4f05fcfba9bcf700af25b8ec61386b'
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
append=(R/'actual-normal-V-append.jsonl').read_bytes();assert sha(append)=='e4bc1a74c715b4493cda3d379387d5e0c103fba705f61a87090eaf5d1ebf4382'
assert L.read_bytes()==git('show',f'{head}:{L}')+append
assert C.read_bytes()==(R/'ownC.after.json').read_bytes() and sha(C.read_bytes())=='738ddb93a36ebc0914d1ca93a720edb22fc941befcf8d767a800002a5103804c'
event=json.loads(append);pl=json.loads((E/'actual-PROVED_LOCAL-evidence.full.json').read_bytes())
assert len(pl)==25 and all(event['evidence'][k]==v for k,v in pl.items())
assert event['to_state']=='VERIFIED' and event['advance_id']=='ASTIS-SA-20261113-GaussianComplexitySourceMatrixRadius'
assert json.loads((R/'VERIFIED-evidence.full.json').read_bytes())==event['evidence']
outcome=(R/'actual-normal-V-outcome.json').read_bytes();assert sha(outcome)=='aa8a3736c4b2064c1fcf61f5c54389551ba0a0757ece9ef03dc4bb5d21b1e9b8'
bundle=R/'portable-final';archive=bundle/'verifier-originals-complete.tar.gz';mf=bundle/'verifier-originals.files.sha256.json'
assert sha(archive.read_bytes())=='8c7eee7a8df419fee162f70684e80e5f989ce4fa99aebc3881acfefa23720838'
assert sha(mf.read_bytes())=='6cb7d40271b6dde4a02e8b4887406bc469779d8641bcec31f2d1dc10f8492336'
manifest=json.loads(mf.read_bytes());assert manifest['file_count']==189
with tarfile.open(archive,'r:gz') as tf:
    for n,x in manifest['files'].items():
        assert not n.startswith('/') and '..' not in Path(n).parts and not any(p.startswith('.PRIVATE') for p in Path(n).parts)
        b=tf.extractfile(n).read();assert len(b)==x['bytes'] and sha(b)==x['sha256']
    nb=tf.extractfile('resume_normal_v_v1/native_package/originals-successor.tar.gz').read()
    assert sha(nb)=='c6cbce262f8162379f9f30db523a40f6711e9628d0267891c092c87a3302e32e'
dest=E/'normal-verification/radius_src_73c1/resumed'
for p in sorted(bundle.iterdir()):
    assert p.is_file();create(dest/'portable-final'/p.name,p.read_bytes())
for n in ['actual-normal-V-outcome.json','actual-normal-V-append.jsonl','VERIFIED-evidence.full.json','actual-API-returned.receipt.json','postwrite-checks.receipt.json','independent-verification-REPORT.md']:
    create(dest/n,(R/n).read_bytes())
for n in ['current-independent-acceptance-summary.json','conditional-reader-acceptance.json','conditional-acceptance-freeze.json','final-four-metadata-results.json']:
    create(E/'native-review/radius_native_5bf8/resumed'/n,(N/'resume-20261113'/n).read_bytes())
native_package=Path('.astis/semantic-neutral-20261113/radius_native_5bf8/portable-successor-20261113-v4')
for n in ['files.sha256.json','package-result.json']:create(E/'native-review/radius_native_5bf8/resumed'/n,(native_package/n).read_bytes())
memory={'local_state':'INDEPENDENT_NORMAL_VERIFIED_ONCE;ORIGINAL_READER_FAIL;CONDITIONAL_CSS_PASS_UNAPPLIED','math_commit':'4c3251454100a4591113b16ed119fdf758c876b7','reader_commit':'c4d031f237fa0e16fbba16987ca6b34c7f3dfd98','checked_held_commit':head,'actual_independent_verifier':'radius_src_73c1_independent_resumed_verifier','PL_calls':1,'V_calls':1,'ROOT_V_calls':0,'actual_V_append_sha256':sha(append),'all25_PL_fields_inline_unchanged':True,'verifier_originals_archive':{'path':str(dest/'portable-final'/archive.name),'sha256':sha(archive.read_bytes()),'indexed_files':189},'native_successor_archive':{'inside_verifier_archive_member':'resume_normal_v_v1/native_package/originals-successor.tar.gz','sha256':sha(nb),'indexed_originals':1783,'actual_tar_members':1784,'extra_member':'SUCCESSOR-FILES.sha256.json; equals the outer indexed-file manifest, not an extra mathematical claim'},'original_reader':'FAIL_MOBILE_TABLE_CLIPPING','conditional_reader':'INDEPENDENT_ACTUAL_AND_VISUAL_PASS_UNAPPLIED','later_stages':'Integration/publication/purification/wholeGoal HOLD; originalglobalownerunreleased, no CSS/rootimport/Registry/globalgraph edits.','next_unclaimed_packet':{'seal':'.astis/huanjian-gc-source-matrix-structure-20261113/statement-seal-v2.json','seal_sha256':'0164b6bcb7f1362c27e459eccf6a68a72a7cea81272f15377e7c193af18e3c60','source_graph_sha256':'9242c7792704cb38a213905baee8cd074b286d5ead153b27defa3d65676cf182','distinct_topology_review_sha256':'5bb669aeea59a3b8320e57ee2339ea4007275ea0affdaadf8fe0147412719e7d','status':'Proof-free exact standardBorel signatures form; sourcegraph/type/topology preparation accepted; no SAU/targetproof yet.'},'private_guards_exported':False,'do_not_replay':'Existing real V is carried verbatim; never call API again.'}
create(E/'local-cycle-memory.json',dump(memory))
readme=r'''# Gaussian source matrix radius — local cycle independently verified

Public P proves both actual truncated-summand and actual-mean operator-norm
bounds. Its private Tests consumer proves the actual centered and deterministic
cosine-weighted radius. The sole source condition is `2*q+1<d`; q=0, the literal
product experiment, actual Bochner means and inclusive cutoff are preserved.

One independent normal VERIFIED event has actually occurred; ROOT did not verify
its own proof. All 25 original PROVED_LOCAL values remain inline unchanged.
The checked math is4c325145; current reviewed reader isc4d031; final metadata
gates and independent normal V were checked at9e5ee568. Exact immutable receipts,
proof-value inspections, failures, source reviews and real V originals are
available through `local-cycle-memory.json` and its lossless archives.

The original production-CSS mobile reader FAIL remains FAIL. The exact separate
one-file CSS candidate passed actual and independent visual checks and remains
unapplied. Integration, publication, purification, both complete main lower
bounds, oracle/TV/precision/query-cap/cost adapters and the overall Goal remain
unfinished. The original shared stabilization owner is unreleased.

The earlier pause/upload-failure records remain historical and unchanged. The
user has resumed the same Goal. The next unclaimed packet concerns actual
centered/weighted matrix measurability, independence, integrability, zero mean
and Hermitian symmetry; proof-free Borel typing and independent source topology
preparation are accepted, but no new SAU or target proof has been claimed.
'''
(E/'README.md').write_bytes(readme.encode())
process=E/'resume-20261113/carrier-originals';create(process/'carry_original_verification.py',(W/'carry_original_verification.py').read_bytes())
paths=[C,L,E/'README.md',E/'local-cycle-memory.json',*[p for p in sorted(dest.rglob('*')) if p.is_file()],*[p for p in sorted((E/'native-review/radius_native_5bf8/resumed').rglob('*')) if p.is_file()],process/'carry_original_verification.py']
spec=W/'normalV-carrier-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(L),str(E/'README.md'),str(E/'local-cycle-memory.json')],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry independent Gaussian radius verification and exact acceptance originals'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
result={'independent_V_carrier_commit':commit,'checked_held_commit':head,'exact_owned_files':len(paths),'actual_V_append_sha256':sha(append),'all25_PL_fields_unchanged':True,'ROOT_V_calls':0,'normal_API_replay':False,'private_guards_exported':False}
create(W/'actual-original-verification-carrier.json',dump(result));print(json.dumps(result))
