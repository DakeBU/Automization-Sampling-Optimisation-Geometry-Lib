import os,sys,json,hashlib,datetime,subprocess,traceback
from pathlib import Path
ROOT=Path('E:/Samplinglib');P=ROOT/'runs/20261007-companion-priority/pbps-sharp-energy68';OLD=P/'exact-science-verification';O=P/'exact-science-verification68-corrected'
SCI='3ad3b127b5a645be9cf71b3d14520b2d8fea3122';BASE='a3191d97ccf78d58c301d024fc86b2a3289fc0a6';ACTOR='/root/exact_science63';SAU='ASTIS-SA-20261009-PBPSSharpCorrectorEnergy';CELL='research-wiki/frontier-cells/ASTIS-SHARED-hilbert-corrector-square-bound.json';PY=sys.executable
NAMES=['AutoSamplingTheory.TechnicalLemmas.Analysis.HilbertCorrectorBound.quadratic_corrector_bound_of_square_identity','AutoSamplingTheory.ExampleCases.ProximalBPS.SharpCorrectorEnergy.actual_sharp_corrector_bound','Tests.ProximalBPSSharpCorrectorEnergy.genuine_actual_modified_energy_equivalence']
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tools'))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def get(n):return read(O/n)
def save(n,v):
 assert not(O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode())
def pin(p):
 p=Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_bytes=len(l),lf_sha256=sha(l))
