from pathlib import Path
import datetime,gzip,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
PR=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-preread88'
C='456e13f9561abcf01a285133e91b3951bf2ed892';BASE='24210c17b36c608fec3c259f811430cc9fc148cf'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitSurvival.lean';MR='2f509ce49343d349f7a9fb21d2f7b1697c1a6de942353f6cd8ff16d522911569'
L='website/content/declaration_lessons/pbps-actual-conditional-next-wait-survival.json';P='website/content/publications/pbps-actual-conditional-next-wait-survival.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival.actual_conditional_next_wait_survival'
ID='ASTIS-SA-20261011-PBPSActualConditionalNextWaitSurvival';CELL='ASTIS-SW-PBPS-actual-conditional-next-wait-survival'
A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitSurvival.json'
BIND='01f6aaf74fd89229d665d649fbe18d0769a8253b9c2e717d56772bb9678344bb';PACK='f9ddb7330489311cdb9471319785d4f369a9744eb1d0cbbdf441780a78fa9d1a'
ME='/root/exact_verify77'
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
assert git('rev-parse','HEAD').decode().strip()==C
assert git('rev-parse',C+'^').decode().strip()==BASE
baseline_path=PR/'pre-fetch88.workspace-RAW.json';baseline=load(baseline_path)['tracked_modified'];assert len(baseline)==21
for p,h in baseline.items():assert info(p)['raw_sha256']==h
archives={rel(e['raw_path']):e for e in load(B/'immutable-RAW-archives88.json')['files']}
excluded={rel(p) for p in load(B/'public-source-exclusions88.json')['paths']}
matches={};nested={};local={};preexisting={}
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if any(r in g for g in [matches,nested,local,preexisting]):return
 if r in baseline:
  assert sha(raw)==baseline[r];preexisting[r]=dict(**info(p),binding='Preexisting collaborator RAW unchanged, not science-contributed content.');return
 if r.startswith('.lake/packages/mathlib/'):
  blob=git('-C',str(R/'.lake/packages/mathlib'),'show','db584cd6d46c92f209a44c0f1c829460d327499d:'+r[len('.lake/packages/mathlib/'):])
  assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
  nested[r]=dict(**info(p),upstream_commit='db584cd6d46c92f209a44c0f1c829460d327499d',git_blob_raw_sha256=sha(blob));return
 q=subprocess.run(['git','show',C+':'+r],cwd=R,capture_output=True);archive=None
 if q.returncode:
  if r=='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html' or r in excluded:
   if r not in excluded:assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
   local[r]=dict(**info(p),binding='Exact pinned private local primary/extract, explicitly not claimed committed; source freeze and RAW manifest committed.');return
  assert r in archives,'Missing named-commit/archive binding '+r
  e=archives[r];archive=rel(e['archive']);ab=git('show',C+':'+archive)
  assert path(archive).read_bytes()==ab and sha(ab)==e['archive_raw_sha256']
  blob=gzip.decompress(ab);assert sha(blob)==e['raw_sha256'] and len(blob)==e['raw_bytes']
 else:blob=q.stdout
 same=raw==blob;lf=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
 assert same or (r not in [M,L,P] and lf),'Current byte drift '+r
 matches[r]=dict(**info(p),git_blob_raw_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archive)
def check(e):
 p=path(e['path']);h=e.get('raw_sha256',e.get('RAW_sha256',e.get('sha256')));size=e.get('bytes',e.get('RAW_bytes'))
 assert info(p)['raw_sha256']==h,'Unexplained current RAW drift '+rel(p)
 assert size is None or info(p)['bytes']==size
 exact(p)
def manifest(p,groups):
 exact(p);v=load(p)
 for k in groups:
  for d in v.get(k,[]):check(d)
 return v

