"""Carry bounded independent native/browser originals without inventing a V event."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode = True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontier
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json')
R = Path('.astis/semantic-neutral-20261113/psd_native_7b31')
D = E/'native-review/psd_native_7b31/originals'
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj: (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git = lambda *args: subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as out:
        out.write(raw)

head=git('rev-parse','HEAD').decode().strip()
assert head=='9687ebe5bd3691c5b4b45125fb6ce428822ea092'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
ledger=Path('runs/substantive_advances.jsonl').read_bytes()
discoveries=Path('runs/substantive_discoveries.jsonl').read_bytes()
b=json.loads((W/'candidate-boundary-v3.private.json').read_bytes())
states=advance._replay_advances([json.loads(x) for x in ledger.splitlines()])
assert states.pop('ASTIS-SA-20261112-RealMatrixPositiveIntegral')['state']=='PROVED_LOCAL'
assert states==b['all_foreign_states']
for p,h in b['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes())==h,p
expected={
    'REPORT.md':'8e340cdb2750afe1bf99841f00716b5f2a1eabb947de8139a6c8e8306ee1a6ed',
    'originals-manifest.json':'8926380d0bda0ee4c92585779af1463b46afe925729f4bcca7bc543c47eff7ac',
    'seal.json':'03dfe1607d2f63743999d17087070253fc05df0a5dafa48161d6974e812e8585',
    'portable-originals-manifest.json':'809cee7055abafd06d8d7c020c3e1eb18e5a5b85314823834a2728d653865c3e',
}
for name,h in expected.items():
    assert sha((R/name).read_bytes())==h,name
seal=json.loads((R/'seal.json').read_bytes())
assert seal['native_result']==seal['bounded_reader_result']=='PASS'
assert seal['normalV_authorized'] is False and seal['full_R9_T_credit'] is False
summary=json.loads((R/'native-summary.json').read_bytes())
assert summary['candidate_commit']=='9964c33c4599f85d27dc8687e8bd6fdb5c44ff49'
assert summary['empty_initial_ASTIS_outputs'] and summary['all_nine_modules_compiled']
assert summary['closure_declarations']==46
assert summary['all_declaration_types_and_bodies_closed_and_kernel_checked']
assert summary['new_SP_handwritten']==summary['new_SP_generated']==2
assert summary['new_SP_unreachable']==[]
assert len(summary['literal_actual_root_proof_value_applications'])==4
for item in summary['source_fake_closure_scan']:
    p=Path(item['module'].replace('.','/')+'.lean')
    assert sha(p.read_bytes())==item['sha256'] and item['forbidden_tokens']==[]
    assert git('show',f"{summary['candidate_commit']}:{p}")==p.read_bytes()
browser=json.loads((R/'browser-report.json').read_bytes())
assert len(browser)==8
for item in browser:
    assert item['exact_statement_and_full_proof_match'] and item['assumptions_preserved']
    assert item['MathJax_errors']==0 and not item['document_overflow_initial']
    assert item['expanded_document_width']['width']==item['expanded_document_width']['scrollWidth']
    assert item['page_errors']==item['failed_HTTP_responses']==item['assets_HTTP_failures']==[]
manifest_raw=(R/'portable-originals-manifest.json').read_bytes()
manifest=json.loads(manifest_raw)
assert len(manifest['entries'])==1548 and manifest['local_only_dumps_exported'] is False
files=[]
for item in manifest['entries']:
    p,dest=Path(item['source']),Path(item['destination'])
    assert p.resolve().is_relative_to(R.resolve()) and not p.is_symlink()
    assert dest.is_relative_to(D) and not dest.is_absolute() and '..' not in dest.parts
    assert 'dump.gz' not in str(p) and p.suffix not in ['.olean','.ilean','.pyc']
    raw=p.read_bytes()
    assert len(raw)==item['bytes'] and sha(raw)==item['sha256'],str(p)
    files.append((dest,raw))
files.append((D/'portable-originals-manifest.json',manifest_raw))
receipt_name='20261112T155841281352Z-freeze-native-reader-originals'
receipt_path=R/'receipts'/(receipt_name+'.json')
receipt=json.loads(receipt_path.read_bytes())
assert receipt['exit']==0
for key in ['stdout','stderr']:
    p=receipt_path.parent/receipt[key+'_file']
    assert sha(p.read_bytes())==receipt[key+'_sha256']
for suffix in ['.json','.stdout','.stderr']:
    p=R/'receipts'/(receipt_name+suffix)
    files.append((D/'post-seal-envelope'/p.name,p.read_bytes()))
assert len({str(p) for p,_ in files})==len(files)
for p,raw in files:
    create(p,raw)
cell=json.loads(C.read_bytes())
assert cell['status']=='proved_locally' and cell['evidence']['independent_verification']==''
cell['evidence']['independent_native_reader']={
    'verifier':'/root/psd_native_7b31','mathematical_candidate':summary['candidate_commit'],
    'report':str(D/'REPORT.md'),'report_sha256':expected['REPORT.md'],
    'seal':str(D/'seal.json'),'seal_sha256':expected['seal.json'],
    'portable_originals_manifest':str(D/'portable-originals-manifest.json'),
    'portable_manifest_sha256':expected['portable-originals-manifest.json'],
    'original_file_count':len(manifest['entries']),
    'bootstrap_archival_qualification':seal['archival_completeness'],
    'native_closure':'9 modules and46 actual full types/bodies, closed/kernel checked, standard axioms only;4 new S/P declarations reachable;4 literal proof-value applications.',
    'reader':'Production canonical shell and exact CSS import closure;4 pages at1440/390, actual Chrome/MathJax/exactfolds/source/download/visual passed.',
    'boundary':'Bounded fixed-candidate native/reader only; no source verdict, normalV, fullR9/T, globalgraph/fullsite/integration/purification or Goal completion.'}
cell['reader_contract']['status']='Independent S/P source review and bounded production reader accepted:4 pages on desktop/mobile, exact folded Lean, MathJax, assumptions/steps/source/download/visual checked. Full public website/source-index/graph integration awaits original stabilization owner; purification remains pending.'
cell['purification']['dead_code_audit']='Independent native checked all46 declarations in9-module closure and complete types/bodies. All4 new S/P declarations are root-reachable;7 older imported GridAlias-generated declarations outside the root union remain historical substrate, not new unused proof. No global purification claim.'
C.write_bytes(dump(cell))
assert not frontier.validate_cells(frontier.load_cells())
record={'mathematical_candidate':summary['candidate_commit'], 'native_report_sha256':expected['REPORT.md'],
    'native_seal_sha256':expected['seal.json'],'portable_manifest_sha256':expected['portable-originals-manifest.json'],
    'portable_originals':len(manifest['entries']),'copied_originals_including_manifest_and_postseal_envelope':len(files),
    'bootstrap_archival_qualification':seal['archival_completeness'],
    'root_VERIFIED_calls':0,'source_and_native_actors_distinct':True,
    'originals_not_rewritten':True,'large_dump_exported':False}
record_path=E/'actual-independent-native-reader-attachment.json'
create(record_path,dump(record))
assert Path('runs/substantive_advances.jsonl').read_bytes()==ledger
assert Path('runs/substantive_discoveries.jsonl').read_bytes()==discoveries
for p,h in b['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes())==h,p
paths=[C,record_path,*[p for p,_ in files]]
pathspec=W/'native-commit-paths.private.nul'
create(pathspec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(pathspec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(record_path)],check=True)
subprocess.run(['git','commit','-m','Carry independent PSD native closure and desktop mobile reader evidence','--quiet'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:
    assert git('show',f'{commit}:{p}')==p.read_bytes()
assert not git('diff','HEAD','--name-only')
result={**record,'native_review_metadata_commit':commit,'parent':head,'exact_carried_files':len(paths)}
create(W/'actual-independent-native-review-commit.json',dump(result))
print(json.dumps(result))
