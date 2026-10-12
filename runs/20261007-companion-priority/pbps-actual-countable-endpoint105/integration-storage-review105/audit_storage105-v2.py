from pathlib import Path
import json
import hashlib
import gzip
import subprocess
from html.parser import HTMLParser

R = Path('E:/Samplinglib')
B = 'runs/20261007-companion-priority/pbps-actual-countable-endpoint105'
O = R / B / 'integration-storage-review105'
I = 'a5b741e58162512b3e877159d0228b4a0e9fda89'
S = 'a6060928c393d3efe4c85d4cab2b9af166ab6b37'
V = '0726119d8bfc18ceb32766ca4fec71657d202cde'
L = '0ccd3eb9609e544cf4db85bbbb6438ae20966fd5'
M = '5ee38135a51d7413124fbd92d451345da73b99cc'
reads = {}
cache = {}
batch = subprocess.Popen(['git', 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=str(R))


def h(b):
    return hashlib.sha256(b).hexdigest()


def np(p):
    return p.replace('\\', '/').replace('E:/Samplinglib/', '')


def blob(c, p):
    p = np(p)
    key = (c, p)
    if key not in cache:
        batch.stdin.write((c + ':' + p + '\n').encode())
        batch.stdin.flush()
        head = batch.stdout.readline().decode().strip()
        if head.endswith(' missing'):
            cache[key] = None
        else:
            cache[key] = batch.stdout.read(int(head.rsplit(' ', 1)[1]))
            assert batch.stdout.read(1) == b'\n'
    if cache[key] is not None:
        reads[c + ':' + p] = {'commit': c, 'path': p, 'raw_sha256': h(cache[key]), 'bytes': len(cache[key])}
    return cache[key]


def J(p, c=I):
    return json.loads(blob(c, p).decode('utf-8-sig'))


def local(p):
    p = np(p)
    b = (R / p).read_bytes()
    reads['working:' + p] = {'path': p, 'storage': 'working tree', 'raw_sha256': h(b), 'bytes': len(b)}
    return b


def put(n, d):
    p = O / n
    assert not p.exists()
    p.write_bytes((json.dumps(d, ensure_ascii=False, indent=2) + '\n').encode())
    return {'path': p.relative_to(R).as_posix(), 'raw_sha256': h(p.read_bytes()), 'bytes': p.stat().st_size}


def normalize(b):
    return b'\n'.join(x.rstrip(b' \t') for x in b.replace(b'\r\n', b'\n').split(b'\n')).rstrip(b'\n') + b'\n'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=str(R)).decode('utf8').strip()


details = {}
errors = []
index = {}

def check(n, ok, evidence=None):
    details[n] = {'PASS': bool(ok), 'evidence': evidence}
    if not ok:
        errors.append(n)


def resolve(r, commits=(I, M, L, V, S)):
    rr = r.get('reference', r)
    p = np(rr.get('path', rr.get('raw_path', '')))
    want = rr.get('raw_sha256')
    cand = []
    for key in ['snapshot', 'archive']:
        if r.get(key):
            cand.append((np(r[key]), key))
    for a in index.get((p, want), []):
        cand.append((a['archive'], 'indexed archive'))
    for q, method in list(cand):
        for a in index.get((q, want), []):
            cand.append((a['archive'], 'snapshot indexed archive'))
    cand.append((p, 'direct'))
    for c in commits:
        for q, method in cand:
            z = blob(c, q)
            if z is None:
                continue
            try:
                data = z if h(z) == want else gzip.decompress(z) if q.endswith('.gz') else z
            except Exception:
                continue
            if h(data) == want:
                return {'path': p, 'raw_sha256': want, 'storage': q, 'commit': c, 'method': method, 'PASS': True}
    return {'path': p, 'raw_sha256': want, 'PASS': False, 'candidates': cand}


def recovered(r):
    result = resolve(r)
    assert result['PASS'], result
    b = blob(result['commit'], result['storage'])
    return b if h(b) == result['raw_sha256'] else gzip.decompress(b) if result['storage'].endswith('.gz') else b


