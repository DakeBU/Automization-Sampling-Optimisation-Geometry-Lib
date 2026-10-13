from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
C='0bb3cd64ba1235114feaeed99ba22e675b23db76';BASE='8280ef700ea01a1e94c9e7a3cba05a26b4156b56'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteFirstEventLaw.lean';MR='d6667ccbb917d6463e96b2082a5a26089950889fd20af4859052cd7a9a1db776'
OLD='cb8bd3e3ed053d114c6871ceaff24ab7782b46be405d69afe7174e0f4b7721d5'
L='website/content/declaration_lessons/pbps-actual-finite-first-event-law.json';LR='9cb0da1316872b2484404316211a9378310656b61ceb02b455793d055e5fb033'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw.actual_finite_first_event_law'
ID='ASTIS-SA-20261011-PBPSActualFiniteFirstEventLaw';CELL='ASTIS-SW-PBPS-actual-finite-first-event-law'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteFirstEventLaw.json'
BIND='30871a16346f70e877abadba35385e969b265af174bfeb19b8914658e0a0ffdd';PACK='05d5060a5a0bbf369040a91cfbb30fe44362bbb439fb2c3132b5cc93e161404a'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def rel(p):return path(p).relative_to(R).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def load(p):return json.loads(path(p).read_bytes())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def canon(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
assert git('rev-parse','HEAD').decode().strip()==C and git('rev-parse',C+'^').decode().strip()==BASE
baseline_path=R/'runs/20261007-companion-priority/pbps-path-law-preread86/pre-fetch86.workspace-RAW.json'
baseline=load(baseline_path)['tracked_modified'];assert len(baseline)==21
for p,h in baseline.items():assert info(p)['raw_sha256']==h
archive_index=load(B/'immutable-whitespace-archives86.json');archives={rel(e['raw_path']):e for e in archive_index['files']}
matches={};nested={};local={};compiled={};collaborator_inputs={};historical=[]
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if any(r in x for x in [matches,nested,local,compiled,collaborator_inputs]):return
 if r in baseline:
  assert sha(raw)==baseline[r];collaborator_inputs[r]=dict(**info(p),binding='Preexisting collaborator RAW preserved; not represented as science-committed changes.');return
 if r.startswith('.lake/packages/mathlib/'):
  blob=git('-C',str(R/'.lake/packages/mathlib'),'show','db584cd6d46c92f209a44c0f1c829460d327499d:'+r[len('.lake/packages/mathlib/'):]);assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');nested[r]=dict(**info(p),upstream_commit='db584cd6d46c92f209a44c0f1c829460d327499d',git_blob_raw_sha256=sha(blob));return
 if r.startswith('.lake/build/'):
  compiled[r]=dict(**info(p),binding='Pinned unchanged local compiled dependency artifact; source checked and current fresh focused build exercises fixed toolchain. Not claimed Git-committed.');return
 q=subprocess.run(['git','show',C+':'+r],cwd=R,capture_output=True);archive=None
 if q.returncode:
  if r=='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html':
   assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760';local[r]=dict(**info(p),binding='Exact private local primary pinned by committed freezes; full HTML not claimed committed.');return
  if path(p).name.startswith('.private.') or (p.parent==B/'independent-source86' and p.name in load(B/'independent-source86/source-review86.eof-rebound.final.native-RAW-manifest.json')['source_private_exclusions']):
   local[r]=dict(**info(p),binding='Hash-pinned private source extract explicitly excluded by native review manifest; original primary checked separately.');return
  assert r in archives,'Missing exact commit/archive binding '+r
  e=archives[r];archive=rel(e['archive']);ab=git('show',C+':'+archive);assert sha(ab)==e['archive_RAW_sha256'];blob=gzip.decompress(ab);assert sha(blob)==e['RAW_sha256'] and len(blob)==e['RAW_bytes']
 else:blob=q.stdout
 if r==rel(B/'science-stage-whitespace86.log') and raw!=blob:
  assert raw==b'' and sha(blob)=='da660dd6027f858107e0bc03a6f16356deb575edcdb8469786a820a7c3fc0012' and len(blob)==243 and archive
  restored=O/'science-stage-whitespace86.original-from-commit.log'
  with restored.open('xb') as f:f.write(blob)
  save('stage-log-history86.json',dict(status='AUTHORITATIVE_COMMITTED_LOSSLESS_ARCHIVE_RESTORED_TO_REVIEWER_OWNED_SNAPSHOT',historical_RAW_sha256=sha(blob),historical_RAW_bytes=len(blob),committed_archive=archive,restored_original=info(restored),current_mutable_root_log=info(p),reason='Root confirmed science staging helper archived prior negative then successful retry overwrote SAME raw path with0B. Nonmathematical staging recorder mistake; source/math/blind/Lean bytes unchanged. Reviewer leaves root path unchanged.',root_acknowledgement='Parent coordination message confirms root staging recorder reuse; future root diagnosis/helper repair separate.'))
  matches[r]=dict(**info(p),git_blob_raw_sha256=sha(blob),exact_equal=False,newline_only_checkout_difference=False,lossless_archive=archive,historical_archive_authoritative=True,original_restored_snapshot=info(restored),nonmathematical_postarchive_observation=True);return
 same=raw==blob;normal=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');assert same or (r not in [M,L] and normal),r
 matches[r]=dict(**info(p),git_blob_raw_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archive)
aliases={(M,OLD):B/'eof-whitespace-repair86/module.before.exactraw.lean',(L,'4940dcf9492e1ae366d1a18215f33111101c32c753e688475156409491f2f0d3'):B/'eof-whitespace-repair86/lesson.before.exactraw.json'}
def check_entry(e):
 expected=e.get('raw_sha256',e.get('RAW_sha256',e.get('sha256')));size=e.get('bytes',e.get('RAW_bytes'))
 p=path(e['path']);r=rel(p)
 if info(p)['raw_sha256']!=expected:
  assert (r,expected) in aliases,'Undeclared historical drift '+r
  oldp=aliases[(r,expected)];historical.append(dict(historical_descriptor=e,authoritative_immutable_snapshot=info(oldp),current_science=info(p),reason='Explicit independently accepted EOF/11 containing-file-hash metadata successor; original native records immutable.'));p=oldp
 assert info(p)['raw_sha256']==expected and (size is None or info(p)['bytes']==size),str(p)
 exact(p)
def manifest(p,groups):
 exact(p);v=load(p)
 for group in groups:
  for e in v.get(group,[]):check_entry(e)
 return v

science=[M,L,'website/content/publications/pbps-actual-finite-first-event-law.json','lean-toolchain','lake-manifest.json',A,'research-wiki/frontier-cells/'+CELL+'.json','runs/substantive_advances.jsonl']
science += [B/n for n in ['root.statement-seal86.json','claim.json','proved-local86.json','root.math86.adoption.json','root.decoder86.adoption.json','root.source86.adoption.json','root.source86.eof-adoption.json','root.eof86.adoption.json','root.exhaustive-topology86.adoption.json','source-review86.eof-successor.packet.json','immutable-whitespace-archives86.json']]
for p in science:exact(p)
assert info(M)['raw_sha256']==MR and info(L)['raw_sha256']==LR
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert path(M).read_bytes()+b'\n'==aliases[(M,OLD)].read_bytes()
oldlesson=load(B/'eof-whitespace-repair86/lesson.before.exactraw.json');newlesson=load(L)
expectedlesson=json.loads(json.dumps(oldlesson))
for step in expectedlesson['units'][0]['steps']:step['lean_source_region']['source_raw_sha256']=MR
assert newlesson==expectedlesson
math=B/'independent-math86'
assert info(math/'closed-RAW-manifest86.json')['raw_sha256']=='e32ee0a619823174891803fb9a7ba26baadf3c581ec7ef4a0cb84d519b5cf077'
assert load(math/'decision86.json')['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY'
manifest(math/'closed-RAW-manifest86.json',['frozen_current_inputs','immutable_original_inputs','owned_artifacts'])
manifest(B/'eof-math-review86/closed-RAW-manifest86.json',['frozen_current_inputs','owned_artifacts'])
assert load(B/'eof-math-review86/decision86.json')['status']=='ACCEPT_EXACT_EOF_WHITESPACE_ONLY_PROPOSAL'
assert load(B/'eof-math-review86/fresh-proposed-source.receipt.json')['exit_code']==0
summary=load(math/'kernel-dependency-summary86.json')
assert summary['standard_axioms_only'] and summary['exact_four_public_parents'] and [summary[k] for k in ['owned_count','transitive_count','edge_count','generic_count']]==[19,39,44,480]
assert len(summary['actual_public_producer_parents'])==4 and len(summary['private_spec_dependencies'])==12
for ab in summary['axiom_blocks']:assert set(ab['axioms'])=={'propext','Classical.choice','Quot.sound'}
oldreceipt=load(math/'fresh-whole-module.receipt.json');assert oldreceipt['exit_code']==0 and oldreceipt['terminal_closed']
assert path(oldreceipt['probe']['path']).read_bytes().startswith(aliases[(M,OLD)].read_bytes())
source=B/'independent-source86'
pins={'source-review86.eof-rebound.final.decision.json':'a3b010d144852bac09f5bd2593df6c679ad9a76d211bfbf58ed6521ab707c30c','source-review86.eof-rebound.final.run.json':'58438b142b71e94e516f2ec44049c2297bb71e7cc16e28571068686bc0148eb6','source-review86.eof-rebound.final.native-RAW-manifest.json':'9858b71471853117b1f959ce1efb2a9405722ce461c6559ee9782e0ff0b1ee0e'}
for n,h in pins.items():assert info(source/n)['raw_sha256']==h;exact(source/n)
sm=manifest(source/'source-review86.eof-rebound.final.native-RAW-manifest.json',['inputs','outputs'])
check_entry(sm['historical_analysis_manifest']);manifest(sm['historical_analysis_manifest']['path'],['inputs','outputs'])
native=load(source/'source-review86.eof-rebound.final.decision.json');sr=load(source/'source-review86.eof-rebound.final.run.json')
assert native['independent_from_formalizer'] and native['independent_from_decoder'] and native['reviewer']=='independent-primary-source-reviewer86'
assert native['verdict']=='equivalent-after-elaboration' and not native['repairs']
assert native['full_module_sha256']==MR and native['publication_binding_sha256']==BIND and native['reviewer_packet_sha256']==PACK
cov=native['source_graph_coverage']['coverage'];assert [cov[k] for k in ['explicit_inventory_anchors','accounted_explicit_anchors','nodes','relations','dependency_edges','excluded_associations']]==[72,72,38,76,73,3] and not cov['missing'] and cov['acyclic']
assert native['source_graph_coverage']['self_validation_of_original_overlay'] is False
check_entry(native['source_graph_coverage']['independent_fifth_edge_review'])
assert load(native['source_graph_coverage']['independent_fifth_edge_review']['path'])['verdict']=='ACCEPTED_EXACT_FIFTH_EDGE'
steps=native['authored_step_coverage'];assert [steps[k] for k in ['total','reviewed','exact_contiguous_code_regions']]==[11,11,11]
assert native['public_statement_coverage']['all14_definitions_audited'] and native['public_statement_coverage']['all_six_analytic_binders_audited']
unit=newlesson['units'][0]
for step in unit['steps']:
 reg=step['lean_source_region'];code=b''.join(path(M).read_bytes().splitlines(keepends=True)[reg['start_line']-1:reg['end_line']]);assert sha(code)==reg['exact_code_raw_sha256'] and code.decode()==step['lean'] and reg['source_raw_sha256']==MR
sp=load(B/'source-review86.eof-successor.packet.json');claimed=sp.pop('packet_sha256');assert claimed==PACK==sha(canon(sp))
audit=load(A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND and audit['semantic_slots']==native['semantic_slots']
assert audit['source_review']['review_run_sha256']==pins['source-review86.eof-rebound.final.run.json'] and audit['source_review']['reviewer_packet_sha256']==PACK and audit['source_review']['evidence']==native['review_evidence']
sa=load(B/'root.source86.eof-adoption.json');assert sa['status']=='ACCEPTED_INDEPENDENT_SOURCE_EOF_REBINDING' and sa['anonymous_byte_identical'] and sa['publication_binding_sha256']==BIND
for k in ['native_decision','native_manifest','native_run']:check_entry(sa[k])
decdir=B/'anonymous-decoder86';dm=load(decdir/'RAW-manifest.json');dec=load(decdir/'decoder-run.json');decoded=load(decdir/'decoder-result.json')
assert info(decdir/'RAW-manifest.json')['raw_sha256']==load(B/'root.decoder86.adoption.json')['native_manifest_RAW_sha256']
assert dm['allowed_inputs_only'] and not dm['source_text_visible'] and dec['allowed_inputs_only'] and not dec['source_text_visible'] and dec['decoder']=='independent-source-blind-decoder86'
for e in dm['input_artifacts']+dm['output_artifacts']:
 p=path(e['path']);assert info(p)['raw_sha256']==e['raw_sha256']
 copy=decdir/p.name if '.astis/decoder86/' in rel(p) else p
 assert copy.read_bytes()==p.read_bytes();exact(copy)
exact(decdir/'RAW-manifest.json')
dp=load(B/'anonymous.decoder86.json');declared=dp.pop('packet_sha256');assert declared==sha(canon(dp))==dec['packet_declared_sha256']=='eaeaa3182a52d5323b6a90cb8d1d0b9130907f387577936d534147cd6237e21c'
assert sha(dp['lean']['statement'].encode())==dec['anonymous_statement_sha256']
assert decoded['decoder_run_sha256']==info(decdir/'decoder-run.json')['raw_sha256']
assert sha(decoded['reconstructed_theorem_text'].encode())==dec['reconstructed_text_sha256']==info(decdir/'reconstruction.txt')['raw_sha256']
assert path(B/'anonymous.decoder86.json').read_bytes()==path(decdir/'anonymous.packet.json').read_bytes()==path(B/'eof-whitespace-repair86/anonymous.eof-successor.packet.json').read_bytes()
for p in ['tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_semantic_roundtrip.py','tools/astis_frontier_cells.py']:exact(p)
for e in archives.values():exact(e['raw_path'])
save('collaborator-preservation86.json',dict(baseline=info(baseline_path),RAWs=[info(p) for p in baseline],count=21))
helper=B/'commit_integration86.py';diff=git('diff','--',rel(helper))
with (O/'postscience-integration-helper.diff').open('xb') as f:f.write(diff)
save('postscience-helper-observation86.json',dict(helper=info(helper),science_blob_raw_sha256=sha(git('show',C+':'+rel(helper))),native_diff=info(O/'postscience-integration-helper.diff'),not_science_mathematical_evidence=True,production_and_reviewed_inputs_unchanged=True,reviewer_does_not_execute_helper=True))
save('input-freeze86.json',dict(verified_commit=C,base=BASE,exact_commit_matches=list(matches.values()),nested_mathlib_matches=list(nested.values()),local_fixed_primary_and_excluded_extracts=list(local.values()),local_compiled_artifacts=list(compiled.values()),preexisting_collaborator_inputs=list(collaborator_inputs.values()),historical_descriptors_resolved_without_native_mutation=historical,publication_binding_sha256=BIND,source_packet_sha256=PACK,native_source_chronology=sr['independent_chronology'],math_reuse='Own accepted full-source standard3axioms,19owned/4public+12private/39transitive/44edges kernel closure transferred over exact1LF deletion; unchanged 11 formula/code regions. Original math/source immutable; old canonical module/lesson descriptors resolve to explicit historical snapshots.',source_coverage=dict(inventory_items=47,anchors=72,nodes=38,relations=76,dependencies=73,excluded_associations=3)))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))));print(n,'EXIT',code,flush=True);assert code==0,n+' failed; native receipt/log retained'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
reviewed=O/'publication_reviewed86.py'
with reviewed.open('x',encoding='utf8',newline='\n') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
probe=O/'CurrentPublicKernel86.lean'
with probe.open('x',encoding='utf8',newline='\n') as f:f.write('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw\n#check '+D+'\n#print axioms '+D+'\n')
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw']),('current-kernel',[lake,'env',lean,str(probe)]),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(reviewed)]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
kerneltext=(O/'current-kernel.stdout.log').read_text('utf8');assert "[propext, Classical.choice, Quot.sound]" in kerneltext and 'sorryAx' not in kerneltext
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan86.json',dict(verifier_id='/root/exact_verify77',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
assert git('rev-parse','HEAD').decode().strip()==C
for group in [matches,nested,local,compiled,collaborator_inputs]:
 for e in group.values():assert info(e['path'])['raw_sha256']==e['raw_sha256']
for p,h in baseline.items():assert info(p)['raw_sha256']==h
save('checks-complete86.json',dict(status='PASS',verified_commit=C,verifier_id='/root/exact_verify77',publication_binding_sha256=BIND,source_packet_sha256=PACK,standard_axioms_only=True,actual_public_parents=summary['actual_public_producer_parents'],private_immediate_count=12,owned_count=19,transitive_ASTIS_constants=39,transitive_ASTIS_edges=44,source_coverage='47inventory/72anchors/38nodes/76relations=73dependencies+3excludedassociations; 11 exact helpers/publicBODY/formula regions',all21collaborator_RAWs_preserved=True,scope='Exact science only; integration/reader/main/PURIFIED/fullpaper/wholeGoal remain separate.'))
print('EXACT SCIENCE86 CHECKS PASS',flush=True)
