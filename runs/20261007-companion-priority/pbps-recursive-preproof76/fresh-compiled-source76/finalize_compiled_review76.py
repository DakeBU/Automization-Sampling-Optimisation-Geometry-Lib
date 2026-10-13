from pathlib import Path
import hashlib, json, os

out=Path(__file__).resolve().parent
assert not (out/'CLOSED_LAST.json').exists()
path=out/'compiled-source-review76.json'
before=path.read_bytes()
original=(out/'initial-compiled-report76'/'compiled-source-review76.json').read_bytes()
assert before==original
report=json.loads(before)
assert report['writer_pid']==46836
assert report['state']==report['source_review']['state']=='accepted'
report['audit_fields']['state']='accepted'
report['substantive_author_writer_pid']=46836
report['substantive_author_actual_exit_evidence']='write_compiled_review76.foreground-exit.json'
report['writer_pid']=os.getpid()
report['writer_actual_exit_evidence']='finalize_compiled_review76.foreground-exit.json is recorded by the foreground runner after this process terminates; no exit is self-asserted.'
report['native_finalization']={'operation':'Explicitly export the already independently justified accepted state in audit_fields as well as source_review. No mathematical verdict, logical reasoning, source mapping, input or code changed.','preserved_initial_report':'initial-compiled-report76/compiled-source-review76.json','initial_report_RAW_sha256':hashlib.sha256(before).hexdigest(),'failed_rerender_preserved':'write_compiled_review76.attempt2.foreground-exit.json records the exclusive-create guard exit1 before any output write.'}
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
path.write_bytes(data)
print(json.dumps({'status':'FINAL_NATIVE_FIELDS_EXPLICIT','writer_pid':os.getpid(),'report_RAW_sha256':hashlib.sha256(data).hexdigest(),'review_run_sha256':report['review_run_sha256'],'packet_sha256':report['packet_sha256'],'publication_binding_sha256':report['publication_binding_sha256']},indent=2))
