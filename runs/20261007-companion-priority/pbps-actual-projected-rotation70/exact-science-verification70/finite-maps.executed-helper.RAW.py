from verify70 import *
import ast,builtins
def diff(a,b,p=''):
 if type(a)!=type(b):return [dict(pointer=p,before=a,after=b)]
 if isinstance(a,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   q=p+'/'+k.replace('~','~0').replace('/','~1')
   out+=diff(a[k],b[k],q) if k in a and k in b else [dict(pointer=q,before=a.get(k),after=b.get(k))]
  return out
 if isinstance(a,list):
  if len(a)!=len(b):return [dict(pointer=p,before_count=len(a),after_count=len(b))]
  return sum((diff(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))),[])
 return [] if a==b else [dict(pointer=p,before=a,after=b)]
def inspect():
 pairs=[('audit',P/'audit.before-source-admission.exactraw.json',AUDIT),('pub',P/'publication.before-final-source-coverage.exactraw.json',PUB),('cellcoverage',P/'cell.before-final-source-coverage.exactraw.json',P/'cell.before-proved.exactraw.json'),('cellstate',P/'cell.before-proved.exactraw.json',CELL)]
 ds={n:diff(read(a),read(b)) for n,a,b in pairs};save('finite-map.inspection.json',ds)
 for n,rows in ds.items():print(n,json.dumps([dict(pointer=r['pointer'],before=str(r.get('before'))[:120],after=str(r.get('after'))[:120]) for r in rows],ensure_ascii=False))
def rowcheck(base,r,lower=False):
 p=base/r['path'];q=pin(p);n=r.get('RAW_bytes',r.get('raw_bytes',r.get('bytes')));h=r.get('RAW_sha256',r.get('raw_sha256'));assert q['raw_bytes']==n and q['raw_sha256']==h,('native row',p)
 if 'LF_sha256' in r:assert q['lf_sha256']==r['LF_sha256'] and q['lf_bytes']==r['LF_bytes']
 if 'lf_sha256' in r:assert q['lf_sha256']==r['lf_sha256'] and q['lf_bytes']==r['lf_bytes']
 return p
def native():
 specs=[(M,'lease.final.json','manifest',121,'run.json','named-review.payload.json'),(S,'lease.final.json','bindings',319,'source.0.review-run.json','complete-named-review-decision-input-payload.json'),(T,'lease.final.json','bindings',14,None,'complete-named-portability-review-input.json'),(D,'lease.json','bindings',12,'review-run.json','complete-reconstruction-decision-input.raw.json')];allpaths=[];packs=[]
 for base,ln,key,count,rn,nn in specs:
  lease=read(base/ln);assert lease['status']=='CLOSED_LAST';rows=lease[key];paths=[]
  for r in rows:
   if key=='manifest':q=dict(r);checkpin({k:v for k,v in q.items() if k!='relative_path'});p=Path(q['path'])
   else:p=rowcheck(base,r)
   paths.append(p)
  paths.append(base/ln);assert len(paths)==count
  if base!=D:assert {p.resolve() for p in paths}=={p.resolve() for p in base.rglob('*') if p.is_file()},('native exact set',base)
  else:assert set(p.name for p in paths)==set(read(D/'native-manifest.json')['owned_paths_including_manifest_and_final_lease'])
  if rn:
   run=read(base/rn);assert logical(run)==run['run_sha256']==lease.get('whole_logical_run_sha256');rh=run['run_sha256']
  else:rh=None
  allpaths+=paths;packs.append(dict(scope=base.as_posix(),native_count=count,lease=pin(base/ln),logical_run_sha256=rh,named_complete_RAW=pin(base/nn),all_manifest_rows_RAW_LF_PASS=True,complete_owned_set_PASS=True))
 # Batch stream exact SCI blobs; only the four named closed70 packages are traversed.
 batch=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);results=[]
 for p in allpaths:
  rel=p.relative_to(ROOT).as_posix();batch.stdin.write((SCI+':'+rel+'\n').encode());batch.stdin.flush();head=batch.stdout.readline().decode().strip().split();assert len(head)==3 and head[1]=='blob',(rel,head);n=int(head[2]);h=hashlib.sha256();left=n
  while left:
   block=batch.stdout.read(min(left,1048576));assert block;h.update(block);left-=len(block)
  assert batch.stdout.read(1)==b'\n';q=pin(p);assert h.hexdigest()==q['raw_sha256'] and n==q['raw_bytes'],('native exact Git RAW',rel);results.append(dict(path=rel,Git_blob_oid=head[0],raw_bytes=n,raw_sha256=h.hexdigest(),exact_current_Git_RAW_equal=True))
 batch.stdin.close();err=batch.stderr.read();code=batch.wait();assert code==0 and not err
 save('native-files.Git.manifest.json',dict(status='PASS',checked_commit=SCI,actual_PID=os.getpid(),actual_foreground_git_batch_PID=batch.pid,actual_git_batch_exit_code=code,closed_packages=packs,Git_RAW_files=len(results),files=results,no_prior63_or69_recursive_scan_or_copy=True));return packs
