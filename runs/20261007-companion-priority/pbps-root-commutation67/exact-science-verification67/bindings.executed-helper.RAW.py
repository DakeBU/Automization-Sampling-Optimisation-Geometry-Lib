import os,sys,json,hashlib,subprocess,datetime,re,traceback
from pathlib import Path
ROOT=Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-root-commutation67';O=P/'exact-science-verification67';PRE=ROOT/'runs/20261007-companion-priority/pbps-first-corrector-energy-preproof67'
SCI='3da29415011a971a65f749502a625e416213f487';BASE='eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176';ACTOR='/root/exact_science63';SAU='ASTIS-SA-20261009-PBPSActualRootInverseCommutation'
NAMES=['AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareCommute.positive_square_commutation','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualRootCommutation.actual_same_root_inverse_commutation','Tests.ProximalBPSActualRootCommutation.genuine_actual_corrector_coefficient_consumer']
CODE=['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareCommute.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/ActualRootCommutation.lean','Tests/ProximalBPSActualRootCommutation.lean']
IDS=['real-l2-positive-square-commutation','pbps-actual-root-inverse-commutation'];AUDITS=['ASTIS-RT-20261009-RealL2PositiveSquareCommutation','ASTIS-RT-20261009-PBPSActualRootInverseCommutation']
PY=sys.executable
sys.path.insert(0,str(ROOT))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def get(n):return read(O/n)
def save(n,v):
 p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(l),lf_sha256=sha(l))
