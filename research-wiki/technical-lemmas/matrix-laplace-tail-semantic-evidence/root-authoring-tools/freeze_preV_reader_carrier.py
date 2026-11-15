from pathlib import Path
import json,hashlib,subprocess,os
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
E='research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/'
e=r/E;base='3fdf32b93a1fcfc9740cec4f1e3460fd201e538c'
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
def git(*a):return subprocess.check_output(['git',*a],cwd=r,env=env)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cp(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():assert dst.read_bytes()==src.read_bytes()
    else:dst.write_bytes(src.read_bytes())
assert git('rev-parse','HEAD').decode().strip()==base
assert not git('diff','--cached','--name-only','-z')
privacy=w/'metadata-drafts/reader-runtime-public-selection'
reports={
 'reader-review-incremental-privacy-custody.v1.json':'e3e3c898ec86bed37efb24cb5960c83334e50ee5df941235d5e7fa92d10861ef',
 'native-supplement36-selection-privacy-audit.v1.json':'4528f46a35655243d8901dc5a62d1a8b370600d3a7e50ab1b6d61cab5f1a0f9e',
 'native-supplement-public-selection.36.v1.json':'daf4e78248532be8d5f856ad41ba147e0569f6d5a824df29b25b67be40c3146a',
 'READER-INCREMENTAL-PUBLIC-CUSTODY-SUMMARY.v1.json':'2261e130170d67d25e7a0aa567b1cbe77305a889c6c0edef7a49688972456991'}
for name,digest in reports.items():
    src=privacy/name;assert sha(src)==digest;cp(src,e/'metadata-custody/current-reader-privacy'/name)
for name in ['package_reader_356.py','package_reader_visual_v1.py','package_reader_visual_supplement_v2.py','package_native_parent_supplement36.py','prepare_preV_reader_metadata.py','finish_preV_reader_metadata_bindings.py']:
    cp(w/name,e/'root-authoring-tools'/name)
# This original normal-admission payload must never be refreshed to a later state.
pl=E+'PROVED_LOCAL-evidence.full.json'
assert (r/pl).read_bytes()==git('show',base+':'+pl)
assert sha(r/pl)=='da479ae33a80a68835bbb517390a8532760df06054872873c767a5cb65cb198a'
for path in ['runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl',
 'AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean',
 'Tests/GaussianComplexityLaplaceTail.lean',
 'website/content/declaration_lessons/huanjian-matrix-laplace-tail.json',
 'website/content/publications/huanjian-matrix-laplace-tail.json',
 'research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json']:
    assert (r/path).read_bytes()==git('show',base+':'+path),path
cell='research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-LAPLACE-TAIL.json'
paths=set(p.decode() for p in git('diff','--name-only','-z').split(b'\0') if p)
paths|=set(p.decode() for p in git('ls-files','--others','--exclude-standard','-z','--',E).split(b'\0') if p)
assert cell in paths and paths
assert all(p==cell or p.startswith(E) for p in paths),sorted(paths)
assert all((r/p).is_file() and not (r/p).is_symlink() for p in paths)
assert all((r/p).stat().st_size<50_000_000 for p in paths)
for path in sorted(paths):
    assert not any(part in {'chrome-tmp','local-private','private-guards','.atlas-upstream'} for part in Path(path).parts),path
    subprocess.run(['git','add','--',path],cwd=r,env=env,check=True)
staged={p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}
assert staged==paths
subprocess.run(['git','diff','--cached','--check'],cwd=r,env=env,check=True)
rowbytes=git('diff','--cached','--raw','--no-abbrev','-z')
guard={'status':'ACTUAL_OWNED_STAGE_GUARD_PASSED_BEFORE_COMMIT','base':base,
 'owned_paths':sorted(paths),'stage_raw_mode_oid_sha256':hashlib.sha256(rowbytes).hexdigest(),
 'old_ledgers_and_core_source_unchanged':True,'foreign_frontier_paths_staged':0,'normal_V_calls':0,
 'not_a_full_workspace_inventory':True}
(w/'preV-owned-stage-guard.v1.json').write_text(json.dumps(guard,indent=2)+'\n')
# Stop on every prerequisite failure; no exception/fallthrough commit.
subprocess.run(['git','commit','-m','Preserve independently accepted matrix Laplace reader evidence'],cwd=r,env=env,check=True)
commit=git('rev-parse','HEAD').decode().strip();assert commit!=base
assert git('rev-list','--parents','-n','1',commit).decode().split()[1:]==[base]
assert not git('status','--porcelain','--untracked-files=no').strip()
out={'status':'IMMUTABLE_PREV_CARRIER_FROZEN_GATES_PENDING','commit':commit,'parent':base,
 'mathematical_commit':'1d1103af694b9663a72b0d610004ed85c7c6b527',
 'original_checked_metadata_commit':'3eeda6aa3447c056b349d1507c6d761e4366efb3',
 'reader_acceptance':E+'post-PL-current-reader-acceptance.v1.json',
 'reader_acceptance_sha256':sha(e/'post-PL-current-reader-acceptance.v1.json'),
 'stage_guard_sha256':sha(w/'preV-owned-stage-guard.v1.json'),
 'normal_PL_calls':1,'normal_V_calls':0,'cell_status':'proved_locally',
 'source_identity_qualification':'No Lean source changed. Actual Lean/native build identity remains the original immutable math source, not this later reader/metadata carrier.'}
(w/'preV-carrier.v1.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
