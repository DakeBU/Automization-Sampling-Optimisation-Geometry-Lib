from pathlib import Path
import gzip,hashlib,json,re,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
C='a4599f28131fcf91d6b0754003facbc46e23ad2e';BASE='57ffbfed9ecde5d49c9dae4f9d2cb5aa593f26fe'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualOrderedPrefix.lean';L='website/content/declaration_lessons/pbps-actual-ordered-prefix.json';P='website/content/publications/pbps-actual-ordered-prefix.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOrderedPrefix.json';CELL='ASTIS-SW-PBPS-actual-ordered-prefix'
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
def canon(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
assert git('rev-parse','HEAD').decode().strip()==C
tree={row.split('\t',1)[1]:row.split()[2] for row in git('ls-tree','-r','--full-tree',C).decode().splitlines()}
cache={}
def blob(r):
 if r not in cache:cache[r]=git('cat-file','blob',tree[r])
 return cache[r]
baseline_path=R/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92/resume-before-seal92/preserved-collaborator92.json';baseline=load(baseline_path);assert len(baseline)==21;baseline_paths={e['path'] for e in baseline}
for e in baseline:assert info(e['path'])==e
archives={rel(e['raw_path']):e for n in ['immutable-RAW-archives92.json','science-console-archives92.json'] for e in load(B/n)['files']}
excluded=set(load(B/'public-source-exclusions92.json')['paths']);matched={};local={};archive_audit=[];archive_by_hash={}
for e in archives.values():
 ab=blob(e['archive']);assert sha(ab)==e['archive_raw_sha256'];rb=gzip.decompress(ab);assert sha(rb)==e['raw_sha256'];assert rb==path(e['raw_path']).read_bytes()
 if 'raw_bytes' in e:assert len(rb)==e['raw_bytes']
 archive_by_hash.setdefault(sha(rb),[]).append(e)
 archive_audit.append(dict(raw_path=rel(e['raw_path']),archive=e['archive'],raw_sha256=sha(rb),archive_raw_sha256=sha(ab)))
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if r in matched or r in local:return
 if r.startswith(('.astis/toolchain/','.lake/')) or r in baseline_paths:
  local[r]=dict(**info(p),reason='Pinned runtime/library/cache or preserved collaborator input');return
 if r not in tree:
  if r in archives:
   e=archives[r];assert gzip.decompress(blob(e['archive']))==raw
   matched[r]=dict(**info(p),binding='lossless-committed-gzip',archive=e['archive'],archive_raw_sha256=e['archive_raw_sha256']);return
  if r in excluded or r=='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html':
   local[r]=dict(**info(p),reason='Pinned primary/private extract deliberately excluded from public commit');return
  raise AssertionError('MISSING COMMITTED EVIDENCE '+r)
 committed=blob(r)
 assert raw==committed or (r not in [M,L,P,A] and raw.replace(b'\r\n',b'\n')==committed.replace(b'\r\n',b'\n')),'BLOB MISMATCH '+r
 matched[r]=dict(**info(p),binding='git-blob',git_blob_raw_sha256=sha(committed),exact_RAW_equal=raw==committed)
historical=[]
def check(e):
 p=path(e['path']);h=e.get('raw_sha256',e.get('sha256'))
 if sha(p.read_bytes())!=h:
  alternatives=archive_by_hash.get(h,[])
  assert alternatives,'UNRESOLVED HISTORICAL RAW '+str(p)+' '+str(h)
  a=alternatives[0];rb=gzip.decompress(blob(a['archive']))
  if 'bytes' in e:assert len(rb)==e['bytes']
  historical.append(dict(original_reference=e,resolved_committed_archive=a));return
 if 'bytes' in e:assert info(p)['bytes']==e['bytes']
 exact(p)
def manifest(p):
 exact(p);v=load(p)
 for g in ['inputs','outputs','files']:
  for e in v.get(g,[]):check(e)
 return v
for p in [M,L,P,A,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl','research-wiki/frontier-cells/'+CELL+'.json',baseline_path]+[B/n for n in ['root.statement-seal92.json','claim.json','proved-local92.v3.json','root.math92.adoption.json','root.math92.rename-adoption.json','root.math92.visibility-adoption.json','root.decoder92.adoption.json','root.source92.visibility-adoption.json','anti-anchored.review92.v3.json','immutable-RAW-archives92.json','science-console-archives92.json','public-source-exclusions92.json','conceptual-mirror-audit92.json']]:exact(p)
assert info(M)['raw_sha256']=='4737e98180ad69da03ad8b68f72f996ebe265b1eda1fafaa0521f591b7644ead'
norm=lambda x:re.sub(r'\s+',' ',x).strip()
statement=path(M).read_text(encoding='utf8').split('private def actual_ordered_prefix_statement',1)[1].split('set_option maxHeartbeats',1)[0]
assert norm(statement)==norm(load(B/'root.statement-seal92.json')['expanded_literal_Prop'])
assert info('lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477';assert info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2';assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
for folder,h in [('independent-math92','4636873806dbbae14ca155b9c7c8ea46371a11d7469c8f3ea7f7b36572116606'),('independent-private-rename92','7dee7ce6b91ffc17162f5de93de54719a6d6d625298a0e2f5390feae885d1baf'),('independent-visibility92','d58c046351f0f8e507a97dd941a566ab35155ba050f926785929b88047b6fd89')]:
 name={'independent-math92':'production-math-review92.native.json','independent-private-rename92':'private-rename-review92.native.json','independent-visibility92':'visibility-review92.native.json'}[folder]
 assert info(B/folder/name)['raw_sha256']==h;exact(B/folder/name);manifest(B/folder/'closed-RAW92.native.json')
source=B/'independent-source92/visibility-transfer92';ad=load(B/'root.source92.visibility-adoption.json');pins=ad['native_hashes']
assert pins=={'source-review92.v3.native.json':'5d0cc8a922ecd1a9a2c9dc3f299e087b5152a7ca92fe0b629b82f09c87e60b94','review-run92.v3.native.json':'75c19b604a7105c0d7f6f01103154a283445eb698838e897408ff248d5e37772','closed-RAW92.v3.native.json':'abc0f06a8c62ff637f6f997bdc6b0aa51e1975cd818b2ecdb3f2c9481e720bb2'}
for n,h in pins.items():assert info(source/n)['raw_sha256']==h;exact(source/n)
manifest(source/'closed-RAW92.v3.native.json')
native=load(source/'source-review92.v3.native.json');audit=load(A)
assert native['independent_from_formalizer'] and native['independent_from_decoder'] and native['reviewer']=='/root/primary_source91'
assert not native['repairs'] and not any(x.get('blocking',False) for x in native['deltas']);assert len(native['six_binder_audit'])==6 and len(native['definition_audit'])==25
assert audit['state']=='accepted' and audit['source_review']['review_run_sha256']==pins['review-run92.v3.native.json'] and audit['semantic_slots']==native['semantic_slots'] and len(audit['semantic_slots'])==7
BIND='5562848422a38455bcdd3fd7956692c4ac67b536b4b05e45382b7f2a68b1b43f';PACK='7b020b19642277b05b46fce89625db4caa215f716b30c80d119cd8389afc6e0d'
assert audit['publication_binding_sha256']==native['publication_binding_sha256']==BIND and audit['source_review']['reviewer_packet_sha256']==native['reviewer_packet_sha256']==PACK
packet=load(B/'anti-anchored.review92.v3.json');assert packet.pop('packet_sha256')==sha(canon(packet))==PACK
for k in ['module','publication','lesson','primary']:check(native[k])
dec=R/'runs/semantic-roundtrip/anonymous92/decoder';dm=load(dec/'closed-RAW.native.json');dr=dm['run_manifest'];result=load(dec/'decoder-result.native.json');da=load(B/'root.decoder92.adoption.json');inp=R/'runs/semantic-roundtrip/anonymous92/input.json';dp=load(inp)
for p in [inp,dec/'closed-RAW.native.json',dec/'decoder-result.native.json',dec/'reconstruction.md']:exact(p)
assert sha((dec/'closed-RAW.native.json').read_bytes())==da['native_manifest_raw_sha256']
assert dp.pop('packet_sha256')==sha(canon(dp))==da['canonical_packet_sha256']==dm['packet_sha256']
assert sha(canon(dr))==da['embedded_run_manifest_canonical_sha256']==dm['decoder_run_sha256']==audit['reconstruction']['decoder_run_sha256']
assert not dm['source_text_visible'] and not dr['source_text_visible'] and '/root/blind_decoder92' in dr['decoder_identity'];assert len(dr['inputs_consulted'])==3 and 'Only assigned input was read' in dr['isolation']
assert sha(inp.read_bytes())==dm['input_raw_sha256']==dr['input_raw_sha256'];assert sha(dp['lean']['statement'].encode())==dr['statement_sha256']
for n,h in dm['output_hashes'].items():assert info(dec/n)['raw_sha256']==h
assert audit['reconstruction']['text']==result['reconstructed_theorem_text']==(dec/'reconstruction.md').read_text(encoding='utf8');assert sha(result['reconstructed_theorem_text'].encode())==dr['reconstruction_sha256'];assert not audit['reconstruction']['source_text_visible']
save('decoder-binding92.json',dict(status='PASS',native_manifest=info(dec/'closed-RAW.native.json'),native_result=info(dec/'decoder-result.native.json'),run_manifest=dr,anonymous_input=info(inp),canonical_reconstruction_matches_native=True,embedded_run_canonical_hash_checked=True))
prior=[]
for p in (B/'checks92').rglob('receipt.json'):
 exact(p);v=load(p);prior.append(dict(**info(p),exit_code=v['exit_code'],argv=v.get('argv')))
 for n in ['stdout.log','stderr.log']:
  q=p.parent/n
  if q.exists():exact(q)
assert all(x['exit_code']==0 for x in prior if '/contributor/' not in x['path'] and '/publication/' not in x['path'])
for p in [R/'tools'/n for n in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_frontier_cells.py','astis_semantic_roundtrip.py']]:exact(p)
save('archive-audit92.json',dict(status='PASS',verified_commit=C,count=len(archive_audit),archives=archive_audit,historical_reference_resolutions=historical,raw_natives_not_normalized=True,resolver='git ls-tree then git cat-file blob object ID; no Windows path-based git-show dependency.'))
save('input-freeze92.json',dict(verified_commit=C,base=BASE,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),all21collaborator_RAWs=baseline,source_review_pins=pins,publication_binding_sha256=BIND,canonical_reviewer_packet_sha256=PACK,prior_checks=prior,archive_count=len(archive_audit),historical_reference_resolutions=historical))
print('PASS exact science inputs, native source/decoder/math review chains, archives, historical RAW resolution and 21 collaborator files',len(matched),len(archive_audit),flush=True)
