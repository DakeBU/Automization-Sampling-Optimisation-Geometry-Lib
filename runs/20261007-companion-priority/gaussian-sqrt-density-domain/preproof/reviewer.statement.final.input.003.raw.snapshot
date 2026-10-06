from pathlib import Path
import hashlib, json

scratch = Path('.astis/gaussian-domain32')
pre = Path('runs/20261007-companion-priority/gaussian-sqrt-density-domain/preproof')
assert not pre.exists()
assert json.loads((scratch / 'reviewer.statement.lease.json').read_text(encoding='utf-8'))['read_lease'] == 'CLOSED'
typecheck = json.loads((scratch / 'root.statement-typecheck.0.json').read_text(encoding='utf-8'))
assert typecheck['status'] == 'type-elaboration-pass' and typecheck['exit_code'] == 0 and typecheck['compiler_lease'] == 'CLOSED'
pre.mkdir(parents=True)
def bind(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': p.as_posix(), 'raw_sha256': hashlib.sha256(b).hexdigest(), 'lf_sha256': hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest(), 'bytes': len(b)}
def write(p, data):
    assert not p.exists()
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
history = pre / 'historical-scratch'
history.mkdir()
copies = []
for p in sorted(scratch.rglob('*')):
    if p.is_file():
        dest = history / p.relative_to(scratch)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(p.read_bytes())
        copies.append({'original': bind(p), 'portable_raw_snapshot': bind(dest)})
proposal = json.loads((scratch / 'root.statement-proposal.json').read_text(encoding='utf-8'))
for target in proposal['targets']:
    source = Path(target['signature']['path'])
    dest = pre / source.name
    dest.write_bytes(source.read_bytes())
    assert bind(dest)['raw_sha256'] == target['signature']['raw_sha256']
    target['signature'] = bind(dest)
proposal['canonical_portability_only'] = 'Signature bytes, binder/conclusion order and source input bindings unchanged. Original scratch proposal and preliminary review remain immutable raw historical snapshots; final independent review must bind these portable target paths.'
proposal['source_binder_audit'][0] = 'Printed fixed-parameter source V/kappa/eta>0 unchanged. S and measurable eta/y are an authored family extension whose Unit specialization recovers every fixed source parameter; these are not printed paper assumptions.'
proposal['dependency_plan'] = {
    'existing_API_search': [
        'AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity',
        'AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment.integrable_norm_sq_and_integral_stdGaussian',
        'AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic',
        'AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.gradient_expNegPotential_eq_of_differentiableAt',
        'AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Gradient.continuous_gradient_of_contDiff_one',
        'AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher.standardized_rgo_position_and_fisher',
    ],
    'new': 'One canonical actual Gaussian-Gibbs relative-density and square-root energy/domain theorem, genuinely instantiated on SAME actual standardized true RGO. Existing nodes supply Gaussian density/moments, curvature and real affine posterior; no LSI/T2/final-output certificate.',
    'generic_minimal_import_candidates': [
        'AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity',
        'AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianMoment',
        'AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization',
    ],
    'source_imports': [
        'AutoSamplingTheory.TechnicalLemmas.Measure.GaussianSqrtDensityDomain',
        'AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher',
    ],
    'API_search_boundary': 'Existing public headers/definitions and module cards only; no candidate proof implementation or proof search. Actual implementation dependencies must be reconciled after proof, not copied as unchecked direct edges.',
}
write(pre / 'root.statement-proposal.json', proposal)
for name, destname in [('root.statement-typecheck.0.log', 'root.statement-typecheck.0.log'), ('StatementTypeProbe.lean', 'root.statement-typeprobe.lean'), ('root.statement-typecheck.0.json', 'root.statement-typecheck.original.raw.json')]:
    (pre / destname).write_bytes((scratch / name).read_bytes())
write(pre / 'typecheck.portable.json', {
    'schema_version': 1, 'status': 'type-elaboration-pass-portable-exact-inputs',
    'actual_original_receipt': bind(pre / 'root.statement-typecheck.original.raw.json'),
    'actual_original_command': typecheck['command'], 'exit_code': 0,
    'exact_signature_copies': [t['signature'] for t in proposal['targets']],
    'exact_probe_copy': bind(pre / 'root.statement-typeprobe.lean'),
    'exact_log_copy': bind(pre / 'root.statement-typecheck.0.log'),
    'compiler_lease': 'CLOSED', 'proof_search_started': False,
    'transformation': typecheck['transformation'],
    'status_boundary': 'Root type-only #check forallPi pass, not a theorem body, proof, StatementSeal or mathematical admission.',
})
write(pre / 'portability.proposal.json', {
    'schema_version': 1, 'status': 'exact-portable-preproof-inputs-await-final-independent-statement-review',
    'raw_copies': copies,
    'canonical_proposal': bind(pre / 'root.statement-proposal.json'),
    'allowed_metadata_changes': ['canonical signature paths, same raw/LF bytes', 'explicit authored measurable-family versus printed fixed-parameter scope', 'bounded existing API inventory and prospective import plan'],
    'mathematical_binders_conclusions_changed': False,
    'source_graph_topology_changes': False,
    'original_preliminary_receipts_immutable': True,
    'proof_search_started': False, 'SAU_claimed': False,
})
print('Exact type-only PASS and preliminary review preserved in portable canonical preproof inputs; final independent StatementSeal review pending.')
