from pathlib import Path
import hashlib,json,gzip,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-endpoint-time-reversal-preread97'
C='b0dafee85d50bc6f37ff9ea8880ff9f1d8dfd6bc';BASE='abc10f7ed0939cd1fa44848a704cacb0b802c989'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualEndpointTimeReversal.lean';L='website/content/declaration_lessons/pbps-actual-endpoint-time-reversal.json';P='website/content/publications/pbps-actual-endpoint-time-reversal.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualEndpointTimeReversal.json';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-endpoint-time-reversal.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws'
sha=lambda b:hashlib.sha256(b).hexdigest();canon=lambda v:json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def rel(p):return str(p).replace('\\','/').removeprefix('E:/Samplinglib/')
def load(p):return json.loads((R/rel(p)).read_bytes())
def info(p):
 p=R/rel(p);b=p.read_bytes();return dict(path=rel(p),raw_sha256=sha(b),bytes=len(b))
def save(n,v):
 p=O/n;assert not p.exists(),str(p);p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
def git(*a):return subprocess.check_output(['git',*a],cwd=R,stderr=subprocess.PIPE)
def head():return git('rev-parse','HEAD').decode().strip()
if __name__=='__main__':
 assert head()==C and git('rev-parse',C+'^').decode().strip()==BASE
 tree={line.split('\t',1)[1]:line.split()[2] for line in git('ls-tree','-r',C).decode().splitlines()};cache={}
 def blob(p):
  p=rel(p)
  if p not in cache:cache[p]=git('cat-file','blob',tree[p])
  return cache[p]
 stage=load(B/'science-staging97.json');assert blob(B/'science-staging97.json')==(B/'science-staging97.json').read_bytes()
 assert not any('next-primary98' in p for p in stage['files'])
 changed=git('diff','--name-only',BASE,C).decode().splitlines();assert set(changed)<=set(stage['files'])|{rel(B/'science-staging97.json')}
 collab=load(B.parent/'pbps-actual-phase-reversal-volume96/exact-commit-verification96/closed-RAW-manifest96.json')['preserved_collaborator_inputs']
 assert len(collab)==21 and collab==stage['preserved_collaborator_inputs']
 for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
 byhash={};archive_rows=[];matched={};local={};history_rows=[];unresolved=[];scope=[]
 for x in stage['raw_archives']:
  ab=blob(x['archive']);rb=gzip.decompress(ab);assert sha(ab)==x['archive_sha256'] and sha(rb)==x['raw_sha256'] and rb==(R/x['raw_path']).read_bytes(),x['raw_path']
  if x.get('public_text_sha256'):assert sha(blob(x['raw_path']))==x['public_text_sha256']
  byhash[sha(rb)]=dict(archive=x['archive'],archive_sha256=sha(ab));archive_rows.append(x)
 for p in stage['files']:
  bb=blob(p)
  if p.endswith('.gz'):
   assert bb==(R/p).read_bytes(),p;byhash.setdefault(sha(gzip.decompress(bb)),dict(archive=p,archive_sha256=sha(bb)))
  else:
   rb=(R/p).read_bytes();nb=rb.replace(b'\r\n',b'\n')
   if p.startswith('runs/') and nb:nb=b'\n'.join(x.rstrip(b' \t') for x in nb.split(b'\n')).rstrip(b'\n')+b'\n'
   assert bb==nb,p;byhash.setdefault(sha(bb),dict(snapshot=p))
  scope.append(dict(path=p,git_blob=tree[p],git_raw_sha256=sha(bb)))
 scanned=False
 def history():
  global scanned
  if scanned:return
  scanned=True
  candidates=[p for p in tree if p.endswith(('.gz','.RAW','.snapshot','.exactraw')) or '.exactraw.' in p]
  batch=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
  for p in candidates:
   batch.stdin.write((tree[p]+'\n').encode());batch.stdin.flush();h=batch.stdout.readline().split();bb=batch.stdout.read(int(h[2]));assert batch.stdout.read(1)==b'\n'
   rb=gzip.decompress(bb) if p.endswith('.gz') else bb
   byhash.setdefault(sha(rb),dict(archive=p,archive_sha256=sha(bb)) if p.endswith('.gz') else dict(snapshot=p))
  batch.stdin.close();assert batch.wait()==0
 def exact(p):
  p=rel(p)
  if p in matched or p in local:return
  b=(R/p).read_bytes();h=sha(b)
  if p in {rel(x['path']) for x in collab} or p.startswith(('.lake/','.astis/')) or h=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760':
   local[p]=dict(**info(p),reason='Pinned library/runtime, preserved collaborator or fixed original primary excluded from republication');return
  if p in tree and blob(p)==b:matched[p]=dict(**info(p),binding='exact Git blob',git_blob=tree[p]);return
  if h not in byhash:history()
  if h in byhash:matched[p]=dict(**info(p),binding='exact committed lossless archive/snapshot',**byhash[h]);return
  if (p in ['lean-toolchain','lake-manifest.json'] or p.startswith('tools/')) and p in tree and blob(p).replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'):
   matched[p]=dict(**info(p),binding='fixed tool/config newline equivalence',git_blob_sha256=sha(blob(p)));return
  raise AssertionError('UNPRESERVED RAW '+p)
 def records(v):
  if isinstance(v,dict):
   p=v.get('path');h=v.get('raw_sha256',v.get('sha256'))
   if isinstance(p,str) and '/' in p and isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h):
    p=rel(p)
    if (R/p).is_file() and sha((R/p).read_bytes())==h:exact(p)
    else:
     if h not in byhash:history()
     if h not in byhash:unresolved.append(v)
     else:
      loc=byhash[h];bb=gzip.decompress(blob(loc['archive'])) if 'archive' in loc else blob(loc['snapshot'])
      assert sha(bb)==h
      if 'bytes' in v:assert len(bb)==v['bytes']
      history_rows.append(dict(reference=v,**loc))
   for q in v.values():records(q)
  elif isinstance(v,list):
   for q in v:records(q)
 def manifest(p):exact(p);v=load(p);records(v);return v
 for p in [M,L,P,A,CELL,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl']:exact(p)
 assert info(M)['raw_sha256']=='01816c27c8371ba9f81e24217ef7732b6c541066cb0b0f37e6494ffd8c58d27a'
 assert info(L)['raw_sha256']=='b43f1a348a577ab0e5a1934286e26c76339cb7283cf46054ea38b188a815a092'
 assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
 seal=manifest(PRE/'root.statement-seal97.json');assert seal['proposed_public_theorem']==D
 for p in stage['files']:
  if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)
 whole=manifest(B/'independent-whole-math97/whole-math-decision97.native.json');assert whole['decision']=='ACCEPT_EXACT_WHOLE_MATHEMATICAL_ASSEMBLY' and whole['production']['raw_sha256']==info(M)['raw_sha256']
 for x in whole['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],('changed fresh-kernel input',x['path'])
 assert whole['public_private_Prop_expansion_kernel_checked']
 # Kernel evidence is reused by exact production/header/input hashes, not by a stale module cache.
 wr=load(B/'independent-whole-math97/fresh-kernel-receipt97.native.json');assert wr['exit_code']==0 and wr['production_raw_sha256']==info(M)['raw_sha256']
 dec=R/'runs/semantic-roundtrip/anonymous97/decoder';dm=manifest(dec/'manifest.json');dr=manifest(dec/'decision.json');run=manifest(dec/'decoder-run.json');dp=manifest(dec.parent/'input.json');audit=load(A)
 for x in dm['files']:
  q=dec/x['path'];assert info(q)['raw_sha256']==x['sha256'] and info(q)['bytes']==x['bytes'];exact(q)
 assert info(dec.parent/'input.json')['raw_sha256']==dm['input_sha256']==dr['input_sha256']==run['input_sha256']
 packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==dm['packet_sha256']==dr['packet_sha256']==audit['reconstruction']['decoder_packet_sha256']
 assert info(dec/'decoder-run.json')['raw_sha256']==dr['decoder_run_sha256']==audit['reconstruction']['decoder_run_sha256']
 assert not dm['source_text_visible'] and not run['source_text_visible'] and not run['source_comparison_performed'] and not run['external_reads'] and not audit['reconstruction']['source_text_visible']
 assert sha(dp['lean']['statement'].encode())==run['statement_sha256']==audit['reconstruction']['lean_statement_sha256']
 assert audit['reconstruction']['text']==dr['reconstructed_theorem_text']==(dec/'reconstruction.md').read_text(encoding='utf8')
 assert sha(dr['reconstructed_theorem_text'].encode())==dr['reconstructed_text_sha256']
 assert audit['reconstruction']['native_semantic_slots']=={k:dr[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']}
 S=B/'independent-final-source97';v=manifest(S/'source-review97.native.json');sr=manifest(S/'source-review-run97.native.json');sm=manifest(S/'closed-raw-manifest97.native.json')
 assert info(S/'source-review97.native.json')['raw_sha256']=='ce75d14aa21a2a24d2206e3c37e2f7a1a061389cf8636e0171deb212268c0960'
 assert info(S/'source-review-run97.native.json')['raw_sha256']==v['review_run_sha256']==v['source_review']['review_run_sha256']
 assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
 for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
 srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review97.native.json');assert audit['source_review']==srev
 assert len(v['semantic_slots'])==7 and not any(x['blocking'] for x in v['deltas']) and not v['repairs']
 assert v['independent_from_formalizer'] and v['independent_from_decoder'] and sr['independent_from_formalizer'] and sr['independent_from_decoder'] and not sr['prior_review_verdicts_used'] and not sr['blocking_findings']
 rp=manifest(B/'reviewer-packet97.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
 assert info(B/'reviewer-packet97.json')['raw_sha256']==v['reviewer_packet_raw_sha256']==sr['reviewer_packet_raw_sha256']
 cov=manifest(S/'compiled-source-coverage97.native.json');primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
 assert len(cov['regions'])==15 and cov['all15regions_have_exact_compiled_or_excluded_disposition'] and cov['all19original_ids_retained']
 for x in cov['regions']:
  bb=primary[x['byte_start']:x['byte_end_exclusive']];assert len(bb)==x['bytes'] and sha(bb)==x['raw_sha256']
 expo=manifest(S/'exposition-review97.native.json');assert expo['status']=='accepted' and not expo['blocking_findings'] and len(expo['steps'])==6 and expo['lesson_raw_sha256']==info(L)['raw_sha256']
 oldraw=(B/'publication-before-final-coverage97.json').read_bytes();old=json.loads(oldraw);current=load(P);transfer=manifest(B/'source-admission-transfer97.json')
 assert sha(oldraw)==next(x for x in sm['inputs'] if x['path']==P)['raw_sha256']==sr['publication_raw_sha256']
 assert old['items'][0]['source_proof_coverage']==transfer['coverage_before'];old['items'][0]['source_proof_coverage']=transfer['coverage_after'];assert old==current
 sys.path[:0]=[str(R),str(R/'tools')]
 from tools import astis_publication as pub
 item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);prior=json.loads(oldraw)
 assert bd==pub.binding_digest(prior['items'][0],prior['items'][0]['bindings'][0])==audit['publication_binding_sha256']==v['publication_binding_sha256']==transfer['publication_binding_unchanged']=='639a315ced95fb604aa3e34c721879d2962b6c31638a2f6cfda2dd9859ebd9a1'
 pub.check_advance([D],reviewed=True)
 save('science-scope97.json',dict(status='PASS',verified_commit=C,baseline=BASE,changed_files=changed,scoped_git_blobs=scope,excluded_next_primary98=True))
 save('archive-audit97.json',dict(status='PASS',verified_commit=C,archives=archive_rows,historical_reference_resolutions=history_rows))
 save('source-acceptance97.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review97.native.json'),native_run=info(S/'source-review-run97.native.json'),closed_manifest=info(S/'closed-raw-manifest97.native.json'),review_run_hash_recipe='Exact RAW SHA256',reviewer_packet_sha256=ph,decoder_packet_sha256=packet_hash,decoder_run_sha256=dr['decoder_run_sha256'],publication_binding_sha256=bd,canonical_copy_exact_except_evidence_path=True,coverage_only_publication_transfer=True,all15source_regions_raw_verified=True,all19source_dispositions_retained=True,six_exposition_regions_accepted=True,lesson=info(L),topology_independent_acceptance=info(PRE/'independent-header-math97/topology97/source-topology-decision97.native.json')))
 save('input-freeze97.json',dict(status='FAIL' if unresolved else 'PASS',verified_commit=C,unresolved=unresolved,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,historical_reference_resolutions=history_rows,kernel_transfer=info(B/'independent-whole-math97/fresh-kernel-receipt97.native.json')))
 assert not unresolved,unresolved
 assert head()==C
 print(json.dumps(dict(status='PASS',scoped_git_blobs=len(scope),exact_RAW_matches=len(matched),local_pinned=len(local),archives=len(archive_rows),historical_resolutions=len(history_rows))))
