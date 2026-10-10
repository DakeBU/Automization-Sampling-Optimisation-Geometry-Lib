from pathlib import Path
import datetime,gzip,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
PR=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89'
C='58ddf518b7c75537680526fa809624ac7fe0b4c7';BASE='7c108c3181cee58bb9305445f903c5f71efda9c5';ME='/root/exact_verify77'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean';MR='36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37'
L='website/content/declaration_lessons/pbps-actual-conditional-next-wait-density.json';P='website/content/publications/pbps-actual-conditional-next-wait-density.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity.actual_conditional_next_wait_density'
ID='ASTIS-SA-20261011-PBPSActualConditionalNextWaitDensity';CELL='ASTIS-SW-PBPS-actual-conditional-next-wait-density';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitDensity.json'
BIND='4da0587d22739a11e111fc835b19408cd722d156f6876a03b84ef1c2673e2ade';PACK='2c336852a39e280610628e129e2f29b8edd1c77a1468bb943ae4d81501392f2f'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def rel(p):return path(p).relative_to(R).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
 p=path(p);b=p.read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def load(p):return json.loads(path(p).read_bytes())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=R,stderr=subprocess.PIPE)
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
assert git('rev-parse','HEAD').decode().strip()==C and git('rev-parse',C+'^').decode().strip()==BASE
baseline_path=PR/'pre-fetch89.workspace-RAW.json';baseline=load(baseline_path)['tracked_modified'];assert len(baseline)==21
for p,h in baseline.items():assert info(p)['raw_sha256']==h
archives={rel(e['raw_path']):e for e in load(B/'immutable-RAW-archives89.json')['files']}
recovery=load(B/'science-whitespace89.recovery.json')
archives[rel(recovery['native_snapshot'])]={'raw_path':recovery['native_snapshot'],'raw_bytes':recovery['native_bytes'],'raw_sha256':recovery['native_RAW_sha256'],'archive':recovery['lossless_archive'],'archive_raw_sha256':recovery['archive_RAW_sha256']}
excluded={rel(p) for p in load(B/'public-source-exclusions89.json')['paths']}
matches={};nested={};local={};preexisting={}
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if any(r in g for g in [matches,nested,local,preexisting]):return
 if r in baseline:
  assert sha(raw)==baseline[r];preexisting[r]=dict(**info(p),binding='Preexisting collaborator RAW preserved; not a science contribution.');return
 if r.startswith('.lake/packages/mathlib/'):
  blob=git('-C',str(R/'.lake/packages/mathlib'),'show','db584cd6d46c92f209a44c0f1c829460d327499d:'+r[len('.lake/packages/mathlib/'):]);assert raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
  nested[r]=dict(**info(p),upstream_commit='db584cd6d46c92f209a44c0f1c829460d327499d',git_blob_raw_sha256=sha(blob));return
 q=subprocess.run(['git','show',C+':'+r],cwd=R,capture_output=True);archive=None
 if q.returncode:
  if r=='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html' or r in excluded:
   if r not in excluded:assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
   local[r]=dict(**info(p),binding='Exact pinned private local source/snapshot; not claimed committed, exclusion/freeze committed.');return
  assert r in archives,'Missing named-commit/archive binding '+r
  e=archives[r];archive=rel(e['archive']);ab=git('show',C+':'+archive);assert path(archive).read_bytes()==ab and sha(ab)==e['archive_raw_sha256']
  blob=gzip.decompress(ab);assert sha(blob)==e['raw_sha256'] and len(blob)==e['raw_bytes']
 else:blob=q.stdout
 same=raw==blob;lf=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n');assert same or (r not in [M,L,P] and lf),'Current byte drift '+r
 matches[r]=dict(**info(p),git_blob_raw_sha256=sha(blob),exact_equal=same,newline_only_checkout_difference=not same,lossless_archive=archive)
def check(e,snapshot=False):
 p=path(e.get('closed_snapshot') if snapshot and e.get('closed_snapshot') else e['path']);h=e.get('raw_sha256',e.get('RAW_sha256',e.get('sha256')));size=e.get('bytes',e.get('RAW_bytes'))
 assert info(p)['raw_sha256']==h,'Unexplained RAW drift '+rel(p)
 assert size is None or info(p)['bytes']==size;exact(p)
