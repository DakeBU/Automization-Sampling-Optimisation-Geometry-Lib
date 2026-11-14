"""Bounded final metadata/normalpark readback. No APIs, builds, browser or shared writes."""
from pathlib import Path
import ast, datetime, gzip, hashlib, json, subprocess
R=Path('/Users/zhouhuanjian/ASTIS-GC')
S=R/'.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
O=S/'final-metadata-readback-v1'
B=R/'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-integration-20261109'
NP=R/'.astis/semantic-neutral-20261109/src_9a6d2f/normalpark-preparation'
C='ab8b47caed9f781191f8408154cd355c7e7c104c';VCOMMIT='62813df927fd3c156dd57099cc11613074d91bc0';CORE='b3581af0fc7e517e6cf5b883f4af064ddaa72aa2'
ADV='ASTIS-SA-20261109-GaussianComplexityFixedSpectrumGeometry';OWNER='huanjian_gc_20261109_fixed_spectrum_geometry';ACTOR='/root/source_reader_9a6d2f'
CP='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-geometry.json';LP='runs/substantive_advances.jsonl'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
canon=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
git=lambda *a:subprocess.check_output(['git',*a],cwd=R)
def readref(ref):
 p=(R/ref['path']).resolve();assert p.is_relative_to(R);b=p.read_bytes();assert sha(b)==ref['sha256'];return b
assert not (O/'review-ACCEPT.json').exists()
projection_raw=(B/'final-local-metadata-projection.json').read_bytes();assert sha(projection_raw)=='3e7c0b5d43c60d7c532d8f1161434073d7e3779dc99b5652fbfd49cac8129721'
projection=json.loads(projection_raw);assert projection['core']==CORE
old=git('show',CORE+':'+CP);new=readref(projection['frontier_after'])
assert sha(old)==projection['frontier_before_sha256']=='e38dc3ca9af01e35d980b7f031955fbd3a3b71d1a824cc5bfa69641a4fc20fa7'
edits=projection['lossless_edits'];assert len(edits)==9
scalars=[x for x in edits if x['old_raw']];insertions=[x for x in edits if not x['old_raw']]
assert len(scalars)==8 and all(isinstance(json.loads(x['old_raw']),str) and isinstance(json.loads(x['new_raw']),str) for x in scalars)
assert len(insertions)==1 and insertions[0]['path']==['evidence','post_integration_acceptance']
before_text=old.decode();after_text=new.decode();forward=before_text
for e in sorted(edits,key=lambda x:x['before_start'],reverse=True):
 assert before_text[e['before_start']:e['before_end']]==e['old_raw']
 forward=forward[:e['before_start']]+e['new_raw']+forward[e['before_end']:]
assert forward.encode()==new
inverse=after_text
for e in sorted(edits,key=lambda x:x['after_start'],reverse=True):
 assert after_text[e['after_start']:e['after_end']]==e['new_raw']
 inverse=inverse[:e['after_start']]+e['old_raw']+inverse[e['after_end']:]
assert inverse.encode()==old
old_obj=json.loads(old);new_obj=json.loads(new)
def difference(x,y,path=''):
 if isinstance(x,dict) and isinstance(y,dict):
  out=[]
  for k in sorted(x.keys()|y.keys()):
   q=path+'/'+k.replace('~','~0').replace('/','~1');out+=difference(x[k],y[k],q) if k in x and k in y else [q]
  return out
 return [] if x==y else [path]
paths=difference(old_obj,new_obj)
expected=sorted('/'+'/'.join(x['path']) for x in edits);assert paths==expected
for k in ['target_statement','source_anchor','parents','source_proof_coverage','shared_floor_audit','conceptual_mirror_audit','purification']:
 assert old_obj[k]==new_obj[k],k
assert {k:v for k,v in old_obj['statement_seal'].items() if k!='status'}=={k:v for k,v in new_obj['statement_seal'].items() if k!='status'}
readme_path=R/projection['README_after']['path'];readme_new=readref(projection['README_after']);readme_old=git('show',CORE+':'+projection['README_after']['path'])
assert sha(readme_old)==projection['README_before_sha256'] and readme_new.endswith(readme_old)
readme_prefix=readme_new[:-len(readme_old)]
for phrase in ['not a fresh build','or a remote release','Both complete main lower bounds','remote original-owner release/publication','purification/Exposition Seal remain open']:
 assert phrase in readme_prefix.decode(),phrase
copies=projection['actual_original_evidence_copies'];assert len(copies)==64
for row in copies:
 a=readref(row['original']);b=readref(row['public']);assert a==b
