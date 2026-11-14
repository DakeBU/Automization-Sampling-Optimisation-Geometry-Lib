"""Pure metadata/schema preflight. No normal API, baseline, or production writes."""
from pathlib import Path
import copy,hashlib,json,subprocess,sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
C=Path('research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-EXPONENTIAL-QUADRATIC.json')
SP=Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-statement-seal.json')
E=Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
ADV='ASTIS-SA-20261114-MatrixBernsteinExponentialQuadratic'
OWNER='huanjian_20261114_matrix_bernstein_exponential'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda o:(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *a:subprocess.check_output(['git',*a])
def create(p,b):
 with p.open('xb') as f:f.write(b)
assert git('rev-parse','HEAD').decode().strip()=='19eaadc52297606595ee5095de95742d4e6394f0'
sealraw=(W/'statement-seal.unclaimed.v1.json').read_bytes()
assert sha(sealraw)=='c3103a9e8d08fea6c83f35201fce953af4dd93e88a1a3d7d647fc4deaaddeb7a'
seal=json.loads(sealraw)
P=seal['producer']['planned_file'];T=seal['actual_private_consumer']['planned_file']
assert not any(p.exists() for p in [C,SP,E,Path(P),Path(T)])
previous=json.loads(Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-gram-realization.json').read_bytes())
reader=copy.deepcopy(previous['reader_contract'])
reader['status']='Contract planned only: concise attributed real deterministic statement, complete formula proof and exact initially folded P/T; source/native/runtime/publication acceptance pending.'
graph=copy.deepcopy(previous['graph_contribution'])
graph.update({'focus_targets':[seal['producer']['name']],
 'visual_review':'Planned one generic shared canonical producer and its actual private source-family consumer. Future weighted source application is planned only. No compiled/root/global graph acceptance.'})
learning=copy.deepcopy(previous['learning_contract'])
learning.update({'process_memory_ids':[],'failure_class':'NONE',
 'salvage':{'required':True,'status':'completed',
  'reason':'All actual proof-free exp/namespace typing, private-name parser/visibility and source-use-edge record iterations preserved. Exact mathematical P/T unchanged; no target proof route attempted or discarded.',
  'promoted_fragments':[],'discarded_fragments':[]},
 'parallelism':{'decision':'serial','direction_fingerprints':[],
  'expected_information_gain':'One ROOT proof worker. Independent raw SG, distinct raw TC and body-free interface audit have distinct review roles; no parallel mathematical proof routes.',
  'shared_verified_context_digest':sha(sealraw)},
 'cross_route_blind_spot_audit':{'required':False,'status':'not-applicable','evidence':'','canonical_route':'','selection_reason':'No competing mathematical proof routes.'},
 'reader_backpressure':{'purification_status':'pending','exposition_seal_status':'pending','exposition_evidence':'','source_expansion_nodes':[],'lean_expansion_nodes':[],
  'assumptions_preserved':True,'boundary_preserved':True}})
searches=[
 'Samplinglib/ASTIS: bounded names and existing sealed-header audit found no exact exp-quadratic or normalized matrix-MGF replacement. Existing actual source mean/radius/structure and RealMatrixPositiveIntegral interfaces are canonical and directly available.',
 'Mathlib: bounded signature search across the pinned matrix/algebra/probability scope found matrix-exp identities, scalar MGFs and rank-one moments, but no exact replacement within the inspected scope. This is not a global absence claim.',
 'Samplinglib private visibility: R10/R11 source-qualified aliases fail ordinary #check, while a successful ordinary-import TYPE-ONLY diagnostic finds exact compiled private names and sealed types. Malformed numeric-name syntax is retained separately. No private theorem is declared absent/unproved.',
 'Reuse supported public Y/actual-mean norm bounds, actual centered structure and PSD-integral floor; derive centered normalized radius inside the actual consumer. No private-proof reconstruction or duplicate public radius wrapper.'
]
public_T_parents=[
 seal['producer']['name'],
 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds',
 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure',
 'AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef']
weighted='AutoSamplingTheory.Tests.GaussianComplexityBernsteinWeightedMgf.actual_source_weighted_normalized_single_summand_mgf'
boundary=('Only the real finite-nonempty self-adjoint deterministic proof component of Tropp Lemma6.7: '
 'A<=I implies exp(sA)<=I+sA+(exp(s)-s-1)A^2 for s>0, expressed by full Matrix.PosSemidef. '
 'The exact private consumer is the original unconditioned product-Gaussian truncated/centered Z_i, '
 'normalized by actual rho=2r(L+1)/d, and its actual single-summand MGF comparison. '
 'All radius positivity, centering, regularity/integrability, PSD expectation and exp adapters are internal proof obligations, never supplied certificates or extra Gaussian binders. '
 'The real restriction is explicit; this is not the full complex Tropp theorem. No Bernstein sum tail/event probability, full C6/Lemma4.4/main lowerbound, oracle/TV/precision/query-cap/cost, public private-consumer API, integration/publication/purification or whole-Goal credit. '
 'Tropp is an independently matched external background source, not a citation provided by the Gaussian paper.')
source_anchor=('Tropp author preprint last revised15June2011, Lemma6.7 deterministic proof p25 and expectation step p26; '
 'standing definitions/regularity/functional calculus p7-8. Independently matched to uncited Gaussian2610.20492v1 C.2 Ex121; '
 'actual Gaussian consumer uses original Ex107-112 definitions and source radius. Both exact source hashes sealed.')
cell={
 'schema_version':3,'cell_id':C.stem,'route':'shared','mode':'faithfulPaper',
 'title':'Shared real matrix Bernstein exponential-quadratic bound with actual Gaussian MGF consumer',
 'source_anchor':source_anchor,'target_statement':seal['producer']['signature']+'\nExact private original-Gaussian single-summand MGF consumer\n'+seal['actual_private_consumer']['signature'],
 'status':'claimed','owner_id':OWNER,'advance_id':ADV,'parents':[],
 'consumers':[seal['actual_private_consumer']['name'],weighted],
 'consumer_scope':{'current_exact_consumer':{'name':seal['actual_private_consumer']['name'],'state':'PLANNED_LITERAL_SEALED_PRIVATE_T;not_yet_compiled'},
  'second_source_required_route':{'name':weighted,'state':'FUTURE_UNIMPLEMENTED_SOURCE_APPLICATION_ONLY;not_an_additional_current_target',
   'source':'GaussianC.2Ex121 second, cosine-weighted tail; the same deterministic source exp bound is needed for its normalized summands.'},
  'compiled_consumer_credit':False,'separate_random_families_not_joint_independence':True},
 'shared_floor_audit':{'searched':searches,'classification':'adapt','decision':'new_canonical_shared','canonical_declaration':seal['producer']['name'],'canonical_shared_cell':C.stem},
 'reuse_plan':{'searched_existing':searches,'reused_declarations':[],
  'planned_existing_P_parents':[],'planned_private_T_parents':public_T_parents,
  'new_shared_declarations':[seal['producer']['name']],
  'known_consumers':[],'planned_consumers':[seal['actual_private_consumer']['name'],weighted],
  'no_duplicate_wrapper':True,
  'decision_reason':'One generic canonical exp bound serves the actual sealed unweighted Gaussian MGF consumer and the source-required future cosine-weighted route. These are two actual source families, not claimed compiled routes. Keep any radius derivation internal and reuse existing public upper bounds.',
  'private_canonical_nodes_retained_without_false_formal_parent':True},
 'reader_contract':reader,'graph_contribution':graph,'learning_contract':learning,
 'source_detail_audit':{'primary_edition':'Tropp revised2011 PDF SHA '+seal['source_sha256']['Tropp_author2011']+'; Gaussian2610.20492v1 HTML SHA '+seal['source_sha256']['Gaussian2610.20492v1'],
  'primary_anchor':'TroppLemma6.7p25-26; source§2.1-2.3p7-8; GaussianC.2Ex107-112 and uncitedEx121use',
  'detail_status':'omitted',
  'gap':'Source calls the scalar remainder monotonicity a calculus exercise. Spectral transfer/series-exp compatibility, actual Gaussian radius normalization/regularity and PSD expectation must be proved or canonically reused; Lieb/master-tail remain separate downstream gaps, not P/T premises.',
  'consulted':[{'source':'Pinned Tropp author preprint, independently matched external background; not attributed as a supplied Gaussian citation.',
   'anchor':'Lemma6.7 deterministic inequality and expectation proof; §2.2 standing regularity; §2.3 transfer and I+C<=exp(C).',
   'hypothesis_adapter':'P explicit real restriction with one-sided PSD(I-A) and positive s; T original unconditional Gaussian construction with sole hq and all s>0. All stochastic well-posedness and normalization facts are internal, q0 retained.'}],
  'fidelity_boundary':boundary},
 'statement_seal':{'status':'EXACT_PROP_TYPES_FORMED;INDEPENDENT_SEAL_ONLY_ACCEPTED;FULL_SOURCE_TOPOLOGY_PENDING;UNPROVED',
  'file':str(SP),'sha256':sha(sealraw),'signature_sha256':seal['producer']['signature_sha256'],'private_consumer_signature_sha256':seal['actual_private_consumer']['signature_sha256']},
 'evidence':{'normal_API_calls':0,'new_target_proof_calls':0,'formalizer_API_pristine':False,
  'draft_metadata_only':True,'source_admission':'PENDING_DISTINCT_FOCUSED_SOURCE_SUPPLEMENT_RECHECK',
  'actual_literal_formation':seal['formation'],'actual_definition_typing':seal['definition_typing']},
 'blocked':{},'owned_files':[P,T,str(C),str(SP),str(E)+'/',
  'website/content/declaration_lessons/huanjian-matrix-bernstein-exponential.json',
  'website/content/publications/huanjian-matrix-bernstein-exponential.json',
  'research-wiki/semantic-roundtrip/audits/huanjian-matrix-bernstein-exponential.json'],
 'forbidden_shared_files':previous['forbidden_shared_files'],
 'truth_boundary':boundary,'conceptual_mirror_audit':{'status':'pending','discovery_ids':[]},
 'reservation_only':'UNCLAIMED_DRAFT_METADATA_ONLY; NO frontier/ledger write, proof or intake.'}
kwargs={'advance_id':ADV,'task_id':'ASTIS-SW-GAUSSIAN-COMPLEXITY-2026',
 'goal':'Prove one canonical real matrix exponential-quadratic Bernstein background bound and materially consume it in the exact original-Gaussian normalized single-summand MGF inequality, keeping every regularity/radius/centering/spectral/expectation fact internal.',
 'source_anchor':source_anchor,'theorem_delta':seal['producer']['signature'],'truth_boundary':boundary,'created_by':OWNER,
 'dag_inputs':[source_anchor,'Actual public R10 norm bounds, R11 centered structure and canonical real PSD-integral floor are consumer-only dependencies; no false generic-P dependence on Gaussian results.'],
 'proposed_files':[p for p in cell['owned_files'] if not p.endswith('/')],
 'focused_checks':['lake env lean '+P,'lake build Tests.GaussianComplexityBernsteinMgf'],
 'modes':['source-reading','proof-design','compiler-diagnosis'],'priority':50,'frontier_cell':C.stem,
 'target_declarations':[seal['producer']['name']]}
advance.AdvanceProposal(**kwargs).validate()
errors=frontiers.validate_cells(frontiers.load_cells()+[{**cell,'__path__':str(C)}])
assert not errors,errors
create(W/'candidate-frontier-cell.unclaimed.v1.json',dump(cell))
create(W/'candidate-proposal-kwargs.unclaimed.v1.json',dump(kwargs))
memory=Path('research-wiki/process-memory.json').read_bytes()
create(W/'metadata-preflight.unclaimed.v1.json',dump({'schema_errors':0,'proposal_validate':'PASS_PURE_ONLY','shared_consumer_states_explicit':True,
 'process_memory_sha256':sha(memory),'process_memory_applicable_ids':[],
 'new_target_proofs':0,'new_frontier_ledger_calls':0,'full_source_topology':'PENDING_FOCUSED_RECHECK',
 'private_maps_captured_or_exported':False,'production_paths_created':False}))
print(json.dumps({'pure_schema_preflight':'PASS','planned_cell':str(C),'normal_API_calls':0,
 'new_target_proofs':0,'source_topology':'PENDING_FOCUSED_RECHECK','no_baseline_or_production_write':True}))