def manifest(p,groups,snapshot=False):
 exact(p);v=load(p)
 for k in groups:
  for d in v.get(k,[]):check(d,snapshot)
 return v
science=[M,L,P,A,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl','research-wiki/frontier-cells/'+CELL+'.json']+[B/n for n in ['root.statement-seal89.json','claim.json','proved-local89.json','root.math89.adoption.json','root.source89.adoption.json','root.decoder89.adoption.json','source-review89.packet.json','immutable-RAW-archives89.json','public-source-exclusions89.json','publication-freeze89.after-exposition.json','conceptual-mirror-audit89.json','science-whitespace89.recovery.json']]
science+=['tools/'+n for n in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_frontier_cells.py','astis_semantic_roundtrip.py','astis_semantic_roundtrip_core.py']]+['.agents/skills/astis-substantive-advance/SKILL.md','.agents/skills/astis-semantic-roundtrip/SKILL.md','docs/contributor-codex-contract.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md']
for p in science:exact(p)
assert info(M)['raw_sha256']==MR and path(M).read_bytes()==git('show',C+':'+M)
assert info(L)['raw_sha256']=='e79d7ece6c0ef61a19caa473448b14d0b5e5001ae756cb394f4281514f1bb1c4'
assert info(P)['raw_sha256']=='7d96cf475f1300cf9e3d95eeacbc936741ec3316eb37ec61575cba3a92a9d66c'
assert info('lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
seal=load(B/'root.statement-seal89.json');assert seal['expanded_literal_Prop'].encode() in path(M).read_bytes();check(seal['header'])
math=B/'independent-math89';assert info(math/'closed-RAW-manifest89.authoritative.json')['raw_sha256']=='ca1a0ca744a6f27ccaeedaadbcbbac706a71375020fc07d8a5893a87c9adb3e5'
manifest(math/'closed-RAW-manifest89.authoritative.json',['frozen_current_inputs','owned_artifacts'])
md=load(math/'decision89.json');assert md['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY' and not md['required_repairs']
assert info(math/'decision89.json')['raw_sha256']==load(B/'root.math89.adoption.json')['native_decision_SHA256']
kernel=load(math/'kernel-dependency89.json');assert kernel['standard_axioms_only'] and kernel['all_project_constants_have_value'] and kernel['actual88_absent']
assert [kernel[k] for k in ['owned_constant_count','immediate_public_count','immediate_private_generated_count','transitive_ASTIS_constant_count','transitive_ASTIS_edge_count']]==[18,6,18,77,126]
for e in kernel['ASTIS_source_files']:check(e)
assert path(math/'FreshWholeSourceKernelClosure89.lean').read_bytes().startswith(path(M).read_bytes())
for n in ['fresh-focused-build','fresh-whole-source-kernel']:
 rec=load(math/(n+'.receipt.json'));assert rec['exit_code']==0 and rec['terminal_closed']
 for k in ['source','stdout','stderr']:check(rec[k])
unit=load(L)['units'][0];pub=load(P)['items'][0];assert unit['statement']==unit['lean_statement']==pub['statement'] and unit['assumptions']==pub['assumptions'] and len(unit['steps'])==6
for s in unit['steps']:
 reg=s['lean_source_region'];code=b''.join(path(M).read_bytes().splitlines(keepends=True)[reg['start_line']-1:reg['end_line']]);assert sha(code)==reg['exact_code_raw_sha256'] and code.decode()==s['lean'] and reg['source_raw_sha256']==MR
source=B/'independent-source89'
pins={'source-review89.decision.v2.native.json':'10d677f93444a33e805acd9c6dfc5e288bb97101335ddd4d2787f5f48d13ba84','source-review89.run.v2.native.json':'9dbd8c7cf34fa0ca08b270c2ae5d61a326766678f4427f4104914caa95d976a6','closed-raw-manifest.source-review89.v2.native.json':'9e9c6584ebcdc43832d9e42539e03c06844be2329f372c4e378afd13492448f5'}
for n,h in pins.items():assert info(source/n)['raw_sha256']==h;exact(source/n)
manifest(source/'closed-raw-manifest.source-review89.v2.native.json',['inputs','outputs'])
manifest(source/'closed-raw-manifest.source-review89.native.json',['inputs','outputs'])
first=manifest(PR/'independent-source-first89/closed-raw-manifest.source-first89.native.json',['inputs','outputs'])
preread=manifest(source/'closed-raw-manifest.final-preread89.native.json',['inputs','outputs'])
primary=path('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
for span in preread['exact_primary_spans']+first['primary_spans']:
 assert sha(primary[span['byte_start_zero_based']:span['byte_end_exclusive']])==span['raw_span_sha256']
manifest(PR/'header-math89/closed-RAW-manifest89.json',['frozen_current_inputs','owned_artifacts'])
top=load(PR/'header-math89/source-topology89.decision.json');assert not top['required_repairs']
native=load(source/'source-review89.decision.v2.native.json');original=load(source/'source-review89.decision.native.json')
assert native['verdict']=='equivalent-after-elaboration' and native['body_source_fidelity_acceptance'] and not native['blocking_deltas'] and not native['repairs']
assert native['reviewer']=='/root/fresh_source87' and native['independent_from_formalizer'] and native['independent_from_decoder'] and not native['topology_creator_self_independent_acceptance']
assert native['publication_binding_sha256']==BIND and native['reviewer_packet_sha256']==PACK
assert len(native['literal_definition_audit'])==23 and len(native['analytic_binder_audit'])==6 and len(native['body_audit'])==6
assert native['native_structured_reconstruction']==original['semantic_slots'] and native['deltas']==original['deltas']
assert 'density component' in native['accepted_truth_boundary']['target'] and 'full A.7' in native['accepted_truth_boundary']['open']
ch=[json.loads(x) for x in path(source/'chronology.final-source89.native.jsonl').read_text('utf8').splitlines()];assert ch[0]['event']=='DIRECT_PRIMARY89_REREAD_BEFORE_PRODUCTION_BODY_LESSON_DECODER_OR_REVIEW_PACKET' and not ch[0]['production_BODY89_read'] and not ch[0]['blind_reconstruction89_read'] and not ch[0]['mathematical_acceptance89_read']
sp=load(B/'source-review89.packet.json');declared=sp.pop('packet_sha256');assert declared==PACK==sha(canon(sp))
audit=load(A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND and audit['semantic_slots']==native['semantic_slots'] and len(audit['semantic_slots'])==7
assert audit['source_review']['review_run_sha256']==pins['source-review89.run.v2.native.json'] and audit['source_review']['reviewer_packet_sha256']==PACK
dec=R/'runs/semantic-decoder-outputs/round89';dm=manifest(dec/'manifest.json',['inputs','outputs']);dr=load(dec/'decoder-run.json');decoded=load(dec/'reconstruction.json')
assert info(dec/'manifest.json')['raw_sha256']==load(B/'root.decoder89.adoption.json')['native_manifest_RAW_sha256']
assert dm['decoder_identity']==dr['decoder_identity']=='/root/blind_decoder89' and not dm['source_text_visible'] and not decoded['source_text_visible']
for k in ['source_text_visible','source_identity_visible','source_anchor_visible','declaration_identity_visible','proof_visible','source_review_visible']:assert dr['context_disclosure'][k] is False
dp=load(B/'anonymous.decoder89.json');exact(B/'anonymous.decoder89.json');assert path(B/'anonymous.decoder89.json').read_bytes()==path(R/'runs/semantic-decoder-inputs/round89/packet.json').read_bytes()
assert sha(canon(dp))==load(B/'root.decoder89.adoption.json')['canonical_sorted_json_complete_sha256']
declared=dp.pop('packet_sha256');assert declared==sha(canon(dp))==load(B/'root.decoder89.adoption.json')['packet_sha256']
assert sha(dp['lean']['statement'].encode())==dm['statement_utf8_sha256']
assert decoded['decoder_run_sha256']==info(dec/'decoder-run.json')['raw_sha256'] and sha(decoded['reconstructed_theorem_text'].encode())==decoded['reconstructed_text_sha256']==dm['reconstructed_text_utf8_sha256']
assert audit['reconstruction']['text']==decoded['reconstructed_theorem_text']
unc=load(source/'decoder89.uncertainties.native.json');assert not unc['native_output_modified'] and not unc['blocking']
archive_audit=[]
for e in archives.values():
 exact(e['raw_path']);ab=git('show',C+':'+rel(e['archive']));assert ab==path(e['archive']).read_bytes() and sha(ab)==e['archive_raw_sha256']
 raw=gzip.decompress(ab);assert sha(raw)==e['raw_sha256'] and len(raw)==e['raw_bytes'] and path(e['raw_path']).read_bytes()==raw
 archive_audit.append(dict(archive=info(e['archive']),exact_decompressed_native=info(e['raw_path'])))
save('lossless-archives89.audit.json',dict(status='PASS',verified_commit=C,count=len(archive_audit),archives=archive_audit,manual_whitespace_diagnostic_recovery=info(B/'science-whitespace89.recovery.json'),no_native_normalization=True))
save('collaborator-preservation89.json',dict(baseline=info(baseline_path),count=21,RAWs=[info(p) for p in baseline]))
save('input-freeze89.json',dict(verified_commit=C,base=BASE,exact_commit_matches=list(matches.values()),nested_mathlib_matches=list(nested.values()),local_fixed_primary_and_excluded_extracts=list(local.values()),preexisting_collaborator_inputs=list(preexisting.values()),publication_binding_sha256=BIND,source_packet_sha256=PACK,math_reuse='Exact committed complete source matches accepted full elaboration with type+value/generated kernel closure:18owned/6public+18private immediate/77transitive/126edges/11sources. All6analytic/14model+9packaging defs retained. Current import is taken only after exact committed module equality.',source_native='Original complete source review and original seven structured slots retained; source-author v2 serializes schema-compatible slots without mathematical/source verdict change. Original full manifest and new inherited closure validated. Density component only; survival88 notAND.',historical_metadata='Original exposition snapshots and hash-only coordinator audit snapshot resolve historical pins. No old historical audit/lesson path is asserted to have current pre-repair bytes.',source_chronology=ch,observed_worktree=git('diff','--name-only').decode().splitlines(),postscience_helper_scope='Root integration helper changes are outside this science proof admission; no current helper is used as mathematical evidence.'))
print('EXACT COMMITTED INPUTS/NATIVE MATH/SOURCE/BLIND/ARCHIVES FROZEN',flush=True)
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=now()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))));print(n,'EXIT',code,flush=True);assert code==0,n+' failed; receipt retained'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
with (O/'publication_reviewed89.py').open('x',encoding='utf8',newline='\n') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
with (O/'CurrentPublicKernel89.lean').open('x',encoding='utf8',newline='\n') as f:f.write('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity\n#check '+D+'\n#print axioms '+D+'\n')
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity']),('current-kernel',[lake,'env',lean,str(O/'CurrentPublicKernel89.lean')]),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(O/'publication_reviewed89.py')]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
text=path(O/'current-kernel.stdout.log').read_text('utf8');ax=re.search(r'depends on axioms:\s*\[([^]]+)\]',text,re.S);assert ax and {x.strip() for x in ax.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'} and 'sorryAx' not in text
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan89.json',dict(verifier_id=ME,verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
assert git('rev-parse','HEAD').decode().strip()==C
for g in [matches,nested,local,preexisting]:
 for e in g.values():assert info(e['path'])['raw_sha256']==e['raw_sha256']
for p,h in baseline.items():assert info(p)['raw_sha256']==h
save('checks-complete89.json',dict(status='PASS',verified_commit=C,verifier_id=ME,publication_binding_sha256=BIND,source_packet_sha256=PACK,standard_axioms_only=True,actual_public_parents=kernel['immediate_public_producers'],owned_count=18,private_immediate_count=18,transitive_ASTIS_constants=77,transitive_ASTIS_edges=126,source_coverage='Only density-component S87-I5/G86-11; all23defs/sixanalytic/sevensemantic slots/sixcontiguousBODYformula regions. FullA7/global remainOPEN.',all21collaborator_RAWs_preserved=True))
print('EXACT SCIENCE89 CHECKS PASS',flush=True)