def logical(v):return sha(json.dumps({k:x for k,x in v.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
def checkpin(q):
 p=pin(q['path']);h=q.get('raw_sha256',q.get('RAW_sha256'));n=q.get('raw_bytes',q.get('RAW_bytes'))
 assert p['raw_sha256']==h and (n is None or p['raw_bytes']==n),('RAW pin mismatch',q['path'],h,p['raw_sha256'])
 lh=q.get('lf_sha256',q.get('LF_sha256'));assert lh is None or lh==p['lf_sha256']
def stable():
 assert git('rev-parse','HEAD').decode().strip()==SCI
 for q in get('inputs.manifest.json')['reference_pins']:checkpin(q)
 for q in get('Git.blobs.manifest.json')['files']:
  b=git('show',SCI+':'+q['relative_path']);assert sha(b)==q['Git_RAW_sha256']
  p=pin(ROOT/q['relative_path']);assert p==q['workspace_pin']
 return True
def ledgerpin():
 b=(ROOT/'runs/substantive_advances.jsonl').read_bytes();rows=[]
 for line in b.splitlines():
  if SAU.encode() in line:
   v=json.loads(line)
   if v.get('advance_id')==SAU:rows.append(v)
 return dict(path='runs/substantive_advances.jsonl',raw_bytes=len(b),raw_sha256=sha(b),lines=len(b.splitlines()),selected_advance_records=rows)
def freeze():
 O.mkdir(parents=True,exist_ok=True);assert not (O/'lease.final.json').exists()
 assert git('rev-parse','HEAD').decode().strip()==SCI and git('rev-parse',SCI+'^').decode().strip()==BASE
 save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_pid=os.getpid(),utc=now(),exact_commit=SCI,owned_scope=O.as_posix(),allowed_shared_write='one nonowner VERIFIED append for named SAU and root67 verified.json only'))
 paths=[ROOT/f for f in CODE]+[ROOT/'lean-toolchain',ROOT/'lake-manifest.json',ROOT/'tools/astis.py',ROOT/'tools/astis_advance.py',ROOT/'tools/astis_publication.py',ROOT/'tools/astis_semantic_roundtrip.py',ROOT/'tools/astis_contributor_contract.py',ROOT/'tools/astis_frontier_cells.py',ROOT/'research-wiki/semantic-roundtrip/registry.json',
 PRE/'root.statement-seal67.json',*[PRE/f'header{i}-expanded.lean' for i in range(3)],*[PRE/f'statement{i}.definition.lean' for i in (1,2)],
 P/'proved-local.json',P/'claim.json',P/'math-freeze.json',P/'root.math67.adoption.json',P/'root.decoder67.adoption.json',P/'root.source67.adoption.json',P/'root.attribution-overlay67.adoption.json',P/'source-delta-schema-adapter67/resolution.json',P/'conceptual-mirror-audit67.json',
 *[P/f'source.{i}.review.root-adapter.json' for i in (0,1)],*[P/f'source.{i}.reviewer-packet.json' for i in (0,1)],
 *[ROOT/f'website/content/publications/{x}.json' for x in IDS],*[ROOT/f'website/content/declaration_lessons/{x}.json' for x in IDS],*[ROOT/f'research-wiki/semantic-roundtrip/audits/{x}.json' for x in AUDITS],
 *[ROOT/f'research-wiki/frontier-cells/{x}.json' for x in ['ASTIS-SHARED-l2-real-positive-square-commutation','ASTIS-SW-PBPS-actual-root-inverse-commutation']],
 P/'independent-math67/lease.final.json',P/'independent-math67/run.json',P/'independent-math67/mathematical-review.json',P/'independent-math67/mathematical-review.named.raw.json',
 P/'independent-source67/lease.final.json',P/'independent-source67/raw-payload-bindings.json',P/'independent-source67/review-run.json',P/'independent-source67/complete-RAW-decision.json',P/'independent-source67/RAW-input-payload.json',P/'independent-source67/finite-current-to-freeze-map.json',*[P/f'independent-source67/source.{i}.decision.json' for i in (0,1)],
 P/'anonymous-decoder/lease.json',P/'anonymous-decoder/final_run.json',P/'anonymous-decoder/reconstruction_payload.json',P/'anonymous-decoder/closure_manifest.json']
 save('inputs.manifest.json',dict(status='PINNED_BEFORE_COMPILER',actual_pid=os.getpid(),utc=now(),checked_commit=SCI,parent=BASE,reference_pins=[pin(p) for p in paths],policy='Compact references to immutable packages; no recursive copying/history/ledger snapshot. Git snapshots only current mathematical/publication statements.'))
 files=[]
 for i,p in enumerate(paths):
  rel=p.relative_to(ROOT).as_posix();b=git('show',SCI+':'+rel);cur=p.read_bytes();eq=b==cur
  assert eq or b==cur.replace(b'\r\n',b'\n'),('Git RAW differs beyond CRLF',rel)
  item=dict(relative_path=rel,Git_RAW_bytes=len(b),Git_RAW_sha256=sha(b),Git_blob_oid=git('rev-parse',SCI+':'+rel).decode().strip(),workspace_pin=pin(p),relation='exact RAW' if eq else 'Git RAW equals workspace LF only; workspace RAW remains separately pinned')
  if rel in CODE or '/header' in rel or '/statement' in rel or '/publications/' in rel or '/declaration_lessons/' in rel or '/semantic-roundtrip/audits/' in rel:
   s=O/f'Git-inputs/{i:03}.blob.RAW';s.parent.mkdir(exist_ok=True);s.write_bytes(b);item['owned_exact_Git_RAW_snapshot']=pin(s)
  files.append(item)
 save('Git.blobs.manifest.json',dict(exact_commit=SCI,actual_parent=BASE,files=files))
 save('ledger.before.pin.json',ledgerpin())
 save('observer.initial-path-diagnostics.json',dict(status='RETAINED_OBSERVER_PATH_ERRORS',failure_class='ENV_BLOCKED',events=['Incorrect guessed tools/check_contributor_contract.py help path: Python cannot open file; corrected to tools/astis_contributor_contract.py.','rg guessed nonexistent tools/astis_check.py; real scanner is tools/astis.py forbidden_pattern_hits.','Guessed old verification.py and decoder lease.final.json did not exist; corrected using bounded directory listing, actual decoder lease.json.'],mathematical_or_gate_credit=False,required_gate_failure=False,no_native_files_modified=True))
 print(json.dumps(dict(status='PINNED',actual_pid=os.getpid(),inputs=len(paths),checked_commit=SCI)))
def focused():
 stable();pre=[pin(ROOT/p) for p in CODE]+[pin(ROOT/'lean-toolchain'),pin(ROOT/'lake-manifest.json')]
 results=[]
 for label,cmd in [('lake-focused',['lake','build','Tests.ProximalBPSActualRootCommutation']),('fresh-Test',['lake','env','lean','Tests/ProximalBPSActualRootCommutation.lean'])]:
  r=command(label,cmd);results.append(r);assert r['exit_code']==0
  log=(O/(label+'.stdout.log')).read_text(encoding='utf-8')+(O/(label+'.stderr.log')).read_text(encoding='utf-8')
  assert not re.search(r': error:|error\(|sorryAx',log)
  parsed=[]
  for name in NAMES:
   matches=re.findall(re.escape(name)+r"' depends on axioms:\s*\[([^\]]+)\]",log)
   assert matches,('missing actual axiom output',label,name)
   for s in matches:
    axioms=[x.strip() for x in s.split(',')];assert set(axioms)=={'propext','Classical.choice','Quot.sound'} and len(axioms)==3
   parsed.append(dict(declaration=name,exact_axioms=['propext','Classical.choice','Quot.sound'],output_instances=len(matches)))
  r['standard3']=parsed
  if label=='lake-focused':assert '3948 jobs' in log
 assert pre==[pin(ROOT/p) for p in CODE]+[pin(ROOT/'lean-toolchain'),pin(ROOT/'lake-manifest.json')]
 save('focused.result.json',dict(status='PASS',actual_pid=os.getpid(),checked_commit=SCI,results=results,pre_post_exact_pins=pre,cache_replay='Lake focused dependency replay separately classified',fresh_proof_compiler='lake env lean exact Test; unchanged producer mathematics reused by exact Git RAW, no forced rebuild'))
 stable();print(json.dumps(dict(status='PASS',actual_pid=os.getpid(),processes=[r['actual_foreground_PID'] for r in results])))
def command(label,cmd):
 with (O/(label+'.stdout.log')).open('wb') as out,(O/(label+'.stderr.log')).open('wb') as err:
  start=now();p=subprocess.Popen(cmd,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(event='FOREGROUND_START',label=label,actual_foreground_PID=p.pid)),flush=True);code=p.wait()
 r=dict(label=label,command=cmd,actual_foreground_PID=p.pid,actual_parent_PID=os.getpid(),started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(O/(label+'.stdout.log')),stderr=pin(O/(label+'.stderr.log')));save(label+'.receipt.json',r);return r
