from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess, sys
ROOT=Path('E:/Samplinglib')
R=ROOT/'runs/20261007-companion-priority/pbps-b4-corrector-perturbation72'
OLD=R/'independent-repository-reader72'
OWN=R/'reader-observation-correction72'
SELF=Path(__file__)
PY='C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
SCI='18183c58eee62145b6059ded11c7be05a4cb82de'
INT='bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19'
EXACT='hAInv and hGInv are sealed explicit structural facts unused by this proof; actual consumer supplies both internally. No premise removal or addition is proposed.'
AUDIT=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSHilbertCorrectorPerturbation.json'
HTML=ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html'
PNG=R/'integration72/visual72/render-unit0-proof-6.png'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def load(p):return json.loads(p.read_bytes())
def write(n,x):(OWN/n).write_bytes(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(row):
 p=Path(row['path']);p=p if p.is_absolute() else ROOT/p
 actual=pin(p)
 for k in ['RAW_bytes','RAW_sha256','LF_sha256']:
  if k in row:assert actual[k]==row[k],(p,k)
 return actual
def files():return [pin(p) for p in sorted(OWN.rglob('*')) if p.is_file() and p.name!='lease.final.json']
def review():
 assert not (OWN/'lease.final.json').exists()
 oldlease=load(OLD/'lease.final.json');assert oldlease['status']=='CLOSED_LAST' and oldlease['file_count_including_lease']==91
 assert pin(OLD/'lease.final.json')['RAW_sha256']=='c277f63a0c7760db9a8a044c81e3aa5af1acace72f38e94444f5d98dd6ba4c24'
 for row in oldlease['files']:check(row)
 assert sha(canon(oldlease['files']))==oldlease['closure_logical_sha256']
 frozen=load(OLD/'inputs.manifest.json')['inputs']
 equality=[]
 for p in [AUDIT,HTML,PNG]:
  current=pin(p);old=next(x for x in frozen if x['path']==current['path']);check(old)
  equality.append(dict(current=current,frozen_RAW_sha256=old['RAW_sha256'],RAW_equal=True))
 paths=[OLD/n for n in ['lease.final.json','decision.json','visual-review.json','review.json','run.json',
       'complete-named-repository-reader.payload.json','inputs.manifest.json','bindings.audit.json','authority-readback.audit.json']]
 paths += [AUDIT,HTML,PNG,R/'integration72/visual72/render-unit0-proof-6.inspect.json',R/'integration72/visual72/render-capture.json']
 rows=[pin(p) for p in paths];assert len(rows)==14
 write('inputs.manifest.json',dict(input_count=14,inputs=rows,LF_recipe='CRLF byte pair -> LF only, preserve bare CR and every other byte; binary LF mechanical only',
       storage='exact finite references; no whole HTML/PNG/native history copied'))
 write('lease.open.json',dict(status='OPEN_OBSERVATION_CORRECTION_ONLY',actor='/root/exact_science63',actual_PID=os.getpid(),owned_scope=OWN.relative_to(ROOT).as_posix(),canonical_or_closed_writes=False))
 head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,check=True).stdout.decode().strip();assert head==INT
 raw=AUDIT.read_bytes();text=raw.decode();assert text.count(EXACT)==1
 a=raw.index(EXACT.encode());line=raw[:a].count(b'\n')+1;assert line==292
 pointer=[]
 def walk(x,p=''):
  if isinstance(x,dict):
   for k,v in x.items():walk(v,p+'/'+k)
  elif isinstance(x,list):
   for i,v in enumerate(x):walk(v,p+'/'+str(i))
  elif x==EXACT:pointer.append(p)
 walk(load(AUDIT));assert len(pointer)==1
 html=HTML.read_bytes();needle=EXACT.encode();assert html.count(needle)==1
 b=html.index(needle);html_line=html[:b].count(b'\n')+1
 left=html.rfind(b'<li>',0,b);right=html.index(b'</li>',b)+len(b'</li>');fragment=html[left:right]
 audit_line=raw.splitlines(keepends=True)[line-1]
 (OWN/'audit-line292.exactraw.fragment.txt').write_bytes(audit_line)
 (OWN/'HTML-semantic-difference.exactraw.fragment.html').write_bytes(fragment)
 git=[]
 for commit in [SCI,INT]:
  blob=subprocess.run(['git','show',f'{commit}:{AUDIT.relative_to(ROOT).as_posix()}'],cwd=ROOT,capture_output=True,check=True).stdout
  assert blob==raw and needle in blob
  git.append(dict(commit=commit,RAW_sha256=sha(blob),RAW_bytes=len(blob),exact_current_audit_RAW_equal=True,wording='unused'))
 previous=load(OLD/'decision.json');assert previous['reader_debts'][0]['exact_text']!=EXACT and 'facts used by this proof' in previous['reader_debts'][0]['exact_text']
 evidence=dict(status='FROZEN_AND_CURRENT_EVIDENCE_AGREES_UNUSED',actual_PID=os.getpid(),checked_HEAD=INT,checked_science_commit=SCI,
      exact_sentence=EXACT,frozen_current_RAW_equality=equality,Git_audit_equality=git,
      audit=dict(path=pin(AUDIT),line=line,JSON_pointer=pointer[0],whole_file_RAW_sha256=sha(raw),
          exact_line_fragment=pin(OWN/'audit-line292.exactraw.fragment.txt'),sentence_start_byte=a,sentence_end_byte=a+len(needle)),
      HTML=dict(path=pin(HTML),line=html_line,whole_file_RAW_sha256=sha(html),literal_fragment=pin(OWN/'HTML-semantic-difference.exactraw.fragment.html'),
          fragment_start_byte=left,fragment_end_byte=right,sentence_start_byte=b,sentence_end_byte=b+len(needle)),
      original_render=dict(image=pin(PNG),actually_reinspected_native_pixels=True,visible_wording='unused by this proof',
          location='Detected semantic differences / assumptions bullet near bottom of original render-unit0-proof-6.png',
          screenshot_and_HTML_byte_pins_equal_original_frozen72=True),old_CLOSED91_all90_nonself_RAW_LF_files_exact=True,
      no_new_render_or_browser_or_Lean_or_math_gate=True)
 write('evidence.json',evidence)
 decision=dict(schema='reader-observation-correction72/v1',status='REVIEWER_TRANSCRIPTION_ERROR_CONFIRMED_ONLY',actor='/root/exact_science63',actual_PID=os.getpid(),
      correction_confirmed=True,reviewer_transcription_error=True,old_review_retained=True,old_review_lease=pin(OLD/'lease.final.json'),
      wrong_original_quote=previous['reader_debts'][0]['exact_text'],correct_exact_sentence=EXACT,
      correction='The reviewer dropped the prefix un from unused. Withdraw only the used-versus-retained exposition debt and proposed canonical wording repair.',
      affected_old_observation='reader_debts[0] in decision/visual-review/review and its copy in complete named payload; old immutable files are preserved.',
      canonical_or_Lean_repair_needed=False,canonical_or_Lean_or_Git_or_ledger_or_old_closed_writes=False,
      original_scoped_aggregate_decision='unchanged; this addendum is no new acceptance badge',
      other_notation_and_dense_graph_debt_unchanged=True,new_math_or_source_or_repository_acceptance=False,
      full_Exposition_Seal=False,PURIFIED=False,main_live=False,whole_paper=False,Goal_complete=False)
 write('decision.json',decision)
 print(json.dumps(dict(status=decision['status'],actual_PID=os.getpid(),input_count=14,audit_line=line,HTML_line=html_line,original_PNG_word='unused',old_review_retained=True)))
