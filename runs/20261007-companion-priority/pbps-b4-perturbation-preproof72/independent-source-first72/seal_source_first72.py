import hashlib
import html
import json
import os
import pathlib
import re

BASE = pathlib.Path('E:/Samplinglib')
OUT = BASE / 'runs/20261007-companion-priority/pbps-b4-perturbation-preproof72/independent-source-first72'
PID = os.getpid()


def H(raw):
    return hashlib.sha256(raw).hexdigest()


def C(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def J(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2).encode('utf-8') + b'\n'


def write(name, raw):
    with (OUT / name).open('xb') as handle:
        handle.write(raw)


initial = {'input-finite-pins72.json', 'next-edge-proposal72.utf8.txt', 'seal_source_first72.py'}
assert {p.name for p in OUT.iterdir()} == initial
pins_raw = (OUT / 'input-finite-pins72.json').read_bytes()
pins = json.loads(pins_raw)
assert len(pins['pins']) == 6
for pin in pins['pins']:
    raw = pathlib.Path(pin['path']).read_bytes()
    assert H(raw) == pin['raw_sha256']
    assert H(raw.replace(b'\r\n', b'\n')) == pin['lf_only_sha256']
locator = json.loads(pathlib.Path(pins['pins'][0]['path']).read_bytes())
primary_raw = pathlib.Path(locator['whole_primary']['path']).read_bytes()
assert H(primary_raw) == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
proposal_raw = (OUT / 'next-edge-proposal72.utf8.txt').read_bytes()
proposal = proposal_raw.decode('utf-8')
assert b'\r' not in proposal_raw and not proposal_raw.startswith(b'\xef\xbb\xbf')

node_specs = {
    'S01-setting': ('context', 'Original C2 strongly convex/smooth potential setting; not an extra condition of the extracted abstract algebra.'),
    'S02-real-Hilbert': ('context', 'Real L2, centered classes, adjoints and closed subspace conventions from D1.'),
    'S03-components-polar': ('upstream-context', 'Actual conditional and polar components live in the same centered macroscopic space; isometry is into the complement.'),
    'S04-corrector-definition': ('definition', 'B20 defines the exact half-difference of squared norms minus the A Gamma^-1 cross term; the inverse is only centered.'),
    'S05-ideal-B21': ('source-predecessor', 'Actual idealized g and its actual components satisfy the printed rotation and B21; this is the other B28 addend, not a dependency of the pure shift algebra.'),
    'S06-same-root-inverse': ('algebraic-parents', 'The same centered root/inverse, selfadjointness, commutation and square-sum identities used by the source algebra.'),
    'S07-actual-B27': ('residual-actual-consumer-parent', 'Actual K/H and the centered r_rho must be constructed before applying the abstract shift identity to actual components.'),
    'S08-expand-cancel': ('source-algebra', 'Ex28-Ex31 expand B20 at the paired B27 shift and cancel the two g_V terms.'),
    'S09-linear-simplify': ('source-algebra', 'Ex32-Ex33 reduce the linear contribution to inner(g_P, Gamma^-1 r_rho) using same-map identities.'),
    'S10-quadratic-simplify': ('source-algebra', 'Ex34 reduces half the sum of the A and Gamma squared norms to half ||r_rho||^2.'),
    'S11-B28-consumer': ('future-actual-consumer', 'Printed B28 is obtained only after combining actual B27, the perturbation algebra and actual B21.'),
    'S12-B17-B29-B30': ('residual-analytic-control', 'Actual half-turn B17, adjoint identification, inverse-weighted r and r_rho bounds remain separate.'),
    'S13-B18-actual-norm': ('residual-dissipation', 'B18 is the actual update norm decay and requires actual H contraction; it is not given by the shift identity.'),
    'S14-B31-error-estimates': ('residual-estimates', 'Bounds on r_rho, pair energy and Young inequality feed B31 after B28.'),
    'S15-B4-weight-closure': ('residual-full-B4', 'Small constants, Lambda_rho, omega, B3 norm equivalence and B18/B31 close B26; no full B4 result is claimed.'),
    'P72-perturbation': ('proposed-unproved-target', 'Extract the unnumbered Ex28-Ex34 algebra as an all-u,v,r identity on the same centered space. This node has no proof or SAU state.')
}


def classify(region, mid):
    if region == 'global-assumptions':
        if mid.startswith('S1.p1.') or mid == 'S1.E1.m1':
            return 'S01-setting'
        return None
    if region == 'real-L2-spectral-conventions-D1':
        if (mid.startswith('A4.Thmtheorem1.p1.') or mid in {'A4.E1.m1', 'A4.E2.m1', 'A4.E3.m1'}
                or mid.startswith('A4.SS1.p1.') or mid in {f'A4.SS1.p2.m{i}' for i in range(1, 7)}):
            return 'S02-real-Hilbert'
        return None
    if region == 'corrector-sharp-energy-and-consumers-B3':
        if mid.startswith(('A2.SS3.p1.', 'A2.SS3.p3.')) or mid in {'A2.Ex6.m1', 'A2.Ex8.m1'}:
            return 'S03-components-polar'
        if mid.startswith('A2.SS3.p2.') or mid.startswith('A2.Ex7.') or mid == 'A2.E18.m1':
            return 'S13-B18-actual-norm'
        if mid == 'A2.E19.m1' or mid == 'A2.SS3.p4.m1':
            return 'S15-B4-weight-closure'
        if mid.startswith('A2.SS3.p4.') or mid == 'A2.E20.m1':
            return 'S04-corrector-definition'
        if mid.startswith('A2.SS3.p5.') or mid == 'A2.E21.m1':
            return 'S05-ideal-B21'
        ex = re.match(r'A2\.Ex(\d+)\.', mid)
        if ex and 9 <= int(ex.group(1)) <= 18:
            return 'S05-ideal-B21'
        if mid in {f'A2.SS3.p7.m{i}' for i in range(1, 6)} or mid == 'A2.Ex19.m1':
            return 'S06-same-root-inverse'
        if mid.startswith('A2.Thmtheorem4.p1.') or mid in {'A2.E25.m1', 'A2.E26.m1'}:
            return 'S15-B4-weight-closure'
        return None
    if region == 'corrector-change-B4-consumer-proof':
        if mid.startswith('A2.SS3.p8.'):
            index = int(mid.rsplit('m', 1)[1])
            if index <= 3:
                return 'S15-B4-weight-closure'
            if index <= 15:
                return 'S07-actual-B27'
            if index <= 21:
                return 'S08-expand-cancel'
            return 'S12-B17-B29-B30'
        if mid.startswith('A2.SS3.p9.'):
            return 'S14-B31-error-estimates'
        if mid.startswith('A2.SS3.p10.'):
            return 'S15-B4-weight-closure'
        ex = re.match(r'A2\.Ex(\d+)\.', mid)
        if ex:
            index = int(ex.group(1))
            if 23 <= index <= 27:
                return 'S07-actual-B27'
            if 28 <= index <= 31:
                return 'S08-expand-cancel'
            if 32 <= index <= 33:
                return 'S09-linear-simplify'
            if index == 34:
                return 'S10-quadratic-simplify'
            if 35 <= index <= 36:
                return 'S11-B28-consumer'
            if index == 37:
                return 'S12-B17-B29-B30'
            if 38 <= index <= 39:
                return 'S14-B31-error-estimates'
            if 40 <= index <= 45:
                return 'S15-B4-weight-closure'
        if mid == 'A2.E27.m1':
            return 'S07-actual-B27'
        if mid == 'A2.E28.m1':
            return 'S11-B28-consumer'
        if mid.startswith(('A2.E29.', 'A2.E30.')):
            return 'S12-B17-B29-B30'
        if mid.startswith('A2.E31X.'):
            return 'S14-B31-error-estimates'
        raise AssertionError(('unclassified B4 primary formula', mid))
    raise AssertionError(region)


def extract(raw, region, primary_start):
    records = []
    for match in re.finditer(rb'<math\b[^>]*>.*?</math>', raw, re.S):
        exact = match.group(0)
        head = exact.split(b'>', 1)[0].decode('utf-8')
        mid_match = re.search(r'\bid="([^"]+)"', head)
        alt_match = re.search(r'\balttext="([^"]*)"', head)
        if not mid_match or not alt_match:
            # The whole-primary supplement scan may encounter unnamed math
            # outside the finite four-region scope; it selects only eight IDs.
            # Exact region counts below independently enforce all 255 items.
            continue
        mid = mid_match.group(1)
        alt = html.unescape(alt_match.group(1))
        records.append({
            'math_id': mid,
            'region': region,
            'primary_start_byte': primary_start + match.start(),
            'primary_end_byte_exclusive': primary_start + match.end(),
            'raw_byte_count': len(exact),
            'raw_sha256': H(exact),
            'lf_only_sha256': H(exact.replace(b'\r\n', b'\n')),
            'exact_alttext': alt,
            'alttext_utf8_sha256': H(alt.encode('utf-8'))
        })
    return records


inventory = []
counts = {}
for region in locator['regions']:
    raw = pathlib.Path(region['RAW']['path']).read_bytes()
    assert raw == primary_raw[region['start_byte']:region['end_byte_exclusive']]
    records = extract(raw, region['name'], region['start_byte'])
    counts[region['name']] = len(records)
    for entry in records:
        node = classify(entry['region'], entry['math_id'])
        entry['classification'] = 'NODE' if node else 'EXCLUDED'
        if node:
            entry['node_id'] = node
            entry['coverage_reason'] = node_specs[node][1]
        else:
            entry['coverage_reason'] = {
                'global-assumptions': 'Introductory main-result, prior-work or algorithm-cost claim; outside the centered corrector perturbation edge, preserved without a completion claim.',
                'real-L2-spectral-conventions-D1': 'General spectral calculus or Markov/density/chi-square convention; no new such result is needed by this algebraic target.',
                'corrector-sharp-energy-and-consumers-B3': 'B3 sharp-energy/norm-equivalence calculation or section typography; not a logical parent of the perturbation identity. Its eventual full-B4 use remains explicitly residual.'
            }[entry['region']]
            # Excluded items retain identity, byte range and exact native hashes,
            # without copying an unrelated historical formula payload.
            del entry['exact_alttext']
            del entry['alttext_utf8_sha256']
    inventory.extend(records)
assert counts == {
    'global-assumptions': 30,
    'corrector-sharp-energy-and-consumers-B3': 108,
    'real-L2-spectral-conventions-D1': 42,
    'corrector-change-B4-consumer-proof': 75
}
assert len(inventory) == 255
supplement_nodes = {
    'A2.E7.m1': 'S07-actual-B27',
    'A2.E10.m1': 'S06-same-root-inverse',
    'A2.E12.m1': 'S06-same-root-inverse',
    'A2.E15.m1': 'S06-same-root-inverse',
    'A2.E16.m1': 'S03-components-polar',
    'A2.Thmtheorem2.p1.m1': 'S12-B17-B29-B30',
    'A2.Thmtheorem2.p1.m2': 'S12-B17-B29-B30',
    'A2.E17.m1': 'S12-B17-B29-B30'
}
supplement = []
for entry in extract(primary_raw, 'supplementary-parent-formulas-and-B17-conditions', 0):
    if entry['math_id'] in supplement_nodes:
        node = supplement_nodes[entry['math_id']]
        entry.update({'classification': 'NODE', 'node_id': node, 'coverage_reason': node_specs[node][1]})
        supplement.append(entry)
assert {entry['math_id'] for entry in supplement} == set(supplement_nodes)
assert len(supplement) == 8
inventory.extend(supplement)
assert len(inventory) == len({entry['math_id'] for entry in inventory}) == 263
assert all(entry['classification'] in {'NODE', 'EXCLUDED'} for entry in inventory)
node_count = sum(entry['classification'] == 'NODE' for entry in inventory)
excluded_count = len(inventory) - node_count
coverage = {
    'schema_version': 1,
    'source_id': 'arXiv:2609.06905v1',
    'primary_raw_sha256': H(primary_raw),
    'primary_lf_only_sha256': H(primary_raw.replace(b'\r\n', b'\n')),
    'authority_rule': 'Exact RAW byte spans are authoritative; alttext is independently extracted from each RAW math element, never taken from prior review inventories.',
    'finite_scope': 'Four pinned regions, all 255 math elements, plus exactly eight named supplementary formula/condition spans. No whole-paper coverage claim.',
    'region_math_counts': counts,
    'region_math_count': 255,
    'supplementary_math_count': 8,
    'finite_item_count': 263,
    'NODE_count': node_count,
    'EXCLUDED_count': excluded_count,
    'missing_count': 0,
    'duplicate_math_id_count': 0,
    'entries_canonical_sha256': H(C(inventory)),
    'entries': inventory
}
coverage_raw = J(coverage)
write('source-inventory-and-coverage72.json', coverage_raw)
nodes = []
for node, (role, description) in node_specs.items():
    nodes.append({'id': node, 'role': role, 'description': description,
                  'source_math_ids': [entry['math_id'] for entry in inventory if entry.get('node_id') == node],
                  'implementation_proved_by_this_task': False})
assert sum(len(node['source_math_ids']) for node in nodes) == node_count
edges = [
    ('S02-real-Hilbert', 'S04-corrector-definition', 'Real inner-product and centered-space interpretation.'),
    ('S03-components-polar', 'S04-corrector-definition', 'Both arguments belong to the same centered macroscopic space.'),
    ('S04-corrector-definition', 'S08-expand-cancel', 'Exact quadratic functional to expand.'),
    ('S06-same-root-inverse', 'S08-expand-cancel', 'Inverse equations and symmetry permit the source simplification.'),
    ('S06-same-root-inverse', 'S09-linear-simplify', 'Commutation, adjoint symmetry and A^2+Gamma^2=I reduce the linear term.'),
    ('S06-same-root-inverse', 'S10-quadratic-simplify', 'Selfadjoint square-sum identity reduces the quadratic term.'),
    ('S08-expand-cancel', 'P72-perturbation', 'Expand at an arbitrary paired shift in the same centered space.'),
    ('S09-linear-simplify', 'P72-perturbation', 'The linear result is inner(u,Inv r).'),
    ('S10-quadratic-simplify', 'P72-perturbation', 'The quadratic result is ||r||^2/2.'),
    ('P72-perturbation', 'S11-B28-consumer', 'Instantiate at actual u=g_P,v=g_V,r=r_rho only after B27 is established.'),
    ('S07-actual-B27', 'S11-B28-consumer', 'Identify actual Kf components with that paired shift.'),
    ('S05-ideal-B21', 'S11-B28-consumer', 'Supply the other signed ideal-step corrector change.'),
    ('S12-B17-B29-B30', 'S14-B31-error-estimates', 'Control the inverse-weighted actual perturbation; not supplied by pure algebra.'),
    ('S05-ideal-B21', 'S14-B31-error-estimates', 'Use existing actual pair-energy control, not an assumed output vector.'),
    ('S11-B28-consumer', 'S14-B31-error-estimates', 'Estimate the exact B28 identity.'),
    ('S14-B31-error-estimates', 'S15-B4-weight-closure', 'Control weighted corrector error.'),
    ('S13-B18-actual-norm', 'S15-B4-weight-closure', 'Combine actual norm dissipation with the corrector estimate.')
]
graph = {
    'schema_version': 1,
    'kind': 'independent-primary-source-proof-graph',
    'source_id': 'arXiv:2609.06905v1',
    'primary_raw_sha256': H(primary_raw),
    'source_inventory_file': 'source-inventory-and-coverage72.json',
    'source_inventory_raw_sha256': H(coverage_raw),
    'source_graph_built_from': 'Independently parsed fixed primary RAW regions/formulas and their adjacent primary prose, before current declaration/metadata inspection; no implementation Lean proof used to reconstruct this graph.',
    'candidate_blind': False,
    'nodes': nodes,
    'edges': [{'from': a, 'to': b, 'ingredient': reason} for a, b, reason in edges],
    'explicit_non_edges': [
        {'from': 'S05-ideal-B21', 'to': 'P72-perturbation', 'reason': 'Scheduling predecessor and later consumer addend, not an ingredient of pure perturbation algebra.'},
        {'from': 'S07-actual-B27', 'to': 'P72-perturbation', 'reason': 'The abstract identity quantifies arbitrary u,v,r; actual B27 is required for its actual application, not its algebraic proof.'},
        {'from': 'S12-B17-B29-B30', 'to': 'P72-perturbation', 'reason': 'Analytic error control is unnecessary for the exact identity and remains unresolved separately.'}
    ],
    'target': {
        'formula': 'C(u+Gamma0 r,v-A0 r)-C(u,v)=inner_R(u,Inv r)+||r||^2/2',
        'C': '(||u||^2-||v||^2)/2-inner_R(A0(Inv u),v)',
        'domain': 'all u,v,r in the SAME H_P,0',
        'source_status': 'Generalized extraction of printed unnumbered Ex28-Ex34, not a separately numbered paper theorem.'
    },
    'actual_consumer': {
        'anchor': 'B4 proof, B27 then B28',
        'r_rho': 'V_perpP^* [I+(1-rho)H_perpperp] f_perp = rho f_V+(1-rho) V_perpP^*(I+H_perpperp) f_perp',
        'actual_component_contract': '(Kf)_P=g_P+Gamma0 r_rho; (Kf)_V=g_V-A0 r_rho',
        'B28': 'C((Kf)_P,(Kf)_V)-C(f_P,f_V)=-||f_P||^2+||f_V||^2+inner_R(g_P,Inv r_rho)+||r_rho||^2/2',
        'consumer_compiled_or_proved_here': False
    },
    'residual': [
        'Actual H and actual half-turn Markov kernel/dynamics/adjoints/invariance/nonexplosion.',
        'Actual r,r_rho centering and actual B27 component identification; no RHS-defined output components.',
        'B17 under beta eta<=c and its B29 adjoint transfer; B30 inverse-weighted perturbation control.',
        'Actual B18 norm decay, B31 estimates, universal constants, exact weights and B3 comparison needed for full B26/B4.',
        'PBPS/SPHMC mains, implementation errors/caps, expected-query costs and actual-input composition.'
    ],
    'finite_coverage': {k: coverage[k] for k in ('finite_item_count','NODE_count','EXCLUDED_count','missing_count','duplicate_math_id_count')},
    'new_mathematical_proof_claimed': False,
    'new_SAU_claimed': False,
    'canonical_or_ledger_edits': False
}
graph_raw = J(graph)
write('source-proof-graph72.json', graph_raw)

declaration_lines = [
    ('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorChange.lean', [1,11,18,138]),
    ('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean', [1,2,6,11,115]),
    ('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean', [18,135]),
    ('AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean', [17,125]),
    ('AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorBound.lean', [1,15,21]),
    ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean', [352,362]),
    ('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Basic.lean', [59,409,435])
]
line_pins = []
for relative, selected in declaration_lines:
    # Stop before the body of the last selected theorem. No whole-module
    # source or proof BODY is needed or retained as an input payload.
    with (BASE / relative).open('rb') as handle:
        for index, raw in enumerate(handle, 1):
            if index in selected:
                line_pins.append({'path': str(BASE / relative), 'line': index,
                                  'exact_line': raw.decode('utf-8').rstrip('\r\n'),
                                  'raw_sha256': H(raw), 'lf_only_sha256': H(raw.replace(b'\r\n',b'\n'))})
            if index >= max(selected):
                break
assert len(line_pins) == sum(len(selected) for _, selected in declaration_lines)
metadata_paths = [
    'runs/20261007-companion-priority/pbps-corrector-change-preproof71/independent-header-source71/stageA.primary-input-manifest.json',
    '.agents/skills/astis-source-dependency-audit/SKILL.md',
    'docs/companion-papers-handoff.md',
    'website/content/samplewiki_companion_frontiers.json',
    'website/content/publications/pbps-actual-corrector-change.json',
    'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-corrector-change.json'
]
metadata_pins = []
for relative in metadata_paths:
    raw = (BASE / relative).read_bytes()
    metadata_pins.append({'path': str(BASE / relative), 'raw_byte_count': len(raw),
                          'raw_sha256': H(raw), 'lf_only_sha256': H(raw.replace(b'\r\n',b'\n')),
                          'role': 'Locator/process/exposure/name context only; not mathematical proof authority for source graph72.'})
exposure = {
    'schema_version': 1,
    'source_text_visible': True,
    'source_identity_visible': True,
    'blind_decode72_eligible': False,
    'candidate_blind': False,
    'preexisting_exposure': ['Anonymous full71 type reconstructed in the previous closed task.', 'New task message suggested the candidate perturbation formula.'],
    'new_task_read_order': ['Source-region locator and stageA input locator; process handoff.', 'Fixed RAW primary regions and exact B4/parent formulas; independently verify RAW slices.', 'Current declaration names, selected pinned Mathlib names, execution/frontier/publication metadata.'],
    'publication_exposure_after_primary': 'An rg metadata search exposed the existing71 source-facing statement and boundary after primary reading. No root source verdict, review artifact or repair overlay was read.',
    'existing71_theorem_BODY_read': False,
    'other_code_exposure': 'A bounded name/API rg also returned a few existing70/technical-lemma API-usage lines; none was used to construct the primary source graph or a new proof.',
    'memory_lookup': 'Lightweight MEMORY.md registry search only, for repository orientation; no prior rollout or prior semantic verdict used as mathematical evidence.',
    'skill_used': '.agents/skills/astis-source-dependency-audit/SKILL.md',
    'skill_output_location_override': 'The direct task restricts all writes to this new owned directory, so no canonical cited-results, proof-obligation, ledger or frontier edit was made.',
    'source_body_implementation_or_compiler_invoked': False,
    'Lean_proof_search_performed': False,
    'new_SAU_claimed': False,
    'new_VERIFIED_transition': False,
    'declaration_line_pins': line_pins,
    'metadata_raw_lf_pins': metadata_pins,
    'bounded_duplicate_name_search': {
        'scope': ['AutoSamplingTheory/ExampleCases/ProximalBPS', 'AutoSamplingTheory/TechnicalLemmas/Analysis'],
        'pattern': '^(theorem|lemma|private theorem|private lemma).*(perturb|corrector|shift)',
        'relevant_names_found': ['actual_sharp_corrector_bound', 'actual_corrector_change', 'quadratic_corrector_bound_of_square_identity'],
        'exact_perturbation_name_established': False,
        'absence_proof': False
    },
    'readiness': {
        'classification': 'local-lemma',
        'root_supplied_checkpoint': 'actual71 B21 is the scheduling predecessor; this task does not re-verify its implementation.',
        'source_ready': 'The exact algebra needs only same-map centered operator properties already present in the supplied71 type and source parents.',
        'frontier_warning': 'Current frontier metadata still says claimed/not implemented. This task neither treats that stale text as current mathematical truth nor edits it.',
        'new_compile_or_independent_verification': False,
        'no_external_analytic_dependency_for_this_target': True,
        'no_SLT_port_needed': True
    }
}
exposure_raw = J(exposure)
write('exposure-and-reuse72.json', exposure_raw)

header_start = proposal.index('  theorem quadratic_corrector_perturbation')
header_end = proposal.index('\n\nThis is an uncompiled proposed Lean header', header_start)
header = proposal[header_start:header_end]
payload = {
    'schema_version': 1,
    'task_kind': 'READ_ONLY_SOURCE_FIRST_PREPROOF_PLANNING_ONLY',
    'writer_actual_pid': PID,
    'source_id': 'arXiv:2609.06905v1',
    'primary_raw_sha256': H(primary_raw),
    'primary_lf_only_sha256': H(primary_raw.replace(b'\r\n',b'\n')),
    'source_text_visible': True,
    'blind_decode72_eligible': False,
    'candidate_blind': False,
    'fixed_primary_read': True,
    'target': {
        'name_proposal': 'quadratic_corrector_perturbation',
        'classification': 'local-lemma; same-witness actual-input integration required when implemented',
        'C': 'C(u,v)=(||u||^2-||v||^2)/2-inner_R(A0(Inv u),v)',
        'statement': 'For all u,v,r in the SAME H_P,0: C(u+Gamma0 r,v-A0 r)-C(u,v)=inner_R(u,Inv r)+||r||^2/2.',
        'source_anchor': 'B4 proof, unnumbered A2.Ex28-A2.Ex34 between printed B27 and B28',
        'source_generalization_boundary': 'Abstracted algebra from the printed actual g_P,g_V,r_rho expansion; no assertion of actual H/K/r_rho construction.',
        'uncompiled_header_proposal': header,
        'same_centered_map_parents': ['IsSelfAdjoint A0', 'IsSelfAdjoint Gamma0', 'IsSelfAdjoint Inv', 'Commute A0 Inv', 'Inv*Gamma0=I', 'Gamma0*Inv=I', 'A0*A0+Gamma0*Gamma0=I'],
        'caller_contract_if_actualized': ['0<alpha', 'alpha<=beta', 'V is globally C2', 'two global Hessian quadratic-form bounds as one caller condition', '0<eta', 'beta*eta<=1'],
        'additional_public_callers_permitted': [],
        'generic_header_claimed_logically_irredundant': False,
        'proof_supplied': False,
        'Lean_implementation_written': False,
        'compiled': False,
        'SAU_claimed': False,
        'VERIFIED': False
    },
    'B21_dependency_distinction': 'B21 is the scheduling predecessor and the other B28 addend, not a logical parent of the pure perturbation identity.',
    'actual_consumer': graph['actual_consumer'],
    'residual': graph['residual'],
    'full_B4_claimed': False,
    'new_canonical_or_ledger_edits': False,
    'complete_named_payloads': [
        {'name': 'next-edge-proposal72.utf8.txt', 'raw_sha256': H(proposal_raw), 'role': 'Complete human-readable target, sufficient uncompiled header, source formulas, actual consumer and residual.'},
        {'name': 'source-inventory-and-coverage72.json', 'raw_sha256': H(coverage_raw), 'role': 'Complete finite 263-item NODE/EXCLUDED coverage with exact primary spans and native RAW/LF hashes.'},
        {'name': 'source-proof-graph72.json', 'raw_sha256': H(graph_raw), 'role': 'Independent source-ingredient graph, actual consumer, explicit non-edges and residual.'},
        {'name': 'input-finite-pins72.json', 'raw_sha256': H(pins_raw), 'role': 'Six complete finite locator/primary/region RAW-LF pins; no huge historical copies.'},
        {'name': 'exposure-and-reuse72.json', 'raw_sha256': H(exposure_raw), 'role': 'Exposure declaration, header/API line pins, bounded name scan and readiness limits.'}
    ],
    'counts': {'primary_regions': 4, 'region_math_items': 255, 'supplementary_math_items': 8, 'finite_source_items': 263, 'NODE': node_count, 'EXCLUDED': excluded_count, 'missing': 0, 'source_graph_nodes': len(nodes), 'source_graph_edges': len(edges), 'raw_lf_input_pins': 6},
    'unresolved_scope': 'No missing finite source classification. Actual mathematics listed in residual remains unproved by this planning task.'
}
payload_raw = J(payload)
write('preproof72.payload.json', payload_raw)
pre_manifest = initial | {'source-inventory-and-coverage72.json', 'source-proof-graph72.json', 'exposure-and-reuse72.json', 'preproof72.payload.json'}
assert {p.name for p in OUT.iterdir()} == pre_manifest
assert len(pre_manifest) == 7
entries = []
for name in sorted(pre_manifest):
    raw = (OUT / name).read_bytes()
    entries.append({'name': name, 'raw_byte_count': len(raw), 'raw_sha256': H(raw), 'lf_only_sha256': H(raw.replace(b'\r\n',b'\n'))})
manifest = {
    'schema_version': 1,
    'task_kind': payload['task_kind'],
    'writer_actual_pid': PID,
    'source_text_visible': True,
    'blind_decode72_eligible': False,
    'primary_raw_sha256': H(primary_raw),
    'primary_lf_only_sha256': H(primary_raw.replace(b'\r\n',b'\n')),
    'complete_payload': 'preproof72.payload.json',
    'complete_proposal': 'next-edge-proposal72.utf8.txt',
    'complete_source_graph': 'source-proof-graph72.json',
    'complete_finite_coverage': 'source-inventory-and-coverage72.json',
    'complete_input_pins': 'input-finite-pins72.json',
    'counts': payload['counts'],
    'manifest_entry_count': len(entries),
    'covered_file_count_excluding_lease': 8,
    'owned_file_count_including_lease': 9,
    'files': entries,
    'closure_lease': 'lease.final72.json',
    'no_proof_or_implementation_claim': True
}
manifest_raw = J(manifest)
write('manifest72.json', manifest_raw)
covered_names = pre_manifest | {'manifest72.json'}
assert {p.name for p in OUT.iterdir()} == covered_names and len(covered_names) == 8
covered = []
for name in sorted(covered_names):
    raw = (OUT / name).read_bytes()
    covered.append({'name': name, 'raw_byte_count': len(raw), 'raw_sha256': H(raw), 'lf_only_sha256': H(raw.replace(b'\r\n',b'\n'))})
closed = {
    'schema_version': 1,
    'status': 'CLOSED_LAST',
    'writer_actual_pid': PID,
    'last_owned_write': True,
    'source_text_visible': True,
    'blind_decode72_eligible': False,
    'owned_directory': str(OUT),
    'covered_file_count': 8,
    'owned_file_count_including_lease': 9,
    'manifest_raw_sha256': H(manifest_raw),
    'covered_files': covered,
    'excluded_self': 'lease.final72.json',
    'post_close_policy': 'No subsequent owned writes; separate external read-only verification only.'
}
closed_raw = J(closed)
summary = {'writer_actual_pid': PID, 'status': 'CLOSED_LAST', 'counts': payload['counts'],
           'owned_file_count': 9, 'covered_file_count': 8,
           'manifest_raw_sha256': H(manifest_raw), 'payload_raw_sha256': H(payload_raw),
           'proposal_raw_sha256': H(proposal_raw), 'source_graph_raw_sha256': H(graph_raw),
           'coverage_raw_sha256': H(coverage_raw), 'lease_raw_sha256': H(closed_raw)}
# Final write to the owned directory. After this point only print precomputed data.
write('lease.final72.json', closed_raw)
print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
