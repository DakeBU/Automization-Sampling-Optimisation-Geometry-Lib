from pathlib import Path
import hashlib, json
W = Path(__file__).parent
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2)+'\n').encode()
base_raw = (W/'minimal-definition-context.json').read_bytes()
base = json.loads(base_raw)
rows = []
changes = []
for i, original in enumerate(base['definitions']):
    row = dict(original)
    p = Path(row['file'])
    raw = p.read_bytes()
    text = raw.decode('utf-8')
    block = row['literal']
    synthetic_display_LF_removed = False
    if block not in text:
        assert row['kind'] == 'characterization-statement-only' and block.endswith('\n')
        block = block[:-1]
        synthetic_display_LF_removed = True
    assert block in text and text.count(block) == 1, (i, p)
    a = text.index(block)
    b = a+len(block)
    assert text[a:b].encode() == block.encode()
    row.update({'wholefile_raw_sha256': sha(raw), 'literal': block,
                'literal_sha256': sha(block.encode()),
                'start_character_inclusive': a, 'end_character_exclusive': b,
                'byte_start_inclusive': len(text[:a].encode()), 'byte_end_exclusive': len(text[:b].encode()),
                'start_line_1based': text[:a].count('\n')+1,
                'end_line_1based_inclusive': text[:b].count('\n')+(0 if block.endswith('\n') else 1),
                'source_LF_included_exactly': block.endswith('\n')})
    for k in ['wholefile_sha256', 'start_line_1based_inclusive']:
        row.pop(k, None)
    rows.append(row)
    changes.append({'row': i, 'old_end_character_exclusive': original.get('end_character_exclusive'),
                    'exact_end_character_exclusive': b,
                    'synthetic_display_LF_removed_from_statement_header_only': synthetic_display_LF_removed,
                    'source_definition_or_target_statement_changed': False})
out = {'base_context_raw_sha256': sha(base_raw),
       'scope': 'Mechanical exact-source locator overlay. Original sealed statement and base context remain immutable. All definitions and characterization signatures have the same mathematical content; definition LF is part of the exact span. One characterization header excludes its synthetic display LF and all proof syntax.',
       'line_convention': 'Literal LF only; Unicode character and raw UTF8 byte spans start-inclusive/end-exclusive; line numbers1-based inclusive and terminal LF belongs to the preceding line.',
       'definitions': rows, 'metadata_changes': changes,
       'no_target_proof_or_normal_API': True, 'independent_overlay_audit': 'Pending distinct topology role.'}
data = dump(out)
for p in [W/'minimal-definition-context-exact-LF.json', E/'minimal-definition-context-exact-LF.json']:
    with p.open('xb') as f:
        f.write(data)
diag = {'base_seal_unchanged_sha256': sha((W/'statement-seal-v1.json').read_bytes()),
        'base_definition_context_unchanged_sha256': sha(base_raw), 'exact_locator_overlay_sha256': sha(data),
        'all10_exact_source_spans_verified': len(rows) == 10,
        'meaning': 'The initial generic extraction reported end before final LF while its display included that LF. This overlay makes every selected literal and locator agree exactly, preserving the initial record and core seal. A statement-only characterization had a synthetic display LF which is explicitly excluded in its exact header span. No new target/binder/formal proof or source verdict.'}
(W/'definition-locator-overlay-diagnostic.json').write_bytes(dump(diag))
(E/'definition-locator-overlay-diagnostic.json').write_bytes(dump(diag))
print(json.dumps(diag))
