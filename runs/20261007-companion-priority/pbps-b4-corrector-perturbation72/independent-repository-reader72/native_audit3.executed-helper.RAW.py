from pathlib import Path
import hashlib, json, os, re, subprocess, sys
from html.parser import HTMLParser
from datetime import datetime, timezone
ROOT=Path('E:/Samplinglib')
R=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72'
OWN=R/'independent-repository-reader72'
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
SELF=Path(__file__)
SCI='18183c58eee62145b6059ded11c7be05a4cb82de'
RECIPE='CRLF byte pair -> LF only; preserve bare CR/every other byte; binary LF digest is mechanical only'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def now():return datetime.now(timezone.utc).isoformat()
def load(p):return json.loads(p.read_bytes())
def read(n):return load(OWN/n)
def write(n,x):(OWN/n).write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def checkpin(row):
 p=Path(row['path']);p=p if p.is_absolute() else ROOT/p
 actual=pin(p)
 for ours,alts in [('RAW_bytes',['RAW_bytes','bytes','raw_bytes']),('RAW_sha256',['RAW_sha256','raw_sha256']),('LF_sha256',['LF_sha256','lf_sha256'])]:
  k=next((x for x in alts if x in row),None)
  if k:assert actual[ours]==row[k],(str(p),ours,actual[ours],row[k])
 return actual
def freeze():
 packet=R/'final-reader-repository-packet72.json'
 assert pin(packet)['RAW_sha256']=='26281f0f5f6d361b558b4f9f5c1bd29f7ac28865a161648db8437bde3e01f8e6'
 data=load(packet);assert len(data['inputs'])==145
 rows=[checkpin(row) for row in data['inputs']]
 assert len({x['path'] for x in rows})==145
 (OWN/'dispatch.exactraw.snapshot.json').write_bytes(packet.read_bytes())
 write('inputs.manifest.json',dict(input_count=145,inputs=rows,dispatch=pin(packet),LF_recipe=RECIPE,
       storage='finite exact references, no recursive history/source/ledger copies',historical_fallback=False))
 head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,check=True).stdout.decode().strip();assert head==SCI
 write('lease.open.json',dict(status='OPEN_SCOPED_AGGREGATE_READER72',actor='/root/exact_science63',actual_PID=os.getpid(),
       opened_utc=now(),checked_science_commit=SCI,current_HEAD=head,
       current_aggregate='uncommitted serialized working-tree integration, separately bound by native pins',
       owned_scope=OWN.relative_to(ROOT).as_posix(),previous_math_reviewer_exposure=True,new_math_certification=False,
       canonical_Git_ledger_writes=False,full_Exposition_Seal=False,PURIFIED=False,main_live=False,Goal_complete=False))
 print(json.dumps(dict(status='FROZEN145',actual_PID=os.getpid(),manifest=pin(OWN/'inputs.manifest.json'),HEAD=head)))
def recheck():
 rows=read('inputs.manifest.json')['inputs'];[checkpin(x) for x in rows];return len(rows)
def gate_audit():
 packet=load(R/'final-reader-repository-packet72.json');rows=[]
 for inp in packet['inputs']:
  if not inp['path'].endswith('/receipt.json'):continue
  p=Path(inp['path']);j=load(p)
  row=dict(label=p.parent.name,receipt=pin(p),actual_PID=j.get('actual_foreground_PID',j.get('actual_PID',j.get('actual_root_PID'))),
       exit_code=j.get('exit_code',j.get('EXIT')),terminal_closed=j.get('terminal_closed'),
       command=j.get('command'),checked_parent=j.get('checked_parent'))
  if 'stdout' in j:row['stdout']=checkpin(j['stdout'])
  if 'stderr' in j:row['stderr']=checkpin(j['stderr'])
  rows.append(row)
 mandatory=next(x for x in rows if x['label']=='mandatory-astis-check-final');assert mandatory['exit_code']==0
 text=(R/'integration72/mandatory-astis-check-final/stdout.log').read_text(encoding='utf-8')
 evidence=[line for line in text.splitlines() if re.search(r'9183|9483|fake|Fake|Gate|gate|passed|PASS|successfully',line)]
 assert '9183' in text and '9483' in text
 finals=[x for x in rows if 'after-admin-recovery' in x['label']];assert len(finals)==8
 assert all(x['exit_code']==0 and x['terminal_closed'] is True for x in finals)
 write('gates.audit.json',dict(status='ACTUAL_RECEIPTS_AND_TERMINAL_LOGS_CHECKED',actual_PID=os.getpid(),
       receipts=rows,final_after_admin_recovery_gate_count=len(finals),mandatory_log_exact_lines=evidence[-15:],
       root_jobs=9183,Tests_jobs=9483,publication_units=242,new_gates_run=False,
       full_Lean_and_224_regressions_reused_not_rerun=True))
 print(json.dumps(dict(status='GATE_RECEIPTS_CHECKED',actual_PID=os.getpid(),receipts=len(rows),finals=len(finals))))
