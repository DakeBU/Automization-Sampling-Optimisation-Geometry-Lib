import copy, hashlib, json, subprocess, sys
from pathlib import Path
sys.path.insert(0, 'tools')
import astis, astis_publication as pub, publication_reader

R = Path('runs/20261007-companion-priority/positive-step-proximal-rgo')
C = '921d39902a3327a4983e197b6e68516fea5fb5d8'
S = 'c2909e15b1b1a5adb9b4778a9c17693dd7521206'
P = '39c19947c6267141f39bcb2b64e0def30b00164e'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n', b'\n')
def read(p): return json.loads(Path(p).read_bytes())
def fp(p):
    b = Path(p).read_bytes()
    return dict(path=str(p).replace('\\','/'), bytes=len(b), raw_sha256=sha(b), lf_sha256=sha(lf(b)))
def git(*args): return subprocess.check_output(['git', *args])
assert git('rev-parse','HEAD').decode().strip() == C
assert subprocess.run(['git','merge-base','--is-ancestor',P,C]).returncode == 0
v=read(R/'verified.json'); m=read(R/'whole-math-review.json'); blocked=read(R/'reviewer.repository.attempt1.blocker.json')
assert sha((R/'verified.json').read_bytes())=='b7ef82fe4955486f259a23f4fc48a2234c786772f913368df18dfba5747b73fb'
assert sha((R/'whole-math-review.json').read_bytes())=='4a07bfc07ceccf8dd7424c5efae68d40c56081546b5135c8a281994f40e5b74e'
assert v['verification_status']=='passed-scoped' and v['verified_commit']==P
changed=git('diff','--name-only',P,C).decode().splitlines()
immutable_prefix=('AutoSamplingTheory/', 'Tests/', 'tools/', 'website/content/declaration_lessons/', 'website/content/publications/', 'research-wiki/semantic-audits/')
assert not [p for p in changed if p.startswith(immutable_prefix) or p in ('AutoSamplingTheory.lean','Tests.lean','lakefile.lean','lake-manifest.json','lean-toolchain')]
repair_delta=git('diff','--name-only',S,C).decode().splitlines()
assert all(p.startswith(str(R).replace('\\','/')+'/') or p=='docs/companion-papers-handoff.md' for p in repair_delta)
assert not git('diff',S,C,'--','research-wiki/frontier-cells')
for item in blocked['inputs'][:5]:
    assert fp(item['path']) == item

integration=read(R/'integration.json')
checks=[]
for check in integration['checks']:
    assert check['exit_code']==0 and sha(Path(check['log']).read_bytes())==check['raw_sha256']
    checks.append(fp(check['log']))
aggregate=Path(integration['checks'][0]['log']).read_text(encoding='utf-8')
assert '9132' in aggregate and '9394' in aggregate and 'ASTIS check passed' in aggregate
refresh=read(R/'graph-administrative-refresh.json')
oldpath=Path(refresh['old_graph_snapshot']); old=read(oldpath)
graphpath=Path('_site/data/underlying-lean-graph.json'); graph=read(graphpath)
assert sha(oldpath.read_bytes())==refresh['old_graph_raw_sha256']==blocked['inputs'][5]['raw_sha256']
assert sha(graphpath.read_bytes())==refresh['current_graph_raw_sha256']
assert old['publication_inputs_sha256']==refresh['old_publication_inputs_sha256']
assert graph['publication_inputs_sha256']==refresh['current_publication_inputs_sha256']==publication_reader.graph_input_digest()
assert len(old['nodes'])==len(graph['nodes'])==2086
assert len(old['edges'])==len(graph['edges'])==5458
assert {n['id'] for n in old['nodes']}=={n['id'] for n in graph['nodes']}
assert old['edges']==graph['edges'], 'formal/source edge payload changed unexpectedly'
assert fp('_site/data/site-data.json')==blocked['inputs'][6]
graph_checks=[]
for check in refresh['graph_checks']:
    assert sha(Path(check['receipt']).read_bytes())==check['raw_sha256']
    saved=read(check['receipt']); live=pub.graph_report(check['cell'],Path('_site'))
    assert saved==live and live['status']=='graph coverage checked'
    graph_checks.append(live)
assert sha(Path(refresh['regeneration_log']).read_bytes())==refresh['regeneration_log_raw_sha256']

source=read(R/'reviewer.exact.source-binding.json')
targets=source['reviewed_publication_targets']
pub.check_advance(targets,reviewed=True)
data=pub.inputs()
source_checks=[]
for record in source['source_reviews']:
    for key in ('review','reviewer_packet','whole_module','decoder_result','original_decoder_result'):
        assert fp(record[key]['path'])==record[key]
    audit=data['audits'][record['audit_id']]
    assert audit['state']=='accepted'
    found=[(i,b) for i in pub.load() for b in i['bindings'] if b.get('audit_id')==record['audit_id'] and b['declaration']==record['declaration']]
    assert len(found)==1
    item,binding=found[0]
    assert pub.binding_digest(item,binding,data)==record['publication_binding_sha256']
    assert pub.digest(pub.review_context(item,binding,data))==record['review_context_sha256']
    source_checks.append(dict(audit_id=record['audit_id'], binding_sha256=record['publication_binding_sha256'],review_run_sha256=record['review_run_sha256'],whole_module=record['whole_module'],decoder_result=record['decoder_result']))