exec_raw=(NP/'execution/execution-manifest.json').read_bytes();assert sha(exec_raw)=='7dc16b48f54002a7eb9c5af97d2f8f304445da63e5258833c564f5b959975bae'
execution=json.loads(exec_raw);api_raw=readref(execution['API_receipt']);api=json.loads(api_raw)
assert execution['actor']==api['actor']==ACTOR and execution['normal_API_calls']==api['normal_API_calls_actual']==1
assert api['returned_success'] is True and api['error'] is None and execution['source_fidelity_reissued'] is False
park=(NP/'execution/actual-normalpark-append.raw.jsonl').read_bytes();assert sha(park)==execution['exact_append_sha256']=='42ffbad99ab4e638c314d83d7c2978d3f197fe00c8f2a975381ed02cd45e395e'
assert park.endswith(b'\n') and len(park.splitlines())==1
event=json.loads(park);assert (event['from_state'],event['to_state'])==('STABILIZING','VERIFIED')
assert event['worker_id']==event['evidence']['verifier_id']==ACTOR and event['advance_id']==ADV
Vraw=(NP/'original-actual-V-event.raw.json').read_bytes();assert sha(Vraw)=='7cd55a70605e1db1c8198f5f7a2eec6dbcb62b562becf539a80a9e5c632a501c'
V=json.loads(Vraw);original=V['evidence'];assert len(original)==7
assert all(event['evidence'][k]==v for k,v in original.items())
assert set(event['evidence'])-set(original)=={'post_integration_normalpark'}
assert sha(canon(original))==execution['original_evidence_canonical_sha256']=='cfe818c3ae87e609929aec9c616682a03947d626c4578d83cfed39d5b4a4dc83'
assert event['evidence']['verified_commit']==C and execution['immutable_integration_core']==CORE
precore=git('show',CORE+':'+LP);ledger=(R/LP).read_bytes();assert ledger==precore+park
assert ledger.count(park)==1 and ledger.count(Vraw)==1
assert sha(ledger)==projection['ledger_after_original_actor_one_normalpark']==execution['after_ledger_sha256']=='820b899aae7ed60f17711496f6a4ac556346f48dbb46eff8feefe0f20903d2b2'
assert sha(precore)==execution['before_ledger_sha256']==api['before_ledger_sha256'] and sha(ledger)==api['after_ledger_sha256']
tree=ast.parse((R/'tools/astis_advance.py').read_text());nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'_replay_advances','_replay_discoveries'}]
ns={'Iterable':list,'Any':object,'NO_PROGRESS_FREEZE_AT':3};exec(compile(ast.Module(body=nodes,type_ignores=[]),'<pure-official-replays-only>','exec'),ns)
states=ns['_replay_advances']([json.loads(x) for x in ledger.splitlines()]);before_states=ns['_replay_advances']([json.loads(x) for x in precore.splitlines()])
assert states[ADV]['state']=='VERIFIED' and states[ADV]['owner_id']==OWNER
assert not any(x['state']=='STABILIZING' for x in states.values())
assert {k:v for k,v in states.items() if k!=ADV}=={k:v for k,v in before_states.items() if k!=ADV}
for p,digest in projection['protected_raw_hashes'].items():assert sha((R/p).read_bytes())==digest,p
checkpoint_raw=(B/'resume-checkpoint.json').read_bytes();checkpoint=json.loads(checkpoint_raw)
post=new_obj['evidence']['post_integration_acceptance']
assert post['accepted_immutable_core']==checkpoint['accepted_immutable_core']==CORE
assert post['source_checked_commit']==checkpoint['source_checked_commit']==C
assert post['source_V_first_carrying_commit']==checkpoint['source_V_first_carrying_commit']==VCOMMIT
assert checkpoint['STAB']==[] and checkpoint['current_ledger_sha256']==sha(ledger)
assert checkpoint['state']==post['state']=='LOCAL_ACCEPTED_EXISTING_V_RELEASED_REMOTE_PURIFICATION_OPEN'
for key in ['local_acceptance','normalpark_execution','eight_same_core_checks','actual44_originals_report','independent_all44_pixel_review','root_actual8_original_review']:
 assert checkpoint[key]==post[key];readref(post[key])
pixel=json.loads(readref(post['independent_all44_pixel_review']));assert pixel['verdict']=='ACCEPT'
assert post['accepted_reader_limits']==checkpoint['accepted_reader_limits']==pixel['scope_limits_and_nonblocking_observations']
for key in ['new_source_verdict','remote_owner_release_confirmed','remote_published','purification_or_Exposition_Seal_complete','Goal_complete']:
 assert post[key] is False and checkpoint[key] is False
