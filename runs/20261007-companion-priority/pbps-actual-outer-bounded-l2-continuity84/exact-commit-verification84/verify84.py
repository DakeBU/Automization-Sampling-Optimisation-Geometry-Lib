from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R)
B=R/'runs/20261007-companion-priority/pbps-actual-outer-bounded-l2-continuity84';O=B/'exact-commit-verification84'
C='dd3a23011b91569acbcd591ccd7b06301147d339';BASE='5f29b2a3b5a95d7ee9f8e166ba833857ef0845e2'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOuterBoundedL2Continuity.lean';MR='8fd35db26717f46313fc53dd90691828b11c9d78cdcc4a62f68c8d59273cc2bd'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity.actual_outer_bounded_l2_continuity';ID='ASTIS-SA-20261011-PBPSActualOuterBoundedL2Continuity'
CELL='ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOuterBoundedL2Continuity.json'
BIND='9653eee231ec71293839aae14374a183c8ebe01441817e44a08736ec3cd02636';PACK='cae491f32e464f9f75e2a5a080b4a68c7439cbbd26fb2bfc1659fc4bf2d6bb76'
def sha(b):return hashlib.sha256(b).hexdigest()
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def rel(p):return path(p).relative_to(R).as_posix()
def load(p):return json.loads(path(p).read_text(encoding='utf8'))
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=rel(p),RAW_bytes=len(b),RAW_sha256=sha(b))
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
assert git('rev-parse','HEAD').decode().strip()==C
assert git('rev-parse',C+'^').decode().strip()==BASE
archives={rel(e['raw_path']):e for e in load(B/'immutable-whitespace-archives84.json')['files']};matches={};nested={};local_primary={}
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if r in matches or r in nested or r in local_primary:return
 if r.startswith('.lake/packages/mathlib/'):
  blob=git('-C',str(R/'.lake/packages/mathlib'),'show','db584cd6d46c92f209a44c0f1c829460d327499d:'+r[len('.lake/packages/mathlib/'):]);assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
  nested[r]=dict(**info(p),upstream_commit='db584cd6d46c92f209a44c0f1c829460d327499d',git_blob_RAW_sha256=sha(blob));return
 q=subprocess.run(['git','show',C+':'+r],cwd=R,capture_output=True);archive=None
 if q.returncode:
  if r=='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html':
   assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';local_primary[r]=dict(**info(p),commit_binding='Local exact primary RAW pinned by committed source freeze/reviews; not claimed committed.');return
  assert r in archives,'Missing commit binding '+r
  e=archives[r];archive=rel(e['archive']);ab=git('show',C+':'+archive);assert sha(ab)==e['archive_RAW_sha256'];blob=gzip.decompress(ab);assert sha(blob)==e['RAW_sha256'] and len(blob)==e['RAW_bytes']
 else:blob=q.stdout
 same=raw==blob;normal=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');assert same or (r!=M and normal),r
 matches[r]=dict(**info(p),git_blob_RAW_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archive)
