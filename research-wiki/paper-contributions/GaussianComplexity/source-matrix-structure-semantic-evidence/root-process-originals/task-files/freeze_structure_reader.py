from pathlib import Path
import hashlib,json,subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-semantic-evidence')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
assert git('rev-parse','HEAD').decode().strip()=='9ed997b7fda8631deb5bc1397d021495d53c4d41'
assert not git('diff','--cached','--name-only')
names=['author_structure_audits.py','author_structure_publication.py','attach_structure_decoders.py','project_decoder_input_metadata.py','source_span_helpers.exact-prefix.original.py','candidate-publication-context.v1.json','private-consumer-audit.draft.json','private-consumer-registry.draft.json','private-consumer-audit.bound.v1.json','private-consumer-registry.bound.v1.json','private-consumer-audit.reconstructed.v1.json','private-consumer-registry.reconstructed.v1.json','private-consumer-audit.reconstructed.v2.json','private-consumer-registry.reconstructed.v2.json','public-reconstructed-pre-input-projection.original.json','fresh-P-review.v1.json','fresh-T-review.v1.json','freeze_structure_reader.py']
for n in names:create(E/'author-originals'/n,(W/n).read_bytes())
for p in sorted((W/'audit-draft-originals').iterdir()):create(E/'author-originals/audit-draft-originals'/p.name,p.read_bytes())
q=Path('.astis/semantic-neutral-20261113/anon_328a/canonical-input-custody.json');create(E/'decoder-originals/anon_328a'/q.name,q.read_bytes())
R=Path('.astis/huanjian-resume-20261103')
for p in sorted(R.glob('*source-matrix-structure-*.receipt.json')):
 if p.name<'20261113T063800':continue
 r=json.loads(p.read_bytes());lp=Path(r['log']);assert sha(lp.read_bytes())==r['log_sha256']
 for f in [p,lp]:create(E/'author-originals/actual-runs'/f.name,f.read_bytes())
ident='huanjian-gaussian-source-matrix-structure'
roots=[Path('website/content/declaration_lessons')/(ident+'.json'),Path('website/content/publications')/(ident+'.json'),Path('research-wiki/semantic-roundtrip/audits')/(ident+'.json')]
tracked=set(git('ls-files','-z').decode().split('\0'))
paths=roots+[p for p in sorted(E.rglob('*')) if p.is_file() and str(p) not in tracked]
assert all('.private.' not in str(p) for p in paths)
spec=W/'reader-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',*[str(p) for p in roots]],check=True)
subprocess.run(['git','commit','--quiet','-m','Author actual centered Gaussian structure reader and blind decodes'],check=True)
head=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{head}:{p}')==p.read_bytes()
out={'reader_candidate_commit':head,'math_candidate_commit':'9ed997b7fda8631deb5bc1397d021495d53c4d41','files':len(paths),'ledger_mutations':0,'shared_CSS_modified':False,'source_native_acceptance':'pending','P_binding':json.loads(roots[2].read_bytes())['publication_binding_sha256']}
create(W/'actual-reader-candidate-commit.json',dump(out));print(json.dumps(out))