history_raw=readref(post['eight_same_core_checks']);history=json.loads(history_raw)
assert sha(history_raw)=='e309ab8d132972ea0a2672ab4659f9060aaa3a68a8f905b3e04706484b9f90e8'
assert history['independent44pixel_acceptance']=='pending separate report; script PASS not pixels' and history['local_acceptance_or_normalpark_or_new_source_verdict'] is False
canonical=history['actual_eight_same_core_checks']['canonical_lean'];lean_receipt=json.loads(readref(canonical['original_receipt']))
lean_log=Path(lean_receipt['log']).read_bytes();assert sha(lean_log)==canonical['raw_log_sha256'] and b'Build completed successfully (9660 jobs).' in lean_log
assert projection['source_digest_unchanged']==checkpoint['source_digest']=='6905b946089555464e4eedadfad3644fb4df3ee5d49ffc8445c16bb7fd997108'
assert not git('diff',CORE,'--name-only','--','AutoSamplingTheory.lean','AutoSamplingTheory','Tests.lean','Tests','lakefile.lean','lean-toolchain','lake-manifest.json').strip()
for phrase in ['strict angle/cosine/Hessian-criterion route','parent standalone source-audit debt','both full main lower bounds','remote original-owner release/delivery','purification/Exposition Seal remain open','not a fresh build']:
 assert phrase in checkpoint['truth_boundary'],phrase
observed_head=git('rev-parse','HEAD').decode().strip()
record={'reviewer':'/root/geometry_integration_reader','verdict':'ACCEPT','scope':'Bounded independent mechanical final metadata/actual-original-actor normalpark readback only; no new source verdict or repeated math/build/site/pixel acceptance.',
 'final_projection_sha256':sha(projection_raw),'resume_checkpoint_sha256':sha(checkpoint_raw),'metadata_observed_HEAD':observed_head,
 'mathematical_candidate':C,'original_V_first_carrying_commit':VCOMMIT,'actual_accepted_build_browser_core':CORE,
 'checks':{'lossless_scalar_replacements':8,'new_evidence_objects':1,'offset_units':'Unicode characters; final inverse compared as exact UTF-8 raw bytes',
 'forward_reconstructs_current_cell':True,'inverse_restores_exact_e38_cell':True,'all_other_old_cell_raw_bytes_preserved':True,
 'old_target_definition_seal_signature_parents_sourcecoverage_preserved':True,'changed_JSON_paths':paths,
 'README_old_raw_bytes_exact_suffix':True,'actual_private_public_copies_compared':64,
 'original_actor_normal_API_calls':1,'normalpark_append_sha256':sha(park),'all7_original_V_fields_exact':True,
 'only_added_event_evidence_key':'post_integration_normalpark','proofowner_preserved':OWNER,'current_normal_state':'VERIFIED','STAB':[],
 'ledger_core_raw_prefix_plus_one_normalpark_exact':True,'ledger_after_sha256':sha(ledger),
 'foreign_state_replay_preserved':len(states)-1,'protected_source_audit_lesson_Test_model_discovery_hashes_checked':len(projection['protected_raw_hashes']),
 'source_tree_diff_against_actual_core':[], 'existing9660job_Lean_log_checked_not_rerun':True},
 'evidence_boundaries':{'actual8gates_44originals_root8_localacceptance':'Existing actual accepted evidence retained as separate layers; no reruns/reinspection.',
 'historical_pending_at_creation_manifest':'Exact e309 bytes remain pending-at-creation history; new actual acceptance does not overwrite it.',
 'reader_scope_limits_preserved_verbatim':post['accepted_reader_limits'],'remote_owner_release':False,'remote_published':False,'purification_Exposition_Seal_complete':False,'both_main_bounds_or_Goal_complete':False,
 'metadata_packaging_is_fresh_build_or_new_source_verdict':False},
 'reviewer_API_build_browser_OS_shared_or_commit_writes':False,'blocking_defects':[],
 'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O/'review-ACCEPT.json').write_bytes(dump(record))
(O/'copies64-verified-manifest.json').write_bytes(dump({'copies':copies,'count':64,'all_raw_equal_and_hashes_valid':True}))
for name,raw in [('final-projection.raw.json.gz',projection_raw),('resume-checkpoint.raw.json.gz',checkpoint_raw),('normalpark-execution.raw.json.gz',exec_raw),('normalpark-API-receipt.raw.json.gz',api_raw),('actual-normalpark-append.raw.jsonl.gz',park),('old-e38-cell.raw.json.gz',old),('current-cell.raw.json.gz',new),('README-new-prefix.raw.md.gz',readme_prefix)]:
 (O/name).write_bytes(gzip.compress(raw,mtime=0))
manifest={'review_sha256':sha((O/'review-ACCEPT.json').read_bytes()),'files':[{'path':str(p.relative_to(R)),'sha256':sha(p.read_bytes())} for p in sorted(O.iterdir()) if p.is_file()], 'new_source_verdict_or_API':False}
(O/'freeze.json').write_bytes(dump(manifest))
assert (R/CP).read_bytes()==new and (R/LP).read_bytes()==ledger and readme_path.read_bytes()==readme_new
print(json.dumps({'review_sha256':manifest['review_sha256'],'freeze_sha256':sha((O/'freeze.json').read_bytes()),'copies64_manifest_sha256':sha((O/'copies64-verified-manifest.json').read_bytes()),'verdict':'ACCEPT','API_calls':0},indent=2))
