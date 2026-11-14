from pathlib import Path
import json,hashlib,subprocess,gzip,sys
sys.dont_write_bytecode=True;sys.path.insert(0,'tools')
import astis_advance as adv
import astis_publication as pub
W=Path(__file__).parent;E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-target-law-semantic-evidence');C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-target-law.json');L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumTargetLaw';OWNER='huanjian_gc_20261110_fixed_spectrum_target_law'
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
assert not (W/'PROVED_LOCAL-attempted.once.json').exists(),'Never replay a normal transition after an uncertain result.'
s=json.loads((W/'statement-seal-v1.json').read_bytes());k=json.loads((E/'actual-kernel-owned-inventory.json').read_bytes());p=Path(s['producer']['planned_file']);t=Path(s['actual_private_consumer']['planned_file']);name=s['producer']['name'];assert sha(p.read_bytes())==k['actual_producer_sha256'] and sha(t.read_bytes())==k['actual_Test_sha256'];assert k['all2_reachable'] and k['both_exact_sealed_types_kernel_applied']
checks=[]
for stem in ['20261110T105759250962Z-target-law-producer-final-native','20261110T110243951932Z-target-law-consumer-final-native','20261110T110453526687Z-target-law-kernel-exact-types-all-owned-actual-parents']:
 rp=Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json');x=json.loads(rp.read_bytes());assert x['exit_code']==0 and sha(Path(x['log']).read_bytes())==x['log_sha256'];checks.append({'receipt':str(rp),'receipt_sha256':sha(rp.read_bytes()),'actual_log_sha256':x['log_sha256'],'actual_HEAD':x['head_before'],'scope':'Actual current mathematical working bytes; no later-commit fresh native or global credit.'})
b=json.loads((W/'intake-tracked-private-preservation.json').read_bytes());base=json.loads((W/'preproof-baseline.private.json').read_bytes())
for f,h in b['all_tracked_hashes_except_own_ledger_and_frontier'].items():assert sha(Path(f).read_bytes())==h,f
for f,h in base['all_existing_frontier_hashes'].items():assert sha(Path(f).read_bytes())==h,f
before=L.read_bytes();states=adv._replay_advances([json.loads(z) for z in before.splitlines()]);assert states[ADV]['state']=='EXPLORING' and states[ADV]['owner_id']==OWNER;assert {a:x for a,x in states.items() if a!=ADV}==b['all_foreign_states']
pub.check_advance([name],reviewed=False)
record=json.loads((E/'publication-draft-record.json').read_bytes());boundary=json.loads(Path('website/content/declaration_lessons/huanjian-fixed-spectrum-target-law.json').read_bytes())['units'][0]['boundary'];ma={'status':'none-found','discovery_ids':[],'evidence':str(E/'postproof-conceptual-mirror-audit.json')}
parents=k['actual_first_public_ASTIS_parents']
evidence={'result_kind':'theorem-edge','theorem_delta':s['producer']['signature'],'lean_files':[str(p),str(t)],'lean_declarations':[name],'publication_declarations':[name],'focused_checks':checks,'truth_boundary':boundary,'conceptual_mirror_audit':ma,'actual_consumer':'Actual private target norm-square L1 and finite inverse-spectrum mean materially consume the new full Gaussian law and canonical existing diagonal Gaussian moment theorem; rotation measurability/norm invariance/integral transport are internal. No law/moment/positivity/regularity certificate input.','actual_ASTIS_parents':parents,'source_VERIFIED_or_global':False}
cellraw=C.read_bytes();(W/'PROVED_LOCAL-attempted.once.json').write_bytes(dump({'advance_id':ADV,'ledger_prefix_sha256':sha(before),'action':'Exactly one normal PROVED_LOCAL invocation; inspect actual ledger if interrupted, never replay.'}));adv.transition_advance(ADV,'PROVED_LOCAL',worker_id=OWNER,evidence=evidence);after=L.read_bytes();assert after.startswith(before);app=after[len(before):];assert len(app.splitlines())==1
new=adv._replay_advances([json.loads(z) for z in after.splitlines()]);assert new[ADV]['state']=='PROVED_LOCAL' and {a:x for a,x in new.items() if a!=ADV}==b['all_foreign_states']
for f,h in b['all_tracked_hashes_except_own_ledger_and_frontier'].items():assert sha(Path(f).read_bytes())==h,f
for f,h in base['all_existing_frontier_hashes'].items():assert sha(Path(f).read_bytes())==h,f
(E/'frontier-before-PROVED_LOCAL.raw.json.gz').write_bytes(gzip.compress(cellraw,mtime=0));(E/'actual-PROVED_LOCAL-append.exact.jsonl').write_bytes(app)
capsule={'state':'PROVED_LOCAL_NOT_SOURCE_VERIFIED','advance_id':ADV,'owner':OWNER,'normal_PROVED_LOCAL_API_calls':1,'append_sha256':sha(app),'foreign_states_preserved':len(b['all_foreign_states']),'foreign_frontiers_preserved':len(base['all_existing_frontier_hashes']),'protected_tracked_files_preserved':len(b['all_tracked_hashes_except_own_ledger_and_frontier']),'producer':{'file':str(p),'sha256':sha(p.read_bytes()),'declaration':name,'actual_ASTIS_parents':parents['producer']},'private_consumer':{'file':str(t),'sha256':sha(t.read_bytes()),'actual_ASTIS_parents':parents['private_consumer'],'source_Anchor':False,'Registry_node':False},'actual_checks':checks,'both_exact_sealed_types_kernel_applied':True,'actual_owned_declarations':2,'all_reachable':True,'recursive_axioms':'standard3 only','binding_sha256':record['publication_binding_sha256'],'source_to_lean_map':str(E/'source-to-lean-map-v1.json'),'conceptual_mirror_audit':ma,'truth_boundary':boundary,'independent_source_native_reader_V_global_purification_Goal_pending':True};(E/'local-proof-capsule.json').write_bytes(dump(capsule))

