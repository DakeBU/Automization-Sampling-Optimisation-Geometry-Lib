from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');os.chdir(R);O=Path(__file__).parent;B=O.parent
C='6d7d42f996a4fbb159c518623fd35c1ac7717fe9';BASE='f145260bd7470ae06d8839fb6d6b158141ce5754'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhaseTransitionKernel.lean';MR='14df46eb96095b6b4cf3e454f7794382c2ba1e09812bd8ab15b7ea6b11842a22'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel.actual_phase_transition_kernel';ID='ASTIS-SA-20261011-PBPSActualPhaseTransitionKernel';CELL='ASTIS-SW-PBPS-actual-phase-transition-kernel'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualPhaseTransitionKernel.json';BIND='93b1b4f22028ed99f4d1fb5cb1fd4be0e0ed974ec1a04e1924b565db77d17382';PACK='fee406605b6338790fd195e688b794f063c78e2364124e30888f71702187b176'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def rel(p):return path(p).relative_to(R).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=rel(p),RAW_sha256=sha(b),RAW_bytes=len(b))
def load(p):return json.loads(path(p).read_bytes())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
assert git('rev-parse','HEAD').decode().strip()==C and git('rev-parse',C+'^').decode().strip()==BASE
archive_index=load(B/'immutable-whitespace-archives85.json');archives={rel(e['raw_path']):e for e in archive_index['files']};matches={};nested={};local={};compiled={}
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if r in matches or r in nested or r in local or r in compiled:return
 if r.startswith('.lake/packages/mathlib/'):
  blob=git('-C',str(R/'.lake/packages/mathlib'),'show','db584cd6d46c92f209a44c0f1c829460d327499d:'+r[len('.lake/packages/mathlib/'):]);assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');nested[r]=dict(**info(p),upstream_commit='db584cd6d46c92f209a44c0f1c829460d327499d',git_blob_RAW_sha256=sha(blob));return
 if r.startswith('.lake/build/'):
  compiled[r]=dict(**info(p),binding='Local compiled artifact pinned in unchanged independent math manifest; source separately checked against named science commit and fresh focused build will exercise same fixed dependency cache. Not claimed Git-committed.');return
 q=subprocess.run(['git','show',C+':'+r],cwd=R,capture_output=True);archive=None
 if q.returncode:
  if r=='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html':
   assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';local[r]=dict(**info(p),binding='Exact local primary RAW pinned by committed sourcefreeze/reviews; fullHTML not claimed committed.');return
  assert r in archives,'Missing commit/archive binding '+r
  e=archives[r];archive=rel(e['archive']);ab=git('show',C+':'+archive);assert sha(ab)==e['archive_RAW_sha256'];blob=gzip.decompress(ab);assert sha(blob)==e['RAW_sha256'] and len(blob)==e['RAW_bytes']
 else:blob=q.stdout
 same=raw==blob;normal=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');assert same or (r!=M and normal),r
 matches[r]=dict(**info(p),git_blob_RAW_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archive)
