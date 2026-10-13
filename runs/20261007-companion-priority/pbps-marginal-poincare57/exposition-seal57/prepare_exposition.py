from pathlib import Path
from html.parser import HTMLParser
import json, hashlib, re, struct, subprocess, sys, datetime, os

ROOT = Path('E:/Samplinglib')
B = ROOT / 'runs/20261007-companion-priority/pbps-marginal-poincare57'
OUT = B / 'exposition-seal57'
SCI = 'e8a9044ba5a945eaa4b4aecd110b63494fe6c68e'
HEAD = 'f311e4296fb5295a2e56e3214d3bd2585f849dcf'
ACTOR = '/root/fresh_blind_decoder56'
PRODUCTION = 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean'
TEST = 'Tests/GaussianMarginalPoincare.lean'
RECIPE = 'SHA256 UTF8 json.dumps(COMPLETE native object minus ONLY complete_object_sha256, ensure_ascii=False, sort_keys=True, separators=(comma,colon)); no newline. No component-payload alias.'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8')

def read(path):
    with Path(path).open('rb') as stream:
        return stream.read()

def pin(path):
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    raw = read(path)
    lf = raw.replace(b'\r\n', b'\n')
    return {'path': str(path).replace('\\', '/'), 'bytes': len(raw), 'raw_sha256': sha(raw), 'lf_bytes': len(lf), 'lf_sha256': sha(lf)}

def emit_raw(name, raw):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('wb') as stream:
        stream.write(raw)
    assert read(path) == raw
    return pin(path)

