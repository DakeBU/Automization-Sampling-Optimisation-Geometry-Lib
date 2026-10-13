from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R);B=R/'runs/20261007-companion-priority/pbps-actual-physical-time-law81';O=B/'exact-commit-verification81'
C='7f815975f0ac55a211af4a4ba8c446b0d7f69a9f';BASE='7b7906944cafaea3bb6b8c289a599dc3a6bf6f51'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/IdealHalfTurnKernel.lean';D='AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel.ideal_half_turn_returned_position_kernel'
CELL='ASTIS-SW-PBPS-ideal-half-turn-kernel';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSIdealHalfTurnKernel.json'
BIND='7f5a864122254a7e0a425edf37e8d68597b161492edb419507199bb24baf29d8';PACK='345c5f2ae584f6aaf5ed9cfb0940cbc67c4855a6138eb0ef99b6c3ab1bf5c66b'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def info(p):
 p=Path(p);p=p if p.is_absolute() else R/p;b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
def save(n,v):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
assert git('rev-parse','HEAD').decode().strip()==C
archives={e['raw_path']:e for e in load(B/'immutable-log-archives81.json')['files']};matches=[];nested=[]
def exact(path):
 p=Path(path);p=p if p.is_absolute() else R/p;rel=p.relative_to(R).as_posix();raw=p.read_bytes()
 if rel.startswith('.lake/packages/mathlib/'):
  blob=git('-C',str(R/'.lake/packages/mathlib'),'show','db584cd6d46c92f209a44c0f1c829460d327499d:'+rel[len('.lake/packages/mathlib/'):])
  assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');nested.append(dict(**info(p),upstream_commit='db584cd6d46c92f209a44c0f1c829460d327499d',git_blob_RAW_sha256=sha(blob)));return
 q=subprocess.run(['git','show',C+':'+rel],cwd=R,capture_output=True);archive=None
 if q.returncode:
  assert rel in archives,'Missing commit binding '+rel
  archive=archives[rel]['archive'];ab=git('show',C+':'+archive);assert sha(ab)==archives[rel]['archive_RAW_sha256'];blob=gzip.decompress(ab);assert sha(blob)==archives[rel]['RAW_sha256']
 else:blob=q.stdout
 same=raw==blob;normal=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
 assert same or (rel!=M and normal),rel
 matches.append(dict(**info(p),git_blob_RAW_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archive))