def checkpin(q):assert pin(q['path'])==q,('RAW/LF pin mismatch',q['path'])
def logical(v):return sha(json.dumps({k:x for k,x in v.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
def ledgerpin():
 b=(ROOT/'runs/substantive_advances.jsonl').read_bytes();selected=[json.loads(x) for x in b.splitlines() if SAU.encode() in x and json.loads(x).get('advance_id')==SAU];return dict(path='runs/substantive_advances.jsonl',raw_bytes=len(b),raw_sha256=sha(b),line_count=len(b.splitlines()),selected_records=selected)
def stable():
 assert git('rev-parse','HEAD').decode().strip()==SCI
 for q in get('inputs.manifest.json')['reference_pins']:checkpin(q)
 for q in get('Git.blobs.manifest.json')['files']:assert sha(git('show',SCI+':'+q['relative_path']))==q['Git_RAW_sha256']
def freeze():
 O.mkdir(parents=True,exist_ok=True);assert git('rev-parse','HEAD').decode().strip()==SCI and git('rev-parse',SCI+'^').decode().strip()==BASE
 for old in ['lease.open.json','inputs.manifest.json']:
  if (O/old).exists():
   snap=O/('freeze-v1.'+old+'.exactraw.snapshot');assert not snap.exists();snap.write_bytes((O/old).read_bytes())
 save('lease.open.json',dict(status='OPEN',actor=ACTOR,actual_PID=os.getpid(),utc=now(),exact_commit=SCI,parent=BASE,allowed_shared_write='one exact NONOWNER VERIFIED append and r68/verified.json after gates only'))
 paths=[Path(x['path']) for x in read(OLD/'inputs.manifest.json')['reference_pins']]
 paths += [OLD/x for x in ['lease.final.json','run.json','named-verification.payload.json','verification-verdict.json','inputs.manifest.json','Git.blobs.manifest.json','mathematics-reuse.json','source-bindings.result.json','fake-closure-scan.json','focused.result.json','gates.result.json','frontier.receipt.json','frontier.stdout.log','ledger.before.pin.json']]
 paths += [P/f'frontier-metadata-correction68/{x}' for x in ['correction.json','before.exactraw.snapshot','after.exactraw.snapshot','executed-helper.RAW.py']]+[P/'correct-frontier-metadata68/receipt.json',ROOT/'.agents/skills/astis-substantive-advance/SKILL.md']
 paths=list(dict.fromkeys(paths));assert all(x.is_file() for x in paths);save('inputs.manifest.json',dict(status='PINNED_BEFORE_GATES',actual_PID=os.getpid(),utc=now(),exact_commit=SCI,parent=BASE,input_count=len(paths),reference_pins=[pin(x) for x in paths],policy='Compact immutable RAW/LF references; original CLOSED131 is reused, never written or copied recursively.'))
 rows=[];external=[]
 exact_external={OLD/x for x in ['lease.final.json','run.json','named-verification.payload.json','verification-verdict.json','inputs.manifest.json','Git.blobs.manifest.json','mathematics-reuse.json','source-bindings.result.json','fake-closure-scan.json','focused.result.json','gates.result.json','frontier.receipt.json','frontier.stdout.log','ledger.before.pin.json']}|{P/'commit-science68/receipt.json',P/'correct-frontier-metadata68/receipt.json'}
 for path in paths:
  rel=path.relative_to(ROOT).as_posix()
  if path in exact_external:
   assert subprocess.run(['git','cat-file','-e',SCI+':'+rel],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
   external.append(dict(RAW_LF=pin(path),classification='Explicit external closed independent verifier evidence' if path.parent==OLD else 'Explicit external foreground process receipt; written after committed payload.'));continue
  b=git('show',SCI+':'+rel);cur=path.read_bytes();assert b==cur or b==cur.replace(b'\r\n',b'\n');rows.append(dict(relative_path=rel,Git_RAW_sha256=sha(b),Git_RAW_bytes=len(b),Git_blob_oid=git('rev-parse',SCI+':'+rel).decode().strip(),workspace_RAW_LF=pin(path),relation='exact RAW' if b==cur else 'Git RAW equals workspace LF; original RAW separately pinned'))
 save('Git.blobs.manifest.json',dict(exact_commit=SCI,parent=BASE,files=rows,exact_named_external_evidence=external,no_generic_or_recursive_exclusion=True));save('ledger.before.pin.json',ledgerpin());print(json.dumps(dict(status='PINNED',actual_PID=os.getpid(),input_count=len(paths),Git_rows=len(rows),explicit_external_rows=len(external))))
def field(v,p):
 for k in p.strip('/').split('/'):v=v[k]
 return v
def diffpaths(a,b,p=''):
 if type(a)!=type(b):return [p]
 if isinstance(a,dict):return [z for k in set(a)|set(b) for z in ([p+'/'+k] if k not in a or k not in b else diffpaths(a[k],b[k],p+'/'+k))]
 if isinstance(a,list):return [] if a==b else [p]
 return [] if a==b else [p]
def review():
 stable();l=read(OLD/'lease.final.json');r=read(OLD/'run.json');assert l['status']=='CLOSED_LAST' and l['owned_file_count_including_self']==131 and logical(r)==r['run_sha256']==l['whole_logical_run_sha256'];checkpin(l['named_complete_RAW_review'])
 listed={Path(q['path']).relative_to(OLD).as_posix() for q in l['all_owned_outputs_except_only_self']}|{'lease.final.json'};actual={x.relative_to(OLD).as_posix() for x in OLD.rglob('*') if x.is_file()};assert actual==listed
 for q in l['all_owned_outputs_except_only_self']:checkpin(q)
 v=read(OLD/'verification-verdict.json');assert v['status']=='OBSTRUCTED_EXACT_SCI68_NO_VERIFIED' and v['checked_commit']==BASE
 for name in ['mathematics-reuse.json','source-bindings.result.json','fake-closure-scan.json','focused.result.json']:assert read(OLD/name)['status']=='PASS'
 c=read(P/'frontier-metadata-correction68/correction.json');checkpin(c['before']);checkpin(c['after']);assert c['science_commit']==BASE and c['native_obstruction_whole_logical_sha256']==r['run_sha256'];checkpin(c['native_obstruction_lease'])
 before=Path(c['before']['path']).read_bytes();after=Path(c['after']['path']).read_bytes();assert git('show',BASE+':'+CELL)==before and git('show',SCI+':'+CELL)==after==(ROOT/CELL).read_bytes();a=read(c['before']['path']);b=read(c['after']['path']);allowed={'/route','/consumers','/shared_floor_audit/decision','/shared_floor_audit/reason','/reuse_plan/decision_reason'};assert set(diffpaths(a,b))==allowed=={x['field'] for x in c['finite_field_changes']}
 for q in c['finite_field_changes']:assert field(a,q['field'])==q['before'] and field(b,q['field'])==q['after']
 assert b['route']=='samplewiki-route' and b['shared_floor_audit']['decision']=='new_route_local' and b['consumers']==NAMES[1:] and b['cell_id']==a['cell_id'];assert b['shared_floor_audit']['canonical_declaration']==NAMES[0] and b['shared_floor_audit']['reason']==b['reuse_plan']['decision_reason']
 assert 'same paper route' in b['shared_floor_audit']['reason'] and 'transitively' in b['shared_floor_audit']['reason'] and b['consumers'][1] in a['reuse_plan']['known_consumers']
 changed=git('diff','--name-only',BASE,SCI).decode().splitlines();canonical=[x for x in changed if not x.startswith('runs/20261007-companion-priority/pbps-sharp-energy68/')];assert canonical==[CELL],canonical
 # Every previous exact Git-bound proof/source/header/publication artifact is unchanged except this ONE documented cell.
 oldgit=read(OLD/'Git.blobs.manifest.json')['files'];eq=[]
 for q in oldgit:
  path=q['relative_path'];prev=git('show',BASE+':'+path);cur=git('show',SCI+':'+path);assert sha(prev)==q['Git_RAW_sha256'];assert path==CELL or prev==cur;eq.append(dict(relative_path=path,parent_RAW_sha256=sha(prev),current_RAW_sha256=sha(cur),relation='five-field finite process correction' if path==CELL else 'exact same Git RAW'))
 oldrefs=read(OLD/'inputs.manifest.json')['reference_pins'];current=[]
 for q in oldrefs:
  if Path(q['path'])==ROOT/CELL:assert q['raw_sha256']==c['before']['raw_sha256'] and pin(ROOT/CELL)['raw_sha256']==c['after']['raw_sha256'];current.append(dict(original=q,explicit_after=pin(ROOT/CELL),finite_map=pin(P/'frontier-metadata-correction68/correction.json')))
  else:checkpin(q)
 focused=read(OLD/'focused.result.json');assert focused['jobs']==3950 and focused['receipt']['exit_code']==0 and len(focused['all_three_standard3'])==3
 neg=read(OLD/'frontier.receipt.json');assert neg['exit_code']==1 and neg['actual_foreground_PID']==25248;root=read(P/'correct-frontier-metadata68/receipt.json');assert root['exit_code']==0 and root['actual_foreground_pid']==16712 and root['terminal_closed']
 save('corrected-commit.review.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,parent=BASE,old_native_closed131=pin(OLD/'lease.final.json'),old_whole_logical_run_sha256=r['run_sha256'],old_complete_named_RAW=l['named_complete_RAW_review'],old_required_gate_negative_preserved=neg,old_gate_obstruction_resolved_only_after_fresh_gate=True,finite_correction=c,exact5_field_changes=True,canonical_commit_delta=canonical,total_commit_paths=len(changed),other_paths_classified='Retained old native obstruction and exact process correction evidence only; no second mathematical or publication delta.',exact_parent_Git_equality=eq,current_to_old_frozen_map=current,source_math_schema_blind_all_unchanged=True,reused_focused3950=focused,no_new_compiler_needed='Only five process fields changed; all three Lean/toolchain/manifest exact RAW identical to accepted independent compilers and SCI68 focused3950.',generic_leaf_remains_canonical_reusable=True,same_PBPS_route_transitive_Test_not_second_route=True,no_wrapper_or_new_source_assumption=True,remaining_truth_boundary=v['truth_boundary'],full_Exposition=False,PURIFIED=False,whole_paper=False,Goal=False));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),old_closed_files=131,finite_fields=5,Git_equal_rows=len(eq)-1)))
def command(label,args):
 with (O/(label+'.stdout.log')).open('wb') as out,(O/(label+'.stderr.log')).open('wb') as err:
  start=now();p=subprocess.Popen(args,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(event='FOREGROUND_START',label=label,actual_PID=p.pid)),flush=True);code=p.wait()
 r=dict(label=label,command=args,actual_foreground_PID=p.pid,parent_PID=os.getpid(),started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(O/(label+'.stdout.log')),stderr=pin(O/(label+'.stderr.log')));save(label+'.receipt.json',r);return r
def gates():
 stable();rs=[]
 for label,args in [('frontier',['tools/astis_frontier_cells.py','check']),('publication',['tools/astis_publication.py','check','--base',BASE,'--ci']),('contributor',['tools/astis_contributor_contract.py','check','--base',BASE,'--ci']),('semantic',['tools/astis_semantic_roundtrip.py','check'])]:
  r=command(label,[PY,'-B','-X','utf8',*args]);rs.append(r);assert r['exit_code']==0,('required gate failure',label)
 from tools import astis_publication as pub
 pub.check_advance(NAMES[:2],reviewed=True);stable();save('gates.result.json',dict(status='PASS',checked_commit=SCI,parent=BASE,results=rs,reviewed_check_advance=dict(actual_PID=os.getpid(),reviewed=True,declarations=NAMES[:2],result='PASS'),reused_science_focused3950=True,separate_Test_consumer=True,no_aggregate_site_claim=True));print(json.dumps(dict(status='PASS',actual_PID=os.getpid(),gates=5)))
def accept():
 stable();assert get('corrected-commit.review.json')['status']==get('gates.result.json')['status']=='PASS'
 from tools import astis_advance as adv
 item=adv.current_advances()[SAU];assert item['state']=='PROVED_LOCAL' and item['owner_id']!=ACTOR;pr=read(P/'proved-local.json');assert pr['lean_declarations']==pr['publication_declarations']==NAMES[:2] and pr['genuine_compiled_source_consumers']==NAMES[2:] and pr['conceptual_mirror_audit']['status']=='none-found'
 save('verification-verdict.json',dict(status='ACCEPTED_EXACT_SCI68B',actor=ACTOR,actual_PID=os.getpid(),verified_commit=SCI,parent=BASE,advance_id=SAU,owner_id=item['owner_id'],corrected_commit_review=get('corrected-commit.review.json'),gate=get('gates.result.json'),production_declarations=NAMES[:2],separately_source_reviewed_genuine_Test=NAMES[2],source_audit=pin(OLD/'source-bindings.result.json'),fake_closure_scan=pin(OLD/'fake-closure-scan.json'),focused3950=pin(OLD/'focused.result.json'),truth_boundary=pr['truth_boundary'],same_route_classification_corrected=True,old_required_frontier_negative_preserved=True,remaining=['B21/B2H1/B4/dynamics/main','invariance/nonexplosion/errors/caps/cost/actual-input composition','serialized aggregate/reader acceptance','S,T alias exposition debt','remoteCI/main/live/fullExposition/PURIFIED/wholepaper/Goal'],full_Exposition=False,PURIFIED=False,Goal=False));print(json.dumps(dict(status='ACCEPTED_EXACT_SCI68B',actual_PID=os.getpid(),owner=item['owner_id'],verifier=ACTOR)))
def transition():
 stable();v=get('verification-verdict.json');assert v['status']=='ACCEPTED_EXACT_SCI68B';before=ledgerpin();initial=get('ledger.before.pin.json');assert before['raw_bytes']==initial['raw_bytes'] and before['raw_sha256']==initial['raw_sha256']
 from tools import astis_advance as adv
 e=dict(verifier_id=ACTOR,verified_commit=SCI,gate=dict(corrected_commit_review=pin(O/'corrected-commit.review.json'),fresh_required_gates=pin(O/'gates.result.json'),unchanged_science_focused3950=pin(OLD/'focused.result.json'),reviewed_two_production_declarations=True,scope='Exact SCI68B independent corrected-commit acceptance; aggregate/reader pending'),source_audit=dict(artifact=pin(OLD/'source-bindings.result.json'),native_source_whole_run=read(P/'root.source68.adoption.json')['native_whole_logical_run_sha256'],all21slots_15deltas_preserved=True,source_admission_unchanged=True,separate_genuine_Test=True),fake_closure_scan=dict(status='PASS',hits=0,private_math_providers=0,artifact=pin(OLD/'fake-closure-scan.json'),exact_Git_RAW_unchanged=True),publication_declarations=NAMES[:2],native_independent_verdict_path=(O/'verification-verdict.json').relative_to(ROOT).as_posix(),prior_exact_science_commit=BASE,prior_required_gate_obstruction_retained=pin(OLD/'frontier.receipt.json'),remaining_boundary=v['truth_boundary'])
 adv.transition_advance(SAU,'VERIFIED',worker_id=ACTOR,modes=['independent-exact-corrected-commit-verification'],evidence=e)
 b=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert sha(b[:before['raw_bytes']])==before['raw_sha256'];tail=b[before['raw_bytes']:];assert len(tail.splitlines())==1;event=json.loads(tail);assert event['advance_id']==SAU and event['evidence']['verifier_id']==ACTOR and event['evidence']['verified_commit']==SCI
 (O/'ledger.VERIFIED.append.exactraw.jsonl').write_bytes(tail);after=ledgerpin();save('ledger.after.pin.json',after);save('transition.receipt.json',dict(status='VERIFIED_BY_NONOWNER',actual_transition_PID=os.getpid(),verified_commit=SCI,parent=BASE,actor=ACTOR,before=before,after=after,append_RAW=pin(O/'ledger.VERIFIED.append.exactraw.jsonl'),one_append=True,historical_prefix_unchanged=True))
 target=P/'verified.json';assert not target.exists();ver=dict(status='VERIFIED',advance_id=SAU,verified_commit=SCI,prior_exact_science_commit=BASE,verifier_id=ACTOR,owner_id=v['owner_id'],actual_transition_PID=os.getpid(),evidence_scope=O.relative_to(ROOT).as_posix(),gate='Exact5 metadata correction; reused unchanged focused3950/standard3/math/source/fakeclosure; fresh frontier/publication-reviewed/contributor/semantic',source_audits=['ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound','ASTIS-RT-20261009-PBPSSharpCorrectorEnergy'],production_declarations=NAMES[:2],separately_source_reviewed_genuine_Test=NAMES[2],truth_boundary=v['truth_boundary'],ledger_before={k:before[k] for k in ['raw_bytes','raw_sha256']},ledger_after={k:after[k] for k in ['raw_bytes','raw_sha256']},old_obstruction_preserved=True,aggregate_integration=False,full_Exposition=False,PURIFIED=False,remoteCI=False,main_live=False,Goal=False);target.write_bytes((json.dumps(ver,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode());save('verified.shared-output.pin.json',pin(target));print(json.dumps(dict(status='VERIFIED_BY_NONOWNER',actual_PID=os.getpid(),verified_commit=SCI)))
def finalchecks():
 stable();assert get('transition.receipt.json')['status']=='VERIFIED_BY_NONOWNER';checkpin(get('verified.shared-output.pin.json'));q=get('ledger.after.pin.json');b=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert len(b)>=q['raw_bytes'] and sha(b[:q['raw_bytes']])==q['raw_sha256']
if __name__=='__main__':
 mode=sys.argv[1]
 try:globals()[mode]()
 except Exception as e:
  if not(O/'lease.final.json').exists():save((sys.argv[2] if len(sys.argv)>2 else mode)+'.failure.json',dict(actual_PID=os.getpid(),utc=now(),error=repr(e),traceback=traceback.format_exc()))
  raise