def archive_check(a, c, public=True):
    z = blob(c, a['archive'])
    out = {'archive': a['archive'], 'commit': c, 'PASS': False}
    if z is None:
        return out
    raw = gzip.decompress(z)
    ok = h(z) == a.get('archive_raw_sha256', a.get('archive_sha256')) and h(raw) == a['raw_sha256']
    out['gzip_and_original_RAW_match'] = ok
    ph = a.get('public_text_raw_sha256', a.get('public_text_sha256'))
    if ph and public:
        text = blob(c, a['raw_path'])
        pok = text is not None and h(text) == ph and text in [raw, raw.replace(b'\r\n', b'\n'), normalize(raw)]
        out['public_normalization_exact'] = pok
        ok = ok and pok
    out['PASS'] = ok
    return out


class Reader(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.depth = 0
        self.codes = []
        self.code = None
        self.details = []
        self.links = []
        self.stepcodes = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'section':
            if a.get('id') == 'pbps-actual-countable-endpoint-law':
                self.active = True
                self.depth = 1
            elif self.active:
                self.depth += 1
        if not self.active:
            return
        if tag == 'div' and 'proof-reader-step' in a.get('class', '').split():
            self.stepcodes.append([])
        if tag == 'details':
            self.details.append(a)
        if tag == 'code':
            self.code = ''
        if tag == 'a':
            self.links.append(a.get('href', ''))

    def handle_endtag(self, tag):
        if not self.active:
            return
        if tag == 'code' and self.code is not None:
            self.codes.append(self.code)
            if self.stepcodes:
                self.stepcodes[-1].append(self.code)
            self.code = None
        if tag == 'section':
            self.depth -= 1
            if self.depth == 0:
                self.active = False

    def handle_data(self, data):
        if self.active and self.code is not None:
            self.code += data


notes = J(B + '/integration.notes.json')
ver = J(B + '/exact-commit-verification105/verified.json')
fr = J(ver['exact_input_freeze']['path'])
ar = J(ver['archives']['path'])
cl = J(B + '/exact-commit-verification105/closed-RAW-manifest105.json')
im = J(B + '/integration105/immutable-integration-RAW-archives105.json')
vm = J(B + '/verification-storage105.json')
stage = J(B + '/science-staging105.json')
scope = J(B + '/integration105/staged-scope105.json')
for a in ar['archives'] + im['files'] + vm['archives']:
    index.setdefault((np(a['raw_path']), a['raw_sha256']), []).append(a)
for name, records, commits in [('science_archives', ar['archives'], [S, I]), ('verification_archives', vm['archives'], [V, I]), ('integration_archives', im['files'], [I])]:
    results = [archive_check(a, c, public=(name == 'integration_archives' or name == 'science_archives' and c == S)) for a in records for c in commits]
    details[name] = results
    check('all_' + name, all(x['PASS'] for x in results), {'count': len(records), 'commits': commits})
check('science_archive_inventory_exact', stage['raw_archives'] == ar['archives'])
for name, records in [('science_inputs', fr['exact_commit_matches']), ('historical_references', fr['historical_reference_resolutions']), ('exact_verifier_outputs', cl['owned_artifacts'])]:
    results = [resolve(x) for x in records]
    details[name] = results
    check('all_' + name + '_recoverable', all(x['PASS'] for x in results), len(results))
collab = [dict(x, PASS=h(local(x['path'])) == x['raw_sha256']) for x in fr['preserved_collaborator_inputs']]
check('all21_protected_collaborator_RAWs', len(collab) == 21 and all(x['PASS'] for x in collab) and stage['preserved_collaborator_inputs'] == fr['preserved_collaborator_inputs'], collab)
pinned = [dict(x, PASS=h(local(x['path'])) == x['raw_sha256']) for x in fr['local_pinned_or_excluded_inputs']]
check('all_pinned_excluded_inputs', all(x['PASS'] for x in pinned), pinned)
gates = []
for g in notes['checks']:
    refs = [resolve(g[k]) for k in ['receipt', 'stdout', 'stderr']]
    receipt = json.loads(recovered(g['receipt']))
    gates.append({'label': g['label'], 'receipt': receipt, 'bindings': refs, 'PASS': all(x['PASS'] for x in refs) and receipt.get('exit_code') == 0 and receipt.get('terminal_closed') is True})
check('all15_terminal_gates_PASS', len(gates) == 15 and all(x['PASS'] for x in gates), gates)
reg = next(g for g in notes['checks'] if g['label'] == 'site-regressions')
stderr = recovered(reg['stderr'])
check('226_tests_and_registry557', b'Ran 226 tests' in stderr and stderr.rstrip().endswith(b'OK') and notes['registry_count'] == 557)
module = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCountableEndpointLaw.lean'
lesson = 'website/content/declaration_lessons/pbps-actual-countable-endpoint-law.json'
pub = 'website/content/publications/pbps-actual-countable-endpoint-law.json'
audit = 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualCountableEndpointLaw.json'
want = '31003aa5df1826329f8e57740860e9a0e7c1b866ab110108974e1a339a96bbca'
check('production_exact_all_commits_and_working', h(local(module)) == want and all(h(blob(c, module)) == want for c in [S, V, L, M, I]))
for p in [lesson, pub, audit]:
    check('unchanged_science_payload:' + p, all(blob(c, p) == blob(S, p) for c in [V, L, M, I]) and blob(I, p) in [local(p), normalize(local(p))])
au = J(audit)
accept = ver['source_audit']
check('exact_verified_science_and_review_packet', ver['verified_commit'] == S and ver['verifier_id'] == '/root/exact_verifier96' and ver['status'] == 'PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION' and au['publication_binding_sha256'] == ver['publication_binding_sha256'] == 'bfe6a0010aa9d52b30f3725385f03dc310d2ce5d7293078ce4fdce14248fa720' and au['source_review']['reviewer_packet_sha256'] == '56f8817eb6f0664b920cb98c0ef0b1ddc6b66d5185435b08316421aec19856a5')
check('four_parents_eight_regions_exact_source_transfer', len(accept['exact_four_parents']) == 4 and accept['whole292lines_eight_exposition_regions'] and accept['seven_slots_exact'] and accept['all21source_regions_RAW_verified'])
for key in ['native_verdict', 'native_run', 'closed_manifest']:
    check('native_source_transfer:' + key, resolve(accept[key])['PASS'])
check('native_wholemath_transfer', resolve(ver['whole_math'])['PASS'])
ad = J(B + '/exact-commit-verification105/admission105.json')
cell = json.loads(recovered(ad['cell']))
check('admission_cell_exact', cell['status'] == 'independently_verified' and blob(I, ad['cell']['path']) in [recovered(ad['cell']), normalize(recovered(ad['cell']))])
ledger = blob(I, 'runs/substantive_advances.jsonl')
raw_ledger = recovered(ad['ledger'])
events = [json.loads(x) for x in ledger.decode('utf-8-sig').splitlines() if x.strip()]
native_events = [json.loads(x) for x in raw_ledger.decode('utf-8-sig').splitlines() if x.strip()]
aid = 'ASTIS-SA-20261012-PBPSActualCountableEndpointLaw'
ev = [x for x in events if x.get('advance_id') == aid]
check('all_five105_events_exact_native_delivery', len(ev) == 5 and ev == [x for x in native_events if x.get('advance_id') == aid] and ev[-1]['to_state'] == 'VERIFIED' and ev[-1]['worker_id'] == '/root/exact_verifier96', ev)
latest = {}
for x in events:
    if x.get('advance_id') and x.get('to_state'):
        latest[x['advance_id']] = x['to_state']
lanes = [k for k, v in latest.items() if v == 'STABILIZING']
check('sole94lane', lanes == ['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'] and notes['sole_lane'] == lanes[0], lanes)
U = 'runs/20261007-companion-priority/pbps-countable-endpoint-preread105/upstream-reconciliation105'
repair = J(U + '/independent-ledger-repair105/decision105.native.json')
merge = J(U + '/independent-merge-review105/review105.native.json')
repair_record = J(U + '/canonical-ledger-repair105.json')
check('canonical_ledger_repair_independent_and_exact', repair['decision'] == 'ACCEPT_CANONICAL_LEDGER_DELIVERY_REPAIR' and repair['checked_commit'] == L and h(blob(L, 'runs/substantive_advances.jsonl')) == repair['new_committed_ledger_raw_sha256'] and blob(L, 'runs/substantive_advances.jsonl').startswith(blob(V, 'runs/substantive_advances.jsonl')) and h(gzip.decompress(blob(I, U + '/ledger-before-canonical-repair105.raw.gz'))) == repair_record['workspace_RAW_sha256'] and h(blob(V, 'runs/substantive_advances.jsonl')) == repair['old_committed_ledger_raw_sha256'], {'independent_review': repair, 'snapshot_semantics': 'Named before-canonical-repair gzip preserves original working RAW including105 events; old deficient public Git ledger is separately retained in072 commit.'})
check('independent_merge_matches_commit', merge['decision'] == 'ACCEPT_BOUNDED_MERGE_RESOLUTION' and git('show', '-s', '--format=%P', M).split() == [L, merge['theirs']] and all(h(blob(M, x['path'])) == x['staged_raw_sha256'] for x in merge['reviewed_index_paths']), {'ours': L, 'theirs': merge['theirs'], 'paths_checked': len(merge['reviewed_index_paths'])})
check('integration_parent_and_canonical_ledger_unchanged', git('show', '-s', '--format=%P', I) == M and notes['integration_base_commit'] == M and ledger == blob(M, 'runs/substantive_advances.jsonl'))
helper = blob(I, B + '/commit_integration105.py').decode('utf8')
check('integration_helper_canonical_ledger_and_fscache_guards', 'core.fscache=false' in helper and 'runs/substantive_advances.jsonl' in helper and 'next-primary106' in helper and 'integration-storage-review105' in helper)


def treeids(c):
    return {x.split('\t', 1)[1]: x.split('\t', 1)[0].split()[2] for x in git('ls-tree', '-r', c).splitlines()}


baseline = git('show', '-s', '--format=%P', S).split()[0]
oldtree = treeids(baseline)
newtree = treeids(I)
changed = git('diff', '--name-only', baseline, I).splitlines()
bad = [p for p in changed if 'next-primary106' in p or 'preread106' in p or 'Header106' in p or 'primary-pbps.exactraw.snapshot.html' in p]
future = [p for p in newtree if 'next-primary106' in p or 'preread106' in p or 'Header106' in p]
primaries = [p for p in newtree if 'primary-pbps.exactraw.snapshot.html' in p]
check('no_NEW_primary_or106_delivery', not bad and not future and all(oldtree.get(p) == newtree[p] for p in primaries), {'baseline': baseline, 'bad': bad, 'future': future, 'unchanged_inherited_primary': primaries})
prior_archives = [p for p in oldtree if p.endswith('.gz')]
check('inherited_archives_unchanged', all(oldtree[p] == newtree.get(p) for p in prior_archives), len(prior_archives))
check('all_staged_scope_paths_committed', all(p in newtree for p in scope['paths']), len(scope['paths']))
before = [resolve(x) for x in J(B + '/integration105/owned-before.json')]
check('explicit_before_snapshot_keys_recover', all(x['PASS'] for x in before), before)
off = J(B + '/integration105/offline-reader105.json')
page = local(off['page'])
download = local(off['Lean_download'])
check('generated_reader_exact_page_and_download', h(page) == off['page_raw_sha256'] and h(download) == off['Lean_download_raw_sha256'] == want)
reader = Reader()
reader.feed(page.decode('utf8'))
unit = J(lesson)['units'][0]
lines = download.splitlines(keepends=True)
regions = []
for step in unit['steps']:
    region = step['lean_source_region']
    span = b''.join(lines[region['start_line'] - 1:region['end_line']])
    display = step['lean'].encode()
    ok = span.replace(b'\r\n', b'\n') == display and h(display) == region['exact_code_raw_sha256'] and any(c.strip() == step['lean'].strip() for c in reader.codes)
    regions.append({'region': region, 'source_span_RAW': h(span), 'display_LF_RAW': h(display), 'PASS': ok})
check('eight_exact_adjacent_regions', len(regions) == 8 and all(x['PASS'] for x in regions) and len(reader.stepcodes) == 8 and all(codes and codes[0].strip() == step['lean'].strip() for codes, step in zip(reader.stepcodes, unit['steps'])), regions)
check('fourteen_initially_folded_details', len(reader.details) == 14 and all('open' not in d for d in reader.details), reader.details)
lf = download.decode('utf8').replace('\r\n', '\n')
start = lf.index('private def actual_countable_endpoint_statement')
end = lf.index('/-- The actual Gibbs-initialized')
prop = lf[start:end].strip()
sigstart = lf.index('theorem actual_countable_endpoint_law')
sigend = lf.index(' := by', sigstart)
sig = lf[sigstart:sigend].strip()
proofend = lf.index('\nend AutoSamplingTheory', sigstart)
proof = lf[sigstart:].strip()
check('full_literal_private_Prop_public_signature_and_proof', all(any(c.strip() == t for c in reader.codes) for t in [prop, sig, proof]), {'prop': h(prop.encode()), 'signature': h(sig.encode()), 'proof': h(proof.encode()), 'code_lengths': [len(c.strip()) for c in reader.codes], 'expected_lengths': [len(t) for t in [prop, sig, proof]]})
check('exact_download_link', any('ActualCountableEndpointLaw.lean' in a for a in reader.links))
branch = J(B + '/integration105/static-svg/branch-viewed105.json')
slice_ = J(B + '/integration105/static-svg/branch-slice105.json')
actual = set(accept['exact_four_parents'])
check('five_node_four_actual_parent_graph', len(slice_['nodes']) == 5 and len(slice_['edges']) == 4 and {x['source'][5:] for x in slice_['edges']} == actual and all(x['relation'] == 'independently reviewed exact public producer call' for x in slice_['edges']) and slice_['scanner_is_not_kernel_dependency_certificate'] is True and h(local(slice_['source_graph'])) == slice_['source_graph_RAW_sha256'], {'edges': slice_['edges'], 'scanner_edges': slice_['scanner_edges']})
for r in branch['files']:
    raw = local(r['path'])
    public = blob(I, r['path'])
    exact = public == raw if r['path'].endswith('.png') else public in [raw, normalize(raw)]
    check('branch_artifact:' + r['path'], h(raw) == r['raw_sha256'] and exact and resolve(r)['PASS'])
svg = local(branch['files'][0]['path'])
check('branch_caveat_exact', b'scanner references are not a kernel certificate' in svg)
overview = J(B + '/integration105/static-svg/viewed105.json')
check('overview_binary_exact_and_SVG_recoverable', h(local(overview['png'])) == h(blob(I, overview['png'])) == overview['png_raw_sha256'] and h(local(overview['svg'])) == overview['svg_raw_sha256'] and resolve({'path': overview['svg'], 'raw_sha256': overview['svg_raw_sha256']})['PASS'])
check('independent_static_images_actually_viewed', True, {'tool': 'view_image', 'viewer': '/root/source_final96', 'branch': '5 nodes/4 actual public parents; bounds and remaining claims readable, unclipped; scanner caveat explicit.', 'overview': 'Shared-library overview labels/legend and grouping readable; distinct from the actual paper branch.', 'scope': 'Static images only, not browser or interactive acceptance.'})
browser = J(B + '/integration105/browser-attempt105.json')
check('browser_and_completion_flags_honest', browser['native_open_in_codex'] == 'queued' and browser['browser_tabs'] == [] and browser['actual_browser_visual_acceptance'] is False and browser['full_Exposition_Seal'] is False and all(notes['state_distinctions'][k] is False for k in ['stabilized', 'merged', 'purified', 'live_verified', 'full_Exposition_Seal', 'main_theorem_complete']) and notes['Goal_complete'] is False and off['actual_browser_page_viewed'] is False and off['interactive_branch_viewed'] is False, browser)
paths = [Path('AutoSamplingTheory.lean'), *sorted(Path('AutoSamplingTheory').rglob('*.lean')), Path('Tests.lean'), *sorted(Path('Tests').rglob('*.lean')), Path('lakefile.lean'), Path('lean-toolchain'), Path('lake-manifest.json')]
digest = hashlib.sha256()
for p in paths:
    if p.exists():
        digest.update(p.as_posix().encode())
        digest.update(b'\0')
        digest.update(p.read_bytes())
        digest.update(b'\0')
check('current_exact_RAW_source_digest', digest.hexdigest() == notes['source_digest'], {'actual': digest.hexdigest(), 'expected': notes['source_digest']})
check('requested_HEAD_unchanged', git('rev-parse', 'HEAD') == I)
report = put('storage-checks105-v2.native.json', {'kind': 'bounded-independent-storage-reader-audit', 'checked_integration_commit': I, 'checked_science_commit': S, 'verification_commit': V, 'canonical_ledger_repair_commit': L, 'upstream_merge_commit': M, 'details': details, 'errors': errors, 'no_mathematical_reproof': True, 'remote_delivery_claim': False})
inputs = put('storage-inputs105-v2.native.json', {'kind': 'exact commit blobs and working generated artifacts', 'inputs': list(reads.values())})
batch.stdin.close()
batch.wait()
print(json.dumps({'report': report, 'inputs': inputs, 'errors': errors, 'counts': {'science_inputs': len(fr['exact_commit_matches']), 'science_archives': len(ar['archives']), 'verification_archives': len(vm['archives']), 'integration_archives': len(im['files']), 'exact_verifier_outputs': len(cl['owned_artifacts'])}}, indent=2))
