import datetime,hashlib,json,os,pathlib,re,shutil,subprocess,sys,traceback
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;D=O.parent;H=D.parent/'pbps-ambient-adjoint-preproof66';C='a115115d42b3fa2b67885d87fe4d5300af36fcd1';P='31ce36e7ca01b203696918672c33d29a337550c3';ACTOR='/root/exact_science63';SAU='ASTIS-SA-20261009-PBPSAmbientAdjointCorrector';PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';M='AutoSamplingTheory/ExampleCases/ProximalBPS/AmbientAdjointCorrector.lean';T='Tests/ProximalBPSAmbientAdjointCorrector.lean';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.AmbientAdjointCorrector.actual_ambient_adjoint_centered_decomposition';TESTDECL='Tests.ProximalBPSAmbientAdjointCorrector.genuine_actual_global_corrector_consumer';PUB='website/content/publications/pbps-ambient-adjoint-corrector.json';LESSON='website/content/declaration_lessons/pbps-ambient-adjoint-corrector.json';AUDIT='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSAmbientAdjointCorrector.json';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-ambient-adjoint-corrector.json';BIND='3d1d9d97cc4ae200fb0b07584cc5a89e6805851d05d0c640f3d3e4b3106bdc7f';CTX='d668766750b3e3471ea7b0d50fd3d562a81ec2044cdc8c210891f4671e6ca60b'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def write(f,j):
 assert not (O/'lease.final.json').exists();p=O/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(j,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':p.as_posix(),'raw_bytes':len(b),'lf_bytes':len(b.replace(b'\r\n',b'\n')),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n'))}
def check(x):
 q=pin(x['path']);assert q['raw_sha256']==x['raw_sha256'];assert q['raw_bytes']==x.get('raw_bytes',x.get('bytes',x.get('RAW_bytes')))
 if 'lf_sha256' in x:assert q['lf_sha256']==x['lf_sha256']
def blob(p,c=C):return subprocess.check_output(['git','show',c+':'+p],cwd=R)
def logical(p):
 r=read(p);h=r.pop('run_sha256');assert sha(canon(r))==h;return h
def current():
 assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==C;assert subprocess.check_output(['git','rev-parse',C+'^'],cwd=R).decode().strip()==P
def checkpins():
 j=read(O/'inputs.manifest.json');current()
 for x in j['external_immutable_pins']:check(x)
 for x in j['exact_Git_current_pins']:
  check(x['current']);b=blob(x['path']);assert sha(b)==x['Git_RAW_sha256'];assert sha(b.replace(b'\r\n',b'\n'))==x['current']['lf_sha256']
 return j
