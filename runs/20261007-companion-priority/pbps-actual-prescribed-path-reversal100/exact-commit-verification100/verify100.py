from pathlib import Path
import hashlib,json,gzip,subprocess,sys,re,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;PRE=B.parent/'pbps-finite-path-reversal-preread100'
C='d9850090b15210e29ecd9b932f02c358d2c9e786';BASE='af9c34eb875fd0261f9c40020d7ee22ecdffebbf'
M='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathReversal.lean';L='website/content/declaration_lessons/pbps-actual-prescribed-path-reversal.json';P='website/content/publications/pbps-actual-prescribed-path-reversal.json';A='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPrescribedPathReversal.json';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-prescribed-path-reversal.json'
D='AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathReversal.actual_prescribed_path_reversal_and_survival'
PRIMARY='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
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
 stage=load(B/'science-staging100.json');assert blob(B/'science-staging100.json')==(B/'science-staging100.json').read_bytes()
 scoped=list(dict.fromkeys(stage['files']+[rel(B/'science-staging100.json')]))
 changed=git('diff','--name-only',BASE,C).decode().splitlines();assert set(changed)<=set(scoped)
 assert len(stage['files'])==195 and len(scoped)==196,(len(scoped),len(stage['files']))
 assert not any('next-primary101' in p or 'exact-commit-verification100' in p for p in scoped)
 collab=load(B.parent/'pbps-actual-prescribed-state-reversal99/exact-commit-verification99/closed-RAW-manifest99.json')['preserved_collaborator_inputs']
 assert len(collab)==21 and collab==stage['preserved_collaborator_inputs']
 for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
 def batch_read(paths):
  batch=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
  for path in paths:
   if path in cache:continue
   batch.stdin.write((tree[path]+'\n').encode());batch.stdin.flush();hh=batch.stdout.readline().split();cache[path]=batch.stdout.read(int(hh[2]));assert batch.stdout.read(1)==b'\n'
  batch.stdin.close();assert batch.wait()==0
 batch_read(scoped)
 byhash={};archive_rows=[];matched={};local={};history_rows=[];unresolved=[];scope=[]
 for x in stage['raw_archives']:
  ab=blob(x['archive']);rb=gzip.decompress(ab);assert sha(ab)==x['archive_sha256'] and sha(rb)==x['raw_sha256'] and rb==(R/x['raw_path']).read_bytes(),x['raw_path']
  assert sha(rb)!=PRIMARY
  if x.get('public_text_sha256'):assert sha(blob(x['raw_path']))==x['public_text_sha256']
  byhash[sha(rb)]=dict(archive=x['archive'],archive_sha256=sha(ab));archive_rows.append(x)
 for p in scoped:
  bb=blob(p)
  if p.endswith('.gz'):
   assert bb==(R/p).read_bytes(),p;rb=gzip.decompress(bb);assert sha(rb)!=PRIMARY;byhash.setdefault(sha(rb),dict(archive=p,archive_sha256=sha(bb)))
  else:
   rb=(R/p).read_bytes();nb=rb.replace(b'\r\n',b'\n')
   if p.startswith('runs/') and nb:nb=b'\n'.join(x.rstrip(b' \t') for x in nb.split(b'\n')).rstrip(b'\n')+b'\n'
   assert bb==nb,p;assert sha(bb)!=PRIMARY;byhash.setdefault(sha(bb),dict(snapshot=p))
  scope.append(dict(path=p,git_blob=tree[p],git_raw_sha256=sha(bb)))
 scanned=False
 def history():
  global scanned
  if scanned:return
  scanned=True
  candidates=[p for p in tree if p.endswith(('.gz','.RAW','.snapshot','.exactraw')) or '.exactraw.' in p]
  batch_read(candidates)
  for p in candidates:
   bb=blob(p);rb=gzip.decompress(bb) if p.endswith('.gz') else bb
   byhash.setdefault(sha(rb),dict(archive=p,archive_sha256=sha(bb)) if p.endswith('.gz') else dict(snapshot=p))
 def exact(p):
  p=rel(p)
  if p in matched or p in local:return
  b=(R/p).read_bytes();h=sha(b)
  if p in {rel(x['path']) for x in collab} or p.startswith(('.lake/','.astis/')) or h==PRIMARY:
   local[p]=dict(**info(p),reason='Pinned library/runtime, preserved collaborator or fixed original primary excluded from republication');return
  if p in tree and blob(p)==b:matched[p]=dict(**info(p),binding='exact Git blob',git_blob=tree[p]);return
  if h not in byhash:history()
  if h in byhash:matched[p]=dict(**info(p),binding='exact committed lossless archive/snapshot',**byhash[h]);return
  if (p in ['lean-toolchain','lake-manifest.json'] or p.startswith('tools/')) and p in tree and blob(p).replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'):
   matched[p]=dict(**info(p),binding='fixed tool/config newline equivalence',git_blob_sha256=sha(blob(p)));return
  unresolved.append(dict(**info(p),reason='Original RAW not resolved in scoped or historical committed archives'))
 def records(v):
  if isinstance(v,dict):
   p=v.get('path');h=v.get('raw_sha256',v.get('sha256'))
   if isinstance(p,str) and '/' in p.replace('\\','/') and isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h):
    p=rel(p)
    if (R/p).is_file() and sha((R/p).read_bytes())==h:exact(p)
    else:
     if h not in byhash:history()
     if h not in byhash:unresolved.append(v)
     else:
      loc=byhash[h];bb=gzip.decompress(blob(loc['archive'])) if 'archive' in loc else blob(loc['snapshot']);assert sha(bb)==h
      if 'bytes' in v:assert len(bb)==v['bytes']
      if 'size_bytes' in v:assert len(bb)==v['size_bytes']
      history_rows.append(dict(reference=v,**loc))
   for q in v.values():records(q)
  elif isinstance(v,list):
   for q in v:records(q)
 def manifest(p):exact(p);v=load(p);records(v);return v
 for p in [M,L,P,A,CELL,'lean-toolchain','lake-manifest.json','runs/substantive_advances.jsonl']:exact(p)
 assert info(M)['raw_sha256']=='59d3131209605d2df34e74abb098f42d41338ae44f7e4f4bee4d75ac7bc0a3c8'
 assert info(L)['raw_sha256']=='dd6966262cfe6fde662bbbc41e9265ea72f5d542d8a7d4b6b61af8637eb2ff2b'
 assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
 seal=manifest(PRE/'root.statement-seal100.json');assert info(PRE/'root.statement-seal100.json')['raw_sha256']=='830f6b01d3d82168085e7e081a123c3152043090ebd7f0b91410e076cb96c108'
 for p in scoped:
  if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)
 whole=manifest(B/'independent-whole-math100/whole-math-decision100.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL_TARGET' and whole['production']['raw_sha256']==info(M)['raw_sha256']
 prep=manifest(B/'independent-whole-math100/prepared-inputs100.native.json')
 for x in prep['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],('changed fresh-kernel input',x['path'])
 wr=manifest(B/'independent-whole-math100/fresh-kernel-receipt100.native.json');assert wr['exit_code']==0 and wr['production_raw_sha256']==info(M)['raw_sha256']
 dec=R/'runs/semantic-roundtrip/anonymous100/decoder-native';dm=manifest(dec/'raw-manifest-v2.json');dr=manifest(dec/'reconstruction.json');run=manifest(dec/'decoder-run.json');dp=manifest(dec.parent/'input.json');audit=load(A)
 for x in dm['entries']:assert info(x['path'])['raw_sha256']==x['raw_sha256'] and info(x['path'])['bytes']==x['size_bytes']
 assert info(dec.parent/'input.json')['raw_sha256']==dr['input_raw_sha256']==run['sole_task_evidence_input']['raw_sha256']
 packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==dm['canonical_packet_sha256']==dr['packet_sha256']==audit['reconstruction']['decoder_packet_sha256']
 canonical={k:v for k,v in dr.items() if k not in ['decoder_run_sha256','decoder_run_hash_method']};assert sha(canon(canonical))==dr['decoder_run_sha256']==run['existing_decoder_run_canonical_sha256']==audit['reconstruction']['native_canonical_payload_hash']
 assert info(dec/'decoder-run.json')['raw_sha256']==audit['reconstruction']['decoder_run_sha256']
 assert not run['source_text_visible'] and not run['source_identity_visible'] and not run['proof_visible'] and not dr['source_text_visible'] and not audit['reconstruction']['source_text_visible']
 assert sha(dp['lean']['statement'].encode())==audit['reconstruction']['lean_statement_sha256']
 assert audit['reconstruction']['text']==dr['reconstructed_theorem_text']==(dec/'reconstructed-theorem.txt').read_text(encoding='utf8')
 assert sha(dr['reconstructed_theorem_text'].encode())==dr['reconstructed_text_sha256']==dm['reconstructed_text_sha256']
 assert audit['reconstruction']['native_semantic_slots']=={k:dr[k] for k in ['objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies']}
 S=B/'final-source100';v=manifest(S/'source-review100.native.json');sr=manifest(S/'source-review-run100.native.json');sm=manifest(S/'closed-RAW-final-source100.native.json')
 assert info(S/'source-review100.native.json')['raw_sha256']=='1b4d23f4e861ed9ac1869620657d8307b130665203300af5a14e0faa216d05b4'
 assert info(S/'source-review-run100.native.json')['raw_sha256']==v['review_run_sha256']==v['source_review']['review_run_sha256']
 assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
 for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
 srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review100.native.json');assert audit['source_review']==srev
 assert len(v['semantic_slots'])==7 and not any(x.get('blocking',False) for x in v['deltas']) and not v['repairs']
 assert v['independent_from_formalizer'] and v['independent_from_decoder'] and sr['independence']['primary_first_frozen_before_current_production_exposition_decoder'] and not sr['independence']['prior_header_or_semantic_acceptance_used_as_fidelity_evidence'] and not sr['independence']['whole_math_verdict_used_as_semantic_anchor']
 rp=manifest(B/'reviewer-packet100.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
 assert info(B/'reviewer-packet100.json')['raw_sha256']==v['reviewer_packet_raw_sha256']
 cov=manifest(S/'compiled-source-coverage100.native.json');primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)==PRIMARY
 assert info(S/'compiled-source-coverage100.native.json')['raw_sha256']=='ce263cd50f95d2a1b32693a94dcdc98e2ddc3d940982387547a5c7ffceaf7e79'
 assert len(cov['source_regions'])==21 and cov['all21_source_slices_RAW_verified'] and len(cov['original19_ids'])==19 and cov['effective_node_count']==31 and cov['all28_inherited_nodes_disposed'] and not cov['topology_self_validation']
 lines=primary.splitlines(keepends=True)
 for x in cov['source_regions']:assert sha(b''.join(lines[x['line_start']-1:x['line_end']]))==x['raw_sha256'],x['id']
 expo=manifest(S/'exposition-review100.native.json');assert len(expo['all6exact_code_regions'])==6 and len(expo['private_helpers'])==3 and expo['private_statement']['no_new_provider_assumptions'] and expo['lesson']['raw_sha256']==info(L)['raw_sha256']
 lesson=load(L)['units'][0];code=(R/M).read_text(encoding='utf8').splitlines(keepends=True)
 for step,claim in zip(lesson['steps'],expo['all6exact_code_regions']):
  literal=''.join(code[claim['start_line']-1:claim['end_line']]);assert step['lean']==literal and step['formula']==claim['formula'];assert claim['byte_match'] and sha(literal.encode())==claim['exact_code_raw_sha256']
 current=load(P);cell=load(CELL);assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'];assert current['items'][0]['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage100.native.json')
 parents=sorted(x['declaration'] for x in whole['direct_consumed_public_producers']);assert len(parents)==5 and sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==parents
 assert sorted(expo['public_adapter']['actual_producers'])==sorted(q.split('.')[-1] for q in parents)
 sys.path[:0]=[str(R),str(R/'tools')]
 from tools import astis_publication as pub
 item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='7ae09932bffe3a6d37b5d6ca0caa183ade8d96019aabd32fb545245b7120d590'
 pub.check_advance([D],reviewed=True)
 topo=manifest(PRE/'independent-header-math100/topology-overlay100/source-topology-admission100.native.json');assert topo['decision']=='ACCEPT_BASE_PLUS_NARROW_OVERLAY_TOPOLOGY_AND_COVERAGE'
 save('science-scope100.json',dict(status='PASS',verified_commit=C,baseline=BASE,changed_files=changed,scoped_git_blobs=scope))
 save('archive-audit100.json',dict(status='PASS' if not unresolved else 'FAIL_UNRESOLVED_REFERENCES',verified_commit=C,archives=archive_rows,historical_reference_resolutions=history_rows,unresolved=unresolved))
 save('input-freeze100.json',dict(status='FAIL' if unresolved else 'PASS',verified_commit=C,unresolved=unresolved,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,historical_reference_resolutions=history_rows,kernel_transfer=info(B/'independent-whole-math100/fresh-kernel-receipt100.native.json')))
 assert not unresolved,unresolved
 oldp=B/'publication-before-compiled-coverage100.exactraw.snapshot.json';old=load(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
 oldcov=old['items'][0]['source_proof_coverage'];old['items'][0]['source_proof_coverage']=current['items'][0]['source_proof_coverage'];assert old==current
 save('metadata-transfer100.json',dict(status='PASS',verified_commit=C,reviewed_publication=info(oldp),prior_coverage=oldcov,only_publication_coverage_changed_after_review=True,publication_binding_sha256=bd,prior_cell_archived=info(B/'cell-before-compiled-coverage100.exactraw.snapshot.json')))
 save('source-acceptance100.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review100.native.json'),native_run=info(S/'source-review-run100.native.json'),closed_manifest=info(S/'closed-RAW-final-source100.native.json'),review_run_hash_recipe='Exact RAW SHA256',reviewer_packet_sha256=ph,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'decoder-run.json')['raw_sha256'],publication_binding_sha256=bd,canonical_copy_exact_except_evidence_path=True,all21source_regions_raw_verified=True,all19original_source_dispositions_retained=True,effective31graph_nodes_disposed=True,six_exposition_regions_accepted=True,all_three_private_helpers_source_reviewed=True,exact_five_actual_producer_parents=parents,lesson=info(L),topology_independent_acceptance=info(PRE/'independent-header-math100/topology-overlay100/source-topology-admission100.native.json'),canonical_final_coverage_pointer_present=True,coverage_only_transfer=True))
 save('primary-scope100.native.json',dict(status='PASS',verified_commit=C,no_new_full_primary_RAW_or_gzip=True,all_scoped_blobs_and_gzip_contents_checked=True,baseline_historical_primary_files_unchanged=True,no_new_primary_archive_created=True))
 assert head()==C
 print(json.dumps(dict(status='PASS_INPUTS_NATIVE_SOURCE',scoped_git_blobs=len(scope),exact_RAW_matches=len(matched),local_pinned=len(local),archives=len(archive_rows),historical_resolutions=len(history_rows))))
