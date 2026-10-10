from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R)
B=R/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82';O=B/'exact-commit-verification82'
C='396c13491e5a9bdf0abcd5d7fb00c1fb8ef97fcc';BASE='4502b48d0319bf35110511aa8c98f0190db3623f'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity.actual_small_time_stochastic_continuity'
CELL='ASTIS-SW-PBPS-actual-small-time-continuity';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualSmallTimeContinuity.json'
BIND='996913629e7bce2e7fb674454986bb49386ac51b3eb9a0f2856b265aa3bff8b7';PACK='5f27cc1b3ab2a6e6563f983e8f111e79151629a1c77b1c3ee701489e22966388'
MR='f2bbb2a495ff6af2f2d1d73f77c498ccf16406bb0b07d20b8437631afb1a7bde'
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf8'))
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def rel(p):return path(p).relative_to(R).as_posix()
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=rel(p),RAW_bytes=len(b),RAW_sha256=sha(b))
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
assert git('rev-parse','HEAD').decode().strip()==C
archives={}
for index in ['immutable-log-archives82.json','immutable-whitespace-archives82.json']:
 for e in load(B/index)['files']:archives[rel(e['raw_path'])]=e
matches=[];nested=[];local_primary=[]
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if r.startswith('.lake/packages/mathlib/'):
  blob=git('-C',str(R/'.lake/packages/mathlib'),'show','db584cd6d46c92f209a44c0f1c829460d327499d:'+r[len('.lake/packages/mathlib/'):])
  assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');nested.append(dict(**info(p),upstream_commit='db584cd6d46c92f209a44c0f1c829460d327499d',git_blob_RAW_sha256=sha(blob)));return
 q=subprocess.run(['git','show',C+':'+r],cwd=R,capture_output=True);archive=None
 if q.returncode:
  if r=='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html':
   assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
   local_primary.append(dict(**info(p),commit_binding='Local fixed primary bytes only; committed source-freeze and reviews pin this RAW. Original primary HTML is not claimed committed.'));return
  assert r in archives,'Missing commit binding '+r
  e=archives[r];archive=rel(e['archive']);ab=git('show',C+':'+archive);assert sha(ab)==e['archive_RAW_sha256'];blob=gzip.decompress(ab);assert sha(blob)==e['RAW_sha256'];assert len(blob)==e['RAW_bytes']
 else:blob=q.stdout
 same=raw==blob;normal=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');assert same or (r!=M and normal),r
 matches.append(dict(**info(p),git_blob_RAW_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archive))
