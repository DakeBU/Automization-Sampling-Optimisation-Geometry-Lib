from context108 import *
assert head()==C
S=B/'final-source108';W=B/'independent-whole-math108'
audit=load(A);v=load(S/'source-review108.native.json');sr=load(S/'source-review-run108.native.json');cov=load(S/'compiled-source-coverage108.native.json');expo=load(S/'exposition108.native.json')
assert info(S/'source-review108.native.json')['raw_sha256']=='d5109c3de5df15e597bea5bba8bd56f333ca3e84f7c8f8c4bd145393e5dd9b7d'
assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k]==sr[k],k
srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review108.native.json');assert audit['source_review']==srev
assert info(S/'source-review-run108.native.json')['raw_sha256']==v['review_run_sha256']==srev['review_run_sha256']
assert len(v['semantic_slots'])==7 and not v['repairs'] and not any(x['blocking'] for x in v['deltas']) and not v['blocking_findings']
assert srev['independent_from_formalizer'] and srev['independent_from_decoder'] and sr['reviewer']=='/root/source_final96'
anti=sr['anti_anchoring'];assert anti['primary_before_current_production_publisher_decoder'] and not anti['prior_final_verdict_slots_deltas_used'] and anti['topology_admission_by_separate_reviewer_only']
assert srev['primary_first'] and srev['whole_module_review'] and srev['private_helpers_reviewed'] and not srev['prior_verdicts_read'] and not srev['topology_creator_self_admission']
rp=load(B/'reviewer108.v2.input.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
dec=R/'runs/semantic-roundtrip/anonymous108/decoder-native';dr=load(dec/'decoder.json');run=load(dec/'manifest.json');dp=load(dec.parent/'input.json');rec=audit['reconstruction']
for p,row in run['outputs'].items():assert info(dec/p)['raw_sha256']==row['raw_sha256']
assert info(dec.parent/'input.json')['raw_sha256']==run['input']['raw_sha256']==dr['input_raw_sha256']
packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==run['input']['packet_sha256']==rec['decoder_packet_sha256']==dr['packet_sha256']
assert info(dec/'manifest.json')['raw_sha256']==rec['decoder_run_sha256']==sr['blind_manifest']['raw_sha256']
assert info(dec/'decoder.json')['raw_sha256']==rec['native_named_payload_sha256'] and rec['native_semantic_slots']==dr
assert all(not x for k,x in run.items() if k.endswith('_visible')) and all(not x for k,x in dr.items() if k.endswith('_visible') or k.endswith('_performed'))
assert run['finalized'] and run['immutable_after_finalization'] and not rec['source_text_visible']
assert sha(dp['lean']['statement'].encode())==rec['lean_statement_sha256']==dr['statement_sha256']
assert rec['text']==(dec/'reconstructed-theorem.txt').read_text(encoding='utf8')==dr['reconstructed_theorem_text'] and sha(rec['text'].encode())==rec['text_sha256']==dr['reconstructed_text_sha256']
payload=copy.deepcopy(dr);native_hash=payload.pop('decoder_run_sha256');assert sha(canon(payload))==native_hash==run['decoder_run_sha256']==sr['native_decoder_run_sha256']
assert dr['decoder']=='independent-source-blind-decoder:/root/blind_decoder108' and sr['canonical_adopted_decoder_run_sha256']==rec['decoder_run_sha256']
assert cov['counts']==dict(source_regions=21,Lean_lines=289,nodes=107,edges=196) and cov['source_creator_does_not_self_admit_topology']
graph=load(cov['effective_graph']['path']);top=load(cov['independent_topology_admission']['path'])
assert top['decision']=='ACCEPT_EXACT_PROSPECTIVE108_GRAPH_V2' and top['reviewer']!=top['source_creator']==sr['reviewer']
assert info(cov['effective_graph']['path'])['raw_sha256']==top['effective_graph_v2_raw_sha256']=='01445f165e08e4402e5d61843d019ad84394f31fb945d724ec79cd183d2bfe6d'
N={x['id'] for x in graph['nodes']};E={(x['source'],x['target']) for x in graph['edges']}
assert len(N)==107 and len(E)==196 and {x['id'] for x in cov['node_coverage']}==N and {(x['source'],x['target']) for x in cov['edge_coverage']}==E
assert all(x['disposition'] for x in cov['node_coverage']+cov['edge_coverage'])
primary=(R/cov['primary']['path']).read_bytes();assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
plines=primary.splitlines(keepends=True)
for x in cov['regions']:assert sha(b''.join(plines[x['line_start']-1:x['line_end']]))==x['raw_sha256']==sha(primary[x['byte_start']:x['byte_end_exclusive']])
covered=set();mlines=(R/M).read_bytes().splitlines(keepends=True)
for x in cov['module_regions']:
 assert sha(b''.join(mlines[x['line_start']-1:x['line_end']]))==x['source_span_RAW_sha256'];covered.update(range(x['line_start'],x['line_end']+1))
assert covered==set(range(1,290)) and cov['source_binder_count']==6 and cov['algorithm_let_count']==37 and cov['statement_let_count']==41
assert expo['verdict']=='ACCEPT_EIGHT_AUTHORED_ADJACENT_FORMULA_REGIONS_ONLY' and expo['lesson']==info(L)
lesson=load(L)['units'][0];assert len(lesson['steps'])==len(expo['regions'])==8
used=[]
for step,x in zip(lesson['steps'],expo['regions']):
 literal=b''.join(mlines[x['line_start']-1:x['line_end']]);assert sha(literal)==x['raw_source_span_sha256']==x['displayed_code_UTF8_sha256']
 assert step['lean']==literal.decode() and step['formula']==x['formula'] and step['title']==x['title'] and x['verdict']=='accepted'
 used.extend(range(x['line_start'],x['line_end']+1))
assert used==list(range(187,286))
repair=load(B/'adjacency-repair108/proposal108.json');admission=load(B/'independent-adjacency-repair108/admission108.native.json')
assert admission['decision']=='ACCEPT_EXACT_ADJACENCY_REPAIR108' and admission['reviewer'] not in [repair['creator'],repair['finding_author']]
assert info(B/'adjacency-repair108/proposal108.json')['raw_sha256']==admission['proposal_RAW_sha256']
assert admission['production_RAW_sha256']==info(M)['raw_sha256'] and not admission['remaining_blocking_findings']
oldlesson=load(repair['before']['path']);newlesson=load(repair['after']['path']);assert newlesson==load(L)
for x in [repair['before'],repair['after']]:assert info(x['path'])==x
for i in [1,2]:
 for k in ['lean','lean_source_region']:oldlesson['units'][0]['steps'][i][k]=newlesson['units'][0]['steps'][i][k]
assert oldlesson==newlesson
assert admission['after_lesson_RAW_sha256']==info(L)['raw_sha256'] and admission['accepted_new_publication_binding_sha256']==v['publication_binding_sha256']
assert info(B/'independent-adjacency-repair108/admission108.native.json')==expo['separate_repair_admission']==sr['repair_history']['independent_admission']
whole=load(W/'whole-math-decision108.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL' and whole['production']==info(M)
prep=load(W/'prepared-inputs108.native.json')
for x in prep['inputs']:assert info(x['path'])==x
assert prep['literal_header_seal_privateProp_equal'] and not prep['imports_target_module']
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.'+x['declaration'] for x in whole['genuine_direct_parents']];assert len(parents)==1
cell=load(CELL);current=load(P)
assert sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==sorted(x['declaration'] for x in cov['genuine_direct_producers'])==parents
assert cov['genuine_direct_producers'][0]['count']==1
assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'] and cell['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage108.native.json')
assert 'accepted compiled' in cell['source_proof_coverage']['coverage_status'].lower()
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='f9236569dac3fd0a3d57346165556a193c3b65d019b37bb5db13bdc84df1a4dd'
pub.check_advance([D],reviewed=True)
oldp=B/'publication-before-compiled-coverage108.exactraw.snapshot.json';old=load(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
old['items'][0]['source_proof_coverage']=item['source_proof_coverage'];assert old==current
oldcell=load(B/'cell-before-compiled-coverage108.exactraw.snapshot.json');oldcell['source_proof_coverage']=cell['source_proof_coverage'];assert oldcell==cell
assert cell['status']=='proved_locally' and cell['evidence']['owner']=='companion_root_20261005' and cell['target_declarations']==[D] and cell['cell_id']=='ASTIS-SW-PBPS-actual-l2-flip-duality'
save('metadata-transfer108.json',dict(status='PASS',verified_commit=C,publication_binding_sha256=bd,reviewed_publication=info(oldp),only_publication_and_cell_coverage_changed_after_final_review=True,adjacency_repair_admission=info(B/'independent-adjacency-repair108/admission108.native.json'),original_seal_and_graph_unchanged=True))
save('source-acceptance108.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review108.native.json'),native_run=info(S/'source-review-run108.native.json'),closed_manifest=info(S/'closed-RAW-final-source108.native.json'),canonical_copy_exact_except_evidence_path_with_prose_retained=True,seven_slots_exact=True,all21source_regions_RAW_verified=True,effective107nodes196edges_disposed=True,whole289lines_eight_exposition_regions=True,exact_one_parent=parents,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'manifest.json')['raw_sha256'],native_decoder_run_sha256=native_hash,native_decoder_run_recipe='Canonical decoder object excluding decoder_run_sha256; distinct from adopted manifest RAW binding.',reviewer_packet_sha256=ph,publication_binding_sha256=bd,no_statement_repairs=True,independent_region_only_adjacency_repair=True,canonical_compiled_coverage_pointer_current=True,topology_and_selected_route_independently_validated=True))
print('PASS_SOURCE_DECODER_ROUTE_COVERAGE')
