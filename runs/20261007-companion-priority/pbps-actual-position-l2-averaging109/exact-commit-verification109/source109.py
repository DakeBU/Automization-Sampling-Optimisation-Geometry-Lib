from context109 import *
assert head()==C
S=B/'final-source109';W=B/'independent-whole-math109'
audit=load(A);v=load(S/'source-review109.native.json');sr=load(S/'reviewer-run109.native.json');cov=load(S/'compiled-source-coverage109.native.json');expo=load(S/'exposition109.native.json')
assert info(S/'source-review109.native.json')['raw_sha256']=='0f8f3b8fb429db8fdd303b27855fdd603687702074532bbba59469ceeb279698'
assert info(S/'closed-RAW-final-source109.native.json')['raw_sha256']=='99a8cc3873530cc3dbaa5e3beecc8de1c5f1acd824fc00c56e9dc3097c45c4ec'
assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review109.native.json');assert audit['source_review']==srev
assert info(S/'reviewer-run109.native.json')['raw_sha256']==v['review_run_sha256']==srev['review_run_sha256']
assert len(v['semantic_slots'])==7 and not v['repairs'] and not any(x['blocking'] for x in v['deltas']) and not sr['blocking_findings']
assert srev['independent_from_formalizer'] and srev['independent_from_decoder'] and sr['reviewer']=='/root/source_final96'
assert not sr['prior_semantic_verdict_slots_deltas_repairs_used'] and not sr['source_graph_self_admitted']
assert all(sr[k] for k in ['read_original_source','read_current_lean_module','read_candidate_exposition','read_fresh_blind_reconstruction','decoder_originals_unchanged'])
rp=load(B/'reviewer109.input.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
dec=R/'runs/semantic-roundtrip/anonymous109/decoder-native';dr=load(dec/'decoder.json');run=load(dec/'manifest.json');dp=load(dec.parent/'input.json');rec=audit['reconstruction']
for row in run['outputs']:assert info(row['path'])['raw_sha256']==row['sha256']
assert info(dec.parent/'input.json')['raw_sha256']==run['input']['raw_sha256']==dr['input_raw_sha256']
packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==run['input']['packet_sha256']==rec['decoder_packet_sha256']==dr['packet_sha256']
assert info(dec/'manifest.json')['raw_sha256']==rec['decoder_run_sha256']==sr['native_decoder_manifest']['raw_sha256']
assert info(dec/'decoder.json')['raw_sha256']==rec['native_named_payload_sha256'] and rec['native_semantic_slots']==dr
assert all(not x for k,x in run.items() if k.endswith('_visible')) and all(not x for k,x in dr.items() if k.endswith('_visible')) and not rec['source_text_visible']
assert sha(dp['lean']['statement'].encode())==rec['lean_statement_sha256']
assert rec['text']==(dec/'reconstructed-theorem.txt').read_text(encoding='utf8')==dr['reconstructed_theorem'] and sha(rec['text'].encode())==rec['text_sha256']==dr['reconstruction_sha256']
assert dr['decoder']==run['decoder']==sr['decoder_identity'] and dr['decoder']['agent']=='/root/blind_decoder109'
assert cov['counts']==dict(source_regions=24,module_lines=349,nodes=123,edges=247) and cov['source_creator_does_not_self_admit_topology']
graph=load(cov['effective_graph']['path']);top=load(cov['independent_topology_admission']['path'])
assert top['decision']=='ACCEPT_EXACT_ROUTE_ADAPTER109_PROPOSAL' and top['reviewer']!=top['proposal_creator']==sr['reviewer'] and not top['blocking_findings']
assert info(cov['effective_graph']['path'])['raw_sha256']==top['graph_RAW_sha256']=='872b52629d4ee4e8f12ffdddc1021f661183a220e61f16f3df741f4f759be1f9'
assert info(B/'route-adapter109/route-adapter-proposal109.native.json')['raw_sha256']==top['proposal_RAW_sha256']
assert top['production_RAW_sha256']==info(M)['raw_sha256'] and top['header_RAW_sha256']==info(PRE/'Header109.lean')['raw_sha256']
assert info(cov['independent_topology_admission']['path'])==cov['independent_topology_admission']
N={x['id'] for x in graph['nodes']};E={(x['source'],x['target']) for x in graph['edges']}
assert len(N)==123 and len(E)==247 and {x['id'] for x in cov['node_coverage']}==N and {(x['source'],x['target']) for x in cov['edge_coverage']}==E
assert all(x['disposition'] for x in cov['node_coverage']+cov['edge_coverage'])
primary=(R/cov['primary']['path']).read_bytes();assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
plines=primary.splitlines(keepends=True)
for x in cov['regions']:assert sha(b''.join(plines[x['line_start']-1:x['line_end']]))==x['raw_sha256']==sha(primary[x['byte_start']:x['byte_end_exclusive']])
covered=set();mlines=(R/M).read_bytes().splitlines(keepends=True)
for x in cov['module_regions']:
 assert sha(b''.join(mlines[x['line_start']-1:x['line_end']]))==x['source_span_RAW_sha256'];covered.update(range(x['line_start'],x['line_end']+1))
assert covered==set(range(1,350)) and cov['source_binder_count']==6 and cov['algorithm_let_count']==37 and cov['statement_let_count']==47
assert expo['verdict']=='ACCEPT_AUTHORED_EIGHT_STEP_EXPOSITION_ONLY' and expo['lesson']==info(L) and not expo['repairs_required']
lesson=load(L)['units'][0];assert len(lesson['steps'])==len(expo['steps'])==8
used=[]
for step,x in zip(lesson['steps'],expo['steps']):
 z=x['region'];literal=b''.join(mlines[z['line_start']-1:z['line_end']]);assert sha(literal)==z['source_span_RAW_sha256']==x['displayed_code_raw_sha256']
 assert step['lean']==literal.decode() and step['formula']==x['formula'] and step['title']==x['title'] and step['text']==x['prose'] and x['judgment']=='accepted'
 used.extend(range(z['line_start'],z['line_end']+1))
assert used==list(range(213,346))
whole=load(W/'whole-math-decision109.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL' and whole['production']==info(M)
prep=load(W/'prepared-inputs109.native.json')
for x in prep['inputs']:assert info(x['path'])==x
assert prep['literal_header_seal_privateProp_equal'] and not prep['imports_target_module']
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.'+x['declaration'] for x in whole['genuine_direct_parents']];assert len(parents)==1
cell=load(CELL);current=load(P)
assert sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==sorted(x['declaration'] for x in cov['genuine_direct_producers'])==parents
assert cov['genuine_direct_producers'][0]['count']==1
assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'] and cell['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage109.native.json')
assert 'accepted compiled' in cell['source_proof_coverage']['coverage_status'].lower()
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='b6a33bb707739b8d84bcf58ba8e78a227b0a053ee46527c61f63215d121ce3f6'
pub.check_advance([D],reviewed=True)
oldp=B/'publication-before-compiled-coverage109.exactraw.snapshot.json';old=load(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
old['items'][0]['source_proof_coverage']=item['source_proof_coverage'];assert old==current
oldcell=load(B/'cell-before-compiled-coverage109.exactraw.snapshot.json');oldcell['source_proof_coverage']=cell['source_proof_coverage'];assert oldcell==cell
assert cell['status']=='proved_locally' and cell['evidence']['owner']=='companion_root_20261005' and cell['target_declarations']==[D] and cell['cell_id']=='ASTIS-SW-PBPS-actual-position-l2-averaging'
save('metadata-transfer109.json',dict(status='PASS',verified_commit=C,publication_binding_sha256=bd,reviewed_publication=info(oldp),only_publication_and_cell_coverage_changed_after_final_review=True,route_adapter_admission=info(cov['independent_topology_admission']['path']),original_seal_and_graph_unchanged=True))
save('source-acceptance109.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review109.native.json'),native_run=info(S/'reviewer-run109.native.json'),closed_manifest=info(S/'closed-RAW-final-source109.native.json'),canonical_copy_exact_except_evidence_path_with_prose_retained=True,seven_slots_exact=True,all24source_regions_RAW_verified=True,effective123nodes247edges_disposed=True,whole349lines_eight_exposition_regions=True,exact_one_parent=parents,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'manifest.json')['raw_sha256'],decoder_run_recipe='Adopted run is exact native manifest RAW. Native109 decoder has no internal run digest field.',reviewer_packet_sha256=ph,publication_binding_sha256=bd,no_statement_repairs=True,route_adapter_independently_admitted=True,canonical_compiled_coverage_pointer_current=True,topology_and_selected_route_independently_validated=True))
print('PASS_SOURCE_DECODER_ROUTE_COVERAGE')
