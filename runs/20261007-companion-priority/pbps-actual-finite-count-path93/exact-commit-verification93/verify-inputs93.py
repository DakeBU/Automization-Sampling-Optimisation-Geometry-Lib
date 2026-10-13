from pathlib import Path
import gzip,hashlib,json,re,subprocess
R=Path('E:/Samplinglib');O=Path(__file__).parent;B=O.parent
C='8ec33d055fb8a9b3ba376d4113e388b00882026f';BASE='a50632d37112aa59b7368079a917add0c69d0852'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean';L='website/content/declaration_lessons/pbps-actual-finite-count-path.json';P='website/content/publications/pbps-actual-finite-count-path.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteCountPath.json';CELL='ASTIS-SW-PBPS-actual-finite-count-path'
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
assert git('rev-parse','HEAD').decode().strip()==C
assert git('merge-base',BASE,C).decode().strip()==BASE
tree={row.split('\t',1)[1]:row.split()[2] for row in git('ls-tree','-r','--full-tree',C).decode().splitlines()}
cache={}
def blob(r):
 if r not in cache:cache[r]=git('cat-file','blob',tree[r])
 return cache[r]
prior92=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92/exact-commit-verification92/closed-RAW-manifest92.json'
baseline=load(prior92)['preserved_collaborator_inputs'];assert len(baseline)==21
baseline_paths={rel(x['path']) for x in baseline}
for x in baseline:assert info(x['path'])['raw_sha256']==x['raw_sha256']
archive_maps=['immutable-RAW-archives93.json','science-text-RAW-archives93.json']
archives={rel(x['raw_path']):x for n in archive_maps for x in load(B/n)['files']}
excluded=set(load(B/'public-source-exclusions93.json')['paths'])
primary='runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
matched={};local={};historical=[];archive_audit=[];archive_by_hash={}
snapshot_by_hash={}
for r in tree:
 if r.startswith(rel(B)+'/') and not r.endswith('.gz') and any(mark in r for mark in ['.RAW','.snapshot','exactraw']):
  snapshot_by_hash.setdefault(sha(blob(r)),[]).append(r)
for r,x in archives.items():
 ab=blob(rel(x['archive']));assert sha(ab)==x['archive_raw_sha256'],r
 rb=gzip.decompress(ab);assert sha(rb)==x['raw_sha256'] and len(rb)==x['raw_bytes'],r
 assert rb==path(r).read_bytes(),'native archival mismatch '+r
 if 'public_text_raw_sha256' in x:assert sha(blob(r))==x['public_text_raw_sha256'],r
 archive_by_hash.setdefault(sha(rb),[]).append(x)
 archive_audit.append(dict(raw_path=r,archive=rel(x['archive']),raw_sha256=sha(rb),archive_raw_sha256=sha(ab)))
print('ARCHIVES PASS',len(archive_audit),flush=True)
def exact(p):
 p=path(p);r=rel(p);raw=p.read_bytes()
 if r in matched or r in local:return
 if r.startswith(('.astis/toolchain/','.lake/')) or r in baseline_paths:
  local[r]=dict(**info(p),reason='Pinned runtime/library or preserved collaborator input');return
 if r==primary or r in excluded:
  local[r]=dict(**info(p),reason='Deliberately local-only primary/private source or excluded evidence');return
 if r in archives and r not in [M,L,P,A]:
  x=archives[r];assert gzip.decompress(blob(rel(x['archive'])))==raw
  matched[r]=dict(**info(p),binding='lossless-committed-gzip',archive=x['archive'],archive_raw_sha256=x['archive_raw_sha256']);return
 assert r in tree,'MISSING COMMITTED EVIDENCE '+r
 committed=blob(r)
 assert raw==committed or (r not in [M,L,P,A] and raw.replace(b'\r\n',b'\n')==committed.replace(b'\r\n',b'\n')),'BLOB MISMATCH '+r
 matched[r]=dict(**info(p),binding='git-blob',git_blob_raw_sha256=sha(committed),exact_RAW_equal=raw==committed)