science=[M,'lean-toolchain','lake-manifest.json',A,'website/content/declaration_lessons/pbps-ideal-half-turn-kernel.json','website/content/publications/pbps-ideal-half-turn-kernel.json','research-wiki/frontier-cells/'+CELL+'.json']
for n in ['root.statement-seal81.json','claim.json','proved-local81.json','root.math81.adoption.json','root.decoder81.adoption.json','root.source81.adoption.json','source-review81.packet.json','immutable-log-archives81.json']:science.append((B/n).relative_to(R).as_posix())
for p in science:exact(p)
raw=(R/M).read_bytes();assert sha(raw)=='5b3d639fbc49e06715ae8f768d5a5c714b7844dc20c5e5a8a16cb564e823df2f'
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
math=B/'independent-math81';decision=load(math/'decision81.json');assert decision['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
assert info(math/'decision81.json')['RAW_sha256']=='c9e33147fcb1ae6bc235aed48bcda3391c1ef115209ea0658a80925e6c06d90c'
for e in load(math/'input-freeze81.json')['inputs']:assert info(e['path'])==e;exact(e['path'])
r=load(math/'fresh-whole-module.receipt.json');assert r['exit_code']==0 and r['terminal_closed'] and r['full_source_prefix_exact']
for e in [r['source'],r['probe'],r['stdout'],r['stderr']]:assert info(e['path'])==e;exact(e['path'])
for e in load(math/'closed-manifest81.json')['artifacts']:assert info(e['path'])==e;exact(e['path'])
exact(math/'closed-manifest81.json')
summary=load(math/'kernel-dependency-summary81.json');assert summary['status']=='PASS' and summary['local_proof_constant_count']==2
assert set(summary['axioms'])=={'propext','Classical.choice','Quot.sound'}
source=load(B/'fresh-source81/source-review.run-manifest81.json');chron=source['source_first_chronology']
for e in source['raw_inputs']+source['raw_outputs']:assert info(e['path'])['RAW_sha256']==e['raw_sha256'];exact(e['path'])
expected_source={'source-review.result81.json':'c5f6f755aea3f75fd45420848dfbafe2a4a680a0e664ff32bf238f2f8cfae060','source-review.run-evidence81.json':'29f08fa35a746fd274f917499f370e494e1d674c60aed710f94ef7d193a125eb','source-review.run-manifest81.json':'4c5b3db4fa08e1846665d518f9ab3f82a536ae2daff208898f3134af761ca55d'}
for n,v in expected_source.items():assert info(B/'fresh-source81'/n)['RAW_sha256']==v;exact(B/'fresh-source81'/n)
assert source['reviewer']=='/root/fresh_source78' and source['reviewer_packet_sha256']==PACK and source['publication_binding_sha256']==BIND
assert chron['original_frozen_bytes_unchanged'] and chron['original_freeze']<chron['prepacket']<source['created_utc']
native=load(B/'fresh-source81/source-review.result81.json');ind=native['independence'];pre=load(B/'fresh-source81/source-review81.prepacket-readiness.json')
assert ind['source_first'] and ind['source_freeze_verified_before_candidate_body'] and ind['prohibited_materials_read']==[] and not ind['proving_worker']
assert not pre['candidate_body_or_new_exposition_seen_this_final_review'] and not pre['canonical_packet_seen']
sp=load(B/'source-review81.packet.json');claimed=sp.pop('packet_sha256');assert claimed==PACK and sha(canon(sp))==PACK
decdir=B/'anonymous-decoder81';dec=load(decdir/'run-manifest.json');decoded=load(decdir/'decoded.json');core={k:v for k,v in dec.items() if k!='decoder_run_sha256'}
assert dec['decoder']=='/root/blind_decoder81' and not dec['source_text_visible'] and sha(canon(core))==dec['decoder_run_sha256']==decoded['decoder_run_sha256']
for p in decdir.iterdir():
 if p.is_file():exact(p)
dp=load(decdir/'parent-packet.json');dp_claim=dp.pop('packet_sha256');assert sha(canon(dp))==dp_claim==dec['packet_sha256']==decoded['decoder_packet_sha256']
assert dec['input_artifacts']==decoded['input_artifacts']==dp['input_artifacts']==['lean-statement','approved-definition-context']
assert sha(decoded['reconstructed_theorem_text'].encode())==dec['reconstructed_text_sha256']==sha((decdir/'reconstruction.txt').read_bytes())
audit=load(R/A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND
assert audit['source_review']['reviewer']=='/root/fresh_source78' and audit['source_review']['reviewer_packet_sha256']==PACK and audit['source_review']['review_run_sha256']==expected_source['source-review.run-evidence81.json']
ackpath=B/'fresh-source81/schema-adapter-acknowledgment81.json';ack=load(ackpath);exact(ackpath)
assert info(ackpath)['RAW_sha256']=='986c324506ba0a6cc15f4a367a54d7cfc6eb80ee38770b376003cb0b0937222e' and ack['canonical_adaptation_confirmed'] and ack['native_files_unchanged']
for e in ack['native_raw_pins']:assert info(e['path'])['RAW_sha256']==e['raw_sha256']
for slot,old in native['semantic_slots'].items():
 now=audit['semantic_slots'][slot]
 for field,value in old.items():assert now[field]==value,(slot,field)
 assert now['original']==old['source'] and now['reconstructed']==old['blind'] and old['assessment'] in now['evidence']
assert audit['source_review']['evidence']==native['verdict_reason'] and not native['blocking_deltas'] and native['no_required_mathematical_repairs']
cov=native['source_graph_coverage'];assert all(not cov[k] for k in ['unmapped_inventory_items','unmapped_nodes','unmapped_edges'])
lesson=load(R/science[4])['units'][0];lines=raw.splitlines(keepends=True);regions=[]
for step in lesson['steps']:
 e=step['lean_source_region'];code=b''.join(lines[e['start_line']-1:e['end_line']]);assert code==step['lean'].encode() and sha(code)==e['exact_code_raw_sha256'] and e['source_raw_sha256']==sha(raw)
 assert step['formula'] and step['text'];regions.append(dict(title=step['title'],start=e['start_line'],end=e['end_line'],RAW_sha256=sha(code),formula=step['formula'],text=step['text']))
assert len(regions)==10 and regions[0]['start']==110 and regions[-1]['end']==310
assert b''.join(step['lean'].encode() for step in lesson['steps'])==b''.join(lines[109:310])
assert all(regions[i]['end']+1==regions[i+1]['start'] for i in range(9))
assert lines[99].startswith(b'theorem ') and b'ideal_half_turn_returned_position_kernel_statement' in lines[109]
assert b':= by' in lines[109] and lines[110].strip()==b'classical'
save('input-freeze81.json',dict(verified_commit=C,base=BASE,exact_commit_matches=matches,nested_pinned_mathlib_matches=nested,native_source_chronology=chron,ten_contiguous_BODY_formula_regions=regions,source_adapter_acknowledgment=info(ackpath),source_adapter_additive_only_checked=True,reused_own_complete_source=info(math/'fresh-whole-module.receipt.json'),reused_own_kernel_closure=info(math/'kernel-dependency-summary81.json'),reuse_reason='Exact unchanged independent complete-source elaboration/axiom/generated-proof closure; bind all raw scientific inputs and terminal logs to this science commit, with lossless archives where necessary. No reproof or fabricated native trajectory.'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command_argv=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))))
 print(n,'EXIT',code,flush=True);assert code==0,n+' failed; logs retained'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');reviewed=O/'publication_reviewed81.py'
with reviewed.open('x',encoding='utf-8') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"], reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.IdealHalfTurnKernel']),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(reviewed)]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan81.json',dict(verifier_id='/root/exact_verify77',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(R/M)))
assert not hits and (R/M).read_bytes()==raw and git('rev-parse','HEAD').decode().strip()==C
for e in matches:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
save('checks-complete81.json',dict(status='PASS',verified_commit=C,verifier_id='/root/exact_verify77',publication_binding_sha256=BIND,source_packet_sha256=PACK,reused_full_source_and_kernel_closure=True,axioms=summary['axioms'],scope='Bounded exact science verification only; canonical aggregate/site/main/purification/whole Goal pending serialized stabilization.'))
print('ALL BOUNDED EXACT COMMIT CHECKS PASS',flush=True)
