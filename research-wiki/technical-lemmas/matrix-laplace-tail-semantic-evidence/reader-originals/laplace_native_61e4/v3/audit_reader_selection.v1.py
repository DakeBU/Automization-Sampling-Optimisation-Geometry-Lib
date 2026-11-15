"""Read-only exact reader-runtime leaf privacy/custody review, no UI verdict."""
from pathlib import Path, PurePosixPath
from collections import Counter
import datetime
import hashlib
import importlib.util
import io
import json
import re
import struct
import sys
import zlib
from urllib.parse import urlsplit, parse_qsl

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
ACTOR = ROOT / '.astis/semantic-neutral-20261114/laplace_native_61e4/reader-runtime-v3'
MANIFEST = ACTOR / 'presentation-selected-originals.manifest.v1.json'
EXPECTED = '3cea83cd0e61df11cba9ab36dca51f1f64c79b18df1238b836d8f9c05f301451'
OLD_DETECTOR = ROOT / '.astis/semantic-neutral-20261114/mgf_public_progress_audit_73af/preflight.py'
PACKER = ROOT / '.astis/huanjian-gc-matrix-laplace-20261114/lossless_allowlist_container.native-dag-v2.py'
def sha(raw): return hashlib.sha256(raw).hexdigest()
def save(name, value): (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
manifest_raw = MANIFEST.read_bytes()
assert sha(manifest_raw) == EXPECTED
manifest = json.loads(manifest_raw)
rows = manifest['leaves']
assert len(rows) == 356 and len({row['path'] for row in rows}) == 356
detector = {'__name__': 'read_only_detector_definitions', '__file__': str(OLD_DETECTOR)}
exec(compile(OLD_DETECTOR.read_text(), str(OLD_DETECTOR), 'exec'), detector)
spec = importlib.util.spec_from_file_location('reader_selection_guard', PACKER)
guard = importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
assert sha(PACKER.read_bytes()) == '4385d8e2ab61344e1ecfdbd3d3f8e5f74f1f5983f33fc5ee3c5efaf1468db774'

checks, findings, png_rows, font_rows, env_rows, structure_rows = [], [], [], [], [], []
local_paths, atlas_literals, urls = [], [], []
seen = set()
text_data = {}
png_paths = []
visited = 0
embedded = 0
def json_walk(value, path):
    global visited, embedded
    stack = [('$', value)]
    while stack:
        pointer, obj = stack.pop(); visited += 1
        if isinstance(obj, dict):
            if len(obj) >= 128:
                path_keys = sum(isinstance(k, str) and ('/' in k or '\\' in k) for k in obj)
                digest_values = sum(isinstance(v, str) and bool(re.fullmatch('[0-9a-f]{40}|[0-9a-f]{64}', v)) for v in obj.values())
                state_values = sum(isinstance(v, dict) and bool({'advance_id', 'discovery_id'} & set(v)) and bool({'state', 'event'} & set(v)) for v in obj.values())
                if path_keys >= len(obj) * .7 and digest_values >= len(obj) * .7:
                    findings.append({'leaf': path, 'field': pointer, 'kind': 'large_workspace_path_digest_map'})
                if state_values >= len(obj) * .7:
                    findings.append({'leaf': path, 'field': pointer, 'kind': 'foreign_state_map'})
            for key, item in obj.items():
                child = pointer + '/' + str(key).replace('~', '~0').replace('/', '~1')
                if re.search(r'(^|_)(environment|env)($|_)', str(key), re.I) and isinstance(item, dict):
                    env_rows.append({'leaf': path, 'field': child, 'keys': sorted(item)})
                if re.search(r'(?:all_existing|foreign).*(?:advance|discovery|frontier|state).*(?:map|hash|digest|snapshot)|git.?index.*(?:raw|base64|bytes)', str(key), re.I) and isinstance(item, (dict, list)) and len(item) >= 32:
                    findings.append({'leaf': path, 'field': child, 'kind': 'private_guard_or_foreign_snapshot', 'records': len(item)})
                if re.fullmatch(r'(authorization|proxy-authorization|cookie|set-cookie|cookies|access_token|refresh_token|client_secret|password)', str(key), re.I):
                    if item not in [None, '', [], {}]:
                        findings.append({'leaf': path, 'field': child, 'kind': 'nonempty_session_or_credential_field', 'value_not_emitted': True})
                stack.append((child, item))
        elif isinstance(obj, list):
            stack.extend((pointer + '/' + str(i), child) for i, child in enumerate(obj))
        elif isinstance(obj, str):
            if '/Users/' in obj or '/private/' in obj or 'chrome-tmp' in obj:
                local_paths.append({'leaf': path, 'field': pointer, 'kind': 'recorded_local_path_string_only'})
            if 'ATLAS' in obj:
                atlas_literals.append({'leaf': path, 'field': pointer, 'characters': len(obj)})
            if obj.startswith(('http://', 'https://')):
                u = urlsplit(obj)
                urls.append({'leaf': path, 'field': pointer, 'scheme': u.scheme, 'host': u.hostname})
                if u.username or u.password:
                    findings.append({'leaf': path, 'field': pointer, 'kind': 'URL_userinfo_credential', 'value_not_emitted': True})
                for key, item in parse_qsl(u.query):
                    if re.search(r'token|secret|password|api.?key', key, re.I) and len(item) >= 12:
                        findings.append({'leaf': path, 'field': pointer + '/query/' + key, 'kind': 'URL_credential_parameter', 'value_not_emitted': True})
            if len(obj) >= 128 and obj.lstrip().startswith(('{', '[')):
                try: nested = json.loads(obj)
                except ValueError: continue
                embedded += 1; stack.append((pointer + '/<structured-string>', nested))

def png_metadata(raw, path):
    assert raw.startswith(b'\x89PNG\r\n\x1a\n')
    pos, chunks, text_blocks = 8, [], []
    width = height = None
    while pos < len(raw):
        size = int.from_bytes(raw[pos:pos+4], 'big'); kind = raw[pos+4:pos+8]
        body = raw[pos+8:pos+8+size]; crc = int.from_bytes(raw[pos+8+size:pos+12+size], 'big')
        assert len(body) == size and zlib.crc32(kind + body) & 0xffffffff == crc
        chunks.append(kind.decode())
        if kind == b'IHDR': width, height = struct.unpack('>II', body[:8])
        if kind == b'tEXt': text_blocks.append(body)
        elif kind == b'zTXt':
            _, rest = body.split(b'\0', 1); text_blocks.append(zlib.decompress(rest[1:]))
        elif kind == b'iTXt':
            _, rest = body.split(b'\0', 1)
            flag, method = rest[0], rest[1]; rest = rest[2:]
            _, rest = rest.split(b'\0', 1); _, text = rest.split(b'\0', 1)
            text_blocks.append(zlib.decompress(text) if flag else text)
        pos += 12 + size
        if kind == b'IEND': break
    assert pos == len(raw) and width and height
    for body in text_blocks:
        detector['scan'](body, path + '::<PNG-text-metadata>')
        try: guard.guard_payload(body, path + '::<PNG-text-metadata>', 256 * 1024 * 1024)
        except Exception as exc: findings.append({'leaf': path, 'kind': 'PNG_text_guard_rejection', 'reason': str(exc)})
    return {'path': path, 'width': width, 'height': height, 'chunks': chunks, 'text_metadata_blocks_scanned': len(text_blocks)}

def woff_metadata(raw, path):
    assert raw[:4] == b'wOFF' and len(raw) >= 44
    length = int.from_bytes(raw[8:12], 'big'); tables = int.from_bytes(raw[12:14], 'big')
    assert length == len(raw)
    offset, size, original_size = [int.from_bytes(raw[p:p+4], 'big') for p in [24, 28, 32]]
    metadata = b''
    if offset:
        metadata = zlib.decompress(raw[offset:offset+size]); assert len(metadata) == original_size
        detector['scan'](metadata, path + '::<WOFF-metadata>')
    return {'path': path, 'table_count': tables, 'metadata_bytes_scanned': len(metadata),
            'classification': 'Selected MathJax vendor webfont asset; not browser cache/profile payload.'}

for row in rows:
    posix = PurePosixPath(row['path'])
    assert not posix.is_absolute() and '..' not in posix.parts
    guard.regular_member_name(row['path'])
    assert not any(part.casefold() in {'chrome-tmp', 'profile', 'default', 'cache', '.cache', '.git', '__pycache__'} for part in posix.parts)
    path = ACTOR / row['path']
    assert path.is_file() and not path.is_symlink()
    raw = path.read_bytes(); digest = sha(raw)
    assert len(raw) == row['bytes'] and digest == row['sha256']
    unique = digest not in seen; seen.add(digest)
    checks.append({'path': row['path'], 'bytes': len(raw), 'sha256': digest, 'exact_original_match': True,
                    'full_content_scan_reused_only_for_identical_bytes': not unique})
    if path.suffix == '.png':
        png_rows.append(png_metadata(raw, row['path'])); png_paths.append(path)
    elif path.suffix == '.woff': font_rows.append(woff_metadata(raw, row['path']))
    elif unique:
        detector['scan'](raw, row['path'])
        try: guard.guard_payload(raw, row['path'], 256 * 1024 * 1024)
        except Exception as exc: findings.append({'leaf': row['path'], 'kind': 'depth32_payload_guard_rejection', 'reason': str(exc)})
        if raw.startswith((b'DIRC', b'PK\x03\x04', b'\x1f\x8b', b'BZh', b'\xfd7zXZ\x00')):
            findings.append({'leaf': row['path'], 'kind': 'unexpected_index_or_compressed_container_magic'})
        if len(re.findall(rb'(?m)(?:^|(?<=\x00))[0-7]{6}\s+(?:blob|tree|commit)\s+[0-9a-f]{40}\t[^\x00\r\n]+(?=\x00|$)', raw)) >= 1000:
            findings.append({'leaf': row['path'], 'kind': 'full_repository_tree_inventory'})
    if path.suffix == '.json':
        value = json.loads(raw); json_walk(value, row['path'])
        structure_rows.append({'leaf': row['path'], 'top_fields': list(value) if isinstance(value, dict) else None,
                               'root_type': type(value).__name__})
    if path.suffix in ['.html', '.js', '.css', '.py', '.raw', '.md']:
        try: text_data[row['path']] = raw.decode()
        except UnicodeDecodeError: pass

# The original manifest is retained as auxiliary evidence, not rewritten.
detector['scan'](manifest_raw, '<original-presentation-selected-originals.manifest.v1.json>')
guard.guard_payload(manifest_raw, '<original-presentation-selected-originals.manifest.v1.json>', 256 * 1024 * 1024)

# Derived contact sheets are local QA views only, never replacements for original
# PNGs or additional archive selections. Original pixels/bytes remain unchanged.
from PIL import Image, ImageDraw, ImageFont
contact_rows = []
for page in range((len(png_paths) + 34) // 35):
    group = png_paths[page*35:(page+1)*35]
    sheet = Image.new('RGB', (1500, 7 * 210), 'white'); draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(group):
        x, y = (i % 5) * 300, (i // 5) * 210
        im = Image.open(path).convert('RGB'); im.thumbnail((292, 178))
        sheet.paste(im, (x + 4, y + 4))
        label = path.name
        draw.text((x + 4, y + 184), label[:43], fill='black')
    output = OUT / ('privacy-contact-sheet-' + str(page + 1) + '.png')
    sheet.save(output)
    contact_rows.append({'path': output.name, 'sha256': sha(output.read_bytes()),
                         'original_paths': [str(path.relative_to(ACTOR)) for path in group]})

selection = {'schema': 'exact-reader-runtime-public-selection-candidate-v1',
             'original_manifest_relative_path': '.astis/semantic-neutral-20261114/laplace_native_61e4/reader-runtime-v3/presentation-selected-originals.manifest.v1.json',
             'original_manifest_bytes': len(manifest_raw), 'original_manifest_sha256': EXPECTED,
             'actual_browser_run': 'v3', 'new_v4_browser_run_claimed': False,
             'file_count': 356, 'selection_scope': 'Exact actor356 task-owned reader runtime leaves only; privacy/custody selection, not presentation/source/math verdict.',
             'files': rows, 'exclusions': []}
save('reader-runtime-public-selection.356.v1.json', selection)
report = {'schema': 'independent-reader-runtime-public-selection-privacy-audit-v1',
          'status': 'MACHINE_SCAN_COMPLETE_PENDING_CONTACT_SHEET_REVIEW',
          'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'original_manifest_sha256': EXPECTED, 'original_manifest_bytes': len(manifest_raw),
          'selected_leaves': len(rows), 'selected_bytes': sum(row['bytes'] for row in rows),
          'original_manifest_may_be_selected_in_full_subject_to_png_view_review': not findings and not detector['findings'] and not detector['errors'],
          'selection_file': 'reader-runtime-public-selection.356.v1.json',
          'selection_sha256': sha((OUT / 'reader-runtime-public-selection.356.v1.json').read_bytes()),
          'leaf_checks': checks, 'png_checks': png_rows, 'woff_checks': font_rows,
          'all_nested_JSON_values_visited': visited, 'nested_JSON_strings_decoded': embedded,
          'JSON_structures': structure_rows, 'command_environment_fields': env_rows,
          'command_environment_key_union': sorted(set(key for row in env_rows for key in row['keys'])),
          'recorded_local_paths_are_not_copied_profile_content': local_paths,
          'ATLAS_literal_mentions_in_JSON': atlas_literals, 'recorded_URL_hosts': dict(Counter(row['host'] for row in urls)),
          'payload_findings': detector['findings'], 'payload_read_errors': detector['errors'], 'additional_guard_findings': findings,
          'contact_sheets_local_QA_only': contact_rows,
          'png_visual_privacy_review': 'pending',
          'privacy_scope': 'Only exact selected original356 bytes. No prior623 source evidence rescanned, no Chrome tmp/profile/cache payload selected. No archive created or original evidence normalized/trimmed.',
          'presentation_math_source_verdict_inherited': False,
          'future_archive_or_Git_commit_approval': False,
          'auditor_API_Git_mutation_Lean_network_production_write_calls': 0,
          'original_manifest_and_all_leaves_unchanged': MANIFEST.read_bytes() == manifest_raw and all(sha((ACTOR / row['path']).read_bytes()) == row['sha256'] for row in rows)}
save('reader-runtime-selection-privacy-audit.v1.json', report)
print(json.dumps({'selected_count': len(rows), 'selected_bytes': report['selected_bytes'],
                  'selection_sha256': report['selection_sha256'], 'guard_findings': findings,
                  'detector_findings': detector['findings'], 'detector_errors': detector['errors'],
                  'PNG_count': len(png_rows), 'PNG_text_blocks': sum(row['text_metadata_blocks_scanned'] for row in png_rows),
                  'WOFF_count': len(font_rows), 'env_keys': report['command_environment_key_union'],
                  'contact_sheets': [row['path'] for row in contact_rows]}, indent=2))
