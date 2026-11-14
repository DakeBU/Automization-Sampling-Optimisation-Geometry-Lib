"""One normal PL call after frozen independent math/source/reader evidence."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools');sys.path.insert(0,str(Path(__file__).resolve().parent))
import astis_advance as advance
import astis_frontier_cells as frontiers
import astis_publication as pub
import preservation_guard as guard
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-gram-realization-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-gram-realization.json')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-gram-realization.json')
SP=Path('research-wiki/paper-contributions/GaussianComplexity/source-gram-realization-statement-seal.json')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261113-GaussianComplexitySourceGramRealization'
OWNER='huanjian_gc_20261113_source_gram_realization'
MATH='60ec0e083261dfa71f009bdd5d8c9e63b1425bb7'
READER='d35db1ade1a63ea9b944c5f2983760ba6d50dfab'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(b)
head=git('rev-parse','HEAD').decode().strip()
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
assert not (W/'normal-PROVED_LOCAL-attempted.once.json').exists()
cfg=json.loads((W/'normal-PL-inputs.json').read_bytes())
assert cfg['metadata_commit']==head
for x in cfg['frozen_inputs']:
 assert sha(Path(x['path']).read_bytes())==x['sha256']
before=L.read_bytes();assert before==git('show',f'{head}:{L}')
states=advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert states[ADV]['state']=='EXPLORING' and states[ADV]['owner_id']==OWNER
preserved_before=guard.check('EXPLORING')
seal=json.loads(SP.read_bytes())
assert sha(SP.read_bytes())=='7b2f71cf9e89a41da4f66b2b3908222c875cd2fec2f8b2ca6533fe61b3bb3ce9'
math=json.loads((E/'local-math-candidate.json').read_bytes())
for x in math['source_files']:
 p=Path(x['path'])
 assert sha(p.read_bytes())==x['sha256'] and git('show',f'{MATH}:{p}')==p.read_bytes()
checks=[math['actual_final_build'],math['actual_final_proof_value_kernel']]
for x in checks:
 rp=Path(x['file']);r=json.loads(rp.read_bytes())
 assert r['exit_code']==0 and sha(Path(r['log']).read_bytes())==r['log_sha256']==x['log_sha256']
native=json.loads(Path(cfg['native_math']['path']).read_bytes())
assert native['status']=='PASS' and native['checked_commit']==MATH
assert native['closure_modules']==8 and native['complete_module_emission_count']==41
assert native['task_module_emission_count']==4 and native['unique_expr_nodes']==52106
for key in ['all_complete_types_and_values_kernel_checked','all_complete_types_and_values_closed',
 'standard_axioms_only','initial_native_output_empty','nine_manifest_packages_clean_at_pin',
 'all_direct_local_olean_resolutions_owned','root_ASTIS_prebuilt_olean_excluded']:
 assert native[key] is True
assert all(x['fullUniversalTypeKernelDefEq'] and x['actualProofAtSealedTypeKernelChecked']
 and x['genuineQ0UniversalApplicationKernelChecked'] and x['genuineQ0ApplicationKernelChecked']
 for x in native['literal_seal_and_qzero_results'])
a=json.loads(A.read_bytes())
assert a['source_review']['state']=='accepted' and a['state'] in ['source-reviewed','accepted']
assert a['publication_binding_sha256']=='65c30c6418698d87435669de50b1d56de12aac5814baa77903556a5e5087c404'
name=a['lean']['declaration'];pub.check_advance([name],reviewed=True)
cell=json.loads(C.read_bytes());assert cell['conceptual_mirror_audit']['status']=='none-found'
assert not frontiers.validate_cells(frontiers.load_cells())
assert cfg['reader']['actual_candidate_commit']==READER
assert cfg['reader']['original']['checker_exit']==1
assert cfg['reader']['combined_C2']['checker_exit']==0
assert cfg['reader']['production_CSS_changed'] is False
assert cfg['reader']['independent_closed_review']['status']=='FINAL_RUNTIME_READER_PENDING_C3'
boundary=cell['truth_boundary']+' Actual complete P/T proof bodies compiled and independently source/native reviewed. Original reader FAIL and isolated C2 automated checks are distinct; full-source horizontal reading/final reader C3 and serialized integration remain pending.'
result={
 'result_kind':'theorem-edge','theorem_delta':seal['producer']['signature'],
 'lean_files':[x['path'] for x in math['source_files']],
 'lean_declarations':[name],'publication_declarations':[name],'focused_checks':checks,
 'truth_boundary':boundary,'mathematical_candidate':MATH,
 'executed_build_qualification':math['build_commit_qualification'],
 'source_review_metadata_commit':head,'reader_metadata_commit':READER,
 'publication_binding_sha256':a['publication_binding_sha256'],
 'actual_compiled_parent_edges':math['canonical_P_parents'],
 'actual_material_consumer':{
  'name':native['targets']['T']['actual_name'],'file':math['source_files'][1]['path'],
  'file_sha256':math['source_files'][1]['sha256'],
  'sealed_signature':seal['actual_private_consumer']['signature'],
  'direct_ASTIS_parents':math['private_T_parents'],
  'both_P_outputs_materially_used':True,'private_implementation_only':True,
  'public_API_registry_credit':False,
  'source_decision':cell['evidence']['independent_source_review']['private_T_decision'],
  'scope':'All-real-threshold deterministic generalization of printed numeric Ex126, conditional on original G and the actual same-outcome centered-sum bounds. Only a<=1 needed and proved internally; no probability claim.'},
 'independent_source_review':cell['evidence']['independent_source_review'],
 'independent_native_math':cfg['native_math'],
 'conceptual_mirror_audit':cell['conceptual_mirror_audit'],'owned_math':math['kernel'],
 'native_emission_count_qualification':'Native rechecked41 actual emitted declarations across8modules. The two target modules emit4=publicP, privateT, generatedP_proof_1_1 and privateT_abel_1_1. ROOTowned4=2handwritten+2generated. No helper is a separate public mathematical node.',
 'kernel_type_check':'Actual full universal P/T proof values at literal sealed types, genuine q0 universal and q0d2 applications. ROOT rawExpr equality false but kernel conversion passed. Native complete lossless structured ExprDAG, real Euclidean L2 norm/CLM action and unchanged topology checked.',
 'formalizer_API_pristine':False,
 'proof_iteration':math['iteration_qualification']+' Native inventory/module-mode API failures and source-label snapshot custody qualification retained; no source/binder/definition change. Original reader failures retained; C1 untested; C2 separately frozen and actually run.',
 'reader_boundary':cfg['reader']['boundary'],'actual_reader_evidence':cfg['reader'],
 'preservation_before_API':preserved_before,
 'integration_notes':'Original shared stabilization owner remains reserved. No shared CSS/root imports/Registry/global graph/source-index/production site or clean-port changed. No Bernstein event probability, full FactC6/Lemma4.4/main lowerbound or oracle/TV/precision/query-cap/cost/purification credit.'}
create(W/'normal-PROVED_LOCAL-attempted.once.json',dump({'advance_id':ADV,'head':head,'before_ledger_sha256':sha(before),'normal_API_calls_requested':1}))
advance.transition_advance(ADV,'PROVED_LOCAL',worker_id=OWNER,evidence=result)
after=L.read_bytes();assert after.startswith(before)
append=after[len(before):];assert len(append.splitlines())==1
event=json.loads(append)
assert event['advance_id']==ADV and event['to_state']=='PROVED_LOCAL' and event['evidence']==result
cell['status']='proved_locally';cell.pop('reservation_only',None);cell['truth_boundary']=boundary
cell['evidence']['focused_checks']=checks
cell['evidence']['actual_PROVED_LOCAL_append_sha256']=sha(append)
cell['evidence']['normal_API_calls']=4
cell['evidence']['independent_native_math']=cfg['native_math']
cell['evidence']['local_math_candidate']['independent_semantic']='accepted exact P and explicit private T generalization'
cell['evidence']['local_math_candidate']['independent_native']='PASS actual60ec complete closure'
cell['statement_seal']['status']='EXACT_UNCHANGED_LITERAL_GRAM_TYPES;LOCAL_COMPILED;INDEPENDENT_SOURCE_NATIVE_ACCEPTED;FINAL_RUNTIME_READER_PENDING;INTEGRATION_HELD'
cell['reader_contract']['status']=cfg['reader']['boundary']
cell['evidence']['actual_reader_evidence']=cfg['reader']
cell['graph_contribution']['visual_review']=cfg['reader']['graph_boundary']
cell['learning_contract']['failure_class']='NONE'
cell['learning_contract']['salvage']={'required':True,'status':'completed',
 'reason':'All actual proof/formation/metadata/custody/native-inventory/reader failures retained. Final P/T signatures, definitions and binders unchanged.',
 'promoted_fragments':[name],'discarded_fragments':[]}
C.write_bytes(dump(cell));assert not frontiers.validate_cells(frontiers.load_cells())
preserved_after=guard.check('PROVED_LOCAL');assert preserved_after==preserved_before
create(E/'actual-PROVED_LOCAL-append.exact.jsonl',append)
create(E/'actual-PROVED_LOCAL-evidence.full.json',dump(result))
create(E/'normal-PROVED_LOCAL-preservation.json',dump(preserved_after))
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
print(json.dumps({'state':'PROVED_LOCAL','actual_API_calls':1,'append_sha256':sha(append),
 'full_original_payload_sha256':sha(dump(result)),'preservation':preserved_after,'root_VERIFIED_calls':0}))
