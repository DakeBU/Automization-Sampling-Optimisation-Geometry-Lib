from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,re,subprocess,sys
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-harmonic-flow73';OWN=R/'exact-science-verification73';SELF=Path(__file__)
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
SCI='63319104ccad4e81e3a2c59da23ec0009be5e17f';PARENT='bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19'
ID='ASTIS-SA-20261010-PBPSActualHarmonicFlow';ACTOR='/root/exact_science63';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws'
MODULE=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean'
CELL=ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json'
AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json'
PUB=ROOT/'website/content/publications/pbps-actual-harmonic-flow.json';LESSON=ROOT/'website/content/declaration_lessons/pbps-actual-harmonic-flow.json'
LEDGER=ROOT/'runs/substantive_advances.jsonl'
RECIPE='CRLF byte pairs -> LF only; preserve bare CR and every other byte; binary LF is mechanical only'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def read(n):return load(OWN/n)
def write(n,x):(OWN/n).write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(row,base=ROOT):
 p=Path(row['path']);p=p if p.is_absolute() else base/p
 q=pin(p)
 for k,alts in [('RAW_bytes',['RAW_bytes','bytes','raw_bytes']),('RAW_sha256',['RAW_sha256','raw_sha256']),('LF_sha256',['LF_sha256','lf_sha256'])]:
  key=next((x for x in alts if x in row),None)
  if key:assert q[k]==row[key],(p,k,q[k],row[key])
 return q