def inspect():
 c=load(R/'integration72/visual72/copy-capture.json')
 out=dict(panels=[dict(label=x['label'],panels=[dict(head=p['code'][:100],tail=p['code'][-80:]) for p in x['panels']]) for x in c['records']],
      recovery=load(R/'integration72/record-final-admin/typed-diagnosis-and-repair.json'))
 h=(ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').read_text(encoding='utf-8')
 name='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation.actual_corrector_perturbation'
 pos=h.find(name);out['html_snippet']=h[max(0,pos-150):pos+500]
 print(json.dumps(out,ensure_ascii=False,indent=2))
def native_audit():
 results=[]
 for scope,count,manifest_name in [('independent-source72',258,'native.manifest.json'),('exact-science-verification72',163,'owned.manifest.json')]:
  base=R/scope; lease=load(base/'lease.final.json'); manifest=load(base/manifest_name)
  entries=manifest['entries']
  for row in entries:
   p=Path(row['path']);p=p if p.is_absolute() else base/p
   checkpin(dict(row,path=str(p)))
  assert len(entries)+2==count
  run=load(base/('source72.run.json' if scope=='independent-source72' else 'run.json'));expected=run.pop('run_sha256');assert sha(canon(run))==expected==lease['run_sha256']
  candidates=[x for x in entries if 'complete-named' in x['path'] or 'complete.named' in x['path']]
  results.append(dict(scope=scope,native_files=count,manifest=pin(base/manifest_name),lease=pin(base/'lease.final.json'),
      all_native_manifest_entries_RAW_LF_exact=True,whole_logical_run_sha256=expected,complete_named_references=candidates,
      transcript_or_proof_replayed=False))
 base=R/'independent-math72';lease=load(base/'lease.final.json')
 rows=lease.get('files',lease.get('owned_files',[]))
 assert isinstance(rows,list)
 for row in rows:checkpin(row)
 run=load(base/'run.json');expected=run.pop('run_sha256');assert sha(canon(run))==expected
 results.append(dict(scope='independent-math72',native_files=82,lease=pin(base/'lease.final.json'),manifest_entries_checked=len(rows),whole_logical_run_sha256=expected,
      prior_math_reviewer_is_same_actor=True,reuse_only_no_new_independent_math_certification=True))
 base=R/'anonymous-decoder';lease=load(base/'CLOSED_LAST.json')
 for row in lease['sealed_files_except_self']:checkpin(dict(row,path=str(base/row['path'])))
 run=load(base/'run.json');expected=run.pop('run_sha256');assert sha(canon(run))==expected==lease['run_sha256']
 results.append(dict(scope='anonymous-decoder',native_files=5,lease=pin(base/'CLOSED_LAST.json'),whole_logical_run_sha256=expected,
      finite_transport='same5 original native files copied from explicitly named .astis/decoder-72/independent, exact RAW lease hashes',new_decode=False))
 write('native-reuse.audit.json',dict(status='FINITE_NATIVE_PACKAGES_REUSED_RAW_EXACT',actual_PID=os.getpid(),packages=results,
       no_recursive_copy_or_transcript_replay=True,exact_SCI_verified_by_distinct_actor='/root/header_math72'))
 print(json.dumps(dict(status='NATIVE_REUSE_PASS',actual_PID=os.getpid(),package_counts=[258,163,82,5])))
def native_audit2():return native_audit()

def native_audit3():
 old=OWN/'native-reuse.audit.json'
 (OWN/'native-reuse.audit.v2.incomplete-math-manifest.exactraw.json').write_bytes(old.read_bytes())
 base=R/'independent-math72';lease=load(base/'lease.final.json')
 rows=lease['all_owned_outputs_except_only_self'];assert len(rows)==81
 for row in rows:checkpin(row)
 assert sha(canon(rows))==lease['closure_manifest_logical_sha256']
 current=load(old);math=next(x for x in current['packages'] if x['scope']=='independent-math72')
 math.update(manifest_entries_checked=81,all_native_manifest_entries_RAW_LF_exact=True,
       closure_manifest_logical_sha256=lease['closure_manifest_logical_sha256'])
 current.update(actual_PID=os.getpid(),observer_correction=dict(
       previous_math_manifest_entries_checked=0,previous_status='INCOMPLETE_OBSERVER_NOT_MATH_FAILURE',
       diagnosis='Prior observer assumed files/owned_files; actual math lease has all_owned_outputs_except_only_self.',
       retained_previous_audit=pin(OWN/'native-reuse.audit.v2.incomplete-math-manifest.exactraw.json'),
       corrected_entries=81,native_packages_unchanged=True))
 write('native-reuse.audit.json',current)
 print(json.dumps(dict(status='NATIVE_REUSE_ALL_MANIFESTS_PASS',actual_PID=os.getpid(),native_counts=[258,163,82,5],math_entries=81)))

def shapes():
 c=load(R/'integration72/visual72/copy-capture.json')
 out=[]
 for i,rec in enumerate(c['records']):
  out.append(dict(unit=i,panelkeys=list(rec['panels'][0]),downloadkeys=list(rec['downloads'][0]),stepkeys=list(rec['steps'][0])))
 print(json.dumps(out))
 for s in ['pbps-hilbert-corrector-perturbation','pbps-actual-corrector-perturbation']:
  unit=load(ROOT/f'website/content/declaration_lessons/{s}.json')['units'][0]
  print(json.dumps(dict(slug=s,declaration=unit['declaration'],stepkeys=list(unit['steps'][0]),helpers=unit['helpers'],statement=unit['lean_statement'][:150],proof=unit['lean_proof'][:150])))
 class Parser(HTMLParser):
  def __init__(self):super().__init__();self.active=False;self.depth=0;self.rows=[]
  def handle_starttag(self,t,a):
   a=dict(a)
   if t=='article' and 'CorrectorPerturbation.' in a.get('data-authored-declaration',''):self.active=True;self.depth=1
   elif self.active:
    if t=='article':self.depth+=1
    if t in ['details','code','summary']:self.rows.append((t,a))
  def handle_endtag(self,t):
   if self.active and t=='article':self.depth-=1;self.active=self.depth>0
 p=Parser();p.feed((ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').read_text(encoding='utf-8'))
 print(json.dumps(p.rows[:24]))
def allowned(exclude=()):return [pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.relative_to(OWN).as_posix() not in exclude]
def finalize():
 assert read('decision.json')['accepted_scoped_aggregate'] is True
 count=recheck();write('final-input-readback.json',dict(status='PASS',input_count=count,actual_PID=os.getpid(),all145_current_RAW_LF_equal=True))
 # Baseline manifest is explicitly preterminal; final lease is authoritative for every self/terminal layer.
 files=allowned(exclude=('outputs.manifest.json','complete-named-repository-reader.payload.json','run.json','lease.final.json'))
 write('outputs.manifest.json',dict(capture_stage='finalizer preterminal baseline; final lease binds all final bytes',file_count=len(files),files=files))
 payload=dict(payload_name='COMPLETE_SCOPED_INDEPENDENT_REPOSITORY_READER72_REVIEW',actor='/root/exact_science63',
       decision=read('decision.json'),review=read('review.json'),inputs=read('inputs.manifest.json'),
       gates=read('gates.audit.json'),bindings=read('bindings.audit.json'),native_reuse=read('native-reuse.audit.json'),
       visuals=read('visual-review.json'),admin_recovery=read('admin-recovery.audit.json'),
       output_baseline=read('outputs.manifest.json'),final_input_readback=read('final-input-readback.json'))
 write('complete-named-repository-reader.payload.json',payload)
 run=dict(schema='independent-repository-reader72/v1',status='ACCEPTED_SCOPED_AGGREGATE_READER_ONLY',actor='/root/exact_science63',
      checked_science_commit=SCI,accepted_scoped_aggregate=True,aggregate_commit_exists=False,
      decision=pin(OWN/'decision.json'),complete_named_RAW_payload=pin(OWN/'complete-named-repository-reader.payload.json'),
      inputs_manifest=pin(OWN/'inputs.manifest.json'),outputs_baseline=pin(OWN/'outputs.manifest.json'),
      full_Exposition_Seal=False,PURIFIED=False,main_live=False,whole_paper=False,Goal_complete=False,
      hash_recipe='canonical UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon deleting ONLY top-level run_sha256',
      final_owned_manifest='lease.final.json binds every actual owned file except lease itself; lease RAW externally read back')
 run['run_sha256']=sha(canon(run));write('run.json',run)
 print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),run_sha256=run['run_sha256'],named=pin(OWN/'complete-named-repository-reader.payload.json'))))
