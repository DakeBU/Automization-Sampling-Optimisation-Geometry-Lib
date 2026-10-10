import hashlib
import json
import os
import pathlib
from datetime import datetime, timezone
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parents[4]
OWN = pathlib.Path(__file__).resolve().parent
BASE = ROOT / 'runs/20261007-companion-priority/pbps-clock-preproof75/independent-source-baseline75'
PRIMARY = ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def record(path, name):
    data = path.read_bytes()
    target = OWN / 'source-only-inputs' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {
        'path': path.relative_to(ROOT).as_posix(),
        'snapshot': target.relative_to(ROOT).as_posix(),
        'RAW_bytes': len(data),
        'RAW_sha256': sha(data),
        'LF_sha256': sha(data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')),
    }


class SourceText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.math_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'math':
            if self.math_depth == 0:
                a = dict(attrs)
                self.parts.append('$' + a.get('alttext', '') + '$')
            self.math_depth += 1
        elif not self.math_depth and tag in {'p', 'div', 'tr', 'li', 'h3', 'h6', 'figcaption'}:
            self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag == 'math':
            self.math_depth -= 1
        elif not self.math_depth and tag in {'p', 'div', 'tr', 'li', 'h3', 'h6', 'figcaption'}:
            self.parts.append('\n')

    def handle_data(self, data):
        if not self.math_depth:
            self.parts.append(data)

    def text(self):
        return '\n'.join(' '.join(line.split()) for line in ''.join(self.parts).splitlines() if line.strip())


def validate_range(raw, entry, label):
    a, b = entry['RAW_range']
    data = raw[a:b]
    assert 0 <= a <= b <= len(raw), label
    assert len(data) == entry['RAW_bytes'], label + ': byte count'
    assert sha(data) == entry['RAW_sha256'], label + ': RAW hash'
    assert sha(data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')) == entry['LF_sha256'], label + ': LF hash'


def main():
    names = ['source-proof-graph75.json', 'source-coverage-inventory75.json',
             'exact-source-formulas75.json', 'stageA.freeze75.json']
    inputs = [record(PRIMARY, '01.primary-pbps.exactraw.snapshot.html.RAW')]
    inputs += [record(BASE / name, f'{n:02d}.{name}.RAW') for n, name in enumerate(names, 2)]
    raw = PRIMARY.read_bytes()
    assert len(raw) == 1482128
    assert sha(raw) == 'd81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
    graph, inventory, formulas, stage = [json.loads((BASE / name).read_text(encoding='utf-8')) for name in names]
    assert len(graph['nodes']) == graph['node_count'] == 32
    assert len(graph['edges']) == graph['edge_count'] == 67
    assert len(inventory['items']) == inventory['item_count'] == 137
    assert len(formulas['source_formulas']) == formulas['source_formula_count'] == 23
    counts = {kind: sum(x['classification'] == kind for x in inventory['items']) for kind in ['NODE', 'EXCLUDED']}
    assert counts == {'NODE': 77, 'EXCLUDED': 60}
    ids = {x['id'] for x in graph['nodes']}
    assert len(ids) == 32
    assert all(e['producer'] in ids and e['consumer'] in ids for e in graph['edges'])
    anchors = {}
    for node in graph['nodes']:
        for anchor in node['source_anchors']:
            validate_range(raw, anchor, node['id'] + ':' + anchor['id'])
            anchors[anchor['id']] = anchor
    for item in inventory['items']:
        validate_range(raw, item, item['item_id'])
        assert item['classification'] in {'NODE', 'EXCLUDED'}
        assert item['nodes'] or item['classification'] == 'EXCLUDED'
        assert all(n in ids for n in item['nodes'])
    for formula in formulas['source_formulas']:
        validate_range(raw, formula, formula['id'])
        data = raw[slice(*formula['RAW_range'])].decode('utf-8')
        parser = SourceText()
        parser.feed(data)
        assert formula['literal_source_alttext'] in parser.text(), formula['id']
    region_checks = []
    source_text = []
    for region in inventory['regions']:
        check = dict(region['RAW'], RAW_range=region['RAW_range'])
        validate_range(raw, check, region['region_id'])
        parser = SourceText()
        parser.feed(raw[slice(*region['RAW_range'])].decode('utf-8'))
        source_text.append('REGION ' + region['region_id'] + ' ' + str(region['RAW_range']) + '\n' + parser.text())
        region_checks.append({'id': region['region_id'], 'RAW_range': region['RAW_range'], 'RAW_sha256': check['RAW_sha256'], 'verified': True})
    text = '\n\n'.join(source_text) + '\n'
    (OWN / 'source-only-primary-extract75.txt').write_bytes(text.encode('utf-8'))
    report = {
        'schema': 'pbps75-fresh-independent-source-range-verification/v1',
        'actor': '/root/independent_clean_source75',
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'actual_PID': os.getpid(),
        'actual_EXIT': 0,
        'primary_expected_hash_verified': True,
        'input_snapshot_count': len(inputs),
        'inputs': inputs,
        'source_graph': {'nodes': 32, 'edges': 67, 'internal_bridge_nodes': sum(n['kind'] == 'ASTIS_INTERNAL_BRIDGE' for n in graph['nodes'])},
        'source_inventory': {'items': 137, **counts, 'all_item_ranges_verified': True},
        'source_formula_count': 23,
        'all_formula_ranges_and_literal_alttext_verified': True,
        'all_node_anchor_ranges_verified': True,
        'regions': region_checks,
        'source_only': True,
        'candidate_statement_BODY_metadata_review_verdict_read': False,
        'source_topology_is_not_Lean_implication': True,
    }
    (OWN / 'source-only-input-manifest75.json').write_bytes((json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    print(json.dumps({k: v for k, v in report.items() if k not in ['inputs', 'regions']}, indent=2))
    print(text)


if __name__ == '__main__':
    main()
