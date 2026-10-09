from pathlib import Path
from html.parser import HTMLParser
from types import SimpleNamespace
import ctypes,datetime,hashlib,json,os,re,subprocess,sys
ROOT=Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-actual-bounce-rate74';O=R/'independent-repository-reader74';DIS=R/'final-reader-repository-packet74.json';ACTOR='/root/header_math72';SCI='d556a7550f0395d149720da6478bfdfff98368a7';DECL='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws';MOD='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean';PY=Path('C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe');ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1');sys.dont_write_bytecode=True
sha=lambda b:hashlib.sha256(b).hexdigest();can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode();load=lambda p:json.loads(Path(p).read_bytes())
def resolve(p):
 p=Path(p);return p if p.is_absolute() else ROOT/p
def pin(p):
 p=resolve(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
def check(z):
 p=resolve(z['path']);b=p.read_bytes();assert len(b)==z.get('RAW_bytes',z.get('bytes')) and sha(b)==z.get('RAW_sha256',z.get('raw_sha256')) and sha(b.replace(b'\r\n',b'\n'))==z.get('LF_sha256',z.get('lf_sha256')),p;return b
def save(n,j):
 assert not (O/'lease.final.json').exists();p=O/n;p.parent.mkdir(parents=True,exist_ok=True);assert not p.exists(),p;p.write_text(json.dumps(j,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf8',newline='\n')
def command(label,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.Popen([str(x) for x in args],cwd=ROOT,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE);print(json.dumps(dict(START=label,PID=p.pid,driver_PID=os.getpid())),flush=True);out,err=p.communicate();d=O/'terminals';d.mkdir(exist_ok=True);a=d/(label+'.stdout.RAW');b=d/(label+'.stderr.RAW');assert not a.exists() and not b.exists();a.write_bytes(out);b.write_bytes(err);rec=dict(label=label,actual_foreground_PID=p.pid,actual_driver_PID=os.getpid(),command=[str(x) for x in args],terminal_closed=True,terminal_EXIT=p.returncode,started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=pin(a),stderr=pin(b));save('terminals/'+label+'.receipt.json',rec);print(json.dumps(dict(END=label,PID=p.pid,EXIT=p.returncode)),flush=True);assert p.returncode==0,label;return out,rec
class Node:
 def __init__(self,tag='',attrs=None):self.tag=tag;self.attrs=dict(attrs or []);self.children=[]
 def all(self,tag=None):
  out=[self] if tag is None or self.tag==tag else []
  for n in self.children:
   if isinstance(n,Node):out+=n.all(tag)
  return out
 def text(self):return ''.join(x.text() if isinstance(x,Node) else x for x in self.children)
class Tree(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node();self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,s):self.stack[-1].children.append(s)
def prepare():
 j=load(DIS);assert j['checked_science_commit']==SCI and len(j['inputs'])==181
 for z in j['inputs']:check(z)
 save('inputs.manifest.json',dict(dispatch=pin(DIS),input_count=181,inputs=j['inputs']))
 save('initial-frozen-input-check.json',dict(status='PASS',actual_PID=os.getpid(),current_RAW_and_CRLF_pairs_only_LF_checked=181,dispatch=pin(DIS)))
 print(json.dumps(dict(status='PREPARED',actual_PID=os.getpid(),inputs=181)))
def native_reuse():
 results=[]
 for name in ['independent-math74','independent-source74','exact-science-verification74','independent-reader-metadata-repair74','anonymous-decoder']:
  lp=R/name/('CLOSED_LAST.json' if name=='anonymous-decoder' else 'lease.final.json');j=load(lp);assert j['status']=='CLOSED_LAST'
  if name=='independent-math74':
   m=load(resolve(j['manifest']['path']));check(j['manifest']);rows=m['entries'];assert len(rows)==m['entry_count'] and len(rows)+2==j['owned_files'] and sha(can(rows))==m['logical_entries_sha256'];extra={lp.resolve(),resolve(j['manifest']['path']).resolve()}
  else:
   key=next(k for k in ['all_files_except_self','all_owned_outputs_except_only_self','prior_owned_files'] if k in j);rows=j[key];extra={lp.resolve()}
  files={p.resolve() for p in lp.parent.rglob('*') if p.is_file()};assert files=={resolve(z['path']).resolve() for z in rows}|extra
  for z in rows:check(z);assert resolve(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
  results.append(dict(name=name,lease=pin(lp),owned_files=len(files),finite_owned_hashes_unchanged=True,recertified_mathematics=False,recertified_source=False))
 return results
def check_child():
 im=load(O/'inputs.manifest.json');assert im['inputs']==load(DIS)['inputs']
 for z in im['inputs']:check(z)
 src=(ROOT/MOD).read_bytes();assert sha(src)=='fcec688033797683b44f279a4d22971598926e6af3e9682ad76493d37580937c';lines=src.splitlines(keepends=True);assert len(lines)==211
 u=load(ROOT/'website/content/declaration_lessons/pbps-actual-bounce-rate.json')['units'][0];pub=load(ROOT/'website/content/publications/pbps-actual-bounce-rate.json')['items'][0];a=load(ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualBounceRate.json');cell=load(ROOT/'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounce-rate.json');assert len(u['steps'])==7 and u['declaration']==DECL and pub['bindings'][0]['declaration']==DECL
 spans=[]
 for i,s in enumerate(u['steps']):
  q=s['lean_source_region'];b=b''.join(lines[q['start_line']-1:q['end_line']]);assert b.decode()==s['lean'] and sha(b)==q['exact_code_raw_sha256'] and q['source_raw_sha256']==sha(src);assert s['formula'] and s['text'];spans.append(dict(step=i+1,title=s['title'],start_line=q['start_line'],end_line=q['end_line'],exact_BODY_RAW_sha256=sha(b)))
 assert [(z['start_line'],z['end_line']) for z in spans]==[(106,111),(112,130),(131,136),(137,161),(162,169),(170,187),(188,208)]
 assert 'unused' in u['statement'] and all(t in u['statement'] for t in ['Positive α, α≤β and βη≤1','C²','global Hessian bounds','η>0','rank zero','No joint continuity of S'])
 sys.path.insert(0,str(ROOT/'tools'));import astis_publication as ap
 data=dict(declarations={DECL:SimpleNamespace(source_file=MOD)},lessons={DECL:u});binding=ap.binding_digest(pub,pub['bindings'][0],data);context=ap.review_context(pub,pub['bindings'][0],data);assert binding==a['publication_binding_sha256'] and context==a['publication_context'];assert a['state']=='source-reviewed' and a['verdict']=='equivalent-after-elaboration';assert a['source_review']['independent_from_formalizer'] and a['source_review']['independent_from_decoder']
 html=(ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html').read_text(encoding='utf8');start=html.index('<section id="pbps-actual-bounce-rate"');end=html.find('<section id=',start+1);fragment=html[start:end if end!=-1 else None];t=Tree();t.feed(fragment);article=next(n for n in t.root.all('article') if n.attrs.get('data-authored-declaration')==DECL);details=article.all('details');assert len(details)==13 and all('open' not in n.attrs for n in details);codes=[n.text() for n in article.all('code') if 'language-lean' in n.attrs.get('class','')];assert len(codes)==10
 for s in u['steps']:assert s['lean'] in codes and s['formula'] in fragment
 assert u['statement'] in article.text();assert all(s['text'] in article.text() for s in u['steps']);assert 'private def actual_bounce_rate_energy_statement' in article.text();assert all('h'+k in article.text() for k in ['α','αβ','V','H','η','βη'])
 vis=R/'integration74/visual74';copy=load(vis/'copy-unit0-copy-and-download.inspect.json');assert copy['initialFolded'] and copy['copyProbeUsesIsolatedPageClipboardCallback'] and not copy['physicalOSClipboardTest'];assert len(copy['panels'])==len(copy['downloads'])==3 and len(copy['steps'])==7
 for p in copy['panels']:assert p['callbackCalled'] and p['copiedExactly'] and p['status']=='Copied' and p['code'] in codes and p['code'] in src.decode()
 for d in copy['downloads']:assert d['status']==200 and d['text'].encode()==src and d['bytes']==len(d['text'])
 for s,ss in zip(u['steps'],copy['steps']):assert s['lean']==ss['lean'] and ss['initiallyFolded']
 render=load(vis/'render-capture.json');cc=load(vis/'copy-capture.json');assert render['ownedBrowserExit']['code']==cc['ownedBrowserExit']['code']==0;assert len(render['records'])==9 and len(cc['records'])==1
 pngs=[z for z in im['inputs'] if z['path'].endswith('.png')];assert len(pngs)==10
 graph=load(ROOT/'_site/data/underlying-lean-graph.json');mid='module:'+DECL.rsplit('.',1)[0];did='decl:'+DECL;nodes={n['id']:n for n in graph['nodes']};assert nodes[mid]['status']==nodes[did]['status']=='compiled';direct=[e for e in graph['edges'] if e['source']==did or e['target']==did];assert len(direct)==3;assert any(e['source']==mid and e['relation']=='declares' for e in direct);assert any(e['relation']=='source correspondence; not a Lean dependency' for e in direct);assert any(e['relation']=='Lean target under audit' for e in direct);assert any(e['source']=='module:AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization' and e['target']==mid and e['relation']=='imports' for e in graph['edges']);assert cell['status']=='independently_verified'
 gates=[]
 for z in im['inputs']:
  if z['path'].endswith('/receipt.json') and '/integration74/' in z['path']:
   q=load(z['path'])
   if 'exit_code' in q:
    name=Path(z['path']).parent.name;expected=1 if name=='narrow-generated-scope' else 0;assert q['terminal_closed'] and q['exit_code']==expected and q['checked_parent']==SCI
    for k in ['stdout','stderr']:check(q[k])
    gates.append(dict(label=name,actual_foreground_PID=q['actual_foreground_PID'],terminal_EXIT=q['exit_code'],terminal_closed=True,receipt=z))
 logs=lambda n:(R/'integration74'/n/'stdout.log').read_text(encoding='utf8')
 assert all(x in logs('mandatory-astis-check-final') for x in ['ASTIS check passed','Build completed successfully (9185 jobs).','Build completed successfully (9485 jobs).']);assert '244 source items' in logs('publication-final');assert '523 compiled local leaves' in logs('website-ci-build');assert 'ASTIS site check passed' in logs('site-check-final');assert '"omitted_connections": 0' in logs('graph-check-final')
 before=load(R/'integration74/before-generator-state.json');side=load(R/'integration74/generator-sideeffects/receipt.json');rest=[x for x in side['rows'] if x['action'].startswith('RESTORE_')];new=[x for x in side['rows'] if x['action'].startswith('PRESERVE_')];assert len(rest)==101 and len(new)==443
 protected=set(before['preexisting_tracked_changes'])|set(before['keep'])|set(before['untracked_cards']);assert not ({x['path'] for x in rest+new}&protected)
 for x in side['rows']:
  assert sha(resolve(x['generated_backup']).read_bytes())==x['generated_RAW_sha256']
  if 'HEAD_backup' in x:assert sha(resolve(x['HEAD_backup']).read_bytes())==x['HEAD_RAW_sha256']
 pairs=[]
 for n,count in [('diagnosis.json',10),('remaining-RAW-diagnosis.json',11)]:
  q=load(R/'integration74/generator-line-ending-diagnosis'/n);assert len(q['rows'])==count
  for x in q['rows']:
   generated=resolve(x['generated_backup']).read_bytes();head=resolve(x['HEAD_backup']).read_bytes();assert generated!=head and generated.replace(b'\r\n',b'\n')==head.replace(b'\r\n',b'\n');assert not x['preexisting_tracked_change'] and x['only_CRLF_pairs_differ'];assert x['path'] not in protected;pairs.append(dict(path=x['path'],generated_RAW_sha256=sha(generated),HEAD_RAW_sha256=sha(head),common_LF_sha256=sha(head.replace(b'\r\n',b'\n'))))
 reuse=load(R/'integration74/unchanged-regression-reuse.json');assert reuse['unchanged_Git_and_workspace'] and reuse['fresh_full_suite_or_full_browser_for74']==False and 'Historical executable RAW hashes were not recorded' in reuse['runtime_qualification'];prior=[]
 for x in reuse['records']:
  q=load(resolve(x['receipt']['path']));check(x['receipt']);check(x['stdout']);check(x['stderr']);assert q['exit_code']==0 and q['terminal_closed'] and not x['fresh_for74'];prior.append(dict(label=x['label'],receipt=x['receipt'],actual_foreground_PID=q['actual_foreground_PID'],terminal_EXIT=0))
 for x in reuse['current_runtime_pins']:check(x['current_pin']);assert x['mtime_predates_reused_runs'] and x['historical_RAW_hash_not_recorded']
 vf=load(R/'verified.json');assert vf['status']=='VERIFIED' and vf['verifier_id']=='/root/exact_science63' and vf['verified_commit']==SCI and vf['transition_count']==1;assert not vf['aggregate'] and not vf['current_reader'];native=native_reuse()
 result=dict(status='PASS_SCOPED_CURRENT_READER_FINITE_CHECKS',actual_foreground_PID=os.getpid(),checked_science_commit=SCI,all_dispatch_RAW_LF_pins=181,formula_BODY_spans=spans,initially_closed_details=13,exact_Lean_code_panels=10,copy_callbacks=3,RAW_downloads=3,download_UTF8_RAW_bytes=len(src),download_Javascript_character_count=len(src.decode()),publication_binding_sha256=binding,publication_context_exact=True,source_binding_reused_unchanged=True,source_and_decoder_distinct=True,native_reviews_reused=native,new_independent_mathematics_certification=False,current_gate_receipts=gates,direct_graph_connections=direct,graph_labels_dense=True,graph_not_theorem_implication=True,protected_generator_scope_paths=sorted(protected),restored_clean_generated_paths=101,unused_new_cards_preserved_exact_backups=443,generated_backup_hashes_checked=len(side['rows']),CRLF_only_pairs=pairs,scoped_failure_PID=27336,scoped_failure_EXIT=1,diagnostic_recheck_PID=31776,prior_full_regressions_reused=prior,runtime_qualification=reuse['runtime_qualification'],physical_OS_clipboard_test=False,new_VERIFIED_transition=False)
 print(json.dumps(result,ensure_ascii=False))
def checks():
 out,headrec=command('checked-current-HEAD',['git','rev-parse','HEAD']);assert out.decode().strip()==SCI
 out,gitrec=command('unchanged-reused-helper-Git-diff',['git','diff','bc3dca8d76432f71e3abbfdbce2c3b2161ec8d19','HEAD','--','tools','website/scripts','website/static','.github/workflows','lean-toolchain','lake-manifest.json']);assert not out
 out,wrec=command('unchanged-reused-helper-workspace-diff',['git','diff','--','tools','website/scripts','website/static','.github/workflows','lean-toolchain','lake-manifest.json']);assert not out
 out,rec=command('independent-finite-reader-checks',[PY,'-B','-X','utf8',O/'review74.py','check-child']);result=json.loads(out);assert result['status'].startswith('PASS_');save('checks.json',dict(result=result,actual_terminal_receipts=[headrec,gitrec,wrec,rec]))
def postclose():
 lp=O/'lease.final.json';l=load(lp);assert l['status']=='CLOSED_LAST' and l['actor']==ACTOR and l['postclose_owned_writes_forbidden'] and l['final_owned_write'];rows=l['files'];assert l['file_count_including_lease']==len(rows)+1 and sha(can(rows))==l['closure_logical_sha256'];assert {p.resolve() for p in O.rglob('*') if p.is_file()}=={resolve(z['path']).resolve() for z in rows}|{lp.resolve()}
 for z in rows:check(z);assert resolve(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
 run=load(O/'run.json');assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==l['run_sha256'];assert run['checked_science_commit']==SCI
 for k in ['decision','inputs_manifest','complete_named_RAW_payload']:check(run[k])
 d=load(resolve(run['decision']['path']));im=load(resolve(run['inputs_manifest']['path']));p=load(resolve(run['complete_named_RAW_payload']['path']));assert p['decision']==d and p['inputs']==im and im['inputs']==load(DIS)['inputs'] and len(im['inputs'])==im['input_count']==181;check(im['dispatch'])
 for z in im['inputs']:check(z)
 assert d['accepted_scoped_aggregate'] and d['independent_of_formalizer_stabilizer'] and not d['blockers'];assert all(not d[k] for k in ['new_VERIFIED_transition','new_independent_mathematics_certification','Goal_complete','PURIFIED','full_Exposition_Seal','main','live','whole_paper']);assert len(d['independently_viewed_PNG_records'])==d['independently_viewed_PNGs']==10
 k=ctypes.WinDLL('kernel32',use_last_error=True);k.OpenProcess.restype=ctypes.c_void_p;h=k.OpenProcess(0x00100000,False,l['writer_PID'])
 if h:k.WaitForSingleObject.argtypes=[ctypes.c_void_p,ctypes.c_ulong];k.CloseHandle.argtypes=[ctypes.c_void_p];assert k.WaitForSingleObject(h,0)==0;k.CloseHandle(h)
 else:assert ctypes.get_last_error()==87
 print(json.dumps(dict(status='PASS',actual_external_readonly_PID=os.getpid(),writer_PID=l['writer_PID'],writer_terminated=True,owned_files=l['file_count_including_lease'],current_inputs=181,run_sha256=run['run_sha256'],no_owned_writes=True,new_VERIFIED_transition=False)))
if __name__=='__main__':{'prepare':prepare,'checks':checks,'check-child':check_child,'postclose':postclose}[sys.argv[1]]()
