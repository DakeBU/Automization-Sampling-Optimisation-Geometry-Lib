#!/opt/anaconda3/bin/python
import datetime,hashlib,json,pathlib,stat,sys
sys.dont_write_bytecode=True
BASE=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0,str(BASE));import preservation_guard as guard
assert not (BASE/'manifest.json').exists(),'Refuse to refreeze phase5.'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
preserved=guard.verify_preserved(allow_own_append=True)
closeout=json.loads((BASE/'normal-V-closeout.json').read_text())
assert closeout['normal_API_invocations']==1 and closeout['state']=='VERIFIED'
assert sha(BASE/'normal-VERIFIED-append.exact.jsonl')==closeout['exact_append_sha256']=='90cc9126e265bd0e401e7bddf7593dc4505ea89c4091d80810c963d72e34bac9'
event=json.loads((BASE/'normal-VERIFIED-append.exact.jsonl').read_text())
assert event['worker_id']=='/root/cosine_gram_fresh_source_7e41d9'
assert (ROOT/guard.LEDGER).read_bytes()==(guard.PRIVATE/'ledger-before.raw.jsonl').read_bytes()+(BASE/'normal-VERIFIED-append.exact.jsonl').read_bytes()
assert (ROOT/guard.FRONTIER).read_bytes()==(BASE/'own-frontier-after.raw.json').read_bytes()
assert event['evidence']['original_proved_local_event']==json.loads((BASE/'original-PROVED_LOCAL-event.exact.jsonl').read_text())
assert event['evidence']['original_proved_local_evidence']==json.loads((BASE/'original-PROVED_LOCAL-evidence.json').read_text())
commands=[json.loads(x) for x in (BASE/'actual_commands.jsonl').read_text().splitlines()]
for row in commands:
    assert row['returncode']==0
    for stream in ['stdout','stderr']:
        path=BASE/row[stream+'_file'];assert sha(path)==row[stream+'_sha256'] and path.stat().st_size==row[stream+'_bytes']
# Private foreign data remain outside the portable tree and are made read-only.
for path in guard.PRIVATE.iterdir():
    if path.is_file():path.chmod(0o400)
guard.PRIVATE.chmod(0o700)
entries=[]
for path in sorted(BASE.rglob('*')):
    assert 'private-phase5-preservation' not in path.parts
    if path.is_file():
        path.chmod(0o444)
        entries.append({'path':str(path.relative_to(BASE)),'original_repo_path':str(path.relative_to(ROOT)),
                        'bytes':path.stat().st_size,'sha256':sha(path),'mode':'0444'})
manifest={'phase':'phase5-single-normal-source-VERIFIED-and-preserved-frontier-closeout',
          'payloads':entries,'excluded_self_and_receipt':['manifest.json','freeze_receipt.json'],
          'explicit_private_full_foreign_exclusion':str(guard.PRIVATE.relative_to(ROOT)),
          'outer_actual_freeze_files_packaged_separately_by_archive_manifest':True}
mp=BASE/'manifest.json';mp.write_text(json.dumps(manifest,indent=2)+'\n');mp.chmod(0o444)
receipt={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':manifest['phase'],
         'manifest_sha256':sha(mp),'actual_normal_V_event_sha256':sha(BASE/'normal-VERIFIED-append.exact.jsonl'),
         'normal_V_closeout_sha256':sha(BASE/'normal-V-closeout.json'),'once_marker_sha256':sha(BASE/'normal-V-once.permanent-marker.json'),
         'normal_API_calls':1,'source_actor':event['worker_id'],'original_owner_unchanged':closeout['owner_id_unchanged'],
         'mathematical_native_checked_commit':closeout['mathematical_native_checked_commit'],
         'metadata_checked_carrier':closeout['metadata_checked_carrier'],
         'payload_count':len(entries),'captured_successful_command_count':len(commands),
         'final_preservation_recheck':preserved,'frontier_before_sha256':sha(BASE/'own-frontier-before.raw.json'),
         'frontier_after_sha256':sha(BASE/'own-frontier-after.raw.json'),
         'all_six_reader_HOLD_remote_STABILIZING_lease_and_global_boundaries_retained':True,
         'private_full_foreign_data_not_included':True,'freeze_execution_record_outside_phase':'../phase5_freeze_execution.json',
         'manifest_excludes_itself_and_receipt':True}
rp=BASE/'freeze_receipt.json';rp.write_text(json.dumps(receipt,indent=2)+'\n');rp.chmod(0o444)
for path in sorted(BASE.rglob('*'),reverse=True):
    if path.is_dir():path.chmod(0o555)
BASE.chmod(0o555)
assert all(stat.S_IMODE(p.stat().st_mode)==0o444 for p in BASE.rglob('*') if p.is_file())
assert all(stat.S_IMODE(p.stat().st_mode)==0o555 for p in BASE.rglob('*') if p.is_dir())
assert stat.S_IMODE(BASE.stat().st_mode)==0o555
print(json.dumps({'manifest_sha256':sha(mp),'receipt_sha256':sha(rp),'payload_count':len(entries),
                  'normal_API_calls':1,'actual_normal_V_event_sha256':sha(BASE/'normal-VERIFIED-append.exact.jsonl'),
                  'frontier_before_sha256':sha(BASE/'own-frontier-before.raw.json'),'frontier_after_sha256':sha(BASE/'own-frontier-after.raw.json'),
                  'phase_directory_mode_observed':'0555','all_phase_file_modes_observed':'0444',
                  'all_phase_subdirectory_modes_observed':'0555','final_preservation_recheck':preserved,
                  'private_full_foreign_data_excluded':True},indent=2))
