from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,stat,traceback
sys.dont_write_bytecode=True
import normal_sourcev as n
OUT=Path(__file__).resolve().parent
PRIVATE=OUT.parent/'PRIVATE-normal-sourceV-baseline'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def freeze(directory):
 rows=[]
 for p in sorted(directory.rglob('*')):
  if p.is_file() and p.name not in {'manifest.json','freeze.receipt.json'}:
   rows.append({'path':str(p.relative_to(directory)),'bytes':p.stat().st_size,'sha256':sha(p),'frozen_mode':'0444'})
 manifest={'schema':1,'actor':n.ACTOR,'scope':'PRIVATE never-export baseline' if directory==PRIVATE else 'Complete portable normal-sourceV raw execution evidence','payload_files':rows,'payload_count':len(rows),'listing_unfiltered':True,'self_reference_policy':'Only this manifest.json and freeze.receipt.json excluded; receipt binds manifest; both frozen0444'}
 mp=directory/'manifest.json';dump(mp,manifest)
 return rows,mp
try:
 baseline=n.readj(PRIVATE/'baseline.json')
 g=n.guard(baseline,True)
 before=(PRIVATE/'ledger.before.raw.jsonl').read_bytes();after=n.LEDGER.read_bytes()
 assert after==(PRIVATE/'ledger.after-api.raw.jsonl').read_bytes()
 assert after.startswith(before) and after[len(before):]==(OUT/'actual-new-event.raw.jsonl').read_bytes()
 _,s0=n.ledger_state(before);_,s1=n.ledger_state(after)
 assert all(n.replay_guard(s0,s1).values())
 assert s1[n.ADV]['state']=='VERIFIED' and s1[n.ADV]['owner_id']==n.OWNER and s1[n.ADV]['last_actor']==n.ACTOR
 assert n.C.read_bytes()==(OUT/'own-C.after.raw.json').read_bytes()
 assert s1[n.ADV]['latest_evidence']==n.readj(OUT/'verification_evidence.json')
 assert stat.S_IMODE(n.MARKER.stat().st_mode)==0o444
 prior={
  'phase1':('ef13349dd0f6b894a6ba171184c65f19edb89b1e42e394ef7d0bd6d550320653','d8e1def94411192058922b64b4b7cb61e1c26ceb3ade1816b69fce2ecd9788ce'),
  'phase2':('fe71e48e45deac24afca70fdc1050e65ab80639093d26e547bac7cd17dd61ceb','0ca53710dee6acfe75295f075b7465fc5483b2fa57e6968ed0f59657458ab6a6'),
  'phase3':('68c4da2106048fab40a0cbff4c78f42a4011508d3b1e881de59a0753e84e6070','ccf7b16ec6988d0cbfcb2b80ecad72758de126a52df81708d83c44425c2f9529')}
 for name,(receipt,mh) in prior.items():
  d=OUT.parent/name;assert sha(d/'receipt.json')==receipt and sha(d/'manifest.json')==mh
  for r in n.readj(d/'manifest.json')['payload_files']:
   p=d/r['path'];assert sha(p)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
 dump(OUT/'final-freeze-guard.json',{'checked_at':datetime.now(timezone.utc).isoformat(),'state':'PASS','foreign_guards':g,'all_foreign_state_latest_evidence_deep_exact':True,'ledger_full_prefix_and_one_exact_own_new_event':True,'own_C_after_exact':True,'original_V_latest_evidence_entire_deep_exact':True,'phase1_phase2_phase3_all_payload_bytes_modes_and_receipts_exact':True,'permanent_once_marker':True,'API_invocations':1,'reader_HOLD_preserved':True,'nested_repo_limited_guard':'Same explicit metadata-only .atlas-upstream exception; no body read/hash/glob','no_private_baseline_export':True})
 private_rows,pm=freeze(PRIVATE)
 private_receipt={'schema':1,'actor':n.ACTOR,'never_export':True,'frozen_at':datetime.now(timezone.utc).isoformat(),'manifest_sha256':sha(pm),'payload_files':len(private_rows),'files_mode':'0444','directories_mode':'0555','API_call_count':1,'no_extra_mutation':'Only own target ledger event and two own C fields changed'}
 pr=PRIVATE/'freeze.receipt.json';dump(pr,private_receipt)
 rows,mp=freeze(OUT)
 receipt={'schema':1,'actor':n.ACTOR,'advance_id':n.ADV,'frozen_at':datetime.now(timezone.utc).isoformat(),'metadata_verified_commit':n.HEAD,'native_math_commit':n.NATIVE,'actual_transition':'PROVED_LOCAL->VERIFIED','actual_event_created_at':s1[n.ADV]['updated_at'],'actual_event_sha256':sha(OUT/'actual-new-event.raw.jsonl'),'verification_evidence_sha256':sha(OUT/'verification_evidence.json'),'manifest_sha256':sha(mp),'payload_file_count':len(rows),'files_mode':'0444','directories_mode':'0555','permanent_once_marker_sha256':sha(n.MARKER),'private_manifest_sha256':sha(pm),'private_freeze_receipt_sha256':sha(pr),'private_payload_count':len(private_rows),'private_directory_exported':False,'all_foreign_states_latest_evidence_history_raw_bytes_files_frontiers_control_guards':'PASS with explicitly limited nested-repo metadata exception','own_C_changed_paths_only':['status','evidence.integration_boundary'],'reader':'QUALIFIED/HOLD unchanged','global_STAB_site_source_index_graph_browser_desktop_mobile_purification_Goal':'OPEN','actual_API_invocations':1,'root_API_invocations_for_target':0,'proof_owner':n.OWNER,'no_retry_or_replay':True,'original_source_phases_byte_mode_exact':True,'all_original_V_topkeys_nested_values_preserved':True,'future_evidence_rule':'Only original verifier may append post_integration; never shrink original V evidence to whitelist'}
 rp=OUT/'freeze.receipt.json';dump(rp,receipt)
 for directory,fs in [(PRIVATE,private_rows),(OUT,rows)]:
  for p in directory.rglob('*'):
   if p.is_file():p.chmod(0o444)
  for p in sorted([p for p in directory.rglob('*') if p.is_dir()],key=lambda p:len(p.parts),reverse=True):p.chmod(0o555)
  directory.chmod(0o555)
  for r in fs:
   p=directory/r['path'];assert sha(p)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
  for p in [directory/'manifest.json',directory/'freeze.receipt.json']:assert stat.S_IMODE(p.stat().st_mode)==0o444
 print(json.dumps({'portable_directory':str(OUT),'actual_event_sha256':receipt['actual_event_sha256'],'evidence_sha256':receipt['verification_evidence_sha256'],'manifest_sha256':sha(mp),'freeze_receipt_sha256':sha(rp),'portable_payload_files':len(rows),'private_never_export':True,'all_hashes_modes_foreign_guards_prior_phases_verified':True,'actual_API_invocations':1,'reader_HOLD':'PRESERVED'},indent=2))
except BaseException:
 p=OUT/'freeze.failure.raw.txt'
 if not p.exists():p.write_text(traceback.format_exc())
 raise
