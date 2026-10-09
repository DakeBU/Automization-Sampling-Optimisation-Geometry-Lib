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

def bindings():
 slugs=['pbps-hilbert-corrector-perturbation','pbps-actual-corrector-perturbation']
 paths=[ROOT/'AutoSamplingTheory/TechnicalLemmas/Analysis/HilbertCorrectorPerturbation.lean',ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCorrectorPerturbation.lean']
 units=[load(ROOT/f'website/content/declaration_lessons/{s}.json')['units'][0] for s in slugs]
 names=[u['declaration'] for u in units]
 class Parser(HTMLParser):
  def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.article=None;self.articles={};self.buf=None;self.code_meta=None
  def handle_starttag(self,t,a):
   a=dict(a)
   if t=='article' and a.get('data-authored-declaration') in names:
    self.article=a['data-authored-declaration'];self.articles[self.article]=dict(codes=[],details=[])
   if self.article and t=='details':self.articles[self.article]['details'].append(a)
   if self.article and t=='code' and a.get('class')=='language-lean':
    self.buf=[];self.code_meta=dict(details=[v for tag,v in self.stack if tag=='details'])
   if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append((t,a))
  def handle_data(self,s):
   if self.buf is not None:self.buf.append(s)
  def handle_endtag(self,t):
   if t=='code' and self.buf is not None:
    self.articles[self.article]['codes'].append(dict(code=''.join(self.buf),**self.code_meta));self.buf=None
   if t=='article' and self.article:self.article=None
   for i in range(len(self.stack)-1,-1,-1):
    if self.stack[i][0]==t:self.stack=self.stack[:i];break
 parser=Parser();htmlpath=ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html'
 parser.feed(htmlpath.read_text(encoding='utf-8'));assert set(parser.articles)==set(names)
 c=load(R/'integration72/visual72/copy-capture.json');result=[]
 for i,(p,u,rec) in enumerate(zip(paths,units,c['records'])):
  raw=p.read_bytes();text=raw.decode();git=subprocess.run(['git','show',f'{SCI}:{p.relative_to(ROOT).as_posix()}'],cwd=ROOT,capture_output=True,check=True).stdout
  assert git==raw;assert len(text.splitlines())==[54,440][i]
  article=parser.articles[u['declaration']];panels=[x for x in article['codes'] if any('inline-lean' in d.get('class','') for d in x['details'])]
  assert len(panels)==[2,3][i];assert len(rec['panels'])==len(panels)
  assert rec['initialFolded'] and not rec['physicalOSClipboardTest'] and rec['copyProbeUsesIsolatedPageClipboardCallback']
  panelpins=[]
  for j,(rendered,copied) in enumerate(zip(panels,rec['panels'])):
   assert rendered['code']==copied['code'];assert copied['callbackCalled'] and copied['copiedExactly'] and copied['status']=='Copied'
   assert copied['code'] in text
   assert all('open' not in d for d in rendered['details'])
   panelpins.append(dict(index=j,code_UTF8_bytes=len(copied['code'].encode()),code_RAW_sha256=sha(copied['code'].encode()),
        exact_canonical_substring=True,exact_current_HTML=True,initially_folded=True,callback_copy_exact=True,
        authored_declaration=[d.get('data-inline-lean') for d in rendered['details'] if 'data-inline-lean' in d]))
  downloads=[]
  for d in rec['downloads']:
   assert d['status']==200 and d['text'].encode()==raw
   downloads.append(dict(href=d['href'],HTTP_status=200,actual_UTF8_RAW_bytes=len(raw),actual_RAW_sha256=sha(raw),
        observer_bytes_field=d['bytes'],observer_bytes_qualification='JavaScript UTF16 string length, not UTF8 RAW byte count'))
  steps=[];assert len(u['steps'])==len(rec['steps'])==[6,4][i]
  lines=raw.splitlines(keepends=True);body_line=next(j+1 for j,l in enumerate(lines) if l.rstrip().endswith(b':= by') and b'theorem' not in l) if i==0 else 151
  # Explicit theorem BODY boundary from the exact public declaration, not a header/example span.
  theorem_start=text.index('theorem '+u['declaration'].split('.')[-1]);body_offset=text.index(':= by',theorem_start)+len(':= by')
  body_line=text[:body_offset].count('\n')+1
  for j,(step,cap) in enumerate(zip(u['steps'],rec['steps'])):
   region=step['lean_source_region'];assert region['source_raw_sha256']==sha(raw)
   assert (ROOT/region['path']).resolve()==p.resolve()
   a,b=region['start_line'],region['end_line'];span=b''.join(lines[a-1:b]);assert a>body_line
   assert sha(span)==region['exact_code_raw_sha256']
   # Authored code is exact, apart from an explicitly recorded optional terminal LF outside textContent.
   code=step['lean'].encode();assert span in (code,code+b'\n')
   assert cap['lean']==step['lean'] and cap['initiallyFolded']
   matches=[x for x in article['codes'] if x['code']==step['lean']];assert matches and all('open' not in d for x in matches for d in x['details'])
   steps.append(dict(step=j+1,start_line=a,end_line=b,whole_source_RAW_sha256=sha(raw),literal_span_RAW_sha256=sha(span),
       formula_RAW_sha256=sha(step['formula'].encode()),exact_BODY=True,source_span_terminal_LF_outside_authored_text=span!=code,
       authored_and_capture_and_HTML_literal_match=True,initially_folded=True))
  if i==1:
   assert 'private def actual_corrector_perturbation_statement' in rec['panels'][2]['code']
   assert rec['panels'][2]['code'].rstrip().endswith('inner ℝ u (Inv r)+‖r‖^2/2))')
  result.append(dict(declaration=u['declaration'],module=pin(p),exact_SCI_Git_RAW_equality=True,module_lines=len(lines),
       statement_and_proof_and_authored_helper_panels=panelpins,RAW_downloads=downloads,literal_BODY_steps=steps,
       private_literal_full_adjacent_fold=i==1,public_statement_and_source_attribution='current accepted lesson/source binding; no new source review'))
 # Exact current source inputs of the official graph freshness function, using its own read-only recipe.
 sys.path[:0]=[str(ROOT/'website/scripts'),str(ROOT/'tools')];import publication_reader
 graph=load(ROOT/'_site/data/underlying-lean-graph.json');digest=publication_reader.graph_input_digest()
 assert digest==graph['publication_inputs_sha256']
 finaladmin=load(R/'integration72/final-admin.json');cells=[checkpin(x) for x in finaladmin['cells']];assert len(cells)==2
 reg=ROOT/'AutoSamplingTheory/TechnicalLemmas/Registry.lean';regtext=reg.read_text(encoding='utf-8');count=len(re.findall(r'status\s*:=\s*LemmaMemoryStatus.formalizedLocal',regtext));assert count==521
 assert all(n in regtext for n in names)
 imports=(ROOT/'AutoSamplingTheory/ExampleCases.lean').read_text(encoding='utf-8');assert 'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation' in imports
 test=(ROOT/'Tests/Basic.lean').read_text(encoding='utf-8');assert 'formalizedTechnicalLemmaCount = 521' in test
 assert 'HilbertCorrectorPerturbation.quadratic_corrector_perturbation' in paths[1].read_text(encoding='utf-8')
 claim=load(R/'claim.json');plan=load(R/'publication-plan.json')
 node=next(n for n in graph['nodes'] if n['id']=='decl:'+names[1])
 gitqualification=[]
 for p in [ROOT/'lean-toolchain',ROOT/'lake-manifest.json']:
  git=subprocess.run(['git','show',f'{SCI}:{p.relative_to(ROOT).as_posix()}'],cwd=ROOT,capture_output=True,check=True).stdout;raw=p.read_bytes()
  assert git.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n')
  gitqualification.append(dict(current=pin(p),Git_RAW_sha256=sha(git),Git_RAW_bytes=len(git),exact_RAW=git==raw,CRLF_only_LF_equal=True))
 write('bindings.audit.json',dict(status='PASS_BOUNDED_EXACT_SOURCE_AND_READER_BINDINGS',actual_PID=os.getpid(),checked_science_commit=SCI,
      input_readback_count=recheck(),units=result,formula_BODY_count=10,copy_callback_count=5,RAW_download_count=5,
      physical_OS_clipboard_test=False,HTML=pin(htmlpath),Registry_count=count,root_import_and_Tests_count_exact=True,
      genuine_generic_to_actual_consumer=True,current_graph=pin(ROOT/'_site/data/underlying-lean-graph.json'),
      current_graph_inputs_digest=digest,current_graph_digest_equals_final_cells_and_publications=True,final_cells=cells,
      graph_edge_truth='formal imports/declares are separate from dashed name-scan reference overlays; name-scan references incomplete and may include false positives',
      actual_node_status=node.get('status'),fixed_toolchain_and_manifest=gitqualification,
      cell_count=2,SAU_count=1,claim_id=claim.get('advance_id',claim.get('id')),publication_plan_keys=list(plan),
      aggregation_commit_exists=False,science_commit_and_uncommitted_current_aggregate_distinct=True))
 print(json.dumps(dict(status='BINDINGS_PASS',actual_PID=os.getpid(),units=2,steps=10,copies=5,downloads=5,Registry=count,digest=digest)))

def bindings2():return bindings()
def bindings3():return bindings()

def jsondiff(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  out=[]
  for k in sorted(set(a)|set(b)):
   if k not in a:out.append(dict(pointer=p+'/'+k,before_absent=True,after=b[k]))
   elif k not in b:out.append(dict(pointer=p+'/'+k,before=a[k],after_absent=True))
   else:out+=jsondiff(a[k],b[k],p+'/'+k)
  return out
 return [] if a==b else [dict(pointer=p,before=a,after=b)]

def admin_scope():
 extras=[]
 def extra(p):
  z=pin(p);extras.append(z);return z
 recovery=load(R/'integration72/record-final-admin/typed-diagnosis-and-repair.json')
 assert recovery['failed_admin_PID']==26688 and recovery['failed_admin_exit']==1 and recovery['failed_before_canonical_admin_writes']
 receipts=[]
 for label,pid,code in [('record-final-admin',26688,1),('record-final-admin-recovered',37784,0),('record-integration-final',40804,0)]:
  p=R/'integration72'/label/'receipt.json';j=load(p);assert j['actual_foreground_PID']==pid and j['exit_code']==code and j['terminal_closed']
  receipts.append(dict(label=label,actual_PID=pid,exit_code=code,receipt=extra(p),stdout=checkpin(j['stdout']),stderr=checkpin(j['stderr'])))
 beforehelper=R/'integration72/record-final-admin/record-integration72.py.before-repair.exactraw.snapshot';h=beforehelper.read_text(encoding='utf-8')
 assert h.index("len(probe['panels'])==len(probe['downloads'])==3")<h.index("dest=r/'integration72/visual72'")<h.index("p.write_text(json.dumps(c")
 failedhelper=extra(beforehelper);diagnosis=extra(R/'integration72/record-final-admin/typed-diagnosis-and-repair.json')
 cellmaps=[]
 for i,slug in enumerate(['hilbert','actual']):
  p=ROOT/f'research-wiki/frontier-cells/ASTIS-SW-PBPS-{slug}-corrector-perturbation.json'
  before=R/f'integration72/cell.{i}.before-final-admin.exactraw.snapshot.json';changes=jsondiff(load(before),load(p))
  assert {x['pointer'] for x in changes}=={'/blocked/reason','/evidence/serialized_shared_gate','/graph_contribution/visual_review'}
  cellmaps.append(dict(before=pin(before),after=pin(p),exact_changes=changes,mathematical_statement_and_source_assumptions_unchanged=True))
 # Preserve the old premature terminals as historical only; they are not final acceptance receipts.
 old=[]
 for label in ['official-graph-final-admin','graph-check-actual-final','graph-check-generic-final','site-check-final']:
  p=R/'integration72'/label/'receipt.json';j=load(p);old.append(dict(label=label,receipt=extra(p),actual_PID=j['actual_foreground_PID'],exit_code=j['exit_code'],
      final_credit=False,qualification='premature chain; final admin/cell state was not the final recovered state'))
 guard=ROOT/'.astis/pbps-perturbation72/foreground72.py';guardbytes=guard.read_bytes()
 assert b'Final admin not written; reject premature dependent gate before any output writes.' in guardbytes
 (OWN/'root-foreground72.guard.exactraw.snapshot.py').write_bytes(guardbytes)
 # Two entry additions are the entire Registry delta. Every prior entry remains byte-exact modulo CRLF-only normalization.
 ownedbefore=load(R/'integration72/owned-before.json');assert ownedbefore['head']==SCI
 snapshots={x['path']:x for x in ownedbefore['owned']}
 def oldbytes(name):
  row=snapshots[name];p=ROOT/row['exact_snapshot'];raw=p.read_bytes();assert sha(raw)==row['RAW_sha256'];return raw.replace(b'\r\n',b'\n')
 regname='AutoSamplingTheory/TechnicalLemmas/Registry.lean';new=(ROOT/regname).read_bytes().replace(b'\r\n',b'\n')
 for key in [b'pbps.hilbertCorrectorPerturbation',b'pbps.actualCorrectorPerturbation']:
  pattern=rb'  \{\n    key := "'+re.escape(key)+rb'"\n.*?\n  \},\n';new,n=re.subn(pattern,b'',new,flags=re.S);assert n==1
 assert new==oldbytes(regname)
 im='AutoSamplingTheory/ExampleCases.lean';new=(ROOT/im).read_bytes().replace(b'\r\n',b'\n');line=b'import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualCorrectorPerturbation\n'
 assert new.count(line)==1 and new.replace(line,b'')==oldbytes(im)
 te='Tests/Basic.lean';assert (ROOT/te).read_bytes().replace(b'\r\n',b'\n').replace(b'formalizedTechnicalLemmaCount = 521',b'formalizedTechnicalLemmaCount = 519')==oldbytes(te)
 generator=load(R/'integration72/generator-sideeffects/receipt.json');assert len(generator['rows'])==541
 restored=preserved=0
 for row in generator['rows']:
  assert sha((ROOT/row['generated_backup']).read_bytes())==row['generated_RAW_sha256']
  if 'HEAD_backup' in row:
   oldraw=(ROOT/row['HEAD_backup']).read_bytes();assert sha(oldraw)==row['HEAD_RAW_sha256']
   assert (ROOT/row['path']).read_bytes()==oldraw;restored+=1
  else:assert not (ROOT/row['path']).exists();preserved+=1
 assert (restored,preserved)==(98,443)
 recovered=R/'integration72/recover-generated-scope/receipt.json';j=load(recovered);assert j['exit_code']==0 and j['terminal_closed'];extra(recovered)
 negative=R/'integration72/narrow-generated-scope/receipt.json';j=load(negative);assert j['exit_code']==1 and j['terminal_closed'];extra(negative)
 extra(R/'integration72/narrow-generated-scope/executed-failed-helper.exactraw.py')
 write('admin-recovery.audit.json',dict(status='RECOVERED_AND_FINAL_STATE_BOUND_NO_NEGATIVE_ERASURE',actual_PID=os.getpid(),
      failed_admin_before_canonical_writes=True,failed_admin_helper=failedhelper,diagnosis=diagnosis,actual_admin_terminals=receipts,
      total_copy_download_panels=5,split=[2,3],old_premature_terminals=old,guard_snapshot=pin(OWN/'root-foreground72.guard.exactraw.snapshot.py'),
      old_outer_guard_stop='Root diagnosis and exact guard source retained; no portable outer terminal receipt supplied, so no outer PID/EXIT invented.',
      final_admin_pending_flag='historical phase marker before regeneration; all8 after-admin-recovery actual final receipts resolve it',
      finite_final_cell_admin_maps=cellmaps,source_math_native_unchanged=True))
 write('scope.audit.json',dict(status='BOUNDED_SHARED_DIFF_AND_GENERATOR_PRESERVATION_PASS',actual_PID=os.getpid(),
      current_HEAD=SCI,aggregate_commit_exists=False,Registry_old=519,Registry_new=521,new_entries=2,all_prior_Registry_entries_preserved=True,
      root_import_delta=1,Tests_only_change='formalizedTechnicalLemmaCount519->521',
      generator_receipt=pin(R/'integration72/generator-sideeffects/receipt.json'),restored_exact_old_files=restored,
      preserved_unused_new_generated_cards=preserved,recovered_generator_negative_PID=24140,recovered_generator_negative_EXIT=1,
      actual_recovery_PID=generator['actual_PID'],bounded_generated_scope_preserved=True,
      approved_scope='16 listed current integration surfaces + native evidence; future73/preproof/canonical state not credited',
      PR_body=pin(R/'integration72/pr315-body72.md'),PR_boundary_reviewed=True,
      full_staged_whitespace_PASS=False,SCI_immutable_whitespace_findings=335,authored_complement_PASS_reused=True))
 write('supplementary-inputs.manifest.json',dict(input_count=len(extras),inputs=extras,recipe=RECIPE,
       classification='finite immutable administrative history and negative/helper/terminal references supplement original145; no historical fallback'))
 previous=read('gates.audit.json');(OWN/'gates.audit.v1.observer.exactraw.json').write_bytes((OWN/'gates.audit.json').read_bytes())
 actual=[x for x in previous['receipts'] if x['exit_code'] is not None]
 metadata=[x for x in previous['receipts'] if x['exit_code'] is None]
 assert len(actual)==20 and len(metadata)==1 and all(x['exit_code']==0 and x['terminal_closed'] for x in actual)
 previous.update(actual_terminal_gate_receipts=20,administrative_metadata_records=1,
       observer_qualification='generator-sideeffects/receipt.json is a metadata/preservation record, not a terminal gate receipt',
       final_after_admin_recovery_gate_count=8)
 write('gates.audit.json',previous)
 print(json.dumps(dict(status='ADMIN_SCOPE_PASS',actual_PID=os.getpid(),restored=restored,preserved=preserved,final_gate_terminals=8)))

def authority_readback():
 results=[]
 for scope,count,m in [('independent-source72',258,'native.manifest.json'),('exact-science-verification72',163,'owned.manifest.json')]:
  base=R/scope;entries=load(base/m)['entries'];expected={str((Path(x['path']) if Path(x['path']).is_absolute() else base/x['path']).resolve()) for x in entries}
  expected|={str((base/m).resolve()),str((base/'lease.final.json').resolve())}
  actual={str(p.resolve()) for p in base.rglob('*') if p.is_file()};assert actual==expected and len(actual)==count
  results.append(dict(scope=scope,all_owned_files=count,manifest_coverage_complete=True))
 verified=load(R/'verified.json');assert verified['native_verified'] and verified['verified_commit']==SCI
 assert verified['verifier_id']=='/root/header_math72' and verified['verifier_id']!='/root/exact_science63'
 assert verified['fake_closure_scan']['hits']==0 and verified['source_audit']['status']=='source-reviewed'
 assert all(x['terminal_EXIT']==0 and x['standard_axioms_only'] and x['fresh_source_elaboration'] for x in verified['gate']['fresh_Lean'])
 semantic=[]
 for slug in ['pbps-hilbert-corrector-perturbation','pbps-actual-corrector-perturbation']:
  for folder in ['website/content/publications','website/content/declaration_lessons']:
   p=ROOT/f'{folder}/{slug}.json';raw=p.read_bytes();git=subprocess.run(['git','show',f'{SCI}:{p.relative_to(ROOT).as_posix()}'],cwd=ROOT,capture_output=True,check=True).stdout
   assert raw==git;semantic.append(dict(current=pin(p),exact_SCI_Git_RAW_equality=True))
 for label in ['Hilbert','Actual']:
  p=ROOT/f'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPS{label}CorrectorPerturbation.json';raw=p.read_bytes()
  git=subprocess.run(['git','show',f'{SCI}:{p.relative_to(ROOT).as_posix()}'],cwd=ROOT,capture_output=True,check=True).stdout
  assert raw==git;semantic.append(dict(current=pin(p),exact_SCI_Git_RAW_equality=True))
 cells=[]
 for slug in ['hilbert','actual']:
  p=ROOT/f'research-wiki/frontier-cells/ASTIS-SW-PBPS-{slug}-corrector-perturbation.json'
  git=subprocess.run(['git','show',f'{SCI}:{p.relative_to(ROOT).as_posix()}'],cwd=ROOT,capture_output=True,check=True).stdout
  diffs=jsondiff(json.loads(git),load(p))
  allowed={'/blocked/reason','/evidence/execution_boundary','/evidence/independent_verification','/evidence/serialized_shared_gate','/evidence/truth_boundary','/graph_contribution/visual_review','/status','/source_detail_audit/fidelity_boundary','/source_detail_audit/gap'}
  assert all(d['pointer'] in allowed for d in diffs),diffs
  cells.append(dict(current=pin(p),SCI_Git_RAW_sha256=sha(git),SCI_Git_RAW_bytes=len(git),finite_process_only_changes=diffs,
       mathematical_target_binders_parents_consumers_unmodified=True))
 # Only the matching SAU record slice is read; the full ledger was never copied into this review.
 records=[json.loads(line) for line in (ROOT/'runs/substantive_advances.jsonl').read_bytes().splitlines() if line.strip()]
 events=[j for j in records if j.get('advance_id')==verified['advance_id'] and j.get('to_state')=='VERIFIED']
 assert len(events)==1
 write('authority-readback.audit.json',dict(status='EXACT_NATIVE_AUTHORITY_AND_UNCHANGED_SCI_PUBLICATION_PASS',actual_PID=os.getpid(),
       packages=results,verified=pin(R/'verified.json'),verified_commit=SCI,nonowner_verifier_id=verified['verifier_id'],
       prior_fresh_exact_Lean=verified['gate']['fresh_Lean'],prior_fake_closure_hits=0,source_review_reused=True,
       current_six_publication_lesson_audit_Git_RAW=semantic,current_cell_finite_SCI_process_maps=cells,
       unique_nonowner_VERIFIED_event=True,ledger_not_copied=True,new_VERIFIED_transition=False,new_math_certification=False))
 print(json.dumps(dict(status='AUTHORITY_PASS',actual_PID=os.getpid(),exact_Git_publication_files=6,unique_prior_VERIFIED=True)))

def authority_readback2():return authority_readback()
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
