import os,sys,json,hashlib,subprocess,datetime,re,traceback
from pathlib import Path
ROOT=Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-sharp-energy68';O=P/'exact-science-verification';PRE=ROOT/'runs/20261007-companion-priority/pbps-sharp-energy-preproof68'
SCI='a3191d97ccf78d58c301d024fc86b2a3289fc0a6';BASE='38e5f34c6b2c82612459d54d6288a15e20d9deab';ACTOR='/root/exact_science63';SAU='ASTIS-SA-20261009-PBPSSharpCorrectorEnergy';PY=sys.executable
CODE=['AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorBound.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/SharpCorrectorEnergy.lean','Tests/ProximalBPSSharpCorrectorEnergy.lean']
NAMES=['AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.quadratic_corrector_bound_of_square_identity','AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound','Tests.ProximalBPSSharpCorrectorEnergy.genuine_actual_modified_energy_equivalence']
IDS=['hilbert-sharp-quadratic-corrector-bound','pbps-sharp-corrector-energy'];AUDITS=['ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound','ASTIS-RT-20261009-PBPSSharpCorrectorEnergy'];KEYS=['0','1','consumer']
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def get(n):return read(O/n)
def save(n,v):
 assert not (O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(l),lf_sha256=sha(l))
def resolve(p,base=ROOT):
 p=Path(p);return p if p.is_absolute() else base/p
def checkpin(q,base=ROOT):
 p=resolve(q['path'],base);cur=pin(p);h=q.get('raw_sha256',q.get('RAW_sha256'));n=q.get('raw_bytes',q.get('RAW_bytes',q.get('bytes')));lh=q.get('lf_sha256',q.get('LF_sha256'))
 assert cur['raw_sha256']==h and (n is None or cur['raw_bytes']==n),('RAW mismatch',str(p),h,cur['raw_sha256']);assert lh is None or cur['lf_sha256']==lh;return cur
