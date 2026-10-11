from context102 import *
import gzip
assert head()==C
PRIMARY='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
if __name__=='__main__':
 assert head()==C and git('rev-parse',C+'^').decode().strip()==BASE
 tree={line.split('\t',1)[1]:line.split()[2] for line in git('ls-tree','-r',C).decode().splitlines()};cache={}
 def blob(p):
  p=rel(p)
  if p not in cache:cache[p]=git('cat-file','blob',tree[p])
  return cache[p]
 stage=load(B/'science-staging102.json');assert blob(B/'science-staging102.json')==(B/'science-staging102.json').read_bytes()
 scoped=list(dict.fromkeys(stage['files']+[rel(B/'science-staging102.json')]))
 changed=git('diff','--name-only',BASE,C).decode().splitlines();assert set(changed)<=set(scoped)
 assert len(stage['files'])==238 and len(scoped)==239,(len(scoped),len(stage['files']))
 assert not any('next-primary103' in p or 'exact-commit-verification102' in p for p in scoped)
 collab=load(B.parent/'pbps-actual-prescribed-weighted-density101/exact-commit-verification101/closed-RAW-manifest101.json')['preserved_collaborator_inputs']
 assert len(collab)==21 and collab==stage['preserved_collaborator_inputs']
 for x in collab:assert info(x['path'])['raw_sha256']==x['raw_sha256'],x['path']
 def batch_read(paths):
  batch=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
  for path in paths:
   if path in cache:continue
   batch.stdin.write((tree[path]+'\n').encode());batch.stdin.flush();hh=batch.stdout.readline().split();cache[path]=batch.stdout.read(int(hh[2]));assert batch.stdout.read(1)==b'\n'
  batch.stdin.close();assert batch.wait()==0
 batch_read(scoped)
 byhash={};archive_rows=[];matched={};local={};history_rows=[];span_rows=[];unresolved=[];scope=[]
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
   if 'source_CRLF_span_RAW_sha256' in v:
    sp=rel(v['path']);sb=b''.join((R/sp).read_bytes().splitlines(keepends=True)[v['line_start']-1:v['line_end']]);assert sha(sb)==v['source_CRLF_span_RAW_sha256'];assert sha(sb.replace(b'\r\n',b'\n'))==v['display_LF_code_RAW_sha256'];exact(sp);span_rows.append(v)
   p=v.get('path');h=v.get('raw_sha256',v.get('sha256'))
   if isinstance(p,str) and '/' in p.replace('\\','/') and isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h):
    p=rel(p)
    if (R/p).is_file() and 'line_start' in v and 'line_end' in v:
     rawlines=(R/p).read_bytes().splitlines(keepends=True);segment=b''.join(rawlines[v['line_start']-1:v['line_end']])
     assert sha(segment)==h,('source span RAW mismatch',v)
     exact(p);span_rows.append(v)
    elif (R/p).is_file() and sha((R/p).read_bytes())==h:exact(p)
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
 assert info(M)['raw_sha256']=='9fa8aee0014fc558c455f0350ffab8c43804645d2878b19d7704c8b6bea5f92b'
 assert info(L)['raw_sha256']=='4ab23c50b84320558679b51095af95570da4106637d0e9ed633a8bfc0d44a873'
 assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
 seal=manifest(PRE/'root.statement-seal102.json');assert info(PRE/'root.statement-seal102.json')['raw_sha256']=='53a4f942841eb1c8cd4f5bf99338bd3279ddc5cac6f1f0e755938c253cc62e51'
 for p in scoped:
  if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)
 whole=manifest(B/'independent-whole-math102/whole-math-decision102.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL_TARGET' and whole['production']['raw_sha256']==info(M)['raw_sha256']
 prep=manifest(B/'independent-whole-math102/prepared-inputs102.native.json')
 for x in prep['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],('changed fresh-kernel input',x['path'])
 wr=manifest(B/'independent-whole-math102/fresh-kernel-receipt102.native.json');assert wr['exit_code']==0 and wr['production_raw_sha256']==info(M)['raw_sha256']
 dec=R/'runs/semantic-roundtrip/anonymous102/decoder-native';dm=manifest(dec/'manifest.json');dr=manifest(dec/'reconstruction.json');run=manifest(dec/'decoder-run.json');dp=manifest(dec.parent/'input.json');audit=load(A);rec=audit['reconstruction']
 for x in dm['artifacts']:assert info(x['path'])['raw_sha256']==x['raw_sha256'] and info(x['path'])['bytes']==x['bytes']
 assert info(dec.parent/'input.json')['raw_sha256']==dm['input_artifact']['raw_sha256']==run['input_artifact']['raw_sha256']=='2127f8d794c96213cee209934393381ac943917a0c6ed1f5a45623fd46119d0c'
 packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==run['packet_sha256_supplied']==rec['decoder_packet_sha256']
 rr=copy.deepcopy(run);rh=rr.pop('decoder_run_payload_sha256');assert sha(canon(rr))==rh==rec['native_canonical_payload_hash']
 assert info(dec/'decoder-run.json')['raw_sha256']==rec['decoder_run_sha256'] and info(dec/'reconstruction.json')['raw_sha256']==rec['native_named_payload_sha256']
 assert all(not run[k] for k in ['source_visible','source_text_visible','source_identity_visible','proof_visible']) and not rec['source_text_visible']
 assert sha(dp['lean']['statement'].encode())==rec['lean_statement_sha256']==run['statement_sha256_supplied']
 assert rec['text']==(dec/'reconstruction.txt').read_text(encoding='utf8') and sha(rec['text'].encode())==rec['text_sha256'] and rec['native_semantic_slots']==dr
 S=B/'final-source102';v=manifest(S/'source-review102.native.json');sr=manifest(S/'source-review-run102.native.json');sm=manifest(S/'closed-RAW-final-source102.native.json')
 assert info(S/'source-review102.native.json')['raw_sha256']=='33e905e18b5c1b355cb5d4b854c6416399764bc4766e8c1270d2cc8615acff2e'
 assert info(S/'source-review-run102.native.json')['raw_sha256']==v['review_run_sha256']==v['source_review']['review_run_sha256']
 assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
 for k in ['semantic_slots','verdict','repairs']:assert audit[k]==v[k],k
 srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review102.native.json');assert audit['source_review']==srev
 adapter=manifest(B/'source-schema-adapter102/source-delta-schema-adapter102.native.json');manifest(B/'source-schema-adapter102/closed-RAW-source-schema-adapter102.native.json')
 assert adapter['reviewer']==v['reviewer'] and adapter['state']=='accepted_schema_adapter_only' and adapter['original_deltas']==v['deltas'] and adapter['canonical_deltas']==audit['deltas'] and adapter['no_new_mathematical_or_source_delta']
 assert len(adapter['canonical_deltas'])==len(v['deltas'])==3
 for old,new in zip(v['deltas'],audit['deltas']):
  assert new['severity']=='informational' and not new['blocking'] and new['description'];check=copy.deepcopy(new);check.pop('description');check['severity']=old['severity'];assert check==old
 beforeadapter=manifest(B/'audit-before-source-schema-adapter102.exactraw.snapshot.json');assert beforeadapter['deltas']==v['deltas'];beforeadapter['deltas']=audit['deltas'];assert beforeadapter==audit
 assert len(v['semantic_slots'])==7 and not v['repairs'] and not v['unresolved_defects'] and not any(x['blocking'] for x in audit['deltas'])
 assert v['independent_from_formalizer'] and v['independent_from_decoder'] and sr['independent_from_formalizer'] and sr['independent_from_decoder'] and not sr['prior_semantic_verdicts_as_decision_input']
 pf=manifest(S/'primary-first102.native.json');assert not pf['new_production_reader_decoder_packet_read_before_freeze'] and pf['no_full_primary_copy']
 rp=manifest(B/'reviewer-packet102.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']==adapter['reviewer_packet_sha256']=='d566b4cf4025c22c2964126a10efb1ee56b02bb16a65ed4eb5d666d70894dc40'
 cov=manifest(S/'compiled-source-coverage102.native.json');primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)==PRIMARY
 assert info(S/'compiled-source-coverage102.native.json')['raw_sha256']=='029dbf732dd9f0729c18e98988f183b140b5ad4da1ad148415b908bc96e8ca43'
 assert len(cov['source_regions'])==21 and cov['all21_RAW_slices_verified'] and len(cov['original19_ids_preserved'])==19 and cov['effective_node_count']==42 and not cov['topology_self_validated']
 assert len(cov['graph_nodes'])==42 and len(cov['required12_direct_nodes'])==12 and not cov['unresolved_gaps_within_selected_boundary'] and cov['display_alias_only']=={'RHO97':'TIME97'}
 lines=primary.splitlines(keepends=True)
 for x in cov['source_regions']:
  assert sha(b''.join(lines[x['line_start']-1:x['line_end']]))==x['raw_sha256'];assert sha(primary[x['byte_start']:x['byte_end_exclusive']])==x['raw_sha256']
 expo=manifest(S/'exposition-review102.native.json');assert expo['verdict']=='PASS_BOUNDED_MATHEMATICAL_EXPOSITION' and len(expo['six_steps'])==6 and expo['private_mathematical_helpers'].startswith('None;') and not expo['unresolved_defects'] and expo['lesson']['raw_sha256']==info(L)['raw_sha256']
 lesson=load(L)['units'][0];code=(R/M).read_text(encoding='utf8').splitlines(keepends=True)
 for step,claim in zip(lesson['steps'],expo['six_steps']):
  region=claim['source_region'];literal=''.join(code[region['line_start']-1:region['line_end']]);assert step['lean']==literal and step['formula']==claim['formula'];assert claim['verdict']=='PASS' and sha(literal.encode())==region['display_LF_code_RAW_sha256']==claim['literal_display_code_RAW_sha256']
 topo=manifest(PRE/'independent-header-math102/source-topology-admission102.native.json');assert topo['decision']=='ACCEPT_BASE_PLUS_IDENTITY_NORMALIZATION_TOPOLOGY_AND_COVERAGE' and topo['reviewer']!=cov['graph_author']
 assert len({x['id'] for x in cov['graph_nodes']})==42 and {x['id'] for x in cov['graph_nodes']}==set(topo['effective_graph']['topological_order'])
 current=load(P);cell=load(CELL);assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'];assert current['items'][0]['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage102.native.json')
 parents=sorted(x['declaration'] for x in whole['direct_consumed_public_producers']);assert len(parents)==3 and sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==sorted(x['declaration'] for x in cov['actual_three_parents'])==parents
 assert sorted(x['declaration'] for x in expo['actual_parent_discharge'])==parents
 sys.path[:0]=[str(R),str(R/'tools')]
 from tools import astis_publication as pub
 item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']==adapter['publication_binding_sha256']=='0ae4b9423e05b131daa5eb62f0cfcb8fc5b074dbe59040abac3f564ba9739dd9'
 pub.check_advance([D],reviewed=True)
 oldp=B/'publication-before-compiled-coverage102.exactraw.snapshot.json';old=manifest(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
 oldcov=old['items'][0]['source_proof_coverage'];old['items'][0]['source_proof_coverage']=current['items'][0]['source_proof_coverage'];assert old==current
 oldcell=manifest(B/'cell-before-compiled-coverage102.exactraw.snapshot.json');preproved=manifest(B/'cell-before-proved-local102.exactraw.snapshot.json');preproved['status']='proved_locally';preproved['evidence']['independent_math']=rel(B/'independent-whole-math102/whole-math-decision102.native.json');assert preproved==oldcell;oldcell['source_proof_coverage']=cell['source_proof_coverage'];assert oldcell==cell
 inherited=manifest(B/'inherited-storage-mirror-normalization102/before-and-plan.json');done=manifest(B/'inherited-storage-mirror-normalization102/completion.json');mapping=manifest(inherited['prior_manifest']['path']);assert done['status']=='PASS' and len(inherited['files'])==2
 for x in inherited['files']:
  record=next(z for z in mapping['files'] if z['raw_path']==x['raw_path']);assert all(x[k]==record[k] for k in record)
  ab=blob(x['archive']);rb=gzip.decompress(ab);assert sha(ab)==x['archive_raw_sha256'] and sha(rb)==x['raw_sha256']
  assert blob(x['raw_path'])==git('show',BASE+':'+x['raw_path'])==(R/x['raw_path']).read_bytes();assert sha(blob(x['raw_path']))==x['public_text_raw_sha256']
  assert ab==git('show',BASE+':'+x['archive'])
 save('inherited-storage-transfer102.native.json',dict(status='PASS',verified_commit=C,baseline=BASE,mapping=info(inherited['prior_manifest']['path']),reconciliation=info(B/'inherited-storage-mirror-normalization102/before-and-plan.json'),files=inherited['files'],exact_originals_in_unchanged_committed_archives=True,public_mirrors_equal_preexisting_baseline_Git_blobs=True,no_native_decision_rewrite=True))
 save('science-scope102.json',dict(status='PASS',verified_commit=C,baseline=BASE,changed_files=changed,scoped_git_blobs=scope))
 save('archive-audit102.json',dict(status='PASS' if not unresolved else 'FAIL_UNRESOLVED_REFERENCES',verified_commit=C,archives=archive_rows,historical_reference_resolutions=history_rows,verified_code_spans=span_rows,unresolved=unresolved))
 save('input-freeze102.json',dict(status='FAIL' if unresolved else 'PASS',verified_commit=C,unresolved=unresolved,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,historical_reference_resolutions=history_rows,kernel_transfer=info(B/'independent-whole-math102/fresh-kernel-receipt102.native.json')))
 assert not unresolved,unresolved
 save('metadata-transfer102.json',dict(status='PASS',verified_commit=C,reviewed_publication=info(oldp),prior_coverage=oldcov,only_publication_coverage_changed_after_review=True,publication_binding_sha256=bd,prior_cell_archived=info(B/'cell-before-compiled-coverage102.exactraw.snapshot.json'),cell_status_and_exact_independent_math_evidence_PROVED_LOCAL_transfer=True,source_schema_adapter=info(B/'source-schema-adapter102/source-delta-schema-adapter102.native.json'),only_reviewed_informational_severity_and_description_adapter=True))
 save('source-acceptance102.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review102.native.json'),native_run=info(S/'source-review-run102.native.json'),closed_manifest=info(S/'closed-RAW-final-source102.native.json'),review_run_hash_recipe='Exact RAW SHA256',reviewer_packet_sha256=ph,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'decoder-run.json')['raw_sha256'],publication_binding_sha256=bd,canonical_copy_exact_except_evidence_path_and_reviewed_delta_schema_adapter=True,source_schema_adapter=info(B/'source-schema-adapter102/source-delta-schema-adapter102.native.json'),all21source_regions_raw_verified=True,all19original_source_dispositions_retained=True,effective42graph_nodes_disposed=True,six_exposition_regions_accepted=True,CRLF_original_and_LF_display_regions_separately_rehashed=True,whole_private_statement_and_public_proof_reviewed=True,exact_three_actual_producer_parents=parents,lesson=info(L),topology_independent_acceptance=info(PRE/'independent-header-math102/source-topology-admission102.native.json'),canonical_final_coverage_pointer_present=True,coverage_only_transfer=True))
 save('primary-scope102.native.json',dict(status='PASS',verified_commit=C,no_new_full_primary_RAW_or_gzip=True,all_scoped_blobs_and_gzip_contents_checked=True,baseline_historical_primary_files_unchanged=True,no_new_primary_archive_created=True))
 assert head()==C
 print(json.dumps(dict(status='PASS_INPUTS_NATIVE_SOURCE',scoped_git_blobs=len(scope),exact_RAW_matches=len(matched),local_pinned=len(local),archives=len(archive_rows),historical_resolutions=len(history_rows),verified_code_spans=len(span_rows))))
