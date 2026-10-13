from pathlib import Path
import json,hashlib,gzip,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;D=O.parent
COMMIT='dc968dfea08e325a14f602d7d942f145cf4c069f'
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_bytes())
def rel(p):return Path(p).relative_to(R).as_posix()
def info(p):return dict(path=rel(p),raw_sha256=sha(Path(p).read_bytes()),bytes=Path(p).stat().st_size)
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def blob(p):return git('show',COMMIT+':'+p)
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert git('rev-parse','HEAD').decode().strip()==COMMIT
review=load(D/'independent-review/merge-resolution-review104.native.json');prior=load(D/'premerge.json');storage=load(D/'merge-storage-map.json')
parents=git('show','-s','--format=%P',COMMIT).decode().split();assert parents==[review['checked_parents']['ours'],review['checked_parents']['upstream']]
assert len(review['staged_files'])==34
for x in review['staged_files']:assert sha(blob(x['path']))==x['index_sha256'],x['path']
changed=set(git('diff','--name-only',parents[0],COMMIT).decode().splitlines());extras=changed-{x['path'] for x in review['staged_files']}
expected=set(storage['added_evidence_only'])|{rel(D/'merge-storage-map.json')};assert extras==expected
allowed103='runs/20261007-companion-priority/pbps-actual-phase-normalization103/integration103/'
assert all(p.startswith(rel(D)+'/') or (p.startswith(allowed103) and Path(p).name.startswith(('postpush-binding103','push103.stdout','push103.stderr'))) for p in extras)
assert not any('Header104' in p or '/independent-header-' in p for p in extras)
mapping={x['raw_path']:x for x in storage['archives']}
for x in storage['archives']:
 z=blob(x['archive']);assert sha(z)==x['archive_raw_sha256'];raw=gzip.decompress(z);assert sha(raw)==x['raw_sha256'];assert (R/x['raw_path']).read_bytes()==raw
 if x['public_text_sha256'] is not None:assert sha(blob(x['raw_path']))==x['public_text_sha256']
resolved=[]
def resolve(row):
 p=row['path'];h=row['raw_sha256'];assert sha((R/p).read_bytes())==h,p
 if p in mapping:
  x=mapping[p];b=gzip.decompress(blob(x['archive']));method=x['archive']
 else:
  b=blob(p);method='exact committed blob'
 assert sha(b)==h,p
 if 'bytes' in row:assert len(b)==row['bytes']
 resolved.append(dict(original=row,storage=method))
closure=load(D/'independent-review/closed-RAW-review104.native.json')
for row in closure['inputs']+closure['artifacts']:resolve(row)
resolve(info(D/'independent-review/closed-RAW-review104.native.json'))
for row in prior['dirty_raw']:assert sha((R/row['path']).read_bytes())==row['raw_sha256']
assert len(prior['dirty_raw'])==47
for row in review['preserved_collaborator_inputs']:assert sha((R/row['path']).read_bytes())==row['raw_sha256']
assert len(review['preserved_collaborator_inputs'])==21
labels=['tests','astis','canonical','publication','contributor','semantic','frontier','process-memory','python-compile','site-build','site-check','graph-after-site','site-regressions','harness','diff-check','curve-graph']
gates=[]
for label in labels:
 p=D/'checks'/('integration-'+label)/'receipt.json';c=load(p);assert c['terminal_closed'] and c['exit_code']==0;resolve(info(p));gates.append(info(p))
reader=load(D/'pbps-reader-after-merge.json');resolve(info(D/'pbps-reader-after-merge.json'))
assert reader['status']=='PASS_GENERATED_CONTENT_ONLY' and reader['exact_step_Lean_regions']==7 and reader['details_initially_folded']==13
assert sha((R/reader['page']).read_bytes())==reader['page_raw_sha256'];assert sha((R/reader['Lean_download']).read_bytes())==reader['Lean_download_raw_sha256']
pbps='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseNormalization.lean';assert blob(pbps)==git('show',parents[0]+':'+pbps)
assert not any('pbps-actual-phase-normalization103' in p and not p.startswith(allowed103) for p in changed)
assert not any(p.startswith('runs/semantic-roundtrip/anonymous103/') for p in changed)
save('exact-commit-transfer104.native.json',{'decision':'ACCEPT_BOUNDED_EXACT_COMMIT_TRANSFER','reviewer':'/root/exact_verifier96','checked_commit':COMMIT,'parents':parents,'reused_merge_review':info(D/'independent-review/merge-resolution-review104.native.json'),'reused_closed_review':info(D/'independent-review/closed-RAW-review104.native.json'),'storage_map':info(D/'merge-storage-map.json'),'all34_reviewed_index_blobs_equal_commit':True,'added_evidence_paths':sorted(extras),'lossless_archive_count':len(mapping),'closed_native_resolutions':resolved,'all47_dirty_RAWs_unchanged':True,'preserved_collaborator_inputs':review['preserved_collaborator_inputs'],'all16_terminal_PASS_receipts':gates,'reader_snapshot':info(D/'pbps-reader-after-merge.json'),'reader_page_and_download_RAW_unchanged':True,'PBPS103_proof_source_decoder_unchanged':True,'sole94_lane_and103_VERIFIED':'Reused accepted ledger review; exact reviewed ledger index equals this commit.','prospective104_header_or_proof_in_commit':False,'tests_rerun':False,'shared_mutations':False,'SAU_transitions':False,'boundaries':['Local merge commit checked; push not asserted.','Incoming main merged into working branch; PBPS merged to main not asserted.','Browser visual acceptance and purification remain separate pending boundaries.']})
save('closed-RAW-transfer104.native.json',{'checked_commit':COMMIT,'inputs':[info(D/'merge-storage-map.json'),info(D/'merge-commit.json'),info(D/'independent-review/closed-RAW-review104.native.json'),info(D/'pbps-reader-after-merge.json')],'outputs':[info(p) for p in sorted(O.iterdir()) if p.is_file()],'native_original_RAW_resolved':True,'proof_replayed':False})
print(info(O/'exact-commit-transfer104.native.json'));print(info(O/'closed-RAW-transfer104.native.json'))