def logical(v):return sha(json.dumps({k:x for k,x in v.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
def stable():
 assert git('rev-parse','HEAD').decode().strip()==SCI
 for q in get('inputs.manifest.json')['reference_pins']:checkpin(q)
 for q in get('Git.blobs.manifest.json')['files']:
  assert sha(git('show',SCI+':'+q['relative_path']))==q['Git_RAW_sha256'];assert pin(ROOT/q['relative_path'])==q['workspace_pin']
def ledgerpin():
 b=(ROOT/'runs/substantive_advances.jsonl').read_bytes();selected=[json.loads(x) for x in b.splitlines() if SAU.encode() in x and json.loads(x).get('advance_id')==SAU]
 return dict(path='runs/substantive_advances.jsonl',raw_bytes=len(b),raw_sha256=sha(b),line_count=len(b.splitlines()),selected_records=selected)
def freeze():
 O.mkdir(parents=True,exist_ok=True);assert not(O/'lease.final.json').exists();assert git('rev-parse','HEAD').decode().strip()==SCI and git('rev-parse',SCI+'^').decode().strip()==BASE
 for old in ['lease.open.json','inputs.manifest.json']:
  if (O/old).exists():
   dest=O/('freeze-v1.'+old+'.exactraw.snapshot');assert not dest.exists();dest.write_bytes((O/old).read_bytes())
 save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),utc=now(),exact_commit=SCI,owned_scope=O.as_posix(),allowed_shared_write='one nonowner VERIFIED event and r68/verified.json after acceptance only'))
 paths=[ROOT/x for x in CODE]+[ROOT/x for x in ['lean-toolchain','lake-manifest.json','tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_semantic_roundtrip.py','tools/astis_contributor_contract.py','tools/astis_frontier_cells.py']]
 paths += [P/x for x in ['proved-local.json','claim.json','math-freeze.json','publication-plan.json','root.math68.adoption.json','root.source68.adoption.json','root.source-delta-schema68.adoption.json','root.decoder68.adoption.json','root.consumer-decoder68.adoption.json','root.prose-span-overlay68.adoption.json','decoder-state-map.for-math68.json','source-admission-finite-current-maps68.json','source-delta-schema-adapter68/proposal.json','finish-exact-admission68/receipt.json','commit-science68/receipt.json']]
 paths += [PRE/'root.statement-seal68.json']+[PRE/f'header{i}-expanded.lean' for i in range(3)]+[PRE/f'statement{i}.definition.lean' for i in [1,2]]
 paths += [P/f'source.{k}.{suffix}.json' for k in KEYS for suffix in ['review.root-adapter','reviewer-packet']]
 paths += [ROOT/f'website/content/{d}/{x}.json' for d in ['publications','declaration_lessons'] for x in IDS]+[ROOT/f'research-wiki/semantic-roundtrip/audits/{x}.json' for x in AUDITS]+[ROOT/f'research-wiki/frontier-cells/{x}.json' for x in ['ASTIS-SHARED-hilbert-corrector-square-bound','ASTIS-SW-PBPS-sharp-corrector-energy']]
 paths += [P/f'independent-math68/{x}' for x in ['lease.final.json','run.json','mathematical-review.json','named-mathematical-review.payload.json','final.inputs.manifest.json','presentation-overlay.decision.json','leaf.compiler.result.json','main.compiler.result.json','test.compiler.result.json']]
 paths += [P/f'independent-source68/{x}' for x in ['lease.final.json','review-run.json','owned-manifest.json','complete-RAW-decision.json','complete-RAW-input-payload.json','source.0.decision.json','source.1.decision.json','source.consumer.decision.json','eleven-literal-BODY-spans.readback.json','nonblocking-exposition-limitation-S-T.json']]
 paths += [P/f'independent-source-delta-schema68/{x}' for x in ['lease.final.json','review-run.json','owned-manifest.json','complete-RAW-decision.json','complete-RAW-input-payload.json']]
 paths += [P/f'{d}/{x}' for d in ['anonymous-decoder','anonymous-consumer-decoder'] for x in ['lease.json','final_run.json','reconstruction_payload.json','closure_manifest.json']]
 paths += [P/f'audit.{i}.{state}.exactraw.snapshot.json' for i in [0,1] for state in ['before-decoder','after-decoder','before-source-admission']]+[P/f'cell.{i}.before-proved.exactraw.snapshot.json' for i in [0,1]]
 paths += [P/'prose-and-span-overlay68-v2/proposal.json']+[P/f'prose-and-span-overlay68-v2/{i}.{s}.exactraw.snapshot.json' for i in [0,1] for s in ['before','after']]+[P/f'applied-prose-span-overlay68/{i}.current-{s}.exactraw.snapshot.json' for i in [0,1] for s in ['before','after']]
 paths=list(dict.fromkeys(paths));assert all(p.is_file() for p in paths),[str(p) for p in paths if not p.is_file()]
 save('inputs.manifest.json',dict(status='PINNED_BEFORE_FOCUSED_COMPILER',actual_PID=os.getpid(),utc=now(),checked_commit=SCI,parent=BASE,input_count=len(paths),reference_pins=[pin(p) for p in paths],policy='Compact exact RAW/LF references. No recursive historical snapshots or ledger copying.'))
 rows=[]
 for i,p in enumerate(paths):
  rel=p.relative_to(ROOT).as_posix()
  if p==P/'commit-science68/receipt.json':
   assert subprocess.run(['git','cat-file','-e',SCI+':'+rel],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
   save('postcommit-receipt-boundary.json',dict(path=rel,RAW=pin(p),not_in_SCI68=True,reason='Foreground commit terminal receipt is necessarily written after its commit; native current observability only, never an input Git-blob claim.',retained_first_observer_failure='freeze.failure.json'));continue
  b=git('show',SCI+':'+rel);cur=p.read_bytes();assert b==cur or b==cur.replace(b'\r\n',b'\n'),('Git relation beyond CRLF',rel)
  r=dict(relative_path=rel,Git_blob_oid=git('rev-parse',SCI+':'+rel).decode().strip(),Git_RAW_sha256=sha(b),Git_RAW_bytes=len(b),workspace_pin=pin(p),relation='exact RAW' if b==cur else 'Git RAW equals workspace LF; workspace RAW separately pinned')
  if rel in CODE or '/header' in rel or '/statement' in rel or '/publications/' in rel or '/declaration_lessons/' in rel or '/semantic-roundtrip/audits/' in rel:
   q=O/f'Git-inputs/{i:03}.blob.RAW';q.parent.mkdir(exist_ok=True);q.write_bytes(b);r['exact_Git_RAW_snapshot']=pin(q)
  rows.append(r)
 save('Git.blobs.manifest.json',dict(exact_commit=SCI,actual_parent=BASE,files=rows));save('ledger.before.pin.json',ledgerpin())
 save('observer.initial-diagnostics.json',dict(status='RETAINED_PATH_OBSERVER_FAILURE',event='Read guessed old audit-helper-v2.executed-helper.RAW.py failed: nonexistent path. Correct evidence located by bounded actual native manifest; no compiler/gate failure and no mathematical credit.',exact_command_exit=1,canonical_or_native_writes=False))
 print(json.dumps(dict(status='PINNED',actual_PID=os.getpid(),inputs=len(paths),exact_commit=SCI)))
def command(label,args):
 with (O/(label+'.stdout.log')).open('wb') as out,(O/(label+'.stderr.log')).open('wb') as err:
  start=now();p=subprocess.Popen(args,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(event='FOREGROUND_START',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 r=dict(label=label,command=args,actual_foreground_PID=p.pid,parent_PID=os.getpid(),started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(O/(label+'.stdout.log')),stderr=pin(O/(label+'.stderr.log')));save(label+'.receipt.json',r);return r
def focused():
 stable();r=command('lake-focused',['lake','build','Tests.ProximalBPSSharpCorrectorEnergy']);assert r['exit_code']==0
 log=(O/'lake-focused.stdout.log').read_text(encoding='utf-8')+(O/'lake-focused.stderr.log').read_text(encoding='utf-8');assert '3950 jobs' in log and not re.search(r': error:|error\(|sorryAx',log)
 pars=[]
 for n in NAMES:
  xs=re.findall(re.escape(n)+r"' depends on axioms:\s*\[([^\]]+)\]",log);assert xs,('no axiom output',n)
  for x in xs:assert set(map(str.strip,x.split(',')))=={'propext','Classical.choice','Quot.sound'} and len(x.split(','))==3
  pars.append(dict(declaration=n,standard3=['propext','Classical.choice','Quot.sound'],instances=len(xs)))
 stable();save('focused.result.json',dict(status='PASS',exact_commit=SCI,receipt=r,all_three_standard3=pars,mode='One nonforced Lake focused build; cached proof output explicitly replay, not newly recompiled producer proof. Fresh independent leaf/main/Test source compilers reused ONLY by exact Git RAW equality in mathematics-reuse.json.',jobs=3950));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),Lake_PID=r['actual_foreground_PID'])))
