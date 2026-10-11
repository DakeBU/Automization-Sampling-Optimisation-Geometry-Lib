from pathlib import Path
import datetime,gzip,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
PR=R/'runs/20261007-companion-priority/pbps-next-history-extension-preread90'
C='8f70c088b7c06f4a3048ff5966f4dda7903f0aa0';BASE='d3bdf486a84f8edaac6930336879b87949fd113c';ME='/root/exact_verify77'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteHistoryExtension.lean';MR='6cdc14328be5ec3ece3f028e6e1dd0185ee4031a8e651956ee0f55d4beebf029'
L='website/content/declaration_lessons/pbps-actual-finite-history-extension.json';P='website/content/publications/pbps-actual-finite-history-extension.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension.actual_finite_history_extension'
ID='ASTIS-SA-20261011-PBPSActualFiniteHistoryExtension';CELL='ASTIS-SW-PBPS-actual-conditional-next-wait-density';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteHistoryExtension.json'
BIND='b3a9241d785c8132839c366f260d5fbc3dcaa40aba8566560ec814e6c5716472';PACK='e05eb6e6f0301337eb17e14396af2577aeb852a022557b036c3e536735906000'
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
baseline_path=R/'runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89/pre-fetch89.workspace-RAW.json';baseline=load(baseline_path)['tracked_modified'];assert len(baseline)==21
for p,h in baseline.items():assert info(p)['raw_sha256']==h
archives={rel(e['raw_path']):e for e in load(B/'immutable-RAW-archives90.json')['files']}
excluded={rel(p) for p in load(B/'public-source-exclusions90.json')['paths']}
matches={};nested={};local={};preexisting={}
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if any(r in g for g in [matches,nested,local,preexisting]):return
 if r.startswith(('.astis/toolchain/','.lake/build/')):
  local[r]=dict(**info(p),binding='Pinned local toolchain executable or build cache; not asserted committed.');return
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
resolutions={}
for e in load(B/'independent-math90/historical-input-resolution90.json')['resolutions']:
 resolutions[(rel(e['path']),e['raw_sha256'])]=e['closed_snapshot']
for e in load(B/'independent-source90/mutable-input-snapshots90.native.json')['snapshots']:
 resolutions[(rel(e['original_path']),e['raw_sha256'])]=e['snapshot_path']
resolved=[]
def check(e,snapshot=True):
 h=e.get('raw_sha256',e.get('RAW_sha256',e.get('sha256')));size=e.get('bytes',e.get('RAW_bytes'))
 original=e['path'];target=e.get('closed_snapshot') or resolutions.get((rel(original),h),original)
 if isinstance(target,dict):target=target['path']
 p=path(target);assert info(p)['raw_sha256']==h,'Unexplained RAW drift '+rel(p)
 assert size is None or info(p)['bytes']==size;exact(p)
 if rel(p)!=rel(original):resolved.append(dict(original_path=rel(original),raw_sha256=h,immutable_snapshot=info(p)))
def manifest(p,groups,snapshot=True):
 exact(p);v=load(p)
 for k in groups:
  for d in v.get(k,[]):check(d,snapshot)
 return v