science=[M,'lean-toolchain','lake-manifest.json',A,'website/content/declaration_lessons/pbps-actual-small-time-continuity.json','website/content/publications/pbps-actual-small-time-continuity.json','research-wiki/frontier-cells/'+CELL+'.json','runs/substantive_advances.jsonl']
for n in ['root.statement-seal82.json','claim.json','proved-local82.json','root.math82.adoption.json','root.decoder82.adoption.json','root.source82.adoption.json','source-review82.packet.json','immutable-log-archives82.json','immutable-whitespace-archives82.json']:science.append(rel(B/n))
for p in science:exact(p)
for e in archives.values():exact(e['raw_path'])
raw=(R/M).read_bytes();assert sha(raw)==MR
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
math=B/'independent-math82';assert load(math/'decision82.json')['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY'
assert info(math/'closed-manifest82.json')['RAW_sha256']=='76b8f6c49106b420a33dcfd57bf434876cd191b79ed777cbc59a143b93790f0d'
for e in load(math/'closed-manifest82.json')['frozen_inputs']+load(math/'closed-manifest82.json')['owned_artifacts']:
 assert info(e['path'])==e;exact(e['path'])
exact(math/'closed-manifest82.json')
mr=load(math/'fresh-whole-module.receipt.json');assert mr['exit_code']==0 and mr['terminal_closed'] and mr['full_source_prefix_exact'] and mr['source']['RAW_sha256']==MR
summary=load(math/'kernel-dependency-summary82.json');assert summary['status']=='PASS' and summary['local_proof_constant_count']==2 and len(summary['external_ASTIS_dependencies'])==4
assert set(summary['axioms'])=={'propext','Classical.choice','Quot.sound'}
source=load(B/'fresh-source82/source-review.run-manifest82.json');chron=source['source_first_chronology']
for e in source['raw_inputs']+source['raw_outputs']:assert info(e['path'])['RAW_sha256']==e['raw_sha256'];exact(e['path'])
expected={'source-review.result82.json':'9324f048b3b557ef585791b0db1549107cd444c61d9541299d845b13795e7776','source-review.run-evidence82.json':'90f6416500e968bdc387c0c42143f4c67472e4af3a5cddfd9df08454ec021948','source-review.run-manifest82.json':'3b165cf2b3bb121c547878b24e959e87b94ed832be15efddfe2e346e1b5caa6f'}
for n,v in expected.items():assert info(B/'fresh-source82'/n)['RAW_sha256']==v;exact(B/'fresh-source82'/n)
assert source['reviewer']=='/root/fresh_source78' and source['reviewer_packet_sha256']==PACK and source['publication_binding_sha256']==BIND and source['full_module_sha256']==MR
assert chron['original_freeze_unchanged'] and chron['source_inventory_created_utc']<chron['prepacket_readiness_created_utc']<source['created_utc']
native=load(B/'fresh-source82/source-review.result82.json');ind=native['independence'];pre=load(B/'fresh-source82/source-review82.prepacket-readiness.json')
assert ind['source_first'] and ind['source_pins_verified_before_fullBODY'] and ind['own_source_graph_frozen_before_candidate'] and not ind['proving_worker']
assert not pre['candidate_full_body_seen'] and not pre['canonical_packet_seen'] and not pre['current_candidate_publication_seen']
assert native['no_required_mathematical_repairs'] and native['no_unresolved_exposition_repairs'] and not native['blocking_deltas']
sp=load(B/'source-review82.packet.json');claimed=sp.pop('packet_sha256');assert claimed==PACK and sha(canon(sp))==PACK
decdir=B/'anonymous-decoder82';dec=load(decdir/'decoder-run.json');decoded=load(decdir/'decoder-result.json');dm=load(decdir/'RAW-manifest.json')
assert dec['decoder']=='root-blind-decoder82' and not dec['source_text_visible'] and dec['allowed_inputs_only']
assert decoded['decoder_run_sha256']==info(decdir/'decoder-run.json')['RAW_sha256'] and not decoded['source_text_visible'] and decoded['decoder']==dec['decoder']
for e in dm['inputs']:assert info(e['path'])['RAW_sha256']==e['raw_sha256'];exact(e['path'])
for e in dm['outputs']:
 local=decdir/Path(e['path']).name;assert info(local)['RAW_sha256']==e['raw_sha256'];exact(local)
exact(decdir/'RAW-manifest.json')
dp=load(B/'anonymous.decoder82.json');dp_claim=dp.pop('packet_sha256');assert sha(canon(dp))==dp_claim==dec['packet_declared_sha256']==decoded['packet_sha256']
assert decoded['input_artifacts']==dec['input_artifacts'] and decoded['packet_raw_sha256']==info(B/'anonymous.decoder82.json')['RAW_sha256']
assert sha(decoded['reconstructed_theorem_text'].encode())==dec['reconstructed_text_sha256']==info(decdir/'reconstruction.txt')['RAW_sha256']
assert info(decdir/'anonymous-statement.txt')['RAW_sha256']==dec['anonymous_statement_sha256']==decoded['anonymous_statement_sha256']
audit=load(R/A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND
assert audit['source_review']['reviewer']=='/root/fresh_source78' and audit['source_review']['reviewer_packet_sha256']==PACK and audit['source_review']['review_run_sha256']==expected['source-review.run-evidence82.json']
assert audit['semantic_slots']==native['semantic_slots'] and audit['source_review']['evidence']==native['verdict_reason']
cov=native['source_graph_coverage'];assert all(not cov[k] for k in ['unmapped_inventory_items','unmapped_nodes','unmapped_edges'])
assert (cov['inventory_expected'],cov['inventory_reviewed'],cov['nodes_expected'],cov['nodes_reviewed'],cov['edges_expected'],cov['edges_reviewed'])==(36,36,13,13,20,20)
lesson=load(R/science[4])['units'][0];lines=raw.splitlines(keepends=True);regions=[]
for step in lesson['steps']:
 e=step['lean_source_region'];code=b''.join(lines[e['start_line']-1:e['end_line']]);assert code==step['lean'].encode() and sha(code)==e['exact_code_raw_sha256'] and e['source_raw_sha256']==MR
 assert step['formula'] and step['text'];regions.append(dict(title=step['title'],start=e['start_line'],end=e['end_line'],RAW_sha256=sha(code)))
assert len(regions)==9 and regions[0]['start']==106 and regions[-1]['end']==260 and all(a['end']+1==b['start'] for a,b in zip(regions,regions[1:]))
assert b''.join(step['lean'].encode() for step in lesson['steps'])==b''.join(lines[105:260])
assert 'P(D_t)' not in lesson['steps'][3]['formula'] and 'P(D_t)' in lesson['steps'][5]['formula']
tools=['tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py']
for p in tools:exact(p)
# Preserve every pre-existing modified tracked file; no cleanup of collaborator work.
modified=git('diff','--name-only','-z').decode().split('\0');modified=[p for p in modified if p]
preserved=[info(p) for p in modified]
save('collaborator-modified-RAW.before82.json',preserved)
save('input-freeze82.json',dict(verified_commit=C,base=BASE,exact_commit_matches=matches,nested_pinned_mathlib_matches=nested,local_fixed_primary=local_primary,native_source_chronology=chron,nine_contiguous_BODY_formula_regions=regions,source_native_slots_exact_canonical=True,blind_run_recipe='Native exact-byte decoder-run.json SHA, not the edge81 canonical-flat recipe. Raw manifest output basenames copied unchanged from native .astis/decoder82 into committed anonymous-decoder82.',reused_own_complete_source=info(math/'fresh-whole-module.receipt.json'),reused_own_kernel_closure=info(math/'kernel-dependency-summary82.json'),reuse_reason='Unchanged accepted complete-source compilation, generated local proof closure and full imported ASTIS closure; all closed inputs and native logs bound to named science commit or honest local fixed primary, with lossless gzip archives. No reproof or fabricated trajectory.'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command_argv=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))))
 print(n,'EXIT',code,flush=True);assert code==0,n+' failed; logs retained'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');reviewed=O/'publication_reviewed82.py'
with reviewed.open('x',encoding='utf8') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity']),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(reviewed)]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan82.json',dict(verifier_id='/root/exact_verify77',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(R/M)))
assert not hits and (R/M).read_bytes()==raw and git('rev-parse','HEAD').decode().strip()==C
for e in matches:assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
for e in preserved:assert info(e['path'])==e
save('checks-complete82.json',dict(status='PASS',verified_commit=C,verifier_id='/root/exact_verify77',publication_binding_sha256=BIND,source_packet_sha256=PACK,reused_full_source_and_kernel_closure=True,axioms=summary['axioms'],all_preexisting_modified_tracked_RAWs_unchanged=True,preexisting_modified_tracked_count=len(preserved),scope='Bounded exact science verification only; aggregate/site/main/purification/whole Goal pending serialized stabilization.'))
print('ALL BOUNDED EXACT COMMIT CHECKS PASS',flush=True)
