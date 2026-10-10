import pathlib,json,hashlib,subprocess,os,gzip,re
from datetime import datetime,timezone
ROOT=pathlib.Path('E:/Samplinglib'); P=ROOT/'runs/20261007-companion-priority/pbps-gaussian-reflected-mean52';OUT=P/'exact-verification52';OUT.mkdir(exist_ok=True)
COMMIT='a18cd1cf8e8310f228391d4c53a2ac8f1a8900ec'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'bytes':len(b)}
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
write(OUT/'lease.json',{'status':'OPEN','owner':'whole_math52','opened_utc':now(),'verified_commit':COMMIT,'scope':'Independent exact scientific commit verification52; only authorized52 evidence/cell/VERIFIED writes','Python_pid':os.getpid()})
assert git('rev-parse','HEAD').decode().strip()==COMMIT
assert not git('status','--porcelain','--untracked-files=no').strip()
source=read(P/'source.0.review.json');auditpath=ROOT/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261007-GaussianReflectedMean.json';audit=read(auditpath)
if 'audits' in audit:audit=audit['audits'][0]
print('AUDIT SUMMARY',json.dumps({k:v for k,v in audit.items() if not isinstance(v,(dict,list))},ensure_ascii=False));print('AUDIT KEYS',list(audit))
print('SOURCE VERDICT',source['verdict'],source['reviewer'],source['publication_binding_sha256'])
assert source['blocking'] is False and source['verdict']=='equivalent-after-elaboration' and len(source['semantic_slots'])==7 and not source['deltas'] and not source['repairs'] and not source['source_excess']
frozen=read(P/'math-freeze.json');freezechecks=[];changed=[]
snapmap={r['input_path'].replace('\\','/'):r['snapshot'] for r in source['raw_snapshot_bindings']}
for e in frozen['inputs']:
 current=pin(ROOT/e['path']);row={'original':e,'current':current,'same':current==e}
 if not row['same']:
  path=(ROOT/e['path']).as_posix();s=snapmap.get(path)
  assert s is not None,'missing strict source snapshot for changed '+path
  actual=pin(pathlib.Path(s['path']))
  assert all(actual[k]==e[k] for k in ['raw_sha256','lf_sha256','bytes']),'snapshot not original freeze'
  row['preserved_original_snapshot']=actual
  changed.append(row)
 freezechecks.append(row)
assert len(freezechecks)==333
print('FREEZE CHANGED',[(r['current']['path'],r['preserved_original_snapshot']['path']) for r in changed])
write(OUT/'freeze.input-bindings.json',{'freeze':pin(P/'math-freeze.json'),'strict_original_inputs':333,'current_unchanged_count':333-len(changed),'changed_admission_inputs':changed,'inputs':freezechecks})
paths=[
 'AutoSamplingTheory/TechnicalLemmas/Measure/GaussianReflectedMean.lean','Tests/ProximalBPSGaussianReflectedMean.lean','lean-toolchain','lake-manifest.json',
 'website/content/declaration_lessons/gaussian-reflected-mean.json','website/content/publications/gaussian-reflected-mean.json',
 'research-wiki/frontier-cells/ASTIS-SHARED-gaussian-reflected-mean.json',auditpath.relative_to(ROOT).as_posix(),
 (P/'proved-local.json').relative_to(ROOT).as_posix(),(P/'source.0.review.json').relative_to(ROOT).as_posix(),(P/'publication-plan.json').relative_to(ROOT).as_posix(),(P/'math-freeze.json').relative_to(ROOT).as_posix()]
bindings=[]
for name in paths:
 current=pin(ROOT/name);blob=git('show',COMMIT+':'+name);blf=blob.replace(b'\r\n',b'\n')
 assert sha(blf)==current['lf_sha256'],'Git/worktree divergence '+name
 bindings.append({'current':current,'commit':COMMIT,'blob_id':git('rev-parse',COMMIT+':'+name).decode().strip(),'blob_raw_sha256':sha(blob),'blob_lf_sha256':sha(blf),'blob_bytes':len(blob),'LF_identical':True})