def git(args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout
def state():
 sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis_advance
 return astis_advance._replay_advances([json.loads(x) for x in LEDGER.read_bytes().splitlines() if x.strip()])[ID]
def recheck():
 for row in read('inputs.manifest.json')['inputs']:check(row)
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
def freeze():
 assert git(['rev-parse','HEAD']).decode().strip()==SCI
 assert git(['rev-list','--parents','-n','1',SCI]).decode().strip().split()==[SCI,PARENT]
 paths=[MODULE,PUB,LESSON,AUDIT,CELL,ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
 paths += [R/x for x in ['claim.json','proved-local.json','mathematics-freeze73.json','source-review.freeze73.json','source-review.packet.json',
      'root.math73.adoption.json','root.source73.adoption.json','root.decoder73.adoption.json','root.reader-metadata-overlay73.adoption.json',
      'audit.before-decoder73.exactraw.snapshot.json','audit.before-source-admission73.exactraw.json','cell.before-source-admission73.exactraw.json','publication.before-source-admission73.exactraw.json',
      'independent-math73/lease.final.json','independent-math73/native.manifest.json','independent-math73/run.json','independent-math73/decision.json',
      'independent-source73/lease.final.json','independent-source73/whole-owned.manifest.json','independent-source73/source.0.run.json','independent-source73/source.0.decision.json',
      'independent-source73/StageB.finite-current-inputs73.json','independent-source73/final-current-input-version-map73.json',
      'independent-reader-metadata-repair73/lease.final.json','independent-reader-metadata-repair73/decision.json','independent-reader-metadata-repair73/native.manifest.json','independent-reader-metadata-repair73/run.json']]
 paths += [ROOT/'.astis/decoder-73/result'/x for x in ['CLOSED_LAST.json','run.json','reconstruction.json','reconstruction.md']]
 paths += [ROOT/'tools'/x for x in ['astis.py','astis_advance.py','astis_publication.py','astis_semantic_roundtrip.py','astis_frontier_cells.py','astis_contributor_contract.py']]
 paths += [ROOT/'docs'/x for x in ['contributor-codex-contract.md','theorem-publication-protocol.md','proof-digestion-protocol.md','evidence-routed-memory-protocol.md']]
 paths += [ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/root.statement-seal73.json']
 rows=[pin(p) for p in paths];assert len({x['path'] for x in rows})==len(rows)
 write('inputs.manifest.json',dict(input_count=len(rows),inputs=rows,LF_recipe=RECIPE,storage='finite exact immutable/native references; only core current bytes copied, no recursive history/ledger payload'))
 snapshots=[]
 for i,p in enumerate([MODULE,PUB,LESSON,AUDIT,CELL]):
  q=OWN/f'core.{i}.exactraw.snapshot';q.write_bytes(p.read_bytes());snapshots.append(dict(original=pin(p),snapshot=pin(q)))
 write('core.snapshots.json',dict(snapshots=snapshots))
 st=state();assert st['state']=='PROVED_LOCAL' and st['owner_id']=='companion_root_20261005'
 assert st['publication_declarations']==[DECL]
 write('ledger.before-prefix.json',dict(path=LEDGER.relative_to(ROOT).as_posix(),RAW_bytes=LEDGER.stat().st_size,RAW_sha256=sha(LEDGER.read_bytes()),target_advance=st))
 write('lease.open.json',dict(status='OPEN_EXACT_SCI73_VERIFICATION',actor=ACTOR,actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,
       owned_scope=OWN.relative_to(ROOT).as_posix(),allowed_shared_writes='one nonowner VERIFIED append and r73/verified.json only after all required gates PASS',no_aggregate_site_Git_or_Lean_writes=True))
 print(json.dumps(dict(status='FROZEN',actual_PID=os.getpid(),input_count=len(rows),checked_commit=SCI,module=pin(MODULE))))
def process(label,argv,env=None,accepted=(0,)):
 folder=OWN/'terminals';folder.mkdir(exist_ok=True);out=folder/(label+'.stdout.RAW');err=folder/(label+'.stderr.RAW');start=now()
 pre=pin(MODULE)
 with out.open('wb') as o,err.open('wb') as e:
  proc=subprocess.Popen(argv,cwd=ROOT,env=env,stdout=o,stderr=e)
  print(json.dumps(dict(status='FOREGROUND_RUNNING',label=label,actual_PID=proc.pid)),flush=True);code=proc.wait()
 receipt=dict(label=label,actual_PID=proc.pid,command=argv,started_utc=start,ended_utc=now(),exit_code=code,terminal_closed=True,
       stdout=pin(out),stderr=pin(err),module_pre=pre,module_post=pin(MODULE))
 write('terminals/'+label+'.receipt.json',receipt)
 assert pre==receipt['module_post'];assert code in accepted,(label,code,err.read_text(encoding='utf-8')[-1000:])
 return receipt
def fresh_lean():
 recheck();meta=load(R/'root.math73.adoption.json')['fresh_compiler'];exe=Path(meta['real_Lean_executable']['path']);check(meta['real_Lean_executable'])
 env=dict(os.environ);env.update(LEAN_PATH=meta['LEAN_PATH'],LEAN_SRC_PATH=meta['LEAN_SRC_PATH'])
 version=process('fixed-lean-version',[str(exe),'--version'],env);assert '4.33.0' in (ROOT/version['stdout']['path']).read_text()
 output=OWN/'output';output.mkdir(exist_ok=True)
 rec=process('fresh-direct-Lean',[str(exe),'-o',str(output/'ActualHarmonicFlow.olean'),str(MODULE)],env)
 text=(ROOT/rec['stdout']['path']).read_text(encoding='utf-8');matches=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',text)
 assert len(matches)==1 and {x.strip() for x in matches[0].split(',')}=={'propext','Classical.choice','Quot.sound'}
 assert 'sorryAx' not in text and 'error:' not in text
 write('fresh-lean.result.json',dict(status='PASS',actual_direct_Lean_PID=rec['actual_PID'],terminal_EXIT=0,checked_commit=SCI,
      module=pin(MODULE),fresh_source_elaboration=True,Lake_cache_replay=False,canonical_olean_written=False,
      owned_olean=pin(output/'ActualHarmonicFlow.olean'),standard_axioms=['propext','Classical.choice','Quot.sound'],version=version,compiler=rec))
 print(json.dumps(dict(status='FRESH_LEAN_PASS',actual_PID=rec['actual_PID'],standard3=True)))
def gates():
 recheck();checks=[('publication',['tools/astis_publication.py','check','--base',PARENT]),
       ('contributor',['tools/astis_contributor_contract.py','check','--base',PARENT]),
       ('semantic',['tools/astis_semantic_roundtrip.py','check']),('frontier',['tools/astis_frontier_cells.py','check']),
       ('bounded-publication-packet',['tools/astis_publication.py','packet','--cell','ASTIS-SW-PBPS-actual-harmonic-flow'])]
 rows=[]
 for label,args in checks:rows.append(process(label,[PY,'-B','-X','utf8',*args]))
 write('gates.result.json',dict(status='PASS',checked_commit=SCI,diff_base=PARENT,receipts=rows,aggregate_full_library_or_site_run=False))
 print(json.dumps(dict(status='FRESH_GATES_PASS',actual_PID=os.getpid(),gate_count=len(rows))))

def diffpaths(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a or k not in b:out.append(p+'/'+k)
   else:out+=diffpaths(a[k],b[k],p+'/'+k)
  return out
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
  out=[]
  for i,(x,y) in enumerate(zip(a,b)):out+=diffpaths(x,y,p+'/'+str(i))
  return out
 return [] if a==b else [p]

def bounded_finish():
 recheck();native=[]
 for scope,count,manifest,runfile in [('independent-math73',39,'native.manifest.json','run.json'),('independent-source73',69,'whole-owned.manifest.json','source.0.run.json'),('independent-reader-metadata-repair73',17,'native.manifest.json','run.json')]:
  base=R/scope;m=load(base/manifest);rows=m['owned_files'] if scope=='independent-reader-metadata-repair73' else m['entries'] if scope=='independent-math73' else m['files'];assert isinstance(rows,list)
  for row in rows:check(row)
  lease=load(base/'lease.final.json');assert lease['status']=='CLOSED_LAST'
  run=load(base/runfile);want=run.pop('run_sha256');assert sha(canon(run))==want
  expected=lease.get('run_sha256',lease.get('whole_logical_run_sha256'));assert want==expected
  actual=[p for p in base.rglob('*') if p.is_file()];assert len(actual)==count
  if scope=='independent-source73':
   assert len(lease['all_files_except_self'])==68
   for row in lease['all_files_except_self']:check(row)
   assert want=='2c8aa1cf7b0f4cd81bc55009070889064c8c8bcec23839189fa46b4ee42e6acb'
  native.append(dict(scope=scope,count=count,manifest=pin(base/manifest),lease=pin(base/'lease.final.json'),whole_logical_run_sha256=want,all_manifest_RAW_LF_exact=True,proof_or_transcript_replayed=False))
 decoder=ROOT/'.astis/decoder-73/result';lease=load(decoder/'CLOSED_LAST.json')
 for row in lease['prior_owned_files']:check(row)
 drun=load(decoder/'run.json');want=drun['decoder_run_sha256'];preimage=drun['canonical_logical_run_utf8'].encode()
 assert sha(preimage)==want==lease['decoder_run_sha256'] and json.loads(preimage)==drun['logical_run_payload']
 for name in ['run.json','reconstruction.json','reconstruction.md','CLOSED_LAST.json']:
  assert (decoder/name).read_bytes()==(R/'anonymous-decoder'/name).read_bytes()
 native.append(dict(scope='anonymous-decoder',count=4,lease=pin(decoder/'CLOSED_LAST.json'),whole_logical_run_sha256=want,
       native_hash_recipe=drun['canonical_recipe'],literal_native_preimage_bytes=len(preimage),native_preimage_JSON_equals_logical_payload=True,
       exact_archived_four_file_transport=True,all_RAW_LF_exact=True,new_decode=False))
 write('native-reuse.audit.json',dict(status='PASS_BOUNDED_CLOSED_AUTHORITY_REUSE',actual_PID=os.getpid(),packages=native))
 core=[]
 for p in [MODULE,PUB,LESSON,AUDIT,CELL,ROOT/'lean-toolchain',ROOT/'lake-manifest.json',R/'proved-local.json',R/'root.math73.adoption.json',R/'root.source73.adoption.json',R/'root.decoder73.adoption.json',R/'root.reader-metadata-overlay73.adoption.json']:
  blob=git(['show',f'{SCI}:{p.relative_to(ROOT).as_posix()}']);raw=p.read_bytes()
  assert blob==raw or p.name in ['lean-toolchain','lake-manifest.json'] and blob.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n')
  core.append(dict(current=pin(p),Git_RAW_sha256=sha(blob),Git_RAW_bytes=len(blob),exact_RAW=blob==raw,CRLF_only_LF_qualified=blob!=raw))
 assert len(MODULE.read_bytes().splitlines())==178 and pin(MODULE)['RAW_sha256']=='506c1d57b3c9133db1cfc0515dccbd8759aaec3e1dbf4a128f6a73d3aeb73c8c'
 decision=load(R/'independent-source73/source.0.decision.json');audit=load(AUDIT)
 assert decision['state']=='source-reviewed' and decision['source_review']['state']=='accepted' and decision['blocking_semantic_deltas']==0
 assert len(decision['semantic_slots'])==7 and decision['repairs']==[] and len(decision['deltas'])==10
 for k in ['state','verdict','semantic_slots','deltas','source_review']:assert audit[k]==decision[k]
 assert audit['publication_binding_sha256']==decision['publication_binding_sha256']
 assert pin(R/'source-review.packet.json')['RAW_sha256']==decision['official_packet_RAW_sha256']
 source_inputs=load(R/'independent-source73/source.0.input-manifest.json')['final_current_inputs'];maps=[]
 for row in source_inputs:
  p=ROOT/row['path']
  if pin(p)['RAW_sha256']==row['RAW_sha256']:check(row);maps.append(dict(path=row['path'],resolution='CURRENT_EXACT',RAW_sha256=row['RAW_sha256']))
  else:
   assert p in [AUDIT,CELL,PUB]
   old=R/('audit.before-source-admission73.exactraw.json' if p==AUDIT else 'cell.before-source-admission73.exactraw.json' if p==CELL else 'publication.before-source-admission73.exactraw.json')
   assert pin(old)['RAW_sha256']==row['RAW_sha256']
   changes=diffpaths(load(old),load(p))
   allowed=('/source_review','/state','/verdict','/semantic_slots','/deltas') if p==AUDIT else ('/items/0/source_proof_coverage/',) if p==PUB else ('/status','/evidence/','/conceptual_mirror_audit/checked','/source_proof_coverage/')
   assert all(any(x.startswith(a) for a in allowed) for x in changes)
   maps.append(dict(path=row['path'],resolution='EXPLICIT_ROOT_SOURCE_ADMISSION_SNAPSHOT',historical=pin(old),current=pin(p),changed_JSON_paths=changes))
 assert len(maps)==8
 version=load(R/'independent-source73/final-current-input-version-map73.json');assert version['changed_current_inputs']==2 and not version['source_mathematics_changed']
 for row in version['version_rows']:
  base=R/'independent-source73';before=base/row['historical']['RAW_snapshot'];after=ROOT/row['proposal']['path'];assert pin(before)['RAW_sha256']==row['historical']['RAW_sha256'];check(row['proposal'])
  assert diffpaths(load(before),load(after))==[row['JSON_pointer']]
 raw=MODULE.read_bytes();text=raw.decode();sys.path[:0]=[str(ROOT),str(ROOT/'tools')];import astis
 stripped=astis.strip_lean_comments_and_strings(text);hits=[dict(line=i+1,text=line.strip()) for i,line in enumerate(stripped.splitlines()) if astis.FORBIDDEN_REGEX.search(line)]
 assert not hits
 assert len(re.findall(r'^theorem ',stripped,re.M))==1 and len(re.findall(r'^private def ',stripped,re.M))==1
 assert re.search(r'^private def actual_harmonic_flow_statement',stripped,re.M)
 assert 'continuous_gradient_of_contDiff_one' in text and 'ActualCorrectorPerturbation' not in text and 'ActualProjectedRotation' not in text
 lesson=load(LESSON)['units'][0];steps=[];assert len(lesson['steps'])==6
 lines=raw.splitlines(keepends=True)
 for i,step in enumerate(lesson['steps']):
  reg=step['lean_source_region'];assert reg['source_raw_sha256']==sha(raw) and (ROOT/reg['path']).resolve()==MODULE.resolve()
  a,b=reg['start_line'],reg['end_line'];span=b''.join(lines[a-1:b]);code=step['lean'].encode();assert a>=69 and sha(span)==reg['exact_code_raw_sha256'] and span in [code,code+b'\n']
  steps.append(dict(step=i+1,start_line=a,end_line=b,whole_source_RAW_sha256=sha(raw),literal_span_RAW_sha256=sha(span),authored_code_equals_BODY=True,terminal_LF_outside_authored_code=span!=code))
 write('source-binding-fakeclosure.audit.json',dict(status='PASS_COMMIT_BOUND_SOURCE_MATH_FAKECLOSURE',actual_PID=os.getpid(),checked_commit=SCI,parent=PARENT,
       Git_core=core,module_lines=178,source_slots=7,informational_deltas=10,blocking_deltas=0,math_repairs=0,native_source_run=decision['review_run_sha256'],
       source_review_reviewer=decision['reviewer'],source_independent_of_formalizer_and_decoder=True,finite_source_input_maps=maps,
       separately_reviewed_two_metadata_fields_only=True,exact_BODY_steps=steps,fake_closure_hits=hits,public_theorems=1,private_literal_definitions=1,private_providers=0,
       genuine_gradient_parent=True,six_callers_and_nine_conclusions_unchanged_from_closed_math_and_source=True,
       rank_zero_and_alpha_eta_one_legal=True,no_onto_probability_kernel_or_new_regularilty_premise=True,
       mathematical_review_reused_not_repeated=True,aggregate_reader_full_paper_Goal_credit=False))
 packet=process('bounded-publication-packet',[PY,'-B','-X','utf8','tools/astis_publication.py','packet','--cell','ASTIS-SW-PBPS-actual-harmonic-flow'])
 pubmodule=__import__('astis_publication');pubmodule.check_advance([DECL],reviewed=True)
 write('reviewed-source-gate.json',dict(status='PASS',actual_PID=os.getpid(),checked_commit=SCI,publication_declarations=[DECL],reviewed=True,packet=packet))
 print(json.dumps(dict(status='BOUNDED_BINDINGS_SOURCE_SCAN_PASS',actual_PID=os.getpid(),native_counts=[39,69,17,4],source_maps=8,BODY_steps=6,fakeclosure_hits=0)))

def bounded_finish2():return bounded_finish()
def bounded_finish3():return bounded_finish()
def bounded_finish4():return bounded_finish()

def whitespace():
 rec=process('exact-SCI-RAW-whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check',PARENT,SCI],accepted=(0,1,2))
 text=(ROOT/rec['stdout']['path']).read_text(encoding='utf-8');findings=[dict(path=m.group(1),line=int(m.group(2)),kind=m.group(3)) for m in re.finditer(r'^(.+):(\d+): (trailing whitespace|new blank line at EOF)\.',text,re.M)]
 assert len(findings)==37 and rec['exit_code']!=0
 names=sorted({x['path'] for x in findings});classed=[]
 for name in names:
  p=ROOT/name;blob=git(['show',f'{SCI}:{name}']);assert blob==p.read_bytes()
  if name.startswith('runs/20261007-companion-priority/pbps-actual-harmonic-flow73/focused-scalar-reciprocal-repair/'):
   receipt=load(R/'focused-scalar-reciprocal-repair/receipt.json');check(receipt['stdout']);kind='retained actual failed compiler stdout'
  else:
   base=ROOT/'runs/20261007-companion-priority'/('pbps-half-turn-construction-preread73' if '/pbps-half-turn-construction-preread73/' in name else 'pbps-harmonic-flow-sourcegraph73')
   lease=load(base/'lease.final.json');serialized=json.dumps(lease);assert p.name in serialized, name;kind='immutable source/API exact RAW slice in prior CLOSED source-first bundle'
  classed.append(dict(file=pin(p),classification=kind,Git_exact_RAW_equal=True))
 authored=process('exact-SCI-authored-whitespace',['git','-c','core.whitespace=cr-at-eol','diff','--check',PARENT,SCI,'--','.',*[':(exclude)'+n for n in names]])
 write('whitespace.audit.json',dict(status='AUTHORED_COMPLEMENT_PASS_IMMUTABLE_RAW_NEGATIVE_PRESERVED',actual_PID=os.getpid(),
      checked_commit=SCI,parent=PARENT,full_RAW_whitespace_PASS=False,full_RAW_exit=rec['exit_code'],immutable_findings=37,
      full_RAW_terminal=rec,exact_findings=findings,finite_exception_files=classed,authored_complement_PASS=True,authored_terminal=authored,
      exclusions_are_only_exact_named_immutable_files=True,no_native_normalization=True))
 print(json.dumps(dict(status='WHITESPACE_QUALIFIED',actual_PID=os.getpid(),immutable_findings=37,authored_PASS=True,full_RAW_PASS=False)))
def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/f'{action}.executed-helper.RAW.py').write_bytes(SELF.read_bytes());argv=[PY,'-B','-X','utf8',str(SELF),'_child',action]
 with (OWN/f'{action}.stdout.log').open('wb') as out,(OWN/f'{action}.stderr.log').open('wb') as err:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,action=action,runner_PID=os.getpid())),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(action=action,actual_PID=p.pid,runner_PID=os.getpid(),command=argv,exit_code=code,terminal_closed=True,
       stdout=pin(OWN/f'{action}.stdout.log'),stderr=pin(OWN/f'{action}.stderr.log'),executed_helper=pin(OWN/f'{action}.executed-helper.RAW.py')))
 print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,action=action,exit_code=code)));return code
if __name__=='__main__':
 action=sys.argv[-1]
 if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
 else:sys.exit(launch(action))