c=json.loads(cellraw)
c['status']='proved_locally'
c['reuse_plan']['known_consumers']=['Compiled private actual_target_gaussian_norm_mean genuinely consumes public law and canonical diagonal Gaussian moments.']
c['conceptual_mirror_audit']=ma
c['evidence'].update({'focused_checks':[z['receipt'] for z in checks],'local_proof_capsule':str(E/'local-proof-capsule.json'),'publication_binding_sha256':record['publication_binding_sha256'],'actual_compiled_ASTIS_parents':parents,'source_to_lean_map':str(E/'source-to-lean-map-v1.json'),'execution_boundary':boundary})
c['statement_seal']['status']='EXACT_UNCHANGED_SEALED_TYPES_COMPILED;ORIGINAL_TC_HOLD_AND_TWO_STRING_SOURCE_SUCCESSOR_RETAINED;FULL_POSTPROOF_REVIEW_PENDING'
c['learning_contract']['reader_backpressure']['assumptions_preserved']=True
c['learning_contract']['reader_backpressure']['boundary_preserved']=True
c['learning_contract']['failure_class']='IMPLEMENTATION_FAILED'
c['learning_contract']['salvage']={'required':True,'status':'completed','reason':'Explicit mean-space API diagnosis and metadata/archiving errors retained; unchanged sealed statements. Both handwritten declarations reachable; no duplicate helper or copied canonical proof. Original source HOLD and exact two-string source-author correction retained. No source/main mathematical refutation.','promoted_fragments':[],'discarded_fragments':[]}
C.write_bytes(dump(c))
print(json.dumps({'state':'PROVED_LOCAL','append_sha256':sha(app),'sourceV':False,'global':False,'protected_foreign_states':len(b['all_foreign_states']),'protected_tracked_files':len(b['all_tracked_hashes_except_own_ledger_and_frontier'])}))
