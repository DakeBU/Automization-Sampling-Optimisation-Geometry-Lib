from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
ident='huanjian-gaussian-source-matrix-radius'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip();assert head=='4c3251454100a4591113b16ed119fdf758c876b7'
assert not git('diff','--cached','--name-only')
names=['author_radius_packet.py','prepare_source_map_and_binding.py','prepare_source_map_and_binding.attempt1.original.py','source-map-attempt1-diagnosis.json','source_span_helpers.exact-prefix.original.py','refine_scalar_wording_and_context.py','refine_scalar_wording_and_context.attempt1.original.py','scalar-wording-attempt1-diagnosis.json','attach_decoders.py','anonymous-P.json','anonymous-T.json','candidate-publication-context.v1.json','candidate-publication-context.v2.json','private-consumer-audit.draft.json','private-consumer-registry.draft.json','private-consumer-audit.bound.v1.json','private-consumer-registry.bound.v1.json','private-consumer-audit.bound.v2.json','private-consumer-registry.bound.v2.json','private-consumer-audit.reconstructed.v1.json','private-consumer-registry.reconstructed.v1.json','fresh-P-review.v1.json','fresh-T-review.v1.json','freeze_reader_candidate.py']
for n in names:create(E/'author-originals'/n,(W/n).read_bytes())
for p in sorted((W/'authored-v1-originals').rglob('*')):
    if p.is_file():create(E/'author-originals'/'authored-v1-originals'/p.relative_to(W/'authored-v1-originals'),p.read_bytes())
R=Path('.astis/huanjian-resume-20261103')
for p in sorted(R.glob('*source-matrix-radius-*.receipt.json')):
    if p.name<'20261113T011700':continue
    r=json.loads(p.read_bytes());log=Path(r['log']);assert sha(log.read_bytes())==r['log_sha256']
    for f in [p,log]:create(E/'author-originals'/'actual-runs'/f.name,f.read_bytes())
L=Path('website/content/declaration_lessons')/(ident+'.json');S=Path('website/content/publications')/(ident+'.json');A=Path('research-wiki/semantic-roundtrip/audits')/(ident+'.json')
paths=[L,S,A,*[p for p in sorted(E.rglob('*')) if p.is_file() and subprocess.run(['git','ls-files','--error-unmatch','--',str(p)],capture_output=True).returncode]]
assert all('.private.' not in str(p) for p in paths)
spec=W/'reader-candidate-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(L),str(S),str(A)],check=True)
subprocess.run(['git','commit','--quiet','-m','Author exact Gaussian radius proof reader and blind reconstructions'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
result={'reader_candidate_commit':commit,'math_candidate_commit':head,'exact_files':len(paths),'P_binding_sha256':json.loads(A.read_bytes())['publication_binding_sha256'],'state':'blind-reconstructed; source review and native acceptance pending','ledger_mutations':0,'production_CSS_changed':False}
create(W/'actual-reader-candidate-commit.json',dump(result));print(json.dumps(result))