def native_packages():
 stable();math=P/'independent-math67';src=P/'independent-source67';dec=P/'anonymous-decoder'
 ma=read(P/'root.math67.adoption.json');sa=read(P/'root.source67.adoption.json');da=read(P/'root.decoder67.adoption.json')
 ml=read(math/'lease.final.json');sl=read(src/'lease.final.json');dl=read(dec/'lease.json')
 assert ml['status']==sl['status']==dl['status']=='CLOSED_LAST'
 assert pin(math/'lease.final.json')['raw_sha256']==ma['native_final_lease']['raw_sha256']
 for q in ml['all_owned_except_this_final_lease']:checkpin(q)
 mr=read(math/'run.json');assert logical(mr)==mr['run_sha256']==ma['native_whole_logical_run_sha256']
 checkpin(ma['native_complete_named_RAW_payload'])
 assert pin(src/'lease.final.json')['raw_sha256']==sa['native_lease']['RAW_sha256']
 for q in sl['owned_files_except_this_final_lease']:checkpin(q)
 sr=read(src/'review-run.json');assert logical(sr)==sr['run_sha256']==sa['native_whole_logical_run_sha256']
 binds=read(src/'raw-payload-bindings.json');assert binds['whole_logical_run_sha256']==sr['run_sha256']
 for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:checkpin(binds[k])
 assert binds['COMPLETE_RAW_REVIEW']['RAW_sha256']==sa['native_complete_RAW_review_sha256'] and binds['COMPLETE_RAW_DECISION']['RAW_sha256']==sa['native_complete_RAW_decision_sha256']
 dr=read(dec/'final_run.json');assert logical(dr)==dr['run_sha256']==da['native_whole_run_sha256']==dl['run_sha256']
 assert pin(dec/'reconstruction_payload.json')['raw_sha256']==da['native_complete_named_RAW_sha256']==dl['reconstruction_payload_raw_sha256']
 assert not dr['source_text_visible'] and not dr['source_identity_visible'] and not dr['compiler_started']
 closure=read(dec/'closure_manifest.json')
 for q in closure['artifacts']:
  p=dec/q['path'];assert pin(p)['raw_sha256']==q['raw_sha256'] and pin(p)['raw_bytes']==q['bytes']
 for q in da['raw_snapshot_mappings']:checkpin(q['explicit_exact_raw_snapshot']);assert q['original']['raw_sha256']==q['explicit_exact_raw_snapshot']['raw_sha256']
 vm=read(math/'mathematical-review.json');rows=[]
 for path,want in zip(CODE,['3c2e4892a24890f0c007ca6ecf9806baa42f0b50f62fc0484066e6643e2b303c','8567673eba335e7c1209f8bd90ce510954426bd5bbcdef6ff53ea97889762748','28028653027a811d677c71efdc621e0f42fc176844677b67b7799821f035e6c1']):
  b=git('show',SCI+':'+path);assert sha(b)==want==pin(ROOT/path)['raw_sha256'];rows.append(dict(path=path,Git_RAW_sha256=want,identical_to_CLOSED_math67=True))
 save('mathematics-reuse.json',dict(status='PASS',actual_pid=os.getpid(),checked_commit=SCI,math_CLOSED_count=164,source_CLOSED_count=262,decoder_CLOSED_count=25,mathematical_verdict=vm['status'],code_rows=rows,math_whole=mr['run_sha256'],math_complete_named_RAW=pin(math/'mathematical-review.named.raw.json'),source_whole=sr['run_sha256'],source_complete_RAW=binds['COMPLETE_RAW_REVIEW'],decoder_whole=dr['run_sha256'],decoder_complete_RAW=pin(dec/'reconstruction_payload.json'),no_proof_transcript_replay=True))
 print(json.dumps(dict(status='PASS',actual_pid=os.getpid(),native_counts=[164,262,25],same_math_files=3)))