def native():
 stable();out=[]
 # Exact immutable native file sets, without duplicating their contents.
 for label,folder,leasefile,runfile,adopt in [('math','independent-math68','lease.final.json','run.json','root.math68.adoption.json'),('source','independent-source68','lease.final.json','review-run.json','root.source68.adoption.json'),('schema','independent-source-delta-schema68','lease.final.json','review-run.json','root.source-delta-schema68.adoption.json'),('decoder','anonymous-decoder','lease.json','final_run.json','root.decoder68.adoption.json'),('consumer-decoder','anonymous-consumer-decoder','lease.json','final_run.json','root.consumer-decoder68.adoption.json')]:
  d=P/folder;l=read(d/leasefile);a=read(P/adopt);r=read(d/runfile);assert l['status']=='CLOSED_LAST';assert logical(r)==r['run_sha256']==a['native_whole_logical_run_sha256']==l['whole_logical_run_sha256']
  if label=='math':
   rows=l['all_owned_outputs_except_only_self'];expected=l['owned_file_count_including_self'];[checkpin(q) for q in rows];checkpin(a['native_lease']);checkpin(a['native_complete_named_RAW_payload'])
  elif label in ['source','schema']:
   checkpin(l['owned_manifest'],d);m=read(d/'owned-manifest.json');rows=m.get('rows',m.get('all_regular_owned_files_excluding_manifest_self_and_final_lease'));[checkpin(q,d) for q in rows];expected=l['total_owned_file_count_including_manifest_and_final_lease']
   for k in ['complete_named_RAW_review','complete_named_RAW_decision','complete_named_RAW_input_payload']:checkpin(l[k],d)
   rows=rows+[dict(path='owned-manifest.json')]
  else:
   rows=l['immutable_file_rows'];[checkpin(q,d) for q in rows];expected=l['total_owned_file_count_including_lease'];checkpin(dict(path='reconstruction_payload.json',raw_sha256=a['native_complete_named_RAW_sha256']),d);assert r['source_text_visible'] is False and r['source_identity_visible'] is False
  actual={x.relative_to(d).as_posix() for x in d.rglob('*') if x.is_file()};listed={resolve(q['path'],d).relative_to(d).as_posix() for q in rows}|{leasefile};assert actual==listed and len(actual)==expected,(label,len(actual),expected,actual-listed,listed-actual)
  out.append(dict(package=label,owned_files=expected,lease=pin(d/leasefile),whole_logical_run_sha256=r['run_sha256'],native_verbatim_readback=True))
 # Reuse original math review and ALL fresh independent compiler receipts only by exact code identity.
 fm=read(P/'independent-math68/final.inputs.manifest.json');eq=[]
 for path in CODE:
  row=next(q for q in fm['inputs'] if q['original']['path']==(ROOT/path).as_posix());checkpin(row['RAW_snapshot']);b=git('show',SCI+':'+path);assert b==Path(row['RAW_snapshot']['path']).read_bytes() and pin(ROOT/path)==row['original'];eq.append(dict(path=path,exact_Git_equals_reviewed_RAW=True,RAW=row['original']))
 comp=[]
 for lab in ['leaf','main','test']:
  c=read(P/f'independent-math68/{lab}.compiler.result.json');assert c['status']=='PASS' and c['pre_post_RAW_LF_unchanged'] and c['receipt']['exit_code']==0 and c['receipt']['fresh_Lean'] and c['receipt']['terminal_closed'];assert set(c['exact_standard3'])=={'propext','Classical.choice','Quot.sound'};checkpin(c['receipt']['stdout']);checkpin(c['receipt']['stderr']);comp.append(c)
 save('mathematics-reuse.json',dict(status='PASS',exact_commit=SCI,native_packages=out,code_identity=eq,fresh_independent_precommit_compilers=comp,mathematical_scope='Same K=A0Inv/D=Inv/c=1/gamma; arbitrary complete real Hilbert sharp c/2 sum-of-squares and actual 1/(2gamma) budget; genuine original-input Test all0<omegaWeight<=gamma energy1/2..3/2. Rank0/alphaeta1 retained. No new assumptions/providers/onto/fullinverse/dynamics.',no_replayed_broad_source_transcripts=True));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),native_packages=5,exact_code_files=3)))
