from context101 import *
import gzip
dispatch=frozen_dispatch();C=dispatch['science_commit'];BASE=dispatch['baseline_commit']
PRIMARY='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
if __name__=='__main__':
 assert head()==C and git('rev-parse',C+'^').decode().strip()==BASE
 tree={line.split('\t',1)[1]:line.split()[2] for line in git('ls-tree','-r',C).decode().splitlines()};cache={}
 def blob(p):
  p=rel(p)
  if p not in cache:cache[p]=git('cat-file','blob',tree[p])
  return cache[p]
 stage=load(B/'science-staging101.json');assert blob(B/'science-staging101.json')==(B/'science-staging101.json').read_bytes()
 scoped=list(dict.fromkeys(stage['files']+[rel(B/'science-staging101.json')]))
 changed=git('diff','--name-only',BASE,C).decode().splitlines();assert set(changed)<=set(scoped)
 assert len(stage['files'])==192 and len(scoped)==193,(len(scoped),len(stage['files']))
 assert not any('next-primary102' in p or 'exact-commit-verification101' in p for p in scoped)
 collab=load(B.parent/'pbps-actual-prescribed-path-reversal100/exact-commit-verification100/closed-RAW-manifest100.json')['preserved_collaborator_inputs']
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
 assert info(M)['raw_sha256']=='b9c6e8ed0655b9c607eff38ecf74eb3a4555ff90184475e8dfc554bb96dcb3c0'
 assert info(L)['raw_sha256']=='d208b02fc4c21700d99cf69bc55af3f0b8c71cc7a440901abc2bc7a854d39343'
 assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
 seal=manifest(PRE/'root.statement-seal101.json');assert info(PRE/'root.statement-seal101.json')['raw_sha256']=='cdd05195156722be3b65c56fc09fe48971e021df81afadb48968dbab50c81d59'
 for p in scoped:
  if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)
 whole=manifest(B/'independent-whole-math101/whole-math-decision101.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL_TARGET' and whole['production']['raw_sha256']==info(M)['raw_sha256']
 prep=manifest(B/'independent-whole-math101/prepared-inputs101.native.json')
 for x in prep['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],('changed fresh-kernel input',x['path'])
 wr=manifest(B/'independent-whole-math101/fresh-kernel-receipt101.native.json');assert wr['exit_code']==0 and wr['production_raw_sha256']==info(M)['raw_sha256']
 dec=R/'runs/semantic-roundtrip/anonymous101/decoder-native';dm=manifest(dec/'manifest.json');dr=manifest(dec/'reconstruction.json');run=manifest(dec/'decoder-run.json');dp=manifest(dec.parent/'input.json');audit=load(A);rec=audit['reconstruction']
 for x in dm['files']:
  assert info(dec/x['path'])['raw_sha256']==x['raw_sha256'] and info(dec/x['path'])['bytes']==x['bytes'];exact(dec/x['path'])
 assert info(dec.parent/'input.json')['raw_sha256']==dm['input']['raw_sha256']==run['input_raw_sha256']=='cb1ec328ad0a57a336da9c109e1a14c12a3f3a04d5a5c295b3762801e21a7a45'
 packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==dm['input']['packet_sha256_supplied']==run['packet_sha256_supplied']==rec['decoder_packet_sha256']
 rr=copy.deepcopy(run);rh=rr.pop('decoder_run_payload_sha256');assert sha(canon(rr))==rh==rec['native_canonical_payload_hash']
 assert info(dec/'decoder-run.json')['raw_sha256']==rec['decoder_run_sha256'] and info(dec/'reconstruction.json')['raw_sha256']==rec['native_named_payload_sha256']
 assert all(not run[k] for k in ['source_visible','source_text_visible','source_identity_visible','proof_visible']) and not rec['source_text_visible']
 assert sha(dp['lean']['statement'].encode())==rec['lean_statement_sha256']==run['lean_statement_utf8_sha256_computed']==run['lean_statement_sha256_supplied']
 assert rec['text']==(dec/'reconstruction.txt').read_text(encoding='utf8') and sha(rec['text'].encode())==rec['text_sha256']
 assert rec['native_semantic_slots']==dr
 S=B/'final-source101';v=manifest(S/'source-review101.native.json');sr=manifest(S/'source-review-run101.native.json');sm=manifest(S/'closed-RAW-final-source101.native.json')
 assert info(S/'source-review101.native.json')['raw_sha256']=='00fdb02e0cc5f2e574e0464f0a5485fc06567667e1e0d2e4e22fbbfc6080e612'
 assert info(S/'source-review-run101.native.json')['raw_sha256']==v['review_run_sha256']==v['source_review']['review_run_sha256']
 assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
 for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
 srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review101.native.json');assert audit['source_review']==srev
 assert len(v['semantic_slots'])==7 and not any(x.get('blocking',False) for x in v['deltas']) and not v['repairs'] and not v['unresolved_defects']
 assert v['independent_from_formalizer'] and v['independent_from_decoder'] and sr['independent_from_formalizer'] and sr['independent_from_decoder'] and sr['graph_author_not_topology_validator']
 pf=manifest(S/'primary-first/closed-RAW-primary-first101.native.json');assert pf['canonical_packet_not_read'] and pf['no_primary_copy']
 assert 'No prior semantic verdict, slots, deltas or whole-math acceptance used as fidelity decision.' in sr['reading_order']
 rp=manifest(B/'reviewer-packet101.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']=='ada43d2d1a5c74087e90387e5505ab9f8032418beb83f3ef56fff3c479903fb8'
 assert info(B/'reviewer-packet101.json')['raw_sha256']==sr['packet']['raw_sha256']
 oldrp=manifest(B/'reviewer-packet101.before-owner-erratum101.exactraw.snapshot.json');oldhash=oldrp.pop('packet_sha256');assert sha(canon(oldrp))==oldhash
 oldowner=oldrp['roles']['formalizer'];assert oldowner!=rp['roles']['formalizer'];oldrp['roles']['formalizer']=rp['roles']['formalizer'];assert oldrp==rp
 erratum=manifest(B/'owner-provenance-erratum101.json');assert rp['roles']['formalizer']==erratum['correct']=='companion_root_20261005' and erratum['reviewer_packet_sha256']==ph
 cov=manifest(S/'compiled-source-coverage101.native.json');primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)==PRIMARY
 assert info(S/'compiled-source-coverage101.native.json')['raw_sha256']=='0c134ba1157587bcc1accedd026a7cc63e7dc35a77635102fc3eca0f1fe5ccad'
 assert len(cov['source_regions'])==21 and cov['all21_RAW_slices_verified'] and cov['original19_ids_preserved'] and cov['effective_node_count']==36 and not cov['topology_self_validated']
 assert len(cov['graph_nodes'])==36 and len(cov['required14_nodes'])==14 and cov['all_selected_source_ingredients_covered_or_excluded'] and not cov['unresolved_gaps']
 assert cov['stable_target']=='WEIGHT100' and cov['display_alias_only']=='WEIGHT101'
 lines=primary.splitlines(keepends=True)
 for x in cov['source_regions']:
  assert sha(b''.join(lines[x['line_start']-1:x['line_end']]))==x['raw_sha256'],x['id']
  assert sha(primary[x['byte_start']:x['byte_end_exclusive']])==x['raw_sha256'],x['id']
 expo=manifest(S/'exposition-review101.native.json');assert expo['state']=='accepted' and len(expo['six_steps'])==6 and len(expo['all26_literal_definition_names'])==26 and expo['first20_exact_public94_text'] and not expo['unresolved_defects'] and expo['lesson']['raw_sha256']==info(L)['raw_sha256']
 lesson=load(L)['units'][0];code=(R/M).read_text(encoding='utf8').splitlines(keepends=True)
 for step,claim in zip(lesson['steps'],expo['six_steps']):
  region=claim['region'];literal=''.join(code[region['line_start']-1:region['line_end']]);assert step['lean']==literal and step['formula']==claim['formula'];assert claim['exact_code_matches'] and claim['judgment']=='PASS' and sha(literal.encode())==region['raw_sha256']
 assert len(expo['whole_module_inventory'])==5
 repair=manifest(B/'independent-index-clarification101/index-clarification-decision101.native.json');assert repair['decision']=='ACCEPT_INDEX_CONVENTION_CLARIFICATION' and repair['after']['raw_sha256']==info(L)['raw_sha256']
 topo=manifest(PRE/'independent-header-math101/source-topology-decision101.native.json');assert topo['decision']=='ACCEPT_SOURCE_TOPOLOGY_AND_COVERAGE' and topo['reviewer']!=cov['graph_author']
 current=load(P);cell=load(CELL);assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'];assert current['items'][0]['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage101.native.json')
 parents=sorted(x['declaration'] for x in whole['direct_consumed_public_producers']);assert len(parents)==4 and sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==sorted(cov['actual_four_parents'])==parents
 sys.path[:0]=[str(R),str(R/'tools')]
 from tools import astis_publication as pub
 item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='53fd5e8723d4680bad200242460cc94ef8cb5c17e07e751ba646eadc10ecd3b1'
 pub.check_advance([D],reviewed=True)
 oldp=B/'publication-before-compiled-coverage101.exactraw.snapshot.json';old=manifest(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256']==sr['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
 oldcov=old['items'][0]['source_proof_coverage'];old['items'][0]['source_proof_coverage']=current['items'][0]['source_proof_coverage'];assert old==current
 oldcell=manifest(B/'cell-before-compiled-coverage101.exactraw.snapshot.json');oldcell['source_proof_coverage']=cell['source_proof_coverage'];assert oldcell==cell
 save('science-scope101.json',dict(status='PASS',verified_commit=C,baseline=BASE,changed_files=changed,scoped_git_blobs=scope))
 save('archive-audit101.json',dict(status='PASS' if not unresolved else 'FAIL_UNRESOLVED_REFERENCES',verified_commit=C,archives=archive_rows,historical_reference_resolutions=history_rows,verified_code_spans=span_rows,unresolved=unresolved))
 save('input-freeze101.json',dict(status='FAIL' if unresolved else 'PASS',verified_commit=C,unresolved=unresolved,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,historical_reference_resolutions=history_rows,kernel_transfer=info(B/'independent-whole-math101/fresh-kernel-receipt101.native.json')))
 assert not unresolved,unresolved
 save('metadata-transfer101.json',dict(status='PASS',verified_commit=C,reviewed_publication=info(oldp),prior_coverage=oldcov,only_publication_and_cell_coverage_changed_after_review=True,publication_binding_sha256=bd,prior_cell_archived=info(B/'cell-before-compiled-coverage101.exactraw.snapshot.json'),owner_erratum=info(B/'owner-provenance-erratum101.json'),only_reviewer_packet_owner_and_derived_hash_changed=True,original_incorrect_owner=oldowner,independent_index_repair=info(B/'independent-index-clarification101/index-clarification-decision101.native.json')))
 save('source-acceptance101.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review101.native.json'),native_run=info(S/'source-review-run101.native.json'),closed_manifest=info(S/'closed-RAW-final-source101.native.json'),review_run_hash_recipe='Exact RAW SHA256',reviewer_packet_sha256=ph,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'decoder-run.json')['raw_sha256'],publication_binding_sha256=bd,canonical_copy_exact_except_evidence_path=True,all21source_regions_raw_verified=True,all19original_source_dispositions_retained=True,effective36graph_nodes_disposed=True,six_exposition_regions_accepted=True,whole_private_statement_and_public_proof_reviewed=True,exact_four_actual_producer_parents=parents,lesson=info(L),topology_independent_acceptance=info(PRE/'independent-header-math101/source-topology-decision101.native.json'),canonical_final_coverage_pointer_present=True,coverage_only_transfer=True,independent_index_repair_accepted=True,owner_erratum_verified=True))
 save('primary-scope101.native.json',dict(status='PASS',verified_commit=C,no_new_full_primary_RAW_or_gzip=True,all_scoped_blobs_and_gzip_contents_checked=True,baseline_historical_primary_files_unchanged=True,no_new_primary_archive_created=True))
 assert head()==C
 print(json.dumps(dict(status='PASS_INPUTS_NATIVE_SOURCE',scoped_git_blobs=len(scope),exact_RAW_matches=len(matched),local_pinned=len(local),archives=len(archive_rows),historical_resolutions=len(history_rows),verified_code_spans=len(span_rows))))
