import base64, hashlib, json, os, pathlib, re
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
run=json.loads((out/'review-run.json').read_bytes())
expected=run.pop('run_sha256');assert sha(canon(run))==expected
assert run['candidate69_seen'] is False and run['header69_seen'] is False
payload=json.loads((out/'RAW-input-payload.json').read_bytes())
assert run['named_complete_RAW_LF_input_payload']==payload
for x in payload['inputs']:
 b=base64.b64decode(x['complete_RAW_bytes_base64']);lf=base64.b64decode(x['complete_LF_bytes_base64'])
 assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256']
 assert b.replace(b'\r\n',b'\n')==lf and len(lf)==x['LF_bytes'] and sha(lf)==x['LF_sha256']
 assert pathlib.Path(x['source_path']).read_bytes()==b
for x in run['named_complete_source_expectation_payload']['complete_outputs']:
 b=base64.b64decode(x['complete_RAW_bytes_base64'])
 assert sha(b)==x['RAW_sha256'] and (out/x['name']).read_bytes()==b
inv=json.loads((out/'source-coverage-inventory.json').read_bytes())
ri=json.loads((out/'source-input-regions.json').read_bytes())
regions={x['name']:x for x in ri['regions']}
assert inv['count']==419 and inv['all_classified'] and len(inv['math_items'])==419
for x in inv['math_items']:
 b=(out/('source.'+x['region']+'.RAW.html')).read_bytes()
 a,z=x['region_RAW_range_end_exclusive'];assert sha(b[a:z])==x['RAW_sha256']
 offset=regions[x['region']]['source_RAW_range_end_exclusive'][0]
 assert x['source_RAW_range_end_exclusive']==[a+offset,z+offset] and x['source_role']!='pending-independent-classification'
finite=json.loads((out/'finite-coverage-manifest.json').read_bytes())
assert len(finite['entries'])==419 and sha(canon(finite['entries']))==finite['entries_canonical_sha256']
graph=json.loads((out/'source-proof-graph.json').read_bytes());ids={x['id'] for x in graph['nodes']}
assert len(ids)==22 and all(e['parent'] in ids and e['child'] in ids for e in graph['edges'])
for n in graph['nodes']:
 for r in n['primary_math']:
  x=next(i for i in inv['math_items'] if i['id']==r['id'])
  assert r['RAW_sha256']==x['RAW_sha256'] and r['source_RAW_range_end_exclusive']==x['source_RAW_range_end_exclusive'] and r['alttext']==x['alttext']
freeze=json.loads((out/'source-expectations-frozen.json').read_bytes())
assert sha((out/'source-proof-graph.json').read_bytes())==freeze['source_graph_RAW_sha256']
assert sha((out/'source-expectations.json').read_bytes())==freeze['expectations_RAW_sha256']
assert sha((out/'finite-coverage-manifest.json').read_bytes())==freeze['finite_coverage_RAW_sha256']
receipts=[]
for p in sorted(out.glob('foreground-*.receipt.json')):
 r=json.loads(p.read_bytes());assert r['actual_exit']==0 and r['completed'] and r['foreground'];receipts.append(dict(name=p.name,pid=r['actual_pid'],actual_exit=0))
report=dict(schema='primary69-complete-readback-v1',actual_pid=os.getpid(),whole_logical_hash_verified=expected,
 deleted_only_top_level_run_sha256=True,complete_inputs_verified=len(payload['inputs']),complete_outputs_verified=len(run['named_complete_source_expectation_payload']['complete_outputs']),
 source_math_count=419,source_graph_nodes=len(ids),source_graph_edges=len(graph['edges']),all_source_offsets_hashes_and_typed_roles_verified=True,
 frozen_source_expectations_unchanged=True,actual_foreground_receipts=receipts,
 candidate69_seen=False,mathematical_or_formal_completion_claim=False)
(out/'readback-report.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,sort_keys=True))
