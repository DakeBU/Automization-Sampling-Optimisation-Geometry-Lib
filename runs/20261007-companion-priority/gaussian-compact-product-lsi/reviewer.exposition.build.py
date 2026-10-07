import datetime, hashlib, html, json, pathlib, re, subprocess
from html.parser import HTMLParser

ROOT = pathlib.Path('E:/Samplinglib')
RUN = ROOT / 'runs/20261007-companion-priority/gaussian-compact-product-lsi'
BASE = 'runs/20261007-companion-priority/'
COMMIT = '46b0b1f23fb3c83de7014ac825950c810d5055a8'
PROOF = 'eaf29841eab8b3d4df5b9419f658fbcc1dda39f3'
ACTOR = 'gaussian_domain_preproof_reviewer_29'
MODULE = 'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactProductLogSobolev'
DECL = MODULE + '.compact_gaussian_pi_logSobolev'
PROD = 'AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianCompactProductLogSobolev.lean'
TEST = 'Tests/GaussianCompactProductLogSobolev.lean'
LESSON = 'website/content/declaration_lessons/gaussian-compact-product-lsi.json'
COMPANION = '_site/example-cases/samplewiki/companions/smoothed-picard-hmc.html'
MODPAGE = '_site/modules/autosamplingtheory-technicallemmas-functionalinequalities-gaussiancompactproductlogsobolev.html'
TESTPAGE = '_site/modules/tests-gaussiancompactproductlogsobolev.html'
GRAPH = '_site/data/underlying-lean-graph.json'

def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
def load(p): return json.loads((ROOT / p).read_text(encoding='utf-8'))
def dump(name, obj):
    encoded = (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if (RUN / name).exists():
        assert (RUN / name).read_bytes() == encoded, 'Immutable prior output mismatch ' + name
        return
    with (RUN / name).open('xb') as f:
        f.write(encoded)
def rel(p): return p.relative_to(ROOT).as_posix()
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=str(ROOT)).decode().strip() == COMMIT
integration = load(BASE + 'gaussian-compact-product-lsi/integration.json')
freeze = load(BASE + 'gaussian-compact-product-lsi/math-freeze.json')
freeze_checks = []
for item in freeze['inputs']:
    raw = (ROOT / item['path']).read_bytes()
    ok = sha(raw) == item['raw_sha256'] and sha(lf(raw)) == item['lf_sha256']
    assert ok, item['path']
    freeze_checks.append({'path': item['path'], 'raw_LF_match': ok, 'scope': 'Byte invariance only; graph author does not validate own topology'})

paths = [PROD, TEST, LESSON,
 'website/content/publications/gaussian-compact-product-lsi.json',
 'research-wiki/frontier-cells/ASTIS-SW-SPHMC-gaussian-compact-product-lsi.json',
 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianCompactProductLogSobolev.json',
 COMPANION, MODPAGE, TESTPAGE, GRAPH,
 BASE + 'gaussian-compact-product-preproof/signature.prospective.txt',
 BASE + 'gaussian-compact-product-preproof/statement-seals.accepted.json',
 BASE + 'gaussian-compact-lsi/preproof/signature.prospective.txt',
 BASE + 'gaussian-product-entropy-preproof/signature.prospective.txt',
 BASE + 'gaussian-compact-product-lsi/publication-plan.json',
 BASE + 'gaussian-compact-product-lsi/math-freeze.json',
 BASE + 'gaussian-compact-product-lsi/integration.json',
 BASE + 'gaussian-compact-product-lsi/verified.json',
 BASE + 'gaussian-compact-product-lsi/whole-proof-review/math.review.json',
 BASE + 'gaussian-compact-product-lsi/source.0.review.json',
 BASE + 'gaussian-compact-product-lsi/reviewer.repository.ProofSeal.json',
 BASE + 'gaussian-compact-product-lsi/graph.0.json',
 BASE + 'gaussian-compact-product-source-topology-review/source-topology-review.repaired.json',
 'AutoSamplingTheory/TechnicalLemmas.lean', 'Tests/Basic.lean', 'lean-toolchain', 'lake-manifest.json']
gate_checks = []
for item in integration['checks']:
    for kind in ['status', 'log']:
        if isinstance(item.get(kind), dict):
            binding = item[kind]
            raw = (ROOT / binding['path']).read_bytes()
            assert sha(raw) == binding['raw_sha256'] and sha(lf(raw)) == binding['lf_sha256'], binding['path']
            paths.append(binding['path'])
    gate_checks.append({'label': item['label'], 'bindings_match': True, 'existing_evidence_only': True})
