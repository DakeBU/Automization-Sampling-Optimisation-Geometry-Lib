from pathlib import Path
import datetime, hashlib, json, os

out=Path(__file__).resolve().parent
assert not (out/'CLOSED_LAST.json').exists()
def sha(b): return hashlib.sha256(b).hexdigest()
def get(n): return json.loads((out/n).read_text(encoding='utf-8'))
source_freeze_hash='b543f6543f3d6c8e22bea1986427c41e9b10a45e0f732f143c59c4d75a3f771f'
packet_hash='1a72e794cd4e22dd03762b4a58d82419d1c49372cd8252f8611ba8335b37580d'
binding='ef7ddf32173166e15704713b04a186c1ae19f324f9d555083a416ed5af930c11'
module_hash='1f1ebc187676e0481247bc2f58ec0bf94b2fc6f02a563b87009a0fe7bfb4910c'
assert sha((out/'source-only.freeze76.json').read_bytes())==source_freeze_hash
intake=get('candidate-intake76.json')
assert len(intake['readable_inputs'])==15 and len(intake['hash_only_inputs'])==3
pin_results=[]
for category in ['readable_inputs','hash_only_inputs']:
    for pin in intake[category]:
        # Hash-only canonical files are never decoded or copied.
        b=Path(pin['path']).read_bytes()
        assert len(b)==pin['RAW_bytes'] and sha(b)==pin['RAW_sha256']
        assert sha(b.replace(b'\r\n',b'\n'))==pin['LF_sha256']
        if category=='readable_inputs':
            assert b==(out/pin['own_raw_copy']).read_bytes()
        else:
            assert pin['content_decoded'] is False and pin['content_inspected'] is False
        pin_results.append({'path':pin['path'],'category':category,'RAW_sha256':sha(b),'status':'MATCH','content_decoded_in_this_validation':False})
