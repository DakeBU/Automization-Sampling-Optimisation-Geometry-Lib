import hashlib,json,pathlib
ROOT=pathlib.Path('E:/Samplinglib'); OUT=pathlib.Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
count=0
def check(p):
    global count
    b=(ROOT/p['path']).read_bytes(); l=b.replace(b'\r\n',b'\n'); assert len(b)==p['bytes'] and sha(b)==p['raw_sha256']; assert len(l)==p['lf_bytes'] and sha(l)==p['lf_sha256']; count+=1
m=json.loads((OUT/'input.manifest.json').read_bytes()); assert len(m['raw_LF_pairs'])==19
for pair in m['raw_LF_pairs']:
    for k in ['original','raw_snapshot','lf_snapshot']:check(pair[k])
    raw=(ROOT/pair['original']['path']).read_bytes()
    assert raw==(ROOT/pair['raw_snapshot']['path']).read_bytes()
    assert raw.replace(b'\r\n',b'\n')==(ROOT/pair['lf_snapshot']['path']).read_bytes()
check(m['primary']); raw=(ROOT/m['primary']['path']).read_bytes()
b=json.loads((OUT/'source.boundary.before-candidate.json').read_bytes())
for x in b['reused_exact_regions']:assert sha(raw[x['start_utf8_byte']:x['end_utf8_byte_exclusive']])==x['slice_sha256']
g=json.loads((OUT/'source.graph.before-candidate.json').read_bytes()); c=json.loads((OUT/'source.coverage.before-candidate.json').read_bytes())
assert len(g['nodes'])==27 and len(g['edges'])==34 and c['regions']==23 and len(c['items'])==45
assert {x['region_id'] for x in c['items']}=={x['id'] for x in b['reused_exact_regions']}
assert all(x['classification'] in ['NODE','EXCLUDED'] for x in c['items'])
p=json.loads((OUT/'named-preproof61.payload.json').read_bytes())
for k in ['review','source_boundary','source_graph','coverage','inputs']:check(p[k])
r=json.loads((OUT/'statement-binder.review.json').read_bytes()); assert p['complete_review']==r
assert not r['blocking_deltas'] and not r['repairs'] and r['excess_count']==0
assert len(r['semantic_slots'])==2 and all(len(x)==7 for x in r['semantic_slots'])
assert not r['elaboration']['compiler_by_reviewer'] and not r['elaboration']['compiler_receipt_reviewed']
print(json.dumps(dict(qualified_raw_LF_pins_checked=count,raw_LF_input_pairs=19,primary_slices=23,coverage_items=45,source_graph_nodes=27,source_graph_edges=34,preproof_source_accepted=True,compiler=False,proof_credit=False)))
