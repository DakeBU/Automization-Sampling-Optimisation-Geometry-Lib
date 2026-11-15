"""Prepare only an unreferenced incremental commit on the existing safe lineage."""
from pathlib import Path
import subprocess,os,json,hashlib,datetime
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
parent='3be3742810b87db7d9d8fac485427e97209c5f41'
sourcebase='3fdf32b93a1fcfc9740cec4f1e3460fd201e538c'
ref='refs/heads/huanjian/gaussian-progress-public-20261114'
advance='ASTIS-SA-20261114-MatrixLaplaceTail'
E='research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/'
readonly_env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
def git(*args,inp=None,env=None):return subprocess.check_output(['git',*args],cwd=r,input=inp,env=readonly_env if env is None else env)
def sha(b):return hashlib.sha256(b).hexdigest()
source=git('rev-parse','HEAD').decode().strip()
index=Path(git('rev-parse','--git-path','index').decode().strip())
if not index.is_absolute():index=r/index
indexhash=sha(index.read_bytes())
assert source!=sourcebase and not git('status','--porcelain','--untracked-files=no').strip()
assert git('rev-parse',ref).decode().strip()==parent
outpath=w/'prepared-public-V-progress.json';assert not outpath.exists()
allowed={'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-LAPLACE-TAIL.json','runs/substantive_advances.jsonl'}
raw=git('diff','--raw','--no-abbrev','--no-renames','-z',sourcebase,source).split(b'\0')
assert raw[-1]==b'';raw=raw[:-1];assert len(raw)%2==0
rows=[]
for i in range(0,len(raw),2):
    oldmode,newmode,oldoid,newoid,status=raw[i].decode().removeprefix(':').split()
    path=raw[i+1].decode();assert status in ['A','M','D']
    assert path in allowed or path.startswith(E),path
    oldpublic=git('ls-tree',parent,'--',path).decode().strip()
    if oldmode=='000000':assert not oldpublic,path
    else:assert oldpublic==f'{oldmode} blob {oldoid}\t{path}',path
    rows.append({'path':path,'old_mode':oldmode,'old_oid':oldoid,'mode':newmode,'oid':newoid,'status':status})
old=git('show',parent+':runs/substantive_advances.jsonl');new=git('show',source+':runs/substantive_advances.jsonl')
assert new.startswith(old)
events=[json.loads(v) for v in new[len(old):].splitlines()]
assert len(events)==1 and events[0]['advance_id']==advance
assert events[0]['event']=='transition' and events[0]['schema_version']==4
assert events[0]['from_state']=='PROVED_LOCAL' and events[0]['to_state']=='VERIFIED'
v=events[0]['evidence'];assert v['verifier_id']==events[0]['worker_id']
assert v['verifier_id']!='huanjian_20261114_matrix_laplace_tail'
pl_bytes=git('show',parent+':'+E+'PROVED_LOCAL-evidence.full.json')
assert git('show',source+':'+E+'PROVED_LOCAL-evidence.full.json')==pl_bytes
assert git('show',source+':'+E+'actual-PROVED_LOCAL-append.exact.jsonl')==git('show',parent+':'+E+'actual-PROVED_LOCAL-append.exact.jsonl')
pl=json.loads(pl_bytes)
old_pl=[json.loads(row)['evidence'] for row in old.splitlines() if json.loads(row).get('advance_id')==advance and json.loads(row).get('to_state')=='PROVED_LOCAL']
assert len(old_pl)==1 and old_pl[0]==pl
assert len(pl)==24 and all(v[k]==value for k,value in pl.items())
assert git('show',source+':runs/substantive_discoveries.jsonl')==git('show',parent+':runs/substantive_discoveries.jsonl')
for p in ['AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean',
 'Tests/GaussianComplexityLaplaceTail.lean',
 'website/content/declaration_lessons/huanjian-matrix-laplace-tail.json',
 'website/content/publications/huanjian-matrix-laplace-tail.json',
 'research-wiki/semantic-roundtrip/audits/huanjian-matrix-laplace-tail.json']:
    assert git('show',source+':'+p)==git('show',parent+':'+p),p
# No accepted wording can be emitted before a separately reviewed, real closeout
# contract is present. This file is a selector, never substitute process evidence.
contract=json.loads((w/'public-V-actual-acceptance-input.v1.json').read_text())
assert contract['actual_source_commit']==source
assert contract['actual_verified_carrier']==v['verified_commit']
assert contract['status']=='ACTUAL_V_AND_BOUNDED_READER_ACCEPTED'
assert len(contract['artifacts'])>=3
actual_artifacts={}
for name,record in contract['artifacts'].items():
    path=record['file'];assert path.startswith(E) and '..' not in Path(path).parts
    data=git('show',source+':'+path)
    assert len(data)==record['bytes'] and sha(data)==record['sha256']
    actual_artifacts[name]=json.loads(data)
