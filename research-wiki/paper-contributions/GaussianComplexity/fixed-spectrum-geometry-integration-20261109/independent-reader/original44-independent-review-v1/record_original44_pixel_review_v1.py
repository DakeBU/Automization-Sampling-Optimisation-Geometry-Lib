"""Record completed individual ORIGINAL44 pixel inspection; no browser/API/shared edits."""
from pathlib import Path
import datetime, gzip, hashlib, json, struct, subprocess, zlib
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
B = S / 'browser/live-20261109T023719009047Z'
O = S / 'original44-independent-review-v1'
CORE = 'b3581af0fc7e517e6cf5b883f4af064ddaa72aa2'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
def pinned(ref):
    p = (R / ref['path']).resolve(); assert p.is_relative_to(R)
    raw = p.read_bytes(); assert sha(raw) == ref['sha256'], ref['path']
    return raw
def png_dimensions(raw):
    assert raw[:8] == b'\x89PNG\r\n\x1a\n'
    pos = 8; chunks = []
    while pos < len(raw):
        length = struct.unpack('>I', raw[pos:pos + 4])[0]
        kind = raw[pos + 4:pos + 8]; data = raw[pos + 8:pos + 8 + length]
        crc = struct.unpack('>I', raw[pos + 8 + length:pos + 12 + length])[0]
        assert (zlib.crc32(kind + data) & 0xffffffff) == crc
        chunks.append(kind); pos += 12 + length
        if kind == b'IEND': break
    assert pos == len(raw) and chunks[0] == b'IHDR' and chunks[-1] == b'IEND' and b'IDAT' in chunks
    return struct.unpack('>II', raw[16:24])
assert O.is_dir() and not (O / 'independent-original44-pixel-review-ACCEPT.json').exists()
report_raw = (B / 'report.json').read_bytes()
assert sha(report_raw) == '303524312bf5933ed8746ea2730d73d53e21e1255cf86c25386e3d80461fb997'
browser = json.loads(report_raw)
assert browser['head'] == browser['site_commit'] == browser['actual_gate_commit'] == CORE
assert browser['source_digest'] == '6905b946089555464e4eedadfad3644fb4df3ee5d49ffc8445c16bb7fd997108'
assert browser['UI_repair'] is None and browser['external_GitHub_HTML_checked'] is False
auth_raw = pinned(browser['authorization']); auth = json.loads(auth_raw)
assert sha(auth_raw) == '245edfa8d48d3461e275948114de38160ad5ac03bbf5d8368b35e1f9deaa2530'
assert auth['authorized_by'] == '/root' and auth['execute_browser_authorized'] is True
assert auth['authorization_kind'] == 'fixed-spectrum-geometry-final-browser-v1'
assert auth['accepted_immutable_core'] == CORE and auth['new_source_verdict'] is False and auth['parking_authorized'] is False
receipt_path = R / '.astis/huanjian-resume-20261103/20261109T023702713942Z-geometry-final-browser-v1.receipt.json'
receipt_raw = receipt_path.read_bytes(); receipt = json.loads(receipt_raw)
assert receipt['exit_code'] == 0 and receipt['head_before'] == receipt['head_after'] == CORE
assert receipt['command'][1] == '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader/check_final_reader_v1.py'
assert receipt['command'][-1] == sha(auth_raw)
log_raw = Path(receipt['log']).read_bytes()
assert sha(log_raw) == receipt['log_sha256'] == '1ba7c7012ca9d4c762bf46919466f1457909df08a17ac166829adb0f59338f16'
assert json.loads(log_raw)['screenshots'] == 44 and json.loads(log_raw)['status'] == 'passed'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip() == CORE
assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'], cwd=R)
gate_refs = []
assert len(auth['actual_checks_before_browser']) == 8
for role, ref in auth['actual_checks_before_browser'].items():
    raw = pinned(ref); row = json.loads(raw); log = Path(row['log']).read_bytes()
    assert row['exit_code'] == 0 and row['head_before'] == row['head_after'] == CORE
    assert sha(log) == row['log_sha256']
    gate_refs.append({'role': role, **ref, 'actual_exit_code': 0, 'actual_head': CORE, 'log_sha256': sha(log)})
