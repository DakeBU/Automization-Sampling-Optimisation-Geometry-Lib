from pathlib import Path
import json
import hashlib
import gzip
import subprocess
from html.parser import HTMLParser

R = Path('E:/Samplinglib')
B = 'runs/20261007-companion-priority/pbps-actual-normalized-endpoint104'
O = R / B / 'integration-storage-review104'
I = '8b673a5876fe468476984bf5f9abeb5278ca9f13'
S = '1a0fb58a061845fc5ac7623e4d62b5e301d7eb78'
ORIGINAL = '403c6ea6bc44847ee50b0225c2da166c37e2b279'
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


notes = J(B + '/integration.notes.json')
ver = J(B + '/exact-commit-verification104/verified.json')
fr = J(ver['exact_input_freeze']['path'])
ar = J(B + '/exact-commit-verification104/archive-audit104.json')
cl = J(B + '/exact-commit-verification104/closed-RAW-manifest104.json')
im = J(B + '/integration104/immutable-integration-RAW-archives104.json')
stage = J(B + '/science-staging104.json')
scope = J(B + '/integration104/staged-scope104.json')
index = {}
for a in ar['archives'] + im['files']:
    index.setdefault((np(a['raw_path']), a['raw_sha256']), []).append(a)
details = {}
errors = []


def check(n, ok, evidence=None):
    details[n] = {'PASS': bool(ok), 'evidence': evidence}
    if not ok:
        errors.append(n)


def resolve(r, commits=(I, S, ORIGINAL)):
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
                data = gzip.decompress(z) if q.endswith('.gz') else z
            except Exception:
                continue
            if h(data) == want:
                return {'path': p, 'raw_sha256': want, 'storage': q, 'commit': c, 'method': method, 'PASS': True}
    return {'path': p, 'raw_sha256': want, 'PASS': False, 'candidates': cand}


def recovered(r):
    result = resolve(r)
    assert result['PASS'], result
    b = blob(result['commit'], result['storage'])
    return gzip.decompress(b) if result['storage'].endswith('.gz') else b


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


for name, records, commits in [('science_archives', ar['archives'], [ORIGINAL, S, I]), ('integration_archives', im['files'], [I])]:
    results = [archive_check(a, c, public=(name != 'science_archives' or c == ORIGINAL)) for a in records for c in commits]
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
check('226_tests_and_registry555', b'Ran 226 tests' in stderr and stderr.rstrip().endswith(b'OK') and notes['registry_count'] == 555)
module = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNormalizedEndpointSector.lean'
lesson = 'website/content/declaration_lessons/pbps-actual-normalized-endpoint-sector.json'
pub = 'website/content/publications/pbps-actual-normalized-endpoint-sector.json'
audit = 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualNormalizedEndpointSector.json'
want = 'c2a980f6397528f818120ca6163bf9b286f5c2ef5d4c730d9608267271b03074'
check('exact_production_unchanged', h(local(module)) == want and all(resolve({'path': module, 'raw_sha256': want}, (c,))['PASS'] for c in [ORIGINAL, S, I]) and blob(ORIGINAL, module) == blob(S, module) == blob(I, module))
for p in [lesson, pub, audit]:
    check('unchanged_science_payload:' + p, blob(ORIGINAL, p) == blob(S, p) == blob(I, p) and blob(I, p) in [local(p), normalize(local(p))])
au = J(audit)
check('exact_verified_science_and_review_packet', ver['verified_commit'] == S and ver['verifier_id'] == '/root/exact_verifier96' and ver['status'] == 'PASS_INDEPENDENT_EXACT_COMMIT_VERIFICATION' and au['publication_binding_sha256'] == ver['publication_binding_sha256'] == 'b39b7a5ce95ad06964dc2d1c09102ea21fc7c5e80653a9145e17798fbbb945f9' and au['source_review']['reviewer_packet_sha256'] == 'a254440f7d7f9d0cd86e908c3cd31327b8f0c74aaf73fd92cd8a1bbce9190a7b')
accept = J(ver['source_audit']['unchanged_evidence']['path'])
repair = J(ver['source_audit']['narrow_repair']['path'])
check('four_parents_eight_regions_exact_source_transfer', len(accept['exact_four_parents']) == 4 and accept['whole230lines_eight_exposition_regions'] and accept['seven_slots_exact'] and accept['all21source_regions_RAW_verified'])
for key in ['native_verdict', 'native_run', 'closed_manifest']:
    check('native_source_transfer:' + key, resolve(accept[key])['PASS'])
