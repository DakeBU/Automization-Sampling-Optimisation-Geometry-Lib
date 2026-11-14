"""Carry conditional repair evidence and bounded independent admission interpretation."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
R=Path('.astis/semantic-neutral-20261113/variance_native_61d0')
V=R/'conditional-reader-v3'
S=Path('.astis/semantic-neutral-20261112/mv_src_6e28/r9-local-verification-admissibility-v1')
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
D=E/'native-review/variance_native_61d0/conditional-proposal-v3/originals'
SD=E/'normal-verification/mv_src_6e28/local-admissibility-originals'
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
head=git('rev-parse','HEAD').decode().strip()
assert head=='8463958bde34c774163ac4fbefa009daeab39d32'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
b=json.loads((W/'continuation-after-S-schema-correction.private.json').read_bytes())
ledger=Path('runs/substantive_advances.jsonl').read_bytes()
states=advance._replay_advances([json.loads(x) for x in ledger.splitlines()])
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance')['state']=='PROVED_LOCAL'
assert states==b['all_foreign_states']
for p,h in b['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes())==h,p
discovery=Path('runs/substantive_discoveries.jsonl').read_bytes()
assert sha((V/'SEAL.json').read_bytes())=='e4d1fc9fdcbc302f62968ed4e0e33e2e6d9748a56e76c47843325f07d48f3195'
assert sha((V/'portable-manifest.json').read_bytes())=='9b567a723469234d167e76080bfc8d710a74e676a05f7c8abfec2015fe1a26b4'
assert sha((V/'postseal-envelope.json').read_bytes())=='f5960f264454157b2e0ae17a04e82dee17565e6a3e230a3312ed120ac1cbee01'
manifest=json.loads((V/'portable-manifest.json').read_bytes());assert len(manifest['files'])==153
records=manifest['files']+json.loads((V/'postseal-envelope.json').read_bytes())['files']
post=V/'postseal-envelope.json'
records.append({'source':str(post.resolve()),'destination':str(D/post.name),'bytes':post.stat().st_size,'sha256':sha(post.read_bytes())})
plans={}
for x in records:
    p,d=Path(x['source']),Path(x['destination'])
    assert p.is_relative_to(R.resolve()) and d.is_relative_to(D) and '..' not in d.parts and not p.is_symlink()
    raw=p.read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256'],str(p)
    if d in plans:assert plans[d]==raw
    plans[d]=raw
assert sha((S/'ADMISSIBILITY-FROZEN.json').read_bytes())=='32018fb316df7d32f805db345b71eea47f79dc1ad7f06d14f27fe5b6409bb3db'
assert sha((S/'originals-manifest.json').read_bytes())=='ee8169b9ddc11f6343dd2e75972d1f5b9134362226bbaa78739857f2bea76885'
for x in json.loads((S/'originals-manifest.json').read_bytes())['files']:
    p=Path(x['path']);assert p.is_relative_to(S) and not p.is_symlink()
    raw=p.read_bytes();assert len(raw)==x['bytes'] and sha(raw)==x['sha256']
    plans[SD/p.relative_to(S)]=raw
for n in ['ADMISSIBILITY-FROZEN.json','originals-manifest.json']:
    plans[SD/n]=(S/n).read_bytes()
assessment=json.loads((V/'assessment.json').read_bytes())
admission=json.loads((S/'bounded-admissibility-decision.json').read_bytes())
assert admission['current_action']=='HOLD_NO_NORMAL_API_OR_C_LEDGER_GIT_CHANGE'
assert admission['reader_failure_must_remain_actual_failure'] is True
assert sha(Path('website/static/proof-readers.css').read_bytes())=='4509e56205aa4bb94c3fa32c7b2b0bd98a9b44a71c23e09f18d5affe038512ad'
for d,raw in plans.items():
    if d.exists():assert d.read_bytes()==raw
    else:create(d,raw)
cell=json.loads(C.read_bytes())
assert cell['status']=='proved_locally' and cell['evidence']['independent_native_reader']['disposition']=='NATIVE_PASS_READER_FAIL'
cell['evidence']['conditional_reader_production_proposal']={
    'disposition':'CONDITIONAL_PROPOSAL_PASS;UNAPPLIED',
    'source_candidate':str(D/'candidate.json'),'candidate_sha256':'50279010816ce1417a9f3b0af342ddc69589969651821c23b788ac50486f2aab',
    'report':str(D/'REPORT.md'),'report_sha256':'0ad261e03e609205b915626694c0af8e6ae4453a5f5156eb69483f6dc8fd0aba',
    'seal':str(D/'SEAL.json'),'seal_sha256':'e4d1fc9fdcbc302f62968ed4e0e33e2e6d9748a56e76c47843325f07d48f3195',
    'assessment':str(D/'assessment.json'),'assessment_sha256':sha((V/'assessment.json').read_bytes()),
    'proposed_CSS_sha256':'60acf59734f5f63567078cc8f442ca04f6e9e661acac745884f094ccc941d8b9',
    'canonical_CSS_remains_sha256':'4509e56205aa4bb94c3fa32c7b2b0bd98a9b44a71c23e09f18d5affe038512ad',
    'actual_browser_exit':0,'production_integrated':False,'original_reader_FAIL_upgraded':False,
    'scope':'Exact proposed production CSS alone changed in the candidate fixture. All4 desktop/mobile contexts and8 source/download checks pass, actualmobile scroll verified. This is neither original production acceptance nor full-site/globalgraph/reader/publication completion.'}
cell['evidence']['local_verification_admissibility']={
    'reviewer':'/root/mv_fresh_source_6e28','decision':str(SD/'bounded-admissibility-decision.json'),
    'decision_sha256':'09285c8723d62efc37d89fc035edfb72f3a0456b7d21a46539b905d1e473f3bf',
    'normative_interpretation':admission['normative_interpretation'],
    'current_action':'HOLD: no V until genuine final math/source/4metadata/guards acceptance and explicit ROOT release',
    'does_not_waive_mobile_delivery_or_owner_release':True}
cell['reader_contract']['status'] += ' A separate exact unapplied production CSS candidate passes actual4context/8source-download/visual-scroll checks. Canonical CSS is unchanged and original productionFAIL remains; no publication/integration/PURIFIED/Goal acceptance.'
C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
record={'kind':'Conditional unapplied production repair QA and bounded local-math admission interpretation carried',
    'metadata_parent':head,'actual_math_commit':'e654e98642350a615c473bc8190fbc1d47fe52bd',
    'reader_author_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae',
    'original_native':'PASS','original_production_reader':'FAIL','conditional_unapplied_patch':'PASS',
    'original_CSS_changed':False,'normalAPI_calls':0,'root_VERIFIED_calls':0,
    'actual_local_V_decision':'HOLD_PENDING_FINAL_ACCEPTANCE','all_complete_original_destinations':len(plans),
    'next':'Hold metadata HEAD; independent native role runs final4metadata gates once, then independent verifier assesses/release under preserved readerFAIL boundary. No source/Lean/code/author-binding changes.'}
rp=E/'actual-conditional-reader-and-admissibility-attachment.json';create(rp,dump(record))
assert Path('runs/substantive_advances.jsonl').read_bytes()==ledger and Path('runs/substantive_discoveries.jsonl').read_bytes()==discovery
for p,h in b['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes())==h,p
paths=[C,rp,*plans]
spec=W/'conditional-reader-admissibility-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry conditional mobile reader repair QA without upgrading original production failure'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
assert not git('diff','HEAD','--name-only')
result={**record,'conditional_metadata_commit':commit,'changed_carried_files':len(paths)}
create(W/'actual-conditional-reader-and-admissibility-commit.json',dump(result))
print(json.dumps(result))
