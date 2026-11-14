"""Preserve failed admission originals and restore the consumer's own canonical target."""
from pathlib import Path
import hashlib
import json
import subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
E22=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
R=Path('.astis/semantic-neutral-20261113/psd_native_7b31/held-gates')
D=E/'native-review/psd_native_7b31/held-gates'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
head=git('rev-parse','HEAD').decode().strip()
assert head=='7d6d61f298e882f54c4bc36b1fb67502d2801e77'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
ledger=Path('runs/substantive_advances.jsonl').read_bytes()
discovery=Path('runs/substantive_discoveries.jsonl').read_bytes()
expected={
    'REPORT.md':'cb0dae443f5672c36e2853f111f8b87eb91c807fbf0c9aa09373ae44b54e6920',
    'originals-manifest.json':'596217c96d193a45c601264505f40c7e7e4a86380b346ab913a69e8e07085cb2',
    'seal.json':'676e7ebdf582a7a87321937450dbd94dce7e3ccdfb161d9e2d48a4a8f1404320',
    'portable-originals-manifest.json':'083d257ac7b3c10ab5b96bcf2cf1a90204975d7463cf112d897502d829a85662'}
for n,h in expected.items():assert sha((R/n).read_bytes())==h,n
manifest=json.loads((R/'portable-originals-manifest.json').read_bytes())
assert len(manifest['entries'])==167
files=[]
for item in manifest['entries']:
    p,dest=Path(item['source']),Path(item['destination'])
    assert p.resolve().is_relative_to(R.resolve()) and not p.is_symlink()
    assert dest.is_relative_to(D) and not dest.is_absolute() and '..' not in dest.parts
    raw=p.read_bytes()
    assert len(raw)==item['bytes'] and sha(raw)==item['sha256']
    files.append((dest,raw))
files.append((D/'portable-originals-manifest.json',(R/'portable-originals-manifest.json').read_bytes()))
for p in sorted((R/'receipts').glob('20261112T160904324244Z-freeze-failed-held-gates-phase.*')):
    files.append((D/'post-seal-envelope'/p.name,p.read_bytes()))
assert len(files)==171
for p,raw in files:create(p,raw)
before=C.read_bytes()
old_path=E22/'active-cell-before-canonical-target-correction.original.json'
create(old_path,before)
cell=json.loads(before)
S='AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef'
P='AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments'
assert cell['shared_floor_audit']['canonical_declaration']==S
assert cell['status']=='claimed' and cell['shared_floor_audit']['decision']=='reuse_existing'
assert S in cell['reuse_plan']['reused_declarations']
cell['shared_floor_audit']['canonical_declaration']=P
after=dump(cell)
check=json.loads(before)
check['shared_floor_audit']['canonical_declaration']=P
assert dump(check)==after
C.write_bytes(after)
diagnosis={
    'failure_class':'IMPLEMENTATION_FAILED',
    'failure_scope':'ROOT active-consumer metadata readback, not mathematical Lean/source failure',
    'actual_failed_gate':'publication --base441d at held7d6d; one actual exit1; remaining3 not run',
    'failed_gate_originals':str(D/'portable-originals-manifest.json'),
    'failed_gate_seal_sha256':expected['seal.json'],
    'precise_cause':'Frontier Cell canonical_declaration is its own publication target P. ROOT incorrectly replaced it with the underlying reused S dependency while updating metadata.',
    'correction':'Restore only /shared_floor_audit/canonical_declaration to exact existing P. Canonical S remains separately referenced once in reuse_plan and its shared cell. Do not claim P as a new shared generic declaration.',
    'path':str(C),'before_sha256':sha(before),'after_sha256':sha(after),
    'before_exact_bytes':str(old_path),'changed_JSON_pointers':['/shared_floor_audit/canonical_declaration'],
    'Lean_source_signature_definition_author_decoder_publication_unchanged':True,
    'R9_status_unchanged':'claimed/EXPLORING','normal_VERIFIED_API_calls':0,
    'next_action':'New held-metadata phase on corrected immutable HEAD; only changed-input publication and the3 previously unexecuted gates. Reuse unchanged independent source/native/browser proofs.'}
record_path=E/'consumer-canonical-binding-failure-and-correction.json'
create(record_path,dump(diagnosis))
b=json.loads((W/'candidate-boundary-v4.private.json').read_bytes())
for p,h in b['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes())==(sha(after) if p==str(C) else h),p
assert b['all_existing_frontier_hashes'][str(C)]==sha(before)
b['all_existing_frontier_hashes'][str(C)]=sha(after)
b['qualification']['v4_boundary_preserved_sha256']=sha((W/'candidate-boundary-v4.private.json').read_bytes())
b['qualification']['canonical_target_metadata_correction']=diagnosis
b['qualification']['only_authorized_active_consumer_cell_delta']['after_sha256']=sha(after)
b['qualification']['only_authorized_active_consumer_cell_delta']['changes']+=' Restore own canonical target P after actual publication metadata rejection; underlying S remains an actual reused dependency.'
create(W/'candidate-boundary-v5.private.json',dump(b))
assert Path('runs/substantive_advances.jsonl').read_bytes()==ledger
assert Path('runs/substantive_discoveries.jsonl').read_bytes()==discovery
paths=[C,old_path,record_path,*[p for p,_ in files]]
spec=W/'canonical-correction-paths.private.nul'
create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C),str(record_path)],check=True)
subprocess.run(['git','commit','--quiet','-m','Preserve failed publication gate and restore actual consumer canonical binding'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
assert not git('diff','HEAD','--name-only')
result={'corrected_metadata_commit':commit,'parent_failed_HEAD':head,
    'changed_canonical_pointer_only':True,'failed_phase_originals':len(files),
    'root_VERIFIED_calls':0,'Lean_or_source_changes':False}
create(W/'actual-canonical-binding-correction-commit.json',dump(result))
print(json.dumps(result))