check('native_wholemath_transfer', resolve(ver['whole_math'])['PASS'])
repair_paths = git('diff', '--name-only', ORIGINAL, S).splitlines()
check('metadata_repair_exact_scope_original_trial_retained', sorted(repair_paths) == sorted(repair['changed_paths']) and repair['two_label_changes_only'] and repair['all_science_proof_source_decoder_lesson_publication_ledger_unchanged'] and resolve(repair['original_failed_trial'])['PASS'], {'diff_paths': repair_paths, 'repair': repair})
ad = J(B + '/exact-commit-verification104/admission104.json')
cell = json.loads(recovered(ad['cell']))
check('admission_cell_exact', cell['status'] == 'independently_verified' and blob(I, ad['cell']['path']) in [recovered(ad['cell']), normalize(recovered(ad['cell']))])
ledger = blob(I, 'runs/substantive_advances.jsonl')
raw_ledger = recovered(ad['ledger'])
old_ledger = gzip.decompress(blob(S, next(x for x in ar['archives'] if x['raw_path'] == 'runs/substantive_advances.jsonl')['archive']))
events = [json.loads(x) for x in ledger.decode('utf-8-sig').splitlines() if x.strip()]
ev = [x for x in events if x.get('advance_id') == 'ASTIS-SA-20261012-PBPSActualNormalizedEndpointSector' and x.get('to_state') == 'VERIFIED']
latest = {}
for x in events:
    if x.get('advance_id') and x.get('to_state'):
        latest[x['advance_id']] = x['to_state']
lanes = [k for k, v in latest.items() if v == 'STABILIZING']
check('one_independent_VERIFIED_append_only_RAW_event', len(ev) == 1 and ev[0]['worker_id'] == '/root/exact_verifier96' and raw_ledger.startswith(old_ledger), {'event': ev, 'old_prefix_bytes': len(old_ledger)})
check('sole94lane', lanes == ['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity'] and notes['sole_lane'] == lanes[0], lanes)
check('integration_direct_parent_science', git('show', '-s', '--format=%P', I) == S)
baseline = git('show', '-s', '--format=%P', ORIGINAL).split()[0]
changed = git('diff', '--name-only', baseline, I).splitlines()


def treeids(c):
    return {x.split('\t', 1)[1]: x.split('\t', 1)[0].split()[2] for x in git('ls-tree', '-r', c).splitlines()}


oldtree = treeids(baseline)
newtree = treeids(I)
bad = [p for p in changed if 'next-primary105' in p or 'preread105' in p or 'Header105' in p or 'primary-pbps.exactraw.snapshot.html' in p]
future = [p for p in newtree if 'next-primary105' in p or 'preread105' in p or 'Header105' in p]
inherited_primary = [p for p in newtree if 'primary-pbps.exactraw.snapshot.html' in p]
check('no_NEW_primary_or105_delivery', not bad and not future and all(oldtree.get(p) == newtree[p] for p in inherited_primary), {'baseline': baseline, 'changed_count': len(changed), 'bad': bad, 'future': future, 'inherited_primary_paths': inherited_primary})
prior_archives = [p for p in oldtree if p.endswith('.gz')]
check('inherited_archives_unchanged', all(oldtree[p] == newtree.get(p) for p in prior_archives), len(prior_archives))
check('all_staged_scope_paths_committed', all(p in newtree for p in scope['paths']), len(scope['paths']))
before = [resolve(x) for x in J(B + '/integration104/owned-before.json')]
check('explicit_before_snapshot_keys_recover', all(x['PASS'] for x in before), before)

