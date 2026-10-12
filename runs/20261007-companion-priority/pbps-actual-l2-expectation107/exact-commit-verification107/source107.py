from context107 import *
assert head()==C
S=B/'final-source107';W=B/'independent-whole-math107'
audit=load(A);v=load(S/'source-review107.native.json');sr=load(S/'source-review-run107.native.json');cov=load(S/'compiled-source-coverage107.native.json');expo=load(S/'exposition107.native.json')
assert info(S/'source-review107.native.json')['raw_sha256']=='299fde7f37b714839ea058253d47c4af5a47aaeb7902b676310e033ea4838581'
assert audit['state']==v['source_review']['state']=='accepted' and v['verdict']=='equivalent-after-elaboration'
for k in ['semantic_slots','deltas','verdict','repairs']:assert audit[k]==v[k],k
srev=copy.deepcopy(v['source_review']);srev['native_evidence_summary']=srev['evidence'];srev['evidence']=rel(S/'source-review107.native.json');assert audit['source_review']==srev
assert info(S/'source-review-run107.native.json')['raw_sha256']==v['review_run_sha256']==srev['review_run_sha256']
assert len(v['semantic_slots'])==7 and not v['repairs'] and not any(x['blocking'] for x in v['deltas']) and not v['blocking_findings']
assert srev['independent_from_formalizer'] and srev['independent_from_decoder'] and sr['reviewer']=='/root/source_final96'
assert sr['primary_before_current_publication_decoder'] and sr['independently_owned_whole_module_review'] and sr['no_topology_self_validation']
assert not sr['prior_semantic_verdict_slots_deltas_or_repairs_used']
assert all(not srev[k] for k in ['prior_semantic_slots_read','prior_deltas_read','prior_verdict_read','prior_repairs_read'])
assert srev['private_helpers_reviewed']
rp=load(B/'reviewer-packet107.json');ph=rp.pop('packet_sha256');assert sha(canon(rp))==ph==v['reviewer_packet_sha256']==sr['reviewer_packet_sha256']
dec=R/'runs/semantic-roundtrip/anonymous107/decoder-native';dr=load(dec/'decoder.json');run=load(dec/'manifest.json');dp=load(dec.parent/'input.json');rec=audit['reconstruction']
for p,row in run['outputs'].items():assert info(dec/p)['raw_sha256']==row['sha256'] and info(dec/p)['bytes']==row['bytes']
assert info(dec.parent/'input.json')['raw_sha256']==run['input_raw_sha256']==dr['input_raw_sha256']
packet_hash=dp.pop('packet_sha256');assert sha(canon(dp))==packet_hash==run['packet_canonical_sha256']==rec['decoder_packet_sha256']==dr['packet_canonical_sha256']
assert info(dec/'manifest.json')['raw_sha256']==rec['decoder_run_sha256']==sr['decoder_manifest']['raw_sha256']
assert info(dec/'decoder.json')['raw_sha256']==rec['native_named_payload_sha256'] and rec['native_semantic_slots']==dr
assert not any(run['visibility'].values()) and not rec['source_text_visible'] and len(run['mathematical_inputs_read'])==1
assert sha(dp['lean']['statement'].encode())==rec['lean_statement_sha256']==dr['statement_sha256']
assert rec['text']==(dec/'reconstruction.txt').read_text(encoding='utf8')==dr['reconstructed_theorem_text'] and sha(rec['text'].encode())==rec['text_sha256']==dr['reconstructed_text_sha256']
assert sha('\n'.join(dr[k] for k in ['agent_identity','input_raw_sha256','packet_canonical_sha256','reconstructed_text_sha256']).encode())==dr['decoder_run_sha256']==run['decoder_run_sha256']
assert cov['effective_counts']==dict(source_regions=21,nodes=85,edges=161,actual_parents=3,production_lines=345,exposition_regions=10,statement_lets=40) and not cov['topology_self_validation']
overlay=load(B/'source-route107/quotient-identification107.proposal.native.json');admission=load(B/'independent-route107/route-admission107.native.json');effective=load(B/'source-graph107.effective.json');original=load(overlay['base_graph']['path'])
assert admission['decision']=='ACCEPT_EXACT_QUOTIENT_IDENTIFICATION_OR_OVERLAY' and admission['reviewer']!=overlay['creator']==sr['reviewer']
assert info(B/'source-route107/quotient-identification107.proposal.native.json')['raw_sha256']==admission['proposal_raw_sha256']
assert overlay['new_nodes']==[] and overlay['new_edges']==[['L2-IDENTIFY107','AE-REP107']]
expected=copy.deepcopy(original)
expected['edges'] += [dict(source=a,target=b,scope='current107-selected-quotient-consequence') for a,b in overlay['new_edges']]
for n in expected['nodes']:
 if n['id']=='AE-REP107':
  n['meaning']=overlay['refined_node_meaning']['meaning'];n['old_mechanism_preserved_in']=overlay['refined_node_meaning']['old_mechanism_preserved_in']
