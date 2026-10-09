from pathlib import Path
import json,hashlib,base64,os
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda d:H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def read(n):return json.loads((O/n).read_bytes())
run=read('review-run.json');core=dict(run);del core['run_sha256'];assert C(core)==run['run_sha256']
pins=read('review-payload-pins.json')
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT','native_semantic_decision']:
 row=pins[k];b=(O/row['name']).read_bytes();assert H(b)==row['RAW_sha256'] and len(b)==row['RAW_bytes'];assert H(b.replace(b'\r\n',b'\n'))==row['LF_sha256']
for row in run['owned_pre_finalization_RAW_LF_bindings']:
 b=(O/row['name']).read_bytes();assert H(b)==row['RAW_sha256'];assert H(b.replace(b'\r\n',b'\n'))==row['LF_sha256']
d=read('decision.json');complete=read('complete-RAW-decision.json');assert complete['source66']==d;assert d['review_run_sha256']==run['run_sha256'];core_d=dict(d);del core_d['review_run_sha256'];assert core_d==run['decisions']['source66'];assert complete['separately_reviewed_metadata_overlay']==run['decisions']['separately_reviewed_metadata_overlay']
slots={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
for decision,k in [(d,'semantic_slots'),(complete['separately_reviewed_metadata_overlay'],'seven_semantic_slots')]:
 assert set(decision[k])==slots
 for s in decision[k].values():assert s['original'] and s['reconstructed'] and s['evidence'] and s['relation']!='not-audited'
assert d['deltas']==[] and d['repairs']==[] and not d['source_mathematical_repair'];assert not d['full_Exposition'] and not d['PURIFIED']
inp=read('RAW-input-payload.json');assert inp==run['complete_named_RAW_INPUT_payload']
for row in inp['inputs']:
 b=base64.b64decode(row['complete_RAW_bytes_base64']);assert b==(O/row['name']).read_bytes();assert H(b)==row['pin']['RAW_sha256']
whole=inp['whole_primary'];b=base64.b64decode(whole['complete_RAW_bytes_base64']);assert H(b)==whole['pin']['RAW_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for row in read('closed-header-representation-reuse-pins.json')['parents']:assert H(Path(row['path']).read_bytes())==row['RAW_sha256']
primary=read('primary-first-adoption.json');assert primary['all_selected_math_items']==310
cov=read('source-coverage.compared.json');assert cov['count']==310 and cov['missing_source_items']==0 and cov['missing_alttext']==0 and cov['annotation_mismatch']==0
ex=read('literal-BODY-excerpt-audit.json');assert ex['step_count']==6
for s in ex['steps']:
 row=s['owned_excerpt'];assert H(Path(row['path']).read_bytes())==row['RAW_sha256']
check=read('final-reviewer-packet-binding-check.json');assert check['publication_binding_sha256']==d['publication_binding_sha256'];assert check['reviewer_packet_sha256']==d['reviewer_packet_sha256']
print(json.dumps(dict(schema='source66-actual-foreground-readback-v1',actual_pid=os.getpid(),whole_logical_run_sha256=run['run_sha256'],whole_logical_entire_object_deleting_only_top_level_run_sha256=True,complete_RAW_REVIEW_distinct=True,complete_RAW_DECISION_full7slots=True,complete_RAW_INPUT_allbytes=True,source_items=310,source_missing=0,BODY_regions=6,closed_parent_pins_unchanged=True,all_pre_finalization_owned_bytes_checked=True,source_mathematical_repair=False),sort_keys=True))
