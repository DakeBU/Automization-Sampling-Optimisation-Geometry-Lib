from pathlib import Path
import sys,json,hashlib,gzip,tarfile
sys.dont_write_bytecode=True
sys.path.insert(0,'.astis/huanjian-gc-fixed-spectrum-detector-20261110')
from lossless_frozen_bundle import archive_exact,put_new,sha
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-target-law-semantic-evidence')
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
files={}
for root in ['.astis/semantic-neutral-20261110/tl_sg_b41a8e','.astis/semantic-neutral-20261110/tl_tc_7c319d']:
    for p in sorted(Path(root).rglob('*')):
        if p.is_file():
            assert p.stat().st_mode&0o777==0o444,p
            assert not p.name.endswith('.private.json'),p
            files[str(p)]=p.read_bytes()
assert files
prepath=E/'independent-preproof-source-topology-all-phases.lossless-file-bytes.tar.gz'
premanifest=E/'independent-preproof-source-topology-archive.json'
if prepath.exists():
    pre=json.loads(premanifest.read_bytes());assert sha(prepath.read_bytes())==pre['sha256']
    with tarfile.open(prepath,'r:gz') as tar:
        assert set(tar.getnames())==set(files)
        for n,b in files.items():assert tar.extractfile(n).read()==b,n
else:
    pre=archive_exact(files,prepath);put_new(premanifest,dump(pre))
checks={}
R=Path('.astis/huanjian-resume-20261103')
for p in sorted(R.glob('*target-law*.receipt.json')):
    x=json.loads(p.read_bytes());log=Path(x['log']);assert sha(log.read_bytes())==x['log_sha256']
    checks[str(p)]=p.read_bytes();checks[str(log.relative_to(Path.cwd()) if log.is_absolute() else log)]=log.read_bytes()
for n in ['producer-attempt-v1.raw.lean.txt','producer-attempt-v2.raw.lean.txt','producer-signature.txt','consumer-signature.txt','strict-statement-projection.json','statement-seal-v1.json','actual-env-at-seal.json','root-confirmed-actual-intake-success.json','normal-intake-attempted.once.json','seal_statements.py','admit_normal_intake_prepared.py','author_publication.py','author-payload.json','package_correspondence.py','check_isolated_static_reader.py']:
    p=W/n;checks[str(p)]=p.read_bytes()
for p in sorted((W/'isolated-static-reader-current').rglob('*')):
    if p.is_file():checks[str(p)]=p.read_bytes()
local=archive_exact(checks,E/'actual-local-checks-and-authoring.lossless-file-bytes.tar.gz')
put_new(E/'actual-local-checks-lossless-archive.json',dump(local))
inputs=[]
for p in [Path('Libraries/conceptual-mirror-protocol.json'),Path('website/content/graph_memory_index.json'),Path('website/content/functor_hypergraph.json'),Path('Libraries/frontloaded-shared-spine.json')]:
    json.loads(p.read_bytes());inputs.append({'path':str(p),'sha256':sha(p.read_bytes())})
audit={'status':'none-found','discovery_ids':[],'scope':'No NEW conceptual mirror: this packet reuses the existing exact Gaussian linear-image, covariance, orthogonal-isometry and measure-integration canonical mathematics. The already reviewed family:gaussian-law-symmetry/transport:gaussian-symmetry-pushforward remains typed conceptual memory, not a formal parent.','hypotheses':'Literal d>=2,kappa>=2, full orthogonal O; precision positivity internally reused from canonical admissibility.','critical_identity':'A^{-1}=O Lambda^{-1} O^T; Gaussian means zero and covariance bilinear forms equal; norm-square invariant under O.','conclusion':'Actual fixed-O full Gaussian measure law; genuine private target norm-square L1 and finite inverse-spectrum mean.','failure_boundary':'Anisotropic Gaussian rotates to conjugated covariance; it is not invariant under arbitrary O with the same covariance. Pointwise O does not supply random-parameter measurability, joint conditional/Haar/adaptive laws or query/cost/TV statements. Shared mechanism does not imply determinant-sign route or any main lower bound.','source_mapping':['S4.E11','S4.SS2.SSS0.Px3.p2.1','A3.SS3.p4'],'exact_formal_parents':json.loads((E/'actual-kernel-owned-inventory.json').read_bytes())['actual_first_public_ASTIS_parents'],'existing_memory_inputs':inputs,'new_solid_Lean_edges_or_graph_global_writes':False}
put_new(E/'postproof-conceptual-mirror-audit.json',dump(audit))
diag={'class':'IMPLEMENTATION_FAILED','scope':'Source-locator generator initially matched the primed sibling too; a specific marker fixed all29 locators. Packager first over-rejected the legitimate private-consumer signature filename, then rejected absolute __file__ keys in its local-check archive. Normalize only archive member names relative to repository. The first completed preproof archive is read back byte-exact and reused without overwrite. No Lean/source mathematics changed; all failures and successors retained.','math_refutation':False}
put_new(E/'source-locator-format-diagnostic.json',dump(diag))
print(json.dumps({'preproof_files':pre['file_count'],'preproof_archive_sha256':pre['sha256'],'actual_local_files':local['file_count'],'local_archive_sha256':local['sha256'],'private_foreign_baselines_never_archived':True,'independent_verdicts_unchanged':True}))