def bindings():
 stable();from tools import astis_publication as pub
 sa=read(P/'root.source67.adoption.json');schema=read(P/'source-delta-schema-adapter67/resolution.json');data=pub.inputs();out=[]
 for i,ident in enumerate(IDS):
  n=read(P/f'independent-source67/source.{i}.decision.json');a=read(P/f'source.{i}.review.root-adapter.json');packet=read(P/f'source.{i}.reviewer-packet.json')
  assert n['verdict']==a['verdict']=='equivalent-after-elaboration' and n['independent_from_decoder'] and n['independent_from_formalizer']
  assert set(n['semantic_slots'])=={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
  expected=json.loads(json.dumps(n));deltas=[]
  for d in n['deltas']:
   assert d['blocking'] is False;v=dict(d,severity='informational',evidence=n['semantic_slots'][d['slot']]['evidence']);deltas.append(v)
  expected['deltas']=deltas;expected['review_run_sha256']=sa['native_whole_logical_run_sha256']
  for k in ['native_complete_RAW_review_sha256','native_review_bytes_preserved','exact_delta_schema_map','external_whole_run_binding']:expected[k]=a[k]
  assert a==expected and a['native_review_bytes_preserved'] and a['native_complete_RAW_review_sha256']==sa['native_complete_RAW_review_sha256']
  assert schema['rows'][i]['native_deltas']==n['deltas'] and schema['rows'][i]['canonical_deltas']==deltas
  item=next(x for x in pub.load() if x['id']==ident);binding=next(x for x in item['bindings'] if x['declaration']==NAMES[i]);ctx=pub.review_context(item,binding,data);digest=pub.binding_digest(item,binding,data)
  assert ctx==n['publication_context']==a['publication_context']
  assert digest==n['publication_binding_sha256']==sa['decisions'][i]['publication_binding_sha256']
  assert pub.digest(ctx)==n['publication_context_sha256']==sa['decisions'][i]['publication_context_sha256']
  assert n['reviewer_packet_sha256']==sa['decisions'][i]['packet_sha256']
  audit=read(ROOT/f'research-wiki/semantic-roundtrip/audits/{AUDITS[i]}.json');assert audit['state']=='accepted' and audit['verdict']=='equivalent-after-elaboration'
  review=audit['source_review'];assert review['state']=='accepted' and review['review_run_sha256']==sa['native_whole_logical_run_sha256'] and review['run_artifact']==f'runs/20261007-companion-priority/pbps-root-commutation67/source.{i}.review.root-adapter.json'
  assert audit['publication_binding_sha256']==digest and review['reviewer_packet_sha256']==n['reviewer_packet_sha256']
  out.append(dict(declaration=NAMES[i],audit_id=AUDITS[i],verdict=a['verdict'],source_reviewer=review['reviewer'],publication_binding_sha256=digest,publication_context_sha256=pub.digest(ctx),retained_nonblocking_deltas=deltas,complete_context_and_adapter_equal=True))
 # Check finite original-freeze maps using only recorded chains and specifically named pre-admission snapshots.
 fm=read(P/'independent-source67/finite-current-to-freeze-map.json');hist=[];explicit=[]
 for i,aid in enumerate(AUDITS):explicit.append(P/f'audit.{i}.before-source-admission.exactraw.snapshot.json')
 explicit += [P/'cell.0.before-proved.exactraw.snapshot.json',P/'cell.1.before-proved.exactraw.snapshot.json']
 explicit += [Path(s[z]['path']) for row in fm['pins'] for s in row.get('finite_chain',[]) for z in ['before','after'] if Path(s[z]['path']).is_file()]
 for row in fm['pins']:
  q=row['original_freeze'];h=q['raw_sha256'];c=row['current_pin'];ch=c['RAW_sha256']
  for state in [q,c]+[s[z] for s in row.get('finite_chain',[]) for z in ['before','after']]:
   want=state.get('raw_sha256',state.get('RAW_sha256'));p=Path(state['path'])
   if p.exists() and pin(p)['raw_sha256']==want:resolved=p
   else:
    candidates=[p2 for p2 in explicit if p2.exists() and pin(p2)['raw_sha256']==want];assert candidates,('no explicit finite map',state['path'],want);resolved=candidates[0]
   hist.append(dict(original_path=state['path'],expected_RAW_sha256=want,explicit_resolved_path=resolved.as_posix(),resolution='current exact' if resolved==p else 'explicit named chain/pre-source/pre-proved snapshot'))
 save('source-bindings.result.json',dict(status='PASS',actual_pid=os.getpid(),exact_commit=SCI,source_audits=out,adapter_preserved_every_delta_and_same_slot_evidence=True,native_unchanged=True,finite_original_freeze_rows=len(fm['pins']),finite_resolutions=hist,no_arbitrary_fallback=True,attribution_requirement='Previously required Test66 attribution separately reviewed and reflected in exact current source contexts'))
 print(json.dumps(dict(status='PASS',actual_pid=os.getpid(),source_audits=2,retained_deltas=sum(len(x['retained_nonblocking_deltas']) for x in out),finite_rows=len(fm['pins']))))
def scans():
 stable();from tools import astis
 hits=[];rows=[]
 for path in CODE:
  t=(ROOT/path).read_text(encoding='utf-8');clean=astis.strip_lean_comments_and_strings(t)
  for i,line in enumerate(clean.splitlines(),1):
   if astis.FORBIDDEN_REGEX.search(line) or re.search(r'\b(native_decide|run_tac|unsafe|opaque|axiom)\b',line):hits.append(dict(path=path,line=i,text=line))
  defs=re.findall(r'(?m)^private def (\S+)',clean);assert len(defs)==(0 if path==CODE[0] else 1) and all(x.endswith('_statement') for x in defs)
  rows.append(dict(path=path,whole_RAW=pin(ROOT/path),private_literal_Prop_definitions=defs,private_math_providers=0,imports=re.findall(r'(?m)^import (.+)$',t)))
 assert not hits
 save('fake-closure-scan.json',dict(status='PASS',actual_pid=os.getpid(),exact_commit=SCI,scanner='tools.astis.strip_lean_comments_and_strings + FORBIDDEN_REGEX and explicit unsafe/provider patterns',files=rows,hits=hits,accepted_math_and_sealed_statements_reused=True,scope='Three exact SCI67 modules; not full aggregate ASTIS check'))
 print(json.dumps(dict(status='PASS',actual_pid=os.getpid(),hits=0,private_math_providers=0)))
def gates():
 stable();results=[]
 for label,args in [('publication',['tools/astis_publication.py','check','--base',BASE,'--ci']),('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check']),('contributor',['tools/astis_contributor_contract.py','check','--base',BASE,'--ci'])]:
  r=command(label,[PY,'-B','-X','utf8',*args]);results.append(r);assert r['exit_code']==0,('required gate failed',label)
 from tools import astis_publication as pub
 pub.check_advance(NAMES[:2],reviewed=True)
 save('gates.result.json',dict(status='PASS',actual_pid=os.getpid(),exact_commit=SCI,base=BASE,results=results,reviewed_check_advance=dict(actual_PID=os.getpid(),reviewed=True,declarations=NAMES[:2],result='PASS'),no_shared_build_or_site_claim=True))
 stable();print(json.dumps(dict(status='PASS',actual_pid=os.getpid(),required_gates=5)))
