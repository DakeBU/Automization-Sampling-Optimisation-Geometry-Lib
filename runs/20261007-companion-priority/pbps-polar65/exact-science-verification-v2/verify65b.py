import importlib.util,json,os,pathlib,sys,traceback
O=pathlib.Path(__file__).resolve().parent;D=O.parent;OLD=D/'exact-science-verification'
spec=importlib.util.spec_from_file_location('closed65_common',OLD/'verify65.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
c.O=O;c.COMMIT='ecd9d1f10ad0241312492cefacd5fe48c317e9c2';c.PARENT='dad6e38c9beed3476cb5d1db06eb57b955c8e3eb'
R=c.R;COMMIT=c.COMMIT;PARENT=c.PARENT;ACTOR=c.ACTOR;SAU=c.SAU;PY=c.PY;FILES=c.FILES;DECLS=c.DECLS
read=c.read;write=c.write;pin=c.pin;sha=c.sha;canon=c.canon;git=c.git;now=c.now;match=c.match;logical=c.logical;checkpins=c.checkpins
def freeze():
 c.exact()
 if not (O/'lease.open.json').exists():write('lease.open.json',{'status':'OPEN','actor':ACTOR,'actual_pid':os.getpid(),'checked_commit':COMMIT,'parent':PARENT,'owned_prefix':O.as_posix(),'opened_utc':now(),'authorized_shared_writes':'one non-owner VERIFIED event and r65/verified.json if required gates pass'})
 else:
  assert read(O/'lease.open.json')['status']=='OPEN' and not (O/'inputs.manifest.json').exists();write('freeze.retry.json',{'actual_pid':os.getpid(),'reason':'First freeze correctly rejected Git LF versus worktree CRLF for fixed toolchain. Retain failed observer and explicitly qualify only toolchain/manifest LF bytes; all science/publication RAW checks remain exact.','retained':'negative-freeze-RAW-LF/'})
 rows=[];seen=set()
 def add(p,e=None,role='scoped-current'):
  p=pathlib.Path(p)
  if e:match(p,e)
  if p.as_posix() not in seen:rows.append({**pin(p),'role':role});seen.add(p.as_posix())
 oldlease=read(OLD/'lease.final.json');assert oldlease['status']=='CLOSED_LAST' and oldlease['final_owned_file_count']==61
 for x in oldlease['all_owned_except_this_final_lease']:add(x['path'],x,'CLOSED61-native-output-no-copy')
 add(OLD/'lease.final.json');assert logical(OLD/'run.json')==oldlease['whole_logical_run_sha256'];assert pin(OLD/'named-verification.payload.json')['raw_sha256']==oldlease['complete_named_RAW_verdict_sha256']
 relevant=FILES+['AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean','lean-toolchain','lake-manifest.json',c.PUB,c.LESSON,c.AUDIT,c.CELL]
 blobs=[]
 for f in relevant:
  add(R/f,role='exact-current-Git-input');b=git('show',COMMIT+':'+f);cur=(R/f).read_bytes();old=git('show',PARENT+':'+f)
  if f in ['lean-toolchain','lake-manifest.json']:assert b.replace(b'\r\n',b'\n')==cur.replace(b'\r\n',b'\n'),('current fixed toolchain/manifest LF qualification',f)
  else:assert b==cur,('current exact Git RAW',f)
  if f!=c.CELL:assert old==b,('unexpected mathematical/source/publication change',f)
  blobs.append({'path':f,'current_Git_blob_id':git('rev-parse',COMMIT+':'+f).decode().strip(),'current_Git_RAW_sha256':sha(b),'parent_Git_RAW_sha256':sha(old),'unchanged_from_reviewed_parent':old==b,'worktree_RAW_equal_Git_RAW':cur==b,'worktree_LF_equal_Git_LF':cur.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'),'qualification':'RAW exact' if cur==b else 'Fixed toolchain/manifest only: Git LF vs worktree CRLF, exact RAW and LF pins kept separately.'})
 names=git('diff','--name-only',PARENT,COMMIT).decode().splitlines();canonical=[x for x in names if not x.startswith('runs/')];assert canonical==[c.CELL],canonical
 before=json.loads(git('show',PARENT+':'+c.CELL));after=read(R/c.CELL);reconstructed=json.loads(json.dumps(before));changes=[]
 for outer,inner in [('shared_floor_audit','searched'),('reuse_plan','searched_existing')]:
  a=before[outer][inner][0];b=after[outer][inner][0];assert b=='Samplinglib: '+a;reconstructed[outer][inner][0]=b;changes.append({'field':outer+'.'+inner+'[0]','before':a,'after':b,'only_prefix_added':True})
 assert reconstructed==after
 for f in ['header0.lean','header1.lean','root.statement-seal65.json']:add(c.P/f,role='unchanged-initial-seal')
 for f in ['root.math65.adoption.json','root.source65.adoption.json','root.decoder65.adoption.json','source.0.review.root-adapter.json','proved-local.json','root.exact65-blocker.adoption.json','frontier-search-repair65/diagnosis.json','frontier-search-repair65/cell.before.exactraw.snapshot.json','frontier-search-repair65-v2/diagnosis.json','frontier-search-repair65-v2/cell.before.exactraw.snapshot.json']:
  add(D/f)
 for folder in ['frontier-repair-gate65','frontier-repair-gate65-v2']:
  for f in ['receipt.json','stdout.log','stderr.log']:add(D/folder/f,role='retained-root-negative-or-corrected-terminal')
 for f in ['tools/astis_advance.py','tools/astis_publication.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py','tools/astis_contributor_contract.py','tools/astis.py','tools/astis_harness.py']:add(R/f,role='actual-required-gate-code')
 previous=read(OLD/'bindings.result.json');assert previous['status']=='PASS'
 for k in ['native_source_complete_RAW_review','native_source_complete_RAW_decision','native_source_complete_RAW_input','native_source_lease','native_decoder_complete_named_RAW','native_decoder_lease']:add(previous[k]['path'],previous[k],'immutable-previously-validated-native-closure-binding')
 for f in ['independent-math65/lease.final.json','independent-math65/run.json','independent-math65/mathematical-review.named.raw.json','independent-source65/owned-manifest.json','anonymous-decoder/final_run.json','anonymous-decoder/closure_manifest.json','anonymous-decoder/decoded0.root-adapter.json']:
  add(D/f,role='bounded-unchanged-native-capsule')
 write('inputs.manifest.json',{'checked_commit':COMMIT,'parent':PARENT,'actual_freezer_pid':os.getpid(),'inputs':rows,'input_count':len(rows),'exact_current_Git_blobs':blobs,'canonical_changed_files':canonical,'canonical_exact_two_string_changes':changes,'all_other_commit_files_are_retained_runs_evidence':True,'retained_native61_whole_logical_run':oldlease['whole_logical_run_sha256'],'retained_native61_explicit_complete_named_RAW':oldlease['complete_named_RAW_verdict_sha256'],'no_broad_history_or_source_inventory_reaudit':True,'finite_previous_historical_maps':'Inherited immutable CLOSED61 inputs manifest with27 explicit finite resolutions; no new historical fallback. Current cell reviewed by exact parent/current Git blobs plus two explicit root repair snapshots.'})
 print(json.dumps({'status':'FROZEN','actual_pid':os.getpid(),'checked_commit':COMMIT,'inputs':len(rows),'canonical_delta_fields':2,'CLOSED61_unchanged':True}),flush=True)
def reuse():
 checkpins();oldlease=read(OLD/'lease.final.json')
 for x in oldlease['all_owned_except_this_final_lease']:match(x['path'],x)
 assert logical(OLD/'run.json')=='46cd394fd1736933f7b76fb6bf8edf433883d68d996f6c47bb32470a1f9aa276';assert pin(OLD/'named-verification.payload.json')['raw_sha256']=='d4cd38ea2a2ed16f15f1ab82c0e55752fb6429843d42f6adb01cf6dd9281b1e4'
 b=read(OLD/'bindings.result.json');assert b['status']=='PASS' and b['all280_primary_math_items_RAW_spans_valid'] and len(b['literal_BODY_steps'])==5
 for x in read(O/'inputs.manifest.json')['exact_current_Git_blobs']:
  if x['path']!=c.CELL:assert x['unchanged_from_reviewed_parent']
 sys.path.insert(0,str(R/'tools'));import astis_publication as pub
 data=pub.inputs();item=next(x for x in pub.load() if any(y['declaration']==c.DECL for y in x['bindings']));binding=next(x for x in item['bindings'] if x['declaration']==c.DECL);digest=pub.binding_digest(item,binding,data);ctx=pub.digest(pub.review_context(item,binding,data));assert digest==b['current_publication_binding_sha256'] and ctx==b['current_review_context_sha256']
 for i,f in enumerate(FILES):
  raw=(R/f).read_bytes();assert raw==git('show',PARENT+':'+f)==git('show',COMMIT+':'+f);assert raw==((D/'independent-math65')/f'candidate{i}.exactraw.snapshot').read_bytes();header=raw[raw.index(b'theorem '):raw.index(b':= by')].rstrip(b'\r\n ');assert header==(c.P/f'header{i}.lean').read_bytes().rstrip(b'\r\n ')
 corrected=read(R/c.CELL);search=corrected['shared_floor_audit']['searched'][0];assert 'Samplinglib: '==search[:13] and 'mathlib' in search.lower();assert corrected['reuse_plan']['searched_existing'][0]==search
 rule=(R/'tools/astis_frontier_cells.py').read_text(encoding='utf-8');assert 'searched = audit.get("searched")' in rule and 'audit = cell.get("shared_floor_audit")' in rule
 write('reuse.result.json',{'status':'PASS','checked_commit':COMMIT,'parent':PARENT,'actual_checker_pid':os.getpid(),'closed61_immutable_manifest_all61_valid':True,'prior_mathematics_source_and_literal_span_checks_reused_by_exact_Git_RAW_equality':pin(OLD/'bindings.result.json'),'source_files':117,'math_files':40,'decoder_files':20,'literal_BODY_steps_reused':5,'primary_items_reused':280,'new_math_or_source_repair':False,'unchanged_publication_binding_sha256':digest,'unchanged_publication_context_sha256':ctx,'metadata_two_prefixes_only':True,'previous_diagnosis_correction':'The original CLOSED61 verdict named reuse_plan.searched_existing as the gate input. That was my field-attribution error. Validator lines156-163 reads shared_floor_audit.searched, then lines191-195 checks library labels. Both duplicate descriptions are now consistent. The original obstruction, root first wrong-field correction and EXIT1 remain retained unchanged; no mathematical conclusion changed.','honesty_of_recorded_search':'The existing entries already describe actual64 canonical local module-card/compiled-output reuse and pinned Mathlib APIs. The canonical parent and original closed mathematical review establish that actual Samplinglib reuse; prefixing its library name changes process attribution only.','canonical_delta':read(O/'inputs.manifest.json')['canonical_exact_two_string_changes'],'source_Lean_graph_distinction':True,'accepted_boundary':'B16 typed polar/isometry and typed B0* consumer only; ambient B* extraction/global centered decomposition/projector next. No onto/reverse-product/full-paper/Exposition/PURIFIED/aggregate/Goal credit.'})
 print(json.dumps({'status':'REUSE_AND_PROCESS_REPAIR_PASS','actual_pid':os.getpid(),'canonical_fields':2,'math_source_unchanged':True}),flush=True)
def focused():c.focused()
def direct():c.direct()
def gates():
 results=[]
 for name,args in [('publication',[PY,'-B','-X','utf8','tools/astis_publication.py','check','--base',PARENT]),('semantic',[PY,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check']),('frontier',[PY,'-B','-X','utf8','tools/astis_frontier_cells.py','check']),('contributor',[PY,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base',PARENT]),('focused-reviewed-fakeclosure',[PY,'-B','-X','utf8',str(O/'verify65b.py'),'direct'])]:
  r=c.command(name,args);results.append({'gate':name,'actual_pid':r['actual_foreground_pid'],'exit_code':r['exit_code'],'terminal_closed':r['terminal_closed'],'receipt':pin(O/name/'receipt.json')})
 write('gates.result.json',{'status':'PASS' if all(x['exit_code']==0 for x in results) else 'FAIL','checked_commit':COMMIT,'parent':PARENT,'fresh_focused_gates':results,'whole_astis_site_aggregate_gate_run':False});assert all(x['exit_code']==0 for x in results)
def runtransition():c.command('transition',[PY,'-B','-X','utf8',str(O/'verify65b.py'),'transition'])
def transition():
 checkpins()
 for f in ['focused.result.json','reuse.result.json','gates.result.json','focused-reviewed-fakeclosure.result.json']:assert read(O/f)['status']=='PASS'
 ledger=R/'runs/substantive_advances.jsonl';before=ledger.read_bytes();target=[json.loads(l) for l in before.splitlines() if SAU.encode() in l];latest=target[-1];assert latest['to_state']=='PROVED_LOCAL' and latest['worker_id']!=ACTOR;assert not (D/'verified.json').exists()
 write('ledger.before.pin.json',{'path':ledger.as_posix(),'raw_bytes':len(before),'raw_sha256':sha(before),'line_count':len(before.splitlines()),'target_records':len(target),'latest_target_state':'PROVED_LOCAL','proving_owner':latest['worker_id'],'whole_ledger_copy_retained':False})
 evidence={'verifier_id':ACTOR,'verified_commit':COMMIT,'gate':{'status':'PASS','focused_compiler':pin(O/'focused.result.json'),'fresh_required_admission_gates':pin(O/'gates.result.json'),'checked_scope':'Exact SCI65b, one fresh nonforced focused Test build, diff-aware publication/contributor at actual parent, fresh frontier/semantic/reviewed-publication/fakeclosure; aggregate/site deferred.'},'source_audit':{'status':'PASS','closed_math_source_decoder_and_literal_steps_reused_by_exact_Git_RAW':pin(O/'reuse.result.json'),'unchanged_prior_native_bindings':pin(OLD/'bindings.result.json'),'exact_only_two_process_string_fields':pin(O/'inputs.manifest.json'),'semantic_slots':7,'literal_BODY_steps':5,'primary_items':280,'no_mathematical_repair':True},'fake_closure_scan':{'status':'PASS','receipt':pin(O/'focused-reviewed-fakeclosure.result.json'),'forbidden_hits':[],'private_providers':0,'standard_axioms':['propext','Classical.choice','Quot.sound']},'publication_declarations':DECLS,'independent_actor_not_proving_owner':True,'remaining_boundary':'Typed B0* consumer only; ambient B* extraction/global-centered decomposition/projector next; no onto/reverse product. Aggregate/reader, B17/H1/full corrector/dynamics/main/errors/cost/actual-input composition/full Exposition/PURIFIED/paper/Goal remain pending.'}
 sys.path.insert(0,str(R));from tools.astis_advance import transition_advance
 transition_advance(SAU,'VERIFIED',worker_id=ACTOR,evidence=evidence)
 after=ledger.read_bytes();assert after.startswith(before);suffix=after[len(before):];items=[json.loads(x) for x in suffix.splitlines()];assert len(items)==1 and items[0]['advance_id']==SAU and items[0]['to_state']=='VERIFIED' and items[0]['worker_id']==ACTOR and items[0]['evidence']['verified_commit']==COMMIT
 (O/'ledger.append.exactraw.jsonl').write_bytes(suffix);write('ledger.after.pin.json',{'path':ledger.as_posix(),'raw_bytes':len(after),'raw_sha256':sha(after),'line_count':len(after.splitlines()),'original_prefix_RAW_unchanged':True,'prefix_raw_bytes':len(before),'prefix_raw_sha256':sha(after[:len(before)]),'one_exact_append':pin(O/'ledger.append.exactraw.jsonl'),'whole_ledger_copy_retained':False})
 result={'status':'PASS','checked_commit':COMMIT,'parent':PARENT,'advance_id':SAU,'actual_transition_pid':os.getpid(),'verifier_id':ACTOR,'proving_owner':latest['worker_id'],'from_state':'PROVED_LOCAL','to_state':'VERIFIED','exact_one_nonowner_append':True,'ledger_before':pin(O/'ledger.before.pin.json'),'ledger_after':pin(O/'ledger.after.pin.json'),'exact_appended_RAW':pin(O/'ledger.append.exactraw.jsonl'),'canonical_Git_Lean_changes':False};write('transition.result.json',result)
 verified={'status':'VERIFIED','advance_id':SAU,'verified_commit':COMMIT,'parent':PARENT,'verifier_id':ACTOR,'actual_transition_pid':os.getpid(),'independent_from_proving_owner':True,'focused':pin(O/'focused.result.json'),'required_gates':pin(O/'gates.result.json'),'source_math_reuse':pin(O/'reuse.result.json'),'proper_transition':pin(O/'transition.result.json'),'native_scope':O.relative_to(R).as_posix(),'remaining_boundary':evidence['remaining_boundary'],'aggregate_full_Exposition_PURIFIED_paper_Goal':False};(D/'verified.json').write_bytes((json.dumps(verified,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8'));write('verified.shared-write.pin.json',{'authorized_shared_verified_json':pin(D/'verified.json'),'only_other_shared_write':'one exact VERIFIED ledger append','root_canonical_Git_Lean_changes':False})
 print(json.dumps({'status':'INDEPENDENT_VERIFIED_APPENDED','actual_pid':os.getpid(),'verified_commit':COMMIT,'verifier_id':ACTOR,'append_RAW_sha256':sha(suffix),'original_prefix_unchanged':True}),flush=True)
if __name__=='__main__':
 mode=sys.argv[1]
 try:globals()[mode]()
 except Exception as e:write(mode+'.failure.json',{'status':'FAIL','actual_pid':os.getpid(),'checked_commit':COMMIT,'exception':repr(e),'traceback':traceback.format_exc(),'utc':now()});raise
