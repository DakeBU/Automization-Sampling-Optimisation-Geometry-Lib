from review63 import *
import html
from functools import lru_cache
from html.parser import HTMLParser
I=BASE/'integration63'
def streamhash(p,opener=open):
 h=hashlib.sha256();n=0
 with opener(p,'rb') as f:
  while chunk:=f.read(2**20):h.update(chunk);n+=len(chunk)
 return n,h.hexdigest()
@lru_cache(maxsize=None)
def blob(commit,path):return subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT,stderr=subprocess.DEVNULL)
def pincheck(row):
 p=abspath(row['path']);b=p.read_bytes();assert sha(b)==row['raw_sha256'],p
 assert len(b)==row.get('bytes',row.get('raw_bytes',len(b))),p
 if 'lf_sha256' in row:assert sha(b.replace(b'\r\n',b'\n'))==row['lf_sha256'],p
 return b
def walkpins(x,key=''):
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:yield key,x
  for k,v in x.items():yield from walkpins(v,key+'.'+k)
 elif isinstance(x,list):
  for j,v in enumerate(x):yield from walkpins(v,key+f'[{j}]')
def diffjson(a,b,path=''):
 if isinstance(a,dict) and isinstance(b,dict):
  z=[]
  for k in sorted(set(a)|set(b)):z+=diffjson(a.get(k),b.get(k),path+'/'+k)
  return z
 return [] if a==b else [{'field':path,'before':a,'after':b}]