def review():
 stable();packs=native();m=read(M/'inputs.manifest.json');c=read(M/'compiler.receipt.json');src=CODE.read_bytes();assert sha(src)=='03a0721ae952f744d0bfdf568039b77f7035bec0a50642f8bc8ebc895273b998';assert m['inputs'][0]['original']['raw_sha256']==sha(src);assert c['source_pre']==c['source_post']==pin(CODE);assert c['exact_standard3'] and c['exit_code']==0 and c['actual_foreground_Lake_PID']==42936 and c['fresh_main_Lean_elaboration'] and not c['Lake_build_cache_replay'];assert all(c['pre_pins'][i]==c['post_pins'][i] for i in range(len(c['pre_pins'])))
 mmaps=[]
 for i,r in enumerate(m['inputs']):
  checkpin(r['RAW_snapshot']);checkpin(r['LF_snapshot']);b=Path(r['RAW_snapshot']['path']).read_bytes();assert sha(b)==r['original']['raw_sha256'] and b.replace(b'\r\n',b'\n')==Path(r['LF_snapshot']['path']).read_bytes()
  if i==17:
   assert b==(P/'cell.before-publication70.json').read_bytes();mmaps.append(dict(index=i,kind='EXACT_PREPUBLICATION_CELL_HISTORY',snapshot=r['RAW_snapshot'],current=pin(CELL),current_equality_not_claimed=True))
  else:checkpin(r['original'])
 cr=read(M/'statement-and-parent-retention.json');save('mathematics-reuse.json',dict(status='PASS',checked_commit=SCI,actual_PID=os.getpid(),native_math=packs[0],code_exact_RAW=pin(CODE),exact_original_callers=6,same_outer_witnesses=12,parent_retention=pin(M/'statement-and-parent-retention.json'),fresh_prior_compile=pin(M/'compiler.receipt.json'),compiler_actual_PID=42936,compiler_EXIT=0,all_other18_math_inputs_current_RAW_equal=True,finite_historical_map=mmaps,scope='Independent CLOSED121 full mathematical proof review reused by exact unchanged SCI70 code/header/parents/toolchain RAW. No proof re-review or source reviewer verdict substitution.',rank0_alphaeta1_legal=True,no_onto_V_or68_energy_premise=True))
 slots={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'};decision=read(S/'source.0.decision.json');run=read(S/'source.0.review-run.json');audit=read(AUDIT);adopt=read(P/'root.source70.adoption.json');portable=read(T/'portable-admission-fields.proposed.json');adm=read(S/'source.0.admission-fields.json');pd=read(T/'portability-only.decision.json')
 assert decision['verdict']=='equivalent-after-elaboration' and decision['repairs']==[] and decision['independent_from_formalizer'] and decision['independent_from_decoder'];assert set(decision['semantic_slots'])==slots and len(decision['deltas'])==13 and all(d['severity']=='informational' and d['evidence'] for d in decision['deltas']);assert audit['semantic_slots']==decision['semantic_slots'] and audit['deltas']==decision['deltas'] and audit['verdict']==decision['verdict'] and audit['repairs']==[];assert audit['source_review']['state']=='accepted';assert audit['source_review']['review_run_sha256']==run['run_sha256']==adopt['native_whole_logical_run_sha256'];assert sha((S/'complete-named-review-decision-input-payload.json').read_bytes())==adopt['native_complete_named_RAW_sha256'];assert pd['verdict']=='APPROVE_EXACT_FIVE_LOCATOR_FIELDS_ONLY' if 'verdict' in pd else pd['status']=='APPROVE_EXACT_FIVE_LOCATOR_FIELDS_ONLY'
 assert portable['audit_fields']=={k:audit[k] for k in portable['audit_fields']};pitems=read(PUB)['items'];assert len(pitems)==1;pub=pitems[0];assert pub['source_proof_coverage']==portable['publication_source_proof_coverage'];before=read(P/'audit.before-source-admission.exactraw.json');expected=copy.deepcopy(before);expected.update(portable['audit_fields']);assert expected==audit,('audit exact approved admission mismatch',diff(expected,audit))
 pb=read(P/'publication.before-final-source-coverage.exactraw.json');pe=copy.deepcopy(pb);pe['items'][0]['source_proof_coverage']=portable['publication_source_proof_coverage'];assert pe==read(PUB),('publication only portable coverage',diff(pe,read(PUB)))
 cb=read(P/'cell.before-final-source-coverage.exactraw.json');cp=read(P/'cell.before-proved.exactraw.json');cd=diff(cb,cp);assert all('source_proof_coverage' in r['pointer'] for r in cd);assert cp['source_proof_coverage']==portable['publication_source_proof_coverage'];state_diff=diff(cp,read(CELL));assert len(state_diff)==1 and state_diff[0]['pointer']=='/status' and state_diff[0]['before']=='claimed' and state_diff[0]['after']=='proved_locally'
 fi=read(S/'complete-exact-input-manifest.json');maps={x['index']:x for x in adopt['finite_current_input_maps']};assert set(maps)=={21,26,28,31,32};resolved=[];current=0
 hist={24:P/'audit.before-source-admission.exactraw.json',26:S/'current70.publication.exactraw.json',28:S/'current70.frontier.exactraw.json',31:S/'current70.inline_lean.exactraw.py',32:S/'current70.check_cross_domain_browser.exactraw.py',62:P/'audit.before-source-admission.exactraw.json',64:P/'publication.before-final-source-coverage.exactraw.json',66:P/'cell.before-final-source-coverage.exactraw.json'}
 for i,r in enumerate(fi['inputs']):
  b=(S/r['snapshot']).read_bytes();assert len(b)==r['RAW_bytes'] and sha(b)==r['RAW_sha256'];lf=(S/r['LF_snapshot']).read_bytes();assert b.replace(b'\r\n',b'\n')==lf and sha(lf)==r['LF_sha256'];orig=Path(r['original_path'])
  if i==21:
   whole=orig.read_bytes();lo,hi=r['original_RAW_range_end_exclusive'];assert whole[lo:hi]==b and sha(whole)==r['original_whole_RAW_sha256']==maps[21]['current_RAW_sha256'];kind='EXACT_RAW_OFFSET_FRAGMENT_NOT_WHOLE_FILE';q=pin(orig)
  elif i in hist:
   assert hist[i].read_bytes()==b;kind='EXPLICIT_FINITE_HISTORICAL_MAP';q=pin(hist[i])
   if i in maps:assert maps[i]['frozen_RAW_sha256']==sha(b)
  else:
   assert orig.read_bytes()==b,('unmapped source input drift',i,str(orig));current+=1;kind='EXACT_CURRENT_RAW';q=pin(orig)
  resolved.append(dict(index=i,snapshot=r['snapshot'],RAW_sha256=sha(b),LF_sha256=sha(lf),resolution=kind,authority=q))
 # Current accepted source fields and bindings must still name the exact official packet.
 packet=read(P/'source-review.packet.1.json');assert audit['source_review']['reviewer_packet_sha256']==decision['reviewer_packet_sha256']==run['fixed_current']['official_packet_canonical_sha256']=='47d6ccfb1422007c0b18f8be0cebffbdbe642f7d3068ee12206e27ecf472cce8';assert audit['publication_binding_sha256']==run['fixed_current']['publication_binding_sha256'];assert audit['publication_context']['file']==sha(src)
 lesson=read(LESSON)['units'][0];assert lesson['declaration']==DECL and len(lesson['steps'])==8;lines=src.splitlines(keepends=True);steps=[]
 for i,s in enumerate(lesson['steps']):
  r=s['lean_source_region'];lo,hi=r['start_line'],r['end_line'];b=b''.join(lines[lo-1:hi]);assert lo>=144 and hi<=539 and r['path']==CODE.relative_to(ROOT).as_posix() and r['source_raw_sha256']==sha(src) and sha(b)==r['exact_code_raw_sha256'] and b==s['lean'].encode();assert s['formula'];steps.append(dict(index=i,start_line=lo,end_line=hi,literal_BODY_RAW_sha256=sha(b),formula_RAW_sha256=sha(s['formula'].encode()),literal_match=True))
 assert steps[0]['start_line']==144 and steps[-1]['end_line']==539 and all(a['end_line']+1==b['start_line'] for a,b in zip(steps,steps[1:]));assert run['coverage']['BODY_steps']==8 and run['coverage']['module_lines']==544 and run['coverage']['all_unclassified']==0
 save('source-bindings.result.json',dict(status='PASS',checked_commit=SCI,actual_PID=os.getpid(),native_source=packs[1],portable_native=packs[2],blind_native=packs[3],source_slots=7,informational_deltas=13,blocking_deltas=0,repairs=0,canonical_source_decision_exact=True,source_proof_coverage_only_exact_five_portable_locator_fields=True,official_packet_sha256=decision['reviewer_packet_sha256'],publication_binding_sha256=audit['publication_binding_sha256'],source_input_count=len(resolved),source_current_whole_RAW_rows=current,finite_historical_rows=len(hist),literal_fragment_rows=1,source_input_resolutions=resolved,all8_literal_BODY_steps=steps,all419_primary_items_and544_module_lines_native_coverage_retained=True,canonical_audit_exact_approved_admission=True,cell_state_only_claimed_to_proved_locally=True,source_graph_not_Lean_graph=True,no_full_Exposition_PURIFIED_or_wholepaper_credit=True))
 tree=ast.parse((ROOT/'tools/astis.py').read_text(encoding='utf-8-sig'));nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FORBIDDEN_REGEX' for t in n.targets) or isinstance(n,ast.FunctionDef) and n.name=='strip_lean_comments_and_strings'];assert len(nodes)==2;env={'re':re};exec(builtins.compile(ast.Module(body=nodes,type_ignores=[]),'pinned_astis_scanner','exec'),env);hits=[];modules=[CODE,ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ReflectionIntertwining.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/GaussianReflection.lean']
 for p in modules:
  clean=env['strip_lean_comments_and_strings'](text(p));hits += [dict(path=p.as_posix(),match=h.group(0)) for h in env['FORBIDDEN_REGEX'].finditer(clean)]
 assert not hits;ct=text(CODE);assert re.findall(r'^import (.+)$',ct,re.M)==['AutoSamplingTheory.ExampleCases.ProximalBPS.ReflectionIntertwining'];assert len(re.findall(r'^private def ',ct,re.M))==1 and len(re.findall(r'^theorem ',ct,re.M))==1;assert 'SharpCorrectorEnergy' not in ct and 'HilbertCorrectorBound' not in ct
 save('fake-closure-scan.json',dict(status='PASS',checked_commit=SCI,actual_PID=os.getpid(),actual_repository_scanner=pin(ROOT/'tools/astis.py'),method='AST extract exact FORBIDDEN_REGEX and strip_lean_comments_and_strings; scan only exact target plus2 actual parents',reviewed_modules=[pin(p) for p in modules],hits=hits,private_literal_full_Props=1,private_mathematical_providers=0,public_theorems=1,no_Test70=True,no68_energy_parent=True,no_onto_V=True,mathematical_meaning_reused_by_exact_RAW=pin(M/'named-review.payload.json')))
 ws=read(P/'whitespace-diagnosis70/diagnosis.json');assert len(ws['findings'])==1539 and ws['full_staged_exit']==2 and ws['authored_complement_exit']==0;save('whitespace.boundary.json',dict(immutable_native_findings=1539,authored_complement_PASS=True,full_staged_whitespace_PASS=False,authority=pin(P/'whitespace-diagnosis70/diagnosis.json'),no_native_whitespace_rewrite=True));stable();print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),native_Git_RAW_files=sum(p['native_count'] for p in packs),source_slots=7,source_deltas=13,BODY_steps=8,source_current_rows=current,source_historical_rows=len(hist),source_fragment_rows=1)))
if __name__=='__main__':
 try:globals()[sys.argv[1]]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else sys.argv[1])+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