science=[M,L,P,A,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl','research-wiki/frontier-cells/'+CELL+'.json']+[B/n for n in ['root.statement-seal90.json','claim.json','proved-local90.json','root.math90.adoption.json','root.source90.adoption.json','root.decoder90.adoption.json','source-review90.packet.json','immutable-RAW-archives90.json','public-source-exclusions90.json','publication-freeze90.after-exposition.json','conceptual-mirror-audit90.json']]
science+=['tools/'+n for n in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_frontier_cells.py','astis_semantic_roundtrip.py','astis_semantic_roundtrip_core.py']]+['.agents/skills/astis-substantive-advance/SKILL.md','.agents/skills/astis-semantic-roundtrip/SKILL.md','docs/contributor-codex-contract.md','docs/theorem-publication-protocol.md','docs/proof-digestion-protocol.md','docs/evidence-routed-memory-protocol.md']
for p in science:exact(p)
assert info(M)['raw_sha256']==MR and path(M).read_bytes()==git('show',C+':'+M)
assert info(L)['raw_sha256']=='f8e3db3c9cffc10938fc6350ec16a589eeb43dc2130c48f0f41544511a56b905'
assert info(P)['raw_sha256']=='908c65e23b7608a2609a515da742a1db378f087c3143807cf1ed21a5f8728022'
assert info('lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
seal=load(B/'root.statement-seal90.json');assert seal['expanded_literal_Prop'].encode() in path(M).read_bytes();check(seal['header'])
math=B/'independent-math90'
assert info(math/'closed-RAW-manifest90.json')['raw_sha256']=='e1c7416c51b114e634d6eb1e9928e2d5bd5a75c3bcf8135bb7bcb928399ae647'
manifest(math/'closed-RAW-manifest90.json',['frozen_inputs','owned_artifacts'])
md=load(math/'decision90.json');assert md['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_AND_CURRENT_EXPOSITION_ONLY' and not md['required_repairs']
assert info(math/'decision90.json')['raw_sha256']==load(B/'root.math90.adoption.json')['native_decision_SHA256']
kernel=load(math/'kernel-dependency90.json');assert kernel['standard_axioms_only'] and kernel['all_project_constants_have_value'] and kernel['actual88_absent']
assert [kernel[k] for k in ['owned_constant_count','immediate_public_count','immediate_private_generated_count','transitive_ASTIS_constant_count','transitive_ASTIS_edge_count']]==[11,4,18,95,170]
for e in kernel['ASTIS_source_files']:check(e)
assert path(math/'FreshWholeSourceKernelClosure90.lean').read_bytes().startswith(path(M).read_bytes())
for n in ['fresh-focused-build','fresh-whole-source-kernel']:
 rec=load(math/(n+'.receipt.json'));assert rec['exit_code']==0 and rec['terminal_closed']
 for k in ['source','stdout','stderr']:check(rec[k])
unit=load(L)['units'][0];pub=load(P)['items'][0];assert unit['statement']==pub['statement'] and unit['assumptions']==pub['assumptions'] and len(unit['steps'])==6
covered=[]
for s in unit['steps']:
 reg=s['lean_source_region'];code=b''.join(path(M).read_bytes().splitlines(keepends=True)[reg['start_line']-1:reg['end_line']]);assert sha(code)==reg['exact_code_raw_sha256'] and code.decode()==s['lean'] and reg['source_raw_sha256']==MR
 covered+=list(range(reg['start_line'],reg['end_line']+1))
assert covered==list(range(120,341))
source=B/'independent-source90'
pins={'source-review90.decision.native.json':'87cac8474e5993931ef3fae75873831d79605b7b6a3558a4b016506defbebb78','source-review90.run.native.json':'ed4231896ef29e595796214d0a77e0b76e6389435ea66cab940216d080ec52c7','closed-raw-manifest.source-review90.native.json':'b0a4ef4cf716d39d191d1f32eb23891a34e6cc2b14920179d28397b34aeef950'}
for n,h in pins.items():assert info(source/n)['raw_sha256']==h;exact(source/n)
manifest(source/'closed-raw-manifest.source-review90.native.json',['inputs','outputs'])
manifest(source/'closed-raw-manifest.final-preread90.native.json',['inputs','outputs'])
manifest(PR/'independent-source-first90/closed-raw-manifest.source-first90.native.json',['inputs','outputs'])
manifest(PR/'independent-header-math90/closed-RAW-manifest90.json',['frozen_inputs','owned_artifacts'])
manifest(PR/'independent-topology-repair90/closed-raw-manifest90.json',['inputs','artifacts'])
manifest(B/'independent-exposition-repair90/closed-raw-manifest90.json',['inputs','artifacts'])
primary=path('runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
spans=load(source/'primary-source90.final-preread.raw-manifest.native.json')['anchors']
for span in spans:assert sha(primary[span['byte_start_zero_based']:span['byte_end_exclusive']])==span['raw_span_sha256']
native=load(source/'source-review90.decision.native.json')
assert native['verdict']=='equivalent-after-elaboration' and native['body_source_fidelity_acceptance'] and not native['blocking_deltas'] and not native['repairs']
assert native['reviewer']=='/root/fresh_source87' and native['independent_from_formalizer'] and native['independent_from_decoder'] and not native['topology_creator_self_independent_acceptance']
assert native['publication_binding_sha256']==BIND and native['reviewer_packet_sha256']==PACK
assert native['literal_definition_count']==len(native['literal_definition_audit'])==28 and native['analytic_binder_count']==len(native['analytic_binder_audit'])==6 and len(native['body_audit'])==6
assert not native['accepted_truth_boundary']['graph_creator_self_independent_approval']
assert 'full A7' in native['accepted_truth_boundary']['open']
ch=[json.loads(x) for x in path(source/'chronology.final-source90.native.jsonl').read_text('utf8').splitlines()]
assert ch[0]['event']=='DIRECT_PRIMARY_REREAD_BEFORE_FINAL90_BODY_LESSON_DECODER_PACKET' and not ch[0]['new90_BODY_read'] and not ch[0]['new90_decoder_read']
assert not ch[1]['math_acceptance90_read']
sp=load(B/'source-review90.packet.json');declared=sp.pop('packet_sha256');assert declared==PACK==sha(canon(sp))
audit=load(A);assert audit['state']=='accepted' and audit['publication_binding_sha256']==BIND and audit['semantic_slots']==native['semantic_slots'] and len(audit['semantic_slots'])==7
assert audit['source_review']['review_run_sha256']==pins['source-review90.run.native.json'] and audit['source_review']['reviewer_packet_sha256']==PACK
dec=R/'runs/semantic-decoder-outputs/round90';dm=manifest(dec/'manifest.json',['inputs','outputs']);dr=load(dec/'decoder-run.json');decoded=load(dec/'reconstruction.json')
adopt=load(B/'root.decoder90.adoption.json');assert info(dec/'manifest.json')['raw_sha256']==adopt['native_manifest_RAW_sha256']
assert dm['decoder']['identity']==dr['decoder']['identity']=='independent-source-blind-decoder-round90' and dr['decoder']['agent_task']=='/root/blind_decoder90'
for k,v in dr['disclosure_flags'].items():assert v is False
assert not dr['extra_mathematical_inputs'] and not decoded['source_text_visible']
dp=load(B/'anonymous.decoder90.json');exact(B/'anonymous.decoder90.json');assert path(B/'anonymous.decoder90.json').read_bytes()==path(R/'runs/semantic-decoder-inputs/round90/packet.json').read_bytes()
declared=dp.pop('packet_sha256');assert declared==sha(canon(dp))==adopt['packet_sha256']
assert sha(dp['lean']['statement'].encode())==dm['statement_utf8_sha256']
assert decoded['decoder_run_sha256']==info(dec/'decoder-run.json')['raw_sha256'] and sha(decoded['reconstructed_theorem_text'].encode())==decoded['reconstructed_text_sha256']==dm['reconstructed_text_utf8_sha256']
assert audit['reconstruction']['text']==decoded['reconstructed_theorem_text']
archive_audit=[]
for e in archives.values():
 exact(e['raw_path']);ab=git('show',C+':'+rel(e['archive']));assert ab==path(e['archive']).read_bytes() and sha(ab)==e['archive_raw_sha256']
 raw=gzip.decompress(ab);assert sha(raw)==e['raw_sha256'] and len(raw)==e['raw_bytes'] and path(e['raw_path']).read_bytes()==raw
 archive_audit.append(dict(archive=info(e['archive']),exact_decompressed_native=info(e['raw_path'])))
save('lossless-archives90.audit.json',dict(status='PASS',verified_commit=C,count=len(archive_audit),archives=archive_audit,no_native_normalization=True))
save('collaborator-preservation90.json',dict(baseline=info(baseline_path),count=21,RAWs=[info(p) for p in baseline]))
save('input-freeze90.json',dict(verified_commit=C,base=BASE,exact_commit_matches=list(matches.values()),nested_mathlib_matches=list(nested.values()),local_fixed_primary_and_excluded_extracts=list(local.values()),preexisting_collaborator_inputs=list(preexisting.values()),publication_binding_sha256=BIND,source_packet_sha256=PACK,math_reuse='Exact committed whole-source and generated type+value kernel closure:11owned/4public+18private immediate/95transitive/170edges/12sources; sixanalytics and28 literal definitions.',source_native='Independent source native wholeBODY and seven canonical semantic slots, own prior topology and distinct repairs; actual88 notAND.',historical_metadata=resolved,source_chronology=ch,observed_worktree=git('diff','--name-only').decode().splitlines(),postscience_helper_scope='Integration-only helper edits are outside this science proof admission and not mathematical evidence.'))
print('EXACT COMMITTED INPUTS/NATIVE MATH/SOURCE/BLIND/ARCHIVES FROZEN',flush=True)
env=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf8');env.pop('ELAN_TOOLCHAIN',None);env['PATH']=str(R/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
def run(n,args):
 start=now()
 with (O/(n+'.stdout.log')).open('xb') as out,(O/(n+'.stderr.log')).open('xb') as err:
  child=subprocess.Popen(args,cwd=R,env=env,stdout=out,stderr=err);print(n,'foreground PID',child.pid,flush=True);code=child.wait()
 save(n+'.receipt.json',dict(command=args,cwd=str(R),checked_commit=C,actual_foreground_PID=child.pid,exit_code=code,terminal_closed=True,started_utc=start,finished_utc=now(),stdout=info(O/(n+'.stdout.log')),stderr=info(O/(n+'.stderr.log'))));print(n,'EXIT',code,flush=True);assert code==0,n+' failed; receipt retained'
py=[sys.executable,'-X','utf8'];lake=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
with (O/'publication_reviewed90.py').open('x',encoding='utf8',newline='\n') as f:f.write("import sys\nsys.path[:0]=['E:/Samplinglib','E:/Samplinglib/tools']\nfrom tools.astis_publication import check_advance\ncheck_advance(["+repr(D)+"],reviewed=True)\nprint('PUBLICATION REVIEWED=TRUE PASS')\n")
with (O/'CurrentPublicKernel90.lean').open('x',encoding='utf8',newline='\n') as f:f.write('import AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension\n#check '+D+'\n#print axioms '+D+'\n')
for n,args in [('packet',py+['tools/astis_publication.py','packet','--cell',CELL]),('focused-module',[lake,'build','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryExtension']),('current-kernel',[lake,'env',lean,str(O/'CurrentPublicKernel90.lean')]),('contributor',py+['tools/astis_contributor_contract.py','check','--base',BASE]),('publication',py+['tools/astis_publication.py','check','--base',BASE]),('publication-reviewed',py+[str(O/'publication_reviewed90.py')]),('semantic',py+['tools/astis_semantic_roundtrip.py','check']),('frontier',py+['tools/astis_frontier_cells.py','check'])]:run(n,args)
packet=load(O/'packet.stdout.log');assert len(packet['targets'])==1 and packet['targets'][0]['publication_binding_sha256']==BIND
text=path(O/'current-kernel.stdout.log').read_text('utf8');ax=re.search(r'depends on axioms:\s*\[([^]]+)\]',text,re.S);assert ax and {x.strip() for x in ax.group(1).split(',')}=={'propext','Classical.choice','Quot.sound'} and 'sorryAx' not in text
sys.path[:0]=[str(R),str(R/'tools')];from tools import astis
hits=astis.forbidden_pattern_hits();save('fake-closure-scan90.json',dict(verifier_id=ME,verified_commit=C,algorithm='tools.astis.forbidden_pattern_hits()',scanned_files=len(astis.lean_source_files()),hits=hits,module=info(M)));assert not hits
assert git('rev-parse','HEAD').decode().strip()==C
for g in [matches,nested,local,preexisting]:
 for e in g.values():assert info(e['path'])['raw_sha256']==e['raw_sha256']
for p,h in baseline.items():assert info(p)['raw_sha256']==h
save('checks-complete90.json',dict(status='PASS',verified_commit=C,verifier_id=ME,publication_binding_sha256=BIND,source_packet_sha256=PACK,standard_axioms_only=True,actual_public_parents=kernel['immediate_public_producers'],owned_count=11,private_immediate_count=18,transitive_ASTIS_constants=95,transitive_ASTIS_edges=170,source_coverage='One next-history strict finite transport step S87-I5/G86-11; all28defs/sixanalytics/sevensemantic slots/six contiguousBODYregions. FullA7/global remainOPEN.',all21collaborator_RAWs_preserved=True))
print('EXACT SCIENCE90 CHECKS PASS',flush=True)
