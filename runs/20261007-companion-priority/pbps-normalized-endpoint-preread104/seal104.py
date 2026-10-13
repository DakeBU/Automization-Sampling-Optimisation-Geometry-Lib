"""Freeze the independently reviewed actual endpoint-pair statement before proof."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess

pre = Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
source = pre.parent / 'pbps-actual-phase-normalization103/next-primary104'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()

def ref(p):
    p = Path(p)
    return dict(path=p.as_posix(), raw_sha256=sha(p.read_bytes()), bytes=p.stat().st_size)

head = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
delivery = load(pre / 'upstream-reconciliation104/postpush-merge.json')
assert head == delivery['local_head'] == delivery['remote_head'] == delivery['pr']['headRefOid']
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only']).strip()
assert load(pre / 'fetch-status104.json')['exit_code'] == 0
header = ref(pre / 'Header104.lean')
assert header['raw_sha256'] == '4fc65e051233c07d0d2272b3371fad1c1164546b51a4c313c0ec0d314b805be4'
mathp = pre / 'independent-header-math104/header-math-decision104.native.json'
sourcep = pre / 'independent-header-source104/header-source-decision104.native.json'
topologyp = pre / 'independent-header-math104/source-topology-admission104.native.json'
assert load(mathp)['decision'] == 'ACCEPT_PROSPECTIVE_MATHEMATICAL_HEADER'
assert load(topologyp)['decision'] == 'ACCEPT_BASE_PLUS_104_DELTA_TOPOLOGY_AND_BOUNDED_COVERAGE'
assert ref(mathp)['raw_sha256'] == '996ac259ceb8c96be0c449325238daf3ce1c3f1bc582986c386706ca47a18db0'
assert ref(sourcep)['raw_sha256'] == '90304031a32ac6dc2a66c27060a1f965b647e4f4b039eb15557bcafbb8fa4abe'
assert ref(topologyp)['raw_sha256'] == '9db2cd7f984bde2fc08958cfd8cc555dada8eb4301feb7136701a308aefdc828'
artifacts, bindings = [], {}

def walk(value):
    if isinstance(value, dict):
        name, digest = value.get('path'), value.get('raw_sha256')
        if isinstance(name, str) and isinstance(digest, str) and len(digest) == 64:
            p = Path(name)
            raw = p.read_bytes()
            row = dict(path=name, raw_sha256=digest)
            if 'line_start' in value and 'line_end' in value:
                raw = b''.join(raw.splitlines(keepends=True)[value['line_start'] - 1:value['line_end']])
                row.update(line_start=value['line_start'], line_end=value['line_end'])
            elif 'byte_start' in value and 'byte_end_exclusive' in value:
                raw = raw[value['byte_start']:value['byte_end_exclusive']]
                row.update(byte_start=value['byte_start'], byte_end_exclusive=value['byte_end_exclusive'])
            assert sha(raw) == digest, ('Unresolved RAW binding; diagnose before seal', name, digest, sha(raw))
            bindings[(name, digest)] = row
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)

for directory in [source, pre / 'independent-header-math104', pre / 'independent-header-source104']:
    for p in sorted(directory.rglob('*.json')):
        artifacts.append(ref(p))
        walk(load(p))
recommendation = load(source / 'recommendation104.native.json')
retrieval = load(source / 'retrieval104.native.json')
parents = [x['artifact']['path'].removesuffix('.lean').replace('/', '.') + '.' + x['declaration']
           for x in retrieval['actual_producers'].values()]
text = (pre / 'Header104.lean').read_text(encoding='utf8')
seal = dict(
    status='SEALED_BEFORE_PROOF_AFTER_INDEPENDENT_HEADER_AND_TOPOLOGY_AUDITS',
    sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), statement_version=1,
    owner='companion_root_20261005', baseline_commit=head, header=header,
    expanded_literal_Prop=text.split('def candidate', 1)[1].split('#check candidate', 1)[0].strip(),
    proposed_public_theorem='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualNormalizedEndpointSector.actual_normalized_endpoint_sector_reversal',
    source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',
    source_anchor='Appendix A.1 fixed-count change of variables and initial Eq3.1 Gibbs averaging; actual normalized endpoint-pair sector measure reversal.',
    independent_math_header=ref(mathp), independent_source_header=ref(sourcep), independent_topology=ref(topologyp),
    source_graph=ref(source / 'source-proof-graph-delta104.native.json'),
    source_coverage=ref(source / 'source-coverage-delta104.native.json'),
    primary=ref(load(source / 'primary-first104.native.json')['primary']['path']),
    all_review_artifacts_rehashed=artifacts, all_bound_RAW_inputs_rehashed=list(bindings.values()),
    binder_audit=dict(SOURCE=['hα', 'hαβ', 'hV', 'hH', 'hη', 'hβη'],
                     TYPING='Finite-dimensional real Hilbert Borel space, including rank zero.', EXCESS=[]),
    definition_audit='Thirty literal lets: unchanged20 actual algorithm definitions; R, proximal position energy, tilted law, standard Gaussian, simplex measure; terminal endpoint, endpoint-pair map, density-weighted sector, pushed-forward measure and flipped swap. Correct position-first and phase-first product orders.',
    core_delta=recommendation['single_public_conclusion'], actual_producer_plan=parents,
    consumer=recommendation['actual_consumer'],
    truth_boundary='Actual normalized fixed-count endpoint-pair measure reversal only. Countable assembly, signed bilinear identity, process invariance, Markovness, hypocoercivity, implementation error, actual expected costs and all full paper/composition results remain open.',
    proof_search_started=False, sau_claimed=False, Goal_complete=False)
target = pre / 'root.statement-seal104.json'
assert not target.exists()
target.write_text(json.dumps(seal, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('Sealed104', ref(target)['raw_sha256'], len(bindings), 'RAW bindings')