def accept():
 stable()
 for n in ['focused.result.json','mathematics-reuse.json','source-bindings.result.json','fake-closure-scan.json','gates.result.json']:assert get(n)['status']=='PASS'
 from tools import astis_advance as advance
 item=advance.current_advances()[SAU];assert item['state']=='PROVED_LOCAL' and item['owner_id']!=ACTOR
 evidence=get('ledger.before.pin.json')['selected_advance_records'];assert any(x.get('to_state')=='PROVED_LOCAL' or x.get('state')=='PROVED_LOCAL' for x in evidence)
 proved=read(P/'proved-local.json');assert set(proved['publication_declarations'])==set(NAMES[:2]) and proved['conceptual_mirror_audit']['status']=='none-found'
 v=dict(status='ACCEPTED_EXACT_SCI67',actor=ACTOR,actual_review_PID=os.getpid(),verified_commit=SCI,parent=BASE,advance_id=SAU,source_audit=get('source-bindings.result.json'),fake_closure_scan=get('fake-closure-scan.json'),gate=get('gates.result.json'),focused=get('focused.result.json'),math_reuse=get('mathematics-reuse.json'),PROVED_LOCAL_owner=item['owner_id'],declarations=NAMES,publication_declarations=NAMES[:2],truth_boundary=proved['truth_boundary'],remaining=['Sharp B23 norm bound and B19/B22/B24 energy equivalence','B21 rotation','B2/H1 and B4 dynamics','main theorem','errors/caps/expected costs/composition','aggregate Registry/root imports/Tests/site/reader admission','push/remoteCI/main/live/full Exposition/PURIFIED/whole paper/Goal'],no_root_self_verification=True,full_Exposition=False,PURIFIED=False)
 save('verification-verdict.json',v);print(json.dumps(dict(status=v['status'],actual_PID=os.getpid(),owner=item['owner_id'],independent_verifier=ACTOR)))