def diffpaths(a,b,prefix=''):
 if type(a)!=type(b):return [prefix]
 if isinstance(a,dict):return [p for k in set(a)|set(b) for p in ([prefix+'/'+str(k)] if k not in a or k not in b else diffpaths(a[k],b[k],prefix+'/'+str(k)))]
 if isinstance(a,list):return [prefix] if len(a)!=len(b) else [p for i,(x,y) in enumerate(zip(a,b)) for p in diffpaths(x,y,prefix+'/'+str(i))]
 return [] if a==b else [prefix]
def bindings():
 stable();from tools import astis_publication as pub
 data=pub.inputs();sa=read(P/'root.source68.adoption.json');proposal=read(P/'source-delta-schema-adapter68/proposal.json');res=[]
 for i,key in enumerate(KEYS):
  n=read(P/f'independent-source68/source.{key}.decision.json');a=read(P/f'source.{key}.review.root-adapter.json');packet=read(P/f'source.{key}.reviewer-packet.json');record=sa['decisions'][i]
  assert n['verdict']==a['verdict']=='equivalent-after-elaboration' and n['independent_from_decoder'] and n['independent_from_formalizer'] and not n['blocking_deltas'] and not n['repairs'];assert set(n['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'};checkpin(record['native_decision'])
  expected=dict(n);deltas=[]
  for d,slot in zip(n['deltas'],proposal['slot_map']):
   assert d['blocking'] is False
   deltas.append(dict(d,slot=slot,severity='informational',description=d['detail'],evidence='Native nonblocking source classification: '+d['class']+'; '+d['necessity']+'. '+n['semantic_slots'][slot]['evidence']))
  assert len(deltas)==len(n['deltas'])==5;assert proposal['entries'][i]['native_deltas']==n['deltas'] and proposal['entries'][i]['canonical_deltas']==deltas
  expected['deltas']=deltas;expected['review_run_sha256']=sa['native_whole_logical_run_sha256']
  for k in ['exact_delta_schema_map','native_complete_RAW_review_sha256','native_review_bytes_preserved','external_whole_run_binding']:expected[k]=a[k]
  assert expected==a and a['native_complete_RAW_review_sha256']==sa['native_complete_RAW_review_sha256']
  assert pub.digest(packet)==n['reviewer_packet_sha256']==record['packet_sha256'];assert n['input_bindings']['full_module_raw_sha256']==pin(ROOT/CODE[i])['raw_sha256'];assert n['publication_binding_sha256']==record['publication_binding_sha256']
  if i<2:
   item=next(x for x in pub.load() if x['id']==IDS[i]);binding=next(x for x in item['bindings'] if x['declaration']==NAMES[i]);ctx=pub.review_context(item,binding,data);dig=pub.binding_digest(item,binding,data);assert dig==n['publication_binding_sha256'] and pub.digest(ctx)==n['candidate_context_canonical_sha256']==record['publication_context_sha256'];audit=read(ROOT/f'research-wiki/semantic-roundtrip/audits/{AUDITS[i]}.json');assert audit['state']=='accepted' and audit['verdict']==n['verdict'] and audit['publication_binding_sha256']==dig and audit['deltas']==deltas;review=audit['source_review'];assert review['state']=='accepted' and review['review_run_sha256']==sa['native_whole_logical_run_sha256'] and review['reviewer_packet_sha256']==n['reviewer_packet_sha256']
  else:assert n['input_bindings']['standalone_context_hash_binding'] and not n['input_bindings']['official_production_binding_recomputed_equal'];dig=n['publication_binding_sha256']
  res.append(dict(key=key,declaration=NAMES[i],production_publication=i<2,audit_id=n['audit_id'],verdict=n['verdict'],publication_binding_sha256=dig,reviewer_packet_sha256=n['reviewer_packet_sha256'],retained_deltas=deltas,slots=n['semantic_slots']))
 # Only explicit path-qualified finite chains, never arbitrary hash/snapshot fallback.
 chains={};changes=[]
 def edge(canonical,before,after,allowed,reason):
  canonical=resolve(canonical);before=resolve(before);after=resolve(after);bp=pin(before);ap=pin(after);ds=diffpaths(read(before),read(after));assert all(any(p==q or p.startswith(q+'/') for q in allowed) for p in ds),(reason,ds,allowed)
  chains.setdefault(canonical.as_posix(),[]).append(dict(before=bp,after=ap,reason=reason,changed_JSON_paths=ds));changes.append(dict(canonical=canonical.as_posix(),reason=reason,paths=ds))
 dm=read(P/'decoder-state-map.for-math68.json')
 for row in dm['rows']:
  assert pin(row['frozen_exact_before_snapshot'])['raw_sha256']==row['before_RAW_sha256'] and pin(row['current_exact_after_snapshot'])['raw_sha256']==row['current_RAW_sha256'];edge(row['canonical_file'],row['frozen_exact_before_snapshot'],row['current_exact_after_snapshot'],['/state','/reconstruction'],'two exact decoder-state fields')
 ov=read(P/'root.prose-span-overlay68.adoption.json');checkpin(ov['proposal']);checkpin(ov['native_complete_decision'])
 for i,row in enumerate(ov['finite_application_maps']):
  for k in ['current_before','current_after','independently_approved_after']:checkpin(row[k])
  if i==0:assert Path(row['current_after']['path']).read_bytes()==Path(row['independently_approved_after']['path']).read_bytes();allowed=['/units/0/steps/1/text','/units/0/steps/4/lean/end_line','/units/0/steps/5/lean/end_line']
  else:
   allowed=['/publication_binding_sha256','/publication_context'];v=read(row['current_after']['path']);approved=read(row['independently_approved_after']['path']);assert all(v[k]==approved[k] for k in ['publication_binding_sha256','publication_context']);assert v['reconstruction']==read(row['current_before']['path'])['reconstruction']
  edge(row['canonical_path'],row['current_before']['path'],row['current_after']['path'],allowed,'separately approved applied V2 phrase+two RAW line endpoints/binding')
 am=read(P/'source-admission-finite-current-maps68.json')
 for row in am['rows']:
  assert pin(ROOT/row['original_exact_RAW_snapshot'])['raw_sha256']==row['original_RAW_sha256'] and pin(ROOT/row['canonical_path'])['raw_sha256']==row['current_accepted_RAW_sha256'];edge(row['canonical_path'],row['original_exact_RAW_snapshot'],row['canonical_path'],['/state','/source_review','/verdict','/deltas','/repairs'],'two accepted source-admission audits')
 for i,cell in enumerate(['ASTIS-SHARED-hilbert-corrector-square-bound','ASTIS-SW-PBPS-sharp-corrector-energy']):edge(f'research-wiki/frontier-cells/{cell}.json',P/f'cell.{i}.before-proved.exactraw.snapshot.json',ROOT/f'research-wiki/frontier-cells/{cell}.json',['/status'],'claimed to proved_locally cell status')
 hist=[]
 def qualify(p,h):
  p=resolve(p);current=pin(p)
  if current['raw_sha256']==h:return dict(path=p.as_posix(),resolution='current exact RAW',raw_sha256=h)
  es=chains.get(p.as_posix(),[]);cursor=h;used=[]
  while cursor!=current['raw_sha256']:
   opts=[e for e in es if e['before']['raw_sha256']==cursor];assert len(opts)==1,('no unique explicit finite mapping',p,h,cursor);e=opts[0];used.append(e);cursor=e['after']['raw_sha256'];assert len(used)<=5
  return dict(path=p.as_posix(),resolution='explicit exact finite chain',frozen_RAW_sha256=h,current_RAW_sha256=current['raw_sha256'],chain=used)
 fm=read(P/'independent-math68/final.inputs.manifest.json');assert fm['input_count']==len(fm['inputs'])==44
 for row in fm['inputs']:
  checkpin(row['RAW_snapshot']);checkpin(row['LF_snapshot']);hist.append(qualify(row['original']['path'],row['original']['raw_sha256']))
 src=P/'independent-source68';sm=read(src/'complete-RAW-input-payload.json');assert sm['entry_count']==len(sm['entries'])==146
 sr=[]
 for q in sm['entries']:
  rb=pin(src/q['raw_snapshot']);lb=pin(src/q['lf_snapshot']);assert rb['raw_sha256']==q['RAW_sha256'] and lb['raw_sha256']==q['LF_sha256'];sr.append(qualify(q['source_path'],q['RAW_sha256']))
 save('source-bindings.result.json',dict(status='PASS',exact_commit=SCI,source_audits=res,all15_native_deltas_preserved=True,accepted_schema_adapter_only=True,finite_changes=changes,math44_finite_resolutions=hist,source146_finite_resolutions=sr,source_current_RAW_equal=sum(x['resolution']=='current exact RAW' for x in sr),source_explicit_historical_rows=sum(x['resolution']!='current exact RAW' for x in sr),historical_pre_PROVED_prose_count_144_qualified_as_current142_plus4=True,no_arbitrary_fallback=True,no_wholefolder_exclusions=True));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),source_slots=21,retained_deltas=15,math_rows=44,source_rows=146)))