def check(x):
 p=path(x['path']);h=x.get('raw_sha256',x.get('sha256'))
 if 'start_line' in x and 'end_line' in x:
  b=p.read_bytes();region=b''.join(b.splitlines(keepends=True)[x['start_line']-1:x['end_line']]);assert sha(region)==h,'REGION HASH '+str(p)
  if 'header_raw_sha256' in x:assert sha(b)==x['header_raw_sha256']
  exact(p);return
 if not p.exists() or sha(p.read_bytes())!=h:
  ss=snapshot_by_hash.get(h,[])
  if ss:
   rb=blob(ss[0])
   if 'bytes' in x:assert len(rb)==x['bytes']
   historical.append(dict(original_reference=x,resolved_committed_snapshot=ss[0],git_blob_raw_sha256=sha(rb)));return
  aa=archive_by_hash.get(h,[]);assert aa,'UNRESOLVED HISTORICAL RAW '+str(p)+' '+str(h)
  rb=gzip.decompress(blob(rel(aa[0]['archive'])))
  if 'bytes' in x:assert len(rb)==x['bytes']
  historical.append(dict(original_reference=x,resolved_committed_archive=aa[0]));return
 if 'bytes' in x:assert p.stat().st_size==x['bytes'],str(p)
 exact(p)
def records(v):
 if isinstance(v,dict):
  if 'path' in v and ('raw_sha256' in v or 'sha256' in v) and isinstance(v['path'],str):check(v)
  for q in v.values():records(q)
 elif isinstance(v,list):
  for q in v:records(q)
def manifest(p):
 exact(p);v=load(p);records(v);return v