science=[M,L,P,A,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl','research-wiki/frontier-cells/'+CELL+'.json']
science += [B/n for n in ['root.statement-seal88.json','claim.json','proved-local88.json','root.math88.adoption.json','root.source88.adoption.json','root.decoder88.adoption.json','source-review88.packet.json','immutable-RAW-archives88.json','public-source-exclusions88.json','publication-freeze88.json','conceptual-mirror-audit88.json','compiler-diagnosis88.json']]
science += ['tools/'+n for n in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_frontier_cells.py','astis_semantic_roundtrip.py']]
science += ['.agents/skills/astis-substantive-advance/SKILL.md','.agents/skills/astis-semantic-roundtrip/SKILL.md','docs/contributor-codex-contract.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md']
for p in science:exact(p)
assert info(M)['raw_sha256']==MR
assert info(L)['raw_sha256']=='30935077e0f7457da469f1ce18fc2bae4e2b598b80fb085af929229c56ee5796'
assert info(P)['raw_sha256']=='4636be49eb4a8793b8d44c2ccf91f2f3884c2b6ab8afa505f540abbed9ed99fd'
assert info('lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
seal=load(B/'root.statement-seal88.json');assert seal['expanded_literal_Prop'].encode() in path(M).read_bytes();check(seal['header'])

math=B/'independent-math88'
assert info(math/'closed-RAW-manifest88.json')['raw_sha256']=='bf9a452ef8c2de6d83b0fa6b1b4e89f07ca2cb26f7dc89005cb774984a2c4479'
manifest(math/'closed-RAW-manifest88.json',['frozen_current_inputs','owned_artifacts'])
md=load(math/'decision88.json');assert md['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY' and not md['required_repairs']
assert info(math/'decision88.json')['raw_sha256']==load(B/'root.math88.adoption.json')['native_decision_SHA256']
kernel=load(math/'kernel-dependency-summary88.json')
assert kernel['standard_axioms_only']
assert [kernel[k] for k in ['local_proof_constant_count','immediate_ASTIS_dependency_count','transitive_ASTIS_constant_count','unique_transitive_ASTIS_edge_count']]==[10,12,58,84]
assert len(kernel['immediate_public_theorem_parents'])==3
for e in load(math/'transitive-kernel-source-binding88.json')['distinct_project_source_files']:check(e)
assert path(math/'FreshWholeSourceKernelClosure88.lean').read_bytes().startswith(path(M).read_bytes())
for n in ['fresh-focused-build','fresh-whole-source-kernel']:
 rec=load(math/(n+'.receipt.json'));assert rec['exit_code']==0 and rec['terminal_closed']
 for k in ['source','stdout','stderr']:check(rec[k])
unit=load(L)['units'][0];pub=load(P)['items'][0]
assert unit['statement']==unit['lean_statement']==pub['statement'] and unit['assumptions']==pub['assumptions']
assert len(unit['steps'])==5
for s in unit['steps']:
 reg=s['lean_source_region'];code=b''.join(path(M).read_bytes().splitlines(keepends=True)[reg['start_line']-1:reg['end_line']])
 assert sha(code)==reg['exact_code_raw_sha256'] and code.decode()==s['lean'] and reg['source_raw_sha256']==MR

source=B/'independent-source88'
pins={'source-review88.decision.native.json':'aa702e1bc0972f90b77b3527ba6e3c68e4ba6e45760cd0221e683548f1bf9da6',
 'source-review88.run.native.json':'dd99702bb970341f85f740bfcaaac30286d086d82c3f38ba6d1afadd74b011a7',
 'closed-raw-manifest.source-review88.native.json':'e9c1c450aa255b65dba3ac3f8423ee02463165d54ed383b8b38328c80fcea332'}
for n,h in pins.items():assert info(source/n)['raw_sha256']==h;exact(source/n)
sm=manifest(source/'closed-raw-manifest.source-review88.native.json',['inputs','outputs'])
native=load(source/'source-review88.decision.native.json');sr=load(source/'source-review88.run.native.json')
assert native['verdict']=='equivalent-after-elaboration' and native['body_source_fidelity_acceptance'] and not native['blocking_deltas'] and not native['repairs']
assert native['reviewer']=='/root/fresh_source87' and native['independent_from_formalizer'] and native['independent_from_decoder']
assert not native['topology_creator_self_independent_acceptance']
assert native['publication_binding_sha256']==BIND and native['reviewer_packet_sha256']==PACK and native['lean_module_raw_sha256']==MR
assert len(native['complete_definition_audit'])==13 and len(native['complete_analytic_binder_audit'])==6 and len(native['exact_body_exposition_audit'])==5
assert all(x['verdict']=='accepted' and x['mathematics'] and x['exposition'] and x['exact_code_matches'] for x in native['exact_body_exposition_audit'])
for x,s in zip(native['exact_body_exposition_audit'],unit['steps']):
 assert x['text_sha256']==sha(s['text'].encode()) and x['formula_sha256']==sha(s['formula'].encode())
 assert all(x[k]==s['lean_source_region'][k] for k in ['path','source_raw_sha256','start_line','end_line','exact_code_raw_sha256'])
assert native['accepted_truth_boundary']['target_source_node']=='S87-I4' and 'full A.7' in native['accepted_truth_boundary']['open']
check(sr['primary']);primary=path(sr['primary']['path']).read_bytes()
for span in sm['exact_primary_spans']:assert sha(primary[span['byte_start_zero_based']:span['byte_end_exclusive']])==span['raw_span_sha256']
first=manifest(PR/'independent-source-first88/closed-raw-manifest.source-first88.native.json',['inputs','outputs'])
assert len(first['inputs'])==10 and len(first['outputs'])==9
for span in first['exact_primary_spans']:assert sha(primary[span['byte_start_zero_based']:span['byte_end_exclusive']])==span['raw_span_sha256']
ch=[json.loads(x) for x in path(PR/'independent-source-first88/chronology.native.jsonl').read_text('utf8').splitlines()]
assert ch[0]['event']=='DIRECT_PRIMARY88_READ_BEFORE_ANY_CANDIDATE'
assert ch[-1]['event']=='SOURCE_FIRST88_FREEZE_COMPLETED' and ch[-1]['candidate88_read'] is False
assert ch[-1]['utc']<seal['sealed_utc']
manifest(PR/'header-math88/closed-RAW-manifest88.json',['frozen_current_inputs','owned_artifacts'])
manifest(PR/'header-source88/closed-raw-manifest.header-source88.native.json',['inputs','outputs'])
top=load(PR/'header-math88/topology-review88.json');assert top['required_repairs']==[] and top['graph_creator_id']=='/root/fresh_source87' and top['reviewer_id']==ME
ch_body=[json.loads(x) for x in path(source/'chronology.source-review88.native.jsonl').read_text('utf8').splitlines()]
assert ch_body[0]['event']=='DIRECT_PRIMARY_REREAD_BEFORE_BODY_PACKET_OR_DECODER' and ch_body[0]['candidate_BODY_packet_read'] is False and ch_body[0]['decoder88_read'] is False and ch_body[0]['production88_read'] is False
ia=sr['independence_attestation'];assert ia['primary_reread_before_fresh_packet'] and not ia['prior_source_verdict_used_as_anchor'] and not ia['prior_independent_math_verdict_read'] and not ia['prior_repair_verdict_read']
sp=load(B/'source-review88.packet.json');declared=sp.pop('packet_sha256');assert declared==PACK==sha(canon(sp))
audit=load(A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND and audit['semantic_slots']==native['semantic_slots'] and len(audit['semantic_slots'])==7
assert audit['source_review']['review_run_sha256']==pins['source-review88.run.native.json'] and audit['source_review']['reviewer_packet_sha256']==PACK and audit['source_review']['evidence']==native['review_evidence']

dec=B/'anonymous-decoder';dm=manifest(dec/'closed-RAW-manifest.json',['inputs','outputs'])
dr=load(dec/'decoder.run.json');decoded=load(dec/'reconstructed-theorem.json')
assert info(dec/'closed-RAW-manifest.json')['raw_sha256']==load(B/'root.decoder88.adoption.json')['native_manifest_RAW_sha256']
assert not dm['source_text_visible'] and not dr['source_text_visible'] and not dr['source_identity_visible'] and not dr['source_anchor_visible'] and not decoded['source_text_visible']
assert dr['reviewer_identity']['agent']=='/root/blind_decoder88'
dp=load(B/'anonymous.decoder88.json');mi=dr['mathematical_inputs'][0];check(mi)
assert path(B/'anonymous.decoder88.json').read_bytes()==path(dec/'input.packet.RAW.json').read_bytes()
assert sha(canon(dp))==mi['canonical_sorted_json_complete_sha256']
declared=dp.pop('packet_sha256');assert declared==sha(canon(dp))==mi['packet_sha256_declared']==load(B/'root.decoder88.adoption.json')['packet_sha256']
assert sha(dp['lean']['statement'].encode())==mi['statement_sha256_computed']==mi['statement_sha256_declared']
assert decoded['decoder_run_sha256']==info(dec/'decoder.run.json')['raw_sha256']
assert sha(decoded['reconstructed_theorem_text'].encode())==decoded['reconstructed_text_sha256']==dr['reconstructed_text_sha256']
assert path(dec/'reconstructed-theorem.txt').read_text('utf8')==decoded['reconstructed_theorem_text']
assert audit['reconstruction']['text']==decoded['reconstructed_theorem_text']
clar=native['decoder_wording_clarification'];assert clar['classification']=='notation-resolution' and not clar['blocking'] and not clar['native_output_modified'] and not clar['canonical_overlay_required']
assert 'every function d on the entire' in decoded['quantifiers']
assert 'No assertion concerns' in decoded['scopes'] and 'future-threshold' in decoded['scopes']
assert 'fixed Borel function' in clar['assessment']

archive_audit=[]
for e in archives.values():
 exact(e['raw_path']);ab=git('show',C+':'+rel(e['archive']));assert ab==path(e['archive']).read_bytes() and sha(ab)==e['archive_raw_sha256']
 raw=gzip.decompress(ab);assert sha(raw)==e['raw_sha256'] and len(raw)==e['raw_bytes'] and path(e['raw_path']).read_bytes()==raw
 archive_audit.append(dict(archive=info(e['archive']),exact_decompressed_native=info(e['raw_path'])))
save('lossless-archives88.audit.json',dict(status='PASS_EVERY_INDEXED_ARCHIVE_COMMITTED_AND_LOSSLESS_NATIVE_EQUAL',verified_commit=C,index=info(B/'immutable-RAW-archives88.json'),count=len(archive_audit),archives=archive_audit,no_native_normalization=True))
save('collaborator-preservation88.json',dict(baseline=info(baseline_path),count=21,RAWs=[info(p) for p in baseline]))
save('input-freeze88.json',dict(verified_commit=C,base=BASE,exact_commit_matches=list(matches.values()),nested_mathlib_matches=list(nested.values()),local_fixed_primary_and_excluded_extracts=list(local.values()),preexisting_collaborator_inputs=list(preexisting.values()),publication_binding_sha256=BIND,source_packet_sha256=PACK,source_first_chronology=ch,source_BODY_chronology=ch_body,math_reuse='Own unchanged exact2f509 complete-source fresh elaboration, standard3axioms and type+value private/generated closure:10owned/12immediate/58transitive/84edges; actual87/75/77 public parents. All native bytes and exact science archive bindings checked, no repeated proof.',source_coverage='Independently accepted local9nodes/10AND edges; source creator distinct topology acceptance not self-issued. Only S87-I4 target; I5/fullG11/fullA7 remainOPEN. Full13definitions/sixanalytics/fivecontiguousBODYformula regions accepted.',metadata_evolution='Original publication-freeze88 lists historical draft audit/cell descriptors. Audit/cell themselves were not independent math input descriptors; no historical path hash is asserted current. Actual canonical science audit/cell bytes are independently checked here. Original source/math/native freezes unchanged.',decoder_wording='Native imprecise phrase d need not be deterministic retained untouched. Exact quantifiers fix a deterministic Borel history function; its value d(H_n) is random. Independent source reviewer resolved this notation explicitly, with no enlarged test class or repair. Verified interpretation agrees with actual private Prop/public statement.',observed_tracked_worktree_changes=git('diff','--name-only').decode().splitlines()))
print('EXACT INPUTS/ARCHIVES/SOURCE/BLIND/MATH FROZEN',flush=True)
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=now()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))));print(n,'EXIT',code,flush=True);assert code==0,n+' failed; receipt retained'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
with (O/'publication_reviewed88.py').open('x',encoding='utf8',newline='\n') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
with (O/'CurrentPublicKernel88.lean').open('x',encoding='utf8',newline='\n') as f:f.write('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival\n#check '+D+'\n#print axioms '+D+'\n')
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival']),('current-kernel',[lake,'env',lean,str(O/'CurrentPublicKernel88.lean')]),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(O/'publication_reviewed88.py')]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
text=path(O/'current-kernel.stdout.log').read_text('utf8');ax=re.search(r'depends on axioms:\s*\[([^]]+)\]',text,re.S)
assert ax and {x.strip() for x in ax.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'} and 'sorryAx' not in text
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan88.json',dict(verifier_id=ME,verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
assert git('rev-parse','HEAD').decode().strip()==C
for g in [matches,nested,local,preexisting]:
 for e in g.values():assert info(e['path'])['raw_sha256']==e['raw_sha256']
for p,h in baseline.items():assert info(p)['raw_sha256']==h
save('checks-complete88.json',dict(status='PASS',verified_commit=C,verifier_id=ME,publication_binding_sha256=BIND,source_packet_sha256=PACK,standard_axioms_only=True,actual_public_parents=kernel['immediate_public_theorem_parents'],owned_count=10,private_immediate_count=9,transitive_ASTIS_constants=58,transitive_ASTIS_edges=84,source_coverage='Only S87-I4 conditional survival closed;13actualdefs/sixanalytics/sevensemantic slots/fivecompleteBODYformula regions and distinct topology accepted. I5/fullG11/fullA7/global obligations remainOPEN.',all21collaborator_RAWs_preserved=True,scope='Exact science only; shared aggregate/Registry/reader/browser/main/PURIFIED/fullpaper/Goal remain separate.'))
print('EXACT SCIENCE88 CHECKS PASS',flush=True)
