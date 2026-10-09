import hashlib,json,os,pathlib
out=pathlib.Path(__file__).resolve().parent
load=lambda n:json.loads((out/n).read_text(encoding='utf-8'))
assert not (out/'lease.final.json').exists()
for label in ['freeze-expectations','expected-code','reused-closures','dom-helper','ingest-final-packet','current-dom',
              'copy-download-review','aggregate-context','aggregate-review','finalize-review','readback-review']:
    r=load(label+'.receipt.json');assert r['actual_exit']==0 and r['completed'] and r['foreground'],label
decision=load('repository-reader69.decision.json');readback=load('complete-payload-readback.json')
assert decision['verdict']=='ACCEPT_LOCAL_REPOSITORY_AND_SCOPED_READER69' and readback['complete_named_inputs']==132
assert len(load('finite-repository-reader-coverage.json')['checks'])==13
assert all((out/n).is_file() for n in ['close-native-lease.py','postclose-readonly.py','RAW-input-payload.json',
    'complete-named-review-decision-input-payload.json','review-run.json','negative-observations.json'])
assert not any(p.suffix=='.pyc' for p in out.rglob('*'))
result=dict(schema='repository-reader69-preclose-native-validation-v1',actual_pid=os.getpid(),ready_for_last_lease=True,
    all_11_prerequisite_foreground_stages_EXIT0=True,complete_named_inputs=132,finite_checks=13,
    all_helpers_negative_and_terminal_files_to_be_in_manifest=True,no_native_closed_tree_modified=True,
    no_canonical_Git_ledger_Goal_edits=True)
(out/'closure-readiness.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,sort_keys=True))