def finalize():
 for row in load(OWN/'inputs.manifest.json')['inputs']:check(row)
 baseline=files();write('outputs.baseline.manifest.json',dict(stage='preterminal baseline; final lease binds every final self/terminal layer',files=baseline))
 payload=dict(payload_name='COMPLETE_READER_OBSERVATION_CORRECTION72',decision=load(OWN/'decision.json'),evidence=load(OWN/'evidence.json'),
       inputs=load(OWN/'inputs.manifest.json'),outputs_baseline=load(OWN/'outputs.baseline.manifest.json'))
 write('complete-named-correction.payload.json',payload)
 run=dict(schema='reader-observation-correction72/run-v1',status='CORRECTION_ONLY_NO_NEW_BADGE',actor='/root/exact_science63',
       decision=pin(OWN/'decision.json'),inputs=pin(OWN/'inputs.manifest.json'),complete_named_RAW_payload=pin(OWN/'complete-named-correction.payload.json'),
       recipe='canonical JSON UTF8 ensure_ascii=false sort_keys=true separators comma/colon; delete ONLY top-level run_sha256',old_CLOSED91_preserved=True)
 run['run_sha256']=sha(canon(run));write('run.json',run)
 print(json.dumps(dict(status='FINALIZED',actual_PID=os.getpid(),whole_logical_run_sha256=run['run_sha256'],complete_named_RAW_payload=run['complete_named_RAW_payload'])))
