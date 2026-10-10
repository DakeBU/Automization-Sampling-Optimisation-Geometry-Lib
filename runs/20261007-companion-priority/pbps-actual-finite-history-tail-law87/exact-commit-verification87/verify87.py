from pathlib import Path
import datetime,gzip,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
C='ada2d073d04a78493555b2ac35344b9c5a264bfc';BASE='ea5422f595d24b528cb84ad6fe24ea5097222a2c'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryTailLaw.lean';MR='01fcff944f1dbd42be2af30063b9baf4e191e2cde959e008724387cadb4fc899'
L='website/content/declaration_lessons/pbps-actual-finite-history-tail-law.json';P='website/content/publications/pbps-actual-finite-history-tail-law.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law';ID='ASTIS-SA-20261011-PBPSActualFiniteHistoryTailLaw';CELL='ASTIS-SW-PBPS-actual-finite-history-tail-law'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteHistoryTailLaw.json'
BIND='aca18a420581e6d76f5404a9991db270c46f875aabf7672488ad4a3c8fe05f59';PACK='876795a8b0d8ee2e569bf89bde988cb05a0e2a67aa3e8f527450a36139cb91a8'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def rel(p):return path(p).relative_to(R).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def load(p):return json.loads(path(p).read_bytes())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
assert git('rev-parse','HEAD').decode().strip()==C and git('rev-parse',C+'^').decode().strip()==BASE
baseline_path=R/'runs/20261007-companion-priority/pbps-clock-tail-preread87/pre-fetch87.workspace-RAW.json';baseline=load(baseline_path)['tracked_modified'];assert len(baseline)==21
for p,h in baseline.items():assert info(p)['raw_sha256']==h
archives={rel(e['raw_path']):e for e in load(B/'immutable-RAW-archives87.json')['files']}
excluded={rel(p) for p in load(B/'public-source-exclusions87.json')['paths']}
matches={};nested={};local={};preexisting={};historical=[]
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if any(r in x for x in [matches,nested,local,preexisting]):return
 if r in baseline:
  assert sha(raw)==baseline[r];preexisting[r]=dict(**info(p),binding='Preexisting collaborator RAW unchanged, not science-contributed content.');return
 if r.startswith('.lake/packages/mathlib/'):
  blob=git('-C',str(R/'.lake/packages/mathlib'),'show','db584cd6d46c92f209a44c0f1c829460d327499d:'+r[len('.lake/packages/mathlib/'):]);assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');nested[r]=dict(**info(p),upstream_commit='db584cd6d46c92f209a44c0f1c829460d327499d',git_blob_raw_sha256=sha(blob));return
 q=subprocess.run(['git','show',C+':'+r],cwd=R,capture_output=True);archive=None
 if q.returncode:
  if r=='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html' or r in excluded:
   if r not in excluded:assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
   local[r]=dict(**info(p),binding='Exact pinned private local primary/extract, explicitly not claimed committed; source freeze and RAW manifest committed.');return
  assert r in archives,'Missing named-commit/archive binding '+r
  e=archives[r];archive=rel(e['archive']);ab=git('show',C+':'+archive);assert sha(ab)==e['archive_raw_sha256'];blob=gzip.decompress(ab);assert sha(blob)==e['raw_sha256'] and len(blob)==e['raw_bytes']
 else:blob=q.stdout
 same=raw==blob;lf=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');assert same or (r not in [M,L,P] and lf),'Current byte drift '+r
 matches[r]=dict(**info(p),git_blob_raw_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archive)
math=B/'independent-math87';aliases={}
for e in load(math/'original-exposition-snapshot-index87.json')['snapshots']:aliases[(rel(e['original']['path']),e['original']['raw_sha256'])]=path(e['immutable_snapshot']['path'])
def check(e):
 expected=e.get('raw_sha256',e.get('RAW_sha256',e.get('sha256')));p=path(e['path']);size=e.get('bytes',e.get('RAW_bytes'))
 if info(p)['raw_sha256']!=expected:
  key=(rel(p),expected);assert key in aliases,'Unexplained historical drift '+rel(p);old=aliases[key]
  historical.append(dict(historical_descriptor=e,authoritative_immutable_snapshot=info(old),current_science=info(p),reason='Distinct accepted exact three-field exposition successor; original native manifest and original bytes retained.'));p=old
 assert info(p)['raw_sha256']==expected and (size is None or info(p)['bytes']==size),str(p)
 exact(p)
