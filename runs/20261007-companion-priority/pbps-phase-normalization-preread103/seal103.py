"""Freeze the independently accepted analytic statement before implementation."""
from pathlib import Path
import datetime, gzip, hashlib, json, subprocess

root = Path.cwd()
pre = Path(__file__).parent
previous = pre.parent / 'pbps-actual-weighted-sector102'
source = previous / 'next-primary103'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()

def ref(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), raw_sha256=sha(b), bytes=len(b))

head = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
assert head == load(previous / 'integration102/postpush-binding102.json')['remote_head']
assert head == load(pre / 'context-before-fetch103.json')['commit']
assert load(pre / 'fetch-status103.json')['exit_code'] == 0
header = ref(pre / 'Header103.lean')
assert header['raw_sha256'] == 'af63f42611e180b198e069c2e636ddf48ee529524ecf3a292c51bf28111fb60d'
mathp = pre / 'independent-header-math103/header-math-decision103.native.json'
sourcep = pre / 'independent-header-source103/header-source-decision103.native.json'
topologyp = pre / 'independent-header-math103/source-topology-admission103.native.json'
assert load(mathp)['decision'] == 'ACCEPT_PROSPECTIVE_HEADER_MATHEMATICS'
assert load(topologyp)['decision'] == 'ACCEPT_BASE_PLUS_API_IDENTITY_OVERLAY_TOPOLOGY_AND_COVERAGE'
assert ref(sourcep)['raw_sha256'] == 'de4b227ed951572ea7917029125d6e863ed851576fd60f81397142c86aa305ad'
assert ref(mathp)['raw_sha256'] == '43e91d7b88d467f87de32470a7eaad16894d3f0ba4e0038f50c55ad880946c8a'
assert ref(topologyp)['raw_sha256'] == 'd4d060a36906851307159315f10770970a82b81282a4fe9c34fd600d60f094ac'

# Context snapshots were independently recovered before this seal. They remain
# scheduling evidence, not theorem premises.
recoveries = {}
for row in load(previous / 'integration102/owned-before.json'):
    recoveries[(row['path'], row['raw_sha256'])] = Path(row['snapshot'])
artifacts = []
bindings = {}
for directory in [source, pre / 'independent-header-math103', pre / 'independent-header-source103']:
    for p in sorted(directory.rglob('*.json')):
        artifacts.append(ref(p))
        def walk(value):
            if isinstance(value, dict):
                name, digest = value.get('path'), value.get('raw_sha256')
                if isinstance(name, str) and isinstance(digest, str) and len(digest) == 64:
                    key = (name.replace('\\', '/'), digest)
                    target = Path(name)
                    if target.exists() and 'line_start' in value and 'line_end' in value:
                        raw = target.read_bytes()
                        piece = b''.join(raw.splitlines(keepends=True)[value['line_start'] - 1:value['line_end']])
                        assert sha(piece) == digest, ('Source line slice mismatch', name, value)
                        bindings[key] = dict(path=name, raw_sha256=digest, resolved_path=name, line_start=value['line_start'], line_end=value['line_end'])
                    elif target.exists() and 'byte_start' in value and 'byte_end_exclusive' in value:
                        piece = target.read_bytes()[value['byte_start']:value['byte_end_exclusive']]
                        assert sha(piece) == digest, ('Source byte slice mismatch', name, value)
                        bindings[key] = dict(path=name, raw_sha256=digest, resolved_path=name, byte_start=value['byte_start'], byte_end_exclusive=value['byte_end_exclusive'])
                    elif target.exists() and sha(target.read_bytes()) == digest:
                        bindings[key] = dict(path=name, raw_sha256=digest, resolved_path=name)
                    elif key in recoveries and sha(recoveries[key].read_bytes()) == digest:
                        bindings[key] = dict(path=name, raw_sha256=digest, resolved_path=recoveries[key].as_posix(), historical_context=True)
                    else:
                        raise AssertionError(('Unresolved RAW input; diagnose before sealing', name, digest))
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(load(p))

recommendation = load(source / 'recommendation103.native.json')
parents = [
    'AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower',
    'AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn',
    'AutoSamplingTheory.TechnicalLemmas.Analysis.Integrability.lintegral_exp_neg_mul_norm_sq_eq',
    'AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity.map_sqrt_smul_stdGaussian_eq_withDensity',
    'AutoSamplingTheory.TechnicalLemmas.Measure.Gibbs.isProbabilityMeasure_withDensity_normalized_gibbs',
]
text = (pre / 'Header103.lean').read_text(encoding='utf8')
seal = dict(
    status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',
    sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    statement_version=1, owner='companion_root_20261005', baseline_commit=head,
    header=header, expanded_literal_Prop=text.split('def candidate', 1)[1].split('#check candidate', 1)[0].strip(),
    proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseNormalization.actual_phase_gibbs_normalization',
    source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',
    source_anchor='Eq3.1 and conditional energy: positive finite phase partition and exact conditional-Gibbs times standard-Gaussian identification; source-implicit normalization used by Appendix A.1 averaging.',
    independent_math_header=ref(mathp), independent_source_header=ref(sourcep), independent_topology=ref(topologyp),
    source_graph=ref(source / 'source-proof-graph-delta103.native.json'),
    source_graph_overlay=ref(source / 'graph-normalization103/source-api-identity-normalization103.native.json'),
    source_coverage=ref(source / 'source-coverage-delta103.native.json'),
    primary=ref(Path(load(source / 'primary-first103.native.json')['primary']['path'])),
    all_review_artifacts_rehashed=artifacts, all_bound_RAW_inputs_rehashed=list(bindings.values()),
    binder_audit=dict(SOURCE=['hα', 'hαβ', 'hV', 'hH', 'hη', 'hβη'], TYPING='Finite-dimensional real Hilbert Borel space, including rank zero.', EXCESS=[]),
    definition_audit='Eleven literal definitions: dimension, proximal position energy, actual phase energy, Gibbs factor, position-first volume, real position partition, exact Gaussian constant, ENNReal phase partition, tilted position measure, normalized phase withDensity and stdGaussian.',
    core_delta=recommendation['selected_single_boundary'], actual_producer_plan=parents,
    consumer='Stable NORM joins SECTOR102-UNNORM only at future normalized SECTOR100 and initial phase-Gibbs averaging. NORM itself is analytically independent of102.',
    truth_boundary='Exact phase probability normalization and product-law identity only; no process invariance, countable sector assembly, Markov property, hypocoercivity, implementation error, cost or main theorem completion.',
    proof_search_started=False, sau_claimed=False, Goal_complete=False)
target = pre / 'root.statement-seal103.json'
assert not target.exists()
target.write_text(json.dumps(seal, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('Sealed103', ref(target)['raw_sha256'], 'with', len(bindings), 'RAW bindings.')