def freeze():
 current();write('lease.open.json',{'schema':'independent-exact-SCI66-OPEN-v1','status':'OPEN','actor':ACTOR,'checked_commit':C,'parent':P,'actual_open_pid':os.getpid(),'opened_utc':now(),'owned_prefix':O.as_posix(),'authorized_shared_writes':'Only one proper nonowner VERIFIED append and r66/verified.json if every required check passes','canonical_aggregate_site_Registry_Lean_edits':False})
 paths=[M,T,'AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean','AutoSamplingTheory/TechnicalLemmas/Measure/L2Expectation.lean','lean-toolchain','lake-manifest.json',PUB,LESSON,AUDIT,CELL]+['tools/'+s+'.py' for s in ['astis','astis_publication','astis_advance','astis_harness','astis_semantic_roundtrip','astis_frontier_cells','astis_contributor_contract']];gitrows=[]
 for p in paths:
  q=pin(R/p);b=blob(p);assert sha(b.replace(b'\r\n',b'\n'))==q['lf_sha256'];gitrows.append({'path':p,'Git_blob':subprocess.check_output(['git','rev-parse',C+':'+p],cwd=R).decode().strip(),'Git_RAW_sha256':sha(b),'current':q,'qualification':'Exact RAW' if sha(b)==q['raw_sha256'] else 'Explicit exact current RAW plus Git LF equality; no reserialization'})
 files=[D/f for f in ['proved-local.json','root.math66.adoption.json','root.source66.adoption.json','root.decoder66.adoption.json','source.1.review.root-adapter.json','source.1.reviewer-packet.json','math-freeze.json','math-freeze1.metadata-overlay.json','claim.json','audit.0.before-decoder.exactraw.snapshot.json','audit.1.before-source-admission.exactraw.snapshot.json','cell.1.before-proved.exactraw.snapshot.json','reuse-plan-metadata-repair66/repair.json','reuse-plan-metadata-repair66/cell.before.exactraw.snapshot.json','presentation-overlay66/applied.json','presentation-overlay66/independent.verdict.exactraw.json']]
 files += [D/'independent-math66'/f for f in ['run.json','lease.final.json','mathematical-review.named.raw.json','mathematical-review.json','structural-math-check.result.json','inputs.manifest.json','finite-presentation-input-maps.json']]
 files += [D/'independent-source66'/f for f in ['review-run.json','complete-RAW-decision.json','RAW-input-payload.json','owned-manifest.json','lease.final.json']]
 files += [D/'anonymous-decoder'/f for f in ['final_run.json','reconstruction_payload.json','lease.json','closure_manifest.json','self_manifest.json','terminal_manifest.json','decoded0.root-adapter.json']]
 files += [H/f for f in ['header0.lean','header1.lean','root.type-representation66.adoption.json','root.statement-representation-seal66.json']]
 write('inputs.manifest.json',{'schema':'exact-SCI66-bounded-inputs-v1','checked_commit':C,'parent':P,'actual_freezer_pid':os.getpid(),'frozen_utc':now(),'exact_Git_current_pins':gitrows,'external_immutable_pins':[pin(p) for p in files],'no_copies_of_native_history_or_whole_ledger':True,'active_commit_observer_excluded':'r66/commit-science66 is untracked postcommit terminal evidence, not a proof input and not scanned as canonical science','finite_maps_only':'Native math adoption, decoder copy mapping, source explicit audit/overlay stages, before-source-admission/before-proved snapshots and reuse-plan before snapshot; no arbitrary fallback'})
 print(json.dumps({'status':'FROZEN','actual_pid':os.getpid(),'checked_commit':C,'Git_inputs':len(gitrows),'bounded_external_inputs':len(files)}),flush=True)
def command(label,args):
 folder=O/label;folder.mkdir(exist_ok=False);started=now()
 with (folder/'stdout.log').open('wb') as out,(folder/'stderr.log').open('wb') as err:
  p=subprocess.Popen(args,cwd=R,stdout=out,stderr=err);print(json.dumps({'event':'START','label':label,'actual_foreground_pid':p.pid,'actual_runner_pid':os.getpid()}),flush=True);code=p.wait()
 r={'label':label,'checked_commit':C,'parent':P,'command':args,'actual_foreground_pid':p.pid,'actual_runner_pid':os.getpid(),'started_utc':started,'finished_utc':now(),'exit_code':code,'terminal_closed':True,'stdout':pin(folder/'stdout.log'),'stderr':pin(folder/'stderr.log')};write(label+'/receipt.json',r);print(json.dumps({'event':'TERMINAL','label':label,'actual_pid':p.pid,'exit_code':code,'terminal_closed':True}),flush=True);return r
