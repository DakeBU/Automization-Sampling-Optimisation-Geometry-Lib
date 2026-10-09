from pathlib import Path
import hashlib,json,os,sys
ROOT=Path('E:/Samplinglib');BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73';OWN=BASE/'independent-source73';OUT=OWN/'reader-metadata-overlay73'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'LF_recipe':'CRLF byte pairs -> LF only'}
def write(n,x):
 p=OUT/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
assert not(OWN/'lease.final.json').exists()
adopt_path=BASE/'root.reader-metadata-overlay73.adoption.json';adopt=load(adopt_path)
decision_path=BASE/'independent-reader-metadata-repair73/decision.json';decision=load(decision_path)
lease_path=BASE/'independent-reader-metadata-repair73/lease.final.json'
assert sha(lease_path.read_bytes())=='e4328779062b83d430eee59aefa82eeb3f49cae0e6518f2fd0089f27b2ac13f8'
assert decision['verdict']=='ACCEPT_EXACT_METADATA_ONLY_PROPOSAL'
assert decision['reviewer']=='/root/header_math72' and decision['proposer']=='/root/independent_primary69'
assert decision['distinct_from_proposer_and_source_reviewer'] and decision['exact_changed_fields']==decision['exact_changed_files']==2
assert decision['proposal']['RAW_sha256']==sha((OUT/'proposal.json').read_bytes())=='252a9ce488ada4e979db0c845466046cc1a8c22eada30a10b212ccabcd117a6e'
assert decision['native_binding_payload_equal'] and decision['native_review_context_equal'] and decision['native_semantic_reviewer_packet_exact']
assert adopt['status']=='APPLIED_DISTINCT_REVIEWED_EXACT_TWO_METADATA_FIELDS_ONLY' and adopt['actual_root_PID']==23988
assert adopt['native_whole_logical_run_sha256']=='6344a0270c950b855a34e5915e4906cf65015dec05e9dd9f32903d4fb915edba'
assert decision['approved_rows']==adopt['approved_rows']
proposal=load(OUT/'proposal.json')
for r in adopt['exact_current']:
 b=(ROOT/r['path']).read_bytes();assert sha(b)==r['RAW_sha256'] and len(b)==r['RAW_bytes']
 c=next(c for c in proposal['changes'] if c['canonical_path']==r['path']);assert sha(b)==c['proposed']['RAW_sha256']
for i,p in enumerate([decision_path,adopt_path]):
 (OUT/f'authority{i}.exactraw.snapshot.json').write_bytes(p.read_bytes())
 (OUT/f'authority{i}.LF.snapshot.json').write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
write('final-authority.json',{'schema':'source73-distinct-reader-metadata-repair-authority/v1','independent_repair_accepted':True,'root_actual_application_completed':True,'proposal_author_is_not_repair_approver':True,'proposal_author':'/root/independent_primary69','repair_reviewer':'/root/header_math72','repair_review_actual_PID':decision['actual_check_PID'],'root_apply_actual_PID':23988,'root_apply_EXIT':0,'root_apply_EXIT_authority':'Explicit root actual terminal receipt report and adoption; not rerun by source reviewer','authority_input_pins':[pin(decision_path),pin(lease_path),pin(adopt_path)],'native_repair_scope':'CLOSED17','native_repair_whole_logical_hash_reported_by_root':adopt['native_whole_logical_run_sha256'],'native_repair_lease_hash_independently_checked_opaque':True,'native_repair_whole_run_or_other_math_verdict_loaded':False,'narrow_decision_incidental_context':'Narrow metadata decision contains opaque prior-math lease/compile locator; no mathematical verdict/body or other reviewer payload read or used.','source_packet_sha256':adopt['source_packet_sha256'],'publication_binding_sha256':adopt['publication_binding_sha256'],'publication_context_sha256':adopt['publication_context_sha256'],'mathematical_repair_or_new_source_credit':False,'self_approval':False,'actual_recording_PID':os.getpid()})
write('authority.terminal.json',{'actual_pid':os.getpid(),'exit_code':0,'argv':sys.argv,'background':False})
print(json.dumps({'actual_pid':os.getpid(),'exit_code':0,'authority':pin(OUT/'final-authority.json'),'narrow_repair_decision':pin(decision_path),'root_adoption':pin(adopt_path)},indent=2))
