from pathlib import Path
import datetime,gzip,hashlib,json,os,re,subprocess,sys
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
C='d62f7b2c89e749953a36d8922124865a4651e55e';BASE='204fd4eee61724db77963cb33ddaddbcd90b906d'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualAbsoluteNextEventTime.lean';L='website/content/declaration_lessons/pbps-actual-absolute-next-event-time.json';P='website/content/publications/pbps-actual-absolute-next-event-time.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualAbsoluteNextEventTime.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_law';ID='ASTIS-SA-20261011-PBPSActualAbsoluteNextEventTime';CELL='ASTIS-SW-PBPS-actual-absolute-next-event-time'
def path(p):
 p=Path(p);return p if p.is_absolute() else R/p
def sha(b):return hashlib.sha256(b).hexdigest()
def rel(p):return path(p).relative_to(R).as_posix()
def info(p):
 p=path(p);return dict(path=rel(p),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def load(p):return json.loads(path(p).read_bytes())
def save(n,v):
 with (O/n).open('x',encoding='utf8',newline='\n') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
tree={row.split('\t',1)[1]:row.split()[2] for row in git('ls-tree','-r','--full-tree',C).decode().splitlines()}
def blob(r):return git('cat-file','blob',tree[r])
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
assert git('rev-parse','HEAD').decode().strip()==C
baseline_path=R/'runs/20261007-companion-priority/pbps-ordered-history-iteration-preread91/pre-fetch91.workspace-RAW.json';baseline=load(baseline_path)['tracked_modified'];assert len(baseline)==21
for p,h in baseline.items():assert info(p)['raw_sha256']==h
archives={rel(e['raw_path']):e for e in load(B/'immutable-RAW-archives91.json')['files']};extra=load(B/'science-archive-completion91.json');archives[extra['raw_path']]=extra
excluded=set(load(B/'public-source-exclusions91.json')['paths']);matched={};local={};archive_audit=[]
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if r in matched or r in local:return
 if r.startswith(('.astis/toolchain/','.lake/build/')) or r in baseline:
  local[r]=dict(**info(p),reason='Pinned runtime/cache or preserved collaborator input');return
 if r not in tree:
  if r in archives:
   e=archives[r];ab=blob(e['archive']);assert sha(ab)==e['archive_raw_sha256'];decompressed=gzip.decompress(ab);assert sha(decompressed)==e['raw_sha256'];assert decompressed==raw
   matched[r]=dict(**info(p),binding='lossless-committed-gzip',archive=e['archive'],archive_raw_sha256=sha(ab));return
  if r in excluded or r=='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html':
   local[r]=dict(**info(p),reason='Pinned source/private extract intentionally excluded from public commit');return
  raise AssertionError('MISSING COMMITTED EVIDENCE '+r)
 committed=blob(r)
 assert raw==committed or (r not in [M,L,P,A] and raw.replace(b'\r\n',b'\n')==committed.replace(b'\r\n',b'\n')),'BLOB MISMATCH '+r
 matched[r]=dict(**info(p),binding='git-blob',git_blob_raw_sha256=sha(committed),exact_RAW_equal=raw==committed)
def check(e):
 p=path(e['path']);assert info(p)['raw_sha256']==e['raw_sha256'],'RAW drift '+str(p)
 if 'bytes' in e:assert info(p)['bytes']==e['bytes']
 exact(p)
def manifest(p,groups):
 exact(p);v=load(p)
 for g in groups:
  for e in v[g]:check(e)
 return v
for p in [M,L,P,A,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl','research-wiki/frontier-cells/'+CELL+'.json',baseline_path]+[B/n for n in ['root.statement-seal91.json','claim.json','proved-local91.json','root.math91.adoption.json','root.decoder91.adoption.json','root.source91.adoption.json','anti-anchored.review91.json','immutable-RAW-archives91.json','science-archive-completion91.json','public-source-exclusions91.json','conceptual-mirror-audit91.json']]:exact(p)
md=load(B/'independent-math91/decision91.native.json');assert info(B/'independent-math91/decision91.native.json')['raw_sha256']=='335138e5ae1b59eff3f46bcc607ca3f5464a42e8d805848f6cd0785fd321ff79';assert md['decision']=='ACCEPT_LOCAL_MATHEMATICS_KERNEL_AND_EXPOSITION';check(md['production']);check(md['statement_seal']);[check(x) for x in md['reviewed_exposition']]
manifest(B/'independent-math91/closed-manifest91.native.json',['files']);exact(B/'independent-math91/closeout91.native.json')
assert path(M).read_bytes().startswith(b'import ');assert load(B/'root.statement-seal91.json')['expanded_literal_Prop'].encode() in path(M).read_bytes()
assert info('lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477';assert info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2';assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
source=B/'independent-source91';pins=load(B/'root.source91.adoption.json')['native_hashes']
assert pins=={'source-review91.native.json':'f4c5518262e3373ce206532c8fd16d2bed0ddf80c16c76351c90508c370bac87','review-run91.native.json':'4015dc4b614116c0acf7edbdd0285ef7e3eca784850b51a52ed6ba4b95d3c47f','closed-RAW91.native.json':'7b9aa6a8350e93c0fd986674c36c2517c1fd667af6b807401395ea4a1c3afe1d'}
for n,h in pins.items():assert info(source/n)['raw_sha256']==h;exact(source/n)
manifest(source/'closed-RAW91.native.json',['inputs','outputs'])
native=load(source/'source-review91.native.json');audit=load(A)
assert native['accepted'] and native['independent_from_formalizer'] and native['independent_from_decoder'] and native['reviewer']=='/root/primary_source91';assert not native['repairs'] and not any(x['blocking'] for x in native['deltas']);assert len(native['binder_audit'])==6 and len(native['literal_definition_audit'])==35 and len(native['body_exposition_audit'])==7 and len(native['source_coverage_audit'])==27
assert audit['state']=='accepted' and audit['source_review']['review_run_sha256']==pins['review-run91.native.json'] and audit['semantic_slots']==native['semantic_slots'] and len(audit['semantic_slots'])==7
BIND='17537bf9a2aec56bbafbeea370fc9741c88ae1d34b48743249cb1b99b655c921';PACK='37574d4aef043ed4415382a43b540f5b78831ef5b02e9f1eaca359103945eca6'
assert audit['publication_binding_sha256']==native['publication_binding_sha256']==BIND and audit['source_review']['reviewer_packet_sha256']==native['reviewer_packet_sha256']==PACK
packet=load(B/'anti-anchored.review91.json');assert packet.pop('packet_sha256')==sha(canon(packet))==PACK
for e in archives.values():
 ab=blob(e['archive']);assert sha(ab)==e['archive_raw_sha256'];rb=gzip.decompress(ab);assert sha(rb)==e['raw_sha256'];assert rb==path(e['raw_path']).read_bytes()
 if 'raw_bytes' in e:assert len(rb)==e['raw_bytes']
 archive_audit.append(dict(raw_path=e['raw_path'],archive=e['archive'],raw_sha256=sha(rb),committed_archive_sha256=sha(ab)))
# Bind the decoder's native run/result and anonymous packet as actual committed evidence.
dec=R/'runs/semantic-roundtrip/anonymous91/decoder-output';ad=load(B/'root.decoder91.adoption.json')
for n,h in ad['native_hashes'].items():assert info(dec/n)['raw_sha256']==h;exact(dec/n)
for p in [R/'runs/semantic-roundtrip/anonymous91/input.json',dec/'run.json',dec/'reconstruction.json',dec/'raw-manifest.json']:exact(p)
dr=load(dec/'run.json');reconstruction=load(dec/'reconstruction.json');dm=load(dec/'raw-manifest.json')
save('decoder-binding91.json',dict(native_manifest=info(dec/'raw-manifest.json'),native_run=info(dec/'run.json'),native_result=info(dec/'reconstruction.json'),canonical_audit_reconstruction=audit['reconstruction'],decoder_run=dr,decoder_manifest=dm))
dp=load(R/'runs/semantic-roundtrip/anonymous91/input.json');assert dp.pop('packet_sha256')==sha(canon(dp))==ad['canonical_packet_sha256'];assert not audit['reconstruction']['source_text_visible'];assert audit['reconstruction']['decoder_run_sha256']==info(dec/'run.json')['raw_sha256']
# The committed pre-science receipts are evidence; their historic negative diff check stays visible.
prior=[]
for p in (B/'checks91').rglob('receipt.json'):
 exact(p);v=load(p);prior.append(dict(**info(p),exit_code=v['exit_code'],argv=v.get('argv')))
 for n in ['stdout.log','stderr.log']:
  q=p.parent/n
  if q.exists():exact(q)
assert all(x['exit_code']==0 for x in prior if '/diff-check/' not in x['path'])
for p in [R/'tools'/n for n in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_frontier_cells.py','astis_semantic_roundtrip.py']]:exact(p)
save('archive-audit91.json',dict(status='PASS',verified_commit=C,count=len(archive_audit),archives=archive_audit,raw_natives_not_normalized=True))
save('input-freeze91.json',dict(verified_commit=C,base=BASE,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),all21collaborator_RAWs=[info(p) for p in baseline],source_review_pins=pins,publication_binding_sha256=BIND,canonical_reviewer_packet_sha256=PACK,prior_checks=prior,archive_count=len(archive_audit)))
print('PASS exact science inputs, native review, archive closure and21 collaborator RAWs',len(matched),len(archive_audit),flush=True)