def focused():
 checkpins();lake=shutil.which('lake');assert lake;pre=[pin(R/p) for p in [M,T,'lean-toolchain','lake-manifest.json']];write('compiler.pre-pins.json',{'exact_current_RAW_LF':pre,'checked_commit':C,'utc':now()})
 a=command('lake-build',[lake,'build','Tests.ProximalBPSAmbientAdjointCorrector']);assert a['exit_code']==0;b=command('fresh-Test',[lake,'env','lean',T]);assert b['exit_code']==0
 text=pathlib.Path(b['stdout']['path']).read_text(encoding='utf-8');found=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]+)\]",text,re.S);assert len(found)==2 and {n for n,x in found}=={DECL,TESTDECL};parsed=[]
 for n,s in found:
  axioms=[x.strip() for x in s.replace('\n',' ').split(',')];assert len(axioms)==3 and set(axioms)=={'propext','Classical.choice','Quot.sound'};parsed.append({'declaration':n,'axioms':axioms})
 build=pathlib.Path(a['stdout']['path']).read_text(encoding='utf-8');assert 'Build completed successfully (3946 jobs).' in build;post=[pin(R/p) for p in [M,T,'lean-toolchain','lake-manifest.json']];assert pre==post;write('compiler.post-pins.json',{'exact_current_RAW_LF':post,'unchanged':True,'utc':now()})
 write('focused.result.json',{'status':'PASS','checked_commit':C,'parent':P,'actual_pid':os.getpid(),'actual_build':a,'fresh_exact_Test':b,'jobs':3946,'Lake_replay':('Replayed' in build),'fresh_Test_proof_compilation':True,'unchanged_fresh_producer_review':'Closed precommit fresh producer35940 reused by exact Git RAW equality in bindings result; no cached Lake output called fresh producer compilation','standard3':parsed,'pre_post_RAW_LF_equal':True})
