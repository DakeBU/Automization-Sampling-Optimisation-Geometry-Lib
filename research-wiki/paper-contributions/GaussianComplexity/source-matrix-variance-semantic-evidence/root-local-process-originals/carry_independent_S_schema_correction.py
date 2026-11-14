"""Apply original verifier's exact S metadata serialization repair, with no V replay."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode = True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
R = Path('.astis/semantic-neutral-20261112/mv_src_6e28/metadata-schema-correction')
E = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
D = E/'metadata-schema-correction/mv_src_6e28/originals'
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json')
sha = lambda raw:hashlib.sha256(raw).hexdigest()
dump = lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git = lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as out:out.write(raw)
head = git('rev-parse','HEAD').decode().strip()
assert head == '9398e158975de14500bcd9d4eb60e5828064dd64'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
baseline = json.loads((W/'continuation-after-shared-VERIFIED.private.json').read_bytes())
before = Path('runs/substantive_advances.jsonl').read_bytes()
discovery = Path('runs/substantive_discoveries.jsonl').read_bytes()
assert sha(before) == baseline['ledger_sha256']
states = advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert {k:v for k,v in states.items() if k != 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'} == baseline['all_foreign_states']
for p,h in baseline['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes()) == h,p
original = C.read_bytes()
assert sha(original) == 'c62351bb2acfc624a1acdb50bff4e25297551a0f56b4aae6d3275f5d923412da'
proposed = (R/'C23.proposed.exact.json').read_bytes()
assert sha(proposed) == '5918990bf0a5fc8c1da2522bf8d02d456dbe443fa0d4eaf9bd56322900533138'
old,new = json.loads(original),json.loads(proposed)
restored = copy.deepcopy(new)
restored['evidence']['independent_verification'] = restored['evidence'].pop('independent_verification_details')
assert restored == old and dump(restored) == original
assert isinstance(new['evidence']['independent_verification'],str) and new['evidence']['independent_verification'].strip()
assert '.astis/' not in new['evidence']['independent_verification']
assert new['evidence']['independent_verification_details'] == old['evidence']['independent_verification']
assert sha((R/'PROPOSAL-FROZEN.json').read_bytes()) == '28962fed76ef3fd1e14ae00e78bc637256b275494bb225e7f7be55f58f055033'
mp = R/'portable-originals-manifest.json'
assert sha(mp.read_bytes()) == '5395c8a4ad47e617dd16a4a42677d6c341fb87dda6cc667733f8beca95d6b79e'
manifest = json.loads(mp.read_bytes()); assert len(manifest['records']) == 21
plans = {}
records = manifest['records'][:]
post = R/'postseal-output-index.json'
assert sha(post.read_bytes()) == 'cbc5c992d06c30b83b5a0c53a5d7338de22db3bc8692beceb7e53ffffc8b1db7'
records += [{'source_path':x['path'],'destination_path':str(D/Path(x['path']).relative_to(R)),
             'sha256':x['sha256'],'bytes':x['bytes']} for x in json.loads(post.read_bytes())['files']]
records += [{'source_path':str(p),'destination_path':str(D/p.name),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size} for p in [mp,post]]
for x in records:
    p,d = Path(x['source_path']),Path(x['destination_path'])
    assert p.is_relative_to(R) and d.is_relative_to(D) and not p.is_symlink() and not d.is_symlink()
    raw = p.read_bytes(); assert len(raw) == x['bytes'] and sha(raw) == x['sha256']
    if d.exists():assert d.read_bytes() == raw
    plans[d] = raw
before_errors = frontiers.validate_cells(frontiers.load_cells())
assert before_errors == [str(C)+': status independently_verified requires independent_verification']
for d,raw in plans.items():
    if not d.exists():create(d,raw)
C.write_bytes(proposed)
assert not frontiers.validate_cells(frontiers.load_cells())
assert Path('runs/substantive_advances.jsonl').read_bytes() == before
assert Path('runs/substantive_discoveries.jsonl').read_bytes() == discovery
for p,h in baseline['all_existing_frontier_hashes'].items():
    if p != str(C):assert sha(Path(p).read_bytes()) == h,p
record = {'kind':'Exact independent original S verifier metadata schema proposal carried',
    'metadata_parent':head,'original_C23_sha256':sha(original),'corrected_C23_sha256':sha(proposed),
    'proposal_author':'/root/mv_fresh_source_6e28','proposal_freeze_sha256':'28962fed76ef3fd1e14ae00e78bc637256b275494bb225e7f7be55f58f055033',
    'original_full_V_payload_sha256':'e1f9b9ab79aa965c4234756f6016bab0584402a7f98731cbc667cb9b32ff435a',
    'original_exact_V_append_sha256':'24cc7ea161d32a42a78e3b2e4d10a091faffe604bb1d1c419ee4b943d6d1ab78',
    'required_field_reference_string_and_unmodified_original_details_only':True,
    'entire_original_cell_restorable_byte_exact':True,'full_frontier_validation_after':[],
    'new_normal_API_calls':0,'new_V_or_ledger_events':0,'root_VERIFIED_calls':0,
    'math_source_statement_status_owner_unchanged':True,
    'historical_qualification':'The earlier normal API receipt and preservation guard did not certify post-write S cell schema acceptance. Its original field type error and all original accepted math/source/native/ledger evidence remain preserved. This metadata correction supplies the later actual schema check, not retroactive evidence.',
}
rp = E/'metadata-schema-correction/actual-independent-proposal-application.json'
create(rp,dump(record))
paths = [C,rp,*plans]
assert set(git('diff','HEAD','--name-only').decode().splitlines()) == {str(C)}
spec = W/'S-schema-correction-paths.private.nul'
create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines()) == set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry independent PSD verification evidence schema correction without event replay'],check=True)
commit = git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}') == p.read_bytes()
assert not git('diff','HEAD','--name-only')
# Explicit successor guard; never overwrite original preproof or continuation snapshots.
qualified = copy.deepcopy(baseline)
qualified['head'] = commit
qualified['kind'] = 'R9 continuation after exact independently authored S evidence-schema correction'
qualified['all_existing_frontier_hashes'][str(C)] = sha(proposed)
qualified['original_after_shared_continuation_sha256'] = sha((W/'continuation-after-shared-VERIFIED.private.json').read_bytes())
qualified['authorized_S_schema_only_delta'] = record
indexraw = git('ls-files','--stage','-z')
indexpath = W/'after-S-schema-full-tracked-index.private.raw'
create(indexpath,indexraw)
qualified['tracked_git_index'] = {'path':str(indexpath),'bytes':len(indexraw),'sha256':sha(indexraw),'encoding':'Exact git ls-files --stage -z raw bytes; private and not exported'}
create(W/'continuation-after-S-schema-correction.private.json',dump(qualified))
result = {**record,'schema_correction_metadata_commit':commit,'byte_exact_files':len(paths)}
create(W/'actual-independent-S-schema-correction-commit.json',dump(result))
print(json.dumps(result))
