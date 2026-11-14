"""Package completed proof/evidence only, preserve open gates, and commit the user pause handoff."""
from pathlib import Path
import gzip,hashlib,json,os,stat,subprocess,tarfile
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
N=Path('.astis/semantic-neutral-20261113/radius_native_5bf8')
S=Path('.astis/semantic-neutral-20261113/radius_src_73c1/normal_v_admissibility_v1')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-radius.json')
L=Path('runs/substantive_advances.jsonl')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip();assert head=='bb04072adab2143e1c656edff93c029df0098e45'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
ledger_before=L.read_bytes();cell=json.loads(C.read_bytes());assert cell['status']=='proved_locally'
assert json.loads(A.read_bytes())['publication_binding_sha256']=='7081c71690e9b29aa32cd09b9e093358d2660a231066384243784fa4654c64fa'
assert not list((N/'receipts').glob('*.pending.json'))
for n,h in [('math-judgment.json','15034ad5253adb449a5b3e52daf9997ce45ae80a49f739a26c6eeb63a21c1042'),('math-freeze-manifest.json','5afca221905cee1be34508dfaec13481a229d1e065bc97239f2a99bbfe0049ea'),('reader/original-browser-freeze.json','fac45815c0c0bd0786bb6f66f1e64fc371ca00a928bb60321e272b4ae77fb40a')]:assert sha((N/n).read_bytes())==h
for name in ['math-freeze-manifest.json','reader/original-browser-freeze.json']:
    for n,h in json.loads((N/name).read_bytes())['files'].items():assert sha((N/n).read_bytes())==h
for p in (N/'receipts').glob('*.json'):
    r=json.loads(p.read_bytes())
    if 'stdout_sha256' in r:
        assert sha(p.with_suffix('.stdout').read_bytes())==r['stdout_sha256']
        assert sha(p.with_suffix('.stderr').read_bytes())==r['stderr_sha256']
orig=json.loads((N/'reader/browser-original/report.json').read_bytes())
cond=json.loads((N/'reader/browser-conditional/report.json').read_bytes())
assert len(orig['layout_failures'])==1 and not cond['layout_failures']
for r in [orig,cond]:
    assert r['server_thread_joined'] and len(r['contexts'])==4 and len(r['source_checks'])==8
    assert not r['page_errors'] and not r['failed_requests'] and not r['http_errors']
