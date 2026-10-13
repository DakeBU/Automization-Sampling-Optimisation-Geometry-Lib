import base64,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda d:json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
load=lambda n:json.loads((out/n).read_text(encoding='utf-8'))
run=load('review-run.json');logical=dict(run);runsha=logical.pop('run_sha256')
assert sha(canonical(logical))==runsha
manifest=load('final-input-manifest.json')
entries=manifest['prior_frozen_inputs']+manifest['final_current_inputs']+manifest['extra_named_negative_inputs']
assert len(entries)==132
def checkpack(p):
    raw=base64.b64decode(p['RAW_base64']);assert len(raw)==p['RAW_bytes'] and sha(raw)==p['RAW_sha256']
    assert raw==(out/p['name']).read_bytes()
    if p['binary']:
        assert 'LF_base64' not in p and 'LF_sha256' not in p
    else:
        lf=base64.b64decode(p['LF_base64']);assert lf==raw.replace(b'\r\n',b'\n')
        assert len(lf)==p['LF_bytes'] and sha(lf)==p['LF_sha256']
    return raw
payload=load('RAW-input-payload.json');assert len(payload['inputs'])==132
for actual,expected in zip(payload['inputs'],entries):
    assert actual['attribution']==expected
    raw=checkpack(actual['payload']);assert sha(raw)==expected['RAW_sha256'] and len(raw)==expected['RAW_bytes']
    # Read-only final-current freshness against exact named original files.
    assert raw==pathlib.Path(expected['original_path']).read_bytes(),expected['original_path']
named=load('complete-named-review-decision-input-payload.json')
assert named['whole_logical_run_sha256']==runsha and len(named['named'])==3
for p in named['named']:checkpack(p)
coverage=load('finite-repository-reader-coverage.json');assert len(coverage['checks'])==13
assert all(c['decision']=='PASS_BOUNDED' for c in coverage['checks'])
decision=load('repository-reader69.decision.json');assert decision['ready_to_close'] and not decision['blocking_findings'] and not decision['required_repairs']
result=dict(schema='repository-reader69-complete-payload-readback-v1',actual_pid=os.getpid(),
    complete_named_inputs=132,all_RAW_LF_payloads_and_originals_exact=True,
    binary_images_preserved_RAW=True,complete_named_review_decision_input_exact=True,
    whole_logical_run_sha256=runsha,whole_logical_deletes_ONLY_top_level_run_sha256=True)
(out/'complete-payload-readback.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,sort_keys=True))