def manifest(p,groups):
 exact(p);d=load(p)
 for k in groups:
  for e in d.get(k,[]):check(e)
 return d
science=[M,L,P,A,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl','research-wiki/frontier-cells/'+CELL+'.json']+[B/n for n in ['root.statement-seal87.json','claim.json','proved-local87.json','root.math87.adoption.json','root.source87.adoption.json','root.decoder87.adoption.json','root.exposition87.adoption.json','source-review87.packet.json','immutable-RAW-archives87.json','public-source-exclusions87.json']]
science += [R/p for p in ['tools/astis.py','tools/astis_advance.py','tools/astis_publication.py','tools/astis_contributor_contract.py','tools/astis_frontier_cells.py','tools/astis_semantic_roundtrip.py','.agents/skills/astis-substantive-advance/SKILL.md','.agents/skills/astis-semantic-roundtrip/SKILL.md','docs/contributor-codex-contract.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md']]
for p in science:exact(p)
assert info(M)['raw_sha256']==MR and info(L)['raw_sha256']=='e6ba01830259ed4d886647c062c6658e07bcd4711636a93354b158c0d12719d5' and info(P)['raw_sha256']=='a8088607020c8685a5d675e7e5cce4de212aafb473e6a4877393d4da27c3a030'
assert info('lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477' and info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert load(B/'root.statement-seal87.json')['expanded_literal_Prop'].encode() in path(M).read_bytes()
assert info(math/'closed-RAW-manifest87.json')['raw_sha256']=='b43b0e0279c27278b84e7a615a7882e5cb3023de596a6207897945424abc0ee6'
manifest(math/'closed-RAW-manifest87.json',['frozen_current_inputs','owned_artifacts'])
assert load(math/'decision87.json')['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY' and not load(math/'decision87.json')['required_mathematical_repairs']
kernel=load(math/'kernel-dependency-summary87.json');assert kernel['standard_axioms_only'] and [kernel[k] for k in ['local_proof_constant_count','immediate_ASTIS_dependency_count','transitive_ASTIS_constant_count','unique_transitive_ASTIS_edge_count']]==[9,8,49,67] and len(kernel['immediate_public_theorem_parents'])==2
for e in load(math/'transitive-kernel-source-binding87.json')['distinct_project_source_files']:check(e)
assert path(math/'FreshWholeSourceKernelClosure87.lean').read_bytes().startswith(path(M).read_bytes())
for n in ['fresh-focused-build','fresh-whole-source-kernel']:assert load(math/(n+'.receipt.json'))['exit_code']==0 and load(math/(n+'.receipt.json'))['terminal_closed']
ex=B/'exposition-repair-review87';manifest(ex/'exposition-repair-review87.closed-RAW-manifest.json',['inputs','outputs'])
ed=load(ex/'exposition-repair-review87.decision.json');assert ed['verdict']=='ACCEPTED_EXACT_THREE_FIELD_EXPOSITION_REPAIR' and ed['reviewer']=='/root/fresh_source86' and ed['proposal_creator']=='/root/exact_verify77' and ed['changed_field_count']==3 and not ed['blocking_deltas'];check(ed['proposal'])
ea=load(B/'root.exposition87.adoption.json');assert ea['status']=='DISTINCT_EXACT_EXPOSITION_REPAIR_APPLIED_ONLY' and ea['publication_binding_sha256']==BIND
for n in ['lesson87.proposed-successor.json','publication87.proposed-successor.json']:assert path(math/n).read_bytes()==path(L if n.startswith('lesson') else P).read_bytes()
unit=load(L)['units'][0];assert len(unit['steps'])==6
for s in unit['steps']:
 reg=s['lean_source_region'];code=b''.join(path(M).read_bytes().splitlines(keepends=True)[reg['start_line']-1:reg['end_line']]);assert sha(code)==reg['exact_code_raw_sha256'] and code.decode()==s['lean'] and reg['source_raw_sha256']==MR
source=B/'independent-source87'
pins={'source-review87.decision.native.json':'af02799b5b85276bed23063b8af2e53243db65b0adf0de1c8a2e1a32c41c4f00','closed-raw-manifest.source-review87.native.json':'8c3a93806b9572639a47d75582bc01e9a8ce2a2789f94386b847b3e4d2a8850b','source-review87.run.native.json':'9e78cec2beb255fb7c78e2cfad6c87b7357b605cdc7f539d8fd093da574501ed'}
for n,h in pins.items():assert info(source/n)['raw_sha256']==h;exact(source/n)
sm=manifest(source/'closed-raw-manifest.source-review87.native.json',['inputs','outputs']);native=load(source/'source-review87.decision.native.json');sr=load(source/'source-review87.run.native.json')
assert native['verdict']=='equivalent-after-elaboration' and native['body_source_fidelity_acceptance'] and not native['blocking_deltas'] and not native['repairs']
assert native['reviewer']=='/root/fresh_source87' and native['independent_from_formalizer'] and native['independent_from_decoder']
assert native['publication_binding_sha256']==BIND and native['reviewer_packet_sha256']==PACK and native['lean_module_raw_sha256']==MR
assert len(native['complete_definition_audit'])==13 and len(native['complete_analytic_binder_audit'])==6 and len(native['exact_body_exposition_audit'])==6
assert all(x['mathematics']==x['exposition']=='accepted' and x['text_read'] and x['formula_read'] and x['exact_lean_read'] for x in native['exact_body_exposition_audit'])
assert native['accepted_truth_boundary']['closed_substrate']==['S87-I1','S87-I2','S87-I3'] and 'full A.7' in native['accepted_truth_boundary']['open']
primary=path(sr['primary_source']['path']).read_bytes();check(sr['primary_source'])
for span in sm['exact_primary_spans']:assert sha(primary[span['byte_start_zero_based']:span['byte_end_exclusive']])==span['raw_span_sha256']
first=path(sr['primary_first_freeze']['path']);check(sr['primary_first_freeze']);rawmanifest=first.parent/'primary-source.raw-manifest.native.json';exact(rawmanifest)
firstmanifest=load(rawmanifest)
for e in firstmanifest.get('inputs',[])+firstmanifest.get('outputs',[]):check(e)
chron=first.parent/'chronology.native.jsonl';exact(chron);ch=[json.loads(x) for x in chron.read_text('utf8').splitlines()];assert ch[0]['event']=='primary-source-opened-before-any-candidate' and ch[-1]['event']=='PRIMARY_FIRST_FREEZE_COMPLETED' and ch[-1]['candidate_exposure'] is False
seal=load(B/'root.statement-seal87.json');assert ch[-1]['utc']<seal['sealed_utc']
assert sr['independence_attestation']['primary_first'] and not sr['independence_attestation']['prior_source_verdict_contents_read'] and not sr['independence_attestation']['prior_repair_review_contents_read']
sp=load(B/'source-review87.packet.json');declared=sp.pop('packet_sha256');assert declared==PACK==sha(canon(sp))
audit=load(A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND and audit['semantic_slots']==native['semantic_slots'] and len(audit['semantic_slots'])==7
assert audit['source_review']['review_run_sha256']==pins['source-review87.run.native.json'] and audit['source_review']['reviewer_packet_sha256']==PACK and audit['source_review']['evidence']==native['review_evidence']
dec=B/'anonymous-decoder87';dm=load(dec/'raw-manifest.closed.json');dr=load(dec/'native-run-evidence.json');decoded=load(dec/'reconstruction.native.json')
assert info(dec/'raw-manifest.closed.json')['raw_sha256']==load(B/'root.decoder87.adoption.json')['native_manifest_RAW_sha256']
assert not dm['source_text_visible'] and not dr['source_text_visible'] and not dr['source_identity_visible'] and not dr['source_anchor_visible'] and not decoded['source_text_visible']
for e in dm['outputs']:
 p=path(e['path']);assert info(p)['raw_sha256']==e['raw_sha256'];copy=dec/p.name;assert copy.read_bytes()==p.read_bytes();exact(copy)
exact(dec/'raw-manifest.closed.json');exact(B/'anonymous.decoder87.json');assert path(dr['input_artifact']).read_bytes()==path(B/'anonymous.decoder87.json').read_bytes() and sha(path(dr['input_artifact']).read_bytes())==dr['raw_input_sha256']
dp=load(B/'anonymous.decoder87.json');assert sha(canon(dp))==dr['canonical_complete_packet_sha256'];declared=dp.pop('packet_sha256');assert declared==sha(canon(dp))==dr['declared_packet_sha256']==load(B/'root.decoder87.adoption.json')['packet_sha256']
assert decoded['decoder_run_sha256']==info(dec/'native-run-evidence.json')['raw_sha256'] and sha(decoded['reconstructed_theorem_text'].encode())==decoded['reconstructed_text_sha256'] and audit['reconstruction']['text']==decoded['reconstructed_theorem_text']
for e in archives.values():exact(e['raw_path'])
save('collaborator-preservation87.json',dict(baseline=info(baseline_path),count=21,RAWs=[info(p) for p in baseline]))
save('reviewer-schema-lookup-diagnosis87.json',dict(status='CORRECTED_READONLY_REVIEWER_SCHEMA_LOOKUP',tool_chunk='e196b6',failed_lookup="audit['decoder']",actual_schema='Canonical87 audit stores reconstruction and source_review; decoder evidence is in native-run-evidence.json/raw-manifest.closed.json, not legacy decoder-run.json.',mathematical_or_source_failure=False,canonical_changes=False,negative_retained_in_native_tool_output=True))
save('input-freeze87.json',dict(verified_commit=C,base=BASE,exact_commit_matches=list(matches.values()),nested_mathlib_matches=list(nested.values()),local_fixed_primary_and_excluded_extracts=list(local.values()),preexisting_collaborator_inputs=list(preexisting.values()),historical_descriptors_resolved_without_native_mutation=historical,publication_binding_sha256=BIND,source_packet_sha256=PACK,source_first_chronology=ch,math_reuse='Own unchanged exact01fc complete-source fresh elaboration, standard3axioms and type+value private/generated ASTIS closure; exact named science hashes and all native review RAW/artifacts rechecked. Exposition-only successor separately accepted by fresh_source86 then exact applied.',source_coverage='Frozen independently accepted source-slice87.v2:5nodes/4edges; I1-I3 local substrate only, I4-I5 remainOPEN; inherited global47inventory/38nodes/76relations unchanged.',observed_worktree_status=git('status','--porcelain').decode(),native_exposition_successor_independently_rechecked=True))
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=now()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))));print(n,'EXIT',code,flush=True);assert code==0,n+' failed; original terminal receipt retained'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
with (O/'publication_reviewed87.py').open('x',encoding='utf8',newline='\n') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
with (O/'CurrentPublicKernel87.lean').open('x',encoding='utf8',newline='\n') as f:f.write('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw\n#check '+D+'\n#print axioms '+D+'\n')
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw']),('current-kernel',[lake,'env',lean,str(O/'CurrentPublicKernel87.lean')]),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(O/'publication_reviewed87.py')]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
text=(O/'current-kernel.stdout.log').read_text('utf8');ax=re.search(r'depends on axioms:\s*\[([^]]+)\]',text,re.S);assert ax and {x.strip() for x in ax.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'} and 'sorryAx' not in text
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan87.json',dict(verifier_id='/root/exact_verify77',verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
assert git('rev-parse','HEAD').decode().strip()==C
for g in [matches,nested,local,preexisting]:
 for e in g.values():assert info(e['path'])['raw_sha256']==e['raw_sha256']
for p,h in baseline.items():assert info(p)['raw_sha256']==h
save('checks-complete87.json',dict(status='PASS',verified_commit=C,verifier_id='/root/exact_verify77',publication_binding_sha256=BIND,source_packet_sha256=PACK,standard_axioms_only=True,actual_public_parents=kernel['immediate_public_theorem_parents'],owned_count=9,private_immediate_count=6,transitive_ASTIS_constants=49,transitive_ASTIS_edges=67,source_coverage='Only I1-I3 of independently source-first-reviewed source-slice87.v2; I4/I5/globalA7 open. All13definitions/sixanalytic binders/seven semantic slots/six contiguous BODY/formula regions accepted.',all21collaborator_RAWs_preserved=True,scope='Named science only; serialized integration/reader/main/PURIFIED/fullpaper/wholeGoal remain separate.'))
print('EXACT SCIENCE87 CHECKS PASS',flush=True)
