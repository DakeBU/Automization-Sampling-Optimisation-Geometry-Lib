"""Carry the independent native PASS and actual original reader FAIL without upgrading either."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode = True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
R = Path('.astis/semantic-neutral-20261113/variance_native_61d0')
E = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
D = E/'native-review/variance_native_61d0/originals'
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
sha = lambda raw:hashlib.sha256(raw).hexdigest()
dump = lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git = lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
head = git('rev-parse','HEAD').decode().strip()
assert head == '339d6176f61fce828f4766a8951857cfef746a62'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
b = json.loads((W/'continuation-after-S-schema-correction.private.json').read_bytes())
before = Path('runs/substantive_advances.jsonl').read_bytes()
states = advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert states.pop('ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance')['state'] == 'PROVED_LOCAL'
assert states == b['all_foreign_states']
for p,h in b['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes()) == h,p
discovery = Path('runs/substantive_discoveries.jsonl').read_bytes()
mp,post = R/'portable-manifest.json',R/'postseal-envelope.json'
assert sha(mp.read_bytes()) == '1379b67fc72814e6a12d04317b3780c56c4ba8b312720663bc8e39928121a72e'
assert sha(post.read_bytes()) == '9f6c9b5ae108dc9739b5a953987feaf08d2f1621c32815242d6451e6c3c81b3b'
assert sha((R/'SEAL.json').read_bytes()) == '8a76e39bd0c097f3ea54f95afe07d142354d968437fe83c7a11bf04f630fdecd'
manifest = json.loads(mp.read_bytes()); assert len(manifest['files']) == 1319
retrieval = R/'conditional-reader-v3/original-wrapper-retrieval.json'
relocations = {x['destination']:x for x in json.loads(retrieval.read_bytes())['files']}
assert len(relocations) == 1
records = manifest['files']+json.loads(post.read_bytes())['files']
records.append({'source':str(post.resolve()),'destination':str(D/post.name),'bytes':post.stat().st_size,'sha256':sha(post.read_bytes())})
plans = {}; relocation_uses = []
for x in records:
    p,d = Path(x['source']),Path(x['destination'])
    assert p.is_relative_to(R.resolve()) and d.is_relative_to(D) and '..' not in d.parts
    if str(d) in relocations:
        y = relocations[str(d)]
        assert y['sha256'] == x['sha256'] and y['bytes'] == x['bytes']
        p = Path(y['source']); relocation_uses.append({'original_source':x['source'],'preserved_original_source':str(p),'destination':str(d),'sha256':x['sha256']})
    assert p.is_relative_to(R.resolve()) and p.is_file() and not p.is_symlink()
    raw = p.read_bytes(); assert len(raw) == x['bytes'] and sha(raw) == x['sha256'],str(p)
    if d in plans:assert plans[d] == raw
    plans[d] = raw
assert len(relocation_uses) == 1
native = json.loads((R/'native-summary.json').read_bytes())
assessment = json.loads((R/'reader-assessment.json').read_bytes())
assert native['actual_math_compiled_commit'] == 'e654e98642350a615c473bc8190fbc1d47fe52bd'
assert native['kernel_exit'] == 0 and native['module_count'] == 12 and native['declaration_count'] == 54
assert native['all_actual_types_and_bodies_closed'] and native['standard_axioms_only']
assert assessment['disposition'] == 'NATIVE_PASS_READER_FAIL' and assessment['browser_actual_exit'] == 1
assert assessment['four_contexts_completed'] and assessment['source_download_checks_completed'] == 8
assert assessment['blocker']['wrapper_overflowX'] == 'visible' and assessment['blocker']['wrapper_scrollLeft_after_set100'] == 0
for d,raw in plans.items():
    if d.exists():assert d.read_bytes() == raw
    else:create(d,raw)
extra = E/'native-review/variance_native_61d0/original-wrapper-retrieval.original.json'
create(extra,retrieval.read_bytes())
cell = json.loads(C.read_bytes())
assert cell['status'] == 'proved_locally'
cell['evidence']['independent_native_reader'] = {
    'assessor':'/root/variance_native_61d0', 'disposition':'NATIVE_PASS_READER_FAIL',
    'math_compiled_commit':native['actual_math_compiled_commit'],'reader_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae',
    'ROOT_operation_commit':head,'native_stage_seal_sha256':'8fcdfb3cfe37033dd30acebdb3e098a3b55970f6b9b6a60ac3a53fdc66f4c3ef',
    'original_result_seal':str(D/'SEAL.json'),'original_result_seal_sha256':sha((R/'SEAL.json').read_bytes()),
    'report':str(D/'REPORT.md'),'report_sha256':sha((R/'REPORT.md').read_bytes()),
    'native_summary':str(D/'native-summary.json'),'native_summary_sha256':sha((R/'native-summary.json').read_bytes()),
    'reader_assessment':str(D/'reader-assessment.json'),'reader_assessment_sha256':sha((R/'reader-assessment.json').read_bytes()),
    'portable_manifest':str(D/mp.name),'portable_manifest_sha256':sha(mp.read_bytes()),
    'reader_failure':assessment['blocker'],'unapplied_production_repair':assessment['repair'],
    'scope':'Native mathematical verification is separate from failed original mobile delivery. ROOT operated unchanged independently authored browser checkers only. No website/integration/publication/purification/wholeGoal credit.',
}
cell['reader_contract']['status'] = 'Independent mathematical whole-code/source/seven-slot review accepted and native12module/54body kernel checks passed. Actual desktop1440 and mobile390 four contexts/source8 downloads executed: original focused mobile publication table crops with no horizontal scroll. Reader delivery FAIL remains open; exact unapplied shared CSS repair is preserved. No conditional prototype is original production acceptance.'
cell['purification']['dead_code_audit'] = 'Independent54 complete type/body kernel checks; publicP2 owned and privateT5 owned allrootreachable;7 old imported generated leaves unused in the joint root union are retained explicitly. No new wrapper/axiom/placeholder closures.'
cell['learning_contract']['reader_backpressure']['purification_status'] = 'pending'
cell['learning_contract']['reader_backpressure']['exposition_seal_status'] = 'pending'
cell['learning_contract']['reader_backpressure']['exposition_evidence'] = 'Original focused mobile publication layout FAIL; see independent_native_reader. Exact source/Lean mathematical assumptions preserved, but human-facing visual delivery is not accepted.'
C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
record = {'kind':'Original independent native mathematical PASS and physical reader FAIL carried unchanged',
    'metadata_parent':head,'actual_math_commit':native['actual_math_compiled_commit'],
    'reader_commit':'1d0dedf3aac3c2ff72ee96566461e29e38a2eeae','disposition':assessment['disposition'],
    'portable_original_files':len(manifest['files']),'portable_original_bytes':sum(x['bytes'] for x in manifest['files']),
    'all_originals_and_postseal_destinations':len(plans),'source_wrapper_relocation':relocation_uses,
    'large_proofdump_and_oleans_local_only':True,'local_only_inventory':manifest['excluded_local_only'],
    'new_normalAPI_calls':0,'root_VERIFIED_calls':0,'original_production_CSS_changed':False,
    'actual_mobile_reader_PASS':False,'conditional_prototype_integrated_or_published':False,
    'remaining_action':'Keep original owner release choice. Minimal reviewed productionCSS proposal requires serialized application and actual final acceptance; mathematical normalV admissibility is independently assessed, never ROOT self-granted.'}
rp = E/'actual-independent-native-PASS-reader-FAIL-attachment.json'; create(rp,dump(record))
assert Path('runs/substantive_advances.jsonl').read_bytes() == before
assert Path('runs/substantive_discoveries.jsonl').read_bytes() == discovery
for p,h in b['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes()) == h,p
paths = [C,rp,extra,*plans]
assert set(git('diff','HEAD','--name-only').decode().splitlines()) == {str(C)}
spec = W/'native-original-PASS-reader-FAIL-paths.private.nul'; create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines()) == set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Carry independent variance native pass and real mobile reader failure'],check=True)
commit = git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}') == p.read_bytes()
assert not git('diff','HEAD','--name-only')
result = {k:record[k] for k in ['metadata_parent','actual_math_commit','reader_commit','disposition','portable_original_files','portable_original_bytes','all_originals_and_postseal_destinations','new_normalAPI_calls','root_VERIFIED_calls']}
result.update({'native_metadata_commit':commit,'changed_carried_files':len(paths)})
create(W/'actual-native-PASS-reader-FAIL-commit.json',dump(result))
print(json.dumps(result))
