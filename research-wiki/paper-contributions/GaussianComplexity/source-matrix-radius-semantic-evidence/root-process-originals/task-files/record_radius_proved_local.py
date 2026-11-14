"""One normal R10 PL transition after actual mathematics and current reviewed publication."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
sys.path.insert(0,str(Path(__file__).resolve().parent))
import astis_advance as advance
import astis_frontier_cells as frontiers
import astis_publication as pub
import preservation_guard as guard
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-radius.json')
SP=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-statement-seal.json')
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixRadius.lean')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixRadius.lean')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261113-GaussianComplexitySourceMatrixRadius'
OWNER='huanjian_gc_20261113_source_matrix_radius'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip()
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
assert not (W/'normal-PROVED_LOCAL-attempted.once.json').exists()
before=L.read_bytes();assert before==git('show',f'{head}:{L}')
states=advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert states[ADV]['state']=='EXPLORING' and states[ADV]['owner_id']==OWNER
preserved_before=guard.check('EXPLORING')
seal=json.loads(SP.read_bytes());assert sha(SP.read_bytes())=='49d5fa00c9ae90d65878d955fab59d6a4bc03e942501677719881f3d26bf1a72'
math=json.loads((E/'local-math-candidate.json').read_bytes())
for p,x in zip([P,T],math['executed_worktree_sources']):
    assert sha(p.read_bytes())==x['sha256']
    assert git('show',f'4c3251454100a4591113b16ed119fdf758c876b7:{p}')==p.read_bytes()
checks=[r for r in math['actual_runs'] if any(s in r['receipt'] for s in ['final-P-T-Lake-build','exact-proof-value-kernel-first'])]
assert len(checks)==2
for x in checks:
    rp=Path(x['receipt']);assert sha(rp.read_bytes())==x['receipt_sha256'];r=json.loads(rp.read_bytes())
    assert r['exit_code']==0 and sha(Path(r['log']).read_bytes())==r['log_sha256']==x['log_sha256']
nativepath=Path('.astis/semantic-neutral-20261113/radius_native_5bf8/math-judgment.json')
assert sha(nativepath.read_bytes())=='15034ad5253adb449a5b3e52daf9997ce45ae80a49f739a26c6eeb63a21c1042'
native=json.loads(nativepath.read_bytes());assert native['initial_native_output_empty'] and native['root_ASTIS_oleans_excluded']
audit=json.loads(A.read_bytes());assert audit['state']=='source-reviewed' and audit['source_review']['state']=='accepted'
assert audit['publication_binding_sha256']=='7081c71690e9b29aa32cd09b9e093358d2660a231066384243784fa4654c64fa'
name=audit['lean']['declaration'];pub.check_advance([name],reviewed=True)
cell=json.loads(C.read_bytes());assert cell['conceptual_mirror_audit']['status']=='none-found'
assert not frontiers.validate_cells(frontiers.load_cells())
readerpath=Path('.astis/semantic-neutral-20261113/radius_native_5bf8/reader/browser-original/report.json')
reader=json.loads(readerpath.read_bytes())
assert reader['candidate']=='c4d031f237fa0e16fbba16987ca6b34c7f3dfd98' and reader['variant']=='original'
assert len(reader['contexts'])==4 and len(reader['source_checks'])==8
assert not reader['page_errors'] and not reader['failed_requests'] and not reader['http_errors']
assert len(reader['layout_failures'])==1
reader_boundary='Independent native math and current source review PASS. Actual original-CSS Chromium reader atc4d031 completed4contexts/8source-download checks with formulas and321full code lines exact, but390px publication table is clipped/unscrollable (client335,scroll496,overflowXvisible,scrollLeft100→0): original reader FAIL. CSS candidate and serialized production delivery remain separate; no complete-site reader claim.'
boundary=cell['truth_boundary']+' Actual P/T local proof bodies are compiled and independently source/native-math reviewed; reader runtime acceptance is separate. T remains private Tests, no public API/Registry credit.'
result={'result_kind':'theorem-edge','theorem_delta':seal['producer']['signature'],'lean_files':[str(P),str(T)],'lean_declarations':[name],'publication_declarations':[name],'focused_checks':checks,'truth_boundary':boundary,'mathematical_candidate':'4c3251454100a4591113b16ed119fdf758c876b7','executed_worktree_build_qualification':math['build_commit_qualification'],'source_review_metadata_commit':head,'reader_metadata_commit':audit['reader_commit'],'publication_binding_sha256':audit['publication_binding_sha256'],'actual_compiled_parent_edges':math['canonical_ASTIS_P_parents'],'actual_material_consumer':{'name':'_private.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius.0.AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius.actual_source_centered_summand_radius','file':str(T),'file_sha256':sha(T.read_bytes()),'sealed_signature':seal['actual_private_consumer']['signature'],'direct_ASTIS_parent':name,'private_implementation_only':True,'public_API_registry_credit':False,'source_decision':cell['evidence']['independent_source_review']['private_T_decision']},'independent_source_review':cell['evidence']['independent_source_review'],'independent_native_math':{'path':str(nativepath),'sha256':sha(nativepath.read_bytes()),'native_math_commit':native['math_candidate_commit'],'actual_module_closure_count':len(native['actual_ASTIS_import_closure_rebuilt']),'actual_declarations_kernel_checked':native['actual_declarations_kernel_checked'],'reader_and_metadata_gate_acceptance':'separate, not implied'},'conceptual_mirror_audit':cell['conceptual_mirror_audit'],'owned_math':math['kernel'],'kernel_type_check':'Actual P/T proof BODIES kernel checked at complete unchanged sealed universal Props, actualq0,d2 applications; raw Expr equalities false, kernel conversion passed. All7owned declarations type/body closed, root reachable, standardaxioms only. Native independently rebuilt8moduleclosure and kernel checked44 actual declarations with lossless ExprDAG.','formalizer_API_pristine':False,'proof_iteration':{'all_failed_draft_originals_retained':True,'statement_and_binders_unchanged':True,'source_label_reader_failure_preserved':'Immutable4b585 actual production reader failed KeyError:label. One citation display label repaired atc4d031 and changed exact context independently reaccepted; no runtime pass is inferred.','no_implementation_failure_used_as_math_refutation':True},'reader_boundary':cell['reader_contract']['status'],'preservation_before_API':preserved_before,'integration_notes':'Original stabilization owner remains unreleased at exact fetched main4db0f863; no shared CSS/root imports/globalgraph/Registry/site/source-index or clean-port. No matrix Bernstein, full Lemma4.4, main lower bound, oracle/TV/precision/cap/cost or purification credit.'}
result['reader_boundary']=reader_boundary
result['actual_original_reader_report']={'path':str(readerpath),'sha256':sha(readerpath.read_bytes()),'status':'FAIL_MOBILE_TABLE_CLIPPED','source_and_formula_checks_completed':True,'production_CSS_applied_fix':False}
create(W/'normal-PROVED_LOCAL-attempted.once.json',dump({'advance_id':ADV,'from_state':'EXPLORING','to_state':'PROVED_LOCAL','head':head,'before_ledger_sha256':sha(before),'normal_API_calls_requested':1}))
advance.transition_advance(ADV,'PROVED_LOCAL',worker_id=OWNER,evidence=result)
after=L.read_bytes();assert after.startswith(before);append=after[len(before):];assert len(append.splitlines())==1
event=json.loads(append);assert event['advance_id']==ADV and event['to_state']=='PROVED_LOCAL' and event['evidence']==result
cell['status']='proved_locally';cell.pop('reservation_only',None);cell['truth_boundary']=boundary
cell['evidence']['focused_checks']=checks;cell['evidence']['actual_PROVED_LOCAL_append_sha256']=sha(append)
cell['evidence']['normal_API_calls']=4;cell['statement_seal']['status']='EXACT_UNCHANGED_SEALED_TYPES;LOCAL_COMPILED;INDEPENDENT_SOURCE_NATIVE_MATH_ACCEPTED;RUNTIME_READER_SEPARATE'
cell['reader_contract']['status']=reader_boundary
cell['evidence']['actual_original_reader_report']=result['actual_original_reader_report']
cell['learning_contract']['salvage']={'required':True,'status':'completed','reason':'All failed proof/serializer/reader metadata attempts retained; no target assumption or definition changed and no mathematical fragment discarded. Real local P/T proofs and independent reviews preserved.','promoted_fragments':[name],'discarded_fragments':[]}
C.write_bytes(dump(cell));assert not frontiers.validate_cells(frontiers.load_cells())
preserved_after=guard.check('PROVED_LOCAL');assert preserved_after==preserved_before
create(E/'actual-PROVED_LOCAL-append.exact.jsonl',append);create(E/'actual-PROVED_LOCAL-evidence.full.json',dump(result));create(E/'normal-PROVED_LOCAL-preservation.json',dump(preserved_after))
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
print(json.dumps({'state':'PROVED_LOCAL','actual_API_calls':1,'append_sha256':sha(append),'full_original_payload_sha256':sha(dump(result)),'preservation':preserved_after,'root_VERIFIED_calls':0}))