def transition():
 stable();v=get('verification-verdict.json');assert v['status']=='ACCEPTED_EXACT_SCI67'
 from tools import astis_advance as advance
 before=ledgerpin();initial=get('ledger.before.pin.json');assert before['raw_sha256']==initial['raw_sha256'] and before['raw_bytes']==initial['raw_bytes']
 evidence=dict(verifier_id=ACTOR,verified_commit=SCI,gate=dict(focused=get('focused.result.json'),required_gates=get('gates.result.json'),scope='Exact SCI67 focused/required admission only; aggregate and reader integration pending'),source_audit=get('source-bindings.result.json'),fake_closure_scan=get('fake-closure-scan.json'),publication_declarations=NAMES[:2],native_independent_verdict_path=(O/'verification-verdict.json').relative_to(ROOT).as_posix(),remaining_boundary=v['truth_boundary'])
 advance.transition_advance(SAU,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-commit-verification'],evidence=evidence)
 full=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert sha(full[:before['raw_bytes']])==before['raw_sha256'];tail=full[before['raw_bytes']:];lines=tail.splitlines();assert len(lines)==1
 event=json.loads(lines[0]);assert event['advance_id']==SAU and event['evidence']['verifier_id']==ACTOR and event['evidence']['verified_commit']==SCI
 (O/'ledger.VERIFIED.append.exactraw.jsonl').write_bytes(tail);after=ledgerpin()
 save('ledger.after.pin.json',after);save('transition.receipt.json',dict(status='VERIFIED_BY_NONOWNER',actual_transition_PID=os.getpid(),exact_commit=SCI,actor=ACTOR,before=before,after=after,append_RAW=pin(O/'ledger.VERIFIED.append.exactraw.jsonl'),one_append=True,historical_prefix_unchanged=True))
 verified=dict(status='VERIFIED',advance_id=SAU,verified_commit=SCI,verifier_id=ACTOR,owner_id=v['PROVED_LOCAL_owner'],actual_transition_PID=os.getpid(),evidence_scope=O.relative_to(ROOT).as_posix(),gate='focused Test3948 plus exact standard3/fakeclosure/publication-reviewed/semantic/frontier/contributor',source_audits=AUDITS,truth_boundary=v['truth_boundary'],ledger_before=dict(raw_bytes=before['raw_bytes'],raw_sha256=before['raw_sha256']),ledger_after=dict(raw_bytes=after['raw_bytes'],raw_sha256=after['raw_sha256']),full_Exposition=False,PURIFIED=False,aggregate_integration=False,remoteCI=False,main_live=False)
 target=P/'verified.json';assert not target.exists();target.write_bytes((json.dumps(verified,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode());save('verified.shared-output.pin.json',pin(target));print(json.dumps(dict(status='VERIFIED_BY_NONOWNER',actual_PID=os.getpid(),verified_commit=SCI,one_append=True)))
def owned():return sorted(p for p in O.rglob('*') if p.is_file())
def term(n):
 t=get(n+'.terminal.json');assert t['exit_code']==0 and t['terminal_closed'];return t
def finalchecks():
 stable();assert get('transition.receipt.json')['status']=='VERIFIED_BY_NONOWNER';checkpin(get('verified.shared-output.pin.json'));r=get('ledger.after.pin.json');b=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert len(b)==r['raw_bytes'] and sha(b)==r['raw_sha256']
def finalize():
 finalchecks();ts={n:term(n) for n in ['freeze','focused','native','bindings','scans','gates','accept','transition']};pre=[pin(p) for p in owned() if p.name not in ['finalize.stdout.log','finalize.stderr.log']]
 payload=dict(complete_verdict=get('verification-verdict.json'),complete_input_manifest=get('inputs.manifest.json'),exact_Git_blob_manifest=get('Git.blobs.manifest.json'),transition=get('transition.receipt.json'),verified_shared_output=get('verified.shared-output.pin.json'),owned_pre_finalizer_outputs=pre,stage_actual_terminals=ts,observer_negatives=get('observer.initial-path-diagnostics.json'),failure_records=[read(p) for p in O.glob('*.failure.json')])
 save('named-verification.payload.json',payload)
 run=dict(schema=1,status='VERIFIED_EXACT_SCI67',actor=ACTOR,exact_commit=SCI,parent=BASE,actual_finalizer_PID=os.getpid(),utc=now(),complete_named_RAW=pin(O/'named-verification.payload.json'),simple_verdict_RAW=pin(O/'verification-verdict.json'),pre_finalizer_outputs=pre,whole_hash_rule='Complete logical JSON removes ONLY top-level run_sha256',full_Exposition=False,PURIFIED=False)
 run['run_sha256']=logical(run);save('run.json',run);save('finalizer.result.json',dict(status='PASS',actual_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW=run['complete_named_RAW']));print(json.dumps(dict(status='PASS',whole_logical=run['run_sha256'],namedRAW=run['complete_named_RAW'])))
def readback():
 finalchecks();r=get('run.json');assert logical(r)==r['run_sha256'];checkpin(r['complete_named_RAW']);checkpin(r['simple_verdict_RAW'])
 for q in r['pre_finalizer_outputs']:checkpin(q)
 save('readback.result.json',dict(status='PASS',actual_PID=os.getpid(),actual_finalizer=term('finalize'),whole_logical=r['run_sha256']));print(json.dumps(dict(status='PASS',actual_PID=os.getpid())))
def close():
 finalchecks();r=get('run.json');assert logical(r)==r['run_sha256'] and get('readback.result.json')['status']=='PASS';ft=term('finalize');rt=term('readback')
 save('close.result.json',dict(status='PASS',actual_close_PID=os.getpid(),utc=now(),all_foreground_sessions_closed=True))
 save('final.manifest.json',dict(status='ALL_OWNED_BEFORE_FINAL_LEASE',files=[pin(p) for p in owned()],excludes_only_self_and_future_lease=True))
 pins=[pin(p) for p in owned()];lease=dict(status='CLOSED_LAST',actor=ACTOR,actual_close_PID=os.getpid(),utc=now(),exact_commit=SCI,owned_file_count_including_lease=len(pins)+1,all_owned_except_final_lease=pins,whole_logical_run_sha256=r['run_sha256'],complete_named_RAW=r['complete_named_RAW'],simple_verdict_RAW=r['simple_verdict_RAW'],actual_finalizer_PID=ft['actual_worker_PID'],actual_finalizer_exit=0,actual_readback_PID=rt['actual_worker_PID'],actual_readback_exit=0,final_owned_write=True,postclose='read-only; no owned writes')
 save('lease.final.json',lease);print(json.dumps(dict(status='CLOSED_LAST',actual_close_PID=os.getpid(),owned_count=len(pins)+1,whole_logical=r['run_sha256'],complete_named_RAW=r['complete_named_RAW'],leaseRAW=pin(O/'lease.final.json'))))
def postclose():
 finalchecks();l=get('lease.final.json');assert l['status']=='CLOSED_LAST' and len(owned())==l['owned_file_count_including_lease']
 for q in l['all_owned_except_final_lease']:checkpin(q)
 assert max(p.stat().st_mtime_ns for p in owned())==(O/'lease.final.json').stat().st_mtime_ns
 r=get('run.json');assert logical(r)==r['run_sha256'];print(json.dumps(dict(status='READ_ONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),owned_count=len(owned()),whole_logical=r['run_sha256'],complete_named_RAW=r['complete_named_RAW'],leaseRAW=pin(O/'lease.final.json'),owned_writes=0)))
if __name__=='__main__':
 mode=sys.argv[1]
 try:{'freeze':freeze,'focused':focused,'native':native_packages,'bindings':bindings,'scans':scans,'gates':gates,'accept':accept,'transition':transition,'finalize':finalize,'readback':readback,'close':close,'postclose':postclose}[mode]()
 except Exception as e:
  if mode not in ['close','postclose'] and not (O/'lease.final.json').exists():save(mode+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),mode=mode,error=repr(e),traceback=traceback.format_exc()))
  raise