packet=get('candidate-input01.raw')
assert sha(json.dumps({k:v for k,v in packet.items() if k!='packet_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())==packet_hash
report=get('compiled-source-review76.json')
logical_bytes=(out/'review-logical-run76.json').read_bytes()
assert logical_bytes==(out/'review-logical-run76.raw.json').read_bytes()
logical=get('review-logical-run76.json')
assert sha(logical_bytes)==report['review_run_sha256']=='f2c1461c58bf015a603c4cd94be6f6aec0da6745ae5f8163b8389dec257400f7'
assert report['packet_sha256']==logical['packet_sha256']==packet_hash
assert report['publication_binding_sha256']==logical['publication_binding_sha256']==binding
assert report['reviewer']==logical['reviewer']=='/root/fresh_source76'
assert logical['reviewer'] not in [logical['formalizer'],logical['decoder']]
assert not logical['prior_verdicts_or_other_reviewer_outcomes_seen']
assert not logical['canonical_audit_cell_publication_contents_seen']
assert not logical['hash_only_pins_used_as_content']
assert not logical['canonical_or_ledger_writes']
expected_slots={'objects','domains','quantifiers','assumptions','conclusion','scopes','constant_dependencies'}
for export in [report['audit_fields'],report['source_review']]:
    assert export['state']=='accepted' and export['verdict']=='equivalent-after-elaboration'
    assert export['review_run_sha256']==sha(logical_bytes)
    assert export['reviewer_packet_sha256']==packet_hash and export['publication_binding_sha256']==binding
    assert export['independent_from_formalizer'] and export['independent_from_decoder']
    assert set(export['semantic_slots'])==expected_slots
    assert all(set(v)=={'original','reconstructed','relation','evidence'} and all(v.values()) and v['relation']!='not-audited' for v in export['semantic_slots'].values())
    assert export['repairs']==[] and len(export['deltas'])==4
assert report['source_review']['blocking_deltas']==logical['blocking_deltas']==[]
assert report['source_review']['no_blocking_delta']
assert report['source_review']['no_PROVED_LOCAL_VERIFIED_Goal_transition'] and logical['no_PROVED_LOCAL_VERIFIED_Goal_transition']
assert len(logical['open_truth_boundary'])==11
assert report['typed_provenance_notes']==logical['provenance_notes']
assert report['typed_provenance_notes'][0]['type']=='auxiliary-coordinate-mismatch'
assert report['typed_provenance_notes'][0]['blocking_for_semantics'] is False
checks=get('candidate-checks76.json')
assert checks['neutral_stale_coordinate_count']==27
header=(out/'candidate-input05.raw').read_bytes()
neutral=get('candidate-input06.raw')
literals={x['id']:x.get('header_literal',x.get('literal','')).encode() for g in ['callers','literal_definitions','conclusion_groups'] for x in neutral[g]}
assert len(checks['neutral_binder_fresh_coordinates'])==27
for x in checks['neutral_binder_fresh_coordinates']:
    a,b=x['current_expanded_header_RAW_range']
    assert header[a:b]==literals[x['id']]
    assert x['literal_matches_current_header'] and not x['provided_range_matches_current_header']
module=(out/'candidate-input03.raw').read_bytes()
assert sha(module)==module_hash and module==(out/'candidate-input04.raw').read_bytes()
lines=module.splitlines(keepends=True)
assert len(lines)==412
assert packet['candidate_publication_context']['current_lean_module'].encode()==module
steps=report['ten_BODY_and_formula_step_reviews']
assert steps==logical['ten_BODY_and_formula_step_reviews'] and len(steps)==10
previous=192
for step,lesson in zip(steps,packet['candidate_publication_context']['lesson']['steps']):
    region=step['BODY_region']; a,b=region['start_line'],region['end_line']
    assert a==previous+1 and region==lesson['lean_source_region']
    raw=b''.join(lines[a-1:b])
    assert raw==lesson['lean'].encode() and sha(raw)==region['exact_code_raw_sha256']
    assert step['text']==lesson['text'] and step['formula']==lesson['formula']
    assert step['state']=='accepted' and step['exact_contiguous_BODY_match']
    previous=b
assert previous==409
covered=set()
for region in report['whole_module_coverage']:
    assert region['status']=='reviewed'
    covered.update(range(region['start_line'],region['end_line']+1))
assert all(n in covered or not raw.strip() for n,raw in enumerate(lines,1))
source=get('source-coverage76.json'); current=get('compiled-source-coverage76.json')
assert current['counts']==source['counts']
assert len(current['inventory'])==131
assert sum(x['disposition']=='NODE' for x in current['inventory'])==44
assert sum(x['disposition']=='EXCLUDED' for x in current['inventory'])==87
for key,count in [('inventory',131),('subclaim_inventory',9),('external_citation_inventory',12)]:
    assert len(current[key])==len(source[key])==count
    for before,after in zip(source[key],current[key]):
        assert all(after[k]==v for k,v in before.items())
    if key!='external_citation_inventory':
        assert all('compiled76_projection' in x for x in current[key])
assert len(current['source_gaps'])==2
assert all(x['state'].startswith('discharged-by-actual') for x in current['source_gaps'])
assert len(current['open_optional_subclaims'])==1
assert current['open_optional_subclaims'][0]['compiled76_projection']['status']=='OPEN_OPTIONAL_NOT_CLAIMED'
cell=get('canonical-cell-source-proof-coverage76.json'); pub=get('canonical-publication-source-proof-coverage76.json')
assert cell['source_proof_coverage']==pub['source_proof_coverage']
for artifact,target in [(cell,'cell'),(pub,'publication')]:
    assert artifact['projection_target']==target and not artifact['canonical_write_performed']
    cp=artifact['source_proof_coverage']
    for key in ['inventory','subclaim_inventory','external_citation_inventory','source_gaps']:
        assert cp[key]==current[key]
    assert cp['reviewed_nodes']==[x['id'] for x in current['inventory'] if x['disposition']=='NODE']
    assert cp['excluded_with_reason']==[{'id':x['id'],'reason':x['reason']} for x in current['inventory'] if x['disposition']=='EXCLUDED']
    assert cp['future_scope_status']=='OPEN' and cp['no_whole_Proposition3_1_credit'] and cp['no_whole_paper_or_Goal_credit']
    assert not cp['other_prospective_graph_seen'] and cp['counts_are_coverage_not_progress_metrics']
topology=get('compiled-source-topology76.json'); original=get('source-proof-graph76.json')
assert topology['nodes']==original['nodes'] and topology['hyperedges']==original['hyperedges']
assert not topology['comparison_to_other_prospective_maps']['other_prospective_graph_read']
assert not topology['comparison_to_other_prospective_maps']['other_prospective_counts_used']
assert sha((out/'compiled-source-coverage76.json').read_bytes())==logical['source_coverage_artifact_sha256']
assert sha((out/'compiled-source-topology76.json').read_bytes())==logical['source_topology_artifact_sha256']
receipts=[]
for path in sorted(out.rglob('*.foreground-exit.json')):
    receipt=json.loads(path.read_text(encoding='utf-8'))
    for stream in ['stdout','stderr']:
        assert sha((path.parent/receipt[stream+'_file']).read_bytes())==receipt[stream+'_sha256']
    receipts.append({'file':path.relative_to(out).as_posix(),'PID':receipt.get('actual_foreground_PID',receipt.get('writer_pid')),'exit_code':receipt['exit_code'],'native_stdout_stderr_hashes':'MATCH'})
for name,pid in [('write_source_freeze76.foreground-exit.json',31828),('write_compiled_review76.foreground-exit.json',46836),('finalize_compiled_review76.foreground-exit.json',3964)]:
    receipt=get(name)
    assert receipt['writer_pid']==pid and receipt['exit_code']==0 and receipt['foreground']
assert report['writer_pid']==3964 and report['substantive_author_writer_pid']==46836
direct=get('direct-review76.foreground-exit.json')
assert direct['actual_foreground_PID']==40920 and direct['exit_code']==0 and direct['Popen_wait_used']
assert direct==logical['direct_focused_Lean_and_axiom_evidence']
assert direct['source_module_raw_sha256']==module_hash
probe=(out/'direct-review-probe76.lean').read_bytes()
assert probe.startswith(module) and sha(probe)==direct['probe_raw_sha256']
assert logical['axioms']==checks['axioms']==['propext','Classical.choice','Quot.sound']
assert all(x in (out/'direct-review76.stdout.raw').read_text(encoding='utf-8') for x in ['depends on axioms: [propext,','Classical.choice,','Quot.sound]'])
assert checks['fake_closure_scan']=='PASS_CURRENT_MODULE'
result={'status':'PASS_NATIVE_COMPILED_SOURCE_REVIEW_INTEGRITY','validator_PID':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'state':'accepted','verdict':report['verdict'],'reviewer':report['reviewer'],'packet_sha256':packet_hash,'publication_binding_sha256':binding,'review_run_sha256':sha(logical_bytes),'report_RAW_sha256':sha((out/'compiled-source-review76.json').read_bytes()),'source_first_freeze_sha256':source_freeze_hash,'whole_module_RAW_sha256':module_hash,'whole_module_lines':412,'ten_contiguous_BODY_steps':[193,409],'semantic_slots':7,'inventory_preserved':{'blocks':131,'NODE':44,'EXCLUDED':87,'subclaims':9,'external_citations':12},'two_canonical_projections_equal':True,'optional_finite_sum_status':'OPEN_NOT_CLAIMED','stale_neutral_metadata_status':'27 stale supplied ranges retained; 27 current literal byte coordinates independently recomputed and validated; nonblocking metadata only','pinned_input_rechecks':pin_results,'native_process_receipts':receipts,'preserved_nonzero_exits':[x for x in receipts if x['exit_code']!=0],'substantive_writer_PID_EXIT':[46836,0],'final_native_export_PID_EXIT':[3964,0],'direct_Lean_PID_EXIT':[40920,0],'standard_axioms':logical['axioms'],'no_canonical_or_ledger_writes':True,'future_truth_boundary':logical['open_truth_boundary'],'closing_pending':True}
target=out/'compiled-review-integrity76.json'
assert not target.exists()
target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['pinned_input_rechecks','native_process_receipts','future_truth_boundary']},ensure_ascii=False,indent=2))