oldgroups=[g for g in expected['AND_groups'] if g['target']=='AE-REP107'];expected['AND_groups']=[g for g in expected['AND_groups'] if g['target']!='AE-REP107']
for key in ['nodes','edges','AND_groups']:assert effective[key]==expected[key],key
assert effective['superseded_single_route_AND_groups']==oldgroups and effective['AND_route_alternatives']==overlay['AND_route_alternatives'] and effective['OR_semantics']==overlay['OR_semantics']
assert effective['independent_topology_admission'] and effective['selected_route']=='universal-quotient-identification107'
N={x['id'] for x in effective['nodes']};E={(x['source'],x['target']) for x in effective['edges']}
assert len(N)==85 and len(E)==161 and {x['id'] for x in cov['node_dispositions']}==N and {(x['source'],x['target']) for x in cov['edge_dispositions']}==E
primary=(R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html').read_bytes();assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
plines=primary.splitlines(keepends=True)
for x in cov['source_regions']:assert sha(b''.join(plines[x['line_start']-1:x['line_end']]))==x['raw_sha256']==sha(primary[x['byte_start']:x['byte_end_exclusive']])
covered=set();mlines=(R/M).read_bytes().splitlines(keepends=True)
for x in cov['all_production_regions']:
 assert sha(b''.join(mlines[x['line_start']-1:x['line_end']]))==x['raw_sha256'];covered.update(range(x['line_start'],x['line_end']+1))
assert covered==set(range(1,346))
assert expo['exposition_verdict']=='ACCEPT_BOUNDED_TEN_STEP_EXPOSITION' and expo['lesson']['raw_sha256']==info(L)['raw_sha256'] and not expo['repairs'] and not expo['blocking_defects']
lesson=load(L)['units'][0];assert len(lesson['steps'])==len(expo['steps'])==10
for step,claim in zip(lesson['steps'],expo['steps']):
 region=claim['source_span'];literal=b''.join(mlines[region['line_start']-1:region['line_end']]);assert sha(literal)==region['raw_sha256']==claim['displayed_UTF8_code_raw_sha256']
 assert step['lean']==literal.decode() and step['formula']==claim['formula'] and step['title']==claim['title'] and claim['verdict']=='accepted'
whole=load(W/'whole-math-decision107.native.json');assert whole['decision']=='ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL' and whole['production']==info(M)
prep=load(W/'prepared-inputs107.native.json')
for x in prep['inputs']:assert info(x['path'])==x
assert prep['literal_header_seal_privateProp_equal'] and not prep['imports_target_module']
def full(s):return ('AutoSamplingTheory.TechnicalLemmas.Probability.' if s.startswith('UnitExponentialProduct.') else 'AutoSamplingTheory.ExampleCases.ProximalBPS.')+s
parents=sorted(full(x['declaration']) for x in whole['genuine_direct_parents']);assert len(parents)==3
cell=load(CELL);current=load(P)
assert sorted(cell['parents'])==sorted(cell['reuse_plan']['reused_declarations'])==sorted(x['declaration'] for x in cov['actual_parent_discharge'])==parents
assert current['items'][0]['source_proof_coverage']==cell['source_proof_coverage'] and cell['source_proof_coverage']['coverage_report']==rel(S/'compiled-source-coverage107.native.json')
assert 'accepted compiled' in cell['source_proof_coverage']['coverage_status'].lower()
sys.path[:0]=[str(R),str(R/'tools')]
from tools import astis_publication as pub
item=current['items'][0];bd=pub.binding_digest(item,item['bindings'][0]);assert bd==audit['publication_binding_sha256']==v['publication_binding_sha256']=='c479ce9043d6693b5669974f1d1ff1f9eab6aba210ddb4621c00bf5c0b934740'
pub.check_advance([D],reviewed=True)
oldp=B/'publication-before-compiled-coverage107.exactraw.snapshot.json';old=load(oldp);assert info(oldp)['raw_sha256']==expo['publication']['raw_sha256'];assert pub.binding_digest(old['items'][0],old['items'][0]['bindings'][0])==bd
old['items'][0]['source_proof_coverage']=item['source_proof_coverage'];assert old==current
oldcell=load(B/'cell-before-compiled-coverage107.exactraw.snapshot.json');oldcell['source_proof_coverage']=cell['source_proof_coverage'];assert oldcell==cell
assert cell['status']=='proved_locally' and cell['evidence']['owner']=='companion_root_20261005' and cell['target_declarations']==[D] and cell['cell_id']=='ASTIS-SW-PBPS-actual-l2-expectation'
save('metadata-transfer107.json',dict(status='PASS',verified_commit=C,publication_binding_sha256=bd,reviewed_publication=info(oldp),only_publication_and_cell_coverage_changed_after_review=True,route_overlay=info(B/'independent-route107/route-admission107.native.json'),original_seal_and_graph_unchanged=True))
save('source-acceptance107.native.json',dict(status='PASS',verified_commit=C,native_verdict=info(S/'source-review107.native.json'),native_run=info(S/'source-review-run107.native.json'),closed_manifest=info(S/'closed-RAW-final-source107.native.json'),canonical_copy_exact_except_evidence_path_with_prose_retained=True,seven_slots_exact=True,all21source_regions_RAW_verified=True,effective85nodes161edges_disposed=True,whole345lines_ten_exposition_regions=True,exact_three_parents=parents,decoder_packet_sha256=packet_hash,decoder_run_sha256=info(dec/'manifest.json')['raw_sha256'],reviewer_packet_sha256=ph,publication_binding_sha256=bd,no_statement_or_exposition_repairs=True,canonical_compiled_coverage_pointer_current=True,topology_and_selected_route_independently_validated=True))
print('PASS_SOURCE_DECODER_ROUTE_COVERAGE')
