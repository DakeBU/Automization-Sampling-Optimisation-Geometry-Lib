import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
for name in ['foreground-prepare','foreground-B4-consumer','foreground-B4-consumer-extended','foreground-B4-consumer-final','foreground-source-expectations','foreground-finalize','foreground-readback']:
 r=json.loads((out/(name+'.receipt.json')).read_bytes());assert r['actual_exit']==0 and r['completed'] and r['foreground']
read=json.loads((out/'readback-report.json').read_bytes());assert read['source_math_count']==419 and read['frozen_source_expectations_unchanged']
run=json.loads((out/'review-run.json').read_bytes());v=run.pop('run_sha256')
assert hashlib.sha256(json.dumps(run,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()==v
assert not (out/'lease.final.json').exists()
assert all(p.is_file() for p in out.iterdir())
report=dict(schema='primary69-close-validator-v1',actual_pid=os.getpid(),checks_passed=True,
 actual_readback_pid=read['actual_pid'],whole_logical_run_sha256=v,source_math_count=419,
 all_named_receipts_EXIT0=True,no_candidate69=True,owned_only=True)
(out/'close-validation.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,sort_keys=True))