for p, digest in browser['input_pins'].items(): assert sha((R / p).read_bytes()) == digest, p
assert sha((R / 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-geometry.json').read_bytes()) == 'a101634a005e20e54c8791cf340b871a3adf79807b75b607f422957392b0bc6c'
assert sha((R / 'runs/substantive_advances.jsonl').read_bytes()) == '5b58146368803e26104d11892b5d29cd6862bda63bb41268bdbc07be2b94190b'

# These notes were authored after the reviewer actually viewed images1–44 in
# eleven batches of four individual view_image(detail=original) calls. They are
# not an automatic inference from hashes, the browser PASS or a contact sheet.
notes = {
 'first': 'Concise actual-quadratic conclusion and D(gradient f_A)(x)=A rendered clearly; adjacent statement initially closed. Mobile title/statement wraps within one column.',
 'assumptions': 'Source d>=2,kappa>=2/full real O including both determinant signs, literal half-node grid and centered f, genuine Frechet Hessian and half-normalized strong convexity, outputs rather than caller certificates are readable. Mobile is a scrolled viewport, not a whole-ledger screenshot.',
 'proof-step1': 'Same Hx=Ax, half-inner-product f and ordinary C-infinity formula/prose readable with adjacent correspondence; mobile equation fits.',
 'proof-step2': 'Genuine gradient identity and derivative applied to v shown; correspondence explicitly produces existence before total-gradient equality; mobile equation fits.',
 'proof-step3': 'Both Euclidean quadratic bounds rendered, constant1 and kappa visible; caller supplies no matrix certificate; source strict-grid alternate remains explicit.',
 'proof-step4': 'Quantitative-gradient lower bound and source modulus one with half normalization readable; author Hessian route stays distinct; long canonical identifier wraps locally on mobile.',
 'proof-step5': 'Desktop complete operator norm<=kappa and kappa-gradient inequality readable. Mobile long formula extends horizontally inside its formula box and visibly says to scroll; the screenshot does not expose the final right-hand tail. No page-wide horizontal leak.',
 'proof-step6': 'Zero origin value, half norm-square lower bound, positivity away from zero and unique global minimizer readable. Mobile has a long-formula scroll hint; the visible formula and nonzero condition remain legible.',
 'proof-step7': 'Actual ordered value/Ax reply Borel for fixed input readable; new regularity genuinely consumed; private-only, no Registry/public node and no joint-in-O/adaptive histories stated.',
 'standard-reuse': 'Three canonical ASTIS parent links separated from Mathlib/external provenance. Long parent names wrap within mobile content. Mobile viewport does not show the entire lower Mathlib/source list.',
 'exact-statement': 'Open adjacent Lean statement disclosure and source-family/output explanation readable. Desktop image includes code beginning; mobile viewport contains disclosure prose, with code further down the scrollable page. No claim that full mobile statement code is visible in this PNG.',
 'exact-proof': 'Open Lean proof disclosure and three-parent/private-consumer explanation readable. Desktop code beginning visible; mobile captured prose/heading, with code below the viewport. Exact bytes/local scroll behavior are separate actual DOM checks.',
 'module': 'Own-site full-module context/download controls and syntax-highlighted exact source visible. Mobile source occupies a bounded local code viewport with right-hand content reachable by local horizontal scrolling; whole source not pictured.',
 'case-boundary': 'Source Theorem4.1 remains visibly a main lower-bound statement. Desktop shows open/red status, exact oracle, seed/history, deterministic cap, delta/d/kappa/epsilon scope and lower bound. Mobile shows the corresponding upper portion; later ranges/boundary are below viewport, not silently removed.',
 'source-index': '57 source-mapped/25 independently reviewed building blocks explicitly do not mean completed paper. Source limitations and reading-context/no chapter credit remain readable; mobile retains one-column hierarchy.',
 'source-index-open': 'Actual Geometry compact disclosure and Read full statement and proof link clearly visible in both widths. Surrounding FirstOrder/admissibility/determinant/normalizer entries remain separate.',
 'graph-focused': 'Actual Geometry selected declaration card readable and inside canvas; dashed source-reference edges distinguished from solid structural owner edge. Surrounding offscreen neighbors are focused-view context, not a claim that all graph labels fit.',
 'graph-module-native-click': 'Actual owning Geometry module selected visibly inside graph; neighbor module/import structure and full detail context remain coherent. Mobile is focused on selected module with surrounding nodes partly offscreen.',
 'typed-supplement': 'Existing quadratic-observation transport contract shown distinctly from Lean-module cards with dashed candidate structure. Mobile detail is visibly PROPOSAL. These pixels are an unchanged FirstOrder conceptual regression; they do not certify a new Geometry conceptual edge or all semantic rows below viewport.'}
images = []; journal = []
assert len(browser['screenshots']) == 44 and len({x['file'] for x in browser['screenshots']}) == 44
assert {p.name for p in B.glob('*.png')} == {x['file'] for x in browser['screenshots']}
for index, row in enumerate(browser['screenshots'], 1):
    p = B / row['file']; raw = p.read_bytes(); assert sha(raw) == row['sha256']
    width, height = png_dimensions(raw)
    expected = (1440, 1000) if index <= 22 else (390, 844)
    assert (width, height) == expected
    name = row['file']
    if name.startswith('canonical-parent'):
        number = int(name[len('canonical-parent')])
        parent = browser['producer_ASTIS_parents'][number - 1]
        note = f'Native selected canonical parent{number}: {parent}. Selected card/label fully inside graph canvas; full declaration identity readable in detail panel. For long parent3, selected label is intentionally abbreviated while full name wraps below; mobile x107..283 card and full wrapped name are readable.'
    else:
        stem = name.removesuffix('.png')
        if stem.startswith('case-boundary-'): kind = 'case-boundary'
        elif stem.startswith('source-index-'): kind = 'source-index'
        elif stem.startswith('existing-conceptual-'): kind = 'typed-supplement'
        else: kind = stem.split('-', 2)[2]
        note = notes[kind]
    image = {'sequence': index, 'path': str(p.relative_to(R)), 'file': name, 'sha256': sha(raw),
             'raw_bytes': len(raw), 'width': width, 'height': height, 'PNG_chunks_CRC_valid': True}
    images.append(image)
    journal.append({**image, 'actually_viewed': True, 'tool': 'view_image', 'detail': 'original',
                    'contact_sheet_crop_transform_or_browser_rerun': False, 'pixel_observation': note})
assert len([x for x in images if x['width'] == 1440]) == len([x for x in images if x['width'] == 390]) == 22
native = browser['native_selection_geometry']; assert len(native) == 12
for row in native:
    g = row['geometry']; assert g['ok'] and all(g['checks'].values())
    assert g['camera_actions_by_harness'] == [] and g['rendered_label_font_px'] >= 10
    if row['route'] in ['native-Lean-parent', 'native-Lean-module']:
        assert (B / row['main_original']).is_file()
    else:
        assert row['pixel_review_claim'] is False and row['extra_screenshot'] is False
assert len([x for x in native if x['route'] in ['native-Lean-parent', 'native-Lean-module']]) == 8
assert len(browser['old_long_Lean_layout_regressions']) == 2
for row in browser['old_long_Lean_layout_regressions']:
    assert row['native_learner_and_summary_clicks'] and row['long_Lean_code_lines'] == 175
    assert row['local_code_geometry']['overflow_x'] == 'auto'
    g = row['ordinary_prose_bounds']
    assert all(r['left'] >= -1 and r['right'] <= g['viewport_width'] + 1 and
               r['top'] >= g['unobscured_top'] - 1 and r['bottom'] <= g['viewport_height'] + 1 for r in g['text_rects'])
assert not browser['errors']
(O / 'actually-opened-originals-journal.json').write_bytes(dump(journal))
input_manifest = {'scope': 'Actual original browser image/provenance freeze, no rerun or transformations',
    'browser_report': {'path': str((B / 'report.json').relative_to(R)), 'sha256': sha(report_raw)},
    'actual_browser_receipt': {'path': str(receipt_path.relative_to(R)), 'sha256': sha(receipt_raw)},
    'actual_browser_log_sha256': sha(log_raw), 'root_authorization_sha256': sha(auth_raw), 'official8_actual_gate_receipts': gate_refs,
    'actual_originals': images, 'images_count': 44, 'desktop22_mobile22': True}
(O / 'input-provenance-and-original-manifest.json').write_bytes(dump(input_manifest))
for name, raw in [('actual-browser-report.raw.json.gz', report_raw), ('actual-browser-command-receipt.raw.json.gz', receipt_raw),
                  ('actual-browser-command-log.raw.gz', log_raw), ('actual-root-browser-authorization.raw.json.gz', auth_raw)]:
    (O / name).write_bytes(gzip.compress(raw, mtime=0))
review = {'reviewer': '/root/geometry_integration_reader', 'verdict': 'ACCEPT',
    'status': 'ACCEPTED_SCOPED_ACTUAL_44_ORIGINAL_PIXEL_REVIEW', 'immutable_core': CORE,
    'source_digest': browser['source_digest'], 'publication_binding_sha256': browser['publication_binding_sha256'],
    'actual_browser_report_sha256': sha(report_raw), 'actual_browser_receipt_sha256': sha(receipt_raw),
    'actual_root_browser_authorization_sha256': sha(auth_raw), 'new_Geometry_OS_prefix_used': True, 'UI_patch': None,
    'independent_original_review': {'actual_originals_individually_viewed': 44, 'desktop': {'count': 22, 'size': [1440, 1000]},
        'mobile': {'count': 22, 'size': [390, 844]}, 'method': '44 individual original image view_image results emitted in11 batches; every original actually examined; no contact sheet, crop, transform, synthesized preview or filename-only acceptance.',
        'all_hashes_dimensions_and_PNG_CRCs_verified': True, 'journal': 'actually-opened-originals-journal.json'},
    'pixel_findings': ['Concise default conclusion, genuine Hessian formula, full assumptions and seven authored proof steps are legible at both widths with expected vertical/local scrolling.',
        'Constants1,kappa,one-half normalization and global zero minimizer preserved visibly; strict-grid/author-Hessian alternate route and private fixed-input Borel boundary explicit.',
        'Compact source index/Geometry disclosure/source proof link and actual source/main-bound distinction remain readable; source ranges/TV/exact oracle/seed/deterministic cap preserved.',
        'Geometry declaration, owning module and all3 canonical parent selected cards stay readable/in canvas at1440/390. Mobile long generic parent has176px card,12px rendered label and full declaration identity wrapped below.',
        'Existing FirstOrder typed-Functor view remains proposal/candidate structure, with no Geometry transport certification; surrounding graph nodes may be offscreen in focused view.'],
    'blocking_visual_defects': [],
    'scope_limits_and_nonblocking_observations': ['These are viewport captures. Long modules/code, assumption ledgers, case boundaries and semantic detail panels extend vertically; no image claims to show all content at once.',
        'Mobile proof-step5 long equation visibly uses horizontal formula scrolling; final right-hand tail is outside that still image. Desktop shows the full equation. Mobile proof-step6 also carries a long-formula hint.',
        'Mobile exact-statement/exact-proof captures show the opened adjacent disclosure and prose; their code is below the captured viewport. Actual exact-code equality and local code scrolling are DOM evidence, while actual module source pixels are visible in the module original.',
        'Generic desktop module inventory displays Compiled/Not mapped, an existing route-status badge distinct from the authored publication/source index reviewed here. No legacy route completion is inferred.',
        'Eight native parent/module selections have corresponding originals. Four extra preset/cross-view geometry rows and two old DensityAffinity175line regressions are DOM/UI-only, with no extra screenshot/pixel claim.',
        'Full typed-Functor semantic-row equality and no Geometry candidate incidence are source/DOM checks; all rows and module names are not readable simultaneously in the conceptual viewport originals.',
        'Only own-site local HTTP/source/module/download paths were checked. Both GitHub immutable-link syntax and external GitHub HTML branches were not executed; no remote/public delivery claim.'],
    'supporting_actual_DOM_evidence': {'seven_steps_each_width': True, 'closed_initial_disclosures': True,
        'adjacent_exact_statement_proof_and_private_Test_source_bytes': True,
        'local_code_scroll': {str(p['width']): p['local_code_scroll'] for p in browser['pages']},
        'native_geometry_rows': 12, 'native_rows_with_originals': 8, 'extra_native_DOM_only_rows': 4,
        'old_DensityAffinity_DOM_only_regressions': 2, 'same_head_official8_receipts_verified': True,
        'DOM_pass_used_as_substitute_for_pixels': False},
    'original_source_verifier_audit_V_and_STAB_preserved': True,
    'new_mathematical_or_source_verdict': False, 'local_integration_acceptance_granted': False,
    'parking_or_API_or_shared_edit_or_browser_rerun_or_OS_or_network_or_commit_by_reviewer': False,
    'remaining_boundaries': 'Root own original-image review and any local integration acceptance remain separate. No park, remote delivery/owner release, purification/Exposition Seal, full main lower-bound or whole-Goal completion follows.',
    'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O / 'independent-original44-pixel-review-ACCEPT.json').write_bytes(dump(review))
(O / 'review-recorder.raw.py.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(), mtime=0))
freeze = {'state': review['status'], 'review_sha256': sha((O / 'independent-original44-pixel-review-ACCEPT.json').read_bytes()),
    'files': [{'path': str(p.relative_to(R)), 'sha256': sha(p.read_bytes())} for p in sorted(O.iterdir()) if p.is_file()],
    'local_integration_or_park_or_new_source_verdict': False}
(O / 'freeze.json').write_bytes(dump(freeze))
for row in images: assert sha((R / row['path']).read_bytes()) == row['sha256']
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip() == CORE
assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'], cwd=R)
print(json.dumps({'review': str((O / 'independent-original44-pixel-review-ACCEPT.json').relative_to(R)), 'review_sha256': freeze['review_sha256'],
    'freeze_sha256': sha((O / 'freeze.json').read_bytes()), 'actually_viewed_originals': 44, 'verdict': review['verdict'],
    'local_integration_or_park_or_sourceV_granted': False}, indent=2))
