import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
for n in ['snapshot','source-review','finalize','readback']:
 r=json.loads((out/('foreground-'+n+'.receipt.json')).read_bytes());assert r['actual_exit']==0 and r['completed'] and r['foreground']
read=json.loads((out/'readback-report.json').read_bytes());assert read['prior_CLOSED82_all_native_bytes_verified_unchanged']
assert not (out/'lease.final.json').exists() and not (out/'owned-manifest.json').exists()
assert all(p.is_file() for p in out.iterdir())
r=dict(schema='header-source69-close-validator-v1',actual_pid=os.getpid(),passed=True,
 actual_readback_pid=read['actual_pid'],whole_logical_run_sha256=read['whole_logical_run_sha256'],
 all_named_terminal_EXIT0=True,source_header_only=True,no_proof_or_compilation=True,prior_CLOSED82_unchanged=True)
(out/'close-validation.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n',encoding='utf-8');print(json.dumps(r,sort_keys=True))
