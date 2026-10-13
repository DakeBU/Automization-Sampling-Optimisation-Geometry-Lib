import json,pathlib,hashlib,os
D=pathlib.Path(__file__).resolve().parent
q=json.loads((D/'inputs.json').read_bytes())
for row in q['inputs']:
 b=pathlib.Path(row['path']).read_bytes();l=b.replace(b'\r\n',b'\n')
 assert len(b)==row['bytes'] and len(l)==row['lf_bytes'] and hashlib.sha256(b).hexdigest()==row['raw_sha256'] and hashlib.sha256(l).hexdigest()==row['lf_sha256']
print(json.dumps(dict(pid=os.getpid(),input_count=len(q['inputs']),all_inputs_match=True)))
