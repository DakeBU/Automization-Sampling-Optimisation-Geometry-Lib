"""Explicit byte-exact public custody of this pre-API own-path exception; never exports full guards."""
import hashlib,json
from pathlib import Path
OUT=Path(__file__).resolve().parent;OWN=OUT.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):
    with Path(p).open('x') as f:f.write(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
source=OWN/'local-private-guards/window1-OS-process';dest=OUT/'original-OS-streams';dest.mkdir(exist_ok=False)
receipt=json.loads((source/'receipt.private.json').read_text())
assert set(receipt['environment_explicit_whitelist'])=={'HOME','PATH','LC_ALL','PYTHONDONTWRITEBYTECODE','PYTHONIOENCODING','GIT_OPTIONAL_LOCKS','ASTIS_ATLAS_ROOT'}
assert receipt['actual_exit_code']==1 and receipt['stdout_bytes']==0 and receipt['stderr_bytes']==1952
copies=[]
for before,after in [('stdout.raw','stdout.raw'),('stderr.raw','stderr.raw'),('receipt.private.json','receipt.original.json')]:
    raw=(source/before).read_bytes()
    with (dest/after).open('xb') as f:f.write(raw)
    assert (dest/after).read_bytes()==raw
    copies.append({'original_source':str((source/before).relative_to(OWN)),'selected_copy':str((dest/after).relative_to(OWN)),'bytes':len(raw),'sha256':sha(dest/after),'byte_exact_no_trim_reconstruction_or_normalization':True})
write(OUT/'original-OS-stream-custody.json',{'schema':'R17-preAPI-path-exception-original-OS-byte-custody-v1','copies':copies,'ROOT_explicitly_authorized_this_own_exception_stream_public_selection':True,'stderr_is_the_actual_relative_path_ValueError_not_API_log_or_foreign_state_map':True,'original_receipt_has_explicit7_key_environment_whitelist_only':'Known HOME/PATH and ASTIS_ATLAS_ROOT literal path references; no credentials, inherited full environment, foreign workspace map or ATLAS body.','full_guard_maps_raw_A_D_ledgers_and_index_not_selected':True})
write(OUT/'invocation-only-successor-choice.json',{'schema':'R17-preserved-failure-successor-choice-v1','old_scripts_not_modified':True,'path_normalization_code_diff_remains_unapplied_proposal':True,'ROOT_requested_preferred_successor':'Copy all3 final scripts byte-exact into a new own directory, fresh guards/output namespace, and pass an ABSOLUTE authorization file path. No rerun in failed namespace; no normalAPI replay, rollback, math/source/reader/gate rerun.'})
names=['verification_common.py','verify_once.py','project_cell_once.py','window1.ROOT-authorization.v1.json','window1-OS-receipt.public.json','window1-stopped.public.json','window1-public-selected-originals.manifest.json','authorization.schema.json','window1.contract.draft.json','PROVED_LOCAL-original25.exact.json']
names+=['window1-failure-review-v1/'+n for n in ['check_preservation.py','freeze_failure_custody.py','postfailure-preservation.outcome.json','path-normalization.proposal.json','path-normalization.proposed.exact.diff','original-OS-stream-custody.json','invocation-only-successor-choice.json','original-OS-streams/stdout.raw','original-OS-streams/stderr.raw','original-OS-streams/receipt.original.json','process/receipt.json','process/stdout.raw','process/stderr.raw']]
assert all('local-private-guards/' not in n for n in names)
write(OUT/'public-selected-originals.manifest.json',{'schema':'R17-failed-preAPI-window-explicit-own-public-leaves-v1','status':'ACTUAL_EXIT1_API0_PL1_V0_ALL_POSTFAILURE_GUARDS_PASSED','files':[{'path':n,'bytes':(OWN/n).stat().st_size,'sha256':sha(OWN/n)} for n in names],'actual_OS_streams_and_original_OS_receipt_are_byte_exact_copies_with_source_custody':True,'full_guardmaps_foreignstates_index_fullledgers_APIlogs_cache_ATLAS_body_credentials_excluded':True,'original_failure_and_scripts_unchanged_no_replay':True})
print(json.dumps({'manifest_sha256':sha(OUT/'public-selected-originals.manifest.json'),'leaves':len(names),'stream_custody_sha256':sha(OUT/'original-OS-stream-custody.json')}))
