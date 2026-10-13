from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R)
B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-measurability80';O=B/'exact-commit-verification80';O.mkdir(exist_ok=True)
C='ac7cabf30e17a322ec187b7eb13e1a9d4a57695d';BASE='bdc743c8022ef5e682f38ecac2f8e5a9815ff3de'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase'
CELL='ASTIS-SW-PBPS-actual-physical-time-measurability';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualPhysicalTimeMeasurability.json'
BIND='d85b866ee0c62651a1a4cecd2db69ae8cf62f244fe547f1baee4bf00eef90eaa';PACK='fc8686899804419df91ce35606537e02e11f0ff1d63b0d6d9808c9e4539d855e'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
def save(n,v):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
assert git('rev-parse','HEAD').decode().strip()==C
archives={e['raw_path']:e for e in load(B/'immutable-log-archives80.json')['files']}
matches=[];nested=[]
def exact(path):
 p=Path(path);p=p if p.is_absolute() else R/p;rel=p.relative_to(R).as_posix();raw=p.read_bytes()
 if rel.startswith('.lake/packages/mathlib/'):
  sub=rel[len('.lake/packages/mathlib/'):];blob=git('-C',str(R/'.lake/packages/mathlib'),'show','db584cd6d46c92f209a44c0f1c829460d327499d:'+sub)
  assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');nested.append(dict(**info(p),upstream_commit='db584cd6d46c92f209a44c0f1c829460d327499d',git_blob_RAW_sha256=sha(blob)));return
 q=subprocess.run(['git','show',C+':'+rel],cwd=R,capture_output=True);archive=None
 if q.returncode:
  assert rel in archives,'Missing commit binding '+rel
  archive=archives[rel]['archive'];ab=git('show',C+':'+archive);assert sha(ab)==archives[rel]['archive_RAW_sha256'];blob=gzip.decompress(ab)
  assert sha(blob)==archives[rel]['RAW_sha256']
 else:blob=q.stdout
 same=raw==blob;normal=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
 assert same or (rel!=M and normal),rel
 matches.append(dict(**info(p),git_blob_RAW_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archive))