paths = list(dict.fromkeys(paths))
inputs = []
for i, path in enumerate(paths):
    raw = (ROOT / path).read_bytes()
    normalized = lf(raw)
    prefix = 'reviewer.exposition.input.%03d' % i
    for suffix, content in [('.raw.snapshot', raw), ('.lf.snapshot', normalized)]:
        snapshot = RUN / (prefix + suffix)
        if snapshot.exists(): assert snapshot.read_bytes() == content, 'Immutable input snapshot mismatch'
        else:
            with snapshot.open('xb') as f: f.write(content)
    blob = subprocess.run(['git', 'show', COMMIT + ':' + path], cwd=str(ROOT), capture_output=True)
    tracked = blob.returncode == 0
    if tracked: assert lf(blob.stdout) == normalized, 'Working/Git mismatch ' + path
    inputs.append({'path': path, 'raw_sha256': sha(raw), 'lf_sha256': sha(normalized), 'bytes': len(raw),
      'raw_snapshot': rel(RUN / (prefix + '.raw.snapshot')), 'lf_snapshot': rel(RUN / (prefix + '.lf.snapshot')),
      'git_at_checked_commit': tracked, 'git_blob_sha256': sha(blob.stdout) if tracked else None,
      'working_equals_git_LF': True if tracked else None,
      'read_scope': 'Static generated artifact, not tracked deployment' if path.startswith('_site/') else
       ('Complete fresh mathematical read' if path in [PROD, TEST] else 'Bounded interface/metadata/receipt or exact hash binding')})
dump('reviewer.exposition.inputs.json', {'checked_commit': COMMIT, 'inputs': inputs, 'math_freeze_byte_checks': freeze_checks})

class Pres(HTMLParser):
    def __init__(self): super().__init__(); self.pres = []; self.current = None
    def handle_starttag(self, tag, attrs):
        if tag == 'pre': self.current = ''
    def handle_data(self, data):
        if self.current is not None: self.current += data
    def handle_endtag(self, tag):
        if tag == 'pre' and self.current is not None:
            self.pres.append(self.current); self.current = None
def pres(path):
    p = Pres(); p.feed((ROOT / path).read_text(encoding='utf-8')); return p.pres
production = lf((ROOT / PROD).read_bytes()).decode('utf-8')
tests = lf((ROOT / TEST).read_bytes()).decode('utf-8')
module_full = any(x.strip() == production.strip() for x in pres(MODPAGE))
tests_full = any(x.strip() == tests.strip() for x in pres(TESTPAGE))
assert module_full and tests_full
public_start = production.index('theorem compact_gaussian_pi_logSobolev')
public_full = production[public_start:]
companion_pres = pres(COMPANION)
assert any(x.strip() == public_full.strip() for x in companion_pres)
signature = (ROOT / (BASE + 'gaussian-compact-product-preproof/signature.prospective.txt')).read_text(encoding='utf-8')
assert sha(signature.encode()) == 'fc859f057a9242675d2a769fa3b2dbbd7b66764fdbe429f608decf0018511d50'
assert public_full.startswith(signature.rstrip() + ' := by')
page = html.unescape((ROOT / COMPANION).read_text(encoding='utf-8'))
unit = load(LESSON)['units'][0]
steps = unit['steps']
assert len(steps) == 7
formula_checks = []
for i, step in enumerate(steps):
    assert step['formula'] in page, 'Missing formula ' + str(i + 1)
    formula_checks.append({'step': i + 1, 'title': step['title'], 'formula': step['formula'], 'actual_HTML_present': True})
pos = page.index('theorem compact_gaussian_pi_logSobolev')
details = page[page.rfind('<details', 0, pos):pos]
assert 'inline-lean-statement' in details and not re.search(r'<details[^>]*\bopen\b', details)
proofpos = page.index(':= by', pos)
proofdetails = page[page.rfind('<details', 0, proofpos):proofpos]
assert 'inline-lean-proof' in proofdetails and not re.search(r'<details[^>]*\bopen\b', proofdetails)
assert 'eaf29841eab8' in page
assert '../../../modules/autosamplingtheory-technicallemmas-functionalinequalities-gaussiancompactproductlogsobolev.html#complete-module-source' in page[pos:proofpos + 5000]

graph = load(GRAPH)
branch = [e for e in graph['edges'] if e.get('source') == 'module:' + MODULE or e.get('target') == 'module:' + MODULE]
imports = [e['source'] for e in branch if e.get('target') == 'module:' + MODULE and e.get('relation') == 'imports']
assert set(imports) == {
 'module:AutoSamplingTheory.TechnicalLemmas.InformationTheory.ProductEntropy',
 'module:AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactLogSobolev'}