science=[M,'lean-toolchain','lake-manifest.json',A,'website/content/declaration_lessons/pbps-actual-phase-transition-kernel.json','website/content/publications/pbps-actual-phase-transition-kernel.json','research-wiki/frontier-cells/'+CELL+'.json','runs/substantive_advances.jsonl']
science += [rel(B/n) for n in ['root.statement-seal85.json','claim.json','proved-local85.json','root.math85.adoption.json','root.decoder85.adoption.json','root.source85.adoption.json','source-review85.packet.json','immutable-whitespace-archives85.json']]
for p in science:exact(p)
for e in archives.values():exact(e['raw_path'])
assert info(M)['RAW_sha256']==MR and git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
math=B/'independent-math85';assert load(math/'decision85.json')['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY' and info(math/'closed-RAW-manifest85.json')['RAW_sha256']=='f1e548950f55cea39141cbeb7808f09b00d2c770302d351fe9fc7ab59a874a99'
for e in load(math/'closed-RAW-manifest85.json')['raw_inputs']+load(math/'closed-RAW-manifest85.json')['raw_outputs']:assert info(e['path'])==e;exact(e['path'])
exact(math/'closed-RAW-manifest85.json');mr=load(math/'fresh-whole-module.receipt.json');assert mr['exit_code']==0 and mr['terminal_closed'] and mr['source']['RAW_sha256']==MR and path(mr['probe']['path']).read_bytes().startswith(path(M).read_bytes())
summary=load(math/'kernel-dependency-summary85.json');classification=load(math/'kernel-dependency-classification85.json');assert classification['public_producer_count']==2 and classification['private_direct_count']==6 and classification['owned_count']==9 and classification['transitive_project_constants']==82 and classification['transitive_project_edges']==142 and classification['no_extra_public_parent']
assert set(summary['axioms'])=={'propext','Classical.choice','Quot.sound'} and not summary['expected_two_public_parents_exact']
for key in ['native_decision','native_closed_manifest','fresh_compiler_receipt','kernel_dependency_receipt','kernel_classification_receipt']:
 e=load(B/'root.math85.adoption.json')[key];assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
source=B/'independent-source85';sm=load(source/'source-review.run-manifest85.json');native=load(source/'source-review.result85.json');sr=load(source/'source-review.run-evidence85.json')
for e in sm['raw_inputs']+sm['raw_outputs']:assert info(e['path'])['RAW_sha256']==e['raw_sha256'] and info(e['path'])['RAW_bytes']==e['bytes'];exact(e['path'])
source_expected={'source-review.result85.json':'0d1e0369d0650d845d8665482bb494698fc8d2559f6490e4dbd5bac4fde526d0','source-review.run-evidence85.json':'2a98c62ccd15b723b80363d9e15439a56828d29aab3a1430b37a62017bd2d76a','source-review.run-manifest85.json':'5daf005621c56e1c6bead96a47edf28b770a1b461378c63756e67bbbe64da5fd'}
for n,v in source_expected.items():assert info(source/n)['RAW_sha256']==v;exact(source/n)
assert sm['reviewer_packet_sha256']==PACK and sm['publication_binding_sha256']==BIND and sm['full_module_sha256']==MR
assert native['reviewer']=='/root/fresh_source78' and native['independent_from_formalizer'] and native['independent_from_decoder'] and native['verdict']=='equivalent-after-elaboration' and native['no_required_mathematical_repairs'] and not native['repairs']
ind=native['independence'];assert not ind['original_graph_selfapproval'] and not ind['independent_math_results_read'] and not ind['root_adoption_reports_read'] and not ind['full_canonical_audit_read'] and not ind['earlier_final_verdicts_read']
assert all(v['status']=='PASS' for v in sr['native_checks']);cov=native['source_graph_coverage'];assert [cov[k] for k in ['inventory_count','nodes_count','relations_count','dependency_count','future_OPEN_dependency_count','excluded_association_count','original_primary_anchors','effective_primary_anchors']]==[16,21,29,26,6,3,28,31] and not cov['gaps']
steps=native['authored_step_coverage'];assert steps['formula_body_exact_matches']==6 and steps['body_start_line']==114 and steps['body_end_line']==161 and not steps['gaps'] and not steps['overlaps'];assert not native['public_statement_coverage']['gaps']
sp=load(B/'source-review85.packet.json');claimed=sp.pop('packet_sha256');assert claimed==PACK==sha(canon(sp))
audit=load(A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND and audit['semantic_slots']==native['semantic_slots'] and audit['source_review']['evidence']==native['verdict_reason'] and audit['source_review']['review_run_sha256']==source_expected['source-review.run-evidence85.json'] and audit['source_review']['reviewer_packet_sha256']==PACK
sa=load(B/'root.source85.adoption.json');assert sa['publication_binding_unchanged'] and sa['publication_binding_sha256']==BIND and sa['full_current_module_RAW_sha256']==MR
for key in ['native_result','native_manifest','native_run_evidence']:
 e=sa[key];assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
decdir=B/'anonymous-decoder85';dec=load(decdir/'decoder-run.json');decoded=load(decdir/'decoder-result.json');dm=load(decdir/'RAW-manifest.json')
assert dec['decoder']=='independent-source-blind-decoder:/root/blind_decoder85' and dec['allowed_inputs_only'] and not dec['source_text_visible'];assert info(decdir/'decoder-run.json')['RAW_sha256']=='ae005c93a964bc1a6840442ff6348b509adabdcdbf93849a1383bb4ef3af5773'
assert decoded['decoder_run_sha256']==info(decdir/'decoder-run.json')['RAW_sha256'] and not decoded['source_text_visible'] and decoded['decoder']==dec['decoder']
for e in dm['input_artifacts']:
 p=path(e['path']);assert info(p)['RAW_sha256']==e['raw_sha256'];copy=decdir/'anonymous.packet.json' if p.name=='anonymous.packet.json' else p;assert copy.read_bytes()==p.read_bytes();exact(copy)
for e in dm['output_artifacts']:
 p=decdir/Path(e['path']).name;assert info(p)['RAW_sha256']==e['raw_sha256'] and p.read_bytes()==path(e['path']).read_bytes();exact(p)
exact(decdir/'RAW-manifest.json');assert info(decdir/'RAW-manifest.json')['RAW_sha256']==load(B/'root.decoder85.adoption.json')['native_manifest_RAW_sha256']
dp=load(B/'anonymous.decoder85.json');claimed=dp.pop('packet_sha256');assert sha(canon(dp))==claimed==dec['packet_declared_sha256']==decoded['packet_declared_sha256'];assert claimed=='02c93d80c62618b17a0b056552d5f96b44897292c1cf6d05288dc62b8f729d84'
assert sha(dp['lean']['statement'].encode())==dec['anonymous_statement_sha256']==decoded['anonymous_statement_sha256'];assert sha(decoded['reconstructed_theorem_text'].encode())==dec['reconstructed_text_sha256']==info(decdir/'reconstruction.txt')['RAW_sha256'];assert path(B/'anonymous.decoder85.json').read_bytes()==path(decdir/'anonymous.packet.json').read_bytes();exact(B/'anonymous.decoder85.json')
for p in ['tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py']:exact(p)
baseline_path=R/'runs/20261007-companion-priority/pbps-transition-kernel-preread85/pre-fetch85.workspace-RAW.json';baseline=load(baseline_path)['tracked_modified'];assert len(baseline)==21;preserved=[info(p) for p in baseline];assert {e['path']:e['RAW_sha256'] for e in preserved}==baseline
save('collaborator-preservation85.json',dict(baseline=info(baseline_path),RAWs=preserved,count=21))
helper=B/'commit_integration85.py';before=git('show',C+':'+rel(helper));after=helper.read_bytes();old=b'paths=sorted(set(owned));';new=b'paths=sorted({Path(p).resolve().relative_to(Path.cwd()).as_posix() for p in owned});';assert before.replace(b'\r\n',b'\n').replace(old,new)==after.replace(b'\r\n',b'\n')
with (O/'postscience-integration-helper.diff').open('xb') as f:f.write(git('diff','--',rel(helper)))
save('postscience-helper-distinction85.json',dict(helper=info(helper),science_blob_RAW_sha256=sha(before),exact_one_line_path_normalization_only=True,production_statement_BODY_source_publication_unchanged=True,not_science_mathematical_evidence=True,root_prior_absolute_relative_staging_negative_retained=info(B/'science-staging-diagnosis85.json'),reviewer_does_not_execute_integration_helper=True))
save('input-freeze85.json',dict(verified_commit=C,base=BASE,exact_commit_matches=list(matches.values()),nested_mathlib_matches=list(nested.values()),local_fixed_primary=list(local.values()),local_compiled_artifacts=list(compiled.values()),source_first_chronology=sr['source_first_chronology'],source_coverage=dict(inventory=16,nodes=21,relations=29,dependencies=26,futureOPEN=6,excluded_associations=3,original_anchors=28,effective_anchors=31),publication_binding_sha256=BIND,source_packet_sha256=PACK,reused_complete_source=info(math/'fresh-whole-module.receipt.json'),reused_expanded_kernel_closure=info(math/'kernel-dependency-summary85.json'),reused_kernel_classification=info(math/'kernel-dependency-classification85.json'),reuse_reason='Unchanged own full-source elaboration, standard3 axioms,2public+6private immediate ASTIS constants,9owned/82transitive/142edges expanded closure. Every native hash checked against named science commit, exact gzip or pinned local primary/build cache. No reproof or fabricated trajectory.'))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))));print(n,'EXIT',code,flush=True);assert code==0,n+' failed; retained native logs'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');reviewed=O/'publication_reviewed85.py'
with reviewed.open('x',encoding='utf8',newline='\n') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseTransitionKernel']),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(reviewed)]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan85.json',dict(verifier_id='/root/exact_verify77',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
assert git('rev-parse','HEAD').decode().strip()==C
for e in list(matches.values())+list(nested.values())+list(local.values())+list(compiled.values()):assert info(e['path'])['RAW_sha256']==e['RAW_sha256']
for e in preserved:assert info(e['path'])==e
save('checks-complete85.json',dict(status='PASS',verified_commit=C,verifier_id='/root/exact_verify77',publication_binding_sha256=BIND,source_packet_sha256=PACK,reused_full_source_and_expanded_kernel_evidence=True,standard_axioms_only=summary['axioms'],actual_two_public_parents=classification['actual_public_producer_parents'],private_direct_parent_constants=6,owned_constants=9,transitive_ASTIS_constants=82,transitive_ASTIS_edges=142,all21collaborator_RAWs_preserved=True,scope='Exact science admission only; aggregate/reader/main/PURIFIED/fullpaper/wholeGoal remain separate.'))
print('EXACT COMMIT CHECKS PASS',flush=True)
