from context104 import *
assert head()==C
S=B/'final-source104';W=B/'independent-whole-math104'
audit=load(A);v=load(S/'source-review104.native.json');sr=load(S/'source-review-run104.native.json');cov=load(S/'compiled-source-coverage104.native.json');expo=load(S/'exposition104.native.json')
assert info(S/'source-review104.native.json')['raw_sha256']=='d0d9ad2cda17d4d8ebfc8d086cc795d2faa160becb72d814ac19b230e7a63bbd'
assert info(S/'closed-RAW-final-source104.native.json')['raw_sha256']=='0f04537d2cfeadfcdbc0692156aa2d44d45ad10560ecedad05f84997b0bcf713'
assert info(S/'source-review-run104.native.json')['raw_sha256']==v['review_run_sha256']==v['source_review']['review_run_sha256']
assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review104.native.json');assert audit['source_review']==srev
assert len(v['semantic_slots'])==7 and not v['repairs'] and not any(x['blocking'] for x in v['deltas'])
assert v['independent_from_formalizer'] and v['independent_from_decoder']
assert sr['reviewer']=='/root/source_final96' and sr['independently_owned_whole_module_review'] and sr['independently_owned_exposition_review']
assert srev['primary_read_before_current_implementation_exposition_decoder'] and not srev['prior_final_semantic_verdict_read'] and not srev['prior_final_semantic_slots_read'] and not srev['prior_final_deltas_or_repairs_used'] and not srev['source_graph_self_topology_validation']
rp=load(B/'reviewer-packet104.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
dec=R/'runs/semantic-roundtrip/anonymous104/decoder-native';dm=load(dec/'manifest.json');dr=load(dec/'reconstruction.json');run=load(dec/'decoder-run.json');dp=load(dec.parent/'input.json');rec=audit['reconstruction']
for x in dm['artifacts']:assert info(x['path'])['raw_sha256']==x['sha256_raw'] and info(x['path'])['bytes']==x['bytes']
assert len(run['input_artifacts'])==1 and info(dec.parent/'input.json')['raw_sha256']==run['input_artifacts'][0]['sha256_raw']
packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==run['canonical_supplied_packet_sha256']==rec['decoder_packet_sha256']
assert info(dec/'decoder-run.json')['raw_sha256']==rec['decoder_run_sha256']==sr['decoder_run']['raw_sha256']
assert info(dec/'reconstruction.json')['raw_sha256']==rec['native_named_payload_sha256'] and rec['native_semantic_slots']==dr
assert all(not run[k] for k in ['source_text_visible','source_identity_visible','prior_audit_visible','repair_proposals_visible']) and not rec['source_text_visible']
assert sha(dp['lean']['statement'].encode())==rec['lean_statement_sha256']
assert rec['text']==(dec/'reconstruction.txt').read_text(encoding='utf8') and sha(rec['text'].encode())==rec['text_sha256']
assert sr['decoder_visibility_flags']=={k:False for k in ['source_text_visible','source_identity_visible','prior_audit_visible','repair_proposals_visible']}
assert cov['effective_counts']==dict(source_regions=21,nodes=55,edges=96,direct_public_parents=4,production_lines=230,exposition_regions=8)
assert not cov['topology_self_validation']
topo=load(PRE/'independent-header-math104/source-topology-admission104.native.json');graph=load(PRE/'independent-header-math104/topology-binding-check104.native.json')['effective_graph']
assert topo['decision']=='ACCEPT_BASE_PLUS_104_DELTA_TOPOLOGY_AND_BOUNDED_COVERAGE' and topo['reviewer']!=sr['reviewer']
assert {x['id'] for x in cov['node_dispositions']}==set(graph['nodes']) and {(x['source'],x['target']) for x in cov['edge_dispositions']}=={tuple(e) for e in graph['edges']}
primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
plines=primary.splitlines(keepends=True)
for x in cov['source_regions']:assert sha(b''.join(plines[x['line_start']-1:x['line_end']]))==x['raw_sha256']==sha(primary[x['byte_start']:x['byte_end_exclusive']]) and x['fresh_RAW_verified']
covered=set();mlines=(R/M).read_bytes().splitlines(keepends=True)
for x in cov['all_production_regions']:
 assert sha(b''.join(mlines[x['line_start']-1:x['line_end']]))==x['raw_sha256'];covered.update(range(x['line_start'],x['line_end']+1))
assert covered==set(range(1,231))
assert expo['verdict']=='ACCEPT_BOUNDED_EIGHT_STEP_AUTHORED_EXPOSITION' and expo['lesson']['raw_sha256']==info(L)['raw_sha256']
lesson=load(L)['units'][0];assert len(lesson['steps'])==len(expo['steps'])==8
for step,claim in zip(lesson['steps'],expo['steps']):
 region=claim['source_span'];literal=b''.join(mlines[region['line_start']-1:region['line_end']]).decode().replace('\r\n','\n');assert step['lean']==literal and step['formula']==claim['formula'] and sha(step['text'].encode())==claim['text_UTF8_sha256'];assert claim['judgment']=='accepted' and sha(literal.encode())==claim['display_code_RAW_sha256']
repair=B/'exposition-index-repair104';proposal=load(repair/'proposal104.json');decision=load(repair/'independent-review/decision104.native.json');assert decision['decision']=='ACCEPT_AUTHORED_NOTATION_CLARIFICATION_ONLY' and decision['reviewer']=='/root/exact_verifier96'
oldlesson=load(repair/'0.before.exactraw.snapshot.json');assert oldlesson['units'][0]['steps'][0]['text']==proposal['old'];oldlesson['units'][0]['steps'][0]['text']=proposal['new'];assert oldlesson==load(L)
assert expo['repair']['applied_exactly'] and not expo['repair']['source_theorem_repair'] and not expo['repair']['Lean_or_decoder_change']
whole=load(W/'whole-math-decision104.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL' and whole['production']==info(M)
prep=load(W/'prepared-inputs104.native.json')
for x in prep['inputs']:assert info(x['path'])==x
assert prep['literal_header_seal_privateProp_equal'] and not prep['imports_target_module']
parents=sorted('AutoSamplingTheory.ExampleCases.ProximalBPS.'+x['declaration'] for x in whole['genuine_direct_parents']);assert len(parents)==4
cell=load(CELL);current=load(P);assert sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==sorted(x['declaration'] for x in cov['actual_parent_discharge'])==parents
assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'] and cell['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage104.native.json')
assert 'accepted compiled' in cell['source_proof_coverage']['coverage_status']
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='b39b7a5ce95ad06964dc2d1c09102ea21fc7c5e80653a9145e17798fbbb945f9'
pub.check_advance([D],reviewed=True)
oldp=B/'publication-before-compiled-coverage104.exactraw.snapshot.json';old=load(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
old['items'][0]['source_proof_coverage']=item['source_proof_coverage'];assert old==current
oldcell=load(B/'cell-before-compiled-coverage104.exactraw.snapshot.json');oldcell['source_proof_coverage']=cell['source_proof_coverage'];assert oldcell==cell
assert cell['status']=='proved_locally' and cell['evidence']['owner']=='companion_root_20261005' and cell['target_declarations']==[D]
assert cell['cell_id']=='ASTIS-SW-PBPS-actual-normalized-endpoint-sector'
save('metadata-transfer104.json',dict(status='PASS',verified_commit=C,publication_binding_sha256=bd,reviewed_publication=info(oldp),only_publication_and_cell_coverage_changed_after_review=True,notation_repair=info(repair/'independent-review/decision104.native.json'),notation_change_exactly_one_text_field=True))
save('source-acceptance104.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review104.native.json'),native_run=info(S/'source-review-run104.native.json'),closed_manifest=info(S/'closed-RAW-final-source104.native.json'),canonical_copy_exact_except_evidence_path_with_prose_retained=True,seven_slots_exact=True,all21source_regions_RAW_verified=True,effective55nodes96edges_disposed=True,whole230lines_eight_exposition_regions=True,exact_four_parents=parents,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'decoder-run.json')['raw_sha256'],reviewer_packet_sha256=ph,publication_binding_sha256=bd,accepted_exposition_notation_repair_only=True,canonical_compiled_coverage_pointer_current=True,topology_independently_validated=True))
print('PASS_SOURCE_DECODER_REPAIR_COVERAGE')