write(OUT/'git.input-bindings.json',{'commit':COMMIT,'tracked_tree_initially_clean':True,'bindings':bindings})
prior=read(P/'whole-proof-review52/lease.json');assert prior['status']=='CLOSED'
for e in prior['actual_final_outputs']:assert pin(ROOT/e['path'])==e
priorrun=read(P/'whole-proof-review52/run.json');h=priorrun.pop('run_sha256');assert sha(json.dumps(priorrun,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==h
native=[]
for name,field in [('source.0.review.json','review_run_sha256'),('reviewer.source.run.json','run_sha256'),('reviewer.source.lease.json','lease_run_sha256'),('source.review.lease.json','lease_run_sha256')]:
 obj=read(P/name);expected=obj.pop(field);actual=sha(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode());assert actual==expected,name+' logical hash';native.append({'file':pin(P/name),'hash_field':field,'logical_hash':actual})
for name in ['reviewer.source.lease.json','source.review.lease.json','anonymous-decoder/lease.json','whole-proof-review52/compiler.lease.json']:
 assert read(P/name)['status']=='CLOSED'
write(OUT/'prior-native-validation.json',{'whole_math_outputs_all_exact':True,'whole_math_run_sha256':h,'native_source_logical_hashes':native,'all_relevant_leases_closed':True})
prod=(ROOT/paths[0]).read_text(encoding='utf-8');sig=prod[prod.index('theorem gaussian_reflected_mean_c1'):].split('\n := by',1)[0]+'\n';assert len(sig.encode())==497 and sha(sig.encode())=='50ca5c7e0b5aed0f892d2e686fd276b11a586b30745d8edd2d5c1256d7e09d11'
hits=[]
for name in paths[:2]:
 for i,line in enumerate((ROOT/name).read_text(encoding='utf-8').splitlines(),1):
  if re.search(r'\b(axiom|sorry|admit|unsafe)\b|Prop\s*:=\s*True|:=\s*trivial',line):hits.append({'path':name,'line':i,'text':line})
assert not hits
write(OUT/'fake-closure-scan.json',{'commit':COMMIT,'sources':[pin(ROOT/n) for n in paths[:2]],'forbidden_hits':hits,'exact_header_LF_bytes':497,'exact_header_sha256':sha(sig.encode()),'production_private_or_local_instance':bool(re.search(r'\bprivate\b|local instance',prod))})
ws=read(P/'whitespace-diagnosis52/diagnosis.json');gz=ROOT/ws['gzip']['path'];assert sha(gz.read_bytes())==ws['gzip']['raw_sha256'];negative=gzip.decompress(gz.read_bytes());assert sha(negative)==ws['full_negative_raw_sha256'];assert ws['findings']==787 and ws['full_staged_exit']==2
print('WS KEYS',list(ws));print('WS NESTED',[(k,len(v)) for k,v in ws.items() if isinstance(v,(list,dict))])
cmd=ws['authored_check_command']; exclusions=[a for a in cmd if a.startswith(':(exclude)')]
assert len(exclusions)==94
wcmd=['git','-c','core.whitespace=cr-at-eol','diff',COMMIT+'^',COMMIT,'--check','--','.',*exclusions]
r=subprocess.run(wcmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(OUT/'authored-whitespace.log').write_bytes(r.stdout);assert r.returncode==0
write(OUT/'authored-whitespace.status.json',{'command':wcmd,'exit_code':r.returncode,'log':pin(OUT/'authored-whitespace.log'),'negative_findings':787,'negative_paths':94,'diagnosis':pin(P/'whitespace-diagnosis52/diagnosis.json'),'gzip':pin(gz),'decompressed_raw_sha256':sha(negative),'full_staged_whitespace_PASS':False,'scope':'Exact committed authored diff with only94 explicit preserved evidence paths excluded; no blanket runs exclusion.'})
print('PASS exact Git/header/fake-scan/native leases/logical hashes,333 frozen originals mapped,authored whitespace')