core=[M,L,P,A,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl','research-wiki/frontier-cells/'+CELL+'.json']
for p in core+[B/n for n in archive_maps+['public-source-exclusions93.json','root.statement-seal93.json','claim.json','proved-local93.scoped.json','root.math93.scoped-adoption.json','root.source93.scoped-adoption.json','root.decoder93.adoption.json','anti-anchored.review93.v3.json']]:exact(p)
assert info(M)['raw_sha256']=='5467078f497e0d40e1916550b2e5e9a5be992a69b20fc143bda06dd988d86d9d'
assert info('lean-toolchain')['raw_sha256']=='b2b5068d5a4835675e651ce83b29c0ddb308d28b80076e7c007aef4630af0477'
assert info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert git('-C',str(R/'.lake/packages/mathlib'),'rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
seal=manifest(B/'root.statement-seal93.json')
statement=path(M).read_text(encoding='utf8').split('private def actual_finite_count_path_statement',1)[1].split('/-- Exact sealed',1)[0].rstrip()
assert statement==seal['expanded_literal_Prop'].rstrip()
for n in ['independent-whole-math93/closed-RAW93.native.json','independent-whole-math93/scoped-classical93/closed-RAW-scoped-classical93.native.json','independent-whole-math93/metadata-transfer93/closed-RAW-metadata-transfer93.native.json','primary-source93/closed-RAW-review93.native.json','primary-source93/scoped-transfer93/closed-RAW-transfer93.native.json']:
 manifest(B/n)
for n in ['root.math93.scoped-adoption.json','root.source93.scoped-adoption.json','proved-local93.scoped.json']:manifest(B/n)
math=load(B/'independent-whole-math93/scoped-classical93/scoped-classical-transfer93.native.json')
assert math['decision']=='ACCEPT_SCOPED_CLASSICAL_WHOLE_MATHEMATICS_TRANSFER' and not math['necessary_fixes']
assert math['new_module']['raw_sha256']==info(M)['raw_sha256'] and all(x['exit_code']==0 for x in math['kernel_checks'])
S=B/'primary-source93/scoped-transfer93';native=load(S/'source-review-decision93.native.json');audit=load(A);run=load(S/'review-run93.native.json')
assert native['independent_from_formalizer'] and native['independent_from_decoder'] and native['source_first'] and native['reviewer']=='/root/primary_source93'
assert native['source_review_status']=='accepted' and native['verdict']=='equivalent-after-elaboration' and not native['repairs'] and not native['blocking_findings']
assert len(native['binder_audit'])==6 and native['literal_definition_audit']['let_count']==36
assert audit['state']=='accepted' and audit['semantic_slots']==native['semantic_slots'] and len(audit['semantic_slots'])==7
RUN='76af76828a6a9739c12822a07ce1654b1cc64b0e9b75f2d03fecaeebba7bf63f';BIND='e858e4fa2c7253010f1362aabe932a559ff2a3b9d5b24b420be438eb680cb174';PACK='a8b2a1a59e27dc65d63201d99089a980f99f62f6d3aeb747e3b5a411e44d8533'
assert audit['source_review']['review_run_sha256']==native['review_run_sha256']==run['review_run_sha256']==RUN
assert sha(canon({k:v for k,v in run.items() if k!='review_run_sha256'}))==RUN
assert sha(canon({k:v for k,v in native.items() if k not in ['review_run_sha256','review_run_artifact']}))==run['decision_payload_sha256']
assert audit['publication_binding_sha256']==native['publication_binding_sha256']==BIND
assert audit['source_review']['reviewer_packet_sha256']==native['reviewer_packet_sha256']==PACK
packet=load(B/'anti-anchored.review93.v3.json');assert packet.pop('packet_sha256')==sha(canon(packet))==PACK
for p,key in [(M,'module_raw_sha256'),(L,'lesson_raw_sha256'),(P,'publication_raw_sha256'),(primary,'primary_raw_sha256')]:assert info(p)['raw_sha256']==native[key];exact(p)
cov=load(S/'compiled-source-coverage-exposition93.native.json');assert cov['all_regions_exact'] and (cov['node_count'],cov['edge_count'],cov['disposition_count'])==(35,94,55) and len(cov['exposition_regions'])==9
lesson=load(L)['units'][0];assert all(x['lean'].strip() in path(M).read_text(encoding='utf8') for x in lesson['steps'])
dec=R/'runs/semantic-roundtrip/anonymous93/v2/decoder';dm=manifest(dec/'raw-manifest.json');dr=load(dec/'decoder-report.json');da=load(B/'root.decoder93.adoption.json');inp=dec.parent/'input.json';dp=load(inp)
for p in [inp,dec/'decoder-report.json',dec/'reconstructed-theorem.txt']:exact(p)
assert info(dec/'raw-manifest.json')['raw_sha256']==da['native_manifest_raw_sha256']==audit['reconstruction']['native_run_manifest_RAW_sha256']
assert dp.pop('packet_sha256')==sha(canon(dp))==da['canonical_packet_sha256']==dm['packet_sha256']==audit['reconstruction']['decoder_packet_sha256']
assert sha(canon({k:v for k,v in dr.items() if k!='decoder_run_sha256'}))==dr['decoder_run_sha256']==da['decoder_run_sha256']==audit['reconstruction']['decoder_run_sha256']
assert not dm['source_text_visible'] and not dr['source_text_visible'] and not audit['reconstruction']['source_text_visible']
assert dr['decoder']=='/root/blind_decoder93' and not dr['access_boundary']['source_files_read'] and not dr['access_boundary']['implementation_files_read'] and not dr['access_boundary']['previous_reviews_read']
assert len(dr['access_boundary']['files_read_this_revision'])==1 and rel(dr['access_boundary']['files_read_this_revision'][0])==rel(inp)
assert sha(dp['lean']['statement'].encode())==native['lean_statement_sha256']==audit['reconstruction']['lean_statement_sha256']
assert dr['exact_lean_statement']==dp['lean']['statement']
assert audit['reconstruction']['text']==dr['reconstructed_theorem_text']==(dec/'reconstructed-theorem.txt').read_text(encoding='utf8')
assert sha(dr['reconstructed_theorem_text'].encode())==dm['reconstructed_text_sha256']==native['reconstruction_sha256']
assert dr['semantic_slots']==audit['reconstruction']['native_semantic_slots']
save('decoder-binding93.json',dict(status='PASS',native_manifest=info(dec/'raw-manifest.json'),native_result=info(dec/'decoder-report.json'),canonical_packet_sha256=da['canonical_packet_sha256'],decoder_run_sha256=dr['decoder_run_sha256'],canonical_reconstruction_matches_native=True,hash_recipes_checked=True,disclosure_isolation_checked=True))
save('source-binding93.json',dict(status='PASS',native_decision=info(S/'source-review-decision93.native.json'),native_run=info(S/'review-run93.native.json'),native_manifest=info(S/'closed-RAW-transfer93.native.json'),review_run_canonical_sha256=RUN,publication_binding_sha256=BIND,canonical_reviewer_packet_sha256=PACK,seven_slots_identical=True,coverage=dict(nodes=35,edges=94,dispositions=55,exposition_regions=9)))
for n in ['astis.py','astis_advance.py','astis_publication.py','astis_contributor_contract.py','astis_frontier_cells.py','astis_semantic_roundtrip.py']:exact(R/'tools'/n)
for x in baseline:assert info(x['path'])['raw_sha256']==x['raw_sha256']
save('archive-audit93.json',dict(status='PASS',verified_commit=C,count=len(archive_audit),archives=archive_audit,historical_reference_resolutions=historical,resolver='Committed git blob object IDs; exact committed gzip is preferred for preserved native evidence even when normalized public text also exists. Runtime/collaborator/source exceptions are explicit.'))
save('input-freeze93.json',dict(status='PASS',verified_commit=C,base=BASE,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),all21collaborator_RAWs=baseline,publication_binding_sha256=BIND,canonical_reviewer_packet_sha256=PACK,source_review_run_sha256=RUN,archive_count=len(archive_audit),historical_reference_resolutions=historical))
print('EXACT SCIENCE93 INPUTS PASS',len(matched),len(local),len(historical),flush=True)
