import gzip
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT = Path('E:/Samplinglib')
PKG = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-flip-duality108/next-primary109'
OUT = PKG / 'independent-topology109'
def sha(b):
    return hashlib.sha256(b).hexdigest()
def read(p):
    return json.loads(Path(p).read_bytes().decode('utf-8-sig'))
def bind(rec):
    b = (ROOT / rec['path']).read_bytes()
    return dict(path=rec['path'], actual_raw_sha256=sha(b),
                hash_ok=sha(b) == rec['raw_sha256'], bytes_ok=len(b) == rec['bytes'])

g = read(PKG / 'source-proof-graph-delta109.native.json')
base = read(ROOT / g['base_graph']['path'])
r = read(PKG / 'retrieval109.native.json')
primary = read(PKG / 'primary-first109.native.json')
coverage = read(PKG / 'source-coverage109.native.json')
closure = read(PKG / 'closed-RAW-manifest109.native.json')
interface = read(PKG / 'actual-interface109.native.json')
ids = [n['id'] for n in g['nodes']]
es = [(e['source'], e['target']) for e in g['edges']]
eset = set(es)
unknown = sorted(set(x for e in es for x in e) - set(ids))
degrees = dict.fromkeys(ids, 0)
adj = defaultdict(list)
for a,b in es:
    degrees[b] = degrees.get(b, 0) + 1
    adj[a].append(b)
q = deque(sorted(k for k,v in degrees.items() if v == 0))
order = []
while q:
    a = q.popleft()
    order.append(a)
    for b in adj[a]:
        degrees[b] -= 1
        if degrees[b] == 0:
            q.append(b)
groups = []
for a in g['new_AND_groups']:
    groups.append(dict(target=a['target'], parent_count=len(a['parents']),
        self_required=a['target'] in a['parents'],
        missing_edges=[p for p in a['parents'] if (p,a['target']) not in eset]))
route = g['OR_route_policy']
selected = next(a for a in route['alternatives'] if a['id'] == route['selected'])
bindings = [bind(x) for x in closure['artifacts'] + closure['inputs']]
apis = []
for a in r['apis']:
    f = ROOT / a['file']['path']
    raw = f.read_bytes()
    span = b''.join(raw.splitlines(keepends=True)[a['line_start']-1:a['line_end']])
    apis.append(dict(id=a['id'], file_binding=bind(a['file']),
        line_start=a['line_start'], line_end=a['line_end'],
        span_hash_ok=sha(span)==a['span_raw_sha256'],
        exact_text_ok=span.decode('utf-8')==a['text']))
src = (ROOT / primary['primary']['path']).read_bytes()
regions = []
for s in primary['regions']:
    bspan=src[s['byte_start']:s['byte_end_exclusive']]
    lspan=b''.join(src.splitlines(keepends=True)[s['line_start']-1:s['line_end']])
    regions.append(dict(id=s['id'], bytes_hash_ok=sha(bspan)==s['raw_sha256'],
                        byte_line_spans_equal=bspan==lspan))
archives=[]
for a in closure['archives']:
    compressed=(ROOT/a['archive']['path']).read_bytes()
    restored=gzip.decompress(compressed)
    archives.append(dict(path=a['archive']['path'], archive_binding=bind(a['archive']),
        raw_roundtrip_ok=sha(restored)==a['original']['raw_sha256'],
        exact_roundtrip_ok=restored==(ROOT/a['original']['path']).read_bytes()))
prod=(ROOT/interface['producer']['path']).read_bytes()
producer_spans=[]
for key in ('literal_statement_span','public_binders_span'):
    s=interface[key]
    span=b''.join(prod.splitlines(keepends=True)[s['start']-1:s['end']])
    producer_spans.append(dict(name=key, hash_ok=sha(span)==s['raw_sha256']))
new_node_ids={n['id'] for n in g['new_nodes']}
base_node_ids={n['id'] for n in base['nodes']}
base_edges={(e['source'],e['target']) for e in base['edges']}
api_from_base=[]
for name in ('MeasureTheory.MemLp.comp_measurePreserving','ContinuousLinearMap.adjoint_inner_left'):
    node=next(n for n in g['nodes'] if n['id']==name)
    if 'binding' in node:
        b=node['binding']
        raw=(ROOT/b['file']['path']).read_bytes().decode('utf-8')
        text=''.join(raw.splitlines(keepends=True)[b['line_start']-1:])
        api_from_base.append(dict(id=name,file_binding=bind(b['file']),
            signature_prefix_ok=text.replace('\r\n','\n').startswith(b['signature_excerpt'].replace('\r\n','\n'))))
