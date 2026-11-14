from pathlib import Path
import json,hashlib,os
from datetime import datetime,timezone
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/normal-verification-v2';V1=B.parent/'normal-verification-v1'
DEST='research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence/normal-verification/mv_src_6e28/originals'
def sha(b):return hashlib.sha256(b).hexdigest()
def rec(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(b),'sha256':sha(b)}
def wr(n,d):
 with (B/n).open('x') as f:f.write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def public_files(base):
 for cur,ds,fs in os.walk(base):
  ds[:]=[d for d in ds if d not in ['private','__pycache__']]
  for f in fs:
   p=Path(cur)/f
   if p.is_file():yield p
assert json.loads((B/'postguard-comparison.json').read_bytes())['all_pass']
api=json.loads((B/'normal-API-receipt.json').read_bytes());assert api['actual_API_calls']==1 and api['actual_API_failures']==0 and api['exit']==0
assert (B/'normal-API.stderr').read_bytes()==b''
# Keep all prior failure-phase public bytes in the transport index; never rewrite them.
core=sorted(public_files(B));v1=sorted(public_files(V1))
result={'schema_version':1,'phase':'normal-verification-v2','result':'S_LOCAL_INDEPENDENTLY_VERIFIED_NORMAL_API_ONCE','advance_id':'ASTIS-SA-20261112-RealMatrixPositiveIntegral','cell':'research-wiki/frontier-cells/ASTIS-SHARED-REAL-MATRIX-POSITIVE-INTEGRAL.json','verifier_id':'/root/mv_fresh_source_6e28','heldHEAD':'5f69ac83737e497210d8d8ad9628c45d83089458','mathCommit':'9964c33c4599f85d27dc8687e8bd6fdb5c44ff49','actual_API_calls':1,'actual_API_failures':0,'pre_V_count':0,'post_V_count':1,'normal_once_sentinel':True,'PL_original_fields_inline_unchanged':20,'all_four_held_gates_actual_exit_zero':True,'full_prepost_foreign_guard_passed':True,'previous_failed_phase':{'heldHEAD':'7d6d61f298e882f54c4bc36b1fb67502d2801e77','API_calls':0,'API_failures':0,'publication_exit':1,'other3gates':'NOT_RUN','frozen_result':rec(V1/'normal-VERIFIED-result.json'),'freeze':rec(V1/'FAILED-PHASE-FROZEN.json')},'own_local_process_failures':'See process-failures-and-exposure.json and verbatim transcribed tool-visible failures. These are not API failures.','normal_command_receipt':rec(B/'normal-command-receipt.json'),'full_V_payload':rec(B/'VERIFIED-evidence.full.json'),'exact_raw_one_line_append':rec(B/'actual-VERIFIED-append.exact.jsonl'),'ownC_before':rec(B/'ownC.before.exact.json'),'ownC_after':rec(B/'ownC.after.exact.json'),'all_core_outputs':[rec(p) for p in core],'v1_originals_count':len(v1),'private_local_only':{'full_snapshots':['before','precall','after'],'counts':{'foreign_full_advances':309,'full_discoveries':43,'foreign_regular_frontiers_including_README':469,'tracked_files':132567,'qualified_controls_including_historical_artifacts':117409},'commitments':json.loads((B/'postguard-comparison.json').read_bytes())['private_snapshot_hashes'],'native_large_lossless_dumps':'local only; not exported or semantically fully read','private_full_bytes_exported':False},'boundary':{'S':'locally independently verified','P':'actual uncentered source-reviewed/compiled consumer only','T_fullR9_main_Goal':'HOLD','integration_publication_purification':'HOLD','owner_released':False,'commit_made':False},'terminal_index_rule':'This file lists all already-existing core outputs. Later original manifest/seal/portable manifest/post-seal envelope are externally hash-bound; no recursive self-hash is fabricated.'}
wr('normal-VERIFIED-result.json',result)
files=sorted(public_files(B));wr('originals-manifest.json',{'kind':'complete-public-normal-phase-originals','files':[rec(p) for p in files],'private_excluded':True,'self_hash_external':True})
wr('NORMAL-VERIFIED-FROZEN.json',{'schema_version':1,'phase':'NORMAL_VERIFIED_FROZEN','frozen_utc':datetime.now(timezone.utc).isoformat(),'verifier_id':'/root/mv_fresh_source_6e28','heldHEAD':result['heldHEAD'],'mathCommit':result['mathCommit'],'result':rec(B/'normal-VERIFIED-result.json'),'originals_manifest':rec(B/'originals-manifest.json'),'actual_API_calls':1,'actual_API_failures':0,'pre_V_count':0,'post_V_count':1,'append':rec(B/'actual-VERIFIED-append.exact.jsonl'),'private_aggregate_commitments':result['private_local_only']['commitments'],'prior_source_freezes_unchanged':True,'remaining_HOLD':result['boundary'],'seal_self_hash':'external only'})
portable=[]
for p in sorted(v1+list(public_files(B))):
 record=rec(p);rel=p.relative_to(B.parent);portable.append({'source_path':record['path'],'destination_path':DEST+'/'+str(rel),'bytes':record['bytes'],'sha256':record['sha256'],'copy_rule':'Exact byte copy only; do not rewrite independent decision, paths, payload, raw event or run. NEVER replay API script.'})
wr('portable-originals-manifest.json',{'schema_version':1,'kind':'normal-verification-original-byte-transfer','verifier':'/root/mv_fresh_source_6e28','records':portable,'files':len(portable),'bytes':sum(x['bytes'] for x in portable),'normal_api_replay_forbidden':True,'private_foreign_control_index_blobs_and_native_gzip_excluded':True,'bootstrap_raw_archival_complete':False,'manifest_self_hash_external':True,'postseal_envelope':'Later postseal-command receipt/stdout/stderr and output-index are externally hashed and supplied separately.'})
print(json.dumps({k:rec(B/k) for k in ['normal-VERIFIED-result.json','originals-manifest.json','NORMAL-VERIFIED-FROZEN.json','portable-originals-manifest.json']},indent=2))