def scans():
 stable();from tools import astis
 rows=[];hits=[]
 for path in CODE:
  t=(ROOT/path).read_text(encoding='utf-8');clean=astis.strip_lean_comments_and_strings(t)
  for no,line in enumerate(clean.splitlines(),1):
   if astis.FORBIDDEN_REGEX.search(line) or re.search(r'\b(native_decide|run_tac|unsafe|opaque|axiom)\b',line):hits.append(dict(path=path,line=no,text=line))
  defs=re.findall(r'(?m)^private def (\S+)',clean);assert len(defs)==(0 if path==CODE[0] else 1) and all(n.endswith('_statement') for n in defs)
  imports=re.findall(r'(?m)^import (.+)$',t);assert path==CODE[2] or not any(x.startswith('Tests') for x in imports);rows.append(dict(file=path,RAW=pin(ROOT/path),private_full_Props=defs,private_math_providers=0,imports=imports))
 assert not hits
 seal=read(PRE/'root.statement-seal68.json');[checkpin(x['header']) for x in seal['headers']]
 for i in [1,2]:
  checkpin(seal['headers'][i]['literal_definition']);s=(PRE/f'statement{i}.definition.lean').read_text(encoding='utf-8').rstrip('\n');assert s in (ROOT/CODE[i]).read_text(encoding='utf-8')
 spans=[]
 for ident in IDS:
  lesson=read(ROOT/f'website/content/declaration_lessons/{ident}.json')
  for unit in lesson['units']:
   for i,step in enumerate(unit['steps']):
    x=step['lean'];p=ROOT/x['file'];raw=p.read_bytes();lines=raw.splitlines(keepends=True);b=b''.join(lines[x['start_line']-1:x['end_line']]);code=x['code'].encode();assert b==code,(ident,i,x['start_line'],x['end_line'],len(b),len(code));assert x['start_line']>next(j for j,line in enumerate(raw.decode().splitlines(),1) if line.lstrip().startswith(' := by') or line.lstrip().startswith(':= by'))
    spans.append(dict(lesson=ident,step=i+1,file=x['file'],start=x['start_line'],end=x['end_line'],whole_RAW_sha256=sha(raw),literal_span_RAW_sha256=sha(b),literal_RAW=True))
 assert len(spans)==11;save('fake-closure-scan.json',dict(status='PASS',exact_commit=SCI,scanner='Pinned tools.astis comment/string stripping plus forbidden regex/explicit unsafe/provider tokens',files=rows,hits=hits,private_math_providers=0,exact_sealed_full_Props=2,literal_BODY_spans=spans,span_hashes_distinct_from_wholefile_hashes=True,scope='Exact three SCI68 files only; aggregate ASTIS gate deferred to stabilization'));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),fakeclosures=0,BODY=11)))