def bindings():
 checkpins();ma=read(D/'root.math66.adoption.json');mo=D/'independent-math66';assert logical(mo/'run.json')==ma['native_whole_logical_run_sha256'];assert pin(mo/'mathematical-review.named.raw.json')['raw_sha256']==ma['native_complete_named_RAW_sha256'];assert pin(mo/'lease.final.json')['raw_sha256']==ma['native_lease']['raw_sha256'];ml=read(mo/'lease.final.json');assert ml['status']=='CLOSED_LAST' and ml['final_owned_file_count']==133
 for x in ml['all_owned_except_this_final_lease']:check(x)
 fm=read(mo/'inputs.manifest.json');mathrows=[]
 for p in [M,T]:
  x=next(x for x in fm['inputs'] if x['original']['path']==(R/p).as_posix());check(x['RAW_snapshot']);assert blob(p)==pathlib.Path(x['RAW_snapshot']['path']).read_bytes();mathrows.append({'path':p,'exact_Git_RAW_sha256':sha(blob(p)),'frozen_math_RAW':x['RAW_snapshot']})
 src=D/'independent-source66';sa=read(D/'root.source66.adoption.json');sl=read(src/'lease.final.json');assert sl['status']=='CLOSED_LAST' and sl['owned_file_count']==172;assert logical(src/'review-run.json')==sa['native_whole_logical_run_sha256'];assert pin(src/'review-run.json')['raw_sha256']==sa['native_complete_RAW_review_sha256'];assert pin(src/'complete-RAW-decision.json')['raw_sha256']==sa['native_complete_RAW_decision_sha256'];assert pin(src/'RAW-input-payload.json')['raw_sha256']==sa['separate_complete_RAW_input_sha256'];assert pin(src/'lease.final.json')['raw_sha256']==sa['native_lease']['raw_sha256']
 sm=read(src/'owned-manifest.json');assert pin(src/'owned-manifest.json')['raw_sha256']==sl['manifest_RAW_sha256'];assert len(sm['regular_file_entries'])==170 and sm['total_owned_files_including_self_and_final_lease']==172
 for row in sm['regular_file_entries']:
  q=pin(src/row['name']);assert q['raw_sha256']==row['RAW_sha256'] and q['raw_bytes']==row['RAW_bytes'] and q['lf_sha256']==row['LF_sha256'] and q['lf_bytes']==row['LF_bytes']
 assert all(sl[k]==0 for k in ['actual_close_validator_exit','actual_finalizer_exit','actual_readback_exit'])
 dec=read(src/'complete-RAW-decision.json');sd=dec['source66'];adapter=read(D/'source.1.review.root-adapter.json');assert adapter==dict(sd,native_complete_RAW_review_sha256=sa['native_complete_RAW_review_sha256'],native_review_bytes_preserved=True);assert sd['verdict']=='equivalent-after-elaboration' and not sd['source_mathematical_repair'] and not sd['final_verdict_pending'];assert len(sd['semantic_slots'])==7 and len(sd['audited_declarations'])==2 and all(x['whole_module_review'] for x in sd['audited_declarations']);assert sd['representation_credit']['entire_current_modules_covered'] and sd['representation_credit']['full_literal_expansion_equals_original_headers'];assert sd['publication_binding_sha256']==BIND and sd['publication_context_sha256']==CTX
 da=read(D/'root.decoder66.adoption.json');dp=D/'anonymous-decoder';assert logical(dp/'final_run.json')==da['native_whole_run_sha256'];assert pin(dp/'reconstruction_payload.json')['raw_sha256']==da['native_complete_named_RAW_sha256'];assert read(dp/'lease.json')['status']=='CLOSED_LAST'
 for x in da['raw_snapshot_mappings']:check(x['explicit_exact_raw_snapshot']);assert x['original']['raw_sha256']==x['explicit_exact_raw_snapshot']['raw_sha256']
 dl=read(dp/'lease.json');dc=read(dp/'closure_manifest.json');assert pin(dp/'closure_manifest.json')['raw_sha256']==dl['closure_manifest_raw_sha256']
 for row in dc['artifacts']:
  q=pin(dp/row['path']);assert q['raw_sha256']==row['raw_sha256'] and q['raw_bytes']==row['bytes']
 historical=[]
 for row in ma['finite_historical_resolutions']:
  check(row['exact_native_frozen_RAW']);check(row['exact_native_frozen_LF']);assert row['original']['raw_sha256']==row['exact_native_frozen_RAW']['raw_sha256'];historical.append({'original':row['original'],'resolved_exact_frozen_RAW':row['exact_native_frozen_RAW'],'approved_then_current_is_historical_stage':row['approved_current']})
 stage=read(src/'explicit-draft-to-decoder-audit-map.json');assert pin(src/stage['draft_own_snapshot'])['raw_sha256']==stage['draft_RAW_sha256']==pin(stage['exact_named_historical'])['raw_sha256'];assert pin(src/stage['after_decoder_own_snapshot'])['raw_sha256']==stage['after_decoder_RAW_sha256']
 overlaymap=read(src/'math-freeze1.metadata-overlay.RAW.json')
 for row in overlaymap['explicit_old_to_approved_current_maps']:
  beforepin=pin(R/row['before_snapshot']['path']);proposedpin=pin(R/row['proposed']['path']);assert beforepin['raw_sha256']==row['before']['raw_sha256'] and proposedpin['raw_sha256']==row['proposed']['raw_sha256'];historical.append({'canonical':row['canonical'],'exact_before':beforepin,'approved_then_current_proposed':proposedpin,'allowed_fields':row['allowed_field_paths']})
 assert pin(D/'audit.1.before-source-admission.exactraw.snapshot.json')['raw_sha256']=='4e51ab638c824f702c3dd1c5121740cb0b174b75565c2d53be815124d833944e'
 assert pin(D/'cell.1.before-proved.exactraw.snapshot.json')['raw_sha256']=='fc8ef086d14479f9789aa159147753dc3daa50a70e53b387c7df0b5328f21d41'
 write('finite-historical-resolutions.json',{'status':'PASS','exact_commit':C,'explicit_qualified_maps':historical,'native_source_draft_decoder_stage':stage,'later_stages':['Named before-source-admission audit is the approved decoder/catalogue stage, accepted current audit is root source admission','Named before-proved cell is the approved catalogue stage, final reuse-plan before snapshot is later PROVED_LOCAL state, exact Git cell is only two mirrored APIs after that snapshot'],'arbitrary_snapshot_fallback':False})
 repairs=read(D/'reuse-plan-metadata-repair66/repair.json');before=read(D/'reuse-plan-metadata-repair66/cell.before.exactraw.snapshot.json');after=json.loads(blob(CELL));assert sha(blob(CELL))==repairs['after_RAW_sha256'];assert pin(D/'reuse-plan-metadata-repair66/cell.before.exactraw.snapshot.json')['raw_sha256']==repairs['before_RAW_sha256'];assert before['reuse_plan']['reused_declarations']==repairs['before'] and after['reuse_plan']['reused_declarations']==repairs['after'];rebuilt=json.loads(json.dumps(before));rebuilt['reuse_plan']['reused_declarations']=repairs['after'];assert rebuilt==after
 APIs=['AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.one','AutoSamplingTheory.TechnicalLemmas.Measure.L2Expectation.inner_one_eq_integral'];assert repairs['after']==repairs['before']+APIs
 overlay=read(D/'presentation-overlay66/independent.verdict.exactraw.json');assert not overlay['source_mathematical_repair'] and overlay['formula_changes']==0
 lesson=json.loads(blob(LESSON))['units'][0];assert all(x in lesson['astis_dependencies'] for x in APIs);literal=[]
 for step in lesson['steps']:
  rg=step['lean_source_region'];b=blob(rg['path']);span=b''.join(b.splitlines(keepends=True)[rg['start_line']-1:rg['end_line']]);assert sha(b)==rg['source_raw_sha256'] and sha(span)==rg['exact_code_raw_sha256'] and span.decode()==step['lean'];literal.append(rg)
 assert len(literal)==6
 sys.path.insert(0,str(R/'tools'));import astis_publication as pub
 data=pub.inputs();item=next(x for x in pub.load() if any(y['declaration']==DECL for y in x['bindings']));binding=next(x for x in item['bindings'] if x['declaration']==DECL);bd=pub.binding_digest(item,binding,data);ctx=pub.digest(pub.review_context(item,binding,data));assert bd==BIND and ctx==CTX
 write('bindings.result.json',{'status':'PASS','checked_commit':C,'parent':P,'actual_pid':os.getpid(),'exact_math_Git_RAW_reuse':mathrows,'CLOSED_math133_all_output_bindings_unchanged':True,'native_math_whole':ma['native_whole_logical_run_sha256'],'native_math_complete_named_RAW':ma['native_complete_named_RAW_sha256'],'native_source172_all_output_bindings_unchanged':True,'native_source172_whole':sa['native_whole_logical_run_sha256'],'native_source_complete_RAW_review':pin(src/'review-run.json'),'native_source_complete_RAW_decision':pin(src/'complete-RAW-decision.json'),'native_source_separate_complete_RAW_input':pin(src/'RAW-input-payload.json'),'native_source_lease':pin(src/'lease.final.json'),'source_seven_slots_and_both_whole_modules_private_literal_expansions':sd['representation_credit'],'source_semantic_slots':sd['semantic_slots'],'native_decoder20_all_closure_bindings_unchanged':True,'native_decoder20_whole':da['native_whole_run_sha256'],'native_decoder_complete_RAW':pin(dp/'reconstruction_payload.json'),'literal6_BODY_spans':literal,'primary_source_items':310,'reviewed_catalogue_overlay':pin(D/'presentation-overlay66/independent.verdict.exactraw.json'),'final_process_repair_only_field':'reuse_plan.reused_declarations','two_actual_APIs_mirrored':APIs,'publication_binding_sha256':bd,'publication_context_sha256':ctx,'source_mathematical_repair':False,'finite_historical_maps':'Root math adoption exact native frozen files, decoder23 explicit snapshots, source decision explicit audit stages/overlay mapping, before-source-admission/before-proved snapshots, final reuse-plan before snapshot; never arbitrary fallback.','remaining':'Actual ambient adjoint/global-centered first-corrector geometry only; full B20/B21/H1/dynamics/main/errors/cost/composition/aggregate/reader/full Exposition/PURIFIED/paper/Goal pending.'});print(json.dumps({'status':'BINDINGS_PASS','actual_pid':os.getpid(),'exact_commit':C,'semantic_slots':7,'BODY_steps':6}),flush=True)
