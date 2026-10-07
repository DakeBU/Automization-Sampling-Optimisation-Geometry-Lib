import pathlib,json,hashlib,datetime,re
D=pathlib.Path(__file__).parent
sha=lambda b:hashlib.sha256(b).hexdigest()
lf=lambda b:b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def save(n,x):
 b=(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();(D/n).open('xb').write(b);return sha(b)
g=json.loads((D/'source-proof-graph.independent.json').read_bytes()); inv=json.loads((D/'source.inventory.json').read_bytes());inputs=json.loads((D/'inputs.frozen.json').read_bytes())['inputs']
for x in inputs:assert sha(pathlib.Path(x['path']).read_bytes())==x['raw_sha256']
usage=[]
spelling_replacements={'API-SCALAR-CALCULUS':['exists_deriv_eq_slope','differentiableAt_log','deriv.log','deriv_sqrt','Filter.EventuallyEq.deriv_eq','hasDerivAt_pow','deriv_add','deriv_sub','deriv_div']}
for n in g['nodes']:
 if not n['id'].startswith('API-'):continue
 old=n['api_names'];wanted=spelling_replacements.get(n['id'],old)
 aliases={'Real.log_zero':'log_zero','Real.sqrt_sq_eq_abs':'sqrt_sq_eq_abs','Real.log_lt_log':'log_lt_log','Real.log_exp':'log_exp'}
 wanted=[aliases.get(t,t) for t in wanted];located=[];unobserved=[]
 for symbol in wanted:
  occ=[]
  for reg in inv['regions']:
   if reg['disposition']!='NODE':continue
   lines=pathlib.Path(reg['raw_snapshot']).read_bytes().decode().replace('\r','').split('\n')
   for j,line in enumerate(lines):
    if symbol in line and not line.lstrip().startswith('--'):occ.append(dict(path=reg['path'],line=reg['start_line']+j,source_region_raw_sha256=reg['raw_sha256'],node_id=reg['node_id']))
  if occ:located.append(dict(source_spelling=symbol,occurrences=occ))
  else:unobserved.append(symbol)
 n['api_names']=[x['source_spelling'] for x in located];n['source_spelling_receipt']='source.api-spellings.json';n['truth_contract']='exact observed source references only; no local compiled/API-availability assertion'
 usage.append(dict(node_id=n['id'],original_family_labels=old,references=located,unobserved_labels_removed=unobserved,classification='literal source references, not Mathlib/API compilation'))
usagehash=save('source.api-spellings.json',dict(status='AUTHOR_LITERAL_REFERENCE_INVENTORY_NOT_API_OR_PROOF_VALIDATION',groups=usage,original_graph_raw_sha256=sha((D/'source-proof-graph.independent.json').read_bytes()),delta='Semantic-family labels sharpened to actual source spellings; unused integral_sub label removed. No mathematical dependency/formula changed.'))
primary=[]
for x in inputs:
 p=x['path'];name=pathlib.Path(p).name
 if not name.startswith('primary.S4.'):continue
 raw=pathlib.Path(p).read_bytes();entry=dict(path=p,raw_sha256=sha(raw),lf_sha256=sha(lf(raw)),physical_lf_lines=raw.count(b'\n')+(0 if raw.endswith(b'\n') else 1),whole_balanced_span=True)
 if '.S4.Ex8.' in name:entry.update(disposition='NODE',node_id='SPHMC-RHO-LAW',scope='entire actual rho definition; no finite Bernoulli theorem attribution')
 elif '.S4.SS1.p4.2.' in name:entry.update(disposition='NODE',node_id='SPHMC-RHO-LAW',scope='whole true standardized RGO density/curvature paragraph')
 elif '.S4.E6.' in name:
  alt=re.search(rb'alttext="([^"]*)"',raw).group(1).decode();pieces=alt.split('\\leqslant');assert len(pieces)==4
  entry.update(disposition='MIXED_BALANCED_SPAN',source_math_id='S4.E6.m1',alttext_exact=alt,clause_dispositions=[dict(relation_index=1,disposition='NODE',node_id='SPHMC-FIRST-4.6',formula=pieces[0]+'\\leqslant'+pieces[1],reason='actual ultimate consumer only'),dict(relation_index=2,disposition='EXCLUDED',formula=pieces[1]+'\\leqslant'+pieces[2],reason='neighbor eta-Lipschitz score bound outside finite Bernoulli/Gaussian-LSI producer delta'),dict(relation_index=3,disposition='EXCLUDED',formula=pieces[2]+'\\leqslant'+pieces[3],reason='neighbor Gibbs mode-zero moment/IBP bound outside delta')],line_partition='single original balanced display; clause partition exhaustive for all three relations; wrappers/label structural only')
 else:
  assert '.S4.SS1.p4.3.' in name
  text=raw.decode();start=text.index('Indeed, the first inequality');second=text.index('the second uses that');last=text.index('follows by integration by parts')
  bounds=[0,len(text[:start].encode()),len(text[:second].encode()),len(text[:last].encode()),len(raw)];reasons=['opening wrappers','Gaussian Talagrand + Gaussian LSI explanation','neighbor mode-zero eta-Lipschitz explanation','neighbor strong-log-concavity mode-zero IBP moment explanation and wrappers'];rec=[]
  for k in range(4):
   a,b=bounds[k:k+2];disp='NODE' if k==1 else 'EXCLUDED';rec.append(dict(relative_raw_byte_half_open=[a,b],raw_sha256=sha(raw[a:b]),disposition=disp,node_id='SPHMC-FIRST-4.6' if k==1 else None,reason=reasons[k]))
  assert bounds[0]==0 and bounds[-1]==len(raw) and sorted(bounds)==bounds
  entry.update(disposition='MIXED_BALANCED_SPAN',subregions=rec,partition_type='exact lexical byte partition within original balanced paragraph; not a replacement source anchor')
 primary.append(entry)
assert len(primary)==4
primaryhash=save('source.primary-coverage.json',dict(status='AUTHOR_COVERAGE_ADDENDUM_AWAITING_DISTINCT_REVIEW',whole_primary_raw_sha256=inputs[0]['raw_sha256'],relevant_balanced_spans=primary,scope='all four relevant original balanced spans; no whole primary/external project claim',no_printed_bernoulli_theorem=True))
g['status']='AUTHORED_REFINED_UNREVIEWED_SOURCE_PROOF_GRAPH';g['source_primary_coverage_raw_sha256']=primaryhash;g['source_api_spelling_receipt_raw_sha256']=usagehash;g['original_graph_raw_sha256']=sha((D/'source-proof-graph.independent.json').read_bytes());g['refinement_contract']='Only literal API spellings and explicit mixed PRIMARY coverage annotations added. All mathematical nodes, edges, source inventory, formulas, OR route and compiled_edges=[] unchanged.'
graphhash=save('source-proof-graph.refined.independent.json',g)
refhash=save('author.refinement.receipt.json',dict(status='AUTHOR_PREPARATION_NOT_INDEPENDENT_VALIDATION',original_graph_raw_sha256=g['original_graph_raw_sha256'],refined_graph_raw_sha256=graphhash,primary_coverage_raw_sha256=primaryhash,api_spelling_receipt_raw_sha256=usagehash,original_inventory_raw_sha256=sha((D/'source.inventory.json').read_bytes()),all_source_input_bytes_unchanged=True,nodes=len(g['nodes']),edges=len(g['edges']),or_hyperedges=len(g['or_hyperedges']),compiled_edges=[],canonical_review_target=(D/'source-proof-graph.refined.independent.json').as_posix(),failed_preparation_attempt='First refinement asserted integral_sub occurred in selected regions; assertion rejected it before any immutable refinement output; actual used spellings now located, unused label removed.'))
arts=[]
for p in sorted(D.iterdir()):
 if p.is_file() and p.name not in ['lease.json','author.refinement.lease.json','author.final-run.json']:
  b=p.read_bytes();arts.append(dict(path=p.as_posix(),raw_sha256=sha(b),lf_sha256=sha(lf(b)),bytes=len(b)))
basis=dict(actor='gaussian_domain_preproof_reviewer_29',artifacts=arts,read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,implementation_exposure=False,self_validation=False,review_target_raw_sha256=graphhash,all_input_hashes_rechecked=True)
runhash=sha(json.dumps(basis,sort_keys=True,separators=(',',':')).encode());save('author.final-run.json',dict(basis,deterministic_run_sha256=runhash,hash_recipe='UTF8 canonical compact sorted JSON basis, no newline'))
lease=json.loads((D/'author.refinement.lease.json').read_bytes());lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',closed_utc=datetime.datetime.utcnow().isoformat()+'Z',run_sha256=runhash,review_target_raw_sha256=graphhash);(D/'author.refinement.lease.json').write_bytes((json.dumps(lease,sort_keys=True,indent=2)+'\n').encode())
print(json.dumps(dict(graph_raw_sha256=graphhash,run_sha256=runhash,primary_coverage_raw_sha256=primaryhash,api_spellings_raw_sha256=usagehash,nodes=len(g['nodes']),edges=len(g['edges']),leases='CLOSED',removed=[(x['node_id'],x['unobserved_labels_removed']) for x in usage if x['unobserved_labels_removed']])))