def write(name, obj):
    obj = dict(obj)
    assert 'complete_object_sha256' not in obj
    obj['complete_object_sha256'] = sha(canonical(obj))
    receipt = emit_raw(name, (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf8'))
    back = json.loads(read(OUT / name))
    value = back.pop('complete_object_sha256')
    assert sha(canonical(back)) == value
    return receipt

inputs = []
input_by_path = {}

def take(path):
    receipt = pin(path)
    if receipt['path'] not in input_by_path:
        raw = read(receipt['path'])
        number = len(inputs)
        label = f'{number:03d}.{Path(receipt["path"]).name}'
        raw_snapshot = emit_raw('inputs/' + label + '.raw.snapshot', raw)
        lf_snapshot = emit_raw('inputs/' + label + '.lf.snapshot', raw.replace(b'\r\n', b'\n'))
        entry = {'input': receipt, 'raw_snapshot': raw_snapshot, 'lf_snapshot': lf_snapshot}
        inputs.append(entry)
        input_by_path[receipt['path']] = receipt
    return read(receipt['path'])

assert not (OUT / 'lease.json').exists(), 'Never reopen an existing CLOSED seal.'
assert not (OUT / 'lease.open.json').exists(), 'Do not overwrite previous preparation.'
write('lease.open.json', {'schema_version': 1, 'status': 'OPEN', 'actor': ACTOR, 'scope': 'Independent scoped ExpositionSeal57 only', 'opened_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'read': 'OPEN', 'write': 'OPEN', 'Python': 'OPEN', 'compiler': 'NOT_STARTED_CLOSED', 'browser': 'NOT_STARTED_BY_REVIEWER_CLOSED', 'sole_write_root': str(OUT).replace('\\', '/'), 'final_lease_written_last': True, 'hash_recipe': RECIPE})

for relative in ['docs/theorem-publication-protocol.md', 'docs/proof-digestion-protocol.md', 'docs/evidence-routed-memory-protocol.md', '.agents/skills/astis-semantic-roundtrip/SKILL.md', 'runs/20261007-companion-priority/pbps-rough-mean-gradient56/exposition-seal56/prepare_exposition.py', 'runs/20261007-companion-priority/pbps-rough-mean-gradient56/exposition-seal56/finalize_exposition.py']:
    take(relative)
for name in ['publication-plan.json', 'verified.json', 'integration.notes.json', 'visual.inspection.json', 'root.integration.0.lease.json', 'source.review.lease.json', 'source.0.reviewer-packet.json']:
    take(B / name)
for name in ['result0.json', 'reviewer.source.run.json', 'source.review.json', 'complete.json', 'publication.binding.payload.json']:
    take(B / 'source-review57' / name)
primary = ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57'
for name in ['primary.contract.json', 'A4.SS2.text.txt', 'A3.SS1.text.txt', 'A3.SS2.text.txt']:
    take(primary / name)
for relative in [PRODUCTION, TEST, 'lean-toolchain', 'lake-manifest.json', 'website/content/publications/gaussian-marginal-poincare.json', 'website/content/declaration_lessons/gaussian-marginal-poincare.json', 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-GaussianMarginalPoincare.json']:
    take(relative)

notes = json.loads(read(B / 'integration.notes.json'))
checks = []
for receipt in notes['checks']:
    actual = pin(receipt['path'])
    assert all(actual[key] == receipt[key] for key in ['bytes', 'raw_sha256', 'lf_sha256'])
    take(receipt['path'])
for status_path in sorted(B.glob('integration.0.*.status.json')):
    status = json.loads(read(status_path))
    assert status['exit_code'] == 0 and status['proof_commit'] == SCI
    log_path = Path(str(status_path).replace('.status.json', '.log'))
    assert sha(read(log_path)) == status['log_raw_sha256']
    checks.append({'name': status_path.name, 'status': pin(status_path), 'log': pin(log_path), 'exit_code': 0})
assert len(checks) == 12
assert (notes['registry_count'], notes['root_jobs'], notes['test_jobs']) == (498, 9160, 9449)
integration_lease = json.loads(read(B / 'root.integration.0.lease.json'))
assert integration_lease['status'] == 'CLOSED' and integration_lease['exit_code'] == 0

native_source_checks = []
for name, field in [('source.review.json', 'content_self_sha256'), ('complete.json', 'content_self_sha256'), ('reviewer.source.run.json', 'run_sha256'), ('publication.binding.payload.json', 'content_self_sha256')]:
    obj = json.loads(read(B / 'source-review57' / name))
    value = obj.pop(field)
    assert sha(canonical(obj)) == value
    native_source_checks.append({'path': str(B / 'source-review57' / name).replace('\\', '/'), 'excluded_top_level_self_field': field, 'complete_native_minus_self_sha256': value})
source_result = json.loads(read(B / 'source-review57/result0.json'))
source_run = json.loads(read(B / 'source-review57/reviewer.source.run.json'))
assert source_result['review_run_sha256'] == source_run['run_sha256']
assert source_result['reviewer'] != ACTOR and source_result['verdict'] == 'equivalent-after-elaboration'
assert len(source_result['semantic_slots']) == 7 and len(source_result['deltas']) == 3
assert all(not delta['blocking'] for delta in source_result['deltas'])
source_lease = json.loads(read(B / 'source.review.lease.json'))
value = source_lease.pop('content_self_sha256')
assert sha(canonical(source_lease)) == value and source_lease['status'] == 'CLOSED'
binding = json.loads(read(B / 'source-review57/publication.binding.payload.json'))
named_binding_hash = sha(canonical(binding['payload']))
assert named_binding_hash == binding['named_payload_sha256'] == 'cd7704313084137b33ef2cff81e754a65cfe0cee0af14f8eddcacef27de8442e'

publication = json.loads(read(ROOT / 'website/content/publications/gaussian-marginal-poincare.json'))['items'][0]
lesson = json.loads(read(ROOT / 'website/content/declaration_lessons/gaussian-marginal-poincare.json'))['units'][0]
audit = json.loads(read(ROOT / 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-GaussianMarginalPoincare.json'))
assert publication['statement'] == lesson['statement']
assert binding['payload']['lesson'] == lesson
assert audit['publication_binding_sha256'] == named_binding_hash and audit['source_review']['state'] == 'accepted'
assert len(lesson['steps']) == 6
source_report = json.loads(read(B / 'source-review57/source.review.json'))
assert [step['formula'] for step in source_report['six_steps_review']] == [step['formula'] for step in lesson['steps']]

images = []
for path in sorted((B / 'visual-inspection57').iterdir()):
    take(path)
    if path.suffix == '.png':
        raw = read(path)
        assert raw[:8] == b'\x89PNG\r\n\x1a\n'
        dimensions = struct.unpack('>II', raw[16:24])
        assert dimensions == (1440, 1800)
        images.append({'pin': pin(path), 'width': 1440, 'height': 1800, 'independent_actual_view': 'Reviewer personally viewed via view_image tool before authoring this report; display resized to 1408x1760, original portable file remains 1440x1800.'})
assert len(images) == 4
captures = []
for prefix in ['cdp', 'proof']:
    capture = json.loads(read(B / 'visual-inspection57' / (prefix + '.capture.json')))
    assert capture['ownedBrowserExit'] == {'code': 0, 'signal': None}
    for record in capture['records']:
        portable = B / 'visual-inspection57' / f'{prefix}.{record["label"]}.png'
        # Review portable captures only; no reopening browser or original hidden capture directories.
        inspection = json.loads(read(B / 'visual-inspection57' / f'{prefix}.{record["label"]}.inspect.json'))
        assert all(inspection[key] == value for key, value in record.items() if key not in ['label', 'png_path'])
        captures.append({'portable': pin(portable), 'native_capture': pin(B / 'visual-inspection57' / (prefix + '.capture.json')), 'inspection_matches_capture': True, 'owned_capture_browser_exit_code': 0, 'recorded_original_path_not_read_by_this_reviewer': record['png_path']})
for artifact in json.loads(read(B / 'visual.inspection.json'))['artifacts']:
    actual = pin(artifact['portable_path'])
    assert actual['bytes'] == artifact['bytes'] and actual['raw_sha256'] == artifact['raw_sha256']

def git(*args):
    result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True)
    assert result.returncode == 0, (args, result.stderr.decode(errors='replace'))
    return result.stdout

assert git('rev-parse', 'HEAD').decode().strip() == HEAD and HEAD != SCI
git('merge-base', '--is-ancestor', SCI, HEAD)
git_evidence = []
for relative in [PRODUCTION, TEST, 'website/content/publications/gaussian-marginal-poincare.json', 'website/content/declaration_lessons/gaussian-marginal-poincare.json']:
    science = git('show', SCI + ':' + relative)
    integration = git('show', HEAD + ':' + relative)
    current = read(ROOT / relative)
    assert science == integration
    assert science.replace(b'\r\n', b'\n') == current.replace(b'\r\n', b'\n')
    science_receipt = emit_raw(Path(relative).name + '.science.raw.snapshot', science)
    git_evidence.append({'path': relative, 'science_git_blob_sha256': sha(science), 'integration_git_blob_sha256': sha(integration), 'current': pin(relative), 'science_snapshot': science_receipt, 'unchanged_science_to_integration': True})
lean = read(ROOT / PRODUCTION).decode('utf8').replace('\r\n', '\n')
assert binding['payload']['current_lean_module'] == lean
assert binding['payload']['file'] == sha(lean.encode('utf8'))
for key, path in [('toolchain', 'lean-toolchain'), ('dependencies', 'lake-manifest.json')]:
    assert binding['payload'][key] == sha(read(ROOT / path).decode('utf8').replace('\r\n', '\n').replace('\r', '\n').encode('utf8'))
a = lean.index('theorem actual_gaussian_marginal_centered_poincare')
b = lean.index(' := by', a)
signature = (lean[a:b].rstrip() + '\n').encode('utf8')
assert len(signature) == 1244 and sha(signature) == 'e706b4e6c3c07f58a090ee86cb51dd91be2f11afe707db653737e4983c7181e9'
emit_raw('production.header.normalized.lf.snapshot.lean', signature)

html_path = ROOT / '_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html'
take(html_path)
s = read(html_path).decode('utf8')
start = s.index('<section id="gaussian-marginal-poincare"')
depth = 0
for match in re.finditer(r'</?section\b[^>]*>', s[start:]):
    depth += -1 if match.group().startswith('</') else 1
    if depth == 0:
        end = start + match.end()
        break
node = s[start:end]
node_receipt = emit_raw('rendered.companion.node.raw.snapshot.html', node.encode('utf8'))

class Inspect(HTMLParser):
    def __init__(self):
        super().__init__()
        self.classes, self.details, self.codes, self.active, self.buffer = {}, [], [], False, []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for cls in attrs.get('class', '').split():
            self.classes[cls] = self.classes.get(cls, 0) + 1
        if tag == 'details':
            self.details.append(attrs)
        if tag == 'code' and attrs.get('class') == 'language-lean':
            self.active, self.buffer = True, []
    def handle_data(self, data):
        if self.active:
            self.buffer.append(data)
    def handle_endtag(self, tag):
        if tag == 'code' and self.active:
            self.codes.append(''.join(self.buffer))
            self.active = False

parser = Inspect()
parser.feed(node)
assert len(parser.details) == 11 and all('open' not in detail for detail in parser.details)
assert parser.classes['proof-reader-equation'] == 8 and parser.classes['proof-reader-step'] == 6 and len(parser.codes) == 2
assert parser.codes[0].strip() == lean[a:b].strip()
assert parser.codes[1].strip() == lean[a:].strip()
for number, code in enumerate(parser.codes):
    emit_raw(f'rendered.exact-lean-{number}.lf.snapshot.lean', (code + '\n').encode('utf8'))
for step in lesson['steps']:
    assert step['title'] in node

graph_path = ROOT / '_site/data/underlying-lean-graph.json'
take(graph_path)
take(ROOT / '_site/lean-foundations.html')
graph = json.loads(read(graph_path))
focus = 'decl:AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare'
module = 'module:AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare'
edges = [edge for edge in graph['edges'] if focus in (edge['source'], edge['target']) or module in (edge['source'], edge['target'])]
ids = {focus, module}
for edge in edges:
    ids.update([edge['source'], edge['target']])
nodes = [entry for entry in graph['nodes'] if entry['id'] in ids]
graph_receipt = write('rendered.graph-focus.slice.json', {'schema_version': 1, 'focus': focus, 'module': module, 'nodes': nodes, 'edges': edges, 'reference_contract': graph['reference_contract'], 'container': pin(graph_path), 'slice_rule': 'Only incident edges to exact declaration or its owning module and endpoint nodes. Solid imports/ownership are not theorem implication; scanned reference edges are incomplete.'})

verification = {'schema_version': 1, 'artifact_kind': 'native-exposition57-verification', 'science_commit': SCI, 'integration_commit': HEAD, 'science_ancestor_of_integration': True, 'git_files': git_evidence, 'checks': checks, 'registry_count': 498, 'root_jobs': 9160, 'test_jobs': 9449, 'native_source_checks': native_source_checks, 'source_run_complete_minus_run_sha256': source_run['run_sha256'], 'named_publication_binding_payload_sha256': named_binding_hash, 'publication_binding_wrapper_complete_minus_content_self_sha256': binding['content_self_sha256'], 'named_payload_is_distinct_from_wrapper': True, 'rendered': {'node': node_receipt, 'node_bytes': len(node.encode('utf8')), 'formula_containers': 8, 'proof_steps': 6, 'all_details_initially_closed': 11, 'step_lean_details': 6, 'exact_statement_and_proof_details': 2, 'additional_folded_reader_ledgers': 3, 'statement_exact': True, 'whole_theorem_proof_exact': True, 'signature_bytes': 1244, 'signature_sha256': sha(signature)}, 'images': images, 'captures': captures, 'site': {'companion_container': pin(html_path), 'selected_section_character_offsets': [start, end], 'graph_container': pin(graph_path), 'graph_focus_slice': graph_receipt}, 'limits': 'All twelve existing gate status/log byte receipts checked; no new compiler/build/browser. Four bounded desktop captures independently viewed; no exhaustive/mobile/live/main/full-paper/PURIFIED admission.'}
write('verification.json', verification)
report = {'schema_version': 1, 'artifact_kind': 'independent-scoped-exposition-seal', 'reviewer': ACTOR, 'independent_from_proving_writer_and_root_visual_creator': True, 'independent_from_source57_reviewer': True, 'verdict': 'ACCEPT_SCOPED_DESKTOP_EXPOSITION_WITH_RETAINED_DEBT', 'blockers': [], 'science_commit': SCI, 'integration_commit': HEAD, 'publication_binding_sha256': named_binding_hash, 'statement_signature_sha256': sha(signature), 'source_review_reused': pin(B / 'source-review57/result0.json'), 'scope': 'Actual Gaussian Gibbs marginal compact-gradient closure centered Poincare, with actual SAME56 T/K and actual55 stationary reflected law yielding the real L2 C3 and sharp C4 rho consumer; four portable desktop captures and exact focused graph only.', 'source_nodes': ['PBPS2609.06905v1 Eq2.13', 'PBPS2609.06905v1 AppendixD.2 D6/D9/D10', 'PBPS2609.06905v1 AppendixC.1 C2/C3/C4 and density/gradient-closedness passage'], 'lean_nodes': {'target': focus, 'production_parents': publication['proof_digestion']['existing_substrate'], 'consumer': 'Tests.GaussianMarginalPoincare.actual_same_mean_centered_contraction', 'consumer_parents': ['AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient.actual_rough_mean_gradient', 'AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean.actual_macroscopic_l2_mean']}, 'lossless_expansion': {'objects_and_assumptions': 'Actual mu=volume.tilted(-V), independent standard-Gaussian pushforward J and nu=J.snd; finite real Hilbert/Borel/canonical volume including rank0 extension expressly disclosed. C2, 0<alpha<=beta, both GLOBAL Hessian bounds, eta>0 and betaeta<=1 retained. Actual normalization, posterior moment/covariance and sharp curvature inputs produced internally, no caller certificates.', 'quantifiers_and_domain': 'One densely defined real compact-smooth gradient G is chosen before ALL centered z in the genuine closed domain. Exact graph is represented by the SAME smooth compact scalar phi and its actual Euclidean gradient AE nu; closability/closedness mean graph closure. E finite-dimensional does not make L2 finite-dimensional. Centering restricts the PI conclusion, rather than an extra mathematical premise for G.', 'constants': 'm_eta=alpha/(1+alphaeta), M_eta=beta/(1+betaeta); PI reciprocal is 1/alpha+eta. SAME56 sharp c=(1-alphaeta)^2/[4(1+alphaeta)] and rho=(1-alphaeta)/(1+alphaeta) are exact. Original cap gives nonnegative rho; alphaeta=1 is included without dividing by 1-alphaeta.', 'same56_actual_input_consumer': 'Both exact compact-core graph characterizations force G56=G57, so SAME56 (Tu,Ku) belongs to the actual Gbar graph. Actual55 reflected Markov conditional law Lambda=nu compProd S with both marginals nu, SAME56 literal AE means and actual L2->L1/disintegration derive integralTu=integralu internally. Then centered u gives centered Tu, C3 applies on its genuine derivative Ku, and sharp energy yields C4 rho. No invented centered-output/domain/stationarity certificate.', 'six_formula_steps': [{'number': index + 1, 'title': step['title'], 'formula': step['formula'], 'expand_to_lean': step['lean']} for index, step in enumerate(lesson['steps'])], 'folded_lean': 'Six corresponding Lean-step references plus exact normalized statement and entire theorem/proof remain initially folded next to readable mathematical statement/proof; two exact code blocks verified against science/integration bytes. Three further folded reader ledgers explain total eleven disclosures.'}, 'semantic_deltas_preserved': source_result['deltas'], 'graph_assessment': 'Focused compiled declaration and ownership/parent references visible. The screenshot legend explicitly distinguishes solid imports/declaration ownership from dashed incomplete scanned references and conceptual correspondences. Long qualified labels wrap heavily. No conceptual mirror promoted into formal implication.', 'presentation_debt': [{'kind': 'horizontal-assumption-table-scroll', 'severity': 'nonblocking-for-scoped-desktop-seal', 'detail': 'Visible horizontal scrollbar; rightmost explanation column requires scrolling.'}, {'kind': 'dense-inline-notation', 'severity': 'reader-polish-debt', 'detail': 'C2/L2/Hessian/AE/source anchors are dense inline text; six displayed proof formulas remain legible.'}, {'kind': 'tall-companion-page', 'severity': 'reader-backpressure-debt', 'detail': 'Native capture records bodyHeight326235px; bounded seal does not inspect entire page.'}, {'kind': 'graph-qualified-label-wrapping', 'severity': 'reader-navigation-debt', 'detail': 'Declaration/source labels wrap across many lines in focused card; reference graph is zoomed densely.'}, {'kind': 'repeated-title-and-statement', 'severity': 'nonblocking', 'detail': 'Publication section and authored lesson repeat their heading, statement and main formula.'}], 'remaining_boundary': ['Separately defined source weak-H1 equivalence', 'Onto full actual macro range identification', 'Full B13/Gamma/inverse/domain/spectral/half-turn', 'Dynamics/mixing/main results/errors/query cost', 'PBPS-SPHMC actual-input composition and other Goal papers', 'Postmerge purification, exhaustive reader/mobile/live/main acceptance'], 'historical_negatives_retained': source_report['retained_negatives'], 'historical_decoder56': 'This actor originally decoded statement56 source-text-blind. This separately authorized exposition57 now reads source and complete production/Test bodies; earlier decoder blindness remains historical and is not extended to this source-visible review.', 'structural_recipe56_only': 'Read prepare/finalize56 scripts only for artifact structure and closure/hash discipline; no old56 verdict replay.', 'compiler': 'NOT_STARTED_CLOSED', 'browser': 'NOT_STARTED_BY_REVIEWER_CLOSED', 'repairs': [], 'whole_goal_completed': False, 'purified': False, 'main_or_live_delivery': False, 'hash_recipe': RECIPE}
write('exposition.review.json', report)
write('input.manifest.json', {'schema_version': 1, 'artifact_kind': 'native-exposition57-input-manifest', 'inputs': inputs, 'input_count': len(inputs), 'receipt_recipe': 'Raw SHA256 and bytes over actual readbacks; LF replaces only raw CRLF bytes by LF. Both independent raw/LF snapshots are read back byte-exact. Paths are native strings.', 'preparation_disclosure': 'Preceding foreground tools read bounded protocols, recipe56 scripts, native source57/current production/Test/publication, captures and generated selected node. Filename discovery via rg (first broad filename result truncated) read paths, not unrelated source contents. This manifest pins all file-content inputs; git object reads are separately pinned to science/integration in verification.', 'own_helpers': [pin(OUT / 'prepare_exposition.py')], 'hash_recipe': RECIPE})
for entry in inputs:
    assert pin(entry['input']['path']) == entry['input']
write('input.readbacks.json', {'schema_version': 1, 'count': len(inputs), 'all_match': True, 'pins': [entry['input'] for entry in inputs], 'hash_recipe': RECIPE})
print(json.dumps({'stage': 'PREPARED', 'pid': os.getpid(), 'input_count': len(inputs), 'checks': 12, 'images_independently_viewed': 4, 'formula_steps': 6, 'node_bytes': len(node.encode('utf8')), 'graph_nodes': len(nodes), 'graph_edges': len(edges), 'verdict': report['verdict'], 'all_file_handles_closed': True, 'normal_foreground_process_exit_required': True}, ensure_ascii=False))
