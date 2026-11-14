from pathlib import Path
import subprocess,os,json,hashlib
r=Path.cwd();w=r/'.astis/huanjian-gc-matrix-laplace-20261114'
base='4a746323019221910dd91b3e0039fe3345ae8d2b'
ref='refs/heads/huanjian/gaussian-progress-public-20261114'
def git(*args,inp=None,env=None):
    return subprocess.check_output(['git',*args],cwd=r,input=inp,env=env)
assert git('rev-parse',ref).decode().strip()==base
source=git('rev-parse','HEAD').decode().strip()
assert source.startswith('b36275452')
e='research-wiki/technical-lemmas/matrix-laplace-tail-semantic-evidence/'
paths=['AutoSamplingTheory/TechnicalLemmas/Probability/MatrixLaplaceTail.lean',
       'Tests/GaussianComplexityLaplaceTail.lean',e+'local-mathematics-checkpoint.v1.json']
stems=['20261114T121038198059Z-matrix-laplace-P-explicit-finite-spectral-sum-proof',
       '20261114T121225753642Z-matrix-laplace-P-production-AE-strong-measurability-import',
       '20261114T121442230413Z-matrix-laplace-T-confirmed-global-selfadjoint-sum-API']
for stem in stems:
    paths.extend([e+'local-math-originals/'+stem+x for x in ['.log','.receipt.json']])
assert len(paths)==9
rows=[]
for p in paths:
    raw=git('ls-tree',source,'--',p).decode().strip()
    mode,kind,rest=raw.split(' ',2);oid,actual=rest.split('\t')
    assert kind=='blob' and actual==p
    assert git('show',source+':'+p)==(r/p).read_bytes()
    rows.append({'path':p,'mode':mode,'oid':oid,'sha256':hashlib.sha256((r/p).read_bytes()).hexdigest()})
notes=['docs/gaussian-public-export/README.md','docs/gaussian-public-export/provenance.json']
readme=git('show',base+':'+notes[0]).decode()
readme+='''
## Matrix Laplace-tail local mathematics — 2026-11-14

This bounded increment adds the real largest-eigenvalue Laplace-tail theorem
and its private consumer for all four signed ordinary/cosine Gaussian sums.
The generic expectation is explicitly a nonnegative extended scalar integral;
the actual Gaussian application derives finite trace-exponential Bochner
integrability inside its proof. It adds no integrability premise, matrix-MGF
product rule, Bernstein theorem or full-paper conclusion.

The exact two proof files were frozen at local mathematical commit
`1d1103af694b9663a72b0d610004ed85c7c6b527`. The actual ROOT Lean check streams,
receipts and source hashes are retained here. Their recorded build HEADs and
file hashes are the evidence; no build of this new public export identity is
claimed. This snapshot publishes compiled local mathematical progress only.
Independent source/reader acceptance and normal PROVED_LOCAL/VERIFIED admission
for this new Laplace packet are not claimed by this increment. Existing R14
verification and old public ledger bytes remain unchanged.

Full independent-sum/Lieb/master-tail/Bernstein, C6/Lemma4.4, both main lower
bounds, oracle/TV/precision/query-cap/expected-cost adaptation, main/site
integration, purification and whole-Goal completion remain unfinished.
'''
prov=json.loads(git('show',base+':'+notes[1]))
old=prov.get('latest_incremental_progress')
hist=prov.setdefault('incremental_progress_history',[])
if old is not None and old not in hist:hist.append(old)
record={'kind':'matrix-laplace-tail-compiled-local-mathematical-progress-only',
 'previous_public_commit':base,'local_source_commit':source,
 'mathematical_commit':'1d1103af694b9663a72b0d610004ed85c7c6b527',
 'owned_exact_path_mode_oid_delta':rows,
 'canonical_ledgers':'Both byte-identical to previous public commit; no new admission/V record asserted in this increment.',
 'truth_boundary':'Compiled local P+private four-family T only; independent source/reader/normal PL/V not claimed; no new public T node; no main/site/purification/full-paper conclusion.',
 'source_history_not_parent':True,'old_omissions_and_projections_unchanged':True}
prov['latest_incremental_progress']=record
payloads={notes[0]:readme.encode(),notes[1]:(json.dumps(prov,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()}
idx=w/'public-math-progress.index.private'
assert not idx.exists()
env=dict(os.environ,GIT_INDEX_FILE=str(idx),GIT_OPTIONAL_LOCKS='0')
beforehead=git('rev-parse','HEAD')
indexpath=Path(git('rev-parse','--git-path','index').decode().strip())
if not indexpath.is_absolute():indexpath=r/indexpath
indexbefore=hashlib.sha256(indexpath.read_bytes()).hexdigest()
git('read-tree',base,env=env)
lines=[f"{x['mode']} {x['oid']}\t{x['path']}\n" for x in rows]
for p,b in payloads.items():
    oid=git('hash-object','-w','--stdin',inp=b).decode().strip()
    lines.append(f'100644 {oid}\t{p}\n')
git('update-index','--index-info',inp=''.join(lines).encode(),env=env)
tree=git('write-tree',env=env).decode().strip()
public=git('commit-tree',tree,'-p',base,inp=b'Publish compiled real matrix Laplace-tail progress for review\n').decode().strip()
changed=git('diff-tree','--no-commit-id','--name-only','-r',base,public).decode().splitlines()
assert set(changed)==set(paths+notes)
assert git('rev-parse','HEAD')==beforehead
assert hashlib.sha256(indexpath.read_bytes()).hexdigest()==indexbefore
for p in ['runs/substantive_advances.jsonl','runs/substantive_discoveries.jsonl']:
    assert git('rev-parse',base+':'+p)==git('rev-parse',public+':'+p)
parents=git('rev-list','--parents','-n','1',public).decode().split()[1:]
assert parents==[base]
report={'public_commit':public,'tree':tree,'sole_safe_parent':base,'local_source_commit':source,
 'ref':ref,'owned_exact_files':rows,'only_two_other_paths':notes,
 'both_public_ledgers_unchanged':True,'original_HEAD_and_index_unchanged':True,
 'no_ref_update_or_push':True,'status':'CANDIDATE_READY_FOR_INDEPENDENT_PRIVACY_REVIEW_NOT_YET_PUSHED'}
(w/'prepared-public-math-progress.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['owned_exact_files']},ensure_ascii=False))
