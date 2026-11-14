"""Continue the first intake after a pre-API schema label error; do not recapture/replay."""
from pathlib import Path
import hashlib,json,os,stat,subprocess,sys
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-gram-realization-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-gram-realization.json')
SP=Path('research-wiki/paper-contributions/GaussianComplexity/source-gram-realization-statement-seal.json')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261113-GaussianComplexitySourceGramRealization'
OWNER='huanjian_gc_20261113_source_gram_realization'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
def fingerprint(p):
 st=p.lstat()
 if stat.S_ISLNK(st.st_mode):return {'mode':stat.S_IMODE(st.st_mode),'kind':'symlink','target':os.readlink(p)}
 assert stat.S_ISREG(st.st_mode)
 return {'mode':stat.S_IMODE(st.st_mode),'kind':'regular','bytes':st.st_size,'sha256':sha(p.read_bytes())}
head=git('rev-parse','HEAD').decode().strip();assert head=='7b0ef4eeab3257d04616e1b6dbbed08d01f03361'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
assert not (W/'normal-intake-attempted.once.json').exists()
b=json.loads((W/'preproof-baseline.private.json').read_bytes())
before=L.read_bytes();assert sha(before)==b['ledger_sha256'] and before==git('show',f'{head}:{L}')
states=advance._replay_advances([json.loads(x) for x in before.splitlines()]);assert ADV not in states and states==b['all_foreign_states']
discover=Path('runs/substantive_discoveries.jsonl').read_bytes();db=json.loads((W/'preproof-discoveries.private.json').read_bytes());assert sha(discover)==db['ledger_sha256'];ds=db['full_states']
index=b['tracked_git_index'].encode();assert git('ls-files','--stage','-z')==index
tracked=b['all_existing_tracked_fingerprints'];controls=b['actual_control_fingerprints'];foreign_frontiers=b['all_existing_frontier_hashes']
for p,fp in {**tracked,**controls}.items():assert fingerprint(Path(p))==fp
for p,h in foreign_frontiers.items():assert sha(Path(p).read_bytes())==h
sealraw=SP.read_bytes();assert sha(sealraw)=='7b2f71cf9e89a41da4f66b2b3908222c875cd2fec2f8b2ca6533fe61b3bb3ce9';seal=json.loads(sealraw)
P,T=[seal[k]['planned_file'] for k in ['producer','actual_private_consumer']]
assert not Path(P).exists() and not Path(T).exists()
admission=json.loads((E/'preproof-source-admission.json').read_bytes());originals=json.loads((E/'independent-preproof-originals.manifest.json').read_bytes())['files']
for p,h in admission['critical_inputs'].items():assert sha(Path(p).read_bytes())==h
cell=json.loads(C.read_bytes())
searches=cell['shared_floor_audit']['searched'];searches[0]='Samplinglib/ASTIS canonical reuse: '+searches[0]
searches.append('Mathlib actual bounded interface search: Matrix Kronecker, multiplication/diagonal/transpose, L2 norm and real sqrt source files. Exact diagonal_mul/mul_diagonal/transpose_mul interfaces found; no generic certificate or target proof supplied.')
cell['shared_floor_audit']['searched']=searches;cell['reuse_plan']['searched_existing']=searches
C.write_bytes(dump(cell));errors=frontiers.validate_cells(frontiers.load_cells());assert not errors,errors
create(E/'intake-originals/complete_gram_intake_after_search_labels.py',Path(__file__).read_bytes())
for n in ['start_gram_sau.attempt1.original.py','frontier-before-search-label-repair.original.json','intake-attempt1-diagnosis.json']:create(E/'intake-originals'/n,(W/n).read_bytes())
R=Path('.astis/huanjian-resume-20261103')
for p in sorted(R.glob('*source-gram-realization-*.receipt.json')):
 r=json.loads(p.read_bytes());lp=Path(r['log']);assert sha(lp.read_bytes())==r['log_sha256']
 for f in [p,lp]:create(E/'intake-originals/actual-runs'/f.name,f.read_bytes())
# Exact normal-intake tail; the preserved first pass stopped before this text.
src=(W/'start_gram_sau.py').read_text();tail=src[src.index('proposal=advance.AdvanceProposal'):]
exec(compile(tail,'<exact-normal-intake-tail-after-pre-API-schema-fix>','exec'))
