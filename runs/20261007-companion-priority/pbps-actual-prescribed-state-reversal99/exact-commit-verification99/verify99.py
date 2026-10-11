from pathlib import Path
import hashlib,json,gzip,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-finite-state-reversal-preread99'
C='ce675a4cfad2d35cc8c4fec2c26979728742ac27';SCI='4afd302cc48cdc9671af978172fa9aac69188d28';BASE='1e1acccb9407abd672f929a0e2305d5cbc867a9e'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedStateReversal.lean';L='website/content/declaration_lessons/pbps-actual-prescribed-state-reversal.json';P='website/content/publications/pbps-actual-prescribed-state-reversal.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPrescribedStateReversal.json';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-prescribed-state-reversal.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedStateReversal.actual_prescribed_state_reversal_and_rate_product'
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
 assert head()==C and git('rev-parse',C+'^').decode().strip()==SCI and git('rev-parse',SCI+'^').decode().strip()==BASE
 tree={line.split('\t',1)[1]:line.split()[2] for line in git('ls-tree','-r',C).decode().splitlines()};cache={}
 def blob(p):
  p=rel(p)
  if p not in cache:cache[p]=git('cat-file','blob',tree[p])
  return cache[p]
 recovery=load(B/'raw-recovery99/recovery99.json');recoverypaths=[x['archive'] for x in recovery['files']]+[rel(B/'raw-recovery99/recovery99.json')];assert set(git('diff','--name-only',SCI,C).decode().splitlines())==set(recoverypaths);assert all(row.startswith('A\t') for row in git('diff','--name-status',SCI,C).decode().splitlines())
 stage=load(B/'science-staging99.json');assert blob(B/'science-staging99.json')==(B/'science-staging99.json').read_bytes()
 assert not any('next-primary100' in p for p in stage['files'])
 batch=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
 for path in stage['files']+recoverypaths:
  assert path in tree;batch.stdin.write((tree[path]+'\n').encode());batch.stdin.flush();hh=batch.stdout.readline().split();cache[path]=batch.stdout.read(int(hh[2]));assert batch.stdout.read(1)==b'\n'
 batch.stdin.close();assert batch.wait()==0
 changed=git('diff','--name-only',BASE,C).decode().splitlines();assert set(changed)<=set(stage['files'])|set(recoverypaths)|{rel(B/'science-staging99.json')}
 collab=load(B.parent/'pbps-actual-prescribed-gibbs-survival98/exact-commit-verification98/closed-RAW-manifest98.json')['preserved_collaborator_inputs']
 assert len(collab)==21 and collab==stage['preserved_collaborator_inputs']
 for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
 byhash={};archive_rows=[];matched={};local={};history_rows=[];unresolved=[];scope=[]
 for x in stage['raw_archives']:
  ab=blob(x['archive']);rb=gzip.decompress(ab);assert sha(ab)==x['archive_sha256'] and sha(rb)==x['raw_sha256'] and rb==(R/x['raw_path']).read_bytes(),x['raw_path']
  if x.get('public_text_sha256'):assert sha(blob(x['raw_path']))==x['public_text_sha256']
  byhash[sha(rb)]=dict(archive=x['archive'],archive_sha256=sha(ab));archive_rows.append(x)
 for p in stage['files']+recoverypaths:
  bb=blob(p)
  if p.endswith('.gz'):
   assert bb==(R/p).read_bytes(),p;byhash.setdefault(sha(gzip.decompress(bb)),dict(archive=p,archive_sha256=sha(bb)))
  else:
   rb=(R/p).read_bytes();nb=rb.replace(b'\r\n',b'\n')
   if p.startswith('runs/') and nb:nb=b'\n'.join(x.rstrip(b' \t') for x in nb.split(b'\n')).rstrip(b'\n')+b'\n'
   assert bb==nb,p;byhash.setdefault(sha(bb),dict(snapshot=p))
  scope.append(dict(path=p,git_blob=tree[p],git_raw_sha256=sha(bb)))
 for x in recovery['files']:
  ab=blob(x['archive']);rb=gzip.decompress(ab);assert sha(ab)==x['archive_sha256'] and sha(rb)==x['raw_sha256'] and len(rb)==x['bytes']
  if x['original_path']!=P:assert rb==(R/x['original_path']).read_bytes()
  byhash[sha(rb)]=dict(archive=x['archive'],archive_sha256=sha(ab))
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
  unresolved.append(dict(**info(p),reason='Original RAW not resolved in scoped or historical committed archives'));return
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
 assert info(M)['raw_sha256']=='687ff485725aaf3e03e67f57e16df6632e085d129d4cbd30f8a4ab0ce356a3e5'
 assert info(L)['raw_sha256']=='a99438291d48e4da3cad09ba91ff534162165975460978ff4fea11f73cf585b7'
 assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
 seal=manifest(PRE/'root.statement-seal99.json');assert seal['proposed_public_theorem']==D
 for p in stage['files']:
  if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)
 whole=manifest(B/'independent-whole-math99/whole-math-decision99.native.json');assert whole['decision']=='ACCEPT_EXACT_WHOLE_MATHEMATICAL_ASSEMBLY' and whole['production']['raw_sha256']==info(M)['raw_sha256']
 for x in whole['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],('changed fresh-kernel input',x['path'])
 assert whole['public_private_Prop_expansion_kernel_checked']
 # Kernel evidence is reused by exact production/header/input hashes, not by a stale module cache.
 wr=load(B/'independent-whole-math99/fresh-kernel-receipt99.native.json');assert wr['exit_code']==0 and wr['production_raw_sha256']==info(M)['raw_sha256']
 dec=R/'runs/semantic-roundtrip/anonymous99/decoder';dm=manifest(dec/'manifest.json');dr=manifest(dec/'decision.json');run=manifest(dec/'decoder-run.json');dp=manifest(dec.parent/'input.json');audit=load(A)
 for x in dm['artifacts']:
  q=dec/x['path'];assert info(q)['raw_sha256']==x['sha256'] and info(q)['bytes']==x['bytes'];exact(q)
 assert info(dec.parent/'input.json')['raw_sha256']==dm['input']['sha256']==dr['input_sha256']==run['input_sha256']
 packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==dm['input']['packet_sha256']==dr['packet_sha256']==audit['reconstruction']['decoder_packet_sha256']
 assert info(dec/'decoder-run.json')['raw_sha256']==dr['decoder_run_sha256']==audit['reconstruction']['decoder_run_sha256']
 assert not run['source_text_visible'] and not run['source_identity_visible'] and not run['proof_visible'] and not run['other_packet_visible'] and not audit['reconstruction']['source_text_visible']
 assert sha(dp['lean']['statement'].encode())==audit['reconstruction']['lean_statement_sha256']
 assert audit['reconstruction']['text']==dr['reconstructed_theorem_text']==(dec/'reconstruction.md').read_text(encoding='utf8')
 assert sha(dr['reconstructed_theorem_text'].encode())==dr['reconstructed_text_sha256']==run['reconstructed_text_sha256']
 assert audit['reconstruction']['native_semantic_slots']=={k:dr[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']}
 S=B/'independent-final-source99';v=manifest(S/'source-review99.native.json');sr=manifest(S/'source-review-run99.native.json');sm=manifest(S/'closed-RAW-manifest99.native.json')
 assert info(S/'source-review99.native.json')['raw_sha256']=='ee3ceceb2115ec75d6bd2a49dae459228d96c99e419190cd46a8576ecbb25f19'
 assert info(S/'closed-RAW-manifest99.native.json')['raw_sha256']=='0fed3005548c7922db6a03287b3137913debf11c422409347245394d8eeb2950'
 assert info(S/'source-review-run99.native.json')['raw_sha256']==v['review_run_sha256']==v['source_review']['review_run_sha256']
 assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
 for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
 srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review99.native.json');assert audit['source_review']==srev
 assert len(v['semantic_slots'])==7 and not any(x.get('blocking',False) for x in v['deltas']) and not v['repairs']
 assert v['independent_from_formalizer'] and v['independent_from_decoder'] and sr['anti_anchoring']['primary_first_frozen_before_final_packet'] and not sr['anti_anchoring']['prior_math_acceptance_used'] and not sr['anti_anchoring']['prior_final_fidelity_slots_deltas_repairs_used'] and not sr['anti_anchoring']['prior_header_acceptance_used']
 rp=manifest(B/'reviewer-packet99.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
 assert info(B/'reviewer-packet99.json')['raw_sha256']==v['reviewer_packet_raw_sha256']
 cov=manifest(S/'compiled-source-coverage99.native.json');primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes()
 assert info(S/'compiled-source-coverage99.native.json')['raw_sha256']=='eeb7aadfc0ae48653fcd6b977f07e96b23abff6601c5c37f30eb0314747b5988'
 assert len(cov['regions'])==21 and cov['all21regions_raw_verified'] and len(cov['original19ids'])==19 and len(cov['nodes'])==28 and cov['all28nodes_disposed']
 for x in cov['regions']:
  bb=primary[x['byte_start']:x['byte_end_exclusive']];assert sha(bb)==x['raw_sha256']
 expo=manifest(S/'exposition-and-whole-module99.native.json');assert len(expo['all6exact_regions'])==6 and len(expo['helper_audit'])==3 and expo['all_private_helpers_used'] and not expo['public_provider_premises_added'] and expo['lesson']['raw_sha256']==info(L)['raw_sha256']
 lesson=load(L)['units'][0];code=(R/M).read_text(encoding='utf8').splitlines(keepends=True)
 for step,claim in zip(lesson['steps'],expo['all6exact_regions']):
  start,end=claim['lines'];literal=''.join(code[start-1:end]);assert step['lean']==literal and step['formula']==claim['formula'];assert claim['exact_adjacent_code']
 current=load(P);cell=load(CELL);assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'];assert current['items'][0]['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage99.native.json')
 expectedparents=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualEndpointTimeReversal.actual_endpoint_time_reversal_laws','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhaseReversalVolume.actual_phase_reversal_volume_laws']
 assert sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==whole['actual_direct_producer_declarations']==expectedparents
 assert sorted(expo['exact_distinct_invoked_parents'])==[q.removeprefix('AutoSamplingTheory.ExampleCases.ProximalBPS.') for q in expectedparents]
 sys.path[:0]=[str(R),str(R/'tools')]
 from tools import astis_publication as pub
 item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='53377ac49cfa5dc649bf01a35652c2068fcd5e580b21338d7229c03ea2cc8b7f'
 pub.check_advance([D],reviewed=True)
 topo=manifest(PRE/'independent-header-math99/topology99/source-topology-decision99.native.json');assert topo['decision']=='ACCEPT_SOURCE_TOPOLOGY_AND_COVERAGE' and topo['graph']['raw_sha256']==cov['source_graph']['raw_sha256']
 save('science-scope99.json',dict(status='PASS',verified_commit=C,baseline=BASE,changed_files=changed,scoped_git_blobs=scope))
 save('archive-audit99.json',dict(status='PASS' if not unresolved else 'FAIL_UNRESOLVED_REFERENCES',verified_commit=C,archives=archive_rows,historical_reference_resolutions=history_rows,unresolved=unresolved))
 save('input-freeze99.json',dict(status='FAIL' if unresolved else 'PASS',verified_commit=C,unresolved=unresolved,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,historical_reference_resolutions=history_rows,kernel_transfer=info(B/'independent-whole-math99/fresh-kernel-receipt99.native.json')))
 assert not unresolved,unresolved
 oldhash=expo['publication']['raw_sha256'];assert oldhash in byhash
 loc=byhash[oldhash];oldraw=gzip.decompress(blob(loc['archive'])) if 'archive' in loc else blob(loc['snapshot']);old= json.loads(oldraw)
 assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
 oldcov=old['items'][0]['source_proof_coverage'];old['items'][0]['source_proof_coverage']=current['items'][0]['source_proof_coverage'];assert old==current
 save('metadata-transfer99.json',dict(status='PASS',verified_commit=C,prior_science_commit=SCI,only_three_recovery_files_added=True,archives=recovery['files'],original_README_RAW_preserved=True,reviewed_publication_exact_prior_independent_hash=True,current_science_metadata_and_production_unchanged=True,coverage_only_prior_publication_transfer=True,publication_binding_sha256=bd,negative_trial_preserved=rel(O/'trial4afd302/blocking-RAW-bindings99.native.json')))
 save('source-acceptance99.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review99.native.json'),native_run=info(S/'source-review-run99.native.json'),closed_manifest=info(S/'closed-RAW-manifest99.native.json'),review_run_hash_recipe='Exact RAW SHA256',reviewer_packet_sha256=ph,decoder_packet_sha256=packet_hash,decoder_run_sha256=dr['decoder_run_sha256'],publication_binding_sha256=bd,canonical_copy_exact_except_evidence_path=True,all21source_regions_raw_verified=True,all19original_source_dispositions_retained=True,all28graph_nodes_disposed=True,six_exposition_regions_accepted=True,all_three_private_helpers_source_reviewed=True,exact_two_actual_producer_parents=expectedparents,lesson=info(L),topology_independent_acceptance=info(PRE/'independent-header-math99/topology99/source-topology-decision99.native.json'),canonical_final_coverage_pointer_present=True,reviewed_prior_publication_RAW=oldhash,prior_coverage=oldcov,coverage_only_transfer=True))
 assert head()==C
 print(json.dumps(dict(status='PASS_INPUTS_NATIVE_SOURCE',scoped_git_blobs=len(scope),exact_RAW_matches=len(matched),local_pinned=len(local),archives=len(archive_rows),historical_resolutions=len(history_rows))))
