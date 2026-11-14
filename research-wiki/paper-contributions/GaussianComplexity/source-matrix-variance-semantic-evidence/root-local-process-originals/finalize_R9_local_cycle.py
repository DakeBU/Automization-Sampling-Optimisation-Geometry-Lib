"""Record completed local R9 mathematics, keeping original mobile delivery and whole Goal open."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
head=git('rev-parse','HEAD').decode().strip()
assert head=='ba4026840a1d763941e803faf9bd375d8212a1b8'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
ledger=Path('runs/substantive_advances.jsonl').read_bytes()
states=advance._replay_advances([json.loads(x) for x in ledger.splitlines()])
adv='ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
assert states[adv]['state']=='VERIFIED'
events=[json.loads(x) for x in ledger.splitlines()]
vs=[x for x in events if x.get('advance_id')==adv and x.get('to_state')=='VERIFIED']
assert len(vs)==1 and vs[0]['worker_id']=='/root/mv_fresh_source_6e28'
assert sha(C.read_bytes())=='69cf7e46d4d084ba82be4a5b87a42fdc99043ff59aa2881431c277387c767d3f'
owner=json.loads((W/'original-owner-after-R9-VERIFIED.json').read_bytes())
assert all(x['original_owner_state']=='STABILIZING' for x in owner['refs'])
v=json.loads((W/'actual-original-independent-VERIFIED-commit.json').read_bytes())
nextpath=Path('.astis/huanjian-gc-source-matrix-radius-20261113/reviewed-preproof-inputs.json')
nextreview=json.loads(nextpath.read_bytes())
memory={
    'advance_id':adv,'state':'VERIFIED; independent local mathematics, not delivered or wholeGoal complete',
    'mathematical_candidate':'e654e98642350a615c473bc8190fbc1d47fe52bd',
    'reader_author_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae',
    'final_held_metadata_commit':'02fb93c64e4222f112e57c97ced2a548235cd0f6',
    'original_V_carrier_commit':head,'exact_original_V_append_sha256':v['append_sha256'],
    'full_original_V_payload_sha256':v['full_original_V_payload_sha256'],
    'independent_normal_V_calls':1,'normal_V_API_failures':0,'root_VERIFIED_calls':0,
    'all21_original_PL_values_inline_unchanged':True,
    'mathematical_result':'Same literal original independent-column product Gaussian experiment and sole2q+1<d includingq0. PublicP proves actualYi² Bochner integrability and PSD(CI-sumEYi²), C=2r(r+2)/d. PrivateT materially consumesP/actualmean/sharedPSDexpectation to prove actualZi² and(wiZi)² integrability and both realL2operatornorm variance bounds<=C. Noncommutative cross terms, true means/PSD and actualnorm are internally discharged.',
    'public_T_API_credit':False,'new_shared_R9_nodes':0,
    'canonical_shared_reuse':'RealMatrixPositiveIntegral.integral_posSemidef belongs to its already independently VERIFIED shared cycle; no duplicateR9shared node or new source assumption.',
    'independent_acceptance':'Original exact statement/binder seal, sourcegraph and distinct topology challenge; completeP216/T206 code and7slot fresh source reviews; original anonymousP/T decoders; independent12module emptyASTIS rebuild,54full actualtypes/bodies/kernelchecks,4sealedliteral actualproofbody applications;4metadata gates eachonce0 on held02fb.',
    'native_original_reader_disposition':'NATIVE_PASS_READER_FAIL',
    'actual_original_mobile_failure':'390publication comparison table cropped, wrapper335/555px overflowvisible andscrollLeft0. Desktop/mobile4contexts and8source/download checks ran; no math/page/HTTP errors. Fullsite/globalgraph later overlays remain outsidefocusedfixture.',
    'conditional_production_repair':'UNAPPLIED exactproof-readers.css4509->60acf patch2442. Separate4context/8source-download/realleft-rightscrollvisual candidatePASS; canonicalCSS unchanged. ConditionalPASS neverupgrades originalFAIL.',
    'local_math_V_admissibility':'Original independent bounded protocol interpretation allows local mathematicalV while explicitreaderFAIL/deliveryboundary remains. RequiredactualLean/source/metadata/fullguards genuinely passed; this is not publication/PURIFIED/Goal admission.',
    'preservation':'Independent before/precall/after:309full foreignadvances,43discovery fullstates+raw,469foreignregularfrontiers inclREADME,134980trackedpaths/modes/index and117409qualifiedhistorical/controlartifacts preserved exceptownC+oneappend. Qualifiedhistorical/control count is not a literalqueue count. Fullprivateguards/index inventories notexported.',
    'failures_and_limits':'All failed draft/probe/source-reader/metadata/schema/native/permission/browser/preflight/custody versions retained and typed. ExistingSverification DICT/string schema mistake corrected by its originalverifier proposal with oldDICT exactly retained and originalS V unreplayed. ROOTsource transfer demanded zero informationaldeltas thenhit pre-existingSschema; fixedwithoutmathchange. Nativeapproval waits had no inventedexecutionreceipts. OriginalmobileFAIL preserved. Five independentnormalVlocalpreflight errors and postsealcustody corrections are explicit; finalclosed-bytecustody supersedesfailedmanifests withoutchangingactualV.',
    'conceptual_mirror':'Independent originalperSAU none-found; existingconceptualmirror identities/status unchanged, not revalidated or promoted to Lean implications.',
    'integration_publication_purification':'HOLD: original formalremote owner stillSTABILIZING afterreal foregroundfetch. No clean-port/rootaggregator/Registry/globalgraph/sourceindex/siteCSS/push/takeover. Canonical public placement ofprivateT, older privatecone/range canonicalization and actualsite/mobile delivery remain serializedwork.',
    'latest_original_owner_observation':owner,
    'next_unclaimed_radius_packet':{
        'state':'Exactstatement/source preparation admitted only; no newintake or targetformalproof',
        'seal_sha256':nextreview['statement_seal_sha256'],
        'readback_sha256':sha(nextpath.read_bytes()),'source_originals_verified':len(nextreview['all_original_files']),
        'target':'ActualpointwiseYi norm<=2rL/d andactualmean norm<=2r/d; materially consumed in literalZ andcosineweightedZ radius<=2r(L+1)/d. All sameexperiment/hq/q0;9internalports remainopen.',
        'next_action':'One normalnewSAU intake with fresh fullpreservationguard, reuseactualmean/feature/standardGaussianmoment andMathlibrealrankone/operatornorm APIs. Prove estimates internally, no norm/mean/integrability/PSD certificate binder. Then ordinary independent source-blind/source/native/reader/metadata verification.'},
    'whole_Goal':'UNFINISHED. Two main lowerbounds, fullnecessarybackground, realexactmatvec/deterministicworstquerycap/TVprecision/dimension-kappa/expectedcost adapters and source/Lean/canonicalwebsite/sourceindex/graph/integration/publication/purification/finalreader acceptance remain required.',
}
create(E/'local-cycle-memory.json',dump(memory))
readme='''# Actual Gaussian matrix variance: local independent verification

On the original independent-column Gaussian experiment, with only
`2*q+1<d` and with `q=0` retained, the public theorem proves genuine squared
summand integrability and

$$\sum_i\mathbb E_\mu[Y_i^2]\preceq C I,\qquad C=\frac{2r(r+2)}d.$$

The exact private Test consumer uses the actual mean
`Z_i=Y_i-integral(Y_i)` and `w_i=cos((2q+1)theta_i)` to prove both actual
centered-square integrability claims and

$$\left\|\sum_i\mathbb E_\mu[Z_i^2]\right\|_{op}\le C,\qquad
\left\|\sum_i\mathbb E_\mu[(w_iZ_i)^2]\right\|_{op}\le C.$$

These use ordinary matrix multiplication and the real Euclidean operator norm.
Noncommutative centering, both fixed-multiplication integrals, PSD expectations
and norm conversion are proved internally. The private consumer is real
mathematics but is not a public API or either main lower bound.

The sole independent normal verification event is carried by
`ba4026840a1d763941e803faf9bd375d8212a1b8`; ROOT did not self-verify or replay it.
See `local-cycle-memory.json`, `actual-original-independent-VERIFIED-carrier.json`
and the complete source/native/normal-verification originals in this directory.

Original focused production reader: **mobile publication FAIL** (cropped
comparison table). Native math: **PASS**. The exact unapplied production CSS
repair has a separate **conditional proposal PASS**, including real horizontal
scrolling. The original failure is not upgraded. Main integration, actual
production repair/delivery, source-index/globalgraph publication, canonical API
placement and purification await the serialized owner; the whole Goal is open.

The next bounded source packet is the actual pointwise summand and mean norm
bounds, followed by the exact centered/cosine-weighted radius. Its statement,
binders, definitions and distinct source topology challenge are sealed/admitted;
its formal mathematical estimates are not yet proved.
'''
create(E/'README.md',readme.encode())
paths=[E/'local-cycle-memory.json',E/'README.md']
public_json_prefixes=('actual-','original-owner-','source-attachment-attempt','conditional-custody-count')
public_json_names={'centered-draft-progress.json','reviewed-preproof-inputs.json','local-proof-transition-attempted.once.json'}
for p in sorted(W.iterdir()):
    if not p.is_file() or p.is_symlink() or '.private.' in p.name:continue
    allowed=p.suffix in {'.py','.lean','.txt'} or (p.suffix=='.json' and (p.name.startswith(public_json_prefixes) or p.name in public_json_names))
    if not allowed:continue
    raw=p.read_bytes();assert len(raw)<5_000_000
    if p.suffix=='.json':
        obj=json.loads(raw)
        assert not any(k in obj for k in ['all_foreign_states','all_existing_frontier_hashes','tracked_git_index','full_states']),str(p)
    d=E/'root-local-process-originals'/p.name;create(d,raw);paths.append(d)
for p in sorted(Path('.astis/huanjian-resume-20261103').glob('*-source-matrix-variance-*.receipt.json')):
    r=json.loads(p.read_bytes());log=Path(r['log']);assert sha(log.read_bytes())==r['log_sha256']
    for q in [p,log]:
        assert q.stat().st_size<5_000_000
        d=E/'root-local-process-originals/actual-runs'/q.name;create(d,q.read_bytes());paths.append(d)
assert Path('runs/substantive_advances.jsonl').read_bytes()==ledger
assert not git('diff','HEAD','--name-only')
spec=W/'cycle-memory-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(E/'README.md'),str(E/'local-cycle-memory.json')],check=True)
subprocess.run(['git','commit','--quiet','-m','Record verified actual matrix variance and explicit mobile delivery boundary'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
assert Path('runs/substantive_advances.jsonl').read_bytes()==ledger
assert not git('diff','HEAD','--name-only')
record={'cycle_memory_commit':commit,'original_V_carrier':head,'state':'R9localindependentVERIFIED;originalmobileFAIL;wholeGoalunfinished','root_VERIFIED_calls':0,'owned_memory_and_process_original_files':len(paths),'next_radius_source_admitted_not_proved':True}
create(W/'actual-cycle-memory-commit.json',dump(record))
print(json.dumps(record))
