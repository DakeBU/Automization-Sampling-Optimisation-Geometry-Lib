"""Refresh only the owned PL cell from separately frozen actual evidence."""
from pathlib import Path
import json
import hashlib

R = Path('/Users/zhouhuanjian/ASTIS-GC')
E = R / 'research-wiki/technical-lemmas/matrix-bernstein-mgf-semantic-evidence'
C = R / 'research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-MGF.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
fixed = {
    'AutoSamplingTheory/TechnicalLemmas/Probability/MatrixBernsteinMgf.lean': 'b46bb5a3eabbcadf31fee93d48c1fbabf9b5b42cf717a8a17c8c8cfdd210a3f3',
    'Tests/GaussianComplexityBernsteinWeightedMgf.lean': '42f372143ffe52e4372271d09fbc6b67391739f2fe2a5fbfffe6cd9fa586936e',
    'website/content/declaration_lessons/huanjian-matrix-bernstein-mgf.json': 'd88b96ad5397be27a9f234a6b3ac993a236267591dd4c922c7ba7aa1915f28c0',
    'website/content/publications/huanjian-matrix-bernstein-mgf.json': '51580fc5033dcfb049ab5e1bc8754f42666f27bdedd65eda60029f40b2d96e1c',
}
assert all(sha(R / p) == h for p, h in fixed.items())
reader = json.loads((E / 'reader-current-acceptance.v1.json').read_text())
assert reader['status'] == 'ACCEPTED_ISOLATED_READER_ONLY'
assert reader['actual_v4']['exit_code'] == 0 and reader['actual_v4']['failures'] == 0
assert reader['independent_visual_review']['accepted'] is True
pl = json.loads((E / 'PROVED_LOCAL-evidence.full.json').read_text())
cell = json.loads(C.read_text())
assert cell['status'] == 'proved_locally'
t = cell['consumer_scope']['current_candidate']['name']
cell['consumer_scope']['current_candidate']['state'] = 'ACTUAL_PRIVATE_COMPILED; INDEPENDENT_NATIVE_SOURCE_AND_ISOLATED_READER_ACCEPTED; NORMAL_PROOF_V_PENDING'
cell['reuse_plan']['known_consumers'] = [t]
cell['reuse_plan']['planned_consumers'] = [cell['consumer_scope']['second_realistic_consumer']['description']]
cell['reuse_plan']['actual_parent_calls_pending'] = False
cell['reuse_plan']['actual_parent_witness'] = 'research-wiki/technical-lemmas/matrix-bernstein-mgf-semantic-evidence/native-originals/weighted_mgf_native_8c2d/actual-canonical-parent-witnesses.v1.json'
cell['reader_contract']['status'] = 'Authored-v2 source/whole-code/seven-slot review and actual isolated reader-v2/browser-v4 accepted independently. Production/shared integration and post-merge purification remain held.'
graph = cell['graph_contribution']
graph['visual_review'] = 'Actual desktop/mobile existing-UI zoom, detail inspector, source-index and parent navigation accepted in the bounded fixture. Default-fit labels are small; zoomed SVG labels can be truncated, so complete identifiers are read in the detail inspector. No global graph or production acceptance.'
graph['functor_view_semantics'] = 'Typed conceptual mechanism normally published and independently validated; global stabilization held. No formal transport, theorem equivalence or certified functor.'
cell['source_detail_audit']['gap'] = 'The bounded real normalized single-matrix MGF and its original-Gaussian fixed +cos consumer now have independently reviewed source expansion and compiled proof. The source paper does not name Tropp here; this is explicitly matched external background. Independent-sum/Lieb/master-tail, full Bernstein/C6 and main lower bounds remain outside this cell.'
coverage = cell['source_proof_coverage']
coverage['historical_preproof_source_gap_ids'] = coverage.get('historical_preproof_source_gap_ids', coverage['source_gaps'])
coverage['source_gaps'] = []
coverage['status'] = 'Bounded P/T source obligations discharged by actual code, source-first whole-module review, blind decoding and seven-slot review; no full sum-tail/C6 closure.'
coverage['discharge_evidence'] = cell['evidence']['independent_source_review']
cell['proof_digestion']['bookkeeping'] = ['Actual Bochner integral algebra and centering in P; actual unconditional Gaussian row/cutoff/radius/regularity, signed-cosine norm cap and normalization in private T. All are implementation proof components, not extra T hypotheses.']
cell['proof_digestion']['status'] = 'Actual P/T proof inventories and canonical parent calls independently checked; compiler-generated support and private T receive no extra public lemma credit. Post-merge purification remains separate.'
ev = cell['evidence']
ev['focused_checks'] = pl['focused_checks']
ev['new_target_proof'] = ev['ROOT_actual_math']
ev['independent_semantic'] = 'P and private T equivalent-after-elaboration with no deltas/repairs; exact independent originals retained.'
ev['independent_native'] = 'Actual immutable4869 type/value/kernel and literal P/T/q0 probes accepted; no retroactive build claim at metadata or public export identities.'
ev['independent_reader'] = 'research-wiki/technical-lemmas/matrix-bernstein-mgf-semantic-evidence/reader-current-acceptance.v1.json'
ev['actual_isolated_reader'] = reader
ev['independent_source_review']['runtime_review'] = ev['independent_reader']
learn = cell['learning_contract']
learn['salvage']['reason'] = 'Original source-locator repair, failed report-writer, original renderer defects, candidate highlighter anchor loss and LF measurement failure all remain immutable originals. Minimal separately reviewed repairs changed no mathematical statement, source binder, definition, proof or raw source byte.'
learn['parallelism']['expected_information_gain'] = 'One ROOT mathematical proof worker; independent source graph, distinct topology challenge, source-blind decoder, source-first whole-code/reader reviewer, native verifier and bounded publication-safety roles addressed distinct uncertainty.'
learn['reader_backpressure']['assumptions_preserved'] = True
learn['reader_backpressure']['boundary_preserved'] = True
cell['conceptual_mirror_audit']['independent_validation'] = 'Actual normal raw-to-validated Discovery by mgf_fresh_source_5b7e; global integration held.'
cell['phase_snapshot'] = 'Normal PROVED_LOCAL retained. P/T code/native/source/seven-slot and actual isolated reader accepted; independent normal proof VERIFIED not yet executed. Original shared stabilization owner held; no production/global integration or whole-Goal completion.'
C.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n')
assert all(sha(R / p) == h for p, h in fixed.items())
print(json.dumps({'cell': str(C.relative_to(R)), 'status': cell['status'], 'normal_V_calls_by_ROOT': 0, 'four_math_metadata_files_byte_unchanged': True}, ensure_ascii=False))