globalcss=Path('website/static/proof-readers.css')
assert sha(globalcss.read_bytes())=='4509e56205aa4bb94c3fa32c7b2b0bd98a9b44a71c23e09f18d5affe038512ad'
candidate=json.loads((N/'reader-conditional/candidate.json').read_bytes())
assert candidate['changed_site_files']==['assets/proof-readers.css'] and not candidate['global_css_changed']
dest=E/'native-review/radius_native_5bf8'
files=[p for p in sorted(N.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
assert all(not p.is_symlink() for p in files)
assert not any(any(t in p.name for t in ['.private.','git-index','foreign-state','control-snapshot']) for p in files)
manifest=[{'path':str(p.relative_to(N)),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size,'mode':stat.S_IMODE(p.stat().st_mode)} for p in files]
create(dest/'originals.manifest.json',dump({'source_root':str(N),'files':manifest,'excluded':'Only Python bytecode caches; no source/proof/receipt/raw failure/inspection/reader originals excluded. Full private foreign/control/index guards are outside this owned directory and are not exported.'}))
archive=dest/'originals.tar.gz'
with archive.open('xb') as raw:
    with gzip.GzipFile(fileobj=raw,mode='wb',mtime=0) as gz:
        with tarfile.open(fileobj=gz,mode='w') as tf:
            for p in files:tf.add(p,arcname=str(p.relative_to(N)),recursive=False)
with tarfile.open(archive,'r:gz') as tf:
    assert set(tf.getnames())=={x['path'] for x in manifest}
    for x in manifest:
        b=tf.extractfile(x['path']).read();assert len(b)==x['bytes'] and sha(b)==x['sha256']
archivehash=sha(archive.read_bytes())
source_dest=E/'normal-verification/radius_src_73c1/admissibility-originals'
for p in sorted(S.rglob('*')):
    if p.is_file():create(source_dest/p.relative_to(S),p.read_bytes())
assert sha((source_dest/'bounded-admissibility-decision.json').read_bytes())=='d04a9fac96bbe344dbf6b7d543d950af3a9374aa765ee3f50fc5b282205d67bf'
status={'user_instruction':'尝试把已经完成的都提交，然后先暂停','state':'PAUSE_REQUESTED;R10_PROVED_LOCAL;NO_NORMAL_VERIFIED','proof_commit':'4c3251454100a4591113b16ed119fdf758c876b7','reader_commit':'c4d031f237fa0e16fbba16987ca6b34c7f3dfd98','source_review_carrier':'8ec8fc501901a6c9aa90f63048f2f865aec183ab','PROVED_LOCAL_carrier':head,'completed':['Exact P/T local Lean proofs, full sealed-type proof-body checks and real q0 applications.','Independent source-blind reconstructions, original source/whole-module review and renewed label-repair context accepted.','Independent native empty-output8module rebuild and44actual type/body kernel checks with full54065node ExprDAG.','Real original4context browser checks completed; original390px publication table FAIL preserved.','Separate exact one-CSS-file conditional candidate automated4context browser PASS, globalCSS unchanged.'],'open':['No normal VERIFIED call; all25original PL fields must remain inline unchanged in any future V.','Final held-commit4metadata gates and fresh independent preservation/once-history checks not run.','Conditional candidate independent visual review and canonical sharedCSS application not completed.','Original stabilization owner remains unreleased; no clean-port/main integration/public site/source index/globalgraph delivery.','Both complete main lower bounds, exactoracle/TV/precision/dimension-conditionnumber/worstcap/expectedcost adapters and final purification unfinished.'],'native_originals_archive':{'path':str(archive),'sha256':archivehash,'files':len(manifest),'bytes':archive.stat().st_size,'lossless_readback_verified':True},'conditional_browser':{'receipt':'receipts/20261113T051428135799Z-browser-conditional-approved.json','actual_exit':0,'status':'AUTOMATED_PASS_UNAPPLIED;INDEPENDENT_VISUAL_REVIEW_PENDING'},'unclaimed_next_statement':{'directory':'.astis/huanjian-gc-source-matrix-structure-20261113','state':'PROOF_FREE_UNCLAIMED;FIRST_FORMATION_FAILED','formation_receipt':'.astis/huanjian-resume-20261103/20261113T051728188098Z-unclaimed-source-matrix-structure-literal-prop-formation.receipt.json','diagnosis':'No MeasurableSpace instance for Matrix in displayed measurability/independence assertions. Audit the canonical Borel/coordinate matrix structure before a separately sealed successor; no new caller premise. No new SAU/ledger/proof exists.'},'root_PROVED_LOCAL_calls':1,'root_VERIFIED_calls':0,'native_browser_processes':'Both owned reader server threads joined and Chrome contexts closed according to actual completed reports. No pending native receipts or live subagent tasks.','other_queues_and_ledger':'Unchanged since exact sole PL append; existing owners/frontiers/foreign results retained.','resume':'Resume from this handoff and actual recorded hashes; do not replay PL or reset states. Finish pending independent V gates before opening the next SAU.','push':'Attempt task branch only; main and shared stabilization ownership untouched.'}
create(E/'pause-handoff-20261113.json',dump(status))
create(E/'README.md',(r'''# Gaussian source matrix radius — paused checkpoint

The public theorem proves the actual truncated summand and actual mean norms.
Its private Tests consumer proves the actual centered and cosine-weighted radius.
The sole source condition is `2*q+1<d`; `q=0`, the original Gaussian product law,
actual Bochner mean and inclusive cutoff are retained.

Math code: `4c3251454100a4591113b16ed119fdf758c876b7`.
Current reviewed reader: `c4d031f237fa0e16fbba16987ca6b34c7f3dfd98`.
One normal PROVED_LOCAL carrier: `bb04072adab2143e1c656edff93c029df0098e45`.

Local Lean, blind reconstruction, independent source/whole-module and independent
native mathematics checks passed. The native lossless archive preserves actual
full type/proof-value inspections, raw commands/receipts, failed attempts, exact
source snapshots, original/conditional generated pages and screenshots.

The original mobile publication table FAIL remains a FAIL. The separate exact
CSS candidate passed automated browser checks, remains unapplied, and still needs
independent visual review. No normal VERIFIED call or final four held metadata
gates have occurred. Main integration, publication, purification, both complete
lower bounds and the overall Goal remain unfinished.

User requested commit/push of completed work, then pause. Use
`pause-handoff-20261113.json` for precise evidence, open items and the unclaimed
proof-free next statement. Do not replay transitions or export private guards.
''').encode())
cell['evidence']['independent_native_math_originals']={'archive':str(archive),'sha256':archivehash,'manifest':str(dest/'originals.manifest.json'),'scope':'Independent math PASS; original reader FAIL; conditional automated PASS is separate/unapplied.'}
cell['evidence']['conditional_reader_candidate']={'automated_status':'PASS','independent_visual_review':'pending','global_CSS_applied':False,'original_reader_status':'FAIL','candidate_css_sha256':candidate['conditional_css_sha256']}
cell['reader_contract']['status']='Original-CSS actual mobile table FAIL preserved. Separate exactCSScandidate automated4context/8source-download PASS; independent candidate visual review, sharedCSS integration and full-site delivery pending. User requested pause.'
cell['paused_by_user']={'requested':True,'handoff':str(E/'pause-handoff-20261113.json'),'normal_state_retained':'PROVED_LOCAL','new_ledger_events':0}
C.write_bytes(dump(cell))
process=E/'pause-process-originals'
for n in ['package_completed_work_and_pause.py','actual-PROVED_LOCAL-carrier-commit.json','carry_label_repair_source_review.py','carry_label_repair_source_review.attempt1.original.py','incremental-source-transfer-attempt1-diagnosis.json']:
    create(process/n,(W/n).read_bytes())
rr=Path('.astis/huanjian-resume-20261103')
for rp in sorted(rr.glob('*source-matrix-radius-*.receipt.json')):
    if rp.name<'20261113T050700':continue
    r=json.loads(rp.read_bytes());log=Path(r['log']);assert sha(log.read_bytes())==r['log_sha256']
    for p in [rp,log]:create(process/'actual-runs'/p.name,p.read_bytes())
assert L.read_bytes()==ledger_before
paths=[C,*[p for p in sorted(E.rglob('*')) if p.is_file() and subprocess.run(['git','ls-files','--error-unmatch','--',str(p)],capture_output=True).returncode]]
assert not any('.private.' in str(p) for p in paths)
spec=W/'pause-commit-paths.private.nul';create(spec,b'\0'.join(str(p).encode() for p in paths)+b'\0')
subprocess.run(['git','add','-f','--pathspec-from-file='+str(spec),'--pathspec-file-nul'],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check','--',str(C)],check=True)
subprocess.run(['git','commit','--quiet','-m','Preserve completed Gaussian proofs and native evidence at user pause'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
for p in paths:assert git('show',f'{commit}:{p}')==p.read_bytes()
result={'pause_commit':commit,'completed_artifact_files_committed':len(paths),'native_lossless_archive_bytes':archive.stat().st_size,'native_original_files':len(manifest),'normal_VERIFIED_calls':0,'ledger_unchanged':True,'global_CSS_unchanged':True,'push':'pending task-branch push'}
create(W/'actual-pause-commit.json',dump(result));print(json.dumps(result))