def gates():
 stable();rs=[]
 for label,args in [('publication',['tools/astis_publication.py','check','--base',BASE,'--ci']),('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check']),('contributor',['tools/astis_contributor_contract.py','check','--base',BASE,'--ci'])]:
  r=command(label,[PY,'-B','-X','utf8',*args]);rs.append(r);assert r['exit_code']==0,('required gate',label,r['exit_code'])
 from tools import astis_publication as pub
 pub.check_advance(NAMES[:2],reviewed=True);stable();save('gates.result.json',dict(status='PASS',exact_commit=SCI,parent=BASE,results=rs,reviewed_check_advance=dict(actual_PID=os.getpid(),declarations=NAMES[:2],reviewed=True,result='PASS'),Test_consumer_separately_reviewed_not_invented_production=True,aggregate_site_main_claim=False));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),gates=5)))
def accept():
 stable()
 for n in ['mathematics-reuse.json','source-bindings.result.json','fake-closure-scan.json','focused.result.json','gates.result.json']:assert get(n)['status']=='PASS'
 from tools import astis_advance as adv
 item=adv.current_advances()[SAU];assert item['state']=='PROVED_LOCAL' and item['owner_id']!=ACTOR;pr=read(P/'proved-local.json');assert pr['lean_declarations']==pr['publication_declarations']==NAMES[:2] and pr['genuine_compiled_source_consumers']==NAMES[2:] and pr['conceptual_mirror_audit']['status']=='none-found'
 save('verification-verdict.json',dict(status='ACCEPTED_EXACT_SCI68',actor=ACTOR,actual_PID=os.getpid(),verified_commit=SCI,parent=BASE,advance_id=SAU,owner_id=item['owner_id'],gate=get('gates.result.json'),focused=get('focused.result.json'),source_audit=get('source-bindings.result.json'),fake_closure_scan=get('fake-closure-scan.json'),math_reuse=get('mathematics-reuse.json'),production_declarations=NAMES[:2],separately_source_reviewed_genuine_Test=NAMES[2],truth_boundary=pr['truth_boundary'],remaining=['B21 rotation/B2 weakH1/B4 dynamics','main/invariance/nonexplosion/errors/caps/cost/actual-input composition','serialized rootimports/Registry/Tests/site/reader admission','generic S,T notation alias reader debt','remoteCI/main/live/fullExposition/PURIFIED/wholepaper/Goal'],no_owner_self_verification=True,full_Exposition=False,PURIFIED=False,Goal=False));print(json.dumps(dict(status='ACCEPTED_EXACT_SCI68',actual_PID=os.getpid(),owner=item['owner_id'],verifier=ACTOR)))