dump('reviewer.exposition.branch.json', {'checked_commit': COMMIT, 'graph_path': GRAPH, 'branch': branch,
 'direct_ASTIS_imports': imports, 'truth_contract': 'Imports/declares only; source correspondence is separately labelled, not a compiled theorem implication',
 'no_fabricated_Bernoulli_formal_parent': True, 'private_providers_displayed_in_full_module_not_claimed_as_individual_graph_nodes': True})
checks = {'schema_version': 1, 'checked_commit': COMMIT, 'proof_commit': PROOF,
 'mathematical_checks': [
  {'region': 'production21-50; lesson1', 'result': 'Actual square/Phi/each coordinate-square/full finite sum L1 internally produced from C2 and compact support before integral operations'},
  {'region': 'production92-105; Tests12-35; lesson2', 'result': 'Fin0 singleton probability retains arbitrary constant mass; homogeneous entropy0 and empty energy0. Zero observer/all dimensions and positive-mass dimension0 tests are actual calls'},
  {'region': 'production52-90,107-141; lesson3-4', 'result': 'Actual measure-preserving Fin.cons law and closed-embedding slice support; original scalar/tail C2. Literal coordinate derivative identification; no Pi sup operator norm/Euclidean gradient conflation'},
  {'region': 'production143-200; lesson5', 'result': 'Internal bounded measurable nonnegative F=f squared; actual39 orientation J_A+J_B<=J_F+Phi(m) yields Entjoint<=integrated original conditional entropies. Slice/marginal/outer L1 precedes subtraction/Fubini, including zero fibers/mass'},
  {'region': 'production202-298; lesson6-7', 'result': 'Strict Nat dimension induction on original tail slice and scalar38 on original scalar slice; true outer L1 before integral_mono; head+tail sum and transport give exact coefficient2 without RMS marginal regularity'},
  {'region': 'Tests37-107', 'result': 'Actual compact C2 signed scalar and signed nonseparable n2 observers; actual sign checks; meaningful producer tests. Existing standard3 evidence is independent proof provenance, no compiler run here'}],
 'static_reader_checks': {'seven_formula_checks': formula_checks, 'folded_exact_public_statement': True,
  'folded_exact_complete_public_proof': True, 'complete_production_module_verbatim': module_full,
  'complete_Test_module_verbatim': tests_full, 'all_eight_private_provider_contexts_in_module_page': True,
  'companion_private_providers_inline': False, 'companion_Test_tails_inline': False,
  'module_context_link_present': True, 'generated_stamp': 'codex/sphmc-standardized-rgo · eaf29841eab8',
  'stamp_boundary': 'Pre-shared-commit generated working artifact, exact raw/LF bound. Accepted static content does not imply a rebuilt46b page, browser rendering, deployment or live verification',
  'scalar_gamma_notation': 'Lesson gamma1(a) is the scalar gaussianReal0 1; FinPi gamma_n is the coordinate product. Actual Fin.cons law keeps the carriers explicit'},
 'existing_gate_binding_checks': gate_checks,
 'conservative_metadata_notes': ['Historical pending-admission prose is preserved as historical status, not used to deny the later independent receipts',
  'Publication default fullLean/Test delivery description is not treated as completed companion Test delivery; explicit gaps remain OPEN'],
 'exposure_attestation': {'sourcegraph41_frozen_CLOSED_before_first40body_Test_exposure': True,
  'sourcegraph41_run_sha256': '1d878af4feb56f5233ad609ffa10ef061ee6abf2c0fd7c6e8a102512616974f0',
  'root_prose_author_distinct_from_reviewer': True, 'no_sourcegraph_selfvalidation': True, 'no_source_blind_or_parent_blind_independence_claim': True},
 'canonical_mutations': [], 'compiler_started': False, 'site_rerender_started': False, 'browser_started': False, 'blockers': []}