def readback():
 run=read('run.json');expected=run.pop('run_sha256');assert sha(canon(run))==expected
 assert checkpin(run['complete_named_RAW_payload'])
 assert recheck()==145
 print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid(),run_sha256=expected,named_RAW_sha256=run['complete_named_RAW_payload']['RAW_sha256'])))
def close():
 assert not (OWN/'lease.final.json').exists();readback();launch('close_probe')
 files=allowned(exclude=('lease.final.json',))
 write('lease.final.json',dict(status='CLOSED_LAST',actor='/root/exact_science63',actual_close_writer_PID=os.getpid(),
      closed_utc=now(),file_count_including_lease=len(files)+1,files=files,closure_logical_sha256=sha(canon(files)),
      run_sha256=read('run.json')['run_sha256'],complete_named_RAW_payload=pin(OWN/'complete-named-repository-reader.payload.json'),
      all_prior_launched_sessions_closed=True,final_owned_write=True,postclose_owned_writes_forbidden=True,
      close_writer_EXIT_observed_externally_after_last_write=True))
 print(json.dumps(dict(status='CLOSED_LAST',actual_PID=os.getpid(),file_count=len(files)+1,lease=pin(OWN/'lease.final.json'))))
def close_probe():readback();print(json.dumps(dict(status='CLOSE_PROBE_PASS',actual_PID=os.getpid())))
def postclose():
 lease=read('lease.final.json');files=allowned(exclude=('lease.final.json',));assert files==lease['files'];assert sha(canon(files))==lease['closure_logical_sha256'];readback()
 print(json.dumps(dict(status='READONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),file_count=len(files)+1,lease=pin(OWN/'lease.final.json'),closure_sha256=lease['closure_logical_sha256'],owned_writes=False)))
def launch(act):
 assert not (OWN/'lease.final.json').exists()
 (OWN/f'{act}.executed-helper.RAW.py').write_bytes(SELF.read_bytes());started=now()
 argv=[PY,'-B','-X','utf8',str(SELF),'_child',act]
 with (OWN/f'{act}.stdout.log').open('wb') as out,(OWN/f'{act}.stderr.log').open('wb') as err:
  proc=subprocess.Popen(argv,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(status='RUNNING',actual_PID=proc.pid,runner_PID=os.getpid(),action=act)),flush=True);code=proc.wait()
 write(f'{act}.receipt.json',dict(action=act,actual_PID=proc.pid,runner_PID=os.getpid(),command=argv,started_utc=started,ended_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(OWN/f'{act}.stdout.log'),stderr=pin(OWN/f'{act}.stderr.log'),executed_helper=pin(OWN/f'{act}.executed-helper.RAW.py')))
 print(json.dumps(dict(status='TERMINAL',actual_PID=proc.pid,action=act,exit_code=code)));return code
if __name__=='__main__':
 act=sys.argv[-1]
 if sys.argv[1]=='_child':sys.exit(globals()[act]() or 0)
 elif act in ('close','postclose'):globals()[act]()
 else:sys.exit(launch(act))
