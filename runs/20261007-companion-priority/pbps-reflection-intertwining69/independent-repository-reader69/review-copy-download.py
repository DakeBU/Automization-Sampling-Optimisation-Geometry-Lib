import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
expected=json.loads((out/'expected-code-and-reader-payload.before-final-packet.json').read_text(encoding='utf-8'))
d=json.loads((out/'current.081.copy-unit0-copy-and-download.inspect.json').read_text(encoding='utf-8'))
raw=(out/'current.014.ReflectionIntertwining.lean').read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
assert len(raw)==21072 and sha(raw)=='7bbaae1abd67305749d385153019061eb055a7968a707f919e7d9ac9fc21846d'
assert len(d['panels'])==3 and len(d['downloads'])==3
panels=[]
for i,(actual,exp) in enumerate(zip(d['panels'],expected['code_panels'])):
    assert actual['callbackCalled'] and actual['copiedExactly'] and actual['status']=='Copied'
    assert actual['code']==exp['text']
    panels.append(dict(panel=exp['panel'],actual_callback_observed=True,exact_code=True,
        UTF8_bytes=len(actual['code'].encode('utf-8')),UTF8_sha256=sha(actual['code'].encode('utf-8'))))
downloads=[]
for i,actual in enumerate(d['downloads']):
    actual_bytes=actual['text'].encode('utf-8')
    assert actual['status']==200 and actual_bytes==raw
    downloads.append(dict(index=i,href=actual['href'],http_status=actual['status'],
        exact_UTF8_roundtrip_RAW_bytes=len(actual_bytes),exact_RAW_sha256=sha(actual_bytes),
        captured_field_named_bytes=actual['bytes'],captured_field_interpretation='JavaScript UTF-16 string length, not byte length',
        RAW_UTF8_roundtrip_verified_independently=True))
assert d['initialFolded'] and d['copyProbeUsesIsolatedPageClipboardCallback'] and not d['physicalOSClipboardTest']
result=dict(schema='repository-reader69-actual-copy-download-review-v1',actual_pid=os.getpid(),
    code_panel_count=3,callback_count=3,download_count=3,code_panels=panels,downloads=downloads,
    copy_probe='Actual page click handler with isolated clipboard callback; physical OS clipboard not tested',
    download_probe='Three actual HTTP200 fetch responses; captured valid UTF8 text independently encodes to the complete exact RAW module',
    no_live_deployment_or_OS_clipboard_claim=True,
    nonblocking_metadata_observation='The capture bytes field is JS string length19568. Exact UTF8 RAW is21072 bytes with the fixed module hash; no content discrepancy.')
(out/'actual-copy-download-review.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['code_panels','downloads']},sort_keys=True))
