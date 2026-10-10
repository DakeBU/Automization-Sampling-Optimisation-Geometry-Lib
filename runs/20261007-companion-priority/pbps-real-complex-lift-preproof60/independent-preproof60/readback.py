import hashlib,json,pathlib,sys
ROOT=pathlib.Path('E:/Samplinglib'); OUT=pathlib.Path(__file__).resolve().parent
def digest(b): return hashlib.sha256(b).hexdigest()
def check(p):
    b=(ROOT/p['path']).read_bytes(); l=b.replace(b'\r\n',b'\n')
    assert len(b)==p['bytes'] and digest(b)==p['raw_sha256'], p['path']
    assert len(l)==p['lf_bytes'] and digest(l)==p['lf_sha256'], p['path']
manifest=json.loads((OUT/'input.manifest.json').read_bytes())
count=0
for pair in manifest['qualified_inputs']:
    for key in ['original','raw_snapshot','lf_snapshot']:
        check(pair[key]); count+=1
    assert (ROOT/pair['original']['path']).read_bytes()==(ROOT/pair['raw_snapshot']['path']).read_bytes()
    assert (ROOT/pair['original']['path']).read_bytes().replace(b'\r\n',b'\n')==(ROOT/pair['lf_snapshot']['path']).read_bytes()
check(manifest['primary']); count+=1
source=json.loads((OUT/'primary.exact-regions.json').read_bytes()); raw=(ROOT/source['primary']['path']).read_bytes()
for r in source['regions']:
    check(r['snapshot']); count+=1
    assert raw[r['start_utf8_byte']:r['end_utf8_byte_exclusive']]==(ROOT/r['snapshot']['path']).read_bytes()
for s in manifest['api_LF_spans']:
    check(s['original']); check(s['snapshot']); count+=2
    lines=(ROOT/s['original']['path']).read_bytes().replace(b'\r\n',b'\n').splitlines(keepends=True)
    assert b''.join(lines[s['start_line']-1:s['end_line']])==(ROOT/s['snapshot']['path']).read_bytes()
payload=json.loads((OUT/'named-preproof-source.payload.json').read_bytes())
for k in ['review','source_graph','coverage','primary']: check(payload[k]); count+=1
for p in payload['headers']: check(p); count+=1
graph=json.loads((OUT/'source.graph.json').read_bytes()); coverage=json.loads((OUT/'source.coverage.json').read_bytes())
assert len(source['regions'])==22 and len(coverage['items'])==43
assert len(graph['nodes'])==14 and len(graph['edges'])==17
assert {x['region_id'] for x in coverage['items']}=={x['id'] for x in source['regions']}
assert all(x['classification'] in ['NODE','EXCLUDED'] for x in coverage['items'])
review=json.loads((OUT/'statement.review.json').read_bytes())
assert review['status']=='ACCEPTED_PREPROOF_STATEMENT_AND_BINDER_SCOPE_ONLY'
assert len(review['seven_slots'])==7 and not review['blocking_deltas'] and not review['repairs']
assert all(x['exit_code']==0 and 'TYPE' in x['scope'] for x in review['elaboration'])
assert review['no_compiler_by_reviewer']
print(json.dumps(dict(qualified_pin_checks=count,exact_input_pairs=len(manifest['qualified_inputs']),source_regions=22,coverage_items=43,nodes=14,edges=17,scope='Exact preproof source/binder acceptance; TYPE only; no proof/root/VERIFIED'),ensure_ascii=True))
