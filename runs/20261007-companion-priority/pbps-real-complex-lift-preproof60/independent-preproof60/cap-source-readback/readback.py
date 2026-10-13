import hashlib,json,pathlib,sys
r=pathlib.Path('E:/Samplinglib'); p=pathlib.Path(sys.argv[1]); x=json.loads(p.read_bytes())
for k in ['primary','raw_snapshot','supplemental_context','immutable_main_run']:
 q=x[k]; b=(r/q['path']).read_bytes(); l=b.replace(b'\r\n',b'\n'); assert len(b)==q['bytes'] and hashlib.sha256(b).hexdigest()==q['raw_sha256']; assert hashlib.sha256(l).hexdigest()==q['lf_sha256']
b=(r/x['primary']['path']).read_bytes(); z=x['source_region']; assert b[z['start_utf8_byte']:z['end_utf8_byte_exclusive']]==(r/x['raw_snapshot']['path']).read_bytes()
print(json.dumps({'qualified_pins':4,'primary_cap_literal':True,'main_closed_artifacts_unchanged':True,'scope':'source index supplement only; exact headers accepted unchanged'}))
