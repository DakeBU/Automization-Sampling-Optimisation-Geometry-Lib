import os,sys,json,pathlib,hashlib,subprocess,gzip,re,datetime
ROOT=pathlib.Path('E:/Samplinglib')
R=ROOT/'runs/20261007-companion-priority/pbps-ambient-adjoint66'
O=R/'independent-repository-exposition66'
SCI='a115115d42b3fa2b67885d87fe4d5300af36fcd1'
INT='eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176'
SCI64='59fff63d320aa5e3dc4b45e81e40e2029ce42734'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(j):return json.dumps(j,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')
def lf(b):return b.replace(b'\r\n',b'\n')
def pin(p,b=None):
 p=pathlib.Path(p);b=p.read_bytes() if b is None else b
 return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_bytes=len(lf(b)),LF_sha256=sha(lf(b)))
def write(n,j): (O/n).write_bytes(json.dumps(j,ensure_ascii=False,sort_keys=True,indent=2).encode()+b'\n')
def read(p):return json.loads(pathlib.Path(p).read_bytes())
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
batch=subprocess.Popen(['git','cat-file','--batch'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
def blob(c,p):
 batch.stdin.write((c+':'+p+'\n').encode());batch.stdin.flush();h=batch.stdout.readline().split()
 if h[-1]==b'missing':return None
 b=batch.stdout.read(int(h[2]));assert batch.stdout.read(1)==b'\n';return b
selected=[]
def capture(p):
 p=pathlib.Path(p);p=p if p.is_absolute() else ROOT/p
 b=p.read_bytes();i=len(selected);a=O/'inputs';a.mkdir(exist_ok=True)
 raw=a/f'{i:03}.RAW.snapshot';normal=a/f'{i:03}.LF.snapshot';raw.write_bytes(b);normal.write_bytes(lf(b))
 z={'original':pin(p,b),'RAW_snapshot':pin(raw,b),'LF_snapshot':pin(normal,lf(b))};selected.append(z);return json.loads(b) if p.suffix=='.json' else b
def match(p,z):
 b=pathlib.Path(p).read_bytes();h=z.get('raw_sha256',z.get('RAW_sha256'));n=z.get('raw_bytes',z.get('RAW_bytes',z.get('bytes')))
 assert sha(b)==h,(str(p),'RAW',sha(b),h)
 if n is not None:assert len(b)==n,(str(p),'bytes',len(b),n)
 h=z.get('lf_sha256',z.get('LF_sha256'))
 if h:assert sha(lf(b))==h,(str(p),'LF')
 return b
def recpins(j):
 if isinstance(j,dict):
  if 'path' in j and ('raw_sha256' in j or 'RAW_sha256' in j):yield j
  for v in j.values():yield from recpins(v)
 elif isinstance(j,list):
  for v in j:yield from recpins(v)
def logical(p):
 j=read(p);expected=j['run_sha256'];del j['run_sha256'];actual=sha(canon(j));assert actual==expected,(str(p),actual,expected);return actual
def native(d):
 p=R/d;lease=capture(p/'lease.final.json');bad=[]
 if 'all_owned_except_this_final_lease' in lease:
  entries=lease['all_owned_except_this_final_lease'];names=[]
  for z in entries:match(z['path'],z);names.append(pathlib.Path(z['path']).resolve())
  actual={q.resolve() for q in p.rglob('*') if q.is_file()};assert actual==set(names)|{(p/'lease.final.json').resolve()},d
 else:
  m=capture(p/'owned-manifest.json');entries=m['regular_file_entries']
  for z in entries:match(p/z['name'],z)
  actual={q.relative_to(p).as_posix() for q in p.rglob('*') if q.is_file()}
  assert actual=={z['name'] for z in entries}|{'owned-manifest.json','lease.final.json'},d
  assert sha((p/'owned-manifest.json').read_bytes())==lease['manifest_RAW_sha256']
 run=p/('run.json' if (p/'run.json').exists() else 'review-run.json')
 l=logical(run);assert l==lease['whole_logical_run_sha256']
 return {'folder':p.as_posix(),'files':len(actual),'lease':pin(p/'lease.final.json'),'whole_logical_run_sha256':l,'status':lease['status'],'close_PID':lease.get('actual_close_pid',lease.get('actual_lease_writer_pid')),'readback_PID':lease.get('actual_readback_pid'),'finalizer_PID':lease.get('actual_finalizer_pid'),'all_owned_bytes_verified':True}

started=datetime.datetime.now(datetime.timezone.utc).isoformat()
print(json.dumps({'actual_foreground_PID':os.getpid(),'stage':'finite-audit-start'}),flush=True)
assert git('show','-s','--format=%P',INT).decode().strip()==SCI
paths=git('diff','--name-only','-z',SCI,INT).decode().split('\0')[:-1]
entries=[];drifts=[]
for p in paths:
 b=blob(INT,p);assert b is not None
 current=(ROOT/p).read_bytes();z={'path':p,'Git_INT':pin(p,b),'current':pin(ROOT/p,current),'current_equals_Git_RAW':current==b}
 if current!=b:
  if p=='runs/substantive_advances.jsonl':
   assert current.startswith(b),'ledger prefix mutation'
   suffix=current[len(b):];events=[json.loads(x) for x in suffix.splitlines() if x.strip()]
   assert events and all(x.get('advance_id')=='ASTIS-SA-20261009-PBPSActualRootInverseCommutation' for x in events),[x.get('advance_id') for x in events]
   (O/'future67.current-ledger-suffix.RAW.jsonl').write_bytes(suffix)
   z['finite_current_mapping']={'kind':'exact_INT_prefix_plus_future67_events','suffix':pin(O/'future67.current-ledger-suffix.RAW.jsonl',suffix),'events':events,'outside_INT66_proof_publication':True}
  else:raise AssertionError(('unmapped current commit drift',p))
  drifts.append(z)
 entries.append(z)
write('exact-commit-files.RAW-LF-map.json',{'schema':'INT66-all1484-exact-commit-paths-v1','SCI_parent':SCI,'INT':INT,'paths':entries,'count':len(entries),'no_folder_exclusion':True,'current_drift':drifts})
authored=[p for p in paths if not p.startswith('runs/')]+['runs/substantive_advances.jsonl']
science=[]
freeze=capture(R/'math-freeze.json')
for z in freeze['inputs']:
 p=pathlib.Path(z['path']).relative_to(ROOT).as_posix()
 if p.startswith(('AutoSamplingTheory/','Tests/','website/content/declaration_lessons/','website/content/theorem_publications/','website/content/semantic_roundtrip/')):
  a=blob(SCI,p);b=blob(INT,p)
  assert a is not None and a==b,(p,'science changed')
  assert (ROOT/p).read_bytes()==b,(p,'current science changed')
  science.append({'path':p,'Git_SCI_equals_INT_equals_current_RAW':True,'pin':pin(ROOT/p,b)})
write('science-unchanged.json',{'exact_commit':INT,'parent':SCI,'selected_science':science,'mathematical_verdict_reused_no_new_proof':True})
scripts=git('ls-tree','-r','--name-only','-z',INT,'--','tools','website/scripts').decode().split('\0')[:-1]
assert git('diff','--name-only',SCI64,INT,'--','tools','website/scripts')==b''
sp=[]
for p in scripts:
 a=blob(INT,p);assert a==blob(SCI64,p);c=(ROOT/p).read_bytes()
 assert lf(c)==lf(a),(p,'script semantic drift')
 sp.append({'path':p,'SCI64_INT_RAW':pin(p,a),'current_RAW_LF':pin(ROOT/p,c),'current_RAW_equal_Git':c==a})
prior=capture(ROOT/'runs/20261007-companion-priority/pbps-centered-root64/integration64/python-regression-suite/receipt.json')
assert prior['exit_code']==0
priorlog=pathlib.Path(prior['stderr']['path']).read_bytes();assert b'Ran 296 tests' in priorlog and priorlog.rstrip().endswith(b'OK')
write('python296-exact-reuse.json',{'status':'REUSED_NOT_RERUN','complete_tracked_tools_and_site_script_inventory':sp,'file_count':len(sp),'SCI64':SCI64,'INT':INT,'exact_Git_bytes_unchanged':True,'prior_receipt_PID':prior.get('actual_foreground_pid'),'prior_receipt_exit':0,'test_count':296,'prior_stderr':pin(prior['stderr']['path'],priorlog)})
notes=capture(R/'integration.notes.json');receipts=[];snapshotmaps=[]
for c in notes['checks']+[{'label':x,'receipt':{'path':(R/'integration66'/x/'receipt.json').as_posix()}} for x in ['contributor-final-admin','publication-final-admin','frontier-final-admin','official-graph-ci-output','official-graph-ci-output-final']]:
 p=pathlib.Path(c['receipt']['path']);p=p if p.is_absolute() else ROOT/p
 if 'raw_sha256' in c['receipt']:match(p,c['receipt'])
 j=capture(p)
 for k in ['stdout','stderr']:
  z=j[k];match(z['path'],z)
  if k in c:match(z['path'],c[k])
 for z in j.get('input_snapshots',[]):
  orig=z['original'];raw=z['exact_raw_snapshot'];norm=z['LF_snapshot']
  rb=match(raw['path'],raw);nb=match(norm['path'],norm)
  assert sha(rb)==orig['raw_sha256'] and len(rb)==orig.get('bytes',orig.get('raw_bytes'))
  assert nb==lf(rb) and sha(nb)==orig['lf_sha256']
  cp=pathlib.Path(orig['path']);cp=cp if cp.is_absolute() else ROOT/cp
  cb=cp.read_bytes();mapping={'label':c['label'],'original_pin':orig,'exact_RAW_snapshot':raw,'exact_LF_snapshot':norm,'current':pin(cp,cb),'current_RAW_equal_original':cb==rb}
  if cb!=rb:
   if cp.name=='substantive_advances.jsonl':
    assert cb.startswith(rb);suffix=cb[len(rb):];mapping['kind']='historical exact prefix plus explicitly inventoried transition/future events';mapping['suffix_sha256']=sha(suffix);mapping['suffix_events']=[json.loads(x) for x in suffix.splitlines() if x.strip()]
   elif cp.relative_to(ROOT).as_posix()=='research-wiki/frontier-cells/ASTIS-SW-PBPS-ambient-adjoint-corrector.json':
    def diffs(a,b,k=''):
     if isinstance(a,dict) and isinstance(b,dict):
      out=[]
      for key in sorted(set(a)|set(b)):
       if key not in a or key not in b:out.append({'field':k+'/'+key,'before':a.get(key),'current':b.get(key)})
       else:out.extend(diffs(a[key],b[key],k+'/'+key))
      return out
     return [] if a==b else [{'field':k,'before':a,'current':b}]
    delta=diffs(json.loads(rb),json.loads(cb));assert {x['field'] for x in delta}=={'/evidence/serialized_shared_gate','/graph_contribution/visual_review','/blocked/reason'}
    mapping['kind']='explicit receipt historical snapshot to exact INT cell: three shared-admission metadata fields only'
    mapping['exact_delta']=delta
   else:raise AssertionError(('unmapped gate input drift',str(cp),c['label']))
  snapshotmaps.append(mapping)
 receipts.append({'label':c['label'],'receipt':pin(p),'actual_foreground_PID':j['actual_foreground_pid'],'exit':j['exit_code'],'terminal_closed':j['terminal_closed'],'command':j['command'],'stdout':j['stdout'],'stderr':j['stderr'],'snapshot_count':len(j.get('input_snapshots',[]))})
assert all(z['exit']==0 for z in receipts[:15]);assert [z['exit'] for z in receipts[15:]]==[1,1]
write('root-gates-and-finite-snapshot-maps.json',{'root_gates':receipts,'exact_snapshot_maps':snapshotmaps,'all_RAW_LF_snapshot_pairs_verified':True,'no_broad_folder_exclusions':True})
diag=capture(R/'integration66/staging-whitespace/diagnosis.json');p=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--check',SCI,INT],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(O/'independent-whitespace-full.stdout.RAW.log').write_bytes(p.stdout);(O/'independent-whitespace-full.stderr.RAW.log').write_bytes(p.stderr)
finding=[]
for line in p.stdout.decode().splitlines():
 m=re.match(r'^(.*?):(\d+): (trailing whitespace|new blank line at EOF)\.?$',line)
 if m:finding.append({'path':m[1],'line':int(m[2]),'kind':m[3]})
assert p.returncode==2 and len(finding)==356,(p.returncode,len(finding))
assert finding==diag['findings'],'whitespace finding mismatch'
negative=gzip.decompress((R/'integration66/staging-whitespace/full-staged-immutable-negative.raw.gz').read_bytes());assert sha(negative)==diag['negative_RAW_sha256']
excluded=[x['path'] for x in diag['exact_immutable_raw_paths']]
assert set(x['path'] for x in finding)==set(excluded)
for x in diag['exact_immutable_raw_paths']:assert sha((ROOT/x['path']).read_bytes())==x['raw_sha256']
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--check',SCI,INT,'--','.',*[':(exclude)'+x for x in excluded]],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
(O/'independent-whitespace-complement.stdout.RAW.log').write_bytes(q.stdout);(O/'independent-whitespace-complement.stderr.RAW.log').write_bytes(q.stderr);assert q.returncode==0
write('whitespace-typed.json',{'actual_auditor_PID':os.getpid(),'explicit_git_policy':'core.whitespace=cr-at-eol','full_exact_commit_check_exit':p.returncode,'full_staged_PASS':False,'finding_count':len(finding),'findings':finding,'exact_three_immutable_RAW_exclusions':diag['exact_immutable_raw_paths'],'authored_complement_exit':q.returncode,'no_folder_exclusion':True,'root_negative_compressed':pin(R/'integration66/staging-whitespace/full-staged-immutable-negative.raw.gz'),'root_decompressed_RAW_sha256':sha(negative)})
native_results=[native(d) for d in ['exact-science-verification66','independent-math66','independent-source66']]
write('native-parent-closures.json',native_results)
capture(R/'root.exact-verification66.adoption.json');verified=capture(R/'verified.json');bindings=capture(R/'exact-science-verification66/bindings.result.json')
for z in recpins(bindings):match(z['path'],z)
event=pathlib.Path(verified['exact_appended_event']['path']).read_bytes() if 'exact_appended_event' in verified else (R/'exact-science-verification66/verified.appended-event.exactraw.jsonl').read_bytes()
a=blob(SCI,'runs/substantive_advances.jsonl');b=blob(INT,'runs/substantive_advances.jsonl');assert b==a+event
e=json.loads(event);assert e['worker_id']=='/root/exact_science63' and e['to_state']=='VERIFIED' and e['evidence']['verified_commit']==SCI
write('nonowner-VERIFIED-binding.json',{'SCI_ledger':pin('Git_SCI/runs/substantive_advances.jsonl',a),'INT_ledger':pin('Git_INT/runs/substantive_advances.jsonl',b),'exact_append':pin(R/'exact-science-verification66/verified.appended-event.exactraw.jsonl',event),'event':e,'prefix_preserved':True,'one_nonowner_VERIFIED_event':True,'this_reviewer_transition':False})
batch.stdin.close();batch.wait();write('inputs.manifest.json',{'schema':'repo66-finite-original-RAW-LF-input-map-v1','inputs':selected})
write('audit66.result.json',{'schema':'repo66-independent-finite-audit-v1','actual_foreground_PID':os.getpid(),'started_utc':started,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','commit_paths':len(paths),'authored_shared_paths':authored,'science_file_count':len(science),'script_file_count':len(scripts),'root_PASS_receipts':15,'retained_graph_NEGATIVE_receipts':2,'gate_snapshot_pairs':len(snapshotmaps),'native_parent_closures':native_results,'whitespace_findings':356,'full_staged_PASS':False,'canonical_Git_ledger_writes':False})
print(json.dumps({'PID':os.getpid(),'status':'PASS','paths':len(paths),'snapshot_pairs':len(snapshotmaps),'native_files':[x['files'] for x in native_results],'owned_inputs':len(selected)}))
