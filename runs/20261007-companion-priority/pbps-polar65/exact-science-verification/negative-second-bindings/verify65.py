import collections,datetime,hashlib,json,os,pathlib,re,subprocess,sys,traceback
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;D=O.parent;M=D/'independent-math65';S=D/'independent-source65';B=D/'anonymous-decoder';P=R/'runs/20261007-companion-priority/pbps-polar-preproof65'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
COMMIT='dad6e38c9beed3476cb5d1db06eb57b955c8e3eb';PARENT='0aef19ca2711159eeaec86d42c9be142a94fa402';ACTOR='/root/exact_science63';SAU='ASTIS-SA-20261009-PBPSActualPolarIsometry'
DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.PolarIsometry.actual_centered_polar_isometry';TEST='Tests.ProximalBPSPolarIsometry.genuine_actual_polar_corrector_consumer';DECLS=[DECL]
FILES=['AutoSamplingTheory/ExampleCases/ProximalBPS/PolarIsometry.lean','Tests/ProximalBPSPolarIsometry.lean'];AUDIT='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualPolarIsometry.json';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-polar-isometry.json';PUB='website/content/publications/pbps-actual-polar-isometry.json';LESSON='website/content/declaration_lessons/pbps-actual-polar-isometry.json'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def write(n,x):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8'))
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return {'path':p.as_posix(),'raw_bytes':len(b),'raw_sha256':sha(b),'lf_bytes':len(l),'lf_sha256':sha(l)}
def expected(x):
 return {'raw_bytes':x.get('raw_bytes',x.get('RAW_bytes',x.get('bytes'))),'raw_sha256':x.get('raw_sha256',x.get('RAW_sha256')),'lf_sha256':x.get('lf_sha256',x.get('LF_sha256'))}
def match(p,x):
 a=pin(p);e=expected(x);assert a['raw_sha256']==e['raw_sha256'],(str(p),a['raw_sha256'],e['raw_sha256'])
 if e['raw_bytes'] is not None:assert a['raw_bytes']==e['raw_bytes']
 if e['lf_sha256'] is not None:assert a['lf_sha256']==e['lf_sha256']
 return a
