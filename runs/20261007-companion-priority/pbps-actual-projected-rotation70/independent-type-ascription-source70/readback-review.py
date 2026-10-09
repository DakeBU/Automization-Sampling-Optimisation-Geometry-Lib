import base64,hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda d:json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
load=lambda n:json.loads((out/n).read_bytes())
payload=load('RAW-LF-input-payload.json');assert payload['count']==12
for e in payload['inputs']:
    a=e['attribution'];raw=base64.b64decode(e['RAW_base64']);lf=base64.b64decode(e['LF_base64'])
    assert raw==(out/a['name']).read_bytes()==pathlib.Path(a['original_path']).read_bytes()
    assert len(raw)==a['RAW_bytes'] and sha(raw)==a['RAW_sha256']
    assert lf==raw.replace(b'\r\n',b'\n') and len(lf)==a['LF_bytes'] and sha(lf)==a['LF_sha256']
run=dict(schema='type-ascription70-complete-independent-source-review-v1',decision=load('decision.json'),
    expectations_before_overlay=load('expectations.before-overlay.json'),finite_coverage=load('finite-coverage.json'),
    exact_line_map=load('exact-116-line-source-retention-map.json'),input_manifest=load('input-manifest.json'),
    negative_evidence=load('negative-observations.json'),no_Lean_compile_or_new_source_theorem_admission=True)
run['run_sha256']=sha(canonical(run))
(out/'review-run.json').write_text(json.dumps(run,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
named=[]
for n in ['review-run.json','decision.json','RAW-LF-input-payload.json']:
    b=(out/n).read_bytes();lf=b.replace(b'\r\n',b'\n')
    named.append(dict(name=n,RAW_bytes=len(b),RAW_sha256=sha(b),RAW_base64=base64.b64encode(b).decode('ascii'),
        LF_bytes=len(lf),LF_sha256=sha(lf),LF_base64=base64.b64encode(lf).decode('ascii'),LF_recipe='CRLF-to-LF only'))
(out/'complete-named-review-decision-input.json').write_text(json.dumps(dict(schema='type-ascription70-complete-named-review-decision-input-v1',
    whole_logical_run_sha256=run['run_sha256'],named=named),sort_keys=True,indent=2)+'\n',encoding='utf-8')
for e in named:assert base64.b64decode(e['RAW_base64'])==(out/e['name']).read_bytes()
print(json.dumps(dict(actual_readback_pid=os.getpid(),all12_RAW_LF_inputs_exact=True,complete_named_payload_exact=True,
    whole_logical_run_sha256=run['run_sha256']),sort_keys=True))
