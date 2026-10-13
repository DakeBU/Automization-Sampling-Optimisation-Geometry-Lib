from common import *
checks=load(B/'whole-proof-review54/checks.json'); stages=[]; leases=[]; negatives=[]
assert checks['actual_four_parent_calls'] and checks['no_private_provider_or_extra_instance'] and checks['T54_original_to_successor_operatively_corrected']
for e in checks['preproof_native_logical_runs']:
 assert equal(e['input']); run=load(e['input']['path']); actual=selfcheck(e['input']['path'],e['full_self_field'])
 assert actual['logical_sha256']==e['full_logical_sha256']
 if 'payload_field' in e: assert logical(run['run_binding_payload'])==run[e['payload_field']]==e['payload_sha256']
 stages.append(dict(original_record=e,actual_current=actual,payload_verified='payload_field' in e))
for e in checks['preproof_actual_CLOSED_leases']:
 assert equal(e['input']); d=load(e['input']['path']); assert d==e['actual_native_fields']
 assert d['read']==d['write']=='CLOSED' and d.get('Python',d.get('python'))=='CLOSED' and d['compiler']=='NOT_STARTED_CLOSED'
 leases.append(dict(input=pin(e['input']['path']),actual_native_fields=d))
for row in checks['preserved_negatives']:
 for k in ['status','source','log','lease']: assert equal(row[k])
 st=load(row['status']['path']); le=load(row['lease']['path']); assert st['exit_code']==le['exit_code']==row['exit_code'] and le['status']=='CLOSED'
 text=path(row['log']['path']).read_text(encoding='utf-8'); assert ('sorryAx' in text)==row['failed_only_compiler_sorryAx']
 if row['failed_only_compiler_sorryAx']: assert row['exit_code']==1
 negatives.append(row)
assert len(negatives)==7 and sum(r['exit_code']==1 for r in negatives)==5
sourceinputs=load(B/'reviewer.source.input-bindings.json')['original566_current_pins']; rootlease=load(B/'source.review.lease.json')
by=lambda rows: {e['path'].replace('\\','/'):(e['raw_sha256'],e['lf_sha256'],e['bytes']) for e in rows}
assert len(rootlease['input_artifacts'])==566 and by(rootlease['input_artifacts'])==by(sourceinputs)
assert rootlease['read_lease']==rootlease['write_lease']==rootlease['Python_lease']=='CLOSED' and rootlease['compiler_lease']=='NOT_STARTED_CLOSED' and not rootlease['compiler_started']
sourcelease=load(B/'reviewer.source.lease.json'); assert sourcelease['read']==sourcelease['write']==sourcelease['Python']=='CLOSED' and sourcelease['compiler']=='NOT_STARTED_CLOSED'
dr=load(B/'anonymous-decoder/run.json'); dl=load(B/'anonymous-decoder/lease.json'); br=load(B/'anonymous-decoder/binding-receipt.json')
for d in [dr,dl]:
 for e in d['input_artifacts']: assert equal(e)
dm=dr['opening_snapshot_mapping']; assert equal(dm['immutable_snapshot_pin']) and equal(dm['opening_lease_pin'],dm['immutable_snapshot_path']) and load(dm['immutable_snapshot_path'])['status']=='OPEN'
assert dl['read_lease']==dl['write_lease']==dl['Python_lease']=='CLOSED' and dl['compiler_lease']=='NOT_STARTED_CLOSED'
for original,portable in br['historical_neutral_path_map'].items():
 for e in br['output_artifacts']:
  p=path(e['path']); relative=p.relative_to(path(portable)); assert path(original).joinpath(relative).read_bytes()==p.read_bytes()
dump('history.checks.json',dict(status='PASS',preproof_complete_native_runs=stages,preproof_actual_CLOSED_leases=leases,original_topology_negative_minimal_repair_and_operative_correction_preserved=True,original_7_production_Test_attempts=negatives,failed_attempts=5,successful_attempts=2,failed_only_sorryAx_not_admitted=True,root_source_566_original_inputs_exactly_match_manifest=True,decoder_actual_input_pins=[pin(e['path']) for e in dr['input_artifacts']],decoder_original_opening_lease_snapshot_matches=True,decoder_private_portable_paths_identical=True,source_decoder_leases_all_CLOSED=True,future55_semantics_or_files_read=False,new_compiler_invocations=0))
print(json.dumps(dict(status='PASS',preproof_full_runs=5,preproof_closed_leases=5,original_production_Test_attempts=7,failures_preserved=5,source_lease_original_inputs=566,decoder_actual_inputs=2)))
