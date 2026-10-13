from pathlib import Path
import hashlib,json,gzip,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-prescribed-gibbs-survival-preread98'
C='9525bc0ea88a96e64ef20a53d2a92b9c8a5b966e';BASE='49fdfd309151b30f6371767dd74d698d440a8974'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedGibbsSurvival.lean';L='website/content/declaration_lessons/pbps-actual-prescribed-gibbs-survival.json';P='website/content/publications/pbps-actual-prescribed-gibbs-survival.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPrescribedGibbsSurvival.json';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-prescribed-gibbs-survival.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedGibbsSurvival.actual_prescribed_gibbs_survival_balance'
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
 stage=load(B/'science-staging98.json');assert blob(B/'science-staging98.json')==(B/'science-staging98.json').read_bytes()
 assert not any('next-primary99' in p for p in stage['files'])
 changed=git('diff','--name-only',BASE,C).decode().splitlines();assert set(changed)<=set(stage['files'])|{rel(B/'science-staging98.json')}
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
 assert info(M)['raw_sha256']=='f4856a5f059ef9875e481830cbd1a6152d7bc7de690ed325a71390a791098b95'
 assert info(L)['raw_sha256']=='e47ec0e759137b08c5e81b9996fb72ea0489a18ed30bc4e970267883681f1579'
 assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
 seal=manifest(PRE/'root.statement-seal98.json');assert seal['header']['raw_sha256']=='50c6999fe069f4cf648832a804b71bb8e447b7a3aea0f0c42a836f81650c6ad0'
 for p in stage['files']:
  if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)
 whole=manifest(B/'independent-whole-math98/whole-math-decision98.native.json');assert whole['decision']=='ACCEPT_EXACT_WHOLE_MATHEMATICAL_ASSEMBLY' and whole['production']['raw_sha256']==info(M)['raw_sha256']
 for x in whole['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],('changed fresh-kernel input',x['path'])
 assert whole['public_private_Prop_expansion_kernel_checked']
 # Kernel evidence is reused by exact production/header/input hashes, not by a stale module cache.
 wr=load(B/'independent-whole-math98/fresh-kernel-receipt98.native.json');assert wr['exit_code']==0 and wr['production_raw_sha256']==info(M)['raw_sha256']
 dec=R/'runs/semantic-roundtrip/anonymous98/decoder';dm=manifest(dec/'manifest.json');dr=manifest(dec/'decision.json');run=manifest(dec/'decoder-run.json');dp=manifest(dec.parent/'input.json');audit=load(A)
 for name,x in dm['files'].items():
  q=dec/name;assert info(q)['raw_sha256']==x['sha256'] and info(q)['bytes']==x['bytes'];exact(q)
 assert info(dec.parent/'input.json')['raw_sha256']==dm['input']['sha256']==dr['input_sha256']==run['input_sha256']
 packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==dm['packet_sha256']==dr['packet_sha256']==audit['reconstruction']['decoder_packet_sha256']
 assert info(dec/'decoder-run.json')['raw_sha256']==dr['decoder_run_sha256']==audit['reconstruction']['decoder_run_sha256']
 assert not dm['source_text_visible'] and not run['source_text_visible'] and not run['source_identity_visible'] and not run['proof_visible'] and not run['other_packet_visible'] and not audit['reconstruction']['source_text_visible']
 assert sha(dp['lean']['statement'].encode())==audit['reconstruction']['lean_statement_sha256']
 assert audit['reconstruction']['text']==dr['reconstructed_theorem_text']==(dec/'reconstruction.md').read_text(encoding='utf8')
 assert sha(dr['reconstructed_theorem_text'].encode())==dr['reconstructed_text_sha256']==run['reconstructed_text_sha256']
 assert audit['reconstruction']['native_semantic_slots']=={k:dr[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']}
 S=B/'independent-final-source98';v=manifest(S/'source-review98.native.json');sr=manifest(S/'source-review-run98.native.json');sm=manifest(S/'closed-raw-manifest98.native.json')
 assert info(S/'source-review98.native.json')['raw_sha256']=='213086c5d3278ae3f29381ea39fd076d7564593cf0f1d0e36e3612a593225e83'
 assert info(S/'closed-raw-manifest98.native.json')['raw_sha256']=='8c40eacae5474884cf0935b5660df2ef5e7e5209649c947104fafa932de4b6da'
 assert info(S/'source-review-run98.native.json')['raw_sha256']==v['review_run_sha256']==v['source_review']['review_run_sha256']
 assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
 for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
 srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=audit['source_review']['evidence'];assert rel(srev['evidence'])==rel(S/'source-review98.native.json');assert audit['source_review']==srev
 assert len(v['semantic_slots'])==7 and not any(x['blocking'] for x in v['deltas']) and not v['repairs']
 assert v['independent_from_formalizer'] and v['independent_from_decoder'] and sr['independent_from_formalizer'] and sr['independent_from_decoder'] and not sr['prior_source_review_verdict_used'] and not sr['prior_topology_verdict_used'] and not sr['fresh_math_verdict_read'] and not sr['blocking_findings']
 rp=manifest(B/'reviewer-packet98.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
 assert info(B/'reviewer-packet98.json')['raw_sha256']==v['reviewer_packet_raw_sha256']==sr['reviewer_packet_raw_sha256']
 cov=manifest(S/'compiled-source-coverage98.native.json');primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
 assert len(cov['regions'])==20 and cov['all20regions_disposed'] and len(cov['original19_ids_preserved'])==19 and cov['all28graph_nodes_disposed']
 for x in cov['regions']:
  bb=primary[x['byte_start']:x['byte_end_exclusive']];assert sha(bb)==x['raw_sha256'];assert x['compiled_disposition']
 expo=manifest(S/'exposition-review98.native.json');assert expo['status']=='accepted' and not expo['blocking_findings'] and len(expo['six_steps'])==6 and expo['lesson_raw_sha256']==info(L)['raw_sha256']
 code=(R/M).read_bytes().splitlines(keepends=True)
 for step in expo['six_steps']:
  x=step['source_region'];bb=b''.join(code[x['start_line']-1:x['end_line']]);assert sha(bb)==x['exact_code_raw_sha256'];assert step['decision']=='accepted' and step['exact_code_verified']
 current=load(P);assert info(P)['raw_sha256']==expo['publication_raw_sha256']==next(x for x in sm['inputs'] if rel(x['path'])==P)['raw_sha256']
 sys.path[:0]=[str(R),str(R/'tools')]
 from tools import astis_publication as pub
 item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='da82cc7c233d0512f6a4b53b09257199f0135fa1a65ad3652fb8f0d4439d11b8'
 pub.check_advance([D],reviewed=True)
 topo=manifest(PRE/'independent-header-math98/topology98/source-topology-decision98.native.json');assert info(PRE/'source-proof-graph98.v3.native.json')['raw_sha256']=='c04c64a8fab1768f95542626f7f0e8f31db3874acd02fbcbe9776624e801b71a'
 save('science-scope98.json',dict(status='PASS',verified_commit=C,baseline=BASE,changed_files=changed,scoped_git_blobs=scope,excluded_next_primary99=True))
 save('archive-audit98.json',dict(status='PASS',verified_commit=C,archives=archive_rows,historical_reference_resolutions=history_rows))
 save('source-acceptance98.native.json',dict(status='PASS_NATIVE_SOURCE_AND_TRANSFER',verified_commit=C,native_verdict=info(S/'source-review98.native.json'),native_run=info(S/'source-review-run98.native.json'),closed_manifest=info(S/'closed-raw-manifest98.native.json'),review_run_hash_recipe='Exact RAW SHA256',reviewer_packet_sha256=ph,decoder_packet_sha256=packet_hash,decoder_run_sha256=dr['decoder_run_sha256'],publication_binding_sha256=bd,canonical_copy_exact_except_evidence_path=True,all20source_regions_raw_verified=True,all19original_source_dispositions_retained=True,all28graph_nodes_disposed=True,six_exposition_regions_accepted=True,lesson=info(L),topology_independent_acceptance=info(PRE/'independent-header-math98/topology98/source-topology-decision98.native.json'),canonical_coverage_metadata_pending_repair=True))
 save('input-freeze98.json',dict(status='FAIL' if unresolved else 'PASS',verified_commit=C,unresolved=unresolved,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,historical_reference_resolutions=history_rows,kernel_transfer=info(B/'independent-whole-math98/fresh-kernel-receipt98.native.json')))
 assert not unresolved,unresolved
 assert head()==C
 print(json.dumps(dict(status='PASS_INPUTS_NATIVE_SOURCE',scoped_git_blobs=len(scope),exact_RAW_matches=len(matched),local_pinned=len(local),archives=len(archive_rows),historical_resolutions=len(history_rows))))
