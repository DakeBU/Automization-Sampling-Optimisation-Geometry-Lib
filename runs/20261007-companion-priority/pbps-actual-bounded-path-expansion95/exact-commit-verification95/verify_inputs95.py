import pathlib,json,hashlib,gzip,subprocess,re,copy
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;B=O.parent
C='5df604f6c9ddab63e552272b2e9056752616621e';BASE='2ebf4ad2e323ad26f62fcf0c9859e66579549536'
PRE=R/'runs/20261007-companion-priority/pbps-bounded-path-expansion-preread95'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedPathExpansion.lean';L='website/content/declaration_lessons/pbps-actual-bounded-path-expansion.json';P='website/content/publications/pbps-actual-bounded-path-expansion.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualBoundedPathExpansion.json';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-path-expansion.json'
def rel(p):
 s=str(p).replace('\\','/');return s[len('E:/Samplinglib/'):] if s.startswith('E:/Samplinglib/') else s
def path(p):return R/rel(p)
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(b):return b.replace(b'\r\n',b'\n')
def info(p):
 b=path(p).read_bytes();return {'path':rel(p),'raw_sha256':sha(b),'bytes':len(b)}
def load(p):return json.loads(path(p).read_bytes())
def save(p,x):(O/p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def canon(x):return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
assert git('rev-parse','HEAD').decode().strip()==C
assert git('merge-base',BASE,C).decode().strip()==BASE
tree={x.split('\t',1)[1]:x.split()[2] for x in git('ls-tree','-r',C).decode().splitlines()};cache={}
def blob(p):
 p=rel(p)
 if p not in cache:cache[p]=git('cat-file','blob',tree[p])
 return cache[p]
stage=load(B/'science-staging95.json');extra=load(B/'preproof-type-evidence-archives95.json')
assert blob(B/'science-staging95.json')==(B/'science-staging95.json').read_bytes()
assert blob(B/'preproof-type-evidence-archives95.json')==(B/'preproof-type-evidence-archives95.json').read_bytes()
prior=load('runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/exact-commit-verification94/closed-RAW-manifest94.json')
collab=prior['preserved_collaborator_inputs'];assert len(collab)==21 and collab==stage['preserved_collaborator_inputs']
for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256']
archives={rel(x['raw_path']):x for x in stage['raw_archives']+extra['raw_archives']};byhash={};archive_audit=[];snapshots={}
for p in stage['files']:
 assert p in tree,p
 if not p.endswith('.gz'):snapshots.setdefault(sha(blob(p)),[]).append(p)
for p,x in archives.items():
 ab=blob(x['archive']);rb=gzip.decompress(ab)
 assert sha(ab)==x['archive_sha256'] and sha(rb)==x['raw_sha256'] and rb==path(p).read_bytes(),p
 if x.get('public_text_sha256'):assert sha(blob(p))==x['public_text_sha256'],p
 byhash.setdefault(sha(rb),[]).append(x);archive_audit.append(x)
matched={};local={};historical=[];unresolved=[]
global_scanned=False
def search_history():
 global global_scanned
 if global_scanned:return
 global_scanned=True
 candidates=[p for p in tree if p.endswith(('.gz','.RAW','.snapshot')) or '.exactraw.' in p]
 batch=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for p in candidates:
  batch.stdin.write((tree[p]+'\n').encode());batch.stdin.flush()
  metadata=batch.stdout.readline().split();size=int(metadata[2]);bb=batch.stdout.read(size);assert batch.stdout.read(1)==b'\n';cache[p]=bb
  if p.endswith('.gz'):
   rb=gzip.decompress(bb)
   byhash.setdefault(sha(rb),[]).append({'archive':p,'raw_sha256':sha(rb),'archive_sha256':sha(bb)})
  elif p.endswith(('.RAW','.snapshot')) or '.exactraw.' in p:
   snapshots.setdefault(sha(bb),[]).append(p)
 batch.stdin.close();assert batch.wait()==0
collabpaths={x['path'] for x in collab}
def exact(p):
 p=rel(p);b=path(p).read_bytes()
 if p in matched or p in local:return
 if p in collabpaths or p.startswith(('.astis/','.lake/')) or 'primary-pbps.exactraw.snapshot.html' in p:
  local[p]={**info(p),'reason':'Exact local primary excluded from republication, fixed runtime/library or preserved collaborator bytes.'};return
 if p in archives:
  assert gzip.decompress(blob(archives[p]['archive']))==b
  matched[p]={**info(p),'binding':'lossless committed gzip','archive':archives[p]['archive']};return
 assert p in tree,'UNCOMMITTED '+p
 if blob(p)!=b:
  search_history()
  if sha(b) in byhash:
   a=byhash[sha(b)][0];matched[p]={**info(p),'binding':'exact historical committed gzip','archive':a['archive']};return
  if sha(b) in snapshots:
   matched[p]={**info(p),'binding':'exact historical committed plain snapshot','snapshot':snapshots[sha(b)][0]};return
  assert (p in ['lean-toolchain','lake-manifest.json'] or p.startswith('tools/')) and norm(blob(p))==norm(b),'RAW BLOB MISMATCH '+p
  matched[p]={**info(p),'binding':'newline-equivalent tool/config','git_blob_sha256':sha(blob(p))};return
 matched[p]={**info(p),'binding':'exact Git blob','git_blob':tree[p]}
def record(x):
 h=x.get('raw_sha256',x.get('sha256'));p=x.get('path')
 if not isinstance(p,str) or not isinstance(h,str) or len(h)!=64:return
 if path(p).exists() and sha(path(p).read_bytes())==h:
  if 'bytes' in x:assert path(p).stat().st_size==x['bytes'],p
  exact(p);return
 search_history()
 if h in byhash:
  a=byhash[h][0];bb=gzip.decompress(blob(a['archive']));historical.append({'reference':x,'archive':a['archive']})
 elif h in snapshots:
  a=snapshots[h][0];bb=blob(a);historical.append({'reference':x,'plain_snapshot':a})
 else:
  unresolved.append(x);return
 if 'bytes' in x:assert len(bb)==x['bytes'],p
def records(x):
 if isinstance(x,dict):
  record(x)
  for v in x.values():records(v)
 elif isinstance(x,list):
  for v in x:records(v)
def manifest(p):exact(p);v=load(p);records(v);return v
for p in [M,L,P,A,CELL,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl']:exact(p)
assert info(M)['raw_sha256']=='c3d4bcf73990d704244225ea647f44ed21fcbd339db49bf2c45f21af5b90d689'
assert info('lake-manifest.json')['raw_sha256']=='b1f16b43aaf4a886cfe0382d5e3ae63d6904281c00afd8f35af20f0270a747e2'
assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
seal=manifest(PRE/'root.statement-seal95.json')
for p in [PRE/'independent-header-math95/closed-RAW-manifest.native.json',B/'independent-whole-math95/closed-RAW-whole95.native.json',B/'primary-source95/closed-raw-manifest95.native.json']:
 manifest(p)
for p in stage['files']:
 if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)
S=B/'primary-source95';native=load(S/'source-review-decision95.native.json');run=load(S/'source-review-run95.native.json');audit=load(A)
assert native['reviewer']=='/root/primary_source93' and native['independent_from_formalizer'] and native['independent_from_decoder']
assert native['source_review']['state']==audit['state']=='accepted' and native['verdict']=='equivalent-after-elaboration' and not native['repairs'] and native['blocking_deltas']==0
assert native['semantic_slots']==audit['semantic_slots']
assert native['publication_binding_sha256']==audit['publication_binding_sha256']=='57c98f3a075d7bdd2e10fbfdd353bc969d51b5eba9d9b973fe529607cb51f5b2'
assert sha(canon(run))==native['review_run_sha256']==audit['source_review']['review_run_sha256']
packet=load(S/'reviewer-packet95.exactraw.json');ph=packet.pop('packet_sha256');assert sha(canon(packet))==ph==native['reviewer_packet_sha256']==audit['source_review']['reviewer_packet_sha256']
for key,p in [('module',M),('lesson',L)]:assert info(p)['raw_sha256']==native[key+'_raw_sha256']
old='fc5e5a42a3a6216544b3b1e043e54ca58cab07e0'
def normalize_refs(v):
 if isinstance(v,dict):return {k:normalize_refs(x) for k,x in v.items()}
 if isinstance(v,list):return [normalize_refs(x) for x in v]
 if isinstance(v,str) and v.replace('\\','/').startswith('E:/Samplinglib/'):return rel(v)
 return v
metadata=[]
for p in [P,A,CELL]:
 before=git('show',old+':'+p);want=normalize_refs(json.loads(before))
 if p==P:want['items'][0]['source_proof_coverage']['coverage_report']=rel(S/'compiled-source-coverage95.native.json')
 if p==CELL:want['source_proof_coverage']['coverage_report']=rel(S/'compiled-source-coverage95.native.json')
 if p==CELL:want['conceptual_mirror_audit']=load(B/'proved-local-evidence95.json')['conceptual_mirror_audit']
 if p==CELL:
  for obj,key in [('shared_floor_audit','searched'),('reuse_plan','searched_existing')]:
   want[obj][key]=['Samplinglib local declarations search: '+x if x.endswith('/local.stdout.log') else x for x in want[obj][key]]
 assert want==load(p),'unexpected metadata delta '+p
 metadata.append({'path':p,'before_raw_sha256':sha(before),'after_raw_sha256':info(p)['raw_sha256']})
assert sha(git('show',old+':'+P))==native['publication_raw_sha256']
assert set(git('diff','--name-only',old,C).decode().splitlines())=={P,A,CELL,*[rel(B/x) for x in ['evidence-recovery95.json','recover_evidence95.py','pre-step4-lesson95.recovered.exactraw.json.gz','normalize_public_refs95.py','public-reference-correction95.json','search-label-correction95.json','draft-audit-recovery95.json','draft-audit95.recovered.exactraw.json.gz']]}
draft=load(B/'draft-audit-recovery95.json');db=blob(draft['archive']);draw=gzip.decompress(db)
assert sha(db)==draft['archive_raw_sha256'] and sha(draw)==draft['decoded_raw_sha256']=='c86dea344eab25a79936130ad11b5ae4da2674baf52af57b2f710436bbe08dc4' and len(draw)==80024
recovery=load(B/'evidence-recovery95.json');ab=blob(recovery['archive']);rb=gzip.decompress(ab)
assert sha(ab)==recovery['archive_raw_sha256'] and sha(rb)==recovery['decoded_raw_sha256']=='32ad86e58ad06e382221f07ae8d0dbc5c135ac5c54455e4e48350c3acf002c1c'
oldlesson=json.loads(rb);currentlesson=load(L);oldlesson['units'][0]['steps'][3]['text']=currentlesson['units'][0]['steps'][3]['text'];assert oldlesson==currentlesson
save('historical-lesson-recovery95.json',{'status':'PASS','archive':recovery['archive'],'raw_sha256':sha(rb),'transparent_new_archive_of_hash_pinned_historical_bytes':True,'only_difference_from_current_lesson':'step4.text'})
save('metadata-transfer95.json',{'status':'PASS','prior_science_commit':old,'current_commit':C,'only_changes':'Repository-relative canonical/public evidence references, final compiled coverage pointer, verbatim existing none-found audit, labels on existing Samplinglib search evidence, and exact-hash recovered historical lesson archive with transparent receipt/scripts. No production, lesson, source-native or decoder change.','records':metadata,'native_evidence_unchanged':True})
dec=R/'runs/semantic-roundtrip/anonymous95/decoder';dm=manifest(dec/'raw-manifest.json');dr=load(dec/'decoder-report.json');dp=load(dec.parent/'input.json')
for p in [dec/'decoder-report.json',dec/'reconstructed-theorem.txt',dec.parent/'input.json']:exact(p)
assert dp.pop('packet_sha256')==sha(canon(dp))==dm['packet_sha256']==audit['reconstruction']['decoder_packet_sha256']
assert sha(canon({k:v for k,v in dr.items() if k!='decoder_run_sha256'}))==dr['decoder_run_sha256']==dm['decoder_run_sha256']==audit['reconstruction']['decoder_run_sha256']
assert not dm['source_text_visible'] and not dr['source_text_visible'] and not audit['reconstruction']['source_text_visible']
assert dr['decoder']=='/root/blind_decoder93' and dr['exact_lean_statement']==dp['lean']['statement']
assert sha(dp['lean']['statement'].encode())==audit['reconstruction']['lean_statement_sha256']
assert audit['reconstruction']['text']==dr['reconstructed_theorem_text']==(dec/'reconstructed-theorem.txt').read_text(encoding='utf8')
assert sha(dr['reconstructed_theorem_text'].encode())==dm['reconstructed_text_sha256']
assert dr['semantic_slots']==audit['reconstruction']['native_semantic_slots']
absolute=[]
def refs(v,field,p):
 if isinstance(v,dict):
  for k,x in v.items():refs(x,field+'.'+k,p)
 elif isinstance(v,list):
  for i,x in enumerate(v):refs(x,field+'['+str(i)+']',p)
 elif isinstance(v,str) and re.search(r'[A-Za-z]:[/\\]',v):absolute.append({'file':p,'field':field,'value':v})
for p in [L,P,A,CELL,rel(B/'claim.json'),rel(PRE/'root.statement-seal95.json')]:refs(load(p),'',p)
save('absolute-path-audit95.json',absolute)
save('source-decoder-bindings95.json',{'status':'PASS','source_run_canonical_sha256':native['review_run_sha256'],'packet_sha256':ph,'publication_binding_sha256':native['publication_binding_sha256'],'decoder_run_sha256':dr['decoder_run_sha256'],'decoder_access_boundary':dr['access_boundary'],'source_hash_recipe':run['hash_recipe'],'native_semantic_slots_match':True})
save('archive-audit95.json',{'status':'PASS','count':len(archive_audit),'archives':archive_audit,'historical_reference_resolutions':historical})
save('input-freeze95.json',{'status':'FAIL' if unresolved else 'PASS','unresolved':unresolved,'verified_commit':C,'baseline':BASE,'exact_commit_matches':list(matched.values()),'local_pinned_or_excluded_inputs':list(local.values()),'preserved_collaborator_inputs':collab,'historical_reference_resolutions':historical})
print(json.dumps({'matched':len(matched),'local':len(local),'historical':len(historical),'archives':len(archive_audit),'absolute_fields':len(absolute)},indent=2))
assert not unresolved,unresolved