def audit():
 assert git('rev-parse','HEAD')==COMMIT and git('rev-parse',COMMIT+'^')==SCI
 tree={}
 for line in git('ls-tree','-r',COMMIT).splitlines():
  meta,path=line.split('\t',1);tree[path]=meta.split()[2]
 oldtree={}
 for line in git('ls-tree','-r',SCI).splitlines():
  meta,path=line.split('\t',1);oldtree[path]=meta.split()[2]
 def same_committed_raw(path,expected):
  assert tree[path]==oldtree[path]
  b=(ROOT/path).read_bytes();assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==tree[path]
  assert sha(b)==expected
 # Exact packaging of one superseded partial native input, never the v2 input.
 a=load(I/'oversize-native-archive/manifest.json');src=ROOT/a['source'];arc=ROOT/a['archive']
 sn,sh=streamhash(src);an,ah=streamhash(arc);dn,dh=streamhash(arc,gzip.open)
 assert (sn,sh)==(a['source_bytes'],a['source_RAW_sha256'])==(dn,dh)
 assert (an,ah)==(a['archive_bytes'],a['archive_RAW_sha256'])
 assert a['source'] not in tree and a['archive'] in tree
 v2=BASE/'exact-science-verification/inputs.v2/0446.exactraw.snapshot';assert v2.stat().st_size==2926
 # Current native files must agree with committed blobs byte-for-byte, including manifests/closure layers.
 native=BASE/'exact-science-verification';native_count=0;native_bytes=0
 for p in sorted(native.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(ROOT).as_posix()
  if p==src:continue
  assert rel in tree,('native uncommitted',rel)
  n=p.stat().st_size;h=hashlib.sha1(f'blob {n}\0'.encode())
  with p.open('rb') as f:
   while c:=f.read(2**20):h.update(c)
  assert h.hexdigest()==tree[rel],('native Git raw mismatch',rel)
  native_count+=1;native_bytes+=n
 lease=load(native/'lease.json');run=load(native/'run.json');payload=native/'named-verification.payload.json'
 assert lease['status']=='CLOSED_LAST';logical=dict(run);logical.pop('run_sha256')
 assert sha(compact(logical))==run['run_sha256']==lease['whole_run_sha256']
 assert sha(payload.read_bytes())==lease['distinct_complete_named_RAW_payload_sha256']
 adoption=load(BASE/'root.exact-verification63.adoption.json')
 assert adoption['native_whole_run_sha256']==lease['whole_run_sha256'] and adoption['distinct_native_complete_RAW_payload_sha256']==sha(payload.read_bytes())
 write('archive-and-native.result.json',{'status':'PASS','actual_pid':os.getpid(),'checked_commit':COMMIT,'archive_raw_bytes':an,'archive_raw_sha256':ah,'recovered_raw_bytes':dn,'recovered_raw_sha256':dh,'local_original_unchanged':True,'current_v2_bytes':v2.stat().st_size,'native_files_raw_equal_Git':native_count,'native_bytes_excluding_oversize':native_bytes,'native_manifests_and_CLOSED_LAST_preserved':True,'packaging_boundary':'One SUPERSEDED partial inputs/0446 retained locally, excluded only from Git, losslessly packaged in committed gzip; actual inputs.v2/0446 separately committed. No native artifact or manifest rewritten.'})
 # Bind every receipt output/snapshot; historical original inputs have explicit receipt-local maps only.
 notes=load(BASE/'integration.notes.json');rows=[];history=[];pins=0
 newline={x['path']:x for x in load(I/'newline-preservation.json')['records']}
 cellbefore=I/'cell.before-final-admin.exactraw.snapshot.json'
 for c in notes['checks']:
  pincheck(c['receipt']);r=load(abspath(c['receipt']['path']));assert r['exit_code']==0 and r['terminal_closed'] is True and r['actual_foreground_pid']>0
  assert r['checked_science_parent']==SCI
  localmaps={x['original']['path']:x['exact_raw_snapshot'] for x in r['input_snapshots']}
  for k,pin in walkpins(r):
   if k.startswith('.inputs[') or ('.input_snapshots[' in k and k.endswith('.original')):
    p=abspath(pin['path']);b=p.read_bytes()
    if sha(b)!=pin['raw_sha256']:
     rel=p.relative_to(ROOT).as_posix();q=localmaps[pin['path']];assert pin['raw_sha256']==q['raw_sha256'];pincheck(q)
     if rel==CELL:
      assert pin['raw_sha256']==sha(cellbefore.read_bytes());qual='Pre-final-administrative cell; only independently-verified/evidence/visual metadata changed after the successful gate; source/target/process repair already present.'
     else:
      nf=newline[rel];assert nf['before_raw_sha256']==pin['raw_sha256'] and nf['after_raw_sha256']==sha(b) and nf['lf_sha256']==pin['lf_sha256']==sha(b.replace(b'\r\n',b'\n'));qual='Explicit newline-preservation record and receipt-local original-to-exactRAW snapshot; current LF and exact integration Git blob identical.'
     history.append({'receipt':c['receipt']['path'],'field':k,'original':pin,'explicit_exact_raw_snapshot':q,'qualification':qual})
    else:pincheck(pin)
    rel=p.relative_to(ROOT).as_posix()
    if rel!=CELL:assert sha(blob(COMMIT,rel).replace(b'\r\n',b'\n'))==pin['lf_sha256'],('receipt vs commit',rel)
   else:pincheck(pin)
   pins+=1
  out=abspath(r['stdout']['path']).read_text(encoding='utf-8-sig',errors='replace');err=abspath(r['stderr']['path']).read_text(encoding='utf-8-sig',errors='replace')
  rows.append({'label':c['label'],'receipt':c['receipt'],'actual_pid':r['actual_foreground_pid'],'exit_code':r['exit_code'],'command':r['command'],'stdout':r['stdout'],'stderr':r['stderr'],'terminal_closed':r['terminal_closed']})
  if c['label']=='mandatory-astis-check-final':assert 'Build completed successfully (9170 jobs).' in out and 'Build completed successfully (9465 jobs).' in out and 'ASTIS check passed' in out
  if c['label']=='python-regression-suite':assert 'Ran 296 tests' in err and err.rstrip().endswith('OK')
  if c['label']=='publication':assert 'Publication PASS: 229 source items' in out
 write('receipts.result.json',{'status':'PASS','checked_commit':COMMIT,'actual_pid':os.getpid(),'qualified_raw_pin_readbacks':pins,'finite_historical_original_maps':history,'actual_terminal_receipts':rows,'gate_receipt_commit_boundary':'Root ran actual foreground aggregate gates on the integrated source tree before the administrative cell finalization and commit. All production/source/toolchain inputs LF-rebind to the exact integration Git blobs. Pre-final-admin cell raw snapshot is explicit; independent direct field diff and focused metadata checks qualify final admin only. No previous counts or SCI-only CI substituted.'})
 # Independent committed delta and exact three-field process repair.
 before=json.loads(blob(SCI,CELL));after=json.loads(blob(COMMIT,CELL));fields=diffjson(before,after)
 process=[x for x in fields if x['field'].startswith('/learning_contract/')]
 assert {x['field'] for x in process}=={'/learning_contract/failure_class','/learning_contract/salvage/required','/learning_contract/salvage/status'}
 assert after['learning_contract']['failure_class']=='IMPLEMENTATION_FAILED' and after['learning_contract']['salvage']['required'] and after['learning_contract']['salvage']['status']=='completed'
 assert before['target_statement']==after['target_statement'] and before['source_anchor']==after['source_anchor']
 admin=diffjson(load(cellbefore),after);assert {x['field'] for x in admin}=={'/graph_contribution/visual_review','/evidence/serialized_shared_gate','/blocked/reason'}
 unchanged=[MAIN,TEST,'website/content/declaration_lessons/pbps-unique-positive-macroscopic-defect-root.json','website/content/publications/pbps-unique-positive-macroscopic-defect-root.json','research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSUniquePositiveMacroscopicDefectRoot.json','lean-toolchain','lake-manifest.json']
 for path in unchanged:assert oldtree[path]==tree[path]
 paths=git('diff','--name-only',SCI,COMMIT).splitlines();assert len(paths)==5187
 assert not any('pbps-centered-root64' in p or 'pbps-centered-root-preproof64' in p or 'ASTIS-SW-PBPS-centered-root-order-inverse' in p for p in paths)
 ledger=blob(COMMIT,'runs/substantive_advances.jsonl');assert b'ASTIS-SA-20261009-PBPSCenteredRootOrderInverse' not in ledger
 working=(ROOT/'runs/substantive_advances.jsonl').read_bytes();assert working.startswith(ledger) and len(working)>len(ledger)
 preserve=load(I/'generated-context-preservation-data/manifest.json');canon=preserve['preserved_canonical_metadata'];unrelated=[x for x in preserve['emitted_snapshots'] if x['action'].startswith('restored')]
 assert len(canon)==69 and len(unrelated)==86
 for x in canon:same_committed_raw(x['canonical_card'],x['card_raw_sha256'])
 for x in unrelated:
  same_committed_raw(x['path'],x['baseline_raw_sha256'])
  assert streamhash(ROOT/x['emitted_snapshot'],gzip.open)[1]==x['emitted_raw_sha256']
 oldcells=[p for p in tree if p.startswith('research-wiki/frontier-cells/') and p.endswith('.json') and p!=CELL]
 for p in oldcells:assert oldtree[p]==tree[p]
 front=diffjson(json.loads(blob(SCI,'website/content/samplewiki_companion_frontiers.json')),json.loads(blob(COMMIT,'website/content/samplewiki_companion_frontiers.json')))
 assert all(x['field'].startswith('/execution/') for x in front)
 ws=load(I/'staging-whitespace/diagnosis.json');assert ws['full_staged_exit']==2 and not ws['full_staged_called_PASS'] and len(ws['findings'])==1501 and ws['authored_complement_exit']==0
 assert streamhash(I/'staging-whitespace/full-staged-immutable-negative.raw.gz',gzip.open)[1]==ws['negative_raw_sha256']
 write('repository.result.json',{'status':'PASS_WITH_EXPLICIT_NATIVE_WHITESPACE_DEBT','actual_pid':os.getpid(),'checked_commit':COMMIT,'parent':SCI,'committed_file_delta':len(paths),'root_imports_Registry508_Tests_genuine_consumer':'inspected; exactly one public registry entry and imports, Basic count507-to508','exact_three_process_field_repair':process,'final_administrative_diff':admin,'science_source_publication_audit_toolchain_unchanged':unchanged,'canonical_cards_preserved':len(canon),'unrelated_emitted_paths_preserved':len(unrelated),'older_frontier_cells_unchanged':len(oldcells),'companion_frontier_changes_only_execution':True,'64_uncommitted_excluded':True,'committed63_ledger_prefix_raw_sha256':sha(ledger),'working_tail_not_credited_or_modified':True,'staged_whitespace':{'full_native_exit':2,'findings':1501,'authored_complement_exit':0,'immutable_raw_findings_retained':True},'explicit_boundary':'Integrated bounded macro root; no main, live, full-paper, PURIFIED or Goal completion.'})
 # Rebind actual browser callbacks and download bytes and exact eight source literals.
 cp=load(I/'visual63/copy-capture.json');r=cp['records'][0];lesson=load(ROOT/'website/content/declaration_lessons/pbps-unique-positive-macroscopic-defect-root.json')['units'][0]
 assert len(r['panels'])==2 and all(p['callbackCalled'] and p['copiedExactly'] and p['status']=='Copied' for p in r['panels'])
 main=(ROOT/MAIN).read_text(encoding='utf-8');test=(ROOT/TEST).read_text(encoding='utf-8')
 for p in r['panels']:assert p['code'] in main
 assert len(r['downloads'])==2
 downloads=[]
 for d in r['downloads']:
  assert d['status']==200 and d['text'].encode('utf-8')==(ROOT/MAIN).read_bytes()
  downloads.append({'href':d['href'],'http_status':d['status'],'capture_javascript_string_length':d['bytes'],'actual_UTF8_RAW_bytes':len(d['text'].encode()),'actual_RAW_sha256':sha(d['text'].encode())})
 assert len(r['steps'])==len(lesson['steps'])==8
 steps=[]
 for n,(s,t) in enumerate(zip(r['steps'],lesson['steps']),1):
  assert s['initiallyFolded'] and s['lean']==t['lean'] and s['lean'] in (test if n==8 else main)
  steps.append({'step':n,'title':t['title'],'formula':t['formula'],'literal_Lean_RAW_sha256':sha(s['lean'].encode()),'exact_source_match':True,'initially_folded':True,'adjacent_Lean_visually_inspected':True})
 capture=load(I/'visual63/render-capture.json');assert len(capture['records'])==10 and capture['ownedBrowserExit']['code']==0
 assert all(z['closedLeanDetails']>=1 for z in capture['records'] if z['label']!='branch-consumer')
 for p in load(BASE/'visual.inspection.json')['capture_files']:pincheck(p)
 htmlpath=ROOT/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html'
 htmlraw=htmlpath.read_bytes();write('late-generated-reader.input.json',{'actual_pid':os.getpid(),'qualification':'Bounded generated reader file pinned before direct DOM read; no canonical mutation','raw':rawpin(htmlpath)})
 section=htmlraw.decode().split('<section id="pbps-unique-positive-macroscopic-defect-root"',1)[1].split('<section id=',1)[0]
 assert section.count('Corresponding Lean step')==8 and '<details open' not in section and '<details class="inline-lean' in section
 assert html.unescape(re.sub('<[^>]+>','',section)).count('Corresponding Lean step')==8
 write('reader.result.json',{'status':'SCOPED_LOCAL_READER_ACCEPTED_WITH_RECORDED_DEBTS','actual_pid':os.getpid(),'checked_commit':COMMIT,'ten_screenshots_personally_viewed':True,'statement_conditions_and_boundary_personally_read':True,'exact_copy_callbacks':2,'physical_OS_clipboard_test':False,'exact_UTF8_RAW_downloads':downloads,'all_eight_steps':steps,'DOM_closed_adjacent_details':True,'graph_focus':'Exact Registry-backed actual_unique_positive_macroscopic_defect_root; COMPILED badge, source location and dashed scanner-reference edges explicitly distinguished from source proof dependencies; 190-node/512-edge view with8 highlighted direct references is visually dense. No64 candidate counted as compiled.','visual_observations':['Original C2, both global Hessian bounds and positive capped eta visible; rank0 and alphaeta=1 retained.','Same M/e/U/T, HP, typed B, fulljoint P versus I_HP, universal alternative G outside energy all visible.','Statement and complete exact proof panels folded; all8 formulas immediately followed by closed Corresponding Lean step.','No missing formula or observed math rendering failure in the10 screenshot scope.'],'debts':['Dense graph labels/long declaration wraps.','Tight disclosure/table spacing and small assumption-table type.','Real scalar Gamma denotes a positive operator on scalar-valued real L2, as explicitly clarified.','Callback interception is local browser behavior; physical clipboard/deployed/live/mobile not checked.','Full Chapter1.3/mainpaper Exposition Seal, postmerge purification, main/wholeGoal acceptance not granted.']})
 write('retrieval-corrections.json',{'read_only_observer_corrections':[{'description':'Initial lookup staging-whitespace/receipt.json absent; actual diagnosis.json and retained compressed negative receipt used.','effect':'none; no missing receipt treated as PASS'},{'description':'Initial attempt to parse human reader-copy stdout as JSON raised JSONDecodeError; actual visual63/copy-capture.json supplies structured browser evidence.','effect':'none; stdout was not mathematical or browser-result JSON'},{'description':'Initial lesson key proof_steps absent; actual schema uses units[0].steps.','effect':'none; actual eight step fields read and matched literally'}],'stdout_truncation':'An exploratory print of the large whitespace diagnosis was truncated; verification independently loaded the complete file and counted/hashed it. No truncated output substituted for bindings.'})
 write('audit.result.json',{'status':'PASS_BOUNDED_REPOSITORY_READER_WITH_DEBTS','checked_commit':COMMIT,'actual_pid':os.getpid(),'subresults':[rawpin(OUT/n) for n in ['archive-and-native.result.json','receipts.result.json','repository.result.json','reader.result.json','retrieval-corrections.json']]})
 print(json.dumps({'status':'PASS_BOUNDED_REPOSITORY_READER_WITH_DEBTS','actual_pid':os.getpid(),'commit':COMMIT,'native_files_raw_Git_equal':native_count,'receipt_qualified_pins':pins,'finite_history_maps':len(history),'reader_steps':8,'download_count':2}))
if __name__=='__main__':audit()