reader=actual_artifacts['current_reader_acceptance']
assert reader['status']=='ACCEPTED_BOUNDED_ISOLATED_READER_WITH_PRESERVED_PARENT_CLIP_CORRECTION'
assert reader['new_v4_browser_run'] is False and reader['parent_clip_correction_independently_accepted'] is True
assert reader['actual_targeted_supplement']['actual_exit_code']==1
assert reader['actual_targeted_supplement']['raw_false_checks']==2
assert reader['actual_targeted_supplement']['original_contract_all_PASS'] is False
assert reader['independent_corrective_review']['necessary_reader_residual']==0
assert reader['optional_v3']['execution'] is False
normal=actual_artifacts['normal_V_public_outcome']
assert normal['advance_id']==advance and normal['verified_commit']==v['verified_commit']
assert normal['verifier_id']==v['verifier_id'] and normal['normal_API_calls']==1 and normal['actual_exit_code']==0
assert normal['original24_top_level_fields_unchanged'] is True
assert normal['exact_appended_record_sha256']==sha(new[len(old):])
assert contract['independent_original_process_custody_checked'] is True
notes=['docs/gaussian-public-export/README.md','docs/gaussian-public-export/provenance.json']
readme=git('show',parent+':'+notes[0]).decode()+'''

## Matrix Laplace-tail independent verification and isolated reader — 2026-11-15

An independent non-proving verifier recorded exactly one normal VERIFIED for
the real matrix Laplace-tail theorem. All24 original PROVED_LOCAL evidence fields,
including their historical pending-reader snapshot, remain inline unchanged.
Separate current evidence records the real browser run and independent visual
review. Mathematical P/T, lesson, publication and semantic audit bytes retain
their previous exact identities. The actual Lean/native build belongs to the
recorded immutable mathematical source1d110, rather than a later metadata or
public-export commit identity.

The original actual-v3 run reported398 checks with0 false checks. Independent
visual review found that two parent SVG zoom-pan screenshots had nodes outside
the SVG clip; the font-size assertion was insufficient. Those raw results and
PNGs remain unchanged. A separate targeted actual-browser supplement produced
four complete parent viewport states. Its raw process retains exit1 and2false
completion checks: desktop crops selected the wrong region and mobile crops
failed before later repeated actions. Independent review excludes the wrong
crops, verifies the four complete viewport states and combines them with the
unchanged previously accepted source/detail/navigation observations. Necessary
bounded-reader residual is0; the failed supplemental contract is never relabelled
PASS. A further optional crop repeat was cancelled before execution. Exactv4
served bytes equalv3; no browser-v4 run is invented.

Formulas, initially folded statement/proof/code, six expanded proof steps,
source anchors, full source/copy/download, source-index and bounded graph/detail
navigation have bounded isolated-reader acceptance. Default graph-fit labels
remain small; zoomed long SVG labels may be ellipsized or extend beyond a mobile
viewport, so full identifiers use the detail inspector. Responsive viewport
checks are not physical-touch, production-site or post-V-status-pixel acceptance.

The original two stabilization owners on observed main9448 remain held. Shared
main/Registry/global graph/production-site integration, post-merge purification,
full independent-sum/Lieb/master-tail/Bernstein and C6/Lemma4.4, both main lower
bounds, and actual oracle/TV/precision/deterministic-query-cap/expected-cost
adaptation and whole-Goal acceptance remain unfinished.
'''
prov=json.loads(git('show',parent+':'+notes[1]))
prov.setdefault('incremental_progress_history',[]).append(prov['latest_incremental_progress'])
prov['latest_incremental_progress']={
 'kind':'matrix-laplace-tail-one-independent-normal-VERIFIED-and-isolated-reader',
 'previous_public_commit':parent,'local_source_commit':source,'source_delta_base':sourcebase,
 'mathematical_commit':'1d1103af694b9663a72b0d610004ed85c7c6b527',
 'original_checked_metadata_commit':'3eeda6aa3447c056b349d1507c6d761e4366efb3',
 'independent_verified_carrier':v['verified_commit'],'independent_verifier_id':v['verifier_id'],
 'owned_exact_path_mode_oid_delta':rows,'normal_V_events_in_this_increment':1,
 'canonical_ledger_policy':'Old public advance bytes exact prefix; only one actual target VERIFIED suffix. Discovery Ledger unchanged.',
 'historical_PL_contract':'All24 original fields inline unchanged; current reader acceptance in separate additional V fields.',
 'original_raw_browser_gap_and_targeted_correction_preserved':True,
 'build_identity_boundary':'Original actual Lean/native immutable-source identity only; no new build claimed for carrier or public export.',
 'source_history_not_parent':True,'old_omissions_and_projections_unchanged':True,
 'truth_boundary':'Independent local verification and isolated reader only; no shared main/site/purification/full-paper completion.',
 'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
payloads={notes[0]:readme.encode(),notes[1]:(json.dumps(prov,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()}
idx=w/'public-V-progress.index.private';assert not idx.exists()
env=dict(os.environ,GIT_INDEX_FILE=str(idx),GIT_OPTIONAL_LOCKS='0')
git('read-tree',parent,env=env)
lines=[f"{row['mode'] if row['mode']!='000000' else '0'} {row['oid']}\t{row['path']}\n" for row in rows]
for path,b in payloads.items():
    oid=git('hash-object','-w','--stdin',inp=b).decode().strip();lines.append(f'100644 {oid}\t{path}\n')
git('update-index','--index-info',inp=''.join(lines).encode(),env=env)
tree=git('write-tree',env=env).decode().strip()
public=git('commit-tree',tree,'-p',parent,inp=b'Publish independently verified matrix Laplace-tail progress\n').decode().strip()
assert git('rev-list','--parents','-n','1',public).decode().split()[1:]==[parent]
changed=git('diff-tree','--no-commit-id','--name-only','-r',parent,public).decode().splitlines()
assert set(changed)=={row['path'] for row in rows}|set(notes)
assert git('rev-parse','HEAD').decode().strip()==source and sha(index.read_bytes())==indexhash
out={'status':'CANDIDATE_ONLY_PENDING_INDEPENDENT_PRIVACY_REVIEW','public_commit':public,'tree':tree,
 'sole_safe_parent':parent,'local_source_commit':source,'source_delta_base':sourcebase,'ref':ref,
 'owned_exact_delta':rows,'only_two_other_paths':notes,'ROOT_HEAD_and_index_unchanged':True,
 'no_ref_update_or_push':True,'actual_V_carrier':v['verified_commit']}
outpath.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:value for k,value in out.items() if k!='owned_exact_delta'}))