science=[M,'lean-toolchain','lake-manifest.json',A,'website/content/declaration_lessons/pbps-actual-outer-bounded-l2-continuity.json','website/content/publications/pbps-actual-outer-bounded-l2-continuity.json','research-wiki/frontier-cells/'+CELL+'.json','runs/substantive_advances.jsonl']
science += [rel(B/n) for n in ['root.statement-seal84.json','claim.json','proved-local84.json','root.math84.adoption.json','root.decoder84.adoption.json','root.source84.adoption.json','source-review84.packet.json','immutable-whitespace-archives84.json']]
for p in science:exact(p)
for e in archives.values():exact(e['raw_path'])
assert info(M)['RAW_sha256']==MR and git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
math=B/'independent-math84';assert load(math/'decision84.json')['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY'
assert info(math/'closed-raw-manifest84.json')['RAW_sha256']=='a97fb0013539363c49961c8b7e2748144ddf64c2a7bf8db42c18a10afa7ef3fe'
for e in load(math/'closed-raw-manifest84.json')['frozen_inputs']+load(math/'closed-raw-manifest84.json')['owned_artifacts']:assert info(e['path'])==e;exact(e['path'])
exact(math/'closed-raw-manifest84.json')
mr=load(math/'fresh-whole-module.receipt.json');assert mr['exit_code']==0 and mr['terminal_closed'] and mr['source']['RAW_sha256']==MR
assert path(mr['probe']['path']).read_bytes().startswith(path(M).read_bytes())
summary=load(math/'kernel-dependency-summary84.json');assert summary['expected_four_parent_frontier_exact'] and summary['local_proof_constant_count']==1 and len(summary['external_ASTIS_dependencies'])==4
assert set(summary['axioms'])=={'propext','Classical.choice','Quot.sound'}
for key in ['native_decision','native_closed_manifest','fresh_compiler_receipt','kernel_dependency_receipt']:
 e=load(B/'root.math84.adoption.json')[key];assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
source=B/'independent-source84';sm=load(source/'source-review.run-manifest84.json');native=load(source/'source-review.result84.json');sr=load(source/'source-review.run-evidence84.json')
for e in sm['raw_inputs']+sm['raw_outputs']:assert info(e['path'])['RAW_sha256']==e['raw_sha256'];exact(e['path'])
expected={'source-review.result84.json':'d0a76bd12531b282aa5e837abab9a54189414438084aaa5a39c784cee39d05e9','source-review.run-evidence84.json':'96d387144d9a82768f283daa83410800441e426798a9935a42654eded1afb295','source-review.run-manifest84.json':'b86b83a46dabbccd23116e421ba066372c847e08ae74b8109380bdd99b058fcd'}
for n,v in expected.items():assert info(source/n)['RAW_sha256']==v;exact(source/n)
assert sm['reviewer_packet_sha256']==PACK and sm['publication_binding_sha256']==BIND and sm['full_module_sha256']==MR
assert native['reviewer']=='/root/fresh_source78' and native['independent_from_formalizer'] and native['independent_from_decoder']
ind=native['independence'];assert not ind['original_graph_self_validation'] and not ind['other_math_review_verdicts_read'] and not ind['root_adoption_reports_read']
assert native['no_required_mathematical_repairs'] and not native['repairs'] and sr['all26_primary_anchor_hashes_match'] and sr['exact_private_prop_matches_preproof_reviewed_successor']
pre=load(source/'prepacket-preparation84.json');assert pre['created_utc']<native['created_utc']
cov=native['source_graph_coverage'];assert (cov['inventory_expected'],cov['inventory_reviewed'],cov['nodes_expected'],cov['nodes_reviewed'],cov['relations_expected'],cov['relations_reviewed'])==(47,47,23,23,39,39)
assert not cov['gaps'] and not cov['missing_required_ingredients'] and cov['dependency_edges']==37 and len(cov['future_open_dependency_ids'])==5 and len(cov['excluded_association_ids'])==2
assert native['authored_step_coverage']['formula_body_exact_matches']==8 and not native['authored_step_coverage']['gaps'] and not native['authored_step_coverage']['overlaps']
sp=load(B/'source-review84.packet.json');claimed=sp.pop('packet_sha256');assert claimed==PACK==sha(canon(sp))
audit=load(A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND
assert audit['semantic_slots']==native['semantic_slots'] and audit['source_review']['evidence']==native['verdict_reason'] and audit['source_review']['review_run_sha256']==expected['source-review.run-evidence84.json'] and audit['source_review']['reviewer_packet_sha256']==PACK
sa=load(B/'root.source84.adoption.json');assert sa['publication_binding_unchanged'] and sa['publication_binding_sha256']==BIND and sa['full_current_module_RAW_sha256']==MR
for key in ['native_result','native_manifest','native_run_evidence']:
 e=sa[key];assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
decdir=B/'anonymous-decoder84';dec=load(decdir/'decoder-run.json');decoded=load(decdir/'decoder-result.json');dm=load(decdir/'RAW-manifest.json')
assert dec['decoder']=='independent-source-blind-decoder84-/root/blind_decoder84' and dec['allowed_inputs_only'] and not dec['source_text_visible']
assert decoded['decoder_run_sha256']==info(decdir/'decoder-run.json')['RAW_sha256'] and not decoded['source_text_visible'] and decoded['decoder']==dec['decoder']
for e in dm['input_artifacts']:
 p=path(e['path']);assert info(p)['RAW_sha256']==e['raw_sha256'];copy=decdir/'packet.json' if p.name=='packet.json' else p
 assert copy.read_bytes()==p.read_bytes();exact(copy)
for e in dm['output_artifacts']:
 p=decdir/Path(e['path']).name;assert info(p)['RAW_sha256']==e['raw_sha256'];assert p.read_bytes()==path(e['path']).read_bytes();exact(p)
exact(decdir/'RAW-manifest.json');assert info(decdir/'RAW-manifest.json')['RAW_sha256']==load(B/'root.decoder84.adoption.json')['native_manifest_RAW_sha256']
dp=load(B/'anonymous.decoder84.json');claimed=dp.pop('packet_sha256');assert sha(canon(dp))==claimed==dec['packet_declared_sha256']==decoded['packet_declared_sha256']
assert sha(dp['lean']['statement'].encode())==dec['anonymous_statement_sha256']==decoded['anonymous_statement_sha256']
assert sha(decoded['reconstructed_theorem_text'].encode())==dec['reconstructed_text_sha256']==info(decdir/'reconstruction.txt')['RAW_sha256']
assert path(B/'anonymous.decoder84.json').read_bytes()==path(decdir/'packet.json').read_bytes();exact(B/'anonymous.decoder84.json')
for p in ['tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py']:exact(p)
baseline=load(R/'runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/pre-fetch84.workspace-RAW.json')['tracked_modified'];assert len(baseline)==21
preserved=[info(p) for p in baseline];assert {e['path']:e['RAW_sha256'] for e in preserved}==baseline
save('collaborator-preservation84.json',dict(baseline=info(R/'runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/pre-fetch84.workspace-RAW.json'),RAWs=preserved,count=21))
save('input-freeze84.json',dict(verified_commit=C,base=BASE,exact_commit_matches=list(matches.values()),nested_mathlib_matches=list(nested.values()),local_fixed_primary=list(local_primary.values()),native_source_chronology=sm['source_first_chronology'],source_coverage=dict(inventory=47,nodes=23,relations=39,dependencies=37,futureOPEN=5,excluded_associations=2),publication_binding_sha256=BIND,source_packet_sha256=PACK,reused_complete_source=info(math/'fresh-whole-module.receipt.json'),reused_kernel_closure=info(math/'kernel-dependency-summary84.json'),reuse_reason='Own unchanged full-source elaboration and standard3/actual4-parent kernel closure, all original native hashes rechecked against named science commit or lossless archive; fixed primary57 honestly local. No reproof or invented trajectory.'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command_argv=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))));print(n,'EXIT',code,flush=True)
 assert code==0,n+' failed; immutable native logs retained'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');reviewed=O/'publication_reviewed84.py'
with reviewed.open('x',encoding='utf8') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOuterBoundedL2Continuity']),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(reviewed)]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan84.json',dict(verifier_id='/root/exact_verify77',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
assert git('rev-parse','HEAD').decode().strip()==C
for e in list(matches.values())+list(nested.values())+list(local_primary.values()):assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
for e in preserved:assert info(e['path'])==e
save('checks-complete84.json',dict(status='PASS',verified_commit=C,verifier_id='/root/exact_verify77',publication_binding_sha256=BIND,source_packet_sha256=PACK,reused_full_source_kernel_evidence=True,standard_axioms_only=summary['axioms'],actual_four_parents=summary['external_ASTIS_dependencies'],all21collaborator_RAWs_preserved=True,scope='Exact science admission only; serialized aggregation/reader/main/PURIFIED/full sourceL2/fullpaper/Goal remain separate.'))
print('EXACT COMMIT CHECKS PASS',flush=True)