def git(*a):return subprocess.run(['git',*a],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout
def exact():assert git('rev-parse','HEAD').decode().strip()==COMMIT and git('rev-parse',COMMIT+'^').decode().strip()==PARENT
def checkpins():
 exact()
 for x in read(O/'inputs.manifest.json')['inputs']:match(x['path'],x)
def logical(p):
 j=read(p);h=j.pop('run_sha256');assert sha(canon(j))==h,(str(p),'whole logical run minus ONLY run_sha256');return h
def finite_map():
 return {str((R/AUDIT).as_posix()):{
 'c9e6d896c543e0eaf7841db6852f1be3bae32886788221139923bf62b5e18763':D/'audit.0.before-decoder.exactraw.snapshot.json',
 '207f7f0ebf5eab055f8a00135a9297723877bf8ac6fdcc2b13573114521683fe':D/'audit.0.before-source-admission.exactraw.snapshot.json'},
 (R/CELL).as_posix():{'05370368af7487680c2b51f9ba82f999001b882f6014440007700f500f8b22bf':D/'cell.0.before-proved.exactraw.snapshot.json'}}
def resolve(p,x):
 p=pathlib.Path(p);e=expected(x)
 if p.is_file() and pin(p)['raw_sha256']==e['raw_sha256']:return p,'current-exact-RAW'
 fm=finite_map();assert p.as_posix() in fm and e['raw_sha256'] in fm[p.as_posix()],('no arbitrary fallback',str(p),e)
 q=fm[p.as_posix()][e['raw_sha256']];match(q,x);return q,'explicit-finite-historical-RAW-map'
def freeze():
 exact();assert not (O/'lease.open.json').exists()
 write('lease.open.json',{'status':'OPEN','actor':ACTOR,'actual_pid':os.getpid(),'opened_utc':now(),'checked_commit':COMMIT,'parent':PARENT,'owned_prefix':O.as_posix(),'only_shared_write_authorized':'one proper non-owner VERIFIED append and r65/verified.json after gates'})
 rows=[];seen=set();resolutions=[]
 def add(p,x=None,role='exact-current'):
  p=pathlib.Path(p)
  if x:match(p,x)
  if p.as_posix() not in seen:
   rows.append({**pin(p),'role':role});seen.add(p.as_posix())
 for x in read(M/'inputs.manifest.json')['inputs']:
  p,kind=resolve(x['resolved_path'],x);add(p,x,'unchanged-precommit-math-input-qualified')
  if kind!='current-exact-RAW':resolutions.append({'original_path':x['resolved_path'],'expected_RAW_sha256':x['raw_sha256'],'resolved':pin(p),'rule':kind})
 for p in [D/'math-freeze.json',D/'proved-local.json',D/'root.math65.adoption.json',D/'root.source65.adoption.json',D/'root.decoder65.adoption.json',D/'source.0.review.root-adapter.json',D/'source.0.reviewer-packet.json',R/AUDIT,R/CELL,R/PUB,R/LESSON]:add(p)
 for x in read(D/'math-freeze.json')['inputs']:
  p,kind=resolve(x['path'],x);add(p,x,'original-freeze-input-qualified')
  if kind!='current-exact-RAW':resolutions.append({'original_path':x['path'],'expected_RAW_sha256':x['raw_sha256'],'resolved':pin(p),'rule':kind})
 ml=read(M/'lease.final.json')
 for x in ml['all_owned_except_this_final_lease']:add(x['path'],x,'CLOSED-math65-native-output-no-copy')
 add(M/'lease.final.json')
 sm=read(S/'owned-manifest.json')
 for x in sm['files']:add(S/x['name'],x,'CLOSED-source65-native-output-no-copy')
 add(S/'owned-manifest.json');add(S/'lease.final.json')
 for mapname in ['candidate-first-inputs.json','finite-candidate-input-map.json']:
  for x in read(S/mapname)['inputs']:
   p,kind=resolve(x['source_path'],x);add(p,x,'source65-finite-input-qualified')
   if kind!='current-exact-RAW':resolutions.append({'original_path':x['source_path'],'expected_RAW_sha256':expected(x)['raw_sha256'],'resolved':pin(p),'rule':kind})
 for x in read(B/'closure_manifest.json')['artifacts']:add(B/x['path'],x,'CLOSED-decoder65-native-output-no-copy')
 add(B/'closure_manifest.json');add(B/'lease.json');add(B/'decoded0.root-adapter.json')
 for x in read(D/'root.decoder65.adoption.json')['raw_snapshot_mappings']:
  a=x['original'];q=x['explicit_exact_raw_snapshot'];add(q['path'],a,'decoder-explicit-original-to-exact-RAW-snapshot')
  resolutions.append({'original_path':a['path'],'expected_RAW_sha256':a['raw_sha256'],'resolved':pin(q['path']),'rule':'finite root.decoder65.adoption explicit mapping'})
 for f in ['tools/astis_publication.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py','tools/astis_contributor_contract.py','tools/astis_advance.py','tools/astis_harness.py']:add(R/f,role='actual-gate-control-code')
 blobs=[]
 for f in FILES+[PUB,LESSON,AUDIT,CELL,'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean']:
  b=git('show',COMMIT+':'+f);cur=(R/f).read_bytes();assert b==cur,('exact Git RAW equality',f)
  blobs.append({'path':f,'exact_commit':COMMIT,'Git_blob_id':git('rev-parse',COMMIT+':'+f).decode().strip(),'Git_RAW_sha256':sha(b),'worktree_RAW':pin(R/f),'RAW_equal':True})
 write('inputs.manifest.json',{'checked_commit':COMMIT,'parent':PARENT,'actual_freezer_pid':os.getpid(),'frozen_utc':now(),'inputs':rows,'input_count':len(rows),'finite_input_resolutions':resolutions,'no_arbitrary_historical_fallback':True,'no_recursive_history_copy':True,'exact_Git_RAW_blobs':blobs,'math_reuse_candidate_files':FILES,'native_math_files':40,'native_source_files':117,'native_decoder_files':20})
 print(json.dumps({'status':'FROZEN','actual_pid':os.getpid(),'checked_commit':COMMIT,'inputs':len(rows),'finite_maps':len(resolutions),'exact_Git_RAW_blobs':len(blobs)}),flush=True)
def command(label,args):
 checkpins();q=O/label;q.mkdir(exist_ok=True);start=now();env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
 before=[pin(R/f) for f in FILES+['lean-toolchain','lake-manifest.json',PUB,LESSON,AUDIT,CELL]]
 write(label+'/pre.json',{'checked_commit':COMMIT,'parent':PARENT,'actual_runner_pid':os.getpid(),'inputs':before,'started_utc':start})
 with (q/'stdout.log').open('wb') as out,(q/'stderr.log').open('wb') as err:
  p=subprocess.Popen(args,cwd=R,stdout=out,stderr=err,env=env);print(json.dumps({'event':'START','label':label,'actual_pid':p.pid,'command':args}),flush=True);code=p.wait()
 after=[pin(R/f) for f in FILES+['lean-toolchain','lake-manifest.json',PUB,LESSON,AUDIT,CELL]]
 receipt={'command':args,'checked_commit':COMMIT,'parent':PARENT,'actual_foreground_pid':p.pid,'actual_runner_pid':os.getpid(),'exit_code':code,'terminal_closed':True,'started_utc':start,'finished_utc':now(),'pre_pins':before,'post_pins':after,'unchanged_RAW_LF':before==after,'stdout':pin(q/'stdout.log'),'stderr':pin(q/'stderr.log')}
 write(label+'/receipt.json',receipt);assert before==after;checkpins();print(json.dumps({'event':'TERMINAL','label':label,'actual_pid':p.pid,'exit_code':code}),flush=True);return receipt
def focused():
 r=command('focused',['lake','build','Tests.ProximalBPSPolarIsometry']);text=(O/'focused/stdout.log').read_text(encoding='utf-8');jobs=re.findall(r'Build completed successfully \((\d+) jobs\)',text);axioms=[]
 for d in [DECL,TEST]:
  m=re.search(re.escape(d)+r"'? depends on axioms: \[propext,\s*Classical.choice,\s*Quot.sound\]",text);assert m,('standard3',d);axioms.append(m.group(0))
 assert r['exit_code']==0 and jobs==['3945'];write('focused.result.json',{'status':'PASS','checked_commit':COMMIT,'parent':PARENT,'actual_compiler_pid':r['actual_foreground_pid'],'exit_code':0,'terminal_closed':True,'jobs':3945,'standard_axioms':['propext','Classical.choice','Quot.sound'],'declarations':[DECL,TEST],'actual_axiom_blocks':axioms,'fresh_nonforced_invocations':1,'all_input_RAW_LF_pins_unchanged':True,'receipt':pin(O/'focused/receipt.json')})
def bindings():
 checkpins();ml=read(M/'lease.final.json');assert ml['status']=='CLOSED_LAST';assert len(ml['all_owned_except_this_final_lease'])+1==40
 for x in ml['all_owned_except_this_final_lease']:match(x['path'],x)
 mathh=logical(M/'run.json');mathraw=pin(M/'mathematical-review.named.raw.json');ad=read(D/'root.math65.adoption.json');assert mathh==ad['native_whole_logical_run_sha256']==ml['whole_logical_run_sha256'];assert mathraw['raw_sha256']==ad['native_complete_RAW_review_sha256']==ml['complete_named_RAW_review_sha256']
 reuse=[]
 for i,f in enumerate(FILES):
  b=git('show',COMMIT+':'+f);old=(M/f'candidate{i}.exactraw.snapshot').read_bytes();assert b==old==(R/f).read_bytes();reuse.append({'path':f,'exact_Git_RAW_sha256':sha(b),'precommit_snapshot_RAW':pin(M/f'candidate{i}.exactraw.snapshot'),'byte_equal':True})
 parentfile='AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean';assert git('show',PARENT+':'+parentfile)==git('show',COMMIT+':'+parentfile)==(R/parentfile).read_bytes()
 write('mathematics-reuse.json',{'status':'PASS','checked_commit':COMMIT,'parent':PARENT,'two_exact_SOURCE_files':reuse,'unchanged_actual64_parent_RAW':pin(R/parentfile),'closed_math_native_files':40,'whole_logical_run_sha256':mathh,'complete_named_RAW_review':mathraw,'lease':pin(M/'lease.final.json'),'reused_full_mathematical_review_without_replaying_old_proofs':True})
 sl=read(S/'lease.final.json');sm=read(S/'owned-manifest.json');assert sl['status']=='CLOSED_LAST';assert pin(S/'owned-manifest.json')['raw_sha256']==sl['manifest_RAW_sha256']
 assert len(sm['all_owned_file_names'])==117 and len(sm['files'])==115
 assert set(sm['all_owned_file_names'])=={p.name for p in S.iterdir() if p.is_file()}
 for x in sm['files']:match(S/x['name'],x)
 sh=logical(S/'review-run.json');source=read(S/'semantic-decision.json');root=read(D/'source.0.review.root-adapter.json');assert source['review_run_sha256']==sh
 assert root=={**source,'native_complete_RAW_review_sha256':pin(S/'review-run.json')['raw_sha256'],'native_review_bytes_preserved':True},'root adapter must preserve complete native decision and only add the two exact native preservation metadata fields'
 assert source['verdict']=='equivalent-after-elaboration' and source['source_mathematical_repair'] is False and source['repairs']==[] and source['deltas']==[] and len(source['semantic_slots'])==7
 for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:match(S/sl[k]['name'],sl[k])
 ad=read(D/'root.source65.adoption.json');assert sh==sl['whole_logical_run_sha256']==ad['native_whole_logical_run_sha256'];assert sl['COMPLETE_RAW_REVIEW']['RAW_sha256']==ad['native_complete_RAW_review_sha256']
 bl=read(B/'lease.json');assert bl['status']=='CLOSED_LAST' and bl['source_text_visible'] is False and bl['source_identity_visible'] is False and bl['compiler_started'] is False
 bm=read(B/'closure_manifest.json');assert pin(B/'closure_manifest.json')['raw_sha256']==bl['closure_manifest_raw_sha256'];assert len(bm['artifacts'])+2==20
 for x in bm['artifacts']:match(B/x['path'],x)
 bh=logical(B/'final_run.json');ad=read(D/'root.decoder65.adoption.json');assert bh==bl['run_sha256']==ad['native_whole_run_sha256'];assert pin(B/'reconstruction_payload.json')['raw_sha256']==bl['reconstruction_payload_raw_sha256']==ad['native_complete_named_RAW_sha256']
 packet=read(B/'input.packet0.raw.json');pclaim=packet.pop('packet_sha256');assert sha(canon(packet))==pclaim
 a=read(R/AUDIT);assert a['state']=='accepted' and a['verdict']=='equivalent-after-elaboration' and a['repairs']==[] and a['deltas']==[]
 assert a['source_review']['review_run_sha256']==sh and a['reconstruction']['decoder_run_sha256']==bh and a['reconstruction']['native_named_payload_sha256']==bl['reconstruction_payload_raw_sha256']
 assert a['reconstruction']['decoder_packet_sha256']==pclaim and a['reconstruction']['source_text_visible'] is False
 sys.path.insert(0,str(R/'tools'));import astis_publication as pub
 data=pub.inputs();item=next(x for x in data['items'] if any(y['declaration']==DECL for y in x['lean_bindings']));binding=next(x for x in item['lean_bindings'] if x['declaration']==DECL)
 digest=pub.binding_digest(item,binding,data);context=pub.digest(pub.review_context(item,binding,data));assert digest==a['publication_binding_sha256']==source['publication_binding_sha256'];assert context==source['current_publication_context_sha256']==read(D/'root.source65.adoption.json')['current_publication_context_sha256']
 seals=[]
 for i,f in enumerate(FILES):
  b=(R/f).read_bytes();header=b[b.index(b'theorem '):b.index(b':= by')].rstrip(b'\r\n ');seal=(P/f'header{i}.lean').read_bytes().rstrip(b'\r\n ');assert header==seal;seals.append({'path':f,'sealed_header_RAW':pin(P/f'header{i}.lean'),'unchanged':True})
 exp=read(D/'exposition.draft.json');steps=[s for u in exp['units'] for s in u['steps']];matches=[];assert len(steps)==5
 for i,s in enumerate(steps):
  x=s['lean_source_region'];b=(R/x['path']).read_bytes();span=b''.join(b.splitlines(keepends=True)[x['start_line']-1:x['end_line']]);assert sha(b)==x['source_raw_sha256'] and sha(span)==x['exact_code_raw_sha256'];assert span.decode('utf-8')==s['lean'];assert x['start_line']>b[:b.index(b':= by')].count(b'\n')+1;matches.append({'step':i+1,'region':x,'literal_BODY_exact':True,'whole_source_and_line_span_digest_scopes_distinct':True})
 inv=read(P/'independent-primary65/source-coverage-inventory.json');sin=read(P/'independent-primary65/source-inputs.json');full=pathlib.Path(sin['primary_path']).read_bytes();actual=[]
 for reg in sin['named_raw_input_payload']['segment_map']:
  a0,z=reg['source_byte_range'];raw=full[a0:z];assert sha(raw)==reg['raw_sha256']
  for m in re.finditer(rb'<math\b.*?</math>',raw,re.S):actual.append((reg['name'],a0+m.start(),a0+m.end(),sha(m.group(0))))
 assert actual==[(x['region'],x['raw_byte_start'],x['raw_byte_end_exclusive'],x['raw_math_sha256']) for x in inv['math_items']] and len(actual)==280
 assert all(x['annotation_exactly_matches_alttext'] for x in inv['math_items'])
 write('bindings.result.json',{'status':'PASS','checked_commit':COMMIT,'parent':PARENT,'actual_checker_pid':os.getpid(),'mathematics_reuse':pin(O/'mathematics-reuse.json'),'native_source_files':117,'native_source_whole_logical_sha256':sh,'native_source_complete_RAW_review':pin(S/'review-run.json'),'native_source_complete_RAW_decision':pin(S/'semantic-decision.json'),'native_source_complete_RAW_input':pin(S/'RAW-input-payload.json'),'native_source_lease':pin(S/'lease.final.json'),'native_decoder_files':20,'native_decoder_whole_logical_sha256':bh,'native_decoder_complete_named_RAW':pin(B/'reconstruction_payload.json'),'native_decoder_lease':pin(B/'lease.json'),'current_accepted_audit':pin(R/AUDIT),'source_verdict':'equivalent-after-elaboration','mathematical_repairs':False,'semantic_slots':7,'root_adapter_preserves_every_native_decision_field':True,'root_adapter_exact_additions':['native_complete_RAW_review_sha256','native_review_bytes_preserved'],'current_publication_binding_sha256':digest,'current_review_context_sha256':context,'exact_initial_headers':seals,'literal_BODY_steps':matches,'all280_primary_math_items_RAW_spans_valid':True,'finite_historical_input_maps_only':True,'source_Lean_graph_distinction':True,'accepted_scope':source['source_admission'],'remaining':'Typed B0* consumer only. Ambient B* extraction/global centered decomposition/projector and onto/reverse product not credited; B17/H1/full corrector/dynamics/main/errors/cost/composition remain open.'})
 print(json.dumps({'status':'BINDINGS_PASS','actual_pid':os.getpid(),'math_files':40,'source_files':117,'decoder_files':20,'literal_BODY_steps':5,'primary_items':280}),flush=True)
def direct():
 sys.path.insert(0,str(R/'tools'));import astis_publication as pub,astis
 pub.check_advance(DECLS,reviewed=True);hits=astis.forbidden_pattern_hits();assert hits==[]
 new=[]
 for f in FILES:
  s=(R/f).read_text(encoding='utf-8');private=re.findall(r'^private\s+(?:theorem|lemma|def|opaque|axiom)\s+(\S+)',s,re.M);decls=re.findall(r'^(?:theorem|lemma|def|opaque|axiom)\s+(\S+)',s,re.M);assert private==[] and len(decls)==1;assert not re.search(r'\b(?:native_decide|run_tac|elab|macro|sorry|admit)\b',s);new.append({'path':f,'declarations':decls,'imports':re.findall(r'^import\s+(\S+)',s,re.M),'private_providers':private})
 write('focused-reviewed-fakeclosure.result.json',{'status':'PASS','checked_commit':COMMIT,'actual_pid':os.getpid(),'reviewed_publication_declarations':DECLS,'repository_forbidden_pattern_hits':hits,'new_files':new,'new_private_providers':0,'aggregate_integration':False});print(json.dumps({'status':'REVIEWED_PUBLICATION_FAKECLOSURE_PASS','actual_pid':os.getpid(),'forbidden_hits':0,'private_providers':0}),flush=True)
def gates():
 results=[]
 for name,args in [('publication',[PY,'-B','-X','utf8','tools/astis_publication.py','check','--base',PARENT]),('semantic',[PY,'-B','-X','utf8','tools/astis_semantic_roundtrip.py','check']),('frontier',[PY,'-B','-X','utf8','tools/astis_frontier_cells.py','check']),('contributor',[PY,'-B','-X','utf8','tools/astis_contributor_contract.py','check','--base',PARENT]),('focused-reviewed-fakeclosure',[PY,'-B','-X','utf8',str(O/'verify65.py'),'direct'])]:
  r=command(name,args);results.append({'gate':name,'actual_pid':r['actual_foreground_pid'],'exit_code':r['exit_code'],'terminal_closed':r['terminal_closed'],'receipt':pin(O/name/'receipt.json')})
 write('gates.result.json',{'status':'PASS' if all(x['exit_code']==0 for x in results) else 'FAIL','checked_commit':COMMIT,'parent':PARENT,'fresh_focused_gates':results,'whole_astis_site_aggregate_gate_run':False});assert all(x['exit_code']==0 for x in results)
if __name__=='__main__':
 mode=sys.argv[1]
 try:globals()[mode]()
 except Exception as e:
  write(mode+'.failure.json',{'status':'FAIL','actual_pid':os.getpid(),'checked_commit':COMMIT,'exception':repr(e),'traceback':traceback.format_exc(),'utc':now()});raise
