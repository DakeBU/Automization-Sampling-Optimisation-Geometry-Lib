from pathlib import Path
import hashlib, json

scratch = Path('.astis/gaussian-domain32')
preread = Path('runs/20261007-companion-priority/gaussian-transport-preread')
def bind(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': p.as_posix(), 'raw_sha256': hashlib.sha256(b).hexdigest(), 'lf_sha256': hashlib.sha256(b.replace(b'\r\n', b'\n')).hexdigest(), 'bytes': len(b)}
review = json.loads((preread / 'reviewer.topology.repaired.review.json').read_text(encoding='utf-8'))
assert review['status'] == 'accepted-scoped' and not review['blocking']
records = []
for label, namespace, file in [
    ('generic', 'AutoSamplingTheory.TechnicalLemmas.Measure.GaussianSqrtDensityDomain', 'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianSqrtDensityDomain.lean'),
    ('source', 'AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOSqrtDensity', 'AutoSamplingTheory/ExampleCases/SmoothedPicardHMC/StandardizedRGOSqrtDensity.lean'),
]:
    p = scratch / (label + '.signature.txt')
    records.append({'kind': label, 'namespace': namespace, 'file': file, 'declaration': namespace + '.' + p.read_text(encoding='utf-8').split()[1], 'signature': bind(p), 'proof_body_present': False})
out = scratch / 'root.statement-proposal.json'
assert not out.exists()
packet = {
    'schema_version': 1,
    'status': 'prospective-statement-before-typecheck-independent-seal-claim-or-proof-search',
    'created_by': 'companion_root_20261005',
    'targets': records,
    'source_inputs': [bind(preread / p) for p in ['repair.proposal.json', 'source-proof-graph.repaired.independent.json', 'source.inventory.repaired.json', 'source.contract.repaired.json', 'reviewer.topology.repaired.review.json']],
    'historical_routing': 'Original dependency-ready.packet.json is immutable reconnaissance and binds the superseded graph. It is not the admission graph for this candidate.',
    'truth_boundary': 'Actual positive Gaussian relative-density and classical C2/L2 square-root/entropy/log-gradient/Dirichlet=Fisher/4 domains, genuinely consumed by the source standardized true RGO. No Gaussian LSI/T2/KL weak representative/Sobolev adapter/W2/bias/fullLemma/main/work/composition credit.',
    'source_binder_audit': [
        'Source inputs unchanged: kappa>=1, globalC2V, Hessian kappa^-1..1, every eta>0, measurable parameter maps. No numerical eta cap.',
        'Finite real Hilbert/complete/Borel represents the cited Euclidean source and includes dimension0.',
        'Generic C2convexrho, origin normalization/stationarity and finite NNReal upper L are authored background inputs; source instantiation must derive each from literal rho, never add them as source-facing premises.',
        'No caller provides density, normalizer, probability, Fisher, moments, LSI/T2, selector, scores or domains.',
    ],
    'definition_audit': {
        'gamma': 'Actual pinned Mathlib stdGaussian E, covarianceI, not merely an IsGaussian assumption.',
        'r': 'Generic actual gamma tilt by -rho; source actual affine pushforward of the original Gibbs conditional RGO, with SAME produced stationary p.',
        'q': 'Explicit exp(-rho)/Z actual relative density. Measure withDensity equality fixes the probability law, not a pointwise arbitrary RN derivative.',
        'f': 'Explicit positive exp(-rho/2)/sqrtZ; squared density relation and all derivative-energy domains produced internally.',
        'energy': 'Euclidean Hilbert gradient. Dirichlet energy equals one-quarter actual relative Fisher integral, with exact measures and all L2 domains. Not sup-norm coordinate energy.',
        'entropy': 'Bochner L1 of explicit qlogq under gamma. It is not yet a theorem equating this to an arbitrary chosen KL API.',
    },
    'intended_route_at_most_seven_steps': [
        'Derive convex rho>=0 and linear gradient growth from actual curvature and stationary origin.',
        'Produce finite positive Z and normalized actual Gaussian tilt internally.',
        'Identify actual Gaussian density and volume Gibbs law; retain explicit withDensity relative representative.',
        'Derive Gaussian and true tilted L2 domains from actual growth bounds and finite Gaussian moments.',
        'Differentiate literal f and logq, preserving exact scalar normalizations.',
        'Produce entropy L1 from quadratic rho growth and true probability normalization.',
        'Use actual withDensity/tilt integral semantics to identify Dirichlet energy as Fisher/4.',
    ],
    'failure_policy': 'After first failure and two unchanged repeats freeze route for typed diagnosis. Missing domains must be internally proved or recorded as a strict smaller source-cited residual, never supplied as new source premise.',
    'proof_search_started': False,
    'compiler_started': False,
}
out.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('Prospective exact target proposal pinned to repaired independently reviewed source graph; no claim, seal or implementation.')