def readback():
 run=load(OWN/'run.json');want=run.pop('run_sha256');assert sha(canon(run))==want;check(run['complete_named_RAW_payload'])
 for row in load(OWN/'inputs.manifest.json')['inputs']:check(row)
 print(json.dumps(dict(status='READBACK_PASS',actual_PID=os.getpid(),whole_logical_run_sha256=want)))
def close_probe():readback()
def close():
 assert not (OWN/'lease.final.json').exists();readback();launch('close_probe');rows=files()
 write('lease.final.json',dict(status='CLOSED_LAST',actor='/root/exact_science63',actual_last_writer_PID=os.getpid(),closed_utc=datetime.now(timezone.utc).isoformat(),
       all_owned_outputs_except_only_self=rows,owned_count=len(rows)+1,closure_logical_sha256=sha(canon(rows)),
       whole_logical_run_sha256=load(OWN/'run.json')['run_sha256'],complete_named_RAW_payload=pin(OWN/'complete-named-correction.payload.json'),
       final_owned_write=True,all_sessions_closed=True,postclose_owned_writes=False))
 print(json.dumps(dict(status='CLOSED_LAST',actual_PID=os.getpid(),lease=pin(OWN/'lease.final.json'),owned_count=len(rows)+1)))
def postclose():
 lease=load(OWN/'lease.final.json');rows=files();assert rows==lease['all_owned_outputs_except_only_self'];assert sha(canon(rows))==lease['closure_logical_sha256'];readback()
 assert max(OWN.iterdir(),key=lambda p:p.stat().st_mtime_ns).name=='lease.final.json'
 print(json.dumps(dict(status='READONLY_POSTCLOSE_PASS',actual_PID=os.getpid(),owned_count=len(rows)+1,
       total_RAW_bytes=sum(p.stat().st_size for p in OWN.iterdir() if p.is_file()),lease=pin(OWN/'lease.final.json'),closure_logical_sha256=lease['closure_logical_sha256'],owned_writes=False)))
def launch(action):
 assert not (OWN/'lease.final.json').exists();(OWN/f'{action}.executed-helper.RAW.py').write_bytes(SELF.read_bytes())
 argv=[PY,'-B','-X','utf8',str(SELF),'_child',action]
 with (OWN/f'{action}.stdout.log').open('wb') as out,(OWN/f'{action}.stderr.log').open('wb') as err:
  p=subprocess.Popen(argv,cwd=ROOT,stdout=out,stderr=err);print(json.dumps(dict(status='RUNNING',actual_PID=p.pid,runner_PID=os.getpid(),action=action)),flush=True);code=p.wait()
 write(action+'.receipt.json',dict(actual_PID=p.pid,runner_PID=os.getpid(),action=action,command=argv,exit_code=code,terminal_closed=True,
       stdout=pin(OWN/f'{action}.stdout.log'),stderr=pin(OWN/f'{action}.stderr.log'),executed_helper=pin(OWN/f'{action}.executed-helper.RAW.py')))
 print(json.dumps(dict(status='TERMINAL',actual_PID=p.pid,exit_code=code)));return code
if __name__=='__main__':
 action=sys.argv[-1]
 if sys.argv[1]=='_child':sys.exit(globals()[action]() or 0)
 elif action in ['close','postclose']:globals()[action]()
 else:sys.exit(launch(action))
