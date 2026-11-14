"""Freeze unchanged P plus the real final centered/weighted consumer and bounded originals."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tarfile
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean')
slug='huanjian-gaussian-source-matrix-variance'
LP=Path('website/content/declaration_lessons')/(slug+'.json')
PP=Path('website/content/publications')/(slug+'.json')
AP=Path('research-wiki/semantic-roundtrip/audits')/(slug+'.json')
R=Path('.astis/semantic-neutral-20261112/mv_src_6e28/r9-centered-whole-code-only-v1')
D=E/'source-review/mv_src_6e28/r9-centered-whole-code-only-v1'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
def copy_once(p,raw):
    if p.exists():assert p.read_bytes()==raw
    else:create(p,raw)
head=git('rev-parse','HEAD').decode().strip()
b=json.loads((W/'continuation-after-shared-VERIFIED.private.json').read_bytes())
assert head==b['head']=='6819e686116e6f18df3ef0e638c6ca24bde7dd8d'
assert not git('diff','--cached','--name-only')
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(LP),str(PP),str(AP)}
ledger=Path('runs/substantive_advances.jsonl').read_bytes()
assert sha(ledger)==b['ledger_sha256']
states=advance._replay_advances([json.loads(x) for x in ledger.splitlines()])
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance')['state']=='EXPLORING'
assert states==b['all_foreign_states']
assert states['ASTIS-SA-20261112-RealMatrixPositiveIntegral']['state']=='VERIFIED'
for p,h in b['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes())==h,p
assert sha(P.read_bytes())=='d9db32e38f18f1f92a94c82886063181375a9e214f7d44ce1bca2a240586ace6'
assert git('show',f'{head}:{P}')==P.read_bytes()
assert sha(T.read_bytes())=='c72d3573c6047b75983a958ad8b98de9c399e13277daa852a66c3e5a0820e73b'
assert sha(Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json').read_bytes())=='5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14'
draft=json.loads((E/'full-consumer-reader-v3b.record.json').read_bytes())
assert draft['publication_binding_sha256']=='bcd7e854e2c26d8201cbc6a25fc23d7acbdcf9866b0d8e799bdda8d88eb39a90'
receipts=[]
for stem in ['20261112T164153811449Z-source-matrix-variance-final-centered-consumer-firstbuild','20261112T164441583114Z-source-matrix-variance-final-P-T-exact-proof-value-kernel-first']:
    p=Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json'); rr=p.read_bytes(); r=json.loads(rr)
    assert r['exit_code']==0 and sha(Path(r['log']).read_bytes())==r['log_sha256']
    receipts.append({'path':str(p),'sha256':sha(rr),'log_sha256':r['log_sha256']})
kernel=Path(json.loads(Path(receipts[1]['path']).read_bytes())['log']).read_text()
assert 'ACTUAL_FINAL_R9_ALL_OWNED_KERNEL_INSPECTED 7' in kernel
assert kernel.count('ACTUAL_FINAL_R9_ROOT_PROOF_VALUE_SEALED_KERNEL_APPLICATION_PASS ')==2
assert sha((R/'portable-custody-manifest.json').read_bytes())=='80c817a1343707c1aaba0c159ecf7857976f21c9f7e79faf65897f3ca6498610'
assert sha((R/'WHOLE-CODE-FROZEN.json').read_bytes())=='3632ed19876d0c30660801c7e3dcfcdcfaa164aa1e7191c712931e43c1988d52'
manifest=json.loads((R/'portable-custody-manifest.json').read_bytes())
assert len(manifest['records'])==52
for item in manifest['records']:
    p,dest=Path(item['source_path']),Path(item['destination_path']); raw=p.read_bytes()
    assert p.is_relative_to(R) and dest.is_relative_to(D) and not p.is_symlink()
    assert len(raw)==item['bytes'] and sha(raw)==item['sha256']
    copy_once(dest,raw)
post=json.loads((R/'postseal-output-index.json').read_bytes())
for item in post['files']:
    p=Path(item['path']); raw=p.read_bytes()
    assert p.is_relative_to(R) and len(raw)==item['bytes'] and sha(raw)==item['sha256']
    copy_once(D/p.relative_to(R),raw)
for name in ['portable-custody-manifest.json','postseal-output-index.json','WHOLE-CODE-FROZEN.json']:
    copy_once(D/name,(R/name).read_bytes())

originals=[]
review=json.loads((W/'reviewed-preproof-inputs.json').read_bytes())
for item in review['independent_originals']:
    p=Path(item['path']); raw=p.read_bytes()
    assert len(raw)==item['bytes'] and sha(raw)==item['sha256']
    originals.append(p)
originals += [p for p in W.iterdir() if p.is_file() and not p.is_symlink() and '.private.' not in p.name]
for p in sorted(Path('.astis/huanjian-resume-20261103').glob('*-source-matrix-variance-*.receipt.json')):
    r=json.loads(p.read_bytes()); log=Path(r['log']).resolve().relative_to(Path.cwd().resolve())
    assert sha(log.read_bytes())==r['log_sha256']
    originals += [p,log]
originals=sorted(set(originals))
assert all(p.stat().st_size<5_000_000 and '.private.' not in p.name for p in originals)
archive_path=E/'full-variance-preproof-and-local-mathematics.original-files.tar.gz'
with tarfile.open(archive_path,'x:gz') as archive:
    for p in originals:archive.add(p,arcname=str(p),recursive=False)
with tarfile.open(archive_path,'r:gz') as archive:
    for p in originals:assert archive.extractfile(str(p)).read()==p.read_bytes()
create(E/'full-variance-preproof-and-local-mathematics.original-manifest.json',dump({'files':{str(p):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in originals},'private_foreign_control_index_excluded':True}))
record={'mathematical_candidate_parent':head,'public_producer':{'file':str(P),'sha256':sha(P.read_bytes()),'same_preexisting_canonical_declaration':True},
    'actual_private_consumer':{'file':str(T),'sha256':sha(T.read_bytes()),'lines':206,'signature_sha256':'95e81a02e5302de9a42e3b60038ffad6195315ac2eca99a4e6abb39978609f7e'},
    'actual_final_build':receipts[0],'actual_final_proof_value_kernel':receipts[1],
    'owned_math':{'handwritten_roots':2,'generated_internal':5,'all7_closed_reachable_standard_axioms':True},
    'both_raw_Expr_equalities':False,'actual_literal_root_proof_values_kernel_checked':True,'q0_instances':True,
    'full_reader':draft,'archive_sha256':sha(archive_path.read_bytes()),'archive_originals':len(originals),
    'independent_T_whole_code_freeze_sha256':'3632ed19876d0c30660801c7e3dcfcdcfaa164aa1e7191c712931e43c1988d52',
    'foreign_full_states_preserved':len(states),'foreign_frontiers_including_verifiedS':len(b['all_existing_frontier_hashes']),
    'state':'EXPLORING; exact P/T mathematics compiled, extended source and fresh native/reader acceptance pending.',
    'normal_R9_intake_replayed':False,'root_VERIFIED_calls':0,'private_T_is_public_API':False}
create(E/'full-variance-local-mathematical-result.json',dump(record))
paths=[T,C,LP,PP,AP,*[p for p in sorted(E.rglob('*')) if p.is_file()]]
changes=[]
for p in paths:
    before=subprocess.run(['git','show',f'{head}:{p}'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if before.returncode or before.stdout!=p.read_bytes():changes.append(p)
assert len(changes)==len(set(changes))
spec=W/'full-variance-math-paths.private.nul'
create(spec,b'\0'.join(str(p).encode() for p in changes)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,changes))
subprocess.run(['git','diff','--cached','--check','--',str(T),str(C),str(LP),str(PP),str(AP)],check=True)
subprocess.run(['git','commit','--quiet','-m','Prove actual centered and weighted Gaussian matrix variance consumer'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in changes:assert git('show',f'{commit}:{p}')==p.read_bytes()
assert Path('runs/substantive_advances.jsonl').read_bytes()==ledger
assert not git('diff','HEAD','--name-only')
result={**record,'mathematical_candidate':commit,'exact_changed_carried_files':len(changes)}
create(W/'actual-full-variance-immutable-math-candidate.json',dump(result))
print(json.dumps({k:result[k] for k in ['mathematical_candidate','mathematical_candidate_parent','actual_final_build','actual_final_proof_value_kernel','exact_changed_carried_files','foreign_full_states_preserved','foreign_frontiers_including_verifiedS','root_VERIFIED_calls']}))