science=[M,'lean-toolchain','lake-manifest.json',A,'website/content/declaration_lessons/pbps-actual-physical-time-measurability.json','website/content/publications/pbps-actual-physical-time-measurability.json','research-wiki/frontier-cells/'+CELL+'.json']
for n in ['root.statement-seal80.json','claim.json','proved-local80.json','root.math80.adoption.json','root.decoder80.adoption.json','root.source80.adoption.json','source-review80.packet.json','immutable-log-archives80.json']:science.append((B/n).relative_to(R).as_posix())
for p in science:exact(p)
raw=(R/M).read_bytes();assert sha(raw)=='bf8f66a8484fa82c46b26ac6b66a6c8484e6dd6465ac8587d7e27b2489e73a5c'
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
math=B/'independent-math80';decision=load(math/'decision80.json');assert decision['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS'
assert info(math/'decision80.json')['RAW_sha256']=='b92f284c3b9113e3bccf0c2744e505b8c5d94f171d903309e8ce9d05389f4d81'
for e in load(math/'input-freeze80.json')['inputs']:assert info(e['path'])==e;exact(e['path'])
r=load(math/'fresh-whole-module.receipt.json');assert r['exit_code']==0 and r['terminal_closed'] and r['full_source_prefix_exact']
for e in [r['source'],r['probe'],r['stdout'],r['stderr']]:assert info(e['path'])==e;exact(e['path'])
for p in math.iterdir():
 if p.is_file() and p.suffix not in ['.gz','.log']:exact(p)
summary=load(math/'kernel-dependency-summary80.json');assert summary['status']=='PASS' and summary['local_proof_constant_count']==2
assert set(summary['axioms'])=={'propext','Classical.choice','Quot.sound'}
source=load(B/'fresh-source80/source-review.run-manifest80.json');chron=source['original_source_first_chronology']
for e in source['raw_inputs']+source['raw_outputs']:
 assert info(e['path'])['RAW_sha256']==e['raw_sha256'];exact(e['path'])
for n in ['source-review.run-manifest80.json','source-review.run-evidence80.json','source-review.result80.json']:exact(B/'fresh-source80'/n)
assert source['reviewer']=='/root/fresh_source78 for80' and source['reviewer_packet_sha256']==PACK and source['publication_binding_sha256']==BIND
assert chron['original_source_freeze_unchanged'] and chron['candidate_not_seen_before_source_inventory_and_topology_freeze'] and chron['formalizer_and_decoder_distinct_from_this_reviewer'] and chron['no_prior80_header_scope_math_review_verdicts_root_adoption_or_other_source_extractor_consulted']
assert datetime.datetime.fromisoformat(chron['source_first_freeze_created_utc'])<datetime.datetime.fromisoformat(source['created_utc'])
sp=load(B/'source-review80.packet.json');claimed=sp.pop('packet_sha256');assert claimed==PACK and sha(canon(sp))==PACK
expected_source={'source-review.result80.json':'98630d82df884de6a3a5cd01929e66b9c5df3353b18ca9f81bc3ff565c8de6c0','source-review.run-evidence80.json':'851df6819e602fb254fb553e2ce9a23a035b949da14b5a9f1c65241481df4f16','source-review.run-manifest80.json':'8a73fcd81f8d47db8488f1fabae08ab79e06293e4b60c66acd0764174f2ccff3'}
for n,v in expected_source.items():assert info(B/'fresh-source80'/n)['RAW_sha256']==v
decdir=B/'anonymous-decoder80';dec=load(decdir/'run-manifest.json');core=dec['core']
assert core['decoder_identity']=='independent-source-blind-decoder-80 (/root/blind_decoder80)'
assert not core['source_identity_visible'] and not core['source_text_visible'] and not core['proof_BODY_visible']
assert sha(canon(core))==dec['decoder_run_sha256']
for p in decdir.rglob('*.json'):exact(p)
for n,e in dec['output_artifacts'].items():assert info(e['path'])['RAW_sha256']==e['raw_sha256'];assert (decdir/n).read_bytes()==Path(e['path']).read_bytes()
dp=load(decdir/'parent-packet.json');dp_claim=dp.pop('packet_sha256');assert dp_claim==core['input_artifact']['canonical_packet_sha256'] and sha(canon(dp))==dp_claim
assert sha(dp['lean']['statement'].encode())==core['input_artifact']['lean_statement_utf8_sha256']
audit=load(R/A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND
assert '/root/fresh_source78' in audit['source_review']['reviewer'] and audit['source_review']['reviewer_packet_sha256']==PACK
assert audit['source_review']['review_run_sha256']==expected_source['source-review.run-evidence80.json']
lesson=load(R/science[4])['units'][0];lines=raw.splitlines(keepends=True);regions=[]
for step in lesson['steps']:
 e=step['lean_source_region'];code=b''.join(lines[e['start_line']-1:e['end_line']])
 assert code==step['lean'].encode() and sha(code)==e['exact_code_raw_sha256'] and e['source_raw_sha256']==sha(raw)
 assert step['formula'] and step['text'];regions.append(dict(title=step['title'],start=e['start_line'],end=e['end_line'],RAW_sha256=sha(code),formula=step['formula'],text=step['text']))
assert len(regions)==9 and regions[0]['start']==93 and regions[-1]['end']==249
assert b''.join(step['lean'].encode() for step in lesson['steps'])==b''.join(lines[92:249])
save('input-freeze80.json',dict(verified_commit=C,base=BASE,exact_commit_matches=matches,nested_pinned_mathlib_matches=nested,native_source_chronology=chron,nine_contiguous_BODY_formula_regions=regions,reused_own_complete_source=info(math/'fresh-whole-module.receipt.json'),reused_own_kernel_closure=info(math/'kernel-dependency-summary80.json'),reuse_reason='Exact unchanged own independent complete-source elaboration/axiom/generated-proof closure at pinned source/toolchain/parents; bind all raw scientific inputs and terminal logs to this commit, with lossless archives when needed. No reproof or fabricated native trajectory.'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command_argv=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))))
 print(n,'EXIT',code,flush=True);assert code==0,n+' failed; logs retained'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe')
reviewed=O/'publication_reviewed80.py'
with reviewed.open('x',encoding='utf-8') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"], reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability']),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(reviewed)]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan80.json',dict(verifier_id='/root/exact_verify77',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits() same production fake-closure scan',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(R/M)))
assert not hits and (R/M).read_bytes()==raw and git('rev-parse','HEAD').decode().strip()==C
for e in matches:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
save('checks-complete80.json',dict(status='PASS',verified_commit=C,verifier_id='/root/exact_verify77',publication_binding_sha256=BIND,source_packet_sha256=PACK,reused_full_source_and_kernel_closure=True,axioms=summary['axioms'],scope='Bounded commit verification only; aggregate/site/main/purification/whole Goal remain pending serialized stabilization.'))
print('ALL BOUNDED EXACT COMMIT CHECKS PASS',flush=True)
