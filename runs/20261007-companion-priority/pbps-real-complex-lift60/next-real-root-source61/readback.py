import hashlib,json,pathlib,sys
r=pathlib.Path('E:/Samplinglib'); o=pathlib.Path(sys.argv[1]); m=json.loads((o/'input.manifest.json').read_bytes()); n=0
def check(x):
 global n
 b=(r/x['path']).read_bytes(); l=b.replace(b'\r\n',b'\n'); assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['raw_sha256']; assert len(l)==x['lf_bytes'] and hashlib.sha256(l).hexdigest()==x['lf_sha256']; n+=1
for pair in m['raw_LF_pairs']:
 for k in ['original','raw_snapshot','lf_snapshot']: check(pair[k])
 assert (r/pair['original']['path']).read_bytes()==(r/pair['raw_snapshot']['path']).read_bytes()
 assert (r/pair['original']['path']).read_bytes().replace(b'\r\n',b'\n')==(r/pair['lf_snapshot']['path']).read_bytes()
check(m['primary']); raw=(r/m['primary']['path']).read_bytes(); anchors=json.loads((o/'primary.anchors.reused.json').read_bytes())
for x in anchors['exact_regions']: assert hashlib.sha256(raw[x['start_utf8_byte']:x['end_utf8_byte_exclusive']]).hexdigest()==x['slice_sha256']
for x in m['api_LF_spans']:
 check(x['original']); check(x['snapshot']); lines=(r/x['original']['path']).read_bytes().replace(b'\r\n',b'\n').splitlines(keepends=True); assert b''.join(lines[x['start_line']-1:x['end_line']])==(r/x['snapshot']['path']).read_bytes()
payload=json.loads((o/'named-source61.payload.json').read_bytes())
for k in ['contract','API','primary','inputs']: check(payload[k])
c=json.loads((o/'next-target.source-contract.json').read_bytes()); assert len(c['route_at_most_7_steps'])==7 and c['status']=='SOURCE_ONLY_NEXT_TARGET_PROPOSAL_NOT_STATEMENT_SEALED_NOT_CLAIMED'
print(json.dumps({'qualified_raw_LF_pins_checked':n,'primary_slices_checked':23,'API_spans':19,'input_pairs':15,'route_steps':7,'source_only':True,'compiler':False}))