def direct():
 checkpins();sys.path.insert(0,str(R/'tools'));import astis_publication as pub,astis
 pub.check_advance([DECL],reviewed=True);hits=astis.forbidden_pattern_hits();assert hits==[];rows=[]
 for p in [M,T]:
  s=(R/p).read_text(encoding='utf-8');assert len(re.findall(r'^private def ',s,re.M))==1 and len(re.findall(r'^theorem ',s,re.M))==1;assert not re.search(r'\b(?:native_decide|run_tac|elab|macro|sorry|admit)\b',s);assert not re.search(r'^private\s+(?:theorem|lemma|opaque|axiom)',s,re.M);rows.append({'path':p,'private_literal_Prop_definitions':1,'private_mathematical_providers':0,'public_proof_declarations':1})
 wdpath=D/'whitespace-diagnosis66/diagnosis.json';wd=read(wdpath);assert blob(wdpath.relative_to(R).as_posix())==wdpath.read_bytes();assert wd['full_staged_exit']==2 and wd['authored_complement_exit']==0 and len(wd['findings'])==1628
 for row in wd['immutable_native_exceptions']:assert pin(R/row['path'])['raw_sha256']==row['raw_sha256']
 import gzip
 archive=D/'whitespace-diagnosis66/staged.raw-negative.log.gz';streamhash=hashlib.sha256();n=0
 with gzip.open(archive,'rb') as stream:
  while True:
   chunk=stream.read(1024*1024)
   if not chunk:break
   n+=len(chunk);streamhash.update(chunk)
 assert streamhash.hexdigest()==wd['negative_RAW_sha256']
 write('whitespace-exceptions.result.json',{'status':'PRESERVED_TYPED_NATIVE_EXCEPTIONS','checked_commit':C,'diagnosis':pin(wdpath),'immutable_native_findings':1628,'immutable_native_paths':40,'full_staged_exit':2,'full_staged_PASS':False,'root_authored_complement_exit':0,'lossless_negative_archive':pin(archive),'uncompressed_RAW_bytes':n,'uncompressed_RAW_sha256':streamhash.hexdigest(),'current_science_proof_not_changed':True})
 write('reviewed-fakeclosure.result.json',{'status':'PASS','checked_commit':C,'actual_pid':os.getpid(),'reviewed_publication_declarations':[DECL],'actual_repository_forbidden_pattern_hits':hits,'new_module_rows':rows,'private_mathematical_providers':0,'standard3_evidence':pin(O/'focused.result.json'),'aggregate_check':False});print(json.dumps({'status':'REVIEWED_FAKECLOSURE_PASS','actual_pid':os.getpid(),'hits':0}),flush=True)
def gates():
 checkpins();results=[]
 for name,args in [('publication',[PY,'-B','-X','utf8','tools/astis_publication.py','check','--base',P]),('semantic',[PY,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check']),('frontier',[PY,'-B','-X','utf8','tools/astis_frontier_cells.py','check']),('contributor',[PY,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base',P]),('reviewed-fakeclosure',[PY,'-B','-X','utf8',str(O/'verify66.py'),'direct'])]:results.append(command(name,args))
 write('gates.result.json',{'status':'PASS' if all(x['exit_code']==0 for x in results) else 'FAIL','checked_commit':C,'parent':P,'actual_runner_pid':os.getpid(),'fresh_required_gates':results,'aggregate_site_build_run':False});assert all(x['exit_code']==0 for x in results)
if __name__=='__main__':
 mode=sys.argv[1]
 try:globals()[mode]()
 except Exception as e:
  if not (O/'lease.final.json').exists():write(mode+'.failure.json',{'status':'FAIL','checked_commit':C,'actual_pid':os.getpid(),'exception':repr(e),'traceback':traceback.format_exc(),'utc':now()})
  raise
