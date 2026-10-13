import hashlib,json,pathlib,sys
ROOT=pathlib.Path('E:/Samplinglib'); OUT=pathlib.Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
count=0
def check(p):
    global count
    b=(ROOT/p['path']).read_bytes(); l=b.replace(b'\r\n',b'\n')
    assert len(b)==p['bytes'] and sha(b)==p['raw_sha256'],p['path']
    assert len(l)==p['lf_bytes'] and sha(l)==p['lf_sha256'],p['path']; count+=1
m=json.loads((OUT/'input.manifest.json').read_bytes())
assert m['original_lease_inputs']==16 and len(m['raw_LF_pairs'])==22
for pair in m['raw_LF_pairs']:
    for k in ['original','raw_snapshot','lf_snapshot']: check(pair[k])
    b=(ROOT/pair['original']['path']).read_bytes()
    assert b==(ROOT/pair['raw_snapshot']['path']).read_bytes()
    assert b.replace(b'\r\n',b'\n')==(ROOT/pair['lf_snapshot']['path']).read_bytes()
check(m['primary']); source=(ROOT/m['primary']['path']).read_bytes()
for r in m['exact_primary_slices']:
    check(r['snapshot']); assert source[r['start_utf8_byte']:r['end_utf8_byte_exclusive']]==(ROOT/r['snapshot']['path']).read_bytes()
for s in m['api_LF_spans']:
    check(s['original']);check(s['snapshot'])
    lines=(ROOT/s['original']['path']).read_bytes().replace(b'\r\n',b'\n').splitlines(keepends=True)
    assert b''.join(lines[s['start_line']-1:s['end_line']])==(ROOT/s['snapshot']['path']).read_bytes()
payload=json.loads((OUT/'named-source-review.payload.json').read_bytes())
for p in payload['decisions']: check(p)
for k in ['source_boundary','body_publication_scope','inputs']: check(payload[k])
for i in range(2):
    d=json.loads((OUT/f'source.{i}.decision.sealed.json').read_bytes())
    assert len(d['semantic_slots'])==7 and d['verdict']=='equivalent-after-elaboration'
    assert not any(x['blocking'] for x in d['deltas']) and not d['repairs'] and d['excess_count']==0
if len(sys.argv)>1 and sys.argv[1]=='final':
    run=json.loads((OUT/'run.json').read_bytes()); logical=run.pop('run_sha256'); assert sha(canon(run))==logical
    assert sha((OUT/'named-source-review.payload.json').read_bytes())==run['named_source_payload_sha256']
    for p in run['outputs']: check(p)
    for i in range(2):
        expected=json.loads((OUT/f'source.{i}.decision.sealed.json').read_bytes()); expected['review_run_sha256']=logical
        actual=json.loads((OUT/f'source.{i}.review.json').read_bytes()); assert actual==expected
print(json.dumps(dict(mode='final' if len(sys.argv)>1 else 'pre',qualified_raw_LF_pin_checks=count,original_lease_inputs=16,exact_input_pairs=22,primary_regions=23,private_providers=26,formula_steps=8,blocking_deltas=0,compiler_run=False),ensure_ascii=True))
