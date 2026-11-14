from pathlib import Path
import json,hashlib,os
from datetime import datetime,timezone
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=R/'.astis/semantic-neutral-20261112/mv_src_6e28/r9-normal-verification/preparation';DEST='research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence/normal-verification/mv_src_6e28/originals/r9-normal-verification/preparation'
def rec(p):
 a=p.read_bytes();return {'path':str(p.relative_to(R)),'bytes':len(a),'sha256':hashlib.sha256(a).hexdigest()}
def public():
 for cur,ds,fs in os.walk(B):
  ds[:]=[d for d in ds if d!='private']
  for n in fs:
   p=Path(cur)/n
   if p.is_file():yield p
def wr(n,d):
 with (B/n).open('x') as f:f.write(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
status=json.loads((B/'PREPARATION-STATUS.json').read_bytes());assert status['normal_API_calls_by_this_verifier']==0 and status['final_held_HEAD'] is None
wr('originals-manifest.json',{'public_files':[rec(p) for p in sorted(public())],'private_full_guard_data_excluded':True,'private_commitment_only':rec(B/'private/ROOT-successor-guard.hash-copy-only.private.json'),'self_hash_external':True})
wr('PREPARATION-FROZEN.json',{'phase':'R9_NORMAL_VERIFICATION_PREPARATION_FROZEN_HOLD','frozen_utc':datetime.now(timezone.utc).isoformat(),'reviewer':'/root/mv_fresh_source_6e28','status':'HOLD_PENDING_NATIVE_CURRENTREADER_FINALHELD_4GATES_AND_ROOT_RELEASE','actual_math_commit':status['actual_math_commit'],'reader_commit':status['reader_commit'],'checkpoint_HEAD':status['checkpoint_HEAD'],'checkpoint_not_final_heldHEAD':True,'full21PL_inline_base':rec(B/'prospective-V-base.original21-inline.json'),'status_artifact':rec(B/'PREPARATION-STATUS.json'),'report':rec(B/'PREPARATION-REPORT.md'),'originals_manifest':rec(B/'originals-manifest.json'),'normal_API_calls':0,'once_sentinel_created':False,'C_or_ledger_writes':False,'proof_native_browser_or_gate_runs':0,'needed_inputs':['Exact independent nativeproof/currentreader original custody','ROOT final heldHEAD aftercarrier','Four actual finalmetadata gates eachzero underthatheldHEAD','ROOT release to resumeverification; freshindependentfullguards thenrequired'],'stop_without_waiting_process':True,'self_hash_external':True})
rows=[]
for p in sorted(public()):
 x=rec(p);rows.append({'source_path':x['path'],'destination_path':DEST+'/'+str(p.relative_to(B)),'bytes':x['bytes'],'sha256':x['sha256'],'copy_rule':'Preparation original only; noV authority, no privateforeign guard export.'})
wr('portable-preparation-manifest.json',{'records':rows,'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'private_full_guard_excluded':True,'self_hash_external':True,'late_freeze_command_envelope':'Externally indexed; copy separately ifneeded','status':'HOLD_NOT_API_READY'})
for n in ['PREPARATION-STATUS.json','PREPARATION-FROZEN.json','PREPARATION-REPORT.md','portable-preparation-manifest.json']:print(json.dumps(rec(B/n)))
