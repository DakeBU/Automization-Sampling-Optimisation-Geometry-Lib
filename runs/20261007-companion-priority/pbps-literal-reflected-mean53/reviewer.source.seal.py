from pathlib import Path
import json, hashlib, datetime

root = Path('E:/Samplinglib')
p = Path(__file__).parent
actor = 'phase_source_reviewer_20261005'
sha = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda v: json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
now = lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(path): return json.loads(Path(path).read_bytes())
def resolve(path):
    z = Path(path)
    return z if z.is_absolute() else root / z
def footprint(path, data=None):
    z = resolve(path)
    b = z.read_bytes() if data is None else data
    return {'path': str(z.relative_to(root)).replace('\\', '/'), 'raw_sha256': sha(b), 'lf_sha256': sha(b.replace(b'\r\n', b'\n')), 'bytes': len(b)}
def write(path, value):
    assert not path.exists(), str(path)
    b = (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    path.write_bytes(b)
    return footprint(path, b)
def seal(value, field):
    assert field not in value
    value[field] = sha(canonical(value))
    return value

started = now()
leasepath = p / 'source.review.lease.json'
ownpath = p / 'reviewer.source.lease.json'
opening = leasepath.read_bytes()
ownopening = ownpath.read_bytes()
lease = json.loads(opening)
own = json.loads(ownopening)
assert lease['status'] == own['status'] == 'OPEN'
assert len(lease['input_artifacts']) == 506
packet = load(p / 'source.0.reviewer-packet.json')
checks = load(p / 'reviewer.source.checks.json')
assert checks['all_raw_LF_match'] and checks['errors'] == []
assert packet['packet_sha256'] == checks['reviewer_packet_sha256_recomputed'] == lease['reviewer_packet_sha256']
assert packet['publication_binding_sha256'] == checks['publication_binding_sha256_recomputed']

snaps = p / 'reviewer.source.snapshots'
assert not snaps.exists()
snaps.mkdir()
(snaps / 'root-opening-lease.raw.snapshot.json').write_bytes(opening)
(snaps / 'reviewer-opening-lease.raw.snapshot.json').write_bytes(ownopening)
initial = {'schema': 'source53-original-506-inputs-before-authorized-helper-extension/v1', 'input_artifacts': lease['input_artifacts']}
write(p / 'reviewer.source.initial-inputs.json', initial)
rows = []
for i, expected in enumerate(lease['input_artifacts']):
    data = resolve(expected['path']).read_bytes()
    current = footprint(expected['path'], data)
    for k in ('raw_sha256', 'lf_sha256', 'bytes'):
        if k in expected: assert current[k] == expected[k], (expected['path'], k)
    target = snaps / f'{i:03d}.raw.snapshot'
    target.write_bytes(data)
    rows.append({'original': expected, 'snapshot': footprint(target, data), 'pre_and_sealing_raw_LF_equal': True})

# Root explicitly authorized semantic reading only of physical47-115; whole
# helper bytes are bound as provenance, not interpreted outside that interval.
helper = root / 'tools/astis_publication.py'
helperdata = helper.read_bytes()
fragment = b''.join(helperdata.splitlines(keepends=True)[46:115])
(snaps / 'publication-helper.47-115.raw.snapshot.py').write_bytes(fragment)
helperpin = footprint(helper, helperdata)
helperfragment = footprint(snaps / 'publication-helper.47-115.raw.snapshot.py', fragment)
inventory = seal({'schema': 'source53-independent-immutable-input-snapshot-inventory/v1', 'created_utc': now(), 'original_input_count': 506, 'rows': rows, 'additional_authorized_input_artifacts': [helperpin], 'authorized_semantic_read': {'path': helperpin['path'], 'physical_lines': [47, 115], 'fragment': helperfragment}, 'original_root_manifest_unchanged': True}, 'inventory_run_sha256')
inventorypin = write(p / 'reviewer.source.inventory.json', inventory)

def slot(original, reconstructed, evidence, relation='same'):
    return dict(original=original, reconstructed=reconstructed, relation=relation, evidence=evidence)
slots = {
 'objects': slot('Literal normalized Gibbs mu, quadratic posterior R_y, volume reflected law S_y with V((y+u)/2) and displacement denominator8eta.', 'The same three literal normalized tilts and the exact map x -> 2x-y.', 'Complete definitions, posterior tilt composition and affine inverse algebra checked. Actual positive ZV and mu probability are produced before use; S_y is the literal volume law, not an arbitrary conditional version.'),
 'domains': slot('Finite-dimensional real Hilbert/Borel E, including rank0; globally C2 V and signed globally C1 compact f.', 'Finite real inner-product space and canonical volume, rank0 allowed, signed compact C1 observer.', 'All five ambient classes, real Frechet derivatives, compact support and true Bochner mean are preserved. Original paper smooth compact Euclidean standing is separately disclosed as narrower than this authored sufficient background.', 'explicit-elaboration'),
 'quantifiers': slot('For every permitted E,V,alpha,eta,f, simultaneously every-y literal law equality and global C1 of the whole mean.', 'For every y, exact pushforward equality; the whole mean function is globally C1; conclusions conjoined.', 'No AE-only y quantifier, arbitrary selector, selected conditional representative or observer-dependent law replaces the literal families.'),
 'assumptions': slot('alpha>0, eta>0, V C2 with global lower Hessian alpha, f C1 compact; no output certificates.', 'Exactly these assumptions; no probability, partition, law, domination, derivative or closed-gradient premise.', 'Binder audit has no EXCESS. Omission of beta/cap and C1/Hilbert/rank0 generalization are explicit sufficient-background extensions; the genuine source Test retains both curvature bounds, beta*eta<=1 and smooth compact f.'),
 'conclusion': slot('Every-y S_y=(2x-y)#R_y and ContDiff1 of y -> integral f dS_y.', 'Exactly that law identity and global continuously differentiable mean.', 'Complete99-line production and all true parent definitions inspected: normalized positive Gibbs -> posterior tilt -> affine identity -> genuine52 mean C1. No score derivative or rough-domain conclusion exported.'),
 'scopes': slot('Attributed analytic integration for PBPS C.1 A3.Ex1/Ex2/E1 toward B.13; not a printed standalone theorem.', 'No derivative formula, rough observer, trajectory, mixing, error or work theorem is asserted.', 'All six formulas and full103-line Tests match this scope. Literal Tf closure, full rough B.13/Gamma, half-turn, main/cost/composition and full-reader/PURIFIED delivery remain open.'),
 'constant_dependencies': slot('Exact scales1/2,2, Gaussian denominator2eta and reflected denominator8eta; all eta>0.', 'The same fixed affine/noise coefficients, inverse half(y+u); no upper step-size premise.', 'Checked norm symmetry/scaling and inverse map; inverse Jacobian2^-d gives ZS=2^d ZR and cancels once in normalized law. Rank0 Test has noncentered mean1 and derivative0, with no unit-vector/nontrivial-space assumption.')
}
receipt = {
 'schema_version': 1, 'status': 'ACCEPTED_SCOPED_SOURCE_FIDELITY', 'blocking': False,
 'reviewer': actor, 'independent_from_formalizer': True, 'independent_from_decoder': True,
 'reviewer_packet_sha256': packet['packet_sha256'], 'publication_binding_sha256': packet['publication_binding_sha256'],
 'semantic_slots': slots, 'verdict': 'equivalent-after-elaboration', 'deltas': [], 'repairs': [], 'source_excess': [],
 'review_evidence': 'Independent own-primary53 interpretation was rechecked before current packet/body/decoder exposure. All506 frozen raw/LF inputs match. The complete production, complete Tests, actual three producer definitions, every-y law/normalization and mean-C1 route, six formula steps and native blind reconstruction were checked. Packet and full publication binding were independently recomputed using the authorized canonical helper47-115; projected review_context is not the binding payload. No mathematical or metadata blocker remains. This is scoped source fidelity of an explicitly authored background integration, not whole-paper or rough B.13 completion.',
 'input_artifacts': lease['input_artifacts'], 'additional_authorized_input_artifacts': [helperpin],
 'input_snapshot_inventory': inventorypin, 'checks': footprint(p / 'reviewer.source.checks.json'),
 'primary_first': {'contract': lease['primary_first_contract'], 'current_copy_byte_equal': True, 'contract_raw_sha256': '9b54d8edb4ef16144b9d2db5adf9cfc8334756d5059077a62fca7a369b5d3eb8', 'chronology': 'Own primary closed before prospective candidate, source topology, current body and decoder. Historical exposures are retained, not described as amnesia.'},
 'exposure': {'historical': ['Earlier PBPS source/API and52 whole body/Test/source review', 'Own53 primary, prospective758 statement and independent original/repaired source-only topology'], 'current': ['Whole53 production99lines and Test103lines', 'Complete actual AffineGibbs/GibbsAugmentation/GaussianReflectedMean provider definitions', 'Relevant actual GaussianConditionalKernel producer and native decoder provenance', 'Current lesson/publication/audit/cell and authorized tools/astis_publication.py physical47-115'], 'whole_math_verdict_read': False, 'compiler_invocations': 0, 'source_history_blind': False, 'strict_decoder_source_identity_blindness': False, 'decoder_source_text_visible': False},
 'definition_and_proof_audit': {'actual_mu_probability_produced': True, 'partition_and_exp_L1_produced': True, 'every_y_posterior_and_source_density_identity': True, 'AE_law_not_used_for_pointwise_derivative': True, 'mean_C1_internal_DOMINATED_derivative_and_continuity': True, 'public_output_certificates_absent': True, 'all_three_parent_bodies_and_relevant_definitions_checked': True, 'all_production_and_Test_proofs_checked': True, 'six_reader_formulas_checked': True, 'direct_dependency_names_checked': True, 'locally_opened_Integrable_of_integral_ne_zero_is_actual_MeasureTheory_API': True},
 'source_topology_provenance': {'source_only_repaired_review': 'runs/20261007-companion-priority/pbps-reflected-density-topology-review53/source-topology-review.repaired.json', 'review_raw_sha256': '6b8b7dfc79540114a8165bfd978f4a56b5d9e4ba7415efa737bd3956324979d1', 'original_T53_1_negative_preserved': True, 'minimal_header_Nonempty_NeZero_repair_preserved': True, 'selected_primary107rows_and_author_route_reused_explicitly': True, 'current_implementation_correspondence_checked': True, 'source_topology_not_inferred_from_current_Lean_success': True},
 'decoder_binding': {'decoder': packet['roles']['blind_decoder'], 'reconstructed_text_sha256': packet['blind_reconstruction']['text_sha256'], 'decoder_packet_sha256': packet['blind_reconstruction']['decoder_packet_sha256'], 'decoder_run_sha256': packet['blind_reconstruction']['decoder_run_sha256'], 'native_decoder_run_recipe': 'SHA256 sorted compact UTF8 explicit run_binding_payload; distinct from raw run.json and complete run_sha256.', 'native_complete_run_sha256': checks['decoder_complete_run_logical_sha256_recomputed'], 'native_plain_string_identity_and_verbatim_text': True, 'portable_bytes_and_initial_lease_basis_verified': True, 'canonical_input_artifacts_literal': ['lean-statement', 'approved-definition-context'], 'inherited_general_AGENTS_source_identity_exposure_disclosed': True},
 'publication_binding_recipe': checks['full_publication_payload_recipe'], 'authorized_helper_fragment': helperfragment,
 'remaining_boundaries': ['Literal actual50 Tf compact C1 and actual51 closed-gradient consumer integration', 'Full rough L2/H1 B.13 and Gamma/operator/half-turn', 'Paper main results, errors, work, composition', 'Complete reader delivery, rendered/live/copy/download and PURIFIED'],
 'hash_recipe': 'review_run_sha256 = SHA256 UTF8 json.dumps(entire receipt without review_run_sha256,ensure_ascii=False,sort_keys=True,separators=(comma,colon),allow_nan=False); no trailing newline.'
}
seal(receipt, 'review_run_sha256')
receiptpin = write(p / 'source.0.review.json', receipt)

# Verify unchanged original inputs once more immediately before closure.
for expected in lease['input_artifacts']:
    current = footprint(expected['path'])
    for k in ('raw_sha256', 'lf_sha256', 'bytes'):
        if k in expected: assert current[k] == expected[k], (expected['path'], k)
assert leasepath.read_bytes() == opening and ownpath.read_bytes() == ownopening
run = seal({'schema': 'native-independent-source53-completed-run/v1', 'reviewer': actor, 'opened_utc': own['opened_utc'], 'sealing_started_utc': started, 'completed_utc': now(), 'input_artifacts': lease['input_artifacts'], 'additional_authorized_input_artifacts': [helperpin], 'opening_root_lease_snapshot': footprint(snaps / 'root-opening-lease.raw.snapshot.json'), 'opening_reviewer_lease_snapshot': footprint(snaps / 'reviewer-opening-lease.raw.snapshot.json'), 'outputs': [receiptpin, inventorypin, footprint(p / 'reviewer.source.initial-inputs.json'), footprint(p / 'reviewer.source.checks.json'), footprint(p / 'reviewer.source.check.py'), footprint(__file__)], 'pre_post_all506_raw_LF_equal': True, 'compiler_started': False, 'scope': 'Independent final source fidelity53; no canonical mutation or theorem self-admission', 'hash_recipe': 'run_sha256 = SHA256 sorted compact ensure_ascii=False UTF8 entire object minus run_sha256,allow_nan=False,no trailing newline.'}, 'run_sha256')
runpin = write(p / 'reviewer.source.run.json', run)
closed = now()
own.update(status='CLOSED', read='CLOSED', write='CLOSED', Python='CLOSED', compiler='NOT_STARTED_CLOSED', closed_utc=closed, input_artifacts=lease['input_artifacts'], additional_authorized_input_artifacts=[helperpin], authorized_helper_semantic_lines=[47,115], outputs=[receiptpin,runpin,inventorypin], review_run_sha256=receipt['review_run_sha256'], no_canonical_mutation=True, compiler_started=False, hash_recipe='lease_run_sha256=SHA256 sorted compact ensure_ascii=False UTF8 entire object minus lease_run_sha256,allow_nan=False,no trailing newline.')
seal(own, 'lease_run_sha256')
ownbytes=(json.dumps(own,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
ownpin=footprint(ownpath,ownbytes)
lease.update(status='CLOSED', read_lease='CLOSED', write_lease='CLOSED', Python_lease='CLOSED', compiler_lease='NOT_STARTED_CLOSED', compiler_started=False, closed_utc=closed, source_review_result=receiptpin, reviewer_stage_run=runpin, independent_reviewer_lease=ownpin, review_run_sha256=receipt['review_run_sha256'], hash_recipe='lease_run_sha256=SHA256 sorted compact ensure_ascii=False UTF8 entire object minus lease_run_sha256,allow_nan=False,no trailing newline.')
seal(lease, 'lease_run_sha256')
leasebytes=(json.dumps(lease,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
leasepin=footprint(leasepath,leasebytes)
# These are the last filesystem operations; no read follows either closure.
ownpath.write_bytes(ownbytes)
leasepath.write_bytes(leasebytes)
print(json.dumps({'verdict':receipt['verdict'], 'receipt':receiptpin,'review_run_sha256':receipt['review_run_sha256'],'stage_run':runpin,'stage_run_sha256':run['run_sha256'],'reviewer_lease':ownpin,'root_lease':leasepin,'root_lease_run_sha256':lease['lease_run_sha256'],'all_read_write_Python_CLOSED':True,'compiler':'NOT_STARTED_CLOSED'},ensure_ascii=False))