def transition():
 stable();v=get('verification-verdict.json');assert v['status']=='ACCEPTED_EXACT_SCI68';before=ledgerpin();initial=get('ledger.before.pin.json');assert before['raw_sha256']==initial['raw_sha256'] and before['raw_bytes']==initial['raw_bytes']
 from tools import astis_advance as adv
 e=dict(verifier_id=ACTOR,verified_commit=SCI,gate=dict(focused=pin(O/'focused.result.json'),required_gates=pin(O/'gates.result.json'),all_three_standard3=True,reviewed_publications=True,scope='Exact SCI68 independent focused acceptance; aggregate/reader pending'),source_audit=dict(artifact=pin(O/'source-bindings.result.json'),native_whole_source=read(P/'root.source68.adoption.json')['native_whole_logical_run_sha256'],all_three_packets_21slots_15deltas=True,production_audits=AUDITS,separate_Test_consumer=True),fake_closure_scan=dict(artifact=pin(O/'fake-closure-scan.json'),status='PASS',hits=0,private_math_providers=0),publication_declarations=NAMES[:2],native_independent_verdict_path=(O/'verification-verdict.json').relative_to(ROOT).as_posix(),remaining_boundary=v['truth_boundary'])
 adv.transition_advance(SAU,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-commit-verification'],evidence=e)
 b=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert sha(b[:before['raw_bytes']])==before['raw_sha256'];tail=b[before['raw_bytes']:];assert len(tail.splitlines())==1;event=json.loads(tail);assert event['advance_id']==SAU and event['evidence']['verifier_id']==ACTOR and event['evidence']['verified_commit']==SCI
 (O/'ledger.VERIFIED.append.exactraw.jsonl').write_bytes(tail);after=ledgerpin();save('ledger.after.pin.json',after);save('transition.receipt.json',dict(status='VERIFIED_BY_NONOWNER',actual_transition_PID=os.getpid(),verified_commit=SCI,before=before,after=after,append_RAW=pin(O/'ledger.VERIFIED.append.exactraw.jsonl'),one_append=True,prefix_unchanged=True))
 target=P/'verified.json';assert not target.exists();ver=dict(status='VERIFIED',advance_id=SAU,verified_commit=SCI,verifier_id=ACTOR,owner_id=v['owner_id'],actual_transition_PID=os.getpid(),evidence_scope=O.relative_to(ROOT).as_posix(),gate='Focused3950/standard3/fakeclosure/publication-reviewed/semantic/frontier/contributor',source_audits=AUDITS,separately_source_reviewed_genuine_Test=NAMES[2],production_declarations=NAMES[:2],truth_boundary=v['truth_boundary'],ledger_before={k:before[k] for k in ['raw_bytes','raw_sha256']},ledger_after={k:after[k] for k in ['raw_bytes','raw_sha256']},aggregate_integration=False,full_Exposition=False,PURIFIED=False,remoteCI=False,main_live=False,Goal=False);target.write_bytes((json.dumps(ver,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode());save('verified.shared-output.pin.json',pin(target));print(json.dumps(dict(status='VERIFIED_BY_NONOWNER',actual_PID=os.getpid(),verified_commit=SCI)))
def finalchecks():
 stable();assert get('transition.receipt.json')['status']=='VERIFIED_BY_NONOWNER';checkpin(get('verified.shared-output.pin.json'));q=get('ledger.after.pin.json');b=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert len(b)>=q['raw_bytes'] and sha(b[:q['raw_bytes']])==q['raw_sha256']
if __name__=='__main__':
 mode=sys.argv[1]
 try:globals()[mode]()
 except Exception as e:
  if not (O/'lease.final.json').exists():save(mode+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