files=astis.lean_source_files(); hits=[]
for path in files:
    for no,line in enumerate(astis.strip_lean_comments_and_strings(path.read_text(encoding='utf-8')).splitlines(),1):
        if astis.FORBIDDEN_REGEX.search(line): hits.append(dict(path=str(path),line=no,text=line))
assert not hits
pins=read('lake-manifest.json')
assert next(p for p in pins['packages'] if p['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert Path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'

# Raw immutable artifacts are compared to Git blobs, not JSON reserialization.
raw_paths=sorted({str(p).replace('\\','/') for p in R.rglob('*') if p.is_file() and p.name!='reviewer.repository.repair-check.py' and not p.name.startswith('reviewer.repository.repair.')})
raw_paths=[p for p in raw_paths if subprocess.run(['git','cat-file','-e',f'{C}:{p}'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0]
proc=subprocess.Popen(['git','cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for path in raw_paths:
    proc.stdin.write(f'{C}:{path}\n'.encode()); proc.stdin.flush()
    header=proc.stdout.readline().decode().split(); blob=proc.stdout.read(int(header[2])); assert proc.stdout.read(1)==b'\n'
    assert blob==Path(path).read_bytes(), path
proc.stdin.close(); assert proc.wait()==0
assert git('rev-parse','HEAD').decode().strip()==C
result=dict(schema_version=1,status='accepted-scoped',verification_status='passed-scoped',checked_commit=C,repository_commit=C,verified_proof_commit=P,verifier_id='picard_commit_verifier_20261005',owner_is_not_verifier=True,
 scope='Packet28 repository ProofSeal: existing two all-positive-step declarations plus unchanged AffineGibbs metadata revalidation; no duplicate proof credit.',
 previous_blocker=fp(R/'reviewer.repository.attempt1.blocker.json'), blocker_resolved='Exact current generated graph digest matches canonical current inputs; both bounded graph reports independently recomputed and equal the retained refresh receipts.',
 repair_commit_delta=repair_delta, mathematical_preservation=dict(proof_to_shared_no_production_Test_pin_tool_Registry_lesson_publication_audit_change=True,c290_to_current_cell_bytes_unchanged=True,whole_math=fp(R/'whole-math-review.json'),exact_verification=fp(R/'verified.json'),whole_math_reused_only_unchanged=True),
 Lean_gate=dict(authoritative_root_aggregate_reused=True,root_jobs=9132,Tests_jobs=9394,log=checks[0],no_new_compiler_or_aggregate_rebuild=True,standard_axioms=v['standard_axioms']),
 graph=dict(refresh=fp(R/'graph-administrative-refresh.json'),old_graph_snapshot=fp(oldpath),current_graph=fp(graphpath),publication_inputs_sha256=graph['publication_inputs_sha256'],node_count=2086,edge_count=5458,exact_same_edge_payload=True,bounded_current_checks=graph_checks,empty_regeneration_log_is_not_visual_evidence=True),
 current_source_binding_checks=source_checks,publication_admission='fresh check_advance(all three targets, reviewed=True) passed',
 fake_closure_scan=dict(canonical_files=len(files),hits=hits,scanner='astis strip_lean_comments_and_strings + FORBIDDEN_REGEX'),
 immutable_raw_Git_artifacts_checked=len(raw_paths),raw_LF_inputs=[fp(R/'integration.json'),fp(R/'graph-administrative-refresh.json')]+checks,
 integration_gate_counts=integration['metadata_checks'],other_gates_reused='Exact immutable integration publication/semantic/frontier/process/contributor/site log bytes checked; previous fresh read-only c290 checks remain valid because mathematics, tools, bindings and cells unchanged.',
 exclusions=['Reference-only Gaussian background availability files do not enter mathematical proof credit.','Untracked gaussian-laplace-domain and future source/theorem work excluded.','Separate ExpositionSeal evidence in repair commit not self-admitted or used as proof/source evidence.'],
 remaining_boundary=['Only source proximal/Gaussian selector and true standardized RGO last TWO comparisons of (4.6) for every eta>0 are certified. FIRST W2 comparison, bias, MGF, full Lemma4.2, joint posterior sampling, Wp/warmness/query costs/composition and both main results remain open.','PURIFIED/Exposition admission, Copy/Download controls, rendered visual QA, own-head remote CI, merge/live acceptance are not granted by this repository ProofSeal.','Original sole PhaseKernel STABILIZING owner preserved.'],
 permitted_mutations='Only owned repository reviewer evidence; no cells/ledger/production/shared writes.',leases=dict(compiler='CLOSED; no compiler started',write='CLOSED after receipt',read='CLOSED'))
out=R/'repository-proof-seal.json'; assert not out.exists()
out.write_bytes((json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(status=result['status'],checked_commit=C,receipt=fp(out),fake_files=len(files),raw_artifacts=len(raw_paths),leases='CLOSED')))
