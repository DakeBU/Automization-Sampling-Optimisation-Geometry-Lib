"""Independent commit-bound bounded gates; reuse exact own proof evidence."""
from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R)
B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-cover79';O=B/'exact-commit-verification79';O.mkdir(exist_ok=True)
C='56e4b7e101a1016e03df2971018b1f018f03e6c1';BASE='cf847f70133d9eb47b4b2a9e12cb979b1ef1be07'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean';D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover'
CELL='ASTIS-SW-PBPS-actual-physical-time-cover';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualPhysicalTimeCover.json'
BIND='2d83e2bd8857f34d06176947dfbf85594073e988ca487c738714e5f7368ccb4c'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def info(p):
 p=Path(p);b=p.read_bytes();return dict(path=str(p),RAW_bytes=len(b),RAW_sha256=sha(b))
def save(n,v):
 p=O/n;assert not p.exists(),p;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
assert git('rev-parse','HEAD').decode().strip()==C
archives={e['raw_path']:e['archive'] for e in load(B/'immutable-log-archives79.json')['files']}
matches=[];runtime_only=[]
def exact(path,allow_runtime=False):
 p=Path(path);p=p if p.is_absolute() else R/p;rel=p.relative_to(R).as_posix();raw=p.read_bytes()
 q=subprocess.run(['git','show',C+':'+rel],cwd=R,capture_output=True);archived=False
 if q.returncode:
  if allow_runtime and p.suffix=='.pyc':
   runtime_only.append(dict(**info(p),scope='Administrative Python bytecode output, native hash checked locally; neither mathematical input nor Git proof certificate.'));return
  assert rel in archives,'Missing exact commit/archive binding '+rel
  blob=gzip.decompress(git('show',C+':'+archives[rel]));archived=True
 else:blob=q.stdout
 same=raw==blob;normalized=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
 assert same or (rel!=M and normalized),rel
 matches.append(dict(**info(p),git_blob_RAW_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archived))
science=[M,'lean-toolchain','lake-manifest.json',A,'website/content/declaration_lessons/pbps-actual-physical-time-cover.json','website/content/publications/pbps-actual-physical-time-cover.json']
for n in ['root.statement-seal79.json','claim.json','proved-local79.json','root.math79.adoption.json','root.decoder79.adoption.json','root.source79.adoption.json','source-review79.packet.json']:
 science.append((B/n).relative_to(R).as_posix())
for p in science:exact(p)
raw=(R/M).read_bytes();assert sha(raw)=='2f329dd32047f46adb81b65f51b9de56305021a944f7b8cdf62ae25665839c86'
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
summary=load(B/'independent-math79/fresh-compiler-dependency-summary79.json')
assert summary['status']=='PASS_FULL_SOURCE_STANDARD_THREE_EXACT_ACTUAL_PARENTS'
assert set(summary['axioms'])=={'propext','Classical.choice','Quot.sound'}
for n in ['fresh-whole-module-attempt2.receipt.json','kernel-local-proof-closure-attempt2.receipt.json']:
 p=B/'independent-math79'/n;r=load(p);assert r['exit_code']==0 and r['terminal_closed'];exact(p)
 for e in r['inputs']+[r['stdout'],r['stderr']]:
  assert info(e['path'])['RAW_sha256']==e['RAW_sha256'];exact(e['path'])
for n in ['decision79.json','whole-proof-mathematics79.json','statement-definition-audit79.json','fresh-compiler-dependency-summary79.json','closed-manifest79.json']:
 exact(B/'independent-math79'/n)
assert info(B/'independent-math79/decision79.json')['RAW_sha256']=='0a278d51e6459e0260d3ff6d1dc6dbb2d59d7a50b4fedc853a99825ebe731694'
source=load(B/'fresh-source79/source-review.run-manifest79.json')
for e in source['raw_inputs']+source['raw_outputs']:
 assert info(e['path'])['RAW_sha256']==e['raw_sha256'];exact(e['path'],allow_runtime=True)
for n in ['source-review.run-manifest79.json','source-review.run-evidence79.json','source-review.result79.json']:
 exact(B/'fresh-source79'/n)
