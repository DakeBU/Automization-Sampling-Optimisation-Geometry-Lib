from context106 import *
assert head()==C
S=B/'final-source106';W=B/'independent-whole-math106'
audit=load(A);v=load(S/'source-review106.native.json');sr=load(S/'source-review-run106.native.json');cov=load(S/'compiled-source-coverage106.native.json');expo=load(S/'exposition106.native.json')
assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review106.native.json');assert audit['source_review']==srev
assert info(S/'source-review-run106.native.json')['raw_sha256']==v['review_run_sha256']==srev['review_run_sha256']
assert len(v['semantic_slots'])==7 and not v['repairs'] and not any(x['blocking'] for x in v['deltas']) and not v['defects']
assert srev['independent_from_formalizer'] and srev['independent_from_decoder'] and sr['reviewer']=='/root/source_final96'
assert sr['source_input_read_before_production_and_decoder'] and sr['independently_owned_whole_module_review'] and sr['no_topology_self_validation']
assert not sr['prior_semantic_verdict_slots_deltas_or_repairs_used'] and not srev['prior_verdicts_or_slots_used'] and not srev['source_graph_creator_self_validation']
assert srev['whole_module_private_helper_reviewed'] and srev['independently_owned_exposition_audit']
rp=load(B/'reviewer-packet106.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
dec=R/'runs/semantic-roundtrip/anonymous106/decoder-native';dr=load(dec/'decoder.json');run=load(dec/'manifest.json');dp=load(dec.parent/'input.json');rec=audit['reconstruction']
for p,h in run['output_hashes'].items():assert info(dec/p)['raw_sha256']==h
assert info(dec.parent/'input.json')['raw_sha256']==run['input_raw_sha256']==dr['input_raw_sha256']
packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==run['packet_sha256']==rec['decoder_packet_sha256']==dr['packet_sha256']
assert info(dec/'manifest.json')['raw_sha256']==rec['decoder_run_sha256']==sr['decoder_manifest']['raw_sha256']
assert info(dec/'decoder.json')['raw_sha256']==rec['native_named_payload_sha256'] and rec['native_semantic_slots']==dr
assert all(not run[k] for k in ['source_visible','informal_proof_visible','publication_visible','repair_visible','reviewer_visible']) and not rec['source_text_visible']
assert sha(dp['lean']['statement'].encode())==rec['lean_statement_sha256']==dr['statement_sha256']
assert rec['text']==(dec/'reconstruction.txt').read_text(encoding='utf8') and sha(rec['text'].encode())==rec['text_sha256']
assert cov['effective_counts']==dict(source_regions=21,nodes=62,edges=123,actual_parents=3,production_lines=247,exposition_regions=8,statement_lets=39)
assert not cov['topology_self_validation']
basepath=B.parent/'pbps-actual-countable-endpoint105/next-primary106/independent-topology106/topology-admission106.native.json'
base=load(basepath);basegraph=base['effective_graph'];overlay=load(B/'source-route106/direct-marginal-overlay106.proposal.native.json');admission=load(W/'route-topology106/route-topology-admission106.native.json')
assert admission['decision']=='ACCEPT_MINIMAL_SELECTED_DIRECT_MARGINAL_OVERLAY' and admission['reviewer']!=sr['reviewer']
effective=load(B/'source-graph106.effective.json');original=load(R/overlay['base_graph']['path'])
expected=copy.deepcopy(original);expected['new_edges']+=overlay['new_edges'];expected['AND_route_alternatives']=overlay['AND_route_alternatives']
for key in original:
 if key not in ['new_edges']:assert effective[key]==original[key],key
assert effective['new_edges']==expected['new_edges'] and effective['AND_route_alternatives']==expected['AND_route_alternatives']
N=set(basegraph['nodes']);E={tuple(e) for e in basegraph['edges']}|{tuple(e) for e in overlay['new_edges']}
assert len(N)==62 and len(E)==123 and {x['id'] for x in cov['node_dispositions']}==N and {(x['source'],x['target']) for x in cov['edge_dispositions']}==E
assert admission['effective_counts']==effective['effective_counts']==dict(nodes=62,edges=123,primary_regions=21)
assert ('ENDPOINT-LAW105','INV100') in E and ('AVG100','INV100') in E
primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
plines=primary.splitlines(keepends=True)
for x in cov['source_regions']:assert sha(b''.join(plines[x['line_start']-1:x['line_end']]))==x['raw_sha256']==sha(primary[x['byte_start']:x['byte_end_exclusive']])
covered=set();mlines=(R/M).read_bytes().splitlines(keepends=True)
for x in cov['all_production_regions']:
 assert sha(b''.join(mlines[x['line_start']-1:x['line_end']]))==x['RAW_sha256'];covered.update(range(x['line_start'],x['line_end']+1))
assert covered==set(range(1,248))
span_count=0
def spans(x):
 global span_count
 if isinstance(x,dict):
  if 'file' in x and 'RAW_sha256' in x and 'line_start' in x:
   bs=b''.join((R/x['file']).read_bytes().splitlines(keepends=True)[x['line_start']-1:x['line_end']]);assert sha(bs)==x['RAW_sha256'];assert sha(bs.replace(b'\r\n',b'\n'))==x['LF_sha256'];span_count+=1
  for y in x.values():spans(y)
 elif isinstance(x,list):
  for y in x:spans(y)
spans(cov);spans(expo)
assert expo['verdict']=='ACCEPT_BOUNDED_AUTHORED_EIGHT_STEP_EXPOSITION_ONLY' and expo['lesson']['raw_sha256']==info(L)['raw_sha256']
assert not expo['source_theorem_repairs'] and not expo['exposition_repairs'] and not expo['defects']
lesson=load(L)['units'][0];assert len(lesson['steps'])==len(expo['steps'])==8
for step,claim in zip(lesson['steps'],expo['steps']):
 region=claim['span'];literal=b''.join(mlines[region['line_start']-1:region['line_end']]).decode().replace('\r\n','\n')
 assert step['lean']==literal and sha(step['formula'].encode())==claim['formula_RAW_sha256'] and sha(step['text'].encode())==claim['explanation_RAW_sha256'] and claim['accepted'] and sha(literal.encode())==claim['display_code_RAW_sha256']
whole=load(W/'whole-math-decision106.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL' and whole['production']==info(M)
prep=load(W/'prepared-inputs106.native.json')
for x in prep['inputs']:assert info(x['path'])==x
assert prep['literal_header_seal_privateProp_equal'] and not prep['imports_target_module']
def full(s):return ('AutoSamplingTheory.TechnicalLemmas.Probability.' if s.startswith('UnitExponentialProduct.') else 'AutoSamplingTheory.ExampleCases.ProximalBPS.')+s
parents=sorted(full(x['declaration']) for x in whole['genuine_direct_parents']);assert len(parents)==3
cell=load(CELL);current=load(P)
assert sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==sorted(x['declaration'] for x in cov['actual_parent_discharge'])==parents
assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'] and cell['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage106.native.json')
assert 'accepted compiled' in cell['source_proof_coverage']['coverage_status'].lower()
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='749440152478c976a357af4e6f2ad8c98031682582839d2b63370224131994dc'
pub.check_advance([D],reviewed=True)
oldp=B/'publication-before-compiled-coverage106.exactraw.snapshot.json';old=load(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
old['items'][0]['source_proof_coverage']=item['source_proof_coverage'];assert old==current
oldcell=load(B/'cell-before-compiled-coverage106.exactraw.snapshot.json');oldcell['source_proof_coverage']=cell['source_proof_coverage'];assert oldcell==cell
assert cell['status']=='proved_locally' and cell['evidence']['owner']=='companion_root_20261005' and cell['target_declarations']==[D]
assert cell['cell_id']=='ASTIS-SW-PBPS-actual-bounded-gibbs-duality'
save('metadata-transfer106.json',dict(status='PASS',verified_commit=C,publication_binding_sha256=bd,reviewed_publication=info(oldp),only_publication_and_cell_coverage_changed_after_review=True,route_overlay=info(W/'route-topology106/route-topology-admission106.native.json'),original_seal_and_graph_unchanged=True))
save('source-acceptance106.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review106.native.json'),native_run=info(S/'source-review-run106.native.json'),closed_manifest=info(S/'closed-RAW-final-source106.native.json'),canonical_copy_exact_except_evidence_path_with_prose_retained=True,seven_slots_exact=True,all21source_regions_RAW_verified=True,effective62nodes123edges_disposed=True,whole247lines_eight_exposition_regions=True,all_referenced_code_spans_verified=span_count,exact_three_parents=parents,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'manifest.json')['raw_sha256'],reviewer_packet_sha256=ph,publication_binding_sha256=bd,no_statement_or_exposition_repairs=True,canonical_compiled_coverage_pointer_current=True,topology_and_selected_route_independently_validated=True))
print('PASS_SOURCE_DECODER_ROUTE_COVERAGE')