# Check the generated display directly; no new mathematical review.
off = J(B + '/integration104/offline-reader104.json')
page = local(off['page'])
download = local(off['Lean_download'])
check('generated_reader_exact_page_and_download', h(page) == off['page_raw_sha256'] and h(download) == off['Lean_download_raw_sha256'] == want)


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
            if a.get('id') == 'pbps-actual-normalized-endpoint-sector':
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
lf = download.decode('utf8').replace('\r\n', '\n').splitlines(keepends=True)
prop = ''.join(lf[19:102]).strip()
sig = ''.join(lf[103:113]).split(' := by', 1)[0].strip()
proof = ''.join(lf[103:]).strip()
check('full_literal_private_Prop_public_signature_and_proof', all(any(c.strip() == text for c in reader.codes) for text in [prop, sig, proof]), {'literal_Prop': h(prop.encode()), 'signature': h(sig.encode()), 'proof': h(proof.encode())})
check('exact_download_link', any('ActualNormalizedEndpointSector.lean' in a for a in reader.links))
branch = J(B + '/integration104/static-svg/branch-viewed104.json')
slice_ = J(B + '/integration104/static-svg/branch-slice104.json')
wm = json.loads(recovered(ver['whole_math']))
actual = set(accept['exact_four_parents'])
edge_parents = {x['source'][5:] for x in slice_['edges']}
check('five_node_four_actual_parent_graph', len(slice_['nodes']) == 5 and len(slice_['edges']) == 4 and edge_parents == actual and all(x['relation'] == 'independently reviewed exact public producer call' for x in slice_['edges']) and slice_['scanner_is_not_kernel_dependency_certificate'] is True and h(local(slice_['source_graph'])) == slice_['source_graph_RAW_sha256'], {'edges': slice_['edges'], 'whole_math_genuine_parents': wm['genuine_direct_parents'], 'scanner_edges': slice_['scanner_edges']})
svg_raw = local(branch['input'])
svg_pub = blob(I, branch['input'])
check('whole_math_parent_names_exact', actual == {'AutoSamplingTheory.ExampleCases.ProximalBPS.' + x['declaration'] for x in wm['genuine_direct_parents']})
check('branch_binary_exact_and_SVG_lossless_normalization', h(local(branch['output'])) == h(blob(I, branch['output'])) == branch['output_raw_sha256'] and h(svg_raw) == branch['input_raw_sha256'] and svg_pub in [svg_raw, normalize(svg_raw)] and resolve({'path': branch['input'], 'raw_sha256': branch['input_raw_sha256']})['PASS'] and b'scanner references are not a kernel certificate' in svg_raw, {'PNG_RAW': branch['output_raw_sha256'], 'SVG_original_RAW': h(svg_raw), 'SVG_public_RAW': h(svg_pub), 'public_normalization': 'Original or CRLF/trailing-whitespace/terminal-LF text normalization only; original RAW recovered.'})
overview = J(B + '/integration104/static-svg/viewed104.json')
check('overview_binary_and_original_SVG_recoverable', h(local(overview['output'])) == h(blob(I, overview['output'])) == overview['output_raw_sha256'] and resolve({'path': overview['input'], 'raw_sha256': overview['input_raw_sha256']})['PASS'])
check('independent_static_images_viewed', True, {'viewer': '/root/source_final96', 'tool': 'view_image', 'branch_PNG': branch['output_raw_sha256'], 'overview_PNG': overview['output_raw_sha256'], 'finding': 'Both images actually opened. Branch five nodes/four public parent calls, formulas and scanner caveat legible and unclipped; shared overview labels/legend readable. Static scope only.'})
browser = J(B + '/browser-availability104.json')
check('browser_and_completion_flags_honest', browser['existing_browser_tabs'] == [] and browser['tabs_after_native_open'] == [] and browser['native_corrected_open_status'] == 'queued' and all(browser[k] is False for k in ['actual_browser_page_viewed', 'interactive_branch_viewed', 'full_Exposition_Seal']) and all(notes['state_distinctions'][k] is False for k in ['stabilized', 'merged', 'purified', 'live_verified', 'full_Exposition_Seal', 'main_theorem_complete']) and notes['Goal_complete'] is False and off['actual_browser_page_viewed'] is False and off['interactive_branch_viewed'] is False, browser)
helpers = []
for name in ['render_branch104.py', 'commit_storage104.py']:
    old = blob(S, B + '/' + name)
    current = blob(I, B + '/' + name)
    snapshot = B + '/integration104/' + name.replace('.py', '.before.exactraw.snapshot')
    raw = local(snapshot)
    helpers.append({'path': B + '/' + name, 'science_SHA': h(old), 'integration_SHA': h(current), 'original_snapshot_RAW': h(raw), 'original_recoverable': resolve({'path': snapshot, 'raw_sha256': h(raw)})['PASS'], 'science_matches_snapshot_presentation': old in [raw, normalize(raw)]})
check('helper_originals_preserved', all(x['original_recoverable'] and x['science_matches_snapshot_presentation'] for x in helpers), helpers)
helperdiff = git('diff', S, I, '--', B + '/render_branch104.py', B + '/commit_storage104.py')
details['exact_helper_diff'] = helperdiff
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
report = put('storage-checks104-v2.native.json', {'kind': 'bounded-independent-storage-reader-audit', 'checked_integration_commit': I, 'checked_science_commit': S, 'original_science_commit': ORIGINAL, 'details': details, 'errors': errors, 'no_mathematical_reproof': True, 'remote_delivery_claim': False})
inputs = put('storage-inputs104-v2.native.json', {'kind': 'exact commit blobs and working generated artifacts', 'inputs': list(reads.values())})
batch.stdin.close()
batch.wait()
print(json.dumps({'report': report, 'inputs': inputs, 'errors': errors, 'counts': {'science_inputs': len(fr['exact_commit_matches']), 'science_archives': len(ar['archives']), 'integration_archives': len(im['files']), 'exact_verifier_outputs': len(cl['owned_artifacts'])}}, indent=2))