dump('reviewer.exposition.checks.json', checks)
index = {x['path']: x for x in inputs}
def binding(path): return {k:v for k,v in index[path].items() if k in ['path','raw_sha256','lf_sha256','bytes']}
seal = {'schema_version': 1, 'verdict': 'ACCEPTED_SCOPED_EXPOSITION_SEAL', 'status': 'accepted-scoped',
 'reviewer': ACTOR, 'checked_commit': COMMIT, 'proof_commit': PROOF,
 'scope': 'Bounded STATIC root-authored compact finite-Pi Gaussian LSI40 exposition, seven formulas and exact generated public code/full module and Test pages',
 'independent_from_prose_author': True,
 'source_graph_author_history': 'Reviewer authored40/41 source graphs; topology/source fidelity is separately admitted by phase. This seal neither selfvalidates them nor re-proves mathematics. 40 production/Test exposure followed41 graph CLOSED freeze.',
 'mathematical_declaration': DECL,
 'mathematical_exposition': 'For every n including0 and signed C2 compactly supported real f on Fin n -> Real, true variance-one product Gaussian square/Phi/coordinate-energy L1 is internal; homogeneous entropy is at most2 times the integral of the full coordinate-square sum. Original-slice binary entropy and scalar LSI induction match the complete actual proof, including zero mass.',
 'formula_proof_steps': formula_checks, 'checks': rel(RUN / 'reviewer.exposition.checks.json'),
 'graph_branch': rel(RUN / 'reviewer.exposition.branch.json'), 'input_bindings': rel(RUN / 'reviewer.exposition.inputs.json'),
 'blockers': [],
 'mathematical_and_source_provenance': {'independent_verified_proof': binding(BASE + 'gaussian-compact-product-lsi/verified.json'),
  'independent_whole_mathematics': binding(BASE + 'gaussian-compact-product-lsi/whole-proof-review/math.review.json'),
  'independent_source_fidelity': binding(BASE + 'gaussian-compact-product-lsi/source.0.review.json'),
  'independent_source_topology': binding(BASE + 'gaussian-compact-product-source-topology-review/source-topology-review.repaired.json'),
  'shared_repository_ProofSeal': binding(BASE + 'gaussian-compact-product-lsi/reviewer.repository.ProofSeal.json'),
  'integration_existing_gates': binding(BASE + 'gaussian-compact-product-lsi/integration.json'),
  'source_and_Test_freeze_unchanged': True, 'fresh_compiler_by_this_reviewer': False},
 'FULL_READER_DELIVERY_GAP': {'status': 'OPEN', 'items': [
  'Actual Test tails and eight private provider proofs are not inline in the companion; full exact module/Test pages exist, and the module context link is checked',
  'Companion Test-page linking and source-copy/download behavior not independently certified or executed',
  'Paper/book/chapter bundles not delivered or checked',
  'Browser/device rendering and fold/copy/download interactions not tested',
  'Own40 remote CI, main merge, deployment and live verification not inferred from static source artifacts',
  'Postmerge PURIFIED and human-facing completeness remain OPEN']},
 'remaining_truth_boundary': ['Finite-Hilbert basis/law/Parseval adapter is separate from this Pi coordinate theorem',
  'Noncompact32 sqrt-density cutoff/entropy/energy closure, full Gaussian W12 LSI, GaussianT2, FIRST4.6, main/work/cost/composition remain OPEN'],
 'lease': rel(RUN / 'reviewer.exposition.lease.json'), 'canonical_mutations': []}
dump('ExpositionSeal.json', seal)
outputs = ['reviewer.exposition.inputs.json','reviewer.exposition.branch.json','reviewer.exposition.checks.json','ExpositionSeal.json','reviewer.exposition.build.py']
run = {'schema_version': 1, 'actor': ACTOR, 'checked_commit': COMMIT, 'proof_commit': PROOF,
 'deterministic_payload': {'inputs': [{k:x[k] for k in ['path','raw_sha256','lf_sha256']} for x in inputs],
 'outputs': [{'path': rel(RUN / p), 'raw_sha256': sha((RUN / p).read_bytes()), 'lf_sha256': sha(lf((RUN / p).read_bytes()))} for p in outputs]},
 'verdict': seal['verdict'], 'all_leases_CLOSED': True, 'compiler_NEVER_STARTED': True, 'canonical_mutations': []}
run['run_sha256'] = sha(json.dumps(run['deterministic_payload'], ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
dump('reviewer.exposition.run.json', run)
for entry in inputs:
    now = (ROOT / entry['path']).read_bytes()
    assert sha(now) == entry['raw_sha256'] and sha(lf(now)) == entry['lf_sha256']
leasepath = RUN / 'reviewer.exposition.lease.json'
lease = json.loads(leasepath.read_text(encoding='utf-8'))
lease.update({'status': 'CLOSED', 'read_lease': 'CLOSED', 'write_lease': 'CLOSED', 'Python_lease': 'CLOSED',
 'compiler_lease': 'CLOSED', 'compiler_started': False, 'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verdict': seal['verdict'], 'run_sha256': run['run_sha256'], 'inputs_rechecked_unchanged': True})
leasepath.write_bytes((json.dumps(lease, ensure_ascii=False, indent=2)+'\n').encode())
dump('reviewer.exposition.lease.closed.json', lease)
print(json.dumps({'verdict': seal['verdict'], 'seal_raw_sha256': sha((RUN / 'ExpositionSeal.json').read_bytes()),
 'run_sha256': run['run_sha256'], 'inputs': len(inputs), 'freeze_inputs': len(freeze_checks), 'leases': 'ALL_CLOSED'}, ensure_ascii=False))