chron=source['chronology'];assert chron['primary_read_first_before_any79_candidate_header_implementation_or_review'] and chron['source_first_seal_original_unchanged'] and chron['candidate_packet_first_read_only_after_freeze']
assert datetime.datetime.fromisoformat(chron['source_first_freeze_created_utc'])<datetime.datetime.fromisoformat(load(B/'root.statement-seal79.json')['sealed_utc'])
dec=load(B/'anonymous-decoder79/run-manifest.json')
assert dec['decoder']=='/root/blind_decoder79' and not dec['source_seen'] and not dec['identity_seen'] and not dec['proof_BODY_seen']
for n in ['run-manifest.json','decoded.json','reconstructed-theorem.txt','parent-packet.json']:
 p=B/'anonymous-decoder79'/n
 if p.exists():exact(p)
for e in dec['output_artifacts']:assert info(e['path'])['RAW_sha256']==e['raw_sha256']
packet_raw=Path(dec['mathematical_inputs'][0]).read_bytes();assert sha(packet_raw)==dec['packet_raw_sha256']
audit=load(R/A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND
assert audit['source_review']['reviewer']=='/root/fresh_source78'
assert audit['source_review']['reviewer_packet_sha256']=='a04fb9a861cac2368722a69b9c899fd43f4884e1d075ffe5beae9c300fc10455'
assert audit['source_review']['review_run_sha256']==info(B/'fresh-source79/source-review.run-evidence79.json')['RAW_sha256']
lesson=load(R/science[4])['units'][0];lines=raw.splitlines(keepends=True);regions=[]
for s in lesson['steps']:
 e=s['lean_source_region'];code=b''.join(lines[e['start_line']-1:e['end_line']])
 assert code==s['lean'].encode() and sha(code)==e['exact_code_raw_sha256'] and e['source_raw_sha256']==sha(raw)
 assert s['formula'] and s['text']
 regions.append(dict(title=s['title'],start=e['start_line'],end=e['end_line'],RAW_sha256=sha(code),formula=s['formula'],text=s['text']))
assert len(regions)==9 and regions[0]['start']==81 and regions[-1]['end']==210
assert b''.join(s['lean'].encode() for s in lesson['steps'])==b''.join(lines[80:210])
save('input-freeze79.json',dict(verified_commit=C,exact_commit_matches=matches,runtime_only_native_outputs=runtime_only,
 source_review_chronology=chron,nine_contiguous_BODY_formula_regions=regions,source_audit_state=audit['state'],
 reused_fresh_complete_source=info(B/'independent-math79/fresh-whole-module-attempt2.receipt.json'),
 reused_kernel_dependency_closure=info(B/'independent-math79/kernel-local-proof-closure-attempt2.receipt.json'),
 reuse_reason='Own unchanged native full-source elaboration/axioms and generated-proof dependency closure; every source/parent/seal/probe/toolchain/manifest/log hash checked and bound to this commit. No proof repeated or native reasoning trajectory fabricated.'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None)
env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  p=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',p.pid,flush=True);code=p.wait()
 save(n+'.receipt.json',dict(command=args,cwd=str(R),checked_commit=C,actual_foreground_PID=p.pid,exit_code=code,terminal_closed=True,
 started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))))
 print(n,'EXIT',code,flush=True);assert code==0,n+' failed; retained logs'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe')
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover']),
 ('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),
 ('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan79.json',dict(verifier_id='/root/exact_verify77',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits same scan as astis.py check',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(R/M)))
assert not hits and (R/M).read_bytes()==raw
assert git('rev-parse','HEAD').decode().strip()==C
save('checks-complete79.json',dict(status='PASS',verified_commit=C,verifier_id='/root/exact_verify77',publication_binding_sha256=BIND,
 reused_fresh_complete_source_and_kernel_dependency_closure=True,axioms=summary['axioms'],
 aggregate_and_site='Pending sole serialized stabilization lane; not run by bounded verifier'))
print('ALL BOUNDED EXACT COMMIT CHECKS PASS',flush=True)
