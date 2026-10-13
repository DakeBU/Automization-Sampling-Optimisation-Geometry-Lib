from context103 import *
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
 stage=load(B/'science-staging103.json');assert blob(B/'science-staging103.json')==(B/'science-staging103.json').read_bytes()
 scoped=list(dict.fromkeys(stage['files']+[rel(B/'science-staging103.json')]))
 changed=git('diff','--name-only',BASE,C).decode().splitlines();assert set(changed)<=set(scoped)
 assert len(stage['files'])==160 and len(scoped)==161,(len(scoped),len(stage['files']))
 assert not any('next-primary104' in p or 'exact-commit-verification103' in p for p in scoped)
 collab=load(B.parent/'pbps-actual-weighted-sector102/exact-commit-verification102/closed-RAW-manifest102.json')['preserved_collaborator_inputs']
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
   if 'source_RAW_sha256' in v:
    sp=rel(v['path']);sb=b''.join((R/sp).read_bytes().splitlines(keepends=True)[v['line_start']-1:v['line_end']]);assert sha(sb)==v['source_RAW_sha256'];assert sha(sb.replace(b'\r\n',b'\n'))==v['display_LF_RAW_sha256'];exact(sp);span_rows.append(v)
   if 'source_CRLF_span_RAW_sha256' in v:
    sp=rel(v['path']);sb=b''.join((R/sp).read_bytes().splitlines(keepends=True)[v['line_start']-1:v['line_end']]);assert sha(sb)==v['source_CRLF_span_RAW_sha256'];assert sha(sb.replace(b'\r\n',b'\n'))==v['display_LF_code_RAW_sha256'];exact(sp);span_rows.append(v)
   p=v.get('path');h=v.get('raw_sha256',v.get('sha256_raw',v.get('sha256')))
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
 assert info(M)['raw_sha256']=='c7806ada54ca78514a75ea1d13ed4bf08e5af4e92546d9ba0165683d77b36af4'
 assert git('-C','.lake/packages/mathlib','rev-parse','HEAD').decode().strip()=='db584cd6d46c92f209a44c0f1c829460d327499d'
 seal=manifest(PRE/'root.statement-seal103.json');assert info(PRE/'root.statement-seal103.json')['raw_sha256']=='ba1ff7c905e61907c4ed33ee79e11f8fd94ea1e24ea9aa3043af46b3e3caaa22'
 for p in scoped:
  if p.endswith('.json') and ('manifest' in p.lower() or 'freeze' in p.lower()):manifest(p)
 whole=manifest(B/'independent-whole-math103/whole-math-decision103.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL_TARGET' and whole['production']['raw_sha256']==info(M)['raw_sha256']
 prep=manifest(B/'independent-whole-math103/prepared-inputs103.native.json')
 for x in prep['inputs']:assert info(x['path'])['raw_sha256']==x['raw_sha256'],('changed fresh-kernel input',x['path'])
 wr=manifest(B/'independent-whole-math103/fresh-kernel-receipt103.native.json');assert wr['exit_code']==0 and wr['production_raw_sha256']==info(M)['raw_sha256']
 dec=R/'runs/semantic-roundtrip/anonymous103/decoder-native';dm=manifest(dec/'manifest.json');dr=manifest(dec/'reconstruction.json');run=manifest(dec/'decoder-run.json');dp=manifest(dec.parent/'input.json');audit=load(A);rec=audit['reconstruction']
 for x in dm['artifacts']:assert info(x['path'])['raw_sha256']==x['sha256_raw'] and info(x['path'])['bytes']==x['bytes']
 assert len(run['input_artifacts'])==1 and info(dec.parent/'input.json')['raw_sha256']==run['input_artifacts'][0]['sha256_raw']=='112ba7fd9de2df2fecb4d53fce76ff4c004da098b86057dbb2ee8c80bcf20bb9'
 packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==run['canonical_supplied_packet_sha256']==rec['decoder_packet_sha256']
 assert info(dec/'decoder-run.json')['raw_sha256']==rec['decoder_run_sha256']=='8e66a827415365514d257ec6e0c2aa2ac7fa0db8e0e10075c513d8f36be6c11a'
 assert info(dec/'reconstruction.json')['raw_sha256']==rec['native_named_payload_sha256'] and rec['native_semantic_slots']==dr
 assert all(not run[k] for k in ['source_text_visible','source_identity_visible','prior_audit_visible','repair_proposals_visible']) and not rec['source_text_visible'] and not run['additional_source_material_read']
 assert sha(dp['lean']['statement'].encode())==rec['lean_statement_sha256']==run['input_statement_sha256']
 assert rec['text']==(dec/'reconstruction.txt').read_text(encoding='utf8') and sha(rec['text'].encode())==rec['text_sha256']
 S=B/'final-source103';v=manifest(S/'source-review103.native.json');sr=manifest(S/'source-review-run103.native.json');sm=manifest(S/'closed-RAW-final-source103.native.json')
 assert info(S/'source-review103.native.json')['raw_sha256']=='56673ccd8c5b924e4e9631467432e76362e898374e341b94b58b43563d37e8cd'
 assert info(S/'source-review-run103.native.json')['raw_sha256']==v['review_run_sha256']==v['source_review']['review_run_sha256']=='69b222453f149eeadea5f8b87ceb4866fce09f539e22f74f3aa250c0c88ce7ea'
 assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
 for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
 srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review103.native.json');assert audit['source_review']==srev
 assert len(v['semantic_slots'])==7 and not v['repairs'] and not any(x['blocking'] for x in audit['deltas'])
 assert v['independent_from_formalizer'] and v['independent_from_decoder'] and sr['reviewer'] not in [sr['formalizer'],sr['decoder']] and sr['primary_first_closed_before_current_packet_and_production'] and not sr['earlier_final_semantic_verdicts_slots_deltas_repairs_used']
 pf=manifest(S/'primary-first103.native.json');assert pf['all21_RAW_slices_revalidated'] and pf['this_artifact_is_not_final_verdict']
 assert not srev['read_flags']['earlier_final_semantic_verdicts_slots_deltas_repairs_used'] and srev['read_flags']['primary_first_frozen_before_current_packet']
 rp=manifest(B/'reviewer-packet103.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']=='c11373d3e8a67a275fe8bcaa6913d30dba5b55aa102ff34e8f63706b6b8d98b4'
 cov=manifest(S/'compiled-source-coverage103.native.json');primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)==PRIMARY
 assert info(S/'compiled-source-coverage103.native.json')['raw_sha256']=='920da7682d433bdf7f2a6bae5876fbb16bccb77dc01cab54e9e028fd884ea9ad'
 assert len(cov['source_regions'])==21 and cov['all21_RAW_slices_verified'] and cov['effective_node_count']==51 and cov['effective_edge_count']==79 and not cov['topology_self_validated'] and cov['no102_to_NORM_proof_dependency']
 assert not cov['unresolved_gaps_within_selected_boundary'] and cov['whole149_lines_reviewed']
 lines=primary.splitlines(keepends=True)
 for x in cov['source_regions']:
  assert sha(b''.join(lines[x['line_start']-1:x['line_end']]))==x['raw_sha256'];assert sha(primary[x['byte_start']:x['byte_end_exclusive']])==x['raw_sha256']
 expo=manifest(S/'exposition-review103.native.json');assert expo['decision']=='ACCEPT_BOUNDED_AUTHORED_SEVEN_STEP_EXPOSITION' and len(expo['seven_regions'])==7 and not expo['repairs_required'] and expo['lesson']['raw_sha256']==info(L)['raw_sha256']
 lesson=load(L)['units'][0];code=(R/M).read_text(encoding='utf8').splitlines(keepends=True);assert len(lesson['steps'])==7
 for step,claim in zip(lesson['steps'],expo['seven_regions']):
  region=claim['source_span'];literal=''.join(code[region['line_start']-1:region['line_end']]);assert step['lean']==literal and step['formula']==claim['formula'] and step['text']==claim['text'];assert claim['accepted'] and sha(literal.encode())==region['display_LF_RAW_sha256']==claim['display_code_RAW_sha256']
 topo=manifest(PRE/'independent-header-math103/source-topology-admission103.native.json');assert topo['decision']=='ACCEPT_BASE_PLUS_API_IDENTITY_OVERLAY_TOPOLOGY_AND_COVERAGE' and topo['reviewer']!=cov['graph_author']
 assert len({x['id'] for x in cov['graph_nodes']})==51 and {x['id'] for x in cov['graph_nodes']}==set(topo['effective_graph']['topological_order'])
 assert {(x['source'],x['target']) for x in cov['edge_coverage']['new18']}=={tuple(x) for x in topo['effective_graph']['new_edges']}
 covered=set()
 for x in cov['whole_module_regions']:covered.update(range(x['line_start'],x['line_end']+1))
 assert covered==set(range(1,150))
 current=load(P);cell=load(CELL);assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'];assert current['items'][0]['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage103.native.json')
 parents=sorted(x['declaration'] for x in whole['direct_consumed_public_producers']);assert len(parents)==5 and sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==sorted(x['declaration'] for x in cov['actual_five_public_parents'])==parents
 assert sorted(x['declaration'] for x in expo['canonical_producers'])==parents and not any('ActualWeightedSector' in p for p in parents)
 sys.path[:0]=[str(R),str(R/'tools')]
 from tools import astis_publication as pub
 item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='349f71636e82ddb57d97fb9e228a792f1d77f13dd232decdccff39c399cce8b7'
 pub.check_advance([D],reviewed=True)
 oldp=B/'publication-before-compiled-coverage103.exactraw.snapshot.json';old=manifest(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
 oldcov=old['items'][0]['source_proof_coverage'];old['items'][0]['source_proof_coverage']=current['items'][0]['source_proof_coverage'];assert old==current
 oldcell=manifest(B/'cell-before-compiled-coverage103.exactraw.snapshot.json');oldcell['source_proof_coverage']=cell['source_proof_coverage'];assert oldcell==cell
 preproved=manifest(B/'cell-before-proved-local103.json');assert preproved['status']=='claimed';preproved['status']='proved_locally';preproved['evidence']['proved_local']=cell['evidence']['proved_local'];preproved['source_proof_coverage']=cell['source_proof_coverage'];assert preproved==cell
 assert cell['evidence']['owner']=='companion_root_20261005' and git('ls-tree',C,M).decode().startswith('100644 ')
 save('science-scope103.json',dict(status='PASS',verified_commit=C,baseline=BASE,changed_files=changed,scoped_git_blobs=scope))
 save('archive-audit103.json',dict(status='PASS' if not unresolved else 'FAIL_UNRESOLVED_REFERENCES',verified_commit=C,archives=archive_rows,historical_reference_resolutions=history_rows,verified_code_spans=span_rows,unresolved=unresolved))
 save('input-freeze103.json',dict(status='FAIL' if unresolved else 'PASS',verified_commit=C,unresolved=unresolved,exact_commit_matches=list(matched.values()),local_pinned_or_excluded_inputs=list(local.values()),preserved_collaborator_inputs=collab,historical_reference_resolutions=history_rows,kernel_transfer=info(B/'independent-whole-math103/fresh-kernel-receipt103.native.json')))
 assert not unresolved,unresolved
 save('metadata-transfer103.json',dict(status='PASS',verified_commit=C,reviewed_publication=info(oldp),prior_coverage=oldcov,only_publication_coverage_changed_after_review=True,publication_binding_sha256=bd,prior_cell_archived=info(B/'cell-before-compiled-coverage103.exactraw.snapshot.json'),cell_status_and_native_PROVED_LOCAL_evidence_transfer=True))
 save('source-acceptance103.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review103.native.json'),native_run=info(S/'source-review-run103.native.json'),closed_manifest=info(S/'closed-RAW-final-source103.native.json'),review_run_hash_recipe='Exact RAW SHA256',reviewer_packet_sha256=ph,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'decoder-run.json')['raw_sha256'],publication_binding_sha256=bd,canonical_copy_exact_except_evidence_path_with_native_prose_retained=True,all21source_regions_raw_verified=True,effective51graph_nodes_and79edges_disposed=True,seven_exposition_regions_accepted=True,whole149_lines_private_statement_and_public_proof_reviewed=True,exact_five_actual_producer_parents=parents,no102_to_NORM_dependency=True,lesson=info(L),topology_independent_acceptance=info(PRE/'independent-header-math103/source-topology-admission103.native.json'),canonical_final_coverage_pointer_present=True,coverage_only_transfer=True))
 save('primary-scope103.native.json',dict(status='PASS',verified_commit=C,no_new_full_primary_RAW_or_gzip=True,all_scoped_blobs_and_gzip_contents_checked=True,baseline_historical_primary_files_unchanged=True,no_new_primary_archive_created=True))
 assert head()==C
 print(json.dumps(dict(status='PASS_INPUTS_NATIVE_SOURCE',scoped_git_blobs=len(scope),exact_RAW_matches=len(matched),local_pinned=len(local),archives=len(archive_rows),historical_resolutions=len(history_rows),verified_code_spans=len(span_rows))))