result=dict(kind='independent prospective109 exact evidence and topology checks',
    reviewer='/root/blind_decoder106',
    author_closure_raw_sha256=sha((PKG/'closed-RAW-manifest109.native.json').read_bytes()),
    author_closure_expected_hash_ok=sha((PKG/'closed-RAW-manifest109.native.json').read_bytes())=='90176a7a924a3ba4e9387d37f343ce97063c50f0a52ccee9e7b07daa3f9fcf87',
    graph_raw_sha256=sha((PKG/'source-proof-graph-delta109.native.json').read_bytes()),
    nodes=len(ids),distinct_nodes=len(set(ids)),edges=len(es),distinct_edges=len(eset),
    new_nodes=len(new_node_ids),new_edges=len(eset-base_edges),
    unknown_endpoints=unknown,acyclic=len(order)==len(ids),topological_order=order,
    inherited_nodes_byte_semantic_equal=all(n in g['nodes'] for n in base['nodes']),
    inherited_edges_byte_semantic_equal=all(e in g['edges'] for e in base['edges']),
    declared_new_nodes_exact=set(ids)-base_node_ids==new_node_ids,
    declared_new_edges_exact=eset-base_edges=={(e['source'],e['target']) for e in g['new_edges']},
    new_AND_groups=groups,selected_OR_target=route['target'],
    selected_OR_parents=selected['AND'],selected_OR_requires_own_target=route['target'] in selected['AND'],
    selected_OR_missing_edges=[p for p in selected['AND'] if (p,route['target']) not in eset],
    inherited_route_logic_exact=(g['inherited_route_logic']['inherited_route_logic']==base['inherited_route_logic'] and
      g['inherited_route_logic']['new_AND_groups']==base['new_AND_groups'] and
      g['inherited_route_logic']['OR_route_policy']==base['OR_route_policy']),
    coverage_nodes_exact=Counter(n['id'] for n in coverage['node_dispositions'])==Counter(ids),
    coverage_edges_exact=Counter((e['source'],e['target']) for e in coverage['edge_dispositions'])==Counter(es),
    coverage_regions_count=len(coverage['regions']),
    coverage_region_pins_equal=all(all(c.get(k)==v for k,v in s.items()) for c,s in zip(coverage['regions'],primary['regions'])),
    file_bindings=bindings,apis=apis,inherited_additional_apis=api_from_base,
    primary_binding=bind(primary['primary']),source_regions=regions,
    producer_binding=bind(interface['producer']),producer_spans=producer_spans,archives=archives)
out=OUT/'checks109.native.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary={k:result[k] for k in ('nodes','distinct_nodes','edges','distinct_edges','new_nodes','new_edges','acyclic','unknown_endpoints','inherited_nodes_byte_semantic_equal','inherited_edges_byte_semantic_equal','declared_new_nodes_exact','declared_new_edges_exact','inherited_route_logic_exact','coverage_nodes_exact','coverage_edges_exact','coverage_regions_count','coverage_region_pins_equal','selected_OR_requires_own_target','selected_OR_missing_edges','author_closure_expected_hash_ok')}
summary['bad_file_bindings']=[b for b in bindings if not(b['hash_ok'] and b['bytes_ok'])]
summary['bad_apis']=[a for a in apis if not(a['file_binding']['hash_ok'] and a['span_hash_ok'] and a['exact_text_ok'])]
summary['bad_source_regions']=[s for s in regions if not(s['bytes_hash_ok'] and s['byte_line_spans_equal'])]
summary['bad_archives']=[a for a in archives if not(a['archive_binding']['hash_ok'] and a['raw_roundtrip_ok'] and a['exact_roundtrip_ok'])]
summary['AND_failures']=[a for a in groups if a['self_required'] or a['missing_edges']]
summary['producer_spans']=producer_spans
print(json.dumps(summary,indent=2))
