"""One normal PL call, only with exact completed independent evidence configured."""
from pathlib import Path
import hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools');sys.path.insert(0,str(Path(__file__).resolve().parent))
import astis_advance as advance
import astis_frontier_cells as frontiers
import astis_publication as pub
import preservation_guard as guard
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-structure.json')
A=Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-structure.json')
SP=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-structure-statement-seal.json')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261113-GaussianComplexitySourceMatrixStructure'
OWNER='huanjian_gc_20261113_source_matrix_structure'
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
seal=json.loads(SP.read_bytes());assert sha(SP.read_bytes())=='0164b6bcb7f1362c27e459eccf6a68a72a7cea81272f15377e7c193af18e3c60'
math=json.loads((E/'local-math-candidate.json').read_bytes())
for x in math['source_files']:
 p=Path(x['path']);assert sha(p.read_bytes())==x['sha256'] and git('show',f'9ed997b7fda8631deb5bc1397d021495d53c4d41:{p}')==p.read_bytes()
checks=[math['actual_final_build'],math['actual_final_proof_value_kernel']]
for x in checks:
 rp=Path(x['file']);r=json.loads(rp.read_bytes());assert r['exit_code']==0 and sha(Path(r['log']).read_bytes())==r['log_sha256']==x['log_sha256']
native=json.loads(Path(cfg['native_math']['path']).read_bytes())
assert native['status']=='PASS_NATIVE_ONLY' and native['compiled_commit']=='9ed997b7fda8631deb5bc1397d021495d53c4d41'
assert native['initial_owned_output_empty'] and native['actual_complete_values_rechecked'] and native['all_closed']
assert native['borel_standard_product_kernel_equality'] and native['l2operator_standard_pi_topology_kernel_equality']
a=json.loads(A.read_bytes());assert a['source_review']['state']=='accepted' and a['state'] in ['source-reviewed','accepted']
assert a['publication_binding_sha256']=='1185046d8ac28b7caff1c3b4a02527e3b56a7fefaafbc59602d04bc62a07c8da'
name=a['lean']['declaration'];pub.check_advance([name],reviewed=True)
cell=json.loads(C.read_bytes());assert cell['conceptual_mirror_audit']['status']=='none-found'
assert not frontiers.validate_cells(frontiers.load_cells())
assert cfg['reader']['actual_candidate_commit']=='7c364dbeaf44c1f23defe10534e6cd3dffdac172'
boundary=cell['truth_boundary']+' Actual complete P/T proof bodies compiled and independently source/native reviewed. Runtime reader and serialized integration remain separate.'
result={'result_kind':'theorem-edge','theorem_delta':seal['producer']['signature'],'lean_files':[x['path'] for x in math['source_files']],'lean_declarations':[name],'publication_declarations':[name],'focused_checks':checks,'truth_boundary':boundary,'mathematical_candidate':'9ed997b7fda8631deb5bc1397d021495d53c4d41','executed_build_qualification':math['build_commit_qualification'],'source_review_metadata_commit':head,'reader_metadata_commit':'7c364dbeaf44c1f23defe10534e6cd3dffdac172','publication_binding_sha256':a['publication_binding_sha256'],'actual_compiled_parent_edges':math['canonical_P_parents'],'actual_material_consumer':{'name':a['lean']['declaration'].replace('AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure','_private.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure.0.AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixStructure.actual_source_weighted_centered_matrix_structure'),'file':math['source_files'][1]['path'],'file_sha256':math['source_files'][1]['sha256'],'sealed_signature':seal['actual_private_consumer']['signature'],'direct_ASTIS_parent':name,'all_five_P_outputs_materially_used':True,'private_implementation_only':True,'public_API_registry_credit':False,'source_decision':cell['evidence']['independent_source_review']['private_T_decision']},'independent_source_review':cell['evidence']['independent_source_review'],'independent_native_math':cfg['native_math'],'conceptual_mirror_audit':cell['conceptual_mirror_audit'],'owned_math':math['kernel'],'native_emission_count_qualification':'Native rechecked9 actual emitted declarations across7modules; targetmodules emit4=P, privateT, generatedP_simp and Matrix.kroneckerMap.eq_1. ROOTnamespaceowned3=P,privateT,P_simp. No helper is a separate public mathematical node.','kernel_type_check':'Actual full universal P/T proof values at literal sealed types, q0 and q0d2. ROOT rawExpr equality false but kernel conversion passed. Native complete lossless structured ExprDAG and standardBorel/L2topology equalities checked.','formalizer_API_pristine':False,'proof_iteration':'All actual proof, formation, serializer and metadata failures preserved. They are API/implementation evidence, not source or mathematical refutations. Initial incomplete compiler-tail diagnosis explicitly corrected; premature strictcheck only failed missingTolean, final fullbuild precedes successful complete proofvaluecheck.','reader_boundary':cfg['reader']['boundary'],'actual_reader_evidence':cfg['reader'],'preservation_before_API':preserved_before,'integration_notes':'One original stabilization owner remains reserved; no shared CSS/root imports/Registry/globalgraph/source-index/production site or clean-port modified. No matrix Bernstein tail, full Lemma4.4/main lowerbound or oracle/TV/precision/cap/cost/purification credit.'}
create(W/'normal-PROVED_LOCAL-attempted.once.json',dump({'advance_id':ADV,'head':head,'before_ledger_sha256':sha(before),'normal_API_calls_requested':1}))
advance.transition_advance(ADV,'PROVED_LOCAL',worker_id=OWNER,evidence=result)
after=L.read_bytes();assert after.startswith(before);append=after[len(before):];assert len(append.splitlines())==1
event=json.loads(append);assert event['advance_id']==ADV and event['to_state']=='PROVED_LOCAL' and event['evidence']==result
cell['status']='proved_locally';cell.pop('reservation_only',None);cell['truth_boundary']=boundary
cell['evidence']['focused_checks']=checks;cell['evidence']['actual_PROVED_LOCAL_append_sha256']=sha(append);cell['evidence']['normal_API_calls']=4
cell['statement_seal']['status']='EXACT_UNCHANGED_STANDARD_BOREL_TYPES;LOCAL_COMPILED;INDEPENDENT_SOURCE_NATIVE_MATH_ACCEPTED;READER_INTEGRATION_SEPARATE'
cell['reader_contract']['status']=cfg['reader']['boundary'];cell['evidence']['actual_reader_evidence']=cfg['reader']
cell['learning_contract']['failure_class']='NONE'
cell['learning_contract']['salvage']={'required':True,'status':'completed','reason':'All actual failed proof/serializer/metadata/reader iterations retained; final P/T no source-binder or definition change.','promoted_fragments':[name],'discarded_fragments':[]}
C.write_bytes(dump(cell));assert not frontiers.validate_cells(frontiers.load_cells())
preserved_after=guard.check('PROVED_LOCAL');assert preserved_after==preserved_before
create(E/'actual-PROVED_LOCAL-append.exact.jsonl',append);create(E/'actual-PROVED_LOCAL-evidence.full.json',dump(result));create(E/'normal-PROVED_LOCAL-preservation.json',dump(preserved_after))
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(C),str(L)}
print(json.dumps({'state':'PROVED_LOCAL','actual_API_calls':1,'append_sha256':sha(append),'full_original_payload_sha256':sha(dump(result)),'preservation':preserved_after,'root_VERIFIED_calls':0}))
