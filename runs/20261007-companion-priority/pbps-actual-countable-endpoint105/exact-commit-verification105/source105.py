from context105 import *
import gzip
assert head()==C
S=B/'final-source105';W=B/'independent-whole-math105'
audit=load(A);v=load(S/'source-review105.native.json');sr=load(S/'source-review-run105.native.json');cov=load(S/'compiled-source-coverage105.native.json');expo=load(S/'exposition105.native.json')
assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review105.native.json');assert audit['source_review']==srev
assert info(S/'source-review-run105.native.json')['raw_sha256']==v['review_run_sha256']==srev['review_run_sha256']
assert len(v['semantic_slots'])==7 and not v['repairs'] and not any(x['blocking'] for x in v['deltas'])
assert v['independent_from_formalizer'] and v['independent_from_decoder'] and sr['reviewer']=='/root/source_final96'
assert srev['source_primary_read_before_current_Lean_and_decoder'] and srev['independently_owned_whole_module_review'] and srev['exposition_reviewed']
assert all(not srev[k] for k in ['prior_semantic_slots_read','prior_deltas_read','prior_verdict_read','prior_source_theorem_repairs_read','topology_self_validation'])
rp=load(B/'reviewer-packet105.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
dec=R/'runs/semantic-roundtrip/anonymous105/decoder-native';dr=load(dec/'reconstruction.json');run=load(dec/'decoder-run.json');dp=load(dec.parent/'input.json');rec=audit['reconstruction']
for p,h in run['output_hashes'].items():assert info(p)['raw_sha256']==h
assert info(dec.parent/'input.json')['raw_sha256']==run['input_sha256']
packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==run['packet_sha256']==rec['decoder_packet_sha256']
assert info(dec/'decoder-run.json')['raw_sha256']==rec['decoder_run_sha256']==sr['decoder_run']['raw_sha256']
assert info(dec/'reconstruction.json')['raw_sha256']==rec['native_named_payload_sha256'] and rec['native_semantic_slots']==dr
assert all(not run[k] for k in ['source_text_visible','source_identity_visible','theorem_number_visible','prior_audit_visible','repair_visible']) and not rec['source_text_visible']
assert sha(dp['lean']['statement'].encode())==rec['lean_statement_sha256']==run['statement_sha256']
assert rec['text']==(dec/'reconstruction.txt').read_text(encoding='utf8') and sha(rec['text'].encode())==rec['text_sha256']
assert cov['effective_counts']==dict(source_regions=21,nodes=60,edges=112,direct_public_parents=4,production_lines=292,exposition_regions=8)
assert not cov['topology_self_validation']
topo=load(PRE/'independent-header-math105/source-topology-admission105.native.json');graph=topo['effective_graph']
assert topo['decision']=='ACCEPT_BASE_PLUS_V2_TOPOLOGY_AND_COVERAGE' and topo['reviewer']!=sr['reviewer']
assert {x['id'] for x in cov['node_dispositions']}==set(graph['nodes'])
assert {(x['source'],x['target']) for x in cov['edge_dispositions']}=={tuple(e) for e in graph['edges']}
primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
plines=primary.splitlines(keepends=True)
for x in cov['source_regions']:assert sha(b''.join(plines[x['line_start']-1:x['line_end']]))==x['raw_sha256']==sha(primary[x['byte_start']:x['byte_end_exclusive']]) and x['fresh_RAW_verified']
covered=set();mlines=(R/M).read_bytes().splitlines(keepends=True)
for x in cov['all_production_regions']:
 assert sha(b''.join(mlines[x['line_start']-1:x['line_end']]))==x['raw_sha256'];covered.update(range(x['line_start'],x['line_end']+1))
assert covered==set(range(1,293))
assert expo['verdict']=='ACCEPT_BOUNDED_EIGHT_STEP_EXPOSITION_ONLY' and expo['lesson']['raw_sha256']==info(L)['raw_sha256']
lesson=load(L)['units'][0];assert len(lesson['steps'])==len(expo['steps'])==8
for step,claim in zip(lesson['steps'],expo['steps']):
 region=claim['source_span'];literal=b''.join(mlines[region['line_start']-1:region['line_end']]).decode().replace('\r\n','\n')
 assert step['lean']==literal and step['formula']==claim['formula'] and step['text']==claim['text'] and claim['accepted'] and sha(literal.encode())==claim['display_LF_RAW_sha256']
repair=B/'exposition-notation-repair105';proposal=load(repair/'proposal105.json');decision=load(repair/'independent-review/decision105.native.json');assert decision['decision']=='ACCEPT_AUTHORED_NOTATION_CLARIFICATION_ONLY' and decision['reviewer']=='/root/exact_verifier96'
oldlesson=load(repair/'lesson.before.exactraw.snapshot');assert oldlesson['units'][0]['steps'][1]['text']==proposal['before'];oldlesson['units'][0]['steps'][1]['text']=proposal['after'];assert oldlesson==load(L)
whole=load(W/'whole-math-decision105.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL' and whole['production']==info(M)
prep=load(W/'prepared-inputs105.native.json')
for x in prep['inputs']:assert info(x['path'])==x
assert prep['literal_header_seal_privateProp_equal'] and not prep['imports_target_module']
def full(s):return ('AutoSamplingTheory.TechnicalLemmas.Probability.' if s.startswith('UnitExponentialProduct.') else 'AutoSamplingTheory.ExampleCases.ProximalBPS.')+s
parents=sorted(full(x['declaration']) for x in whole['genuine_direct_parents']);assert len(parents)==4
cell=load(CELL);current=load(P)
assert sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==sorted(full(x['declaration']) for x in cov['actual_parent_discharge'])==parents
assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'] and cell['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage105.native.json')
assert 'accepted compiled' in cell['source_proof_coverage']['coverage_status'].lower()
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='bfe6a0010aa9d52b30f3725385f03dc310d2ce5d7293078ce4fdce14248fa720'
pub.check_advance([D],reviewed=True)
oldp=B/'publication-before-compiled-coverage105.exactraw.snapshot.json';old=load(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
old['items'][0]['source_proof_coverage']=item['source_proof_coverage'];assert old==current
oldcell=load(B/'cell-before-compiled-coverage105.exactraw.snapshot.json');oldcell['source_proof_coverage']=cell['source_proof_coverage'];assert oldcell==cell
assert cell['status']=='proved_locally' and cell['evidence']['owner']=='companion_root_20261005' and cell['target_declarations']==[D]
assert cell['cell_id']=='ASTIS-SW-PBPS-actual-countable-endpoint-law'
save('metadata-transfer105.json',dict(status='PASS',verified_commit=C,publication_binding_sha256=bd,reviewed_publication=info(oldp),only_publication_and_cell_coverage_changed_after_review=True,notation_repair=info(repair/'independent-review/decision105.native.json'),notation_change_exactly_one_text_field=True))
save('source-acceptance105.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review105.native.json'),native_run=info(S/'source-review-run105.native.json'),closed_manifest=info(S/'closed-RAW-final-source105.native.json'),canonical_copy_exact_except_evidence_path_with_prose_retained=True,seven_slots_exact=True,all21source_regions_RAW_verified=True,effective60nodes112edges_disposed=True,whole292lines_eight_exposition_regions=True,exact_four_parents=parents,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'decoder-run.json')['raw_sha256'],reviewer_packet_sha256=ph,publication_binding_sha256=bd,accepted_exposition_notation_repair_only=True,canonical_compiled_coverage_pointer_current=True,topology_independently_validated=True))
print('PASS_SOURCE_DECODER_REPAIR_COVERAGE')
